from __future__ import annotations

import copy
import fnmatch
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from material_basis import inspect as inspect_material_basis, sensitivity
from v3lib import canonical_digest, load_yaml, validate_schema


DEFAULT_RECOVERY_AFTER_SECONDS = 300
MIN_RECOVERY_AFTER_SECONDS = 60
TERMINAL_SESSION_STATES = {"TERMINATED", "CANCELLED", "FAILED"}


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _matches(path: str, pattern: str) -> bool:
    path = path.replace("\\", "/").lstrip("./")
    pattern = pattern.replace("\\", "/").lstrip("./")
    if fnmatch.fnmatchcase(path, pattern):
        return True
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return False


def _worktree_digest(root: Path, patterns: list[str]) -> str:
    """Digest current tracked + untracked worktree content for sensitive paths.

    Unlike material_basis, this intentionally observes uncommitted work. It is
    liveness evidence only; it never becomes checkpoint/material authority.
    """

    raw = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
    )
    paths = sorted(
        {
            item
            for item in raw.decode("utf-8", errors="strict").split("\0")
            if item and any(_matches(item, pattern) for pattern in patterns)
        }
    )
    records: list[dict[str, Any]] = []
    for relative in paths:
        target = root / relative
        if not target.exists():
            records.append({"path": relative, "state": "MISSING"})
            continue
        if target.is_dir():
            continue
        records.append({
            "path": relative,
            "state": "PRESENT",
            "digest": "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest(),
        })
    return canonical_digest(records)


def material_activity_basis(root: Path, ep: dict[str, Any], base_ref: str) -> dict[str, Any]:
    inspected = inspect_material_basis(root, ep, base_ref)
    material = inspected.get("material_basis") or {}
    patterns, dependency_patterns = sensitivity(ep)
    return {
        "relevant_worktree_digest": _worktree_digest(root, patterns),
        "dependency_worktree_digest": _worktree_digest(root, dependency_patterns),
        "material_head": str(material.get("head") or ""),
        "base_ref": str(base_ref),
    }


