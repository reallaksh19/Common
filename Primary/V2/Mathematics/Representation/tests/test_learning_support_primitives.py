import pytest

from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import (
    UnsupportedPrimaryPrimitive,
    render_primitive,
)


def test_same_rate_support_primitives_are_realized():
    backend = MockVectorBackend()
    bbox = BoundingBox(x=40.0, y=40.0, width=420.0, height=140.0)

    render_primitive("RATE_COMPARE", {"base_amount": 120, "target_amount": 240}, backend, bbox)
    render_primitive("SCALE_FACTOR_VIEW", {"scale_factor": 2}, backend, bbox)
    render_primitive(
        "RATE_SCALE_MODEL",
        {"base_amount": 120, "target_amount": 240, "base_count": 3, "target_count": 6, "scale_factor": 2},
        backend,
        bbox,
    )

    evidence = backend.get_evidence()
    assert [item["kind"] for item in evidence] == ["RATE_COMPARE", "SCALE_FACTOR_VIEW", "RATE_SCALE_MODEL"]
    assert all(item["rendered_evidence"]["element_count"] > 0 for item in evidence)


def test_division_table_support_primitives_are_realized():
    backend = MockVectorBackend()
    bbox = BoundingBox(x=40.0, y=40.0, width=420.0, height=160.0)

    render_primitive("DIVISION_TABLE_MODEL", {"columns": [720, 480], "rows": [60, 15]}, backend, bbox)
    render_primitive("DIVISION_TABLE_ROLE_HIGHLIGHT", {"columns": [720, 480], "rows": [60, 15]}, backend, bbox)
    render_primitive("DIVISION_TABLE_CELL_MODEL", {"column": 720, "row": 60, "quotient": 12}, backend, bbox)

    evidence = backend.get_evidence()
    assert [item["kind"] for item in evidence] == [
        "DIVISION_TABLE_MODEL",
        "DIVISION_TABLE_ROLE_HIGHLIGHT",
        "DIVISION_TABLE_CELL_MODEL",
    ]
    labels = [label for item in evidence for label in item["rendered_evidence"]["labels"]]
    assert "720" in labels
    assert "60" in labels
    assert "12" in labels


def test_unknown_learning_visual_fails_closed():
    backend = MockVectorBackend()
    bbox = BoundingBox(x=40.0, y=40.0, width=420.0, height=140.0)
    with pytest.raises(UnsupportedPrimaryPrimitive, match="TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED"):
        render_primitive("EMPTY_LABEL_CARD", {}, backend, bbox)
