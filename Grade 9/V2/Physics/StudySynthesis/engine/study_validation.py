from study_common import canonical,digest,fail
from study_treatment_core import _has_model_validity,_has_frame_sign

def validate_model(model, study_scope, policy):
    if study_scope["study_scope_digest"] != digest(study_scope, "study_scope_digest"):
        fail("STUDY_SCOPE_DIGEST_MISMATCH")
    if model["study_model_digest"] != digest(model, "study_model_digest"):
        fail("STUDY_MODEL_DIGEST_MISMATCH")
    if model["study_scope_ref"] != study_scope["study_scope_id"] or model["study_scope_digest"] != study_scope["study_scope_digest"]:
        fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE")

    scope_records = {x["capability_ref"]: x for x in study_scope["capability_scope_records"]}
    records = {x["capability_ref"]: x for x in model["capability_records"]}
    if len(records) != len(model["capability_records"]) or set(records) != set(scope_records):
        fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE")
    longs = {x["capability_ref"]: x for x in model["longitudinal_initializations"]}
    if set(longs) != set(records):
        fail("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL", "longitudinal coverage")

    structural_fields = [
        "scope_role","assessment_question_refs","supporting_assessed_question_refs",
        "source_scope_trace_item_refs","prerequisite_refs","system_frame_obligations",
        "state_phase_obligations","model_validity_obligations","representation_requirements",
        "physical_model_refs","law_refs","problem_family_refs","reasoning_route_roles",
        "verification_requirements","verification_route_refs",
    ]
    for cap, row in records.items():
        src = scope_records[cap]
        for field in structural_fields:
            if canonical(row[field]) != canonical(src[field]):
                if field == "model_validity_obligations":
                    fail("MODEL_VALIDITY_DROPPED_FROM_STUDYMODEL", cap)
                if field == "system_frame_obligations":
                    fail("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_STUDYMODEL", cap)
                if field == "source_scope_trace_item_refs":
                    fail("STUDYMODEL_WITHOUT_SOURCE_SCOPE_TRACE", cap)
                fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE", f"{cap}:{field}")
        if not row["source_scope_trace_item_refs"]:
            fail("STUDYMODEL_WITHOUT_SOURCE_SCOPE_TRACE", cap)
        if model["learner_attempt_mode"] == "ABSENT" and row["learner_state"] == "UNKNOWN" and row["treatment"] in policy["no_attempt_forbidden_treatments"]:
            fail("NO_ATTEMPT_FORCES_REPAIR", cap)
        if row["learner_state"] == "DEMONSTRATED" and row["treatment"] != "READY_VERIFY_ONLY":
            fail("UPSTREAM_PHYSICS_STRENGTH_RELABELLED_WEAK_TO_SUPPORT_REPAIR", cap)
        if row["treatment"] == "READY_VERIFY_ONLY":
            forbidden = set(row["required_pck_jobs"]) & set(policy["ready_forbidden_full_reteach_jobs"])
            if forbidden:
                fail("READY_CAPABILITY_FULLY_RETAUGHT_FOR_PAGE_DENSITY", f"{cap}:{sorted(forbidden)}")
        if row["treatment"] == "PROBE_FIRST" and not row["probe_requirements"]:
            fail("PROBE_FIRST_WITHOUT_PROBE_REQUIREMENT", cap)
        if _has_model_validity(src):
            if policy["mandatory_jobs"]["model_validity"] not in row["required_pck_jobs"]:
                fail("MODEL_VALIDITY_DROPPED_FROM_STUDYMODEL", cap)
        if _has_frame_sign(src):
            if policy["mandatory_jobs"]["frame_or_sign"] not in row["required_pck_jobs"]:
                fail("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_STUDYMODEL", cap)
        if src["verification_requirements"]:
            if policy["mandatory_jobs"]["verification"] not in row["required_pck_jobs"]:
                fail("VERIFICATION_REQUIREMENT_DROPPED_FROM_STUDYMODEL", cap)
        dims = longs[cap]["dimensions"]
        if dims["delayed_retention"] != "OPEN":
            fail("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL", cap)
        for dim in ["near_transfer","far_transfer","mixed_model_discrimination","fluency","timed_performance"]:
            if dims[dim] != "OPEN":
                fail("ONE_CURRENT_SUCCESS_CLOSES_FUTURE_EVIDENCE", f"{cap}:{dim}")

    if model["summary"]["required_capability_count"] != len(records):
        fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE", "summary count")
    if not model["summary"]["scope_complete"] or not model["summary"]["source_trace_complete"]:
        fail("STUDYMODEL_WITHOUT_SOURCE_SCOPE_TRACE", "summary")
    return True
