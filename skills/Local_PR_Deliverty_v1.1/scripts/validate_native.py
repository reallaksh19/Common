#!/usr/bin/env python3
"""Native Local v1.1 validation adapter over the established validator.

Native `TASK(kind=RESPONSIBILITY)` / Acceptance Epoch / Acceptance Profile records
remain the stored authority. This adapter validates those native facts, builds an
in-memory CHILD-compatible validation view, delegates substantive acceptance and
pipeline checking to `validate.py`, then applies native-only postconditions.

It does NOT create a second acceptance engine and never mutates the supplied bundle.
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import validate as legacy
from acceptance_basis import canonical_digest, validate_profile
from responsibility import validate_native_release
from role_transition import transition_contract

NATIVE_SUPPORT_KEYS = {
    "acceptance_epochs",
    "acceptance_profiles",
    "authority_grants",
    "role_transitions",
}
TRUSTED_GRANT_SOURCES = {"GITHUB_PROVIDER", "DIRECT_OWNER_SESSION", "OTHER_AUTHENTICATED_PROVIDER"}
TRUSTED_AUTH = {"AUTHENTICATED", "OBSERVED_TRUSTED_PROVIDER"}


class NativeValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise NativeValidationError(message)


def instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp needs timezone")
    return parsed.astimezone(timezone.utc)


def _index(records: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    require(isinstance(records, list), label + " must be an array")
    values = [record[key] for record in records]
    require(len(values) == len(set(values)), "Duplicate " + label + " identity")
    return {record[key]: record for record in records}


def _native_support(bundle: dict[str, Any]) -> dict[str, Any]:
    support = bundle.get("native_support")
    require(isinstance(support, dict) and set(support) == NATIVE_SUPPORT_KEYS, "native_support needs acceptance_epochs, acceptance_profiles, authority_grants and role_transitions only")
    return support


def _protocol_for_task(bundle: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    matches = [
        protocol for protocol in bundle["support"]["project_protocols"]
        if protocol["source_ref"] == task["project_protocol_ref"]
        and protocol["digest"] == task["project_protocol_digest"]
    ]
    require(len(matches) == 1, "Native TASK project protocol does not resolve uniquely")
    return matches[0]


def _criteria(protocol: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = {}
    for acceptance_set in protocol["acceptance_sets"]:
        for criterion in acceptance_set["criteria"]:
            require(criterion["id"] not in rows, "Duplicate project criterion")
            rows[criterion["id"]] = criterion
    return rows


def _derive_acceptance(profile: dict[str, Any], protocol: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = _criteria(protocol)
    derived = []
    for criterion_id in profile["criterion_refs"]:
        criterion = by_id[criterion_id]
        derived.append({
            "id": criterion_id,
            "requirement": f"Acceptance Profile {profile['profile_id']} criterion {criterion_id}",
            "required": criterion["required"],
            "verification_method_ids": list(criterion["verification_method_ids"]),
            "super_review_required": criterion["super_review_required"],
        })
    return derived


def _validate_grants(parent: dict[str, Any], grants: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index = {}
    for grant in grants:
        legacy.validate_against_schema(grant, "authority-grant")
        require(grant["grant_id"] not in index, "Duplicate authority grant ID")
        require(grant["issued_by"] in parent["owner_principals"], "Authority grant was not issued by an authorized Owner")
        require(grant["source_kind"] in TRUSTED_GRANT_SOURCES, "Authority grant source is untrusted")
        require(grant["authentication_status"] in TRUSTED_AUTH, "Authority grant authentication is untrusted")
        index[grant["grant_id"]] = grant
    declared = set(parent.get("control_plane", {}).get("authority_grant_refs", []))
    require(declared <= set(index), "Parent control plane references missing authority grant")
    return index


def _validate_native_basis(bundle: dict[str, Any], native: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    parents = [task for task in bundle["tasks"] if task["kind"] == "PARENT"]
    require(len(parents) == 1, "Native validation requires exactly one Parent TASK")
    parent = parents[0]
    require(parent.get("control_plane"), "Native validation requires Parent TASK control_plane")
    require(parent["control_plane"]["bootstrap_state"] == "ESTABLISHED", "Parent control plane bootstrap is not established")

    epochs = _index(native["acceptance_epochs"], "epoch_id", "acceptance epoch")
    profiles = _index(native["acceptance_profiles"], "profile_id", "acceptance profile")
    grants = _validate_grants(parent, native["authority_grants"])

    for epoch in epochs.values():
        legacy.validate_against_schema(epoch, "acceptance-epoch")
        require(epoch["digest"] == canonical_digest(epoch), "Acceptance Epoch digest mismatch")
        require(epoch["parent_task_id"] == parent["task_id"], "Acceptance Epoch belongs to another Parent TASK")

    registry = {row["epoch_id"]: row for row in parent["control_plane"]["acceptance_basis_registry"]}
    require(len(registry) == len(parent["control_plane"]["acceptance_basis_registry"]), "Duplicate Parent acceptance-basis registry epoch")
    current_epoch = parent["control_plane"]["current_acceptance_epoch_id"]
    require(current_epoch in epochs and current_epoch in registry, "Parent current acceptance epoch does not resolve")
    require(registry[current_epoch]["epoch_digest"] == epochs[current_epoch]["digest"], "Parent current acceptance epoch digest differs from native epoch")

    for profile in profiles.values():
        legacy.validate_against_schema(profile, "acceptance-profile")

    native_tasks = [task for task in bundle["tasks"] if task["kind"] == "RESPONSIBILITY"]
    require(native_tasks, "Native validation requires at least one RESPONSIBILITY TASK")
    for task in native_tasks:
        legacy.schema_check(task)
        require(task["acceptance"] == [], "Native RESPONSIBILITY TASK must not carry a second acceptance denominator")
        try:
            validate_native_release(parent, task)
        except Exception as error:
            raise NativeValidationError(str(error)) from error
        require(task["acceptance_epoch_id"] == current_epoch, "Responsibility is not bound to Parent current acceptance epoch")
        epoch = epochs.get(task["acceptance_epoch_id"])
        require(epoch is not None, "Responsibility acceptance epoch is missing")
        profile = profiles.get(task["acceptance_profile_ref"])
        require(profile is not None, "Responsibility Acceptance Profile ref does not resolve")
        require(profile["task_id"] == task["task_id"], "Acceptance Profile belongs to another responsibility")
        require(profile["digest"] == task["acceptance_profile_digest"], "Responsibility Acceptance Profile digest mismatch")
        protocol = _protocol_for_task(bundle, task)
        require(epoch["project_protocol_ref"] == task["project_protocol_ref"], "Acceptance Epoch project protocol ref differs from TASK")
        require(epoch["project_protocol_digest"] == task["project_protocol_digest"], "Acceptance Epoch project protocol digest differs from TASK")
        try:
            validate_profile(profile, protocol, epoch)
        except Exception as error:
            raise NativeValidationError(str(error)) from error
        applicable_gate_ids = {
            gate["id"] for gate in protocol["external_gates"]
            if gate["applies_to"] in {"CHILD", "ALL"}
        }
        require(
            set(profile["external_gate_ids"]) == applicable_gate_ids,
            "Native adapter refuses ambiguous external-gate projection; profile external_gate_ids must exactly name currently applicable project gates",
        )

    return epochs, profiles, grants


def _alias(role: str, principal: str) -> str:
    effective = "COORDINATOR" if role == "PARENT_CHECK" else role
    return f"__LOCAL_VALIDATION_ROLE__::{effective}::{principal}"


def _transition_index(native: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = {}
    for transition in native["role_transitions"]:
        legacy.validate_against_schema(transition, "role-transition")
        key = (transition["previous_record_id"], transition["next_record_id"])
        require(key not in rows, "Duplicate ROLE_TRANSITION boundary")
        rows[key] = transition
    return rows


def _validate_role_transitions(bundle: dict[str, Any], native: dict[str, Any], grants: dict[str, dict[str, Any]]) -> dict[str, Any]:
    parent = next(task for task in bundle["tasks"] if task["kind"] == "PARENT")
    tasks = {task["task_id"]: task for task in bundle["tasks"]}
    transitions = _transition_index(native)
    used = set()
    collapse_count = 0

    by_task: dict[str, list[dict[str, Any]]] = {}
    for stage in bundle["stages"]:
        if tasks[stage["task_id"]]["kind"] == "RESPONSIBILITY" and stage["stage"] in {"CODER", "REVIEWER", "COORDINATOR"}:
            by_task.setdefault(stage["task_id"], []).append(stage)

    for task_id, rows in by_task.items():
        task = tasks[task_id]
        ordered = sorted(rows, key=lambda row: instant(row["started_at"]))
        for previous, current in zip(ordered, ordered[1:]):
            if previous["stage"] == current["stage"]:
                continue
            same_principal = previous["executor"] == current["executor"]
            transition = transitions.get((previous["record_id"], current["record_id"]))
            if not same_principal:
                if transition:
                    used.add(transition["transition_id"])
                continue
            require(transition is not None, "Same-principal role boundary lacks durable ROLE_TRANSITION evidence")
            used.add(transition["transition_id"])
            collapse_count += 1
            require(transition["task_id"] == task_id, "ROLE_TRANSITION targets wrong responsibility")
            require(previous["publications"]["end"] is not None, "Same-principal boundary lacks previous END publication")
            require(transition["previous_end_ref"] == previous["publications"]["end"]["comment_ref"], "ROLE_TRANSITION previous END ref mismatch")
            require(transition["next_start_ref"] == current["publications"]["start"]["comment_ref"], "ROLE_TRANSITION next START ref mismatch")
            require(transition["next_context_start_ref"] == current["context_start_ref"], "ROLE_TRANSITION fresh reconstruction ref mismatch")
            require(set(transition["fresh_replay_evidence_refs"]) <= set(current["evidence_refs"]), "ROLE_TRANSITION replay evidence is not from the new role attempt")
            require(transition["fresh_replay_evidence_refs"], "ROLE_TRANSITION needs fresh role replay evidence")
            at = instant(transition["transition_at"])
            require(instant(previous["publications"]["end"]["published_at"]) <= at <= instant(current["started_at"]), "ROLE_TRANSITION timestamp is outside stage boundary")
            try:
                contract = transition_contract(
                    parent_task_id=parent["task_id"],
                    task=task,
                    previous_stage=previous["stage"],
                    previous_executor=previous["executor"],
                    next_stage=current["stage"],
                    next_executor=current["executor"],
                    grants=list(grants.values()),
                    at=at,
                    previous_end_published=True,
                    previous_timer_stopped=bool(transition["previous_timer_stop_ref"]),
                    fresh_start_published=True,
                    fresh_timer_armed=bool(transition["next_timer_arm_ref"]),
                    fresh_reconstruction=True,
                    fresh_role_replay=True,
                )
            except Exception as error:
                raise NativeValidationError(str(error)) from error
            require(contract["role_execution_grant_ref"] == transition["role_execution_grant_ref"], "ROLE_TRANSITION grant ref differs from active ROLE_EXECUTION authority")
            require(contract["principal_independence"] == "DEGRADED", "Same-principal transition must record degraded principal independence")

    unused = {row["transition_id"] for row in transitions.values()} - used
    require(not unused, "ROLE_TRANSITION record does not correspond to an actual stage boundary: " + ", ".join(sorted(unused)))
    return {"same_principal_collapses": collapse_count, "transition_records_used": sorted(used)}


def _readdress_leases(view: dict[str, Any]) -> None:
    mapping = {}
    for lease in view["support"]["review_leases"]:
        role = "COORDINATOR" if lease["certifier_role"] == "PARENT_CHECK" else lease["certifier_role"]
        lease["certifier_principal"] = _alias(role, lease["certifier_principal"])
        old = lease["lease_id"]
        lease["lease_id"] = "sha256:" + legacy.canonical_digest(lease, ("lease_id",))
        mapping[old] = lease["lease_id"]
    if not mapping:
        return
    for stage in view["stages"]:
        if stage.get("review_lease_ref") in mapping:
            stage["review_lease_ref"] = mapping[stage["review_lease_ref"]]
    for result in view["results"]:
        if result.get("review_lease_ref") in mapping:
            result["review_lease_ref"] = mapping[result["review_lease_ref"]]
    for evidence in view["support"]["evidence_records"]:
        if evidence.get("review_lease_ref") in mapping:
            evidence["review_lease_ref"] = mapping[evidence["review_lease_ref"]]
    for waiver in view["support"]["waivers"]:
        if waiver.get("lease_id") in mapping:
            waiver["lease_id"] = mapping[waiver["lease_id"]]


def _project_validation_view(bundle: dict[str, Any], profiles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    view = copy.deepcopy({key: value for key, value in bundle.items() if key != "native_support"})
    tasks = {task["task_id"]: task for task in view["tasks"]}
    native_ids = {task_id for task_id, task in tasks.items() if task["kind"] == "RESPONSIBILITY"}
    parent = next(task for task in view["tasks"] if task["kind"] == "PARENT")

    # Role-specific aliases let the established legacy validator continue enforcing
    # stage separation while native transition evidence separately proves any
    # Owner-authorized principal collapse. Aliases exist only in this deep copy.
    original_parent_owner = parent["parent_owner"]
    parent["parent_owner"] = _alias("COORDINATOR", original_parent_owner)
    parent.pop("control_plane", None)

    for task in view["tasks"]:
        original_parent = task["parent_owner"]
        task["parent_owner"] = _alias("COORDINATOR", original_parent)
        task["role_principals"] = {
            role: [_alias(role, principal) for principal in principals]
            for role, principals in task["role_principals"].items()
        }
        if task["task_id"] in native_ids:
            original = next(row for row in bundle["tasks"] if row["task_id"] == task["task_id"])
            protocol = _protocol_for_task(bundle, original)
            profile = profiles[original["acceptance_profile_ref"]]
            task["kind"] = "CHILD"
            task["acceptance"] = _derive_acceptance(profile, protocol)
            task["children"] = []
            for field in ("representation", "acceptance_epoch_id", "acceptance_profile_ref", "acceptance_profile_digest"):
                task.pop(field, None)

    for permission in parent.get("start_permissions", []):
        permission["coordinator"] = _alias("COORDINATOR", permission["coordinator"])

    for stage in view["stages"]:
        role = "COORDINATOR" if stage["stage"] == "PARENT_CHECK" else stage["stage"]
        stage["executor"] = _alias(role, stage["executor"])
        stage["role_integrity"]["principal"] = stage["executor"]

    for evidence in view["support"]["evidence_records"]:
        role = "COORDINATOR" if evidence["collected_by_role"] == "PARENT_CHECK" else evidence["collected_by_role"]
        evidence["collected_by_principal"] = _alias(role, evidence["collected_by_principal"])
        if evidence["origin_kind"] == "STAGE_EXECUTOR":
            evidence["origin_principal"] = _alias(role, evidence["origin_principal"])

    _readdress_leases(view)

    for result in view["results"]:
        if result["task_id"] in native_ids and result["kind"] == "RESPONSIBILITY":
            result["kind"] = "CHILD"

    return view


def _validate_native_lease_bindings(bundle: dict[str, Any]) -> None:
    tasks = {task["task_id"]: task for task in bundle["tasks"] if task["kind"] == "RESPONSIBILITY"}
    stages = {stage["record_id"]: stage for stage in bundle["stages"]}
    for lease in bundle["support"]["review_leases"]:
        task = tasks.get(lease["task_id"])
        if task is None:
            continue
        stage = stages.get(lease["stage_record_id"])
        require(stage is not None, "Native review lease references missing stage")
        require(lease.get("acceptance_epoch_id") == task["acceptance_epoch_id"], "Native review lease acceptance epoch is stale")
        require(lease.get("acceptance_profile_digest") == task["acceptance_profile_digest"], "Native review lease acceptance profile digest is stale")
        require(lease["certifier_principal"] == stage["executor"], "Native review lease certifier principal differs from actual stage executor")


def validate_native_bundle(bundle: dict[str, Any], now: str | datetime | None = None) -> dict[str, Any]:
    require(isinstance(bundle, dict), "Native bundle must be an object")
    require(set(bundle) == {"tasks", "stages", "results", "observed", "support", "native_support"}, "Native bundle needs tasks, stages, results, observed, support and native_support only")
    source_snapshot = json.dumps(bundle, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    native = _native_support(bundle)
    epochs, profiles, grants = _validate_native_basis(bundle, native)
    for result in bundle["results"]:
        legacy.schema_check(result)
    _validate_native_lease_bindings(bundle)
    transition_summary = _validate_role_transitions(bundle, native, grants)
    view = _project_validation_view(bundle, profiles)
    try:
        delegated = legacy.validate_bundle(view, now)
    except Exception as error:
        raise NativeValidationError(str(error)) from error
    require(source_snapshot == json.dumps(bundle, sort_keys=True, separators=(",", ":"), ensure_ascii=False), "Native validation mutated source truth")
    return {
        **delegated,
        "native_projection": "PASS",
        "native_responsibility_ids": sorted(task["task_id"] for task in bundle["tasks"] if task["kind"] == "RESPONSIBILITY"),
        "acceptance_epoch_ids": sorted(epochs),
        "acceptance_profile_ids": sorted(profiles),
        "role_transition_summary": transition_summary,
        "projection_mutated_source": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--now")
    args = parser.parse_args()
    try:
        result = validate_native_bundle(json.loads(args.bundle.read_text(encoding="utf-8-sig")), args.now)
        print(json.dumps(result, indent=2))
        return 0
    except (NativeValidationError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"record_consistency": "FAIL", "reason": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
