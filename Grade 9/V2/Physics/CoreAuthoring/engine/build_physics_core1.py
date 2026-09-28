#!/usr/bin/env python3
"""P-G — Promoted Physics PCK selection and Core1 instructional authoring.

    P-F PhysicsLearnerStudyScope + PhysicsLearnerStudyModel  (treatment authority)
  + P-D problem-family / reasoning-route / verification semantics (carried in P-F)
  + P-G promoted-pilot Physics PCK registry                   (teaching affordances)
  + P-G authoring profiles                                    (instance constraints)
  -> PhysicsCore1StudyPlan  (SEE -> REALIZE -> UNDERSTAND lessons + Appendices A/B/C)

PCK never chooses treatment and never redefines canonical Physics. Family
selection is derived from the structural obligations already present in the P-F
record, so a new Physics topic is data, not a new code branch.
"""
import argparse, copy, hashlib, importlib.util, json
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]
FULL = "FULL_LEARNING"
CONCISE = "CONCISE_VERIFY_ONLY"
PROBE = "PROBE"


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def uniq(xs):
    return sorted(set(xs))


# --------------------------------------------------------------------------- PCK


def load_pck_registry(path=None):
    p = Path(path) if path else D / "registry" / "physics_promoted_pck.py"
    spec = importlib.util.spec_from_file_location("physics_promoted_pck", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build_registry()


def validate_pck_registry(reg, minimum_state="PROMOTED_PILOT"):
    """Structural + honesty validation of the promoted PCK registry.

    The point of this function is that an AI/automated review can never be
    laundered into a human expert release state, and a promotion state can never
    be declared beyond what its own review ledger justifies.
    """
    if reg.get("subject") != "PHYSICS":
        fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", "registry subject")
    if reg.get("registry_digest") != digest(reg, "registry_digest"):
        fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", "registry digest")
    if reg.get("pedagogy_model") != "SEE_REALIZE_UNDERSTAND":
        fail("SEE_REALIZE_UNDERSTAND_PHASE_MISSING", "registry pedagogy model")
    automated = set(reg["automated_issuable_review_classes"])
    human_only = set(reg["human_only_review_classes"])
    if automated & human_only:
        fail("AI_REVIEW_COUNTED_AS_EXPERT_PASS", "review class partition")
    if "AI_ASSISTED_REFERENCE_REVIEW" not in automated:
        fail("AI_REVIEW_COUNTED_AS_EXPERT_PASS", "AI review must be automated-issuable")
    if not {"SUBJECT_EXPERT_PASS", "PEDAGOGY_EXPERT_PASS"} <= human_only:
        fail("AI_REVIEW_COUNTED_AS_EXPERT_PASS", "expert passes must be human-only")

    order = reg["promotion_states"]
    seen = set()
    for a in reg["assets"]:
        aid = a["asset_id"]
        if aid in seen:
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", "duplicate " + aid)
        seen.add(aid)
        if a.get("asset_digest") != digest(a, "asset_digest"):
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":digest")
        if a.get("raw_mature_reference_used") is not False:
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":raw reference")
        for phase in ("see_phase", "realize_phase", "understand_phase"):
            if not a.get(phase):
                fail("SEE_REALIZE_UNDERSTAND_PHASE_MISSING", f"{aid}:{phase}")
        if len(a.get("reconstruction_route", [])) < 2:
            fail("NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING", aid)
        if not a.get("verification_method"):
            fail("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY", aid)
        if a.get("family") not in reg["families"]:
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":unknown family")

        ledger = a.get("review_ledger") or []
        if not ledger:
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":empty review ledger")
        for row in ledger:
            rc = row.get("review_class")
            if rc not in reg["review_classes"]:
                fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":unknown review class")
            if row.get("stage") not in reg["review_stages"]:
                fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":unknown review stage")
            expected_reviewer = {
                "AI_ASSISTED_REFERENCE_REVIEW": "REPOSITORY_AUTOMATED_AGENT",
                "MACHINE_AUTHORITY_CHECK": "MACHINE_AUTHORITY_CHECK",
                "SUBJECT_EXPERT_PASS": "AUTHORIZED_HUMAN_SUBJECT_EXPERT",
                "PEDAGOGY_EXPERT_PASS": "AUTHORIZED_HUMAN_PEDAGOGY_EXPERT",
                "ASSESSMENT_EXPERT_PASS": "AUTHORIZED_HUMAN_ASSESSMENT_EXPERT",
            }[rc]
            if row.get("reviewer_authority_class") != expected_reviewer:
                fail("FABRICATED_EXPERT_REVIEWER_IDENTITY", f"{aid}:{rc}")
            if rc in human_only:
                # a human-only PASS is only legal with an attestation reference
                if row.get("state") == "PASS" and not row.get("attestation_ref"):
                    fail("FAKE_HUMAN_REVIEW_STATE", f"{aid}:{rc} PASS without attestation")
            else:
                if row.get("attestation_ref"):
                    fail("AI_REVIEW_COUNTED_AS_EXPERT_PASS", f"{aid}:{rc} carries an attestation")

        auth = a.get("promotion_authority") or {}
        declared = auth.get("promotion_state")
        derived = _derive_promotion_state(ledger, human_only)
        if declared != derived:
            fail("FABRICATED_PROMOTION_STATE", f"{aid}: declared {declared} derived {derived}")
        if declared not in order:
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":promotion state")
        if order.index(declared) < order.index(minimum_state):
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", aid + ":below minimum promotion state")
        expert_granted = declared == "PROMOTED_RELEASE"
        if (auth.get("subject_expert_release_state") == "GRANTED") != expert_granted:
            fail("AI_REVIEW_COUNTED_AS_EXPERT_PASS", aid + ":subject release state")
        if (auth.get("pedagogy_expert_release_state") == "GRANTED") != expert_granted:
            fail("AI_REVIEW_COUNTED_AS_EXPERT_PASS", aid + ":pedagogy release state")
        if auth.get("final_product_release_blocked") is not (not expert_granted):
            fail("FAKE_HUMAN_REVIEW_STATE", aid + ":release blocking")
    return True


