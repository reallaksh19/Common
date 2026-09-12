"""
Decimals Visual Primitives for Primary Mathematics V2.
Enforces 10x10 hundred-grid precision and calibrated number line accuracy.
"""
from __future__ import annotations

from typing import Any, Dict, List
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class DecimalPrimitives:
    """Hundred-grid and decimal number line primitives."""

    @staticmethod
    def draw_hundred_grid(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Draws 10x10 hundredths grid with shaded squares = round(decimal_value * 100)."""
        val = params.get("decimal_value", 0.45)
        shaded = params.get("grid_shaded_cells", round(val * 100))

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(val), str(shaded), f"{val} = {shaded}/100"]
        backend.draw_text(
            f"Decimal Hundred-Grid: {labels[2]}",
            bbox.x + 12.0, bbox.y_max - 20.0,
            font_size=12.5, color=PrimaryPalette.NAVY
        )

        grid_dim = min(bbox.width - 40.0, bbox.height - 45.0)
        cell_size = grid_dim / 10.0
        gx = bbox.x + (bbox.width - grid_dim) / 2.0
        gy = bbox.y + 12.0

        for row in range(10):
            for col in range(10):
                cell_idx = row * 10 + col
                cx = gx + col * cell_size
                cy = gy + (9 - row) * cell_size  # Start filling from bottom or top consistently
                is_shaded = (cell_idx < shaded)
                fill_col = PrimaryPalette.TEAL if is_shaded else PrimaryPalette.LIGHT_BG
                backend.draw_rect(
                    cx, cy, cell_size, cell_size,
                    fill=fill_col, stroke=PrimaryPalette.GRID_LINE, stroke_width=0.5
                )

        # Outer border
        backend.draw_rect(gx, gy, grid_dim, grid_dim, fill=None, stroke=PrimaryPalette.NAVY, stroke_width=1.5)

        backend.record_evidence("DECIMAL_HUNDRED_GRID", params, len(labels) + 100, labels)

    @staticmethod
    def draw_decimal_number_line(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Calibrated decimal number line with target marker."""
        min_v = params.get("min_val", 0.0)
        max_v = params.get("max_val", 1.0)
        target = params.get("target_val", 0.45)

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(min_v), str(max_v), str(target)]
        title = f"Number Line: Plotting {target} between {min_v} and {max_v}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.NAVY)
        labels.append(title)

        line_y = bbox.y + bbox.height / 2.0 - 5.0
        line_start_x = bbox.x + 30.0
        line_end_x = bbox.x_max - 30.0
        line_len = line_end_x - line_start_x

        # Main axis
        backend.draw_line(line_start_x, line_y, line_end_x, line_y, stroke=PrimaryPalette.NAVY, stroke_width=1.5)

        # Ticks (tenths)
        for i in range(11):
            tick_val = min_v + (max_v - min_v) * (i / 10.0)
            tx = line_start_x + (i / 10.0) * line_len
            backend.draw_line(tx, line_y - 6.0, tx, line_y + 6.0, stroke=PrimaryPalette.SLATE, stroke_width=1.0)
            tick_lbl = f"{tick_val:.1f}"
            backend.draw_text(tick_lbl, tx, line_y - 18.0, font_size=10.0, color=PrimaryPalette.SLATE, align="center")
            labels.append(tick_lbl)

        # Plot target
        if max_v > min_v:
            ratio = (target - min_v) / (max_v - min_v)
            px = line_start_x + ratio * line_len
            backend.draw_circle(px, line_y, 4.5, fill=PrimaryPalette.AMBER, stroke=PrimaryPalette.NAVY, stroke_width=1.2)
            backend.draw_text(str(target), px, line_y + 12.0, font_size=12.0, color=PrimaryPalette.AMBER, align="center")

        backend.record_evidence("DECIMAL_NUMBER_LINE", params, len(labels) + 12, labels)
