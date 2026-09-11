#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]
PHYSICS = D.parent
sys.path.insert(0, str(PHYSICS / "AssessmentIntake" / "engine"))
from build_physics_assessment_intake import validate_question_set  # noqa: E402

VALIDITY_STATES = {
    "CLEAN", "VALID_ASSUMPTION_SENSITIVE",
    "VALID_MULTIPLE_MODELS_OR_INTERPRETATIONS", "UNDERDETERMINED",
    "MATHEMATICAL_OR_DOMAIN_ISSUE", "KEY_ERROR", "DATA_ERROR",
    "TRUNCATED_OR_MISSING_FIGURE", "REVIEW_REQUIRED",
}
SOURCE_INTEGRITY_STATES = {
    "CLEAN", "TYPOGRAPHIC_OR_OCR_AMBIGUITY", "DATA_ERROR",
    "TRUNCATED_OR_MISSING_FIGURE", "REVIEW_REQUIRED",
}
FORBIDDEN_LEARNER_KEYS = {
    "attempt", "attempt_set", "attempt_interpretation", "learner_state",
    "learner_diagnosis", "diagnosis", "misconception", "learner_evidence",
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
            "question_ref": qid, "part_ref": None, "item_kind": "QUESTION",
            "source_question_digest": q["source_provenance"]["source_digest"],
        }
        for part in q["subparts"]:
            pref = part["part_id"]
            out[pref] = {
                "question_ref": qid, "part_ref": pref, "item_kind": "SUBPART",
                "source_question_digest": q["source_provenance"]["source_digest"],
            }
    return out

def source_asserted_answer(question, part_ref):
    if part_ref is not None:
        return None
    key = question.get("answer_key")
    return key.get("source_assertion") if key else None

def representation_bindings(question):
    return [
        {
            "representation_ref": rep["representation_id"],
            "representation_digest": rep["representation_digest"],
            "status": rep["status"],
            "kind": rep["kind"],
        }
        for rep in question["figure_refs"]
    ]

def expand_review(decision, registry, binding, question):
    source_review = {
        "rendered_source_inspected": False,
        "ambiguity_resolution_state": "NOT_APPLICABLE",
        "ambiguity_details": [],
        "missing_or_damaged_representation": any(
            r["status"] == "MISSING_OR_TRUNCATED" for r in question["figure_refs"]
        ),
        "reconstruction_performed": False,
        "representation_bindings": representation_bindings(question),
    }
    source_review.update(decision.get("source_integrity_override", {}))
    return {
        "review_id": decision["review_id"],
        "item_ref": decision["item_ref"],
        "question_ref": binding["question_ref"],
        "part_ref": binding["part_ref"],
        "item_kind": binding["item_kind"],
        "source_question_digest": decision["source_question_digest"],
        "source_integrity_state": decision["source_integrity_state"],
        "validity_state": decision["validity_state"],
        "source_asserted_answer": source_asserted_answer(question, binding["part_ref"]),
        "canonical_answer": copy.deepcopy(decision["canonical_answer"]),
        "required_model_assumptions": copy.deepcopy(decision.get("required_model_assumptions", [])),
        "frame_sign_assumptions": copy.deepcopy(decision.get("frame_sign_assumptions", [])),
        "source_integrity_review": source_review,
        "review_rationale": decision["review_rationale"],
        "canonical_physics_refs": copy.deepcopy(decision["canonical_physics_refs"]),
        "diagnostic_use": decision["diagnostic_use"],
        "confidence": decision["confidence"],
        "review_policy_version": registry["review_policy_version"],
        "review_provenance": copy.deepcopy(registry["review_provenance"]),
    }

def validate_policy(policy):
    if policy["policy_digest"] != digest_without_field(policy, "policy_digest"):
        fail("DIAGNOSTIC_USE_POLICY_DIGEST_MISMATCH")
    validity = [r["validity_state"] for r in policy["validity_rules"]]
    if set(validity) != VALIDITY_STATES or len(validity) != len(set(validity)):
        fail("DIAGNOSTIC_USE_POLICY_STATE_COVERAGE")
    source = [r["source_integrity_state"] for r in policy["source_integrity_rules"]]
    if set(source) != SOURCE_INTEGRITY_STATES or len(source) != len(set(source)):
        fail("SOURCE_INTEGRITY_POLICY_STATE_COVERAGE")
    return (
        {r["validity_state"]: r for r in policy["validity_rules"]},
        {r["source_integrity_state"]: r for r in policy["source_integrity_rules"]},
    )

