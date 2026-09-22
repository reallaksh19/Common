#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lease_admission import build_native_lease
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
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, _ = _authority(root)
    old_lease_id = (state.get("execution") or {}).get("lease")
    old_lease = None
    if old_lease_id:
        old_lease = load_yaml(root / "relay/LEASES" / f"{old_lease_id}.yaml")
        if old_lease.get("state") == "ACTIVE" and (old_lease.get("executor") or {}).get("id") != executor_id:
            # Build against a release view so the pure admission helper can evaluate the transfer.
            old_path = root / "relay/LEASES" / f"{old_lease_id}.yaml"
            original = old_path.read_bytes()
            released = copy.deepcopy(old_lease)
            released["state"] = "RELEASED"
            old_path.write_bytes(yaml_bytes(released))
            try:
                new_lease = build_native_lease(
                    root,
                    lease_id=lease_id,
                    executor_id=executor_id,
                    method=method,
                    qualification=qualification,
                    owner_basis=owner_basis,
                    branch=branch,
                )
            finally:
                old_path.write_bytes(original)
        else:
            new_lease = build_native_lease(
                root,
                lease_id=lease_id,
                executor_id=executor_id,
                method=method,
                qualification=qualification,
                owner_basis=owner_basis,
                branch=branch,
            )
    else:
        new_lease = build_native_lease(
            root,
            lease_id=lease_id,
            executor_id=executor_id,
            method=method,
            qualification=qualification,
            owner_basis=owner_basis,
            branch=branch,
        )

    replacements: dict[str, bytes] = {}
    if old_lease and old_lease_id != lease_id and old_lease.get("state") == "ACTIVE":
        released = copy.deepcopy(old_lease)
        released["state"] = "RELEASED"
        replacements[f"relay/LEASES/{old_lease_id}.yaml"] = yaml_bytes(released)

    new_state = copy.deepcopy(state)
    execution = new_state["execution"]
    execution["lifecycle"] = "ACTIVE"
    execution["ep"] = (new_lease.get("basis") or {}).get("ep_id")
    execution["lease"] = lease_id
    execution["route"] = new_lease.get("route")
    replacements[f"relay/LEASES/{lease_id}.yaml"] = yaml_bytes(new_lease)
    replacements["relay/STATE.yaml"] = yaml_bytes(new_state)

    events = _events(root)
    if any(item.get("event_id") == event_id for item in events):
        raise TransactionError(f"duplicate event id: {event_id}")
    if old_lease and old_lease_id != lease_id and old_lease.get("state") == "ACTIVE":
        events.append(_event(
            event_id + "-REL",
            "LEASE_RELEASED",
            actor,
            old_lease_id,
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

    return execute(
        root,
        tx_id=tx_id,
        command="ACTIVATE_LEASE",
        actor=actor,
        replacements=replacements,
        fail_after=fail_after,
    )


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

    events = _events(root)
    if any(item.get("event_id") == event_id for item in events):
        raise TransactionError(f"duplicate event id: {event_id}")
    events.append(_event(event_id, "LEASE_RELEASED", actor, lease_id, [tx_id], {}))

    return execute(
        root,
        tx_id=tx_id,
        command="RELEASE_LEASE",
        actor=actor,
        replacements={
            f"relay/LEASES/{lease_id}.yaml": yaml_bytes(released),
            "relay/STATE.yaml": yaml_bytes(new_state),
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

    cp_id = checkpoint.get("id")
    target = f"relay/CHECKPOINTS/{cp_id}.yaml"
    new_state = copy.deepcopy(state)
    new_state["accepted"]["checkpoint"] = cp_id

    events = _events(root)
    if any(item.get("event_id") == event_id for item in events):
        raise TransactionError(f"duplicate event id: {event_id}")
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
    fail_after: int | None = None,
) -> dict[str, Any]:
    state, controls = _authority(root)
    matches = [item for item in controls.get("controls") or [] if item.get("id") == control_id]
    if len(matches) != 1:
        raise TransactionError(f"expected one control {control_id}; found {len(matches)}")
    item = matches[0]
    if item.get("state") != "OPEN":
        raise TransactionError(f"control {control_id} is not OPEN")
    if not evidence:
        raise TransactionError("control resolution requires durable evidence")

    new_controls = copy.deepcopy(controls)
    for row in new_controls["controls"]:
        if row.get("id") == control_id:
            row["state"] = "RESOLVED"
            row["resolution"]["evidence"] = list(evidence)

    events = _events(root)
    if any(item.get("event_id") == event_id for item in events):
        raise TransactionError(f"duplicate event id: {event_id}")
    events.append(_event(
        event_id,
        "CONTROL_RESOLVED",
        actor,
        control_id,
        [tx_id, *evidence],
        {},
    ))
    controls_path = str((state.get("controls") or {}).get("path"))

    return execute(
        root,
        tx_id=tx_id,
        command="RESOLVE_CONTROL",
        actor=actor,
        replacements={
            controls_path: yaml_bytes(new_controls),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Engineering Relay V3 transactional command surface.")
    parser.add_argument("repo_root", nargs="?", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    recover = sub.add_parser("recover")
    recover.add_argument("--actor", default="recovery")

    activate = sub.add_parser("activate-lease")
    activate.add_argument("--tx-id", required=True)
    activate.add_argument("--event-id", required=True)
    activate.add_argument("--lease-id", required=True)
    activate.add_argument("--executor-id", required=True)
    activate.add_argument("--actor", required=True)
    activate.add_argument("--method", choices=["DETERMINISTIC", "QUALIFIED", "OWNER_OVERRIDE"], required=True)
    activate.add_argument("--qualification")
    activate.add_argument("--owner-utterance-digest")
    activate.add_argument("--owner-session-timestamp")
    activate.add_argument("--branch")

    release = sub.add_parser("release-lease")
    release.add_argument("--tx-id", required=True)
    release.add_argument("--event-id", required=True)
    release.add_argument("--actor", required=True)

    checkpoint = sub.add_parser("accept-checkpoint")
    checkpoint.add_argument("--tx-id", required=True)
    checkpoint.add_argument("--event-id", required=True)
    checkpoint.add_argument("--actor", required=True)
    checkpoint.add_argument("--checkpoint", required=True)

    control = sub.add_parser("resolve-control")
    control.add_argument("--tx-id", required=True)
    control.add_argument("--event-id", required=True)
    control.add_argument("--actor", required=True)
    control.add_argument("--control-id", required=True)
    control.add_argument("--evidence", action="append", default=[])

    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if args.command == "recover":
        for result in recover_all(root):
            print(f"{result['id']}: {result['status']}")
        return
    if args.command == "activate-lease":
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
        )
    elif args.command == "release-lease":
        result = release_lease(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
        )
    elif args.command == "accept-checkpoint":
        result = accept_checkpoint(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            checkpoint_path=Path(args.checkpoint),
        )
    else:
        result = resolve_control(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
            control_id=args.control_id,
            evidence=args.evidence,
        )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
