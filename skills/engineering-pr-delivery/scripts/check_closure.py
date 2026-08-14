#!/usr/bin/env python3
"""Run structural work-report and changed-file closure checks."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(args: list[str]) -> int:
    print("$", " ".join(args))
    return subprocess.call(args)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: check_closure.py <base-ref> <workreport.md>", file=sys.stderr)
        return 2
    base, report = sys.argv[1], sys.argv[2]
    here = Path(__file__).resolve().parent
    python = sys.executable
    results = [
        run([python, str(here / "validate_workreport.py"), report]),
        run([python, str(here / "reconcile_changed_files.py"), base, report]),
    ]
    if any(results):
        print("CLOSURE STRUCTURAL CHECK: BLOCKED")
        return 1
    print("CLOSURE STRUCTURAL CHECK: PASS")
    print("Note: engineering validation and release authorization still require substantive review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
