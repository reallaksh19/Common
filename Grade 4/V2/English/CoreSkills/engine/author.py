"""Deterministic Grade-4 English V2 semantic authoring.

This module intentionally does not infer English semantics from raw question prose.
The caller must provide normalized QuestionEvidence/SourceModel/LearnerEvidence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"


class EnglishAuthoringError(ValueError):
    """Raised when normalized evidence violates the English V2 authoring boundary."""


def _load_ids(filename: str, collection_key: str) -> set[str]:
    payload = json.loads((REGISTRY / filename).read_text(encoding="utf-8"))
    return {row["id"] for row in payload[collection_key]}


CAPABILITY_IDS = _load_ids("capability_registry.json", "capabilities")
TASK_FAMILY_IDS = _load_ids("task_family_registry.json", "task_families")
RESPONSE_STRUCTURE_IDS = _load_ids("response_structure_registry.json", "response_structures")
REPRESENTATION_IDS = _load_ids("representation_registry.json", "representations")

FORBIDDEN_INVENTED_CATEGORIES = {
    "QUALITY",
    "PHYSICAL_QUALITY",
    "QUALITY_TYPE",
    "CONDITION",
}


def _require_nonempty_strings(values: Iterable[Any], path: str) -> list[str]:
    values = list(values)
    if not values or any(not isinstance(v, str) or not v.strip() for v in values):
        raise EnglishAuthoringError(f"{path} must contain non-empty strings")
    return values


def validate_source_model(model: Mapping[str, Any]) -> None:
    model_id = model.get("source_model_id")
    if not isinstance(model_id, str) or not model_id:
        raise EnglishAuthoringError("source_model_id is required")

    categories = _require_nonempty_strings(model.get("categories", []), f"{model_id}.categories")
    forbidden = FORBIDDEN_INVENTED_CATEGORIES.intersection(categories)
    if forbidden:
        raise EnglishAuthoringError(
            f"{model_id} invents forbidden source categories: {sorted(forbidden)}"
        )

    ordering = model.get("ordering", [])
    if ordering:
        ordering = _require_nonempty_strings(ordering, f"{model_id}.ordering")
        unknown = [item for item in ordering if item not in categories]
        if unknown:
            raise EnglishAuthoringError(
                f"{model_id}.ordering contains categories absent from source categories: {unknown}"
            )

    boundary = model.get("boundary_policy", {})
    if boundary.get("no_force_fit") is not True:
        raise EnglishAuthoringError(f"{model_id} must set boundary_policy.no_force_fit=true")


def validate_question_evidence(evidence: Mapping[str, Any], source_models: Mapping[str, Mapping[str, Any]]) -> None:
    qref = evidence.get("question_ref")
    if not isinstance(qref, str) or not qref:
        raise EnglishAuthoringError("question_ref is required")

    capabilities = _require_nonempty_strings(evidence.get("capability_refs", []), f"{qref}.capability_refs")
    missing_caps = [cap for cap in capabilities if cap not in CAPABILITY_IDS]
    if missing_caps:
        raise EnglishAuthoringError(f"{qref} uses unknown capability ids: {missing_caps}")

    families = _require_nonempty_strings(evidence.get("task_family_refs", []), f"{qref}.task_family_refs")
    missing_families = [family for family in families if family not in TASK_FAMILY_IDS]
    if missing_families:
        raise EnglishAuthoringError(f"{qref} uses unknown task family ids: {missing_families}")

    response = evidence.get("response_demand") or {}
    response_ref = response.get("response_structure_ref")
    if response_ref not in RESPONSE_STRUCTURE_IDS:
        raise EnglishAuthoringError(f"{qref} uses unknown response structure: {response_ref!r}")

    reps = evidence.get("representation_requirements") or []
    if not reps:
        raise EnglishAuthoringError(f"{qref} requires at least one representation requirement")
    for rep in reps:
        rep_id = rep.get("representation_id")
        if rep_id not in REPRESENTATION_IDS:
            raise EnglishAuthoringError(f"{qref} uses unknown representation id: {rep_id!r}")

    source_model_ref = evidence.get("source_model_ref")
    if source_model_ref is not None and source_model_ref not in source_models:
        raise EnglishAuthoringError(f"{qref} references unknown source model {source_model_ref!r}")

    blueprint = evidence.get("learning_support_blueprint") or {}
    for level in ("H1", "H2", "H3"):
        if not isinstance(blueprint.get(level), Mapping):
            raise EnglishAuthoringError(f"{qref}.learning_support_blueprint.{level} is required")
    retry = blueprint.get("fresh_retry") or {}
    if retry.get("required") is not True or retry.get("conceptual_support") != "H0":
        raise EnglishAuthoringError(f"{qref} must require a fresh H0 retry")

    coverage = blueprint.get("coverage_obligations") or {}
    required_coverage = ("teach", "model", "practice", "hints", "verify", "answer_or_rubric")
    missing_coverage = [name for name in required_coverage if coverage.get(name) is not True]
    if missing_coverage:
        raise EnglishAuthoringError(f"{qref} is missing coverage obligations: {missing_coverage}")

    if response.get("teacher_or_source_judgement_required") is True:
        if "model_answer" in evidence or "exact_answer" in response:
            raise EnglishAuthoringError(
                f"{qref} is an interpretive/open response and must not be reduced to exact-answer matching"
            )


def validate_learner_evidence(row: Mapping[str, Any], known_question_refs: set[str]) -> None:
    qref = row.get("question_ref")
    if qref not in known_question_refs:
        raise EnglishAuthoringError(f"learner evidence references unknown question {qref!r}")
    support = row.get("conceptual_support")
    if support not in {"H0", "H1", "H2", "H3", "H4", "H5"}:
        raise EnglishAuthoringError(f"{qref}.conceptual_support is invalid")
    access = row.get("access_support")
    if not isinstance(access, list):
        raise EnglishAuthoringError(f"{qref}.access_support must be a list separate from conceptual support")


def author_core_skills(primary_input: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate normalized evidence and produce a deterministic CoreSkills handoff.

    No semantic inference is performed here. The output is a normalized, registry-
    validated package that LearningDesign may consume.
    """
    source_models_list = list(primary_input.get("source_models") or [])
    source_models = {row["source_model_id"]: row for row in source_models_list}
    if len(source_models) != len(source_models_list):
        raise EnglishAuthoringError("source_model_id values must be unique")
    for model in source_models_list:
        validate_source_model(model)

    question_evidence = list(primary_input.get("question_evidence") or [])
    if not question_evidence:
        raise EnglishAuthoringError("primary_input.question_evidence must not be empty")

    seen: set[str] = set()
    for row in question_evidence:
        qref = row.get("question_ref")
        if qref in seen:
            raise EnglishAuthoringError(f"duplicate question_ref: {qref}")
        validate_question_evidence(row, source_models)
        seen.add(qref)

    learner_evidence = list(primary_input.get("learner_evidence") or [])
    for row in learner_evidence:
        validate_learner_evidence(row, seen)

    return {
        "schema_version": "1.0.0",
        "grade": 4,
        "subject": "ENGLISH",
        "source": dict(primary_input.get("source") or {}),
        "source_models": source_models_list,
        "question_evidence": question_evidence,
        "learner_evidence": learner_evidence,
        "authoring_invariants": {
            "semantic_inference_from_raw_prose": False,
            "source_model_force_fit": False,
            "open_response_exact_string_grading": False,
            "learner_evidence_separate_from_source_truth": True,
            "fresh_h0_retry_required_after_support": True,
        },
    }
