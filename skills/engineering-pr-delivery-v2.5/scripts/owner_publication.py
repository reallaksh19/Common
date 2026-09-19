from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from relaylib import load_yaml
from takeoverlib import digest_mapping, yaml_digest

OWNER_PUBLICATION_PATH = "agents/relay/publication/OWNER_PUBLICATION.yaml"

EVENT_CLASSES = {
    "INITIAL_SNAPSHOT",
    "TASK_PROGRESS",
    "TASK_REGRESSION",
    "IMPLEMENTATION_CHANGE",
    "EVIDENCE_PROGRESS",
    "DELIVERY_OR_CUSTODY_PROGRESS",
    "CONTROL_STATE_CHANGE",
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
        "checkpoint_id": checkpoint.get("id"),
        "summary": result.get("summary"),
        "completed_steps": _list(result.get("completed_steps")),
        "files_changed": _list(result.get("files_changed")),
    }


def normalize_report(report: dict) -> dict:
    progress = _mapping(report.get("progress"))
    current = _mapping(progress.get("current"))
    checkpoint = _mapping(report.get("checkpoint"))
    current_work = _mapping(report.get("current_work"))
    return {
        "task": {
            "acceptance": _acceptance_state(report),
            "progress_basis": copy.deepcopy(progress.get("progress_basis") or {}),
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
        "quality": {
            "plane": _mapping(report.get("quality")),
            "findings": _list(checkpoint.get("quality_findings")),
            "known_limitations": _list(checkpoint.get("known_limitations")),
        },
        "delivery_or_custody": {
            "projection": _mapping(report.get("projection")),
            "relay_readiness": _mapping(report.get("relay_readiness")),
            "takeover_admissions": _list(report.get("takeover_admissions")),
            "delivery": _mapping(report.get("delivery")),
        },
        "execution": _mapping(report.get("execution")),
        "stop": _mapping(report.get("stop")),
        "roadmap": {
            "summary": _mapping(report.get("roadmap_summary")),
            "reconciliation": _mapping(checkpoint.get("roadmap_reconciliation")),
        },
        "next_work": _mapping(report.get("next_work")),
        "issues": _list(current_work.get("issues")),
        "owner_decisions": _list(report.get("owner_decisions")),
    }


def _baseline(value: dict | None) -> dict | None:
    if value is None:
        return None
    if "task" in value and "evidence" in value and "roadmap" in value:
        return copy.deepcopy(value)
    return normalize_report(value)


def _acceptance_transitions(previous: dict, current: dict) -> list[dict]:
    old = {str(x.get("id")): x for x in previous["task"]["acceptance"]}
    new = {str(x.get("id")): x for x in current["task"]["acceptance"]}
    rows = []
    for key in sorted(set(old) | set(new)):
        before = old.get(key)
        after = new.get(key)
        if before == after:
            continue
        rows.append(
            {
                "id": key,
                "from_status": before.get("status") if before else None,
                "to_status": after.get("status") if after else None,
                "from_percent": before.get("percent") if before else None,
                "to_percent": after.get("percent") if after else None,
            }
        )
    return rows


def _details(previous: dict | None, current: dict) -> dict:
    if previous is None:
        return {
            "acceptance_transitions": [],
            "progress_basis": {"from": None, "to": copy.deepcopy(current["task"].get("progress_basis") or {})},
            "completed_steps": current["implementation"]["completed_steps"],
            "files_changed": current["implementation"]["files_changed"],
            "evidence_state": {"from": None, "to": current["evidence"]["plane"].get("state")},
            "roadmap_revision": {"from": None, "to": current["roadmap"]["summary"].get("revision")},
            "issue_change": bool(current["issues"]),
            "stop_change": bool(current["stop"].get("active")),
            "next_work_change": bool(current["next_work"]),
        }
    return {
        "acceptance_transitions": _acceptance_transitions(previous, current),
        "progress_basis": {
            "from": copy.deepcopy(previous["task"].get("progress_basis") or {}),
            "to": copy.deepcopy(current["task"].get("progress_basis") or {}),
        },
        "completed_steps": (
            current["implementation"]["completed_steps"]
            if previous["implementation"] != current["implementation"]
            else []
        ),
        "files_changed": (
            current["implementation"]["files_changed"]
            if previous["implementation"] != current["implementation"]
            else []
        ),
        "evidence_state": {
            "from": previous["evidence"]["plane"].get("state"),
            "to": current["evidence"]["plane"].get("state"),
        },
        "roadmap_revision": {
            "from": previous["roadmap"]["summary"].get("revision"),
            "to": current["roadmap"]["summary"].get("revision"),
        },
        "issue_change": previous["issues"] != current["issues"],
        "stop_change": previous["stop"] != current["stop"],
        "next_work_change": previous["next_work"] != current["next_work"],
    }


def diff_baselines(previous: dict | None, current: dict) -> dict:
    previous = _baseline(previous)
    current = _baseline(current) or {}
    if previous is None:
        dimensions = {
            "task": True,
            "implementation": bool(
                current["implementation"]["completed_steps"]
                or current["implementation"]["files_changed"]
                or current["implementation"]["summary"]
            ),
            "evidence": True,
            "quality": bool(current["quality"]["plane"] or current["quality"]["findings"]),
            "delivery_or_custody": True,
            "execution": True,
            "stop": bool(current["stop"].get("active")),
            "roadmap": True,
            "next_work": bool(current["next_work"]),
            "issues": bool(current["issues"]),
            "owner_decisions": bool(current["owner_decisions"]),
        }
        return {
            "initial": True,
            "previous": None,
            "current": current,
            "dimensions": dimensions,
            "details": _details(None, current),
        }

    execution_changed = previous["execution"] != current["execution"]
    waiting_or_monitoring = execution_changed and (
        current["execution"].get("state") == "WAITING"
        or not bool(current["execution"].get("can_continue"))
    )
    dimensions = {
        "task": previous["task"] != current["task"],
        "implementation": previous["implementation"] != current["implementation"],
        "evidence": previous["evidence"] != current["evidence"],
        "quality": previous["quality"] != current["quality"],
        "delivery_or_custody": previous["delivery_or_custody"] != current["delivery_or_custody"],
        "execution": execution_changed,
        "waiting_or_monitoring": waiting_or_monitoring,
        "stop": previous["stop"] != current["stop"],
        "roadmap": previous["roadmap"] != current["roadmap"],
        "next_work": previous["next_work"] != current["next_work"],
        "issues": previous["issues"] != current["issues"],
        "owner_decisions": previous["owner_decisions"] != current["owner_decisions"],
    }
    return {
        "initial": False,
        "previous": previous,
        "current": current,
        "dimensions": dimensions,
        "details": _details(previous, current),
    }


def diff_reports(previous_report: dict | None, current_report: dict) -> dict:
    previous = normalize_report(previous_report) if previous_report is not None else None
    return diff_baselines(previous, normalize_report(current_report))


def classify_baseline(previous: dict | None, current: dict) -> dict:
    diff = diff_baselines(previous, current)
    if diff["initial"]:
        event = "INITIAL_SNAPSHOT"
    else:
        prior = diff["previous"]
        now = diff["current"]
        previous_score = _accepted_score(prior["task"]["acceptance"])
        current_score = _accepted_score(now["task"]["acceptance"])
        if current_score > previous_score:
            event = "TASK_PROGRESS"
        elif current_score < previous_score:
            event = "TASK_REGRESSION"
        elif diff["dimensions"]["implementation"]:
            event = "IMPLEMENTATION_CHANGE"
        elif diff["dimensions"]["evidence"]:
            event = "EVIDENCE_PROGRESS"
        elif diff["dimensions"]["task"]:
            event = "CONTROL_STATE_CHANGE"
        elif diff["dimensions"]["delivery_or_custody"] or diff["dimensions"]["issues"]:
            event = "DELIVERY_OR_CUSTODY_PROGRESS"
        elif (
            diff["dimensions"]["quality"]
            or diff["dimensions"]["roadmap"]
            or diff["dimensions"]["next_work"]
            or diff["dimensions"]["stop"]
            or diff["dimensions"]["owner_decisions"]
        ):
            event = "CONTROL_STATE_CHANGE"
        elif diff["dimensions"]["waiting_or_monitoring"]:
            event = "WAITING_OR_MONITORING"
        elif diff["dimensions"]["execution"]:
            event = "CONTROL_STATE_CHANGE"
        else:
            event = "NO_MATERIAL_PROGRESS"

    changed = [name for name, value in diff["dimensions"].items() if value]
    return {
        "event_class": event,
        "changed_dimensions": changed,
        "publication_due": event != "NO_MATERIAL_PROGRESS",
        "current_digest": digest_mapping(diff["current"]),
        "details": diff["details"],
    }


def classify_change(previous_report: dict | None, current_report: dict) -> dict:
    previous = normalize_report(previous_report) if previous_report is not None else None
    return classify_baseline(previous, normalize_report(current_report))


def load_cursor(root: Path) -> dict | None:
    path = root / OWNER_PUBLICATION_PATH
    if not path.exists():
        return None
    return load_yaml(path)


def cursor_baseline(cursor: dict | None) -> dict | None:
    if not cursor:
        return None
    baseline = _mapping(cursor.get("baseline"))
    return _mapping(baseline.get("report")) or None


def publication_status(root: Path, report: dict) -> dict:
    cursor = load_cursor(root)
    previous = cursor_baseline(cursor)
    result = classify_baseline(previous, normalize_report(report))
    publication = _mapping((cursor or {}).get("publication"))
    result.update(
        {
            "previous_publication_id": publication.get("id"),
            "previous_sequence": publication.get("sequence"),
            "cursor_path": OWNER_PUBLICATION_PATH,
            "cursor_present": cursor is not None,
        }
    )
    return result


def make_cursor(
    report: dict,
    owner_view: str,
    change: dict,
    previous_cursor: dict | None = None,
) -> dict:
    prior = _mapping((previous_cursor or {}).get("publication"))
    sequence = int(prior.get("sequence") or 0) + 1
    baseline = normalize_report(report)
    report_digest = digest_mapping(report)
    return {
        "schema_version": "relay-v2.5-owner-publication",
        "publication": {
            "id": f"PUB-{sequence:04d}",
            "sequence": sequence,
            "event_class": change.get("event_class"),
            "changed_dimensions": list(change.get("changed_dimensions") or []),
            "owner_view_digest": digest_mapping({"text": owner_view}),
            "report_projection_digest": report_digest,
            "normalized_report_digest": digest_mapping(baseline),
        },
        "source": {
            "report_sources": copy.deepcopy(report.get("generated_from") or {}),
            "roadmap_revision": (report.get("roadmap_summary") or {}).get("revision"),
            "progress_basis": ((report.get("generated_from") or {}).get("progress_basis")),
            "checkpoint_id": ((report.get("generated_from") or {}).get("checkpoint_id")),
            "ep_id": ((report.get("generated_from") or {}).get("ep_id")),
        },
        "baseline": {
            "digest": digest_mapping(baseline),
            "report": baseline,
        },
    }


def cursor_digest(root: Path) -> str | None:
    path = root / OWNER_PUBLICATION_PATH
    return yaml_digest(path) if path.exists() else None
