#!/usr/bin/env python3
"""Scan repository selector text for active Relay paths under Local v1.1 activation.

The scanner is intentionally narrow: it reads selector/configuration surfaces, not
historical prose. A lower-precedence repository/global selector may conflict with
the Owner-selected Local stack; that conflict is reported and overridden. Unknown
or contradictory higher-authority selectors remain fatal in version_guard.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ACTIVE_RELAY = "skills/engineering-pr-delivery-v3.5"
OLD_RELAY_RE = re.compile(
    r"skills/engineering-pr-delivery-v(?:2(?:[.]5)?|3[.]0|3[.]1|3[.]2|3(?![.][0-9]))(?=/|\b)(?:/SKILL[.]md|/)?"
)
V35_RE = re.compile(r"skills/engineering-pr-delivery-v3[.]5(?=/|\b)(?:/SKILL[.]md|/)?")


class SelectorScanError(ValueError):
    pass


def _paths(pattern: re.Pattern[str], text: str) -> list[str]:
    normalized = []
    for match in pattern.findall(text):
        value = match.rstrip("/")
        if value.endswith("/SKILL.md"):
            value = value[: -len("/SKILL.md")]
        if value not in normalized:
            normalized.append(value)
    return normalized


def scan_selector_text(text: str, *, source: str, source_level: str = "REPOSITORY_SELECTOR") -> dict[str, Any]:
    source_level = source_level.upper()
    if source_level not in {"REPOSITORY_SELECTOR", "GLOBAL_SELECTOR"}:
        raise SelectorScanError("Text selector scanner is only for lower-precedence repository/global selectors")
    old = _paths(OLD_RELAY_RE, text)
    active = _paths(V35_RE, text)
    findings = [
        {
            "source": source,
            "source_level": source_level,
            "selected_path": path,
            "resolution": "OVERRIDDEN_BY_OWNER_STACK_PRECEDENCE",
        }
        for path in old
        if path != ACTIVE_RELAY
    ]
    return {
        "status": "OVERRIDDEN_SELECTOR_CONFLICT" if findings else "PASS",
        "effective_relay_path": ACTIVE_RELAY,
        "observed_v35": ACTIVE_RELAY in active,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    results = []
    for path in args.paths:
        results.append(scan_selector_text(path.read_text(encoding="utf-8"), source=str(path)))
    aggregate = {
        "status": "OVERRIDDEN_SELECTOR_CONFLICT" if any(r["findings"] for r in results) else "PASS",
        "effective_relay_path": ACTIVE_RELAY,
        "sources": results,
    }
    print(json.dumps(aggregate, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
