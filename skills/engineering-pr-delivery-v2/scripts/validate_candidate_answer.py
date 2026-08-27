#!/usr/bin/env python3
from pathlib import Path
import re
import sys

REQUIRED_FIELDS = [
    "CHAIN_ID",
    "ENDPOINT_ID",
    "QUESTION_SET_ID",
    "QUALIFICATION_BASIS_HEAD",
    "CANDIDATE_ID",
    "LIVE_PR_HEAD_OBSERVED",
    "LIVE_MAIN_HEAD_OBSERVED",
    "RECONCILIATION",
    "QUALIFICATION_STATUS",
    "TAKEOVER_AUTHORITY",
]

ALLOWED_RECONCILIATION = {
    "MATCH",
    "METADATA_DRIFT",
    "MATERIAL_DRIFT",
    "CONTRADICTION",
}


def field_value(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)
    return m.group(1).strip() if m else None


def question_body(text: str, q: int):
    m = re.search(
        rf"(?mis)^##\s+Q{q}\b[^\n]*\n(.*?)(?=^##\s+Q[1-5]\b|^##\s+Candidate declaration\b|\Z)",
        text,
    )
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_candidate_answer.py <candidate-answer.md>", file=sys.stderr)
        return 2

    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    errors = []

    for name in REQUIRED_FIELDS:
        if not field_value(text, name):
            errors.append(f"answer missing {name}")

    reconciliation = field_value(text, "RECONCILIATION")
    if reconciliation and reconciliation not in ALLOWED_RECONCILIATION:
        errors.append(f"invalid RECONCILIATION: {reconciliation}")

    status = field_value(text, "QUALIFICATION_STATUS")
    authority = field_value(text, "TAKEOVER_AUTHORITY")
    if status and status != "DEFERRED_VERIFICATION":
        errors.append(
            "candidate answer must remain QUALIFICATION_STATUS=DEFERRED_VERIFICATION until an independent verifier verdict exists"
        )
    if authority and authority != "READ_ONLY":
        errors.append(
            "candidate answer must remain TAKEOVER_AUTHORITY=READ_ONLY; candidate cannot self-authorize"
        )

    if field_value(text, "VERIFIER_ID"):
        errors.append("candidate answer must not declare VERIFIER_ID")
    if field_value(text, "VERDICT"):
        errors.append("candidate answer must not declare a VERDICT")

    # Candidate answers supply evidence, not their own scores.
    if re.search(r"(?mi)^\s*Q[1-5]\s+\d{1,2}\s*/\s*20\s*$", text):
        errors.append("candidate answer must not score its own Q1-Q5 responses")
    if re.search(r"(?mi)^\s*TOTAL\s+\d{1,3}\s*/\s*100\s*$", text):
        errors.append("candidate answer must not declare its own TOTAL score")

    for q in range(1, 6):
        if not re.search(rf"(?mi)^##\s+Q{q}\b", text):
            errors.append(f"answer missing Q{q} response section")
            continue
        body = question_body(text, q)
        if body is None or not body.strip():
            errors.append(f"answer Q{q} response is empty")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print("PASS: candidate answer is complete and remains deferred/read-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
