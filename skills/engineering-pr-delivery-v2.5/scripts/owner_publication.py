from __future__ import annotations

from typing import Any

from takeoverlib import digest_mapping

EVENT_CLASSES = {
    "INITIAL_SNAPSHOT",
    "TASK_PROGRESS",
    "TASK_REGRESSION",
    "IMPLEMENTATION_CHANGE",
    "EVIDENCE_PROGRESS",
    "DELIVERY_OR_CUSTODY_PROGRESS",
    "WAITING_OR_MONITORING",
    "NO_MATERIAL_PROGRESS",
}


def _mapping(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _acceptance_state(report: dict) -> list[dict]:
    rows = []
    for item in _list(report.get("acceptance")):
        if not isinstance(item, dict):
            continue
        rows.append(
            {
                "id": item.get("id"),
                "status": item.get("status"),
                "percent": item.get("percent"),
                "basis": item.get("basis") or [],
            }
        )
    return sorted(rows, key=lambda x: str(x.get("id")))


def _accepted_score(rows: list[dict]) -> float:
    total = 0.0
    for row in rows:
        value = row.get("percent")
        if isinstance(value, (int, float)):
            total += float(value)
        elif row.get("status") == "COMPLETE":
            total += 100.0
    return total


def _implementation_state(report: dict) -> dict:
    checkpoint = _mapping(report.get("checkpoint"))
    result = _mapping(checkpoint.get("implementation_result"))
    return {
        "summary": result.get("summary"),
        "completed_steps": _list(result.get("completed_steps")),
        "files_changed": _list(result.get("files_changed")),
    }


def normalize_report(report: dict) -> dict:
    progress = _mapping(report.get("progress"))
    current = _mapping(progress.get("current"))
    checkpoint = _mapping(report.get("checkpoint"))
    return {
        "task": {
            "acceptance": _acceptance_state(report),
            "overall_percent": progress.get("overall_percent"),
            "phase_percent": current.get("phase_percent"),
            "work_package_percent": current.get("work_package_percent"),
            "ep_percent": current.get("ep_percent"),
        },
        "implementation": _implementation_state(report),
        "evidence": {
            "plane": _mapping(report.get("evidence")),
            "validation_results": _list(checkpoint.get("validation_results")),
        },
        "delivery_or_custody": {
            "projection": _mapping(report.get("projection")),
            "relay_readiness": _mapping(report.get("relay_readiness")),
            "takeover_admissions": _list(report.get("takeover_admissions")),
        },
        "execution": _mapping(report.get("execution")),
        "stop": _mapping(report.get("stop")),
        "roadmap": {
            "summary": _mapping(report.get("roadmap_summary")),
            "reconciliation": _mapping(checkpoint.get("roadmap_reconciliation")),
        },
        "next_work": _mapping(report.get("next_work")),
        "issues": _mapping(report.get("issue_summary")),
    }


def diff_reports(previous_report: dict | None, current_report: dict) -> dict:
    current = normalize_report(current_report)
    if previous_report is None:
        return {
            "initial": True,
            "previous": None,
            "current": current,
            "dimensions": {
                "task": True,
                "implementation": bool(
                    current["implementation"]["completed_steps"]
                    or current["implementation"]["files_changed"]
                    or current["implementation"]["summary"]
                ),
                "evidence": True,
                "delivery_or_custody": True,
                "waiting_or_monitoring": current["execution"].get("state") == "WAITING",
                "roadmap": True,
                "next_work": True,
                "issues": True,
            },
        }

    previous = normalize_report(previous_report)
    task_changed = previous["task"] != current["task"]
    implementation_changed = previous["implementation"] != current["implementation"]
    evidence_changed = previous["evidence"] != current["evidence"]
    delivery_changed = previous["delivery_or_custody"] != current["delivery_or_custody"]
    execution_changed = previous["execution"] != current["execution"] or previous["stop"] != current["stop"]
    waiting = execution_changed and (
        current["execution"].get("state") == "WAITING"
        or not bool(current["execution"].get("can_continue"))
    )
    return {
        "initial": False,
        "previous": previous,
        "current": current,
        "dimensions": {
            "task": task_changed,
            "implementation": implementation_changed,
            "evidence": evidence_changed,
            "delivery_or_custody": delivery_changed,
            "waiting_or_monitoring": waiting,
            "roadmap": previous["roadmap"] != current["roadmap"],
            "next_work": previous["next_work"] != current["next_work"],
            "issues": previous["issues"] != current["issues"],
        },
    }


def classify_change(previous_report: dict | None, current_report: dict) -> dict:
    diff = diff_reports(previous_report, current_report)
    if diff["initial"]:
        event = "INITIAL_SNAPSHOT"
    else:
        previous = diff["previous"]
        current = diff["current"]
        previous_score = _accepted_score(previous["task"]["acceptance"])
        current_score = _accepted_score(current["task"]["acceptance"])
        if current_score > previous_score:
            event = "TASK_PROGRESS"
        elif current_score < previous_score:
            event = "TASK_REGRESSION"
        elif diff["dimensions"]["implementation"]:
            event = "IMPLEMENTATION_CHANGE"
        elif diff["dimensions"]["evidence"]:
            event = "EVIDENCE_PROGRESS"
        elif diff["dimensions"]["delivery_or_custody"] or diff["dimensions"]["issues"]:
            event = "DELIVERY_OR_CUSTODY_PROGRESS"
        elif diff["dimensions"]["waiting_or_monitoring"]:
            event = "WAITING_OR_MONITORING"
        else:
            event = "NO_MATERIAL_PROGRESS"

    changed = [name for name, value in diff["dimensions"].items() if value]
    return {
        "event_class": event,
        "changed_dimensions": changed,
        "publication_due": event != "NO_MATERIAL_PROGRESS",
        "current_digest": digest_mapping(diff["current"]),
    }
