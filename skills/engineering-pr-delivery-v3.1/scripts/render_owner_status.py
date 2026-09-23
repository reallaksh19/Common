#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from v3lib import load_yaml


def _counts(summary: dict[str, Any] | None, keys: list[str]) -> str:
    value = summary or {}
    total = value.get("total", 0)
    parts = [f"{key}={value.get(key, 0)}" for key in keys]
    return f"{', '.join(parts)}; total={total}"


def render(
    snapshot: dict,
    task_snapshot: dict | None = None,
    improvement_view: dict | None = None,
) -> str:
    p = snapshot.get("programme") or {}
    e = snapshot.get("execution") or {}
    c = snapshot.get("controls") or {}
    d = snapshot.get("delivery") or {}
    n = snapshot.get("next") or {}
    o = snapshot.get("owner") or {}
    lines = [
        "# Owner Roadmap",
        "",
        f"Roadmap revision: **{(snapshot.get('generated_from') or {}).get('roadmap_revision')}**",
        f"Programme progress: **{p.get('programme_progress')}%**",
        f"Accepted evidence coverage: **{p.get('accepted_progress')}%**",
        "",
        "## Outcome",
        str(o.get("outcome") or "Unknown"),
        "",
        "## Current goal",
        str(o.get("current_goal") or "Unknown"),
        "",
        "## Current execution",
        f"- Lifecycle: **{e.get('lifecycle')}**",
        f"- Work package: **{e.get('work_package') or 'NONE'}**",
        f"- EP / lease: **{e.get('ep') or 'NONE'} / {e.get('lease') or 'NONE'}**",
        f"- Executor: **{e.get('executor') or 'NONE'}**",
        "",
    ]

    if task_snapshot:
        current = (task_snapshot.get("current_task_progress") or {}).get("summary") or {}
        parent = (task_snapshot.get("parent_issue_progress") or {}).get("summary") or {}
        lines += [
            "## Quantitative task status",
            f"- Current task: {_counts(current, ['complete', 'partial', 'pending', 'blocked'])}",
            f"- Parent issue: {_counts(parent, ['complete', 'partial', 'pending', 'blocked', 'deferred', 'not_applicable', 'unknown'])}",
            f"- Pending tracked items: {len(task_snapshot.get('pending_items') or [])}",
            f"- Known issues: {len(task_snapshot.get('known_issues') or [])}",
            "",
        ]

    if improvement_view:
        improvement = improvement_view.get("improvement") or {}
        lines += [
            "## Evidence-bound value added",
            f"- Capability added: {len(improvement.get('capability_added') or [])}",
            f"- Capability strengthened: {len(improvement.get('capability_strengthened') or [])}",
            f"- Evidence added: {len(improvement.get('evidence_added') or [])}",
            f"- Understanding improved: {len(improvement.get('understanding_improved') or [])}",
            f"- Downstream unlocked: {len(improvement.get('downstream_unlocked') or [])}",
            f"- Still not proved: {len(improvement_view.get('still_not_proved') or [])}",
            f"- New questions: {len(improvement_view.get('new_questions') or [])}",
            "",
        ]

    lines += [
        "## Blockers by consequence",
        f"- Execution: {', '.join(c.get('execution_blockers') or []) or 'none'}",
        f"- Handover: {', '.join(c.get('handover_blockers') or []) or 'none'}",
        f"- Delivery: {', '.join(c.get('delivery_blockers') or []) or 'none'}",
        f"- Informational: {', '.join(c.get('informational') or []) or 'none'}",
        "",
        "## Next",
        f"- Material: {n.get('immediate_material_action') or 'none'}",
        f"- Delivery: {n.get('delivery_action') or 'none'}",
        "",
        "## Delivery",
        f"- PR: {d.get('pr') or 'none'}; Issue: {d.get('issue') or 'none'}; lifecycle: {d.get('lifecycle')}",
        f"- Merge authorized: **{'YES' if d.get('merge_authorized') else 'NO'}**",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", help="Path to generated CURRENT_SNAPSHOT.yaml")
    parser.add_argument("--task-snapshot")
    parser.add_argument("--improvement-view")
    args = parser.parse_args()
    task = load_yaml(Path(args.task_snapshot)) if args.task_snapshot else None
    improvement = load_yaml(Path(args.improvement_view)) if args.improvement_view else None
    print(render(load_yaml(Path(args.snapshot)), task, improvement), end="")


if __name__ == "__main__":
    main()
