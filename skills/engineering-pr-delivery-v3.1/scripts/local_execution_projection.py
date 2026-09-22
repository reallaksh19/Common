from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from v3lib import canonical_digest, validate_schema


def _branch(root: Path) -> str:
    value = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
        text=True,
    ).strip()
    return value or "DETACHED"


def build(
    root: Path,
    snapshot: dict[str, Any],
    ep: dict[str, Any] | None,
    checkpoint: dict[str, Any] | None,
) -> dict[str, Any]:
    execution = snapshot.get("execution") or {}
    checkpoint_handoff = (checkpoint or {}).get("handoff") or {}
    ep_scope = (ep or {}).get("scope") or {}
    snapshot_scope = snapshot.get("scope") or {}
    scope = snapshot_scope
    if ep is not None and execution.get("ep") is None:
        scope = {
            "allowed_writes": list(ep_scope.get("write") or []),
            "protected": list(ep_scope.get("protect") or []),
            "prohibited": list(ep_scope.get("prohibit") or []),
        }
    package = {
        "schema_version": "relay-v3.1-local-execution",
        "authority": "DERIVED_EXECUTION_PACKAGE",
        "generated_from": {
            "state_digest": (snapshot.get("generated_from") or {}).get("state_digest"),
            "snapshot_digest": canonical_digest(snapshot),
        },
        "project": {
            "outcome": (snapshot.get("owner") or {}).get("outcome"),
            "roadmap_revision": (snapshot.get("generated_from") or {}).get("roadmap_revision"),
            "work_package": (ep or {}).get("work_package") or execution.get("work_package"),
        },
        "execution": {
            "ep": (ep or {}).get("id") or execution.get("ep"),
            "lease": execution.get("lease"),
            "executor": execution.get("executor"),
            "branch": _branch(root),
        },
        "material": snapshot.get("material") or {},
        "scope": scope,
        "acceptance": list((ep or {}).get("acceptance") or []),
        "controls": snapshot.get("controls") or {},
        "checkpoint": {
            "id": (checkpoint or {}).get("id"),
            "handoff": (checkpoint or {}).get("handoff") if checkpoint else None,
        },
        "next": {
            "first_action": (
                (snapshot.get("next") or {}).get("immediate_material_action")
                or checkpoint_handoff.get("first_successor_action")
                or ((ep or {}).get("next") or {}).get("first_action")
            ),
            "stop_conditions": list((snapshot.get("next") or {}).get("stop_conditions") or []),
        },
        "delivery_boundary": {
            "merge_authorized": bool((snapshot.get("delivery") or {}).get("merge_authorized")),
            "delivery_lifecycle": str((snapshot.get("delivery") or {}).get("lifecycle") or "UNKNOWN"),
        },
    }
    errors = validate_schema("local-execution", package, "LOCAL_EXECUTION")
    if errors:
        raise RuntimeError("; ".join(errors))
    return package
