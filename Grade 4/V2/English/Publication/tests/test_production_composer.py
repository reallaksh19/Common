from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_SET = ROOT / "Benchmarks" / "source_sets" / "english_worksheet_09"
PUB_ENGINE = ROOT / "Publication" / "engine"
for path in (SOURCE_SET, PUB_ENGINE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build_fixture import build_handoff  # type: ignore  # noqa: E402
from production_composer import (  # type: ignore  # noqa: E402
    render_practice_workbook,
    render_study_guide,
    render_teacher_diagnostic_key,
)
from publication_model import build_study_guide_model, build_teacher_key_model  # type: ignore  # noqa: E402


def test_publication_models_preserve_open_response_and_source_boundary_semantics(tmp_path: Path) -> None:
    handoff = build_handoff()
    study = build_study_guide_model(handoff)
    teacher = build_teacher_key_model(handoff)

    assert len(study["pages"]) == 9
    assert len(teacher["pages"]) == 9

    boundary = next(page for page in study["pages"] if page.get("question_ref") == "ENG-G4-WS09-III")
    assert boundary["source_boundary_required"] is True
    assert "traditional" in " ".join(boundary["ambiguity"])
    assert boundary["source_model"]["boundary_policy"]["no_force_fit"] is True

    inference = next(page for page in teacher["pages"] if page.get("question_ref") == "ENG-G4-WS09-V-Q1")
    assert inference["judgement_required"] is True
    assert inference["expected_evidence"] == ["ANSWER", "TEXT_CLUE", "CONNECTION"]
    assert "exact_answer" not in inference
    assert "model_answer" not in inference

    for plan in handoff["learning_representation_plans"]:
        assert plan["representation_specs"]
        assert plan["support"]["fresh_retry"]["conceptual_support"] == "H0"
        assert plan["support"]["fresh_retry"]["must_be_new_item"] is True


def test_all_three_production_artifacts_render_from_one_handoff(tmp_path: Path) -> None:
    handoff = build_handoff()
    renderers = [
        (render_study_guide, "study.pdf", "STUDY_GUIDE"),
        (render_practice_workbook, "workbook.pdf", "WORKBOOK"),
        (render_teacher_diagnostic_key, "teacher.pdf", "TEACHER_KEY"),
    ]
    for renderer, filename, kind in renderers:
        path, metadata = renderer(handoff, tmp_path / filename)
        out = Path(path)
        assert out.exists() and out.stat().st_size > 5000
        assert metadata["document_kind"] == kind
        assert metadata["page_count"] == 9
        assert len(metadata["question_refs"]) == 8
