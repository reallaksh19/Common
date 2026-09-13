from __future__ import annotations

from copy import deepcopy
from typing import Any

from common import BlueprintError, digest, load_assimilation_policy

IMPORTANT_EQUATION_FIELDS = [
    "physical_question", "parent_law_or_model", "assumptions", "frame_axis_sign",
    "derivation_steps", "final_relation", "symbol_meanings", "physical_interpretation",
    "special_cases", "inverse_uses", "checks", "validity_limits", "failure_cases"
]
REP_REQ_FIELDS = ["learning_problem", "knowledge_type", "must_make_visible", "notice_before_math", "must_not_imply"]


def _nonempty(value: Any) -> bool:
    return value not in (None, "", [], {})


def _validate_ct(row: dict[str, Any], cap: str) -> None:
    ct = row.get("cognitive_transformation") or {}
    required = ["transformation_id", "learner_before", "required_change", "learner_after"]
    if any(not _nonempty(ct.get(k)) for k in required):
        raise BlueprintError("COGNITIVE_TRANSFORMATION_INCOMPLETE", cap)
    if ct["learner_before"].strip() == ct["learner_after"].strip():
        raise BlueprintError("COGNITIVE_TRANSFORMATION_NO_CHANGE", cap)


def _validate_atoms(row: dict[str, Any], cap: str, policy: dict[str, Any]) -> None:
    atoms = row.get("learning_atoms") or []
    if not atoms:
        raise BlueprintError("LEARNING_ATOMS_MISSING", cap)
    ids = [a.get("atom_id") for a in atoms]
    if len(set(ids)) != len(ids) or any(not x for x in ids):
        raise BlueprintError("LEARNING_ATOM_IDS_INVALID", cap)
    for atom in atoms:
        if atom.get("transition_kind") not in policy["transition_kinds"]:
            raise BlueprintError("LEARNING_ATOM_TRANSITION_KIND_INVALID", str(atom.get("atom_id")))
        if not _nonempty(atom.get("statement")):
            raise BlueprintError("LEARNING_ATOM_STATEMENT_MISSING", str(atom.get("atom_id")))
        if atom.get("inferential_moves_to_next", 1) > 1:
            raise BlueprintError("LEARNING_ATOM_STOP_RULE_VIOLATED", str(atom.get("atom_id")))


def _validate_inference(row: dict[str, Any], learner_state: dict[str, Any], cap: str, policy: dict[str, Any]) -> None:
    chain = row.get("inference_chain") or {}
    steps = chain.get("steps") or []
    if not chain.get("chain_id") or not steps:
        raise BlueprintError("INFERENCE_CHAIN_MISSING", cap)
    prior = str(learner_state["readiness_prior"])
    require_bridge_states = set(policy["readiness_profiles"][prior]["require_bridge_for_states"])
    for step in steps:
        if not _nonempty(step.get("statement")):
            raise BlueprintError("INFERENCE_STEP_STATEMENT_MISSING", cap)
        state = step.get("learner_status")
        if state not in policy["learner_states"]:
            raise BlueprintError("INFERENCE_STEP_LEARNER_STATE_INVALID", cap)
        if state in require_bridge_states:
            if not step.get("bridge_required") or not _nonempty(step.get("bridge")):
                raise BlueprintError("INFERENCE_JUMP_UNBRIDGED", f"{cap}:{step.get('step_id')}")
        if step.get("compression_allowed") and state != "SECURE":
            raise BlueprintError("INFERENCE_COMPRESSION_WITHOUT_SECURE_STATE", f"{cap}:{step.get('step_id')}")


def _validate_equations(row: dict[str, Any]) -> None:
    for eq in row.get("equations") or []:
        if eq.get("importance") != "IMPORTANT":
            continue
        missing = [k for k in IMPORTANT_EQUATION_FIELDS if not _nonempty(eq.get(k))]
        if missing:
            raise BlueprintError("IMPORTANT_EQUATION_ANATOMY_INCOMPLETE", f"{eq.get('equation_id')}:{','.join(missing)}")
        for step in eq["derivation_steps"]:
            if not _nonempty(step.get("step")) or not _nonempty(step.get("why_legitimate")):
                raise BlueprintError("EQUATION_DERIVATION_JUSTIFICATION_MISSING", str(eq.get("equation_id")))