def renew_copy(
    lease: dict[str, Any],
    *,
    renewed_at: str | None = None,
    activity_basis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(lease)
    custody = updated.get("custody") or {}
    next_at = renewed_at or _now()
    previous = str(custody.get("renewed_at") or "")
    if previous and _parse_timestamp(next_at) < _parse_timestamp(previous):
        raise ValueError("LEASE_RENEWAL_TIME_REGRESSION")
    custody["renewed_at"] = next_at
    if activity_basis is not None:
        custody["activity_basis"] = copy.deepcopy(activity_basis)
    updated["custody"] = custody
    return updated


def active_lease_renewal(
    root: Path,
    state: dict[str, Any],
    actor: str,
    *,
    base_ref: str | None = None,
    renewed_at: str | None = None,
) -> tuple[str, dict[str, Any]] | None:
    """Return an automatically renewed current lease for a governed actor action.

    Only the executor that owns current custody can renew it. This prevents Owner,
    provider-sync, helper, or successor activity from accidentally keeping a
    predecessor lease alive.
    """

    execution = state.get("execution") or {}
    if execution.get("lifecycle") != "ACTIVE":
        return None
    lease_id = execution.get("lease")
    ep_id = execution.get("ep")
    if not lease_id or not ep_id:
        return None

    lease_path = root / "relay/LEASES" / f"{lease_id}.yaml"
    if not lease_path.exists():
        return None
    lease = load_yaml(lease_path)
    if lease.get("state") != "ACTIVE":
        return None
    if str(((lease.get("executor") or {}).get("id") or "")) != str(actor):
        return None

    custody = lease.get("custody") or {}
    required_liveness = {
        "epoch",
        "granted_at",
        "renewed_at",
        "recovery_after_seconds",
        "recovery_policy",
    }
    if not required_liveness.issubset(custody):
        # Pre-liveness native leases remain readable. Do not partially upgrade
        # their custody shape as a side effect of an unrelated command.
        return None
    epoch = execution.get("custody_epoch")
    lease_epoch = custody.get("epoch")
    if epoch is not None and lease_epoch is not None and int(epoch) != int(lease_epoch):
        return None

    basis = None
    if base_ref:
        ep = load_yaml(root / "relay/WORK" / f"{ep_id}.yaml")
        basis = material_activity_basis(root, ep, base_ref)

    updated = renew_copy(lease, renewed_at=renewed_at, activity_basis=basis)
    return f"relay/LEASES/{lease_id}.yaml", updated


def validate_terminal_observation(
    lease: dict[str, Any],
    observation: dict[str, Any] | None,
) -> tuple[bool, str, str | None]:
    if observation is None:
        return False, "NO_TERMINAL_SESSION_EVIDENCE", None

    errors = validate_schema("recovery-observation", observation, "RECOVERY_OBSERVATION")
    if errors:
        return False, "TERMINAL_SESSION_EVIDENCE_INVALID", None

    custody = lease.get("custody") or {}
    if observation.get("lease_id") != lease.get("id"):
        return False, "TERMINAL_SESSION_LEASE_MISMATCH", None
    if str(observation.get("executor_id")) != str(((lease.get("executor") or {}).get("id") or "")):
        return False, "TERMINAL_SESSION_EXECUTOR_MISMATCH", None
    if int(observation.get("custody_epoch")) != int(custody.get("epoch") or -1):
        return False, "TERMINAL_SESSION_EPOCH_MISMATCH", None
    if str(observation.get("session_state")) not in TERMINAL_SESSION_STATES:
        return False, "TERMINAL_SESSION_NOT_TERMINAL", None

    observed_at = str(observation.get("observed_at") or "")
    renewed_at = str(custody.get("renewed_at") or "")
    if observed_at and renewed_at and _parse_timestamp(observed_at) < _parse_timestamp(renewed_at):
        return False, "TERMINAL_SESSION_EVIDENCE_STALE", None

    return True, "TERMINAL_SESSION_CONFIRMED", canonical_digest(observation)


def recovery_eligibility(
    root: Path,
    lease: dict[str, Any],
    *,
    ep: dict[str, Any] | None,
    base_ref: str | None,
    observed_at: str | None = None,
    terminal_observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return diagnostics for an explicit recovery takeover.

    Recorder-first V3.1 never blocks a successor because a predecessor lease is
    young, stale, or followed by unaccepted material activity. Those facts remain
    visible in the returned basis so reconstruction can account for them.
    """

    custody = lease.get("custody") or {}
    terminal, terminal_reason, terminal_digest = validate_terminal_observation(
        lease,
        terminal_observation,
    )
    if terminal:
        return {
            "eligible": True,
            "reason": terminal_reason,
            "basis": [
                str((terminal_observation or {}).get("provider_ref") or ""),
                str(terminal_digest or ""),
            ],
            "terminal_observation_digest": terminal_digest,
        }

    basis: list[str] = []
    renewed = str(custody.get("renewed_at") or "")
    seconds = int(custody.get("recovery_after_seconds") or 0)
    policy = str(custody.get("recovery_policy") or "")
    if policy:
        basis.append(f"recovery_policy:{policy}")
    if renewed:
        basis.append(f"renewed_at:{renewed}")
    if seconds:
        basis.append(f"recovery_after_seconds:{seconds}")

    if renewed and seconds:
        try:
            observed = _parse_timestamp(observed_at) if observed_at else datetime.now(timezone.utc)
            expires = _parse_timestamp(renewed).timestamp() + seconds
            if observed.timestamp() < expires:
                basis.append("advisory:PREDECESSOR_LEASE_NOT_EXPIRED")
            else:
                basis.append("advisory:INACTIVITY_HORIZON_EXPIRED")
        except Exception as exc:
            basis.append(f"advisory:RECOVERY_METADATA_INVALID:{exc}")
    elif custody:
        basis.append("advisory:RECOVERY_METADATA_INVALID")

    stored_basis = custody.get("activity_basis") or {}
    if stored_basis and isinstance(ep, dict) and base_ref:
        try:
            current_basis = material_activity_basis(root, ep, base_ref)
        except Exception as exc:
            basis.append(f"advisory:RECOVERY_MATERIAL_BASIS_UNKNOWN:{exc}")
        else:
            for key in ("relevant_worktree_digest", "dependency_worktree_digest"):
                if stored_basis.get(key) != current_basis.get(key):
                    basis.extend([
                        "advisory:UNACCEPTED_MATERIAL_ACTIVITY_PRESENT",
                        f"last_activity:{stored_basis.get(key)}",
                        f"current:{current_basis.get(key)}",
                    ])
                    break

    if terminal_observation is not None and terminal_reason != "NO_TERMINAL_SESSION_EVIDENCE":
        basis.append(f"advisory:{terminal_reason}")

    return {
        "eligible": True,
        "reason": "RECORDER_EXPLICIT_TAKEOVER",
        "basis": list(dict.fromkeys(x for x in basis if x)),
        "terminal_observation_digest": terminal_digest,
    }

