#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
MATH = D.parent
sys.path.insert(0, str(D / "engine"))
sys.path.insert(0, str(MATH / "AssessmentIntake" / "engine"))

from review_math_assessment import build_review, digest_without_field  # noqa: E402
from build_math_assessment_intake import digest as intake_digest, source_payload  # noqa: E402

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

questions = load(MATH / "AssessmentIntake" / "fixtures" / "mixed-grade9-question-set.fixture.json")
registry = load(D / "registry" / "assessment-item-validity-registry.json")
policy = load(D / "policies" / "diagnostic-use-policy.json")

def redigest_registry(r):
    r["registry_digest"] = digest_without_field(r, "registry_digest")
    return r

def expect_error(code, fn):
    try:
        fn()
    except ValueError as exc:
        assert str(exc).startswith(code), (code, str(exc))
        return
    raise AssertionError(f"expected {code}")

bundle = build_review(copy.deepcopy(questions), copy.deepcopy(registry), copy.deepcopy(policy))
assert bundle["review_precedes_attempt_interpretation"] is True
assert bundle["attempt_data_consumed"] is False
assert bundle["summary"]["item_count"] == 17

by_ref = {x["item_ref"]: x for x in bundle["item_reviews"]}
assert set(by_ref) == {f"Q{i}" for i in range(1, 15)} | {"Q14.a", "Q14.b", "Q14.c"}

assert by_ref["Q5"]["validity_state"] == "VALID"
assert by_ref["Q5"]["source_key_status"] == "MATCH"
assert by_ref["Q5"]["canonical_answer"]["accepted_option_labels"] == ["d"]

q9 = by_ref["Q9"]
assert q9["validity_state"] == "UNDERDETERMINED"
assert q9["diagnostic_use"] == "POSITIVE_EVIDENCE_ONLY"
assert q9["diagnostic_constraints"]["negative_inference_allowed"] is False
assert q9["diagnostic_constraints"]["confident_diagnosis_allowed"] is False
assert q9["canonical_answer"]["uniqueness_status"] == "NON_UNIQUE"

q12 = by_ref["Q12"]
assert q12["validity_state"] == "VALID_MULTIPLE_SOLUTIONS"
assert set(q12["canonical_answer"]["accepted_answers"]) == {"(0,2sqrt(3))", "(3,-sqrt(3))"}
assert q12["canonical_answer"]["uniqueness_status"] == "MULTIPLE"

assert by_ref["Q14"]["validity_state"] == "VALID"
assert all(by_ref[p]["validity_state"] == "VALID" for p in ["Q14.a", "Q14.b", "Q14.c"])

bad = copy.deepcopy(registry)
next(x for x in bad["reviews"] if x["item_ref"] == "Q9")["diagnostic_use"] = "FULL"
redigest_registry(bad)
expect_error("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS",
             lambda: build_review(copy.deepcopy(questions), bad, copy.deepcopy(policy)))

bad = copy.deepcopy(registry)
r12 = next(x for x in bad["reviews"] if x["item_ref"] == "Q12")
r12["canonical_answer"]["accepted_answers"] = ["(0,2sqrt(3))"]
redigest_registry(bad)
expect_error("MULTI_SOLUTION_ITEM_FORCED_TO_ONE_KEY",
             lambda: build_review(copy.deepcopy(questions), bad, copy.deepcopy(policy)))

qbad = copy.deepcopy(questions)
q5 = next(x for x in qbad["questions"] if x["question_id"] == "Q5")
q5["answer_key"]["source_assertion"] = "c"
q5["source_provenance"]["source_digest"] = intake_digest(source_payload(q5))
qbad["question_set_digest"] = digest_without_field(qbad, "question_set_digest")

rbad = copy.deepcopy(registry)
r5 = next(x for x in rbad["reviews"] if x["item_ref"] == "Q5")
r5["source_key_assertion"] = "c"
r5["source_question_digest"] = q5["source_provenance"]["source_digest"]
redigest_registry(rbad)
expect_error("SOURCE_KEY_OVERRIDES_CANONICAL_MATH",
             lambda: build_review(qbad, rbad, copy.deepcopy(policy)))

r5["validity_state"] = "KEY_ERROR"
r5["diagnostic_use"] = "PARTIAL"
redigest_registry(rbad)
key_bundle = build_review(qbad, rbad, copy.deepcopy(policy))
key_q5 = {x["item_ref"]: x for x in key_bundle["item_reviews"]}["Q5"]
assert key_q5["source_key_status"] == "MISMATCH"
assert key_q5["canonical_answer"]["accepted_option_labels"] == ["d"]
assert key_q5["diagnostic_constraints"]["negative_inference_allowed"] is False

bad = copy.deepcopy(registry)
r8 = next(x for x in bad["reviews"] if x["item_ref"] == "Q8")
r8["validity_state"] = "REVIEW_REQUIRED"
r8["diagnostic_use"] = "FULL"
redigest_registry(bad)
expect_error("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS",
             lambda: build_review(copy.deepcopy(questions), bad, copy.deepcopy(policy)))

bad = copy.deepcopy(registry)
bad["learner_diagnosis"] = {"invented": True}
redigest_registry(bad)
expect_error("ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS",
             lambda: build_review(copy.deepcopy(questions), bad, copy.deepcopy(policy)))

bad = copy.deepcopy(registry)
bad["reviews"] = [x for x in bad["reviews"] if x["item_ref"] != "Q14.b"]
redigest_registry(bad)
expect_error("ITEM_REVIEW_COVERAGE_GAP",
             lambda: build_review(copy.deepcopy(questions), bad, copy.deepcopy(policy)))

bad = copy.deepcopy(registry)
next(x for x in bad["reviews"] if x["item_ref"] == "Q7")["source_question_digest"] = "0" * 64
redigest_registry(bad)
expect_error("ITEM_REVIEW_SOURCE_DRIFT",
             lambda: build_review(copy.deepcopy(questions), bad, copy.deepcopy(policy)))

again = build_review(copy.deepcopy(questions), copy.deepcopy(registry), copy.deepcopy(policy))
assert json.dumps(bundle, sort_keys=True, separators=(",", ":")) == json.dumps(again, sort_keys=True, separators=(",", ":"))
assert bundle["bundle_digest"] == digest_without_field(bundle, "bundle_digest")

print("MATH M-B assessment-safety falsifiers = 9 PASS")
print("MATH M-B pilot cases = valid MCQ / underdetermined / multi-solution / multi-stage PASS")
