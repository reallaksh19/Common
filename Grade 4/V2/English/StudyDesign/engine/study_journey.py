"""Document-level Grade 4 English study journey semantics.

This layer fixes the RCA gap between task-level QuestionEvidence and publication.
A source question must map to required learning objects, which contain real teaching
blocks. Source coverage references those block IDs; boolean claims are forbidden.
Publication may render the blocks but may not invent missing pedagogy.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping


TEACH_TYPES = {
    "CONCEPT", "SOURCE_RULE", "VOCABULARY", "TEXT_ANALYSIS", "READING_ROUTINE",
    "SOURCE_BOUNDARY", "CONTRAST", "MISCONCEPTION_CHECK", "REFERENCE",
}
MODEL_TYPES = {"WORKED_EXAMPLE", "ANNOTATED_MODEL"}
PRACTICE_TYPES = {"GUIDED_PRACTICE", "INDEPENDENT_RETRY", "TRANSFER", "RETRIEVAL"}
HINT_TYPES = {"HINT_LADDER", "DIAGNOSTIC_PROBE"}
VERIFY_TYPES = {"INDEPENDENT_RETRY", "TRANSFER", "RETRIEVAL"}
ANSWER_TYPES = {"RUBRIC", "ANSWER_CHECK"}
INDEPENDENT_TYPES = VERIFY_TYPES
ANSWER_VISIBLE = {"WORKED_EXAMPLE", "ANSWER_KEY_ONLY"}


class StudyJourneyError(ValueError):
    pass


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise StudyJourneyError(f"{code}: {detail}")


def _refs(entry: Mapping[str, Any], field: str) -> list[str]:
    return [str(x) for x in (entry.get(field) or [])]


def validate_study_journey(plan: Mapping[str, Any]) -> Dict[str, Any]:
    _require(plan.get("schema_version") == "1.0.0", "SCHEMA_VERSION", str(plan.get("schema_version")))
    _require(plan.get("grade_level") == 4, "GRADE_LEVEL", str(plan.get("grade_level")))
    _require(plan.get("subject") == "ENGLISH", "SUBJECT", str(plan.get("subject")))

    objects = list(plan.get("learning_objects") or [])
    _require(bool(objects), "LEARNING_OBJECTS_REQUIRED", "no learning objects")

    object_index: dict[str, Mapping[str, Any]] = {}
    block_index: dict[str, tuple[str, Mapping[str, Any]]] = {}
    source_to_objects: dict[str, set[str]] = {}
    independent_count = 0
    worked_count = 0

    for obj in objects:
        object_id = str(obj.get("learning_object_id") or "")
        _require(bool(object_id), "LEARNING_OBJECT_ID_REQUIRED", repr(obj))
        _require(object_id not in object_index, "DUPLICATE_LEARNING_OBJECT_ID", object_id)
        object_index[object_id] = obj
        obj_sources = {str(x) for x in (obj.get("source_refs") or [])}
        _require(bool(obj_sources), "LEARNING_OBJECT_SOURCE_REFS_REQUIRED", object_id)
        for ref in obj_sources:
            source_to_objects.setdefault(ref, set()).add(object_id)

        blocks = list(obj.get("blocks") or [])
        _require(bool(blocks), "TEACHING_BLOCKS_REQUIRED", object_id)
        has_teach = False
        has_model = False
        has_practice = False
        has_hint = False
        has_verify = False
        for block in blocks:
            block_id = str(block.get("block_id") or "")
            block_type = str(block.get("block_type") or "")
            _require(bool(block_id), "BLOCK_ID_REQUIRED", object_id)
            _require(block_id not in block_index, "DUPLICATE_BLOCK_ID", block_id)
            block_index[block_id] = (object_id, block)

            block_sources = {str(x) for x in (block.get("source_refs") or [])}
            _require(block_sources.issubset(obj_sources), "BLOCK_SOURCE_OUTSIDE_LEARNING_OBJECT", f"{block_id}: {sorted(block_sources - obj_sources)}")

            if block_type in TEACH_TYPES:
                has_teach = True
            if block_type in MODEL_TYPES:
                has_model = True
                worked_count += 1
            if block_type in PRACTICE_TYPES:
                has_practice = True
            if block_type in HINT_TYPES:
                has_hint = True
            if block_type in VERIFY_TYPES:
                has_verify = True
                independent_count += 1

            visibility = str(block.get("answer_visibility") or "")
            if block_type in INDEPENDENT_TYPES:
                _require(visibility == "HIDDEN", "INDEPENDENT_ANSWER_LEAK", block_id)
                _require(str(block.get("support_level") or "H0") == "H0", "INDEPENDENT_NOT_H0", block_id)
            if visibility == "WORKED_EXAMPLE":
                _require(block_type in MODEL_TYPES, "WORKED_VISIBILITY_SCOPE", block_id)
                _require(bool(str(block.get("solution_text") or "").strip()), "WORKED_SOLUTION_REQUIRED", block_id)
            if visibility == "ANSWER_KEY_ONLY":
                _require(str(block.get("audience")) in {"ADULT", "BOTH"}, "ANSWER_KEY_AUDIENCE", block_id)

            if block_type == "SOURCE_BOUNDARY":
                _require(str(block.get("provenance")) == "SOURCE_DERIVED", "BOUNDARY_MUST_BE_SOURCE_DERIVED", block_id)

        _require(has_teach, "TEACH_BLOCK_REQUIRED", object_id)
        _require(has_model, "MODEL_BLOCK_REQUIRED", object_id)
        _require(has_practice, "PRACTICE_BLOCK_REQUIRED", object_id)
        _require(has_hint, "HINT_BLOCK_REQUIRED", object_id)
        _require(has_verify, "VERIFY_BLOCK_REQUIRED", object_id)

        evidence_refs = _refs(obj, "independent_evidence_refs")
        _require(bool(evidence_refs), "INDEPENDENT_EVIDENCE_REFS_REQUIRED", object_id)
        for ref in evidence_refs:
            _require(ref in block_index, "UNKNOWN_INDEPENDENT_EVIDENCE_REF", f"{object_id}/{ref}")
            owner, block = block_index[ref]
            _require(owner == object_id, "INDEPENDENT_EVIDENCE_OUTSIDE_OBJECT", f"{object_id}/{ref}")
            _require(str(block.get("block_type")) in VERIFY_TYPES, "INDEPENDENT_EVIDENCE_WRONG_TYPE", f"{object_id}/{ref}")

    required = {str(x) for x in (plan.get("required_source_refs") or [])}
    _require(bool(required), "REQUIRED_SOURCE_REFS", "empty")
    coverage_entries = list(plan.get("source_coverage") or [])
    _require(bool(coverage_entries), "SOURCE_COVERAGE_REQUIRED", "empty")

    coverage_by_source: dict[str, Mapping[str, Any]] = {}
    role_specs = {
        "teach_block_refs": TEACH_TYPES,
        "model_block_refs": MODEL_TYPES,
        "practice_block_refs": PRACTICE_TYPES,
        "hint_block_refs": HINT_TYPES,
        "verify_block_refs": VERIFY_TYPES,
        "answer_or_rubric_block_refs": ANSWER_TYPES,
    }

    for coverage in coverage_entries:
        source_ref = str(coverage.get("source_ref") or "")
        _require(bool(source_ref), "COVERAGE_SOURCE_REF_REQUIRED", repr(coverage))
        _require(source_ref not in coverage_by_source, "DUPLICATE_SOURCE_COVERAGE", source_ref)
        coverage_by_source[source_ref] = coverage

        object_refs = set(_refs(coverage, "learning_object_refs"))
        _require(bool(object_refs), "COVERAGE_LEARNING_OBJECT_REQUIRED", source_ref)
        for object_ref in object_refs:
            _require(object_ref in object_index, "UNKNOWN_COVERAGE_LEARNING_OBJECT", f"{source_ref}/{object_ref}")
            _require(source_ref in set(_refs(object_index[object_ref], "source_refs")), "SOURCE_NOT_IN_COVERAGE_OBJECT", f"{source_ref}/{object_ref}")

        for field, allowed_types in role_specs.items():
            refs = _refs(coverage, field)
            _require(bool(refs), "COVERAGE_ROLE_EMPTY", f"{source_ref}/{field}")
            for block_ref in refs:
                _require(block_ref in block_index, "UNKNOWN_COVERAGE_BLOCK", f"{source_ref}/{field}/{block_ref}")
                owner, block = block_index[block_ref]
                _require(owner in object_refs, "COVERAGE_BLOCK_OUTSIDE_OBJECT", f"{source_ref}/{block_ref}")
                _require(source_ref in set(_refs(block, "source_refs")), "COVERAGE_BLOCK_SOURCE_MISMATCH", f"{source_ref}/{block_ref}")
                _require(str(block.get("block_type")) in allowed_types, "COVERAGE_ROLE_WRONG_BLOCK_TYPE", f"{source_ref}/{field}/{block_ref}/{block.get('block_type')}")

    declared = set(coverage_by_source)
    _require(required == declared, "SOURCE_COVERAGE_SET_MISMATCH", f"missing={sorted(required-declared)} extra={sorted(declared-required)}")
    _require(required.issubset(source_to_objects), "SOURCE_WITHOUT_LEARNING_OBJECT", str(sorted(required - set(source_to_objects))))
    _require(worked_count >= len(objects), "INSUFFICIENT_MODELS", f"worked={worked_count} objects={len(objects)}")
    _require(independent_count >= len(objects), "INSUFFICIENT_INDEPENDENT_EVIDENCE", f"independent={independent_count} objects={len(objects)}")

    return {
        "status": "PASS",
        "learning_object_count": len(object_index),
        "teaching_block_count": len(block_index),
        "source_coverage_count": len(coverage_by_source),
        "worked_model_count": worked_count,
        "independent_evidence_count": independent_count,
    }


def block_index(plan: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(block["block_id"]): block
        for obj in (plan.get("learning_objects") or [])
        for block in (obj.get("blocks") or [])
    }
