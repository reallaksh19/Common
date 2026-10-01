#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from lease_liveness import DEFAULT_RECOVERY_AFTER_SECONDS, material_activity_basis
from v3lib import canonical_digest, load_yaml, require_identifier, validate_schema
from validate_foundation import validate_authority


NORMAL_ACTIONS = [
    "READ",
    "ANALYZE",
    "MATERIAL_WRITE",
    "TEST",
    "CHECKPOINT",
    "HANDOVER",
    "LOCAL_EXECUTION_EXPORT",
    "DRAFT_PR_UPDATE",
]
OWNER_OVERRIDE_ACTIONS = [
    "READ",
    "ANALYZE",
    "MATERIAL_WRITE",
    "TEST",
    "DRAFT_PR_UPDATE",
]


class AdmissionError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _current(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    errors = validate_authority(root)
    if errors:
        raise AdmissionError("invalid V3 authority: " + "; ".join(errors[:8]))
    state = load_yaml(root / "relay/STATE.yaml")
    execution = state.get("execution") or {}
    ep_id = execution.get("ep")
    if not ep_id:
        raise AdmissionError("no active EP is available for admission")
    ep = load_yaml(root / "relay/WORK" / f"{ep_id}.yaml")
    current_lease = None
    lease_id = execution.get("lease")
    if lease_id:
        current_lease = load_yaml(root / "relay/LEASES" / f"{lease_id}.yaml")
    return state, ep, current_lease


def _qualification_required(ep: dict[str, Any]) -> bool:
    policy = ep.get("admission_policy") or {}
    return policy.get("qualification") == "REQUIRED"


def build_native_lease(
    root: Path,
    *,
    lease_id: str,
    executor_id: str,
    method: str,
    qualification: dict[str, Any] | None = None,
    owner_basis: dict[str, str] | None = None,
    branch: str | None = None,
    replace_active_lease_id: str | None = None,
    state_override: dict[str, Any] | None = None,
    ep_override: dict[str, Any] | None = None,
    current_lease_override: dict[str, Any] | None = None,
    custody_epoch: int | None = None,
    recovery_after_seconds: int = DEFAULT_RECOVERY_AFTER_SECONDS,
    recovery_policy: str = "TAKEOVER_AFTER_EXPIRY",
    base_ref: str | None = None,
) -> dict[str, Any]:
    if state_override is not None or ep_override is not None:
        if not isinstance(state_override, dict) or not isinstance(ep_override, dict):
            raise AdmissionError("state_override and ep_override must be supplied together")
        state, ep, current_lease = state_override, ep_override, current_lease_override
    else:
        state, ep, current_lease = _current(root)
    method = method.upper()
    if method not in {"DETERMINISTIC", "QUALIFIED", "OWNER_OVERRIDE"}:
        raise AdmissionError(f"unsupported admission method: {method}")
    try:
        require_identifier(lease_id, "LEASE-", "lease_id")
    except ValueError as exc:
        raise AdmissionError(str(exc)) from exc
    if not executor_id.strip():
        raise AdmissionError("executor_id must be explicit")

    current_lease_id = str((current_lease or {}).get("id") or "")
    current_executor = str(((current_lease or {}).get("executor") or {}).get("id") or "")
    # Recorder-first V3.1 does not use an existing executor as an admission gate.
    # The next transaction records whichever executor becomes current.

    required = _qualification_required(ep)

    if method == "QUALIFIED" and isinstance(qualification, dict):
        qset = str(qualification.get("qset") or "").strip()
        evaluator = str(qualification.get("evaluator") or "").strip()
        evidence = [str(x) for x in qualification.get("evidence") or [] if str(x).strip()]
        complete = bool(qset and evaluator and evidence)
        q = {
            "required": bool(complete),
            "qset": qset or None,
            "evaluator": evaluator or None,
            "result": "PASS" if complete else None,
            "evidence": evidence,
        }
    else:
        # EP qualification policy is preserved as historical intent only. It may
        # be reported by projections, but it cannot stop the recorder from
        # assigning the next executor.
        q = {
            "required": False,
            "qset": None,
            "evaluator": None,
            "result": None,
            "evidence": [],
        }

    execution = state.get("execution") or {}
    if recovery_after_seconds < 60:
        raise AdmissionError("recovery_after_seconds must be at least 60")
    if recovery_policy not in {"MANUAL_ONLY", "TAKEOVER_AFTER_EXPIRY"}:
        raise AdmissionError("unsupported recovery_policy")
    if custody_epoch is None:
        current_epoch = execution.get("custody_epoch")
        if current_epoch is None:
            current_epoch = ((current_lease or {}).get("custody") or {}).get("epoch") or 0
        custody_epoch = int(current_epoch) + 1
    if custody_epoch < 1:
        raise AdmissionError("custody_epoch must be positive")
    now = _now()
    ep_basis = ep.get("basis") or {}
    lease: dict[str, Any] = {
        "schema_version": "relay-v3.1-lease",
        "id": lease_id,
        "route": execution.get("route"),
        "executor": {"id": executor_id},
        "basis": {
            "ep_id": ep.get("id"),
            "ep_digest": canonical_digest(ep),
            "material_base": ep_basis.get("material_base"),
            "predecessor_checkpoint": ep_basis.get("predecessor_checkpoint"),
            "protocol_basis": ep_basis.get("protocol_basis"),
        },
        "authority": {
            "actions": list(OWNER_OVERRIDE_ACTIONS if method == "OWNER_OVERRIDE" else NORMAL_ACTIONS)
        },
        "admission": {
            "method": method,
            "result": "PASS",
            "repository_only": method != "OWNER_OVERRIDE",
            "qualification": q,
        },
        "custody": {
            "epoch": int(custody_epoch),
            "granted_at": now,
            "renewed_at": now,
            "recovery_after_seconds": int(recovery_after_seconds),
            "recovery_policy": recovery_policy,
        },
        "state": "ACTIVE",
        "invalidation": {"reasons": []},
    }

    if base_ref:
        lease["custody"]["activity_basis"] = material_activity_basis(root, ep, base_ref)

    if method == "OWNER_OVERRIDE":
        if not isinstance(owner_basis, dict):
            raise AdmissionError("OWNER_OVERRIDE requires direct Owner basis")
        utterance = str(owner_basis.get("direct_utterance_digest") or "").strip()
        timestamp = str(owner_basis.get("session_timestamp") or "").strip()
        if not utterance or not timestamp:
            raise AdmissionError("OWNER_OVERRIDE requires direct_utterance_digest and session_timestamp")
        if not branch:
            raise AdmissionError("OWNER_OVERRIDE requires a bounded branch")
        lease["admission"]["owner_basis"] = {
            "direct_utterance_digest": utterance,
            "session_timestamp": timestamp,
        }
        scope = ep.get("scope") or {}
        lease["scope"] = {
            "ep_or_task": str(ep.get("id")),
            "branch": branch,
            "allowed_writes": list(scope.get("write") or []),
            "prohibited": list(scope.get("prohibit") or []) + ["MERGE", "RELEASE"],
        }

    errors = validate_schema("lease", lease, "LEASE")
    if errors:
        raise AdmissionError("; ".join(errors))
    return lease


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build one native V3 lease admission object. Transactional activation is owned by relay_tx.py."
    )
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--lease-id", required=True)
    parser.add_argument("--executor-id", required=True)
    parser.add_argument("--method", choices=["DETERMINISTIC", "QUALIFIED", "OWNER_OVERRIDE"], required=True)
    parser.add_argument("--qualification", help="YAML file containing qset/evaluator/evidence for QUALIFIED admission.")
    parser.add_argument("--owner-utterance-digest")
    parser.add_argument("--owner-session-timestamp")
    parser.add_argument("--branch")
    args = parser.parse_args()

    qualification = load_yaml(Path(args.qualification)) if args.qualification else None
    owner_basis = None
    if args.method == "OWNER_OVERRIDE":
        owner_basis = {
            "direct_utterance_digest": args.owner_utterance_digest,
            "session_timestamp": args.owner_session_timestamp,
        }

    lease = build_native_lease(
        Path(args.repo_root).resolve(),
        lease_id=args.lease_id,
        executor_id=args.executor_id,
        method=args.method,
        qualification=qualification,
        owner_basis=owner_basis,
        branch=args.branch,
    )
    print(yaml.safe_dump(lease, sort_keys=False), end="")


if __name__ == "__main__":
    main()
