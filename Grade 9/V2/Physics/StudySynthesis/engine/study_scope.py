import copy
from study_common import capability_map,transitive_prereqs,learner_evidence_scope_fingerprint,digest,fail,uniq,_binding_related_to_cap

def derive_study_scope(bindings_registry, authority, problem_semantics, study_scope_id=None):
    if bindings_registry["authority_ref"] != authority["authority_id"]:
        fail("SCOPE_AUTHORITY_IDENTITY_MISMATCH")
    if bindings_registry["authority_digest"] != authority["authority_digest"]:
        fail("SCOPE_AUTHORITY_DIGEST_MISMATCH")
    if problem_semantics["question_set_ref"] != bindings_registry["question_set_ref"]:
        fail("PROBLEM_SEMANTICS_QUESTION_SET_MISMATCH")
    if problem_semantics["package_digest"] != digest(problem_semantics, "package_digest"):
        fail("PROBLEM_SEMANTICS_DIGEST_MISMATCH")

    cmap = capability_map(authority)
    bindings = bindings_registry["bindings"]
    mapped = [b for b in bindings if b["mapping_state"] != "UNMAPPED"]
    required_items = uniq(b["item_ref"] for b in bindings)
    scope_exceptions = uniq(
        b["item_ref"] for b in bindings
        if b["mapping_state"] != "MAPPED" or b["resolution_status"] != "CLOSED"
    )

    direct = {c for b in mapped for c in b["canonical_capability_refs"]}
    unknown = direct - set(cmap)
    if unknown:
        fail("SCOPE_UNKNOWN_CAPABILITY", ",".join(sorted(unknown)))
    closures = {cap: transitive_prereqs(cap, cmap) for cap in direct}
    prereq_support = set().union(*(closures.values() or [set()])) - direct
    all_caps = sorted(direct | prereq_support)

    sem_by = {x["item_ref"]: x for x in problem_semantics["items"]}
    for b in mapped:
        if b["item_ref"] not in sem_by:
            fail("P_D_SEMANTICS_MISSING_FOR_SCOPE_ITEM", b["item_ref"])
        if set(sem_by[b["item_ref"]]["family_refs"]) != set(b["problem_family_refs"]):
            fail("P_D_PROBLEM_FAMILY_SCOPE_DRIFT", b["item_ref"])

    records = []
    for cap in all_caps:
        direct_items = uniq(
            b["item_ref"] for b in mapped if cap in b["canonical_capability_refs"]
        )
        dependent_direct = uniq(
            direct_cap for direct_cap in direct
            if direct_cap != cap and cap in closures[direct_cap]
        )
        related = [b for b in mapped if _binding_related_to_cap(b, cap, closures)]
        support_items = uniq(
            b["item_ref"] for b in related if cap not in b["canonical_capability_refs"]
        )
        trace_items = uniq(direct_items + support_items)
        if not trace_items:
            fail("STUDY_SCOPE_CAPABILITY_WITHOUT_SOURCE_TRACE", cap)

        is_direct = cap in direct
        is_dependency = bool(dependent_direct)
        role = (
            "DIRECT_AND_PREREQUISITE" if is_direct and is_dependency
            else "DIRECT_ASSESSED" if is_direct
            else "PREREQUISITE_SUPPORT"
        )

        system_frame = []
        state_phase = []
        model_validity = []
        reps, models, laws, families, route_roles, verify, verify_routes = (
            set(), set(), set(), set(), set(), set(), set()
        )
        for b in sorted(related, key=lambda x: x["item_ref"]):
            item = b["item_ref"]
            sem = sem_by[item]
            system_frame.append({
                "item_ref": item,
                "system_refs": list(b["system_refs"]),
                "object_roles": list(b["object_roles"]),
                "reference_frame": copy.deepcopy(b["reference_frame"]),
                "sign_convention": copy.deepcopy(b["sign_convention"]),
            })
            phase = b["phase_structure"]
            state_phase.append({
                "item_ref": item,
                "state_variable_refs": list(b["state_variable_refs"]),
                "phase_kind": phase["kind"],
                "phases": list(phase["phases"]),
                "continuity_state_refs": list(phase["continuity_state_refs"]),
            })
            required_model_validity = (
                bool(b["model_validity_conditions"])
                or any(cmap[d]["requires_model_validity"] for d in b["canonical_capability_refs"])
            )
            model_validity.append({
                "item_ref": item,
                "required": bool(required_model_validity),
                "physical_model_refs": list(b["physical_model_refs"]),
                "law_refs": list(b["law_refs"]),
                "validity_conditions": list(b["model_validity_conditions"]),
                "model_assumption_scope_status": b["model_assumption_scope_status"],
            })
            reps.update(b["representation_demands"])
            models.update(b["physical_model_refs"])
            laws.update(b["law_refs"])
            families.update(b["problem_family_refs"])
            verify.update(b["verification_obligations"])
            verify_routes.update(sem["verification_route_refs"])
            route_roles.update(step["role"] for step in sem["reasoning_route"]["steps"])
            if sem["model_validity_binding"]["required"] and not required_model_validity:
                fail("MODEL_VALIDITY_DROPPED_FROM_STUDY_SCOPE", item)

        records.append({
            "capability_ref": cap,
            "scope_role": role,
            "assessment_question_refs": direct_items,
            "supporting_assessed_question_refs": support_items,
            "source_scope_trace_item_refs": trace_items,
            "dependent_assessed_capability_refs": dependent_direct,
            "prerequisite_refs": uniq(cmap[cap]["prerequisite_capability_refs"]),
            "system_frame_obligations": system_frame,
            "state_phase_obligations": state_phase,
            "model_validity_obligations": model_validity,
            "representation_requirements": sorted(reps),
            "physical_model_refs": sorted(models),
            "law_refs": sorted(laws),
            "problem_family_refs": sorted(families),
            "reasoning_route_roles": sorted(route_roles),
            "verification_requirements": sorted(verify),
            "verification_route_refs": sorted(verify_routes),
        })

    evidence_scope_ref, evidence_scope_digest = learner_evidence_scope_fingerprint(problem_semantics)
    scope = {
        "study_scope_id": "PENDING",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "question_set_ref": bindings_registry["question_set_ref"],
        "scope_binding_registry_ref": bindings_registry["binding_registry_id"],
        "scope_binding_registry_digest": bindings_registry["binding_registry_digest"],
        "scope_authority_ref": authority["authority_id"],
        "scope_authority_digest": authority["authority_digest"],
        "problem_semantics_ref": problem_semantics["package_id"],
        "problem_semantics_digest": problem_semantics["package_digest"],
        "learner_evidence_scope_ref": evidence_scope_ref,
        "learner_evidence_scope_digest": evidence_scope_digest,
        "required_item_refs": required_items,
        "scope_exception_item_refs": scope_exceptions,
        "direct_assessed_capability_refs": sorted(direct),
        "prerequisite_support_capability_refs": sorted(prereq_support),
        "capability_scope_records": records,
        "scope_invariant": True,
        "study_scope_digest": "",
    }
    if study_scope_id is None:
        seed = copy.deepcopy(scope)
        seed.pop("study_scope_id")
        seed.pop("study_scope_digest")
        study_scope_id = "PHY-P-F-LSS-" + digest(seed)[:16]
    scope["study_scope_id"] = study_scope_id
    scope["study_scope_digest"] = digest(scope, "study_scope_digest")
    return scope
