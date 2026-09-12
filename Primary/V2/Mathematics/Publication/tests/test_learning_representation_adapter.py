import copy

import pytest

from Primary.V2.Mathematics.Publication.engine.learning_representation_adapter import (
    LearningRepresentationAdapter,
    LearningRepresentationPublicationError,
)
from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive


def _rate_plan():
    states = [
        {"visual_state_id": "RATE-H1", "primitive_kind": "RATE_COMPARE", "semantic_params": {"base_amount": 120, "target_amount": 240}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "FULL", "representation_ref": "REP-RATE-COMPARE"},
        {"visual_state_id": "RATE-H2", "primitive_kind": "SCALE_FACTOR_VIEW", "semantic_params": {"scale_factor": 2}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "PARTIAL", "representation_ref": "REP-RATE-FACTOR"},
        {"visual_state_id": "RATE-H3", "primitive_kind": "RATE_SCALE_MODEL", "semantic_params": {"base_count": 3, "scale_factor": 2}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "PARTIAL", "representation_ref": "REP-RATE-APPLY"},
        {"visual_state_id": "RATE-P1", "primitive_kind": "RATE_COMPARE", "semantic_params": {"base_amount": 120, "target_amount": 240}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "PARTIAL", "representation_ref": "REP-RATE-COMPARE"},
        {"visual_state_id": "RATE-P2", "primitive_kind": "SCALE_FACTOR_VIEW", "semantic_params": {"scale_factor": 2}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "PARTIAL", "representation_ref": "REP-RATE-FACTOR"},
        {"visual_state_id": "RATE-P3", "primitive_kind": "RATE_SCALE_MODEL", "semantic_params": {"base_count": 3, "scale_factor": 2}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "PARTIAL", "representation_ref": "REP-RATE-APPLY"},
        {"visual_state_id": "RATE-P4", "primitive_kind": "RATE_SCALE_MODEL", "semantic_params": {"base_count": 3, "target_count": 6, "scale_factor": 2}, "validator_refs": ["SAME_RATE_SCALE"], "fidelity": "SCHEMATIC", "fade_mode": "PARTIAL", "representation_ref": "REP-RATE-CHECK"},
    ]
    return {
        "schema_version": "1.0.0",
        "plan_id": "LRP-FIX-RATE",
        "task_ref": "FIX-RATE",
        "learner_profile_ref": "PRIMARY_SUPPORT_G4_5",
        "representation_class": "STRUCTURAL",
        "primary_visual": states[0],
        "all_visual_states": states,
        "hint_visuals": {"H1": states[0], "H2": states[1], "H3": states[2]},
        "hint_ladder": {
            "ladder_id": "HL-RATE",
            "fresh_retry_ref": "FRESH-RATE",
            "steps": [
                {"level": "H1", "child_label": "LOOK", "verbal_cue": "Compare the money.", "learner_action": "Point to the change.", "may_reveal_final_answer": False},
                {"level": "H2", "child_label": "REMEMBER", "verbal_cue": "Use the same factor.", "learner_action": "Mark x2.", "may_reveal_final_answer": False},
                {"level": "H3", "child_label": "SHOW IT", "verbal_cue": "Apply x2 to 3 hats.", "learner_action": "Write 3 x 2.", "may_reveal_final_answer": False},
            ],
        },
        "thinking_path": {
            "path_id": "TP-RATE",
            "steps": [
                {"step_id": "P1", "child_label": "LOOK", "one_line_action": "Compare money.", "micro_visual_ref": "RATE-P1"},
                {"step_id": "P2", "child_label": "SHOW IT", "one_line_action": "Find x2.", "micro_visual_ref": "RATE-P2"},
                {"step_id": "P3", "child_label": "WORK", "one_line_action": "Scale hats.", "micro_visual_ref": "RATE-P3"},
                {"step_id": "P4", "child_label": "CHECK", "one_line_action": "Check rate.", "micro_visual_ref": "RATE-P4"},
            ],
        },
        "thinking_path_micro_visual_refs": ["RATE-P1", "RATE-P2", "RATE-P3", "RATE-P4"],
        "work_surface_ref": None,
        "work_surface": None,
        "hint_ladder_ref": "HL-RATE",
        "thinking_path_ref": "TP-RATE",
        "fresh_retry_support_policy": "NONE",
        "reference_visual_ref": None,
        "visual_language_key": {"money": "TEAL", "hats": "BLUE"},
        "publisher_invention_allowed": False,
    }


def test_adapter_uses_upstream_hint_visuals_without_replanning():
    plan = _rate_plan()
    cards = LearningRepresentationAdapter.build_hint_cards(plan)
    assert [card["child_label"] for card in cards] == ["LOOK", "REMEMBER", "SHOW IT"]
    assert [card["primitive_call"]["kind"] for card in cards] == ["RATE_COMPARE", "SCALE_FACTOR_VIEW", "RATE_SCALE_MODEL"]

    backend = MockVectorBackend()
    bbox = BoundingBox(x=40.0, y=40.0, width=360.0, height=120.0)
    for card in cards:
        render_primitive(card["primitive_call"]["kind"], card["primitive_call"]["params"], backend, bbox)
    assert len(backend.get_evidence()) == 3


def test_adapter_resolves_thinking_path_visuals():
    path = LearningRepresentationAdapter.build_thinking_path(_rate_plan())
    assert len(path) == 4
    assert all(step["resolved_visual"] is not None for step in path)
    assert path[0]["child_label"] == "LOOK"
    assert path[-1]["child_label"] == "CHECK"


def test_adapter_requires_resolved_semantic_objects():
    plan = _rate_plan()
    broken = copy.deepcopy(plan)
    broken.pop("hint_ladder")
    with pytest.raises(LearningRepresentationPublicationError) as exc:
        LearningRepresentationAdapter.build_hint_cards(broken)
    assert exc.value.code == "PUBLISHER_REQUIRES_RESOLVED_HINT_LADDER"


def test_adapter_forbids_publisher_invention():
    plan = _rate_plan()
    plan["publisher_invention_allowed"] = True
    with pytest.raises(LearningRepresentationPublicationError) as exc:
        LearningRepresentationAdapter.validate_plan(plan)
    assert exc.value.code == "PUBLISHER_INVENTION_NOT_FORBIDDEN"
