"""
PharmaPulse Statistical Analysis Engine
Implements rigorous hypothesis testing, chi-square tests of independence,
Cramér's V, Mann-Whitney U, Kruskal-Wallis, Likert distributions, and confidence intervals.
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any, Tuple, List

def calculate_wilson_score_ci(
    count: int,
    n: int,
    confidence: float = 0.95
) -> Tuple[float, float, float]:
    """
    Calculates the Wilson score confidence interval for a binomial proportion.
    More robust than the normal approximation, especially near 0 and 1 or small sample sizes.
    Returns: (point_estimate, ci_lower, ci_upper)
    """
    if n == 0:
        return 0.0, 0.0, 0.0
    p = count / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denom = 1 + (z ** 2) / n
    centre_adj = p + (z ** 2) / (2 * n)
    margin = z * np.sqrt((p * (1 - p) + (z ** 2) / (4 * n)) / n)
    lower = max(0.0, (centre_adj - margin) / denom)
    upper = min(1.0, (centre_adj + margin) / denom)
    return round(p, 4), round(lower, 4), round(upper, 4)


def perform_chi_square_test(
    df: pd.DataFrame,
    var1: str,
    var2: str
) -> Dict[str, Any]:
    """
    Performs Pearson's Chi-Square Test of Independence between two categorical variables.
    Computes test statistic, p-value, degrees of freedom, expected frequencies,
    Cochran's assumption check, and Cramér's V effect size.
    """
    contingency = pd.crosstab(df[var1], df[var2])
    chi2, p_val, dof, expected = stats.chi2_contingency(contingency)

    # Cochran's criteria check:
    # 1. No expected frequencies < 1
    # 2. No more than 20% of expected frequencies < 5
    n_cells = expected.size
    cells_under_5 = np.sum(expected < 5)
    pct_cells_under_5 = (cells_under_5 / n_cells) * 100
    min_expected = expected.min()
    assumptions_met = (min_expected >= 1.0) and (pct_cells_under_5 <= 20.0)

    # Cramér's V effect size
    n = contingency.values.sum()
    min_dim = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if (n * min_dim) > 0 else 0.0

    return {
        "variable_1": var1,
        "variable_2": var2,
        "chi2_statistic": round(float(chi2), 3),
        "p_value": float(p_val),
        "degrees_of_freedom": int(dof),
        "contingency_table": contingency.to_dict(),
        "expected_frequencies": expected.round(2).tolist(),
        "cramers_v": round(float(cramers_v), 3),
        "is_statistically_significant": bool(p_val < 0.05),
        "cochran_assumptions_met": bool(assumptions_met),
        "pct_cells_expected_under_5": round(float(pct_cells_under_5), 1),
        "minimum_expected_freq": round(float(min_expected), 2),
        "interpretation": (
            f"Statistically significant relationship detected (p={p_val:.4f} < 0.05) with Cramér's V={cramers_v:.3f}."
            if p_val < 0.05 else
            f"No statistically significant relationship detected (p={p_val:.4f} >= 0.05)."
        ),
    }


def analyze_likert_question(
    df: pd.DataFrame,
    col_name: str,
    label: str = ""
) -> Dict[str, Any]:
    """
    Comprehensive statistical breakdown for a 1-5 Likert question:
    - Mean, Standard Deviation, Median, IQR
    - Top-Box % (Rating 4 or 5) with 95% Wilson CI
    - Bottom-Box % (Rating 1 or 2)
    - Net Agreement / Severity Score (Top-Box % minus Bottom-Box %)
    - Distribution breakdown (1 to 5 counts and percentages)
    """
    series = df[col_name].dropna()
    n = len(series)
    if n == 0:
        return {}

    mean_val = series.mean()
    std_val = series.std()
    median_val = series.median()
    iqr_val = series.quantile(0.75) - series.quantile(0.25)

    counts = series.value_counts().to_dict()
    dist = {i: {"count": counts.get(i, 0), "pct": round(counts.get(i, 0) / n * 100, 1)} for i in range(1, 6)}

    top_box_count = counts.get(4, 0) + counts.get(5, 0)
    top_box_pct, tb_ci_low, tb_ci_high = calculate_wilson_score_ci(top_box_count, n)

    bottom_box_count = counts.get(1, 0) + counts.get(2, 0)
    bottom_box_pct = bottom_box_count / n

    net_score = (top_box_pct - bottom_box_pct) * 100

    return {
        "metric_id": col_name,
        "label": label or col_name,
        "sample_size": n,
        "mean": round(float(mean_val), 2),
        "std_dev": round(float(std_val), 2),
        "median": float(median_val),
        "iqr": round(float(iqr_val), 2),
        "distribution": dist,
        "top_box_pct": round(float(top_box_pct * 100), 1),
        "top_box_ci_95": (round(tb_ci_low * 100, 1), round(tb_ci_high * 100, 1)),
        "bottom_box_pct": round(float(bottom_box_pct * 100), 1),
        "net_severity_score": round(float(net_score), 1),
    }


def compare_groups_kruskal(
    df: pd.DataFrame,
    group_col: str,
    value_col: str
) -> Dict[str, Any]:
    """
    Performs Kruskal-Wallis H-test (non-parametric ANOVA) to compare Likert ratings across groups.
    """
    groups = [group[value_col].dropna().values for _, group in df.groupby(group_col)]
    h_stat, p_val = stats.kruskal(*groups)
    
    group_means = df.groupby(group_col)[value_col].agg(["count", "mean", "median", "std"]).round(2).to_dict("index")

    return {
        "group_variable": group_col,
        "value_variable": value_col,
        "h_statistic": round(float(h_stat), 3),
        "p_value": float(p_val),
        "is_significant": bool(p_val < 0.05),
        "group_breakdown": group_means,
        "interpretation": (
            f"Statistically significant divergence across {group_col} (Kruskal-Wallis p={p_val:.4f})."
            if p_val < 0.05 else
            f"No statistically significant difference across {group_col} (p={p_val:.4f})."
        ),
    }


def compute_barrier_correlation_matrix(
    df: pd.DataFrame,
    barrier_cols: List[str]
) -> pd.DataFrame:
    """Computes Spearman rank correlation matrix across adoption barrier metrics."""
    return df[barrier_cols].corr(method="spearman").round(3)
