from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
GOLDEN = ROOT / "golden" / "technical_composition" / "01-medium-equidistant-page-blueprint.json"
SPEC = importlib.util.spec_from_file_location(
    "validate_learner_page_blueprint",
    ROOT / "engine" / "validate_learner_page_blueprint.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def load_golden():
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


def page(doc, page_id):
    return next(x for x in doc["pages"] if x["page_id"] == page_id)


def test_medium_six_core_page_blueprint_passes():
    mod.validate_page_blueprint(load_golden())


def test_prose_only_page_is_forbidden():
    doc = load_golden()
    page(doc, "C1-P1")["technical_blocks"] = []
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_PROSE_ONLY_PAGE_FORBIDDEN" in str(exc)
    else:
        raise AssertionError("expected prose-only page to fail")


def test_representation_geometry_must_be_clipped_to_its_viewport():
    doc = load_golden()
    page(doc, "C1B-P1")["representations"][0]["clip_to_viewport"] = False
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_REPRESENTATION_VIEWPORT_CLIP_REQUIRED" in str(exc)
    else:
        raise AssertionError("expected unbounded representation geometry to fail")


def test_manual_spacer_padding_is_forbidden():
    doc = load_golden()
    page(doc, "C1A-P1")["pagination"]["manual_spacers_used"] = True
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_MANUAL_SPACER_PADDING_FORBIDDEN" in str(exc)
    else:
        raise AssertionError("expected manual spacer padding to fail")


def test_downstream_narrative_copy_is_forbidden():
    doc = load_golden()
    c1 = page(doc, "C1-P1")["prose_blocks"][0]
    c1a = page(doc, "C1A-P1")["prose_blocks"][0]
    c1a["content_signature"] = c1["content_signature"]
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_CROSS_CORE_NARRATIVE_DUPLICATION_FORBIDDEN" in str(exc)
    else:
        raise AssertionError("expected copied prose across cores to fail")


def test_immutable_source_may_repeat_only_as_declared_carry():
    doc = load_golden()
    problem = next(x for x in page(doc, "C2A-P1")["technical_blocks"] if x["block_id"] == "C2A-PROBLEM")
    problem["transformation"] = "SOLUTION_ANATOMY"
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_ALLOWED_REPEAT_MUST_DECLARE_IMMUTABLE_CARRY" in str(exc)
    else:
        raise AssertionError("expected undeclared immutable-source carry to fail")


def test_open_tutor_page_requires_answer_derivation_and_verification():
    doc = load_golden()
    p = page(doc, "C1B-P1")
    p["technical_blocks"] = [x for x in p["technical_blocks"] if x["kind"] != "ANSWER_DERIVATION"]
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_PAGE_REQUIRED_TECHNICAL_BLOCK_MISSING" in str(exc)
    else:
        raise AssertionError("expected missing self-help closure to fail")


def test_medium_required_depth_cannot_be_replaced_by_page_count():
    doc = load_golden()
    row = next(
        x for x in doc["depth_obligations"]
        if x["stage"] == "CORE1A" and x["obligation_id"] == "MISCONCEPTION_COUNTEREXAMPLE"
    )
    row["disposition"] = "NOT_APPLICABLE"
    row["evidence_refs"] = []
    row["not_applicable_reason"] = "Removed only to test the required depth gate."
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_REQUIRED_DEPTH_OBLIGATION_MUST_BE_SATISFIED" in str(exc)
    else:
        raise AssertionError("expected missing MEDIUM technical depth to fail")


def test_flow_pagination_cannot_hide_forced_blank_space():
    doc = load_golden()
    page(doc, "C1A-P1")["pagination"]["break_reason"] = "Force another page to approach the page allowance."
    try:
        mod.validate_page_blueprint(doc)
    except ValueError as exc:
        assert "MATH_FLOW_PAGE_CANNOT_CARRY_BREAK_REASON" in str(exc)
    else:
        raise AssertionError("expected fake flow break to fail")
