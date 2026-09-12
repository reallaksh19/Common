import json
from pathlib import Path

import pytest

from Grade4.V2.Mathematics.Publication.engine.core1_components import (
    Core1ComponentError,
    WorkSurfaceComponent,
)
from Grade4.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "LearningDesign" / "fixtures" / "learning_representation"


def _tasks():
    for name in ("cases.json", "extended_cases.json"):
        path = FIXTURE_DIR / name
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for case in payload.get("cases", []):
            task = case.get("task")
            if task:
                yield case.get("case_id", task.get("task_ref", name)), task


def _render_visual(case_id, visual):
    backend = MockVectorBackend()
    render_primitive(
        visual["primitive_kind"],
        dict(visual.get("semantic_params") or {}),
        backend,
        BoundingBox(20, 20, 520, 190),
    )
    assert backend.operations, f"{case_id}:{visual.get('visual_state_id')} rendered no vector operations"
    assert backend.get_evidence(), f"{case_id}:{visual.get('visual_state_id')} emitted no semantic render evidence"


def test_every_learning_representation_fixture_visual_is_concretely_realized():
    seen = 0
    for case_id, task in _tasks():
        _render_visual(case_id, task["primary_visual"])
        seen += 1
        for visual in task.get("visual_states", []):
            _render_visual(case_id, visual)
            seen += 1
    assert seen >= 20, "fixture coverage unexpectedly small"


def test_every_fixture_work_surface_has_a_typed_realizer():
    seen = 0
    for case_id, task in _tasks():
        surface = task.get("work_surface")
        if not surface:
            continue
        backend = MockVectorBackend()
        required_h = WorkSurfaceComponent.measure(surface, 520)
        WorkSurfaceComponent.render(backend, BoundingBox(20, 20, 520, required_h), surface)
        assert backend.operations, f"{case_id}:{surface.get('kind')} rendered no work-surface operations"
        seen += 1
    assert seen >= 2, "expected procedural/geometry work-surface fixtures"


def test_measured_work_surface_rejects_a_box_shorter_than_its_contract():
    surface = next(task["work_surface"] for _, task in _tasks() if task.get("work_surface") and task["work_surface"].get("kind") == "LONG_DIVISION_WORK")
    required_h = WorkSurfaceComponent.measure(surface, 520)
    with pytest.raises(Core1ComponentError) as exc:
        WorkSurfaceComponent.render(MockVectorBackend(), BoundingBox(20, 20, 520, required_h - 1), surface)
    assert exc.value.code == "WORK_SURFACE_BOX_TOO_SHORT"
