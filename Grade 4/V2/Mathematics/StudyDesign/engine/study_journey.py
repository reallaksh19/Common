"""Document-level Grade 4 study journey semantics.

This layer sits above task-level LearningRepresentationPlan. It groups source
questions into teaching concepts and controls the order of instruction, worked
examples, guided practice, independent practice, transfer and self-check.

The publisher may realize this plan; it may not invent or reorder pedagogy.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Mapping


TEACHING_BLOCKS = {"SEE_DISCOVER", "NOTICE", "CONNECT", "WORKED_EXAMPLE", "GUIDED_TRY", "ERROR_ANALYSIS"}
INDEPENDENT_BLOCKS = {"INDEPENDENT_TRY", "TRANSFER", "RETRIEVAL"}
QUESTION_BLOCKS = {"WORKED_EXAMPLE", "GUIDED_TRY", "INDEPENDENT_TRY", "ERROR_ANALYSIS", "TRANSFER", "RETRIEVAL"}
ANSWER_VISIBLE = {"WORKED_EXAMPLE", "ANSWER_KEY_ONLY"}
SOURCE_NUMBERING_RE = re.compile(r"^(?:[IVXLCDM]+\s*\([A-Za-z0-9]+\)|[A-Za-z]?\d+\s*\([A-Za-z0-9]+\)|[A-Za-z]?\d+[.)]?)$", re.I)
NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


class StudyJourneyError(ValueError):
    pass


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise StudyJourneyError(f"{code}: {detail}")


def _norm(text: Any) -> str:
    return " ".join(str(text or "").replace("×", "x").replace("÷", "/").split()).strip().lower()


def _norm_num(token: Any) -> str:
    return str(token).replace(",", "").strip()


def _numeric_tokens(text: Any) -> list[str]:
    return [_norm_num(x) for x in NUMBER_RE.findall(str(text or ""))]


def _validate_question(question: Mapping[str, Any], block: Mapping[str, Any], block_type: str) -> None:
    qid = str(question.get("question_id") or "")
    origin = str(question.get("origin") or "")
    display_ref = str(question.get("display_ref") or "")
    prompt = str(question.get("prompt") or "")
    policy = str(question.get("task_support_policy") or "")
    answer = question.get("answer_contract") or {}
    hint = question.get("hint_contract") or {}

    _require(bool(qid), "QUESTION_ID_REQUIRED", str(block.get("block_id")))
    _require(origin in {"SOURCE", "GENERATED_PRACTICE"}, "QUESTION_ORIGIN_INVALID", qid)
    _require(bool(display_ref), "QUESTION_DISPLAY_REF_REQUIRED", qid)
    _require(bool(prompt.strip()), "SOURCE_QUESTION_TEXT_MISSING" if origin == "SOURCE" else "QUESTION_PROMPT_MISSING", qid)
    _require(policy in {"NUMERIC_FIRST", "VISUAL_FIRST", "MIXED", "NO_HINT"}, "HINT_MODALITY_MISSING", qid)

    _require(bool(answer), "QUESTION_WITHOUT_ANSWER_CONTRACT", qid)
    _require(bool(str(answer.get("answer_text") or "").strip()), "QUESTION_WITHOUT_ANSWER_CONTRACT", qid)
    _require(bool(str(answer.get("answer_ref") or "").strip()), "ANSWER_CHECK_ROUTE_MISSING", qid)
    route = str(answer.get("check_route") or "")
    _require(route in {"INLINE", "CHECK_AFTER_TRY", "ANSWER_MAP", "TEACHER_KEY"}, "ANSWER_CHECK_ROUTE_MISSING", qid)
    if block_type == "WORKED_EXAMPLE":
        _require(route == "INLINE", "WORKED_EXAMPLE_ANSWER_NOT_INLINE", qid)
    if block_type in INDEPENDENT_BLOCKS:
        _require(route in {"ANSWER_MAP", "TEACHER_KEY"}, "INDEPENDENT_ANSWER_ROUTE_INVALID", qid)

    modality = str(hint.get("modality") or "")
    _require(modality in {"NUMERIC", "VISUAL", "MIXED", "NONE"}, "HINT_MODALITY_MISSING", qid)
    _require(hint.get("may_reveal_final_answer") is False, "HINT_FINAL_ANSWER_POLICY_INVALID", qid)
    hint_text = str(hint.get("hint_text") or "")
    if policy == "NO_HINT":
        _require(modality == "NONE", "HINT_POLICY_MODALITY_MISMATCH", qid)
    elif policy == "NUMERIC_FIRST":
        _require(modality in {"NUMERIC", "MIXED"}, "NUMERIC_TASK_WITH_GENERIC_TEXT_ONLY_HINT", qid)
        _require(bool(_numeric_tokens(hint_text)), "NUMERIC_TASK_WITH_GENERIC_TEXT_ONLY_HINT", qid)
    elif policy == "VISUAL_FIRST":
        _require(modality in {"VISUAL", "MIXED"}, "HINT_POLICY_MODALITY_MISMATCH", qid)
        _require(bool(hint.get("visual_ref")), "VISUAL_HINT_REFERENCE_MISSING", qid)
    elif policy == "MIXED":
        _require(modality == "MIXED", "HINT_POLICY_MODALITY_MISMATCH", qid)
        _require(bool(hint.get("visual_ref")), "VISUAL_HINT_REFERENCE_MISSING", qid)

    if route != "INLINE" and hint_text:
        answer_text = _norm(answer.get("answer_text"))
        _require(not (answer_text and answer_text in _norm(hint_text)), "HINT_REVEALS_ANSWER", qid)

    if origin == "SOURCE":
        src = question.get("source_identity") or {}
        source_ref = str(src.get("source_ref") or "")
        source_display_ref = str(src.get("source_display_ref") or "")
        source_text = str(src.get("source_text") or "")
        _require(bool(source_ref), "SOURCE_REF_MISSING", qid)
        _require(bool(source_display_ref), "SOURCE_DISPLAY_REF_MISSING", qid)
        _require(display_ref == source_display_ref, "SOURCE_ITEM_RENUMBERED", f"{qid}: {display_ref!r} != {source_display_ref!r}")
        _require(source_ref in {str(x) for x in (block.get("source_refs") or [])}, "SOURCE_REF_OUTSIDE_BLOCK", qid)
        _require(bool(source_text.strip()), "SOURCE_QUESTION_TEXT_MISSING", qid)
        _require(_norm(source_text) in _norm(prompt), "SOURCE_QUESTION_TEXT_MISSING", qid)
        source_numbers = [_norm_num(x) for x in (src.get("source_numeric_tokens") or [])]
        prompt_numbers = set(_numeric_tokens(prompt))
        missing_numbers = [x for x in source_numbers if x not in prompt_numbers]
        _require(not missing_numbers, "SOURCE_NUMERIC_VALUE_DROPPED", f"{qid}: {missing_numbers}")
    else:
        _require(question.get("source_identity") in (None, {}), "GENERATED_ITEM_HAS_SOURCE_IDENTITY", qid)
        _require(not SOURCE_NUMBERING_RE.match(display_ref.strip()), "GENERATED_ITEM_USES_SOURCE_NUMBERING", f"{qid}: {display_ref}")
        _require(display_ref.lower().startswith(("practice ", "fresh try ", "challenge ", "check ")), "GENERATED_ITEM_LABEL_INVALID", f"{qid}: {display_ref}")


def validate_study_journey(plan: Mapping[str, Any]) -> Dict[str, Any]:
    _require(plan.get("schema_version") == "1.0.0", "SCHEMA_VERSION", str(plan.get("schema_version")))
    _require(plan.get("grade_level") == 4, "GRADE_LEVEL", str(plan.get("grade_level")))
    modules = list(plan.get("modules") or [])
    _require(bool(modules), "MODULES_REQUIRED", "study journey has no modules")

    module_ids: set[str] = set()
    block_ids: set[str] = set()
    question_ids: set[str] = set()
    answer_refs: set[str] = set()
    source_question_refs: set[str] = set()
    covered: set[str] = set()
    worked_example_count = 0
    independent_count = 0
    learner_question_count = 0

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

            questions = list(block.get("questions") or [])
            if block_type in QUESTION_BLOCKS:
                _require(bool(questions), "LEARNER_QUESTION_REQUIRED", f"{module_id}/{block_id}")
            for question in questions:
                _validate_question(question, block, block_type)
                qid = str(question["question_id"])
                _require(qid not in question_ids, "DUPLICATE_QUESTION_ID", qid)
                question_ids.add(qid)
                aref = str((question.get("answer_contract") or {}).get("answer_ref") or "")
                _require(aref not in answer_refs, "DUPLICATE_ANSWER_REF", aref)
                answer_refs.add(aref)
                if str(question.get("origin") or "") == "SOURCE":
                    source_question_refs.add(str((question.get("source_identity") or {}).get("source_ref") or ""))
                learner_question_count += 1

        _require(any(str(b.get("block_type")) in TEACHING_BLOCKS for b in blocks), "TEACHING_BLOCK_REQUIRED", module_id)

    required = {str(x) for x in ((plan.get("source_coverage") or {}).get("required_source_refs") or [])}
    declared_covered = {str(x) for x in ((plan.get("source_coverage") or {}).get("covered_source_refs") or [])}
    _require(covered == declared_covered, "DECLARED_COVERAGE_MISMATCH", f"computed={sorted(covered)} declared={sorted(declared_covered)}")
    _require(required.issubset(covered), "SOURCE_COVERAGE_GAP", str(sorted(required - covered)))
    _require(required.issubset(source_question_refs), "SOURCE_QUESTION_COVERAGE_GAP", str(sorted(required - source_question_refs)))
    _require(worked_example_count >= 1, "WORKED_EXAMPLE_REQUIRED", "journey has no worked example")
    _require(independent_count >= 1, "INDEPENDENT_EVIDENCE_REQUIRED", "journey has no independent task")

    return {
        "status": "PASS",
        "module_count": len(modules),
        "block_count": len(block_ids),
        "learner_question_count": learner_question_count,
        "answer_contract_count": len(answer_refs),
        "source_question_count": len(source_question_refs),
        "worked_example_count": worked_example_count,
        "independent_block_count": independent_count,
        "source_coverage_count": len(covered),
    }


def coverage_refs(plan: Mapping[str, Any]) -> set[str]:
    return {str(ref) for module in (plan.get("modules") or []) for ref in (module.get("source_refs") or [])}
