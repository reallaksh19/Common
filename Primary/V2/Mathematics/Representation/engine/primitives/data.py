"""
Data Visual Primitives for Primary Mathematics V2.
Bar charts with reconciled scale units and key values.
"""
from __future__ import annotations

from typing import Any, Dict, List
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class DataPrimitives:
    """Scaled bar charts and pictograms."""

    @staticmethod
    def draw_scaled_bar_chart(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        categories = params.get("categories", ["Apples", "Bananas", "Oranges"])
        values = params.get("values", [15, 25, 10])
        scale_unit = params.get("scale_unit", 5)

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(scale_unit)] + [str(v) for v in values] + categories
        title = f"Bar Chart (1 grid line = {scale_unit} items)"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)
        labels.append(title)

        # Chart axes
        ax_x = bbox.x + 45.0
        ax_y = bbox.y + 35.0
        chart_w = bbox.width - 65.0
        chart_h = bbox.height - 70.0

        backend.draw_line(ax_x, ax_y, ax_x + chart_w, ax_y, stroke=PrimaryPalette.NAVY, stroke_width=1.5)
        backend.draw_line(ax_x, ax_y, ax_x, ax_y + chart_h, stroke=PrimaryPalette.NAVY, stroke_width=1.5)

        # Scale lines
        max_val = max(values) if values else 25
        max_steps = int(max_val / scale_unit) + 1
        for s in range(max_steps + 1):
            sy = ax_y + (s / max_steps) * chart_h
            val_lbl = str(s * scale_unit)
            backend.draw_line(ax_x - 4.0, sy, ax_x + chart_w, sy, stroke=PrimaryPalette.GRID_LINE, stroke_width=0.8)
            backend.draw_text(val_lbl, ax_x - 8.0, sy - 4.0, font_size=10.0, color=PrimaryPalette.SLATE, align="right")
            labels.append(val_lbl)

        # Bars
        bar_count = len(categories)
        bar_slot = chart_w / max(bar_count, 1)
        bar_w = bar_slot * 0.55

        for idx, (cat, val) in enumerate(zip(categories, values)):
            bx = ax_x + idx * bar_slot + (bar_slot - bar_w) / 2.0
            bh = (val / (max_steps * scale_unit)) * chart_h
            fill_c = PrimaryPalette.TEAL if idx % 2 == 0 else PrimaryPalette.AMBER
            backend.draw_rect(bx, ax_y, bar_w, bh, fill=fill_c, stroke=PrimaryPalette.NAVY, stroke_width=1.0)
            # Value above bar
            backend.draw_text(str(val), bx + bar_w / 2.0, ax_y + bh + 4.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")
            # Category label below
            backend.draw_text(cat, bx + bar_w / 2.0, ax_y - 14.0, font_size=11.0, color=PrimaryPalette.NAVY, align="center")

        backend.record_evidence("DATA_BAR_CHART", params, len(labels) + bar_count, labels)
