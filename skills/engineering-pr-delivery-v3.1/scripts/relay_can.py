#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
from typing import Any

from material_basis import inspect as inspect_material_basis
from v3lib import load_yaml, validate_schema
from validate_foundation import validate_authority


ACTIONS = {
    "READ",
    "ANALYZE",
    "MATERIAL_WRITE",
    "TEST",
    "CHECKPOINT",
    "HANDOVER",
    "LOCAL_EXECUTION_EXPORT",
    "DRAFT_PR_UPDATE",
    "PR_READY",
    "MERGE",
    "RELEASE",
    "CLOSE_TASK",
    "PROTOCOL_CUTOVER",
}
EXECUTION_ACTIONS = {"MATERIAL_WRITE", "TEST", "CHECKPOINT"}
LEASE_ACTIONS = {"MATERIAL_WRITE", "TEST", "CHECKPOINT"}
WORK_CONTEXT_ACTIONS = {"HANDOVER", "LOCAL_EXECUTION_EXPORT"}
DELIVERY_VEHICLE_ACTIONS = {"DRAFT_PR_UPDATE", "PR_READY", "MERGE", "RELEASE"}
DELIVERY_OWNER_ACTIONS = {"MERGE", "RELEASE"}
CHECKPOINT_ACTIONS = {"PR_READY", "MERGE", "RELEASE", "CLOSE_TASK"}
QUALITY_ACTIONS = {"PR_READY", "MERGE", "RELEASE"}
LIVE_V3_ACTIONS = {"MATERIAL_WRITE", "TEST", "CHECKPOINT", "DRAFT_PR_UPDATE", "PR_READY", "MERGE", "RELEASE", "CLOSE_TASK"}
FENCED_ACTIONS = {"MATERIAL_WRITE", "TEST", "CHECKPOINT", "HANDOVER", "LOCAL_EXECUTION_EXPORT", "DRAFT_PR_UPDATE", "PR_READY", "MERGE", "RELEASE", "CLOSE_TASK"}


def _load_current(root: Path) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None, dict[str, Any], dict[str, Any] | None]:
    relay = root / "relay"
    state = load_yaml(relay / "STATE.yaml")
    execution = state.get("execution") or {}
    ep_id = execution.get("ep")
    lease_id = execution.get("lease")
    cp_id = (state.get("accepted") or {}).get("checkpoint")
    ep = load_yaml(relay / "WORK" / f"{ep_id}.yaml") if ep_id else None
    lease = load_yaml(relay / "LEASES" / f"{lease_id}.yaml") if lease_id else None
    controls = load_yaml(root / str((state.get("controls") or {}).get("path")))
    checkpoint = load_yaml(relay / "CHECKPOINTS" / f"{cp_id}.yaml") if cp_id else None
    return state, ep, lease, controls, checkpoint


def _matches(path: str, pattern: str) -> bool:
    path = path.replace("\\", "/").lstrip("./")
    pattern = pattern.replace("\\", "/").lstrip("./")
    if fnmatch.fnmatchcase(path, pattern):
        return True
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return False


def _open_controls_for(controls: dict[str, Any], action: str) -> list[dict[str, Any]]:
    return [
        item
        for item in controls.get("controls") or []
        if isinstance(item, dict)
        and item.get("state") == "OPEN"
        and action in (item.get("blocks") or [])
    ]


def _owner_authorizes(controls: dict[str, Any], action: str) -> bool:
    for item in controls.get("controls") or []:
        if not isinstance(item, dict) or item.get("state") != "OPEN":
            continue
        if item.get("kind") != "OWNER":
            continue
        source = item.get("source") or {}
        if source.get("type") != "OWNER":
            continue
        if action in (item.get("permits") or []) and action not in (item.get("blocks") or []):
            return True
    return False


def _checkpoint_accepted(checkpoint: dict[str, Any] | None) -> bool:
    if not isinstance(checkpoint, dict):
        return False
    results = checkpoint.get("acceptance") or []
    return bool(results) and all(isinstance(item, dict) and item.get("result") == "PASS" for item in results)


def _quality_clear(checkpoint: dict[str, Any] | None) -> bool:
    return isinstance(checkpoint, dict) and (checkpoint.get("quality") or {}).get("result") == "CLEAR"


