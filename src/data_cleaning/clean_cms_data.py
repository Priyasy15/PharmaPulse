"""
PharmaPulse CMS Medicare Part D Data Cleaning & Standardization Pipeline
Cleans, standardizes, deduplicates, and enriches CMS Medicare Part D prescriber records.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
from config.settings import (
    CMS_RAW_CSV,
    CMS_PROCESSED_CSV,
    T2D_DRUG_CATALOG,
    PROCESSED_DATA_DIR,
)

def create_drug_lookup_dict() -> Dict[str, Dict[str, Any]]:
    """Builds a lookup mapping from any brand or generic variant to standardized metadata."""
    lookup = {}
    for gen_name, meta in T2D_DRUG_CATALOG.items():
        gen_clean = gen_name.strip().upper()
        entry = {
            "canonical_generic": gen_clean,
            "drug_class": meta["drug_class"],
            "route": meta["route"],
            "standard_tier": meta["standard_tier"],
            "is_newer_class": meta["is_newer_class"],
        }
        lookup[gen_clean] = entry
        for brand in meta["brand_names"]:
            lookup[brand.strip().upper()] = entry
    return lookup


def clean_cms_prescribing_data(
    input_path: Path = CMS_RAW_CSV,
    output_path: Path = CMS_PROCESSED_CSV
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw CMS Medicare Part D Prescriber data:
    1. Trims and standardizes case for strings.
    2. Removes exact and key-level duplicates.
    3. Maps drug names and generic names to standard classes and canonical names.
    4. Calculates cost and claim efficiency metrics.
    5. Saves cleaned dataset to CSV.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"CMS Raw dataset not found at: {input_path}")

    df_raw = pd.read_csv(input_path)
    initial_rows = len(df_raw)

    # 1. Clean string fields
    string_cols = ["PRSCRBR_LAST_ORG_NAME", "PRSCRBR_FIRST_NAME", "PRSCRBR_CITY",
                   "PRSCRBR_STATE_ABRVTN", "PRSCRBR_TYPE", "DRUG_NAME", "GENERIC_NAME"]
    for col in string_cols:
        if col in df_raw.columns:
            df_raw[col] = df_raw[col].astype(str).str.strip().str.upper()

    # 2. Deduplication
    df_clean = df_raw.drop_duplicates(subset=["PRSCRBR_NPI", "DRUG_NAME", "YEAR"]).copy()
    duplicates_removed = initial_rows - len(df_clean)

    # 3. Standardize and Map Drugs
    lookup = create_drug_lookup_dict()

    canonical_generics = []
    drug_classes = []
    routes = []
    tiers = []
    is_newer_flags = []

    for _, row in df_clean.iterrows():
        drug_name = row["DRUG_NAME"]
        generic_name = row["GENERIC_NAME"]

        matched = None
        if drug_name in lookup:
            matched = lookup[drug_name]
        elif generic_name in lookup:
            matched = lookup[generic_name]
        else:
            # Fallback search for partial match
            for key, val in lookup.items():
                if key in drug_name or key in generic_name:
                    matched = val
                    break

        if matched:
            canonical_generics.append(matched["canonical_generic"])
            drug_classes.append(matched["drug_class"])
            routes.append(matched["route"])
            tiers.append(matched["standard_tier"])
            is_newer_flags.append(matched["is_newer_class"])
        else:
            canonical_generics.append(generic_name)
            drug_classes.append("Other T2D")
            routes.append("Unknown")
            tiers.append("Other")
            is_newer_flags.append(False)

    df_clean["CANONICAL_GENERIC"] = canonical_generics
    df_clean["DRUG_CLASS"] = drug_classes
    df_clean["ADMINISTRATION_ROUTE"] = routes
    df_clean["FORMULARY_TIER"] = tiers
    df_clean["IS_NEWER_THERAPY"] = is_newer_flags

    # 4. Numeric Cleaning & Verification
    numeric_cols = ["TOT_CLMS", "TOT_30DAY_FILLS", "TOT_DRUG_CST", "TOT_BENES"]
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0)

    # 5. Derived Commercial Metrics
    # Avoid zero-division
    df_clean["COST_PER_CLAIM"] = np.where(
        df_clean["TOT_CLMS"] > 0,
        (df_clean["TOT_DRUG_CST"] / df_clean["TOT_CLMS"]).round(2),
        0.0
    )
    df_clean["COST_PER_30DAY_FILL"] = np.where(
        df_clean["TOT_30DAY_FILLS"] > 0,
        (df_clean["TOT_DRUG_CST"] / df_clean["TOT_30DAY_FILLS"]).round(2),
        0.0
    )
    df_clean["FILLS_PER_CLAIM"] = np.where(
        df_clean["TOT_CLMS"] > 0,
        (df_clean["TOT_30DAY_FILLS"] / df_clean["TOT_CLMS"]).round(2),
        0.0
    )
    df_clean["CLAIMS_PER_BENE"] = np.where(
        df_clean["TOT_BENES"] > 0,
        (df_clean["TOT_CLMS"] / df_clean["TOT_BENES"]).round(2),
        0.0
    )

    # 6. Save Cleaned Data
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)

    summary_stats = {
        "initial_raw_records": initial_rows,
        "cleaned_records": len(df_clean),
        "duplicates_removed": duplicates_removed,
        "unique_prescribers": df_clean["PRSCRBR_NPI"].nunique(),
        "total_claims": int(df_clean["TOT_CLMS"].sum()),
        "total_drug_cost": float(df_clean["TOT_DRUG_CST"].sum()),
        "distinct_drug_classes": df_clean["DRUG_CLASS"].nunique(),
        "output_path": str(output_path),
    }

    print(f"CMS Data cleaned: {summary_stats['cleaned_records']} records. Output saved to {output_path}")
    return df_clean, summary_stats


if __name__ == "__main__":
    df_cleaned, stats = clean_cms_prescribing_data()
    print("Summary Stats:", stats)
