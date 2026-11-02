"""
PharmaPulse Configuration and Central Settings
Type 2 Diabetes (T2D) Commercial Insights Platform
"""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"
POWERBI_EXPORTS_DIR = PROCESSED_DATA_DIR / "powerbi_exports"
REPORTS_DIR = PROJECT_ROOT / "reports"
DOCS_DIR = PROJECT_ROOT / "docs"

# Ensure directories exist
for p in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SYNTHETIC_DATA_DIR, POWERBI_EXPORTS_DIR, REPORTS_DIR, DOCS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Random Seed for Reproducibility
RANDOM_SEED = 42

# CMS Medicare Part D Settings
CMS_REPORTING_YEAR = 2022
CMS_DATA_URL_SAMPLE = "https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers"

# T2D Drug Master Catalog (Generic, Brand, Class, Mechanism, Route)
T2D_DRUG_CATALOG = {
    # GLP-1 Receptor Agonists (and dual incretins)
    "SEMAGLUTIDE": {
        "brand_names": ["OZEMPIC", "RYBELSUS", "WEGOVY"],
        "drug_class": "GLP-1 RA",
        "route": "Subcutaneous / Oral",
        "standard_tier": "Tier 3 / Specialty",
        "avg_30d_cost_benchmark": 935.0,
        "is_newer_class": True,
    },
    "DULAGLUTIDE": {
        "brand_names": ["TRULICITY"],
        "drug_class": "GLP-1 RA",
        "route": "Subcutaneous",
        "standard_tier": "Tier 3",
        "avg_30d_cost_benchmark": 880.0,
        "is_newer_class": True,
    },
    "TIRZEPATIDE": {
        "brand_names": ["MOUNJARO", "ZEPBOUND"],
        "drug_class": "GLP-1 / GIP Dual Agonist",
        "route": "Subcutaneous",
        "standard_tier": "Tier 3 / Specialty",
        "avg_30d_cost_benchmark": 1020.0,
        "is_newer_class": True,
    },
    "LIRAGLUTIDE": {
        "brand_names": ["VICTOZA", "SAXENDA"],
        "drug_class": "GLP-1 RA",
        "route": "Subcutaneous",
        "standard_tier": "Tier 3",
        "avg_30d_cost_benchmark": 780.0,
        "is_newer_class": True,
    },
    
    # SGLT2 Inhibitors
    "EMPAGLIFLOZIN": {
        "brand_names": ["JARDIANCE", "SYNJARDY", "TRIJARDY XR"],
        "drug_class": "SGLT2 Inhibitor",
        "route": "Oral",
        "standard_tier": "Tier 2 / Tier 3",
        "avg_30d_cost_benchmark": 590.0,
        "is_newer_class": True,
    },
    "DAPAGLIFLOZIN": {
        "brand_names": ["FARXIGA", "XIGDUO XR"],
        "drug_class": "SGLT2 Inhibitor",
        "route": "Oral",
        "standard_tier": "Tier 2 / Tier 3",
        "avg_30d_cost_benchmark": 575.0,
        "is_newer_class": True,
    },
    "CANAGLIFLOZIN": {
        "brand_names": ["INVOKANA", "INVOKAMET"],
        "drug_class": "SGLT2 Inhibitor",
        "route": "Oral",
        "standard_tier": "Tier 3",
        "avg_30d_cost_benchmark": 550.0,
        "is_newer_class": True,
    },

    # DPP-4 Inhibitors
    "SITAGLIPTIN": {
        "brand_names": ["JANUVIA", "JANUMET", "JANUMET XR"],
        "drug_class": "DPP-4 Inhibitor",
        "route": "Oral",
        "standard_tier": "Tier 2 / Tier 3",
        "avg_30d_cost_benchmark": 480.0,
        "is_newer_class": False,
    },
    "LINAGLIPTIN": {
        "brand_names": ["TRADJENTA", "JENTADUETO"],
        "drug_class": "DPP-4 Inhibitor",
        "route": "Oral",
        "standard_tier": "Tier 3",
        "avg_30d_cost_benchmark": 470.0,
        "is_newer_class": False,
    },

    # Biguanides
    "METFORMIN HCL": {
        "brand_names": ["GLUCOPHAGE", "GLUCOPHAGE XR", "FORTAMET", "GLUMETZA", "METFORMIN"],
        "drug_class": "Biguanide (Metformin)",
        "route": "Oral",
        "standard_tier": "Tier 1 (Generic)",
        "avg_30d_cost_benchmark": 12.5,
        "is_newer_class": False,
    },

    # Sulfonylureas
    "GLIMEPIRIDE": {
        "brand_names": ["AMARYL", "GLIMEPIRIDE"],
        "drug_class": "Sulfonylurea",
        "route": "Oral",
        "standard_tier": "Tier 1 (Generic)",
        "avg_30d_cost_benchmark": 14.0,
        "is_newer_class": False,
    },
    "GLIPIZIDE": {
        "brand_names": ["GLUCOTROL", "GLUCOTROL XL", "GLIPIZIDE"],
        "drug_class": "Sulfonylurea",
        "route": "Oral",
        "standard_tier": "Tier 1 (Generic)",
        "avg_30d_cost_benchmark": 15.0,
        "is_newer_class": False,
    },

    # Basal Insulins
    "INSULIN GLARGINE": {
        "brand_names": ["LANTUS", "BASAGLAR", "TOUJEO", "SEMGLEE"],
        "drug_class": "Basal Insulin",
        "route": "Subcutaneous",
        "standard_tier": "Tier 3 / Biosimilar Tier 2",
        "avg_30d_cost_benchmark": 320.0,
        "is_newer_class": False,
    },
    "INSULIN DEGLUDEC": {
        "brand_names": ["TRESIBA"],
        "drug_class": "Basal Insulin",
        "route": "Subcutaneous",
        "standard_tier": "Tier 3",
        "avg_30d_cost_benchmark": 350.0,
        "is_newer_class": False,
    },
}

# Target Physician Specialties for T2D
PHYSICIAN_SPECIALTIES = [
    "Internal Medicine",
    "Family Practice",
    "Endocrinology, Diabetes & Metabolism",
    "Nurse Practitioner",
]

# Survey Specification Constants
SURVEY_SAMPLE_SIZE = 350
SURVEY_EXPERIENCE_BANDS = ["<5 years", "5-10 years", "11-20 years", ">20 years"]
SURVEY_PRACTICE_SETTINGS = [
    "Academic Medical Center",
    "Community Hospital System",
    "Private Group Practice",
    "Solo Practice",
    "FQHC / Community Clinic",
]

# Likert Scale Mappings
LIKERT_LABELS = {
    1: "Strongly Disagree / Not a Barrier",
    2: "Disagree / Minor Barrier",
    3: "Neutral / Moderate Barrier",
    4: "Agree / Significant Barrier",
    5: "Strongly Agree / Severe Barrier",
}

# Output File Paths
SURVEY_RAW_CSV = SYNTHETIC_DATA_DIR / "t2d_hcp_survey_responses_synthetic.csv"
CMS_RAW_CSV = RAW_DATA_DIR / "cms_medicare_part_d_t2d_prescribers.csv"
CMS_PROCESSED_CSV = PROCESSED_DATA_DIR / "cms_part_d_t2d_cleaned.csv"
SURVEY_PROCESSED_CSV = PROCESSED_DATA_DIR / "t2d_survey_cleaned.csv"
POWERPOINT_OUTPUT = REPORTS_DIR / "PharmaPulse_Executive_Report.pptx"
