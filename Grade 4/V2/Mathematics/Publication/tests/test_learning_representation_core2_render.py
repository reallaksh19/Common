from pathlib import Path

from Primary.V2.Mathematics.Publication.engine.page_composer import PrimaryPageComposer


def _learning_plan():
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
                {"level": "H1", "child_label": "LOOK", "verbal_cue": "Compare Rs 120 and Rs 240.", "learner_action": "Point to the change.", "may_reveal_final_answer": False},
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
                {"step_id": "P4", "child_label": "CHECK", "one_line_action": "Check the rate.", "micro_visual_ref": "RATE-P4"},
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


def test_core2_composer_renders_visual_hint_ladder_and_thinking_path(tmp_path: Path):
    output = tmp_path / "core2-learning-representation.pdf"
    plan = {
        "companion_id": "C2-TEST",
        "linked_core1_id": "C1-TEST",
        "appendix_a": {"batches": []},
        "appendix_b": {
            "ladders": [
                {
                    "item_id": "RATE-ITEM-01",
                    "learning_representation_plan": _learning_plan(),
                    "fresh_independent_retry_H0": "5 bottles cost Rs 150. How many bottles can be bought for Rs 300?"
                }
            ]
        },
        "appendix_c": {},
    }

    pdf_sha, custody = PrimaryPageComposer().render_core2_companion(plan, output)

    assert output.exists() and output.stat().st_size > 0
    assert len(pdf_sha) == 64
    semantic_ids = [sid for page in custody["page_map"] for sid in page["semantic_ids"]]
    assert "RATE-ITEM-01:H1" in semantic_ids
    assert "RATE-ITEM-01:H2" in semantic_ids
    assert "RATE-ITEM-01:H3" in semantic_ids
    assert "RATE-ITEM-01" in semantic_ids
