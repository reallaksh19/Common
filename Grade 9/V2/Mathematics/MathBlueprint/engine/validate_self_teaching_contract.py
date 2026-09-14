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
