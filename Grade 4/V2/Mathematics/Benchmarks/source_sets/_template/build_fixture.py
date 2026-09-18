"""Explicit semantic-extraction template for one scanned Grade-4 Math source set.

Copy this directory before editing it. This template intentionally contains no
keyword guessing and no default mathematical interpretation. Every source
question must receive an explicit QUESTION_SPECS entry before authoring can run.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source.json"
TOPIC_HINTS: list[str] = []
QUESTION_SPECS: Dict[str, Dict[str, Any]] = {}

REQUIRED_SPEC_FIELDS = (
    "concept_key",
    "concept_title",
    "scope_basis",
    "capability_refs",
    "prerequisite_refs",
    "problem_family_refs",
    "translation_refs",
    "quantity_structure",
    "representation_requirements",
    "learning_support_blueprint",
)


def _load_source() -> Dict[str, Any]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if payload.get("template_only") is True:
        raise ValueError("TEMPLATE_NOT_FILLED: set template_only=false only after faithful source transcription")
    source_set_id = str(payload.get("source_set_id") or "")
    if not source_set_id or "REPLACE_" in source_set_id:
        raise ValueError("TEMPLATE_NOT_FILLED: source_set_id")
    questions = payload.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("SOURCE_QUESTION_SET_REQUIRED")

    seen: set[str] = set()
    seen_display: set[str] = set()
    for row in questions:
        qref = str(row.get("question_ref") or "")
        if not qref:
            raise ValueError("SOURCE_QUESTION_REF_REQUIRED")
        if qref in seen:
            raise ValueError(f"DUPLICATE_SOURCE_QUESTION_REF: {qref}")
        seen.add(qref)

        display_ref = str(row.get("source_display_ref") or "")
        if not display_ref or "REPLACE_" in display_ref:
            raise ValueError(f"SOURCE_DISPLAY_REF_MISSING: {qref}")
        if display_ref in seen_display:
            raise ValueError(f"DUPLICATE_SOURCE_DISPLAY_REF: {display_ref}")
        seen_display.add(display_ref)

        raw = str(row.get("raw_text") or "")
        if not raw or "REPLACE_" in raw:
            raise ValueError(f"TEMPLATE_NOT_FILLED: {qref}.raw_text")
        numeric_tokens = row.get("source_numeric_tokens")
        if not isinstance(numeric_tokens, list) or any("REPLACE_" in str(x) for x in numeric_tokens):
            raise ValueError(f"SOURCE_NUMERIC_TOKENS_REQUIRED: {qref}")
        if row.get("source_issue") == "TEMPLATE_NOT_FILLED":
            raise ValueError(f"TEMPLATE_NOT_FILLED: {qref}.source_issue")
    return payload


def _validate_spec(qref: str, spec: Mapping[str, Any]) -> None:
    missing = [key for key in REQUIRED_SPEC_FIELDS if key not in spec]
    if missing:
        raise ValueError(f"SEMANTIC_MAPPING_INCOMPLETE: {qref}: missing {missing}")
    if spec.get("scope_basis") == "CURRICULUM_CONFIRMED" and not spec.get("authority_ref"):
        raise ValueError(f"CURRICULUM_CONFIRMED_WITHOUT_AUTHORITY_REF: {qref}")
    if not spec.get("capability_refs"):
        raise ValueError(f"SEMANTIC_MAPPING_INCOMPLETE: {qref}: capability_refs")
    if not spec.get("representation_requirements"):
        raise ValueError(f"SEMANTIC_MAPPING_INCOMPLETE: {qref}: representation_requirements")
    if not spec.get("learning_support_blueprint"):
        raise ValueError(f"SEMANTIC_MAPPING_INCOMPLETE: {qref}: learning_support_blueprint")


def _source_identity(row: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "source_ref": str(row["question_ref"]),
        "source_display_ref": str(row["source_display_ref"]),
        "source_text": str(row["raw_text"]),
        "source_numeric_tokens": [str(x) for x in row.get("source_numeric_tokens") or []],
        "source_asset_ref": row.get("asset_ref"),
        "source_page_or_image_index": row.get("page_or_image_index"),
        "source_section_label": row.get("source_section_label"),
        "source_item_label": row.get("source_item_label"),
        "source_issue": row.get("source_issue"),
    }


def build_primary_input() -> Dict[str, Any]:
    source = _load_source()
    source_set_id = str(source["source_set_id"])
    questions: list[Dict[str, Any]] = []

    source_refs = {str(row["question_ref"]) for row in source["questions"]}
    extra_specs = sorted(set(QUESTION_SPECS) - source_refs)
    if extra_specs:
        raise ValueError(f"SEMANTIC_SPEC_WITHOUT_SOURCE_QUESTION: {extra_specs}")

    for row in source["questions"]:
        qref = str(row["question_ref"])
        if qref not in QUESTION_SPECS:
            raise ValueError(f"SEMANTIC_EVIDENCE_REQUIRED: {qref}; add an explicit QUESTION_SPECS entry")
        spec = QUESTION_SPECS[qref]
        _validate_spec(qref, spec)

        ambiguity: list[str] = []
        if row.get("source_issue"):
            ambiguity.append(str(row["source_issue"]))

        evidence = {
            "question_ref": qref,
            "source_ref": source_set_id,
            "source_identity": _source_identity(row),
            "raw_text": row["raw_text"],
            "concept_key": spec["concept_key"],
            "concept_title": spec["concept_title"],
            "scope_basis": spec["scope_basis"],
            "authority_ref": spec.get("authority_ref"),
            "capability_refs": list(spec["capability_refs"]),
            "prerequisite_refs": list(spec["prerequisite_refs"]),
            "problem_family_refs": list(spec["problem_family_refs"]),
            "translation_refs": list(spec["translation_refs"]),
            "quantity_structure": spec["quantity_structure"],
            "representation_requirements": list(spec["representation_requirements"]),
            "learning_support_blueprint": spec["learning_support_blueprint"],
            "ambiguity": ambiguity,
            "source_refs": [source_set_id, qref],
        }
        questions.append({"question_ref": qref, "text": row["raw_text"], "evidence": evidence})

    return {
        "schema_version": "1.0.0",
        "input_id": f"{source_set_id}-PRIMARY-INPUT",
        "question_set": {"source_ref": source_set_id, "questions": questions},
        "topic_hints": list(TOPIC_HINTS),
    }


if __name__ == "__main__":
    print(json.dumps(build_primary_input(), indent=2))
