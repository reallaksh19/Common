#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from handover_projection import render as render_handover
from intelligence_projection import build_improvement, build_task
from lease_admission import build_native_lease
from material_basis import inspect as inspect_material_basis
from local_execution_projection import build as build_local_execution
from render_local_execution_request import render as render_local_execution_request
from relay_can import _protocol_state, evaluate as can_action
from snapshot_projection import build as build_snapshot
from transactionlib import TransactionError, execute, jsonl_bytes, recover_all, yaml_bytes
from v3lib import canonical_digest, load_events, load_yaml, require_identifier, validate_schema
from validate_foundation import validate_authority


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _authority(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = validate_authority(root)
    if errors:
        raise TransactionError("invalid V3 authority: " + "; ".join(errors[:8]))
    state = load_yaml(root / "relay/STATE.yaml")
    controls = load_yaml(root / str((state.get("controls") or {}).get("path")))
    return state, controls


def _events(root: Path) -> list[dict[str, Any]]:
    events, errors = load_events(root / "relay/EVENTS.jsonl")
    if errors:
        raise TransactionError("invalid event history: " + "; ".join(errors[:8]))
    return events


def _event(event_id: str, event_type: str, actor: str, subject: str, basis: list[str], details: dict[str, Any]) -> dict[str, Any]:
    value = {
        "schema_version": "relay-v3.1-event",
        "event_id": event_id,
        "type": event_type,
        "timestamp": _now(),
        "actor": actor,
        "subject": subject,
        "basis": basis,
        "details": details,
    }
    errors = validate_schema("event", value, "EVENT")
    if errors:
        raise TransactionError("; ".join(errors))
    return value


def _assert_event_ids_available(events: list[dict[str, Any]], event_ids: list[str]) -> None:
    existing = {str(item.get("event_id")) for item in events}
    duplicates = sorted(set(event_ids) & existing)
    if duplicates:
        raise TransactionError(f"duplicate event id(s): {', '.join(duplicates)}")
    if len(event_ids) != len(set(event_ids)):
        raise TransactionError("transaction event ids must be unique")


def _snapshot_path(state: dict[str, Any]) -> str:
    value = str((state.get("generated") or {}).get("snapshot") or "")
    if not value:
        raise TransactionError("STATE.generated.snapshot must be explicit")
    return value


def _require_action(
    root: Path,
    action: str,
    *,
    path: str | None = None,
    base_ref: str | None = None,
) -> None:
    result = can_action(root, action, path=path, base_ref=base_ref)
    if not result["allowed"]:
        raise TransactionError(f"{action} denied: {', '.join(result['reason_codes'])}")


def _current_checkpoint(root: Path, state: dict[str, Any]) -> dict[str, Any] | None:
    cp_id = (state.get("accepted") or {}).get("checkpoint")
    return load_yaml(root / "relay/CHECKPOINTS" / f"{cp_id}.yaml") if cp_id else None


def _current_ep(root: Path, state: dict[str, Any]) -> dict[str, Any] | None:
    ep_id = (state.get("execution") or {}).get("ep")
    return load_yaml(root / "relay/WORK" / f"{ep_id}.yaml") if ep_id else None


def _require_fresh_handover(
    root: Path,
    state: dict[str, Any],
    *,
    base_ref: str | None,
) -> str:
    context_path = root / "relay/GENERATED/HANDOVER_CONTEXT.yaml"
    if not context_path.exists():
        raise TransactionError("graceful lease release requires a fresh HANDOVER_CONTEXT")

    context = load_yaml(context_path)
    errors = validate_schema("handover-context", context, "HANDOVER_CONTEXT")
    if errors:
        raise TransactionError("; ".join(errors))

    frozen = context.get("frozen_basis") or {}
    execution = state.get("execution") or {}
    if frozen.get("lease") != execution.get("lease") or frozen.get("ep") != execution.get("ep"):
        raise TransactionError("HANDOVER_STALE: handover EP/lease does not match current execution")
    if frozen.get("state_digest") != canonical_digest(state):
        raise TransactionError("HANDOVER_STALE: handover state digest does not match current authority")

    ep = _current_ep(root, state)
    if isinstance(ep, dict):
        if not base_ref:
            raise TransactionError("graceful lease release requires --base-ref to verify handover material freshness")
        inspected = inspect_material_basis(root, ep, base_ref)["material_basis"]
        for key, frozen_key in (
            ("head", "material_head"),
            ("relevant_paths_digest", "relevant_paths_digest"),
            ("dependency_digest", "dependency_digest"),
        ):
            if inspected.get(key) != frozen.get(frozen_key):
                raise TransactionError(f"HANDOVER_STALE: {frozen_key} no longer matches current material reality")

    learning = context.get("accumulated_learning") or {}
    task_meta = learning.get("task_snapshot") or {}
    improvement_meta = learning.get("improvement_view") or {}
    task_path = root / str(task_meta.get("path") or "")
    improvement_path = root / str(improvement_meta.get("path") or "")
    if not task_path.exists() or not improvement_path.exists():
        raise TransactionError("HANDOVER_STALE: task/improvement projection is missing")
    task_snapshot = load_yaml(task_path)
    improvement_view = load_yaml(improvement_path)
    if canonical_digest(task_snapshot) != task_meta.get("digest"):
        raise TransactionError("HANDOVER_STALE: task snapshot digest changed")
    if canonical_digest(improvement_view) != improvement_meta.get("digest"):
        raise TransactionError("HANDOVER_STALE: improvement view digest changed")

    roadmap_effect = improvement_view.get("roadmap_effect") or {}
    if roadmap_effect.get("concept_change") == "UNKNOWN":
        raise TransactionError("ROADMAP_RECONCILIATION_REQUIRED before graceful lease release")

    parent_issue = task_snapshot.get("parent_issue") or {}
    if parent_issue.get("number") and parent_issue.get("disposition") == "UNKNOWN":
        raise TransactionError("PARENT_ISSUE_RECONCILIATION_REQUIRED before graceful lease release")

    digest = canonical_digest(context)
    planned = any(
        item.get("type") == "HANDOVER_PLANNED"
        and digest in (item.get("basis") or [])
        for item in _events(root)
    )
    if not planned:
        raise TransactionError("graceful lease release requires a committed HANDOVER_PLANNED event for the current context")
    return digest


def admit_task(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    admission_path: Path,
    base_ref: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    live_v3, protocol_state = _protocol_state(root)
    if not live_v3:
        raise TransactionError(f"ADMIT_TASK denied: PROTOCOL_NOT_ACTIVE ({protocol_state})")

    state, _ = _authority(root)
    execution = state.get("execution") or {}
    if execution.get("lifecycle") != "IDLE" or any(execution.get(key) for key in ("ep", "lease", "route")):
        raise TransactionError("ADMIT_TASK requires an IDLE repository with no active EP/lease/route")

    admission = load_yaml(admission_path)
    errors = validate_schema("task-admission", admission, "TASK_ADMISSION")
    if errors:
        raise TransactionError("; ".join(errors))
    ep = admission.get("ep") or {}
    errors = validate_schema("ep", ep, "EP")
    if errors:
        raise TransactionError("; ".join(errors))
    try:
        require_identifier(str(ep.get("id")), "EP-", "ep_id")
    except ValueError as exc:
        raise TransactionError(str(exc)) from exc

    roadmap_path = root / str((state.get("roadmap") or {}).get("path"))
    roadmap = load_yaml(roadmap_path)
    rplan = admission["roadmap"]
    wp = copy.deepcopy(rplan["work_package"])
    wp_id = str(wp.get("id"))
    if str(ep.get("work_package")) != wp_id:
        raise TransactionError("EP work_package must match admitted roadmap work package")
    if rplan["new_revision"] == roadmap.get("revision"):
        raise TransactionError("ADMIT_TASK requires a new roadmap revision")

    work_packages = copy.deepcopy(roadmap.get("work_packages") or [])
    existing_index = next((i for i, item in enumerate(work_packages) if str(item.get("id")) == wp_id), None)
    disposition = rplan["disposition"]
    if disposition == "ADDED_EXECUTION_WP":
        if existing_index is not None:
            raise TransactionError("ADDED_EXECUTION_WP requires a new work package id")
        work_packages.append(wp)
    elif existing_index is None:
        raise TransactionError(f"{disposition} requires an existing work package")
    elif disposition == "MAPPED_EXISTING_WP":
        existing = work_packages[existing_index]
        for key in ("id", "title", "weight", "depends_on"):
            if existing.get(key) != wp.get(key):
                raise TransactionError("MAPPED_EXISTING_WP cannot silently revise the work package contract")
        existing["state"] = "ACTIVE"
    else:
        work_packages[existing_index] = wp

    if any(item.get("state") == "ACTIVE" and item.get("id") != wp_id for item in work_packages):
        raise TransactionError("serial ADMIT_TASK cannot create a second ACTIVE work package")

    ep_path = root / "relay/WORK" / f"{ep['id']}.yaml"
    lease_spec = admission["lease"]
    lease_id = str(lease_spec["id"])
    lease_path = root / "relay/LEASES" / f"{lease_id}.yaml"
    if ep_path.exists() or lease_path.exists():
        raise TransactionError("ADMIT_TASK refuses to overwrite an existing EP or lease")

    new_roadmap = copy.deepcopy(roadmap)
    new_roadmap["revision"] = rplan["new_revision"]
    new_roadmap["work_packages"] = work_packages

    route = f"SERIAL:{ep['id']}"
    provisional_state = copy.deepcopy(state)
    provisional_state["roadmap"]["revision"] = rplan["new_revision"]
    provisional_state["execution"] = {
        "lifecycle": "ACTIVE",
        "ep": ep["id"],
        "lease": lease_id,
        "route": route,
    }
    provisional_state["delivery"] = copy.deepcopy(admission["delivery"])

    lease = build_native_lease(
        root,
        lease_id=lease_id,
        executor_id=lease_spec["executor_id"],
        method=lease_spec["method"],
        qualification=lease_spec.get("qualification"),
        owner_basis=lease_spec.get("owner_basis"),
        branch=lease_spec.get("branch"),
        state_override=provisional_state,
        ep_override=ep,
        current_lease_override=None,
    )
    snapshot = build_snapshot(
        root,
        base_ref,
        state_override=provisional_state,
        roadmap_override=new_roadmap,
        ep_override=ep,
        lease_override=lease,
    )

    events = _events(root)
    ids = [event_id + "-OWNER", event_id + "-EP", event_id + "-LEASE"]
    _assert_event_ids_available(events, ids)
    events.extend([
        _event(ids[0], "OWNER_TASK_ADMITTED", actor, wp_id, [tx_id, disposition, *rplan["basis"]], {"roadmap_revision": rplan["new_revision"]}),
        _event(ids[1], "EP_CREATED", actor, ep["id"], [tx_id, wp_id, str((ep.get("basis") or {}).get("protocol_basis"))], {}),
        _event(ids[2], "LEASE_GRANTED", actor, lease_id, [tx_id, route], {"executor": lease_spec["executor_id"], "method": lease_spec["method"]}),
    ])

    return execute(
        root,
        tx_id=tx_id,
        command="ADMIT_TASK",
        actor=actor,
        replacements={
            str((state.get("roadmap") or {}).get("path")): yaml_bytes(new_roadmap),
            "relay/STATE.yaml": yaml_bytes(provisional_state),
            f"relay/WORK/{ep['id']}.yaml": yaml_bytes(ep),
            f"relay/LEASES/{lease_id}.yaml": yaml_bytes(lease),
            _snapshot_path(provisional_state): yaml_bytes(snapshot),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def activate_lease(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    lease_id: str,
    executor_id: str,
    actor: str,
    method: str,
    qualification: dict[str, Any] | None,
    owner_basis: dict[str, str] | None,
    branch: str | None,
    base_ref: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, _ = _authority(root)
    try:
        require_identifier(lease_id, "LEASE-", "lease_id")
    except ValueError as exc:
        raise TransactionError(str(exc)) from exc
    old_lease_id = (state.get("execution") or {}).get("lease")
    old_lease = load_yaml(root / "relay/LEASES" / f"{old_lease_id}.yaml") if old_lease_id else None
    if old_lease_id == lease_id:
        raise TransactionError("new lease id must differ from the current lease id")
    new_lease_path = root / "relay/LEASES" / f"{lease_id}.yaml"
    if new_lease_path.exists():
        raise TransactionError(f"new lease id already exists: {lease_id}")

    transfer_from = (
        str(old_lease_id)
        if isinstance(old_lease, dict)
        and old_lease.get("state") == "ACTIVE"
        and ((old_lease.get("executor") or {}).get("id") != executor_id)
        else None
    )
    new_lease = build_native_lease(
        root,
        lease_id=lease_id,
        executor_id=executor_id,
        method=method,
        qualification=qualification,
        owner_basis=owner_basis,
        branch=branch,
        replace_active_lease_id=transfer_from,
    )

    replacements: dict[str, bytes] = {}
    transfer = bool(old_lease and old_lease_id != lease_id and old_lease.get("state") == "ACTIVE")
    if transfer:
        released = copy.deepcopy(old_lease)
        released["state"] = "RELEASED"
        replacements[f"relay/LEASES/{old_lease_id}.yaml"] = yaml_bytes(released)

    new_state = copy.deepcopy(state)
    new_state["execution"] = {
        "lifecycle": "ACTIVE",
        "ep": (new_lease.get("basis") or {}).get("ep_id"),
        "lease": lease_id,
        "route": new_lease.get("route"),
    }
    replacements[f"relay/LEASES/{lease_id}.yaml"] = yaml_bytes(new_lease)
    replacements["relay/STATE.yaml"] = yaml_bytes(new_state)
    snapshot = build_snapshot(root, base_ref, state_override=new_state, lease_override=new_lease)
    replacements[_snapshot_path(new_state)] = yaml_bytes(snapshot)

    events = _events(root)
    release_event_id = event_id + "-REL" if transfer else None
    _assert_event_ids_available(events, [x for x in [release_event_id, event_id] if x])
    if transfer:
        events.append(_event(
            str(release_event_id),
            "LEASE_RELEASED",
            actor,
            str(old_lease_id),
            [tx_id, f"transfer-to:{lease_id}"],
            {"successor_lease": lease_id},
        ))
    events.append(_event(
        event_id,
        "LEASE_GRANTED",
        actor,
        lease_id,
        [tx_id, str(new_lease.get("route"))],
        {"executor": executor_id, "method": method},
    ))
    replacements["relay/EVENTS.jsonl"] = jsonl_bytes(events)

    return execute(root, tx_id=tx_id, command="ACTIVATE_LEASE", actor=actor, replacements=replacements, fail_after=fail_after)


def release_lease(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    reason: str = "HANDOFF",
    base_ref: str | None = None,
    fail_after: int | None = None,
) -> dict[str, Any]:
    if reason not in {"HANDOFF", "ADMINISTRATIVE"}:
        raise TransactionError("lease release reason must be HANDOFF or ADMINISTRATIVE")

    state, _ = _authority(root)
    execution = state.get("execution") or {}
    lease_id = execution.get("lease")
    if not lease_id:
        raise TransactionError("no active lease to release")
    lease_path = root / "relay/LEASES" / f"{lease_id}.yaml"
    lease = load_yaml(lease_path)
    if lease.get("state") != "ACTIVE":
        raise TransactionError("current lease is not ACTIVE")

    handover_digest = None
    if reason == "HANDOFF":
        handover_digest = _require_fresh_handover(root, state, base_ref=base_ref)

    released = copy.deepcopy(lease)
    released["state"] = "RELEASED"
    new_state = copy.deepcopy(state)
    new_state["execution"] = {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None}
    snapshot = build_snapshot(root, state_override=new_state)

    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    basis = [tx_id, f"reason:{reason}"]
    if handover_digest:
        basis.append(handover_digest)
    events.append(_event(
        event_id,
        "LEASE_RELEASED",
        actor,
        str(lease_id),
        basis,
        {
            "reason": reason,
            "graceful": reason == "HANDOFF",
            "handover_context_digest": handover_digest,
        },
    ))

    return execute(
        root,
        tx_id=tx_id,
        command="RELEASE_LEASE",
        actor=actor,
        replacements={
            f"relay/LEASES/{lease_id}.yaml": yaml_bytes(released),
            "relay/STATE.yaml": yaml_bytes(new_state),
            _snapshot_path(new_state): yaml_bytes(snapshot),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def accept_checkpoint(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    checkpoint_path: Path,
    base_ref: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    _require_action(root, "CHECKPOINT", base_ref=base_ref)
    state, _ = _authority(root)
    checkpoint = load_yaml(checkpoint_path)
    errors = validate_schema("checkpoint", checkpoint, "CHECKPOINT")
    if errors:
        raise TransactionError("; ".join(errors))
    if any(item.get("result") != "PASS" for item in checkpoint.get("acceptance") or []):
        raise TransactionError("checkpoint acceptance requires every criterion PASS")
    if (checkpoint.get("quality") or {}).get("result") != "CLEAR":
        raise TransactionError("checkpoint acceptance requires quality CLEAR")
    validation = checkpoint.get("validation") or {}
    if any(value == "FAIL" for value in validation.values()):
        raise TransactionError("checkpoint acceptance cannot contain failed validation")
    active_ep = (state.get("execution") or {}).get("ep")
    if active_ep and checkpoint.get("ep") != active_ep:
        raise TransactionError("checkpoint EP does not match active execution EP")
    ep = _current_ep(root, state)
    if not isinstance(ep, dict):
        raise TransactionError("checkpoint acceptance requires the current authoritative EP")

    expected_ac_ids = [str(item.get("id")) for item in ep.get("acceptance") or []]
    observed_ac_ids = [str(item.get("id")) for item in checkpoint.get("acceptance") or []]
    if len(observed_ac_ids) != len(set(observed_ac_ids)):
        raise TransactionError("checkpoint acceptance contains duplicate criterion ids")
    if set(observed_ac_ids) != set(expected_ac_ids) or len(observed_ac_ids) != len(expected_ac_ids):
        raise TransactionError("checkpoint acceptance ids must exactly match the current EP acceptance contract")

    expected_quality = str((ep.get("quality_policy") or {}).get("level") or "")
    if (checkpoint.get("quality") or {}).get("policy") != expected_quality:
        raise TransactionError("checkpoint quality policy must match the current EP quality policy")

    material = inspect_material_basis(root, ep, base_ref)
    current_material = material["material_basis"]
    observed_material = checkpoint.get("material_result") or {}
    for key in ("head", "relevant_paths_digest", "dependency_digest"):
        if observed_material.get(key) != current_material.get(key):
            raise TransactionError(
                f"checkpoint material_result.{key} does not match current material basis"
            )

    cp_id = str(checkpoint.get("id"))
    target = f"relay/CHECKPOINTS/{cp_id}.yaml"
    if (root / target).exists():
        raise TransactionError(f"checkpoint id already exists and is immutable: {cp_id}")
    new_state = copy.deepcopy(state)
    new_state["accepted"]["checkpoint"] = cp_id
    snapshot = build_snapshot(root, base_ref, state_override=new_state, checkpoint_override=checkpoint)

    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "CHECKPOINT_ACCEPTED",
        actor,
        cp_id,
        [tx_id, str(checkpoint.get("ep"))],
        {"material_head": (checkpoint.get("material_result") or {}).get("head")},
    ))

    return execute(
        root,
        tx_id=tx_id,
        command="ACCEPT_CHECKPOINT",
        actor=actor,
        replacements={
            target: yaml_bytes(checkpoint),
            "relay/STATE.yaml": yaml_bytes(new_state),
            _snapshot_path(new_state): yaml_bytes(snapshot),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def resolve_control(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    control_id: str,
    evidence: list[str],
    base_ref: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, controls = _authority(root)
    matches = [item for item in controls.get("controls") or [] if item.get("id") == control_id]
    if len(matches) != 1:
        raise TransactionError(f"expected one control {control_id}; found {len(matches)}")
    item = matches[0]
    if item.get("state") != "OPEN":
        raise TransactionError(f"control {control_id} is not OPEN")
    evidence = [str(item).strip() for item in evidence if str(item).strip()]
    if not evidence:
        raise TransactionError("control resolution requires durable evidence")

    new_controls = copy.deepcopy(controls)
    for row in new_controls["controls"]:
        if row.get("id") == control_id:
            row["state"] = "RESOLVED"
            row["resolution"]["evidence"] = list(evidence)

    snapshot = build_snapshot(root, base_ref, controls_override=new_controls)
    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(event_id, "CONTROL_RESOLVED", actor, control_id, [tx_id, *evidence], {}))
    controls_path = str((state.get("controls") or {}).get("path"))

    return execute(
        root,
        tx_id=tx_id,
        command="RESOLVE_CONTROL",
        actor=actor,
        replacements={
            controls_path: yaml_bytes(new_controls),
            _snapshot_path(state): yaml_bytes(snapshot),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def reconcile_roadmap(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    reconciliation_path: Path,
    base_ref: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, _ = _authority(root)
    roadmap_path = str((state.get("roadmap") or {}).get("path"))
    current = load_yaml(root / roadmap_path)

    reconciliation = load_yaml(reconciliation_path)
    errors = validate_schema("roadmap-reconciliation", reconciliation, "ROADMAP_RECONCILIATION")
    if errors:
        raise TransactionError("; ".join(errors))
    if reconciliation.get("expected_revision") != current.get("revision"):
        raise TransactionError("roadmap reconciliation expected_revision does not match current ROADMAP")

    after = reconciliation.get("roadmap_after") or {}
    errors = validate_schema("roadmap", after, "ROADMAP_AFTER")
    if errors:
        raise TransactionError("; ".join(errors))

    disposition = str(reconciliation.get("disposition") or "")
    if disposition in {"NO_CHANGE", "OWNER_DECISION_REQUIRED"}:
        if canonical_digest(after) != canonical_digest(current):
            raise TransactionError(f"{disposition} cannot mutate ROADMAP")
    elif after.get("revision") == current.get("revision"):
        raise TransactionError("a roadmap-changing reconciliation requires a new ROADMAP revision")

    ep = _current_ep(root, state)
    if isinstance(ep, dict):
        work_package = str(ep.get("work_package") or "")
        after_ids = {str(row.get("id")) for row in after.get("work_packages") or [] if isinstance(row, dict)}
        if work_package and work_package not in after_ids:
            raise TransactionError("roadmap reconciliation cannot orphan the current EP work package")

    new_state = copy.deepcopy(state)
    new_state["roadmap"]["revision"] = after.get("revision")
    snapshot = build_snapshot(
        root,
        base_ref,
        state_override=new_state,
        roadmap_override=after,
        ep_override=ep,
    )

    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "ROADMAP_RECONCILED",
        actor,
        str(after.get("revision")),
        [tx_id, *list(reconciliation.get("basis") or [])],
        {
            "disposition": disposition,
            "from_revision": current.get("revision"),
            "to_revision": after.get("revision"),
        },
    ))

    return execute(
        root,
        tx_id=tx_id,
        command="RECONCILE_ROADMAP",
        actor=actor,
        replacements={
            roadmap_path: yaml_bytes(after),
            "relay/STATE.yaml": yaml_bytes(new_state),
            _snapshot_path(new_state): yaml_bytes(snapshot),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )

def publish_handover(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    base_ref: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    _require_action(root, "HANDOVER")
    state, _ = _authority(root)
    snapshot = build_snapshot(root, base_ref)
    checkpoint = _current_checkpoint(root, state)
    task_snapshot = build_task(root, base_ref)
    improvement_view = build_improvement(root)
    handover = render_handover(snapshot, checkpoint, task_snapshot, improvement_view).encode("utf-8")
    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "HANDOVER_PUBLISHED",
        actor,
        str((state.get("execution") or {}).get("ep") or (state.get("accepted") or {}).get("checkpoint") or "relay"),
        [tx_id, _snapshot_path(state)],
        {"artifact": "relay/GENERATED/HANDOVER.md"},
    ))
    return execute(
        root,
        tx_id=tx_id,
        command="PUBLISH_HANDOVER",
        actor=actor,
        replacements={
            _snapshot_path(state): yaml_bytes(snapshot),
            "relay/GENERATED/HANDOVER.md": handover,
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def export_local_execution(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    base_ref: str,
    mode: str = "VALIDATE_ONLY",
    fail_after: int | None = None,
) -> dict[str, Any]:
    _require_action(root, "LOCAL_EXECUTION_EXPORT")
    state, _ = _authority(root)
    snapshot = build_snapshot(root, base_ref)
    ep = _current_ep(root, state)
    checkpoint = _current_checkpoint(root, state)
    if ep is None and isinstance(checkpoint, dict) and checkpoint.get("ep"):
        ep = load_yaml(root / "relay/WORK" / f"{checkpoint['ep']}.yaml")
    package = build_local_execution(root, snapshot, ep, checkpoint, mode=mode)
    request_md = render_local_execution_request(package).encode("utf-8")
    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "LOCAL_EXECUTION_EXPORTED",
        actor,
        str((state.get("execution") or {}).get("ep") or "relay"),
        [tx_id, _snapshot_path(state)],
        {
            "artifacts": [
                "relay/GENERATED/LOCAL_EXECUTION.yaml",
                "relay/GENERATED/LOCAL_EXECUTION.md",
            ],
            "request_id": (package.get("request") or {}).get("id"),
            "mode": mode,
        },
    ))
    return execute(
        root,
        tx_id=tx_id,
        command="EXPORT_LOCAL_EXECUTION",
        actor=actor,
        replacements={
            _snapshot_path(state): yaml_bytes(snapshot),
            "relay/GENERATED/LOCAL_EXECUTION.yaml": yaml_bytes(package),
            "relay/GENERATED/LOCAL_EXECUTION.md": request_md,
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def accept_local_execution_result(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    result_path: Path,
    fail_after: int | None = None,
) -> dict[str, Any]:
    package_path = root / "relay/GENERATED/LOCAL_EXECUTION.yaml"
    if not package_path.exists():
        raise TransactionError("local execution result requires an exported LOCAL_EXECUTION package")
    package = load_yaml(package_path)
    package_errors = validate_schema("local-execution", package, "LOCAL_EXECUTION")
    if package_errors:
        raise TransactionError("; ".join(package_errors))

    result = load_yaml(result_path)
    result_errors = validate_schema("local-execution-result", result, "LOCAL_EXECUTION_RESULT")
    if result_errors:
        raise TransactionError("; ".join(result_errors))

    request = package.get("request") or {}
    if result.get("request_id") != request.get("id"):
        raise TransactionError("local execution result request_id does not match the active exported request")

    required_head = str(((request.get("exact_basis") or {}).get("material_head")) or "")
    observed_head = str(result.get("observed_head") or "")
    status = str(result.get("status") or "")
    if status == "HEAD_MISMATCH":
        if observed_head == required_head:
            raise TransactionError("HEAD_MISMATCH result must report a different observed_head")
    elif observed_head != required_head:
        raise TransactionError("local execution result observed_head does not match the exported exact basis")

    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "LOCAL_EXECUTION_RETURNED",
        actor,
        str(request.get("id")),
        [tx_id, str(request.get("id")), str((package.get("generated_from") or {}).get("snapshot_digest"))],
        {
            "status": status,
            "observed_head": observed_head,
            "required_head": required_head,
        },
    ))

    return execute(
        root,
        tx_id=tx_id,
        command="IMPORT_LOCAL_EXECUTION_RESULT",
        actor=actor,
        replacements={
            "relay/GENERATED/LOCAL_EXECUTION_RESULT.yaml": yaml_bytes(result),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )

def sync_delivery(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    observation_path: Path,
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, _ = _authority(root)
    delivery = state.get("delivery") or {}
    expected = delivery.get("primary_vehicle")
    if delivery.get("required") is not True or not isinstance(expected, dict):
        raise TransactionError("STATE has no required primary delivery vehicle")
    observation = load_yaml(observation_path)
    errors = validate_schema("delivery-status", observation, "DELIVERY_STATUS")
    if errors:
        raise TransactionError("; ".join(errors))
    if observation.get("vehicle") != expected:
        raise TransactionError("provider readback vehicle does not match STATE.delivery.primary_vehicle")
    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "DELIVERY_SYNCED",
        actor,
        f"{expected.get('kind')}:{expected.get('number')}",
        [tx_id, str(observation.get("provider_ref"))],
        {"lifecycle": observation.get("lifecycle")},
    ))
    return execute(
        root,
        tx_id=tx_id,
        command="SYNC_DELIVERY",
        actor=actor,
        replacements={
            "relay/GENERATED/DELIVERY_STATUS.yaml": yaml_bytes(observation),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def close_task(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    fail_after: int | None = None,
) -> dict[str, Any]:
    _require_action(root, "CLOSE_TASK")
    state, _ = _authority(root)
    delivery = state.get("delivery") or {}
    vehicle = delivery.get("primary_vehicle")
    if delivery.get("required") is True:
        path = root / "relay/GENERATED/DELIVERY_STATUS.yaml"
        if not path.exists():
            raise TransactionError("required delivery has no provider-readback DELIVERY_STATUS")
        observed = load_yaml(path)
        errors = validate_schema("delivery-status", observed, "DELIVERY_STATUS")
        if errors:
            raise TransactionError("; ".join(errors))
        if observed.get("vehicle") != vehicle:
            raise TransactionError("DELIVERY_STATUS vehicle does not match STATE")
        if (vehicle or {}).get("kind") == "PULL_REQUEST" and observed.get("lifecycle") != "MERGED":
            raise TransactionError("pull-request delivery must be MERGED before CLOSE_TASK")
        if (vehicle or {}).get("kind") == "ISSUE" and observed.get("lifecycle") != "CLOSED":
            raise TransactionError("issue delivery must be CLOSED before CLOSE_TASK")

    execution = state.get("execution") or {}
    lease_id = execution.get("lease")
    lease = load_yaml(root / "relay/LEASES" / f"{lease_id}.yaml") if lease_id else None
    new_state = copy.deepcopy(state)
    new_state["execution"] = {"lifecycle": "TERMINAL", "ep": None, "lease": None, "route": None}
    snapshot = build_snapshot(root, state_override=new_state)

    replacements: dict[str, bytes] = {
        "relay/STATE.yaml": yaml_bytes(new_state),
        _snapshot_path(new_state): yaml_bytes(snapshot),
    }
    if lease and lease.get("state") == "ACTIVE":
        released = copy.deepcopy(lease)
        released["state"] = "RELEASED"
        replacements[f"relay/LEASES/{lease_id}.yaml"] = yaml_bytes(released)

    events = _events(root)
    release_event_id = event_id + "-REL" if lease and lease.get("state") == "ACTIVE" else None
    _assert_event_ids_available(events, [x for x in [release_event_id, event_id] if x])
    if release_event_id:
        events.append(_event(str(release_event_id), "LEASE_RELEASED", actor, str(lease_id), [tx_id, "close-task"], {}))
    events.append(_event(
        event_id,
        "TASK_CLOSED",
        actor,
        str((state.get("accepted") or {}).get("checkpoint") or "relay"),
        [tx_id],
        {"delivery_required": bool(delivery.get("required"))},
    ))
    replacements["relay/EVENTS.jsonl"] = jsonl_bytes(events)
    return execute(root, tx_id=tx_id, command="CLOSE_TASK", actor=actor, replacements=replacements, fail_after=fail_after)


def _add_start_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tx-id", required=True)
    parser.add_argument("--event-id", required=True)
    parser.add_argument("--lease-id", required=True)
    parser.add_argument("--executor-id", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--method", choices=["DETERMINISTIC", "QUALIFIED", "OWNER_OVERRIDE"], required=True)
    parser.add_argument("--qualification")
    parser.add_argument("--owner-utterance-digest")
    parser.add_argument("--owner-session-timestamp")
    parser.add_argument("--branch")
    parser.add_argument("--base-ref", required=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Engineering Relay V3.1 transactional command surface.")
    parser.add_argument("repo_root", nargs="?", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("recover")

    admit_task_parser = sub.add_parser("admit-task")
    admit_task_parser.add_argument("--tx-id", required=True)
    admit_task_parser.add_argument("--event-id", required=True)
    admit_task_parser.add_argument("--actor", required=True)
    admit_task_parser.add_argument("--admission", required=True)
    admit_task_parser.add_argument("--base-ref", required=True)

    admit = sub.add_parser("admit")
    admit.add_argument("--lease-id", required=True)
    admit.add_argument("--executor-id", required=True)
    admit.add_argument("--method", choices=["DETERMINISTIC", "QUALIFIED", "OWNER_OVERRIDE"], required=True)
    admit.add_argument("--qualification")
    admit.add_argument("--owner-utterance-digest")
    admit.add_argument("--owner-session-timestamp")
    admit.add_argument("--branch")

    start = sub.add_parser("start")
    _add_start_args(start)
    activate = sub.add_parser("activate-lease")
    _add_start_args(activate)

    release = sub.add_parser("release-lease")
    release.add_argument("--tx-id", required=True)
    release.add_argument("--event-id", required=True)
    release.add_argument("--actor", required=True)
    release.add_argument("--reason", choices=["HANDOFF", "ADMINISTRATIVE"], default="HANDOFF")
    release.add_argument("--base-ref")

    checkpoint = sub.add_parser("checkpoint")
    checkpoint.add_argument("--tx-id", required=True)
    checkpoint.add_argument("--event-id", required=True)
    checkpoint.add_argument("--actor", required=True)
    checkpoint.add_argument("--checkpoint", required=True)
    checkpoint.add_argument("--base-ref", required=True)
    accept_cp = sub.add_parser("accept-checkpoint")
    accept_cp.add_argument("--tx-id", required=True)
    accept_cp.add_argument("--event-id", required=True)
    accept_cp.add_argument("--actor", required=True)
    accept_cp.add_argument("--checkpoint", required=True)
    accept_cp.add_argument("--base-ref", required=True)

    control = sub.add_parser("resolve-control")
    control.add_argument("--tx-id", required=True)
    control.add_argument("--event-id", required=True)
    control.add_argument("--actor", required=True)
    control.add_argument("--control-id", required=True)
    control.add_argument("--evidence", action="append", default=[])
    control.add_argument("--base-ref", required=True)

    roadmap = sub.add_parser("reconcile-roadmap")
    roadmap.add_argument("--tx-id", required=True)
    roadmap.add_argument("--event-id", required=True)
    roadmap.add_argument("--actor", required=True)
    roadmap.add_argument("--reconciliation", required=True)
    roadmap.add_argument("--base-ref", required=True)

    handover = sub.add_parser("handover")
    handover.add_argument("--tx-id", required=True)
    handover.add_argument("--event-id", required=True)
    handover.add_argument("--actor", required=True)
    handover.add_argument("--base-ref", required=True)

    local = sub.add_parser("local-execution")
    local.add_argument("--tx-id", required=True)
    local.add_argument("--event-id", required=True)
    local.add_argument("--actor", required=True)
    local.add_argument("--base-ref", required=True)
    local.add_argument("--mode", choices=["VALIDATE_ONLY", "BOUNDED_EXECUTION"], default="VALIDATE_ONLY")

    local_result = sub.add_parser("local-execution-result")
    local_result.add_argument("--tx-id", required=True)
    local_result.add_argument("--event-id", required=True)
    local_result.add_argument("--actor", required=True)
    local_result.add_argument("--result", required=True)

    delivery = sub.add_parser("sync-delivery")
    delivery.add_argument("--tx-id", required=True)
    delivery.add_argument("--event-id", required=True)
    delivery.add_argument("--actor", required=True)
    delivery.add_argument("--observation", required=True)

    close = sub.add_parser("close")
    close.add_argument("--tx-id", required=True)
    close.add_argument("--event-id", required=True)
    close.add_argument("--actor", required=True)

    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if args.command == "recover":
        for result in recover_all(root):
            print(f"{result['id']}: {result['status']}")
        return

    if args.command == "admit-task":
        result = admit_task(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            admission_path=Path(args.admission),
            base_ref=args.base_ref,
        )
        print(f"{result['id']}: {result['status']}")
        return

    if args.command == "admit":
        qualification = load_yaml(Path(args.qualification)) if args.qualification else None
        owner_basis = None
        if args.method == "OWNER_OVERRIDE":
            owner_basis = {
                "direct_utterance_digest": args.owner_utterance_digest,
                "session_timestamp": args.owner_session_timestamp,
            }
        lease = build_native_lease(
            root,
            lease_id=args.lease_id,
            executor_id=args.executor_id,
            method=args.method,
            qualification=qualification,
            owner_basis=owner_basis,
            branch=args.branch,
        )
        print(yaml_bytes(lease).decode("utf-8"), end="")
        return

    if args.command in {"start", "activate-lease"}:
        qualification = load_yaml(Path(args.qualification)) if args.qualification else None
        owner_basis = None
        if args.method == "OWNER_OVERRIDE":
            owner_basis = {
                "direct_utterance_digest": args.owner_utterance_digest,
                "session_timestamp": args.owner_session_timestamp,
            }
        result = activate_lease(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            lease_id=args.lease_id,
            executor_id=args.executor_id,
            actor=args.actor,
            method=args.method,
            qualification=qualification,
            owner_basis=owner_basis,
            branch=args.branch,
            base_ref=args.base_ref,
        )
    elif args.command == "release-lease":
        result = release_lease(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            reason=args.reason,
            base_ref=args.base_ref,
        )
    elif args.command in {"checkpoint", "accept-checkpoint"}:
        result = accept_checkpoint(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            checkpoint_path=Path(args.checkpoint),
            base_ref=args.base_ref,
        )
    elif args.command == "resolve-control":
        result = resolve_control(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            control_id=args.control_id,
            evidence=args.evidence,
            base_ref=args.base_ref,
        )
    elif args.command == "reconcile-roadmap":
        result = reconcile_roadmap(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            reconciliation_path=Path(args.reconciliation),
            base_ref=args.base_ref,
        )
    elif args.command == "handover":
        result = publish_handover(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            base_ref=args.base_ref,
        )
    elif args.command == "local-execution":
        result = export_local_execution(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            base_ref=args.base_ref,
            mode=args.mode,
        )
    elif args.command == "local-execution-result":
        result = accept_local_execution_result(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            result_path=Path(args.result),
        )
    elif args.command == "sync-delivery":
        result = sync_delivery(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            observation_path=Path(args.observation),
        )
    else:
        result = close_task(root, tx_id=args.tx_id, event_id=args.event_id, actor=args.actor)
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
