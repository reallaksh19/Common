"""Cardinality-faithful Primary Math array primitive.

Unlike a labeled rectangle, this renderer realizes every row/column intersection
so the learner can actually see rows × columns = total.
"""
from __future__ import annotations

from typing import Any, Dict

from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, PrimaryPalette, VectorRenderBackend


class RealizedArrayPrimitive:
    @staticmethod
    def draw(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        rows = int(params.get("rows", 0))
        cols = int(params.get("cols", 0))
        if rows <= 0 or cols <= 0:
            raise ValueError("ARRAY requires positive rows and cols")
        total = rows * cols
        if total > 400:
            raise ValueError("ARRAY cardinality too large for discrete Primary rendering")

        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        title = f"Array: {rows} rows × {cols} columns = {total}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.0, color=PrimaryPalette.NAVY)

        left = bbox.x + 32.0
        right = bbox.x_max - 20.0
        bottom = bbox.y + 18.0
        top = bbox.y_max - 42.0
        cell_w = (right - left) / cols
        cell_h = (top - bottom) / rows
        radius = max(1.6, min(4.0, cell_w * 0.28, cell_h * 0.28))

        for r in range(rows):
            y = top - (r + 0.5) * cell_h
            for c in range(cols):
                x = left + (c + 0.5) * cell_w
                backend.draw_circle(x, y, radius, fill=PrimaryPalette.ACCENT_BLUE, stroke=PrimaryPalette.ACCENT_BLUE, stroke_width=0.4)

        backend.draw_text(str(rows), left - 12.0, (top + bottom) / 2.0 - 4.0, font_size=11.5, color=PrimaryPalette.NAVY, align="right")
        backend.draw_text(str(cols), (left + right) / 2.0, top + 7.0, font_size=11.5, color=PrimaryPalette.NAVY, align="center")
        backend.draw_text(f"{rows} × {cols} = {total}", (left + right) / 2.0, bottom - 13.0, font_size=11.0, color=PrimaryPalette.TEAL, align="center")
        backend.record_evidence("ARRAY", params, total + 4, [title, str(rows), str(cols), str(total)])
