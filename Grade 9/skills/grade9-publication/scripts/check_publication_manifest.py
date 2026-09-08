#!/usr/bin/env python3
"""Deterministic baseline check for a Grade 9 Publication audit manifest.

This script verifies structural zero-loss and anti-drift conditions. For
question-bank products it also verifies per-question attemptability,
representation closure, answer-choice integrity, progressive hints, solution
self-containment, method/answer distinctness, math typography, and link closure.

It does not replace teacher/subject review or visual inspection.

Usage:
    python check_publication_manifest.py manifest.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SOURCE_STATUSES = {
    "PRESERVED",
    "RECOMPOSED",
    "MERGED",
    "SPLIT",
    "INTENTIONALLY_ABSENT",
    "REVIEW_REQUIRED",
}

FIGURE_STATUSES = {
    "PRESERVE",
    "REDRAW",
    "RECONSTRUCT",
    "SUPPORT_ADD",
    "INTENTIONALLY_ABSENT",
    "REVIEW_REQUIRED",
}

VALUE_PURPOSES = {
    "clarify",
    "connect",
    "diagnose",
    "practice",
    "navigate",
    "reduce_cognitive_load",
}

EDITORIAL_STATUSES = {"APPROVED", "REVIEW_REQUIRED", "REJECTED"}

QUESTION_PRODUCT_TYPES = {
    "question_bank",
    "transfer_book",
    "worksheet_collection",
    "question_plus_solution",
}

REPRESENTATION_DEPENDENCIES = {
    "NONE",
    "GRAPH",
    "DIAGRAM",
    "TABLE",
    "TIMELINE",
    "NUMBER_LINE",
    "OPTION_FIGURES",
    "STATEMENT_SET",
    "MIXED",
}

REPRESENTATION_SOURCE_STATUSES = {
    "PRESENT_SOURCE",
    "INTENTIONALLY_ABSENT",
    "SOURCE_CORRUPT",
    "SOURCE_INCOMPLETE",
    "RECONSTRUCT_APPROVED",
    "REVIEW_REQUIRED",
}

ANSWER_CHOICE_STATUSES = {
    "NOT_APPLICABLE",
    "VISIBLE_SOURCE",
    "VISIBLE_PUBLISHED",
    "TRANSPARENTLY_ADAPTED",
    "RECONSTRUCT_APPROVED",
    "REVIEW_REQUIRED",
}

QUESTION_STATUSES = {"PASS", "REVIEW_REQUIRED"}

RENDER_ZERO_FIELDS = (
    "clipped_core_objects",
    "hidden_core_objects",
    "overflow_findings",
    "text_overlap_findings",
    "component_bounds_escape_findings",
    "critical_equation_collision_findings",
    "unreadable_critical_labels",
    "math_glyph_errors",
    "broken_internal_links",
    "unresolved_external_source_links",
)

QUESTION_BANK_ZERO_FIELDS = (
    "unattemptable_questions",
    "representation_dependency_failures",
    "invisible_choice_failures",
    "question_recap_failures",
    "hint_progression_failures",
    "method_answer_duplication_failures",
    "method_reasoning_failures",
    "solution_self_containment_failures",
    "math_typography_failures",
    "question_solution_link_failures",
    "copy_paste_drift_failures",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require_dict(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(errors, f"top-level {key!r} must be an object")
        return {}
    return value


def require_list(data: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        fail(errors, f"top-level {key!r} must be an array")
        return []
    return value


def require_true(item: dict[str, Any], key: str, prefix: str, errors: list[str]) -> None:
    if item.get(key) is not True:
        fail(errors, f"{prefix}.{key} must be true")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_publication_manifest.py manifest.json", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"PUBLICATION MANIFEST CHECK: FAIL\n- cannot read JSON: {exc}")
        return 1

    if not isinstance(data, dict):
        print("PUBLICATION MANIFEST CHECK: FAIL\n- root must be a JSON object")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    publication = require_dict(data, "publication", errors)
    source_units = require_list(data, "source_units", errors)
    value_additions = require_list(data, "value_additions", errors)
    references = require_list(data, "references", errors)
    figures = require_list(data, "figures", errors)
    render_qa = require_dict(data, "render_qa", errors)
    editorial_exceptions = require_list(data, "editorial_exceptions", errors)

    product_type = publication.get("product_type")
    is_question_product = product_type in QUESTION_PRODUCT_TYPES

    question_records_raw = data.get("question_records")
    question_bank_qa_raw = data.get("question_bank_qa")

    if is_question_product:
        if not isinstance(question_records_raw, list):
            fail(errors, "top-level 'question_records' must be an array for question-bank products")
            question_records: list[Any] = []
        else:
            question_records = question_records_raw
        if not isinstance(question_bank_qa_raw, dict):
            fail(errors, "top-level 'question_bank_qa' must be an object for question-bank products")
            question_bank_qa: dict[str, Any] = {}
        else:
            question_bank_qa = question_bank_qa_raw
    else:
        question_records = question_records_raw if isinstance(question_records_raw, list) else []
        question_bank_qa = question_bank_qa_raw if isinstance(question_bank_qa_raw, dict) else {}

    for key in ("source_file", "source_pages", "published_pages"):
        if key not in publication:
            fail(errors, f"publication.{key} is required")

    if "product_type" not in publication:
        warnings.append("publication.product_type is missing; question-bank gates cannot be inferred")

    if publication.get("core_preservation_required") is not True:
        warnings.append("publication.core_preservation_required is not true")

    if render_qa.get("all_pages_rendered") is not True:
        fail(errors, "render_qa.all_pages_rendered must be true")

    # ---- Source units -----------------------------------------------------
    source_ids: set[str] = set()
    core_count = 0
    mapped_core_count = 0
    review_source_count = 0

    for idx, item in enumerate(source_units):
        prefix = f"source_units[{idx}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix} must be an object")
            continue

        source_id = item.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            fail(errors, f"{prefix}.source_id is required")
            continue
        if source_id in source_ids:
            fail(errors, f"duplicate source_id: {source_id}")
        source_ids.add(source_id)

        status = item.get("status")
        if status not in SOURCE_STATUSES:
            fail(errors, f"{source_id}: invalid source status {status!r}")
        if status == "REVIEW_REQUIRED":
            review_source_count += 1
            fail(errors, f"{source_id}: REVIEW_REQUIRED blocks publication")

        core = item.get("core") is True
        if core:
            core_count += 1
            targets = item.get("mapped_targets")
            intentional_absence = status == "INTENTIONALLY_ABSENT"
            if intentional_absence:
                mapped_core_count += 1
            elif isinstance(targets, list) and any(str(t).strip() for t in targets):
                mapped_core_count += 1
            else:
                fail(errors, f"{source_id}: core unit has no mapped target")

        if item.get("numbers_units_ok") is False:
            fail(errors, f"{source_id}: numeric/unit reconciliation failed")
        if item.get("equation_semantics_ok") is False:
            fail(errors, f"{source_id}: equation semantics reconciliation failed")

    if not source_units:
        fail(errors, "source_units must not be empty")
    if core_count == 0:
        fail(errors, "no core source units found")
    if core_count != mapped_core_count:
        fail(errors, f"core mapping mismatch: core={core_count}, mapped/intentional={mapped_core_count}")

    # ---- Value additions -------------------------------------------------
    value_ids: set[str] = set()
    for idx, item in enumerate(value_additions):
        prefix = f"value_additions[{idx}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix} must be an object")
            continue
        value_id = item.get("value_id")
        if not isinstance(value_id, str) or not value_id.strip():
            fail(errors, f"{prefix}.value_id is required")
            continue
        if value_id in value_ids:
            fail(errors, f"duplicate value_id: {value_id}")
        value_ids.add(value_id)

        purpose = item.get("purpose")
        if purpose not in VALUE_PURPOSES:
            fail(errors, f"{value_id}: invalid purpose {purpose!r}")
        if item.get("replaces_source") is not False:
            fail(errors, f"{value_id}: value addition must declare replaces_source=false")

        supports = item.get("supports")
        if not isinstance(supports, list) or not supports:
            fail(errors, f"{value_id}: supports must contain at least one source_id")
        else:
            for source_id in supports:
                if source_id not in source_ids:
                    fail(errors, f"{value_id}: supports unknown source_id {source_id!r}")

    # ---- References ------------------------------------------------------
    reference_ids: set[str] = set()
    unresolved_refs = 0
    for idx, item in enumerate(references):
        prefix = f"references[{idx}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix} must be an object")
            continue
        ref_id = item.get("reference_id")
        if not isinstance(ref_id, str) or not ref_id.strip():
            fail(errors, f"{prefix}.reference_id is required")
            continue
        if ref_id in reference_ids:
            fail(errors, f"duplicate reference_id: {ref_id}")
        reference_ids.add(ref_id)

        if item.get("resolved") is not True:
            unresolved_refs += 1
            fail(errors, f"{ref_id}: unresolved reference")
        target_id = item.get("target_id")
        if not isinstance(target_id, str) or not target_id.strip():
            fail(errors, f"{ref_id}: target_id is required")

    # ---- Figures ---------------------------------------------------------
    figure_ids: set[str] = set()
    for idx, item in enumerate(figures):
        prefix = f"figures[{idx}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix} must be an object")
            continue
        figure_id = item.get("figure_id")
        if not isinstance(figure_id, str) or not figure_id.strip():
            fail(errors, f"{prefix}.figure_id is required")
            continue
        if figure_id in figure_ids:
            fail(errors, f"duplicate figure_id: {figure_id}")
        figure_ids.add(figure_id)

        status = item.get("status")
        if status not in FIGURE_STATUSES:
            fail(errors, f"{figure_id}: invalid figure status {status!r}")
        if status == "REVIEW_REQUIRED":
            fail(errors, f"{figure_id}: REVIEW_REQUIRED blocks publication")
        if status in {"PRESERVE", "REDRAW", "RECONSTRUCT"}:
            if item.get("semantic_check") is not True:
                fail(errors, f"{figure_id}: semantic_check must be true")
            if item.get("labels_check") is not True:
                fail(errors, f"{figure_id}: labels_check must be true")
        if status == "INTENTIONALLY_ABSENT" and item.get("intentional_absence") is not True:
            fail(errors, f"{figure_id}: intentional_absence must be true")

    # ---- Question records ------------------------------------------------
    question_ids: set[str] = set()
    question_pass_count = 0
    representation_required_count = 0

    for idx, item in enumerate(question_records):
        prefix = f"question_records[{idx}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix} must be an object")
            continue

        question_id = item.get("question_id")
        if not isinstance(question_id, str) or not question_id.strip():
            fail(errors, f"{prefix}.question_id is required")
            continue
        if question_id in question_ids:
            fail(errors, f"duplicate question_id: {question_id}")
        question_ids.add(question_id)

        dep = item.get("representation_dependency")
        if dep not in REPRESENTATION_DEPENDENCIES:
            fail(errors, f"{question_id}: invalid representation_dependency {dep!r}")
            dep = "NONE"

        rep_status = item.get("representation_source_status")
        if rep_status not in REPRESENTATION_SOURCE_STATUSES:
            fail(errors, f"{question_id}: invalid representation_source_status {rep_status!r}")
        elif rep_status == "REVIEW_REQUIRED":
            fail(errors, f"{question_id}: representation REVIEW_REQUIRED blocks publication")

        choice_status = item.get("answer_choice_status")
        if choice_status not in ANSWER_CHOICE_STATUSES:
            fail(errors, f"{question_id}: invalid answer_choice_status {choice_status!r}")
        elif choice_status == "REVIEW_REQUIRED":
            fail(errors, f"{question_id}: answer-choice REVIEW_REQUIRED blocks publication")

        status = item.get("status")
        if status not in QUESTION_STATUSES:
            fail(errors, f"{question_id}: invalid status {status!r}")
        elif status == "REVIEW_REQUIRED":
            fail(errors, f"{question_id}: REVIEW_REQUIRED blocks publication")
        elif status == "PASS":
            question_pass_count += 1

        require_true(item, "question_recap_complete", question_id, errors)
        require_true(item, "method_distinct_from_answer", question_id, errors)
        require_true(item, "answer_present", question_id, errors)
        require_true(item, "math_typography_ok", question_id, errors)
        require_true(item, "question_to_solution_link_ok", question_id, errors)
        require_true(item, "solution_to_question_link_ok", question_id, errors)
        require_true(item, "source_link_ok", question_id, errors)
        require_true(item, "copy_paste_drift_check", question_id, errors)

        if item.get("h1_present") or item.get("h2_present") or item.get("h3_present"):
            require_true(item, "hint_progression_ok", question_id, errors)

        if dep != "NONE":
            representation_required_count += 1
            require_true(item, "representation_present_student", question_id, errors)
            require_true(item, "representation_legible", question_id, errors)
            # For question-bank products the solution artifact is expected to be standalone.
            if is_question_product:
                require_true(item, "representation_present_solution", question_id, errors)

        # A solution must contain an executable route. For question-bank products
        # it should also explain why the model/relation applies.
        if is_question_product:
            require_true(item, "method_has_executable_route", question_id, errors)
            require_true(item, "method_has_why", question_id, errors)
            require_true(item, "concept_to_keep_present", question_id, errors)

        if choice_status not in {None, "NOT_APPLICABLE"}:
            require_true(item, "answer_semantic_if_choice", question_id, errors)

    if is_question_product and not question_records:
        fail(errors, "question_records must not be empty for question-bank products")

    # ---- Question-bank summary ------------------------------------------
    if is_question_product:
        frozen = question_bank_qa.get("questions_frozen")
        published = question_bank_qa.get("questions_published")
        if not isinstance(frozen, int):
            fail(errors, "question_bank_qa.questions_frozen must be an integer")
        if not isinstance(published, int):
            fail(errors, "question_bank_qa.questions_published must be an integer")
        if isinstance(frozen, int) and isinstance(published, int) and frozen != published:
            fail(errors, f"question count mismatch: frozen={frozen}, published={published}")
        if isinstance(published, int) and published != len(question_records):
            fail(errors, f"question_records mismatch: published={published}, records={len(question_records)}")

        for field in QUESTION_BANK_ZERO_FIELDS:
            value = question_bank_qa.get(field)
            if value is None:
                fail(errors, f"question_bank_qa.{field} is required")
            elif not isinstance(value, int):
                fail(errors, f"question_bank_qa.{field} must be an integer")
            elif value != 0:
                fail(errors, f"question_bank_qa.{field} must be 0, got {value}")

    # ---- Render QA -------------------------------------------------------
    for field in RENDER_ZERO_FIELDS:
        value = render_qa.get(field)
        if value is None:
            fail(errors, f"render_qa.{field} is required")
        elif not isinstance(value, int):
            fail(errors, f"render_qa.{field} must be an integer")
        elif value != 0:
            fail(errors, f"render_qa.{field} must be 0, got {value}")

    # ---- Editorial exceptions -------------------------------------------
    for idx, item in enumerate(editorial_exceptions):
        prefix = f"editorial_exceptions[{idx}]"
        if not isinstance(item, dict):
            fail(errors, f"{prefix} must be an object")
            continue
        status = item.get("status")
        if status not in EDITORIAL_STATUSES:
            fail(errors, f"{prefix}: invalid status {status!r}")
        elif status == "REVIEW_REQUIRED":
            fail(errors, f"{prefix}: editorial REVIEW_REQUIRED blocks publication")

    print("PUBLICATION MANIFEST SUMMARY")
    print(f"- product type: {product_type or 'unspecified'}")
    print(f"- source units: {len(source_units)}")
    print(f"- core units: {core_count}")
    print(f"- mapped/intentional core units: {mapped_core_count}")
    print(f"- value additions: {len(value_additions)}")
    print(f"- references: {len(references)}")
    print(f"- figures: {len(figures)}")
    print(f"- unresolved references: {unresolved_refs}")
    print(f"- source review-required: {review_source_count}")
    if is_question_product:
        print(f"- question records: {len(question_records)}")
        print(f"- question PASS: {question_pass_count}")
        print(f"- representation-dependent questions: {representation_required_count}")

    if warnings:
        print("WARNINGS")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("PUBLICATION MANIFEST CHECK: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PUBLICATION MANIFEST CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
