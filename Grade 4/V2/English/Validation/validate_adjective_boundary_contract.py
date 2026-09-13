#!/usr/bin/env python3
"""Validate Grade 4 adjective boundary/placement regression fixtures.

Dependency-free by design so the draft contract can be checked in a minimal
Python environment before it is wired into a larger publishing pipeline.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_PLACEMENT_AUTHORITIES = {
    "EXPLICIT_SOURCE_RULE",
    "EXPLICIT_SOURCE_EXAMPLE",
    "OWNER_OR_TEACHER_SUPPLIED_RULE",
    "DERIVED_STUDY_MATERIAL_ASSERTION",
    "OUTSIDE_CANONICAL_KNOWLEDGE",
    "SOURCE_UNRESOLVED",
}

INTERNAL_LABELS = {
    "SOURCE_MODEL_BOUNDARY",
    "SOURCE_UNRESOLVED",
    "OUTSIDE_CANONICAL_KNOWLEDGE",
    "DERIVED_STUDY_MATERIAL_ASSERTION",
    "OWNER_OR_TEACHER_SUPPLIED_RULE",
}

INVENTED_CATEGORY_SENTINELS = {
    "QUALITY",
    "PHYSICAL_QUALITY",
    "CONDITION",
    "TYPE",
    "GENERAL_DESCRIPTION",
    "OTHER_ADJECTIVE",
}


class ContractError(Exception):
    pass


def fail(code: str, detail: str) -> None:
    raise ContractError(f"{code}: {detail}")


def validate_model(model_id: str, model: dict) -> None:
    categories = model.get("categories")
    order = model.get("order")
    if not isinstance(categories, list) or not categories:
        fail("INVALID_MODEL", f"{model_id} has no categories")
    if len(categories) != len(set(categories)):
        fail("INVALID_MODEL", f"{model_id} repeats a category")
    if order != categories:
        fail("INVALID_MODEL", f"{model_id} order must exactly match its frozen categories")
    if model.get("immutable_for_episode") is not True:
        fail("MODEL_NOT_FROZEN", f"{model_id} must set immutable_for_episode=true")


def validate_case(case: dict, models: dict) -> None:
    case_id = case.get("id", "<missing-id>")
    model_id = case.get("model_id")
    if model_id not in models:
        fail("UNKNOWN_MODEL", f"{case_id} references {model_id!r}")

    model_categories = set(models[model_id]["categories"])
    if "model_extensions" in case:
        fail("MODEL_MUTATED_BY_EXAMPLE", f"{case_id} contains model_extensions")

    items = case.get("items") or []
    if not items:
        fail("INVALID_CASE", f"{case_id} has no adjective items")

    positions: dict[int, str] = {}
    for item in items:
        word = item.get("word", "<missing-word>")
        school = item.get("school_analysis") or {}
        placement = item.get("phrase_placement") or {}
        category = school.get("category")
        status = school.get("status")
        child_message = school.get("child_message", "")

        if category is not None and category not in model_categories:
            fail(
                "CATEGORY_NOT_IN_FROZEN_MODEL",
                f"{case_id}/{word}: {category} not in {model_id}",
            )

        forbidden = set(item.get("forbidden_categories") or [])
        if category in forbidden:
            fail(
                "BOUNDARY_WORD_ASSIGNED_INVENTED_CATEGORY",
                f"{case_id}/{word}: assigned forbidden category {category}",
            )

        if category is None:
            if status != "SOURCE_MODEL_BOUNDARY":
                fail(
                    "BOUNDARY_STATUS_REQUIRED",
                    f"{case_id}/{word}: null category requires SOURCE_MODEL_BOUNDARY",
                )
            authority = placement.get("authority")
            if authority not in ALLOWED_PLACEMENT_AUTHORITIES:
                fail(
                    "BOUNDARY_WORD_MISSING_PLACEMENT_AUTHORITY",
                    f"{case_id}/{word}: invalid or missing placement authority",
                )
            if authority == "SOURCE_UNRESOLVED" and case.get("expected_phrase"):
                fail(
                    "UNRESOLVED_PLACEMENT_USED_IN_FINAL_PHRASE",
                    f"{case_id}/{word}: final phrase claimed with unresolved placement",
                )

        required_category = item.get("requires_model_category")
        if required_category is not None:
            if required_category not in model_categories:
                fail(
                    "PURPOSE_ASSIGNED_WITHOUT_PURPOSE_MODEL",
                    f"{case_id}/{word}: requires {required_category}, absent from {model_id}",
                )
            if category != required_category:
                fail(
                    "REQUIRED_MODEL_CATEGORY_MISMATCH",
                    f"{case_id}/{word}: expected {required_category}, got {category}",
                )

        if category in INVENTED_CATEGORY_SENTINELS and category not in model_categories:
            fail(
                "BOUNDARY_WORD_ASSIGNED_INVENTED_CATEGORY",
                f"{case_id}/{word}: invented category {category}",
            )

        for label in INTERNAL_LABELS:
            if label in child_message:
                fail(
                    "INTERNAL_LABEL_LEAKED_TO_CHILD_SURFACE",
                    f"{case_id}/{word}: child message exposes {label}",
                )

        position = placement.get("position_index")
        if not isinstance(position, int) or position < 0:
            fail("INVALID_PHRASE_POSITION", f"{case_id}/{word}: {position!r}")
        if position in positions:
            fail(
                "DUPLICATE_PHRASE_POSITION",
                f"{case_id}: {word} and {positions[position]} both use {position}",
            )
        positions[position] = word

    expected_positions = list(range(len(items)))
    if sorted(positions) != expected_positions:
        fail(
            "NON_CONTIGUOUS_PHRASE_POSITIONS",
            f"{case_id}: expected {expected_positions}, got {sorted(positions)}",
        )

    ordered_words = [positions[index] for index in expected_positions]
    assembled = " ".join([*ordered_words, case["noun"]])
    if assembled != case.get("expected_phrase"):
        fail(
            "EXPECTED_PHRASE_MISMATCH",
            f"{case_id}: assembled {assembled!r}, expected {case.get('expected_phrase')!r}",
        )


def main() -> int:
    fixture = Path(__file__).with_name("adjective-boundary-regressions.json")
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    models = payload.get("models") or {}
    for model_id, model in models.items():
        validate_model(model_id, model)

    cases = payload.get("cases") or []
    case_ids = {case.get("id") for case in cases}
    required = set(payload.get("required_case_ids") or [])
    missing = sorted(required - case_ids)
    if missing:
        fail("MISSING_REQUIRED_REGRESSION", ", ".join(missing))

    for case in cases:
        validate_case(case, models)

    print(
        "PASS: adjective boundary contract "
        f"({len(models)} frozen models, {len(cases)} regression cases)"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
