from __future__ import annotations

from typing import Any


ACTIVE_LIFECYCLES = {"ACTIVE", "PARALLEL"}
CURRENT_DISPOSITION = "NO_CHANGE"


def assess(task_snapshot: dict[str, Any]) -> dict[str, Any]:
    """Assess whether a handover may treat the current EP as a live programme frontier.

    This is intentionally a coordination-quality boundary, not an execution/write
    authorization gate. Repositories without a provider-backed parent issue are
    unaffected. Provider-backed active work must have a current parent observation
    and that observation must not indicate a terminal or changed programme contract.
    """

    execution = task_snapshot.get("execution") or {}
    lifecycle = str(execution.get("lifecycle") or "")
    parent = task_snapshot.get("parent_issue") or {}
    issue_number = parent.get("number")

    result = {
        "status": "CURRENT",
        "reason_codes": [],
        "lifecycle": lifecycle,
        "parent_issue": issue_number,
        "parent_state": parent.get("state"),
        "parent_disposition": parent.get("disposition"),
    }

    if lifecycle not in ACTIVE_LIFECYCLES or not issue_number:
        return result

    state = str(parent.get("state") or "UNKNOWN")
    disposition = str(parent.get("disposition") or "UNKNOWN")
    reasons: list[str] = []

    if state == "UNKNOWN":
        reasons.append("PARENT_PROVIDER_STATE_REQUIRED")
    elif state == "CLOSED":
        reasons.append("PARENT_ISSUE_TERMINAL")

    if disposition == "UNKNOWN":
        reasons.append("PARENT_DISPOSITION_REQUIRED")
    elif disposition != CURRENT_DISPOSITION:
        reasons.append("PARENT_DISPOSITION_CHANGED")

    if reasons:
        result["status"] = (
            "PROGRAMME_RECONCILIATION_REQUIRED"
            if any(code in {"PARENT_ISSUE_TERMINAL", "PARENT_DISPOSITION_CHANGED"} for code in reasons)
            else "PROGRAMME_CURRENTNESS_REQUIRED"
        )
        result["reason_codes"] = reasons

    return result


def require_handover_currentness(task_snapshot: dict[str, Any]) -> None:
    result = assess(task_snapshot)
    if result["status"] == "CURRENT":
        return

    parent = result.get("parent_issue")
    reasons = ",".join(result.get("reason_codes") or [])
    raise RuntimeError(
        f"{result['status']}: parent issue {parent} cannot be carried forward as the "
        f"current programme frontier ({reasons})"
    )
