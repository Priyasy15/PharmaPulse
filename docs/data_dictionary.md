# PharmaPulse Data Dictionary
## Type 2 Diabetes Commercial Insights Platform

This document describes all variables, dimensions, indicators, and metrics utilized across the CMS Medicare Part D prescribing pipeline and the Healthcare Professional (HCP) survey dataset.

---

## 1. CMS Medicare Part D Prescribing Dataset

Data source: Centers for Medicare & Medicaid Services (CMS) Medicare Part D Prescribers Public Use File (PUF).  
Reporting Year: 2022.

| Column Name | Data Type | Description | Values / Range |
| :--- | :--- | :--- | :--- |
| `PRSCRBR_NPI` | Integer (10-digit) | National Provider Identifier of the prescribing clinician | 1000000000 - 9999999999 |
| `PRSCRBR_LAST_ORG_NAME`| String | Clinician last name or organizational practice name | Standardized Uppercase |
| `PRSCRBR_FIRST_NAME` | String | Clinician first name | Standardized Uppercase |
| `PRSCRBR_CITY` | String | Prescribing practice city location | Text |
| `PRSCRBR_STATE_ABRVTN` | String (2-letter) | US Postal State Abbreviation | 50 US States |
| `PRSCRBR_TYPE` | String | Primary medical specialty of the prescriber | Internal Medicine, Family Practice, Endocrinology, Diabetes & Metabolism, Nurse Practitioner |
| `DRUG_NAME` | String | Trade / brand name of medication as submitted on Part D claim | e.g., OZEMPIC, JARDIANCE, JANUVIA, METFORMIN HCL |
| `GENERIC_NAME` | String | Active chemical compound / generic entity | e.g., SEMAGLUTIDE, EMPAGLIFLOZIN, SITAGLIPTIN |
| `CANONICAL_GENERIC` | String | Standardized generic name mapped via drug catalog | Unified Generic Compound |
| `DRUG_CLASS` | String | Therapeutic drug classification | GLP-1 RA, SGLT2 Inhibitor, DPP-4 Inhibitor, Biguanide (Metformin), Sulfonylurea, Basal Insulin |
| `ADMINISTRATION_ROUTE` | String | Clinical delivery mechanism | Oral, Subcutaneous |
| `FORMULARY_TIER` | String | Standard Part D formulary tiering classification | Tier 1 (Generic), Tier 2/3 (Brand), Specialty |
| `IS_NEWER_THERAPY` | Boolean | Flag indicating modern incretin / SGLT2 therapy | TRUE (GLP-1 RA, SGLT2i), FALSE (Legacy) |
| `TOT_CLMS` | Integer | Total Medicare Part D claims dispensed (including original and refills) | >= 11 (CMS privacy threshold) |
| `TOT_30DAY_FILLS` | Integer | Standardized 30-day supply fills | Calculated by CMS |
| `TOT_DRUG_CST` | Decimal ($) | Gross total drug expenditure paid by Part D plan, beneficiary, and subsidies | Numeric |
| `TOT_BENES` | Integer | Total unique Medicare beneficiaries who filled the medication | >= 11 |
| `YEAR` | Integer | CMS Reporting Calendar Year | 2022 |
| `COST_PER_CLAIM` | Decimal ($) | Derived metric: `TOT_DRUG_CST / TOT_CLMS` | Positive Decimal |
| `COST_PER_30DAY_FILL`| Decimal ($) | Derived metric: `TOT_DRUG_CST / TOT_30DAY_FILLS` | Positive Decimal |

---

## 2. Healthcare Professional (HCP) Survey Dataset

Design: Quantitative web survey measuring clinical treatment preferences and perceived adoption barriers.  
Sample: N=350 verified clinicians (Internal Medicine, Family Practice, Endocrinology, NPs).  
Data Flag: `IS_SYNTHETIC = TRUE` (Certified reproducible synthetic simulation).

