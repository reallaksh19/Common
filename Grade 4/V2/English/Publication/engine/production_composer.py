"""Canonical Grade-4 English V2 production entry points."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from pdf_renderer import render_publication_model  # type: ignore  # noqa: E402
from publication_model import (  # type: ignore  # noqa: E402
    assert_publication_model_safe,
    build_study_guide_model,
    build_teacher_key_model,
    build_workbook_model,
)


def _require_handoff(handoff: Mapping[str, Any]) -> None:
    if handoff.get("subject") != "ENGLISH" or handoff.get("grade") != 4:
        raise ValueError("Grade 4 English V2 Publication requires a Grade-4 ENGLISH authoring handoff")
    plans = handoff.get("learning_representation_plans") or []
    if not plans:
        raise ValueError("LearningRepresentationPlan is required; renderer-local authoring is forbidden")
    for plan in plans:
        if not plan.get("representation_specs"):
            raise ValueError(f"{plan.get('question_ref')}: typed representation specs are required")
        support = plan.get("support") or {}
        retry = support.get("fresh_retry") or {}
        if retry.get("conceptual_support") != "H0" or retry.get("must_be_new_item") is not True:
            raise ValueError(f"{plan.get('question_ref')}: publication requires a fresh H0 retry")


def _render(handoff: Mapping[str, Any], output_pdf_path: Path, kind: str) -> Tuple[str, Dict[str, Any]]:
    _require_handoff(handoff)
    builders = {
        "STUDY_GUIDE": build_study_guide_model,
        "WORKBOOK": build_workbook_model,
        "TEACHER_KEY": build_teacher_key_model,
    }
    model = builders[kind](handoff)
    assert_publication_model_safe(model)
    result = dict(render_publication_model(model, output_pdf_path))
    result["source_id"] = (handoff.get("source") or {}).get("source_id")
    result["question_refs"] = [p["question_ref"] for p in handoff["learning_representation_plans"]]
    return str(output_pdf_path), result


def render_study_guide(handoff: Mapping[str, Any], output_pdf_path: Path) -> Tuple[str, Dict[str, Any]]:
    return _render(handoff, output_pdf_path, "STUDY_GUIDE")


def render_practice_workbook(handoff: Mapping[str, Any], output_pdf_path: Path) -> Tuple[str, Dict[str, Any]]:
    return _render(handoff, output_pdf_path, "WORKBOOK")


def render_teacher_diagnostic_key(handoff: Mapping[str, Any], output_pdf_path: Path) -> Tuple[str, Dict[str, Any]]:
    return _render(handoff, output_pdf_path, "TEACHER_KEY")
