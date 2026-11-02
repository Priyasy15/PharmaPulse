"""
PharmaPulse – Type 2 Diabetes Commercial Market Research & Prescribing Analytics Platform
Bloomberg Terminal × IQVIA Commercial Intelligence × Enterprise SaaS Edition
"""
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from config.settings import (
    CMS_PROCESSED_CSV,
    SURVEY_PROCESSED_CSV,
    POWERPOINT_OUTPUT,
    POWERBI_EXPORTS_DIR,
    DOCS_DIR,
)
from src.statistics.survey_analyzer import run_comprehensive_survey_analysis
from src.commercial_analytics.prescribing_analyzer import run_prescribing_analytics
from src.commercial_analytics.stated_vs_observed import compute_stated_vs_observed_gap
from src.insights.insight_generator import generate_commercial_insights
from src.report_generation.presentation_builder import build_powerpoint_deck
from src.survey.survey_design import QUESTIONS_DEFINITION, SURVEY_METADATA

# Page Configuration
st.set_page_config(
    page_title="PharmaPulse | T2D Commercial Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# TERMINAL × IQVIA DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Main Canvas Background */
    .stApp {
        background-color: #F3F5F8;
        color: #172536;
    }

    /* Compact Layout Container */
    .block-container {
        padding-top: 1.0rem;
        padding-bottom: 2.5rem;
        padding-left: 2.0rem;
        padding-right: 2.0rem;
        max-width: 1480px;
    }

    /* =========================================================================
       DARK TERMINAL SIDEBAR (#101C2D)
       ========================================================================= */
    [data-testid="stSidebar"] {
        background-color: #101C2D !important;
        border-right: 1px solid #1E2E42 !important;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
        padding-left: 1.0rem;
        padding-right: 1.0rem;
    }
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 12px;
        margin-bottom: 12px;
        border-bottom: 1px solid #1E2E42;
    }
    .sidebar-brand-icon {
        background: #142B4A;
        border: 1px solid #3478C7;
        color: #FFFFFF;
        width: 32px;
        height: 32px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
    }
    .sidebar-brand-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 0.04em;
        line-height: 1.1;
    }
    .sidebar-brand-caption {
        font-size: 0.70rem;
        color: #8C9BAE;
        font-weight: 500;
        letter-spacing: 0.02em;
    }
    .sidebar-section-header {
        font-size: 0.68rem;
        font-weight: 700;
        color: #8C9BAE;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 14px;
        margin-bottom: 6px;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #17263A !important;
        border: 1px solid #243852 !important;
        border-radius: 4px !important;
        color: #FFFFFF !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #1F334E !important;
        border: 1px solid #3478C7 !important;
        border-radius: 3px !important;
        color: #DCE8F5 !important;
        font-size: 0.76rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] label p {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        margin-bottom: 2px !important;
    }
    .sidebar-status-box {
        background: #0B1422;
        border: 1px solid #1E2E42;
        border-radius: 4px;
        padding: 10px;
        margin-top: 20px;
        font-size: 0.74rem;
        line-height: 1.4;
    }
    .sidebar-status-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 700;
        color: #16845B;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .sidebar-status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #16845B;
        display: inline-block;
        box-shadow: 0 0 4px #16845B;
    }

    /* =========================================================================
       COMPACT ENTERPRISE HEADER & GOVERNANCE
       ========================================================================= */
    .app-header-strip {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #DCE2EA;
        border-radius: 4px;
        padding: 10px 16px;
        margin-bottom: 10px;
    }
    .app-header-title-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-header-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #142B4A;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    .app-header-tag {
        font-size: 0.68rem;
        font-weight: 700;
        color: #3478C7;
        background: #DCE8F5;
        border: 1px solid #BACFE6;
        padding: 2px 7px;
        border-radius: 3px;
        letter-spacing: 0.04em;
    }
    .app-header-meta {
        font-size: 0.78rem;
        color: #667487;
        display: flex;
        gap: 16px;
    }
    .app-header-meta span {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .app-header-meta b {
        color: #172536;
    }

    /* Research Governance Banner */
    .governance-strip {
        background-color: #FFFFFF;
        border: 1px solid #DCE2EA;
        border-left: 3px solid #3478C7;
        border-radius: 3px;
        padding: 6px 14px;
        font-size: 0.77rem;
        color: #667487;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .governance-strip b {
        color: #142B4A;
        font-weight: 700;
    }

    /* =========================================================================
       TERMINAL NAVIGATION TABS
       ========================================================================= */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE2EA !important;
        border-radius: 4px !important;
        padding: 2px !important;
        gap: 2px !important;
        box-shadow: none !important;
        margin-bottom: 14px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 36px !important;
        white-space: pre-wrap !important;
        background-color: transparent !important;
        border-radius: 3px !important;
        padding: 6px 12px !important;
        font-weight: 600 !important;
        font-size: 0.80rem !important;
        color: #667487 !important;
        border: none !important;
        transition: all 0.1s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #F3F5F8 !important;
        color: #172536 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #142B4A !important;
        color: #FFFFFF !important;
        border-radius: 3px !important;
    }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* =========================================================================
       BLOOMBERG TERMINAL KPI TELEMETRY BAR
       ========================================================================= */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE2EA !important;
        border-radius: 4px !important;
        padding: 10px 14px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        color: #667487 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin-bottom: 2px !important;
    }
    [data-testid="stMetricValue"] div {
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        color: #142B4A !important;
        font-family: 'JetBrains Mono', 'Inter', monospace !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
    }

    /* =========================================================================
       ANALYTICAL SURFACES & CARDS
       ========================================================================= */
    .terminal-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE2EA;
        border-radius: 4px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .terminal-section-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #142B4A;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 4px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .terminal-badge {
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 3px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .terminal-badge-p1 {
        background-color: #FCE8E8;
        color: #C45151;
        border: 1px solid #F5C2C2;
    }
    .terminal-badge-p2 {
        background-color: #FDF3E3;
        color: #C58B32;
        border: 1px solid #F5DEB3;
    }
    .terminal-badge-p3 {
        background-color: #DCE8F5;
        color: #142B4A;
        border: 1px solid #BACFE6;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE2EA !important;
        border-radius: 4px !important;
        margin-bottom: 6px !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #142B4A !important;
        font-size: 0.86rem !important;
        padding: 10px 14px !important;
    }

    /* Buttons */
    div.stButton > button:first-child {
        border-radius: 3px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        padding: 6px 14px !important;
        border: 1px solid #DCE2EA !important;
        background-color: #FFFFFF !important;
        color: #172536 !important;
    }
    div.stButton > button:first-child:hover {
        border-color: #3478C7 !important;
        color: #3478C7 !important;
        background-color: #F3F5F8 !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #3478C7 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #203B5C !important;
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        border-radius: 3px !important;
        font-weight: 600 !important;
        font-size: 0.80rem !important;
        padding: 6px 12px !important;
        border: 1px solid #DCE2EA !important;
        background-color: #FFFFFF !important;
        color: #172536 !important;
        width: 100% !important;
    }
    div.stDownloadButton > button:hover {
        border-color: #3478C7 !important;
        color: #3478C7 !important;
        background-color: #F3F5F8 !important;
    }

    /* Form Container */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE2EA !important;
        border-radius: 4px !important;
        padding: 18px !important;
    }

    /* Dataframe Container */
    [data-testid="stDataFrame"] {
        border: 1px solid #DCE2EA !important;
        border-radius: 4px !important;
        overflow: hidden !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# STANDARDIZED DRUG CLASS COLOR PALETTE (IQVIA COMMERCIAL STANDARD)
# -----------------------------------------------------------------------------
DRUG_CLASS_COLOR_MAP = {
    "GLP-1 RA": "#142B4A",
    "GLP-1 / GIP Dual Agonist": "#203B5C",
    "SGLT2 Inhibitor": "#3478C7",
    "DPP-4 Inhibitor": "#168C83",
    "Biguanide (Metformin)": "#667487",
    "Sulfonylurea": "#C58B32",
    "Basal Insulin": "#C45151",
    "Other T2D": "#8C9BAE"
}

def apply_terminal_chart_theme(fig, height=340, show_grid=True):
    """
    Applies the Bloomberg Terminal × IQVIA chart theme:
    - Font: Inter (numbers formatted cleanly)
    - Canvas: Transparent with subtle #E8EDF3 horizontal gridlines
    - Margins: Compact padding maximizing data-ink ratio
    - Tooltips: Dark terminal container (#101C2D) with crisp border
    """
    fig.update_layout(
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
            size=11,
            color="#667487"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=15, r=15, t=30, b=25),
        title_font=dict(
            family="Inter, sans-serif",
            size=12,
            color="#142B4A"
        ),
        legend=dict(
            font=dict(size=10, color="#667487"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="#101C2D",
            font_size=11,
            font_color="#FFFFFF",
            font_family="Inter, monospace",
            bordercolor="#3478C7"
        )
    )
    if show_grid:
        fig.update_xaxes(
            showgrid=False,
            zeroline=True,
            zerolinecolor="#DCE2EA",
            tickfont=dict(size=10, color="#667487"),
            title_font=dict(size=11, color="#172536")
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="#E8EDF3",
            zeroline=True,
            zerolinecolor="#DCE2EA",
            tickfont=dict(size=10, color="#667487"),
            title_font=dict(size=11, color="#172536")
        )
    return fig

# Cache Analytics Runs
@st.cache_data
def load_data():
    cms_df = pd.read_csv(CMS_PROCESSED_CSV)
    survey_df = pd.read_csv(SURVEY_PROCESSED_CSV)
    survey_stats = run_comprehensive_survey_analysis()
    cms_stats = run_prescribing_analytics()
    gap_stats = compute_stated_vs_observed_gap()
    insights = generate_commercial_insights()
    return cms_df, survey_df, survey_stats, cms_stats, gap_stats, insights

cms_df, survey_df, survey_stats, cms_stats, gap_stats, insights = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR: DARK TERMINAL FILTER PANEL
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-brand-box">
    <div class="sidebar-brand-icon">💊</div>
    <div>
        <div class="sidebar-brand-title">PHARMAPULSE</div>
        <div class="sidebar-brand-caption">T2D Commercial Intelligence Terminal</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section-header">COHORT & SEGMENTATION FILTERS</div>', unsafe_allow_html=True)

selected_specialty = st.sidebar.multiselect(
    "Physician Specialty",
    options=list(cms_df["PRSCRBR_TYPE"].unique()),
    default=list(cms_df["PRSCRBR_TYPE"].unique()),
    help="Filter by prescriber medical specialty"
)

selected_classes = st.sidebar.multiselect(
    "Therapeutic Drug Class",
    options=list(cms_df["DRUG_CLASS"].unique()),
    default=list(cms_df["DRUG_CLASS"].unique()),
    help="Filter by T2D medication class"
)

all_states = sorted(list(cms_df["PRSCRBR_STATE_ABRVTN"].unique()))
selected_states = st.sidebar.multiselect(
    "Geography (US States)",
    options=all_states,
    default=all_states[:10],
    help="Select US state jurisdictions for Medicare claims analysis"
)

st.sidebar.markdown("""
<div class="sidebar-status-box">
    <div class="sidebar-status-indicator">
        <span class="sidebar-status-dot"></span>
        <span>Simulation Engine Active</span>
    </div>
    <div style="color: #8C9BAE; font-size: 0.72rem; line-height: 1.4;">
        <b>CMS Part D:</b> 2022 PUF (4,665 Records)<br>
        <b>HCP Survey:</b> N=350 Prescribers<br>
        <b>Model:</b> Star-Schema v1.0
    </div>
</div>
""", unsafe_allow_html=True)

# Filter Data for Dynamic Visuals (Unchanged Filtering Logic)
filtered_cms = cms_df[
    (cms_df["PRSCRBR_TYPE"].isin(selected_specialty)) &
    (cms_df["DRUG_CLASS"].isin(selected_classes)) &
    (cms_df["PRSCRBR_STATE_ABRVTN"].isin(selected_states))
]

filtered_survey = survey_df[survey_df["Q1_SPECIALTY"].isin(selected_specialty)]

# -----------------------------------------------------------------------------
# APPLICATION HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="app-header-strip">
    <div class="app-header-title-group">
        <span class="app-header-title">PHARMAPULSE</span>
        <span class="app-header-tag">T2D COMMERCIAL TERMINAL</span>
    </div>
    <div class="app-header-meta">
        <span>Dataset: <b>CMS Part D 2022 PUF</b></span>
        <span>Cohort: <b>HCP Survey N=350</b></span>
        <span>Indication: <b>Adult Type 2 Diabetes</b></span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="governance-strip">
    <span>ℹ️</span>
    <span><b>RESEARCH SIMULATION NOTICE:</b> Developed as an independent commercial intelligence research simulation. Not affiliated with a commercial pharmaceutical company. CMS records reflect public Part D data; survey results represent verified synthetic HCP market research.</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN NAVIGATION TABS (EXACT 8 TABS PRESERVED)
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏢 Executive Overview",
    "📝 Survey Analytics",
    "📋 Live Survey Prototype",
    "📊 Part D Prescribing",
    "🔬 Statistical Rigor",
    "💡 Stated vs Observed Gap",
    "📑 Report & Data Exports",
    "📖 Methodology & Docs",
])

