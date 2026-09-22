#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from v3lib import load_events, load_yaml, validate_schema


def _load(path: Path, label: str, errors: list[str]):
    try:
        return load_yaml(path)
    except Exception as exc:
        errors.append(f"{label}: cannot load {path}: {exc}")
        return None


def validate_authority(repo_root: Path) -> list[str]:
    """Validate only durable present-authority objects.

    Generated snapshots and append-only history are intentionally excluded so
    execution authorization cannot be coupled to derived-view/history freshness.
    """
    errors: list[str] = []
    relay = repo_root / "relay"
    state_path = relay / "STATE.yaml"
    state = _load(state_path, "STATE", errors)
    if not isinstance(state, dict):
        return errors or ["STATE: expected mapping"]

    errors.extend(validate_schema("state", state, "STATE"))

    controls_ref = ((state.get("controls") or {}).get("path"))
    if controls_ref:
        controls = _load(repo_root / str(controls_ref), "CONTROLS", errors)
        if isinstance(controls, dict):
            errors.extend(validate_schema("controls", controls, "CONTROLS"))
            for index, control in enumerate(controls.get("controls") or []):
                blocked = set(control.get("blocks") or [])
                permitted = set(control.get("permits") or [])
                overlap = sorted(blocked & permitted)
                if overlap:
                    errors.append(
                        f"CONTROLS.controls[{index}]: actions cannot be both blocked and permitted: {', '.join(overlap)}"
                    )

    execution = state.get("execution") or {}
    ep_id = execution.get("ep")
    lease_id = execution.get("lease")
    route = execution.get("route")

    if ep_id:
        ep_path = relay / "WORK" / f"{ep_id}.yaml"
        ep = _load(ep_path, "EP", errors)
        if isinstance(ep, dict):
            errors.extend(validate_schema("ep", ep, "EP"))
            if ep.get("id") != ep_id:
                errors.append(f"EP.id {ep.get('id')} does not match STATE.execution.ep {ep_id}")

    if lease_id:
        lease_path = relay / "LEASES" / f"{lease_id}.yaml"
        lease = _load(lease_path, "LEASE", errors)
        if isinstance(lease, dict):
            errors.extend(validate_schema("lease", lease, "LEASE"))
            if lease.get("id") != lease_id:
                errors.append(f"LEASE.id {lease.get('id')} does not match STATE.execution.lease {lease_id}")
            if lease.get("route") != route:
                errors.append("LEASE.route does not match STATE.execution.route")
            if (lease.get("basis") or {}).get("ep_id") != ep_id:
                errors.append("LEASE.basis.ep_id does not match STATE.execution.ep")
            if execution.get("lifecycle") == "ACTIVE" and lease.get("state") != "ACTIVE":
                errors.append("ACTIVE STATE requires referenced LEASE.state ACTIVE")

    checkpoint_id = ((state.get("accepted") or {}).get("checkpoint"))
    if checkpoint_id:
        cp_path = relay / "CHECKPOINTS" / f"{checkpoint_id}.yaml"
        checkpoint = _load(cp_path, "CHECKPOINT", errors)
        if isinstance(checkpoint, dict):
            errors.extend(validate_schema("checkpoint", checkpoint, "CHECKPOINT"))
            if checkpoint.get("id") != checkpoint_id:
                errors.append(
                    f"CHECKPOINT.id {checkpoint.get('id')} does not match STATE.accepted.checkpoint {checkpoint_id}"
                )

    return errors


def validate(repo_root: Path) -> list[str]:
    """Validate durable authority plus derived snapshot and append-only history."""
    errors = validate_authority(repo_root)
    relay = repo_root / "relay"
    state = _load(relay / "STATE.yaml", "STATE", errors)
    if not isinstance(state, dict):
        return errors or ["STATE: expected mapping"]

    execution = state.get("execution") or {}
    checkpoint_id = ((state.get("accepted") or {}).get("checkpoint"))

    snapshot_ref = ((state.get("generated") or {}).get("snapshot"))
    if snapshot_ref:
        snapshot = _load(repo_root / str(snapshot_ref), "SNAPSHOT", errors)
        if isinstance(snapshot, dict):
            errors.extend(validate_schema("snapshot", snapshot, "SNAPSHOT"))
            if (snapshot.get("generated_from") or {}).get("roadmap_revision") != (
                (state.get("roadmap") or {}).get("revision")
            ):
                errors.append("SNAPSHOT roadmap revision disagrees with STATE authority")
            sexec = snapshot.get("execution") or {}
            for key in ("lifecycle", "ep", "lease"):
                if sexec.get(key) != execution.get(key):
                    errors.append(f"SNAPSHOT.execution.{key} disagrees with STATE authority")
            if (snapshot.get("evidence") or {}).get("latest_checkpoint") != checkpoint_id:
                errors.append("SNAPSHOT latest checkpoint disagrees with STATE authority")

    events, event_errors = load_events(relay / "EVENTS.jsonl")
    errors.extend(event_errors)
    seen = set()
    for event in events:
        event_id = event.get("event_id")
        if event_id in seen:
            errors.append(f"EVENTS: duplicate event_id {event_id}")
        seen.add(event_id)

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Engineering Relay V3 foundation objects and authority links.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument(
        "--authority-only",
        action="store_true",
        help="Validate durable present-authority objects only; ignore generated snapshot/history freshness.",
    )
    args = parser.parse_args()
    validator = validate_authority if args.authority_only else validate
    errors = validator(Path(args.repo_root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
