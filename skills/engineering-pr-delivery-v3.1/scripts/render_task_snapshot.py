#!/usr/bin/env python3
"""Render the compact Owner-facing V3.1 Task Snapshot.

Reporting only. This module never grants or denies engineering execution.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from v3lib import load_yaml


def _items(values: Any) -> list[str]:
    return [str(value) for value in (values or []) if str(value)]


def _coverage(progress: dict[str, Any] | None) -> str:
    if not progress:
        return "UNKNOWN — no mapped denominator"
    coverage = progress.get("coverage") or {}
    percent = coverage.get("percent")
    total = coverage.get("applicable_total")
    satisfied = coverage.get("satisfied")
    basis = coverage.get("basis")
    if percent is None or not total:
        return "UNKNOWN — no mapped denominator"
    if basis == "DECLARED_WEIGHTS":
        return f"{satisfied:g}/{total:g} declared weight satisfied — {percent:g}%"
    return f"{satisfied:g}/{total:g} criteria satisfied — {percent:g}% unweighted coverage"


def _legacy_coverage(progress: dict[str, Any] | None) -> str:
    summary = (progress or {}).get("summary") or {}
    total = int(summary.get("total") or 0)
    if not total:
        return "UNKNOWN — legacy snapshot has no denominator"
    complete = int(summary.get("complete") or 0)
    return f"{complete}/{total} legacy-complete — {round(100.0 * complete / total, 1):g}%"


def _progress_line(task: dict[str, Any], key: str, legacy_key: str | None = None) -> str:
    progress = task.get(key)
    if progress is not None:
        return _coverage(progress)
    if legacy_key:
        return _legacy_coverage(task.get(legacy_key))
    return "UNKNOWN — no mapped denominator"


def _axis_state(task: dict[str, Any], key: str, fallback: str = "UNKNOWN") -> str:
    completion = task.get("completion") or {}
    return str(completion.get(key) or fallback)


def _acceptance_axis(progress: dict[str, Any] | None) -> str:
    coverage = (progress or {}).get("coverage") or {}
    total = coverage.get("applicable_total")
    percent = coverage.get("percent")
    summary = (progress or {}).get("summary") or {}
    if not total or percent is None:
        return "UNKNOWN"
    if percent == 100:
        return "SATISFIED"
    if (coverage.get("satisfied") or 0) > 0 or summary.get("partial", 0) > 0:
        return "PARTIAL"
    return "OPEN"


def _bullet_section(lines: list[str], title: str, values: Any, empty: str = "none") -> None:
    rows = _items(values)
    lines += ["", f"### {title}"]
    if rows:
        lines.extend(f"- {row}" for row in rows)
    else:
        lines.append(f"- {empty}")


def render(task: dict[str, Any]) -> str:
    if task.get("authority") != "DERIVED_READ_MODEL":
        raise ValueError("TASK_SNAPSHOT must declare authority: DERIVED_READ_MODEL")
    if task.get("schema_version") != "relay-v3.1-task-snapshot":
        raise ValueError("TASK_SNAPSHOT must use schema_version relay-v3.1-task-snapshot")

    protocol_basis = task.get("protocol_basis") or {}
    identity = task.get("identity") or {}
    work = task.get("parent_issue") or {}
    programme = task.get("programme_parent") or {}
    planning = task.get("planning") or {}
    expected = planning.get("expected_next_observable") or {}
    material = task.get("material") or {}
    delivery = task.get("delivery") or {}
    delivery_stack = [
        row for row in (task.get("delivery_stack") or []) if isinstance(row, dict)
    ]
    completion = task.get("completion") or {}
    verification = task.get("verification") or {}
    nxt = task.get("next") or {}

    overall = str(completion.get("overall_state") or "UNKNOWN")
    headline = str(
        completion.get("headline")
        or f"{work.get('repository') or 'unknown'}#{work.get('number') or 'unknown'} {overall}"
    )

    lines = [
        "## Task Snapshot",
        "",
        f"**{headline}**",
        "",
        f"- Protocol basis: {protocol_basis.get('protocol') or 'UNKNOWN'}"
        + (f" — Common@{protocol_basis.get('common_sha')}" if protocol_basis.get("common_sha") else "")
        + (f" — {protocol_basis.get('two_pass_revision')}" if protocol_basis.get("two_pass_revision") else ""),
        f"- Programme: {programme.get('repository') or 'unknown'}#{programme.get('number') or 'NONE'}"
        + (f" — {programme.get('title')}" if programme.get("title") else ""),
        f"- Work issue: {work.get('repository') or 'unknown'}#{work.get('number') or 'NONE'}"
        + (f" — {work.get('title')}" if work.get("title") else "")
        + f" [{work.get('state') or 'UNKNOWN'}]",
        f"- Work package / EP: {identity.get('work_package') or 'NONE'} / {identity.get('ep') or 'NONE'}",
        f"- Plan: {planning.get('state') or 'UNKNOWN'}"
        + (f" rev {planning.get('revision')}" if planning.get("revision") is not None else "")
        + (f" — {planning.get('provider_ref')}" if planning.get("provider_ref") else ""),
        f"- Material: base={material.get('base') or delivery.get('base') or 'unknown'}; "
        f"head={material.get('current_head') or delivery.get('head') or 'unknown'}",
        f"- Delivery: {delivery.get('lifecycle') or _axis_state(task, 'delivery')}"
        + (f" — PR #{delivery.get('pr')}" if delivery.get("pr") else ""),
        f"- Expected next observable: {expected.get('statement') or 'none'}",
        "",
        "### Completion matrix",
        "",
        "| Axis | State | Coverage / detail |",
        "| --- | --- | --- |",
        f"| Implementation plan | {_axis_state(task, 'implementation')} | {_progress_line(task, 'plan_progress')} |",
        f"| Child/work-issue acceptance | {_axis_state(task, 'work_issue_acceptance')} | {_progress_line(task, 'work_issue_progress', 'parent_issue_progress')} |",
        f"| Current task / EP acceptance | {_acceptance_axis(task.get('task_acceptance_progress'))} | {_progress_line(task, 'task_acceptance_progress', 'current_task_progress')} |",
        f"| Verification | {verification.get('state') or _axis_state(task, 'verification')} | failure origins: "
        + (", ".join(f"{k}={v}" for k, v in sorted((verification.get('failure_origins') or {}).items())) or "none") + " |",
        f"| Delivery | {_axis_state(task, 'delivery', str(delivery.get('lifecycle') or 'UNKNOWN'))} | {delivery.get('lifecycle') or 'UNKNOWN'} |",
        f"| Programme contribution | {_axis_state(task, 'programme_contribution')} | {_progress_line(task, 'programme_progress')} |",
        f"| Provider issue | {_axis_state(task, 'provider_issue', str(work.get('state') or 'UNKNOWN'))} | {work.get('state') or 'UNKNOWN'} |",
    ]

    if delivery_stack:
        lines += [
            "",
            "### Delivery stack",
            "",
            "| Relationship | PR | Lifecycle | Base | Head | Note |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for row in delivery_stack:
            pr_label = f"#{row.get('pr')}" if row.get("pr") else "-"
            lines.append(
                f"| {row.get('relationship') or 'RELATED'} | {pr_label} | "
                f"{row.get('lifecycle') or 'UNKNOWN'} | {row.get('base') or '-'} | "
                f"{row.get('head') or '-'} | {row.get('note') or '-'} |"
            )

    _bullet_section(lines, "What is done", completion.get("what_done"), "none proved by the current acceptance denominator")
    _bullet_section(lines, "What remains", completion.get("what_remains"), "none on the mapped child/task acceptance criteria")
    _bullet_section(lines, "Dependencies / external causes", completion.get("dependencies"), "none")
    _bullet_section(lines, "Needs you", completion.get("owner_decisions"), "NONE")

    lines += [
        "",
        "### Next",
        f"- Immediate action: {nxt.get('immediate_action') or 'none'}",
        f"- Next value frontier: {nxt.get('next_value_frontier') or 'none'}",
        "",
        "> Reporting note: implementation, verification, delivery, child acceptance and programme completion are independent axes. "
        "This snapshot is derived reporting context, not engineering permission.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a compact Owner-facing V3.1 Task Snapshot.")
    parser.add_argument("task_snapshot")
    args = parser.parse_args()
    print(render(load_yaml(Path(args.task_snapshot))), end="")


if __name__ == "__main__":
    main()
