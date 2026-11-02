"""
PharmaPulse – Type 2 Diabetes Commercial Market Research & Prescribing Analytics Platform
Interactive Streamlit Web Application
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
    page_title="PharmaPulse | T2D Commercial Analytics",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1A365D;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .disclaimer-banner {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.88rem;
        color: #1E40AF;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #F1F5F9;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A365D !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

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

# Sidebar Controls
st.sidebar.image("https://img.icons8.com/fluency/96/pill.png", width=64)
st.sidebar.title("PharmaPulse T2D")
st.sidebar.caption("Commercial Intelligence Platform v1.0")

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

selected_specialty = st.sidebar.multiselect(
    "Physician Specialty",
    options=list(cms_df["PRSCRBR_TYPE"].unique()),
    default=list(cms_df["PRSCRBR_TYPE"].unique())
)

selected_classes = st.sidebar.multiselect(
    "Drug Class",
    options=list(cms_df["DRUG_CLASS"].unique()),
    default=list(cms_df["DRUG_CLASS"].unique())
)

all_states = sorted(list(cms_df["PRSCRBR_STATE_ABRVTN"].unique()))
selected_states = st.sidebar.multiselect(
    "Geography (US States)",
    options=all_states,
    default=all_states[:10]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Simulation Mode Active**\n\n"
    "Public CMS Medicare Part D 2022 Data + Verified Synthetic Survey (N=350)."
)

# Filter Data for Dynamic Visuals
filtered_cms = cms_df[
    (cms_df["PRSCRBR_TYPE"].isin(selected_specialty)) &
    (cms_df["DRUG_CLASS"].isin(selected_classes)) &
    (cms_df["PRSCRBR_STATE_ABRVTN"].isin(selected_states))
]

filtered_survey = survey_df[survey_df["Q1_SPECIALTY"].isin(selected_specialty)]

# Header
st.markdown('<p class="main-header">PharmaPulse – Type 2 Diabetes Commercial Insights Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">End-to-End Pharmaceutical Market Research, HCP Perceptions & Medicare Part D Real-World Prescribing Analytics</p>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-banner">
    <b>INDEPENDENT RESEARCH SIMULATION:</b> This platform is developed as an independent commercial research simulation. 
    It is not sponsored by or affiliated with an actual pharmaceutical enterprise. CMS records reflect Medicare Part D public data; 
    survey findings represent reproducible synthetic HCP market research.
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
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
    st.subheader("Executive Market Overview & Key Performance Indicators")
    
    # KPI Metrics Row
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
            delta=f"{top_b['top_box_pct']}% High Severity",
            delta_color="inverse"
        )

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### Drug Class Market Share: Claims Volume vs Gross Expenditure")
        class_agg = filtered_cms.groupby("DRUG_CLASS").agg(
            claims=("TOT_CLMS", "sum"),
            cost=("TOT_DRUG_CST", "sum")
        ).reset_index()

        fig_inv = go.Figure()
        fig_inv.add_trace(go.Bar(
            x=class_agg["DRUG_CLASS"],
            y=class_agg["claims"] / class_agg["claims"].sum() * 100,
            name="Claims Share %",
            marker_color="#1A365D"
        ))
        fig_inv.add_trace(go.Bar(
            x=class_agg["DRUG_CLASS"],
            y=class_agg["cost"] / class_agg["cost"].sum() * 100,
            name="Gross Spend Share %",
            marker_color="#0284C7"
        ))
        fig_inv.update_layout(
            barmode="group",
            yaxis_title="% of Total",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=30, b=20),
            height=360
        )
        st.plotly_chart(fig_inv, use_container_width=True)

    with col_right:
        st.markdown("#### Top Executive Insights & Strategic Takeaways")
        for i, ins in enumerate(insights["insights_catalog"][:3]):
            with st.expander(f"**{i+1}. {ins['title']}**", expanded=(i==0)):
                st.write(ins["statement"])
                st.caption(f"**Metric:** `{ins['traceable_metrics']}` | **Source:** {ins['evidence_sources'][0]}")
                st.markdown(f"**Strategic Action:** {ins['strategic_recommendation']}")

# =============================================================================
# TAB 2: SURVEY ANALYTICS
# =============================================================================
with tab2:
    st.subheader("HCP Market Research Survey Insights (N=350)")
    
    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("#### Second-Line Therapy Preference in ASCVD (Q7)")
        ascvd_df = pd.DataFrame([
            {"Therapy": k.split(" (")[0], "Percentage": v["pct"], "CI_Low": v["ci_95"][0], "CI_High": v["ci_95"][1]}
            for k, v in survey_stats["second_line_ascvd_preferences"].items()
        ])
        fig_ascvd = px.bar(
            ascvd_df,
            x="Therapy",
            y="Percentage",
            color="Therapy",
            color_discrete_sequence=["#1A365D", "#0284C7", "#94A3B8", "#F59E0B", "#64748B"],
            text="Percentage"
        )
        fig_ascvd.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_ascvd.update_layout(showlegend=False, height=340, yaxis_range=[0, max(ascvd_df['Percentage'])*1.2])
        st.plotly_chart(fig_ascvd, use_container_width=True)

    with s_col2:
        st.markdown("#### Second-Line Therapy Preference in CKD / Heart Failure (Q8)")
        ckd_df = pd.DataFrame([
            {"Therapy": k, "Percentage": v["pct"]}
            for k, v in survey_stats["second_line_ckd_preferences"].items()
        ])
        fig_ckd = px.bar(
            ckd_df,
            x="Therapy",
            y="Percentage",
            color="Therapy",
            color_discrete_sequence=["#0284C7", "#1A365D", "#94A3B8", "#F59E0B", "#64748B"],
            text="Percentage"
        )
        fig_ckd.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_ckd.update_layout(showlegend=False, height=340, yaxis_range=[0, max(ckd_df['Percentage'])*1.2])
        st.plotly_chart(fig_ckd, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Adoption Barriers: Ranked Severity & Top-Box Agreement (Likert 1-5)")

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
        color_continuous_scale="Reds",
        labels={"mean": "Mean Severity Score (1-5)", "label": "Adoption Barrier"},
        height=320
    )
    fig_barriers.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    st.plotly_chart(fig_barriers, use_container_width=True)

# =============================================================================
# TAB 3: LIVE SURVEY PROTOTYPE
# =============================================================================
with tab3:
    st.subheader("Interactive Healthcare Professional (HCP) Survey Prototype")
    st.markdown(
        "Experience the survey instrument used to collect prescriber insights. "
        "Responses submitted here demonstrate interactive data capture."
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
            st.success("✅ Response recorded successfully! Survey instrument is fully operational.")

    st.markdown("---")
    st.markdown("#### Qualtrics Transfer & Integration Center")
    st.markdown("To import this survey into Qualtrics:")
    st.markdown("1. Download the **Qualtrics Advanced TXT Definition** or **QSF Schema** below.")
    st.markdown("2. In Qualtrics, go to **Tools → Import/Export → Import Survey → From a text file**.")
    
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
    st.subheader("CMS Medicare Part D Prescribing Landscape")
    
    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown("#### Top Prescribed T2D Products by Claims")
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
            labels={"claims": "Total Claims", "DRUG_NAME": "Product Brand Name"},
            height=380
        )
        fig_drugs.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_drugs, use_container_width=True)

    with p_col2:
        st.markdown("#### Geographic Claim Distribution Across Top States")
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
            color_continuous_scale="Viridis",
            height=380
        )
        st.plotly_chart(fig_state, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Prescriber Specialty Prescribing Intensity")
    spec_mat_df = pd.DataFrame(cms_stats["specialty_class_matrix"]).T
    st.dataframe(spec_mat_df, use_container_width=True)

# =============================================================================
# TAB 5: STATISTICAL RIGOR & HYPOTHESIS TESTING
# =============================================================================
with tab5:
    st.subheader("Statistical Validation & Inferential Testing")
    st.markdown("Distinguishing descriptive observations from statistically verified relationships.")

    stat_c1, stat_c2 = st.columns(2)

    with stat_c1:
        st.markdown("#### Pearson Chi-Square Test of Independence")
        chi_ascvd = survey_stats["hypothesis_tests"]["chi2_specialty_vs_ascvd_preference"]
        st.markdown(f"**Test:** Physician Specialty vs Second-Line ASCVD Preference")
        st.markdown(f"• **Chi-Square Statistic ($\chi^2$):** `{chi_ascvd['chi2_statistic']}`")
        st.markdown(f"• **Degrees of Freedom:** `{chi_ascvd['degrees_of_freedom']}`")
        st.markdown(f"• **p-value:** `{chi_ascvd['p_value']:.4e}`")
        st.markdown(f"• **Effect Size (Cramér's V):** `{chi_ascvd['cramers_v']}`")
        st.markdown(f"• **Cochran Assumptions Met:** `{chi_ascvd['cochran_assumptions_met']}` (Cells < 5: {chi_ascvd['pct_cells_expected_under_5']}%)")
        
        if chi_ascvd["is_statistically_significant"]:
            st.success("✅ **Statistically Significant Relationship:** Prescribing preference is strongly dependent on physician specialty.")
        else:
            st.warning("No significant relationship.")

    with stat_c2:
        st.markdown("#### Kruskal-Wallis Non-Parametric Evaluation")
        kw_pa = survey_stats["hypothesis_tests"]["kruskal_specialty_vs_prior_auth"]
        st.markdown(f"**Test:** Prior Auth Burden across Specialties")
        st.markdown(f"• **H-Statistic:** `{kw_pa['h_statistic']}`")
        st.markdown(f"• **p-value:** `{kw_pa['p_value']:.4f}`")
        st.markdown(f"• **Conclusion:** {kw_pa['interpretation']}")

        kw_needle = survey_stats["hypothesis_tests"]["kruskal_specialty_vs_needle_anxiety"]
        st.markdown(f"\n**Test:** Needle Hesitation Barrier across Specialties")
        st.markdown(f"• **H-Statistic:** `{kw_needle['h_statistic']}`")
        st.markdown(f"• **p-value:** `{kw_needle['p_value']:.4f}`")
        st.markdown(f"• **Conclusion:** {kw_needle['interpretation']}")

    st.markdown("---")
    st.markdown("#### Barrier Correlation Matrix (Spearman Rank)")
    corr_df = pd.DataFrame(survey_stats["barrier_correlation_matrix"])
    short_corr_names = ["Prior Auth", "Out-of-Pocket", "Side Effects", "Supply Shortage", "Needle Anxiety"]
    corr_df.index = short_corr_names
    corr_df.columns = short_corr_names
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="Blues",
        aspect="auto",
        height=340
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# =============================================================================
# TAB 6: STATED VS OBSERVED GAP & INSIGHTS
# =============================================================================
with tab6:
    st.subheader("The Stated vs. Observed Prescribing Gap")
    st.markdown("Bridging the clinical guideline preference with real-world Medicare dispensing.")

    gap_df = pd.DataFrame(gap_stats["class_comparisons"])
    
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=gap_df["drug_class"],
        y=gap_df["stated_preference_pct"],
        name="Survey Stated Preference %",
        marker_color="#1A365D"
    ))
    fig_gap.add_trace(go.Bar(
        x=gap_df["drug_class"],
        y=gap_df["observed_part_d_claims_share_pct"],
        name="Observed Part D Claims Share %",
        marker_color="#D97706"
    ))
    fig_gap.update_layout(
        barmode="group",
        yaxis_title="% Share",
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    st.dataframe(gap_df[[
        "drug_class", "stated_preference_pct", "observed_part_d_claims_share_pct",
        "adoption_gap_pct_pts", "realization_ratio", "market_status", "underlying_commercial_driver"
    ]], use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Actionable Commercial Recommendations Portfolio")
    for rec in insights["recommendations_portfolio"]:
        st.markdown(f"##### 🎯 {rec['priority']} — {rec['initiative']}")
        st.markdown(f"• **Target Stakeholder:** {rec['target']}")
        st.markdown(f"• **Expected Commercial Impact:** {rec['expected_impact']}")

# =============================================================================
# TAB 7: REPORT GENERATOR & DATA EXPORTS
# =============================================================================
with tab7:
    st.subheader("Deliverable Export Center")
    st.markdown("Generate and download publication-ready executive decks and Power BI star-schema tables.")

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        st.markdown("#### 📊 Automated PowerPoint Presentation")
        st.markdown("A 10-slide executive deck populated with calculated metrics, charts, and strategic recommendations.")
        
        if st.button("Generate / Refresh PowerPoint Report", type="primary"):
            with st.spinner("Building executive presentation deck..."):
                deck_path = build_powerpoint_deck()
                st.success("PowerPoint generated successfully!")

        if POWERPOINT_OUTPUT.exists():
            with open(POWERPOINT_OUTPUT, "rb") as f:
                st.download_button(
                    label="📥 Download Executive Presentation (.pptx)",
                    data=f.read(),
                    file_name="PharmaPulse_Executive_Report.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

    with r_col2:
        st.markdown("#### 📁 Power BI Star-Schema Datasets")
        st.markdown("Pre-formatted CSV files ready for direct ingestion into Power BI:")
        
        pbi_files = list(POWERBI_EXPORTS_DIR.glob("*.csv"))
        for pfile in pbi_files:
            with open(pfile, "r", encoding="utf-8") as f:
                st.download_button(
                    label=f"📥 Download {pfile.name}",
                    data=f.read(),
                    file_name=pfile.name,
                    mime="text/csv",
                    key=f"dl_{pfile.name}"
                )

# =============================================================================
# TAB 8: METHODOLOGY & DOCUMENTATION
# =============================================================================
with tab8:
    st.subheader("Data Dictionary, Sources & Methodology Documentation")

    st.markdown("""
    ### Data Sources & Scope
    1. **Public CMS Medicare Part D Prescriber Data (2022 PUF)**
       - **Source:** Centers for Medicare & Medicaid Services (CMS).
       - **Coverage:** Prescribers submitting Medicare Part D claims for adult beneficiaries.
       - **Standardized Drug Catalog:** GLP-1 RAs (Semaglutide, Dulaglutide, Tirzepatide, Liraglutide), SGLT2i (Empagliflozin, Dapagliflozin, Canagliflozin), DPP-4i (Sitagliptin, Linagliptin), Biguanide (Metformin), Sulfonylureas (Glimepiride, Glipizide), Basal Insulins (Glargine, Degludec).
       - **Limitation:** Medicare Part D covers predominantly individuals aged 65+ and disabled adults; commercial employer-sponsored prescribing trends may differ.
    
    2. **Synthetic Healthcare Professional (HCP) Survey**
       - **Sample:** N=350 verified simulated clinicians (Internal Medicine, Family Practice, Endocrinology, NPs).
       - **Methodology:** Probabilistic simulation seeded at `RANDOM_SEED=42` with specialty-conditioned adoption profiles.
       - **Ethics & Compliance:** Certified synthetic research simulation. No real patient health information (PHI) or identifiable provider records are exposed.
    
    3. **Statistical Governance**
       - Pearson Chi-Square tests are validated against Cochran's criteria (no cells with expected frequency <1; <=20% cells <5).
       - Likert scale analyses report both parametric (mean, std) and non-parametric (median, IQR, top-box %) measures.
       - Wilson score 95% confidence intervals avoid standard normal approximation pitfalls for low/high proportions.
    """)
