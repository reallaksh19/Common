#!/usr/bin/env python3
from pathlib import Path
import re
import sys

SECTIONS = [
    "Inputs",
    "Benchmarks",
    "Common / governing documents",
    "Authoritative sources",
    "Production paths",
    "Validation / test paths",
]


def section_body(text: str, heading: str):
    m = re.search(
        rf"(?mis)^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|\Z)", text
    )
    return m.group(1).strip() if m else None


def meaningful(body: str | None):
    if body is None:
        return False
    cleaned = re.sub(r"[`*_>#-]", "", body).strip()
    return bool(cleaned)


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_source_index.py <endpoint.md>", file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    errors = []
    for heading in SECTIONS:
        body = section_body(text, heading)
        if body is None:
            errors.append(f"missing section: {heading}")
        elif not meaningful(body):
            errors.append(f"empty section: {heading}")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: endpoint source/input custody sections are present and non-empty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
