#!/usr/bin/env python3
"""Compare Git changed files with the work-report changed-file ledger."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def git_files(base: str) -> set[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", f"{base}...HEAD"], text=True
    )
    return {line.strip() for line in out.splitlines() if line.strip()}


def ledger_files(text: str) -> set[str]:
    files: set[str] = set()
    in_ledger = False
    for line in text.splitlines():
        if line.startswith("## Changed-File Ledger"):
            in_ledger = True
            continue
        if in_ledger and line.startswith("## "):
            break
        if not in_ledger or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"File", "---", ""} or set(cells[0]) <= {"-", ":"}:
            continue
        candidate = cells[0].strip("`")
        if "/" in candidate or "." in Path(candidate).name:
            files.add(candidate)
    return files


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: reconcile_changed_files.py <base-ref> <workreport.md>", file=sys.stderr)
        return 2
    base, report = sys.argv[1], Path(sys.argv[2])
    if not report.is_file():
        print(f"FAIL: work report not found: {report}")
        return 1
    actual = git_files(base)
    ledger = ledger_files(report.read_text(encoding="utf-8"))
    missing = sorted(actual - ledger)
    extra = sorted(ledger - actual)
    print(f"Actual changed files: {len(actual)}")
    print(f"Ledger files: {len(ledger)}")
    if missing:
        print("Missing from ledger:")
        for item in missing:
            print(f"- {item}")
    if extra:
        print("Ledger entries not in diff:")
        for item in extra:
            print(f"- {item}")
    if missing or extra:
        print("CHANGED-FILE RECONCILIATION: FAIL")
        return 1
    print("CHANGED-FILE RECONCILIATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
