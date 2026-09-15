#!/usr/bin/env python3
"""Topic-neutral projection of Engineering problem-family semantics into learner roles.

This module prevents metadata with different semantic polarity from being flattened into
one learner-facing list. In particular, a common fatal error is an ERROR_TO_AVOID and
can never be projected as a METHOD_STEP.
"""
from __future__ import annotations

from typing import Any


class ChemistrySemanticProjectionError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistrySemanticProjectionError(code, message)


def _required_text(row: dict[str, Any], field: str) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        fail("CHEM_SEMANTIC_PROJECTION_SOURCE_FIELD_MISSING", field)
    return value.strip()


def project_problem_family(problem_family: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(problem_family, dict):
        fail("CHEM_SEMANTIC_PROJECTION_SOURCE_INVALID")
    projection = {
        "problem_family_ref": _required_text(problem_family, "family_id"),
        "chemical_signature": _required_text(problem_family, "name"),
        "recognition_signals": [_required_text(problem_family, "recognition_cues")],
        "method_steps": [_required_text(problem_family, "first_technical_move")],
        "common_fatal_errors": [_required_text(problem_family, "common_fatal_error")],
        "typical_unknown": _required_text(problem_family, "typical_unknown"),
        "semantic_role_trace": {
            "recognition_cues": "RECOGNITION_SIGNAL",
            "first_technical_move": "METHOD_STEP",
            "common_fatal_error": "ERROR_TO_AVOID",
            "typical_unknown": "TARGET_UNKNOWN",
        },
    }
    validate_problem_family_projection(problem_family, projection)
    return projection


def validate_problem_family_projection(
    problem_family: dict[str, Any],
    projection: dict[str, Any],
) -> dict[str, Any]:
    first_move = _required_text(problem_family, "first_technical_move")
    fatal_error = _required_text(problem_family, "common_fatal_error")
    methods = projection.get("method_steps")
    errors = projection.get("common_fatal_errors")
    trace = projection.get("semantic_role_trace")
    if not isinstance(methods, list) or first_move not in methods:
        fail("CHEM_SEMANTIC_PROJECTION_METHOD_STEP_MISSING")
    if fatal_error in methods:
        fail("CHEM_SEMANTIC_PROJECTION_FATAL_ERROR_AS_METHOD_STEP")
    if not isinstance(errors, list) or fatal_error not in errors:
        fail("CHEM_SEMANTIC_PROJECTION_FATAL_ERROR_MISSING")
    if not isinstance(trace, dict):
        fail("CHEM_SEMANTIC_PROJECTION_ROLE_TRACE_MISSING")
    if trace.get("first_technical_move") != "METHOD_STEP":
        fail("CHEM_SEMANTIC_PROJECTION_ROLE_DRIFT", "first_technical_move")
    if trace.get("common_fatal_error") != "ERROR_TO_AVOID":
        fail("CHEM_SEMANTIC_PROJECTION_ROLE_DRIFT", "common_fatal_error")
    return {
        "status": "PASS",
        "problem_family_ref": projection.get("problem_family_ref"),
        "method_step_count": len(methods),
        "fatal_error_count": len(errors),
    }