def _derive_promotion_state(ledger, human_only):
    def passed(stage, classes):
        return any(
            r["stage"] == stage and r["review_class"] in classes and r["state"] == "PASS"
            for r in ledger
        )

    anyclass = {r["review_class"] for r in ledger}
    if not passed("EVIDENCE", anyclass):
        return "CANDIDATE"
    if not (passed("PEDAGOGICAL", anyclass) and passed("SCOPE", anyclass)):
        return "EVIDENCE_REVIEWED"
    if passed("SUBJECT", {"SUBJECT_EXPERT_PASS"}) and passed("PEDAGOGICAL", {"PEDAGOGY_EXPERT_PASS"}):
        return "PROMOTED_RELEASE"
    return "PROMOTED_PILOT"


# ------------------------------------------------------- structural obligations


def has_frame_or_sign(rec):
    return any(
        x["reference_frame"]["required"] or x["sign_convention"]["required"]
        for x in rec["system_frame_obligations"]
    )


def has_model_validity(rec):
    return any(x["required"] for x in rec["model_validity_obligations"])


def is_multiphase(rec):
    return any(
        x["phase_kind"] != "SINGLE_PHASE" or bool(x["continuity_state_refs"])
        for x in rec["state_phase_obligations"]
    )


def is_graph(rec):
    return any("GRAPH" in x.upper() or "SIGNED_AREA" in x.upper() for x in rec["representation_requirements"])


def is_vector(rec):
    return bool(
        {"MOTION_VECTOR_DIAGRAM", "RELATIVE_STATE_DIAGRAM"} & set(rec["representation_requirements"])
    )


def structural_flags(rec):
    return {
        "frame_or_sign_required": has_frame_or_sign(rec),
        "model_validity_required": has_model_validity(rec),
        "multiphase": is_multiphase(rec),
        "graph": is_graph(rec),
        "vector": is_vector(rec),
        "has_representation_requirement": bool(rec["representation_requirements"]),
        "has_verification_requirement": bool(rec["verification_requirements"]),
    }


