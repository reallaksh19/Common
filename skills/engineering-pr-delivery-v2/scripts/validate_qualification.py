#!/usr/bin/env python3
from pathlib import Path
import re
import sys

PASS_TOTAL = 92
PASS_MIN = 17
EMPTY_REASON_TOKENS = {"", "NONE", "N/A", "NA", "NOT_APPLICABLE"}


def field_values(text: str, name: str):
    return [v.strip() for v in re.findall(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)]


def field_value(text: str, name: str):
    values = field_values(text, name)
    return values[0] if len(values) == 1 else None


def meaningful_reason(value):
    return bool(value and value.strip().upper() not in EMPTY_REASON_TOKENS)


def score_values(text: str, q: int):
    return [int(v) for v in re.findall(rf"(?mi)^\s*Q{q}\s+(\d{{1,2}})\s*/\s*20\s*$", text)]


def declared_totals(text: str):
    return [int(v) for v in re.findall(r"(?mi)^\s*TOTAL\s+(\d{1,3})\s*/\s*100\s*$", text)]


def declared_mins(text: str):
    return [int(v) for v in re.findall(r"(?mi)^\s*MINIMUM_QUESTION\s+(\d{1,2})\s*/\s*20\s*$", text)]


def require_exactly_one_field(text, name, label, errors):
    values = field_values(text, name)
    if not values:
        errors.append(f"{label} missing {name}")
        return None
    if len(values) != 1:
        errors.append(f"{label} field {name} must appear exactly once; found {len(values)}")
        return None
    return values[0]


def optional_protocol_version(answer, verdict, errors):
    av = field_values(answer, "QUALIFICATION_PROTOCOL_VERSION")
    vv = field_values(verdict, "QUALIFICATION_PROTOCOL_VERSION")
    if len(av) > 1 or len(vv) > 1:
        errors.append("QUALIFICATION_PROTOCOL_VERSION may appear at most once in answer/verdict")
        return None
    a = av[0] if av else None
    v = vv[0] if vv else None
    if (a is None) != (v is None):
        errors.append("QUALIFICATION_PROTOCOL_VERSION must appear in both answer and verdict or neither")
        return None
    if a and v and a != v:
        errors.append(f"QUALIFICATION_PROTOCOL_VERSION mismatch: answer={a} verdict={v}")
        return None
    return a


def main():
    if len(sys.argv) != 3:
        print("Usage: validate_qualification.py <candidate-answer.md> <verifier-verdict.md>", file=sys.stderr)
        return 2

    answer = Path(sys.argv[1]).read_text(encoding="utf-8")
    verdict = Path(sys.argv[2]).read_text(encoding="utf-8")
    errors = []
    protocol = optional_protocol_version(answer, verdict, errors)

    shared_fields = ["CHAIN_ID", "ENDPOINT_ID", "QUESTION_SET_ID", "QUALIFICATION_BASIS_HEAD", "CANDIDATE_ID"]
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
    verdict_basis = require_exactly_one_field(verdict, "VERDICT_BASIS_HEAD", "verdict", errors)
    if verdict_basis and basis and verdict_basis != basis:
        errors.append(f"verdict basis {verdict_basis} differs from qualification basis {basis}")

    auto_fail_values = field_values(verdict, "AUTOMATIC_FAILURE_REASON")
    if len(auto_fail_values) != 1:
        errors.append(f"verdict field AUTOMATIC_FAILURE_REASON must appear exactly once; found {len(auto_fail_values)}")
    auto_fail = auto_fail_values[0] if len(auto_fail_values) == 1 else None
    decision = require_exactly_one_field(verdict, "VERDICT", "verdict", errors)

    for q in range(1, 6):
        headings = re.findall(rf"(?mi)^#+\s+Q{q}\b[^\n]*$", answer)
        if len(headings) != 1:
            errors.append(f"answer Q{q} response heading must appear exactly once; found {len(headings)}")

    scores = []
    for q in range(1, 6):
        values = score_values(verdict, q)
        if len(values) != 1:
            errors.append(f"verdict score Q{q} must appear exactly once; found {len(values)}")
            scores.append(None)
            continue
        score = values[0]
        if not 0 <= score <= 20:
            errors.append(f"Q{q} score out of range: {score}")
        scores.append(score)

    totals = declared_totals(verdict)
    total = totals[0] if len(totals) == 1 else None
    if len(totals) != 1:
        errors.append(f"verdict TOTAL must appear exactly once; found {len(totals)}")
    minimums = declared_mins(verdict)
    minimum = minimums[0] if len(minimums) == 1 else None
    if len(minimums) != 1:
        errors.append(f"verdict MINIMUM_QUESTION must appear exactly once; found {len(minimums)}")

    if all(s is not None for s in scores):
        actual_total = sum(scores)
        actual_min = min(scores)
        if total is not None and total != actual_total:
            errors.append(f"TOTAL arithmetic mismatch: declared {total}, actual {actual_total}")
        if minimum is not None and minimum != actual_min:
            errors.append(f"MINIMUM_QUESTION mismatch: declared {minimum}, actual {actual_min}")
        qualified = actual_total >= PASS_TOTAL and actual_min >= PASS_MIN

        if protocol == "3":
            allowed = {"PASS_QUALIFIED_READ_ONLY", "FAIL_READ_ONLY", "DEFERRED_READ_ONLY", "INVALID_SELF_VERIFIED"}
            if decision == "PASS_WRITE_ALLOWED":
                errors.append("version-3 qualification cannot grant WRITE_ALLOWED; use PASS_QUALIFIED_READ_ONLY")
            elif decision == "PASS_QUALIFIED_READ_ONLY" and not qualified:
                errors.append(f"PASS_QUALIFIED_READ_ONLY invalid below threshold: total={actual_total}, minimum={actual_min}")
            elif decision == "FAIL_READ_ONLY" and qualified and not meaningful_reason(auto_fail):
                errors.append("FAIL_READ_ONLY despite passing threshold requires substantive AUTOMATIC_FAILURE_REASON")
            elif decision and decision not in allowed:
                errors.append(f"invalid version-3 VERDICT value: {decision}")
        else:
            allowed = {"PASS_WRITE_ALLOWED", "FAIL_READ_ONLY", "STALE_REQUALIFICATION_REQUIRED", "INVALID_SELF_VERIFIED"}
            if decision == "PASS_WRITE_ALLOWED" and not qualified:
                errors.append(f"PASS_WRITE_ALLOWED invalid below threshold: total={actual_total}, minimum={actual_min}")
            elif decision == "FAIL_READ_ONLY" and qualified and not meaningful_reason(auto_fail):
                errors.append("FAIL_READ_ONLY despite passing threshold requires substantive AUTOMATIC_FAILURE_REASON")
            elif decision and decision not in allowed:
                errors.append(f"invalid legacy VERDICT value: {decision}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    if protocol == "3":
        print("PASS: version-3 qualification structure/scoring; PASS remains READ_ONLY pending reconciliation")
    else:
        print("PASS: legacy independent qualification structure, uniqueness, and scoring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
