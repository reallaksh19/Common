import pytest

from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive


@pytest.mark.parametrize(
    "kind,params",
    [
        ("OBJECT_GROUPS", {"declared_quantity": 12, "rendered_quantity": 12}),
        ("MONEY_MODEL", {"groups": [{"kind": "PEN", "count": 4, "unit_price": 50}, {"kind": "PENCIL", "count": 8, "unit_price": 40}]}),
        ("MONEY_MODEL", {"subtotals": [200, 320]}),
        ("QUANTITY_STRUCTURE_MAP", {"branches": ["4x50", "8x40"]}),
        ("INVERSE_CHECK", {"expression": "520 - 320 = 200"}),
        ("DIV_EQUAL_GROUP", {"group_size": 12}),
        ("DIV_MULTIPLES_STRIP", {"divisor": 24}),
        ("DIV_MULTIPLES_STRIP", {"comparisons": ["12x40=480", "12x39=468"]}),
        ("DIV_REMAINDER_CONTEXT", {"declared_quantity": 39, "rendered_quantity": 3, "continuation_marker": "... x39", "group_size": 12, "leftover": 7}),
        ("ESTIMATE_BOUND", {"estimate": 300}),
        ("DIV_LONG_ALGORITHM", {"dividend": 7048, "divisor": 24, "quotient": 293, "remainder": 16}),
        ("DIV_LONG_ALGORITHM", {"partial_dividend": 70, "quotient_digit": 2, "product": 48}),
        ("ANGLE_RAYS_ARC", {"degrees": 60}),
        ("ANGLE_BENCHMARK_COMPARE", {"degrees": 90}),
        ("ANGLE_OBJECT_EXAMPLE", {"examples": ["scissors", "clock", "triangle"]}),
        ("ANGLE_OBJECT_EXAMPLE", {"mark_vertex": True}),
    ],
)
def test_grade4_semantic_primitive_is_realized_and_records_evidence(kind, params):
    backend = MockVectorBackend()
    render_primitive(kind, params, backend, BoundingBox(20, 20, 520, 190))

    assert backend.operations, kind
    evidence = backend.get_evidence()
    assert evidence, kind
    assert evidence[-1]["rendered_evidence"]["data_grounded"] is True


def test_angle_rays_arc_uses_actual_geometry_not_placeholder_card():
    backend = MockVectorBackend()
    render_primitive("ANGLE_RAYS_ARC", {"degrees": 60}, backend, BoundingBox(20, 20, 520, 190))
    operations = backend.operations

    assert len([op for op in operations if op["op"] == "line"]) >= 3
    assert any(op["op"] == "polygon" for op in operations)  # arrowheads
    assert any(op["op"] == "text" and "60" in str(op["text"]) for op in operations)


def test_long_division_primary_visual_contains_bracket_and_quotient_digits():
    backend = MockVectorBackend()
    render_primitive(
        "DIV_LONG_ALGORITHM",
        {"dividend": 7048, "divisor": 24, "quotient": 293, "remainder": 16},
        backend,
        BoundingBox(20, 20, 520, 190),
    )
    texts = [str(op["text"]) for op in backend.operations if op["op"] == "text"]
    lines = [op for op in backend.operations if op["op"] == "line"]

    assert "24" in texts
    assert "7" in texts and "0" in texts and "4" in texts and "8" in texts
    assert "2" in texts and "9" in texts and "3" in texts
    assert len(lines) >= 2
