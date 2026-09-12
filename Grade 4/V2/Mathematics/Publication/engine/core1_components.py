"""Measured Core1 components driven only by LearningRepresentationPlan.

These components do not select pedagogy. They realize an already validated
primary visual and typed work surface. Unsupported semantic kinds fail closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend,
)
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import (
    UnsupportedPrimaryPrimitive,
    render_primitive,
)


@dataclass
class Core1ComponentError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise Core1ComponentError(code, message)


class PrimaryVisualComponent:
    """Large learner visual. No label-only fallback is permitted."""

    HEIGHT = 190.0

    @classmethod
    def measure(cls, visual: Mapping[str, Any], width: float) -> float:
        _require(bool(visual.get("primitive_kind")), "CORE1_PRIMARY_VISUAL_MISSING", "primitive_kind required")
        _require(isinstance(visual.get("semantic_params"), dict), "CORE1_PRIMARY_VISUAL_PARAMS_MISSING", "semantic_params required")
        _require(bool(visual.get("validator_refs")), "UNVALIDATED_VISUAL_DRAWN", "primary visual needs validator refs")
        return cls.HEIGHT

    @classmethod
    def render(cls, backend: VectorRenderBackend, bbox: BoundingBox, visual: Mapping[str, Any]) -> None:
        cls.measure(visual, bbox.width)
        try:
            render_primitive(
                str(visual["primitive_kind"]),
                dict(visual.get("semantic_params") or {}),
                backend,
                bbox,
            )
        except UnsupportedPrimaryPrimitive as exc:
            raise Core1ComponentError(
                "CORE1_PRIMARY_VISUAL_NOT_REALIZED",
                f"{visual.get('primitive_kind')}: upstream Representation must provide a realized primitive",
            ) from exc


class WorkSurfaceComponent:
    """Typed mathematical work surfaces; never degrades to a generic math box."""

    HEIGHTS = {
        "LONG_DIVISION_WORK": 255.0,
        "SHORT_DIVISION_WORK": 225.0,
        "DIVISION_TABLE_WORKSPACE": 185.0,
        "ANGLE_DRAWING_WORKSPACE": 175.0,
        "VERTICAL_MULTIPLICATION_WORK": 230.0,
        "MULTIPLICATION_PARTIAL_PRODUCTS_WORK": 185.0,
        "UNIT_CHAIN_WORK": 165.0,
    }

    @classmethod
    def measure(cls, surface: Mapping[str, Any], width: float) -> float:
        kind = str(surface.get("kind") or "")
        _require(kind in cls.HEIGHTS, "WORK_SURFACE_KIND_NOT_REALIZED", kind or "<missing>")
        _require(isinstance(surface.get("semantic_params"), dict), "WORK_SURFACE_PARAMS_MISSING", kind)
        _require(bool(surface.get("validator_refs")), "UNVALIDATED_WORK_SURFACE", kind)
        return cls.HEIGHTS[kind]

    @classmethod
    def _draw_notebook_grid(cls, backend: VectorRenderBackend, bbox: BoundingBox, grid: float = 22.0) -> None:
        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE,
            stroke=PrimaryPalette.CARD_BORDER,
            stroke_width=1.0,
            corner_radius=5.0,
        )
        x = bbox.x + grid
        while x < bbox.x_max:
            backend.draw_line(x, bbox.y, x, bbox.y_max, stroke=PrimaryPalette.GRID_LINE, stroke_width=0.45)
            x += grid
        y = bbox.y + grid
        while y < bbox.y_max:
            backend.draw_line(bbox.x, y, bbox.x_max, y, stroke=PrimaryPalette.GRID_LINE, stroke_width=0.45)
            y += grid

    @classmethod
    def _render_long_division_semantic(
        cls,
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Mapping[str, Any],
    ) -> None:
        required = {"dividend", "divisor", "quotient", "remainder"}
        _require(required.issubset(params), "LONG_DIVISION_WORK_SURFACE_INVALID", f"missing {sorted(required - set(params))}")

        dividend = int(params["dividend"])
        divisor = int(params["divisor"])
        quotient = int(params["quotient"])
        remainder = int(params["remainder"])
        steps = list(params.get("steps") or [])
        quotient_places = [int(x) for x in params.get("quotient_places", list(str(quotient)))]

        _require(divisor > 0, "LONG_DIVISION_WORK_SURFACE_INVALID", "divisor must be positive")
        _require(divisor * quotient + remainder == dividend, "PRIMARY_VISUAL_ALGORITHM_INVALID", "D x Q + R must equal dividend")
        _require(0 <= remainder < divisor, "PRIMARY_VISUAL_REMAINDER_INVALID", "remainder must be smaller than divisor")
        _require(quotient_places == [int(x) for x in str(quotient)], "DIVISION_QUOTIENT_PLACE_SLOTS_INVALID", "quotient place slots must preserve every digit")

        cls._draw_notebook_grid(backend, bbox)

        # Long-division bracket on the left.
        col_w = 23.0
        origin_x = bbox.x + 58.0
        start_y = bbox.y_max - 52.0
        dividend_s = str(dividend)
        quotient_s = "".join(str(x) for x in quotient_places)
        backend.draw_text(str(divisor), origin_x - 12.0, start_y, font_size=15.0, color=PrimaryPalette.NAVY, align="right")
        bracket_x = origin_x - 4.0
        backend.draw_line(bracket_x, start_y - 4.0, bracket_x, start_y + 18.0, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
        backend.draw_line(bracket_x, start_y + 18.0, bracket_x + len(dividend_s) * col_w + 16.0, start_y + 18.0, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
        for index, char in enumerate(dividend_s):
            backend.draw_text(char, origin_x + index * col_w + 8.0, start_y, font_size=15.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")

        offset = len(dividend_s) - len(quotient_s)
        for index, char in enumerate(quotient_s):
            target_col = offset + index
            backend.draw_text(char, origin_x + target_col * col_w + 8.0, start_y + 23.0, font_size=15.0, color=PrimaryPalette.NAVY, align="center")

        # Semantic step ledger on the right. This is derived from the canonical
        # work-surface fields rather than an unrelated renderer-specific step schema.
        ledger_x = bbox.x + bbox.width * 0.56
        ledger_y = bbox.y_max - 32.0
        backend.draw_text("Divide  •  Multiply  •  Subtract  •  Bring down", ledger_x, ledger_y, font_size=10.5, color=PrimaryPalette.TEAL)
        ledger_y -= 24.0

        for index, step in enumerate(steps):
            for key in ("partial_dividend", "quotient_digit", "product", "subtraction_remainder"):
                _require(key in step, "LONG_DIVISION_WORK_SURFACE_INVALID", f"step {index} missing {key}")
            partial = int(step["partial_dividend"])
            q_digit = int(step["quotient_digit"])
            product = int(step["product"])
            step_rem = int(step["subtraction_remainder"])
            bring = step.get("bring_down_digit")
            _require(product == divisor * q_digit, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: product mismatch")
            _require(partial - product == step_rem, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: subtraction mismatch")

            backend.draw_text(f"{index + 1}", ledger_x, ledger_y, font_size=10.5, color=PrimaryPalette.SLATE)
            backend.draw_text(str(partial), ledger_x + 38.0, ledger_y, font_size=13.5, color=PrimaryPalette.STUDENT_PENCIL, align="right")
            ledger_y -= 17.0
            backend.draw_text(f"- {product}", ledger_x + 38.0, ledger_y, font_size=13.5, color=PrimaryPalette.STUDENT_PENCIL, align="right")
            backend.draw_line(ledger_x + 2.0, ledger_y - 3.0, ledger_x + 44.0, ledger_y - 3.0, stroke=PrimaryPalette.SLATE, stroke_width=1.0)
            ledger_y -= 18.0
            result_text = str(step_rem)
            if bring is not None:
                result_text += f"  ↓ {int(bring)}"
            else:
                result_text += "  remainder"
            backend.draw_text(result_text, ledger_x + 4.0, ledger_y, font_size=12.5, color=PrimaryPalette.TEAL)
            ledger_y -= 24.0

        check_y = bbox.y + 18.0
        backend.draw_text(
            f"Check: {divisor} × {quotient} + {remainder} = {dividend}",
            bbox.x + bbox.width * 0.54,
            check_y,
            font_size=11.5,
            color=PrimaryPalette.NAVY,
        )

    @classmethod
    def render(cls, backend: VectorRenderBackend, bbox: BoundingBox, surface: Mapping[str, Any]) -> None:
        cls.measure(surface, bbox.width)
        kind = str(surface["kind"])
        params = dict(surface.get("semantic_params") or {})

        if kind in {"LONG_DIVISION_WORK", "SHORT_DIVISION_WORK"}:
            cls._render_long_division_semantic(backend, bbox, params)
            return

        if kind == "DIVISION_TABLE_WORKSPACE":
            _require(bool(params.get("columns")) and bool(params.get("rows")), "DIVISION_TABLE_WORKSPACE_INVALID", "columns and rows required")
            # Correct quotients remain semantic evidence but are intentionally not
            # passed to the learner-facing workspace: cells start blank.
            render_primitive(
                "DIVISION_TABLE_MODEL",
                {"columns": list(params["columns"]), "rows": list(params["rows"]), "cell_mode": "BLANK"},
                backend,
                bbox,
            )
            return

        if kind == "ANGLE_DRAWING_WORKSPACE":
            slots = int(params.get("slots", 0))
            _require(1 <= slots <= 6, "ANGLE_DRAWING_WORKSPACE_INVALID", "slots must be 1..6")
            gap = 10.0
            slot_w = (bbox.width - gap * (slots - 1)) / slots
            for index in range(slots):
                x = bbox.x + index * (slot_w + gap)
                backend.draw_rect(
                    x, bbox.y, slot_w, bbox.height,
                    fill=PrimaryPalette.WHITE,
                    stroke=PrimaryPalette.CARD_BORDER,
                    stroke_width=1.0,
                    corner_radius=5.0,
                )
                backend.draw_text(str(index + 1), x + 9.0, bbox.y_max - 18.0, font_size=11.0, color=PrimaryPalette.SLATE)
                # A neutral vertex marker provides a place to start without
                # prescribing an angle size or leaking an answer.
                vx = x + slot_w * 0.28
                vy = bbox.y + bbox.height * 0.40
                backend.draw_text("•", vx, vy, font_size=16.0, color=PrimaryPalette.SLATE, align="center")
            return

        if kind == "VERTICAL_MULTIPLICATION_WORK":
            required = {"factors", "partial_products", "total_product"}
            _require(required.issubset(params), "VERTICAL_MULTIPLICATION_WORK_INVALID", f"missing {sorted(required - set(params))}")
            render_primitive(
                "VERTICAL_MULTIPLICATION",
                {
                    "factors": list(params["factors"]),
                    "carry_rows": list(params.get("carry_rows") or []),
                    "partial_products": list(params["partial_products"]),
                    "total_product": params["total_product"],
                    "tier": surface.get("provenance", "STRUCTURED_REPLAY"),
                },
                backend,
                bbox,
            )
            return

        if kind == "MULTIPLICATION_PARTIAL_PRODUCTS_WORK":
            render_primitive("PARTIAL_PRODUCTS", params, backend, bbox)
            return

        if kind == "UNIT_CHAIN_WORK":
            render_primitive("UNIT_CHAIN", params, backend, bbox)
            return

        raise Core1ComponentError("WORK_SURFACE_KIND_NOT_REALIZED", kind)
