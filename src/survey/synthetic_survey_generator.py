"""
PharmaPulse Synthetic Survey Dataset Generator
Generates a realistic, reproducible synthetic dataset of 350 Healthcare Professionals (HCPs)
evaluating Type 2 Diabetes treatment preferences, barriers, and commercial perceptions.
"""
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from config.settings import RANDOM_SEED, SURVEY_SAMPLE_SIZE, SYNTHETIC_DATA_DIR, SURVEY_RAW_CSV

def generate_synthetic_survey(
    sample_size: int = SURVEY_SAMPLE_SIZE,
    seed: int = RANDOM_SEED,
    inject_missing: bool = True
) -> pd.DataFrame:
    """
    Generates realistic synthetic responses for HCP survey on T2D.
    Uses conditional probability distributions conditioned on physician specialty.
    """
    np.random.seed(seed)

    respondent_ids = [f"HCP_T2D_{i+1:04d}" for i in range(sample_size)]

    # 1. Specialty distribution
    specialties = [
        "Internal Medicine",
        "Family Practice",
        "Endocrinology, Diabetes & Metabolism",
        "Nurse Practitioner",
    ]
    p_specialty = [0.38, 0.32, 0.18, 0.12]
    assigned_specialties = np.random.choice(specialties, size=sample_size, p=p_specialty)

    # 2. Experience distribution conditioned on specialty
    exp_bands = ["<5 years", "5-10 years", "11-20 years", ">20 years"]
    assigned_experience = []
    assigned_practice_settings = []
    assigned_patient_volumes = []
    assigned_medicare_pct = []

    for spec in assigned_specialties:
        # Experience
        if spec == "Nurse Practitioner":
            p_exp = [0.30, 0.40, 0.20, 0.10]
        else:
            p_exp = [0.15, 0.28, 0.35, 0.22]
        assigned_experience.append(np.random.choice(exp_bands, p=p_exp))

        # Practice Setting
        if spec == "Endocrinology, Diabetes & Metabolism":
            settings = [
                "Academic Medical Center",
                "Community Hospital System",
                "Private Group Practice",
                "Solo Practice",
                "FQHC / Community Health Center",
            ]
            p_setting = [0.45, 0.25, 0.22, 0.05, 0.03]
        elif spec == "Family Practice":
            settings = [
                "Academic Medical Center",
                "Community Hospital System",
                "Private Group Practice",
                "Solo Practice",
                "FQHC / Community Health Center",
            ]
            p_setting = [0.08, 0.27, 0.40, 0.12, 0.13]
        else:
            settings = [
                "Academic Medical Center",
                "Community Hospital System",
                "Private Group Practice",
                "Solo Practice",
                "FQHC / Community Health Center",
            ]
            p_setting = [0.18, 0.32, 0.35, 0.08, 0.07]
        assigned_practice_settings.append(np.random.choice(settings, p=p_setting))

        # Monthly T2D Patient Volume
        if spec == "Endocrinology, Diabetes & Metabolism":
            p_vol = [0.02, 0.10, 0.40, 0.48]
        elif spec == "Internal Medicine":
            p_vol = [0.12, 0.38, 0.35, 0.15]
        else:
            p_vol = [0.22, 0.45, 0.25, 0.08]
        assigned_patient_volumes.append(np.random.choice(["15-30", "31-60", "61-100", ">100"], p=p_vol))

        # Pct Medicare Patients
        p_medicare = [0.15, 0.38, 0.35, 0.12]
        assigned_medicare_pct.append(np.random.choice(["<25%", "25-50%", "51-75%", ">75%"], p=p_medicare))

    # 3. Treatment Preferences
    first_line_options = [
        "Metformin Monotherapy",
        "Metformin + SGLT2 Inhibitor",
        "Metformin + GLP-1 Receptor Agonist",
        "SGLT2 Inhibitor Monotherapy",
        "GLP-1 Receptor Agonist Monotherapy",
        "DPP-4 Inhibitor Monotherapy",
    ]

    second_line_ascvd_options = [
        "GLP-1 Receptor Agonist (e.g. Semaglutide, Dulaglutide)",
        "SGLT2 Inhibitor (e.g. Empagliflozin, Dapagliflozin)",
        "DPP-4 Inhibitor (e.g. Sitagliptin)",
        "Sulfonylurea (e.g. Glimepiride)",
        "Basal Insulin",
    ]

    second_line_ckd_options = [
        "SGLT2 Inhibitor",
        "GLP-1 Receptor Agonist",
        "DPP-4 Inhibitor",
        "Sulfonylurea",
        "Basal Insulin",
    ]

    assigned_first_line = []
    assigned_second_ascvd = []
    assigned_second_ckd = []

    # Likert Scales (1 to 5)
    familiarity_glp1 = []
    familiarity_sglt2 = []
    barrier_prior_auth = []
    barrier_cost = []
    barrier_side_effects = []
    barrier_shortages = []
    barrier_needle = []

    primary_drivers = []
    assigned_unmet_needs = []

    driver_options = [
        "Glycemic (HbA1c) Efficacy",
        "Cardiovascular Risk Reduction (CVOT Data)",
        "Renal / CKD Progression Protection",
        "Weight Loss / Body Composition Benefit",
        "Patient Out-of-Pocket Cost & Tier 1/2 Coverage",
        "Tolerability & Low Hypoglycemia Risk",
    ]

    unmet_options = [
        "Real-time Electronic Prior Authorization (ePA) integration",
        "Manufacturer Copay Assistance bridging for Medicare Part D / Low Income",
        "High-potency Oral GLP-1 Formulation with lower GI symptoms",
        "Fixed-dose SGLT2i + GLP-1 RA combination pill",
        "Multilingual Patient Injection & Lifestyle Navigation apps",
    ]

    for spec, exp in zip(assigned_specialties, assigned_experience):
        is_endo = (spec == "Endocrinology, Diabetes & Metabolism")
        is_im = (spec == "Internal Medicine")

        # First line
        if is_endo:
            p_fl = [0.48, 0.24, 0.22, 0.03, 0.02, 0.01]
        elif is_im:
            p_fl = [0.68, 0.16, 0.12, 0.02, 0.01, 0.01]
        else:
            p_fl = [0.76, 0.11, 0.08, 0.02, 0.01, 0.02]
        assigned_first_line.append(np.random.choice(first_line_options, p=p_fl))

        # Second line ASCVD (Guideline preference)
        if is_endo:
            p_ascvd = [0.66, 0.28, 0.03, 0.02, 0.01]
        elif is_im:
            p_ascvd = [0.52, 0.32, 0.07, 0.06, 0.03]
        else:
            p_ascvd = [0.42, 0.34, 0.11, 0.09, 0.04]
        assigned_second_ascvd.append(np.random.choice(second_line_ascvd_options, p=p_ascvd))

        # Second line CKD / HF
        if is_endo:
            p_ckd = [0.74, 0.22, 0.02, 0.01, 0.01]
        elif is_im:
            p_ckd = [0.65, 0.25, 0.05, 0.03, 0.02]
        else:
            p_ckd = [0.58, 0.26, 0.08, 0.05, 0.03]
        assigned_second_ckd.append(np.random.choice(second_line_ckd_options, p=p_ckd))

        # Familiarity with CVOTs
        if is_endo:
            fam_g = np.random.choice([3, 4, 5], p=[0.05, 0.30, 0.65])
            fam_s = np.random.choice([3, 4, 5], p=[0.05, 0.35, 0.60])
        else:
            fam_g = np.random.choice([1, 2, 3, 4, 5], p=[0.03, 0.09, 0.28, 0.42, 0.18])
            fam_s = np.random.choice([1, 2, 3, 4, 5], p=[0.04, 0.11, 0.32, 0.38, 0.15])
        familiarity_glp1.append(fam_g)
        familiarity_sglt2.append(fam_s)

        # Adoption Barriers (1-5 Likert)
        # Prior Auth is universally high, slightly higher in PCP clinics lacking dedicated PA staff
        if is_endo:
            b_pa = np.random.choice([2, 3, 4, 5], p=[0.04, 0.16, 0.44, 0.36])
        else:
            b_pa = np.random.choice([2, 3, 4, 5], p=[0.02, 0.10, 0.40, 0.48])
        barrier_prior_auth.append(b_pa)

        # Out-of-pocket Cost
        b_cost = np.random.choice([2, 3, 4, 5], p=[0.05, 0.15, 0.42, 0.38])
        barrier_cost.append(b_cost)

        # Side Effects (GI for GLP-1, mycotic for SGLT2)
        b_se = np.random.choice([1, 2, 3, 4, 5], p=[0.08, 0.28, 0.38, 0.20, 0.06])
        barrier_side_effects.append(b_se)

        # Supply Shortages
        b_sup = np.random.choice([1, 2, 3, 4, 5], p=[0.04, 0.12, 0.26, 0.38, 0.20])
        barrier_shortages.append(b_sup)

        # Needle / Injection Hesitation (Higher in primary care)
        if is_endo:
            b_needle = np.random.choice([1, 2, 3, 4, 5], p=[0.14, 0.35, 0.32, 0.15, 0.04])
        else:
            b_needle = np.random.choice([1, 2, 3, 4, 5], p=[0.06, 0.22, 0.35, 0.26, 0.11])
        barrier_needle.append(b_needle)

        # Decision Driver
        if is_endo:
            p_drv = [0.18, 0.34, 0.20, 0.18, 0.06, 0.04]
        else:
            p_drv = [0.28, 0.22, 0.15, 0.12, 0.17, 0.06]
        primary_drivers.append(np.random.choice(driver_options, p=p_drv))

        # Unmet Needs (Pick 1-3)
        n_unmet = np.random.choice([1, 2, 3], p=[0.4, 0.45, 0.15])
        chosen_unmet = np.random.choice(unmet_options, size=n_unmet, replace=False)
        assigned_unmet_needs.append("; ".join(chosen_unmet))

    # Assemble DataFrame
    df = pd.DataFrame({
        "RESPONDENT_ID": respondent_ids,
        "Q1_SPECIALTY": assigned_specialties,
        "Q2_YEARS_EXPERIENCE": assigned_experience,
        "Q3_PRACTICE_SETTING": assigned_practice_settings,
        "Q4_MONTHLY_T2D_PATIENTS": assigned_patient_volumes,
        "Q5_PCT_MEDICARE_PATIENTS": assigned_medicare_pct,
        "Q6_FIRST_LINE_PREFERENCE": assigned_first_line,
        "Q7_SECOND_LINE_ASCVD_PREFERENCE": assigned_second_ascvd,
        "Q8_SECOND_LINE_CKD_HF_PREFERENCE": assigned_second_ckd,
        "Q9_FAMILIARITY_GLP1": familiarity_glp1,
        "Q10_FAMILIARITY_SGLT2": familiarity_sglt2,
        "Q11_BARRIER_PRIOR_AUTH": barrier_prior_auth,
        "Q12_BARRIER_OUT_OF_POCKET_COST": barrier_cost,
        "Q13_BARRIER_SIDE_EFFECTS": barrier_side_effects,
        "Q14_BARRIER_SUPPLY_SHORTAGES": barrier_shortages,
        "Q15_BARRIER_PATIENT_NEEDLE_HESITATION": barrier_needle,
        "Q16_PRIMARY_PRESCRIBING_DRIVER": primary_drivers,
        "Q17_UNMET_NEEDS": assigned_unmet_needs,
        "IS_SYNTHETIC": True,
        "DATA_SOURCE_DISCLAIMER": "SYNTHETIC DEMONSTRATION DATASET - NOT REAL CLINICAL DATA",
        "GENERATION_TIMESTAMP": datetime.utcnow().isoformat(),
    })

    # Controlled realistic missingness (~2.5% MCAR in non-critical demographic columns)
    if inject_missing:
        cols_with_missing = ["Q3_PRACTICE_SETTING", "Q4_MONTHLY_T2D_PATIENTS", "Q5_PCT_MEDICARE_PATIENTS"]
        for col in cols_with_missing:
            mask = np.random.rand(sample_size) < 0.025
            df.loc[mask, col] = np.nan

    return df


def save_synthetic_survey(df: pd.DataFrame, file_path: Path = SURVEY_RAW_CSV) -> Path:
    """Saves generated synthetic survey dataset to CSV."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Synthetic survey dataset successfully saved to: {file_path} ({len(df)} rows)")
    return file_path


if __name__ == "__main__":
    synthetic_df = generate_synthetic_survey()
    save_synthetic_survey(synthetic_df)
