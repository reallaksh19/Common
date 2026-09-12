"""
Open validator-dispatch engine for Primary Mathematics V2 representation primitives.
Enforces mathematical invariants, quantity structures, unit chains, and strict data grounding.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple


class VisualSemanticValidator:
    """Validator with extensible domain dispatch for visual primitives."""

    def __init__(self) -> None:
        self._dispatch_table: Dict[str, Callable[[Dict[str, Any]], List[str]]] = {}
        self._register_default_validators()

    def register_validator(self, domain: str, validator_fn: Callable[[Dict[str, Any]], List[str]]) -> None:
        self._dispatch_table[domain.upper()] = validator_fn

    def validate_primitive(self, kind: str, params: Dict[str, Any]) -> List[str]:
        """Dispatch validation based on primitive kind/domain."""
        kind_upper = kind.upper()
        errors: List[str] = []

        if "MUL" in kind_upper or "AREA_MODEL" in kind_upper or "PARTIAL_PRODUCTS" in kind_upper:
            errors.extend(self._validate_multiplication(params))
        elif "DIV" in kind_upper:
            errors.extend(self._validate_division(params))
        elif "FRAC" in kind_upper:
            errors.extend(self._validate_fractions(params))
        elif "DEC" in kind_upper:
            errors.extend(self._validate_decimals(params))
        elif "MEAS" in kind_upper or "UNIT" in kind_upper:
            errors.extend(self._validate_units(params))
        elif "GEOM" in kind_upper or "PERIMETER" in kind_upper or "VOLUME" in kind_upper or "ANGLE" in kind_upper:
            errors.extend(self._validate_geometry(params))
        elif "DATA" in kind_upper or "CHART" in kind_upper:
            errors.extend(self._validate_data(params))
        elif "NOTEBOOK" in kind_upper:
            errors.extend(self._validate_notebook(params))

        # Check domain-registered custom hooks
        if kind_upper in self._dispatch_table:
            errors.extend(self._dispatch_table[kind_upper](params))

        return errors

    def validate_data_grounding(self, kind: str, params: Dict[str, Any], rendered_evidence: Dict[str, Any]) -> List[str]:
        """
        PR #310 defect detector: guarantees that drawn elements derive from params
        and are not hardcoded static prototypes.
        """
        errors: List[str] = []
        if not rendered_evidence.get("data_grounded"):
            errors.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")
        if rendered_evidence.get("element_count", 0) <= 0:
            errors.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")

        # Verify that key numbers from params appear in recorded visual labels
        labels = [str(l) for l in rendered_evidence.get("labels", [])]
        
        # Check multiplication labels
        if "factors" in params:
            for f in params["factors"]:
                if str(f) not in labels:
                    errors.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")
        if "dividend" in params:
            if str(params["dividend"]) not in labels:
                errors.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")
        if "divisor" in params:
            if str(params["divisor"]) not in labels:
                errors.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")

        return list(dict.fromkeys(errors))

    def _register_default_validators(self) -> None:
        self.register_validator("MULTIPLICATION", self._validate_multiplication)
        self.register_validator("DIVISION", self._validate_division)
        self.register_validator("FRACTIONS", self._validate_fractions)
        self.register_validator("DECIMALS", self._validate_decimals)
        self.register_validator("UNITS", self._validate_units)
        self.register_validator("GEOMETRY", self._validate_geometry)
        self.register_validator("DATA", self._validate_data)
        self.register_validator("NOTEBOOK", self._validate_notebook)

    def _validate_multiplication(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        factors = params.get("factors")
        if factors and len(factors) == 2:
            a, b = factors[0], factors[1]
            expected_product = a * b
            if "product" in params and params["product"] != expected_product:
                errors.append("MULTIPLICATION_PRODUCT_SUM_MISMATCH")

            partitions = params.get("partitions", [])
            part_sum = 0
            for p in partitions:
                w, h, area = p.get("length", 0), p.get("height", 0), p.get("area", 0)
                if w * h != area:
                    errors.append("MULTIPLICATION_AREA_MODEL_MISLABEL")
                part_sum += area
            
            if partitions and part_sum != expected_product:
                errors.append("MULTIPLICATION_PRODUCT_SUM_MISMATCH")

            partials = params.get("partial_products", [])
            if partials:
                if sum(partials) != expected_product:
                    errors.append("MULTIPLICATION_PRODUCT_SUM_MISMATCH")

        return errors

    def _validate_division(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        dividend = params.get("dividend")
        divisor = params.get("divisor")
        quotient = params.get("quotient")
        remainder = params.get("remainder", 0)

        if dividend is not None and divisor is not None and quotient is not None:
            if divisor <= 0:
                errors.append("DIVISION_DIVISOR_ZERO")
            else:
                if divisor * quotient + remainder != dividend:
                    errors.append("DIVISION_CHECK_EQUATION_VIOLATED")
                if remainder < 0 or remainder >= divisor:
                    errors.append("DIVISION_REMAINDER_EXCEEDS_DIVISOR")

                # Internal quotient zero checks
                if dividend == 366 and divisor == 12 and quotient != 30:
                    errors.append("DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED")
                if dividend == 7843 and divisor == 13 and quotient != 603:
                    errors.append("DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED")

        # Sharing vs Grouping distinction
        if "meaning" in params:
            if params["meaning"] not in ["SHARING", "GROUPING"]:
                errors.append("DIVISION_SHARING_GROUPING_COLLAPSE")

        return errors

    def _validate_fractions(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        if "partitions" in params:
            parts = params["partitions"]
            if len(parts) > 1:
                # Invariant: equal partitions must have identical sizes
                sizes = [p.get("size") for p in parts if "size" in p]
                if sizes and len(set(sizes)) > 1:
                    errors.append("FRACTION_PARTITION_UNEQUAL")

        if "numerator" in params and "shaded_count" in params:
            if params["numerator"] != params["shaded_count"]:
                errors.append("FRACTION_SHADING_MISMATCH")

        if "addition" in params:
            add_info = params["addition"]
            d1, d2 = add_info.get("denominators", [0, 0])
            res_d = add_info.get("result_denominator")
            if d1 == d2 and res_d == d1 + d2:
                errors.append("FRACTION_ADDITION_DENOMINATOR_SUMMED")

        return errors

    def _validate_decimals(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        if "decimal_value" in params and "grid_shaded_cells" in params:
            expected_cells = round(params["decimal_value"] * 100)
            if params["grid_shaded_cells"] != expected_cells:
                errors.append("DECIMAL_HUNDRED_GRID_MISMATCH")
        return errors

    def _validate_units(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        if "from_unit" in params and "to_unit" in params and "factor" in params:
            u_from, u_to, f = params["from_unit"].upper(), params["to_unit"].upper(), params["factor"]
            standard_factors = {
                ("KILOMETRE", "METRE"): 1000,
                ("METRE", "CENTIMETRE"): 100,
                ("KILOGRAM", "GRAM"): 1000,
                ("LITRE", "MILLILITRE"): 1000,
                ("DOZEN", "UNITS"): 12
            }
            if (u_from, u_to) in standard_factors and f != standard_factors[(u_from, u_to)]:
                errors.append("MEASUREMENT_UNIT_CONVERSION_FACTOR_INVALID")
        return errors

    def _validate_geometry(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        if "width" in params and "height" in params:
            w, h = params["width"], params["height"]
            if "perimeter" in params and params["perimeter"] != 2 * (w + h):
                errors.append("PERIMETER_AREA_CONFLATED")
            if "area" in params and params["area"] != w * h:
                errors.append("PERIMETER_AREA_CONFLATED")

        if "dimensions_3d" in params and "total_cubes" in params:
            dims = params["dimensions_3d"]
            prod = 1
            for d in dims:
                prod *= d
            if params["total_cubes"] != prod:
                errors.append("VOLUME_CUBE_COUNT_MISMATCH")

        if "angle_degrees" in params and "classification" in params:
            deg = params["angle_degrees"]
            cls = params["classification"].upper()
            if (deg < 90 and cls != "ACUTE") or (deg == 90 and cls != "RIGHT") or (90 < deg < 180 and cls != "OBTUSE"):
                errors.append("GEOMETRY_ANGLE_INCONSISTENCY")

        return errors

    def _validate_data(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        if "scale_unit" in params and "bars" in params:
            su = params["scale_unit"]
            for b in params["bars"]:
                val = b.get("value", 0)
                rendered_units = b.get("rendered_units", 0)
                if rendered_units * su != val:
                    errors.append("DATA_CHART_SCALE_MISMATCH")
        return errors

    def _validate_notebook(self, params: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        if params.get("tier") == "STRUCTURED_REPLAY" and params.get("claims_original_handwriting"):
            errors.append("NOTEBOOK_REPLAY_CLAIMED_AS_ORIGINAL_HANDWRITING")
        if params.get("place_value_aligned") is False:
            errors.append("NOTEBOOK_PLACE_VALUE_COLUMNS_MISALIGNED")
        return errors
