"""Acceptance-basis adoption, scoped authority and replay helpers for Local PR Delivery v1.1.

This module deliberately keeps acceptance-basis identity separate from Review Lease
freshness. Historical evidence is never mutated; validity is derived against the
current candidate/basis inputs.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from typing import Any


class AcceptanceBasisError(ValueError):
    pass


CHANGE_KINDS = {
    "DEFECT_REPAIR",
    "COVERAGE_EXTENSION",
    "METHOD_CHANGE",
    "ORACLE_CHANGE",
    "BASELINE_CHANGE",
    "TOLERANCE_CHANGE",
    "REQUIREMENT_CHANGE",
    "CLARIFICATION",
}
RISK_EFFECTS = {"STRENGTHENING", "NEUTRAL", "RELAXING", "UNKNOWN"}
CAPABILITIES = {
    "ROLE_EXECUTION",
    "PRODUCT_WRITE",
    "ACCEPTANCE_POLICY_WRITE",
    "RISK_RELAXATION",
    "MERGE",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AcceptanceBasisError(message)


def instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp needs a timezone")
    return parsed.astimezone(timezone.utc)


def canonical_digest(value: Any, omit_fields: tuple[str, ...] = ("digest",)) -> str:
    if isinstance(value, dict):
        omit = set(omit_fields)
        payload = {key: item for key, item in value.items() if key not in omit}
    else:
        payload = value
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def grant_active(grant: dict[str, Any], at: datetime) -> bool:
    issued = instant(grant["issued_at"])
    expires = instant(grant["expires_at"]) if grant.get("expires_at") else None
    revoked = instant(grant["revoked_at"]) if grant.get("revoked_at") else None
    return issued <= at and (expires is None or at <= expires) and (revoked is None or at < revoked)


def _scope_matches(grant_scope: dict[str, Any], requested_scope: dict[str, Any]) -> bool:
    for key in ("parent_task_id", "responsibility_task_id", "acceptance_epoch_id"):
        granted = grant_scope.get(key)
        requested = requested_scope.get(key)
        if granted is not None and granted != requested:
            return False
    return True


def matching_grants(
    grants: list[dict[str, Any]],
    *,
    principal: str,
    capability: str,
    scope: dict[str, Any],
    at: datetime,
) -> list[dict[str, Any]]:
    require(capability in CAPABILITIES, f"Unknown capability: {capability}")
    return [
        grant
        for grant in grants
        if grant["principal"] == principal
        and grant["capability"] == capability
        and grant_active(grant, at)
        and _scope_matches(grant["scope"], scope)
    ]


def require_grant(
    grants: list[dict[str, Any]],
    *,
    principal: str,
    capability: str,
    scope: dict[str, Any],
    at: datetime,
) -> dict[str, Any]:
    matches = matching_grants(
        grants,
        principal=principal,
        capability=capability,
        scope=scope,
        at=at,
    )
    require(matches, f"{principal} lacks {capability} authority for requested scope")
    require(len(matches) == 1, f"Ambiguous active {capability} grants for {principal}")
    return matches[0]


def validate_change_proposal(proposal: dict[str, Any]) -> None:
    require(proposal["change_kind"] in CHANGE_KINDS, "Unknown acceptance change_kind")
    require(proposal["risk_effect"] in RISK_EFFECTS, "Unknown acceptance risk_effect")
    require(proposal["status"] in {"PROPOSED", "ADOPTED", "REJECTED"}, "Unknown proposal status")
    require(bool(proposal["rationale"].strip()), "Acceptance change needs rationale")
    require(bool(proposal["evidence_refs"]), "Acceptance change needs evidence")
    if proposal["status"] == "ADOPTED":
        require(proposal.get("adopted_by"), "Adopted change needs adopted_by")
        require(proposal.get("adoption_ref"), "Adopted change needs adoption_ref")
        require(proposal.get("adopted_at"), "Adopted change needs adopted_at")


def validate_adoption_authority(
    proposal: dict[str, Any],
    grants: list[dict[str, Any]],
) -> None:
    validate_change_proposal(proposal)
    require(proposal["status"] == "ADOPTED", "Only adopted proposals establish a governing basis")
    at = instant(proposal["adopted_at"])
    scope = {
        "parent_task_id": proposal["parent_task_id"],
        "responsibility_task_id": proposal.get("responsibility_task_id"),
        "acceptance_epoch_id": proposal.get("previous_epoch_id"),
    }
    require_grant(
        grants,
        principal=proposal["adopted_by"],
        capability="ACCEPTANCE_POLICY_WRITE",
        scope=scope,
        at=at,
    )
    if proposal["risk_effect"] in {"RELAXING", "UNKNOWN"}:
        risk_principal = proposal.get("risk_accepted_by")
        require(risk_principal, "RELAXING/UNKNOWN acceptance change requires risk_accepted_by")
        require(proposal.get("risk_acceptance_ref"), "RELAXING/UNKNOWN change needs risk acceptance reference")
        require_grant(
            grants,
            principal=risk_principal,
            capability="RISK_RELAXATION",
            scope=scope,
            at=at,
        )


def build_epoch(proposal: dict[str, Any], grants: list[dict[str, Any]]) -> dict[str, Any]:
    validate_adoption_authority(proposal, grants)
    epoch = {
        "record": "ACCEPTANCE_EPOCH",
        "epoch_id": proposal["new_epoch_id"],
        "parent_task_id": proposal["parent_task_id"],
        "previous_epoch_id": proposal.get("previous_epoch_id"),
        "project_protocol_ref": proposal["proposed_project_protocol_ref"],
        "project_protocol_digest": proposal["proposed_project_protocol_digest"],
        "protected_surface_digest": proposal["proposed_protected_surface_digest"],
        "adopted_by": proposal["adopted_by"],
        "adoption_ref": proposal["adoption_ref"],
        "adopted_at": proposal["adopted_at"],
        "change_proposal_ref": proposal["proposal_id"],
        "change_kind": proposal["change_kind"],
        "risk_effect": proposal["risk_effect"],
    }
    epoch["digest"] = canonical_digest(epoch)
    return epoch


def protocol_indexes(protocol: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    criteria: dict[str, Any] = {}
    for acceptance_set in protocol["acceptance_sets"]:
        for criterion in acceptance_set["criteria"]:
            require(criterion["id"] not in criteria, "Duplicate project criterion")
            criteria[criterion["id"]] = criterion
    methods = {method["id"]: method for method in protocol["verification_methods"]}
    require(len(methods) == len(protocol["verification_methods"]), "Duplicate project verification method")
    gates = {gate["id"]: gate for gate in protocol["external_gates"]}
    require(len(gates) == len(protocol["external_gates"]), "Duplicate project external gate")
    return criteria, methods, gates


def _binding_method_ids(profile: dict[str, Any], role: str, criterion_id: str) -> set[str]:
    return {
        binding["verification_method_id"]
        for binding in profile["role_bindings"][role]
        if binding["criterion_id"] == criterion_id
    }


def validate_profile(
    profile: dict[str, Any],
    protocol: dict[str, Any],
    epoch: dict[str, Any],
) -> None:
    require(profile["acceptance_epoch_id"] == epoch["epoch_id"], "Profile binds wrong acceptance epoch")
    require(profile["project_protocol_ref"] == epoch["project_protocol_ref"], "Profile binds wrong project protocol ref")
    require(profile["project_protocol_digest"] == epoch["project_protocol_digest"], "Profile binds wrong project protocol digest")
    require(profile["digest"] == canonical_digest(profile), "Acceptance Profile digest mismatch")

    criteria, methods, gates = protocol_indexes(protocol)
    selected = set(profile["criterion_refs"])
    excluded = set(profile["excluded_criteria"])
    require(selected, "Acceptance Profile needs at least one criterion")
    require(not selected & excluded, "Criterion cannot be both selected and excluded")
    require(selected <= set(criteria), "Acceptance Profile references unknown criterion")
    require(set(profile["external_gate_ids"]) <= set(gates), "Acceptance Profile references unknown external gate")

    for role, flag in (("REVIEWER", "reviewer_check_required"), ("COORDINATOR", "super_review_required")):
        bindings = profile["role_bindings"][role]
        seen_pairs: set[tuple[str, str]] = set()
        for binding in bindings:
            pair = (binding["criterion_id"], binding["verification_method_id"])
            require(pair not in seen_pairs, "Duplicate Acceptance Profile role binding")
            seen_pairs.add(pair)
            require(binding["criterion_id"] in selected, "Role binding criterion is outside Acceptance Profile")
            criterion = criteria[binding["criterion_id"]]
            require(criterion[flag], f"{role} binding supplied for criterion not required by that role")
            method = methods.get(binding["verification_method_id"])
            require(method, "Role binding references unknown verification method")
            require(binding["verification_method_id"] in criterion["verification_method_ids"], "Role binding method is not declared by criterion")
            require(role in method["applies_to_roles"], "Verification method does not apply to role")
            require(binding.get("harness_id") == method.get("harness_id"), "Role binding harness differs from project method")
            require(binding.get("external_gate_id") == method.get("external_gate_id"), "Role binding external gate differs from project method")
            require(set(binding["required_evidence_classes"]) == set(method["required_evidence_classes"]), "Role binding evidence classes differ from project method")

        for criterion_id in selected:
            criterion = criteria[criterion_id]
            if not criterion[flag]:
                continue
            expected = {
                mid
                for mid in criterion["verification_method_ids"]
                if role in methods[mid]["applies_to_roles"]
            }
            require(expected, f"{criterion_id} requires {role} but has no applicable verification method")
            require(
                _binding_method_ids(profile, role, criterion_id) == expected,
                f"Acceptance Profile does not exactly bind required {role} methods for {criterion_id}",
            )


def evidence_validity_projection(
    evidence: dict[str, Any],
    *,
    candidate_sha: str,
    acceptance_epoch_id: str,
    project_protocol_digest: str,
    acceptance_profile_digest: str,
    protected_surface_digest: str,
    environment_digest: str | None = None,
    dependency_heads: dict[str, str] | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    checks = (
        ("candidate_sha", candidate_sha, "CANDIDATE_CHANGED"),
        ("acceptance_epoch_id", acceptance_epoch_id, "ACCEPTANCE_BASIS_CHANGED"),
        ("project_protocol_digest", project_protocol_digest, "PROJECT_PROTOCOL_CHANGED"),
        ("acceptance_profile_digest", acceptance_profile_digest, "ACCEPTANCE_PROFILE_CHANGED"),
        ("protected_surface_digest", protected_surface_digest, "PROTECTED_SURFACE_CHANGED"),
    )
    for key, expected, reason in checks:
        if evidence.get(key) != expected:
            reasons.append(reason)
    if environment_digest is not None and evidence.get("environment_digest") != environment_digest:
        reasons.append("ENVIRONMENT_CHANGED")
    if dependency_heads is not None and evidence.get("dependency_heads", {}) != dependency_heads:
        reasons.append("DEPENDENCY_HEAD_CHANGED")
    return {
        "evidence_id": evidence["evidence_id"],
        "current": not reasons,
        "reasons": reasons,
    }


def replay_plan(
    *,
    required_method_ids: set[str],
    method_material_inputs: dict[str, set[str]],
    method_rerun_policy: dict[str, str],
    changed_inputs: set[str] | None,
) -> dict[str, Any]:
    if changed_inputs is None:
        return {
            "mode": "CONSERVATIVE_FULL_REQUIRED_SET",
            "rerun_method_ids": sorted(required_method_ids),
        }

    rerun: set[str] = set()
    for method_id in required_method_ids:
        policy = method_rerun_policy.get(method_id)
        if policy == "FULL_REQUIRED_SET":
            return {
                "mode": "FULL_REQUIRED_SET",
                "rerun_method_ids": sorted(required_method_ids),
            }
        if policy != "DECLARED_MATERIAL_INPUTS":
            return {
                "mode": "CONSERVATIVE_FULL_REQUIRED_SET",
                "rerun_method_ids": sorted(required_method_ids),
            }
        inputs = method_material_inputs.get(method_id)
        if inputs is None:
            return {
                "mode": "CONSERVATIVE_FULL_REQUIRED_SET",
                "rerun_method_ids": sorted(required_method_ids),
            }
        if inputs & changed_inputs:
            rerun.add(method_id)

    return {
        "mode": "SELECTIVE_DECLARED_INPUTS",
        "rerun_method_ids": sorted(rerun),
    }
