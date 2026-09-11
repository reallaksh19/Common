#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
PHYSICS = D.parent
sys.path.insert(0, str(D / "engine"))
from review_physics_assessment import build_review, digest_without_field  # noqa: E402

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def redigest_registry(registry):
    registry["registry_digest"] = digest_without_field(registry, "registry_digest")
    return registry

def redigest_policy(policy):
    policy["policy_digest"] = digest_without_field(policy, "policy_digest")
    return policy

def expect_fail(code, fn):
    try:
        fn()
    except ValueError as exc:
        if code not in str(exc):
            raise AssertionError(f"expected {code}, got {exc}") from exc
        return
    raise AssertionError(f"expected failure {code}")

questions = load(PHYSICS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
registry = load(D / "registry" / "physics-item-validity-registry.json")
policy = load(D / "policies" / "diagnostic-use-policy.json")

bundle = build_review(questions, registry, policy, "TEST")
by_ref = {x["item_ref"]: x for x in bundle["item_reviews"]}

assert bundle["attempt_data_consumed"] is False
assert bundle["review_precedes_attempt_interpretation"] is True
assert len(bundle["item_reviews"]) == 17
assert by_ref["Q3"]["validity_state"] == "VALID_ASSUMPTION_SENSITIVE"
assert by_ref["Q3"]["required_model_assumptions"]
assert by_ref["Q8"]["source_integrity_review"]["representation_bindings"][0]["representation_ref"] == "FIG-Q8-VT"
assert by_ref["Q10"]["validity_state"] == "UNDERDETERMINED"
assert by_ref["Q10"]["diagnostic_constraints"]["negative_inference_allowed"] is False
assert by_ref["Q13"]["source_integrity_state"] == "TRUNCATED_OR_MISSING_FIGURE"
assert by_ref["Q13"]["source_integrity_review"]["reconstruction_performed"] is False
assert by_ref["Q14"]["source_integrity_state"] == "TYPOGRAPHIC_OR_OCR_AMBIGUITY"
assert by_ref["Q14"]["source_integrity_review"]["ambiguity_resolution_state"] == "UNRESOLVED"
assert by_ref["Q14"]["diagnostic_use"] == "EXCLUDE_FROM_NEGATIVE_INFERENCE"

# OCR_AMBIGUITY_SILENTLY_CORRECTED
bad = copy.deepcopy(registry)
q14 = next(x for x in bad["reviews"] if x["item_ref"] == "Q14")
q14.setdefault("source_integrity_override", {})["ambiguity_resolution_state"] = "RESOLVED"
redigest_registry(bad)
expect_fail("OCR_AMBIGUITY_SILENTLY_CORRECTED", lambda: build_review(questions, bad, policy))

# UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS
bad = copy.deepcopy(registry)
q10 = next(x for x in bad["reviews"] if x["item_ref"] == "Q10")
q10["diagnostic_use"] = "FULL"
redigest_registry(bad)
expect_fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", lambda: build_review(questions, bad, policy))

# MISSING_FIGURE_SILENTLY_INVENTED
bad = copy.deepcopy(registry)
q13 = next(x for x in bad["reviews"] if x["item_ref"] == "Q13")
q13.setdefault("source_integrity_override", {})["reconstruction_performed"] = True
redigest_registry(bad)
expect_fail("MISSING_FIGURE_SILENTLY_INVENTED", lambda: build_review(questions, bad, policy))

# ASSUMPTION_SENSITIVE_ITEM_LOSES_ASSUMPTION
bad = copy.deepcopy(registry)
q3 = next(x for x in bad["reviews"] if x["item_ref"] == "Q3")
q3["required_model_assumptions"] = []
redigest_registry(bad)
expect_fail("ASSUMPTION_SENSITIVE_ITEM_LOSES_ASSUMPTION", lambda: build_review(questions, bad, policy))

# SOURCE_KEY_OVERRIDES_CANONICAL_PHYSICS
bad = copy.deepcopy(registry)
q5 = next(x for x in bad["reviews"] if x["item_ref"] == "Q5")
q5["canonical_answer"]["accepted_option_labels"] = ["a"]
redigest_registry(bad)
expect_fail("SOURCE_KEY_OVERRIDES_CANONICAL_PHYSICS", lambda: build_review(questions, bad, policy))

# DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR
bad = copy.deepcopy(registry)
q9 = next(x for x in bad["reviews"] if x["item_ref"] == "Q9")
q9["diagnostic_use"] = "FULL"
redigest_registry(bad)
expect_fail("DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR", lambda: build_review(questions, bad, policy))

# REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS
bad = copy.deepcopy(registry)
q1 = next(x for x in bad["reviews"] if x["item_ref"] == "Q1")
q1["validity_state"] = "REVIEW_REQUIRED"
q1["diagnostic_use"] = "FULL"
redigest_registry(bad)
expect_fail("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS", lambda: build_review(questions, bad, policy))

# ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS
bad = copy.deepcopy(registry)
bad["learner_state"] = {"Q1": "WEAK"}
redigest_registry(bad)
expect_fail("ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS", lambda: build_review(questions, bad, policy))

# ITEM_REVIEW_COVERAGE_GAP
bad = copy.deepcopy(registry)
bad["reviews"] = [x for x in bad["reviews"] if x["item_ref"] != "Q14.c"]
redigest_registry(bad)
expect_fail("ITEM_REVIEW_COVERAGE_GAP", lambda: build_review(questions, bad, policy))

# ITEM_REVIEW_SOURCE_DRIFT
bad = copy.deepcopy(registry)
q2 = next(x for x in bad["reviews"] if x["item_ref"] == "Q2")
q2["source_question_digest"] = "0" * 64
redigest_registry(bad)
expect_fail("ITEM_REVIEW_SOURCE_DRIFT", lambda: build_review(questions, bad, policy))

# Source-key mismatch is only safe when explicitly classified KEY_ERROR.
bad = copy.deepcopy(registry)
q5 = next(x for x in bad["reviews"] if x["item_ref"] == "Q5")
q5["canonical_answer"]["accepted_option_labels"] = ["a"]
q5["validity_state"] = "KEY_ERROR"
q5["diagnostic_use"] = "PARTIAL"
redigest_registry(bad)
safe = build_review(questions, bad, policy, "KEY-ERROR-SAFE")
assert next(x for x in safe["item_reviews"] if x["item_ref"] == "Q5")["source_key_status"] == "MISMATCH"

# Deterministic semantic replay.
a = build_review(questions, registry, policy, "DET")
b = build_review(questions, registry, policy, "DET")
assert a == b

print("PHYSICS P-B assessment-review falsifiers = 11 PASS")
