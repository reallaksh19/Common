#!/usr/bin/env python3
from pathlib import Path
import re
import sys

PASS_TOTAL = 92
PASS_MIN = 17
EMPTY_REASON_TOKENS = {"", "NONE", "N/A", "NA", "NOT_APPLICABLE"}


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


def meaningful_reason(value):
    return bool(value and value.strip().upper() not in EMPTY_REASON_TOKENS)


def score_values(text: str, q: int):
    return [
        int(value)
        for value in re.findall(
            rf"(?mi)^\s*Q{q}\s+(\d{{1,2}})\s*/\s*20\s*$", text
        )
    ]


def declared_totals(text: str):
    return [
        int(value)
        for value in re.findall(
            r"(?mi)^\s*TOTAL\s+(\d{1,3})\s*/\s*100\s*$", text
        )
    ]


def declared_mins(text: str):
    return [
        int(value)
        for value in re.findall(
            r"(?mi)^\s*MINIMUM_QUESTION\s+(\d{1,2})\s*/\s*20\s*$", text
        )
    ]


def require_exactly_one_field(text: str, name: str, label: str, errors: list[str]):
    values = field_values(text, name)
    if not values:
        errors.append(f"{label} missing {name}")
        return None
    if len(values) != 1:
        errors.append(f"{label} field {name} must appear exactly once; found {len(values)}")
        return None
    return values[0]


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
    shared = {}
    for name in shared_fields:
        av = require_exactly_one_field(answer, name, "answer", errors)
        vv = require_exactly_one_field(verdict, name, "verdict", errors)
        shared[name] = (av, vv)
        if av and vv and av != vv:
            errors.append(f"{name} mismatch: answer={av} verdict={vv}")

    candidate = shared.get("CANDIDATE_ID", (None, None))[1]
    verifier = require_exactly_one_field(verdict, "VERIFIER_ID", "verdict", errors)
    if candidate and verifier and candidate == verifier:
        errors.append("candidate and verifier are identical: INVALID_SELF_VERIFIED")

    basis = shared.get("QUALIFICATION_BASIS_HEAD", (None, None))[1]
    verdict_basis = require_exactly_one_field(
        verdict, "VERDICT_BASIS_HEAD", "verdict", errors
    )
    if verdict_basis and basis and verdict_basis != basis:
        errors.append(
            f"verdict basis {verdict_basis} differs from qualification basis {basis}; re-ground/requalify"
        )

    auto_fail_values = field_values(verdict, "AUTOMATIC_FAILURE_REASON")
    if len(auto_fail_values) != 1:
        errors.append(
            f"verdict field AUTOMATIC_FAILURE_REASON must appear exactly once; found {len(auto_fail_values)}"
        )
    auto_fail = auto_fail_values[0] if len(auto_fail_values) == 1 else None

    decision = require_exactly_one_field(verdict, "VERDICT", "verdict", errors)

    for q in range(1, 6):
        headings = re.findall(rf"(?mi)^#+\s+Q{q}\b[^\n]*$", answer)
        if not headings:
            errors.append(f"answer missing Q{q} response section")
        elif len(headings) != 1:
            errors.append(
                f"answer Q{q} response heading must appear exactly once; found {len(headings)}"
            )

    scores = []
    for q in range(1, 6):
        values = score_values(verdict, q)
        if not values:
            errors.append(f"verdict missing score Q{q} __/20")
            scores.append(None)
            continue
        if len(values) != 1:
            errors.append(f"verdict score Q{q} must appear exactly once; found {len(values)}")
            scores.append(None)
            continue
        score = values[0]
        if not 0 <= score <= 20:
            errors.append(f"Q{q} score out of range: {score}")
        scores.append(score)

    totals = declared_totals(verdict)
    if not totals:
        errors.append("verdict missing TOTAL __/100")
        total = None
    elif len(totals) != 1:
        errors.append(f"verdict TOTAL must appear exactly once; found {len(totals)}")
        total = None
    else:
        total = totals[0]

    minimums = declared_mins(verdict)
    if not minimums:
        errors.append("verdict missing MINIMUM_QUESTION __/20")
        minimum = None
    elif len(minimums) != 1:
        errors.append(
            f"verdict MINIMUM_QUESTION must appear exactly once; found {len(minimums)}"
        )
        minimum = None
    else:
        minimum = minimums[0]

    if all(s is not None for s in scores):
        actual_total = sum(scores)
        actual_min = min(scores)

        if total is not None and total != actual_total:
            errors.append(f"TOTAL arithmetic mismatch: declared {total}, actual {actual_total}")
        if minimum is not None and minimum != actual_min:
            errors.append(
                f"MINIMUM_QUESTION mismatch: declared {minimum}, actual {actual_min}"
            )

        qualified = actual_total >= PASS_TOTAL and actual_min >= PASS_MIN
        if decision == "PASS_WRITE_ALLOWED" and not qualified:
            errors.append(
                f"PASS_WRITE_ALLOWED invalid below threshold: total={actual_total}, minimum={actual_min}"
            )
        elif decision == "FAIL_READ_ONLY" and qualified:
            if not meaningful_reason(auto_fail):
                errors.append(
                    "FAIL_READ_ONLY despite passing numeric threshold requires a substantive AUTOMATIC_FAILURE_REASON"
                )
        elif decision and decision not in {
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

    print("PASS: independent qualification structure, uniqueness, and scoring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
