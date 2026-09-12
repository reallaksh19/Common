"""Primary Math V2 learning-design -> representation contract builder.

This module deliberately does not render pages and does not infer pedagogy from raw
question text. It consumes an explicit, upstream-authored learning-support spec,
validates Primary #182/#164 support semantics, and emits a publisher-neutral
LearningRepresentationPlan.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping


@dataclass
class LearningRepresentationError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


PRIMARY_SUPPORT_G4_5 = {
    "schema_version": "1.0.0",
    "profile_id": "PRIMARY_SUPPORT_G4_5",
    "body_font_min_pt": 12.0,
    "micro_label_min_pt": 9.5,
    "heading_min_pt": 16.0,
    "visual_area_target": {"min": 0.45, "max": 0.60},
    "workspace_area_target": {"min": 0.20, "max": 0.30},
    "text_area_max": 0.25,
    "max_major_learning_zones_per_page": 3,
    "solution_on_hint_page": False,
    "progressive_disclosure": True,
    "internal_semantic_labels_visible": False,
    "supported_success_counts_as_independent": False,
    "fresh_retry_required_after_support": True,
    "shrink_to_fit_child_readability": False,
}

_ALLOWED_HINTS = (
    ("H1", "NOTICE", "LOOK"),
    ("H2", "REMEMBER", "REMEMBER"),
    ("H3", "REPRESENT", "SHOW IT"),
)
_ALLOWED_CHILD_LABELS = {"LOOK", "SHOW IT", "WORK", "PUT TOGETHER", "CHECK"}
_INTERNAL_ROLES = {"INTERPRET", "MODEL", "EXECUTE", "COMBINE", "VERIFY"}


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise LearningRepresentationError(code, message)


def _require_keys(obj: Mapping[str, Any], keys: Iterable[str], code: str, owner: str) -> None:
    missing = [key for key in keys if key not in obj]
    _require(not missing, code, f"{owner} missing fields {missing}")


def validate_learner_profile(profile: Mapping[str, Any]) -> None:
    _require(profile.get("body_font_min_pt", 0) >= 12, "LEARNER_FONT_MIN", "body font must be >= 12pt")
    _require(profile.get("micro_label_min_pt", 0) >= 9.5, "LEARNER_FONT_MIN", "micro labels must be >= 9.5pt")
    _require(profile.get("heading_min_pt", 0) >= 16, "LEARNER_FONT_MIN", "headings must be >= 16pt")
    _require(profile.get("solution_on_hint_page") is False, "COMPLETE_SOLUTION_VISIBLE_DURING_HINT_LADDER", "solution_on_hint_page must be false")
    _require(profile.get("progressive_disclosure") is True, "LEARNER_PROFILE_INVALID", "progressive disclosure is required")
    _require(profile.get("internal_semantic_labels_visible") is False, "INTERNAL_REASONING_ROLE_EXPOSED_AS_PRIMARY_CHILD_LABEL", "internal semantic roles must stay hidden")
    _require(profile.get("supported_success_counts_as_independent") is False, "SUPPORTED_SUCCESS_COUNTED_AS_INDEPENDENT", "supported success cannot count as independent")
    _require(profile.get("fresh_retry_required_after_support") is True, "H3_WITHOUT_FRESH_H0_RETRY", "fresh retry is required after support")
    _require(profile.get("shrink_to_fit_child_readability") is False, "PAGE_FIT_ACHIEVED_BY_SHRINKING_CHILD_READABILITY", "shrink-to-fit is forbidden")
    visual = profile.get("visual_area_target", {})
    workspace = profile.get("workspace_area_target", {})
    _require(0.45 <= visual.get("min", 0) <= visual.get("max", 0) <= 0.60, "VISUAL_AREA_PROFILE", "visual area target must stay within 45%-60%")
    _require(0.20 <= workspace.get("min", 0) <= workspace.get("max", 0) <= 0.30, "LEARNER_PROFILE_INVALID", "workspace target must stay within 20%-30%")
    _require(profile.get("text_area_max", 1) <= 0.25, "LEARNER_PROFILE_INVALID", "text area must be <= 25%")


def validate_visual_state(state: Mapping[str, Any], owner: str) -> None:
    _require_keys(
        state,
        ["visual_state_id", "primitive_kind", "representation_ref", "fidelity", "fade_mode", "semantic_params", "validator_refs"],
        "VISUAL_STATE_INCOMPLETE",
        owner,
    )
    _require(bool(state.get("validator_refs")), "UNVALIDATED_VISUAL_DRAWN", f"{owner} has no validator refs")
    fidelity = state["fidelity"]
    params = state.get("semantic_params") or {}
    if fidelity == "EXACT" and "declared_quantity" in params and "rendered_quantity" in params:
        _require(
            params["declared_quantity"] == params["rendered_quantity"],
            "PRIMARY_VISUAL_QUANTITATIVE_MISMATCH",
            f"{owner}: declared/rendered quantity mismatch",
        )
    if fidelity == "REPRESENTATIVE_SAMPLE":
        _require(bool(params.get("continuation_marker")), "REPRESENTATIVE_SAMPLE_WITHOUT_CONTINUATION_MARKER", f"{owner} needs an explicit continuation marker")
        if "declared_quantity" in params and "rendered_quantity" in params:
            _require(params["rendered_quantity"] <= params["declared_quantity"], "PRIMARY_VISUAL_QUANTITATIVE_MISMATCH", f"{owner}: representative sample exceeds declared quantity")


def validate_hint_ladder(ladder: Mapping[str, Any], visual_states: Mapping[str, Mapping[str, Any]]) -> None:
    steps = list(ladder.get("steps") or [])
    _require(len(steps) == 3, "HINT_LADDER_INVALID", "Primary hint ladder must contain H1/H2/H3")
    for step, expected in zip(steps, _ALLOWED_HINTS):
        level, role, child_label = expected
        _require(step.get("level") == level, "HINT_LADDER_INVALID", f"expected {level}")
        _require(step.get("semantic_role") == role, "HINT_LADDER_INVALID", f"{level} must use {role}")
        _require(step.get("child_label") == child_label, "HINT_LADDER_INVALID", f"{level} child label must be {child_label}")
        ref = step.get("visual_state_ref")
        _require(ref in visual_states, "HINT_STEP_WITHOUT_VISUAL_WHEN_REPRESENTATION_REQUIRED", f"{level} visual state {ref!r} missing")
        validate_visual_state(visual_states[ref], f"{level} visual")
        _require(step.get("may_reveal_final_answer") is False, "H3_REVEALS_COMPLETE_SOLUTION" if level == "H3" else "HINT_REVEALS_COMPLETE_SOLUTION", f"{level} may not reveal final answer")
    _require(bool(ladder.get("fresh_retry_ref")), "H3_WITHOUT_FRESH_H0_RETRY", "fresh H0 ref is required")


def validate_thinking_path(path: Mapping[str, Any], visual_states: Mapping[str, Mapping[str, Any]]) -> None:
    steps = list(path.get("steps") or [])
    _require(2 <= len(steps) <= 6, "THINKING_PATH_INVALID", "thinking path requires 2-6 steps")
    for step in steps:
        role = step.get("semantic_role")
        child = step.get("child_label")
        _require(role in _INTERNAL_ROLES, "THINKING_PATH_INVALID", f"unknown semantic role {role}")
        _require(child in _ALLOWED_CHILD_LABELS, "THINKING_PATH_INVALID", f"unknown child label {child}")
        _require(child != role, "INTERNAL_REASONING_ROLE_EXPOSED_AS_PRIMARY_CHILD_LABEL", f"{role} leaked as child label")
        ref = step.get("micro_visual_ref")
        _require(ref in visual_states, "THINKING_PATH_MICRO_VISUAL_MISSING", f"micro visual {ref!r} missing")
        validate_visual_state(visual_states[ref], f"thinking step {step.get('step_id', '<unknown>')}")


def validate_long_division_surface(surface: Mapping[str, Any]) -> None:
    params = surface.get("semantic_params") or {}
    _require_keys(params, ["dividend", "divisor", "quotient", "remainder", "quotient_places", "steps", "check"], "LONG_DIVISION_WORK_SURFACE_INVALID", "long division")
    dividend = int(params["dividend"])
    divisor = int(params["divisor"])
    quotient = int(params["quotient"])
    remainder = int(params["remainder"])
    _require(divisor > 0, "LONG_DIVISION_WORK_SURFACE_INVALID", "divisor must be positive")
    _require(divisor * quotient + remainder == dividend, "PRIMARY_VISUAL_ALGORITHM_INVALID", "D*Q+R must equal dividend")
    _require(0 <= remainder < divisor, "PRIMARY_VISUAL_REMAINDER_INVALID", "remainder must satisfy 0 <= R < divisor")
    digits = [int(x) for x in str(quotient)]
    _require(list(params["quotient_places"]) == digits, "DIVISION_QUOTIENT_PLACE_SLOTS_INVALID", "quotient_places must preserve every quotient digit including internal zero")
    for index, step in enumerate(params["steps"]):
        qd = int(step["quotient_digit"])
        partial = int(step["partial_dividend"])
        product = int(step["product"])
        rem = int(step["subtraction_remainder"])
        _require(product == divisor * qd, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: product != divisor*quotient_digit")
        _require(partial - product == rem, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: subtraction remainder mismatch")
        _require(0 <= rem < divisor, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: partial remainder out of range")


def validate_division_table_surface(surface: Mapping[str, Any]) -> None:
    params = surface.get("semantic_params") or {}
    _require_keys(params, ["columns", "rows", "cells"], "DIVISION_TABLE_WORKSPACE_INVALID", "division table")
    columns = [int(x) for x in params["columns"]]
    rows = [int(x) for x in params["rows"]]
    cells = list(params["cells"])
    _require(all(row > 0 for row in rows), "DIVISION_TABLE_WORKSPACE_INVALID", "division-table divisors must be positive")
    expected_pairs = {(column, row) for column in columns for row in rows}
    actual_pairs = {(int(cell["column"]), int(cell["row"])) for cell in cells}
    _require(actual_pairs == expected_pairs, "DIVISION_TABLE_COVERAGE_INVALID", "division table must contain exactly one semantic cell for each row/column pair")
    for cell in cells:
        column = int(cell["column"])
        row = int(cell["row"])
        quotient = int(cell["quotient"])
        _require(column == row * quotient, "DIVISION_TABLE_ARITHMETIC_INVALID", f"{column}/{row} != {quotient}")


def validate_same_rate_task(task: Mapping[str, Any]) -> None:
    if str(task.get("task_kind")) != "SAME_RATE_SCALE":
        return
    primary = task.get("primary_visual") or {}
    _require(primary.get("primitive_kind") in {"RATE_SCALE_MODEL", "SAME_RATE_SCALE"}, "SAME_RATE_VISUAL_REQUIRED", "same-rate task requires a rate/scale visual")
    params = primary.get("semantic_params") or {}
    _require_keys(params, ["base_amount", "target_amount", "base_count", "target_count", "scale_factor"], "SAME_RATE_SCALE_INVALID", "same-rate visual")
    factor = float(params["scale_factor"])
    _require(factor > 0, "SAME_RATE_SCALE_INVALID", "scale factor must be positive")
    _require(float(params["base_amount"]) * factor == float(params["target_amount"]), "SAME_RATE_SCALE_INVALID", "money/quantity scale factor mismatch")
    _require(float(params["base_count"]) * factor == float(params["target_count"]), "SAME_RATE_SCALE_INVALID", "object-count scale factor mismatch")


def validate_division_table_task(task: Mapping[str, Any], surface: Mapping[str, Any] | None) -> None:
    if str(task.get("task_kind")) != "DIVISION_TABLE":
        return
    primary = task.get("primary_visual") or {}
    _require(primary.get("primitive_kind") == "DIVISION_TABLE_MODEL", "DIVISION_TABLE_VISUAL_REQUIRED", "division-table task requires DIVISION_TABLE_MODEL")
    _require(surface is not None and surface.get("kind") == "DIVISION_TABLE_WORKSPACE", "DIVISION_TABLE_WITHOUT_WORKSPACE", "division-table task requires a table workspace")
    validate_division_table_surface(surface)


def validate_work_surface(surface: Mapping[str, Any] | None, task_kind: str) -> None:
    if task_kind == "MULTI_DIGIT_DIVISION":
        _require(surface is not None and surface.get("kind") == "LONG_DIVISION_WORK", "PROCEDURAL_DIVISION_WITHOUT_LONG_DIVISION_WORK_SURFACE", "multi-digit division requires LONG_DIVISION_WORK")
    if surface and surface.get("kind") == "LONG_DIVISION_WORK":
        validate_long_division_surface(surface)
    if surface and surface.get("kind") == "DIVISION_TABLE_WORKSPACE":
        validate_division_table_surface(surface)
    if task_kind.startswith("ANGLE_"):
        _require(surface is not None and surface.get("kind") == "ANGLE_DRAWING_WORKSPACE", "ANGLE_TASK_WITHOUT_RENDERED_RAYS", "angle task requires an angle drawing workspace")


def build_learning_representation(task: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate and emit the publisher-neutral learning representation seam."""
    _require_keys(task, ["task_ref", "task_kind", "representation_class", "primary_visual", "visual_states", "hint_ladder", "thinking_path", "fresh_retry_ref"], "LEARNING_REPRESENTATION_INPUT_INCOMPLETE", "task")
    profile = task.get("learner_profile") or PRIMARY_SUPPORT_G4_5
    validate_learner_profile(profile)

    states = {state["visual_state_id"]: state for state in task["visual_states"]}
    _require(len(states) == len(task["visual_states"]), "DUPLICATE_VISUAL_STATE_ID", task["task_ref"])
    validate_visual_state(task["primary_visual"], "primary visual")
    for state in states.values():
        validate_visual_state(state, state["visual_state_id"])

    validate_hint_ladder(task["hint_ladder"], states)
    validate_thinking_path(task["thinking_path"], states)
    _require(task["hint_ladder"].get("fresh_retry_ref") == task["fresh_retry_ref"], "H3_WITHOUT_FRESH_H0_RETRY", "hint ladder and task must share the same fresh retry ref")

    work_surface = task.get("work_surface")
    validate_work_surface(work_surface, str(task["task_kind"]))
    validate_same_rate_task(task)
    validate_division_table_task(task, work_surface)

    if str(task["task_kind"]).startswith("ANGLE_"):
        primitive_kinds = {task["primary_visual"].get("primitive_kind")} | {x.get("primitive_kind") for x in states.values()}
        _require(bool(primitive_kinds & {"ANGLE_RAYS_ARC", "ANGLE_BENCHMARK_COMPARE", "ANGLE_OBJECT_EXAMPLE"}), "ANGLE_TASK_WITHOUT_RENDERED_RAYS", "angle task must contain actual angle geometry")

    return {
        "schema_version": "1.0.0",
        "plan_id": f"LRP-{task['task_ref']}",
        "task_ref": task["task_ref"],
        "learner_profile_ref": profile["profile_id"],
        "representation_class": task["representation_class"],
        "primary_visual": task["primary_visual"],
        "hint_visuals": {
            step["level"]: states[step["visual_state_ref"]]
            for step in task["hint_ladder"]["steps"]
        },
        "thinking_path_micro_visual_refs": [step["micro_visual_ref"] for step in task["thinking_path"]["steps"]],
        "work_surface_ref": work_surface.get("surface_id") if work_surface else None,
        "hint_ladder_ref": task["hint_ladder"]["ladder_id"],
        "thinking_path_ref": task["thinking_path"]["path_id"],
        "fresh_retry_support_policy": "NONE",
        "reference_visual_ref": task.get("reference_visual_ref"),
        "visual_language_key": dict(task.get("visual_language_key") or {}),
        "publisher_invention_allowed": False,
    }
