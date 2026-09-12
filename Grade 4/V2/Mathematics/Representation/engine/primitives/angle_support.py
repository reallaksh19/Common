"""Grade-4 angle classification visual sets.

A classification-set visual is different from a single benchmark comparison: it
must expose several geometrically distinct openings at once so a learner can
actually perform a match/classification task. Names are deliberately omitted.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List

from Grade4.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend,
)


class AngleSupportPrimitives:
    @staticmethod
    def _draw_sweep(
        backend: VectorRenderBackend,
        cx: float,
        cy: float,
        radius: float,
        degrees: float,
        stroke: str,
    ) -> int:
        sweep = max(1.0, min(float(degrees), 350.0))
        segments = max(5, int(sweep / 18.0))
        points = []
        for index in range(segments + 1):
            theta = math.radians(sweep * index / segments)
            points.append((cx + radius * math.cos(theta), cy + radius * math.sin(theta)))
        for p1, p2 in zip(points, points[1:]):
            backend.draw_line(p1[0], p1[1], p2[0], p2[1], stroke=stroke, stroke_width=1.1)
        if len(points) >= 2:
            p1, p2 = points[-2], points[-1]
            backend.draw_arrow(p1[0], p1[1], p2[0], p2[1], stroke=stroke, stroke_width=1.1, arrowhead_size=4.0)
        return segments + 1

    @staticmethod
    def draw_classification_set(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any],
    ) -> None:
        degrees: List[float] = [float(x) for x in (params.get("degrees") or [45, 90, 120, 180, 240])]
        if len(degrees) < 3 or len(degrees) > 6:
            raise ValueError("ANGLE_CLASSIFICATION_SET requires 3..6 angle values")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE,
            stroke=PrimaryPalette.CARD_BORDER,
            stroke_width=1.0,
            corner_radius=6.0,
        )

        cols = 3
        rows = int(math.ceil(len(degrees) / cols))
        gap = 10.0
        panel_w = (bbox.width - gap * (cols + 1)) / cols
        panel_h = (bbox.height - gap * (rows + 1)) / rows
        labels: List[str] = []
        element_count = 1

        for index, deg in enumerate(degrees):
            row = index // cols
            col = index % cols
            x = bbox.x + gap + col * (panel_w + gap)
            y = bbox.y_max - gap - (row + 1) * panel_h - row * gap
            panel = BoundingBox(x, y, panel_w, panel_h)
            backend.draw_rect(panel.x, panel.y, panel.width, panel.height, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.GRID_LINE, corner_radius=4.0)

            vx = panel.x + panel.width * 0.40
            vy = panel.y + panel.height * 0.37
            ray_len = min(panel.width * 0.34, panel.height * 0.28)
            backend.draw_arrow(vx, vy, vx + ray_len, vy, stroke=PrimaryPalette.ACCENT_BLUE, stroke_width=1.7, arrowhead_size=4.5)
            theta = math.radians(deg)
            backend.draw_arrow(vx, vy, vx + ray_len * math.cos(theta), vy + ray_len * math.sin(theta), stroke=PrimaryPalette.ACCENT_BLUE, stroke_width=1.7, arrowhead_size=4.5)
            backend.draw_circle(vx, vy, 2.4, fill=PrimaryPalette.ACCENT_BLUE, stroke=PrimaryPalette.ACCENT_BLUE)
            element_count += 4

            sweep_radius = max(11.0, ray_len * 0.38)
            element_count += AngleSupportPrimitives._draw_sweep(backend, vx, vy, sweep_radius, deg, PrimaryPalette.AMBER)

            label = chr(ord("A") + index)
            backend.draw_text(label, panel.x + 12.0, panel.y_max - 18.0, font_size=12.0, color=PrimaryPalette.NAVY)
            labels.append(label)
            element_count += 1

        backend.record_evidence("ANGLE_CLASSIFICATION_SET", params, element_count, labels)
