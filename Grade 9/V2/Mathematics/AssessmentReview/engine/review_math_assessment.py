#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]
MATH = D.parent
sys.path.insert(0, str(MATH / "AssessmentIntake" / "engine"))
from build_math_assessment_intake import validate_question_set  # noqa: E402

VALIDITY_STATES = {
    "VALID",
    "VALID_MULTIPLE_SOLUTIONS",
    "UNDERDETERMINED",
    "AMBIGUOUS",
    "KEY_ERROR",
    "DATA_ERROR",
    "REVIEW_REQUIRED",
}
FORBIDDEN_LEARNER_KEYS = {
    "attempt",
    "attempt_set",
    "attempt_interpretation",
    "learner_state",
    "learner_diagnosis",
    "diagnosis",
    "misconception",
    "learner_evidence",
    "observed_answer",
}

def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def digest_without_field(value, field):
    clone = copy.deepcopy(value)
    clone.pop(field, None)
    return digest(clone)

def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def assert_no_learner_inference_payload(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_LEARNER_KEYS:
                fail("ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS", f"{path}.{key}")
            assert_no_learner_inference_payload(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            assert_no_learner_inference_payload(child, f"{path}[{i}]")

def expected_item_bindings(question_set):
    out = {}
    for q in question_set["questions"]:
        qid = q["question_id"]
        out[qid] = {
            "question_ref": qid,
            "part_ref": None,
            "item_kind": "QUESTION",
            "source_question_digest": q["source_provenance"]["source_digest"],
        }
        for part in q["subparts"]:
            pref = part["part_id"]
            out[pref] = {
                "question_ref": qid,
                "part_ref": pref,
                "item_kind": "SUBPART",
                "source_question_digest": q["source_provenance"]["source_digest"],
            }
    return out

def source_key_for(question, part_ref):
    if part_ref is not None:
        return None
    key = question.get("answer_key")
    return key.get("source_assertion") if key else None

def validate_policy(policy):
    if policy["policy_digest"] != digest_without_field(policy, "policy_digest"):
        fail("DIAGNOSTIC_USE_POLICY_DIGEST_MISMATCH")
    states = [r["validity_state"] for r in policy["rules"]]
    if set(states) != VALIDITY_STATES or len(states) != len(set(states)):
        fail("DIAGNOSTIC_USE_POLICY_STATE_COVERAGE")
    return {r["validity_state"]: r for r in policy["rules"]}

def validate_registry(registry, question_set, rules):
    if registry["registry_digest"] != digest_without_field(registry, "registry_digest"):
        fail("ITEM_VALIDITY_REGISTRY_DIGEST_MISMATCH")
    if registry["question_set_ref"] != question_set["question_set_id"]:
        fail("ITEM_REVIEW_QUESTION_SET_MISMATCH")
    assert_no_learner_inference_payload(registry)

    expected = expected_item_bindings(question_set)
    reviews = registry["reviews"]
    refs = [r["item_ref"] for r in reviews]
    if len(refs) != len(set(refs)):
        fail("DUPLICATE_ITEM_REVIEW")
    missing = sorted(set(expected) - set(refs))
    extra = sorted(set(refs) - set(expected))
    if missing or extra:
        fail("ITEM_REVIEW_COVERAGE_GAP", f"missing={missing}, extra={extra}")

    by_q = {q["question_id"]: q for q in question_set["questions"]}
    for review in reviews:
        item_ref = review["item_ref"]
        bind = expected[item_ref]
        for field in ("question_ref", "part_ref", "item_kind", "source_question_digest"):
            if review[field] != bind[field]:
                fail("ITEM_REVIEW_SOURCE_DRIFT", f"{item_ref}:{field}")
        if review["review_policy_version"] != registry["review_policy_version"]:
            fail("ITEM_REVIEW_POLICY_VERSION_DRIFT", item_ref)

        q = by_q[review["question_ref"]]
        actual_source_key = source_key_for(q, review["part_ref"])
        if review["source_key_assertion"] != actual_source_key:
            fail("SOURCE_KEY_ASSERTION_DRIFT", item_ref)

        state = review["validity_state"]
        rule = rules[state]
        use = review["diagnostic_use"]
        if use not in rule["allowed_diagnostic_use"]:
            if state == "UNDERDETERMINED":
                fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", item_ref)
            if state == "REVIEW_REQUIRED":
                fail("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS", item_ref)
            fail("DIAGNOSTIC_USE_POLICY_VIOLATION", item_ref)

        ans = review["canonical_answer"]
        if state == "UNDERDETERMINED":
            if rule["negative_inference_allowed"] or rule["confident_diagnosis_allowed"]:
                fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", item_ref)
            if ans["uniqueness_status"] != "NON_UNIQUE" or not ans["answer_conditions"]:
                fail("UNDERDETERMINED_REVIEW_MISSING_NON_UNIQUENESS", item_ref)

        if state == "VALID_MULTIPLE_SOLUTIONS":
            solution_count = len(ans["accepted_answers"]) + len(ans["accepted_option_labels"])
            if ans["uniqueness_status"] != "MULTIPLE" or solution_count < 2:
                fail("MULTI_SOLUTION_ITEM_FORCED_TO_ONE_KEY", item_ref)

        if state == "REVIEW_REQUIRED":
            if use == "FULL" or rule["confident_diagnosis_allowed"]:
                fail("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS", item_ref)

        accepted_options = set(ans["accepted_option_labels"])
        if actual_source_key is not None and accepted_options:
            mismatch = actual_source_key not in accepted_options
            if mismatch and state != "KEY_ERROR":
                fail("SOURCE_KEY_OVERRIDES_CANONICAL_MATH", item_ref)
            if not mismatch and state == "KEY_ERROR":
                fail("KEY_ERROR_WITHOUT_SOURCE_KEY_MISMATCH", item_ref)

def build_review(question_set, registry, policy, review_bundle_id="MATH-ASSESSMENT-REVIEW"):
    validate_question_set(question_set)
    if question_set["subject"] != "MATHEMATICS":
        fail("ASSESSMENT_REVIEW_SUBJECT_MISMATCH")

    assert_no_learner_inference_payload(policy)
    rules = validate_policy(policy)
    validate_registry(registry, question_set, rules)

    reviewed = []
    for src in registry["reviews"]:
        item = copy.deepcopy(src)
        rule = rules[item["validity_state"]]
        key = item["source_key_assertion"]
        accepted = set(item["canonical_answer"]["accepted_option_labels"])
        if key is None:
            key_status = "ABSENT"
        elif not accepted:
            key_status = "NOT_APPLICABLE"
        elif key in accepted:
            key_status = "MATCH"
        else:
            key_status = "MISMATCH"
        item["source_key_status"] = key_status
        item["diagnostic_constraints"] = {
            "positive_inference_allowed": rule["positive_inference_allowed"],
            "negative_inference_allowed": rule["negative_inference_allowed"],
            "confident_diagnosis_allowed": rule["confident_diagnosis_allowed"],
        }
        reviewed.append(item)

    validity_counts = Counter(x["validity_state"] for x in reviewed)
    use_counts = Counter(x["diagnostic_use"] for x in reviewed)
    bundle = {
        "review_bundle_id": review_bundle_id,
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "question_set_ref": question_set["question_set_id"],
        "question_set_digest": question_set["question_set_digest"],
        "review_registry_ref": registry["registry_id"],
        "review_registry_digest": registry["registry_digest"],
        "diagnostic_use_policy_ref": policy["policy_id"],
        "diagnostic_use_policy_digest": policy["policy_digest"],
        "review_precedes_attempt_interpretation": True,
        "attempt_data_consumed": False,
        "item_reviews": reviewed,
        "summary": {
            "item_count": len(reviewed),
            "validity_counts": dict(sorted(validity_counts.items())),
            "diagnostic_use_counts": dict(sorted(use_counts.items())),
        },
        "bundle_digest": "",
    }
    bundle["bundle_digest"] = digest_without_field(bundle, "bundle_digest")
    return bundle

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--review-bundle-id", default="MATH-ASSESSMENT-REVIEW")
    args = ap.parse_args()
    result = build_review(load(args.questions), load(args.registry), load(args.policy), args.review_bundle_id)
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
