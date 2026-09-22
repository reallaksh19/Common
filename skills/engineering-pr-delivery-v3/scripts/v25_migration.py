#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v3lib import canonical_digest, load_yaml, validate_schema


V25_ROOT = Path(__file__).resolve().parents[2] / "engineering-pr-delivery-v2.5"
V25_STATE = "agents/relay/REPO_STATE.yaml"
V25_TREE = "agents/relay"
MIGRATION_REPORT = "relay/MIGRATION/V25_REPORT.yaml"
PROTOCOL_SELECTION = "relay/PROTOCOL_SELECTION.yaml"
MIGRATION_CONTROL = "CTRL-MIGRATION-RECONCILE"


class MigrationError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _category(path: str) -> str:
    low = path.lower()
    if path.endswith("REPO_STATE.yaml"):
        return "REPO_STATE"
    if "/roadmap/" in low:
        if "event" in low:
            return "ROADMAP_EVENT"
        return "ROADMAP"
    if "/execution-packages/" in low:
        return "EP"
    if "/checkpoints/" in low:
        return "CHECKPOINT"
    if "/discovery/" in low:
        return "DISCOVERY"
    if "qualification" in low:
        return "QUALIFICATION"
    if "takeover" in low or "certification" in low:
        return "TAKEOVER_CERTIFICATION"
    if "control" in low or "pending" in low or "known-issue" in low or "delegat" in low:
        return "CONTROL"
    if "delivery" in low:
        return "DELIVERY"
    if "projection" in low or "github" in low:
        return "PROJECTION"
    if "/parallel/" in low:
        return "PARALLEL"
    return "OTHER"


def _schema_version(path: Path) -> str | None:
    if path.suffix.lower() not in {".yaml", ".yml", ".json"}:
        return None
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return str(value.get("schema_version")) if isinstance(value, dict) and value.get("schema_version") else None


def legacy_inventory(root: Path) -> tuple[list[dict[str, Any]], str]:
    base = root / V25_TREE
    if not base.exists():
        raise MigrationError(f"legacy relay tree is missing: {V25_TREE}")
    entries = []
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        entries.append({
            "path": rel,
            "digest": _sha256_bytes(path.read_bytes()),
            "category": _category(rel),
            "schema_version": _schema_version(path),
        })
    if not entries:
        raise MigrationError("legacy relay tree contains no files")
    return entries, canonical_digest([{"path": x["path"], "digest": x["digest"]} for x in entries])


