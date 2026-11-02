"""
Unit tests for PharmaPulse Data Cleaning and Preparation Pipelines.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.data_cleaning.clean_cms_data import clean_cms_prescribing_data, create_drug_lookup_dict
from src.data_cleaning.clean_survey_data import clean_survey_data
from src.survey.synthetic_survey_generator import generate_synthetic_survey
from config.settings import CMS_RAW_CSV, SURVEY_RAW_CSV

def test_drug_lookup_dictionary():
    lookup = create_drug_lookup_dict()
    assert "OZEMPIC" in lookup
    assert lookup["OZEMPIC"]["drug_class"] == "GLP-1 RA"
    assert "JARDIANCE" in lookup
    assert lookup["JARDIANCE"]["drug_class"] == "SGLT2 Inhibitor"
    assert "METFORMIN HCL" in lookup
    assert lookup["METFORMIN HCL"]["canonical_generic"] == "METFORMIN HCL"


def test_survey_generation_and_cleaning(tmp_path):
    # Generate test synthetic survey
    test_raw_csv = tmp_path / "test_raw_survey.csv"
    test_clean_csv = tmp_path / "test_clean_survey.csv"

    df_synth = generate_synthetic_survey(sample_size=100, seed=123, inject_missing=True)
    assert len(df_synth) == 100
    assert "Q1_SPECIALTY" in df_synth.columns
    assert df_synth["IS_SYNTHETIC"].all()

    df_synth.to_csv(test_raw_csv, index=False)

    df_clean, report = clean_survey_data(input_path=test_raw_csv, output_path=test_clean_csv)
    assert len(df_clean) == 100
    assert report["remaining_missing_values"] == 0
    assert "Q11_BARRIER_PRIOR_AUTH_TOP_BOX" in df_clean.columns
    assert "COMPOSITE_BARRIER_INDEX" in df_clean.columns
    assert 1.0 <= df_clean["COMPOSITE_BARRIER_INDEX"].mean() <= 5.0


def test_cms_data_cleaning(tmp_path):
    # Create sample dirty CMS data
    dirty_data = pd.DataFrame([
        {
            "PRSCRBR_NPI": 1234567890,
            "PRSCRBR_LAST_ORG_NAME": " Smith ",
            "PRSCRBR_FIRST_NAME": " John ",
            "PRSCRBR_CITY": " Los Angeles ",
            "PRSCRBR_STATE_ABRVTN": "ca",
            "PRSCRBR_TYPE": "Internal Medicine",
            "DRUG_NAME": " ozempic ",
            "GENERIC_NAME": "semaglutide",
            "TOT_CLMS": 50,
            "TOT_30DAY_FILLS": 100,
            "TOT_DRUG_CST": 50000.0,
            "TOT_BENES": 30,
            "YEAR": 2022
        },
        # Duplicate row
        {
            "PRSCRBR_NPI": 1234567890,
            "PRSCRBR_LAST_ORG_NAME": " Smith ",
            "PRSCRBR_FIRST_NAME": " John ",
            "PRSCRBR_CITY": " Los Angeles ",
            "PRSCRBR_STATE_ABRVTN": "ca",
            "PRSCRBR_TYPE": "Internal Medicine",
            "DRUG_NAME": " ozempic ",
            "GENERIC_NAME": "semaglutide",
            "TOT_CLMS": 50,
            "TOT_30DAY_FILLS": 100,
            "TOT_DRUG_CST": 50000.0,
            "TOT_BENES": 30,
            "YEAR": 2022
        }
    ])
    dirty_csv = tmp_path / "dirty_cms.csv"
    cleaned_csv = tmp_path / "cleaned_cms.csv"
    dirty_data.to_csv(dirty_csv, index=False)

    df_clean, stats = clean_cms_prescribing_data(input_path=dirty_csv, output_path=cleaned_csv)
    assert len(df_clean) == 1  # Duplicate removed
    assert stats["duplicates_removed"] == 1
    assert df_clean.iloc[0]["PRSCRBR_STATE_ABRVTN"] == "CA"
    assert df_clean.iloc[0]["DRUG_NAME"] == "OZEMPIC"
    assert df_clean.iloc[0]["DRUG_CLASS"] == "GLP-1 RA"
    assert df_clean.iloc[0]["COST_PER_CLAIM"] == 1000.0
    assert df_clean.iloc[0]["COST_PER_30DAY_FILL"] == 500.0
