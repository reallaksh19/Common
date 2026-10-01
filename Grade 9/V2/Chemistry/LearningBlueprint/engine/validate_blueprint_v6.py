#!/usr/bin/env python3
"""Fail-closed validator for Chemistry LearningBlueprint v6.

v6 freezes the canonical architecture above the v4/v5 controls:
- Canonical Domain Registry stores validated stable domain assets.
- CDAU owns cross-Core lineage/differentiation, not learner fit.
- SDU governs Core1A/Core1B only and never consumes learner knowledge.
- LAU governs Core2A/Core2B only and routes support from learner state/owner override × task demand × purpose.
- Concept TTUs and Problem TTUs are separate canonical technical objects.
- B layers require a static, target-driven Tutor Dialogue contract.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class BlueprintV6Error(ValueError):
    pass


TASK_DIMS = (
    "conceptual_demand",
    "structural_distance",
    "representation_change",
    "model_discrimination",
    "hidden_constraint",
    "sign_direction_reversal",
    "reversed_target",
    "constraint_inversion",
    "multi_step_bridge",
    "synthesis",
    "competitive_mixing",
    "calculation_load",
)

SDU_EVIDENCE_DIMS = (
    "prerequisite_depth",
    "element_interactivity",
    "inferential_jump_severity",
    "representation_translation",
    "model_discrimination",
    "sign_frame_sensitivity",
    "multi_step_dependency",
    "abstraction",
    "misconception_density",
    "synthesis",
)

LEARNER_SUBDIMS = (
    "recognition",
    "representation",
    "model_selection",
    "first_move",
    "execution",
    "explanation",
    "verification",
)

SUPPORT_BANDS = {
    "FOUNDATION_HIGH_SUPPORT",
    "GUIDED",
    "STANDARD",
    "CHALLENGE_MINIMAL",
}


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _require_fields(payload: dict[str, Any], fields: set[str], code: str) -> None:
    missing = sorted(fields - set(payload))
    if missing:
        raise BlueprintV6Error(f"{code}:{','.join(missing)}")


def _require_numeric_range(mapping: dict[str, Any], names: tuple[str, ...], lo: float, hi: float, code: str) -> None:
    missing = [name for name in names if name not in mapping]
    if missing:
        raise BlueprintV6Error(f"{code}_MISSING:{','.join(missing)}")
    for name in names:
        value = mapping[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not lo <= value <= hi:
            raise BlueprintV6Error(f"{code}_INVALID:{name}")


def validate_registry(payload: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "registry_id", "subtopic_id", "join_ref", "assets", "stable_id_policy", "provenance_closed"}, "CHEM_V6_REGISTRY_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0":
        raise BlueprintV6Error("CHEM_V6_REGISTRY_SCHEMA_INVALID")
    if payload.get("stable_id_policy") != "ASSETS_KEEP_STABLE_IDS_ACROSS_DOWNSTREAM_REALIZATIONS":
        raise BlueprintV6Error("CHEM_V6_REGISTRY_STABLE_ID_POLICY_INVALID")
    if payload.get("provenance_closed") is not True:
        raise BlueprintV6Error("CHEM_V6_REGISTRY_PROVENANCE_OPEN")
    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        raise BlueprintV6Error("CHEM_V6_REGISTRY_ASSETS_MISSING")
    ids: set[str] = set()
    for asset in assets:
        _require_fields(asset, {"asset_id", "asset_type", "ground_truth_refs", "validation_status", "content_hash"}, "CHEM_V6_REGISTRY_ASSET_REQUIRED_FIELD_MISSING")
        aid = asset["asset_id"]
        if not aid or aid in ids:
            raise BlueprintV6Error("CHEM_V6_REGISTRY_ASSET_ID_INVALID")
        ids.add(aid)
        if asset.get("validation_status") != "VALIDATED":
            raise BlueprintV6Error("CHEM_V6_REGISTRY_UNVALIDATED_ASSET")
        if not asset.get("ground_truth_refs"):
            raise BlueprintV6Error("CHEM_V6_REGISTRY_GROUND_TRUTH_REF_MISSING")
        if not str(asset.get("content_hash", "")).strip():
            raise BlueprintV6Error("CHEM_V6_REGISTRY_CONTENT_HASH_MISSING")
    return {"status": "PASS", "asset_count": len(ids), "stable_ids": True, "provenance_closed": True}


def validate_cdau(payload: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {
        "schema_version", "governance_id", "subtopic_id", "purpose_contracts", "content_lineage",
        "asset_reuse", "duplicate_control", "representation_lineage", "example_fingerprints",
        "source_custody", "a_b_differentiation", "owner_decision_provenance", "self_help_requirements", "release_policy",
    }, "CHEM_V6_CDAU_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0":
        raise BlueprintV6Error("CHEM_V6_CDAU_SCHEMA_INVALID")
    purposes = payload["purpose_contracts"]
    if set(purposes) != {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
        raise BlueprintV6Error("CHEM_V6_CDAU_PURPOSE_CONTRACT_INCOMPLETE")
    dup = payload["duplicate_control"]
    if dup.get("semantic_reuse_allowed") is not True or dup.get("pedagogical_duplication_forbidden") is not True:
        raise BlueprintV6Error("CHEM_V6_CDAU_DUPLICATION_POLICY_INVALID")
    custody = payload["source_custody"]
    if not all(custody.get(k) is True for k in ("frozen_question_identity_preserved", "source_provenance_preserved", "canonical_solution_authority_preserved")):
        raise BlueprintV6Error("CHEM_V6_CDAU_SOURCE_CUSTODY_DRIFT")
    diff = payload["a_b_differentiation"]
    if diff.get("learner_action_differs") is not True or diff.get("sequence_differs") is not True or diff.get("pedagogical_duplication_status") != "PASS":
        raise BlueprintV6Error("CHEM_V6_CDAU_AB_DIFFERENTIATION_FAILED")
    release = payload["release_policy"]
    if release.get("cdau_may_not_select_core2_support") is not True:
        raise BlueprintV6Error("CHEM_V6_CDAU_LAU_AUTHORITY_LEAK")
    if release.get("cdau_may_not_rewrite_intrinsic_difficulty") is not True:
        raise BlueprintV6Error("CHEM_V6_CDAU_SDU_AUTHORITY_LEAK")
    return {"status": "PASS", "cross_core_governance": True, "learner_fit_owned_by_lau": True}


def validate_sdu(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "router_id", "subtopic_id", "difficulty", "research_dossier", "concept_decomposition", "representation_plan", "misconception_plan", "core1a_plan", "core1b_plan", "depth_release_gate"}, "CHEM_V6_SDU_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0" or payload.get("router_id") != "SDU":
        raise BlueprintV6Error("CHEM_V6_SDU_IDENTITY_INVALID")
    forbidden = {"knowledge_percent", "learner_state", "support_band", "resolved_support"}
    leaked = sorted(forbidden & set(_walk_keys(payload)))
    if leaked:
        raise BlueprintV6Error(f"CHEM_V6_SDU_LEARNER_ADAPTATION_LEAK:{','.join(leaked)}")
    difficulty = payload["difficulty"]
    badge = difficulty.get("badge")
    allowed = policy["study_differentiation_unit"]["difficulty_bands"]
    if badge not in allowed:
        raise BlueprintV6Error("CHEM_V6_SDU_DIFFICULTY_INVALID")
    if difficulty.get("authority") not in policy["study_differentiation_unit"]["difficulty_authorities"]:
        raise BlueprintV6Error("CHEM_V6_SDU_DIFFICULTY_AUTHORITY_INVALID")
    profile = difficulty.get("evidence_profile", {})
    _require_numeric_range(profile, SDU_EVIDENCE_DIMS, 0, 4, "CHEM_V6_SDU_EVIDENCE_PROFILE")
    dossier = payload["research_dossier"]
    required_level = allowed[badge]["research_level"]
    if dossier.get("research_level") != required_level:
        raise BlueprintV6Error("CHEM_V6_SDU_RESEARCH_LEVEL_INVALID")
    if badge in {"MEDIUM", "HARD"}:
        for key in ("semantic_sources", "learning_difficulty_sources", "misconception_evidence", "representation_evidence", "design_decisions"):
            if not dossier.get(key):
                raise BlueprintV6Error(f"CHEM_V6_SDU_RESEARCH_DOSSIER_INCOMPLETE:{key}")
    decomposition = payload["concept_decomposition"]
    if not decomposition.get("learning_atom_ids"):
        raise BlueprintV6Error("CHEM_V6_SDU_LEARNING_ATOMS_MISSING")
    if badge == "HARD" and not decomposition.get("major_inferential_jump_ids"):
        raise BlueprintV6Error("CHEM_V6_SDU_HARD_INFERENTIAL_JUMPS_MISSING")
    max_allowed = int(allowed[badge]["max_pages"])
    for key, mode in (("core1a_plan", "CORE1A"), ("core1b_plan", "CORE1B")):
        plan = payload[key]
        if plan.get("product_mode") != mode or not plan.get("concept_ttu_refs"):
            raise BlueprintV6Error(f"CHEM_V6_SDU_{mode}_PLAN_INVALID")
        pages = plan.get("max_pages")
        if not isinstance(pages, int) or pages < 1 or pages > max_allowed:
            raise BlueprintV6Error(f"CHEM_V6_SDU_{mode}_PAGE_ENVELOPE_INVALID")
        if plan.get("page_count_is_quality_metric") is not False:
            raise BlueprintV6Error("CHEM_V6_SDU_PAGE_COUNT_QUALITY_METRIC_FORBIDDEN")
    gate = payload["depth_release_gate"]
    true_keys = ("all_learning_atoms_closed", "all_major_inferential_jumps_bridged", "representation_coverage_complete", "equation_assimilation_complete", "misconception_coverage_complete")
    if not all(gate.get(k) is True for k in true_keys) or gate.get("page_budget_exhaustion_required") is not False:
        raise BlueprintV6Error("CHEM_V6_SDU_DEPTH_RELEASE_GATE_OPEN")
    return {"status": "PASS", "router": "SDU", "difficulty_badge": badge, "learner_knowledge_used": False, "max_pages": max_allowed}


def _validate_task_demand(task: dict[str, Any]) -> int:
    _require_numeric_range(task, TASK_DIMS, 0, 3, "CHEM_V6_TASK_DEMAND")
    return int(sum(float(task[k]) for k in TASK_DIMS))


def validate_lau(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "router_id", "question_id", "question_authority_ref", "problem_family", "purpose", "conditioning", "task_demand", "resolved_support", "core2a_plan", "core2b_plan"}, "CHEM_V6_LAU_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0" or payload.get("router_id") != "LAU":
        raise BlueprintV6Error("CHEM_V6_LAU_IDENTITY_INVALID")
    if payload.get("purpose") not in {"FIRST_STUDY", "REVISION", "COMPETITIVE_EXAM"}:
        raise BlueprintV6Error("CHEM_V6_LAU_PURPOSE_INVALID")
    score = _validate_task_demand(payload["task_demand"])
    conditioning = payload["conditioning"]
    mode = conditioning.get("mode")
    support = payload["resolved_support"]
    if support.get("support_band") not in SUPPORT_BANDS:
        raise BlueprintV6Error("CHEM_V6_LAU_SUPPORT_BAND_INVALID")
    if support.get("task_demand_used") is not True or support.get("purpose_used") is not True:
        raise BlueprintV6Error("CHEM_V6_LAU_FIT_INPUT_OMITTED")
    if mode == "KNOWLEDGE_EVIDENCE":
        if "owner_override" in conditioning:
            raise BlueprintV6Error("CHEM_V6_LAU_DUAL_CONDITIONING")
        state = conditioning.get("learner_state")
        if not isinstance(state, dict):
            raise BlueprintV6Error("CHEM_V6_LAU_LEARNER_STATE_MISSING")
        pct = state.get("knowledge_percent")
        if not isinstance(pct, (int, float)) or isinstance(pct, bool) or not 0 <= pct <= 100:
            raise BlueprintV6Error("CHEM_V6_LAU_KNOWLEDGE_PERCENT_INVALID")
        if not state.get("capability_scope") or not state.get("provenance") or not isinstance(state.get("evidence_count"), int) or state["evidence_count"] < 1:
            raise BlueprintV6Error("CHEM_V6_LAU_LEARNER_EVIDENCE_INCOMPLETE")
        _require_numeric_range(state.get("subdimensions", {}), LEARNER_SUBDIMS, 0, 100, "CHEM_V6_LAU_LEARNER_SUBDIMENSION")
        if support.get("decision_basis") != "LEARNER_TASK_FIT" or support.get("learner_state_used") is not True:
            raise BlueprintV6Error("CHEM_V6_LAU_KNOWLEDGE_ONLY_ROUTING_FORBIDDEN")
    elif mode == "OWNER_OVERRIDE":
        if "learner_state" in conditioning:
            raise BlueprintV6Error("CHEM_V6_LAU_DUAL_CONDITIONING")
        override = conditioning.get("owner_override")
        if not isinstance(override, dict) or override.get("support_band") not in SUPPORT_BANDS or not str(override.get("reason", "")).strip() or override.get("preserve_system_finding") is not True:
            raise BlueprintV6Error("CHEM_V6_LAU_OWNER_OVERRIDE_INVALID")
        if support.get("decision_basis") != "OWNER_OVERRIDE_WITH_TASK_DEMAND" or support.get("learner_state_used") is not False:
            raise BlueprintV6Error("CHEM_V6_LAU_OWNER_OVERRIDE_DECISION_INVALID")
        if support.get("support_band") != override.get("support_band"):
            raise BlueprintV6Error("CHEM_V6_LAU_OWNER_OVERRIDE_SUPPORT_DRIFT")
        if "knowledge_percent" in set(_walk_keys(conditioning)):
            raise BlueprintV6Error("CHEM_V6_LAU_OWNER_OVERRIDE_FABRICATED_PERCENT")
    else:
        raise BlueprintV6Error("CHEM_V6_LAU_CONDITIONING_UNRESOLVED")
    for key, mode_name in (("core2a_plan", "CORE2A"), ("core2b_plan", "CORE2B")):
        plan = payload[key]
        if plan.get("product_mode") != mode_name or not plan.get("problem_ttu_refs"):
            raise BlueprintV6Error(f"CHEM_V6_LAU_{mode_name}_PLAN_INVALID")
        if plan.get("support_band") != support.get("support_band"):
            raise BlueprintV6Error("CHEM_V6_LAU_PLAN_SUPPORT_DRIFT")
    return {"status": "PASS", "router": "LAU", "conditioning_mode": mode, "task_demand_score": score, "support_band": support["support_band"], "fit_used": True}


def validate_concept_ttu(payload: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "ttu_family", "ttu_id", "product_mode", "identity", "canonical_expert_state", "learner_transformation", "reconstruction_options", "reconstructable_ttu_refs", "self_help_closure_ref", "realization_contract", "differentiation_fingerprint"}, "CHEM_V6_CONCEPT_TTU_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0" or payload.get("ttu_family") != "CONCEPT_TTU":
        raise BlueprintV6Error("CHEM_V6_CONCEPT_TTU_IDENTITY_INVALID")
    identity = payload["identity"]
    if not identity.get("concept_id") or not identity.get("capability_ids") or not identity.get("learning_atom_ids"):
        raise BlueprintV6Error("CHEM_V6_CONCEPT_TTU_DOMAIN_IDENTITY_INCOMPLETE")
    expert = payload["canonical_expert_state"]
    for key in ("concept_statement", "model", "prerequisites", "conditions", "representations", "equations", "representation_equation_bindings", "reasoning_chain", "misconception_contrasts", "verification"):
        if key not in expert:
            raise BlueprintV6Error(f"CHEM_V6_CONCEPT_TTU_EXPERT_STATE_INCOMPLETE:{key}")
    transform = payload["learner_transformation"]
    if not all(str(transform.get(k, "")).strip() for k in ("before_model", "target_model", "conceptual_change")):
        raise BlueprintV6Error("CHEM_V6_CONCEPT_TTU_TRANSFORMATION_INCOMPLETE")
    if not payload.get("reconstruction_options") or not payload.get("reconstructable_ttu_refs") or not payload.get("self_help_closure_ref"):
        raise BlueprintV6Error("CHEM_V6_CONCEPT_TTU_RECONSTRUCTION_CLOSURE_MISSING")
    mode = payload["product_mode"]
    rc = payload["realization_contract"]
    if mode == "CORE1A":
        if rc.get("identity") != "DECLARATIVE_CONCEPT_REFERENCE" or rc.get("exposure_mode") != "MODEL_THEN_RECONSTRUCT":
            raise BlueprintV6Error("CHEM_V6_CORE1A_CONCEPT_REALIZATION_INVALID")
        if payload.get("tutor_dialogue_ref"):
            raise BlueprintV6Error("CHEM_V6_CORE1A_TUTOR_DIALOGUE_FORBIDDEN")
    elif mode == "CORE1B":
        if rc.get("identity") != "OPEN_CONCEPT_RECONSTRUCTION_TUTOR" or rc.get("exposure_mode") != "RECONSTRUCT_BEFORE_CANONICAL":
            raise BlueprintV6Error("CHEM_V6_CORE1B_CONCEPT_REALIZATION_INVALID")
        if not payload.get("tutor_dialogue_ref"):
            raise BlueprintV6Error("CHEM_V6_CORE1B_TUTOR_DIALOGUE_REQUIRED")
    else:
        raise BlueprintV6Error("CHEM_V6_CONCEPT_TTU_MODE_INVALID")
    if len(set(rc.get("learner_actions", []))) < 2:
        raise BlueprintV6Error("CHEM_V6_CONCEPT_TTU_LEARNER_ACTIONS_TOO_THIN")
    return {"status": "PASS", "ttu_family": "CONCEPT_TTU", "product_mode": mode, "tutor_dialogue_required": mode == "CORE1B"}


def validate_problem_ttu(payload: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "ttu_family", "ttu_id", "product_mode", "identity", "task_state", "expert_solution_state", "task_demand", "learner_interaction", "self_help_closure_ref", "transfer_lineage", "reconstructable_ttu_refs", "support_band_ref", "realization_contract", "differentiation_fingerprint"}, "CHEM_V6_PROBLEM_TTU_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0" or payload.get("ttu_family") != "PROBLEM_TTU":
        raise BlueprintV6Error("CHEM_V6_PROBLEM_TTU_IDENTITY_INVALID")
    ident = payload["identity"]
    if not ident.get("problem_family_id") or not ident.get("capability_requirements") or not ident.get("question_id") or not ident.get("question_authority_ref"):
        raise BlueprintV6Error("CHEM_V6_PROBLEM_TTU_DOMAIN_IDENTITY_INCOMPLETE")
    task = payload["task_state"]
    for key in ("givens", "unknown", "constraints", "event", "representation_options", "competing_models"):
        if key not in task:
            raise BlueprintV6Error(f"CHEM_V6_PROBLEM_TTU_TASK_STATE_INCOMPLETE:{key}")
    expert = payload["expert_solution_state"]
    for key in ("recognition", "representation", "model_selection", "first_move", "reasoning_steps", "equations", "result", "verification", "wrong_routes"):
        if key not in expert:
            raise BlueprintV6Error(f"CHEM_V6_PROBLEM_TTU_EXPERT_STATE_INCOMPLETE:{key}")
    _validate_task_demand(payload["task_demand"])
    if not payload.get("reconstructable_ttu_refs") or not payload.get("self_help_closure_ref") or not payload.get("support_band_ref"):
        raise BlueprintV6Error("CHEM_V6_PROBLEM_TTU_CLOSURE_MISSING")
    lineage = payload["transfer_lineage"]
    expected = {
        "FADING_ANCHOR": "NOT_TRANSFER_EVIDENCE",
        "STRUCTURAL_SIBLING": "NEAR_TRANSFER",
        "FAR_TRANSFER_SIBLING": "FAR_TRANSFER",
    }
    if lineage.get("relationship") not in expected or lineage.get("transfer_evidence_status") != expected[lineage.get("relationship")]:
        raise BlueprintV6Error("CHEM_V6_PROBLEM_TTU_TRANSFER_LINEAGE_INVALID")
    mode = payload["product_mode"]
    rc = payload["realization_contract"]
    if mode == "CORE2A":
        if rc.get("identity") != "ADAPTIVE_DECLARATIVE_PROBLEM_REFERENCE" or rc.get("exposure_mode") != "SETUP_THEN_COMPLETE":
            raise BlueprintV6Error("CHEM_V6_CORE2A_PROBLEM_REALIZATION_INVALID")
        if payload.get("tutor_dialogue_ref"):
            raise BlueprintV6Error("CHEM_V6_CORE2A_TUTOR_DIALOGUE_FORBIDDEN")
    elif mode == "CORE2B":
        if rc.get("identity") != "ADAPTIVE_OPEN_PROBLEM_TUTOR" or rc.get("exposure_mode") != "CHOOSE_OR_RECONSTRUCT_BEFORE_HINTS":
            raise BlueprintV6Error("CHEM_V6_CORE2B_PROBLEM_REALIZATION_INVALID")
        if not payload.get("tutor_dialogue_ref"):
            raise BlueprintV6Error("CHEM_V6_CORE2B_TUTOR_DIALOGUE_REQUIRED")
    else:
        raise BlueprintV6Error("CHEM_V6_PROBLEM_TTU_MODE_INVALID")
    if len(set(rc.get("learner_actions", []))) < 2:
        raise BlueprintV6Error("CHEM_V6_PROBLEM_TTU_LEARNER_ACTIONS_TOO_THIN")
    return {"status": "PASS", "ttu_family": "PROBLEM_TTU", "product_mode": mode, "transfer_relationship": lineage["relationship"]}


def validate_tutor_dialogue(payload: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "dialogue_id", "product_mode", "target_change", "initial_attempt", "learner_output_required", "stages", "stage_selection_reason", "misconception_branches", "canonical_reveal", "reflection", "verification", "repair_route", "delivery_mode"}, "CHEM_V6_DIALOGUE_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0" or payload.get("product_mode") not in {"CORE1B", "CORE2B"}:
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_IDENTITY_INVALID")
    if payload.get("delivery_mode") != "STATIC":
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_LIVE_RUNTIME_FORBIDDEN")
    attempt = payload["initial_attempt"]
    if attempt.get("answer_hidden") is not True or attempt.get("learner_commitment_required") is not True:
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_ATTEMPT_FIRST_REQUIRED")
    outputs = set(payload.get("learner_output_required", []))
    if len(outputs) < 2:
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_LEARNER_OUTPUT_TOO_THIN")
    stages = payload.get("stages", [])
    if len(stages) < 2:
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_STAGES_TOO_THIN")
    stage_types = [s.get("stage_type") for s in stages]
    if len(set(stage_types)) != len(stage_types):
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_DUPLICATE_STAGE_TYPE")
    allowed = {"ATTEMPT", "NOTICE", "REPRESENT", "EXPLAIN", "CONNECT", "START", "CHECK", "REFLECT"}
    if any(t not in allowed for t in stage_types):
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_STAGE_TYPE_INVALID")
    if not str(payload.get("stage_selection_reason", "")).strip():
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_TEMPLATE_DRIVEN_NO_SELECTION_REASON")
    if payload["canonical_reveal"].get("after_attempt") is not True or payload["reflection"].get("compare_my_reasoning") is not True or payload["verification"].get("independent") is not True:
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_REVEAL_REFLECTION_VERIFICATION_OPEN")
    repair = payload["repair_route"]
    if repair.get("available") is not True or repair.get("static_cross_reference_only") is not True:
        raise BlueprintV6Error("CHEM_V6_DIALOGUE_REPAIR_ROUTE_INVALID")
    return {"status": "PASS", "product_mode": payload["product_mode"], "stage_count": len(stages), "target_driven": True, "delivery_mode": "STATIC"}


def validate_self_help(payload: dict[str, Any]) -> dict[str, Any]:
    _require_fields(payload, {"schema_version", "closure_id", "product_mode", "canonical_answer_available", "progressive_help_available", "misconception_help_available", "canonical_reveal_available", "independent_verification", "repair_path", "next_step"}, "CHEM_V6_SELF_HELP_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "6.0.0" or payload.get("product_mode") not in {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
        raise BlueprintV6Error("CHEM_V6_SELF_HELP_IDENTITY_INVALID")
    for key in ("canonical_answer_available", "progressive_help_available", "misconception_help_available", "canonical_reveal_available"):
        if payload.get(key) is not True:
            raise BlueprintV6Error(f"CHEM_V6_SELF_HELP_OPEN:{key}")
    if payload["independent_verification"].get("required") is not True or payload["repair_path"].get("available") is not True or payload["next_step"].get("defined") is not True:
        raise BlueprintV6Error("CHEM_V6_SELF_HELP_CLOSURE_INCOMPLETE")
    return {"status": "PASS", "product_mode": payload["product_mode"], "self_help_closed": True}


def validate_ab_differentiation(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    if a.get("ttu_family") != b.get("ttu_family"):
        raise BlueprintV6Error("CHEM_V6_AB_PAIR_TTU_FAMILY_MISMATCH")
    if a.get("ttu_family") == "CONCEPT_TTU":
        if a.get("product_mode") != "CORE1A" or b.get("product_mode") != "CORE1B":
            raise BlueprintV6Error("CHEM_V6_AB_CONCEPT_PAIR_MODE_INVALID")
    elif a.get("ttu_family") == "PROBLEM_TTU":
        if a.get("product_mode") != "CORE2A" or b.get("product_mode") != "CORE2B":
            raise BlueprintV6Error("CHEM_V6_AB_PROBLEM_PAIR_MODE_INVALID")
    else:
        raise BlueprintV6Error("CHEM_V6_AB_PAIR_TTU_FAMILY_INVALID")
    fa = a.get("differentiation_fingerprint", {})
    fb = b.get("differentiation_fingerprint", {})
    if fa.get("learner_action") == fb.get("learner_action"):
        raise BlueprintV6Error("CHEM_V6_AB_LEARNER_ACTION_DUPLICATION")
    if fa.get("sequence") == fb.get("sequence") if "sequence" in fa and "sequence" in fb else False:
        raise BlueprintV6Error("CHEM_V6_AB_SEQUENCE_DUPLICATION")
    common = set(fa) & set(fb)
    if common and all(fa.get(k) == fb.get(k) for k in common):
        raise BlueprintV6Error("CHEM_V6_AB_PEDAGOGICAL_DUPLICATION")
    return {"status": "PASS", "ttu_family": a["ttu_family"], "learner_action_differs": True, "pedagogical_duplication": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--registry")
    parser.add_argument("--cdau")
    parser.add_argument("--sdu")
    parser.add_argument("--lau")
    parser.add_argument("--concept-ttu")
    parser.add_argument("--problem-ttu")
    parser.add_argument("--dialogue")
    parser.add_argument("--self-help")
    args = parser.parse_args()
    choices = [args.registry, args.cdau, args.sdu, args.lau, args.concept_ttu, args.problem_ttu, args.dialogue, args.self_help]
    if sum(bool(x) for x in choices) != 1:
        raise SystemExit("supply exactly one v6 payload")
    policy = json.loads(Path(args.policy).read_text(encoding="utf-8"))
    if args.registry:
        result = validate_registry(json.loads(Path(args.registry).read_text(encoding="utf-8")))
    elif args.cdau:
        result = validate_cdau(json.loads(Path(args.cdau).read_text(encoding="utf-8")))
    elif args.sdu:
        result = validate_sdu(json.loads(Path(args.sdu).read_text(encoding="utf-8")), policy)
    elif args.lau:
        result = validate_lau(json.loads(Path(args.lau).read_text(encoding="utf-8")), policy)
    elif args.concept_ttu:
        result = validate_concept_ttu(json.loads(Path(args.concept_ttu).read_text(encoding="utf-8")))
    elif args.problem_ttu:
        result = validate_problem_ttu(json.loads(Path(args.problem_ttu).read_text(encoding="utf-8")))
    elif args.dialogue:
        result = validate_tutor_dialogue(json.loads(Path(args.dialogue).read_text(encoding="utf-8")))
    else:
        result = validate_self_help(json.loads(Path(args.self_help).read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
