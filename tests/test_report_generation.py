"""
Unit tests for PharmaPulse Automated PowerPoint Generator.
"""
import pytest
from pptx import Presentation
from pathlib import Path
from src.report_generation.presentation_builder import build_powerpoint_deck

def test_powerpoint_generation(tmp_path):
    test_deck_path = tmp_path / "test_deck.pptx"
    output = build_powerpoint_deck(output_path=test_deck_path)
    
    assert output.exists()
    assert output.stat().st_size > 50000 # Valid presentation file with charts

    # Inspect PowerPoint object structure
    prs = Presentation(str(output))
    assert len(prs.slides) == 10
    
    # Check widescreen dimensions (13.333 x 7.5 inches)
    assert round(prs.slide_width.inches, 2) == 13.33
    assert round(prs.slide_height.inches, 2) == 7.50

    # Ensure slide 1 has the project title
    first_slide_text = ""
    for shape in prs.slides[0].shapes:
        if shape.has_text_frame:
            first_slide_text += shape.text_frame.text
    assert "PharmaPulse" in first_slide_text