def rule_matches(rule, rec, flags):
    when = rule.get("when") or {}
    if not when:
        return True
    for key, want in when.items():
        if key == "any_representation_requirement":
            if not (set(want) & set(rec["representation_requirements"])):
                return False
        elif key == "any_representation_requirement_substring":
            reps = [x.upper() for x in rec["representation_requirements"]]
            if not any(any(sub in r for r in reps) for sub in want):
                return False
        elif key in flags:
            if bool(flags[key]) != bool(want):
                return False
        else:
            fail("CORE1_IS_ONLY_A_REPAIR_MEMO", "unknown family-selection predicate " + key)
    return True


def select_primary_family(rec, profile):
    flags = structural_flags(rec)
    for rule in profile["family_selection_rules"]:
        if rule_matches(rule, rec, flags):
            return rule["family"], rule["rule_id"]
    fail("CORE1_IS_ONLY_A_REPAIR_MEMO", "no family-selection rule matched " + rec["capability_ref"])


def select_pck(rec, reg, profile):
    by_family = {}
    for a in reg["assets"]:
        if a["topic_scope_refs"]:
            continue  # topic-scoped assets need an explicit topic binding, never a default
        by_family.setdefault(a["family"], a)
    family, rule_id = select_primary_family(rec, profile)
    primary = by_family.get(family)
    if not primary:
        fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", rec["capability_ref"] + ":no promoted asset for " + family)
    flags = structural_flags(rec)
    support_families = list(profile["support_pck_families"])
    for flag, fam in profile["conditional_support_families"].items():
        key = {"frame_or_sign": "frame_or_sign_required", "model_validity": "model_validity_required",
               "multiphase": "multiphase", "verification": "has_verification_requirement"}[flag]
        if flags[key]:
            support_families.append(fam)
    # every mandated PCK job must have a backing family present
    for job in rec["required_pck_jobs"]:
        fam = profile["pck_job_to_family"].get(job)
        if not fam:
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", rec["capability_ref"] + ":unmapped pck job " + job)
        support_families.append(fam)
    support = [
        by_family[f]
        for f in dict.fromkeys(support_families)
        if f in by_family and by_family[f]["asset_id"] != primary["asset_id"]
    ]
    return primary, support, rule_id


def asset_of_family(assets, family, fallback):
    return next((a for a in assets if a["family"] == family), fallback)


# ------------------------------------------------------------------- authoring


def structure_clause(rec, problem_profile):
    flags = structural_flags(rec)
    clauses = problem_profile["structure_clause_by_obligation"]
    picked = [
        clauses[key]
        for key, flag in (
            ("frame_or_sign", "frame_or_sign_required"),
            ("model_validity", "model_validity_required"),
            ("multiphase", "multiphase"),
            ("graph", "graph"),
            ("vector", "vector"),
            ("representation", "has_representation_requirement"),
        )
        if flags[flag]
    ]
    return "; ".join(picked) if picked else clauses["default"]


def family_ref(rec):
    refs = rec["problem_family_refs"]
    if not refs:
        fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY", rec["capability_ref"])
    return sorted(refs)[0]


def prompt_for(rec, problem_profile):
    return problem_profile["prompt_frame"].format(
        family=family_ref(rec), structure=structure_clause(rec, problem_profile)
    )


def reasoning_steps(rec, problem_profile):
    roles = [r for r in problem_profile["solution_reasoning_roles"] if r in rec["reasoning_route_roles"]]
    if not roles:
        roles = list(problem_profile["solution_reasoning_roles"])
    steps = [{"role": r, "text": problem_profile["reasoning_role_text"][r]} for r in roles]
    if not any(s["role"] in {"VERIFY_PHYSICAL_PLAUSIBILITY", "CHECK_UNITS"} for s in steps):
        steps.append(
            {
                "role": "VERIFY_PHYSICAL_PLAUSIBILITY",
                "text": problem_profile["reasoning_role_text"]["VERIFY_PHYSICAL_PLAUSIBILITY"],
            }
        )
    return steps


def verification_steps(rec, primary):
    steps = list(rec["verification_requirements"]) or list(primary["verification_method"])
    if not steps:
        fail("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY", rec["capability_ref"])
    return steps


