#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
sys.path.insert(0, str(CHEM / "AssessmentIntake" / "engine"))
from build_chemistry_assessment_intake import verify_source_set, verify_questions  # noqa: E402

INTEGRITY_STATES = {
    "CLEAN","SOURCE_INTERNAL_TYPO","TYPOGRAPHIC_OR_OCR_AMBIGUITY","FORMULA_OR_CHARGE_AMBIGUITY",
    "EQUATION_OR_COEFFICIENT_ISSUE","TRUNCATED_OR_MISSING_STRUCTURE_OR_FIGURE","REVIEW_REQUIRED",
}
VALIDITY_STATES = {
    "VALID","VALID_CONDITION_SENSITIVE","VALID_MULTIPLE_INTERPRETATIONS","UNDERDETERMINED",
    "CHEMICAL_DOMAIN_ISSUE","KEY_ERROR","DATA_ERROR","REVIEW_REQUIRED",
}
FORBIDDEN_LEARNER_KEYS = {
    "attempt","attempt_set","attempt_interpretation","learner_state","learner_diagnosis",
    "diagnosis","misconception","learner_evidence","observed_answer","learner_error",
}

def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def digest_without_field(value, field):
    clone = copy.deepcopy(value)
    clone.pop(field, None)
    return digest(clone)

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)

def load_registry(path):
    path = Path(path)
    manifest = load(path)
    if manifest["registry_digest"] != digest_without_field(manifest, "registry_digest"):
        fail("ITEM_VALIDITY_REGISTRY_MANIFEST_DIGEST_MISMATCH")
    source_reviews = []
    question_reviews = []
    for field, target in (("source_review_shards", source_reviews), ("question_review_shards", question_reviews)):
        for ref in manifest[field]:
            shard_path = path.parent / ref["path"]
            shard = load(shard_path)
            if shard["shard_digest"] != digest_without_field(shard, "shard_digest"):
                fail("ITEM_VALIDITY_REVIEW_SHARD_DIGEST_MISMATCH", ref["path"])
            if shard["shard_digest"] != ref["shard_digest"]:
                fail("ITEM_VALIDITY_REVIEW_SHARD_REF_MISMATCH", ref["path"])
            if len(shard["reviews"]) != ref["record_count"]:
                fail("ITEM_VALIDITY_REVIEW_SHARD_COUNT_MISMATCH", ref["path"])
            target.extend(shard["reviews"])
    expanded = {k: manifest[k] for k in (
        "registry_id","schema_version","subject","source_set_ref","question_set_ref",
        "review_policy_version","qc_registry_ref"
    )}
    expanded["source_reviews"] = source_reviews
    expanded["question_reviews"] = question_reviews
    expanded["registry_digest"] = manifest["expanded_registry_digest"]
    if expanded["registry_digest"] != digest_without_field(expanded, "registry_digest"):
        fail("ITEM_VALIDITY_EXPANDED_REGISTRY_DIGEST_MISMATCH")
    return expanded, manifest["registry_digest"]

