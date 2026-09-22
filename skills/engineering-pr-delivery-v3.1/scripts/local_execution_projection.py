from __future__ import annotations

import re
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


def _safe_token(value: Any) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "current")).strip("-")
    return text or "current"


def _steps(
    ep: dict[str, Any] | None,
    first_action: str | None,
    commands: list[str] | None,
) -> list[dict[str, Any]]:
    explicit = [str(x).strip() for x in (commands or []) if str(x).strip()]
    if explicit:
        return [{
            "id": f"STEP-CMD-{index}",
            "instruction": "Run this exact caller-supplied command and capture its result.",
            "command": command,
            "working_directory": ".",
            "expected_result": "Capture exit status and concise output; do not silently repair failures.",
        } for index, command in enumerate(explicit, 1)]

    result: list[dict[str, Any]] = []
    for ac in (ep or {}).get("acceptance") or []:
        if not isinstance(ac, dict):
            continue
        ac_id = str(ac.get("id") or f"AC-{len(result) + 1}")
        statement = str(ac.get("statement") or ac_id)
        for index, evidence in enumerate(ac.get("evidence_requirements") or [], 1):
            if not isinstance(evidence, dict):
                continue
            if evidence.get("test"):
                result.append({
                    "id": f"{ac_id}-TEST-{index}",
                    "instruction": f"Satisfy test evidence for {ac_id}: {statement}. Test requirement: {evidence['test']}",
                    "command": None,
                    "working_directory": ".",
                    "expected_result": "The required test evidence passes and its output is captured.",
                })
            elif evidence.get("oracle"):
                result.append({
                    "id": f"{ac_id}-ORACLE-{index}",
                    "instruction": f"Evaluate required oracle evidence for {ac_id}: {statement}",
                    "command": None,
                    "working_directory": ".",
                    "expected_result": str(evidence["oracle"]),
                })
    if not result:
        result.append({
            "id": "STEP-1",
            "instruction": str(first_action or "Execute the bounded local validation requested by the current EP."),
            "command": None,
            "working_directory": ".",
            "expected_result": "Return objective evidence for the bounded action without changing product state.",
        })
    return result


def build(
    root: Path,
    snapshot: dict[str, Any],
    ep: dict[str, Any] | None,
    checkpoint: dict[str, Any] | None,
    *,
    mode: str = "VALIDATE_ONLY",
    commands: list[str] | None = None,
) -> dict[str, Any]:
    if mode not in {"VALIDATE_ONLY", "BOUNDED_EXECUTION"}:
        raise ValueError(f"unsupported local execution mode: {mode}")

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

    branch = _branch(root)
    material = snapshot.get("material") or {}
    ep_id = (ep or {}).get("id") or execution.get("ep")
    work_package = (ep or {}).get("work_package") or execution.get("work_package")
    first_action = (
        (snapshot.get("next") or {}).get("immediate_material_action")
        or checkpoint_handoff.get("first_successor_action")
        or ((ep or {}).get("next") or {}).get("first_action")
    )
    material_head = str(material.get("head") or "")
    request_id = f"LOCAL-{_safe_token(ep_id or (checkpoint or {}).get('id'))}-{_safe_token(material_head[:12])}"

    prohibited = [
        "Do not commit or push.",
        "Do not advance PR, merge, release, or delivery state.",
        "Do not silently repair a failure; return the observed failure to the originating owner.",
    ]
    if mode == "VALIDATE_ONLY":
        prohibited.insert(0, "Do not modify product/source files.")

    stop_conditions = [
        "If git rev-parse HEAD does not equal request.exact_basis.material_head, stop immediately and return HEAD_MISMATCH.",
        *list((snapshot.get("next") or {}).get("stop_conditions") or []),
    ]

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
            "work_package": work_package,
        },
        "execution": {
            "ep": ep_id,
            "lease": execution.get("lease"),
            "executor": execution.get("executor"),
            "branch": branch,
        },
        "material": material,
        "scope": scope,
        "acceptance": list((ep or {}).get("acceptance") or []),
        "controls": snapshot.get("controls") or {},
        "checkpoint": {
            "id": (checkpoint or {}).get("id"),
            "handoff": (checkpoint or {}).get("handoff") if checkpoint else None,
        },
        "next": {
            "first_action": first_action,
            "stop_conditions": list((snapshot.get("next") or {}).get("stop_conditions") or []),
        },
        "request": {
            "id": request_id,
            "purpose": str(first_action or f"Perform bounded local evidence work for {ep_id or work_package or 'the current task'}."),
            "mode": mode,
            "exact_basis": {
                "material_head": material_head,
                "branch": branch,
                "work_package": work_package,
                "ep": ep_id,
            },
            "preflight": [
                "Fetch/check out the requested work and run git rev-parse HEAD.",
                "Compare the observed HEAD with request.exact_basis.material_head before running any validation step.",
                "If the HEAD differs, do not continue; return HEAD_MISMATCH with the observed HEAD.",
            ],
            "steps": _steps(ep, first_action, commands),
            "success_conditions": [
                "Every requested step is attempted on the exact material head or an explicit non-run status is returned.",
                "The result packet contains the required evidence fields and no unrequested product-state change is made.",
            ],
            "stop_conditions": stop_conditions,
            "prohibited_actions": prohibited,
        },
        "return_contract": {
            "request_id": request_id,
            "allowed_results": [
                "PASS",
                "FAIL",
                "BLOCKED",
                "NOT_RUN_ENVIRONMENT",
                "NOT_RUN_INFRASTRUCTURE",
                "HEAD_MISMATCH",
            ],
            "required_fields": [
                "observed_head",
                "environment",
                "command_results",
                "failures",
                "artifacts",
            ],
            "resume_owner": {
                "agent_id": execution.get("executor"),
                "responsibility": "The originating owner resumes responsibility after this bounded local result is returned; the helper does not inherit task custody.",
            },
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
