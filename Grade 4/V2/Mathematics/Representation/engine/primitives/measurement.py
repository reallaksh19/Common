"""
Measurement Visual Primitives for Primary Mathematics V2.
Unit conversions and metric/customary equivalence scales.
"""
from __future__ import annotations

from typing import Any, Dict, List
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class MeasurementPrimitives:
    """Unit conversions and double number line models."""

    @staticmethod
    def draw_conversion(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        from_val = params.get("from_value", 3)
        from_unit = params.get("from_unit", "KILOMETRE")
        factor = params.get("factor", 1000)
        to_val = params.get("to_value", from_val * factor)
        to_unit = params.get("to_unit", "METRE")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(from_val), from_unit, str(to_val), to_unit, str(factor)]
        title = f"Unit Conversion: {from_val} {from_unit.lower()} = {to_val} {to_unit.lower()}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)
        labels.append(title)

        # Draw two conversion cards connected by multiplier arrow
        card_w = (bbox.width - 120.0) / 2.0
        card_h = 44.0
        cy = bbox.y + (bbox.height - card_h - 20.0) / 2.0

        # Left: source unit
        lx = bbox.x + 30.0
        backend.draw_rect(lx, cy, card_w, card_h, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.TEAL, stroke_width=1.2, corner_radius=4.0)
        backend.draw_text(f"{from_val} {from_unit.lower()}", lx + card_w / 2.0, cy + card_h / 2.0 - 5.0, font_size=13.0, color=PrimaryPalette.NAVY, align="center")

        # Right: target unit
        rx = bbox.x_max - 30.0 - card_w
        backend.draw_rect(rx, cy, card_w, card_h, fill=PrimaryPalette.HIGHLIGHT_YELLOW, stroke=PrimaryPalette.AMBER, stroke_width=1.2, corner_radius=4.0)
        backend.draw_text(f"{to_val} {to_unit.lower()}", rx + card_w / 2.0, cy + card_h / 2.0 - 5.0, font_size=13.0, color=PrimaryPalette.NAVY, align="center")

        # Arrow
        arrow_start_x = lx + card_w + 10.0
        arrow_end_x = rx - 10.0
        arrow_y = cy + card_h / 2.0
        backend.draw_arrow(arrow_start_x, arrow_y, arrow_end_x, arrow_y, stroke=PrimaryPalette.AMBER, stroke_width=2.0)
        backend.draw_text(f"x {factor}", (arrow_start_x + arrow_end_x) / 2.0, arrow_y + 8.0, font_size=11.0, color=PrimaryPalette.AMBER, align="center")

        backend.record_evidence("MEASUREMENT_CONVERSION", params, len(labels) + 4, labels)
