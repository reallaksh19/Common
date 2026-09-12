"""
Place Value Visual Primitives for Primary Mathematics V2.
Base-10 positional decomposition blocks and standard expanded form.
"""
from __future__ import annotations

from typing import Any, Dict, List
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class NumberPrimitives:
    """Place value blocks and expanded form representation."""

    @staticmethod
    def draw_place_value(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        number = params.get("number", 4567)
        expanded = params.get("expanded", [4000, 500, 60, 7])

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(number)]
        title = f"Place Value Decomposition of {number}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)
        labels.append(title)

        # Draw place value columns: Thousands, Hundreds, Tens, Ones
        col_count = len(expanded)
        col_w = (bbox.width - 30.0) / col_count
        headers = ["Thousands", "Hundreds", "Tens", "Ones"][-col_count:]

        cy = bbox.y + (bbox.height - 50.0) / 2.0
        for idx, val in enumerate(expanded):
            cx = bbox.x + 15.0 + idx * col_w
            backend.draw_rect(
                cx + 4.0, cy - 20.0, col_w - 8.0, 48.0,
                fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.ACCENT_BLUE, stroke_width=1.0, corner_radius=4.0
            )
            backend.draw_text(headers[idx], cx + col_w / 2.0, cy + 16.0, font_size=10.0, color=PrimaryPalette.SLATE, align="center")
            backend.draw_text(str(val), cx + col_w / 2.0, cy - 8.0, font_size=13.5, color=PrimaryPalette.NAVY, align="center")
            labels.extend([headers[idx], str(val)])

        # Equation at bottom: 4000 + 500 + 60 + 7 = 4567
        eq_str = " + ".join(str(v) for v in expanded) + f" = {number}"
        backend.draw_text(eq_str, bbox.x + bbox.width / 2.0, bbox.y + 12.0, font_size=12.0, color=PrimaryPalette.AMBER, align="center")
        labels.append(eq_str)

        backend.record_evidence("PLACE_VALUE_BLOCKS", params, len(labels) + col_count, labels)
