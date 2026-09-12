"""
Master Primitive Dispatcher for Primary Mathematics V2.
Maps primitive calls to concrete implementations and fails closed on unknown kinds.
A caller may suffix a primitive kind with ``__<semantic-id>`` for non-visible
placement custody; rendering dispatch uses only the base kind before ``__``.
"""
from __future__ import annotations

from typing import Any, Dict
from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, VectorRenderBackend
from Primary.V2.Mathematics.Representation.engine.primitives.operations import MultiplicationPrimitives, DivisionPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.realized_array import RealizedArrayPrimitive
from Primary.V2.Mathematics.Representation.engine.primitives.fractions import FractionPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.fraction_bridges import FractionBridgePrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.decimals import DecimalPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.numbers import NumberPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.measurement import MeasurementPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.geometry import GeometryPrimitives
from Primary.V2.Mathematics.Representation.engine.primitives.data import DataPrimitives
from Primary.V2.Mathematics.Representation.engine.notebook import AuthenticNotebookEngine, LongDivisionWorkoutSpec, ProvenanceTier


def render_primitive(kind: str, params: Dict[str, Any], backend: VectorRenderBackend, bbox: BoundingBox) -> None:
    """Render one grounded Primary Math primitive or fail closed."""
    k = kind.upper().split("__", 1)[0]
    if k == "EQUAL_GROUPS":
        MultiplicationPrimitives.draw_equal_groups(backend, bbox, params)
    elif k == "ARRAY":
        RealizedArrayPrimitive.draw(backend, bbox, params)
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
    elif k == "FRACTION_NUMBER_LINE":
        FractionBridgePrimitives.draw_fraction_number_line(backend, bbox, params)
    elif k == "FRACTION_ADDITION_REPARTITION":
        FractionBridgePrimitives.draw_fraction_addition_repartition(backend, bbox, params)
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
        factors = params.get("factors")
        partial_products = params.get("partial_products")
        total_product = params.get("total_product")
        if not factors or partial_products is None or total_product is None:
            raise ValueError("VERTICAL_MULTIPLICATION requires factors, partial_products and total_product")
        nb = AuthenticNotebookEngine(backend)
        nb.render_vertical_multiplication(
            bbox=bbox,
            factors=factors,
            carry_rows=params.get("carry_rows", []),
            partial_products=partial_products,
            total_product=total_product,
            tier=ProvenanceTier(params.get("tier", "STRUCTURED_REPLAY")),
        )
    else:
        raise ValueError(f"UNKNOWN_PRIMARY_MATH_PRIMITIVE: {kind}")
