"""
PharmaPulse Power BI Star-Schema Exporter
Exports dimension and fact tables as optimized, Power BI-ready CSV files.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from config.settings import (
    POWERBI_EXPORTS_DIR,
    CMS_PROCESSED_CSV,
    SURVEY_PROCESSED_CSV,
    T2D_DRUG_CATALOG,
    PHYSICIAN_SPECIALTIES,
)
from src.commercial_analytics.stated_vs_observed import compute_stated_vs_observed_gap

def export_powerbi_tables(output_dir: Path = POWERBI_EXPORTS_DIR) -> dict:
    """
    Exports clean star-schema CSV tables for direct ingestion into Microsoft Power BI:
    - Fact_CMS_Prescribing
    - Fact_Survey_Responses
    - Fact_Stated_vs_Observed_Gap
    - Dim_Drug_Product
    - Dim_Prescriber_Specialty
    - Dim_Geography_State
    - Dim_Barrier_Category
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    exported_files = {}

    # 1. Fact_CMS_Prescribing
    cms_df = pd.read_csv(CMS_PROCESSED_CSV)
    cms_fact = cms_df[[
        "PRSCRBR_NPI", "PRSCRBR_STATE_ABRVTN", "PRSCRBR_TYPE",
        "CANONICAL_GENERIC", "DRUG_NAME", "DRUG_CLASS",
        "TOT_CLMS", "TOT_30DAY_FILLS", "TOT_DRUG_CST", "TOT_BENES",
        "COST_PER_CLAIM", "COST_PER_30DAY_FILL", "YEAR"
    ]].copy()
    cms_fact_path = output_dir / "Fact_CMS_Prescribing.csv"
    cms_fact.to_csv(cms_fact_path, index=False)
    exported_files["Fact_CMS_Prescribing"] = cms_fact_path

    # 2. Fact_Survey_Responses
    survey_df = pd.read_csv(SURVEY_PROCESSED_CSV)
    survey_fact = survey_df[[
        "RESPONDENT_ID", "Q1_SPECIALTY", "Q2_YEARS_EXPERIENCE", "Q3_PRACTICE_SETTING",
        "Q4_MONTHLY_T2D_PATIENTS", "Q5_PCT_MEDICARE_PATIENTS",
        "Q6_FIRST_LINE_PREFERENCE", "Q7_SECOND_LINE_ASCVD_PREFERENCE", "Q8_SECOND_LINE_CKD_HF_PREFERENCE",
        "Q9_FAMILIARITY_GLP1", "Q10_FAMILIARITY_SGLT2",
        "Q11_BARRIER_PRIOR_AUTH", "Q12_BARRIER_OUT_OF_POCKET_COST", "Q13_BARRIER_SIDE_EFFECTS",
        "Q14_BARRIER_SUPPLY_SHORTAGES", "Q15_BARRIER_PATIENT_NEEDLE_HESITATION",
        "Q16_PRIMARY_PRESCRIBING_DRIVER", "COMPOSITE_BARRIER_INDEX", "IS_HIGH_VOLUME_PRACTITIONER"
    ]].copy()
    survey_fact_path = output_dir / "Fact_Survey_Responses.csv"
    survey_fact.to_csv(survey_fact_path, index=False)
    exported_files["Fact_Survey_Responses"] = survey_fact_path

    # 3. Fact_Stated_vs_Observed_Gap
    gap_data = compute_stated_vs_observed_gap()
    gap_df = pd.DataFrame(gap_data["class_comparisons"])
    gap_fact_path = output_dir / "Fact_Stated_vs_Observed_Gap.csv"
    gap_df.to_csv(gap_fact_path, index=False)
    exported_files["Fact_Stated_vs_Observed_Gap"] = gap_fact_path

    # 4. Dim_Drug_Product
    drug_rows = []
    for gen, meta in T2D_DRUG_CATALOG.items():
        for brand in meta["brand_names"]:
            drug_rows.append({
                "Drug_Key": f"{gen}_{brand}",
                "Brand_Name": brand,
                "Generic_Name": gen,
                "Drug_Class": meta["drug_class"],
                "Administration_Route": meta["route"],
                "Formulary_Tier_Standard": meta["standard_tier"],
                "Is_Newer_Incretin_SGLT2": meta["is_newer_class"],
                "Benchmark_30Day_Cost": meta["avg_30d_cost_benchmark"],
            })
    dim_drug = pd.DataFrame(drug_rows).drop_duplicates(subset=["Brand_Name"])
    dim_drug_path = output_dir / "Dim_Drug_Product.csv"
    dim_drug.to_csv(dim_drug_path, index=False)
    exported_files["Dim_Drug_Product"] = dim_drug_path

    # 5. Dim_Prescriber_Specialty
    dim_specialty = pd.DataFrame([
        {"Specialty_Key": "INTERNAL MEDICINE", "Specialty_Name": "Internal Medicine", "Specialty_Category": "Primary Care", "Prescribing_Tier": "High Volume"},
        {"Specialty_Key": "FAMILY PRACTICE", "Specialty_Name": "Family Practice", "Specialty_Category": "Primary Care", "Prescribing_Tier": "High Volume"},
        {"Specialty_Key": "ENDOCRINOLOGY, DIABETES & METABOLISM", "Specialty_Name": "Endocrinology, Diabetes & Metabolism", "Specialty_Category": "Subspecialty", "Prescribing_Tier": "High Adoption / Guideline Pioneer"},
        {"Specialty_Key": "NURSE PRACTITIONER", "Specialty_Name": "Nurse Practitioner", "Specialty_Category": "Advanced Practice Provider", "Prescribing_Tier": "Growing Frontline"},
    ])
    dim_spec_path = output_dir / "Dim_Prescriber_Specialty.csv"
    dim_specialty.to_csv(dim_spec_path, index=False)
    exported_files["Dim_Prescriber_Specialty"] = dim_spec_path

    # 6. Dim_Geography_State
    state_meta = {
        "CA": ("California", "West"), "TX": ("Texas", "South"), "FL": ("Florida", "South"),
        "NY": ("New York", "Northeast"), "PA": ("Pennsylvania", "Northeast"), "IL": ("Illinois", "Midwest"),
        "OH": ("Ohio", "Midwest"), "NC": ("North Carolina", "South"), "MI": ("Michigan", "Midwest"),
        "GA": ("Georgia", "South"), "NJ": ("New Jersey", "Northeast"), "VA": ("Virginia", "South"),
        "WA": ("Washington", "West"), "AZ": ("Arizona", "West"), "MA": ("Massachusetts", "Northeast"),
        "TN": ("Tennessee", "South"), "IN": ("Indiana", "Midwest"), "MO": ("Missouri", "Midwest"),
        "MD": ("Maryland", "South"), "WI": ("Wisconsin", "Midwest"), "CO": ("Colorado", "West"),
        "MN": ("Minnesota", "Midwest"), "SC": ("South Carolina", "South"), "AL": ("Alabama", "South"),
        "LA": ("Louisiana", "South"), "KY": ("Kentucky", "South"), "OR": ("Oregon", "West"),
        "OK": ("Oklahoma", "South"), "CT": ("Connecticut", "Northeast"), "UT": ("Utah", "West")
    }
    dim_geo = pd.DataFrame([
        {"State_Code": code, "State_Name": name, "Census_Region": reg}
        for code, (name, reg) in state_meta.items()
    ])
    dim_geo_path = output_dir / "Dim_Geography_State.csv"
    dim_geo.to_csv(dim_geo_path, index=False)
    exported_files["Dim_Geography_State"] = dim_geo_path

    # 7. Dim_Barrier_Category
    dim_barrier = pd.DataFrame([
        {"Barrier_Code": "Q11_BARRIER_PRIOR_AUTH", "Barrier_Name": "Prior Authorization & Step Therapy", "Domain": "Administrative / Payer", "Impact_Level": "Critical"},
        {"Barrier_Code": "Q12_BARRIER_OUT_OF_POCKET_COST", "Barrier_Name": "Patient Out-of-Pocket Copay", "Domain": "Affordability / Financial", "Impact_Level": "Critical"},
        {"Barrier_Code": "Q13_BARRIER_SIDE_EFFECTS", "Barrier_Name": "Clinical Side Effects (GI / Mycotic)", "Domain": "Clinical Safety", "Impact_Level": "Moderate"},
        {"Barrier_Code": "Q14_BARRIER_SUPPLY_SHORTAGES", "Barrier_Name": "Supply Shortages & Stockouts", "Domain": "Supply Chain", "Impact_Level": "High"},
        {"Barrier_Code": "Q15_BARRIER_PATIENT_NEEDLE_HESITATION", "Barrier_Name": "Patient Needle Hesitation", "Domain": "Patient Administration", "Impact_Level": "Moderate to High"},
    ])
    dim_barrier_path = output_dir / "Dim_Barrier_Category.csv"
    dim_barrier.to_csv(dim_barrier_path, index=False)
    exported_files["Dim_Barrier_Category"] = dim_barrier_path

    print(f"Power BI Star-Schema CSVs successfully exported to: {output_dir}")
    return exported_files


if __name__ == "__main__":
    export_powerbi_tables()
