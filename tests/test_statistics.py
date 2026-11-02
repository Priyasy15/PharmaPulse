"""
Unit tests for PharmaPulse Statistical Analysis and Hypothesis Testing.
"""
import pytest
import pandas as pd
import numpy as np

from src.statistics.statistical_tests import (
    calculate_wilson_score_ci,
    perform_chi_square_test,
    analyze_likert_question,
    compare_groups_kruskal,
)
from src.statistics.survey_analyzer import run_comprehensive_survey_analysis

def test_wilson_score_ci():
    # Known benchmark test: 50 successes out of 100 trials at 95% confidence
    p, lower, upper = calculate_wilson_score_ci(50, 100, 0.95)
    assert p == 0.50
    assert 0.40 <= lower <= 0.45
    assert 0.55 <= upper <= 0.61

    # Edge cases
    p0, l0, u0 = calculate_wilson_score_ci(0, 50, 0.95)
    assert p0 == 0.0
    assert l0 == 0.0
    assert u0 < 0.10


def test_chi_square_test():
    # Construct synthetic contingency dataset
    np.random.seed(42)
    group_a = ["Endo"] * 50 + ["PCP"] * 50
    # Clear divergence: Endo prefers GLP1, PCP prefers Metformin
    choice = (["GLP1"] * 40 + ["Metformin"] * 10) + (["GLP1"] * 10 + ["Metformin"] * 40)
    df = pd.DataFrame({"Specialty": group_a, "Choice": choice})

    res = perform_chi_square_test(df, "Specialty", "Choice")
    assert res["is_statistically_significant"] is True
    assert res["p_value"] < 0.001
    assert res["cramers_v"] > 0.50
    assert res["degrees_of_freedom"] == 1


def test_likert_analysis():
    df = pd.DataFrame({"Rating": [1, 2, 3, 4, 5, 5, 4, 4, 3, 2]})
    res = analyze_likert_question(df, "Rating", "Test Barrier")
    assert res["sample_size"] == 10
    assert res["mean"] == 3.3
    assert res["top_box_pct"] == 50.0
    assert res["median"] == 3.5


def test_kruskal_wallis_test():
    df = pd.DataFrame({
        "Group": ["A"] * 20 + ["B"] * 20,
        "Score": [5, 4, 5, 5, 4] * 4 + [1, 2, 2, 1, 2] * 4
    })
    res = compare_groups_kruskal(df, "Group", "Score")
    assert res["is_significant"] is True
    assert res["p_value"] < 0.01
    assert res["group_breakdown"]["A"]["mean"] > res["group_breakdown"]["B"]["mean"]


def test_full_survey_analyzer():
    res = run_comprehensive_survey_analysis()
    assert res["sample_size"] == 350
    assert len(res["ranked_barriers"]) == 5
    assert "chi2_specialty_vs_ascvd_preference" in res["hypothesis_tests"]