def validate_v25_repo_state(root: Path) -> tuple[str, list[str]]:
    validator = V25_ROOT / "scripts/validate_repo_state.py"
    if not validator.exists():
        return "FAIL", [f"missing Common V2.5 validator: {validator}"]
    proc = subprocess.run(
        [sys.executable, str(validator), str(root)],
        cwd=V25_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    basis = [f"validate_repo_state.py exit={proc.returncode}"]
    basis.extend(output[-12:] or ["validator produced no output"])
    return ("PASS" if proc.returncode == 0 else "FAIL"), basis


def build_report(root: Path) -> dict[str, Any]:
    state_path = root / V25_STATE
    if not state_path.exists():
        raise MigrationError(f"V2.5 state is missing: {V25_STATE}")
    state = load_yaml(state_path)
    if not isinstance(state, dict) or state.get("schema_version") != "relay-v2.5":
        raise MigrationError("source REPO_STATE is not relay-v2.5")
    roadmap_ref = str((state.get("roadmap") or {}).get("path") or "")
    if not roadmap_ref or not (root / roadmap_ref).exists():
        raise MigrationError("source REPO_STATE roadmap pointer is missing or invalid")

    entries, tree_digest = legacy_inventory(root)
    status, basis = validate_v25_repo_state(root)
    counts = Counter(item["category"] for item in entries)
    report = {
        "schema_version": "relay-v3-migration-report",
        "authority": "DERIVED_MIGRATION_REPORT",
        "source_protocol": "2.5",
        "generated_at": _now(),
        "source": {
            "root": str(root),
            "state_path": V25_STATE,
            "state_digest": _sha256_bytes(state_path.read_bytes()),
            "roadmap_path": roadmap_ref,
            "legacy_tree_digest": tree_digest,
        },
        "validation": {
            "repo_state": status,
            "basis": basis,
        },
        "legacy_inventory": {
            "file_count": len(entries),
            "category_counts": dict(sorted(counts.items())),
            "entries": entries,
        },
        "current": {
            "relay_state": state.get("relay_state"),
            "active_ep": None if (state.get("active_ep") or {}).get("id") in {None, "", "NONE"} else (state.get("active_ep") or {}).get("id"),
            "last_checkpoint": None if (state.get("last_checkpoint") or {}).get("id") in {None, "", "NONE"} else (state.get("last_checkpoint") or {}).get("id"),
            "roadmap_revision": str((state.get("roadmap") or {}).get("revision") or ""),
            "execution_policy": str((state.get("execution_policy") or {}).get("mode") or ""),
            "delivery_required": bool((state.get("delivery") or {}).get("required", False)),
        },
        "bootstrap": {
            "allowed": status == "PASS",
            "lifecycle": "INITIALIZING",
            "preserves_legacy_tree": True,
            "creates_native_history": False,
            "reason": (
                "Bootstrap creates only present-day V3 INITIALIZING authority and retains V2.5 evidence as read-only source history."
                if status == "PASS"
                else "V2.5 REPO_STATE validation failed; V3 bootstrap is denied."
            ),
        },
    }
    errors = validate_schema("migration-report", report, "MIGRATION_REPORT")
    if errors:
        raise MigrationError("; ".join(errors))
    return report


def _legacy_work_packages(root: Path, state: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    roadmap = load_yaml(root / str((state.get("roadmap") or {}).get("path")))
    title = str(((roadmap.get("roadmap") or {}).get("title")) or "Migrated V2.5 roadmap")
    progress_path = root / "agents/relay/roadmap/PROGRESS.yaml"
    weights: dict[str, float] = {}
    if progress_path.exists():
        progress = load_yaml(progress_path)
        for row in (progress or {}).get("work_packages") or []:
            if isinstance(row, dict) and row.get("id"):
                total = float(row.get("total_weight") or 0)
                if total > 0:
                    weights[str(row["id"])] = total

    rows: list[dict[str, Any]] = []
    state_map = {
        "COMPLETE": "COMPLETE",
        "ACTIVE": "ACTIVE",
        "BLOCKED": "BLOCKED",
        "PLANNED": "PLANNED",
        "FUTURE": "PLANNED",
        "SUPERSEDED": "COMPLETE",
        "CANCELLED": "COMPLETE",
    }
    for objective in roadmap.get("objectives") or []:
        for phase in (objective or {}).get("phases") or []:
            for wp in (phase or {}).get("work_packages") or []:
                if not isinstance(wp, dict) or not wp.get("id"):
                    continue
                wid = str(wp["id"])
                rows.append({
                    "id": wid,
                    "title": str(wp.get("title") or wid),
                    "weight": weights.get(wid, 1.0),
                    "state": state_map.get(str(wp.get("state") or "PLANNED"), "PLANNED"),
                    "depends_on": [str(x) for x in (wp.get("depends_on") or []) if str(x)],
                })
    if not rows:
        raise MigrationError("legacy roadmap has no work packages that can seed the V3 conceptual roadmap")
    return title, rows


def _event(event_id: str, actor: str, report: dict[str, Any]) -> dict[str, Any]:
    value = {
        "schema_version": "relay-v3-event",
        "event_id": event_id,
        "type": "MIGRATION_BOOTSTRAPPED",
        "timestamp": _now(),
        "actor": actor,
        "subject": "V2.5-to-V3",
        "basis": [
            str((report.get("source") or {}).get("legacy_tree_digest")),
            str((report.get("source") or {}).get("state_digest")),
        ],
        "details": {
            "legacy_history_rewritten": False,
            "native_history_imported": False,
        },
    }
    errors = validate_schema("event", value, "EVENT")
    if errors:
        raise MigrationError("; ".join(errors))
    return value


def _initial_snapshot(
    root: Path,
    state: dict[str, Any],
    roadmap: dict[str, Any],
    controls: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, Any]:
    head = _git(root, "rev-parse", "HEAD")
    empty = canonical_digest([])
    groups = {
        "execution_blockers": [],
        "handover_blockers": [],
        "delivery_blockers": [],
        "informational": [],
    }
    for row in controls["controls"]:
        if row.get("state") != "OPEN":
            continue
        blocks = set(row.get("blocks") or [])
        cid = str(row.get("id"))
        if blocks & {"READ", "ANALYZE", "MATERIAL_WRITE", "TEST", "CHECKPOINT"}:
            groups["execution_blockers"].append(cid)
        if blocks & {"HANDOVER", "LOCAL_EXECUTION_EXPORT"}:
            groups["handover_blockers"].append(cid)
        if blocks & {"DRAFT_PR_UPDATE", "PR_READY", "MERGE", "RELEASE", "CLOSE_TASK"}:
            groups["delivery_blockers"].append(cid)

    snapshot = {
        "schema_version": "relay-v3-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "generated_from": {
            "roadmap_revision": roadmap["revision"],
            "state_digest": canonical_digest(state),
            "material_basis": {
                "head": head,
                "tree_digest": empty,
                "relevant_paths_digest": empty,
                "dependency_digest": empty,
            },
            "coordination_head": head,
        },
        "owner": dict(roadmap["owner"]),
        "programme": {
            "accepted_progress": 0.0,
            "completed_work": [],
            "remaining_work": [row["id"] for row in roadmap["work_packages"]],
        },
        "execution": {
            "lifecycle": "INITIALIZING",
            "work_package": None,
            "ep": None,
            "lease": None,
            "executor": None,
        },
        "scope": {"allowed_writes": [], "protected": [], "prohibited": []},
        "material": {
            "base": head,
            "head": head,
            "relevant_paths_digest": empty,
            "dependency_digest": empty,
        },
        "evidence": {"latest_checkpoint": None, "latest_material_validation": {}},
        "controls": groups,
        "delivery": {"issue": None, "pr": None, "lifecycle": "NOT_REQUIRED", "merge_authorized": False},
        "next": {
            "immediate_material_action": "Reconcile legacy intent/evidence into one native V3 EP and lease before material work.",
            "delivery_action": None,
            "stop_conditions": ["Do not infer native V3 acceptance or custody from V2.5 receipts."],
        },
        "handoff": {
            "zero_context_takeover_possible": False,
            "reconstruction_sources": [
                "relay/ROADMAP/ROADMAP.yaml",
                "relay/STATE.yaml",
                "relay/CONTROLS/controls.yaml",
                MIGRATION_REPORT,
                V25_STATE,
            ],
        },
    }
    errors = validate_schema("snapshot", snapshot, "CURRENT_SNAPSHOT")
    if errors:
        raise MigrationError("; ".join(errors))
    return snapshot


def bootstrap(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    owner_outcome: str,
    current_goal: str,
) -> dict[str, Any]:
    if (root / "relay/STATE.yaml").exists():
        raise MigrationError("native V3 STATE already exists; migration bootstrap refuses overwrite")
    report = build_report(root)
    if report["validation"]["repo_state"] != "PASS":
        raise MigrationError("V2.5 REPO_STATE validation must PASS before V3 bootstrap")
    state25 = load_yaml(root / V25_STATE)
    title, work_packages = _legacy_work_packages(root, state25)
    roadmap = {
        "schema_version": "relay-v3-roadmap",
        "revision": str((state25.get("roadmap") or {}).get("revision")),
        "title": title,
        "owner": {
            "outcome": owner_outcome.strip(),
            "current_goal": current_goal.strip(),
        },
        "work_packages": work_packages,
    }
    if not roadmap["owner"]["outcome"] or not roadmap["owner"]["current_goal"]:
        raise MigrationError("owner_outcome and current_goal must be explicit; migration does not invent Owner intent")
    errors = validate_schema("roadmap", roadmap, "ROADMAP")
    if errors:
        raise MigrationError("; ".join(errors))

    controls = {
        "schema_version": "relay-v3-controls",
        "controls": [{
            "id": MIGRATION_CONTROL,
            "kind": "PROTOCOL",
            "state": "OPEN",
            "source": {"type": "VALIDATOR", "ref": MIGRATION_REPORT},
            "condition": "Legacy V2.5 intent/evidence has not yet been reconciled into native V3 execution authority.",
            "blocks": ["MATERIAL_WRITE", "TEST", "CHECKPOINT", "HANDOVER", "LOCAL_EXECUTION_EXPORT", "DRAFT_PR_UPDATE", "PR_READY", "MERGE", "RELEASE", "CLOSE_TASK"],
            "permits": ["READ", "ANALYZE"],
            "resolution": {
                "condition": "Native V3 roadmap/frontier/EP/lease/checkpoint disposition is established without rewriting V2.5 history.",
                "evidence": [],
            },
        }],
    }
    errors = validate_schema("controls", controls, "CONTROLS")
    if errors:
        raise MigrationError("; ".join(errors))

    state = {
        "schema_version": "relay-v3",
        "roadmap": {
            "revision": roadmap["revision"],
            "path": "relay/ROADMAP/ROADMAP.yaml",
        },
        "execution": {"lifecycle": "INITIALIZING", "ep": None, "lease": None, "route": None},
        "accepted": {"checkpoint": None},
        "controls": {"path": "relay/CONTROLS/controls.yaml"},
        "delivery": {"required": False, "primary_vehicle": None},
        "generated": {"snapshot": "relay/GENERATED/CURRENT_SNAPSHOT.yaml"},
    }
    errors = validate_schema("state", state, "STATE")
    if errors:
        raise MigrationError("; ".join(errors))

    selection = {
        "schema_version": "relay-v3-protocol-selection",
        "selected_protocol": "V2_5",
        "status": "PREPARED",
        "legacy": {
            "root": V25_TREE,
            "tree_digest": report["source"]["legacy_tree_digest"],
            "policy": "LIVE_COMPATIBILITY",
        },
        "v3": {
            "state_path": "relay/STATE.yaml",
            "validation": "PENDING",
        },
        "cutover": {
            "owner_authorized": False,
            "owner_basis": None,
            "readiness_digest": None,
            "activated_at": None,
        },
    }
    errors = validate_schema("protocol-selection", selection, "PROTOCOL_SELECTION")
    if errors:
        raise MigrationError("; ".join(errors))

    snapshot = _initial_snapshot(root, state, roadmap, controls, report)
    events = [_event(event_id, actor, report)]
    replacements = {
        MIGRATION_REPORT: yaml_bytes(report),
        PROTOCOL_SELECTION: yaml_bytes(selection),
        "relay/ROADMAP/ROADMAP.yaml": yaml_bytes(roadmap),
        "relay/STATE.yaml": yaml_bytes(state),
        "relay/CONTROLS/controls.yaml": yaml_bytes(controls),
        "relay/GENERATED/CURRENT_SNAPSHOT.yaml": yaml_bytes(snapshot),
        "relay/EVENTS.jsonl": jsonl_bytes(events),
    }
    return execute(
        root,
        tx_id=tx_id,
        command="BOOTSTRAP_V3_MIGRATION",
        actor=actor,
        replacements=replacements,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory V2.5 relay truth and optionally bootstrap non-destructive V3 INITIALIZING authority.")
    parser.add_argument("repo_root", nargs="?", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("report")

    boot = sub.add_parser("bootstrap")
    boot.add_argument("--tx-id", required=True)
    boot.add_argument("--event-id", required=True)
    boot.add_argument("--actor", required=True)
    boot.add_argument("--owner-outcome", required=True)
    boot.add_argument("--current-goal", required=True)

    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if args.command == "report":
        print(yaml.safe_dump(build_report(root), sort_keys=False), end="")
        return
    result = bootstrap(
        root,
        tx_id=args.tx_id,
        event_id=args.event_id,
        actor=args.actor,
        owner_outcome=args.owner_outcome,
        current_goal=args.current_goal,
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
