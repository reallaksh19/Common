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


def field_values(text: str, name: str):
    return [
        value.strip()
        for value in re.findall(
            rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text
        )
    ]


def field_value(text: str, name: str):
    values = field_values(text, name)
    return values[0] if len(values) == 1 else None


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
        values = field_values(text, name)
        if not values:
            errors.append(f"answer missing {name}")
        elif len(values) != 1:
            errors.append(
                f"answer field {name} must appear exactly once; found {len(values)}"
            )

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

    verifier_values = field_values(text, "VERIFIER_ID")
    if verifier_values:
        errors.append("candidate answer must not declare VERIFIER_ID")
    verdict_values = field_values(text, "VERDICT")
    if verdict_values:
        errors.append("candidate answer must not declare a VERDICT")

    # Candidate answers supply evidence, not their own scores.
    if re.search(r"(?mi)^\s*Q[1-5]\s+\d{1,2}\s*/\s*20\s*$", text):
        errors.append("candidate answer must not score its own Q1-Q5 responses")
    if re.search(r"(?mi)^\s*TOTAL\s+\d{1,3}\s*/\s*100\s*$", text):
        errors.append("candidate answer must not declare its own TOTAL score")

    for q in range(1, 6):
        headings = re.findall(rf"(?mi)^##\s+Q{q}\b[^\n]*$", text)
        if not headings:
            errors.append(f"answer missing Q{q} response section")
            continue
        if len(headings) != 1:
            errors.append(
                f"answer Q{q} response heading must appear exactly once; found {len(headings)}"
            )
            continue
        body = question_body(text, q)
        if body is None or not body.strip():
            errors.append(f"answer Q{q} response is empty")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print("PASS: candidate answer is complete, unique-field, and deferred/read-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
