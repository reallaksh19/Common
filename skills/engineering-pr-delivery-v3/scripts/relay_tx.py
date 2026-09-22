#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from handover_projection import render as render_handover
from lease_admission import build_native_lease
from local_execution_projection import build as build_local_execution
from relay_can import evaluate as can_action
from snapshot_projection import build as build_snapshot
from transactionlib import TransactionError, execute, jsonl_bytes, recover_all, yaml_bytes
from v3lib import load_events, load_yaml, validate_schema
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
        "schema_version": "relay-v3-event",
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


def _require_action(root: Path, action: str) -> None:
    result = can_action(root, action)
    if not result["allowed"]:
        raise TransactionError(f"{action} denied: {', '.join(result['reason_codes'])}")


def _current_checkpoint(root: Path, state: dict[str, Any]) -> dict[str, Any] | None:
    cp_id = (state.get("accepted") or {}).get("checkpoint")
    return load_yaml(root / "relay/CHECKPOINTS" / f"{cp_id}.yaml") if cp_id else None


def _current_ep(root: Path, state: dict[str, Any]) -> dict[str, Any] | None:
    ep_id = (state.get("execution") or {}).get("ep")
    return load_yaml(root / "relay/WORK" / f"{ep_id}.yaml") if ep_id else None


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
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, _ = _authority(root)
    execution = state.get("execution") or {}
    lease_id = execution.get("lease")
    if not lease_id:
        raise TransactionError("no active lease to release")
    lease_path = root / "relay/LEASES" / f"{lease_id}.yaml"
    lease = load_yaml(lease_path)
    if lease.get("state") != "ACTIVE":
        raise TransactionError("current lease is not ACTIVE")

    released = copy.deepcopy(lease)
    released["state"] = "RELEASED"
    new_state = copy.deepcopy(state)
    new_state["execution"] = {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None}
    snapshot = build_snapshot(root, state_override=new_state)

    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(event_id, "LEASE_RELEASED", actor, str(lease_id), [tx_id], {}))

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
    handover = render_handover(snapshot, checkpoint).encode("utf-8")
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
    fail_after: int | None = None,
) -> dict[str, Any]:
    _require_action(root, "LOCAL_EXECUTION_EXPORT")
    state, _ = _authority(root)
    snapshot = build_snapshot(root, base_ref)
    ep = _current_ep(root, state)
    checkpoint = _current_checkpoint(root, state)
    package = build_local_execution(root, snapshot, ep, checkpoint)
    events = _events(root)
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "LOCAL_EXECUTION_EXPORTED",
        actor,
        str((state.get("execution") or {}).get("ep") or "relay"),
        [tx_id, _snapshot_path(state)],
        {"artifact": "relay/GENERATED/LOCAL_EXECUTION.yaml"},
    ))
    return execute(
        root,
        tx_id=tx_id,
        command="EXPORT_LOCAL_EXECUTION",
        actor=actor,
        replacements={
            _snapshot_path(state): yaml_bytes(snapshot),
            "relay/GENERATED/LOCAL_EXECUTION.yaml": yaml_bytes(package),
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
    parser = argparse.ArgumentParser(description="Engineering Relay V3 transactional command surface.")
    parser.add_argument("repo_root", nargs="?", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("recover")

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
        result = release_lease(root, tx_id=args.tx_id, event_id=args.event_id, actor=args.actor)
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
