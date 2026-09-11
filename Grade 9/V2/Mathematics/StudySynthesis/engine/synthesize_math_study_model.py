#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

DIMENSIONS = [
    "acquisition", "independent_reconstruction", "delayed_retention", "near_transfer",
    "far_transfer", "mixed_discrimination", "fluency", "timed_performance",
]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value, omit=None):
    if isinstance(value, dict) and omit:
        value = {k: v for k, v in value.items() if k != omit}
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def capability_map(authority):
    return {x["capability_id"]: x for x in authority["capabilities"]}


def transitive_prereqs(capability_ref, cmap, trail=None):
    trail = set(trail or ())
    if capability_ref in trail:
        raise ValueError(f"CAPABILITY_DEPENDENCY_CYCLE:{capability_ref}")
    if capability_ref not in cmap:
        raise ValueError(f"UNKNOWN_CAPABILITY:{capability_ref}")
    trail.add(capability_ref)
    out = set()
    for prereq in cmap[capability_ref]["prerequisite_capability_refs"]:
        if prereq not in cmap:
            raise ValueError(f"UNKNOWN_PREREQUISITE:{prereq}")
        out.add(prereq)
        out.update(transitive_prereqs(prereq, cmap, trail))
    return out


def build_study_scope(bindings_registry, authority):
    cmap = capability_map(authority)
    bindings = bindings_registry["bindings"]
    required_items = sorted(x["item_ref"] for x in bindings)
    exceptions = sorted(x["item_ref"] for x in bindings if x["mapping_state"] != "MAPPED")

    direct = set()
    for binding in bindings:
        if binding["mapping_state"] != "UNMAPPED":
            direct.update(binding["canonical_capability_refs"])
    unknown_direct = direct - set(cmap)
    if unknown_direct:
        raise ValueError("SCOPE_UNKNOWN_CAPABILITY:" + ",".join(sorted(unknown_direct)))

    closures = {cap: transitive_prereqs(cap, cmap) for cap in direct}
    prereq_support = set().union(*(closures.values() or [set()])) - direct
    all_caps = sorted(direct | prereq_support)

    records = []
    for cap in all_caps:
        direct_items = sorted(
            b["item_ref"] for b in bindings
            if b["mapping_state"] != "UNMAPPED" and cap in b["canonical_capability_refs"]
        )
        dependent_direct = sorted(d for d in direct if d != cap and cap in closures[d])
        is_direct = cap in direct
        is_dependency = bool(dependent_direct)
        if is_direct and is_dependency:
            role = "DIRECT_AND_PREREQUISITE"
        elif is_direct:
            role = "DIRECT_ASSESSED"
        else:
            role = "PREREQUISITE_SUPPORT"

        reps, families, verification = set(), set(), set()
        for binding in bindings:
            if binding["mapping_state"] == "UNMAPPED":
                continue
            related = set(binding["canonical_capability_refs"])
            for d in binding["canonical_capability_refs"]:
                related.update(closures[d])
            if cap in related:
                reps.update(binding["representation_demands"])
                families.update(binding["problem_family_refs"])
                verification.update(binding["verification_obligations"])

        records.append({
            "capability_ref": cap,
            "scope_role": role,
            "assessment_question_refs": direct_items,
            "dependent_assessed_capability_refs": dependent_direct,
            "prerequisite_refs": sorted(cmap[cap]["prerequisite_capability_refs"]),
            "representation_requirements": sorted(reps),
            "problem_family_refs": sorted(families),
            "verification_requirements": sorted(verification),
        })

    scope = {
        "study_scope_id": "PENDING",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "question_set_ref": bindings_registry["question_set_ref"],
        "scope_binding_registry_ref": bindings_registry["binding_registry_id"],
        "scope_authority_ref": authority["authority_id"],
        "scope_authority_digest": authority["authority_digest"],
        "required_item_refs": required_items,
        "scope_exception_item_refs": exceptions,
        "direct_assessed_capability_refs": sorted(direct),
        "prerequisite_support_capability_refs": sorted(prereq_support),
        "capability_scope_records": records,
    }
    scope["study_scope_id"] = "MATH-LSS-" + digest(scope)[:16]
    scope["scope_digest"] = digest(scope, "scope_digest")
    return scope


def longitudinal_obligations(readiness):
    needs = {
        "acquisition": "independent evidence that the mathematical meaning and operation are established",
        "independent_reconstruction": "reconstruct or execute without supplied method scaffolds",
        "delayed_retention": "successful delayed retrieval after a meaningful interval",
        "near_transfer": "independent success on a structurally similar new problem",
        "far_transfer": "independent success in a materially different context",
        "mixed_discrimination": "select the correct model or method among competing problem types",
        "fluency": "repeated accurate independent execution without scaffold",
        "timed_performance": "accurate execution under an authorized timed assessment",
    }
    out = []
    for dim in DIMENSIONS:
        if readiness == "READY" and dim in {"acquisition", "independent_reconstruction"}:
            status = "CURRENT_EVIDENCE"
        elif readiness == "DEVELOPING" and dim == "acquisition":
            status = "PARTIAL_CURRENT_EVIDENCE"
        elif dim in {"delayed_retention", "near_transfer", "far_transfer", "mixed_discrimination", "fluency", "timed_performance"}:
            status = "OPEN_FUTURE_EVIDENCE"
        else:
            status = "NOT_EVIDENCED"
        out.append({"dimension": dim, "status": status, "evidence_needed": needs[dim]})
    return out


