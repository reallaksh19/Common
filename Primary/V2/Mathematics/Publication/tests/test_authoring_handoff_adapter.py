from pathlib import Path

import pytest

from Primary.V2.Mathematics.Publication.engine.authoring_handoff_adapter import (
    AuthoringHandoffAdapter,
    AuthoringHandoffPublicationError,
)
from Primary.V2.Mathematics.Publication.engine.page_composer import PrimaryPageComposer


def _learning_plan(module_id="C2-RATE-BUILD"):
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
        "plan_id": f"LRP-{module_id}",
        "task_ref": module_id,
        "learner_profile_ref": "PRIMARY_SUPPORT_G4_5",
        "representation_class": "STRUCTURAL",
        "primary_visual": states[0],
        "all_visual_states": states,
        "hint_visuals": {"H1": states[0], "H2": states[1], "H3": states[2]},
        "hint_ladder": {
            "ladder_id": f"HL-{module_id}",
            "fresh_retry_ref": f"FRESH-{module_id}",
            "steps": [
                {"level": "H1", "child_label": "LOOK", "verbal_cue": "Compare Rs 120 and Rs 240.", "learner_action": "Point to the change.", "may_reveal_final_answer": False},
                {"level": "H2", "child_label": "REMEMBER", "verbal_cue": "Use the same factor.", "learner_action": "Mark x2.", "may_reveal_final_answer": False},
                {"level": "H3", "child_label": "SHOW IT", "verbal_cue": "Apply x2 to 3 hats.", "learner_action": "Write 3 x 2.", "may_reveal_final_answer": False},
            ],
        },
        "thinking_path": {
            "path_id": f"TP-{module_id}",
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
        "hint_ladder_ref": f"HL-{module_id}",
        "thinking_path_ref": f"TP-{module_id}",
        "fresh_retry_support_policy": "NONE",
        "fresh_retry_prompt": "5 bottles cost Rs 150. How many bottles can be bought for Rs 300?",
        "reference_visual_ref": None,
        "visual_language_key": {"money": "TEAL", "hats": "BLUE"},
        "publisher_invention_allowed": False,
    }


def _handoff():
    plan = _learning_plan()
    return {
        "schema_version": "1.0.0",
        "handoff_id": "PMV2-HANDOFF-TEST",
        "input_ref": "INPUT-TEST",
        "publisher_invention_allowed": False,
        "coverage": {
            "total_modules": 3,
            "planned_modules": 2,
            "independent_probe_modules": 1,
            "unaccounted_modules": 0,
        },
        "module_support": [
            {
                "product": "CORE1",
                "module_id": "C1-RATE",
                "concept_ref": "CONCEPT-RATE",
                "support_status": "PLANNED",
                "learning_representation_plan": _learning_plan("C1-RATE"),
                "fresh_retry_prompt": "5 bottles cost Rs 150. How many bottles can be bought for Rs 300?",
            },
            {
                "product": "CORE2",
                "module_id": "C2-RATE-BUILD",
                "concept_ref": "CONCEPT-RATE",
                "support_status": "PLANNED",
                "learning_representation_plan": plan,
                "fresh_retry_prompt": plan["fresh_retry_prompt"],
            },
            {
                "product": "CORE2",
                "module_id": "C2-DIV-PROBE",
                "concept_ref": "CONCEPT-DIV",
                "support_status": "INDEPENDENT_PROBE_ONLY",
                "learning_representation_plan": None,
                "fresh_retry_prompt": None,
            },
        ],
    }


def test_authoring_handoff_builds_core2_ladders_and_preserves_probe_exemption():
    result = AuthoringHandoffAdapter.build_core2_ladders(_handoff())
    assert result["guided_module_count"] == 1
    assert result["probe_module_count"] == 1
    assert result["independent_probe_module_ids"] == ["C2-DIV-PROBE"]
    assert result["ladders"][0]["item_id"] == "C2-RATE-BUILD"
    assert result["ladders"][0]["learning_representation_plan"]["task_ref"] == "C2-RATE-BUILD"


def test_authoring_handoff_renders_through_existing_core2_composer(tmp_path: Path):
    companion = AuthoringHandoffAdapter.build_core2_companion_plan(
        _handoff(),
        companion_id="C2-HANDOFF-TEST",
        linked_core1_id="C1-HANDOFF-TEST",
    )
    output = tmp_path / "core2-from-authoring-handoff.pdf"
    pdf_sha, custody = PrimaryPageComposer().render_core2_companion(companion, output)

    assert output.exists() and output.stat().st_size > 0
    assert len(pdf_sha) == 64
    semantic_ids = [sid for page in custody["page_map"] for sid in page["semantic_ids"]]
    assert "C2-RATE-BUILD:H1" in semantic_ids
    assert "C2-RATE-BUILD:H2" in semantic_ids
    assert "C2-RATE-BUILD:H3" in semantic_ids
    assert "C2-RATE-BUILD" in semantic_ids
    assert "C2-DIV-PROBE" not in semantic_ids
    assert companion["authoring_handoff_trace"]["independent_probe_module_ids"] == ["C2-DIV-PROBE"]


def test_authoring_handoff_fails_closed_on_unaccounted_modules():
    handoff = _handoff()
    handoff["coverage"]["unaccounted_modules"] = 1
    with pytest.raises(AuthoringHandoffPublicationError) as exc:
        AuthoringHandoffAdapter.build_core2_ladders(handoff)
    assert exc.value.code == "AUTHORING_HANDOFF_COVERAGE_INCOMPLETE"


def test_probe_cannot_receive_guided_plan():
    handoff = _handoff()
    handoff["module_support"][2]["learning_representation_plan"] = _learning_plan("C2-DIV-PROBE")
    with pytest.raises(AuthoringHandoffPublicationError) as exc:
        AuthoringHandoffAdapter.build_core2_ladders(handoff)
    assert exc.value.code == "PROBE_MODULE_RECEIVED_GUIDED_HINTS"


def test_planned_module_requires_exact_task_ref():
    handoff = _handoff()
    handoff["module_support"][1]["learning_representation_plan"]["task_ref"] = "OTHER"
    with pytest.raises(AuthoringHandoffPublicationError) as exc:
        AuthoringHandoffAdapter.build_core2_ladders(handoff)
    assert exc.value.code == "AUTHORING_HANDOFF_TASK_REF_MISMATCH"
