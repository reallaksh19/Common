#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from owner_publication import evaluate as evaluate_publication, load_cursor
from v3lib import load_yaml


DERIVED = "DERIVED_READ_MODEL"


def _counts(summary: dict[str, Any] | None, keys: list[str]) -> str:
    value = summary or {}
    total = value.get("total", 0)
    parts = [f"{key}={value.get(key, 0)}" for key in keys]
    return f"{', '.join(parts)}; total={total}"


def _items(values: Any) -> str:
    rows = [str(value) for value in (values or []) if str(value)]
    return "; ".join(rows) if rows else "none"


def _require_read_model(value: dict | None, *, schema_version: str, label: str) -> None:
    if value is None:
        return
    if value.get("authority") != DERIVED:
        raise ValueError(f"{label} must declare authority: {DERIVED}")
    if value.get("schema_version") != schema_version:
        raise ValueError(
            f"{label} must use schema_version {schema_version}, got {value.get('schema_version')}"
        )



def _change_lines(delta: dict[str, Any] | None) -> list[str]:
    if not delta:
        return []
    details = delta.get("details") or {}
    event = str(delta.get("event_class") or "UNKNOWN")
    changed = [str(x) for x in delta.get("changed_dimensions") or []]
    lines = [
        "## What changed",
        f"- Publication class: **{event}**",
        f"- Changed dimensions: {_items(changed)}",
    ]
    previous_at = delta.get("previous_published_at")
    if previous_at:
        lines.append(f"- Compared with Owner publication: **{previous_at}**")
    if event == "NO_MATERIAL_PROGRESS":
        lines.append("- No material, acceptance, evidence, delivery, roadmap, or next-work reporting dimension changed.")
    if event == "EVIDENCE_PROGRESS":
        lines.append("- Evidence changed without claiming task/acceptance completion.")
    if event == "IMPLEMENTATION_CHANGE":
        lines.append("- Material/implementation state changed without claiming acceptance movement.")

    for row in details.get("acceptance_transitions") or []:
        lines.append(
            f"- Acceptance {row.get('id')}: "
            f"{row.get('from_state') or 'absent'} → {row.get('to_state') or 'absent'}"
        )

    for label, key in (
        ("Programme progress", "programme_progress"),
        ("Accepted evidence coverage", "accepted_progress"),
        ("Roadmap revision", "roadmap_revision"),
        ("Material head", "material_head"),
        ("Checkpoint", "checkpoint"),
    ):
        value = details.get(key) or {}
        if value.get("from") != value.get("to"):
            lines.append(f"- {label}: {value.get('from')} → {value.get('to')}")
    lines.append("")
    return lines

