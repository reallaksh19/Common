from __future__ import annotations

from typing import Any

FAST_RECOVERY_STEPS = (
    "BASIS",
    "LIVE_MATERIAL",
    "DELTA",
    "RECONCILE",
    "TASK_EVIDENCE_RECOVERY",
    "CONTRIBUTE_CONTINUE",
)

DEEP_RECOVERY_TRIGGERS = (
    "RESPONSIBILITY_IDENTITY_UNCERTAIN",
    "OWNER_AUTHORITY_CONTRADICTION",
    "PROGRAMME_DEPENDENCY_PRESENT",
    "RLL_OR_OFFLOAD_REFERENCE_PRESENT",
    "NEGATIVE_KNOWLEDGE_CONTRADICTION",
    "MATERIAL_PROVIDER_UNRECONCILED",
)


class CompatibilityError(ValueError):
    pass


def normalize_task_result(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize V3.2 and historical V3.1 result semantics without guessing completion."""
    scope = raw.get("result_scope", raw.get("RESULT_SCOPE"))
    coverage = raw.get("coverage", raw.get("COVERAGE"))
    complete = raw.get(
        "responsibility_complete",
        raw.get("RESPONSIBILITY_COMPLETE"),
    )
    if isinstance(complete, str):
        token = complete.strip().upper()
        if token == "YES":
            complete = True
        elif token == "NO":
            complete = False
        else:
            complete = None
    elif complete not in {True, False, None}:
        complete = None

    if scope not in {"STEP", "PRODUCT", "RESPONSIBILITY"}:
        scope = "UNKNOWN"
    if complete is True and scope != "RESPONSIBILITY":
        raise CompatibilityError(
            "result cannot claim responsibility complete outside RESPONSIBILITY scope"
        )
    missing_complete = (
        "responsibility_complete" not in raw
        and "RESPONSIBILITY_COMPLETE" not in raw
    )
    return {
        "result_scope": scope,
        "coverage": coverage if coverage is not None else "UNKNOWN",
        "responsibility_complete": complete,
        "compatibility_inferred": (
            scope == "UNKNOWN"
            or coverage is None
            or missing_complete
        ),
    }