def assert_no_learner_inference_payload(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_LEARNER_KEYS:
                fail("ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS", f"{path}.{key}")
            assert_no_learner_inference_payload(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            assert_no_learner_inference_payload(child, f"{path}[{i}]")

def validate_policy(policy):
    if policy["policy_digest"] != digest_without_field(policy, "policy_digest"):
        fail("DIAGNOSTIC_USE_POLICY_DIGEST_MISMATCH")
    vr = policy["validity_rules"]
    ir = policy["integrity_rules"]
    vstates = [r["validity_state"] for r in vr]
    istates = [r["source_integrity_state"] for r in ir]
    if set(vstates) != VALIDITY_STATES or len(vstates) != len(set(vstates)):
        fail("DIAGNOSTIC_USE_POLICY_VALIDITY_COVERAGE")
    if set(istates) != INTEGRITY_STATES or len(istates) != len(set(istates)):
        fail("DIAGNOSTIC_USE_POLICY_INTEGRITY_COVERAGE")
    return ({r["validity_state"]: r for r in vr},
            {r["source_integrity_state"]: r for r in ir})

def validate_qc_registry(qc):
    if qc["registry_digest"] != digest_without_field(qc, "registry_digest"):
        fail("QC_REGISTRY_DIGEST_MISMATCH")
    events = {}
    for e in qc["events"]:
        if e["event_id"] in events:
            fail("DUPLICATE_QC_EVENT", e["event_id"])
        if e["event_digest"] != digest_without_field(e, "event_digest"):
            fail("QC_EVENT_DIGEST_MISMATCH", e["event_id"])
        if e["scope_changed"] is not False:
            fail("QC_REPAIR_SILENTLY_EXPANDS_SCOPE", e["event_id"])
        events[e["event_id"]] = e
    return events

def expected_source_bindings(source_set):
    return {
        u["source_unit_id"]: {
            "source_unit_ref": u["source_unit_id"],
            "source_digest": u["source_provenance"]["source_digest"],
            "source_asserted_text": u["statement"],
        }
        for u in source_set["units"]
    }

def expected_question_bindings(question_set):
    out = {}
    for q in question_set["questions"]:
        qid = q["question_id"]
        out[qid] = {
            "item_ref": qid, "question_ref": qid, "part_ref": None, "item_kind": "QUESTION",
            "source_question_digest": q["source_provenance"]["source_digest"],
            "source_asserted_text": q["stem"],
        }
        for p in q["subparts"]:
            item_ref = f"{qid}.{p['part_id']}"
            out[item_ref] = {
                "item_ref": item_ref, "question_ref": qid, "part_ref": p["part_id"], "item_kind": "SUBPART",
                "source_question_digest": q["source_provenance"]["source_digest"],
                "source_asserted_text": p["stem"],
            }
    return out

def source_key_for(question, part_ref):
    if part_ref is not None:
        return None
    key = question.get("answer_key")
    if key is None:
        return None
    if isinstance(key, str):
        return key
    if isinstance(key, dict):
        return key.get("source_assertion")
    fail("SOURCE_KEY_SHAPE_UNSUPPORTED", question["question_id"])

def qc_event_for(review, events):
    ref = review["qc_event_ref"]
    if ref is None:
        return None
    if ref not in events:
        fail("QC_EVENT_MISSING", ref)
    event = events[ref]
    target = review.get("source_unit_ref", review.get("item_ref"))
    if event["target_ref"] != target:
        fail("QC_EVENT_TARGET_MISMATCH", target)
    return event

def validate_common_review(review, validity_rules, integrity_rules, events):
    state = review["validity_state"]
    integrity = review["source_integrity_state"]
    use = review["diagnostic_use"]
    vrule = validity_rules[state]
    irule = integrity_rules[integrity]

    if use not in vrule["allowed_diagnostic_use"] or use not in irule["allowed_diagnostic_use"]:
        if state == "UNDERDETERMINED":
            fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", review["review_id"])
        if state == "CHEMICAL_DOMAIN_ISSUE":
            fail("DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR", review["review_id"])
        if state == "REVIEW_REQUIRED" or integrity == "REVIEW_REQUIRED":
            fail("REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS", review["review_id"])
        if integrity == "FORMULA_OR_CHARGE_AMBIGUITY":
            fail("IONIC_CHARGE_AMBIGUITY_USED_AS_CONFIDENT_EVIDENCE", review["review_id"])
        fail("DIAGNOSTIC_USE_POLICY_VIOLATION", review["review_id"])

    if state == "UNDERDETERMINED":
        ans = review.get("canonical_answer")
        if ans is not None:
            if ans["uniqueness_status"] != "NON_UNIQUE" or not ans["answer_conditions"]:
                fail("UNDERDETERMINED_REVIEW_MISSING_NON_UNIQUENESS", review["review_id"])
        if vrule["negative_inference_allowed"] or vrule["confident_diagnosis_allowed"]:
            fail("UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS", review["review_id"])

    if state == "VALID_MULTIPLE_INTERPRETATIONS":
        interpretations = review["canonical_interpretations"]
        if len(interpretations) < 2:
            fail("MULTIPLE_INTERPRETATIONS_FORCED_TO_ONE", review["review_id"])

    if state == "VALID_CONDITION_SENSITIVE" and not review["required_conditions"]:
        fail("CONDITION_SENSITIVE_ITEM_LOSES_CONDITION", review["review_id"])

    if review["replacement_representation_invented"]:
        if integrity == "TRUNCATED_OR_MISSING_STRUCTURE_OR_FIGURE" or review["missing_or_damaged_representation"]:
            fail("MISSING_STRUCTURE_SILENTLY_INVENTED", review["review_id"])
        fail("REPRESENTATION_INVENTED_DURING_REVIEW", review["review_id"])

    if irule["requires_rendered_source_inspection"] and review["rendered_source_inspection"] != "CONFIRMED":
        if use != "EXCLUDE_FROM_NEGATIVE_INFERENCE":
            if integrity == "FORMULA_OR_CHARGE_AMBIGUITY":
                fail("IONIC_CHARGE_AMBIGUITY_USED_AS_CONFIDENT_EVIDENCE", review["review_id"])
            fail("OCR_FORMULA_AMBIGUITY_SILENTLY_NORMALIZED", review["review_id"])

    event = qc_event_for(review, events)
    return vrule, irule, event

def validate_registry(registry, source_set, question_set, validity_rules, integrity_rules, events):
    if registry["registry_digest"] != digest_without_field(registry, "registry_digest"):
        fail("ITEM_VALIDITY_REGISTRY_DIGEST_MISMATCH")
    if registry["source_set_ref"] != source_set["source_set_id"]:
        fail("SOURCE_REVIEW_SET_MISMATCH")
    if registry["question_set_ref"] != question_set["question_set_id"]:
        fail("ITEM_REVIEW_QUESTION_SET_MISMATCH")
    assert_no_learner_inference_payload(registry)

    expected_sources = expected_source_bindings(source_set)
    srefs = [r["source_unit_ref"] for r in registry["source_reviews"]]
    if len(srefs) != len(set(srefs)):
        fail("DUPLICATE_SOURCE_REVIEW")
    missing = sorted(set(expected_sources)-set(srefs))
    extra = sorted(set(srefs)-set(expected_sources))
    if missing or extra:
        fail("SOURCE_REVIEW_COVERAGE_GAP", f"missing={missing}, extra={extra}")

    by_source = {u["source_unit_id"]:u for u in source_set["units"]}
    for review in registry["source_reviews"]:
        ref = review["source_unit_ref"]
        bind = expected_sources[ref]
        for field in ("source_digest","source_asserted_text"):
            if review[field] != bind[field]:
                fail("SOURCE_REVIEW_SOURCE_DRIFT", f"{ref}:{field}")
        if review["review_policy_version"] != registry["review_policy_version"]:
            fail("ITEM_REVIEW_POLICY_VERSION_DRIFT", ref)
        _, irule, event = validate_common_review(review, validity_rules, integrity_rules, events)
        if review["learner_use_statement"] != review["source_asserted_text"]:
            if event is None:
                if review["source_integrity_state"] == "SOURCE_INTERNAL_TYPO":
                    fail("SOURCE_TYPO_SILENTLY_CORRECTED", ref)
                fail("OCR_FORMULA_AMBIGUITY_SILENTLY_NORMALIZED", ref)
            if event["source_before"] != review["source_asserted_text"] or event["learner_use_after"] != review["learner_use_statement"]:
                fail("QC_EVENT_CONTENT_MISMATCH", ref)
        if irule["requires_qc_event_for_learner_use"] and review["learner_use_statement"] != review["source_asserted_text"] and event is None:
            fail("SOURCE_TYPO_SILENTLY_CORRECTED", ref)
        if review["validity_state"] == "VALID_CONDITION_SENSITIVE":
            source_conditions = by_source[ref]["representation"]["conditions"]
            if source_conditions and not set(source_conditions).issubset(set(review["required_conditions"])):
                fail("CONDITION_SENSITIVE_ITEM_LOSES_CONDITION", ref)

    expected_questions = expected_question_bindings(question_set)
    qrefs = [r["item_ref"] for r in registry["question_reviews"]]
    if len(qrefs) != len(set(qrefs)):
        fail("DUPLICATE_ITEM_REVIEW")
    missing = sorted(set(expected_questions)-set(qrefs))
    extra = sorted(set(qrefs)-set(expected_questions))
    if missing or extra:
        fail("ITEM_REVIEW_COVERAGE_GAP", f"missing={missing}, extra={extra}")

    by_q = {q["question_id"]:q for q in question_set["questions"]}
    for review in registry["question_reviews"]:
        ref = review["item_ref"]
        bind = expected_questions[ref]
        for field in ("question_ref","part_ref","item_kind","source_question_digest","source_asserted_text"):
            if review[field] != bind[field]:
                fail("ITEM_REVIEW_SOURCE_DRIFT", f"{ref}:{field}")
        if review["review_policy_version"] != registry["review_policy_version"]:
            fail("ITEM_REVIEW_POLICY_VERSION_DRIFT", ref)

        q = by_q[review["question_ref"]]
        actual_key = source_key_for(q, review["part_ref"])
        if review["source_asserted_answer"] != actual_key:
            fail("SOURCE_KEY_ASSERTION_DRIFT", ref)

        vrule, _, _ = validate_common_review(review, validity_rules, integrity_rules, events)

        if review["validity_state"] == "VALID_CONDITION_SENSITIVE":
            source_conditions = q["representation"]["conditions"]
            if source_conditions and not set(source_conditions).issubset(set(review["required_conditions"])):
                fail("CONDITION_SENSITIVE_ITEM_LOSES_CONDITION", ref)

        accepted = set(review["canonical_answer"]["accepted_option_ids"])
        if actual_key is not None and accepted:
            mismatch = actual_key not in accepted
            if mismatch and review["validity_state"] != "KEY_ERROR":
                fail("SOURCE_KEY_OVERRIDES_CANONICAL_CHEMISTRY", ref)
            if not mismatch and review["validity_state"] == "KEY_ERROR":
                fail("KEY_ERROR_WITHOUT_SOURCE_KEY_MISMATCH", ref)

        if review["validity_state"] == "CHEMICAL_DOMAIN_ISSUE":
            if review["diagnostic_use"] != "EXCLUDE_FROM_NEGATIVE_INFERENCE" or vrule["negative_inference_allowed"]:
                fail("DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR", ref)

def build_review(source_set, question_set, registry, policy, qc_registry, review_bundle_id="CHEM-ASSESSMENT-REVIEW", registry_manifest_digest=None):
    verify_source_set(source_set)
    verify_questions(question_set)
    if source_set["subject"] != "CHEMISTRY" or question_set["subject"] != "CHEMISTRY":
        fail("ASSESSMENT_REVIEW_SUBJECT_MISMATCH")
    assert_no_learner_inference_payload(policy)
    assert_no_learner_inference_payload(qc_registry)
    validity_rules, integrity_rules = validate_policy(policy)
    events = validate_qc_registry(qc_registry)
    if registry["qc_registry_ref"] != qc_registry["qc_registry_id"]:
        fail("QC_REGISTRY_REF_MISMATCH")
    validate_registry(registry, source_set, question_set, validity_rules, integrity_rules, events)

    src_out = copy.deepcopy(registry["source_reviews"])
    q_out = []
    by_q = {q["question_id"]:q for q in question_set["questions"]}
    for review in registry["question_reviews"]:
        item = copy.deepcopy(review)
        rule = validity_rules[item["validity_state"]]
        irule = integrity_rules[item["source_integrity_state"]]
        actual_key = source_key_for(by_q[item["question_ref"]], item["part_ref"])
        accepted = set(item["canonical_answer"]["accepted_option_ids"])
        if actual_key is None:
            key_status = "ABSENT"
        elif not accepted:
            key_status = "NOT_APPLICABLE"
        elif actual_key in accepted:
            key_status = "MATCH"
        else:
            key_status = "MISMATCH"
        item["source_key_status"] = key_status
        item["diagnostic_constraints"] = {
            "positive_inference_allowed": rule["positive_inference_allowed"],
            "negative_inference_allowed": rule["negative_inference_allowed"],
            "confident_diagnosis_allowed": rule["confident_diagnosis_allowed"],
            "integrity_requires_qc_event": irule["requires_qc_event_for_learner_use"],
            "integrity_requires_rendered_source_inspection": irule["requires_rendered_source_inspection"],
        }
        q_out.append(item)

    src_integrity_counts=Counter(x["source_integrity_state"] for x in src_out)
    q_validity_counts=Counter(x["validity_state"] for x in q_out)
    use_counts=Counter(x["diagnostic_use"] for x in q_out)
    blocking=sorted(
        [f"SOURCE:{x['source_unit_ref']}" for x in src_out if x["source_integrity_state"]=="REVIEW_REQUIRED"]
        + [f"QUESTION:{x['item_ref']}" for x in q_out if x["validity_state"]=="REVIEW_REQUIRED" or x["source_integrity_state"]=="REVIEW_REQUIRED"]
    )

    bundle={
        "review_bundle_id":review_bundle_id,"schema_version":"1.0.0","subject":"CHEMISTRY",
        "source_set_ref":source_set["source_set_id"],"source_set_digest":source_set["source_set_digest"],
        "question_set_ref":question_set["question_set_id"],"question_set_digest":question_set["question_set_digest"],
        "review_registry_ref":registry["registry_id"],"review_registry_digest":registry["registry_digest"],
        "review_registry_manifest_digest":registry_manifest_digest or registry["registry_digest"],
        "diagnostic_use_policy_ref":policy["policy_id"],"diagnostic_use_policy_digest":policy["policy_digest"],
        "qc_registry_ref":qc_registry["qc_registry_id"],"qc_registry_digest":qc_registry["registry_digest"],
        "review_precedes_attempt_interpretation":True,"attempt_data_consumed":False,
        "source_reviews":src_out,"question_reviews":q_out,
        "summary":{
            "source_unit_count":len(src_out),"question_item_count":len(q_out),
            "source_integrity_counts":dict(sorted(src_integrity_counts.items())),
            "question_validity_counts":dict(sorted(q_validity_counts.items())),
            "diagnostic_use_counts":dict(sorted(use_counts.items())),
            "blocking_review_refs":blocking,
        },
        "bundle_digest":"",
    }
    bundle["bundle_digest"]=digest_without_field(bundle,"bundle_digest")
    return bundle

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sources",required=True)
    ap.add_argument("--questions",required=True)
    ap.add_argument("--registry",required=True)
    ap.add_argument("--policy",required=True)
    ap.add_argument("--qc-events",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--review-bundle-id",default="CHEM-ASSESSMENT-REVIEW")
    a=ap.parse_args()
    registry, manifest_digest = load_registry(a.registry)
    result=build_review(load(a.sources),load(a.questions),registry,load(a.policy),load(a.qc_events),a.review_bundle_id,manifest_digest)
    Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
