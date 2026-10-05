"""Answer closure with subject recomputation kept outside composition."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

from .contracts import digest, require, strings, text


def subject_adapter(subject: str):
    require(subject in {"Physics", "Mathematics", "Chemistry"}, "SUBJECT_UNSUPPORTED")
    path = Path(__file__).resolve().parents[2] / subject / "ProductionKit" / "validator.py"
    spec = importlib.util.spec_from_file_location(f"v3b_{subject.lower()}_validator", path)
    require(spec is not None and spec.loader is not None, "SUBJECT_VALIDATOR_MISSING")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_answer(question: dict, subject: str) -> dict:
    answer = question.get("answer", {})
    response = question.get("response_mode")
    require(response in {"MCQ", "CLOSED", "OPEN_ENDED"}, "RESPONSE_MODE_INVALID")
    if response == "OPEN_ENDED":
        strings(answer.get("expected_response_rubric"), "OPEN_RESPONSE_RUBRIC_REQUIRED")
    else:
        require("canonical_answer" in answer, "CANONICAL_ANSWER_REQUIRED")
        text(answer.get("quick_check"), "QUICK_CHECK_REQUIRED")
        strings(answer.get("full_working"), "FULL_WORKING_REQUIRED")
    strings(answer.get("verification"), "ANSWER_VERIFICATION_REQUIRED")
    if response == "MCQ":
        options = question.get("options", [])
        require(len(options) >= 2 and len(set(options)) == len(options), "MCQ_OPTIONS_INVALID")
        require(answer["canonical_answer"] in options, "MCQ_ANSWER_NOT_IN_OPTIONS")
    case = answer.get("validation_case")
    if question["origin"] == "GENERATED_ORIGINAL":
        require(isinstance(case, dict), "GENERATED_INDEPENDENT_VALIDATOR_REQUIRED")
    if case is not None:
        try:
            result = subject_adapter(subject).recompute(case)
        except (ValueError, KeyError, TypeError, ZeroDivisionError, OverflowError) as exc:
            require(False, "DOMAIN_VALIDATION_FAILED", str(exc))
        require(_same(result, answer.get("canonical_answer")), "RECOMPUTED_ANSWER_MISMATCH")
        return {"kind": "DOMAIN_RECOMPUTATION", "result": result, "case_digest": digest(case)}
    return {"kind": "INDEPENDENT_ANSWER_REVIEW_REQUIRED", "result": None}


def _same(result: object, declared: object) -> bool:
    if type(result) in {int, float} and type(declared) in {int, float}:
        return math.isfinite(result) and math.isfinite(declared) and math.isclose(result, declared, rel_tol=1e-9, abs_tol=1e-9)
    return type(result) is type(declared) and result == declared


def validate_help(question: dict) -> None:
    help_rows = question.get("hints", [])
    if question["support_mode"] == "INDEPENDENT":
        require(help_rows == [], "INDEPENDENT_ITEM_CONTAINS_HINTS")
        return
    require([x.get("level") for x in help_rows] == ["H1", "H2", "H3"], "HINT_LADDER_REQUIRED")
    answer = question["answer"]
    working = {" ".join(x.lower().split()) for x in answer.get("full_working", [])}
    for row in help_rows:
        value = text(row.get("text"), "HINT_TEXT_REQUIRED")
        strings(row.get("capability_ids"), "HINT_CAPABILITIES_REQUIRED")
        strings(row.get("operation_refs"), "HINT_OPERATION_BINDING_REQUIRED")
        require(" ".join(value.lower().split()) not in working, "HINT_DUPLICATES_FULL_WORKING")
    # Exact-line checks detect one leakage class only. The independent review
    # must also assess whether hints disclose the decisive answer/solution.
