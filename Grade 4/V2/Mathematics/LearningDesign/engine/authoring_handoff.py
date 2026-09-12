"""Automatic #336 -> #339 handoff for Primary Math V2.

The deterministic CoreSkills authoring engine remains renderer-independent.  This
module consumes its result plus explicit learning-support blueprints carried by
normalized question evidence and emits one validated LearningRepresentationPlan
per publishable Core1/Core2 module.

No pedagogy is inferred from primitive names or raw question text.  Missing or
conflicting support blueprints fail closed.  Diagnostic PROBE modules are the
only explicit exemption: they remain independent H0 probes and do not receive a
hint ladder before diagnosis.
"""
from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Tuple

from Primary.V2.Mathematics.CoreSkills.engine.author import author
from Primary.V2.Mathematics.LearningDesign.engine.build_learning_representation import (
    LearningRepresentationError,
    build_learning_representation,
)


@dataclass
class AuthoringHandoffError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise AuthoringHandoffError(code, message)


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", str(value).strip()).strip("-").upper() or "UNNAMED"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _question_blueprints(primary_input: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    result: Dict[str, Mapping[str, Any]] = {}
    questions = list((primary_input.get("question_set") or {}).get("questions") or [])
    for question in questions:
        evidence = question.get("evidence") or {}
        question_ref = str(evidence.get("question_ref") or question.get("question_ref") or "").strip()
        if not question_ref:
            continue
        blueprint = evidence.get("learning_support_blueprint")
        if blueprint is not None:
            validate_support_blueprint(blueprint, owner=question_ref)
            result[question_ref] = blueprint
    return result


def validate_support_blueprint(blueprint: Mapping[str, Any], owner: str = "support blueprint") -> None:
    required = [
        "schema_version", "task_kind", "representation_class", "primary",
        "hint_steps", "thinking_path", "fresh_retry_prompt",
    ]
    missing = [key for key in required if key not in blueprint]
    _require(not missing, "LEARNING_SUPPORT_BLUEPRINT_INCOMPLETE", f"{owner}: missing {missing}")
    _require(blueprint.get("schema_version") == "1.0.0", "LEARNING_SUPPORT_BLUEPRINT_SCHEMA_UNSUPPORTED", owner)
    _require(
        blueprint.get("representation_class") in {"CONCRETE_PICTORIAL", "STRUCTURAL", "PROCEDURAL_WORK", "ABSTRACT_SYMBOLIC"},
        "LEARNING_SUPPORT_REPRESENTATION_CLASS_INVALID",
        owner,
    )
    _require(bool(str(blueprint.get("task_kind", "")).strip()), "LEARNING_SUPPORT_TASK_KIND_REQUIRED", owner)
    _require(bool(str(blueprint.get("fresh_retry_prompt", "")).strip()), "FRESH_H0_PROMPT_REQUIRED", owner)

    primary = blueprint.get("primary") or {}
    _validate_visual_selection(primary, f"{owner}:primary")

    hints = list(blueprint.get("hint_steps") or [])
    expected = [
        ("H1", "NOTICE", "LOOK"),
        ("H2", "REMEMBER", "REMEMBER"),
        ("H3", "REPRESENT", "SHOW IT"),
    ]
    _require(len(hints) == 3, "HINT_LADDER_INVALID", f"{owner}: H1/H2/H3 required")
    for step, (level, role, label) in zip(hints, expected):
        _validate_visual_selection(step, f"{owner}:{level}")
        _require(step.get("level") == level, "HINT_LADDER_INVALID", f"{owner}: expected {level}")
        _require(step.get("semantic_role") == role, "HINT_LADDER_INVALID", f"{owner}:{level} expected {role}")
        _require(step.get("child_label") == label, "HINT_LADDER_INVALID", f"{owner}:{level} expected child label {label}")
        _require(bool(str(step.get("verbal_cue", "")).strip()), "HINT_LADDER_INVALID", f"{owner}:{level} verbal cue required")
        _require(bool(str(step.get("learner_action", "")).strip()), "HINT_LADDER_INVALID", f"{owner}:{level} learner action required")

    path = list(blueprint.get("thinking_path") or [])
    _require(2 <= len(path) <= 6, "THINKING_PATH_INVALID", f"{owner}: 2-6 thinking steps required")
    allowed_roles = {"INTERPRET", "MODEL", "EXECUTE", "COMBINE", "VERIFY"}
    allowed_labels = {"LOOK", "SHOW IT", "WORK", "PUT TOGETHER", "CHECK"}
    for index, step in enumerate(path, start=1):
        _validate_visual_selection(step, f"{owner}:thinking:{index}")
        _require(step.get("semantic_role") in allowed_roles, "THINKING_PATH_INVALID", f"{owner}:thinking:{index} role")
        _require(step.get("child_label") in allowed_labels, "THINKING_PATH_INVALID", f"{owner}:thinking:{index} child label")
        _require(bool(str(step.get("one_line_action", "")).strip()), "THINKING_PATH_INVALID", f"{owner}:thinking:{index} action")

    surface = blueprint.get("work_surface_template")
    if surface is not None:
        _require(bool(surface.get("kind")), "WORK_SURFACE_TEMPLATE_INVALID", f"{owner}: kind required")
        _require(isinstance(surface.get("semantic_params"), dict), "WORK_SURFACE_TEMPLATE_INVALID", f"{owner}: semantic_params required")
        _require(bool(surface.get("validator_refs")), "WORK_SURFACE_TEMPLATE_INVALID", f"{owner}: validator_refs required")