def attempt(stage, rec, primary, problem_profile, lesson_id):
    return {
        "attempt_id": f"{lesson_id}-{stage}",
        "support_stage": stage,
        "prompt": prompt_for(rec, problem_profile) + " " + problem_profile["stage_modifiers"][stage],
        "representation_spec": list(rec["representation_requirements"]),
        "frame_sign_required": has_frame_or_sign(rec),
        "model_validity_required": has_model_validity(rec),
        "verification_steps": verification_steps(rec, primary),
    }


def worked_example(rec, primary, problem_profile, lesson_id):
    return {
        "instance_id": f"{lesson_id}-WORKED-NEW",
        "source_class": problem_profile["new_instance_source_class"],
        "problem_family_ref": family_ref(rec),
        "primary_capability_ref": rec["capability_ref"],
        "physical_model_refs": list(rec["physical_model_refs"]),
        "law_refs": list(rec["law_refs"]),
        "prompt": prompt_for(rec, problem_profile)
        + " Work a newly authored instance of this family; original external transfer items stay reserved for Core2.",
        "representation_spec": list(rec["representation_requirements"]),
        "surface_variation": "situation_reframing_with_family_preserved",
        "external_candidate_refs": [],
        "reasoning_steps": reasoning_steps(rec, problem_profile),
        "verification_steps": verification_steps(rec, primary),
    }


def scope_trace(rec):
    return {
        "assessment_question_refs": list(rec["assessment_question_refs"]),
        "supporting_assessed_question_refs": list(rec["supporting_assessed_question_refs"]),
        "source_scope_trace_item_refs": list(rec["source_scope_trace_item_refs"]),
        "prerequisite_refs": list(rec["prerequisite_refs"]),
        "problem_family_refs": list(rec["problem_family_refs"]),
        "physical_model_refs": list(rec["physical_model_refs"]),
        "law_refs": list(rec["law_refs"]),
        "verification_route_refs": list(rec["verification_route_refs"]),
    }


