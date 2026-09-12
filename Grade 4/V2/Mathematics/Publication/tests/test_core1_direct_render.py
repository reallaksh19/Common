from pathlib import Path

import pytest

import Primary.V2.Mathematics.Publication.engine.core1_components as core1_components
from Primary.V2.Mathematics.Publication.engine.core1_components import (
    Core1ComponentError,
    PrimaryVisualComponent,
    WorkSurfaceComponent,
)
from Primary.V2.Mathematics.Publication.engine.core1_direct_composer import (
    render_core1_from_authoring_handoff,
)
from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend


def _state(state_id, kind, params):
    return {
        "visual_state_id": state_id,
        "primitive_kind": kind,
        "representation_ref": f"REP-{state_id}",
        "fidelity": "SCHEMATIC",
        "fade_mode": "PARTIAL",
        "semantic_params": dict(params),
        "validator_refs": ["DIVISION_TABLE"],
    }


def _division_table_plan(module_id="C1-DIV-TABLE"):
    primary = _state(
        "TABLE-PRIMARY",
        "DIVISION_TABLE_MODEL",
        {"columns": [720, 480], "rows": [60, 15]},
    )
    h1 = _state("TABLE-H1", "DIVISION_TABLE_ROLE_HIGHLIGHT", {"columns": [720, 480], "rows": [60, 15]})
    h2 = _state("TABLE-H2", "DIVISION_TABLE_CELL_MODEL", {"column": 720, "row": 60})
    h3 = _state("TABLE-H3", "DIVISION_TABLE_CELL_MODEL", {"column": 720, "row": 60, "quotient": 12})
    p1 = _state("TABLE-P1", "DIVISION_TABLE_ROLE_HIGHLIGHT", {"columns": [720, 480], "rows": [60, 15]})
    p2 = _state("TABLE-P2", "DIVISION_TABLE_CELL_MODEL", {"column": 720, "row": 60})
    p3 = _state("TABLE-P3", "DIVISION_TABLE_MODEL", {"columns": [720, 480], "rows": [60, 15]})

    surface = {
        "schema_version": "1.0.0",
        "surface_id": "WS-DIV-TABLE",
        "task_ref": module_id,
        "kind": "DIVISION_TABLE_WORKSPACE",
        "semantic_params": {
            "columns": [720, 480],
            "rows": [60, 15],
            "cells": [
                {"column": 720, "row": 60, "quotient": 12},
                {"column": 480, "row": 60, "quotient": 8},
                {"column": 720, "row": 15, "quotient": 48},
                {"column": 480, "row": 15, "quotient": 32},
            ],
        },
        "validator_refs": ["DIVISION_TABLE"],
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }

    return {
        "schema_version": "1.0.0",
        "plan_id": f"LRP-{module_id}",
        "task_ref": module_id,
        "learner_profile_ref": "PRIMARY_SUPPORT_G4_5",
        "representation_class": "STRUCTURAL",
        "primary_visual": primary,
        "all_visual_states": [primary, h1, h2, h3, p1, p2, p3],
        "hint_visuals": {"H1": h1, "H2": h2, "H3": h3},
        "hint_ladder": {
            "ladder_id": f"HL-{module_id}",
            "fresh_retry_ref": f"FRESH-{module_id}",
            "steps": [
                {"level": "H1", "child_label": "LOOK", "verbal_cue": "Read the top and side.", "learner_action": "Point to one cell.", "may_reveal_final_answer": False},
                {"level": "H2", "child_label": "REMEMBER", "verbal_cue": "Top divided by side.", "learner_action": "Write one division.", "may_reveal_final_answer": False},
                {"level": "H3", "child_label": "SHOW IT", "verbal_cue": "Model one cell.", "learner_action": "Continue the same way.", "may_reveal_final_answer": False},
            ],
        },
        "thinking_path": {
            "path_id": f"TP-{module_id}",
            "steps": [
                {"step_id": "P1", "child_label": "LOOK", "one_line_action": "Read the table.", "micro_visual_ref": "TABLE-P1"},
                {"step_id": "P2", "child_label": "WORK", "one_line_action": "Divide.", "micro_visual_ref": "TABLE-P2"},
                {"step_id": "P3", "child_label": "CHECK", "one_line_action": "Check all cells.", "micro_visual_ref": "TABLE-P3"},
            ],
        },
        "thinking_path_micro_visual_refs": ["TABLE-P1", "TABLE-P2", "TABLE-P3"],
        "work_surface_ref": surface["surface_id"],
        "work_surface": surface,
        "hint_ladder_ref": f"HL-{module_id}",
        "thinking_path_ref": f"TP-{module_id}",
        "fresh_retry_support_policy": "NONE",
        "reference_visual_ref": None,
        "visual_language_key": {"columns": "BLUE", "rows": "TEAL"},
        "publisher_invention_allowed": False,
    }