| Column Name | Question Reference | Data Type | Description | Valid Choices / Values |
| :--- | :--- | :--- | :--- | :--- |
| `RESPONDENT_ID` | System Key | String | Unique respondent identifier | `HCP_T2D_0001` - `HCP_T2D_0350` |
| `Q1_SPECIALTY` | Q1 | Categorical | Primary medical specialty | Internal Medicine, Family Practice, Endocrinology, Diabetes & Metabolism, Nurse Practitioner |
| `Q2_YEARS_EXPERIENCE`| Q2 | Categorical | Post-training clinical experience | `<5 years`, `5-10 years`, `11-20 years`, `>20 years` |
| `Q3_PRACTICE_SETTING` | Q3 | Categorical | Clinical practice organizational model | Academic Medical Center, Community Hospital System, Private Group Practice, Solo Practice, FQHC / Community Clinic |
| `Q4_MONTHLY_T2D_PATIENTS`| Q4 | Categorical | Average monthly adult T2D patient volume | `15-30`, `31-60`, `61-100`, `>100` |
| `Q5_PCT_MEDICARE_PATIENTS`| Q5 | Categorical | Estimated percentage of patient panel insured by Medicare | `<25%`, `25-50%`, `51-75%`, `>75%` |
| `Q6_FIRST_LINE_PREFERENCE`| Q6 | Categorical | Standard initial pharmacotherapy for newly diagnosed T2D | Metformin Monotherapy, Metformin + SGLT2i, Metformin + GLP-1 RA, SGLT2i Monotherapy, GLP-1 Monotherapy, DPP-4i Monotherapy |
| `Q7_SECOND_LINE_ASCVD_PREFERENCE`| Q7 | Categorical | Preferred add-on therapy for patient with established ASCVD | GLP-1 Receptor Agonist, SGLT2 Inhibitor, DPP-4 Inhibitor, Sulfonylurea, Basal Insulin |
| `Q8_SECOND_LINE_CKD_HF_PREFERENCE`| Q8 | Categorical | Preferred add-on therapy for patient with CKD or Heart Failure | SGLT2 Inhibitor, GLP-1 Receptor Agonist, DPP-4 Inhibitor, Sulfonylurea, Basal Insulin |
| `Q9_FAMILIARITY_GLP1` | Q9 | Likert (1-5) | Self-rated familiarity with GLP-1 RA CVOT outcome trial evidence | 1 (Very Low) to 5 (Expert) |
| `Q10_FAMILIARITY_SGLT2` | Q10 | Likert (1-5) | Self-rated familiarity with SGLT2i heart failure/renal trial evidence | 1 (Very Low) to 5 (Expert) |
| `Q11_BARRIER_PRIOR_AUTH`| Q11 | Likert (1-5) | Severity of Prior Authorization & Step Therapy documentation burden | 1 (Not a Barrier) to 5 (Critical Barrier) |
| `Q12_BARRIER_OUT_OF_POCKET_COST`| Q12 | Likert (1-5) | Severity of patient out-of-pocket copay and coverage-gap burden | 1 (Not a Barrier) to 5 (Critical Barrier) |
| `Q13_BARRIER_SIDE_EFFECTS`| Q13 | Likert (1-5) | Severity of clinical adverse effects (GI nausea, mycotic infections) | 1 (Not a Barrier) to 5 (Critical Barrier) |
| `Q14_BARRIER_SUPPLY_SHORTAGES`| Q14 | Likert (1-5) | Impact of national dispensing shortages and stockouts | 1 (Not a Barrier) to 5 (Critical Barrier) |
| `Q15_BARRIER_PATIENT_NEEDLE_HESITATION`| Q15 | Likert (1-5) | Impact of patient resistance or anxiety to subcutaneous injections | 1 (Not a Barrier) to 5 (Critical Barrier) |
| `Q16_PRIMARY_PRESCRIBING_DRIVER`| Q16 | Categorical | Single most important clinical factor influencing drug choice | HbA1c Efficacy, CV Risk Reduction (CVOTs), Renal Protection, Weight Loss Benefit, Patient Cost / Formulary Tier, Tolerability |
| `Q17_UNMET_NEEDS` | Q17 | Multi-Select | Top commercial innovation / support program needed | Electronic PA, Co-pay Foundation Assistance, Oral GLP-1, Fixed-Dose Combination, Injection Apps |
| `COMPOSITE_BARRIER_INDEX`| Derived | Decimal (1.0-5.0) | Mean across Q11, Q12, Q13, Q14, Q15 | Continuous Scale |
| `IS_HIGH_VOLUME_PRACTITIONER`| Derived | Binary (0 or 1) | Clinicians managing >60 T2D patients per month | 1 if Q4 in (`61-100`, `>100`), else 0 |
| `IS_SYNTHETIC` | Governance | Boolean | Audit flag certifying synthetic origin | TRUE |

---

## 3. Power BI Star Schema Dimension & Fact Tables

1. **`Fact_CMS_Prescribing`**: Clean prescriber-drug level transactional records.
2. **`Fact_Survey_Responses`**: Clean respondent-level survey answers with top-box and composite indicators.
3. **`Fact_Stated_vs_Observed_Gap`**: Pre-aggregated bridge table comparing stated survey preference with real-world Medicare Part D claims share.
4. **`Dim_Drug_Product`**: Master drug dimension with generic name, brand aliases, route, tier, and 30-day cost benchmark.
5. **`Dim_Prescriber_Specialty`**: Physician specialty lookup classifying providers into Primary Care, Subspecialty, or Advanced Practice.
6. **`Dim_Geography_State`**: US state lookup with Census Regions (Northeast, Midwest, South, West).
7. **`Dim_Barrier_Category`**: Barrier taxonomy mapping questions to operational domains (Payer, Affordability, Clinical Safety, Supply).
