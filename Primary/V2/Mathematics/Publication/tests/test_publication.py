"""
Tests for Primary Mathematics V2 Publication Engine, Custody, and Surface Guard.
"""
from pathlib import Path
import pytest

from Primary.V2.Mathematics.Publication.engine.page_composer import PrimaryPageComposer
from Primary.V2.Mathematics.Publication.engine.surface_guard import LearnerSurfaceGuard


@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path


def test_learner_surface_guard_clean_text():
    guard = LearnerSurfaceGuard()
    text = "Find the product of 23 and 6 using the area model. Then draw an array."
    res = guard.scan_text(text)
    assert res["pass"] is True
    assert len(res["detected_internal_tokens"]) == 0


def test_learner_surface_guard_detects_leak():
    guard = LearnerSurfaceGuard()
    text = "Follow the pedagogical_sequence and update PrimaryMathSkillModel with diagnosticprobe."
    res = guard.scan_text(text)
    assert res["pass"] is False
    assert "pedagogical_sequence" in res["detected_internal_tokens"]
    assert "primarymathskillmodel" in res["detected_internal_tokens"]
    assert "diagnosticprobe" in res["detected_internal_tokens"]


def test_render_core1_study_guide_pdf(temp_output_dir):
    composer = PrimaryPageComposer()
    plan = {
        "title": "Grade 4 Multiplication Bridge",
        "topic": "Multiplication & Division",
        "grade_level": 4,
        "modules": [
            {
                "module_id": "MOD-MUL-01",
                "title": "Bridging 23 x 6",
                "pedagogical_sequence": ["NOTICE", "MODEL", "WORKED", "SUPPORTED", "INDEPENDENT"],
                "dominant_representation": "AREA_MODEL",
                "representation_bridge": ["GROUPS", "ARRAY", "AREA", "PARTIALS", "ALGORITHM"],
                "sections": [
                    {"section_type": "NOTICE", "title": "Look at the numbers", "content": "How can 23 be broken into friendly parts?"},
                    {
                        "section_type": "MAKE_DRAW_REPRESENT",
                        "title": "Visual Area Model",
                        "content": "Partition 23 into 20 and 3.",
                        "primitive_call": {
                            "kind": "AREA_MODEL",
                            "params": {
                                "factors": [23, 6],
                                "partitions": [{"length": 20, "height": 6, "area": 120}, {"length": 3, "height": 6, "area": 18}]
                            }
                        }
                    }
                ]
            }
        ]
    }
    out_pdf = temp_output_dir / "core1_test.pdf"
    pdf_sha256, custody_rec = composer.render_core1_study_guide(plan, out_pdf)

    assert out_pdf.exists()
    assert len(pdf_sha256) == 64
    assert custody_rec["page_count"] >= 1
    assert custody_rec["child_first_geometry"]["min_body_font_pt"] >= 12.0
    assert custody_rec["child_first_geometry"]["overflow_strategy"] == "ADD_PAGE"


def test_render_core2_companion_pdf(temp_output_dir):
    composer = PrimaryPageComposer()
    plan = {
        "companion_id": "C2-COMP-01",
        "linked_core1_id": "MOD-MUL-01",
        "appendix_a": {
            "batches": [
                {
                    "batch_id": "BATCH-1",
                    "title": "Building Confidence",
                    "practice_role": "BUILD",
                    "items": [{"item_id": "Q1", "prompt": "Calculate 24 x 5 using area model partition."}]
                }
            ]
        },
        "appendix_b": {
            "ladders": [
                {
                    "item_id": "Q1",
                    "H0_try": "24 x 5",
                    "H1_notice": "Break 24 into 20 + 4",
                    "H2_remember": "Multiply 20x5 and 4x5",
                    "H3_represent": "Draw 20x5 and 4x5 area model",
                    "fresh_independent_retry_H0": "Now try 25 x 4"
                }
            ]
        },
        "appendix_c": {
            "title": "Multiplication Partition Reference",
            "format": "VISUAL_DECISION_REFERENCE",
            "decision_aid_name": "Area Model Flowcard",
            "is_prose_cram_sheet": False,
            "primitive_call": {
                "kind": "AREA_MODEL",
                "params": {
                    "factors": [23, 6],
                    "partitions": [{"length": 20, "height": 6, "area": 120}, {"length": 3, "height": 6, "area": 18}]
                }
            }
        }
    }
    out_pdf = temp_output_dir / "core2_test.pdf"
    pdf_sha256, custody_rec = composer.render_core2_companion(plan, out_pdf)

    assert out_pdf.exists()
    assert len(pdf_sha256) == 64
    assert custody_rec["page_count"] >= 3
