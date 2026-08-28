#!/usr/bin/env python3
from pathlib import Path
import re
import sys

DRIFT = {
    "NONE",
    "METADATA_ONLY",
    "MATERIAL_WITHIN_QUALIFIED_BOUNDARY",
    "MATERIAL_BOUNDARY_CHANGED",
    "AUTHORITY_CHANGED",
    "CONTAMINATED",
}


def fields(text: str, name: str):
    return [
        v.strip()
        for v in re.findall(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)
    ]


def one(text: str, name: str, errors: list[str]):
    vals = fields(text, name)
    if not vals:
        errors.append(f"missing {name}")
        return None
    if len(vals) != 1:
        errors.append(f"field {name} must appear exactly once; found {len(vals)}")
        return None
    return vals[0]


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_post_basis_drift.py <reconciliation.md>", file=sys.stderr)
        return 2

    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    errors = []

    protocol = one(text, "QUALIFICATION_PROTOCOL_VERSION", errors)
    if protocol != "3":
        errors.append("QUALIFICATION_PROTOCOL_VERSION must be 3")

    for name in (
        "CHAIN_ID",
        "ENDPOINT_ID",
        "QUESTION_SET_ID",
        "QUALIFICATION_BASIS_HEAD",
        "CANDIDATE_ID",
        "RECONCILIATION_REVIEWER_ID",
        "LIVE_HEAD",
        "POST_BASIS_COMMITS",
        "RECONCILIATION_EVIDENCE",
    ):
        value = one(text, name, errors)
        if value and name == "RECONCILIATION_EVIDENCE" and value.upper() in {"NONE", "N/A", "NOT_APPLICABLE"}:
            errors.append("RECONCILIATION_EVIDENCE must be concrete")

    candidate = one(text, "CANDIDATE_ID", errors)
    reviewer = one(text, "RECONCILIATION_REVIEWER_ID", errors)
    drift = one(text, "POST_BASIS_DRIFT", errors)
    coverage = one(text, "QUALIFICATION_COVERAGE", errors)
    current = one(text, "CURRENT_STATE_AUTHORITY", errors)
    decision = one(text, "WRITE_AUTHORITY_DECISION", errors)

    if drift and drift not in DRIFT:
        errors.append(f"invalid POST_BASIS_DRIFT: {drift}")
    if current not in {"CLEAR", "BLOCKED"}:
        errors.append("CURRENT_STATE_AUTHORITY must be CLEAR or BLOCKED")
    if decision not in {"READ_ONLY", "WRITE_ALLOWED"}:
        errors.append("WRITE_AUTHORITY_DECISION must be READ_ONLY or WRITE_ALLOWED")

    if drift in {"NONE", "METADATA_ONLY"}:
        if coverage != "RETAINED":
            errors.append(f"{drift} requires QUALIFICATION_COVERAGE: RETAINED")
    elif drift == "MATERIAL_WITHIN_QUALIFIED_BOUNDARY":
        if coverage != "INDEPENDENTLY_CONFIRMED":
            errors.append("MATERIAL_WITHIN_QUALIFIED_BOUNDARY requires QUALIFICATION_COVERAGE: INDEPENDLY_CONFIRMED".replace("INDEPENDLY", "INDEPENDENTLY"))
        if candidate and reviewer and candidate == reviewer:
            errors.append("candidate cannot self-confirm material qualification coverage")
    elif drift in {"MATERIAL_BOUNDARY_CHANGED", "AUTHORITY_CHANGED", "CONTAMINATED"}:
        if coverage != "REQUALIFICATION_REQUIRED":
            errors.append(f"{drift} requires QUALIFICATION_COVERAGE: REQUALIFICATION_REQUIRED")
        if decision == "WRITE_ALLOWED":
            errors.append(f"{drift} cannot grant WRITE_ALLOWED; requalification is required")

    if decision == "WRITE_ALLOWED":
        if current != "CLEAR":
            errors.append("WRITE_ALLOWED requires CURRENT_STATE_AUTHORITY: CLEAR")
        if candidate and reviewer and candidate == reviewer:
            errors.append("candidate cannot self-grant WRITE_ALLOWED after reconciliation")
        if coverage not in {"RETAINED", "INDEPENDENTLY_CONFIRMED"}:
            errors.append("WRITE_ALLOWED requires retained or independently confirmed qualification coverage")

    if current == "BLOCKED" and decision == "WRITE_ALLOWED":
        errors.append("blocked current-state authority cannot grant WRITE_ALLOWED")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print(f"PASS: post-basis drift {drift} -> {coverage} / {decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
