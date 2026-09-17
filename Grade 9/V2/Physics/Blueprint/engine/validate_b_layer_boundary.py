#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_B_ROLES = {"CORE1B", "CORE2B"}
REQUIRED_TRANSFER_DIMENSIONS = {
    "STRUCTURAL_DISTANCE", "REPRESENTATION_CHANGE", "MODEL_DISCRIMINATION",
    "MULTI_STEP_BRIDGE", "SYNTHESIS", "COMPETITIVE_MIXING",
}
REQUIRED_FORBIDDEN_EVIDENCE = {"UNIT_READINESS_FLAG", "TEACHING_RECEIPT", "AUTHOR_CONFIG", "SIMULATED_PASS"}


def validate_boundary(policy: Mapping, architecture: Mapping, bindings: Mapping) -> None:
    roles = set(architecture.get("roles") or [])
    if not REQUIRED_B_ROLES <= roles:
        raise AssertionError("B_LAYER_ROLES_MISSING")

    lifecycle = architecture.get("role_lifecycle") or {}
    if lifecycle.get("CORE1B") not in {"DRAFT", "ACTIVE"} or lifecycle.get("CORE2B") not in {"DRAFT", "ACTIVE"}:
        raise AssertionError("B_LAYER_LIFECYCLE_INVALID")

    bound = bindings.get("roles") or {}
    for role in REQUIRED_B_ROLES:
        if role not in bound:
            raise AssertionError("B_LAYER_ROLE_BINDING_MISSING:" + role)
        authority = str(bound[role].get("authority", ""))
        if "NO_" not in authority or "AUTHORITY" not in authority:
            raise AssertionError("B_LAYER_AUTHORITY_BOUNDARY_WEAK:" + role)

    split = policy.get("role_split") or {}
    if not all(split.get(k) is True for k in (
        "a_layers_authorize", "b_layers_execute", "b_layers_may_not_change_physics_truth",
        "b_layers_may_not_expand_transfer_legality", "b_layers_may_capture_observed_learner_evidence",
    )):
        raise AssertionError("B_LAYER_ROLE_SPLIT_DRIFT")

    receipts = policy.get("receipt_semantics") or {}
    expected_receipts = {
        "core1a_authority_release": "AUTHORIZES_WHAT_MAY_BE_TAUGHT",
        "core1b_exposure_receipt": "PROVES_RUNTIME_EXPOSURE_NOT_MASTERY",
        "observed_learner_evidence": "MAY_UPDATE_CONTROL_STATE_WITH_PROVENANCE",
        "core2a_legal_pool": "AUTHORIZES_WHICH_TRANSFER_ITEMS_ARE_LEGAL",
        "core2b_attempt_receipt": "OBSERVED_RUNTIME_EVIDENCE_NOT_LEGALITY",
    }
    if any(receipts.get(k) != v for k, v in expected_receipts.items()):
        raise AssertionError("B_LAYER_RECEIPT_SEMANTICS_DRIFT")

    handoffs = policy.get("handoffs") or {}
    if not handoffs.get("core1a_to_core1b_requires_release_ref_and_digest"):
        raise AssertionError("CORE1B_UPSTREAM_CUSTODY_MISSING")
    if not handoffs.get("core2a_to_core2b_requires_legal_pool_ref_and_digest"):
        raise AssertionError("CORE2B_LEGAL_POOL_CUSTODY_MISSING")
    if not handoffs.get("core2b_item_requires_exact_core2a_item_ref"):
        raise AssertionError("CORE2B_ITEM_CUSTODY_MISSING")
    if not handoffs.get("b_to_control_requires_observed_evidence"):
        raise AssertionError("B_LAYER_CONTROL_FEEDBACK_UNGROUNDED")
    if not handoffs.get("core2b_to_core1b_repair_is_request_only"):
        raise AssertionError("B_LAYER_REPAIR_AUTHORITY_LEAK")

    c1b = policy.get("core1b_release_criteria") or {}
    for key, code in (
        ("prerequisite_may_be_omitted_only_with_secure_observed_evidence", "CORE1B_SECURE_PREREQUISITE_SKIP_UNGROUNDED"),
        ("unit_readiness_flags_are_requirements_not_evidence", "CORE1B_READINESS_FLAG_MASQUERADES_AS_EVIDENCE"),
        ("applicability_required_when_upstream_model_validity_required", "CORE1B_APPLICABILITY_GATE_DROPPED"),
        ("explain_required_when_capability_contract_requires_explanation", "CORE1B_EXPLAIN_CONTRACT_DROPPED"),
        ("release_claims_require_observed_evidence_refs", "CORE1B_RELEASE_EVIDENCE_CUSTODY_MISSING"),
    ):
        if not c1b.get(key):
            raise AssertionError(code)

    evidence = policy.get("learner_evidence") or {}
    if not evidence.get("state_may_not_be_synthesized_from_unit_configuration"):
        raise AssertionError("UNIT_CONFIGURATION_MASQUERADES_AS_LEARNER_EVIDENCE")
    if not evidence.get("evidence_ref_and_digest_required"):
        raise AssertionError("LEARNER_EVIDENCE_CUSTODY_MISSING")
    if not evidence.get("event_identity_and_order_required"):
        raise AssertionError("LEARNER_EVIDENCE_EVENT_IDENTITY_MISSING")
    if not evidence.get("supersession_preserves_prior_events"):
        raise AssertionError("LEARNER_EVIDENCE_HISTORY_OVERWRITABLE")
    if not evidence.get("representation_coverage_requires_successful_observed_use"):
        raise AssertionError("REPRESENTATION_EXPOSURE_MASQUERADES_AS_MASTERY")
    if not evidence.get("append_only"):
        raise AssertionError("RUNTIME_EVIDENCE_NOT_APPEND_ONLY")
    if not REQUIRED_FORBIDDEN_EVIDENCE <= set(evidence.get("forbidden_basis") or []):
        raise AssertionError("LEARNER_EVIDENCE_FORBIDDEN_BASIS_INCOMPLETE")

    transfer = policy.get("transfer_selection") or {}
    for key, code in (
        ("single_session_state_insufficient", "CORE2B_SINGLE_STATE_OVERREACH"),
        ("per_required_capability_state_required", "CORE2B_PER_CAPABILITY_EVIDENCE_MISSING"),
        ("all_required_capabilities_must_meet_item_floor", "CORE2B_MULTI_CAPABILITY_FLOOR_MISSING"),
        ("representation_transfer_requires_matching_observed_representation_evidence", "CORE2B_REPRESENTATION_EVIDENCE_MISSING"),
        ("independent_may_reach_representation_transfer_only_with_matching_evidence", "CORE2B_T2_INDEPENDENT_RULE_MISSING"),
        ("scalar_transfer_rank_may_not_be_sole_authorizer", "CORE2B_SCALAR_TRANSFER_RANK_OVERREACH"),
        ("discrimination_and_synthesis_are_independent_dimensions", "CORE2B_DISCRIMINATION_SYNTHESIS_COLLAPSED"),
        ("purpose_cannot_expand_core2a_legal_pool", "CORE2B_PURPOSE_EXPANDS_LEGALITY"),
        ("retrieval_due_cannot_expand_core2a_legal_pool", "CORE2B_RETRIEVAL_EXPANDS_LEGALITY"),
    ):
        if not transfer.get(key):
            raise AssertionError(code)
    if set(transfer.get("transfer_dimensions") or []) != REQUIRED_TRANSFER_DIMENSIONS:
        raise AssertionError("CORE2B_TRANSFER_DIMENSION_DRIFT")

    repair = policy.get("repair_loop") or {}
    if not repair.get("wrong_answer_is_not_diagnosis"):
        raise AssertionError("CORE2B_WRONG_ANSWER_USED_AS_DIAGNOSIS")
    if not repair.get("automatic_error_classification_is_hypothesis_until_correlated"):
        raise AssertionError("CORE2B_ERROR_HYPOTHESIS_OVERCLAIM")
    if not repair.get("repair_smallest_explanatory_prerequisite_set"):
        raise AssertionError("CORE1B_REPAIR_SCOPE_TOO_BROAD")
    if not repair.get("repair_request_may_not_mutate_core1a_authority") or not repair.get("repair_request_may_not_mutate_core2a_legality"):
        raise AssertionError("B_LAYER_REPAIR_MUTATES_A_LAYER")
    if not repair.get("return_to_original_target_after_repair"):
        raise AssertionError("B_LAYER_REPAIR_LOSES_ORIGINAL_TARGET")


def main() -> None:
    load = lambda p: json.loads(p.read_text(encoding="utf-8"))
    validate_boundary(
        load(ROOT / "policy" / "b-layer-runtime-boundary.v1.json"),
        load(ROOT / "policy" / "architecture.v1.json"),
        load(ROOT / "policy" / "role-bindings.v1.json"),
    )
    print("Blueprint B-layer runtime boundary: PASS")


if __name__ == "__main__":
    main()
