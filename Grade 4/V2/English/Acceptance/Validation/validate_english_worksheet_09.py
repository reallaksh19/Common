"""Acceptance gate for the first real Grade-4 English V2 source set."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGLISH_ROOT = HERE.parents[1]
SOURCE_SET = ENGLISH_ROOT / "Benchmarks" / "source_sets" / "english_worksheet_09"
if str(SOURCE_SET) not in sys.path:
    sys.path.insert(0, str(SOURCE_SET))

from build_fixture import build_handoff, build_primary_input  # type: ignore  # noqa: E402

EXPECTED_CATEGORIES = ["OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL"]
EXPECTED_SOURCE_WORDS = {
    "Japanese", "leather", "huge", "tasty", "pink", "fascinating", "plastic", "new", "round",
    "Spanish", "tiny", "sad", "wooden", "wide", "small", "grey", "wool", "Swedish", "metal",
    "square", "fantastic", "yellow", "old",
}
EXPECTED_QUESTION_REFS = {
    "ENG-G4-WS09-I",
    "ENG-G4-WS09-II",
    "ENG-G4-WS09-III",
    "ENG-G4-WS09-IV",
    "ENG-G4-WS09-V-Q1",
    "ENG-G4-WS09-V-Q2",
    "ENG-G4-WS09-V-Q3",
    "ENG-G4-WS09-V-Q4",
}
FORBIDDEN_CATEGORIES = {"QUALITY", "PHYSICAL_QUALITY", "QUALITY_TYPE", "CONDITION"}


def _fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    source = json.loads((SOURCE_SET / "source.json").read_text(encoding="utf-8"))
    primary = build_primary_input()
    handoff = build_handoff()

    if source.get("pii_redacted") is not True:
        _fail("benchmark must explicitly redact direct child/school identifiers")

    section_i = next(row for row in source["sections"] if row["section_ref"] == "I")
    if set(section_i["printed_words"]) != EXPECTED_SOURCE_WORDS:
        _fail("all 23 visible Section-I source words must be dispositioned exactly once")
    if len(section_i["printed_words"]) != 23:
        _fail("Section I must contain exactly 23 visible source words")

    models = primary["source_models"]
    if len(models) != 1:
        _fail("worksheet benchmark must carry exactly one adjective source model")
    model = models[0]
    if model["categories"] != EXPECTED_CATEGORIES or model["ordering"] != EXPECTED_CATEGORIES:
        _fail("worksheet adjective categories/order must remain source-bound and exact")
    if FORBIDDEN_CATEGORIES.intersection(model["categories"]):
        _fail("invented source categories are forbidden")
    if "traditional" not in model.get("boundary_examples", []):
        _fail("traditional must remain an explicit source-model boundary word")
    if model["boundary_policy"].get("no_force_fit") is not True:
        _fail("source-boundary policy must forbid force-fitting")

    evidence = primary["question_evidence"]
    refs = {row["question_ref"] for row in evidence}
    if refs != EXPECTED_QUESTION_REFS:
        _fail(f"visible source obligations are not fully mapped: got {sorted(refs)}")

    section_iii = next(row for row in evidence if row["question_ref"] == "ENG-G4-WS09-III")
    if section_iii.get("source_boundary_required") is not True:
        _fail("Section III must require source-boundary handling")
    if not any("traditional" in text for text in section_iii.get("ambiguity", [])):
        _fail("Section III must preserve traditional ambiguity explicitly")

    for row in evidence:
        blueprint = row["learning_support_blueprint"]
        if blueprint["fresh_retry"].get("conceptual_support") != "H0":
            _fail(f"{row['question_ref']} does not fade to an H0 fresh retry")
        if blueprint["fresh_retry"].get("must_be_new_item") is not True:
            _fail(f"{row['question_ref']} fresh retry must be structurally new")
        coverage = blueprint["coverage_obligations"]
        for key in ("teach", "model", "practice", "hints", "verify", "answer_or_rubric"):
            if coverage.get(key) is not True:
                _fail(f"{row['question_ref']} is missing {key} coverage")
        response = row["response_demand"]
        if response.get("teacher_or_source_judgement_required") is True:
            if "exact_answer" in response or "model_answer" in row:
                _fail(f"{row['question_ref']} incorrectly reduces an open response to exact matching")

    plans = handoff["learning_representation_plans"]
    if len(plans) != len(EXPECTED_QUESTION_REFS):
        _fail("handoff plan count does not match source-obligation count")
    for plan in plans:
        if "INDEPENDENT_RETRY" not in plan["teaching_sequence"]:
            _fail(f"{plan['question_ref']} lacks independent retry")
        if not plan["representations"]:
            _fail(f"{plan['question_ref']} lacks typed representation requirements")

    invariants = handoff["authoring_invariants"]
    expected_true = {
        "source_model_force_fit": False,
        "open_response_exact_string_grading": False,
        "learner_evidence_separate_from_source_truth": True,
        "fresh_h0_retry_required_after_support": True,
    }
    for key, value in expected_true.items():
        if invariants.get(key) is not value:
            _fail(f"authoring invariant {key} drifted")

    print("Grade 4 English V2 worksheet-09 source coverage and semantic authoring acceptance passed.")


if __name__ == "__main__":
    main()
