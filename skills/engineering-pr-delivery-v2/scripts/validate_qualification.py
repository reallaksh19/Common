#!/usr/bin/env python3
from pathlib import Path
import re
import sys

PASS_TOTAL = 92
PASS_MIN = 17
EMPTY_REASON_TOKENS = {"", "NONE", "N/A", "NA", "NOT_APPLICABLE"}


def field_value(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)
    return m.group(1).strip() if m else None


def meaningful_reason(value):
    return bool(value and value.strip().upper() not in EMPTY_REASON_TOKENS)


def score_value(text: str, q: int):
    m = re.search(rf"(?mi)^\s*Q{q}\s+(\d{{1,2}})\s*/\s*20\s*$", text)
    return int(m.group(1)) if m else None


def declared_total(text: str):
    m = re.search(r"(?mi)^\s*TOTAL\s+(\d{1,3})\s*/\s*100\s*$", text)
    return int(m.group(1)) if m else None


def declared_min(text: str):
    m = re.search(r"(?mi)^\s*MINIMUM_QUESTION\s+(\d{1,2})\s*/\s*20\s*$", text)
    return int(m.group(1)) if m else None


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: validate_qualification.py <candidate-answer.md> <verifier-verdict.md>",
            file=sys.stderr,
        )
        return 2

    answer = Path(sys.argv[1]).read_text(encoding="utf-8")
    verdict = Path(sys.argv[2]).read_text(encoding="utf-8")
    errors = []

    shared_fields = [
        "CHAIN_ID",
        "ENDPOINT_ID",
        "QUESTION_SET_ID",
        "QUALIFICATION_BASIS_HEAD",
        "CANDIDATE_ID",
    ]
    for name in shared_fields:
        av = field_value(answer, name)
        vv = field_value(verdict, name)
        if not av:
            errors.append(f"answer missing {name}")
        if not vv:
            errors.append(f"verdict missing {name}")
        if av and vv and av != vv:
            errors.append(f"{name} mismatch: answer={av} verdict={vv}")

    candidate = field_value(verdict, "CANDIDATE_ID")
    verifier = field_value(verdict, "VERIFIER_ID")
    if not verifier:
        errors.append("verdict missing VERIFIER_ID")
    if candidate and verifier and candidate == verifier:
        errors.append("candidate and verifier are identical: INVALID_SELF_VERIFIED")

    basis = field_value(verdict, "QUALIFICATION_BASIS_HEAD")
    verdict_basis = field_value(verdict, "VERDICT_BASIS_HEAD")
    if not verdict_basis:
        errors.append("verdict missing VERDICT_BASIS_HEAD")
    elif basis and verdict_basis != basis:
        errors.append(
            f"verdict basis {verdict_basis} differs from qualification basis {basis}; re-ground/requalify"
        )

    for q in range(1, 6):
        if not re.search(rf"(?mi)^#+\s+Q{q}\b", answer):
            errors.append(f"answer missing Q{q} response section")

    scores = []
    for q in range(1, 6):
        score = score_value(verdict, q)
        if score is None:
            errors.append(f"verdict missing score Q{q} __/20")
        elif not 0 <= score <= 20:
            errors.append(f"Q{q} score out of range: {score}")
        scores.append(score)

    if all(s is not None for s in scores):
        actual_total = sum(scores)
        actual_min = min(scores)
        total = declared_total(verdict)
        minimum = declared_min(verdict)
        if total is None:
            errors.append("verdict missing TOTAL __/100")
        elif total != actual_total:
            errors.append(f"TOTAL arithmetic mismatch: declared {total}, actual {actual_total}")
        if minimum is None:
            errors.append("verdict missing MINIMUM_QUESTION __/20")
        elif minimum != actual_min:
            errors.append(
                f"MINIMUM_QUESTION mismatch: declared {minimum}, actual {actual_min}"
            )

        decision = field_value(verdict, "VERDICT")
        qualified = actual_total >= PASS_TOTAL and actual_min >= PASS_MIN
        if not decision:
            errors.append("verdict missing VERDICT field")
        elif decision == "PASS_WRITE_ALLOWED" and not qualified:
            errors.append(
                f"PASS_WRITE_ALLOWED invalid below threshold: total={actual_total}, minimum={actual_min}"
            )
        elif decision == "FAIL_READ_ONLY" and qualified:
            # A verifier may still fail for an automatic-failure reason, but it must be substantive.
            auto_fail = field_value(verdict, "AUTOMATIC_FAILURE_REASON")
            if not meaningful_reason(auto_fail):
                errors.append(
                    "FAIL_READ_ONLY despite passing numeric threshold requires a substantive AUTOMATIC_FAILURE_REASON"
                )
        elif decision not in {
            "PASS_WRITE_ALLOWED",
            "FAIL_READ_ONLY",
            "STALE_REQUALIFICATION_REQUIRED",
            "INVALID_SELF_VERIFIED",
        }:
            errors.append(f"invalid VERDICT value: {decision}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print("PASS: independent qualification structure and scoring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
