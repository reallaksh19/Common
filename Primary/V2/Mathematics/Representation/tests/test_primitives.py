"""
Tests for all Primary Mathematics V2 representation primitives using MockVectorBackend.
Verifies no exceptions, non-zero element counts, and valid recorded evidence.
"""
import pytest
from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, MockVectorBackend
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive


@pytest.fixture
def mock_backend():
    return MockVectorBackend()


@pytest.fixture
def test_bbox():
    return BoundingBox(x=40.0, y=40.0, width=515.27, height=200.0)


def test_render_multiplication_primitives(mock_backend, test_bbox):
    render_primitive("EQUAL_GROUPS", {"group_count": 6, "items_per_group": 23}, mock_backend, test_bbox)
    render_primitive("ARRAY", {"rows": 6, "cols": 23}, mock_backend, test_bbox)
    render_primitive("AREA_MODEL", {
        "factors": [23, 6],
        "partitions": [{"length": 20, "height": 6, "area": 120}, {"length": 3, "height": 6, "area": 18}]
    }, mock_backend, test_bbox)
    render_primitive("PARTIAL_PRODUCTS", {"factors": [23, 6], "partial_products": [120, 18], "product": 138}, mock_backend, test_bbox)
    render_primitive("ESTIMATE_CHECK", {"actual": 138, "estimate_expr": "20 x 6 = 120"}, mock_backend, test_bbox)

    evidence = mock_backend.get_evidence()
    assert len(evidence) == 5
    for ev in evidence:
        assert ev["rendered_evidence"]["data_grounded"] is True
        assert ev["rendered_evidence"]["element_count"] > 0


def test_render_division_internal_zero_bracket(mock_backend, test_bbox):
    params = {
        "dividend": 7843,
        "divisor": 13,
        "quotient": 603,
        "remainder": 4,
        "quotient_digits": ["6", "0", "3"],
        "multiples_table": [13, 26, 39, 52, 65, 78, 91, 104, 117, 130],
        "steps": [
            {"type": "SUBTRACTION", "value": 78, "col": 1},
            {"type": "BRING_DOWN", "value": 4, "col": 2},
            {"type": "SUBTRACTION", "value": 0, "col": 2},
            {"type": "BRING_DOWN", "value": 3, "col": 3},
            {"type": "SUBTRACTION", "value": 39, "col": 3},
            {"type": "REMAINDER", "value": 4, "col": 3}
        ]
    }
    render_primitive("LONG_DIVISION_WORKOUT", params, mock_backend, test_bbox)
    evidence = mock_backend.get_evidence()
    assert len(evidence) == 1
    assert "0" in evidence[0]["rendered_evidence"]["labels"]
    assert "7843" in evidence[0]["rendered_evidence"]["labels"]
    assert "13" in evidence[0]["rendered_evidence"]["labels"]


def test_render_fractions_decimals_geometry_primitives(mock_backend, test_bbox):
    render_primitive("FRACTION_STRIP", {"numerator": 3, "denominator": 4, "label": "3/4"}, mock_backend, test_bbox)
    render_primitive("DECIMAL_HUNDRED_GRID", {"decimal_value": 0.45, "grid_shaded_cells": 45}, mock_backend, test_bbox)
    render_primitive("DECIMAL_NUMBER_LINE", {"min_val": 0.0, "max_val": 1.0, "target_val": 0.45}, mock_backend, test_bbox)
    render_primitive("PLACE_VALUE_BLOCKS", {"number": 4567, "expanded": [4000, 500, 60, 7]}, mock_backend, test_bbox)
    render_primitive("MEASUREMENT_CONVERSION", {"from_value": 3, "from_unit": "KILOMETRE", "factor": 1000, "to_value": 3000, "to_unit": "METRE"}, mock_backend, test_bbox)
    render_primitive("RECTILINEAR_PERIMETER_AREA", {"width": 5, "height": 3, "perimeter": 16, "area": 15, "unit": "cm"}, mock_backend, test_bbox)
    render_primitive("VOLUME_CUBE_LAYERS", {"length": 4, "width": 3, "height": 2}, mock_backend, test_bbox)
    render_primitive("GEOMETRIC_ANGLE", {"angle_degrees": 120, "classification": "OBTUSE"}, mock_backend, test_bbox)
    render_primitive("DATA_BAR_CHART", {"categories": ["Apples", "Bananas"], "values": [15, 25], "scale_unit": 5}, mock_backend, test_bbox)

    evidence = mock_backend.get_evidence()
    assert len(evidence) == 9
    for ev in evidence:
        assert ev["rendered_evidence"]["data_grounded"] is True
        assert ev["rendered_evidence"]["element_count"] > 0
