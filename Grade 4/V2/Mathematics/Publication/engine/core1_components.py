"""Measured Core1 components driven only by LearningRepresentationPlan.

These components do not select pedagogy. They realize an already validated
primary visual and typed work surface. Unsupported semantic kinds fail closed.
Learner work surfaces preserve validated answer semantics upstream but do not
print those answers into the workspace.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from Grade4.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend,
)
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import (
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
    """Large learner visual. No label-only fallback or shrink-to-fit is permitted."""

    MIN_HEIGHT = 170.0

    @classmethod
    def measure(cls, visual: Mapping[str, Any], width: float) -> float:
        _require(width > 0, "CORE1_PRIMARY_VISUAL_WIDTH_INVALID", str(width))
        _require(bool(visual.get("primitive_kind")), "CORE1_PRIMARY_VISUAL_MISSING", "primitive_kind required")
        _require(isinstance(visual.get("semantic_params"), dict), "CORE1_PRIMARY_VISUAL_PARAMS_MISSING", "semantic_params required")
        _require(bool(visual.get("validator_refs")), "UNVALIDATED_VISUAL_DRAWN", "primary visual needs validator refs")

        kind = str(visual["primitive_kind"]).upper()
        params = visual.get("semantic_params") or {}
        if kind == "DIVISION_TABLE_MODEL":
            rows = len(params.get("rows") or [])
            return max(cls.MIN_HEIGHT, 48.0 * (rows + 1) + 28.0)
        if kind in {"MONEY_MODEL", "OBJECT_GROUPS", "QUANTITY_STRUCTURE_MAP"}:
            groups = len(params.get("groups") or params.get("branches") or [])
            return max(cls.MIN_HEIGHT, 170.0 + max(0, groups - 2) * 18.0)
        if kind in {"ANGLE_RAYS_ARC", "ANGLE_BENCHMARK_COMPARE", "ANGLE_OBJECT_EXAMPLE", "GEOMETRIC_ANGLE"}:
            return 190.0
        if kind in {"DIV_LONG_ALGORITHM", "LONG_DIVISION_WORKOUT"}:
            return 215.0
        if kind in {"DIV_MULTIPLES_STRIP", "RATE_SCALE_MODEL", "SAME_RATE_SCALE"}:
            return 185.0
        return 190.0

    @classmethod
    def render(cls, backend: VectorRenderBackend, bbox: BoundingBox, visual: Mapping[str, Any]) -> None:
        required = cls.measure(visual, bbox.width)
        _require(bbox.height + 0.01 >= required, "CORE1_PRIMARY_VISUAL_BOX_TOO_SHORT", f"required={required}, got={bbox.height}")
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
    """Typed learner work surfaces; never degrades to a generic math box."""

    BASE_HEIGHTS = {
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
        _require(kind in cls.BASE_HEIGHTS, "WORK_SURFACE_KIND_NOT_REALIZED", kind or "<missing>")
        _require(width > 0, "WORK_SURFACE_WIDTH_INVALID", str(width))
        _require(isinstance(surface.get("semantic_params"), dict), "WORK_SURFACE_PARAMS_MISSING", kind)
        _require(bool(surface.get("validator_refs")), "UNVALIDATED_WORK_SURFACE", kind)
        params = surface.get("semantic_params") or {}

        if kind in {"LONG_DIVISION_WORK", "SHORT_DIVISION_WORK"}:
            steps = len(params.get("steps") or [])
            return max(cls.BASE_HEIGHTS[kind], 128.0 + 48.0 * max(steps, 1))
        if kind == "DIVISION_TABLE_WORKSPACE":
            rows = len(params.get("rows") or [])
            return max(cls.BASE_HEIGHTS[kind], 48.0 * (rows + 1) + 28.0)
        if kind == "ANGLE_DRAWING_WORKSPACE":
            slots = int(params.get("slots", 1) or 1)
            return max(cls.BASE_HEIGHTS[kind], 155.0 + min(slots, 6) * 6.0)
        if kind == "VERTICAL_MULTIPLICATION_WORK":
            rows = max(2, len(params.get("partial_products") or []))
            return max(cls.BASE_HEIGHTS[kind], 150.0 + rows * 28.0)
        return cls.BASE_HEIGHTS[kind]

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

        for index, step in enumerate(steps):
            for key in ("partial_dividend", "quotient_digit", "product", "subtraction_remainder"):
                _require(key in step, "LONG_DIVISION_WORK_SURFACE_INVALID", f"step {index} missing {key}")
            partial = int(step["partial_dividend"])
            q_digit = int(step["quotient_digit"])
            product = int(step["product"])
            step_rem = int(step["subtraction_remainder"])
            _require(product == divisor * q_digit, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: product mismatch")
            _require(partial - product == step_rem, "PRIMARY_VISUAL_ALGORITHM_INVALID", f"step {index}: subtraction mismatch")

        cls._draw_notebook_grid(backend, bbox)

        # Long-division bracket with blank quotient slots. Answer semantics above
        # validate the surface but are deliberately not rendered into learner work.
        col_w = 25.0
        origin_x = bbox.x + 70.0
        start_y = bbox.y_max - 58.0
        dividend_s = str(dividend)
        backend.draw_text(str(divisor), origin_x - 14.0, start_y, font_size=15.0, color=PrimaryPalette.NAVY, align="right")
        bracket_x = origin_x - 5.0
        backend.draw_line(bracket_x, start_y - 5.0, bracket_x, start_y + 20.0, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
        backend.draw_line(bracket_x, start_y + 20.0, bracket_x + len(dividend_s) * col_w + 16.0, start_y + 20.0, stroke=PrimaryPalette.NAVY, stroke_width=1.6)
        for index, char in enumerate(dividend_s):
            backend.draw_text(char, origin_x + index * col_w + 8.0, start_y, font_size=15.0, color=PrimaryPalette.STUDENT_PENCIL, align="center")

        offset = len(dividend_s) - len(quotient_places)
        for index in range(len(quotient_places)):
            target_col = offset + index
            cx = origin_x + target_col * col_w + 8.0
            backend.draw_line(cx - 8.0, start_y + 30.0, cx + 8.0, start_y + 30.0, stroke=PrimaryPalette.TEAL, stroke_width=1.1)

        ledger_x = bbox.x + bbox.width * 0.53
        ledger_y = bbox.y_max - 34.0
        backend.draw_text("Divide -> Multiply -> Subtract -> Bring down", ledger_x, ledger_y, font_size=10.5, color=PrimaryPalette.TEAL)
        ledger_y -= 28.0
        step_count = max(len(steps), len(quotient_places), 1)
        for index in range(step_count):
            backend.draw_text(f"Step {index + 1}", ledger_x, ledger_y, font_size=10.5, color=PrimaryPalette.SLATE)
            backend.draw_line(ledger_x + 58.0, ledger_y - 1.0, bbox.x_max - 18.0, ledger_y - 1.0, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0)
            ledger_y -= 28.0
            backend.draw_text("Multiply / subtract", ledger_x + 12.0, ledger_y, font_size=9.5, color=PrimaryPalette.SLATE)
            backend.draw_line(ledger_x + 112.0, ledger_y - 1.0, bbox.x_max - 18.0, ledger_y - 1.0, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0)
            ledger_y -= 30.0

        backend.draw_text("Check: divisor x quotient + remainder = dividend", bbox.x + bbox.width * 0.53, bbox.y + 18.0, font_size=10.5, color=PrimaryPalette.NAVY)

    @classmethod
    def _render_vertical_multiplication_workspace(
        cls,
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Mapping[str, Any],
    ) -> None:
        factors = [int(x) for x in (params.get("factors") or [])]
        _require(len(factors) >= 2, "VERTICAL_MULTIPLICATION_WORK_INVALID", "at least two factors required")
        cls._draw_notebook_grid(backend, bbox)
        right = bbox.x + bbox.width * 0.48
        y = bbox.y_max - 48.0
        backend.draw_text(str(factors[0]), right, y, font_size=16.0, color=PrimaryPalette.STUDENT_PENCIL, align="right")
        y -= 25.0
        backend.draw_text(f"x {factors[1]}", right, y, font_size=16.0, color=PrimaryPalette.STUDENT_PENCIL, align="right")
        backend.draw_line(right - 90.0, y - 8.0, right + 4.0, y - 8.0, stroke=PrimaryPalette.NAVY, stroke_width=1.3)
        rows = max(2, len(params.get("partial_products") or []))
        for _ in range(rows):
            y -= 34.0
            backend.draw_line(right - 90.0, y, right + 4.0, y, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0)
        y -= 28.0
        backend.draw_line(right - 90.0, y, right + 4.0, y, stroke=PrimaryPalette.NAVY, stroke_width=1.2)
        backend.draw_text("partial products", bbox.x + bbox.width * 0.62, bbox.y_max - 58.0, font_size=10.5, color=PrimaryPalette.TEAL)
        backend.draw_text("align place values, then add", bbox.x + bbox.width * 0.62, bbox.y_max - 82.0, font_size=10.5, color=PrimaryPalette.SLATE)

    @classmethod
    def render(cls, backend: VectorRenderBackend, bbox: BoundingBox, surface: Mapping[str, Any]) -> None:
        required = cls.measure(surface, bbox.width)
        _require(bbox.height + 0.01 >= required, "WORK_SURFACE_BOX_TOO_SHORT", f"required={required}, got={bbox.height}")
        kind = str(surface["kind"])
        params = dict(surface.get("semantic_params") or {})

        if kind in {"LONG_DIVISION_WORK", "SHORT_DIVISION_WORK"}:
            cls._render_long_division_semantic(backend, bbox, params)
            return

        if kind == "DIVISION_TABLE_WORKSPACE":
            _require(bool(params.get("columns")) and bool(params.get("rows")), "DIVISION_TABLE_WORKSPACE_INVALID", "columns and rows required")
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
                vx = x + slot_w * 0.28
                vy = bbox.y + bbox.height * 0.40
                backend.draw_circle(vx, vy, 2.2, fill=PrimaryPalette.SLATE, stroke=PrimaryPalette.SLATE, stroke_width=0.8)
            return

        if kind == "VERTICAL_MULTIPLICATION_WORK":
            required_fields = {"factors", "partial_products", "total_product"}
            _require(required_fields.issubset(params), "VERTICAL_MULTIPLICATION_WORK_INVALID", f"missing {sorted(required_fields - set(params))}")
            cls._render_vertical_multiplication_workspace(backend, bbox, params)
            return

        if kind == "MULTIPLICATION_PARTIAL_PRODUCTS_WORK":
            cls._draw_notebook_grid(backend, bbox)
            backend.draw_text("Break apart by place value", bbox.x + 18.0, bbox.y_max - 28.0, font_size=11.0, color=PrimaryPalette.TEAL)
            backend.draw_line(bbox.x + 18.0, bbox.y + bbox.height * 0.52, bbox.x_max - 18.0, bbox.y + bbox.height * 0.52, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0)
            backend.draw_line(bbox.x + 18.0, bbox.y + bbox.height * 0.28, bbox.x_max - 18.0, bbox.y + bbox.height * 0.28, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0)
            return

        if kind == "UNIT_CHAIN_WORK":
            cls._draw_notebook_grid(backend, bbox)
            backend.draw_text("Write each unit conversion as one step", bbox.x + 18.0, bbox.y_max - 28.0, font_size=11.0, color=PrimaryPalette.TEAL)
            return

        raise Core1ComponentError("WORK_SURFACE_KIND_NOT_REALIZED", kind)
