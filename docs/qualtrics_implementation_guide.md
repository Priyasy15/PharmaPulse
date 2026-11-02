# PharmaPulse Qualtrics Survey Implementation & Transfer Guide

This guide provides instructions for transferring the PharmaPulse Type 2 Diabetes (T2D) Healthcare Professional (HCP) survey into **Qualtrics CoreXM / Qualtrics Research Suite**.

---

## 1. Supported Import Methods

The project generates two native formats:
1. **Qualtrics Advanced TXT Format**: `docs/qualtrics_survey_definition.txt` (Recommended)
2. **Qualtrics Survey Format (QSF JSON)**: `docs/qualtrics_survey_template.qsf`

---

## 2. Step-by-Step Import via Qualtrics Advanced Text File

1. Log into your **Qualtrics** account at `yourinstitution.qualtrics.com`.
2. Click **Create new project** > **Survey** > **From scratch**.
3. Name the survey: `PharmaPulse Type 2 Diabetes HCP Market Research`.
4. In the survey builder, click **Tools** in the top navigation bar.
5. Select **Import / Export** > **Import survey...**.
6. Select **From a text file** and upload `docs/qualtrics_survey_definition.txt`.
7. Click **Import**. Qualtrics will automatically:
   - Construct blocks: *Screening & Demographics*, *Treatment Preference*, *Awareness & Evidence*, *Adoption Barriers*, *Clinical Decision Drivers*, *Commercial Opportunities*.
   - Assign question tags: `Q1_SPECIALTY`, `Q6_FIRST_LINE_PREFERENCE`, `Q11_BARRIER_PRIOR_AUTH`, etc.
   - Configure choice formats (Single-select vertical, horizontal Likert, multi-select).

---

## 3. Alternative Method: Import via QSF JSON

1. In Qualtrics, click **Create new project** > **Survey**.
2. Select **Import a QSF** or **From a file**.
3. Upload `docs/qualtrics_survey_template.qsf`.
4. The entire survey schema and element mappings will be instantiated.

---

## 4. Screening & Quota Recommendations

For a live field execution, implement the following screening logic in Qualtrics Survey Flow:

- **Screening Question (Q0)**: *"Do you currently treat 15 or more adult patients with Type 2 Diabetes each month in the United States?"*
  - Yes → Continue.
  - No → Terminate with customized screen-out message.
- **Specialty Quotas**:
  - Primary Care (Internal Medicine + Family Practice): 70% (~245 respondents)
  - Endocrinology, Diabetes & Metabolism: 18% (~63 respondents)
  - Nurse Practitioners / Physician Assistants: 12% (~42 respondents)

---

## 5. Live Prototype in Streamlit

If you do not currently have an active Qualtrics license, use the built-in **Live HCP Survey Prototype** directly within the PharmaPulse Streamlit application:
1. Launch the Streamlit application: `streamlit run src/dashboard/app.py`.
2. Navigate to **Tab 3: 📋 Live Survey Prototype**.
3. Fill out the form interactively and download the Qualtrics template files with a single click.
