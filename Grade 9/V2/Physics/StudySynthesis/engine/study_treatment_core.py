import copy
from collections import Counter
from study_common import TREATMENTS,canonical,digest,fail,validate_policy

def _has_frame_sign(rec):
    return any(
        x["reference_frame"]["required"] or x["sign_convention"]["required"]
        for x in rec["system_frame_obligations"]
    )

def _has_model_validity(rec):
    return any(x["required"] for x in rec["model_validity_obligations"])

def _is_multiphase(rec):
    return any(
        x["phase_kind"] != "SINGLE_PHASE" or bool(x["continuity_state_refs"])
        for x in rec["state_phase_obligations"]
    )

def _is_graph(rec):
    return any("GRAPH" in x.upper() for x in rec["representation_requirements"]) or any(
        "GRAPH" in x.upper() for x in rec["problem_family_refs"]
    )

def future_evidence_obligations(rec):
    out = {
        "DELAYED_INDEPENDENT_RECONSTRUCTION",
        "NEAR_TRANSFER_NEW_INSTANCE",
        "FAR_TRANSFER_NEW_CONTEXT",
        "MIXED_MODEL_DISCRIMINATION",
        "FLUENCY_CHECK",
        "TIMED_PERFORMANCE_CHECK",
    }
    if rec["representation_requirements"]:
        out.add("SAME_CONCEPT_NEW_REPRESENTATION")
    if rec["problem_family_refs"] or rec["physical_model_refs"]:
        out.add("SAME_MODEL_DIFFERENT_STORY")
    if _is_multiphase(rec):
        out.add("MULTIPHASE_STATE_PROPAGATION_AFTER_DELAY")
        out.add("TIMED_MULTI_STAGE_PROBLEM")
    if _has_frame_sign(rec):
        out.add("SIGN_FRAME_DISCRIMINATION")
    if _has_model_validity(rec):
        out.add("MODEL_VALIDITY_HIDDEN_CONDITION")
    if _is_graph(rec):
        out.add("MIXED_GRAPH_MODEL_SELECTION")
    if rec["verification_requirements"]:
        out.add("PHYSICAL_VERIFICATION_WITHOUT_PROMPTING")
    return sorted(out)

def longitudinal_dimensions(state, rec):
    if state == "DEMONSTRATED":
        acquisition = independent = "CURRENT_EVIDENCE"
    elif state in {"EVIDENCE_OF_DIFFICULTY","MIXED"}:
        acquisition, independent = "PARTIAL_CURRENT_EVIDENCE", "OPEN"
    else:
        acquisition = independent = "OPEN"
    return {
        "acquisition": acquisition,
        "independent_reconstruction": independent,
        "delayed_retention": "OPEN",
        "near_transfer": "OPEN",
        "far_transfer": "OPEN",
        "mixed_model_discrimination": "OPEN",
        "representation_translation": "OPEN" if rec["representation_requirements"] else "NOT_APPLICABLE",
        "fluency": "OPEN",
        "timed_performance": "OPEN",
    }

def _probe_requirements_for_cap(snap, cap):
    probes = set()
    for case in snap["diagnostic_cases"]:
        if cap not in case.get("capability_refs", []):
            continue
        if case["status"] != "PROBE_REQUIRED":
            continue
        if case.get("probe_requirement"):
            probes.add(case["probe_requirement"])
        else:
            probes.add("PROBE_FOR_" + case["hypothesis_code"])
    return sorted(probes)

def choose_treatment(rec, state, probe_requirements, policy, attempt_mode):
    if probe_requirements or state == "MIXED":
        treatment = "PROBE_FIRST"
    elif state == "DEMONSTRATED":
        treatment = "READY_VERIFY_ONLY"
    elif state == "EVIDENCE_OF_DIFFICULTY":
        treatment = (
            policy["prerequisite_difficulty_treatment"]
            if rec["dependent_assessed_capability_refs"]
            else policy["state_to_treatment"][state]
        )
    else:
        treatment = policy["state_to_treatment"][state]
    if treatment not in TREATMENTS:
        fail("UNKNOWN_TREATMENT", treatment)
    if attempt_mode == "ABSENT" and state == "UNKNOWN" and treatment in policy["no_attempt_forbidden_treatments"]:
        fail("NO_ATTEMPT_FORCES_REPAIR", rec["capability_ref"])
    if treatment == "PROBE_FIRST" and not probe_requirements:
        fail("PROBE_FIRST_WITHOUT_PROBE_REQUIREMENT", rec["capability_ref"])
    return treatment

def pck_jobs(rec, treatment, policy):
    jobs = list(policy["required_pck_jobs_by_treatment"][treatment])
    if _has_frame_sign(rec):
        jobs.append(policy["mandatory_jobs"]["frame_or_sign"])
    if _has_model_validity(rec):
        jobs.append(policy["mandatory_jobs"]["model_validity"])
    if rec["verification_requirements"]:
        jobs.append(policy["mandatory_jobs"]["verification"])
    return list(dict.fromkeys(jobs))

