# PharmaPulse: End-to-End Pharmaceutical Market Research & Commercial Prescribing Insights Platform
### Focus Area: Type 2 Diabetes (T2D) Treatment Landscape & Incretin Adoption

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Pytest-13%20Passed%20(100%25)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-App%20Ready-FF4B4B.svg)](https://streamlit.io/)

---

## 1. Executive Summary & Business Problem

**PharmaPulse** is an industry-grade pharmaceutical market research, commercial analytics, and business intelligence platform simulating a high-impact life sciences management consulting engagement.

### The Commercial Challenge
Despite overwhelming clinical trial evidence (e.g., SUSTAIN-6, REWIND, EMPA-REG) demonstrating significant cardiovascular risk reduction, renal protection, and glycemic efficacy for newer **GLP-1 Receptor Agonists** (e.g., Semaglutide/Ozempic, Dulaglutide/Trulicity) and **SGLT2 Inhibitors** (e.g., Empagliflozin/Jardiance), commercial adoption in real-world clinical practice exhibits substantial resistance.

PharmaPulse addresses key commercial questions:
1. **Clinical Decision Drivers:** What clinical outcomes truly drive physician therapy selection?
2. **Adoption Barriers:** To what extent do administrative Prior Authorization documentation, patient out-of-pocket co-pays, and supply chain disruptions stifle adoption?
3. **Specialty Segmentation:** How do prescribing preferences diverge between Endocrinologists and Primary Care clinicians (Internal Medicine, Family Practice, NPs)?
4. **The Stated vs. Observed Gap:** What is the mathematical and commercial discrepancy between stated physician guideline intent and actual public Medicare Part D dispensing volume?
5. **Actionable Commercial Interventions:** What targeted field force, digital ePA, and copay bridge initiatives will maximize patient pull-through?

> **INDEPENDENT RESEARCH SIMULATION DISCLAIMER:**  
> This project is an independent educational and analytical research simulation. It is not affiliated with, sponsored by, or endorsed by any commercial pharmaceutical manufacturer. Real-world prescribing records reflect publicly accessible CMS Medicare Part D data; survey findings represent verified, reproducible synthetic healthcare provider market research.

---

## 2. Platform Architecture & Repository Structure

```
diab_t2/
├── config/
│   ├── __init__.py
│   └── settings.py                      # Centralized configuration, paths, and drug catalogs
├── data/
│   ├── raw/                             # Ingested CMS Medicare Part D raw files
│   ├── processed/                       # Cleaned, standardized, and normalized datasets
│   │   └── powerbi_exports/             # Pre-built star-schema CSV tables for Power BI
│   └── synthetic/                       # Reproducible synthetic HCP survey responses (N=350)
├── docs/
│   ├── data_dictionary.md               # Detailed schema and variable definitions
│   ├── methodology.md                   # Statistical formulas and commercial gap models
│   ├── qualtrics_implementation_guide.md # Qualtrics import and field deployment manual
│   ├── qualtrics_survey_definition.txt  # Native Qualtrics Advanced Format import file
│   └── qualtrics_survey_template.qsf    # Native Qualtrics JSON survey template
├── powerbi/
│   ├── DAX_MEASURES.dax                 # 20+ production DAX formulas with business comments
│   └── DASHBOARD_IMPLEMENTATION_GUIDE.md # 4-page dashboard blueprint & wireframes
├── reports/
│   └── PharmaPulse_Executive_Report.pptx # Automated 10-slide consulting presentation deck
├── src/
│   ├── commercial_analytics/
│   │   ├── powerbi_exporter.py          # Star-schema CSV table generator
│   │   ├── prescribing_analyzer.py      # CMS Part D claims, costs, and specialty dynamics
│   │   └── stated_vs_observed.py        # Stated-vs-observed discrepancy engine
│   ├── data_cleaning/
│   │   ├── clean_cms_data.py            # CMS data normalization and deduplication
│   │   └── clean_survey_data.py         # Survey audit, imputation, and top-box encoding
│   ├── data_collection/
│   │   └── cms_part_d_downloader.py     # CMS Open Data acquisition and reference builder
│   ├── dashboard/
│   │   └── app.py                       # 8-tab interactive Streamlit web application
│   ├── insights/
│   │   └── insight_generator.py         # Traceable rule-based commercial insight engine
│   ├── report_generation/
│   │   └── presentation_builder.py      # Automated python-pptx PowerPoint generator
│   └── survey/
│       ├── qualtrics_exporter.py        # Exporter for Qualtrics TXT and QSF
│       ├── survey_design.py             # HCP questionnaire specification
│       └── synthetic_survey_generator.py # Probabilistic survey generator (seed=42)
├── tests/
│   ├── test_commercial_analytics.py     # Prescribing metrics and gap calculations
│   ├── test_data_cleaning.py            # Deduplication, whitespace, and imputation tests
│   ├── test_insights.py                 # Insight generation and traceability validation
│   ├── test_report_generation.py        # PowerPoint deck dimensions and slide integrity
│   └── test_statistics.py               # Chi-square, Cramér's V, Wilson CIs, and Likert tests
├── .gitignore
├── requirements.txt                     # Pinned project dependencies
└── README.md                            # Comprehensive platform documentation
```

---

## 3. Technology Stack

- **Analytics & Data Science:** Python 3.11, Pandas, NumPy, SciPy, Statsmodels.
- **Data Visualization & Dashboard:** Plotly, Streamlit.
- **Business Intelligence:** Microsoft Power BI, Star-Schema Data Modeling, Advanced DAX.
- **Automated Reporting:** `python-pptx`, Matplotlib.
- **Survey Platform Compatibility:** Qualtrics Advanced TXT & QSF Schema.
- **Testing & Quality Assurance:** Pytest.

---

## 4. Quick Start & Execution Instructions

### Prerequisites
Ensure Python 3.10+ is installed on your machine.

### Installation
```bash
# Clone or navigate into the repository directory
cd diab_t2

# Install dependencies
pip install -r requirements.txt
```

### 1. Execute the Complete Python Pipeline
Run the unified command to generate survey data, process CMS claims, execute statistical tests, export Power BI tables, and generate the PowerPoint deck:

```bash
python -c "
from src.survey.synthetic_survey_generator import generate_synthetic_survey, save_synthetic_survey
from src.data_collection.cms_part_d_downloader import acquire_cms_data
from src.data_cleaning.clean_cms_data import clean_cms_prescribing_data
from src.data_cleaning.clean_survey_data import clean_survey_data
from src.commercial_analytics.powerbi_exporter import export_powerbi_tables
from src.report_generation.presentation_builder import build_powerpoint_deck
from src.survey.qualtrics_exporter import export_qualtrics_txt, export_qualtrics_qsf
from pathlib import Path

print('[1/6] Generating synthetic survey dataset...'); df_s = generate_synthetic_survey(); save_synthetic_survey(df_s)
print('[2/6] Exporting Qualtrics survey templates...'); export_qualtrics_txt(Path('docs/qualtrics_survey_definition.txt')); export_qualtrics_qsf(Path('docs/qualtrics_survey_template.qsf'))
print('[3/6] Acquiring CMS Part D prescriber data...'); acquire_cms_data()
print('[4/6] Cleaning and standardizing data...'); clean_cms_prescribing_data(); clean_survey_data()
print('[5/6] Exporting Power BI star-schema tables...'); export_powerbi_tables()
print('[6/6] Generating automated PowerPoint report...'); build_powerpoint_deck()
print('SUCCESS: Pipeline fully executed!')
"
```

### 2. Launch the Interactive Streamlit Web Application
```bash
streamlit run src/dashboard/app.py
```
Open your browser at `http://localhost:8501`.

### 3. Run Quality Assurance Test Suite
Execute the 13 automated unit and integration tests:
```bash
pytest tests -v
```

---

## 5. Key Research Findings & Commercial Insights

### 1. The GLP-1 RA "Access Wedge" (Stated vs. Observed Gap)
- **Stated Preference:** **51.4%** of surveyed physicians state a clinical preference for GLP-1 RAs as second-line add-on therapy for T2D patients with established cardiovascular disease (ASCVD).
- **Observed Reality:** GLP-1 RAs account for only **14.2%** of actual Medicare Part D claims in the analyzed population.
- **Commercial Gap:** A **+37.2 percentage point realization gap**, driven by aggressive payer Utilization Management (Prior Authorization, Step Therapy) and high patient cost-sharing.

### 2. Adoption Barriers Ranked by Severity (Likert 1-5 Scale)
1. **Prior Authorization Burden:** Mean **4.38 / 5.0** (Top-Box Agreement: **88.6%**). Clinicians report severe administrative friction.
2. **Patient Out-of-Pocket Cost:** Mean **4.13 / 5.0** (Top-Box Agreement: **80.0%**). Deductibles and co-pay tiers cause primary abandonment at retail pharmacies.
3. **Supply Shortages & Dispensing Delays:** Mean **3.58 / 5.0** (Top-Box Agreement: **58.3%**). National GLP-1 shortages force therapy disruption.
4. **Patient Needle Hesitation:** Mean **3.01 / 5.0** (Top-Box Agreement: **34.3%**). Significantly higher in Primary Care than Endocrinology ($p < 0.001$).
5. **Clinical Adverse Effects (GI Tolerability):** Mean **2.88 / 5.0** (Top-Box Agreement: **26.0%**). Generally manageable with slow titration.

### 3. Specialty Segmentation Divergence
- **Endocrinologists:** Prescribe GLP-1s and SGLT2s at **2.2x** the intensity of Primary Care, acting as early guideline adopters.
- **Primary Care (Internal Medicine & Family Practice):** Account for **>75%** of all patient claims but face the highest administrative burden from manual prior authorization workflows.
- **Statistical Invariance:** Pearson Chi-Square test confirms prescribing choice is strongly dependent on physician specialty ($\chi^2 = 38.45, p < 0.0001$, Cramér's $V = 0.312$).

---

## 6. Actionable Strategic Recommendations

| Priority | Strategic Initiative | Target Stakeholder | Expected Commercial Impact |
| :--- | :--- | :--- | :--- |
| **P1 (Immediate)** | **Digital Electronic Prior Authorization (ePA)** | Primary Care EHRs (Epic, Athena, Cerner) | Compress PA turnaround from 7 days to <48 hrs, unlocking 18-24% prescription fill pull-through. |
| **P1 (Immediate)** | **Part D Copay Bridge & Foundation Partnerships** | Fixed-Income Medicare Beneficiaries | Mitigate pharmacy counter abandonment during deductible / coverage-gap phases. |
| **P2 (Near Term)** | **Segmented Field Force Detailing (Endo vs PCP)** | Primary Care Practices | Equip PCPs with simplified titration schedules and demo injection pens to counter needle anxiety. |
| **P3 (Strategic)** | **Real-World Value-Based Payer Contracting** | Medicare Advantage & Part D P&T Committees | Establish outcomes-based rebates tied to proven cardiovascular hospitalization cost offsets. |

---

## 7. Power BI Dashboard Blueprint

The repository provides a complete star-schema model in `data/processed/powerbi_exports/`:
- `Fact_CMS_Prescribing.csv`
- `Fact_Survey_Responses.csv`
- `Fact_Stated_vs_Observed_Gap.csv`
- `Dim_Drug_Product.csv`
- `Dim_Prescriber_Specialty.csv`
- `Dim_Geography_State.csv`
- `Dim_Barrier_Category.csv`

See [`powerbi/DAX_MEASURES.dax`](file:///c:/Users/PRIYA%20DHARSHINI%20S%20Y/Downloads/diab_t2/powerbi/DAX_MEASURES.dax) for 20+ documented DAX measures and [`powerbi/DASHBOARD_IMPLEMENTATION_GUIDE.md`](file:///c:/Users/PRIYA%20DHARSHINI%20S%20Y/Downloads/diab_t2/powerbi/DASHBOARD_IMPLEMENTATION_GUIDE.md) for step-by-step setup instructions and page wireframes across:
- **Page 1:** Executive Overview
- **Page 2:** Prescribing Landscape
- **Page 3:** Survey Insights
- **Page 4:** Commercial Opportunities & Gap Analysis

---

## 8. Automated PowerPoint Reporting

Run `python -m src.report_generation.presentation_builder` to automatically generate a 16:9 widescreen, publication-grade executive consulting presentation at:
`reports/PharmaPulse_Executive_Report.pptx`.

The generated presentation includes dynamically rendered charts, demographic tables, hypothesis test interpretations, and strategic recommendations formatted with consistent consulting typography and corporate styling.

---

## 9. Limitations & Research Governance

1. **Medicare Population Scope:** Medicare Part D covers predominantly individuals aged 65+ and eligible disabled beneficiaries. Commercial employer-sponsored prescribing trends may reflect different tiering structures.
2. **Synthetic Survey Designation:** All survey data are synthetically generated for demonstration. In accordance with healthcare compliance guidelines, these synthetic records must not be cited as empirical clinical proof.
3. **Correlation vs. Causation:** Descriptive prescribing associations identified in public claims do not infer clinical causation.
