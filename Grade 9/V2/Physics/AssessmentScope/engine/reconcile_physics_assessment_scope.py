#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]
PHYSICS = D.parent
sys.path[:0] = [
    str(PHYSICS / "AssessmentIntake" / "engine"),
    str(PHYSICS / "AssessmentReview" / "engine"),
]
from build_physics_assessment_intake import validate_question_set, validate_topic_scope  # noqa: E402
from review_physics_assessment import build_review  # noqa: E402

MAPPING_STATES = {"MAPPED", "PARTIAL_SCOPE_MATCH", "OUTSIDE_DECLARED_SCOPE", "UNMAPPED"}
RESOLUTION_STATES = {"CLOSED", "PARTIAL", "BLOCKED"}
BAD_KEYS = {
    "attempt", "attempts", "attempt_set", "attempt_interpretation", "learner_state",
    "learner_diagnosis", "diagnosis", "misconception", "learner_evidence",
    "observed_answer", "hint_level", "support_state", "treatment",
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

def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

def assert_no_learner_payload(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in BAD_KEYS:
                fail("SCOPE_RESOLUTION_CONSUMES_LEARNER_DATA", f"{path}.{key}")
            assert_no_learner_payload(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            assert_no_learner_payload(child, f"{path}[{i}]")

def index(rows, key, code):
    out = {}
    for row in rows:
        value = row[key]
        if value in out:
            fail(code, value)
        out[value] = row
    return out

def topic_ids(scope):
    all_ids = set()
    sub_ids = set()
    for topic in scope["topics"]:
        all_ids.add(topic["topic_id"])
        for sub in topic["subtopics"]:
            all_ids.add(sub["subtopic_id"])
            sub_ids.add(sub["subtopic_id"])
    return all_ids, sub_ids

def expected_item_refs(question_set):
    out = {}
    for q in question_set["questions"]:
        qid = q["question_id"]
        out[qid] = {"question_ref": qid, "part_ref": None, "source_question_digest": q["source_provenance"]["source_digest"]}
        for part in q["subparts"]:
            pref = part["part_id"]
            out[pref] = {"question_ref": qid, "part_ref": pref, "source_question_digest": q["source_provenance"]["source_digest"]}
    return out

def canonical_registry_ids(canonical_caps):
    rows = canonical_caps["capabilities"]
    ids = [x["capability_id"] for x in rows]
    if len(ids) != len(set(ids)):
        fail("DUPLICATE_CANONICAL_CAPABILITY_ID")
    return set(ids)

def authority_maps(authority, canonical_caps):
    assert_no_learner_payload(authority)
    if authority["authority_digest"] != digest_without_field(authority, "authority_digest"):
        fail("PHYSICS_SCOPE_AUTHORITY_DIGEST_MISMATCH")
    if authority["subject"] != "PHYSICS" or authority["authority_class"] != "PHYSICS_ASSESSMENT_SCOPE_AUTHORITY":
        fail("PHYSICS_SCOPE_AUTHORITY_CLASS_MISMATCH")
    canonical_digest = digest(canonical_caps)
    if authority.get("canonical_capability_registry_digest") != canonical_digest:
        fail("CANONICAL_CAPABILITY_REGISTRY_DRIFT")
    required_boundary = {
        "LEARNER_STATE", "DIAGNOSIS", "PROBLEM_FAMILY_SEMANTICS",
        "REASONING_ROUTE_SEMANTICS", "DEMAND_DIFFICULTY", "TEACHING_CHOREOGRAPHY",
        "HINTS", "SOLUTIONS", "PUBLICATION_LAYOUT",
    }
    if not required_boundary <= set(authority["does_not_own"]):
        fail("PHYSICS_SCOPE_AUTHORITY_BOUNDARY_MISSING")
    concepts = index(authority["concepts"], "concept_id", "DUPLICATE_SCOPE_CONCEPT_ID")
    caps = index(authority["capabilities"], "capability_id", "DUPLICATE_SCOPE_CAPABILITY_ID")
    families = index(authority["problem_families"], "problem_family_id", "DUPLICATE_SCOPE_PROBLEM_FAMILY_ID")
    canonical_ids = canonical_registry_ids(canonical_caps)
    for cap in caps.values():
        if any(ref not in concepts for ref in cap["concept_refs"]):
            fail("UNKNOWN_SCOPE_CONCEPT_REF", cap["capability_id"])
        if any(ref not in caps for ref in cap["prerequisite_capability_refs"]):
            fail("UNKNOWN_PREREQUISITE_CAPABILITY_REF", cap["capability_id"])
        if any(ref not in canonical_ids for ref in cap["canonical_foundation_refs"]):
            fail("UNKNOWN_CANONICAL_FOUNDATION_REF", cap["capability_id"])
    seen = {}
    def visit(cap_id):
        if seen.get(cap_id) == 1:
            fail("PREREQUISITE_CYCLE", cap_id)
        if seen.get(cap_id) == 2:
            return
        seen[cap_id] = 1
        for parent in caps[cap_id]["prerequisite_capability_refs"]:
            visit(parent)
        seen[cap_id] = 2
    for cap_id in caps:
        visit(cap_id)
    if any(f["identity_status"] != "BOUND_IDENTITY" or f["semantic_owner_phase"] != "P-D" for f in families.values()):
        fail("PROBLEM_FAMILY_SEMANTICS_PREMATURELY_OWNED")
    return {
        "concepts": concepts,
        "capabilities": caps,
        "families": families,
        "models": set(authority["physical_model_identities"]),
        "laws": set(authority["law_identities"]),
        "representations": set(authority["representation_identities"]),
        "verification": set(authority["verification_obligation_identities"]),
        "roles": set(authority["reasoning_role_expectations"]),
        "states": set(authority["state_variable_identities"]),
    }

def prerequisite_closure(direct, caps):
    direct = set(direct)
    out = set()
    stack = [p for cap_id in direct for p in caps[cap_id]["prerequisite_capability_refs"]]
    while stack:
        cap_id = stack.pop()
        if cap_id in direct or cap_id in out:
            continue
        out.add(cap_id)
        stack.extend(caps[cap_id]["prerequisite_capability_refs"])
    return sorted(out)

def capability_scope_relation(direct, caps, declared):
    refs = {t for cap_id in direct for t in caps[cap_id]["declared_topic_refs"]}
    if not refs:
        return "CROSS_CUTTING"
    if refs & declared:
        return "WITHIN_DECLARED_SCOPE"
    return "OUTSIDE_DECLARED_SCOPE"

def source_representation_refs(question):
    return sorted(rep["representation_id"] for rep in question["figure_refs"])

def missing_source_representation_refs(question):
    return sorted(rep["representation_id"] for rep in question["figure_refs"] if rep["status"] == "MISSING_OR_TRUNCATED")

def validate_bindings(bindings, question_set, topic_scope, authority, maps, review_bundle):
    if bindings["binding_registry_digest"] != digest_without_field(bindings, "binding_registry_digest"):
        fail("QUESTION_SCOPE_BINDING_REGISTRY_DIGEST_MISMATCH")
    if (
        bindings["question_set_ref"] != question_set["question_set_id"]
        or bindings["declared_topic_scope_ref"] != topic_scope["declared_topic_scope_id"]
        or bindings["authority_ref"] != authority["authority_id"]
        or bindings["authority_digest"] != authority["authority_digest"]
    ):
        fail("QUESTION_SCOPE_BINDING_AUTHORITY_MISMATCH")
    assert_no_learner_payload(bindings)

    expected = expected_item_refs(question_set)
    review_by_item = {x["item_ref"]: x for x in review_bundle["item_reviews"]}
    rows = bindings["bindings"]
    refs = [x["item_ref"] for x in rows]
    if len(refs) != len(set(refs)):
        fail("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE", "duplicate item_ref")
    if set(refs) != set(review_by_item) or set(refs) != set(expected):
        fail("QUESTION_DROPPED_DURING_SCOPE_DERIVATION", f"missing={sorted(set(review_by_item)-set(refs))}, extra={sorted(set(refs)-set(review_by_item))}")

    declared, _ = topic_ids(topic_scope)
    q_by_id = {q["question_id"]: q for q in question_set["questions"]}
    caps = maps["capabilities"]
    for row in rows:
        item = row["item_ref"]
        expected_binding = expected[item]
        for key in ("question_ref", "part_ref", "source_question_digest"):
            if row[key] != expected_binding[key]:
                fail("QUESTION_SCOPE_BINDING_SOURCE_DRIFT", f"{item}:{key}")
        if row["mapping_state"] not in MAPPING_STATES or row["resolution_status"] not in RESOLUTION_STATES:
            fail("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE", item)

        validations = [
            (row["declared_topic_refs"], declared, "QUESTION_EVIDENCE_SILENTLY_EXPANDS_DECLARED_BOUNDARY"),
            (row["canonical_concept_refs"], set(maps["concepts"]), "UNKNOWN_SCOPE_CONCEPT_REF"),
            (row["canonical_capability_refs"], set(caps), "UNKNOWN_SCOPE_CAPABILITY_REF"),
            (row["prerequisite_capability_refs"], set(caps), "UNKNOWN_PREREQUISITE_CAPABILITY_REF"),
            (row["problem_family_refs"], set(maps["families"]), "UNKNOWN_SCOPE_PROBLEM_FAMILY_REF"),
            (row["physical_model_refs"], maps["models"], "UNKNOWN_PHYSICAL_MODEL_REF"),
            (row["law_refs"], maps["laws"], "UNKNOWN_LAW_REF"),
            (row["representation_demands"], maps["representations"], "UNKNOWN_REPRESENTATION_REF"),
            (row["verification_obligations"], maps["verification"], "UNKNOWN_VERIFICATION_OBLIGATION_REF"),
            (row["reasoning_role_expectations"], maps["roles"], "UNKNOWN_REASONING_ROLE_EXPECTATION"),
            (row["state_variable_refs"], maps["states"], "UNKNOWN_STATE_VARIABLE_REF"),
        ]
        for values, allowed, code in validations:
            if any(v not in allowed for v in values):
                fail(code, item)

        if row["mapping_state"] == "UNMAPPED":
            semantic_keys = [
                "canonical_concept_refs", "canonical_capability_refs", "prerequisite_capability_refs",
                "problem_family_refs", "physical_model_refs", "law_refs",
            ]
            if any(row[k] for k in semantic_keys):
                fail("UNMAPPED_QUESTION_HAS_INVENTED_SEMANTICS", item)
            continue

        if not row["canonical_concept_refs"] or not row["canonical_capability_refs"] or not row["problem_family_refs"]:
            fail("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE", f"{item}: incomplete semantic mapping")

        direct = row["canonical_capability_refs"]
        closure = prerequisite_closure(direct, caps)
        if closure != sorted(row["prerequisite_capability_refs"]):
            fail("PREREQUISITE_INFERRED_BUT_NOT_RECORDED", item)

        relation = capability_scope_relation(direct, caps, declared)
        if relation == "OUTSIDE_DECLARED_SCOPE" and row["mapping_state"] in {"MAPPED", "PARTIAL_SCOPE_MATCH"}:
            fail("TOPIC_LIST_SILENTLY_OVERRIDES_QUESTION_EVIDENCE", item)
        if row["mapping_state"] == "OUTSIDE_DECLARED_SCOPE" and relation != "OUTSIDE_DECLARED_SCOPE":
            fail("QUESTION_EVIDENCE_SILENTLY_EXPANDS_DECLARED_BOUNDARY", item)

        all_caps = [caps[x] for x in set(direct) | set(closure)]
        needs_frame = any(c["requires_reference_frame"] for c in all_caps)
        fr = row["reference_frame"]
        if fr["required"] != needs_frame:
            fail("REFERENCE_FRAME_REQUIRED_BUT_UNBOUND", f"{item}: required flag")
        if needs_frame and not fr["frame_text"]:
            if not (row["resolution_status"] == "BLOCKED" and "REFERENCE_FRAME" in row["unresolved_requirements"]):
                fail("REFERENCE_FRAME_REQUIRED_BUT_UNBOUND", item)

        needs_model_validity = any(c["requires_model_validity"] for c in all_caps)
        if needs_model_validity and not row["model_validity_conditions"]:
            fail("MODEL_VALIDITY_INFERRED_BUT_NOT_RECORDED", item)

        q = q_by_id[row["question_ref"]]
        actual_reps = source_representation_refs(q)
        if sorted(row["source_representation_refs"]) != actual_reps:
            fail("REPRESENTATION_DEPENDENCY_DROPPED", item)
        missing_reps = missing_source_representation_refs(q)
        if missing_reps:
            if row["resolution_status"] != "BLOCKED" or "REPRESENTATION" not in row["unresolved_requirements"]:
                fail("REPRESENTATION_DEPENDENCY_DROPPED", f"{item}: missing source representation not failed closed")

        multi_required = any(c["multi_phase_required"] for c in [caps[x] for x in direct])
        ph = row["phase_structure"]
        if multi_required and ph["kind"] != "MULTI_PHASE" and not ph["justification"].strip():
            fail("MULTIPHASE_ITEM_MAPPED_AS_SINGLE_PHASE_WITHOUT_JUSTIFICATION", item)
        if ph["kind"] == "MULTI_PHASE" and len(ph["phases"]) < 2:
            fail("MULTIPHASE_ITEM_MAPPED_AS_SINGLE_PHASE_WITHOUT_JUSTIFICATION", item)

        review = review_by_item[item]
        required_assumptions = review.get("required_model_assumptions", [])
        for assumption in required_assumptions:
            if assumption not in row["model_validity_conditions"]:
                fail("ASSUMPTION_SENSITIVE_ITEM_LOSES_ASSUMPTION", f"{item}:{assumption}")
    return rows

def finding(code, item_ref=None, topic_ref=None, capability_ref=None, detail="", severity="WARNING"):
    return {
        "code": code, "severity": severity, "item_ref": item_ref,
        "declared_topic_ref": topic_ref, "capability_ref": capability_ref, "detail": detail,
    }

def reconcile(question_set, topic_scope, review_registry, review_policy, canonical_caps, authority, bindings):
    validate_question_set(question_set)
    validate_topic_scope(topic_scope)
    if question_set["subject"] != "PHYSICS" or topic_scope["subject"] != "PHYSICS" or question_set["grade"] != topic_scope["grade"]:
        fail("ASSESSMENT_SCOPE_IDENTITY_MISMATCH")
    assert_no_learner_payload(canonical_caps)
    maps = authority_maps(authority, canonical_caps)
    review = build_review(question_set, review_registry, review_policy, "PHYSICS-ASSESSMENT-REVIEW-FOR-PC")
    if review["attempt_data_consumed"]:
        fail("SCOPE_RESOLUTION_CONSUMES_LEARNER_DATA", "review bundle consumed learner data")
    rows = validate_bindings(bindings, question_set, topic_scope, authority, maps, review)

    declared_all, declared_subs = topic_ids(topic_scope)
    caps = maps["capabilities"]
    review_by_item = {x["item_ref"]: x for x in review["item_reviews"]}
    q_by_id = {q["question_id"]: q for q in question_set["questions"]}

    findings = []
    used_declared_subtopics = set()
    undeclared_prereqs_by_item = {}

    for row in rows:
        item = row["item_ref"]
        mapping = row["mapping_state"]
        used_declared_subtopics |= set(row["declared_topic_refs"]) & declared_subs

        if mapping == "OUTSIDE_DECLARED_SCOPE":
            findings.append(finding("QUESTION_OUTSIDE_DECLARED_SCOPE", item_ref=item, detail="Question evidence is preserved but lies outside DeclaredTopicScope.", severity="BLOCKING"))
        elif mapping == "PARTIAL_SCOPE_MATCH":
            findings.append(finding("PARTIAL_SCOPE_MATCH", item_ref=item, detail="Only partial assessment-demand closure is justified by the reviewed source.", severity="WARNING"))
        elif mapping == "UNMAPPED":
            findings.append(finding("UNMAPPED_QUESTION", item_ref=item, detail="Repository authority is insufficient; semantics were not invented.", severity="BLOCKING"))

        undeclared = []
        for prereq in row["prerequisite_capability_refs"]:
            topic_refs = set(caps[prereq]["declared_topic_refs"])
            if not topic_refs:
                undeclared.append(prereq)
                findings.append(finding(
                    "QUESTION_REQUIRES_UNDECLARED_PREREQUISITE", item_ref=item, capability_ref=prereq,
                    detail="Cross-cutting Physics prerequisite is required but not explicitly named in DeclaredTopicScope.",
                    severity="INFO",
                ))
            elif not topic_refs & declared_all:
                undeclared.append(prereq)
                findings.append(finding(
                    "QUESTION_REQUIRES_UNDECLARED_PREREQUISITE", item_ref=item, capability_ref=prereq,
                    detail=f"Prerequisite {prereq} lies outside DeclaredTopicScope.",
                    severity="WARNING",
                ))
        undeclared_prereqs_by_item[item] = sorted(set(undeclared))

        if row["model_assumption_scope_status"] == "NOT_EXPLICITLY_DECLARED" and row["model_validity_conditions"]:
            findings.append(finding(
                "MODEL_ASSUMPTION_NOT_IN_DECLARED_SCOPE", item_ref=item,
                detail="Model-validity assumptions are required by canonical Physics but are not explicit topic labels in DeclaredTopicScope.",
                severity="INFO",
            ))

        if missing_source_representation_refs(q_by_id[row["question_ref"]]):
            findings.append(finding(
                "REPRESENTATION_DEPENDENCY_UNRESOLVED", item_ref=item,
                detail="A required source representation is missing/truncated; exact graph/figure demand remains blocked.",
                severity="BLOCKING",
            ))

    for topic_ref in sorted(declared_subs - used_declared_subtopics):
        findings.append(finding(
            "DECLARED_TOPIC_NOT_ASSESSED", topic_ref=topic_ref,
            detail="Declared subtopic is not directly assessed by any mapped source item.", severity="INFO",
        ))

    findings.sort(key=lambda x: (x["code"], x["item_ref"] or "", x["declared_topic_ref"] or "", x["capability_ref"] or ""))
    for i, f in enumerate(findings, 1):
        f["finding_id"] = f"PC-F{i:03d}"

    findings_by_item = {}
    for f in findings:
        if f["item_ref"]:
            findings_by_item.setdefault(f["item_ref"], []).append(f["finding_id"])

    coverage_rows = []
    prereq_rows = []
    for row in rows:
        item = row["item_ref"]
        review_item = review_by_item[item]
        coverage_rows.append({
            "item_ref": item,
            "question_ref": row["question_ref"],
            "part_ref": row["part_ref"],
            "source_question_digest": row["source_question_digest"],
            "source_integrity_state": review_item["source_integrity_state"],
            "validity_state": review_item["validity_state"],
            "diagnostic_use": review_item["diagnostic_use"],
            "mapping_state": row["mapping_state"],
            "resolution_status": row["resolution_status"],
            "declared_topic_refs": sorted(row["declared_topic_refs"]),
            "canonical_concept_refs": sorted(row["canonical_concept_refs"]),
            "canonical_capability_refs": sorted(row["canonical_capability_refs"]),
            "prerequisite_capability_refs": sorted(row["prerequisite_capability_refs"]),
            "system_refs": sorted(row["system_refs"]),
            "object_roles": sorted(row["object_roles"]),
            "reference_frame": row["reference_frame"],
            "sign_convention": row["sign_convention"],
            "state_variable_refs": sorted(row["state_variable_refs"]),
            "phase_structure": row["phase_structure"],
            "physical_model_refs": sorted(row["physical_model_refs"]),
            "law_refs": sorted(row["law_refs"]),
            "model_validity_conditions": row["model_validity_conditions"],
            "problem_family_refs": sorted(row["problem_family_refs"]),
            "representation_demands": sorted(row["representation_demands"]),
            "source_representation_refs": sorted(row["source_representation_refs"]),
            "verification_obligations": sorted(row["verification_obligations"]),
            "reasoning_role_expectations": row["reasoning_role_expectations"],
            "unresolved_requirements": sorted(row["unresolved_requirements"]),
            "finding_refs": sorted(findings_by_item.get(item, [])),
        })
        prereq_rows.append({
            "item_ref": item,
            "direct_capability_refs": sorted(row["canonical_capability_refs"]),
            "prerequisite_capability_refs": sorted(row["prerequisite_capability_refs"]),
            "undeclared_prerequisite_refs": undeclared_prereqs_by_item[item],
        })

    counts = dict(sorted(Counter(x["mapping_state"] for x in coverage_rows).items()))
    resolution_counts = dict(sorted(Counter(x["resolution_status"] for x in coverage_rows).items()))

    def union(field):
        return sorted({v for row in coverage_rows for v in row[field]})

    model = {
        "scope_model_id": "PHY-G9-MOTION-ASSESSMENT-SCOPE-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "question_set_ref": question_set["question_set_id"],
        "declared_topic_scope_ref": topic_scope["declared_topic_scope_id"],
        "authority_ref": authority["authority_id"],
        "assessment_review_bundle_ref": review["review_bundle_id"],
        "binding_registry_ref": bindings["binding_registry_id"],
        "attempt_data_consumed": False,
        "assessed_declared_topic_refs": union("declared_topic_refs"),
        "assessed_concept_refs": union("canonical_concept_refs"),
        "assessed_capability_refs": union("canonical_capability_refs"),
        "required_prerequisite_capability_refs": union("prerequisite_capability_refs"),
        "physical_model_refs": union("physical_model_refs"),
        "law_refs": union("law_refs"),
        "problem_family_refs": union("problem_family_refs"),
        "representation_demands": union("representation_demands"),
        "verification_obligations": union("verification_obligations"),
        "reasoning_role_expectations": union("reasoning_role_expectations"),
        "mapping_state_counts": counts,
        "resolution_status_counts": resolution_counts,
        "scope_model_digest": "",
    }
    model["scope_model_digest"] = digest_without_field(model, "scope_model_digest")

    coverage = {
        "coverage_matrix_id": "PHY-G9-MOTION-COVERAGE-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "question_set_ref": question_set["question_set_id"],
        "scope_model_ref": model["scope_model_id"],
        "rows": coverage_rows,
        "coverage_complete": len(coverage_rows) == len(review["item_reviews"]),
        "matrix_digest": "",
    }
    if not coverage["coverage_complete"]:
        fail("QUESTION_DROPPED_DURING_SCOPE_DERIVATION")
    coverage["matrix_digest"] = digest_without_field(coverage, "matrix_digest")

    prereq = {
        "prerequisite_closure_id": "PHY-G9-MOTION-PREREQUISITES-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "authority_ref": authority["authority_id"],
        "items": prereq_rows,
        "closure_digest": "",
    }
    prereq["closure_digest"] = digest_without_field(prereq, "closure_digest")

    report = {
        "reconciliation_id": "PHY-G9-MOTION-RECONCILIATION-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "question_set_ref": question_set["question_set_id"],
        "question_set_digest": question_set["question_set_digest"],
        "declared_topic_scope_ref": topic_scope["declared_topic_scope_id"],
        "declared_topic_scope_digest": topic_scope["scope_digest"],
        "assessment_review_bundle_digest": review["bundle_digest"],
        "authority_ref": authority["authority_id"],
        "authority_digest": authority["authority_digest"],
        "binding_registry_ref": bindings["binding_registry_id"],
        "binding_registry_digest": bindings["binding_registry_digest"],
        "attempt_data_consumed": False,
        "findings": findings,
        "summary": {
            "item_count": len(coverage_rows),
            "mapping_state_counts": counts,
            "resolution_status_counts": resolution_counts,
            "finding_code_counts": dict(sorted(Counter(x["code"] for x in findings).items())),
        },
        "report_digest": "",
    }
    report["report_digest"] = digest_without_field(report, "report_digest")
    return model, coverage, report, prereq

def main():
    ap = argparse.ArgumentParser()
    for name in [
        "questions", "topic-scope", "review-registry", "review-policy",
        "canonical-capabilities", "authority", "bindings",
        "scope-model-out", "coverage-out", "reconciliation-out", "prerequisite-out",
    ]:
        ap.add_argument("--" + name, required=True)
    args = ap.parse_args()
    outputs = reconcile(
        load(args.questions), load(args.topic_scope), load(args.review_registry),
        load(args.review_policy), load(args.canonical_capabilities),
        load(args.authority), load(args.bindings),
    )
    for path, value in zip(
        [args.scope_model_out, args.coverage_out, args.reconciliation_out, args.prerequisite_out],
        outputs,
    ):
        write(path, value)

if __name__ == "__main__":
    main()