def validate_item(review, question, validity_rules, source_rules):
    item_ref = review["item_ref"]
    source_evidence = review["source_integrity_review"]
    expected_reps = representation_bindings(question)
    if source_evidence["representation_bindings"] != expected_reps:
        if any(x["status"] == "MISSING_OR_TRUNCATED" for x in expected_reps):
            fail("MISSING_FIGURE_SILENTLY_INVENTED", item_ref)
        fail("ITEM_REVIEW_REPRESENTATION_DRIFT", item_ref)

    actual_missing = any(x["status"] == "MISSING_OR_TRUNCATED" for x in expected_reps)
    if source_evidence["missing_or_damaged_representation"] != actual_missing:
        fail("MISSING_FIGURE_SILENTLY_INVENTED", item_ref)
    if actual_missing and review["source_integrity_state"] != "TRUNCATED_OR_MISSING_FIGURE":
        fail("MISSING_FIGURE_SILENTLY_INVENTED", item_ref)
    if actual_missing and source_evidence["reconstruction_performed"]:
        fail("MISSING_FIGURE_SILENTLY_INVENTED", item_ref)

    source_state = review["source_integrity_state"]
    source_rule = source_rules[source_state]
    ambiguity_state = source_evidence["ambiguity_resolution_state"]

    if source_state == "TYPOGRAPHIC_OR_OCR_AMBIGUITY":
        if source_evidence["rendered_source_inspected"]:
            if ambiguity_state not in {"RESOLVED", "UNRESOLVED"}:
                fail("OCR_AMBIGUITY_SILENTLY_CORRECTED", item_ref)
        elif ambiguity_state != "UNRESOLVED":
            fail("OCR_AMBIGUITY_SILENTLY_CORRECTED", item_ref)
        if source_evidence["reconstruction_performed"]:
            fail("OCR_AMBIGUITY_SILENTLY_CORRECTED", item_ref)
        if ambiguity_state == "UNRESOLVED" and review["diagnostic_use"] not in source_rule["unresolved_allowed_diagnostic_use"]:
            fail("OCR_AMBIGUITY_SILENTLY_CORRECTED", item_ref)

    if source_state in {"DATA_ERROR", "TRUNCATED_OR_MISSING_FIGURE", "REVIEW_REQUIRED"}:
        if review["diagnostic_use"] not in source_rule["unresolved_allowed_diagnostic_use"]:
            fail("SOURCE_INTEGRITY_DIAGNOSTIC_POLICY_VIOLATION", item_ref)
    if source_evidence["reconstruction_performed"] and not source_rule["synthetic_reconstruction_allowed"]:
        if source_state == "TRUNCATED_OR_MISSING_FIGURE":
            fail("MISSING_FIGURE_SILENTLY_INVENTED", item_ref)
        fail("SOURCE_RECONSTRUCTION_NOT_ALLOWED", item_ref)

    state = review["validity_state"]
    rule = validity_rules[state]
    use = review["diagnostic_use"]
    if use not in rule["allowed_diagnostic_use"]:
        if state == "UNDERDETERMINED":
            fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", item_ref)
        if state == "MATHEMATICAL_OR_DOMAIN_ISSUE":
            fail("DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR", item_ref)
        if state == "REVIEW_REQUIRED":
            fail("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS", item_ref)
        fail("DIAGNOSTIC_USE_POLICY_VIOLATION", item_ref)

    ans = review["canonical_answer"]
    if state == "VALID_ASSUMPTION_SENSITIVE" and not review["required_model_assumptions"]:
        fail("ASSUMPTION_SENSITIVE_ITEM_LOSES_ASSUMPTION", item_ref)

    if state == "VALID_MULTIPLE_MODELS_OR_INTERPRETATIONS":
        routes = len(ans["accepted_answers"]) + len(ans["accepted_option_labels"]) + len(ans["answer_conditions"])
        if routes < 2 or rule["negative_inference_allowed"] or rule["confident_diagnosis_allowed"]:
            fail("MULTIPLE_MODELS_FORCED_TO_ONE_INTERPRETATION", item_ref)

    if state == "UNDERDETERMINED":
        if rule["negative_inference_allowed"] or rule["confident_diagnosis_allowed"]:
            fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", item_ref)
        if ans["uniqueness_status"] not in {"NON_UNIQUE", "UNRESOLVED"} or not ans["answer_conditions"]:
            fail("UNDERDETERMINED_REVIEW_MISSING_NON_UNIQUENESS", item_ref)

    if state == "MATHEMATICAL_OR_DOMAIN_ISSUE":
        if rule["negative_inference_allowed"] or rule["confident_diagnosis_allowed"]:
            fail("DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR", item_ref)

    if state == "TRUNCATED_OR_MISSING_FIGURE":
        if use != "EXCLUDE_FROM_NEGATIVE_INFERENCE" or rule["negative_inference_allowed"]:
            fail("MISSING_FIGURE_SILENTLY_INVENTED", item_ref)

    if state == "REVIEW_REQUIRED":
        if use == "FULL" or rule["confident_diagnosis_allowed"]:
            fail("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS", item_ref)

    source_key = review["source_asserted_answer"]
    accepted_options = set(ans["accepted_option_labels"])
    if source_key is not None and accepted_options:
        mismatch = source_key not in accepted_options
        if mismatch and state != "KEY_ERROR":
            fail("SOURCE_KEY_OVERRIDES_CANONICAL_PHYSICS", item_ref)
        if not mismatch and state == "KEY_ERROR":
            fail("KEY_ERROR_WITHOUT_SOURCE_KEY_MISMATCH", item_ref)

