#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import fail, load, validate_schema

EXPECTED = {
    "CORE1A": {
        "mode": "DECLARATIVE",
        "role": "BUILD_UNDERSTANDING",
        "attempt_before_explanation": False,
        "required_moves": {"SEE", "CONNECT", "EXPLAIN", "RECONSTRUCT", "VERIFY"},
    },
    "CORE1B": {
        "mode": "OPEN_ENDED",
        "role": "RECONSTRUCT_AND_CONSOLIDATE",
        "attempt_before_explanation": True,
        "required_moves": {"PREDICT", "REPRESENT", "EXPLAIN", "RECONSTRUCT", "CONTRAST", "INDEPENDENT_USE", "VERIFY"},
    },
    "CORE2A": {
        "mode": "DECLARATIVE",
        "role": "SOLUTION_APPRENTICESHIP",
        "attempt_before_explanation": False,
        "required_moves": {"RECOGNIZE", "REPRESENT", "FOLLOW_EXPERT_MOVE", "JUSTIFY", "COMPARE_WRONG_CHAIN", "VERIFY", "VARY"},
    },
    "CORE2B": {
        "mode": "OPEN_ENDED",
        "role": "SELECT_TRANSFER_DISCRIMINATE_SYNTHESIZE",
        "attempt_before_explanation": True,
        "required_moves": {"ATTEMPT", "CLASSIFY", "SELECT_REPRESENTATION", "SELECT_METHOD", "TRANSFER", "DISCRIMINATE", "SYNTHESIZE", "VERIFY"},
    },
}

CORE1B_HELP = {"MEANING_HELP", "REPRESENTATION_HELP", "CONCEPT_HELP", "FIRST_MOVE_HELP", "PROCEDURE_HELP", "ANSWER_VERIFICATION"}
CORE2A_HELP = {"RECOGNITION_HELP", "REPRESENTATION_HELP", "FIRST_MOVE_HELP", "PROCEDURE_HELP", "FULL_WORKING", "ANSWER_VERIFICATION"}
CORE2B_HELP = {"RECOGNITION_HELP", "CONCEPT_HELP", "REPRESENTATION_HELP", "FIRST_MOVE_HELP", "METHOD_HELP", "ANSWER_VERIFICATION"}

EXPECTED_DEPTH = {
    "EASY": {
        "max_pages": 10,
        "pedagogy_web_research": "OPTIONAL",
        "research_depth": "NONE",
        "subsubtopic_decomposition_allowed": False,
        "visual_intensity": "STANDARD",
        "step_by_step_required": True,
        "dedicated_diagrams_required": True,
    },
    "MEDIUM": {
        "max_pages": 20,
        "pedagogy_web_research": "REQUIRED",
        "research_depth": "STANDARD",
        "subsubtopic_decomposition_allowed": True,
        "visual_intensity": "HIGH",
        "step_by_step_required": True,
        "dedicated_diagrams_required": True,
    },
    "HARD": {
        "max_pages": 30,
        "pedagogy_web_research": "REQUIRED",
        "research_depth": "DEEP",
        "subsubtopic_decomposition_allowed": True,
        "visual_intensity": "VERY_HIGH",
        "step_by_step_required": True,
        "dedicated_diagrams_required": True,
    },
}


def validate_contract(doc: dict) -> None:
    validate_schema(doc, "math-self-teaching-contract.schema.json")
    if doc.get("self_taught") is not True:
        fail("MATH_SELF_TEACHING_REQUIRED")

    profiles = doc["stage_profiles"]
    for stage, exp in EXPECTED.items():
        row = profiles[stage]
        if row["mode"] != exp["mode"]:
            fail("MATH_SELF_TEACHING_STAGE_MODE_DRIFT", stage)
        if row["role"] != exp["role"]:
            fail("MATH_SELF_TEACHING_STAGE_ROLE_DRIFT", stage)
        if row["attempt_before_explanation"] is not exp["attempt_before_explanation"]:
            fail("MATH_SELF_TEACHING_ATTEMPT_ORDER_DRIFT", stage)
        moves = set(row["required_cognitive_moves"])
        if not exp["required_moves"].issubset(moves):
            fail("MATH_SELF_TEACHING_COGNITIVE_MOVE_GAP", stage)
        answer = row["answer_support"]
        if not all(answer.values()):
            fail("MATH_SELF_TEACHING_ANSWER_CLOSURE_GAP", stage)
        visual = row["visual_contract"]
        if not visual["must_make_visible"] or not visual["must_not_imply"]:
            fail("MATH_SELF_TEACHING_VISUAL_CONTRACT_INCOMPLETE", stage)

    if not CORE1B_HELP.issubset(set(profiles["CORE1B"]["help_path"])):
        fail("MATH_CORE1B_SELF_GUIDED_HELP_INCOMPLETE")
    if not CORE2A_HELP.issubset(set(profiles["CORE2A"]["help_path"])):
        fail("MATH_CORE2A_SOLUTION_APPRENTICESHIP_INCOMPLETE")
    if not CORE2B_HELP.issubset(set(profiles["CORE2B"]["help_path"])):
        fail("MATH_CORE2B_TRANSFER_HELP_INCOMPLETE")

    governance = doc["generation_governance"]
    c1 = governance["core1_series"]
    if c1["learner_knowledge_controls_depth"]:
        fail("MATH_CORE1_DEPTH_MAY_NOT_USE_KNOWLEDGE_PERCENT")
    if not c1["page_budget_is_cap_not_target"]:
        fail("MATH_CORE1_PAGE_BUDGET_MUST_BE_CAP")
    if not c1["pedagogy_research_does_not_change_authority"]:
        fail("MATH_CORE1_RESEARCH_AUTHORITY_DRIFT")
    if not c1["research_source_count_is_not_quality_proxy"]:
        fail("MATH_CORE1_RESEARCH_COUNT_PROXY_FORBIDDEN")
    for badge, expected in EXPECTED_DEPTH.items():
        if c1["difficulty_badges"][badge] != expected:
            fail("MATH_CORE1_DIFFICULTY_BADGE_POLICY_DRIFT", badge)

    c2 = governance["core2_series"]
    if c2["calibration_applies_to"] != ["CORE2A", "CORE2B"]:
        fail("MATH_CORE2_CALIBRATION_SCOPE_DRIFT")
    required_true = [
        "learner_knowledge_percent_required_unless_owner_waiver",
        "owner_waiver_allowed",
        "missing_calibration_blocks_generation",
        "purpose_still_required",
        "no_silent_default",
        "core2a_question_demand_is_calibrated",
        "core2b_transfer_demand_is_calibrated",
        "owner_waiver_must_supply_all_resolved_controls",
    ]
    if not all(c2[k] for k in required_true):
        fail("MATH_CORE2_CALIBRATION_POLICY_WEAKENED")
    if c2["knowledge_percent_is_mastery_claim"]:
        fail("MATH_CORE2_KNOWLEDGE_PERCENT_NOT_MASTERY")

    inv = doc["global_invariants"]
    if not all(inv.values()):
        fail("MATH_SELF_TEACHING_GLOBAL_INVARIANT_FALSE")


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate Mathematics self-teaching pedagogy contract.")
    ap.add_argument("--input", required=True)
    args = ap.parse_args()
    doc = load(args.input)
    validate_contract(doc)
    print(json.dumps({"status": "PASS", "stages": sorted(doc["stage_profiles"])}, indent=2))


if __name__ == "__main__":
    main()