def _validate_visual_selection(selection: Mapping[str, Any], owner: str) -> None:
    _require(bool(selection.get("representation_ref")), "LEARNING_SUPPORT_REPRESENTATION_REF_REQUIRED", owner)
    _require(selection.get("fidelity") in {"EXACT", "REPRESENTATIVE_SAMPLE", "SCHEMATIC"}, "LEARNING_SUPPORT_FIDELITY_INVALID", owner)
    _require(selection.get("fade_mode") in {"FULL", "PARTIAL", "EMPTY_FRAME", "NONE"}, "LEARNING_SUPPORT_FADE_MODE_INVALID", owner)
    overlay = selection.get("semantic_params_overlay")
    _require(overlay is None or isinstance(overlay, dict), "LEARNING_SUPPORT_SEMANTIC_OVERLAY_INVALID", owner)


def _representation_index(authoring_result: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    reps = list((authoring_result.get("representation_plan") or {}).get("representations") or [])
    return {str(rep["representation_id"]): dict(rep) for rep in reps}


def _resolve_visual_state(
    selection: Mapping[str, Any],
    *,
    state_id: str,
    concept_ref: str,
    representations: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    rep_ref = str(selection["representation_ref"])
    _require(rep_ref in representations, "LEARNING_SUPPORT_REPRESENTATION_REF_UNKNOWN", rep_ref)
    rep = representations[rep_ref]
    _require(rep.get("concept_ref") == concept_ref, "LEARNING_SUPPORT_CROSS_CONCEPT_REPRESENTATION", f"{rep_ref} does not belong to {concept_ref}")

    fade_mode = str(selection["fade_mode"])
    allowed_fades = list(rep.get("fade_modes") or [])
    _require(fade_mode in allowed_fades, "LEARNING_SUPPORT_FADE_MODE_INVALID", f"{rep_ref} does not allow {fade_mode}")

    params = copy.deepcopy(rep.get("semantic_params") or {})
    overlay = selection.get("semantic_params_overlay") or {}
    for key, value in overlay.items():
        if key in params and params[key] != value:
            raise AuthoringHandoffError(
                "SUPPORT_BLUEPRINT_SEMANTIC_OVERRIDE_CONFLICT",
                f"{rep_ref}: overlay attempted to change grounded semantic param {key!r}",
            )
        params[key] = copy.deepcopy(value)

    return {
        "visual_state_id": state_id,
        "primitive_kind": rep["primitive_kind"],
        "representation_ref": rep_ref,
        "fidelity": selection["fidelity"],
        "fade_mode": fade_mode,
        "semantic_params": params,
        "validator_refs": list(rep.get("validator_refs") or []),
    }


def _find_blueprint_for_module(
    module: Mapping[str, Any],
    blueprints_by_question: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    refs = {str(x) for x in (module.get("source_refs") or [])}
    matches: List[Mapping[str, Any]] = [bp for qref, bp in blueprints_by_question.items() if qref in refs]
    if not matches:
        return None
    signatures = {_canonical(bp) for bp in matches}
    _require(len(signatures) == 1, "LEARNING_SUPPORT_BLUEPRINT_CONFLICT", str(module.get("module_id")))
    return matches[0]


def _surface_from_blueprint(blueprint: Mapping[str, Any], module_id: str) -> Dict[str, Any] | None:
    template = blueprint.get("work_surface_template")
    if template is None:
        return None
    return {
        "schema_version": "1.0.0",
        "surface_id": f"WS-{_slug(module_id)}",
        "task_ref": module_id,
        "kind": template["kind"],
        "semantic_params": copy.deepcopy(template.get("semantic_params") or {}),
        "validator_refs": list(template.get("validator_refs") or []),
        "provenance": template.get("provenance", "ENGINE_AUTHORED_VISUAL"),
    }


def _task_from_blueprint(
    module: Mapping[str, Any],
    blueprint: Mapping[str, Any],
    representations: Mapping[str, Mapping[str, Any]],
) -> Tuple[Dict[str, Any], str]:
    module_id = str(module["module_id"])
    concept_ref = str(module["concept_ref"])
    fresh_ref = f"FRESH-{_slug(module_id)}"

    primary = _resolve_visual_state(
        blueprint["primary"],
        state_id=f"{_slug(module_id)}-PRIMARY",
        concept_ref=concept_ref,
        representations=representations,
    )

    visual_states: List[Dict[str, Any]] = []
    hint_steps: List[Dict[str, Any]] = []
    for raw in blueprint["hint_steps"]:
        level = str(raw["level"])
        state = _resolve_visual_state(
            raw,
            state_id=f"{_slug(module_id)}-{level}",
            concept_ref=concept_ref,
            representations=representations,
        )
        visual_states.append(state)
        hint_steps.append({
            "hint_id": f"HINT-{_slug(module_id)}-{level}",
            "level": level,
            "semantic_role": raw["semantic_role"],
            "child_label": raw["child_label"],
            "verbal_cue": raw["verbal_cue"],
            "visual_state_ref": state["visual_state_id"],
            "learner_action": raw["learner_action"],
            "information_revealed": list(raw.get("information_revealed") or []),
            "may_reveal_final_answer": False,
        })

    path_steps: List[Dict[str, Any]] = []
    for index, raw in enumerate(blueprint["thinking_path"], start=1):
        state = _resolve_visual_state(
            raw,
            state_id=f"{_slug(module_id)}-PATH-{index}",
            concept_ref=concept_ref,
            representations=representations,
        )
        visual_states.append(state)
        path_steps.append({
            "step_id": f"TP-{_slug(module_id)}-{index}",
            "semantic_role": raw["semantic_role"],
            "child_label": raw["child_label"],
            "micro_visual_ref": state["visual_state_id"],
            "one_line_action": raw["one_line_action"],
        })

    task = {
        "task_ref": module_id,
        "task_kind": blueprint["task_kind"],
        "representation_class": blueprint["representation_class"],
        "primary_visual": primary,
        "visual_states": visual_states,
        "hint_ladder": {
            "ladder_id": f"HL-{_slug(module_id)}",
            "task_ref": module_id,
            "steps": hint_steps,
            "fresh_retry_ref": fresh_ref,
        },
        "thinking_path": {
            "schema_version": "1.0.0",
            "path_id": f"TP-{_slug(module_id)}",
            "task_ref": module_id,
            "steps": path_steps,
        },
        "fresh_retry_ref": fresh_ref,
        "work_surface": _surface_from_blueprint(blueprint, module_id),
        "visual_language_key": dict(blueprint.get("visual_language_key") or {}),
    }
    return task, str(blueprint["fresh_retry_prompt"]).strip()


def build_authoring_handoff(primary_input: Mapping[str, Any]) -> Dict[str, Any]:
    """Run #336 authoring, then deterministically construct #339 plans.

    Every non-PROBE Core1/Core2 module must receive a LearningRepresentationPlan.
    PROBE modules are explicitly recorded as independent-only exemptions; they may
    not silently fall through to text-only support.
    """
    authoring_result = author(primary_input)
    representations = _representation_index(authoring_result)
    blueprints = _question_blueprints(primary_input)

    module_support: List[Dict[str, Any]] = []
    planned = 0
    probe_exempt = 0

    for product_key in ("core1_plan", "core2_plan"):
        product = "CORE1" if product_key == "core1_plan" else "CORE2"
        modules = list((authoring_result.get(product_key) or {}).get("modules") or [])
        for module in modules:
            module_id = str(module["module_id"])
            mode = str(module.get("concept_mode") or "")
            if mode == "PROBE":
                module_support.append({
                    "product": product,
                    "module_id": module_id,
                    "concept_ref": module.get("concept_ref"),
                    "support_status": "INDEPENDENT_PROBE_ONLY",
                    "learning_representation_plan": None,
                    "fresh_retry_prompt": None,
                })
                probe_exempt += 1
                continue

            blueprint = _find_blueprint_for_module(module, blueprints)
            _require(
                blueprint is not None,
                "LEARNING_SUPPORT_BLUEPRINT_REQUIRED",
                f"{product}:{module_id} has no explicit support blueprint in normalized question evidence",
            )
            task, fresh_prompt = _task_from_blueprint(module, blueprint, representations)
            try:
                plan = build_learning_representation(task)
            except LearningRepresentationError as exc:
                raise AuthoringHandoffError(exc.code, f"{product}:{module_id}: {exc.message}") from exc
            plan["fresh_retry_prompt"] = fresh_prompt
            module_support.append({
                "product": product,
                "module_id": module_id,
                "concept_ref": module.get("concept_ref"),
                "support_status": "PLANNED",
                "learning_representation_plan": plan,
                "fresh_retry_prompt": fresh_prompt,
            })
            planned += 1

    total_modules = sum(len((authoring_result.get(key) or {}).get("modules") or []) for key in ("core1_plan", "core2_plan"))
    _require(planned + probe_exempt == total_modules, "AUTHORING_HANDOFF_COVERAGE_INCOMPLETE", "not every module was accounted for")

    return {
        "schema_version": "1.0.0",
        "handoff_id": f"PMV2-HANDOFF-{_slug(authoring_result['input_ref'])}",
        "input_ref": authoring_result["input_ref"],
        "authoring_result": authoring_result,
        "module_support": module_support,
        "coverage": {
            "total_modules": total_modules,
            "planned_modules": planned,
            "independent_probe_modules": probe_exempt,
            "unaccounted_modules": 0,
        },
        "publisher_invention_allowed": False,
    }