def _result(action: str, allowed: bool, basis: list[str], blocking_controls: list[str], reasons: list[str]) -> dict[str, Any]:
    result = {
        "schema_version": "relay-v3.1-authorization-result",
        "action": action,
        "allowed": allowed,
        "basis": list(dict.fromkeys(x for x in basis if x)),
        "blocking_controls": list(dict.fromkeys(blocking_controls)),
        "reason_codes": list(dict.fromkeys(reasons)) or ["ALLOW"],
    }
    errors = validate_schema("authorization-result", result, "AUTHORIZATION_RESULT")
    if errors:
        raise RuntimeError("; ".join(errors))
    return result


def _protocol_state(root: Path) -> tuple[bool, str]:
    selection_path = root / "relay/PROTOCOL_SELECTION.yaml"
    legacy_state = root / "agents/relay/REPO_STATE.yaml"
    if not selection_path.exists():
        if legacy_state.exists():
            return False, "V2_5:LEGACY_DEFAULT"
        return True, "V3_1:NATIVE_NO_SELECTOR"
    selection = load_yaml(selection_path)
    selected = str(selection.get("selected_protocol") or "")
    status = str(selection.get("status") or "")
    return selected == "V3_1" and status == "ACTIVE", f"{selected}:{status}"


def evaluate(
    root: Path,
    action: str,
    *,
    path: str | None = None,
    base_ref: str | None = None,
    expected_custody_epoch: int | None = None,
) -> dict[str, Any]:
    action = action.upper()
    if action not in ACTIONS:
        raise ValueError(f"unknown action: {action}")

    authority_errors = validate_authority(root)
    if authority_errors:
        return _result(
            action,
            False,
            ["authority validation failed", *authority_errors[:5]],
            [],
            ["INVALID_FOUNDATION"],
        )

    state, ep, lease, controls, checkpoint = _load_current(root)
    reasons: list[str] = []
    basis: list[str] = []
    live_v3, protocol_state = _protocol_state(root)
    basis.append(f"protocol:{protocol_state}")
    if action in LIVE_V3_ACTIONS and not live_v3:
        reasons.append("PROTOCOL_NOT_ACTIVE")
    blocking_controls: list[str] = []
    execution = state.get("execution") or {}
    current_epoch = execution.get("custody_epoch")
    if action in FENCED_ACTIONS and execution.get("lifecycle") in {"ACTIVE", "PARALLEL"} and current_epoch is not None:
        basis.append(f"custody_epoch:{current_epoch}")
        if expected_custody_epoch is None:
            reasons.append("CUSTODY_EPOCH_REQUIRED")
        elif int(expected_custody_epoch) != int(current_epoch):
            reasons.append("STALE_CUSTODY_EPOCH")

    if action in EXECUTION_ACTIONS:
        if execution.get("lifecycle") not in {"ACTIVE", "PARALLEL"} or not ep:
            reasons.append("NO_ACTIVE_EXECUTION")
        if not lease or lease.get("state") != "ACTIVE":
            reasons.append("NO_ACTIVE_LEASE")

    if action in WORK_CONTEXT_ACTIONS and not ep and not checkpoint:
        reasons.append("WORK_CONTEXT_REQUIRED")

    if lease and ep:
        if lease.get("route") != execution.get("route"):
            reasons.append("LEASE_ROUTE_MISMATCH")
        if (lease.get("basis") or {}).get("ep_id") != ep.get("id"):
            reasons.append("LEASE_EP_MISMATCH")
        if (lease.get("basis") or {}).get("material_base") != (ep.get("basis") or {}).get("material_base"):
            reasons.append("MATERIAL_BASIS_MISMATCH")
        if action in LEASE_ACTIONS and action not in ((lease.get("authority") or {}).get("actions") or []):
            reasons.append("ACTION_NOT_IN_LEASE_AUTHORITY")
        basis.extend([
            f"ep:{ep.get('id')}",
            f"lease:{lease.get('id')}",
            f"route:{execution.get('route')}",
            f"material_base:{(ep.get('basis') or {}).get('material_base')}",
        ])

    if action == "MATERIAL_WRITE":
        if not path:
            reasons.append("PATH_REQUIRED")
        elif ep:
            if not any(_matches(path, pattern) for pattern in ((ep.get("scope") or {}).get("write") or [])):
                reasons.append("PATH_OUTSIDE_EP_WRITE_SCOPE")
            if any(_matches(path, pattern) for pattern in ((ep.get("scope") or {}).get("protect") or [])):
                reasons.append("PATH_PROTECTED")
            basis.append(f"path:{path}")

    if action in {"MATERIAL_WRITE", "CHECKPOINT"}:
        if not base_ref:
            reasons.append("BASE_REF_REQUIRED")
        elif ep:
            try:
                material = inspect_material_basis(root, ep, base_ref)
            except Exception as exc:
                reasons.append("MATERIAL_BASIS_INVALID")
                basis.append(f"material_basis_error:{exc}")
            else:
                mb = material["material_basis"]
                drift = material["drift"]
                basis.extend([
                    f"material_head:{mb.get('head')}",
                    f"coordination_head:{(material.get('coordination_basis') or {}).get('head')}",
                    f"drift:{drift.get('classification')}",
                    f"base_ref:{base_ref}",
                ])
                if mb.get("ancestry_valid") is not True:
                    reasons.append("MATERIAL_BASIS_INVALID")
                if drift.get("classification") == "RELEVANT":
                    reasons.append("DRIFT_RELEVANT")
                elif drift.get("classification") == "UNKNOWN":
                    reasons.append("DRIFT_UNKNOWN")

    if action in CHECKPOINT_ACTIONS:
        if not _checkpoint_accepted(checkpoint):
            reasons.append("CHECKPOINT_REQUIRED" if checkpoint is None else "CHECKPOINT_NOT_ACCEPTED")
        elif checkpoint:
            basis.append(f"checkpoint:{checkpoint.get('id')}")

    if action in QUALITY_ACTIONS and not _quality_clear(checkpoint):
        reasons.append("QUALITY_NOT_CLEAR")

    if action in DELIVERY_VEHICLE_ACTIONS:
        delivery = state.get("delivery") or {}
        vehicle = delivery.get("primary_vehicle")
        if delivery.get("required") is not True or not isinstance(vehicle, dict):
            reasons.append("DELIVERY_VEHICLE_REQUIRED")
        elif action in {"DRAFT_PR_UPDATE", "PR_READY", "MERGE"} and vehicle.get("kind") != "PULL_REQUEST":
            reasons.append("DELIVERY_VEHICLE_REQUIRED")
        else:
            basis.append(
                f"delivery:{vehicle.get('provider')}:{vehicle.get('kind')}:{vehicle.get('number')}"
            )

    if action in DELIVERY_OWNER_ACTIONS:
        if lease and (lease.get("admission") or {}).get("method") == "OWNER_OVERRIDE":
            reasons.append("OWNER_OVERRIDE_DELIVERY_FORBIDDEN")
        if not _owner_authorizes(controls, action):
            reasons.append("OWNER_DELIVERY_AUTHORITY_REQUIRED")
        else:
            basis.append(f"owner_delivery_authority:{action}")

    blocking = _open_controls_for(controls, action)
    if blocking:
        blocking_controls = sorted(str(item.get("id")) for item in blocking)
        reasons.append("CONTROL_BLOCKS_ACTION")

    reasons = list(dict.fromkeys(reasons))
    allowed = not reasons
    return _result(action, allowed, basis, blocking_controls, ["ALLOW"] if allowed else reasons)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate one Engineering Relay V3.1 action against current authoritative state.")
    parser.add_argument("action", choices=sorted(ACTIONS))
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--path", help="Repository-relative material path for MATERIAL_WRITE.")
    parser.add_argument(
        "--base-ref",
        help="Current base branch/ref. MATERIAL_WRITE uses it to derive DISJOINT/RELEVANT/UNKNOWN drift mechanically.",
    )
    parser.add_argument("--expected-custody-epoch", type=int)
    args = parser.parse_args()
    result = evaluate(
        Path(args.repo_root).resolve(),
        args.action,
        path=args.path,
        base_ref=args.base_ref,
        expected_custody_epoch=args.expected_custody_epoch,
    )
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["allowed"] else 1)


if __name__ == "__main__":
    main()
