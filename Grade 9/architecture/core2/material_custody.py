#!/usr/bin/env python3
"""Core (2) material-model -> PublicationStructure custody helpers.

This module is deliberately independent from rendering. It answers one question:
can every MATERIAL item in the Study Guide main learning sections be accounted
for by PublicationStructure, either as selected content or an explicit
learner-publication disposition?
"""
from __future__ import annotations


_ALLOWED_DISPOSITIONS = {
    "RENDERED",
    "RENDERED_VIA_DERIVED_ITEM",
    "OMITTED_FOR_LEARNER",
    "BLOCKED",
}


def main_material_ids(study_model: dict) -> set[str]:
    return {
        item["item_id"]
        for section in study_model.get("main_sections", [])
        for item in section.get("items", [])
        if item.get("traceability_class") == "MATERIAL"
    }


def structure_content_ids(structure: dict) -> set[str]:
    return {
        ref
        for unit in structure.get("study_guide", {}).get("learning_units", [])
        for step in unit.get("arc_steps", [])
        for ref in step.get("content_refs", [])
    }


def disposition_map(structure: dict) -> dict[str, dict]:
    rows = structure.get("study_guide", {}).get("content_dispositions", [])
    return {row.get("content_ref"): row for row in rows if row.get("content_ref")}


def reconciliation_errors(study_model: dict, structure: dict) -> list[str]:
    material = main_material_ids(study_model)
    selected = structure_content_ids(structure)
    dispositions = disposition_map(structure)
    errors: list[str] = []

    for content_ref, row in dispositions.items():
        if content_ref not in material:
            errors.append(f"disposition references unknown/non-material main content: {content_ref}")
        state = row.get("disposition")
        if state not in _ALLOWED_DISPOSITIONS:
            errors.append(f"{content_ref}: invalid material disposition {state!r}")
        if state == "RENDERED" and content_ref not in selected:
            errors.append(f"{content_ref}: disposition says RENDERED but PublicationStructure does not select it")
        if state == "RENDERED_VIA_DERIVED_ITEM" and not row.get("derived_content_ref"):
            errors.append(f"{content_ref}: RENDERED_VIA_DERIVED_ITEM requires derived_content_ref")
        if state in {"OMITTED_FOR_LEARNER", "BLOCKED"} and not row.get("reason"):
            errors.append(f"{content_ref}: {state} requires a reason")

    for content_ref in sorted(material):
        if content_ref in selected:
            row = dispositions.get(content_ref)
            if row and row.get("disposition") not in {"RENDERED", "RENDERED_VIA_DERIVED_ITEM"}:
                errors.append(f"{content_ref}: selected content conflicts with disposition {row.get('disposition')}")
            continue
        row = dispositions.get(content_ref)
        if not row:
            errors.append(f"{content_ref}: MATERIAL item disappears between StudyGuide model and PublicationStructure")
            continue
        if row.get("disposition") not in {"RENDERED_VIA_DERIVED_ITEM", "OMITTED_FOR_LEARNER", "BLOCKED"}:
            errors.append(f"{content_ref}: unselected MATERIAL item lacks a valid downstream disposition")

    return errors
