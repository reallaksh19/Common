#!/usr/bin/env python3
"""Heuristic preflight for question-bank solution assimilation.

Designed for solution PDFs using headings such as QUESTION RECAP, WHY THIS WORKS,
METHOD, ANSWER / CHECK, and CONCEPT TO KEEP. It flags missing structural roles and
METHOD/ANSWER near-duplication. It is intentionally conservative and does not
replace subject review.

Usage:
    python check_question_bank_assimilation.py solutions.pdf
"""

from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

try:
    import fitz
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyMuPDF/fitz is required: {exc}")

HEADINGS = {
    "recap": re.compile(r"\bQUESTION\s+RECAP\b", re.I),
    "why": re.compile(r"\bWHY\s+THIS\s+WORKS\b", re.I),
    "method": re.compile(r"\bMETHOD\b", re.I),
    "answer": re.compile(r"\bANSWER(?:\s*/\s*CHECK)?\b", re.I),
    "concept": re.compile(r"\bCONCEPT\s+TO\s+KEEP\b", re.I),
}

STOP_PATTERN = re.compile(
    r"\b(?:QUESTION\s+RECAP|WHY\s+THIS\s+WORKS|METHOD|ANSWER(?:\s*/\s*CHECK)?|CONCEPT\s+TO\s+KEEP|RETURN\s+TO\s+QUESTION)\b",
    re.I,
)


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_after(text: str, heading: re.Pattern[str]) -> str:
    match = heading.search(text)
    if not match:
        return ""
    tail = text[match.end():]
    stop = STOP_PATTERN.search(tail)
    return tail[: stop.start()] if stop else tail


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_question_bank_assimilation.py solutions.pdf", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    doc = fitz.open(path)
    findings: list[str] = []
    solution_pages = 0

    for page_no, page in enumerate(doc, 1):
        text = page.get_text("text")
        if not HEADINGS["recap"].search(text):
            continue
        solution_pages += 1

        for key in ("why", "method", "answer", "concept"):
            if not HEADINGS[key].search(text):
                findings.append(f"p.{page_no}: missing {key} heading")

        method = normalize(extract_after(text, HEADINGS["method"]))
        answer = normalize(extract_after(text, HEADINGS["answer"]))

        if method and answer:
            ratio = SequenceMatcher(None, method, answer).ratio()
            if method == answer or ratio >= 0.88:
                findings.append(
                    f"p.{page_no}: METHOD≈ANSWER similarity={ratio:.2f}; review for answer-only solution"
                )
            if len(method.split()) < 6:
                findings.append(
                    f"p.{page_no}: METHOD is very short ({len(method.split())} words); verify executable reasoning"
                )

    print("QUESTION-BANK ASSIMILATION PREFLIGHT")
    print(f"- pages: {len(doc)}")
    print(f"- pages with QUESTION RECAP: {solution_pages}")
    print(f"- findings: {len(findings)}")
    for finding in findings:
        print(f"- {finding}")

    if solution_pages == 0:
        print("QUESTION-BANK ASSIMILATION PREFLIGHT: FAIL")
        print("- no QUESTION RECAP blocks found; wrong artifact or unsupported solution structure")
        return 1

    if findings:
        print("QUESTION-BANK ASSIMILATION PREFLIGHT: FAIL")
        return 1

    print("QUESTION-BANK ASSIMILATION PREFLIGHT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