def build_lesson(rec, reg, profile, problem_profile):
    cap = rec["capability_ref"]
    primary, support, rule_id = select_pck(rec, reg, profile)
    mode = profile["lesson_mode_by_treatment"][rec["treatment"]]
    lesson_id = "PHY-CORE1-" + cap
    assets = [primary] + support
    first_move = asset_of_family(support, "FIRST_MOVE_DECISION_SUPPORT", primary)
    contrast = asset_of_family(support, "MISCONCEPTION_MINIMAL_CONTRAST", primary)
    frame_asset = asset_of_family(assets, "SYSTEM_FRAME_SIGN_SETUP", primary)
    validity_asset = asset_of_family(assets, "MODEL_SELECTION_AND_VALIDITY", primary)
    verify_asset = asset_of_family(assets, "PHYSICAL_VERIFICATION", primary)
    transfer_asset = asset_of_family(assets, "TRANSFER_VARIATION", primary)
    ver = verification_steps(rec, primary)

    base = {
        "lesson_id": lesson_id,
        "capability_ref": cap,
        "treatment": rec["treatment"],
        "lesson_mode": mode,
        "priority": rec["priority"],
        "primary_pck_family": primary["family"],
        "family_selection_rule_ref": rule_id,
        "pck_asset_refs": uniq(a["asset_id"] for a in assets),
        "content_roles": list(profile["content_roles_by_mode"][mode]),
        "scope_trace": scope_trace(rec),
        "required_pck_jobs": list(rec["required_pck_jobs"]),
        "frame_sign_required": has_frame_or_sign(rec),
        "model_validity_required": has_model_validity(rec),
        "multiphase": is_multiphase(rec),
        "representation_requirements": list(rec["representation_requirements"]),
        "verification_steps": ver,
        "future_evidence_obligations": list(rec["future_evidence_obligations"]),
        "release_authority_state": profile["release_authority_state"],
    }

    if mode == FULL:
        base.update(
            {
                "see_phenomenon_anchor": primary["physical_anchor"],
                "see_phase": primary["see_phase"],
                "see_system_frame_sign": frame_asset["system_frame_sign_cue"]
                if has_frame_or_sign(rec)
                else "This capability declares no frame or sign obligation; state the system anyway before writing symbols.",
                "realize_phase": primary["realize_phase"],
                "realize_representation_path": list(primary["representation_path"])
                + ["REQUIRED:" + x for x in rec["representation_requirements"]],
                "realize_reconstruction_steps": list(primary["reconstruction_route"]),
                "understand_phase": primary["understand_phase"],
                "understand_relation_and_validity": validity_asset["model_rule_condition_cue"]
                if has_model_validity(rec)
                else primary["model_rule_condition_cue"],
                "model_validity_conditions": uniq(
                    c for x in rec["model_validity_obligations"] for c in x["validity_conditions"]
                ),
                "ordinary_language_explanation": primary["ordinary_language_bridge"],
                "activation": "First move: " + first_move["reconstruction_route"][0],
                "worked_example": worked_example(rec, primary, problem_profile, lesson_id),
                "concept_helper": first_move["ordinary_language_bridge"],
                "misconception_repair": {
                    "wrong_model": primary["common_wrong_model"],
                    "why_plausible": "The shortcut looks sufficient because it reproduces the right answer in the cases seen so far, before the decisive physical feature is tested.",
                    "minimal_contrast": contrast["minimal_contrast"],
                    "repair_steps": list(contrast["repair_route"]),
                    "retry_prompt": prompt_for(rec, problem_profile)
                    + " Retry on a close but newly authored instance after applying the repaired model.",
                },
                "guided_attempt": attempt("GUIDED", rec, primary, problem_profile, lesson_id),
                "faded_attempt": attempt("FADED", rec, primary, problem_profile, lesson_id),
                "independent_attempt": attempt("INDEPENDENT", rec, primary, problem_profile, lesson_id),
                "probe_attempt": None,
                "physical_verification": verify_asset["understand_phase"],
                "transfer_bridge": "Transfer family: "
                + transfer_asset["transfer_family"]
                + ". Original external transfer items remain reserved for Core2.",
            }
        )
        return base

    if mode == CONCISE:
        base.update(
            {
                "see_phenomenon_anchor": "",
                "see_phase": primary["see_phase"],
                "see_system_frame_sign": frame_asset["system_frame_sign_cue"]
                if has_frame_or_sign(rec)
                else "",
                "realize_phase": "",
                "realize_representation_path": ["REQUIRED:" + x for x in rec["representation_requirements"]],
                "realize_reconstruction_steps": [],
                "understand_phase": "",
                "understand_relation_and_validity": "",
                "model_validity_conditions": uniq(
                    c for x in rec["model_validity_obligations"] for c in x["validity_conditions"]
                ),
                "ordinary_language_explanation": "",
                "activation": "Brief activation: " + first_move["reconstruction_route"][0],
                "worked_example": None,
                "concept_helper": "",
                "misconception_repair": None,
                "guided_attempt": None,
                "faded_attempt": None,
                "independent_attempt": attempt("INDEPENDENT", rec, primary, problem_profile, lesson_id),
                "probe_attempt": None,
                "physical_verification": verify_asset["understand_phase"],
                "transfer_bridge": "Continue without reteaching once the independent physical check has passed.",
            }
        )
        return base

    base.update(
        {
            "see_phenomenon_anchor": "",
            "see_phase": primary["see_phase"],
            "see_system_frame_sign": "",
            "realize_phase": "",
            "realize_representation_path": ["PROBE:" + x for x in rec["representation_requirements"]],
            "realize_reconstruction_steps": [],
            "understand_phase": "",
            "understand_relation_and_validity": "",
            "model_validity_conditions": [],
            "ordinary_language_explanation": "",
            "activation": "Collect the decisive evidence before choosing a repair depth.",
            "worked_example": None,
            "concept_helper": "",
            "misconception_repair": None,
            "guided_attempt": None,
            "faded_attempt": None,
            "independent_attempt": None,
            "probe_attempt": attempt("PROBE", rec, primary, problem_profile, lesson_id),
            "probe_requirements": list(rec["probe_requirements"]),
            "physical_verification": verify_asset["understand_phase"],
            "transfer_bridge": "No transfer escalation until the probe has been interpreted.",
        }
    )
    return base


