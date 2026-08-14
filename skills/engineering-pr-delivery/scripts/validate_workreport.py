#!/usr/bin/env python3
"""Lightweight structural validation for engineering PR work reports."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "# CURRENT STATE — READ THIS FIRST",
    "## Handover in 60 Seconds",
    "## Repository Ground Truth",
    "## Mission and Engineering Intent",
    "## Capability Status",
    "## Active Engineering Items",
    "## Validation Summary",
    "## Changed-File Ledger",
    "## Exact Next Action",
    "## Next-Agent Handover",
    "# HISTORICAL RECORD — DO NOT USE AS CURRENT STATE",
]

VALID_STATUSES = {"PASS", "FAIL", "NOT_RUN", "NOT_APPLICABLE"}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_workreport.py <workreport.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")
    if not re.search(r"Current HEAD\s*\|\s*[^|\n]+", text, re.IGNORECASE):
        errors.append("Current HEAD appears missing or empty")
    seen_statuses = set(re.findall(r"\b(?:PASS|FAIL|NOT_RUN|NOT_APPLICABLE)\b", text))
    if not seen_statuses:
        errors.append("no controlled validation status found")
    unknown = set(re.findall(r"\b[A-Z]+_[A-Z_]+\b", text)) - VALID_STATUSES
    # Unknown tokens are informational only; many are valid workflow states.
    if errors:
        print("WORKREPORT VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("WORKREPORT VALIDATION: PASS")
    print(f"Controlled validation statuses observed: {', '.join(sorted(seen_statuses))}")
    if unknown:
        print(f"Other controlled tokens observed: {', '.join(sorted(unknown))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
