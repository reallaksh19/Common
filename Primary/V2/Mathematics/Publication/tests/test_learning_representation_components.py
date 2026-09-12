from Primary.V2.Mathematics.Publication.engine.learning_representation_components import (
    HintLadderComponent,
    ThinkingPathComponent,
)
from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend


def _hint_cards():
    return [
        {"level": "H1", "child_label": "LOOK", "verbal_cue": "Compare Rs 120 and Rs 240.", "learner_action": "Point to the change.", "visual_state_id": "RATE-H1", "primitive_call": {"kind": "RATE_COMPARE", "params": {"base_amount": 120, "target_amount": 240}}},
        {"level": "H2", "child_label": "REMEMBER", "verbal_cue": "Use the same scale factor.", "learner_action": "Mark x2.", "visual_state_id": "RATE-H2", "primitive_call": {"kind": "SCALE_FACTOR_VIEW", "params": {"scale_factor": 2}}},
        {"level": "H3", "child_label": "SHOW IT", "verbal_cue": "Apply x2 to 3 hats.", "learner_action": "Write 3 x 2, then solve it.", "visual_state_id": "RATE-H3", "primitive_call": {"kind": "RATE_SCALE_MODEL", "params": {"base_count": 3, "scale_factor": 2}}},
    ]


def _thinking_steps():
    return [
        {"step_id": "P1", "child_label": "LOOK", "one_line_action": "Compare money.", "micro_visual_ref": "RATE-P1", "resolved_visual": {"primitive_kind": "RATE_COMPARE", "semantic_params": {"base_amount": 120, "target_amount": 240}}},
        {"step_id": "P2", "child_label": "SHOW IT", "one_line_action": "Find x2.", "micro_visual_ref": "RATE-P2", "resolved_visual": {"primitive_kind": "SCALE_FACTOR_VIEW", "semantic_params": {"scale_factor": 2}}},
        {"step_id": "P3", "child_label": "WORK", "one_line_action": "Scale hats.", "micro_visual_ref": "RATE-P3", "resolved_visual": {"primitive_kind": "RATE_SCALE_MODEL", "semantic_params": {"base_count": 3, "scale_factor": 2}}},
        {"step_id": "P4", "child_label": "CHECK", "one_line_action": "Check the rate.", "micro_visual_ref": "RATE-P4", "resolved_visual": {"primitive_kind": "RATE_SCALE_MODEL", "semantic_params": {"base_count": 3, "target_count": 6, "scale_factor": 2}}},
    ]


def _inside(parent, child):
    return child.x >= parent.x and child.y >= parent.y and child.x_max <= parent.x_max and child.y_max <= parent.y_max


def test_hint_ladder_uses_measured_separate_visual_and_text_lanes():
    backend = MockVectorBackend()
    cards = _hint_cards()
    width = 500.0
    height = HintLadderComponent.measure(cards, width)
    parent = BoundingBox(40.0, 40.0, width, height)
    placements = HintLadderComponent.render(backend, parent, cards)

    card_boxes = [p.bbox for p in placements if p.kind == "HINT_CARD"]
    visual_boxes = [p.bbox for p in placements if p.kind == "HINT_VISUAL"]
    text_boxes = [p.bbox for p in placements if p.kind == "HINT_TEXT"]
    assert len(card_boxes) == len(visual_boxes) == len(text_boxes) == 3
    for card, visual, text in zip(card_boxes, visual_boxes, text_boxes):
        assert _inside(card, visual)
        assert _inside(card, text)
        assert visual.x_max <= text.x
    assert all((p.font_min_used or 12.0) >= 12.0 for p in placements if p.kind in {"HINT_CARD", "HINT_TEXT"})
    assert len(backend.get_evidence()) == 3


def test_thinking_path_uses_resolved_microvisuals():
    backend = MockVectorBackend()
    steps = _thinking_steps()
    parent = BoundingBox(40.0, 40.0, 500.0, ThinkingPathComponent.CARD_H)
    placements = ThinkingPathComponent.render(backend, parent, steps)
    assert len([p for p in placements if p.kind == "THINKING_PATH_CARD"]) == 4
    assert len([p for p in placements if p.kind == "THINKING_PATH_VISUAL"]) == 4
    assert len(backend.get_evidence()) == 4
