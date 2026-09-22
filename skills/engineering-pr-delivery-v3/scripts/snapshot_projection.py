from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from material_basis import inspect as inspect_material_basis
from v3lib import canonical_digest, load_yaml, validate_schema
from validate_foundation import validate_authority


EXECUTION_ACTIONS = {"READ", "ANALYZE", "MATERIAL_WRITE", "TEST", "CHECKPOINT"}
HANDOVER_ACTIONS = {"HANDOVER", "LOCAL_EXECUTION_EXPORT"}
DELIVERY_ACTIONS = {"DRAFT_PR_UPDATE", "PR_READY", "MERGE", "RELEASE", "CLOSE_TASK"}


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _load_optional(path: Path) -> dict[str, Any] | None:
    return load_yaml(path) if path.exists() else None


def _accepted_checkpoint(cp: dict[str, Any]) -> bool:
    acceptance = cp.get("acceptance") or []
    return bool(acceptance) and all(
        isinstance(item, dict) and item.get("result") == "PASS" for item in acceptance
    ) and (cp.get("quality") or {}).get("result") == "CLEAR"


def _progress(
    root: Path,
    roadmap: dict[str, Any],
    *,
    checkpoint_override: dict[str, Any] | None = None,
    ep_override: dict[str, Any] | None = None,
) -> tuple[float, list[str], list[str]]:
    wp_rows = roadmap.get("work_packages") or []
    weights = {str(row.get("id")): float(row.get("weight") or 0) for row in wp_rows if isinstance(row, dict)}
    accepted: set[str] = set()
    cp_dir = root / "relay/CHECKPOINTS"
    for path in sorted(cp_dir.glob("CP-*.yaml")) if cp_dir.exists() else []:
        cp = load_yaml(path)
        if not isinstance(cp, dict) or not _accepted_checkpoint(cp):
            continue
        ep_id = cp.get("ep")
        ep_path = root / "relay/WORK" / f"{ep_id}.yaml"
        if not ep_path.exists():
            continue
        ep = load_yaml(ep_path)
        wp = str((ep or {}).get("work_package") or "")
        if wp in weights:
            accepted.add(wp)
    if checkpoint_override and _accepted_checkpoint(checkpoint_override):
        ep_id = checkpoint_override.get("ep")
        if ep_override and ep_override.get("id") == ep_id:
            ep = ep_override
        else:
            ep_path = root / "relay/WORK" / f"{ep_id}.yaml"
            ep = _load_optional(ep_path)
        wp = str((ep or {}).get("work_package") or "")
        if wp in weights:
            accepted.add(wp)
    total = sum(weights.values())
    earned = sum(weights[wp] for wp in accepted)
    percent = 0.0 if total <= 0 else round(earned * 100.0 / total, 2)
    order = [str(row.get("id")) for row in wp_rows if isinstance(row, dict)]
    completed = [wp for wp in order if wp in accepted]
    remaining = [wp for wp in order if wp not in accepted]
    return percent, completed, remaining


def _control_groups(controls: dict[str, Any]) -> dict[str, list[str]]:
    groups = {
        "execution_blockers": [],
        "handover_blockers": [],
        "delivery_blockers": [],
        "informational": [],
    }
    for item in controls.get("controls") or []:
        if not isinstance(item, dict) or item.get("state") != "OPEN":
            continue
        cid = str(item.get("id"))
        blocks = set(item.get("blocks") or [])
        classified = False
        if blocks & EXECUTION_ACTIONS:
            groups["execution_blockers"].append(cid)
            classified = True
        if blocks & HANDOVER_ACTIONS:
            groups["handover_blockers"].append(cid)
            classified = True
        if blocks & DELIVERY_ACTIONS:
            groups["delivery_blockers"].append(cid)
            classified = True
        if not classified:
            groups["informational"].append(cid)
    return groups


def _owner_merge_authorized(controls: dict[str, Any]) -> bool:
    return any(
        isinstance(item, dict)
        and item.get("state") == "OPEN"
        and item.get("kind") == "OWNER"
        and (item.get("source") or {}).get("type") == "OWNER"
        and "MERGE" in (item.get("permits") or [])
        and "MERGE" not in (item.get("blocks") or [])
        for item in controls.get("controls") or []
    )


