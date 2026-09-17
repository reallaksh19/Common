#!/usr/bin/env python3
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def fail(msg):
    raise AssertionError(msg)


def validate_state(state):
    schema = load("contracts/calibration-audit-state.schema.json")
    policy = load("policy/calibration-audit-layer.v1.json")
    ccu = load("policy/content-custody-coverage-unit.v2.json")
    jsonschema.validate(state, schema)

    for domain_name in ("duplication", "difficulty", "learner_fit"):
        domain = state[domain_name]
        maturity = domain["maturity"]
        if maturity == "ENGINEERING":
            if domain["validated_policy_ref"] is not None:
                fail(f"{domain_name}: ENGINEERING state cannot cite validated policy")
            if domain.get("approval_ref") is not None:
                fail(f"{domain_name}: ENGINEERING state cannot claim validation approval")
        elif maturity == "CALIBRATING":
            if not domain["evidence_refs"]:
                fail(f"{domain_name}: CALIBRATING requires evidence refs")
            if domain["validated_policy_ref"] is not None:
                fail(f"{domain_name}: CALIBRATING cannot cite validated policy")
        elif maturity == "VALIDATED":
            held = domain["held_out_evaluation"]
            if not domain["evidence_refs"]:
                fail(f"{domain_name}: VALIDATED requires evidence refs")
            if held["status"] != "COMPLETE" or not held.get("report_ref"):
                fail(f"{domain_name}: VALIDATED requires complete held-out evaluation")
            if not domain["validated_policy_ref"]:
                fail(f"{domain_name}: VALIDATED requires versioned policy ref")
            if not domain.get("approval_ref"):
                fail(f"{domain_name}: VALIDATED requires approval ref")

    if state["duplication"]["maturity"] == "ENGINEERING":
        if ccu["similarity"]["lexical_five_shingle_jaccard"]["engineering_threshold_action"] != "REVIEW_ONLY":
            fail("ENGINEERING lexical similarity threshold cannot auto-block")
        if ccu["similarity"]["structural_fingerprint"]["engineering_threshold_action"] != "REVIEW_ONLY":
            fail("ENGINEERING structural similarity threshold cannot auto-block")
        if ccu["similarity"]["semantic_similarity"]["hardcoded_universal_cosine_threshold_allowed"]:
            fail("universal semantic cosine threshold is forbidden before calibration")

    if policy["duplication_calibration"]["current_maturity"] != state["duplication"]["maturity"]:
        fail("duplication calibration policy/state maturity drift")
    if policy["difficulty_calibration"]["current_maturity"] != state["difficulty"]["maturity"]:
        fail("difficulty calibration policy/state maturity drift")
    if policy["learner_fit_calibration"]["current_maturity"] != state["learner_fit"]["maturity"]:
        fail("learner-fit calibration policy/state maturity drift")

    return True


def main():
    state = load("calibration/physics-calibration-state.v1.json")
    validate_state(state)
    print("Physics CAL maturity / promotion guards: PASS")


if __name__ == "__main__":
    main()
