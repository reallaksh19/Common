#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v25_migration import INTELLIGENCE_CONTINUITY_CONTROL, MIGRATION_CONTROL, MIGRATION_REPORT, PROTOCOL_SELECTION, legacy_inventory, validate_v25_repo_state
from v3lib import canonical_digest, load_events, load_yaml, validate_schema
from validate_foundation import validate as validate_v3


READINESS_PATH = "relay/MIGRATION/CUTOVER_READINESS.yaml"
DEPRECATION_PATH = "relay/MIGRATION/V25_DEPRECATION.md"
INTELLIGENCE_CONTINUITY_PATH = "relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml"


class CutoverError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_required(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    if not path.exists():
        raise CutoverError(f"required cutover object is missing: {rel}")
    value = load_yaml(path)
    if not isinstance(value, dict):
        raise CutoverError(f"expected mapping: {rel}")
    return value


def freeze_legacy(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
) -> dict[str, Any]:
    selection = _load_required(root, PROTOCOL_SELECTION)
    selection_errors = validate_schema("protocol-selection", selection, "PROTOCOL_SELECTION")
    if selection_errors:
        raise CutoverError("; ".join(selection_errors))
    if selection.get("selected_protocol") != "V2_5" or selection.get("status") != "PREPARED":
        raise CutoverError("legacy cutover freeze requires V2_5 / PREPARED")

    source_status, source_basis = validate_v25_repo_state(root)
    if source_status != "PASS":
        raise CutoverError("cannot freeze invalid live V2.5 authority: " + "; ".join(source_basis[-5:]))

    _, freeze_digest = legacy_inventory(root)
    new_selection = {
        **selection,
        "cutover": {
            **selection["cutover"],
            "legacy_freeze_digest": freeze_digest,
        },
    }
    selection_errors = validate_schema("protocol-selection", new_selection, "PROTOCOL_SELECTION")
    if selection_errors:
        raise CutoverError("; ".join(selection_errors))

    events, event_errors = load_events(root / "relay/EVENTS.jsonl")
    if event_errors:
        raise CutoverError("; ".join(event_errors[:8]))
    if any(item.get("event_id") == event_id for item in events):
        raise CutoverError(f"duplicate event id: {event_id}")
    event = {
        "schema_version": "relay-v3-event",
        "event_id": event_id,
        "type": "LEGACY_CUTOVER_FROZEN",
        "timestamp": _now(),
        "actor": actor,
        "subject": "V2.5",
        "basis": [freeze_digest, *source_basis[-4:]],
        "details": {
            "bootstrap_digest": (selection.get("legacy") or {}).get("tree_digest"),
            "freeze_digest": freeze_digest,
        },
    }
    event_errors = validate_schema("event", event, "EVENT")
    if event_errors:
        raise CutoverError("; ".join(event_errors))
    events.append(event)

    return execute(
        root,
        tx_id=tx_id,
        command="FREEZE_LEGACY_CUTOVER",
        actor=actor,
        replacements={
            PROTOCOL_SELECTION: yaml_bytes(new_selection),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
    )


def assess(root: Path) -> dict[str, Any]:
    report = _load_required(root, MIGRATION_REPORT)
    selection = _load_required(root, PROTOCOL_SELECTION)
    state = _load_required(root, "relay/STATE.yaml")
    controls = _load_required(root, str((state.get("controls") or {}).get("path")))

    report_errors = validate_schema("migration-report", report, "MIGRATION_REPORT")
    selection_errors = validate_schema("protocol-selection", selection, "PROTOCOL_SELECTION")
    v3_errors = validate_v3(root)

    _, live_legacy_digest = legacy_inventory(root)
    bootstrap_legacy_digest = str((report.get("source") or {}).get("legacy_tree_digest") or "")
    freeze_legacy_digest = str(((selection.get("cutover") or {}).get("legacy_freeze_digest")) or "")
    source_status, source_basis = validate_v25_repo_state(root)
    source_validation = source_status == "PASS"

    migration_rows = [
        item for item in controls.get("controls") or []
        if isinstance(item, dict) and item.get("id") == MIGRATION_CONTROL
    ]
    migration_resolved = len(migration_rows) == 1 and migration_rows[0].get("state") == "RESOLVED"

    continuity_rows = [
        item for item in controls.get("controls") or []
        if isinstance(item, dict) and item.get("id") == INTELLIGENCE_CONTINUITY_CONTROL
    ]
    continuity_report_path = root / INTELLIGENCE_CONTINUITY_PATH
    continuity_report = load_yaml(continuity_report_path) if continuity_report_path.exists() else None
    continuity_report_errors = (
        validate_schema("intelligence-continuity", continuity_report, "INTELLIGENCE_CONTINUITY")
        if isinstance(continuity_report, dict)
        else ["continuity report missing"]
    )
    recomputed_continuity = None
    recomputed_continuity_error = None
    try:
        # Import lazily: intelligence_projection resolves protocol selection through
        # protocol_default, which itself imports validate_selection from this module.
        # Deferring this import avoids a module-initialization cycle while still
        # independently re-proving continuity at cutover assessment time.
        from intelligence_projection import assess_continuity
        recomputed_continuity = assess_continuity(root)
    except Exception as exc:
        recomputed_continuity_error = str(exc)

    continuity_report_ready = (
        isinstance(continuity_report, dict)
        and not continuity_report_errors
        and continuity_report.get("ready") is True
        and bool(freeze_legacy_digest)
        and ((continuity_report.get("source") or {}).get("legacy_tree_digest") == freeze_legacy_digest)
        and isinstance(recomputed_continuity, dict)
        and recomputed_continuity.get("ready") is True
        and canonical_digest(continuity_report) == canonical_digest(recomputed_continuity)
    )
    continuity_resolved = (
        len(continuity_rows) == 1
        and continuity_rows[0].get("state") == "RESOLVED"
        and bool(((continuity_rows[0].get("resolution") or {}).get("evidence") or []))
        and continuity_report_ready
    )

    lifecycle = str((state.get("execution") or {}).get("lifecycle") or "")
    lifecycle_ready = lifecycle in {"ACTIVE", "IDLE", "TERMINAL"}

    selection_prepared = (
        not selection_errors
        and selection.get("selected_protocol") == "V2_5"
        and selection.get("status") == "PREPARED"
        and (selection.get("legacy") or {}).get("policy") == "LIVE_COMPATIBILITY"
        and (selection.get("legacy") or {}).get("tree_digest") == bootstrap_legacy_digest
        and bool(freeze_legacy_digest)
    )

    checks = {
        "v3_conformance": "PASS" if not v3_errors else "FAIL",
        "legacy_digest_unchanged": "PASS" if freeze_legacy_digest and live_legacy_digest == freeze_legacy_digest else "FAIL",
        "source_validation": "PASS" if source_validation else "FAIL",
        "migration_control_resolved": "PASS" if migration_resolved else "FAIL",
        "roadmap_intelligence_continuity": "PASS" if continuity_resolved else "FAIL",
        "native_lifecycle_ready": "PASS" if lifecycle_ready else "FAIL",
        "protocol_selection_prepared": "PASS" if selection_prepared else "FAIL",
    }
    basis = [
        f"v3_conformance_errors={len(v3_errors)}",
        f"migration_report_errors={len(report_errors)}",
        f"protocol_selection_errors={len(selection_errors)}",
        f"legacy_bootstrap={bootstrap_legacy_digest}",
        f"legacy_freeze={freeze_legacy_digest or 'MISSING'}",
        f"legacy_live={live_legacy_digest}",
        f"source_validation={source_status}",
        f"lifecycle={lifecycle}",
        f"migration_control={migration_rows[0].get('state') if len(migration_rows) == 1 else 'MISSING_OR_AMBIGUOUS'}",
        f"roadmap_intelligence_continuity={continuity_rows[0].get('state') if len(continuity_rows) == 1 else 'MISSING_OR_AMBIGUOUS'}",
        f"roadmap_intelligence_evidence={len(((continuity_rows[0].get('resolution') or {}).get('evidence') or [])) if len(continuity_rows) == 1 else 0}",
        f"intelligence_continuity_report={'PASS' if continuity_report_ready else 'FAIL'}",
        f"intelligence_continuity_errors={len(continuity_report_errors)}",
        f"intelligence_continuity_recomputed={'PASS' if isinstance(recomputed_continuity, dict) and recomputed_continuity.get('ready') is True else 'FAIL'}",
        f"intelligence_continuity_recompute_error={recomputed_continuity_error or ''}",
    ]
    basis.extend(f"v3:{item}" for item in v3_errors[:8])
    readiness = {
        "schema_version": "relay-v3-cutover-readiness",
        "authority": "DERIVED_CUTOVER_READINESS",
        "assessed_at": _now(),
        "ready": all(value == "PASS" for value in checks.values()),
        "checks": checks,
        "basis": basis,
    }
    errors = validate_schema("cutover-readiness", readiness, "CUTOVER_READINESS")
    if errors:
        raise CutoverError("; ".join(errors))
    return readiness


def _event(event_id: str, actor: str, readiness: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any]:
    value = {
        "schema_version": "relay-v3-event",
        "event_id": event_id,
        "type": "PROTOCOL_CUTOVER_ACTIVATED",
        "timestamp": _now(),
        "actor": actor,
        "subject": "V3",
        "basis": [
            canonical_digest(readiness),
            str((selection.get("legacy") or {}).get("tree_digest")),
        ],
        "details": {
            "legacy_policy": "READ_ONLY_HISTORY",
            "selected_protocol": "V3",
        },
    }
    errors = validate_schema("event", value, "EVENT")
    if errors:
        raise CutoverError("; ".join(errors))
    return value


def activate(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    owner_utterance_digest: str,
    owner_session_timestamp: str,
) -> dict[str, Any]:
    readiness = assess(root)
    if readiness["ready"] is not True:
        failed = [key for key, value in readiness["checks"].items() if value != "PASS"]
        raise CutoverError("V3 cutover is not ready: " + ", ".join(failed))

    selection = _load_required(root, PROTOCOL_SELECTION)
    new_selection = {
        **selection,
        "selected_protocol": "V3",
        "status": "ACTIVE",
        "legacy": {
            **selection["legacy"],
            "policy": "READ_ONLY_HISTORY",
        },
        "v3": {
            **selection["v3"],
            "validation": "PASS",
        },
        "cutover": {
            **selection["cutover"],
            "owner_authorized": True,
            "owner_basis": {
                "direct_utterance_digest": owner_utterance_digest,
                "session_timestamp": owner_session_timestamp,
            },
            "readiness_digest": canonical_digest(readiness),
            "activated_at": _now(),
        },
    }
    errors = validate_schema("protocol-selection", new_selection, "PROTOCOL_SELECTION")
    if errors:
        raise CutoverError("; ".join(errors))

    events, event_errors = load_events(root / "relay/EVENTS.jsonl")
    if event_errors:
        raise CutoverError("; ".join(event_errors[:8]))
    if any(item.get("event_id") == event_id for item in events):
        raise CutoverError(f"duplicate event id: {event_id}")
    events.append(_event(event_id, actor, readiness, new_selection))

    notice = f"""# Engineering Relay V2.5 deprecation notice

Status: **READ_ONLY_HISTORY**

V3 became the selected relay protocol at {new_selection['cutover']['activated_at']}.

The preserved V2.5 tree remains at `agents/relay/**` with cutover digest:

```text
{new_selection['cutover']['legacy_freeze_digest']}
```

After cutover:
- existing V2.5 files remain inspectable as migration/history evidence;
- new relay authority must be written through V3 objects and commands;
- do not append new DISC/QSET/QUAL/TC/checkpoint/projection authority to the legacy tree;
- any change to the preserved legacy tree invalidates V3 cutover conformance until explicitly reconciled.
"""

    return execute(
        root,
        tx_id=tx_id,
        command="ACTIVATE_PROTOCOL_CUTOVER",
        actor=actor,
        replacements={
            PROTOCOL_SELECTION: yaml_bytes(new_selection),
            READINESS_PATH: yaml_bytes(readiness),
            DEPRECATION_PATH: notice.encode("utf-8"),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
    )


def validate_selection(root: Path) -> list[str]:
    path = root / PROTOCOL_SELECTION
    if not path.exists():
        return []
    selection = load_yaml(path)
    errors = validate_schema("protocol-selection", selection, "PROTOCOL_SELECTION")
    if errors:
        return errors

    if selection.get("selected_protocol") == "V3" and selection.get("status") == "ACTIVE":
        v3_errors = validate_v3(root)
        errors.extend(f"V3_CONFORMANCE: {item}" for item in v3_errors)
        try:
            _, live_digest = legacy_inventory(root)
        except Exception as exc:
            errors.append(f"LEGACY_HISTORY: {exc}")
            return errors
        expected = str(((selection.get("cutover") or {}).get("legacy_freeze_digest")) or "")
        if not expected:
            errors.append("LEGACY_HISTORY: active V3 selection has no frozen legacy digest")
            return errors
        if live_digest != expected:
            errors.append(
                f"LEGACY_HISTORY: agents/relay tree changed after V3 cutover: expected {expected}, got {live_digest}"
            )
        if not (root / DEPRECATION_PATH).exists():
            errors.append("V3_ACTIVE: V2.5 deprecation notice is missing")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess, activate, and validate Engineering Relay V3 protocol cutover.")
    parser.add_argument("repo_root", nargs="?", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("assess")

    freeze_parser = sub.add_parser("freeze")
    freeze_parser.add_argument("--tx-id", required=True)
    freeze_parser.add_argument("--event-id", required=True)
    freeze_parser.add_argument("--actor", required=True)

    activate_parser = sub.add_parser("activate")
    activate_parser.add_argument("--tx-id", required=True)
    activate_parser.add_argument("--event-id", required=True)
    activate_parser.add_argument("--actor", required=True)
    activate_parser.add_argument("--owner-utterance-digest", required=True)
    activate_parser.add_argument("--owner-session-timestamp", required=True)

    sub.add_parser("validate")

    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if args.command == "assess":
        value = assess(root)
        print(yaml.safe_dump(value, sort_keys=False), end="")
        raise SystemExit(0 if value["ready"] else 1)
    if args.command == "freeze":
        result = freeze_legacy(
            root,
            tx_id=args.tx_id,
            event_id=args.event_id,
            actor=args.actor,
        )
        print(f"{result['id']}: {result['status']}")
        return
    if args.command == "validate":
        errors = validate_selection(root)
        for error in errors:
            print(f"FAIL: {error}")
        if errors:
            raise SystemExit(1)
        print("PASS")
        return
    result = activate(
        root,
        tx_id=args.tx_id,
        event_id=args.event_id,
        actor=args.actor,
        owner_utterance_digest=args.owner_utterance_digest,
        owner_session_timestamp=args.owner_session_timestamp,
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