def build_appendices(lessons, records, profile, problem_profile, completeness):
    rec_by = {r["capability_ref"]: r for r in records}
    items, solutions, handout = [], [], []
    for lesson in lessons:
        rec = rec_by[lesson["capability_ref"]]
        stages = completeness["appendix_a_stage_plan_by_lesson_mode"][lesson["lesson_mode"]]
        for stage in stages:
            iid = f"A-{lesson['capability_ref']}-{stage}"
            sol = f"B-SOL-{iid}"
            items.append(
                {
                    "item_id": iid,
                    "source_class": problem_profile["new_instance_source_class"],
                    "problem_family_ref": family_ref(rec),
                    "primary_capability_ref": lesson["capability_ref"],
                    "support_stage": stage,
                    "scored": stage != "PROBE",
                    "prompt": prompt_for(rec, problem_profile) + " " + problem_profile["stage_modifiers"][stage],
                    "representation_spec": list(rec["representation_requirements"]),
                    "frame_sign_required": has_frame_or_sign(rec),
                    "model_validity_required": has_model_validity(rec),
                    "external_candidate_refs": [],
                    "solution_ref": sol,
                }
            )
            solutions.append(
                {
                    "solution_id": sol,
                    "item_ref": iid,
                    "primary_capability_ref": lesson["capability_ref"],
                    "reasoning_steps": reasoning_steps(rec, problem_profile),
                    "verification_steps": list(lesson["verification_steps"]),
                    "final_response": problem_profile["final_response_frame"],
                    "model_validity_note": "Model assumptions to check: "
                    + ", ".join(
                        uniq(c for x in rec["model_validity_obligations"] for c in x["validity_conditions"])
                    )
                    if has_model_validity(rec)
                    else "This capability record declares no additional model-validity condition.",
                }
            )
        handout.append(
            {
                "capability_ref": lesson["capability_ref"],
                "first_move": lesson["activation"],
                "frame_sign_cue": lesson["see_system_frame_sign"]
                or "Declare the system before writing any signed quantity.",
                "relation_or_decision_cue": lesson["understand_relation_and_validity"]
                or "Match the relation to the known and wanted state variables.",
                "verification_cue": lesson["verification_steps"][0],
            }
        )
    return {
        "appendix_a": {"title": "Appendix A — Core Practice", "present": True, "items": items},
        "appendix_b": {"title": "Appendix B — Core Solutions", "present": True, "solutions": solutions},
        "appendix_c": {
            "title": "Appendix C — Printable Handout",
            "present": True,
            "answer_free": True,
            "supported_capability_refs": uniq(l["capability_ref"] for l in lessons),
            "introduced_capability_refs": [],
            "reference_entries": handout,
            "print_constraints": list(completeness["appendix_c_print_constraints"]),
        },
    }


