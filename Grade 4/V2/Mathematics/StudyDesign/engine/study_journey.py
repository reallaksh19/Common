"""Document-level Grade 4 study journey semantics.

This layer sits above task-level LearningRepresentationPlan.  It groups source
questions into teaching concepts and controls the order of instruction, worked
examples, guided practice, independent practice, transfer and self-check.

The publisher may realize this plan; it may not invent or reorder pedagogy.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping


TEACHING_BLOCKS = {"SEE_DISCOVER", "NOTICE", "CONNECT", "WORKED_EXAMPLE", "GUIDED_TRY", "ERROR_ANALYSIS"}
INDEPENDENT_BLOCKS = {"INDEPENDENT_TRY", "TRANSFER", "RETRIEVAL"}
ANSWER_VISIBLE = {"WORKED_EXAMPLE", "ANSWER_KEY_ONLY"}


class StudyJourneyError(ValueError):
    pass


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise StudyJourneyError(f"{code}: {detail}")


def validate_study_journey(plan: Mapping[str, Any]) -> Dict[str, Any]:
    _require(plan.get("schema_version") == "1.0.0", "SCHEMA_VERSION", str(plan.get("schema_version")))
    _require(plan.get("grade_level") == 4, "GRADE_LEVEL", str(plan.get("grade_level")))
    modules = list(plan.get("modules") or [])
    _require(bool(modules), "MODULES_REQUIRED", "study journey has no modules")

    module_ids: set[str] = set()
    block_ids: set[str] = set()
    covered: set[str] = set()
    worked_example_count = 0
    independent_count = 0

    for module in modules:
        module_id = str(module.get("module_id") or "")
        _require(bool(module_id), "MODULE_ID_REQUIRED", repr(module))
        _require(module_id not in module_ids, "DUPLICATE_MODULE_ID", module_id)
        module_ids.add(module_id)
        source_refs = {str(x) for x in (module.get("source_refs") or [])}
        _require(bool(source_refs), "MODULE_SOURCE_REFS_REQUIRED", module_id)
        covered.update(source_refs)

        blocks = list(module.get("blocks") or [])
        _require(bool(blocks), "MODULE_BLOCKS_REQUIRED", module_id)
        seen_teaching = False
        for block in blocks:
            block_id = str(block.get("block_id") or "")
            block_type = str(block.get("block_type") or "")
            visibility = str(block.get("answer_visibility") or "")
            _require(bool(block_id), "BLOCK_ID_REQUIRED", module_id)
            _require(block_id not in block_ids, "DUPLICATE_BLOCK_ID", block_id)
            block_ids.add(block_id)

            if block_type in TEACHING_BLOCKS:
                seen_teaching = True
            if block_type == "WORKED_EXAMPLE":
                worked_example_count += 1
            if block_type in INDEPENDENT_BLOCKS:
                independent_count += 1
                _require(seen_teaching or block_type == "RETRIEVAL", "TEACH_BEFORE_INDEPENDENT", f"{module_id}/{block_id}")

            if visibility in ANSWER_VISIBLE:
                _require(block_type == "WORKED_EXAMPLE" or visibility == "ANSWER_KEY_ONLY", "ANSWER_VISIBILITY_SCOPE", f"{module_id}/{block_id}")
            if block_type in INDEPENDENT_BLOCKS:
                _require(visibility == "HIDDEN", "INDEPENDENT_ANSWER_LEAK", f"{module_id}/{block_id}")
            if visibility == "WORKED_EXAMPLE":
                _require(bool(str(block.get("solution_text") or "").strip()), "WORKED_SOLUTION_REQUIRED", block_id)

            block_refs = {str(x) for x in (block.get("source_refs") or [])}
            _require(block_refs.issubset(source_refs), "BLOCK_SOURCE_OUTSIDE_MODULE", f"{block_id}: {sorted(block_refs - source_refs)}")

        # Procedural/concept modules should not be worksheet-only.
        _require(any(str(b.get("block_type")) in TEACHING_BLOCKS for b in blocks), "TEACHING_BLOCK_REQUIRED", module_id)

    required = {str(x) for x in ((plan.get("source_coverage") or {}).get("required_source_refs") or [])}
    declared_covered = {str(x) for x in ((plan.get("source_coverage") or {}).get("covered_source_refs") or [])}
    _require(covered == declared_covered, "DECLARED_COVERAGE_MISMATCH", f"computed={sorted(covered)} declared={sorted(declared_covered)}")
    _require(required.issubset(covered), "SOURCE_COVERAGE_GAP", str(sorted(required - covered)))
    _require(worked_example_count >= 1, "WORKED_EXAMPLE_REQUIRED", "journey has no worked example")
    _require(independent_count >= 1, "INDEPENDENT_EVIDENCE_REQUIRED", "journey has no independent task")

    return {
        "status": "PASS",
        "module_count": len(modules),
        "block_count": len(block_ids),
        "worked_example_count": worked_example_count,
        "independent_block_count": independent_count,
        "source_coverage_count": len(covered),
    }


def coverage_refs(plan: Mapping[str, Any]) -> set[str]:
    return {str(ref) for module in (plan.get("modules") or []) for ref in (module.get("source_refs") or [])}