def sequencing_rationale(rec, state, treatment, attempt_mode):
    if treatment == "READY_VERIFY_ONLY":
        return "Current evidence supports brief activation and an independent physical check; assessed scope remains present without full reteaching."
    if treatment == "REPAIR_BEFORE":
        return "Evidence indicates difficulty in a prerequisite that supports assessed Physics capabilities; repair it before dependent work without relabelling downstream strengths."
    if treatment == "REPAIR_IN_UNIT":
        return "Evidence indicates localized Physics difficulty that can be repaired inside this required assessed capability."
    if treatment == "PROBE_FIRST":
        return "Current evidence is mixed or diagnostically unresolved; retain the targeted probe before committing to a repair treatment."
    if attempt_mode == "ABSENT":
        return "No learner attempt evidence exists; required assessment scope receives complete neutral teaching without a weakness claim."
    return "No reliable readiness evidence exists for this required capability; keep complete assessed teaching rather than inventing weakness."

def build_model(study_scope, learner_snapshot, policy, study_model_id=None):
    snap = learner_snapshot.get("snapshot", learner_snapshot)
    if snap["subject"] != "PHYSICS" or policy["subject"] != "PHYSICS":
        fail("STUDY_MODEL_SUBJECT_MISMATCH")
    if snap["assessment_scope_ref"] != study_scope["learner_evidence_scope_ref"]:
        fail("LEARNER_STATE_SCOPE_REF_DRIFT")
    if snap["assessment_scope_digest"] != study_scope["learner_evidence_scope_digest"]:
        fail("LEARNER_STATE_SCOPE_DIGEST_DRIFT")
    if not snap["scope_unchanged"]:
        fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE")
    validate_policy(policy)

    states = {x["capability_ref"]: x for x in snap["capability_states"]}
    records, longitudinal = [], []
    for rec in study_scope["capability_scope_records"]:
        cap = rec["capability_ref"]
        state_row = states.get(cap, {
            "capability_ref": cap, "state": "UNKNOWN", "confidence": 0.0,
            "positive_evidence_refs": [], "negative_evidence_refs": [],
        })
        state = state_row["state"]
        probes = _probe_requirements_for_cap(snap, cap)
        treatment = choose_treatment(rec, state, probes, policy, snap["attempt_mode"])
        jobs = pck_jobs(rec, treatment, policy)
        future = future_evidence_obligations(rec)
        records.append({
            "capability_ref": cap,
            "scope_role": rec["scope_role"],
            "assessment_question_refs": list(rec["assessment_question_refs"]),
            "supporting_assessed_question_refs": list(rec["supporting_assessed_question_refs"]),
            "source_scope_trace_item_refs": list(rec["source_scope_trace_item_refs"]),
            "prerequisite_refs": list(rec["prerequisite_refs"]),
            "learner_state_ref": snap["snapshot_id"],
            "learner_state": state,
            "treatment": treatment,
            "priority": policy["priority_by_treatment"][treatment],
            "sequencing_rationale": sequencing_rationale(rec, state, treatment, snap["attempt_mode"]),
            "supporting_downstream_refs": list(rec["dependent_assessed_capability_refs"]),
            "probe_requirements": probes,
            "required_pck_jobs": jobs,
            "system_frame_obligations": copy.deepcopy(rec["system_frame_obligations"]),
            "state_phase_obligations": copy.deepcopy(rec["state_phase_obligations"]),
            "model_validity_obligations": copy.deepcopy(rec["model_validity_obligations"]),
            "representation_requirements": list(rec["representation_requirements"]),
            "physical_model_refs": list(rec["physical_model_refs"]),
            "law_refs": list(rec["law_refs"]),
            "problem_family_refs": list(rec["problem_family_refs"]),
            "reasoning_route_roles": list(rec["reasoning_route_roles"]),
            "verification_requirements": list(rec["verification_requirements"]),
            "verification_route_refs": list(rec["verification_route_refs"]),
            "future_evidence_obligations": future,
        })
        longitudinal.append({
            "capability_ref": cap,
            "dimensions": longitudinal_dimensions(state, rec),
            "future_evidence_obligations": future,
        })

    counts = Counter(x["treatment"] for x in records)
    seed = {
        "study_scope_digest": study_scope["study_scope_digest"],
        "learner_snapshot_ref": snap["snapshot_id"],
        "attempt_mode": snap["attempt_mode"],
        "treatment_policy_ref": policy["policy_id"],
        "capability_records": records,
        "longitudinal_initializations": longitudinal,
    }
    if study_model_id is None:
        study_model_id = "PHY-P-F-LSM-" + digest(seed)[:16]
    model = {
        "study_model_id": study_model_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "study_scope_ref": study_scope["study_scope_id"],
        "study_scope_digest": study_scope["study_scope_digest"],
        "learner_snapshot_ref": snap["snapshot_id"],
        "learner_attempt_mode": snap["attempt_mode"],
        "treatment_policy_ref": policy["policy_id"],
        "capability_records": records,
        "longitudinal_initializations": longitudinal,
        "summary": {
            "required_capability_count": len(records),
            "treatment_counts": dict(sorted(counts.items())),
            "scope_complete": True,
            "source_trace_complete": True,
        },
        "study_model_digest": "",
    }
    model["study_model_digest"] = digest(model, "study_model_digest")
    from study_validation import validate_model
    validate_model(model, study_scope, policy)
    return model