def treatment_for(scope_record, state, diagnostic_cases, attempt_mode, policy):
    readiness = state["readiness"]
    unresolved = any(
        c["target_capability_ref"] == scope_record["capability_ref"] and c["hypothesis_status"] == "UNRESOLVED"
        for c in diagnostic_cases
    )
    bottleneck = (
        readiness == "DEVELOPING"
        and len(scope_record["dependent_assessed_capability_refs"])
        >= policy["prerequisite_bottleneck_rule"]["minimum_dependent_assessed_capabilities"]
    )
    if readiness == "READY":
        return "VERIFY_ONLY", "VERIFY_AND_MOVE_ON", "Current independent evidence supports brief activation plus verification; full reteaching is not justified."
    if readiness == "DEVELOPING" and bottleneck:
        return "REPAIR_BEFORE", "EARLY_REPAIR", "A demonstrated developing prerequisite feeds multiple assessed capabilities, so repair precedes dependent work."
    if readiness == "DEVELOPING":
        return "REPAIR_IN_UNIT", "EMBEDDED_REPAIR", "A demonstrated developing capability is localized and can be repaired inside the relevant assessed unit."
    if readiness == "UNKNOWN" and unresolved:
        return "PROBE_FIRST", "EARLY_PROBE", "Learner state is unresolved and treatment depends on the distinction; collect decisive evidence before choosing a repair path."
    if readiness == "UNKNOWN":
        note = "No learner attempt evidence exists; unknown status requires assessment-complete teaching without a weakness claim." if attempt_mode == "ABSENT" else "No reliable readiness evidence exists for this in-scope capability; teach it completely rather than inventing weakness."
        return "ACTIVE_STUDY", "CORE_STUDY", note
    raise ValueError(f"UNSUPPORTED_READINESS:{readiness}")


def pck_jobs(treatment, verification_requirements, policy):
    jobs = list(policy["pck_jobs"][treatment])
    if verification_requirements and treatment != "VERIFY_ONLY" and "VERIFICATION_HABIT" not in jobs:
        jobs.append("VERIFICATION_HABIT")
    return jobs


def synthesize(study_scope, learner_snapshot, policy):
    states = {x["capability_ref"]: x for x in learner_snapshot["capability_states"]}
    plans = []
    for rec in study_scope["capability_scope_records"]:
        state = states.get(rec["capability_ref"], {
            "readiness": "UNKNOWN", "confidence": 0.0, "observation_refs": [],
        })
        treatment, band, rationale = treatment_for(
            rec, state, learner_snapshot["diagnostic_cases"], learner_snapshot["attempt_mode"], policy
        )
        plans.append({
            "capability_ref": rec["capability_ref"],
            "scope_role": rec["scope_role"],
            "assessment_question_refs": rec["assessment_question_refs"],
            "prerequisite_refs": rec["prerequisite_refs"],
            "learner_state_readiness": state["readiness"],
            "learner_state_confidence": state["confidence"],
            "learner_state_observation_refs": state["observation_refs"],
            "treatment": treatment,
            "priority_band": band,
            "sequencing_rationale": rationale,
            "required_pck_jobs": pck_jobs(treatment, rec["verification_requirements"], policy),
            "representation_requirements": rec["representation_requirements"],
            "problem_family_refs": rec["problem_family_refs"],
            "verification_requirements": rec["verification_requirements"],
            "future_evidence_obligations": longitudinal_obligations(state["readiness"]),
        })

    input_payload = {
        "study_scope_digest": study_scope["scope_digest"],
        "learner_state_snapshot_digest": learner_snapshot["snapshot_digest"],
        "treatment_policy_version": policy["policy_id"],
    }
    model = {
        "study_model_id": "MATH-LSM-" + digest(input_payload)[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "study_scope_ref": study_scope["study_scope_id"],
        "study_scope_digest": study_scope["scope_digest"],
        "learner_state_snapshot_ref": learner_snapshot["snapshot_id"],
        "learner_state_snapshot_digest": learner_snapshot["snapshot_digest"],
        "learner_attempt_mode": learner_snapshot["attempt_mode"],
        "treatment_policy_version": policy["policy_id"],
        "capability_plans": plans,
        "longitudinal_initialization": {
            "dimensions": DIMENSIONS,
            "invariant": "CURRENT_SUCCESS_DOES_NOT_CLOSE_DELAYED_OR_TRANSFER_OBLIGATIONS",
        },
        "input_digest": digest(input_payload),
    }
    model["study_model_digest"] = digest(model, "study_model_digest")
    return model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope-bindings", required=True)
    ap.add_argument("--authority", required=True)
    ap.add_argument("--learner-state", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    scope = build_study_scope(load(args.scope_bindings), load(args.authority))
    model = synthesize(scope, load(args.learner_state), load(args.policy))
    Path(args.out).write_text(json.dumps({"learner_study_scope": scope, "learner_study_model": model}, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