def build(
    root: Path,
    base_ref: str | None = None,
    *,
    state_override: dict[str, Any] | None = None,
    roadmap_override: dict[str, Any] | None = None,
    ep_override: dict[str, Any] | None = None,
    lease_override: dict[str, Any] | None = None,
    checkpoint_override: dict[str, Any] | None = None,
    controls_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    authority_errors = validate_authority(root)
    if authority_errors:
        raise RuntimeError("invalid V3 authority: " + "; ".join(authority_errors[:8]))

    relay = root / "relay"
    state = state_override or load_yaml(relay / "STATE.yaml")
    roadmap_path = root / str((state.get("roadmap") or {}).get("path"))
    roadmap = roadmap_override or load_yaml(roadmap_path)
    roadmap_errors = validate_schema("roadmap", roadmap, "ROADMAP")
    if roadmap_errors:
        raise RuntimeError("invalid V3 roadmap: " + "; ".join(roadmap_errors[:8]))
    if roadmap.get("revision") != (state.get("roadmap") or {}).get("revision"):
        raise RuntimeError("ROADMAP revision disagrees with STATE.roadmap.revision")

    execution = state.get("execution") or {}
    ep_id = execution.get("ep")
    lease_id = execution.get("lease")
    checkpoint_id = (state.get("accepted") or {}).get("checkpoint")

    if ep_id and ep_override and ep_override.get("id") == ep_id:
        ep = ep_override
    else:
        ep = _load_optional(relay / "WORK" / f"{ep_id}.yaml") if ep_id else None

    if lease_id and lease_override and lease_override.get("id") == lease_id:
        lease = lease_override
    else:
        lease = _load_optional(relay / "LEASES" / f"{lease_id}.yaml") if lease_id else None

    if checkpoint_id and checkpoint_override and checkpoint_override.get("id") == checkpoint_id:
        checkpoint = checkpoint_override
    else:
        checkpoint = _load_optional(relay / "CHECKPOINTS" / f"{checkpoint_id}.yaml") if checkpoint_id else None

    controls = controls_override or load_yaml(root / str((state.get("controls") or {}).get("path")))

    coordination_head = _git(root, "rev-parse", "HEAD")
    if ep:
        if not base_ref:
            raise RuntimeError("active snapshot generation requires --base-ref for live material/drift inspection")
        inspected = inspect_material_basis(root, ep, base_ref)
        material_info = inspected["material_basis"]
        generated_material_basis = {
            "head": material_info["head"],
            "tree_digest": material_info["tree_digest"],
            "relevant_paths_digest": material_info["relevant_paths_digest"],
            "dependency_digest": material_info["dependency_digest"],
        }
        material = {
            "base": material_info["base"],
            "head": material_info["head"],
            "relevant_paths_digest": material_info["relevant_paths_digest"],
            "dependency_digest": material_info["dependency_digest"],
        }
    elif checkpoint:
        mr = checkpoint.get("material_result") or {}
        generated_material_basis = {
            "head": mr.get("head"),
            "tree_digest": canonical_digest(mr),
            "relevant_paths_digest": mr.get("relevant_paths_digest"),
            "dependency_digest": mr.get("dependency_digest"),
        }
        material = {
            "base": mr.get("head"),
            "head": mr.get("head"),
            "relevant_paths_digest": mr.get("relevant_paths_digest"),
            "dependency_digest": mr.get("dependency_digest"),
        }
    else:
        empty = canonical_digest([])
        generated_material_basis = {
            "head": coordination_head,
            "tree_digest": empty,
            "relevant_paths_digest": empty,
            "dependency_digest": empty,
        }
        material = {
            "base": coordination_head,
            "head": coordination_head,
            "relevant_paths_digest": empty,
            "dependency_digest": empty,
        }

    accepted_progress, completed_work, remaining_work = _progress(
        root,
        roadmap,
        checkpoint_override=checkpoint_override,
        ep_override=ep_override or ep,
    )
    scope = ep.get("scope") if ep else {}
    cp_validation = (checkpoint or {}).get("validation") or {}
    groups = _control_groups(controls)
    delivery = state.get("delivery") or {}
    vehicle = delivery.get("primary_vehicle") or {}
    wp = (ep or {}).get("work_package")
    executor = ((lease or {}).get("executor") or {}).get("id")

    reconstruction_sources = [
        str((state.get("roadmap") or {}).get("path")),
        "relay/STATE.yaml",
        str((state.get("controls") or {}).get("path")),
    ]
    if ep_id:
        reconstruction_sources.append(f"relay/WORK/{ep_id}.yaml")
    if lease_id:
        reconstruction_sources.append(f"relay/LEASES/{lease_id}.yaml")
    if checkpoint_id:
        reconstruction_sources.append(f"relay/CHECKPOINTS/{checkpoint_id}.yaml")

    snapshot = {
        "schema_version": "relay-v3-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "generated_from": {
            "roadmap_revision": roadmap.get("revision"),
            "state_digest": canonical_digest(state),
            "material_basis": generated_material_basis,
            "coordination_head": coordination_head,
        },
        "owner": {
            "outcome": (roadmap.get("owner") or {}).get("outcome"),
            "current_goal": (roadmap.get("owner") or {}).get("current_goal"),
        },
        "programme": {
            "accepted_progress": accepted_progress,
            "completed_work": completed_work,
            "remaining_work": remaining_work,
        },
        "execution": {
            "lifecycle": execution.get("lifecycle"),
            "work_package": wp,
            "ep": ep_id,
            "lease": lease_id,
            "executor": executor,
        },
        "scope": {
            "allowed_writes": list((scope or {}).get("write") or []),
            "protected": list((scope or {}).get("protect") or []),
            "prohibited": list((scope or {}).get("prohibit") or []),
        },
        "material": material,
        "evidence": {
            "latest_checkpoint": checkpoint_id,
            "latest_material_validation": cp_validation,
        },
        "controls": groups,
        "delivery": {
            "issue": vehicle.get("number") if vehicle.get("kind") == "ISSUE" else None,
            "pr": vehicle.get("number") if vehicle.get("kind") == "PULL_REQUEST" else None,
            "lifecycle": "DECLARED" if delivery.get("required") else "NOT_REQUIRED",
            "merge_authorized": _owner_merge_authorized(controls),
        },
        "next": {
            "immediate_material_action": ((ep or {}).get("next") or {}).get("first_action"),
            "delivery_action": (
                "Perform the explicitly authorized delivery transition."
                if delivery.get("required")
                else None
            ),
            "stop_conditions": list(((ep or {}).get("next") or {}).get("stop_conditions") or []),
        },
        "handoff": {
            "zero_context_takeover_possible": bool(roadmap and (ep or checkpoint) and reconstruction_sources),
            "reconstruction_sources": reconstruction_sources,
        },
    }
    errors = validate_schema("snapshot", snapshot, "CURRENT_SNAPSHOT")
    if errors:
        raise RuntimeError("; ".join(errors))
    return snapshot
