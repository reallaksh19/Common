#!/usr/bin/env python3
"""Flag suspicious plain-text math notation in a rendered student PDF.

This is a conservative preflight for publication artifacts. It looks for common
source-notation leaks such as x_f, s_(n+2), a_avg and sqrt(...), which should be
properly typeset in the student PDF. It does not attempt to validate equation
semantics.

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
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_math_typography.py student.pdf", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    doc = fitz.open(path)
    findings: list[tuple[int, str, str]] = []

    for page_no, page in enumerate(doc, 1):
        text = page.get_text("text")
        for label, pattern in PATTERNS:
            for match in pattern.finditer(text):
                snippet = text[max(0, match.start()-24):match.end()+40].replace("\n", " ")
                findings.append((page_no, label, snippet.strip()))

    print("MATH TYPOGRAPHY PREFLIGHT")
    print(f"- pages: {len(doc)}")
    print(f"- suspicious findings: {len(findings)}")
    for page_no, label, snippet in findings:
        print(f"- p.{page_no} [{label}] {snippet}")

    if findings:
        print("MATH TYPOGRAPHY PREFLIGHT: FAIL")
        return 1
    print("MATH TYPOGRAPHY PREFLIGHT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
