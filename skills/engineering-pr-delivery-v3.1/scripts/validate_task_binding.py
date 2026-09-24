#!/usr/bin/env python3
"""Validate that a pull request is represented by its owned issue Task Snapshot.

Reporting/reconstruction integrity only; this does not grant or deny execution.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

OWNERSHIP_PATTERNS = (
    re.compile(r"(?im)\bIssue ownership remains\s+#(\d+)\b"),
    re.compile(r"(?im)\bOwned issue\s*:?\s*#(\d+)\b"),
    re.compile(r"(?im)\b(?:Closes|Fixes|Resolves)\s+#(\d+)\b"),
)


def owned_issue_from_body(body: str | None) -> int | None:
    text = body or ""
    for pattern in OWNERSHIP_PATTERNS:
        match = pattern.search(text)
        if match:
            return int(match.group(1))
    return None


def _load_snapshot(path: Path) -> dict[str, Any] | None:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _issue_number(task: dict[str, Any]) -> int | None:
    number = ((task.get("parent_issue") or {}).get("number"))
    if isinstance(number, int):
        return number
    number = ((task.get("identity") or {}).get("issue"))
    return number if isinstance(number, int) else None


def _delivery_rows(task: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    primary = task.get("delivery")
    if isinstance(primary, dict) and isinstance(primary.get("pr"), int):
        rows.append({"relationship": "PRIMARY", **primary})
    rows.extend(
        dict(row)
        for row in (task.get("delivery_stack") or [])
        if isinstance(row, dict) and isinstance(row.get("pr"), int)
    )
    return rows


def validate_binding(root: Path, issue_number: int, pr_number: int, head_sha: str) -> list[str]:
    task_dir = root / "relay/GENERATED/tasks"
    candidates: list[tuple[Path, dict[str, Any]]] = []
    if task_dir.exists():
        for path in sorted(task_dir.glob("*.snapshot.yaml")):
            task = _load_snapshot(path)
            if task and _issue_number(task) == issue_number:
                candidates.append((path, task))

    if not candidates:
        return [
            f"owned issue #{issue_number} has no Task Snapshot under relay/GENERATED/tasks",
            "publish/regenerate an issue-local Task Snapshot before treating Relay CI as task-current",
        ]

    represented: list[str] = []
    for path, task in candidates:
        for row in _delivery_rows(task):
            if row.get("pr") != pr_number:
                continue
            represented.append(str(path.relative_to(root)))
            row_head = row.get("head")
            if row_head == head_sha:
                return []
            material_head = ((task.get("material") or {}).get("current_head"))
            if row_head in {None, ""} and material_head == head_sha:
                return []

    if not represented:
        return [
            f"Task Snapshot for owned issue #{issue_number} does not represent PR #{pr_number}",
            "add the PR to delivery or delivery_stack[]",
        ]

    return [
        f"Task Snapshot for issue #{issue_number} represents PR #{pr_number} but not exact head {head_sha}",
        f"matched snapshot(s): {', '.join(represented)}",
        "refresh the Task Snapshot from current provider/material state",
    ]


def validate_event(root: Path, event: dict[str, Any]) -> tuple[bool, list[str]]:
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        return True, ["SKIP: event is not pull_request"]

    issue_number = owned_issue_from_body(pr.get("body"))
    if issue_number is None:
        return True, ["SKIP: PR body has no explicit owned-issue marker"]

    pr_number = pr.get("number") or event.get("number")
    head_sha = ((pr.get("head") or {}).get("sha"))
    if not isinstance(pr_number, int) or not head_sha:
        return False, ["pull_request event is missing PR number or head SHA"]

    errors = validate_binding(root, issue_number, pr_number, str(head_sha))
    if errors:
        return False, errors
    return True, [
        f"PASS: issue #{issue_number} Task Snapshot represents PR #{pr_number} at {head_sha}"
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate PR -> owned issue -> Task Snapshot -> exact-head binding."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--event", required=True, help="GitHub event JSON path")
    args = parser.parse_args()

    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    ok, messages = validate_event(Path(args.root), event)
    for message in messages:
        print(message)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
