#!/usr/bin/env python3
"""Render detailed Owner statistics from existing Relay read models.

This is a read-only presentation surface. It creates no execution, programme,
provider, checkpoint, or delivery authority.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from v3lib import load_yaml


_MARK = {
    "COMPLETE": "[x]",
    "PASS": "[x]",
    "LANDED": "[x]",
    "READY_TO_CLOSE": "[x]",
    "PARTIAL": "[~]",
    "PENDING": "[ ]",
    "STILL_REAL": "[ ]",
    "BLOCKED": "[!]",
    "CLOSED_WITH_DEBT": "[!]",
    "DEFERRED": "[-]",
    "TRANSFERRED": "[-]",
    "SPLIT": "[-]",
    "SUPERSEDED": "[-]",
    "NOT_APPLICABLE": "[-]",
    "UNKNOWN": "[?]",
}


def _mark(state: Any) -> str:
    return _MARK.get(str(state or "UNKNOWN").upper(), "[?]")


def _checklist(lines: list[str], title: str, rows: list[dict[str, Any]]) -> None:
    lines.extend(["", f"## {title}"])
    if not rows:
        lines.append("- none")
        return
    for row in rows:
        state = str(row.get("state") or row.get("ownership") or "UNKNOWN")
        rid = row.get("id") or row.get("ref") or row.get("ep") or "item"
        statement = row.get("statement") or row.get("title") or row.get("work_package") or ""
        lines.append(f"- {_mark(state)} **{rid}** — {state}: {statement}")
        evidence = list(row.get("evidence") or [])
        if evidence:
            lines.append(f"  - Evidence: {', '.join(str(x) for x in evidence)}")


def render(
    snapshot: dict[str, Any],
    task_snapshot: dict[str, Any],
    programme_reconciliation: dict[str, Any],
    handover_ledger: dict[str, Any] | None = None,
) -> str:
    owner = snapshot.get("owner") or {}
    programme = snapshot.get("programme") or {}
    execution = snapshot.get("execution") or {}
    recon = programme_reconciliation or {}
    task = task_snapshot or {}
    ledger = handover_ledger or {}

    lines = [
        "# Engineering Relay V3.1 — Detailed Stats",
        "",
        "> Read-only Owner view. Checklist state is derived from repository authority and supplied live provider observations.",
        "",
        "## Programme",
        f"- Outcome: {owner.get('outcome') or 'unknown'}",
        f"- Current goal: {owner.get('current_goal') or 'unknown'}",
        f"- Roadmap revision: {(snapshot.get('generated_from') or {}).get('roadmap_revision') or 'unknown'}",
        f"- Programme progress: {programme.get('programme_progress')}%",
        f"- Accepted evidence coverage: {programme.get('accepted_progress')}%",
        f"- Current EP / lease: {execution.get('ep') or 'NONE'} / {execution.get('lease') or 'NONE'}",
        "",
        "## Programme classification",
        f"- Programme frontier: {recon.get('programme_frontier') or []}",
        f"- Execution blocked: {recon.get('execution_blocked') or []}",
        f"- Acceptance debt: {recon.get('acceptance_debt') or []}",
        f"- Delivery / governance debt: {recon.get('delivery_governance_debt') or []}",
        f"- Deferred / future: {recon.get('deferred_or_future') or []}",
    ]

    _checklist(lines, "Parent / sub-issue programme set", list(recon.get("parents") or []))
    _checklist(
        lines,
        "Governing parent issue acceptance",
        list((task.get("parent_issue_progress") or {}).get("checklist") or []),
    )
    _checklist(
        lines,
        "Current task acceptance",
        list((task.get("current_task_progress") or {}).get("checklist") or []),
    )

    lines.extend(["", "## EP / sub-work index"])
    ep_index = list(ledger.get("ep_index") or [])
    if not ep_index:
        lines.append("- none")
    else:
        for row in ep_index:
            status = row.get("status") or "UNKNOWN"
            lines.append(
                f"- {_mark(status)} **{row.get('ep')}** / {row.get('work_package')} — "
                f"{status}; continuation={row.get('continuation')}; "
                f"checkpoint={row.get('checkpoint') or 'none'}; lease={row.get('lease') or 'none'}"
            )

    for title, key in (
        ("Pending items", "pending_items"),
        ("Known issues", "known_issues"),
        ("Delegated / local work", "offloads"),
    ):
        lines.extend(["", f"## {title}"])
        rows = list(task.get(key) or ledger.get(key) or [])
        if not rows:
            lines.append("- none")
        else:
            for row in rows:
                if isinstance(row, dict):
                    rid = row.get("id") or row.get("control_ref") or row.get("origin_ep") or "item"
                    state = row.get("status") or row.get("state") or "OPEN"
                    statement = row.get("statement") or row.get("task") or ""
                    lines.append(f"- {_mark(state)} **{rid}** — {state}: {statement}")
                else:
                    lines.append(f"- [ ] {row}")

    accepted = ledger.get("accepted_truth") or {}
    material = ledger.get("material") or {}
    lines.extend([
        "",
        "## Material / acceptance",
        f"- Accepted checkpoint: {accepted.get('checkpoint') or (snapshot.get('evidence') or {}).get('latest_checkpoint') or 'none'}",
        f"- Accepted head: {accepted.get('accepted_head') or 'unknown'}",
        f"- Working head: {material.get('working_head') or (snapshot.get('material') or {}).get('head') or 'unknown'}",
        f"- Unaccepted material status: {material.get('status') or 'UNKNOWN'}",
        "",
        "## Next",
        f"- Reconciled first programme frontier: {(recon.get('programme_frontier') or [None])[0] or 'none'}",
        f"- Current material action: {(snapshot.get('next') or {}).get('immediate_material_action') or 'none'}",
        f"- Delivery action: {(snapshot.get('next') or {}).get('delivery_action') or 'none'}",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render detailed point-wise Relay stats.")
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--task-snapshot", required=True)
    parser.add_argument("--programme-reconciliation", required=True)
    parser.add_argument("--handover-ledger")
    args = parser.parse_args()
    print(
        render(
            load_yaml(Path(args.snapshot)),
            load_yaml(Path(args.task_snapshot)),
            load_yaml(Path(args.programme_reconciliation)),
            load_yaml(Path(args.handover_ledger)) if args.handover_ledger else None,
        ),
        end="",
    )


if __name__ == "__main__":
    main()
