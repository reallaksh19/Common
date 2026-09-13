"""Source-anchored visual-hint resolver for Grade 4 Mathematics V2.

The resolver does not invent diagrams in Publication. It binds each SOURCE
learner question to an already-authored representation requirement from the
semantic-extraction / LearningDesign evidence for that same source question.

Invariant for scanned-source study material:
    source question -> visual hint -> optional numeric/verbal hint -> answer route

Fresh generated independent practice may remain NO_HINT.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, Mapping


class SourceVisualHintError(ValueError):
    pass


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise SourceVisualHintError(f"{code}: {detail}")


def build_source_visual_catalog(primary_input: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Resolve one authored H1 visual per source question from QuestionEvidence.

    Selection priority is the H1 representation ref from the authored support
    blueprint. If the blueprint has no H1 ref, the first declared representation
    requirement is used. No keyword guessing or publisher-local semantics are
    permitted.
    """
    catalog: Dict[str, Dict[str, Any]] = {}
    questions = ((primary_input.get("question_set") or {}).get("questions") or [])
    for row in questions:
        qref = str(row.get("question_ref") or "")
        evidence = row.get("evidence") or {}
        reps = list(evidence.get("representation_requirements") or [])
        _require(bool(qref), "SOURCE_VISUAL_HINT_QUESTION_REF_MISSING", repr(row))
        _require(bool(reps), "SOURCE_VISUAL_HINT_REPRESENTATION_MISSING", qref)

        by_id = {str(rep.get("representation_id") or ""): rep for rep in reps}
        blueprint = evidence.get("learning_support_blueprint") or {}
        h1_ref = None
        for step in blueprint.get("hint_steps") or []:
            if str(step.get("level") or "") == "H1":
                h1_ref = str(step.get("representation_ref") or "") or None
                break
        selected = by_id.get(h1_ref or "") if h1_ref else None
        if selected is None:
            selected = reps[0]

        primitive_kind = str(selected.get("primitive_kind") or "")
        semantic_params = selected.get("semantic_params")
        _require(bool(primitive_kind), "SOURCE_VISUAL_HINT_PRIMITIVE_MISSING", qref)
        _require(isinstance(semantic_params, Mapping), "SOURCE_VISUAL_HINT_PARAMS_MISSING", qref)
        visual_ref = str(selected.get("representation_id") or f"VH-{qref}")
        catalog[qref] = {
            "visual_ref": visual_ref,
            "primitive_kind": primitive_kind,
            "semantic_params": dict(semantic_params),
            "fidelity": "SCHEMATIC",
            "provenance": str(selected.get("provenance") or "ENGINE_AUTHORED_VISUAL"),
            "validator_refs": list(selected.get("validator_refs") or []),
        }
    return catalog


def attach_source_visual_hints(
    plan: Mapping[str, Any],
    visual_catalog: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    """Return a deep-copied StudyJourney with visual hints bound to every SOURCE item.

    Existing numeric/verbal help is preserved and becomes MIXED support. A
    source question with no authored visual fails closed. GENERATED_PRACTICE is
    untouched, so fresh independent evidence can still be genuinely hint-free.
    """
    out = copy.deepcopy(plan)
    source_count = 0
    visual_count = 0
    for module in out.get("modules") or []:
        for block in module.get("blocks") or []:
            for question in block.get("questions") or []:
                if str(question.get("origin") or "") != "SOURCE":
                    continue
                source_count += 1
                src = question.get("source_identity") or {}
                source_ref = str(src.get("source_ref") or "")
                _require(bool(source_ref), "SOURCE_VISUAL_HINT_SOURCE_REF_MISSING", str(question.get("question_id")))
                visual = visual_catalog.get(source_ref)
                _require(visual is not None, "SOURCE_VISUAL_HINT_REQUIRED", source_ref)

                hint = question.setdefault("hint_contract", {})
                hint_text = hint.get("hint_text")
                hint["visual_ref"] = str(visual["visual_ref"])
                hint["visual_hint"] = {
                    "primitive_kind": str(visual["primitive_kind"]),
                    "semantic_params": dict(visual["semantic_params"]),
                    "fidelity": str(visual.get("fidelity") or "SCHEMATIC"),
                }
                hint["modality"] = "MIXED" if str(hint_text or "").strip() else "VISUAL"
                hint["may_reveal_final_answer"] = False
                question["task_support_policy"] = "MIXED" if str(hint_text or "").strip() else "VISUAL_FIRST"
                visual_count += 1

    _require(source_count > 0, "SOURCE_VISUAL_HINT_SOURCE_QUESTIONS_MISSING", "study journey")
    _require(source_count == visual_count, "SOURCE_VISUAL_HINT_COVERAGE_INCOMPLETE", f"{visual_count}/{source_count}")
    return out


def assert_source_visual_hint_coverage(plan: Mapping[str, Any]) -> Dict[str, int]:
    """Fail if a SOURCE learner question lacks a concrete visual-hint object."""
    source_count = 0
    visual_count = 0
    for module in plan.get("modules") or []:
        for block in module.get("blocks") or []:
            for question in block.get("questions") or []:
                if str(question.get("origin") or "") != "SOURCE":
                    continue
                source_count += 1
                hint = question.get("hint_contract") or {}
                visual = hint.get("visual_hint")
                _require(str(question.get("task_support_policy") or "") in {"VISUAL_FIRST", "MIXED"}, "SOURCE_VISUAL_HINT_POLICY_INVALID", str(question.get("question_id")))
                _require(str(hint.get("modality") or "") in {"VISUAL", "MIXED"}, "SOURCE_VISUAL_HINT_MODALITY_INVALID", str(question.get("question_id")))
                _require(bool(str(hint.get("visual_ref") or "").strip()), "SOURCE_VISUAL_HINT_REFERENCE_MISSING", str(question.get("question_id")))
                _require(isinstance(visual, Mapping), "SOURCE_VISUAL_HINT_REQUIRED", str(question.get("question_id")))
                _require(bool(str(visual.get("primitive_kind") or "").strip()), "SOURCE_VISUAL_HINT_PRIMITIVE_MISSING", str(question.get("question_id")))
                _require(isinstance(visual.get("semantic_params"), Mapping), "SOURCE_VISUAL_HINT_PARAMS_MISSING", str(question.get("question_id")))
                visual_count += 1
    _require(source_count == visual_count, "SOURCE_VISUAL_HINT_COVERAGE_INCOMPLETE", f"{visual_count}/{source_count}")
    return {"source_question_count": source_count, "source_visual_hint_count": visual_count}