def validate_registry(registry, question_set, validity_rules, source_rules):
    if registry["registry_digest"] != digest_without_field(registry, "registry_digest"):
        fail("ITEM_VALIDITY_REGISTRY_DIGEST_MISMATCH")
    if registry["question_set_ref"] != question_set["question_set_id"]:
        fail("ITEM_REVIEW_QUESTION_SET_MISMATCH")
    assert_no_learner_inference_payload(registry)

    expected = expected_item_bindings(question_set)
    decisions = registry["reviews"]
    refs = [r["item_ref"] for r in decisions]
    if len(refs) != len(set(refs)):
        fail("DUPLICATE_ITEM_REVIEW")
    missing = sorted(set(expected) - set(refs))
    extra = sorted(set(refs) - set(expected))
    if missing or extra:
        fail("ITEM_REVIEW_COVERAGE_GAP", f"missing={missing}, extra={extra}")

    by_q = {q["question_id"]: q for q in question_set["questions"]}
    expanded = []
    for decision in decisions:
        item_ref = decision["item_ref"]
        binding = expected[item_ref]
        if decision["source_question_digest"] != binding["source_question_digest"]:
            fail("ITEM_REVIEW_SOURCE_DRIFT", f"{item_ref}:source_question_digest")
        q = by_q[binding["question_ref"]]
        review = expand_review(decision, registry, binding, q)
        validate_item(review, q, validity_rules, source_rules)
        expanded.append(review)
    return expanded

def build_review(question_set, registry, policy, review_bundle_id="PHYSICS-ASSESSMENT-REVIEW"):
    validate_question_set(question_set)
    if question_set["subject"] != "PHYSICS":
        fail("ASSESSMENT_REVIEW_SUBJECT_MISMATCH")

    assert_no_learner_inference_payload(policy)
    validity_rules, source_rules = validate_policy(policy)
    reviewed = validate_registry(registry, question_set, validity_rules, source_rules)

    for item in reviewed:
        rule = validity_rules[item["validity_state"]]
        source_rule = source_rules[item["source_integrity_state"]]
        key = item["source_asserted_answer"]
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
        item["source_integrity_constraints"] = {
            "requires_rendered_source_inspection_or_unresolved": source_rule["requires_rendered_source_inspection_or_unresolved"],
            "synthetic_reconstruction_allowed": source_rule["synthetic_reconstruction_allowed"],
        }

    source_counts = Counter(x["source_integrity_state"] for x in reviewed)
    validity_counts = Counter(x["validity_state"] for x in reviewed)
    use_counts = Counter(x["diagnostic_use"] for x in reviewed)
    bundle = {
        "review_bundle_id": review_bundle_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
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
            "source_integrity_counts": dict(sorted(source_counts.items())),
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
    ap.add_argument("--review-bundle-id", default="PHYSICS-ASSESSMENT-REVIEW")
    args = ap.parse_args()
    result = build_review(load(args.questions), load(args.registry), load(args.policy), args.review_bundle_id)
    Path(args.out).write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

if __name__ == "__main__":
    main()