def render(
    snapshot: dict,
    task_snapshot: dict | None = None,
    improvement_view: dict | None = None,
    publication_delta: dict[str, Any] | None = None,
) -> str:
    _require_read_model(
        snapshot,
        schema_version="relay-v3.1-snapshot",
        label="CURRENT_SNAPSHOT",
    )
    _require_read_model(
        task_snapshot,
        schema_version="relay-v3.1-task-snapshot",
        label="TASK_SNAPSHOT",
    )
    _require_read_model(
        improvement_view,
        schema_version="relay-v3.1-improvement-view",
        label="IMPROVEMENT_VIEW",
    )

    p = snapshot.get("programme") or {}
    e = snapshot.get("execution") or {}
    c = snapshot.get("controls") or {}
    d = snapshot.get("delivery") or {}
    n = snapshot.get("next") or {}
    o = snapshot.get("owner") or {}
    ev = snapshot.get("evidence") or {}
    h = snapshot.get("handoff") or {}

    lines = [
        "# V3.1 Owner / Task Status",
        "",
        f"Authority: **{snapshot.get('authority')}**",
        "Reporting surface: **CURRENT_SNAPSHOT + TASK_SNAPSHOT + IMPROVEMENT_VIEW**",
        "This report is derived; it does not grant execution, acceptance, delivery, or programme authority.",
        "",
    ]
    lines += _change_lines(publication_delta)
    lines += [
        "## Programme truth vs accepted evidence",
        f"- Roadmap revision: **{(snapshot.get('generated_from') or {}).get('roadmap_revision')}**",
        f"- Programme progress: **{p.get('programme_progress')}%**",
        f"- Accepted evidence coverage: **{p.get('accepted_progress')}%**",
        f"- Completed work: {_items(p.get('completed_work'))}",
        f"- Remaining work: {_items(p.get('remaining_work'))}",
        f"- Evidence-backed work: {_items(p.get('evidence_backed_work'))}",
        "",
        "## Outcome and current goal",
        f"- Outcome: {o.get('outcome') or 'Unknown'}",
        f"- Current goal: {o.get('current_goal') or 'Unknown'}",
        "",
        "## Current execution / custody",
        f"- Lifecycle: **{e.get('lifecycle')}**",
        f"- Work package: **{e.get('work_package') or 'NONE'}**",
        f"- EP: **{e.get('ep') or 'NONE'}**",
        f"- Lease: **{e.get('lease') or 'NONE'}**",
        f"- Custody epoch: **{e.get('custody_epoch') if e.get('custody_epoch') is not None else 'NONE'}**",
        f"- Executor: **{e.get('executor') or 'NONE'}**",
        "",
        "## Accepted truth",
        f"- Latest accepted checkpoint: **{ev.get('latest_checkpoint') or 'NONE'}**",
        f"- Latest material validation: {ev.get('latest_material_validation') or {}}",
        "",
    ]

    if task_snapshot:
        identity = task_snapshot.get("identity") or {}
        purpose = task_snapshot.get("purpose") or {}
        current = (task_snapshot.get("current_task_progress") or {}).get("summary") or {}
        parent = (task_snapshot.get("parent_issue_progress") or {}).get("summary") or {}
        next_task = task_snapshot.get("next") or {}
        lines += [
            "## Task-local completion",
            f"- Source protocol: **{task_snapshot.get('source_protocol')}**",
            f"- Work package / EP: **{identity.get('work_package') or 'NONE'} / {identity.get('ep') or 'NONE'}**",
            f"- Task outcome: {purpose.get('task_outcome') or 'Unknown'}",
            f"- Current task: {_counts(current, ['complete', 'partial', 'pending', 'blocked'])}",
            f"- Parent issue: {_counts(parent, ['complete', 'partial', 'pending', 'blocked', 'deferred', 'not_applicable', 'unknown'])}",
            f"- Offloads: {len(task_snapshot.get('offloads') or [])}",
            f"- Pending tracked items: {len(task_snapshot.get('pending_items') or [])}",
            f"- Known issues: {len(task_snapshot.get('known_issues') or [])}",
            f"- Task next action: {next_task.get('immediate_action') or 'none'}",
            f"- Task next value frontier: {next_task.get('next_value_frontier') or 'none'}",
            f"- Task stop conditions: {_items(next_task.get('stop_conditions'))}",
            "",
        ]

    lines += [
        "## Blockers by consequence",
        f"- Execution: {_items(c.get('execution_blockers'))}",
        f"- Handover: {_items(c.get('handover_blockers'))}",
        f"- Delivery: {_items(c.get('delivery_blockers'))}",
        f"- Informational: {_items(c.get('informational'))}",
        "",
    ]

    if improvement_view:
        improvement = improvement_view.get("improvement") or {}
        roadmap_effect = improvement_view.get("roadmap_effect") or {}
        lines += [
            "## Evidence-bound improvement",
            f"- Capability added: {_items(improvement.get('capability_added'))}",
            f"- Capability strengthened: {_items(improvement.get('capability_strengthened'))}",
            f"- Evidence added: {_items(improvement.get('evidence_added'))}",
            f"- Understanding improved: {_items(improvement.get('understanding_improved'))}",
            f"- Downstream unlocked: {_items(improvement.get('downstream_unlocked'))}",
            f"- Controls resolved: {_items(improvement.get('controls_resolved'))}",
            f"- Controls created: {_items(improvement.get('controls_created'))}",
            f"- Roadmap effect: {roadmap_effect}",
            f"- Not improved: {_items(improvement_view.get('not_improved'))}",
            f"- Still not proved: {_items(improvement_view.get('still_not_proved'))}",
            f"- New questions: {_items(improvement_view.get('new_questions'))}",
            "",
        ]

    lines += [
        "## Legal next boundary",
        f"- Material: {n.get('immediate_material_action') or 'none'}",
        f"- Delivery: {n.get('delivery_action') or 'none'}",
        f"- Stop conditions: {_items(n.get('stop_conditions'))}",
        "",
        "## Delivery",
        f"- PR: {d.get('pr') or 'none'}; Issue: {d.get('issue') or 'none'}; lifecycle: {d.get('lifecycle')}",
        f"- Merge authorized: **{'YES' if d.get('merge_authorized') else 'NO'}**",
        "",
        "## Reconstruction",
        f"- Zero-context takeover possible: **{'YES' if h.get('zero_context_takeover_possible') else 'NO'}**",
        f"- Project reconstruction sources: {_items(h.get('reconstruction_sources'))}",
    ]
    if task_snapshot:
        lines.append(
            f"- Task reconstruction sources: {_items(task_snapshot.get('reconstruction_sources'))}"
        )
    if improvement_view:
        lines.append(
            f"- Improvement reconstruction sources: {_items(improvement_view.get('reconstruction_sources'))}"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render V3.1 owner/task status from existing derived read models without creating new authority."
    )
    parser.add_argument("snapshot", help="Path to generated CURRENT_SNAPSHOT.yaml")
    parser.add_argument("--task-snapshot")
    parser.add_argument("--improvement-view")
    parser.add_argument(
        "--publication-cursor",
        help="Optional previous Owner publication cursor. Reporting metadata only; never authority.",
    )
    args = parser.parse_args()
    snapshot = load_yaml(Path(args.snapshot))
    task = load_yaml(Path(args.task_snapshot)) if args.task_snapshot else None
    improvement = load_yaml(Path(args.improvement_view)) if args.improvement_view else None
    delta = None
    if args.publication_cursor:
        cursor = load_cursor(Path(args.publication_cursor))
        delta = evaluate_publication(snapshot, task, improvement, cursor)
        delta.pop("current_baseline", None)
    print(render(snapshot, task, improvement, delta), end="")


if __name__ == "__main__":
    main()
