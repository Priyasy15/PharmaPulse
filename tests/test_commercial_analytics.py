"""
Unit tests for PharmaPulse Commercial Analytics and Stated vs Observed Gap Engines.
"""
import pytest
from src.commercial_analytics.prescribing_analyzer import run_prescribing_analytics
from src.commercial_analytics.stated_vs_observed import compute_stated_vs_observed_gap
from src.commercial_analytics.powerbi_exporter import export_powerbi_tables

def test_prescribing_analytics():
    cms_res = run_prescribing_analytics()
    assert cms_res["market_totals"]["total_claims"] > 0
    assert cms_res["market_totals"]["total_gross_drug_cost"] > 0
    assert cms_res["market_totals"]["unique_prescribers"] > 100
    assert len(cms_res["drug_class_summary"]) >= 5
    assert len(cms_res["top_drugs_by_claims"]) == 10
    assert "ENDOCRINOLOGY, DIABETES & METABOLISM" in cms_res["specialty_class_matrix"]


def test_stated_vs_observed_gap():
    gap_res = compute_stated_vs_observed_gap()
    assert len(gap_res["class_comparisons"]) >= 5
    
    glp1_entry = next((c for c in gap_res["class_comparisons"] if c["drug_class"] == "GLP-1 RA"), None)
    assert glp1_entry is not None
    assert glp1_entry["stated_preference_pct"] > glp1_entry["observed_part_d_claims_share_pct"]
    assert glp1_entry["adoption_gap_pct_pts"] > 0
    assert "Suppressed Adoption" in glp1_entry["market_status"]


def test_powerbi_exporter(tmp_path):
    exported = export_powerbi_tables(output_dir=tmp_path)
    assert "Fact_CMS_Prescribing" in exported
    assert "Fact_Survey_Responses" in exported
    assert "Fact_Stated_vs_Observed_Gap" in exported
    assert "Dim_Drug_Product" in exported
    assert "Dim_Prescriber_Specialty" in exported
    assert "Dim_Geography_State" in exported
    assert "Dim_Barrier_Category" in exported
    
    for name, path in exported.items():
        assert path.exists()
        assert path.stat().st_size > 0