def _validate_representations(row: dict[str, Any], cap: str) -> None:
    for rep in row.get("representations") or []:
        req = rep.get("requirement") or {}
        missing = [k for k in REP_REQ_FIELDS if not _nonempty(req.get(k))]
        if missing:
            raise BlueprintError("REPRESENTATION_COGNITIVE_REQUIREMENT_INCOMPLETE", f"{cap}:{','.join(missing)}")
        candidates = rep.get("candidates") or []
        waiver = rep.get("single_candidate_waiver")
        if len(candidates) < 2 and (not waiver or not _nonempty(waiver.get("reason"))):
            raise BlueprintError("REPRESENTATION_CANDIDATE_COMPETITION_MISSING", cap)
        ids = [c.get("candidate_id") for c in candidates]
        if len(set(ids)) != len(ids) or any(not x for x in ids):
            raise BlueprintError("REPRESENTATION_CANDIDATE_IDS_INVALID", cap)
        decision = rep.get("decision") or {}
        if not _nonempty(decision.get("selection_reason")):
            raise BlueprintError("REPRESENTATION_SELECTION_REASON_MISSING", cap)
        selected = [decision.get("primary_candidate_id")] + list(decision.get("secondary_candidate_ids") or [])
        if any(x not in ids for x in selected if x):
            raise BlueprintError("REPRESENTATION_DECISION_UNKNOWN_CANDIDATE", cap)


def _validate_symbol_bridge(row: dict[str, Any], purpose: dict[str, Any], cap_state: dict[str, Any], cap: str) -> None:
    has_important = any(eq.get("importance") == "IMPORTANT" for eq in row.get("equations") or [])
    needs = has_important and purpose["symbol_bridge"] == "REQUIRED_FOR_IMPORTANT_EQUATION"
    needs = needs or (has_important and purpose["symbol_bridge"] == "REQUIRED_WHEN_LEARNER_STATE_NOT_SECURE" and cap_state["state"] != "SECURE")
    if needs:
        sb = row.get("symbol_bridge") or {}
        for key in ["bridge_id", "picture", "words", "symbols", "equation"]:
            if not _nonempty(sb.get(key)):
                raise BlueprintError("SYMBOL_BRIDGE_REQUIRED", cap)


def _validate_fading(row: dict[str, Any], cap: str) -> None:
    fp = row.get("fading_plan") or {}
    for stage in ["worked", "faded", "independent"]:
        if not _nonempty(fp.get(stage)):
            raise BlueprintError("FADING_PLAN_STAGE_MISSING", f"{cap}:{stage}")
    independent = fp["independent"]
    if not _nonempty(independent.get("task")) or not _nonempty(independent.get("check")):
        raise BlueprintError("INDEPENDENT_PRACTICE_CHECK_MISSING", cap)


def compile_assimilation(join: dict[str, Any], learner_state: dict[str, Any], purpose: dict[str, Any], design_input: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load_assimilation_policy()
    if join.get("join_state") != "READY_FOR_LEARNER_STATE":
        raise BlueprintError("ASSIMILATION_JOIN_NOT_READY", str(join.get("join_state")))
    if purpose.get("prerequisite_bypass_allowed") is not False:
        raise BlueprintError("PURPOSE_PREREQUISITE_BYPASS_FORBIDDEN")
    if learner_state.get("join_packet_ref") != join.get("packet_id") or learner_state.get("join_digest") != join.get("digest"):
        raise BlueprintError("LEARNER_STATE_JOIN_BINDING_MISMATCH")

    obligations = {o["capability_ref"]: o for o in join.get("obligations", [])}
    learner_caps = {r["capability_ref"]: r for r in learner_state.get("capabilities", [])}
    treatments = design_input.get("capability_treatments") or []
    treatment_caps = [r.get("capability_ref") for r in treatments]
    if set(treatment_caps) != set(obligations) or len(treatment_caps) != len(set(treatment_caps)):
        raise BlueprintError("ASSIMILATION_OBLIGATION_COVERAGE_MISMATCH")

    validated = []
    for source in treatments:
        row = deepcopy(source)
        cap = row["capability_ref"]
        if row.get("obligation_ref") != obligations[cap]["obligation_id"]:
            raise BlueprintError("ASSIMILATION_OBLIGATION_REF_MISMATCH", cap)
        cap_state = learner_caps.get(cap)
        if not cap_state:
            raise BlueprintError("ASSIMILATION_LEARNER_STATE_MISSING", cap)
        _validate_ct(row, cap)
        _validate_atoms(row, cap, policy)
        _validate_inference(row, learner_state, cap, policy)
        _validate_equations(row)
        _validate_representations(row, cap)
        _validate_symbol_bridge(row, purpose, cap_state, cap)
        _validate_fading(row, cap)
        if cap_state["bridge_required_by_profile"] and not row.get("misconception_contrasts"):
            raise BlueprintError("MISCONCEPTION_OR_BOUNDARY_CONTRAST_REQUIRED", cap)
        row["validation_status"] = "PASS"
        validated.append(row)

    bundle = {
        "packet_id": f"A-{design_input['assimilation_request_id']}",
        "packet_type": "A",
        "join_packet_ref": join["packet_id"],
        "join_digest": join["digest"],
        "learner_state_ref": learner_state["packet_id"],
        "learner_state_digest": learner_state["digest"],
        "purpose_ref": purpose["packet_id"],
        "purpose_digest": purpose["digest"],
        "purpose_mode": purpose["mode"],
        "capability_treatments": validated,
        "manuscript_ready": True,
        "validation_status": "PASS",
        "unresolved": []
    }
    bundle["digest"] = digest(bundle)
    return bundle