def reject_forbidden_inputs(obj, forbidden, path="root"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if any(t.lower() in str(k).lower() for t in forbidden):
                fail("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON", f"{path}.{k}")
            reject_forbidden_inputs(v, forbidden, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            reject_forbidden_inputs(v, forbidden, f"{path}[{i}]")


def build_plan(
    study_model,
    study_scope,
    pck_registry,
    profile,
    completeness,
    problem_profile,
    plan_id=None,
):
    validate_pck_registry(pck_registry, profile["minimum_promotion_state_for_authoring"])
    if study_model["subject"] != "PHYSICS" or study_scope["subject"] != "PHYSICS":
        fail("CORE1_IS_ONLY_A_REPAIR_MEMO", "subject")
    if study_model["study_scope_digest"] != study_scope["study_scope_digest"]:
        fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE", "scope drift")
    forbidden = completeness["forbidden_producer_inputs"]
    for obj in (study_model, study_scope, profile, problem_profile):
        reject_forbidden_inputs(obj, forbidden)

    lessons = [build_lesson(r, pck_registry, profile, problem_profile) for r in study_model["capability_records"]]
    appendices = build_appendices(
        lessons, study_model["capability_records"], profile, problem_profile, completeness
    )
    counts = Counter(l["lesson_mode"] for l in lessons)
    plan = {
        "plan_id": plan_id or "PHY-P-G-CORE1-PLAN-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "pedagogy_model": "SEE_REALIZE_UNDERSTAND",
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "study_scope_ref": study_scope["study_scope_id"],
        "study_scope_digest": study_scope["study_scope_digest"],
        "learner_attempt_mode": study_model["learner_attempt_mode"],
        "pck_registry_ref": pck_registry["registry_id"],
        "pck_registry_digest": pck_registry["registry_digest"],
        "authoring_profile_ref": profile["profile_id"],
        "problem_authoring_profile_ref": problem_profile["profile_id"],
        "completeness_policy_ref": completeness["policy_id"],
        "lessons": lessons,
        "appendices": appendices,
        "external_transfer_unspoiled": True,
        "scope_complete": True,
        "summary": {
            "lesson_count": len(lessons),
            "lesson_mode_counts": dict(sorted(counts.items())),
            "appendix_a_item_count": len(appendices["appendix_a"]["items"]),
            "appendix_b_solution_count": len(appendices["appendix_b"]["solutions"]),
        },
        "release_authority_state": profile["release_authority_state"],
        "human_expert_review_states": {
            "SUBJECT_EXPERT_PASS": "PENDING",
            "PEDAGOGY_EXPERT_PASS": "PENDING",
            "ASSESSMENT_EXPERT_PASS": "PENDING",
        },
        "plan_digest": "",
    }
    plan["plan_digest"] = digest(plan, "plan_digest")
    validate_plan(plan, study_model, study_scope, pck_registry, profile, completeness, problem_profile)
    return plan


def validate_plan(plan, study_model, study_scope, pck_registry, profile, completeness, problem_profile):
    validate_pck_registry(pck_registry, profile["minimum_promotion_state_for_authoring"])
    if plan["plan_digest"] != digest(plan, "plan_digest"):
        fail("CORE1_IS_ONLY_A_REPAIR_MEMO", "plan digest")
    if plan["study_model_digest"] != study_model["study_model_digest"]:
        fail("LEARNER_WEAKNESS_SHRINKS_ASSESSMENT_SCOPE", "study model digest")
    for state in plan["human_expert_review_states"].values():
        if state == "PASS":
            fail("FAKE_HUMAN_REVIEW_STATE", "plan claims an expert pass")

    required = {r["capability_ref"] for r in study_scope["capability_scope_records"]}
    lessons = {l["capability_ref"]: l for l in plan["lessons"]}
    if len(lessons) != len(plan["lessons"]) or set(lessons) != required:
        fail("CORE1_IS_ONLY_A_REPAIR_MEMO", "lesson coverage")
    recs = {r["capability_ref"]: r for r in study_model["capability_records"]}
    assets = {a["asset_id"]: a for a in pck_registry["assets"]}

    for cap, l in lessons.items():
        rec = recs[cap]
        if not l["pck_asset_refs"] or any(x not in assets for x in l["pck_asset_refs"]):
            fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY", cap)
        if l["treatment"] != rec["treatment"]:
            fail("PCK_DECIDES_TREATMENT", cap)
        if not l["scope_trace"]["source_scope_trace_item_refs"]:
            fail("CORE1_WITHOUT_SOURCE_SCOPE_TRACE", cap)
        if l["frame_sign_required"] != has_frame_or_sign(rec):
            fail("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_CORE1", cap)
        if l["model_validity_required"] != has_model_validity(rec):
            fail("MODEL_VALIDITY_DROPPED_FROM_CORE1", cap)
        if set(l["representation_requirements"]) != set(rec["representation_requirements"]):
            fail("REPRESENTATION_REQUIREMENT_DROPPED_FROM_CORE1", cap)
        if not l["verification_steps"]:
            fail("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY", cap)
        if l["content_roles"] != profile["content_roles_by_mode"][l["lesson_mode"]]:
            fail("CORE1_IS_ONLY_A_REPAIR_MEMO", cap + ":content roles")

        if l["lesson_mode"] == FULL:
            if has_frame_or_sign(rec) and not l["see_system_frame_sign"]:
                fail("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_CORE1", cap)
            if has_model_validity(rec) and not l["understand_relation_and_validity"]:
                fail("MODEL_VALIDITY_DROPPED_FROM_CORE1", cap)
            if not l["see_phase"] or not l["realize_phase"] or not l["understand_phase"]:
                fail("SEE_REALIZE_UNDERSTAND_PHASE_MISSING", cap)
            if not l["ordinary_language_explanation"] or len(l["realize_reconstruction_steps"]) < 2:
                fail("NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING", cap)
            if rec["representation_requirements"] and not all(
                "REQUIRED:" + x in l["realize_representation_path"]
                for x in rec["representation_requirements"]
            ):
                fail("REPRESENTATION_REQUIREMENT_DROPPED_FROM_CORE1", cap + ":representation path")
            w = l["worked_example"]
            if w is None:
                fail("NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING", cap + ":no worked example")
            if w["source_class"] != "NEW_AUTHORED_CORE1" or w["external_candidate_refs"]:
                fail("CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE", cap)
            if not w["problem_family_ref"]:
                fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY", cap)
            if not w["verification_steps"]:
                fail("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY", cap + ":worked example")
            m = l["misconception_repair"]
            if not m or not m["repair_steps"] or not m["retry_prompt"]:
                fail("MISCONCEPTION_WARNING_WITHOUT_REPAIR", cap)
            for stage in ("guided_attempt", "faded_attempt", "independent_attempt"):
                if l[stage] is None:
                    fail("CORE1_IS_ONLY_A_REPAIR_MEMO", f"{cap}:{stage}")
        elif l["lesson_mode"] == CONCISE:
            if l["worked_example"] or l["guided_attempt"] or l["faded_attempt"] or l["misconception_repair"]:
                fail("READY_CAPABILITY_FULLY_RETAUGHT", cap)
            if l["independent_attempt"] is None:
                fail("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY", cap + ":no independent check")
        else:
            if l["worked_example"] or l["guided_attempt"] or l["faded_attempt"] or l["independent_attempt"]:
                fail("PROBE_SILENTLY_BECOMES_RETEACHING", cap)
            if not l.get("probe_requirements"):
                fail("PROBE_FIRST_WITHOUT_PROBE_REQUIREMENT", cap)

    aps = plan["appendices"]
    for key, code in (
        ("appendix_a", "APPENDIX_A_MISSING"),
        ("appendix_b", "APPENDIX_B_MISSING"),
        ("appendix_c", "APPENDIX_C_MISSING"),
    ):
        if key not in aps or not aps[key].get("present"):
            fail(code)
    items = aps["appendix_a"]["items"]
    sols = aps["appendix_b"]["solutions"]
    if {x["primary_capability_ref"] for x in items} != required:
        fail("CORE1_IS_ONLY_A_REPAIR_MEMO", "Appendix A coverage")
    for x in items:
        if x["source_class"] != "NEW_AUTHORED_CORE1" or x["external_candidate_refs"]:
            fail("APPENDIX_A_USES_ORIGINAL_EXTERNAL_TRANSFER", x["item_id"])
        if not x["problem_family_ref"]:
            fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY", x["item_id"])
    if {x["item_ref"] for x in sols} != {x["item_id"] for x in items} or len(sols) != len(items):
        fail("APPENDIX_B_INCOMPLETE")
    for x in sols:
        if not x["reasoning_steps"] or not x["verification_steps"]:
            fail("PHYSICAL_VERIFICATION_REDUCED_TO_ANSWER_ONLY", x["solution_id"])
    hand = aps["appendix_c"]
    if hand.get("answer_free") is not True:
        fail("HANDOUT_CONTAINS_ANSWERS")
    if (
        hand.get("introduced_capability_refs")
        or set(hand.get("supported_capability_refs", [])) != required
        or {x["capability_ref"] for x in hand.get("reference_entries", [])} != required
    ):
        fail("HANDOUT_INTRODUCES_NEW_PHYSICS")
    blob = canonical(hand).lower()
    for token in ("final_response", "answer is", "= "):
        if token in blob:
            fail("HANDOUT_CONTAINS_ANSWERS", token)
    return True


def main():
    ap = argparse.ArgumentParser()
    for x in ["study-model", "study-scope", "instructional-profile", "problem-profile", "completeness-policy", "out"]:
        ap.add_argument("--" + x, required=True)
    ap.add_argument("--plan-id", default=None)
    a = ap.parse_args()
    plan = build_plan(
        load(a.study_model),
        load(a.study_scope),
        load_pck_registry(),
        load(a.instructional_profile),
        load(a.completeness_policy),
        load(a.problem_profile),
        a.plan_id,
    )
    Path(a.out).write_text(
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
