#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from transactionlib import incomplete_transactions
from v3lib import canonical_digest, load_events, load_yaml, repo_path, require_identifier, validate_schema


def _load(path: Path, label: str, errors: list[str]):
    try:
        return load_yaml(path)
    except Exception as exc:
        errors.append(f"{label}: cannot load {path}: {exc}")
        return None


def _repo_load(repo_root: Path, relative: str, label: str, errors: list[str]):
    try:
        path = repo_path(repo_root, relative, label)
    except ValueError as exc:
        errors.append(f"{label}: {exc}")
        return None
    return _load(path, label, errors)


def _safe_id(value, prefix: str, label: str, errors: list[str]):
    if value in {None, ""}:
        return None
    try:
        return require_identifier(str(value), prefix, label)
    except ValueError as exc:
        errors.append(f"{label}: {exc}")
        return None


def validate_authority(repo_root: Path) -> list[str]:
    """Validate durable present-authority objects only."""
    errors: list[str] = []
    pending = incomplete_transactions(repo_root)
    for path, manifest, error in pending:
        if error == "MISSING_MANIFEST":
            errors.append(f"TRANSACTION {path.parent.name}: incomplete staging directory has no manifest; recovery required")
        elif error:
            errors.append(f"TRANSACTION {path}: invalid/incomplete manifest: {error}")
        else:
            errors.append(
                f"TRANSACTION {manifest.get('id')}: status {manifest.get('status')} requires recovery before authority can be used"
            )

    relay = repo_root / "relay"
    state_path = relay / "STATE.yaml"
    state = _load(state_path, "STATE", errors)
    if not isinstance(state, dict):
        return errors or ["STATE: expected mapping"]

    errors.extend(validate_schema("state", state, "STATE"))

    roadmap_ref = (state.get("roadmap") or {}).get("path")
    roadmap = None
    if roadmap_ref:
        roadmap = _repo_load(repo_root, str(roadmap_ref), "ROADMAP", errors)
        if isinstance(roadmap, dict):
            errors.extend(validate_schema("roadmap", roadmap, "ROADMAP"))
            if roadmap.get("revision") != (state.get("roadmap") or {}).get("revision"):
                errors.append("ROADMAP.revision does not match STATE.roadmap.revision")

    controls_ref = (state.get("controls") or {}).get("path")
    controls = None
    if controls_ref:
        controls = _repo_load(repo_root, str(controls_ref), "CONTROLS", errors)
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
    ep = None
    lease = None

    ep_id = _safe_id(ep_id, "EP-", "STATE.execution.ep", errors)
    if ep_id:
        ep_path = relay / "WORK" / f"{ep_id}.yaml"
        ep = _load(ep_path, "EP", errors)
        if isinstance(ep, dict):
            errors.extend(validate_schema("ep", ep, "EP"))
            if ep.get("id") != ep_id:
                errors.append(f"EP.id {ep.get('id')} does not match STATE.execution.ep {ep_id}")
            if isinstance(roadmap, dict):
                wp_ids = {str(row.get("id")) for row in roadmap.get("work_packages") or [] if isinstance(row, dict)}
                if str(ep.get("work_package")) not in wp_ids:
                    errors.append("EP.work_package is not present in authoritative ROADMAP")

    lease_id = _safe_id(lease_id, "LEASE-", "STATE.execution.lease", errors)
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
            state_epoch = execution.get("custody_epoch")
            lease_epoch = ((lease.get("custody") or {}).get("epoch"))
            if state_epoch is not None:
                if lease_epoch is None:
                    errors.append("epoch-aware STATE requires referenced LEASE.custody.epoch")
                elif int(state_epoch) != int(lease_epoch):
                    errors.append("LEASE.custody.epoch does not match STATE.execution.custody_epoch")

    checkpoint_id = _safe_id((state.get("accepted") or {}).get("checkpoint"), "CP-", "STATE.accepted.checkpoint", errors)
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
    """Validate durable authority plus generated snapshot and append-only history."""
    errors = validate_authority(repo_root)
    relay = repo_root / "relay"
    state = _load(relay / "STATE.yaml", "STATE", errors)
    if not isinstance(state, dict):
        return errors or ["STATE: expected mapping"]

    roadmap_ref = (state.get("roadmap") or {}).get("path")
    roadmap = _repo_load(repo_root, str(roadmap_ref), "ROADMAP", errors) if roadmap_ref else None
    execution = state.get("execution") or {}
    ep_id = _safe_id(execution.get("ep"), "EP-", "STATE.execution.ep", errors)
    lease_id = _safe_id(execution.get("lease"), "LEASE-", "STATE.execution.lease", errors)
    checkpoint_id = _safe_id((state.get("accepted") or {}).get("checkpoint"), "CP-", "STATE.accepted.checkpoint", errors)
    ep = _load(relay / "WORK" / f"{ep_id}.yaml", "EP", errors) if ep_id else None
    lease = _load(relay / "LEASES" / f"{lease_id}.yaml", "LEASE", errors) if lease_id else None

    snapshot_ref = (state.get("generated") or {}).get("snapshot")
    if snapshot_ref:
        snapshot = _repo_load(repo_root, str(snapshot_ref), "SNAPSHOT", errors)
        if isinstance(snapshot, dict):
            errors.extend(validate_schema("snapshot", snapshot, "SNAPSHOT"))
            generated = snapshot.get("generated_from") or {}
            if generated.get("roadmap_revision") != (state.get("roadmap") or {}).get("revision"):
                errors.append("SNAPSHOT roadmap revision disagrees with STATE authority")
            if generated.get("state_digest") != canonical_digest(state):
                errors.append("SNAPSHOT state digest disagrees with STATE authority")
            if isinstance(roadmap, dict):
                owner = snapshot.get("owner") or {}
                expected_owner = roadmap.get("owner") or {}
                for key in ("outcome", "current_goal"):
                    if owner.get(key) != expected_owner.get(key):
                        errors.append(f"SNAPSHOT.owner.{key} disagrees with ROADMAP authority")
            sexec = snapshot.get("execution") or {}
            for key in ("lifecycle", "ep", "lease"):
                if sexec.get(key) != execution.get(key):
                    errors.append(f"SNAPSHOT.execution.{key} disagrees with STATE authority")
            if execution.get("custody_epoch") is not None and sexec.get("custody_epoch") != execution.get("custody_epoch"):
                errors.append("SNAPSHOT.execution.custody_epoch disagrees with STATE authority")
            if isinstance(ep, dict):
                if sexec.get("work_package") != ep.get("work_package"):
                    errors.append("SNAPSHOT.execution.work_package disagrees with EP authority")
                scope = snapshot.get("scope") or {}
                escope = ep.get("scope") or {}
                if scope.get("allowed_writes") != (escope.get("write") or []):
                    errors.append("SNAPSHOT.scope.allowed_writes disagrees with EP authority")
                if scope.get("protected") != (escope.get("protect") or []):
                    errors.append("SNAPSHOT.scope.protected disagrees with EP authority")
                if scope.get("prohibited") != (escope.get("prohibit") or []):
                    errors.append("SNAPSHOT.scope.prohibited disagrees with EP authority")
            if isinstance(lease, dict):
                expected_executor = ((lease.get("executor") or {}).get("id"))
                if sexec.get("executor") != expected_executor:
                    errors.append("SNAPSHOT.execution.executor disagrees with LEASE authority")
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
    parser = argparse.ArgumentParser(description="Validate Engineering Relay V3.1 foundation objects and authority links.")
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
