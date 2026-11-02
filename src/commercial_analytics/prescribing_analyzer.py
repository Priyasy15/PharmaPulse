"""
PharmaPulse CMS Prescribing Analytics Engine
Analyzes real-world claims, gross expenditure, specialty nuances, and geographic patterns in Medicare Part D.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
from config.settings import CMS_PROCESSED_CSV

def run_prescribing_analytics(
    cms_path: Path = CMS_PROCESSED_CSV
) -> Dict[str, Any]:
    """
    Computes market share, specialty variations, geographic breakdowns,
    and cost efficiencies from cleaned CMS Part D Prescriber data.
    """
    if not cms_path.exists():
        raise FileNotFoundError(f"Cleaned CMS data not found at: {cms_path}")

    df = pd.read_csv(cms_path)

    total_market_claims = df["TOT_CLMS"].sum()
    total_market_cost = df["TOT_DRUG_CST"].sum()
    total_beneficiaries = df["TOT_BENES"].sum()
    unique_prescribers = df["PRSCRBR_NPI"].nunique()

    # 1. Market Share by Drug Class
    class_agg = df.groupby("DRUG_CLASS").agg(
        total_claims=("TOT_CLMS", "sum"),
        total_30day_fills=("TOT_30DAY_FILLS", "sum"),
        total_drug_cost=("TOT_DRUG_CST", "sum"),
        total_benes=("TOT_BENES", "sum"),
        prescriber_count=("PRSCRBR_NPI", "nunique"),
    ).reset_index()

    class_agg["claims_market_share_pct"] = (class_agg["total_claims"] / total_market_claims * 100).round(2)
    class_agg["cost_market_share_pct"] = (class_agg["total_drug_cost"] / total_market_cost * 100).round(2)
    class_agg["avg_cost_per_claim"] = (class_agg["total_drug_cost"] / class_agg["total_claims"]).round(2)
    class_agg["avg_cost_per_30d_fill"] = (class_agg["total_drug_cost"] / class_agg["total_30day_fills"]).round(2)

    class_summary = class_agg.sort_values(by="total_claims", ascending=False).to_dict("records")

    # 2. Product-Level Breakdown (Top Drugs by Claims & Cost)
    drug_agg = df.groupby(["DRUG_NAME", "CANONICAL_GENERIC", "DRUG_CLASS"]).agg(
        total_claims=("TOT_CLMS", "sum"),
        total_drug_cost=("TOT_DRUG_CST", "sum"),
        total_benes=("TOT_BENES", "sum"),
        prescribers=("PRSCRBR_NPI", "nunique")
    ).reset_index()

    drug_agg["claims_share_pct"] = (drug_agg["total_claims"] / total_market_claims * 100).round(2)
    drug_agg["cost_share_pct"] = (drug_agg["total_drug_cost"] / total_market_cost * 100).round(2)
    drug_agg["cost_per_claim"] = (drug_agg["total_drug_cost"] / drug_agg["total_claims"]).round(2)
    top_drugs_by_claims = drug_agg.sort_values(by="total_claims", ascending=False).head(10).to_dict("records")
    top_drugs_by_cost = drug_agg.sort_values(by="total_drug_cost", ascending=False).head(10).to_dict("records")

    # 3. Specialty Prescribing Profiles
    spec_agg = df.groupby(["PRSCRBR_TYPE", "DRUG_CLASS"]).agg(
        claims=("TOT_CLMS", "sum"),
        cost=("TOT_DRUG_CST", "sum")
    ).reset_index()

    # Calculate class share within each specialty
    spec_totals = spec_agg.groupby("PRSCRBR_TYPE")["claims"].transform("sum")
    spec_agg["class_share_within_specialty"] = (spec_agg["claims"] / spec_totals * 100).round(2)
    
    specialty_class_matrix = spec_agg.pivot(
        index="PRSCRBR_TYPE",
        columns="DRUG_CLASS",
        values="class_share_within_specialty"
    ).fillna(0).round(1).to_dict("index")

    # 4. Geographic Variation (State Level)
    state_agg = df.groupby("PRSCRBR_STATE_ABRVTN").agg(
        total_claims=("TOT_CLMS", "sum"),
        total_cost=("TOT_DRUG_CST", "sum"),
        prescribers=("PRSCRBR_NPI", "nunique"),
        glp1_claims=("TOT_CLMS", lambda s: s[df.loc[s.index, "DRUG_CLASS"].isin(["GLP-1 RA", "GLP-1 / GIP Dual Agonist"])].sum()),
        sglt2_claims=("TOT_CLMS", lambda s: s[df.loc[s.index, "DRUG_CLASS"] == "SGLT2 Inhibitor"].sum())
    ).reset_index()

    state_agg["glp1_penetration_pct"] = (state_agg["glp1_claims"] / state_agg["total_claims"] * 100).round(2)
    state_agg["sglt2_penetration_pct"] = (state_agg["sglt2_claims"] / state_agg["total_claims"] * 100).round(2)
    state_agg["cost_per_claim"] = (state_agg["total_cost"] / state_agg["total_claims"]).round(2)
    state_summary = state_agg.sort_values(by="total_claims", ascending=False).to_dict("records")

    # 5. Prescriber Concentration (Pareto / Decile Analysis)
    prescriber_totals = df.groupby("PRSCRBR_NPI")["TOT_CLMS"].sum().sort_values(ascending=False)
    n_p = len(prescriber_totals)
    top_10_pct_count = max(1, int(n_p * 0.10))
    top_10_pct_claims = prescriber_totals.head(top_10_pct_count).sum()
    top_10_pct_volume_share = round((top_10_pct_claims / total_market_claims) * 100, 2)

    return {
        "market_totals": {
            "total_claims": int(total_market_claims),
            "total_gross_drug_cost": round(float(total_market_cost), 2),
            "total_beneficiaries": int(total_beneficiaries),
            "unique_prescribers": int(unique_prescribers),
            "overall_avg_cost_per_claim": round(float(total_market_cost / total_market_claims), 2),
        },
        "drug_class_summary": class_summary,
        "top_drugs_by_claims": top_drugs_by_claims,
        "top_drugs_by_cost": top_drugs_by_cost,
        "specialty_class_matrix": specialty_class_matrix,
        "state_summary": state_summary,
        "prescriber_concentration": {
            "top_10_pct_prescribers_volume_share": top_10_pct_volume_share,
            "prescribers_in_top_decile": top_10_pct_count,
        },
    }


if __name__ == "__main__":
    res = run_prescribing_analytics()
    print("Market Totals:", res["market_totals"])
    print("Top Class by Claims:", res["drug_class_summary"][0]["DRUG_CLASS"])
