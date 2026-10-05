#!/usr/bin/env python3
"""Validate that a pull request is represented by its owned issue Task Snapshot.

Reporting/reconstruction integrity only; this does not grant or deny execution.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

from live_protocol_basis import resolve as resolve_live_protocol_basis

OWNERSHIP_PATTERNS = (
    re.compile(r"(?im)\bIssue ownership remains\s+#(\d+)\b"),
    re.compile(r"(?im)\bOwned issue\s*:?\s*#(\d+)\b"),
    re.compile(r"(?im)\b(?:Closes|Fixes|Resolves)\s+#(\d+)\b"),
)

COORDINATION_PATH_PREFIXES = ("relay/",)
COORDINATION_PATHS = {".github/workflows/v3-relay.yml"}


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


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _coordination_only_since(root: Path, recorded_head: str | None, current_head: str) -> bool:
    if not recorded_head or recorded_head == current_head:
        return bool(recorded_head)
    ancestor = _git(root, "merge-base", "--is-ancestor", recorded_head, current_head)
    if ancestor.returncode != 0:
        return False
    diff = _git(root, "diff", "--name-only", f"{recorded_head}..{current_head}")
    if diff.returncode != 0:
        return False
    paths = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    if not paths:
        return True
    return all(
        path in COORDINATION_PATHS
        or any(path.startswith(prefix) for prefix in COORDINATION_PATH_PREFIXES)
        for path in paths
    )


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


def _protocol_basis_errors(
    task: dict[str, Any],
    *,
    expected_common_sha: str | None,
    expected_two_pass_revision: str | None,
) -> list[str]:
    if not expected_common_sha:
        return []
    basis = task.get("protocol_basis")
    if not isinstance(basis, dict):
        return ["Task Snapshot is missing protocol_basis required for live V3.1 freshness"]
    errors: list[str] = []
    if basis.get("protocol") != "V3.1":
        errors.append(f"Task Snapshot protocol_basis.protocol is {basis.get('protocol')!r}, expected 'V3.1'")
    if basis.get("common_sha") != expected_common_sha:
        errors.append(
            f"Task Snapshot Common basis {basis.get('common_sha')!r} is stale; live Common/main is {expected_common_sha}"
        )
    if expected_two_pass_revision and basis.get("two_pass_revision") != expected_two_pass_revision:
        errors.append(
            "Task Snapshot Two-Pass revision "
            f"{basis.get('two_pass_revision')!r} is stale; live revision is {expected_two_pass_revision}"
        )
    return errors


def validate_binding(
    root: Path,
    issue_number: int,
    pr_number: int,
    head_sha: str,
    *,
    expected_common_sha: str | None = None,
    expected_two_pass_revision: str | None = None,
) -> list[str]:
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
    protocol_failures: list[str] = []
    for path, task in candidates:
        task_protocol_errors = _protocol_basis_errors(
            task,
            expected_common_sha=expected_common_sha,
            expected_two_pass_revision=expected_two_pass_revision,
        )
        if task_protocol_errors:
            protocol_failures.extend(
                f"{path.relative_to(root)}: {error}" for error in task_protocol_errors
            )
            continue
        for row in _delivery_rows(task):
            if row.get("pr") != pr_number:
                continue
            represented.append(str(path.relative_to(root)))
            row_head = row.get("head")
            material_head = ((task.get("material") or {}).get("current_head"))
            for recorded_head in (row_head, material_head):
                if recorded_head == head_sha:
                    return []
                if _coordination_only_since(root, recorded_head, head_sha):
                    return []

    if protocol_failures:
        return [
            f"Task Snapshot for owned issue #{issue_number} is not on the live V3.1 protocol basis",
            *protocol_failures,
            "refresh Common/main, re-read the live V3.1/Two-Pass contract, then regenerate the issue-local Task Snapshot",
        ]

    if not represented:
        return [
            f"Task Snapshot for owned issue #{issue_number} does not represent PR #{pr_number}",
            "add the PR to delivery or delivery_stack[]",
        ]

    return [
        f"Task Snapshot for issue #{issue_number} represents PR #{pr_number} but not current material basis for head {head_sha}",
        f"matched snapshot(s): {', '.join(represented)}",
        "refresh the Task Snapshot; coordination-only commits after the recorded material head are allowed",
    ]


def validate_event(
    root: Path,
    event: dict[str, Any],
    *,
    expected_common_sha: str | None = None,
    expected_two_pass_revision: str | None = None,
) -> tuple[bool, list[str]]:
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

    errors = validate_binding(
        root,
        issue_number,
        pr_number,
        str(head_sha),
        expected_common_sha=expected_common_sha,
        expected_two_pass_revision=expected_two_pass_revision,
    )
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
    parser.add_argument(
        "--require-current-protocol-basis",
        action="store_true",
        help="Require the owned issue Task Snapshot to name this exact Common checkout and live Two-Pass revision.",
    )
    args = parser.parse_args()

    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    basis = resolve_live_protocol_basis() if args.require_current_protocol_basis else {}
    ok, messages = validate_event(
        Path(args.root),
        event,
        expected_common_sha=basis.get("common_sha"),
        expected_two_pass_revision=basis.get("two_pass_revision"),
    )
    for message in messages:
        print(message)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
