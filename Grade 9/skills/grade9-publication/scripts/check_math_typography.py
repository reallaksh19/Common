#!/usr/bin/env python3
"""Flag suspicious source-style math notation in a rendered student PDF.

This is a conservative preflight for publication artifacts. It detects common
source-notation leaks that should be typeset for learners. It does not validate
mathematical semantics; every finding must be checked against the source before
changing notation.

Usage:
    python check_math_typography.py student.pdf
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import fitz
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyMuPDF/fitz is required: {exc}")

PATTERNS = [
    ("literal_subscript", re.compile(r"\b[A-Za-z]\w*_[A-Za-z0-9(]")),
    ("parenthesized_subscript", re.compile(r"\b[A-Za-z]_\([^\n)]")),
    ("ascii_sqrt", re.compile(r"\bsqrt\s*\(", re.I)),
    ("caret_power", re.compile(r"\b[A-Za-z0-9)]\s*\^\s*[-+]?\d+")),
    ("unit_square_ascii", re.compile(r"\b(?:m|cm|mm|km)/s2\b", re.I)),
    # Common single-letter indexed variables in school Physics/Math. These are
    # only suspicious, not automatically wrong: inspect semantics before fixing.
    ("plain_numeric_index", re.compile(r"\b(?:u|v|a|s|x|y|t|S|T)[0-9]\b")),
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_math_typography.py student.pdf", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    doc = fitz.open(path)
    findings: list[tuple[int, str, str]] = []

    for page_no, page in enumerate(doc, 1):
        text = page.get_text("text")
        for label, pattern in PATTERNS:
            for match in pattern.finditer(text):
                snippet = text[max(0, match.start()-28):match.end()+48].replace("\n", " ")
                findings.append((page_no, label, snippet.strip()))

    print("MATH TYPOGRAPHY PREFLIGHT")
    print(f"- pages: {len(doc)}")
    print(f"- suspicious findings: {len(findings)}")
    for page_no, label, snippet in findings:
        print(f"- p.{page_no} [{label}] {snippet}")

    if findings:
        print("MATH TYPOGRAPHY PREFLIGHT: FAIL")
        print("Review each finding against source semantics; do not blindly convert index to exponent or vice versa.")
        return 1

    print("MATH TYPOGRAPHY PREFLIGHT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
