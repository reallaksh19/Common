#!/usr/bin/env python3
"""Derived Owner-publication delta reporting for Relay V3.1.

This module is reporting-only. It must never be imported by production
authorization, admission, recovery, checkpoint, handover, delivery, or closure
paths as a gate.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
from pathlib import Path
from typing import Any

import yaml

from v3lib import canonical_digest, load_yaml, validate_schema


DEFAULT_CURSOR = Path("relay/PUBLICATION/OWNER_STATUS.yaml")
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


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mapping(value: Any) -> dict[str, Any]:
    return copy.deepcopy(value) if isinstance(value, dict) else {}


def _rows(value: Any) -> list[Any]:
    return copy.deepcopy(value) if isinstance(value, list) else []


def _stable_task(task_snapshot: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(task_snapshot, dict):
        return None
    return {
        "identity": _mapping(task_snapshot.get("identity")),
        "purpose": _mapping(task_snapshot.get("purpose")),
        "parent_issue": _mapping(task_snapshot.get("parent_issue")),
        "parent_issue_progress": _mapping(task_snapshot.get("parent_issue_progress")),
        "current_task_progress": _mapping(task_snapshot.get("current_task_progress")),
        "acceptance": _rows(task_snapshot.get("acceptance")),
        "benchmarks": _rows(task_snapshot.get("benchmarks")),
        "benchmark_debt": _mapping(task_snapshot.get("benchmark_debt")),
        "pending_items": _rows(task_snapshot.get("pending_items")),
        "known_issues": _rows(task_snapshot.get("known_issues")),
        "offloads": _rows(task_snapshot.get("offloads")),
        "next": _mapping(task_snapshot.get("next")),
        "history": _mapping(task_snapshot.get("history")),
        "knowledge_state": _mapping(task_snapshot.get("knowledge_state")),
        "negative_knowledge": _rows(task_snapshot.get("negative_knowledge")),
        "preserve": _mapping(task_snapshot.get("preserve")),
    }


def _stable_improvement(improvement_view: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(improvement_view, dict):
        return None
    return {
        "task": improvement_view.get("task"),
        "checkpoint": improvement_view.get("checkpoint"),
        "from": _mapping(improvement_view.get("from")),
        "to": _mapping(improvement_view.get("to")),
        "improvement": _mapping(improvement_view.get("improvement")),
        "roadmap_effect": _mapping(improvement_view.get("roadmap_effect")),
        "not_improved": _rows(improvement_view.get("not_improved")),
        "still_not_proved": _rows(improvement_view.get("still_not_proved")),
        "new_questions": _rows(improvement_view.get("new_questions")),
    }


def normalize(
    snapshot: dict[str, Any],
    task_snapshot: dict[str, Any] | None = None,
    improvement_view: dict[str, Any] | None = None,
) -> dict[str, Any]:
    generated = snapshot.get("generated_from") or {}
    return {
        "programme": {
            "roadmap_revision": generated.get("roadmap_revision"),
            **_mapping(snapshot.get("programme")),
        },
        "owner": _mapping(snapshot.get("owner")),
        "execution": _mapping(snapshot.get("execution")),
        "material": _mapping(snapshot.get("material")),
        "evidence": _mapping(snapshot.get("evidence")),
        "controls": _mapping(snapshot.get("controls")),
        "delivery": _mapping(snapshot.get("delivery")),
        "project_next": _mapping(snapshot.get("next")),
        "task": _stable_task(task_snapshot),
        "improvement": _stable_improvement(improvement_view),
    }


def _criterion_map(baseline: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    task = ((baseline or {}).get("task") or {})
    rows = task.get("acceptance") or []
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        rid = row.get("id")
        if rid in {None, ""}:
            continue
        result[str(rid)] = copy.deepcopy(row)
    return result


def _acceptance_transitions(previous: dict[str, Any] | None, current: dict[str, Any]) -> list[dict[str, Any]]:
    before = _criterion_map(previous)
    after = _criterion_map(current)
    rows = []
    for rid in sorted(set(before) | set(after)):
        old = before.get(rid)
        new = after.get(rid)
        if old == new:
            continue
        rows.append({
            "id": rid,
            "from_state": (old or {}).get("state"),
            "to_state": (new or {}).get("state"),
            "from_evidence": (old or {}).get("evidence") or [],
            "to_evidence": (new or {}).get("evidence") or [],
        })
    return rows


def _progress_score(baseline: dict[str, Any] | None) -> tuple[float | None, float | None]:
    programme = ((baseline or {}).get("programme") or {})
    p = programme.get("programme_progress")
    a = programme.get("accepted_progress")
    return (
        float(p) if isinstance(p, (int, float)) else None,
        float(a) if isinstance(a, (int, float)) else None,
    )


def diff_baselines(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    if previous is None:
        return {
            "initial": True,
            "changed_dimensions": [
                "programme",
                "owner",
                "execution",
                "material",
                "evidence",
                "controls",
                "delivery",
                "project_next",
                "task",
                "improvement",
            ],
            "details": {
                "acceptance_transitions": [],
                "programme_progress": {"from": None, "to": _progress_score(current)[0]},
                "accepted_progress": {"from": None, "to": _progress_score(current)[1]},
                "roadmap_revision": {"from": None, "to": (current.get("programme") or {}).get("roadmap_revision")},
                "material_head": {"from": None, "to": (current.get("material") or {}).get("head")},
                "checkpoint": {"from": None, "to": (current.get("evidence") or {}).get("latest_checkpoint")},
            },
        }

    dimensions = [
        key for key in (
            "programme",
            "owner",
            "execution",
            "material",
            "evidence",
            "controls",
            "delivery",
            "project_next",
            "task",
            "improvement",
        )
        if previous.get(key) != current.get(key)
    ]
    before_programme, before_accepted = _progress_score(previous)
    after_programme, after_accepted = _progress_score(current)
    return {
        "initial": False,
        "changed_dimensions": dimensions,
        "details": {
            "acceptance_transitions": _acceptance_transitions(previous, current),
            "programme_progress": {"from": before_programme, "to": after_programme},
            "accepted_progress": {"from": before_accepted, "to": after_accepted},
            "roadmap_revision": {
                "from": (previous.get("programme") or {}).get("roadmap_revision"),
                "to": (current.get("programme") or {}).get("roadmap_revision"),
            },
            "material_head": {
                "from": (previous.get("material") or {}).get("head"),
                "to": (current.get("material") or {}).get("head"),
            },
            "checkpoint": {
                "from": (previous.get("evidence") or {}).get("latest_checkpoint"),
                "to": (current.get("evidence") or {}).get("latest_checkpoint"),
            },
        },
    }


def classify(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    diff = diff_baselines(previous, current)
    if diff["initial"]:
        event = "INITIAL_SNAPSHOT"
    else:
        before_programme, before_accepted = _progress_score(previous)
        after_programme, after_accepted = _progress_score(current)
        if (
            before_programme is not None
            and after_programme is not None
            and after_programme < before_programme
        ) or (
            before_accepted is not None
            and after_accepted is not None
            and after_accepted < before_accepted
        ) or any(
            row.get("from_state") == "PASS" and row.get("to_state") not in {"PASS", None}
            for row in diff["details"]["acceptance_transitions"]
        ):
            event = "TASK_REGRESSION"
        elif (
            before_programme is not None
            and after_programme is not None
            and after_programme > before_programme
        ) or (
            before_accepted is not None
            and after_accepted is not None
            and after_accepted > before_accepted
        ) or any(
            row.get("to_state") == "PASS" and row.get("from_state") != "PASS"
            for row in diff["details"]["acceptance_transitions"]
        ):
            event = "TASK_PROGRESS"
        elif "material" in diff["changed_dimensions"]:
            event = "IMPLEMENTATION_CHANGE"
        elif "evidence" in diff["changed_dimensions"] or (
            "improvement" in diff["changed_dimensions"] and "task" not in diff["changed_dimensions"]
        ):
            event = "EVIDENCE_PROGRESS"
        elif "delivery" in diff["changed_dimensions"] or "execution" in diff["changed_dimensions"]:
            event = "DELIVERY_OR_CUSTODY_PROGRESS"
        elif any(
            key in diff["changed_dimensions"]
            for key in ("controls", "owner", "programme", "project_next", "task", "improvement")
        ):
            event = "CONTROL_STATE_CHANGE"
        else:
            event = "NO_MATERIAL_PROGRESS"

        execution = current.get("execution") or {}
        if (
            event == "CONTROL_STATE_CHANGE"
            and execution.get("lifecycle") in {"IDLE", "INITIALIZING"}
            and "material" not in diff["changed_dimensions"]
        ):
            event = "WAITING_OR_MONITORING"

        if not diff["changed_dimensions"]:
            event = "NO_MATERIAL_PROGRESS"

    return {
        "schema_version": "relay-v3.1-owner-publication-delta",
        "authority": "DERIVED_REPORTING_VIEW",
        "event_class": event,
        "changed_dimensions": diff["changed_dimensions"],
        "details": diff["details"],
        "current_digest": canonical_digest(current),
    }


def load_cursor(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    cursor = load_yaml(path)
    errors = validate_schema("owner-publication-cursor", cursor, "OWNER_PUBLICATION_CURSOR")
    if errors:
        raise ValueError("; ".join(errors))
    return cursor


def evaluate(
    snapshot: dict[str, Any],
    task_snapshot: dict[str, Any] | None = None,
    improvement_view: dict[str, Any] | None = None,
    previous_cursor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current = normalize(snapshot, task_snapshot, improvement_view)
    previous = (previous_cursor or {}).get("baseline") if previous_cursor else None
    delta = classify(previous, current)
    delta["previous_sequence"] = (previous_cursor or {}).get("sequence")
    delta["previous_published_at"] = (previous_cursor or {}).get("published_at")
    delta["current_baseline"] = current
    return delta


def build_cursor(
    snapshot: dict[str, Any],
    task_snapshot: dict[str, Any] | None,
    improvement_view: dict[str, Any] | None,
    previous_cursor: dict[str, Any] | None,
    *,
    note: str | None = None,
) -> dict[str, Any]:
    baseline = normalize(snapshot, task_snapshot, improvement_view)
    cursor = {
        "schema_version": "relay-v3.1-owner-publication-cursor",
        "authority": "DERIVED_REPORTING_METADATA",
        "sequence": int((previous_cursor or {}).get("sequence") or 0) + 1,
        "published_at": _now(),
        "sources": {
            "snapshot_digest": canonical_digest(snapshot),
            "task_snapshot_digest": canonical_digest(task_snapshot) if task_snapshot else None,
            "improvement_view_digest": canonical_digest(improvement_view) if improvement_view else None,
        },
        "baseline": baseline,
        "note": note,
    }
    errors = validate_schema("owner-publication-cursor", cursor, "OWNER_PUBLICATION_CURSOR")
    if errors:
        raise ValueError("; ".join(errors))
    return cursor


def apply_cursor(path: Path, cursor: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(yaml.safe_dump(cursor, sort_keys=False), encoding="utf-8")
    tmp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate or record V3.1 Owner-reporting deltas. Reporting only; never production authority."
    )
    parser.add_argument("snapshot")
    parser.add_argument("--task-snapshot")
    parser.add_argument("--improvement-view")
    parser.add_argument("--cursor", default=str(DEFAULT_CURSOR))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--note")
    args = parser.parse_args()

    snapshot = load_yaml(Path(args.snapshot))
    task = load_yaml(Path(args.task_snapshot)) if args.task_snapshot else None
    improvement = load_yaml(Path(args.improvement_view)) if args.improvement_view else None
    cursor_path = Path(args.cursor)
    previous = load_cursor(cursor_path)

    result = evaluate(snapshot, task, improvement, previous)
    result.pop("current_baseline", None)

    if args.apply:
        cursor = build_cursor(snapshot, task, improvement, previous, note=args.note)
        apply_cursor(cursor_path, cursor)
        result["recorded_cursor"] = str(cursor_path)
        result["recorded_sequence"] = cursor["sequence"]

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
