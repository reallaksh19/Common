#!/usr/bin/env python3
from pathlib import Path
import re
import sys

VALID_STATUS = "VALID"
ALLOWED_STATUSES = {
    "VALID",
    "STALE",
    "MALFORMED",
    "AUTHORITY_CONTAMINATED",
    "INSUFFICIENT_TECHNICAL_DEPTH",
}
VALID_AUTHORITY = {"VALID", "NOT_APPLICABLE"}


def fields(text: str, name: str):
    return [
        v.strip()
        for v in re.findall(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)
    ]


def one(text: str, name: str, label: str, errors: list[str], required=True):
    vals = fields(text, name)
    if not vals:
        if required:
            errors.append(f"{label} missing {name}")
        return None
    if len(vals) != 1:
        errors.append(f"{label} field {name} must appear exactly once; found {len(vals)}")
        return None
    return vals[0]


def main():
    if len(sys.argv) not in {3, 4}:
        print(
            "Usage: validate_question_set_admission.py <endpoint.md> <admission.md> [<candidate-answer.md>]",
            file=sys.stderr,
        )
        return 2

    endpoint_path = Path(sys.argv[1])
    admission_path = Path(sys.argv[2])
    endpoint = endpoint_path.read_text(encoding="utf-8")
    admission = admission_path.read_text(encoding="utf-8")
    candidate = Path(sys.argv[3]).read_text(encoding="utf-8") if len(sys.argv) == 4 else None
    errors = []

    ep_fields = {}
    adm_fields = {}
    for name in ("CHAIN_ID", "ENDPOINT_ID", "QUESTION_SET_ID", "QUALIFICATION_BASIS_HEAD"):
        ep_fields[name] = one(endpoint, name, "endpoint", errors)
        adm_fields[name] = one(admission, name, "admission", errors)
        if ep_fields[name] and adm_fields[name] and ep_fields[name] != adm_fields[name]:
            errors.append(f"{name} mismatch: endpoint={ep_fields[name]} admission={adm_fields[name]}")

    protocol = one(admission, "QUALIFICATION_PROTOCOL_VERSION", "admission", errors)
    if protocol != "3":
        errors.append("admission QUALIFICATION_PROTOCOL_VERSION must be 3")

    status = one(admission, "QUESTION_SET_ADMISSION_STATUS", "admission", errors)
    if status and status not in ALLOWED_STATUSES:
        errors.append(f"invalid QUESTION_SET_ADMISSION_STATUS: {status}")
    if status and status != VALID_STATUS:
        errors.append(f"question set is not admissible: {status}")

    authority = one(admission, "ADMISSION_AUTHORITY_ID", "admission", errors)
    if not authority:
        errors.append("admission requires independent ADMISSION_AUTHORITY_ID")

    retrievable = one(admission, "BASIS_RETRIEVABLE", "admission", errors)
    if retrievable != "TRUE":
        errors.append("BASIS_RETRIEVABLE must be TRUE")

    depth = one(admission, "TECHNICAL_DEPTH_STATUS", "admission", errors)
    if depth != "PASS":
        errors.append("TECHNICAL_DEPTH_STATUS must be PASS")

    for name in ("ROADMAP_AUTHORITY_STATUS", "SOURCE_ORACLE_AUTHORITY_STATUS"):
        value = one(admission, name, "admission", errors)
        if value and value not in VALID_AUTHORITY:
            errors.append(f"{name} must be VALID or NOT_APPLICABLE")

    legacy = one(admission, "LEGACY_SET", "admission", errors)
    if legacy not in {"TRUE", "FALSE"}:
        errors.append("LEGACY_SET must be TRUE or FALSE")

    evidence = one(admission, "ADMISSION_EVIDENCE", "admission", errors)
    if not evidence or evidence.upper() in {"NONE", "N/A", "NOT_APPLICABLE"}:
        errors.append("ADMISSION_EVIDENCE must identify concrete admission evidence")

    candidate_id = None
    if candidate is not None:
        candidate_id = one(candidate, "CANDIDATE_ID", "candidate answer", errors)
    else:
        candidate_id = one(admission, "CANDIDATE_ID", "admission", errors, required=False)

    if candidate_id and authority and candidate_id == authority:
        errors.append("candidate cannot be sole admission authority for its own question set")

    for n in range(1, 6):
        matches = re.findall(rf"(?mi)^####\s+Q{n}\b", endpoint)
        if len(matches) != 1:
            errors.append(f"endpoint must contain exactly one Q{n}; found {len(matches)}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print("PASS: question-set admission is VALID and independently attributable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