def _handoff():
    module_id = "C1-DIV-TABLE"
    plan = _division_table_plan(module_id)
    return {
        "schema_version": "1.0.0",
        "handoff_id": "HANDOFF-CORE1-DIRECT",
        "input_ref": "INPUT-CORE1-DIRECT",
        "publisher_invention_allowed": False,
        "coverage": {
            "total_modules": 1,
            "planned_modules": 1,
            "independent_probe_modules": 0,
            "unaccounted_modules": 0,
        },
        "authoring_result": {
            "skill_model": {
                "concepts": [
                    {"concept_id": "CONCEPT-DIV-TABLE", "title": "Read a division table"}
                ]
            },
            "core1_plan": {
                "modules": [
                    {
                        "module_id": module_id,
                        "concept_ref": "CONCEPT-DIV-TABLE",
                        "concept_mode": "INTRODUCE",
                        "objective": "Use the top number and side number to complete each division cell.",
                        "learner_action": "Read one column and one row, divide, then check the table.",
                        "source_refs": ["fixture://division-table"],
                    }
                ]
            },
        },
        "module_support": [
            {
                "product": "CORE1",
                "module_id": module_id,
                "concept_ref": "CONCEPT-DIV-TABLE",
                "support_status": "PLANNED",
                "learning_representation_plan": plan,
                "fresh_retry_prompt": "Complete a new division table.",
            }
        ],
    }


def test_core1_renders_directly_from_learning_representation_plan(tmp_path: Path):
    output = tmp_path / "core1-direct.pdf"
    pdf_sha, custody = render_core1_from_authoring_handoff(_handoff(), output)

    assert output.exists() and output.stat().st_size > 0
    assert len(pdf_sha) == 64
    semantic_ids = [sid for page in custody["page_map"] for sid in page["semantic_ids"]]
    assert "TABLE-PRIMARY" in semantic_ids
    assert "WS-DIV-TABLE" in semantic_ids
    assert custody["core1_handoff"]["planned_module_count"] == 1
    assert custody["core1_handoff"]["publisher_invention_allowed"] is False


def test_division_table_workspace_does_not_publish_answer_cells(monkeypatch):
    captured = {}

    def fake_render(kind, params, backend, bbox):
        captured["kind"] = kind
        captured["params"] = dict(params)

    monkeypatch.setattr(core1_components, "render_primitive", fake_render)
    surface = _division_table_plan()["work_surface"]
    WorkSurfaceComponent.render(MockVectorBackend(), BoundingBox(20, 20, 500, 180), surface)

    assert captured["kind"] == "DIVISION_TABLE_MODEL"
    assert captured["params"]["columns"] == [720, 480]
    assert captured["params"]["rows"] == [60, 15]
    assert "cells" not in captured["params"]


def test_long_division_surface_uses_canonical_semantic_steps():
    surface = {
        "schema_version": "1.0.0",
        "surface_id": "WS-DIV-7048-24",
        "task_ref": "C1-DIV-7048-24",
        "kind": "LONG_DIVISION_WORK",
        "semantic_params": {
            "dividend": 7048,
            "divisor": 24,
            "quotient": 293,
            "remainder": 16,
            "quotient_places": [2, 9, 3],
            "steps": [
                {"partial_dividend": 70, "quotient_digit": 2, "product": 48, "subtraction_remainder": 22, "bring_down_digit": 4},
                {"partial_dividend": 224, "quotient_digit": 9, "product": 216, "subtraction_remainder": 8, "bring_down_digit": 8},
                {"partial_dividend": 88, "quotient_digit": 3, "product": 72, "subtraction_remainder": 16, "bring_down_digit": None},
            ],
            "check": {"identity_holds": True, "remainder_in_range": True},
        },
        "validator_refs": ["DIVISION_IDENTITY_AND_STEPS", "REMAINDER_RANGE"],
        "provenance": "AUTHORED_NOTEBOOK_EXAMPLE",
    }
    backend = MockVectorBackend()
    WorkSurfaceComponent.render(backend, BoundingBox(20, 20, 520, 255), surface)

    broken = dict(surface)
    broken["semantic_params"] = dict(surface["semantic_params"])
    broken["semantic_params"]["remainder"] = 17
    with pytest.raises(Core1ComponentError) as exc:
        WorkSurfaceComponent.render(MockVectorBackend(), BoundingBox(20, 20, 520, 255), broken)
    assert exc.value.code == "PRIMARY_VISUAL_ALGORITHM_INVALID"


def test_angle_workspace_is_typed_and_unsupported_surface_fails_closed():
    angle = {
        "kind": "ANGLE_DRAWING_WORKSPACE",
        "semantic_params": {"slots": 3},
        "validator_refs": ["ANGLE_GEOMETRY"],
    }
    WorkSurfaceComponent.render(MockVectorBackend(), BoundingBox(20, 20, 520, 175), angle)

    unsupported = {
        "kind": "DECIMAL_ALIGNMENT_WORK",
        "semantic_params": {},
        "validator_refs": ["DECIMAL_ALIGNMENT"],
    }
    with pytest.raises(Core1ComponentError) as exc:
        WorkSurfaceComponent.measure(unsupported, 520)
    assert exc.value.code == "WORK_SURFACE_KIND_NOT_REALIZED"


def test_unsupported_primary_visual_fails_closed():
    visual = {
        "primitive_kind": "UNREALIZED_VISUAL",
        "semantic_params": {"value": 1},
        "validator_refs": ["TEST_VALIDATOR"],
    }
    with pytest.raises(Core1ComponentError) as exc:
        PrimaryVisualComponent.render(MockVectorBackend(), BoundingBox(20, 20, 520, 190), visual)
    assert exc.value.code == "CORE1_PRIMARY_VISUAL_NOT_REALIZED"