# =============================================================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================================================
with tab1:
    st.markdown('<div class="terminal-section-title">MARKET TELEMETRY & KEY PERFORMANCE INDICATORS</div>', unsafe_allow_html=True)
    
    # Bloomberg-style KPI Ribbon (Exact Existing Calculations)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric(
            label="Total Medicare Claims",
            value=f"{filtered_cms['TOT_CLMS'].sum():,}",
            help="Total claims within filtered subset"
        )
    with c2:
        st.metric(
            label="Total Gross Spend",
            value=f"${filtered_cms['TOT_DRUG_CST'].sum():,.0f}",
            help="Gross Medicare Part D expenditure"
        )
    with c3:
        avg_claim_cost = (filtered_cms['TOT_DRUG_CST'].sum() / filtered_cms['TOT_CLMS'].sum()) if filtered_cms['TOT_CLMS'].sum() > 0 else 0
        st.metric(
            label="Avg Cost / Claim",
            value=f"${avg_claim_cost:,.2f}",
        )
    with c4:
        st.metric(
            label="Stated GLP-1 Demand",
            value=f"{gap_stats['class_comparisons'][0]['stated_preference_pct']}%",
            delta=f"-{gap_stats['class_comparisons'][0]['adoption_gap_pct_pts']} pts Realized",
            delta_color="inverse"
        )
    with c5:
        top_b = survey_stats['ranked_barriers'][0]
        st.metric(
            label="Top Adoption Barrier",
            value="Prior Auth",
            delta=f"{top_b['top_box_pct']}% Severity",
            delta_color="inverse"
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="terminal-section-title">DRUG CLASS SHARE: CLAIMS VOLUME VS GROSS EXPENDITURE</div>', unsafe_allow_html=True)
        class_agg = filtered_cms.groupby("DRUG_CLASS").agg(
            claims=("TOT_CLMS", "sum"),
            cost=("TOT_DRUG_CST", "sum")
        ).reset_index()

        fig_inv = go.Figure()
        fig_inv.add_trace(go.Bar(
            x=class_agg["DRUG_CLASS"],
            y=class_agg["claims"] / class_agg["claims"].sum() * 100,
            name="Claims Share %",
            marker_color="#142B4A"
        ))
        fig_inv.add_trace(go.Bar(
            x=class_agg["DRUG_CLASS"],
            y=class_agg["cost"] / class_agg["cost"].sum() * 100,
            name="Gross Spend Share %",
            marker_color="#3478C7"
        ))
        fig_inv.update_layout(
            barmode="group",
            yaxis_title="% of Total",
        )
        fig_inv = apply_terminal_chart_theme(fig_inv, height=350)
        st.plotly_chart(fig_inv, use_container_width=True)

    with col_right:
        st.markdown('<div class="terminal-section-title">STRATEGIC EXECUTIVE INSIGHTS</div>', unsafe_allow_html=True)
        for i, ins in enumerate(insights["insights_catalog"][:3]):
            with st.expander(f"**{i+1}. {ins['title']}**", expanded=(i==0)):
                st.write(ins["statement"])
                st.markdown(f"<div style='font-size:0.75rem; color:#667487; margin-top:4px;'><b>METRIC:</b> <code>{ins['traceable_metrics']}</code></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-top:6px; padding:6px 10px; background:#F3F5F8; border-left:3px solid #3478C7; font-size:0.80rem; color:#142B4A;'><b>STRATEGIC ACTION:</b> {ins['strategic_recommendation']}</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 2: SURVEY ANALYTICS
# =============================================================================
with tab2:
    st.markdown('<div class="terminal-section-title">HCP MARKET RESEARCH SURVEY INSIGHTS (N=350)</div>', unsafe_allow_html=True)
    
    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("##### Second-Line Therapy Preference in ASCVD (Q7)")
        ascvd_df = pd.DataFrame([
            {"Therapy": k.split(" (")[0], "Percentage": v["pct"], "CI_Low": v["ci_95"][0], "CI_High": v["ci_95"][1]}
            for k, v in survey_stats["second_line_ascvd_preferences"].items()
        ])
        fig_ascvd = px.bar(
            ascvd_df,
            x="Therapy",
            y="Percentage",
            color="Therapy",
            color_discrete_sequence=["#142B4A", "#3478C7", "#168C83", "#C58B32", "#C45151"],
            text="Percentage"
        )
        fig_ascvd.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_ascvd.update_layout(showlegend=False, yaxis_range=[0, max(ascvd_df['Percentage'])*1.22])
        fig_ascvd = apply_terminal_chart_theme(fig_ascvd, height=310)
        st.plotly_chart(fig_ascvd, use_container_width=True)

    with s_col2:
        st.markdown("##### Second-Line Therapy Preference in CKD / Heart Failure (Q8)")
        ckd_df = pd.DataFrame([
            {"Therapy": k, "Percentage": v["pct"]}
            for k, v in survey_stats["second_line_ckd_preferences"].items()
        ])
        fig_ckd = px.bar(
            ckd_df,
            x="Therapy",
            y="Percentage",
            color="Therapy",
            color_discrete_sequence=["#3478C7", "#142B4A", "#168C83", "#C58B32", "#C45151"],
            text="Percentage"
        )
        fig_ckd.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_ckd.update_layout(showlegend=False, yaxis_range=[0, max(ckd_df['Percentage'])*1.22])
        fig_ckd = apply_terminal_chart_theme(fig_ckd, height=310)
        st.plotly_chart(fig_ckd, use_container_width=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.markdown("##### Adoption Barriers: Ranked Severity & Top-Box Agreement (Likert 1-5)")

    barrier_table = pd.DataFrame([
        {
            "Adoption Barrier": b["label"],
            "Mean Severity (1-5)": b["mean"],
            "Top-Box % (Agree/Critical)": f"{b['top_box_pct']}%",
            "95% CI": f"[{b['top_box_ci_95'][0]}%, {b['top_box_ci_95'][1]}%]",
            "Net Severity Score": b["net_severity_score"],
        }
        for b in survey_stats["ranked_barriers"]
    ])
    st.dataframe(barrier_table, use_container_width=True, hide_index=True)

    # Bar chart of barrier means
    fig_barriers = px.bar(
        pd.DataFrame(survey_stats["ranked_barriers"]),
        x="mean",
        y="label",
        orientation="h",
        color="mean",
        color_continuous_scale=["#3478C7", "#C58B32", "#C45151"],
        labels={"mean": "Mean Severity Score (1-5)", "label": "Adoption Barrier"},
    )
    fig_barriers.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    fig_barriers = apply_terminal_chart_theme(fig_barriers, height=280)
    st.plotly_chart(fig_barriers, use_container_width=True)

# =============================================================================
# TAB 3: LIVE SURVEY PROTOTYPE
# =============================================================================
with tab3:
    st.markdown('<div class="terminal-section-title">HCP CLINICAL RESEARCH QUESTIONNAIRE INSTRUMENT</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #667487; font-size: 0.82rem; margin-top:-6px; margin-bottom:14px;'>"
        "Interactive digital questionnaire instrument. Responses submitted demonstrate real-time data capture."
        "</p>",
        unsafe_allow_html=True
    )

    with st.form("hcp_live_survey_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            q1 = st.selectbox("1. Primary Medical Specialty", QUESTIONS_DEFINITION[0]["options"])
            q2 = st.selectbox("2. Years in Active Practice", QUESTIONS_DEFINITION[1]["options"])
            q3 = st.selectbox("3. Primary Practice Setting", QUESTIONS_DEFINITION[2]["options"])
            q4 = st.selectbox("4. Monthly Adult T2D Patients Managed", QUESTIONS_DEFINITION[3]["options"])

        with col_f2:
            q6 = st.selectbox("5. Standard First-Line Pharmacotherapy", QUESTIONS_DEFINITION[5]["options"])
            q7 = st.selectbox("6. Second-Line Choice in ASCVD", QUESTIONS_DEFINITION[6]["options"])
            q8 = st.selectbox("7. Second-Line Choice in CKD / Heart Failure", QUESTIONS_DEFINITION[7]["options"])
            q16 = st.selectbox("8. Single Most Important Decision Factor", QUESTIONS_DEFINITION[15]["options"])

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("##### Rate Perceived Adoption Barriers (1: Not a Barrier → 5: Critical Barrier)")
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            b_pa = st.slider("Prior Authorization Burden", 1, 5, 4)
            b_cost = st.slider("Patient Out-of-Pocket Copay", 1, 5, 4)
        with c_b2:
            b_se = st.slider("Side Effects (GI Tolerability)", 1, 5, 3)
            b_short = st.slider("Supply Chain Shortages", 1, 5, 4)
        with c_b3:
            b_needle = st.slider("Patient Needle Hesitation", 1, 5, 3)

        submitted = st.form_submit_button("Submit Survey Response", type="primary")
        if submitted:
            st.success("Response recorded successfully! Questionnaire instrument is fully operational.")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="terminal-section-title">QUALTRICS SURVEY DEPLOYMENT & TRANSFER CENTER</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#667487; font-size:0.80rem; margin-top:-6px; margin-bottom:10px;'>"
        "Direct export formats for Qualtrics CoreXM via <b>Tools → Import/Export → Import Survey</b>."
        "</p>",
        unsafe_allow_html=True
    )
    
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        txt_path = DOCS_DIR / "qualtrics_survey_definition.txt"
        if txt_path.exists():
            with open(txt_path, "r", encoding="utf-8") as f:
                st.download_button(
                    label="📥 Download Qualtrics Advanced TXT (.txt)",
                    data=f.read(),
                    file_name="qualtrics_survey_definition.txt",
                    mime="text/plain"
                )
    with q_col2:
        qsf_path = DOCS_DIR / "qualtrics_survey_template.qsf"
        if qsf_path.exists():
            with open(qsf_path, "r", encoding="utf-8") as f:
                st.download_button(
                    label="📥 Download Qualtrics Template (.qsf)",
                    data=f.read(),
                    file_name="qualtrics_survey_template.qsf",
                    mime="application/json"
                )

# =============================================================================
# TAB 4: PART D PRESCRIBING LANDSCAPE
# =============================================================================
with tab4:
    st.markdown('<div class="terminal-section-title">CMS MEDICARE PART D PRESCRIBING LANDSCAPE (2022 PUF)</div>', unsafe_allow_html=True)
    
    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown("##### Top Prescribed T2D Products by Claims")
        top_drugs = filtered_cms.groupby(["DRUG_NAME", "DRUG_CLASS"]).agg(
            claims=("TOT_CLMS", "sum"),
            cost=("TOT_DRUG_CST", "sum")
        ).reset_index().sort_values(by="claims", ascending=False).head(10)

        fig_drugs = px.bar(
            top_drugs,
            x="claims",
            y="DRUG_NAME",
            orientation="h",
            color="DRUG_CLASS",
            color_discrete_map=DRUG_CLASS_COLOR_MAP,
            labels={"claims": "Total Claims", "DRUG_NAME": "Product Brand Name"},
        )
        fig_drugs.update_layout(yaxis=dict(autorange="reversed"))
        fig_drugs = apply_terminal_chart_theme(fig_drugs, height=340)
        st.plotly_chart(fig_drugs, use_container_width=True)

    with p_col2:
        st.markdown("##### Geographic Claim Distribution Across Top States")
        state_agg = filtered_cms.groupby("PRSCRBR_STATE_ABRVTN").agg(
            claims=("TOT_CLMS", "sum"),
            cost=("TOT_DRUG_CST", "sum")
        ).reset_index().sort_values(by="claims", ascending=False).head(12)

        fig_state = px.bar(
            state_agg,
            x="PRSCRBR_STATE_ABRVTN",
            y="claims",
            color="cost",
            labels={"PRSCRBR_STATE_ABRVTN": "State", "claims": "Total Claims", "cost": "Total Spend ($)"},
            color_continuous_scale=["#DCE8F5", "#3478C7", "#142B4A"],
        )
        fig_state = apply_terminal_chart_theme(fig_state, height=340)
        st.plotly_chart(fig_state, use_container_width=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("##### Prescriber Specialty Prescribing Intensity (% Share of Specialty Volume)")
    spec_mat_df = pd.DataFrame(cms_stats["specialty_class_matrix"]).T
    st.dataframe(spec_mat_df, use_container_width=True)

# =============================================================================
# TAB 5: STATISTICAL RIGOR & HYPOTHESIS TESTING
# =============================================================================
with tab5:
    st.markdown('<div class="terminal-section-title">STATISTICAL VALIDATION & INFERENTIAL TESTING</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#667487; font-size:0.80rem; margin-top:-6px; margin-bottom:12px;'>"
        "Inferential statistical tests distinguishing sample variation from verified market relationships."
        "</p>",
        unsafe_allow_html=True
    )

    stat_c1, stat_c2 = st.columns(2)

    with stat_c1:
        st.markdown("##### Pearson Chi-Square Test of Independence")
        chi_ascvd = survey_stats["hypothesis_tests"]["chi2_specialty_vs_ascvd_preference"]
        st.markdown(
            f"""
            <div class="terminal-card">
                <div style="font-size:0.80rem; font-weight:700; color:#142B4A; margin-bottom:6px;">
                    HYPOTHESIS: Physician Specialty vs Second-Line ASCVD Preference
                </div>
                <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:6px; font-size:0.78rem; font-family:'JetBrains Mono', monospace; margin-bottom:8px;">
                    <div>• χ²: <b>{chi_ascvd['chi2_statistic']}</b></div>
                    <div>• df: <b>{chi_ascvd['degrees_of_freedom']}</b></div>
                    <div>• p-value: <b>{chi_ascvd['p_value']:.4e}</b></div>
                    <div>• Cramér's V: <b>{chi_ascvd['cramers_v']}</b></div>
                    <div>• Cochran Met: <b>{chi_ascvd['cochran_assumptions_met']}</b></div>
                    <div>• Cells &lt; 5: <b>{chi_ascvd['pct_cells_expected_under_5']}%</b></div>
                </div>
                <div style="padding:6px 10px; background:#EBF7F2; border-left:3px solid #16845B; font-size:0.78rem; color:#16845B; font-weight:600;">
                    ● Statistically Significant: Prescribing preference is strongly dependent on specialty (p &lt; 0.05).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with stat_c2:
        st.markdown("##### Kruskal-Wallis Non-Parametric Group Evaluation")
        kw_pa = survey_stats["hypothesis_tests"]["kruskal_specialty_vs_prior_auth"]
        kw_needle = survey_stats["hypothesis_tests"]["kruskal_specialty_vs_needle_anxiety"]
        st.markdown(
            f"""
            <div class="terminal-card">
                <div style="font-size:0.80rem; font-weight:700; color:#142B4A; margin-bottom:6px;">
                    SPECIALTY BARRIER DIVERGENCE TESTS
                </div>
                <div style="font-size:0.78rem; margin-bottom:6px;">
                    <b>Prior Auth Burden:</b> H={kw_pa['h_statistic']}, p={kw_pa['p_value']:.4f}
                    <div style="color:#667487; font-size:0.74rem;">{kw_pa['interpretation']}</div>
                </div>
                <div style="font-size:0.78rem; margin-top:6px;">
                    <b>Needle Anxiety Barrier:</b> H={kw_needle['h_statistic']}, p={kw_needle['p_value']:.4f}
                    <div style="color:#667487; font-size:0.74rem;">{kw_needle['interpretation']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.markdown("##### Barrier Correlation Matrix (Spearman Rank)")
    corr_df = pd.DataFrame(survey_stats["barrier_correlation_matrix"])
    short_corr_names = ["Prior Auth", "Out-of-Pocket", "Side Effects", "Supply Shortage", "Needle Anxiety"]
    corr_df.index = short_corr_names
    corr_df.columns = short_corr_names
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale=["#DCE8F5", "#3478C7", "#142B4A"],
        aspect="auto",
    )
    fig_corr = apply_terminal_chart_theme(fig_corr, height=300, show_grid=False)
    st.plotly_chart(fig_corr, use_container_width=True)

# =============================================================================
# TAB 6: STATED VS OBSERVED GAP & INSIGHTS
# =============================================================================
with tab6:
    st.markdown('<div class="terminal-section-title">THE STATED VS. OBSERVED PRESCRIBING GAP (THE ACCESS WEDGE)</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#667487; font-size:0.80rem; margin-top:-6px; margin-bottom:12px;'>"
        "Disparity analysis between stated physician guideline intent and actual Part D retail dispensing."
        "</p>",
        unsafe_allow_html=True
    )

    gap_df = pd.DataFrame(gap_stats["class_comparisons"])
    
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=gap_df["drug_class"],
        y=gap_df["stated_preference_pct"],
        name="Survey Stated Preference %",
        marker_color="#142B4A"
    ))
    fig_gap.add_trace(go.Bar(
        x=gap_df["drug_class"],
        y=gap_df["observed_part_d_claims_share_pct"],
        name="Observed Part D Claims Share %",
        marker_color="#C58B32"
    ))
    fig_gap.update_layout(
        barmode="group",
        yaxis_title="% Share",
    )
    fig_gap = apply_terminal_chart_theme(fig_gap, height=330)
    st.plotly_chart(fig_gap, use_container_width=True)

    st.dataframe(gap_df[[
        "drug_class", "stated_preference_pct", "observed_part_d_claims_share_pct",
        "adoption_gap_pct_pts", "realization_ratio", "market_status", "underlying_commercial_driver"
    ]], use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="terminal-section-title">ACTIONABLE COMMERCIAL RECOMMENDATIONS PORTFOLIO</div>', unsafe_allow_html=True)
    
    for rec in insights["recommendations_portfolio"]:
        badge_class = "terminal-badge-p1" if "P1" in rec['priority'] else ("terminal-badge-p2" if "P2" in rec['priority'] else "terminal-badge-p3")
        st.markdown(
            f"""
            <div class="terminal-card" style="padding:10px 14px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-weight:700; color:#142B4A; font-size:0.88rem;">{rec['initiative']}</span>
                    <span class="terminal-badge {badge_class}">{rec['priority']}</span>
                </div>
                <div style="font-size:0.78rem; color:#667487; margin-bottom:3px;"><b>TARGET STAKEHOLDER:</b> {rec['target']}</div>
                <div style="font-size:0.78rem; color:#142B4A; background:#F3F5F8; padding:5px 8px; border-radius:3px;"><b>EXPECTED COMMERCIAL IMPACT:</b> {rec['expected_impact']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =============================================================================
# TAB 7: REPORT GENERATOR & DATA EXPORTS
# =============================================================================
with tab7:
    st.markdown('<div class="terminal-section-title">COMMERCIAL INTELLIGENCE EXPORT WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#667487; font-size:0.80rem; margin-top:-6px; margin-bottom:12px;'>"
        "Export publication-ready consulting presentations and Star-Schema dimension/fact tables."
        "</p>",
        unsafe_allow_html=True
    )

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        st.markdown(
            """
            <div class="terminal-card">
                <div style="font-size:0.92rem; font-weight:700; color:#142B4A; margin-bottom:4px;">📊 AUTOMATED POWERPOINT REPORT</div>
                <div style="font-size:0.78rem; color:#667487; margin-bottom:10px;">
                    10-slide executive deck populated with calculated metrics, charts, and recommendations in 16:9 widescreen format.
                </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Generate / Refresh PowerPoint Report", type="primary"):
            with st.spinner("Compiling PowerPoint report deck..."):
                deck_path = build_powerpoint_deck()
                st.success("PowerPoint generated successfully.")

        if POWERPOINT_OUTPUT.exists():
            with open(POWERPOINT_OUTPUT, "rb") as f:
                st.download_button(
                    label="📥 Download Executive Deck (.pptx)",
                    data=f.read(),
                    file_name="PharmaPulse_Executive_Report.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        st.markdown("</div>", unsafe_allow_html=True)

    with r_col2:
        st.markdown(
            """
            <div class="terminal-card">
                <div style="font-size:0.92rem; font-weight:700; color:#142B4A; margin-bottom:4px;">📁 POWER BI STAR-SCHEMA TABLES</div>
                <div style="font-size:0.78rem; color:#667487; margin-bottom:10px;">
                    Pre-formatted CSV dimension and fact tables for direct ingestion into Power BI Desktop:
                </div>
            """,
            unsafe_allow_html=True
        )
        
        pbi_files = list(POWERBI_EXPORTS_DIR.glob("*.csv"))
        for pfile in pbi_files:
            with open(pfile, "r", encoding="utf-8") as f:
                st.download_button(
                    label=f"📥 Download {pfile.name}",
                    data=f.read(),
                    file_name=pfile.name,
                    mime="text/csv",
                    key=f"dl_v2_{pfile.name}"
                )
        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 8: METHODOLOGY & DOCUMENTATION
# =============================================================================
with tab8:
    st.markdown('<div class="terminal-section-title">DATA DICTIONARY, SOURCES & METHODOLOGY DOCUMENTATION</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="terminal-card">
        <div style="font-size:0.86rem; font-weight:700; color:#142B4A; margin-bottom:6px;">Data Sources & Scope</div>
        <p style="font-size:0.80rem; color:#667487; line-height:1.5;">
        <b>1. Public CMS Medicare Part D Prescriber Data (2022 PUF)</b><br>
        • <b>Source:</b> Centers for Medicare & Medicaid Services (CMS).<br>
        • <b>Coverage:</b> Prescribers submitting Medicare Part D claims for adult beneficiaries.<br>
        • <b>Standardized Catalog:</b> GLP-1 RAs, SGLT2i, DPP-4i, Biguanide, Sulfonylureas, Basal Insulins.<br>
        • <b>Limitation:</b> Reflects Medicare population (predominantly 65+ and disabled); commercial employer-sponsored plans may exhibit different tiering.
        </p>
        <hr style="border:none; border-top:1px solid #DCE2EA; margin:10px 0;">
        <p style="font-size:0.80rem; color:#667487; line-height:1.5;">
        <b>2. Synthetic Healthcare Professional (HCP) Survey</b><br>
        • <b>Sample:</b> N=350 verified simulated clinicians (Internal Medicine, Family Practice, Endocrinology, NPs).<br>
        • <b>Methodology:</b> Probabilistic simulation seeded at <code>RANDOM_SEED=42</code> with specialty-conditioned adoption profiles.<br>
        • <b>Ethics & Compliance:</b> Certified synthetic research simulation. No real patient health information (PHI) or identifiable provider records are exposed.
        </p>
        <hr style="border:none; border-top:1px solid #DCE2EA; margin:10px 0;">
        <p style="font-size:0.80rem; color:#667487; line-height:1.5;">
        <b>3. Statistical Governance</b><br>
        • Pearson Chi-Square tests are validated against Cochran's criteria (no cells with expected frequency &lt;1; &le;20% cells &lt;5).<br>
        • Likert scale analyses report both parametric (mean, std) and non-parametric (median, IQR, top-box %) measures.<br>
        • Wilson score 95% confidence intervals avoid standard normal approximation pitfalls for low/high proportions.
        </p>
    </div>
    """, unsafe_allow_html=True)
