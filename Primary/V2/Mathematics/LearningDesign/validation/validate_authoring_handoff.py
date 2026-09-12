#!/usr/bin/env python3
"""Regression validation for the #336 -> #339 automatic handoff."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Primary.V2.Mathematics.LearningDesign.engine.authoring_handoff import (
    AuthoringHandoffError,
    build_authoring_handoff,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "CoreSkills" / "fixtures" / "authoring" / "cold_start_cases.json"
HANDOFF_SOURCE = Path(__file__).resolve().parents[1] / "engine" / "authoring_handoff.py"


def fail(message: str) -> None:
    raise SystemExit(f"Primary Math V2 authoring handoff failed: {message}")


def load_case(case_id: str):
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
    return copy.deepcopy(next(case["input"] for case in cases if case["case_id"] == case_id))


def multiplication_blueprint():
    return {
        "schema_version": "1.0.0",
        "task_kind": "MULTIPLICATION_BRIDGE",
        "representation_class": "STRUCTURAL",
        "primary": {
            "representation_ref": "REP-MUL-EQUAL-GROUPS",
            "fidelity": "EXACT",
            "fade_mode": "FULL"
        },
        "hint_steps": [
            {
                "level": "H1",
                "semantic_role": "NOTICE",
                "child_label": "LOOK",
                "representation_ref": "REP-MUL-EQUAL-GROUPS",
                "fidelity": "SCHEMATIC",
                "fade_mode": "FULL",
                "verbal_cue": "See 6 equal groups of 23.",
                "learner_action": "Point to the number of groups and the amount in each group.",
                "information_revealed": ["EQUAL_GROUP_STRUCTURE"]
            },
            {
                "level": "H2",
                "semantic_role": "REMEMBER",
                "child_label": "REMEMBER",
                "representation_ref": "REP-MUL-ARRAY",
                "fidelity": "SCHEMATIC",
                "fade_mode": "PARTIAL",
                "verbal_cue": "An array shows the same multiplication.",
                "learner_action": "Connect the 6 groups to 6 rows.",
                "information_revealed": ["ARRAY_CONNECTION"]
            },
            {
                "level": "H3",
                "semantic_role": "REPRESENT",
                "child_label": "SHOW IT",
                "representation_ref": "REP-MUL-WRITTEN",
                "fidelity": "SCHEMATIC",
                "fade_mode": "PARTIAL",
                "verbal_cue": "Set up the written multiplication with place values aligned.",
                "learner_action": "Write the first executable multiplication step.",
                "information_revealed": ["WRITTEN_SETUP"]
            }
        ],
        "thinking_path": [
            {
                "semantic_role": "INTERPRET",
                "child_label": "LOOK",
                "representation_ref": "REP-MUL-EQUAL-GROUPS",
                "fidelity": "SCHEMATIC",
                "fade_mode": "PARTIAL",
                "one_line_action": "See equal groups."
            },
            {
                "semantic_role": "MODEL",
                "child_label": "SHOW IT",
                "representation_ref": "REP-MUL-ARRAY",
                "fidelity": "SCHEMATIC",
                "fade_mode": "PARTIAL",
                "one_line_action": "Show the multiplication as an array."
            },
            {
                "semantic_role": "EXECUTE",
                "child_label": "WORK",
                "representation_ref": "REP-MUL-PARTIALS",
                "fidelity": "SCHEMATIC",
                "fade_mode": "PARTIAL",
                "one_line_action": "Work the partial products."
            },
            {
                "semantic_role": "VERIFY",
                "child_label": "CHECK",
                "representation_ref": "REP-MUL-WRITTEN",
                "fidelity": "SCHEMATIC",
                "fade_mode": "NONE",
                "one_line_action": "Check the written result."
            }
        ],
        "fresh_retry_prompt": "Calculate 34 x 5. Show a useful model first, then solve without hints.",
        "visual_language_key": {
            "groups": "AMBER",
            "structure": "BLUE",
            "check": "GREEN"
        }
    }


def attach_blueprint(primary_input, blueprint=None):
    evidence = primary_input["question_set"]["questions"][0]["evidence"]
    evidence["learning_support_blueprint"] = copy.deepcopy(blueprint or multiplication_blueprint())
    return primary_input


def expect_error(primary_input, code: str) -> None:
    try:
        build_authoring_handoff(primary_input)
    except AuthoringHandoffError as exc:
        if exc.code != code:
            fail(f"expected {code}, got {exc.code}: {exc.message}")
        return
    fail(f"expected {code}, but handoff succeeded")


def validate_positive_handoff() -> None:
    primary_input = attach_blueprint(load_case("QUESTION_ONLY"))
    result = build_authoring_handoff(primary_input)
    coverage = result["coverage"]
    if coverage != {
        "total_modules": 3,
        "planned_modules": 3,
        "independent_probe_modules": 0,
        "unaccounted_modules": 0,
    }:
        fail(f"unexpected coverage {coverage}")
    if result.get("publisher_invention_allowed") is not False:
        fail("publisher invention must remain false")

    for row in result["module_support"]:
        if row["support_status"] != "PLANNED":
            fail(f"unexpected support status {row}")
        plan = row["learning_representation_plan"]
        if set(plan["hint_visuals"]) != {"H1", "H2", "H3"}:
            fail(f"{row['module_id']}: visual hint coverage incomplete")
        if plan.get("fresh_retry_prompt") != multiplication_blueprint()["fresh_retry_prompt"]:
            fail(f"{row['module_id']}: fresh H0 prompt lost")
        if plan.get("publisher_invention_allowed") is not False:
            fail(f"{row['module_id']}: publisher invention changed")
        if not plan.get("all_visual_states") or len(plan.get("thinking_path_micro_visual_refs") or []) != 4:
            fail(f"{row['module_id']}: thinking-path visual realization incomplete")


def validate_probe_exemption() -> None:
    primary_input = load_case("QUESTION_PLUS_WORK")
    result = build_authoring_handoff(primary_input)
    coverage = result["coverage"]
    if coverage["planned_modules"] != 0 or coverage["independent_probe_modules"] != coverage["total_modules"]:
        fail(f"probe modules were not explicitly exempted: {coverage}")
    if any(row["support_status"] != "INDEPENDENT_PROBE_ONLY" for row in result["module_support"]):
        fail("probe module silently received guided hints")


def validate_falsifiers() -> None:
    missing = load_case("QUESTION_ONLY")
    expect_error(missing, "LEARNING_SUPPORT_BLUEPRINT_REQUIRED")

    unknown = attach_blueprint(load_case("QUESTION_ONLY"))
    unknown["question_set"]["questions"][0]["evidence"]["learning_support_blueprint"]["hint_steps"][0]["representation_ref"] = "REP-DOES-NOT-EXIST"
    expect_error(unknown, "LEARNING_SUPPORT_REPRESENTATION_REF_UNKNOWN")

    bad_fade = attach_blueprint(load_case("QUESTION_ONLY"))
    bad_fade["question_set"]["questions"][0]["evidence"]["learning_support_blueprint"]["hint_steps"][2]["fade_mode"] = "EMPTY_FRAME"
    expect_error(bad_fade, "LEARNING_SUPPORT_FADE_MODE_INVALID")

    semantic_override = attach_blueprint(load_case("QUESTION_ONLY"))
    semantic_override["question_set"]["questions"][0]["evidence"]["learning_support_blueprint"]["primary"]["semantic_params_overlay"] = {"group_count": 5}
    expect_error(semantic_override, "SUPPORT_BLUEPRINT_SEMANTIC_OVERRIDE_CONFLICT")


def validate_no_publication_dependency() -> None:
    source = HANDOFF_SOURCE.read_text(encoding="utf-8").lower()
    forbidden = ["reportlab", "publication.engine", "page_composer", "canvas"]
    leaks = [token for token in forbidden if token in source]
    if leaks:
        fail(f"authoring handoff leaked publisher dependency: {leaks}")


def main() -> None:
    validate_positive_handoff()
    validate_probe_exemption()
    validate_falsifiers()
    validate_no_publication_dependency()
    print("Primary Math V2 authoring -> learning representation handoff: PASS")


if __name__ == "__main__":
    main()
