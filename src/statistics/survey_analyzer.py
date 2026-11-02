"""
PharmaPulse Survey Statistical Analyzer Pipeline
Executes descriptive, bivariate, and non-parametric statistical evaluations on survey data.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
from config.settings import SURVEY_PROCESSED_CSV
from src.statistics.statistical_tests import (
    analyze_likert_question,
    perform_chi_square_test,
    compare_groups_kruskal,
    compute_barrier_correlation_matrix,
    calculate_wilson_score_ci,
)

BARRIER_QUESTION_MAP = {
    "Q11_BARRIER_PRIOR_AUTH": "Prior Authorization & Step Therapy Documentation",
    "Q12_BARRIER_OUT_OF_POCKET_COST": "Patient Out-of-Pocket Copay & Deductible",
    "Q13_BARRIER_SIDE_EFFECTS": "Clinical Tolerability & Side Effects (GI / Mycotic)",
    "Q14_BARRIER_SUPPLY_SHORTAGES": "National Supply Shortages & Dispensing Delays",
    "Q15_BARRIER_PATIENT_NEEDLE_HESITATION": "Patient Needle Anxiety & Subcutaneous Hesitation",
}

AWARENESS_QUESTION_MAP = {
    "Q9_FAMILIARITY_GLP1": "Familiarity with GLP-1 RA Cardiorenal Outcome Trials (CVOTs)",
    "Q10_FAMILIARITY_SGLT2": "Familiarity with SGLT2i Heart Failure & CKD Trials",
}

def run_comprehensive_survey_analysis(
    survey_path: Path = SURVEY_PROCESSED_CSV
) -> Dict[str, Any]:
    """
    Executes a complete statistical suite across the survey dataset:
    1. Sample demographic profile & margins of error.
    2. Likert scale barrier rankings & Net Severity scores.
    3. Treatment preference distributions with 95% Wilson CIs.
    4. Hypothesis testing:
       - Chi-square: Specialty vs Second-line ASCVD treatment choice.
       - Chi-square: Specialty vs First-line choice.
       - Kruskal-Wallis: Specialty vs Prior Authorization burden.
       - Kruskal-Wallis: Specialty vs Needle Anxiety barrier.
    5. Barrier correlation matrix.
    """
    if not survey_path.exists():
        raise FileNotFoundError(f"Processed survey dataset not found at: {survey_path}")

    df = pd.read_csv(survey_path)
    total_n = len(df)

    # 1. Demographic Frequencies
    specialty_dist = df["Q1_SPECIALTY"].value_counts(normalize=True).mul(100).round(1).to_dict()
    exp_dist = df["Q2_YEARS_EXPERIENCE"].value_counts(normalize=True).mul(100).round(1).to_dict()
    setting_dist = df["Q3_PRACTICE_SETTING"].value_counts(normalize=True).mul(100).round(1).to_dict()

    # 2. Likert Barrier Analysis
    barrier_stats = {}
    for col, label in BARRIER_QUESTION_MAP.items():
        barrier_stats[col] = analyze_likert_question(df, col, label)

    # Ranked Barriers by Mean Score
    ranked_barriers = sorted(
        barrier_stats.values(),
        key=lambda x: x["mean"],
        reverse=True
    )

    # 3. Awareness / Familiarity Stats
    awareness_stats = {}
    for col, label in AWARENESS_QUESTION_MAP.items():
        awareness_stats[col] = analyze_likert_question(df, col, label)

    # 4. Treatment Preferences & CIs
    first_line_counts = df["Q6_FIRST_LINE_PREFERENCE"].value_counts()
    first_line_analysis = {}
    for choice, count in first_line_counts.items():
        p, low, high = calculate_wilson_score_ci(count, total_n)
        first_line_analysis[choice] = {
            "count": int(count),
            "pct": round(p * 100, 1),
            "ci_95": (round(low * 100, 1), round(high * 100, 1)),
        }

    second_ascvd_counts = df["Q7_SECOND_LINE_ASCVD_PREFERENCE"].value_counts()
    second_ascvd_analysis = {}
    for choice, count in second_ascvd_counts.items():
        p, low, high = calculate_wilson_score_ci(count, total_n)
        second_ascvd_analysis[choice] = {
            "count": int(count),
            "pct": round(p * 100, 1),
            "ci_95": (round(low * 100, 1), round(high * 100, 1)),
        }

    second_ckd_counts = df["Q8_SECOND_LINE_CKD_HF_PREFERENCE"].value_counts()
    second_ckd_analysis = {}
    for choice, count in second_ckd_counts.items():
        p, low, high = calculate_wilson_score_ci(count, total_n)
        second_ckd_analysis[choice] = {
            "count": int(count),
            "pct": round(p * 100, 1),
            "ci_95": (round(low * 100, 1), round(high * 100, 1)),
        }

    # 5. Statistical Hypothesis Tests
    test_specialty_vs_ascvd = perform_chi_square_test(
        df, "Q1_SPECIALTY", "Q7_SECOND_LINE_ASCVD_PREFERENCE"
    )

    test_specialty_vs_first_line = perform_chi_square_test(
        df, "Q1_SPECIALTY", "Q6_FIRST_LINE_PREFERENCE"
    )

    kw_prior_auth = compare_groups_kruskal(
        df, "Q1_SPECIALTY", "Q11_BARRIER_PRIOR_AUTH"
    )

    kw_needle = compare_groups_kruskal(
        df, "Q1_SPECIALTY", "Q15_BARRIER_PATIENT_NEEDLE_HESITATION"
    )

    # 6. Barrier Correlation Matrix
    corr_df = compute_barrier_correlation_matrix(df, list(BARRIER_QUESTION_MAP.keys()))

    return {
        "sample_size": total_n,
        "demographics": {
            "specialty_distribution": specialty_dist,
            "experience_distribution": exp_dist,
            "setting_distribution": setting_dist,
        },
        "barrier_analysis": barrier_stats,
        "ranked_barriers": ranked_barriers,
        "awareness_analysis": awareness_stats,
        "first_line_preferences": first_line_analysis,
        "second_line_ascvd_preferences": second_ascvd_analysis,
        "second_line_ckd_preferences": second_ckd_analysis,
        "hypothesis_tests": {
            "chi2_specialty_vs_ascvd_preference": test_specialty_vs_ascvd,
            "chi2_specialty_vs_first_line": test_specialty_vs_first_line,
            "kruskal_specialty_vs_prior_auth": kw_prior_auth,
            "kruskal_specialty_vs_needle_anxiety": kw_needle,
        },
        "barrier_correlation_matrix": corr_df.to_dict(),
    }


if __name__ == "__main__":
    results = run_comprehensive_survey_analysis()
    print("Survey Analysis Finished.")
    print("Top Barrier:", results["ranked_barriers"][0]["label"], "Mean:", results["ranked_barriers"][0]["mean"])
    print("Chi2 ASCVD:", results["hypothesis_tests"]["chi2_specialty_vs_ascvd_preference"]["interpretation"])
