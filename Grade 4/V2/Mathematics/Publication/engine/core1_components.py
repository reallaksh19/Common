"""Measured Core1 components driven only by LearningRepresentationPlan.

These components do not select pedagogy. They realize an already validated
primary visual and typed work surface. Unsupported semantic kinds fail closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping

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
    def render(cls, backend: VectorRenderBackend, bbox: BoundingBox, surface: Mapping[str, Any]) -> None:
        cls.measure(surface, bbox.width)
        kind = str(surface["kind"])
        params = dict(surface.get("semantic_params") or {})

        if kind in {"LONG_DIVISION_WORK", "SHORT_DIVISION_WORK"}:
            required = {"dividend", "divisor", "quotient", "remainder"}
            _require(required.issubset(params), "LONG_DIVISION_WORK_SURFACE_INVALID", f"missing {sorted(required - set(params))}")
            call = {
                "dividend": params["dividend"],
                "divisor": params["divisor"],
                "quotient": params["quotient"],
                "remainder": params["remainder"],
                "quotient_digits": [str(x) for x in params.get("quotient_places", list(str(params["quotient"])))],
                "steps": list(params.get("steps") or []),
                "provenance_tier": surface.get("provenance", "STRUCTURED_REPLAY"),
                "actor": "CHILD",
                "claims_original_handwriting": False,
            }
            render_primitive("LONG_DIVISION_WORKOUT", call, backend, bbox)
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
