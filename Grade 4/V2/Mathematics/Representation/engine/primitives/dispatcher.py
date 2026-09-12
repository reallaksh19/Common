"""Master Primitive Dispatcher for Grade 4 Mathematics V2.

Maps typed LearningDesign primitive calls to concrete vector implementations.
Unsupported mathematical visuals fail closed rather than becoming label-only cards.
"""
from __future__ import annotations

from typing import Any, Dict
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    VectorRenderBackend,
)
from Primary.V2.Mathematics.Representation.engine.primitives.operations import (
    MultiplicationPrimitives,
    DivisionPrimitives,
)
from Primary.V2.Mathematics.Representation.engine.primitives.fractions import FractionPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.decimals import DecimalPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.numbers import NumberPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.measurement import MeasurementPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.geometry import GeometryPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.data import DataPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.learning_support import LearningSupportPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.grade4_semantics import Grade4SemanticPrimitives
from Primary.V2.Mathematics.Representation.engine.notebook import (
    AuthenticNotebookEngine,
    LongDivisionWorkoutSpec,
    ProvenanceTier,
)


class UnsupportedPrimaryPrimitive(ValueError):
    """Fail closed rather than degrade a required learning visual to an empty card."""


def render_primitive(
    kind: str,
    params: Dict[str, Any],
    backend: VectorRenderBackend,
    bbox: BoundingBox,
) -> None:
    """Render one validated mathematical primitive from semantic params only."""
    k = kind.upper()

    # Canonical Grade-4 LearningDesign semantic primitives.
    if k == "OBJECT_GROUPS":
        Grade4SemanticPrimitives.draw_object_groups(backend, bbox, params)
    elif k == "MONEY_MODEL":
        Grade4SemanticPrimitives.draw_money_model(backend, bbox, params)
    elif k == "QUANTITY_STRUCTURE_MAP":
        Grade4SemanticPrimitives.draw_quantity_structure_map(backend, bbox, params)
    elif k == "INVERSE_CHECK":
        Grade4SemanticPrimitives.draw_inverse_check(backend, bbox, params)
    elif k == "DIV_EQUAL_GROUP":
        Grade4SemanticPrimitives.draw_div_equal_group(backend, bbox, params)
    elif k == "DIV_MULTIPLES_STRIP":
        Grade4SemanticPrimitives.draw_div_multiples_strip(backend, bbox, params)
    elif k == "DIV_REMAINDER_CONTEXT":
        Grade4SemanticPrimitives.draw_div_remainder_context(backend, bbox, params)
    elif k == "ESTIMATE_BOUND":
        Grade4SemanticPrimitives.draw_estimate_bound(backend, bbox, params)
    elif k == "DIV_LONG_ALGORITHM":
        Grade4SemanticPrimitives.draw_div_long_algorithm(backend, bbox, params)
    elif k == "ANGLE_RAYS_ARC":
        Grade4SemanticPrimitives.draw_angle_rays_arc(backend, bbox, params)
    elif k == "ANGLE_BENCHMARK_COMPARE":
        Grade4SemanticPrimitives.draw_angle_benchmark_compare(backend, bbox, params)
    elif k == "ANGLE_OBJECT_EXAMPLE":
        Grade4SemanticPrimitives.draw_angle_object_example(backend, bbox, params)

    # Existing reusable mathematical primitives.
    elif k == "EQUAL_GROUPS":
        MultiplicationPrimitives.draw_equal_groups(backend, bbox, params)
    elif k == "ARRAY":
        MultiplicationPrimitives.draw_array(backend, bbox, params)
    elif k == "AREA_MODEL":
        MultiplicationPrimitives.draw_area_model(backend, bbox, params)
    elif k == "PARTIAL_PRODUCTS":
        MultiplicationPrimitives.draw_partial_products(backend, bbox, params)
    elif k == "ESTIMATE_CHECK":
        MultiplicationPrimitives.draw_estimate_check(backend, bbox, params)
    elif k in {"DIVISION_STRUCTURE", "DIVISION_SHARING_VS_GROUPING"}:
        DivisionPrimitives.draw_sharing_vs_grouping(backend, bbox, params)
    elif k == "DIVISION_REMAINDER_CONTEXT":
        DivisionPrimitives.draw_remainder_context(backend, bbox, params)
    elif k == "UNIT_CHAIN":
        DivisionPrimitives.draw_unit_chain(backend, bbox, params)
    elif k == "FRACTION_STRIP":
        FractionPrimitives.draw_fraction_strip(backend, bbox, params)
    elif k == "FRACTION_COMPARISON":
        FractionPrimitives.draw_fraction_comparison(backend, bbox, params)
    elif k == "FRACTION_ADDITION":
        FractionPrimitives.draw_fraction_addition(backend, bbox, params)
    elif k == "DECIMAL_HUNDRED_GRID":
        DecimalPrimitives.draw_hundred_grid(backend, bbox, params)
    elif k == "DECIMAL_NUMBER_LINE":
        DecimalPrimitives.draw_decimal_number_line(backend, bbox, params)
    elif k == "PLACE_VALUE_BLOCKS":
        NumberPrimitives.draw_place_value(backend, bbox, params)
    elif k == "MEASUREMENT_CONVERSION":
        MeasurementPrimitives.draw_conversion(backend, bbox, params)
    elif k == "RECTILINEAR_PERIMETER_AREA":
        GeometryPrimitives.draw_perimeter_area(backend, bbox, params)
    elif k == "VOLUME_CUBE_LAYERS":
        GeometryPrimitives.draw_volume_layers(backend, bbox, params)
    elif k == "GEOMETRIC_ANGLE":
        GeometryPrimitives.draw_angle(backend, bbox, params)
    elif k in {"DATA_BAR_CHART", "BAR_CHART"}:
        DataPrimitives.draw_scaled_bar_chart(backend, bbox, params)
    elif k == "RATE_COMPARE":
        LearningSupportPrimitives.draw_rate_compare(backend, bbox, params)
    elif k == "SCALE_FACTOR_VIEW":
        LearningSupportPrimitives.draw_scale_factor(backend, bbox, params)
    elif k in {"RATE_SCALE_MODEL", "SAME_RATE_SCALE"}:
        LearningSupportPrimitives.draw_rate_scale_model(backend, bbox, params)
    elif k == "DIVISION_TABLE_MODEL":
        LearningSupportPrimitives.draw_division_table_model(backend, bbox, params)
    elif k == "DIVISION_TABLE_ROLE_HIGHLIGHT":
        LearningSupportPrimitives.draw_division_table_roles(backend, bbox, params)
    elif k == "DIVISION_TABLE_CELL_MODEL":
        LearningSupportPrimitives.draw_division_table_cell(backend, bbox, params)
    elif k == "LONG_DIVISION_WORKOUT":
        nb = AuthenticNotebookEngine(backend)
        spec = LongDivisionWorkoutSpec(
            dividend=params.get("dividend", 0),
            divisor=params.get("divisor", 1),
            quotient=params.get("quotient", 0),
            remainder=params.get("remainder", 0),
            quotient_digits=params.get("quotient_digits", [str(params.get("quotient", 0))]),
            steps=params.get("steps", []),
            multiples_table=params.get("multiples_table"),
            provenance_tier=ProvenanceTier(params.get("provenance_tier", "STRUCTURED_REPLAY")),
            actor=params.get("actor", "CHILD"),
            claims_original_handwriting=params.get("claims_original_handwriting", False),
        )
        nb.render_long_division_bracket(bbox, spec)
    elif k == "VERTICAL_MULTIPLICATION":
        nb = AuthenticNotebookEngine(backend)
        nb.render_vertical_multiplication(
            bbox=bbox,
            factors=params.get("factors", [23, 6]),
            carry_rows=params.get("carry_rows", []),
            partial_products=params.get("partial_products", [18, 120]),
            total_product=params.get("total_product", 138),
            tier=ProvenanceTier(params.get("tier", "STRUCTURED_REPLAY")),
        )
    else:
        raise UnsupportedPrimaryPrimitive(
            f"TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED: unsupported primitive {kind!r}"
        )
