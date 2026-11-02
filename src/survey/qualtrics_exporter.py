"""
PharmaPulse Qualtrics Survey Export Utility
Generates Qualtrics Advanced TXT and QSF formats for Qualtrics Survey platform import.
"""
import json
from pathlib import Path
from src.survey.survey_design import QUESTIONS_DEFINITION, SURVEY_METADATA

def export_qualtrics_txt(output_path: Path) -> Path:
    """
    Exports the survey into Qualtrics Advanced Format (.txt).
    Qualtrics Advanced Format allows direct import via Qualtrics Web UI:
    Tools > Import/Export > Import Survey > Browse for TXT file.
    """
    lines = [
        "[[AdvancedFormat]]",
        f"[[SurveyName:{SURVEY_METADATA['survey_title']}]]",
        "",
        "[[Block:Screening & Demographics]]",
        "[[Question:DB]]",
        f"<b>{SURVEY_METADATA['survey_title']}</b><br><br>{SURVEY_METADATA['disclaimer']}<br><br><b>Screening Criteria:</b> {SURVEY_METADATA['screening_criteria']}",
        "",
    ]

    current_category = ""
    for q in QUESTIONS_DEFINITION:
        cat = q["category"]
        if cat != current_category and cat != "Demographics & Professional Profile":
            current_category = cat
            lines.append(f"[[Block:{cat}]]")
            lines.append("")

        q_type = q["type"]
        q_id = q["id"]
        q_text = q["text"]
        options = q["options"]

        if q_type in ["Single-Select", "Demographic", "Continuous / Numeric Band", "Continuous / Percentage"]:
            lines.append(f"[[Question:MC:SingleAnswer:Vertical]]")
            lines.append(f"[[ID:{q_id}]]")
            lines.append(q_text)
            lines.append("[[Choices]]")
            for opt in options:
                lines.append(opt)
            lines.append("")

        elif "Likert" in q_type:
            lines.append(f"[[Question:MC:SingleAnswer:Horizontal]]")
            lines.append(f"[[ID:{q_id}]]")
            lines.append(f"<b>{q_text}</b>")
            lines.append("[[Choices]]")
            for opt in options:
                lines.append(opt)
            lines.append("")

        elif "Multiple-Select" in q_type:
            lines.append(f"[[Question:MC:MultipleAnswer:Vertical]]")
            lines.append(f"[[ID:{q_id}]]")
            lines.append(q_text)
            lines.append("[[Choices]]")
            for opt in options:
                lines.append(opt)
            lines.append("")

    content = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path


def export_qualtrics_qsf(output_path: Path) -> Path:
    """
    Exports a valid Qualtrics Survey Format (QSF) JSON schema template.
    """
    qsf = {
        "SurveyEntry": {
            "SurveyID": "SV_PharmaPulseT2D",
            "SurveyName": SURVEY_METADATA["survey_title"],
            "SurveyDescription": SURVEY_METADATA["disclaimer"],
            "SurveyStatus": "Active",
            "SurveyStartDate": "2024-01-01 00:00:00",
            "SurveyExpirationDate": "2026-12-31 00:00:00",
            "SurveyCreationDate": "2024-01-01 00:00:00",
        },
        "SurveyElements": [],
    }

    element_id = 1
    for q in QUESTIONS_DEFINITION:
        elem = {
            "SurveyID": "SV_PharmaPulseT2D",
            "Element": "SQ",
            "PrimaryAttribute": q["id"],
            "SecondaryAttribute": q["text"],
            "Payload": {
                "QuestionText": q["text"],
                "QuestionType": "MC",
                "Selector": "SAVR" if "Multiple" not in q["type"] else "MAVR",
                "SubSelector": "TX",
                "DataExportTag": q["id"],
                "QuestionDescription": q["text"],
                "Choices": {str(i + 1): {"Display": opt} for i, opt in enumerate(q["options"])},
            },
        }
        qsf["SurveyElements"].append(elem)
        element_id += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(qsf, f, indent=2)
    return output_path


if __name__ == "__main__":
    txt_path = Path("docs/qualtrics_survey_definition.txt")
    qsf_path = Path("docs/qualtrics_survey_template.qsf")
    export_qualtrics_txt(txt_path)
    export_qualtrics_qsf(qsf_path)
    print("Qualtrics definitions successfully generated.")
