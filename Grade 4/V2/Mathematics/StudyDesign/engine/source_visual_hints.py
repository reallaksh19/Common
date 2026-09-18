"""Source-anchored staged visual-hint resolver for Grade 4 Mathematics V2.

Publication does not invent diagrams or pedagogy. For each SOURCE learner
question this resolver projects the already-authored H1/H2/H3 support blueprint
and its representation requirements into a staged learner-support object.

Invariant for scanned-source study material:
    source question -> H1 LOOK -> H2 SHOW -> H3 NEXT -> attempt/check route

Each stage carries a real visual representation. Existing concise numeric/verbal
help is preserved. Source-defect metadata is never copied into learner hint copy.
Fresh generated independent practice may remain NO_HINT.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, Mapping, Sequence


class SourceVisualHintError(ValueError):
    pass


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise SourceVisualHintError(f"{code}: {detail}")


def _resolve_stage(qref: str, raw: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]) -> Dict[str, Any]:
    level = str(raw.get("level") or "")
    rep_ref = str(raw.get("representation_ref") or "")
    selected = by_id.get(rep_ref)
    _require(level in {"H1", "H2", "H3"}, "SOURCE_HINT_STAGE_LEVEL_INVALID", f"{qref}: {level}")
    _require(selected is not None, "SOURCE_VISUAL_HINT_REFERENCE_MISSING", f"{qref}: {level}/{rep_ref}")
    primitive_kind = str(selected.get("primitive_kind") or "")
    semantic_params = selected.get("semantic_params")
    _require(bool(primitive_kind), "SOURCE_VISUAL_HINT_PRIMITIVE_MISSING", f"{qref}: {level}")
    _require(isinstance(semantic_params, Mapping), "SOURCE_VISUAL_HINT_PARAMS_MISSING", f"{qref}: {level}")
    return {
        "level": level,
        "semantic_role": str(raw.get("semantic_role") or ""),
        "child_label": str(raw.get("child_label") or {"H1": "LOOK", "H2": "SHOW", "H3": "NEXT"}[level]),
        "visual_ref": rep_ref,
        "primitive_kind": primitive_kind,
        "semantic_params": dict(semantic_params),
        "fidelity": str(raw.get("fidelity") or "SCHEMATIC"),
        "fade_mode": str(raw.get("fade_mode") or "PARTIAL"),
        "verbal_cue": str(raw.get("verbal_cue") or ""),
        "learner_action": str(raw.get("learner_action") or ""),
        "information_revealed": list(raw.get("information_revealed") or []),
        "provenance": str(selected.get("provenance") or "ENGINE_AUTHORED_VISUAL"),
        "validator_refs": list(selected.get("validator_refs") or []),
    }


def _resolve_thinking_path(qref: str, blueprint: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]) -> list[Dict[str, Any]]:
    out: list[Dict[str, Any]] = []
    for index, raw in enumerate(blueprint.get("thinking_path") or [], start=1):
        rep_ref = str(raw.get("representation_ref") or "")
        selected = by_id.get(rep_ref)
        _require(selected is not None, "SOURCE_THINKING_PATH_VISUAL_MISSING", f"{qref}: step {index}/{rep_ref}")
        out.append({
            "semantic_role": str(raw.get("semantic_role") or ""),
            "child_label": str(raw.get("child_label") or f"STEP {index}"),
            "one_line_action": str(raw.get("one_line_action") or ""),
            "visual_ref": rep_ref,
            "primitive_kind": str(selected.get("primitive_kind") or ""),
            "semantic_params": dict(selected.get("semantic_params") or {}),
        })
    return out


def build_source_visual_catalog(primary_input: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Resolve authored H1/H2/H3 visuals for every source question.

    The authored support blueprint is the authority for stage order and wording.
    Representation requirements are the authority for mathematical visuals.
    Missing stages fail closed; there is no publisher-local fallback.
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
        raw_stages = list(blueprint.get("hint_steps") or [])
        _require(len(raw_stages) == 3, "SOURCE_STAGED_HINT_REQUIRED", f"{qref}: {len(raw_stages)} stages")
        stages = [_resolve_stage(qref, stage, by_id) for stage in raw_stages]
        _require([stage["level"] for stage in stages] == ["H1", "H2", "H3"], "SOURCE_HINT_STAGE_ORDER_INVALID", qref)

        catalog[qref] = {
            "stages": stages,
            "thinking_path": _resolve_thinking_path(qref, blueprint, by_id),
            "task_kind": str(blueprint.get("task_kind") or ""),
            "representation_class": str(blueprint.get("representation_class") or ""),
        }
    return catalog


def attach_source_visual_hints(
    plan: Mapping[str, Any],
    visual_catalog: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    """Deep-copy a StudyJourney and bind staged visual support to SOURCE items."""
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
                support = visual_catalog.get(source_ref)
                _require(support is not None, "SOURCE_VISUAL_HINT_REQUIRED", source_ref)
                stages = list(support.get("stages") or [])
                _require(len(stages) == 3, "SOURCE_STAGED_HINT_REQUIRED", source_ref)

                hint = question.setdefault("hint_contract", {})
                existing_text = str(hint.get("hint_text") or "").strip()
                # Backwards-compatible H1 binding plus the canonical staged object.
                first = stages[0]
                hint["visual_ref"] = str(first["visual_ref"])
                hint["visual_hint"] = {
                    "primitive_kind": str(first["primitive_kind"]),
                    "semantic_params": dict(first["semantic_params"]),
                    "fidelity": str(first.get("fidelity") or "SCHEMATIC"),
                }
                hint["stages"] = copy.deepcopy(stages)
                hint["thinking_path"] = copy.deepcopy(support.get("thinking_path") or [])
                hint["modality"] = "MIXED"
                hint["may_reveal_final_answer"] = False
                # Existing numeric hint text is retained as an extra concise cue,
                # not substituted for the staged visuals.
                if existing_text:
                    hint["hint_text"] = existing_text
                question["task_support_policy"] = "MIXED"
                visual_count += 1

    _require(source_count > 0, "SOURCE_VISUAL_HINT_SOURCE_QUESTIONS_MISSING", "study journey")
    _require(source_count == visual_count, "SOURCE_VISUAL_HINT_COVERAGE_INCOMPLETE", f"{visual_count}/{source_count}")
    return out


def assert_source_visual_hint_coverage(plan: Mapping[str, Any]) -> Dict[str, int]:
    """Require a concrete three-stage visual ladder for every SOURCE question."""
    source_count = 0
    visual_count = 0
    stage_count = 0
    for module in plan.get("modules") or []:
        for block in module.get("blocks") or []:
            for question in block.get("questions") or []:
                if str(question.get("origin") or "") != "SOURCE":
                    continue
                source_count += 1
                qid = str(question.get("question_id"))
                hint = question.get("hint_contract") or {}
                stages = list(hint.get("stages") or [])
                _require(str(question.get("task_support_policy") or "") == "MIXED", "SOURCE_VISUAL_HINT_POLICY_INVALID", qid)
                _require(str(hint.get("modality") or "") == "MIXED", "SOURCE_VISUAL_HINT_MODALITY_INVALID", qid)
                _require(len(stages) == 3, "SOURCE_STAGED_HINT_REQUIRED", qid)
                _require([str(stage.get("level") or "") for stage in stages] == ["H1", "H2", "H3"], "SOURCE_HINT_STAGE_ORDER_INVALID", qid)
                for stage in stages:
                    _require(bool(str(stage.get("visual_ref") or "").strip()), "SOURCE_VISUAL_HINT_REFERENCE_MISSING", f"{qid}/{stage.get('level')}")
                    _require(bool(str(stage.get("primitive_kind") or "").strip()), "SOURCE_VISUAL_HINT_PRIMITIVE_MISSING", f"{qid}/{stage.get('level')}")
                    _require(isinstance(stage.get("semantic_params"), Mapping), "SOURCE_VISUAL_HINT_PARAMS_MISSING", f"{qid}/{stage.get('level')}")
                    _require(bool(str(stage.get("child_label") or "").strip()), "SOURCE_HINT_CHILD_LABEL_MISSING", f"{qid}/{stage.get('level')}")
                    stage_count += 1
                visual_count += 1
    _require(source_count == visual_count, "SOURCE_VISUAL_HINT_COVERAGE_INCOMPLETE", f"{visual_count}/{source_count}")
    return {
        "source_question_count": source_count,
        "source_visual_hint_count": visual_count,
        "source_visual_stage_count": stage_count,
    }
