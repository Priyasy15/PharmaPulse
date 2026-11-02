"""
PharmaPulse Survey Design & Question Definitions
Type 2 Diabetes (T2D) Healthcare Professional (HCP) Market Research
"""
from typing import Dict, List, Any

SURVEY_METADATA = {
    "survey_title": "PharmaPulse Type 2 Diabetes (T2D) Treatment Landscape & Commercial Adoption Survey",
    "target_audience": "Licensed Healthcare Professionals (MD, DO, NP, PA) actively managing adult T2D patients",
    "screening_criteria": "Minimum 15 adult T2D patients managed per month in the United States",
    "disclaimer": (
        "INDEPENDENT RESEARCH SIMULATION DISCLAIMER: This survey prototype and any associated data "
        "are created for academic, educational, and commercial analytics demonstration purposes. "
        "It is not sponsored by, endorsed by, or affiliated with any commercial pharmaceutical company, "
        "nor does it represent actual patient medical records or unverified clinical claims."
    ),
    "version": "1.0.0",
}

QUESTIONS_DEFINITION: List[Dict[str, Any]] = [
    {
        "id": "Q1_SPECIALTY",
        "category": "Demographics & Professional Profile",
        "type": "Single-Select",
        "text": "What is your primary medical specialty?",
        "options": [
            "Internal Medicine",
            "Family Practice",
            "Endocrinology, Diabetes & Metabolism",
            "Nurse Practitioner",
        ],
    },
    {
        "id": "Q2_YEARS_EXPERIENCE",
        "category": "Demographics & Professional Profile",
        "type": "Single-Select",
        "text": "How many years have you been in active clinical practice post-training?",
        "options": [
            "<5 years",
            "5-10 years",
            "11-20 years",
            ">20 years",
        ],
    },
    {
        "id": "Q3_PRACTICE_SETTING",
        "category": "Demographics & Professional Profile",
        "type": "Single-Select",
        "text": "Which best describes your primary clinical practice setting?",
        "options": [
            "Academic Medical Center",
            "Community Hospital System",
            "Private Group Practice",
            "Solo Practice",
            "FQHC / Community Health Center",
        ],
    },
    {
        "id": "Q4_MONTHLY_T2D_PATIENTS",
        "category": "Demographics & Professional Profile",
        "type": "Continuous / Numeric Band",
        "text": "Approximately how many adult patients with Type 2 Diabetes do you personally manage each month?",
        "options": ["15-30", "31-60", "61-100", ">100"],
    },
    {
        "id": "Q5_PCT_MEDICARE_PATIENTS",
        "category": "Demographics & Professional Profile",
        "type": "Continuous / Percentage",
        "text": "Approximately what percentage of your T2D patient panel is insured under Medicare (Part D / Medicare Advantage)?",
        "options": ["<25%", "25-50%", "51-75%", ">75%"],
    },
    {
        "id": "Q6_FIRST_LINE_PREFERENCE",
        "category": "Treatment Preference",
        "type": "Single-Select",
        "text": "For a newly diagnosed, treatment-naive T2D patient with HbA1c 7.5%-8.5% and no established cardiovascular disease, what is your standard initial pharmacotherapy?",
        "options": [
            "Metformin Monotherapy",
            "Metformin + SGLT2 Inhibitor",
            "Metformin + GLP-1 Receptor Agonist",
            "SGLT2 Inhibitor Monotherapy",
            "GLP-1 Receptor Agonist Monotherapy",
            "DPP-4 Inhibitor Monotherapy",
        ],
    },
    {
        "id": "Q7_SECOND_LINE_ASCVD_PREFERENCE",
        "category": "Treatment Preference",
        "type": "Single-Select",
        "text": "For a T2D patient on Metformin with uncontrolled HbA1c (8.4%) and established Atherosclerotic Cardiovascular Disease (ASCVD), which second-line class do you prioritize?",
        "options": [
            "GLP-1 Receptor Agonist (e.g. Semaglutide, Dulaglutide)",
            "SGLT2 Inhibitor (e.g. Empagliflozin, Dapagliflozin)",
            "DPP-4 Inhibitor (e.g. Sitagliptin)",
            "Sulfonylurea (e.g. Glimepiride)",
            "Basal Insulin",
        ],
    },
    {
        "id": "Q8_SECOND_LINE_CKD_HF_PREFERENCE",
        "category": "Treatment Preference",
        "type": "Single-Select",
        "text": "For a T2D patient with microalbuminuria (CKD) or Heart Failure with preserved/reduced ejection fraction, which add-on therapy do you prioritize?",
        "options": [
            "SGLT2 Inhibitor",
            "GLP-1 Receptor Agonist",
            "DPP-4 Inhibitor",
            "Sulfonylurea",
            "Basal Insulin",
        ],
    },
    # Likert Scale Questions: Familiarity (1-5)
    {
        "id": "Q9_FAMILIARITY_GLP1",
        "category": "Awareness & Evidence",
        "type": "Likert (1-5)",
        "text": "Rate your familiarity with the cardiovascular and renal outcome trial evidence (CVOTs) for GLP-1 Receptor Agonists.",
        "options": ["1 - Very Low", "2 - Low", "3 - Moderate", "4 - High", "5 - Very High / Expert"],
    },
    {
        "id": "Q10_FAMILIARITY_SGLT2",
        "category": "Awareness & Evidence",
        "type": "Likert (1-5)",
        "text": "Rate your familiarity with the heart failure and renal protection outcome trials for SGLT2 Inhibitors.",
        "options": ["1 - Very Low", "2 - Low", "3 - Moderate", "4 - High", "5 - Very High / Expert"],
    },
    # Likert Scale Questions: Adoption Barriers (1-5)
    {
        "id": "Q11_BARRIER_PRIOR_AUTH",
        "category": "Adoption Barriers",
        "type": "Likert (1-5)",
        "text": "To what extent is Prior Authorization / Step Therapy documentation a barrier to prescribing newer T2D therapies (GLP-1 / SGLT2i)?",
        "options": ["1 - Not a Barrier", "2 - Minor Barrier", "3 - Moderate Barrier", "4 - Significant Barrier", "5 - Critical Barrier"],
    },
    {
        "id": "Q12_BARRIER_OUT_OF_POCKET_COST",
        "category": "Adoption Barriers",
        "type": "Likert (1-5)",
        "text": "To what extent is high patient out-of-pocket copay / deductible a barrier to patient adherence and initiation?",
        "options": ["1 - Not a Barrier", "2 - Minor Barrier", "3 - Moderate Barrier", "4 - Significant Barrier", "5 - Critical Barrier"],
    },
    {
        "id": "Q13_BARRIER_SIDE_EFFECTS",
        "category": "Adoption Barriers",
        "type": "Likert (1-5)",
        "text": "To what extent do clinical side-effects (e.g. GI nausea with GLP-1s, mycotic infections/eGFR limits with SGLT2s) prevent you from prescribing?",
        "options": ["1 - Not a Barrier", "2 - Minor Barrier", "3 - Moderate Barrier", "4 - Significant Barrier", "5 - Critical Barrier"],
    },
    {
        "id": "Q14_BARRIER_SUPPLY_SHORTAGES",
        "category": "Adoption Barriers",
        "type": "Likert (1-5)",
        "text": "To what extent have national supply chain shortages / dispensing delays restricted your adoption of newer incretin therapies?",
        "options": ["1 - Not a Barrier", "2 - Minor Barrier", "3 - Moderate Barrier", "4 - Significant Barrier", "5 - Critical Barrier"],
    },
    {
        "id": "Q15_BARRIER_PATIENT_NEEDLE_HESITATION",
        "category": "Adoption Barriers",
        "type": "Likert (1-5)",
        "text": "To what extent is patient needle resistance or anxiety regarding subcutaneous injection a barrier for injectable GLP-1 therapies?",
        "options": ["1 - Not a Barrier", "2 - Minor Barrier", "3 - Moderate Barrier", "4 - Significant Barrier", "5 - Critical Barrier"],
    },
    # Ranking / Importance
    {
        "id": "Q16_PRIMARY_PRESCRIBING_DRIVER",
        "category": "Clinical Decision Drivers",
        "type": "Single-Select",
        "text": "When deciding between oral SGLT2i, injectable GLP-1 RA, and legacy therapies, what is your single most important decision factor?",
        "options": [
            "Glycemic (HbA1c) Efficacy",
            "Cardiovascular Risk Reduction (CVOT Data)",
            "Renal / CKD Progression Protection",
            "Weight Loss / Body Composition Benefit",
            "Patient Out-of-Pocket Cost & Tier 1/2 Coverage",
            "Tolerability & Low Hypoglycemia Risk",
        ],
    },
    {
        "id": "Q17_UNMET_NEEDS",
        "category": "Commercial Opportunities",
        "type": "Multiple-Select / Multi-Choice",
        "text": "Which commercial innovation or support program would most improve your ability to treat T2D patients effectively?",
        "options": [
            "Real-time Electronic Prior Authorization (ePA) integration",
            "Manufacturer Copay Assistance bridging for Medicare Part D / Low Income",
            "High-potency Oral GLP-1 Formulation with lower GI symptoms",
            "Fixed-dose SGLT2i + GLP-1 RA combination pill",
            "Multilingual Patient Injection & Lifestyle Navigation apps",
        ],
    },
]
