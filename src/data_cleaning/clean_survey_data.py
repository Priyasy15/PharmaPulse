"""
PharmaPulse Survey Data Cleaning & Imputation Pipeline
Cleans, handles missing data, encodes metrics, and prepares HCP survey data for analysis.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
from config.settings import SURVEY_RAW_CSV, SURVEY_PROCESSED_CSV

def clean_survey_data(
    input_path: Path = SURVEY_RAW_CSV,
    output_path: Path = SURVEY_PROCESSED_CSV
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans and prepares survey response data:
    1. Audits missing values and imputes non-critical categories using specialty-level modes.
    2. Encodes Top-Box (Likert >= 4) binary indicators for barriers and awareness.
    3. Calculates Composite Barrier Index per respondent.
    4. Categorizes High vs Low patient volume practitioners.
    5. Saves cleaned dataset to CSV.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Raw survey file not found at: {input_path}")

    df = pd.read_csv(input_path)
    initial_rows = len(df)
    missing_audit_before = df.isnull().sum().to_dict()

    # 1. Missing Value Imputation
    # For categorical practice setting and volume bands, impute with mode within same specialty
    impute_cols = ["Q3_PRACTICE_SETTING", "Q4_MONTHLY_T2D_PATIENTS", "Q5_PCT_MEDICARE_PATIENTS"]
    for col in impute_cols:
        if col in df.columns and df[col].isnull().any():
            # Mode by specialty
            for spec in df["Q1_SPECIALTY"].unique():
                spec_mask = df["Q1_SPECIALTY"] == spec
                mode_val = df.loc[spec_mask, col].mode()
                val_to_fill = mode_val[0] if not mode_val.empty else "Not Disclosed"
                df.loc[spec_mask & df[col].isnull(), col] = val_to_fill

    missing_after = int(df.isnull().sum().sum())

    # 2. Likert Top-Box Encodings (Ratings 4 or 5 = 1, else 0)
    likert_cols = [
        "Q9_FAMILIARITY_GLP1",
        "Q10_FAMILIARITY_SGLT2",
        "Q11_BARRIER_PRIOR_AUTH",
        "Q12_BARRIER_OUT_OF_POCKET_COST",
        "Q13_BARRIER_SIDE_EFFECTS",
        "Q14_BARRIER_SUPPLY_SHORTAGES",
        "Q15_BARRIER_PATIENT_NEEDLE_HESITATION",
    ]

    for col in likert_cols:
        df[f"{col}_TOP_BOX"] = (df[col] >= 4).astype(int)

    # 3. Composite Barrier Score (Mean across 5 adoption barrier questions)
    barrier_cols = [
        "Q11_BARRIER_PRIOR_AUTH",
        "Q12_BARRIER_OUT_OF_POCKET_COST",
        "Q13_BARRIER_SIDE_EFFECTS",
        "Q14_BARRIER_SUPPLY_SHORTAGES",
        "Q15_BARRIER_PATIENT_NEEDLE_HESITATION",
    ]
    df["COMPOSITE_BARRIER_INDEX"] = df[barrier_cols].mean(axis=1).round(2)

    # 4. Binary High Volume Indicator (>60 patients/month)
    df["IS_HIGH_VOLUME_PRACTITIONER"] = df["Q4_MONTHLY_T2D_PATIENTS"].isin(["61-100", ">100"]).astype(int)

    # 5. Save Cleaned Data
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    quality_report = {
        "total_respondents": initial_rows,
        "missing_values_imputed": sum(missing_audit_before.values()) - missing_after,
        "remaining_missing_values": missing_after,
        "mean_composite_barrier_index": float(df["COMPOSITE_BARRIER_INDEX"].mean().round(2)),
        "output_path": str(output_path),
    }

    print(f"Survey data cleaned: {len(df)} records. Imputed missing values: {quality_report['missing_values_imputed']}")
    return df, quality_report


if __name__ == "__main__":
    df_cleaned_survey, report = clean_survey_data()
    print("Survey Quality Report:", report)
