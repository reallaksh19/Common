#!/usr/bin/env python3
"""Validate Grade 4 Math V2 learning-representation contracts and falsifiers."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.LearningDesign.engine.build_learning_representation import (
    LearningRepresentationError,
    PRIMARY_SUPPORT_G4_5,
    build_learning_representation,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "learning_representation" / "cases.json"
EXTENDED_FIXTURE = ROOT / "fixtures" / "learning_representation" / "extended_cases.json"


def fail(message: str) -> None:
    raise SystemExit(f"Grade 4 Math V2 learning-representation validation failed: {message}")


def expect_error(task, code: str) -> None:
    try:
        build_learning_representation(task)
    except LearningRepresentationError as exc:
        if exc.code != code:
            fail(f"expected {code}, got {exc.code}: {exc.message}")
        return
    fail(f"expected {code}, but validation succeeded")


def load_cases():
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
    extended = json.loads(EXTENDED_FIXTURE.read_text(encoding="utf-8"))["cases"]
    return base + extended


def validate_positive_cases() -> None:
    cases = load_cases()
    required = {
        "MONEY_TWO_PART",
        "REMAINDER_REPRESENTATIVE_SAMPLE",
        "LONG_DIVISION_7048_24",
        "ANGLE_DRAWING",
        "SAME_RATE_HATS_120_240",
        "DIVISION_TABLE_720_480",
    }
    seen = {case["case_id"] for case in cases}
    if seen != required:
        fail(f"fixture set mismatch: {sorted(seen)}")

    results = {}
    for case in cases:
        result = build_learning_representation(case["task"])
        results[case["case_id"]] = result
        if result.get("publisher_invention_allowed") is not False:
            fail(f"{case['case_id']}: publisher invention must be false")
        if set(result.get("hint_visuals", {})) != {"H1", "H2", "H3"}:
            fail(f"{case['case_id']}: H1/H2/H3 visual coverage incomplete")
        if not result.get("thinking_path_micro_visual_refs"):
            fail(f"{case['case_id']}: thinking-path microvisuals missing")
        if result.get("fresh_retry_support_policy") != "NONE":
            fail(f"{case['case_id']}: fresh H0 inherited support")
        if (result.get("solution_guard") or {}).get("policy") != "FORBID_DURING_HINTS_AND_THINKING_PATH":
            fail(f"{case['case_id']}: solution guard policy missing")

    rem = results["REMAINDER_REPRESENTATIVE_SAMPLE"]["primary_visual"]
    if rem.get("fidelity") != "REPRESENTATIVE_SAMPLE" or not rem["semantic_params"].get("continuation_marker"):
        fail("remainder fixture did not preserve representative-sample honesty")

    long_div = results["LONG_DIVISION_7048_24"]
    if long_div.get("work_surface_ref") != "WS-DIV-7048-24":
        fail("long division fixture lost required work surface")

    angle = results["ANGLE_DRAWING"]
    if angle.get("work_surface_ref") != "WS-ANGLE-01":
        fail("angle drawing fixture lost learner drawing workspace")

    rate = results["SAME_RATE_HATS_120_240"]["primary_visual"]["semantic_params"]
    if rate.get("scale_factor") != 2 or rate.get("target_count") != 6:
        fail("same-rate fixture lost linked x2 scaling")

    table = results["DIVISION_TABLE_720_480"]
    if table.get("work_surface_ref") != "WS-DIV-TABLE-720-480":
        fail("division-table fixture lost required workspace")


def validate_falsifiers() -> None:
    cases = {case["case_id"]: case["task"] for case in load_cases()}

    missing_hint_visual = copy.deepcopy(cases["MONEY_TWO_PART"])
    missing_hint_visual["hint_ladder"]["steps"][0]["visual_state_ref"] = "DOES-NOT-EXIST"
    expect_error(missing_hint_visual, "HINT_STEP_WITHOUT_VISUAL_WHEN_REPRESENTATION_REQUIRED")

    answer_leak = copy.deepcopy(cases["MONEY_TWO_PART"])
    answer_leak["hint_ladder"]["steps"][2]["may_reveal_final_answer"] = True
    expect_error(answer_leak, "H3_REVEALS_COMPLETE_SOLUTION")

    concrete_text_leak = copy.deepcopy(cases["MONEY_TWO_PART"])
    concrete_text_leak["solution_tokens"] = ["520"]
    concrete_text_leak["hint_ladder"]["steps"][2]["verbal_cue"] = "The total is 520."
    expect_error(concrete_text_leak, "SOLUTION_TOKEN_VISIBLE_DURING_SUPPORT")

    concrete_visual_leak = copy.deepcopy(cases["MONEY_TWO_PART"])
    concrete_visual_leak["solution_tokens"] = ["520"]
    h3_ref = concrete_visual_leak["hint_ladder"]["steps"][2]["visual_state_ref"]
    h3_state = next(state for state in concrete_visual_leak["visual_states"] if state["visual_state_id"] == h3_ref)
    h3_state["semantic_params"]["final_total"] = 520
    expect_error(concrete_visual_leak, "SOLUTION_TOKEN_VISIBLE_DURING_SUPPORT")

    allowed_operand = copy.deepcopy(cases["MONEY_TWO_PART"])
    allowed_operand["solution_tokens"] = ["50"]
    allowed_operand["allowed_support_solution_tokens"] = ["50"]
    build_learning_representation(allowed_operand)

    no_fresh_retry = copy.deepcopy(cases["MONEY_TWO_PART"])
    no_fresh_retry["fresh_retry_ref"] = "DIFFERENT-FRESH-REF"
    expect_error(no_fresh_retry, "H3_WITHOUT_FRESH_H0_RETRY")

    false_sample = copy.deepcopy(cases["REMAINDER_REPRESENTATIVE_SAMPLE"])
    false_sample["primary_visual"]["semantic_params"].pop("continuation_marker")
    expect_error(false_sample, "REPRESENTATIVE_SAMPLE_WITHOUT_CONTINUATION_MARKER")

    no_division_surface = copy.deepcopy(cases["LONG_DIVISION_7048_24"])
    no_division_surface.pop("work_surface")
    expect_error(no_division_surface, "PROCEDURAL_DIVISION_WITHOUT_LONG_DIVISION_WORK_SURFACE")

    broken_division = copy.deepcopy(cases["LONG_DIVISION_7048_24"])
    broken_division["work_surface"]["semantic_params"]["remainder"] = 15
    expect_error(broken_division, "PRIMARY_VISUAL_ALGORITHM_INVALID")

    quotient_slot_loss = copy.deepcopy(cases["LONG_DIVISION_7048_24"])
    quotient_slot_loss["work_surface"]["semantic_params"]["quotient_places"] = [2, 3]
    expect_error(quotient_slot_loss, "DIVISION_QUOTIENT_PLACE_SLOTS_INVALID")

    no_angle_geometry = copy.deepcopy(cases["ANGLE_DRAWING"])
    no_angle_geometry["primary_visual"]["primitive_kind"] = "TEXT_LABEL"
    for state in no_angle_geometry["visual_states"]:
        state["primitive_kind"] = "TEXT_LABEL"
    expect_error(no_angle_geometry, "ANGLE_TASK_WITHOUT_RENDERED_RAYS")

    tiny_font = copy.deepcopy(cases["MONEY_TWO_PART"])
    tiny_font["learner_profile"] = copy.deepcopy(PRIMARY_SUPPORT_G4_5)
    tiny_font["learner_profile"]["body_font_min_pt"] = 9
    expect_error(tiny_font, "LEARNER_FONT_MIN")

    broken_rate = copy.deepcopy(cases["SAME_RATE_HATS_120_240"])
    broken_rate["primary_visual"]["semantic_params"]["target_count"] = 5
    expect_error(broken_rate, "SAME_RATE_SCALE_INVALID")

    no_table_surface = copy.deepcopy(cases["DIVISION_TABLE_720_480"])
    no_table_surface.pop("work_surface")
    expect_error(no_table_surface, "DIVISION_TABLE_WITHOUT_WORKSPACE")

    broken_table = copy.deepcopy(cases["DIVISION_TABLE_720_480"])
    broken_table["work_surface"]["semantic_params"]["cells"][0]["quotient"] = 11
    expect_error(broken_table, "DIVISION_TABLE_ARITHMETIC_INVALID")


def validate_no_renderer_dependency() -> None:
    source = (ROOT / "engine" / "build_learning_representation.py").read_text(encoding="utf-8").lower()
    forbidden = ["reportlab", "publication.engine", "canvas", "pagemetrics", "boundingbox"]
    leaks = [token for token in forbidden if token in source]
    if leaks:
        fail(f"learning-design engine leaked renderer dependency: {leaks}")


def main() -> None:
    validate_positive_cases()
    validate_falsifiers()
    validate_no_renderer_dependency()
    print("Grade 4 Math V2 learning representation: fixtures and falsifiers PASS")


if __name__ == "__main__":
    main()
