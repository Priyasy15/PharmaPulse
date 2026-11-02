"""
Unit tests for PharmaPulse Automated Insight Generator.
"""
import pytest
from src.insights.insight_generator import generate_commercial_insights

def test_generate_commercial_insights():
    catalog = generate_commercial_insights()
    insights = catalog["insights_catalog"]
    recs = catalog["recommendations_portfolio"]

    assert len(insights) >= 5
    assert len(recs) >= 4

    for ins in insights:
        assert "id" in ins
        assert "category" in ins
        assert "title" in ins
        assert "statement" in ins
        assert "traceable_metrics" in ins
        assert "evidence_sources" in ins
        assert "strategic_recommendation" in ins

    # Check top barrier insight traceability
    top_ins = next((i for i in insights if i["id"] == "INSIGHT_001_TOP_BARRIERS"), None)
    assert top_ins is not None
    assert "top_barrier_mean" in top_ins["traceable_metrics"]
    assert top_ins["traceable_metrics"]["top_barrier_mean"] >= 4.0
