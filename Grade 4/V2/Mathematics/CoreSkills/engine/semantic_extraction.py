"""Normalize grounded semantic extraction into QuestionEvidence for PR #336 authoring.

This module does not infer mathematics from prose. An upstream model/manual/source
extractor supplies claims. This module verifies provenance and canonical refs,
then attaches validated QuestionEvidence to the PrimaryMathInput question set.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, Mapping

from .author import AuthoringError, RegistryIndex, validate_question_evidence


def _norm_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def normalize_extraction(
    primary_input: Mapping[str, Any],
    extraction: Mapping[str, Any],
) -> Dict[str, Any]:
    if extraction.get("schema_version") != "1.0.0":
        raise AuthoringError("SEMANTIC_EXTRACTION_SCHEMA_INVALID", "schema_version must be 1.0.0")
    if not extraction.get("extraction_id"):
        raise AuthoringError("SEMANTIC_EXTRACTION_SCHEMA_INVALID", "extraction_id is required")

    extractor = extraction.get("extractor") or {}
    kind = extractor.get("kind")
    if kind not in {"MODEL_ASSISTED", "MANUAL", "SOURCE_STRUCTURED"} or not extractor.get("name"):
        raise AuthoringError("SEMANTIC_EXTRACTION_PROVENANCE_MISSING", "extractor kind/name required")

    enriched = copy.deepcopy(dict(primary_input))
    question_set = enriched.get("question_set") or {}
    questions = list(question_set.get("questions") or [])
    if not questions:
        raise AuthoringError("QUESTION_SET_REQUIRED", "question_set.questions must be non-empty")

    source_by_ref = {}
    for q in questions:
        qref = q.get("question_ref")
        if not qref or qref in source_by_ref:
            raise AuthoringError("QUESTION_REFERENCE_INVALID", f"duplicate/missing question_ref: {qref}")
        source_by_ref[qref] = q

    extracted_rows = list(extraction.get("questions") or [])
    extracted_by_ref = {}
    for row in extracted_rows:
        qref = row.get("question_ref")
        if not qref or qref in extracted_by_ref:
            raise AuthoringError("SEMANTIC_EXTRACTION_DUPLICATE_QUESTION", str(qref))
        extracted_by_ref[qref] = row

    expected = set(source_by_ref)
    actual = set(extracted_by_ref)
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise AuthoringError(
            "SEMANTIC_EXTRACTION_QUESTION_COVERAGE_MISMATCH",
            f"missing={missing}, extra={extra}",
        )

    registry = RegistryIndex()
    for qref, q in source_by_ref.items():
        row = extracted_by_ref[qref]
        source_text = row.get("source_text")
        raw_text = q.get("text") if q.get("text") is not None else q.get("raw_text")
        if _norm_text(source_text) != _norm_text(raw_text):
            raise AuthoringError(
                "SEMANTIC_EXTRACTION_SOURCE_TEXT_MISMATCH",
                f"{qref} extraction is not bound to the exact source question",
            )

        claims = copy.deepcopy(row.get("claims") or {})
        confidence = claims.get("confidence")
        ambiguity = list(claims.get("ambiguity") or [])
        if kind == "MODEL_ASSISTED" and confidence is None:
            raise AuthoringError("MODEL_ASSISTED_EXTRACTION_CONFIDENCE_MISSING", qref)
        if confidence is not None and not (0 <= float(confidence) <= 1):
            raise AuthoringError("SEMANTIC_EXTRACTION_CONFIDENCE_INVALID", qref)
        if confidence is not None and float(confidence) < 0.65:
            if claims.get("scope_basis") != "MAPPING_PENDING" and not ambiguity:
                raise AuthoringError(
                    "LOW_CONFIDENCE_EXTRACTION_SILENTLY_FORCED",
                    f"{qref} confidence={confidence} requires ambiguity or MAPPING_PENDING",
                )

        evidence = claims
        evidence["question_ref"] = qref
        evidence["raw_text"] = str(raw_text or "")
        evidence["source_ref"] = row.get("source_ref") or question_set.get("source_ref")
        source_refs = list(evidence.get("source_refs") or [])
        if evidence.get("source_ref") and evidence["source_ref"] not in source_refs:
            source_refs.append(evidence["source_ref"])
        source_refs.append(f"extraction://{extraction['extraction_id']}#{qref}")
        evidence["source_refs"] = sorted(set(source_refs))

        # Confidence is extraction provenance, not part of the canonical semantic claim.
        evidence.pop("confidence", None)
        validate_question_evidence(evidence, registry)
        q["evidence"] = evidence

    question_set["extraction_provenance"] = {
        "extraction_id": extraction["extraction_id"],
        "extractor": copy.deepcopy(extractor),
        "question_count": len(questions),
        "policy": "CLAIMS_VERIFIED_NOT_INFERRED_BY_NORMALIZER",
    }
    enriched["question_set"] = question_set
    return enriched
