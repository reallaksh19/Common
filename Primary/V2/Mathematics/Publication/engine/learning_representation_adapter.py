"""Adapter from publisher-neutral LearningRepresentationPlan to page components.

The adapter is intentionally thin: it does not choose pedagogy, invent visual
states, or repair missing semantics. It validates the upstream plan and exposes
measured-publication inputs. Unsupported/missing states fail closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping


@dataclass
class LearningRepresentationPublicationError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise LearningRepresentationPublicationError(code, message)


class LearningRepresentationAdapter:
    """Consumes a validated upstream learning-representation plan without inference."""

    CHILD_LABELS = {"H1": "LOOK", "H2": "REMEMBER", "H3": "SHOW IT"}

    @classmethod
    def validate_plan(cls, plan: Mapping[str, Any]) -> None:
        _require(plan.get("schema_version") == "1.0.0", "LEARNING_REPRESENTATION_SCHEMA_UNSUPPORTED", "expected schema_version 1.0.0")
        _require(plan.get("publisher_invention_allowed") is False, "PUBLISHER_INVENTION_NOT_FORBIDDEN", "publisher_invention_allowed must be false")
        _require(plan.get("fresh_retry_support_policy") == "NONE", "FRESH_H0_INHERITS_SUPPORT", "fresh retry must have no inherited support")
        hint_visuals = plan.get("hint_visuals") or {}
        _require(set(hint_visuals) == {"H1", "H2", "H3"}, "HINT_VISUAL_COVERAGE_INCOMPLETE", "H1/H2/H3 visual states are required")
        for level, state in hint_visuals.items():
            _require(bool(state.get("primitive_kind")), "HINT_VISUAL_PRIMITIVE_MISSING", f"{level} primitive_kind missing")
            _require(isinstance(state.get("semantic_params"), dict), "HINT_VISUAL_PARAMS_MISSING", f"{level} semantic_params missing")
            _require(bool(state.get("validator_refs")), "UNVALIDATED_VISUAL_DRAWN", f"{level} validator refs missing")

        ladder = plan.get("hint_ladder")
        path = plan.get("thinking_path")
        _require(isinstance(ladder, dict), "PUBLISHER_REQUIRES_RESOLVED_HINT_LADDER", "plan must carry the validated hint ladder object, not only a ref")
        _require(isinstance(path, dict), "PUBLISHER_REQUIRES_RESOLVED_THINKING_PATH", "plan must carry the validated thinking path object, not only a ref")
        _require(ladder.get("fresh_retry_ref"), "H3_WITHOUT_FRESH_H0_RETRY", "resolved hint ladder needs fresh retry ref")

    @classmethod
    def build_hint_cards(cls, plan: Mapping[str, Any]) -> List[Dict[str, Any]]:
        cls.validate_plan(plan)
        visuals = plan["hint_visuals"]
        ladder_steps = {step["level"]: step for step in plan["hint_ladder"].get("steps", [])}
        _require(set(ladder_steps) == {"H1", "H2", "H3"}, "HINT_LADDER_INVALID", "resolved H1/H2/H3 steps are required")

        cards: List[Dict[str, Any]] = []
        for level in ("H1", "H2", "H3"):
            step = ladder_steps[level]
            expected_label = cls.CHILD_LABELS[level]
            _require(step.get("child_label") == expected_label, "PRIMARY_CHILD_LABEL_MISMATCH", f"{level} must display {expected_label}")
            _require(step.get("may_reveal_final_answer") is False, "HINT_REVEALS_COMPLETE_SOLUTION", f"{level} may not reveal the final answer")
            state = visuals[level]
            cards.append({
                "level": level,
                "child_label": expected_label,
                "verbal_cue": step.get("verbal_cue", ""),
                "learner_action": step.get("learner_action", ""),
                "primitive_call": {
                    "kind": state["primitive_kind"],
                    "params": dict(state.get("semantic_params") or {}),
                },
                "visual_state_id": state.get("visual_state_id"),
                "fidelity": state.get("fidelity"),
                "fade_mode": state.get("fade_mode"),
                "validator_refs": list(state.get("validator_refs") or []),
            })
        return cards

    @classmethod
    def build_thinking_path(cls, plan: Mapping[str, Any]) -> List[Dict[str, Any]]:
        cls.validate_plan(plan)
        path = plan["thinking_path"]
        steps = list(path.get("steps") or [])
        _require(bool(steps), "THINKING_PATH_INVALID", "resolved thinking path steps required")
        refs = list(plan.get("thinking_path_micro_visual_refs") or [])
        state_index = {
            state.get("visual_state_id"): state
            for state in (plan.get("all_visual_states") or [])
            if state.get("visual_state_id")
        }
        result = []
        for idx, step in enumerate(steps):
            ref = step.get("micro_visual_ref")
            result.append({
                "step_id": step.get("step_id"),
                "child_label": step.get("child_label"),
                "one_line_action": step.get("one_line_action"),
                "micro_visual_ref": ref,
                "resolved_visual": state_index.get(ref),
                "position": idx + 1,
            })
        _require(len(refs) == len(steps), "THINKING_PATH_MICRO_VISUAL_MISSING", "thinking-path microvisual refs must match steps")
        return result

    @classmethod
    def work_surface(cls, plan: Mapping[str, Any]) -> Dict[str, Any] | None:
        cls.validate_plan(plan)
        surface = plan.get("work_surface")
        ref = plan.get("work_surface_ref")
        if ref is None:
            _require(surface is None, "WORK_SURFACE_REF_MISMATCH", "work surface exists without stable ref")
            return None
        _require(isinstance(surface, dict), "PUBLISHER_REQUIRES_RESOLVED_WORK_SURFACE", "work_surface_ref must resolve to a work-surface object")
        _require(surface.get("surface_id") == ref, "WORK_SURFACE_REF_MISMATCH", "work surface id does not match work_surface_ref")
        return dict(surface)
