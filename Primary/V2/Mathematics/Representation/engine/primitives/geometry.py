"""
Geometry Visual Primitives for Primary Mathematics V2.
Perimeter vs area non-conflation, volume unit cube layers, and angles.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class GeometryPrimitives:
    """Perimeter, area, volume layers, and angle primitives."""

    @staticmethod
    def draw_perimeter_area(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Contrasts perimeter (boundary line) and area (surface covering)."""
        w = params.get("width", 5)
        h = params.get("height", 3)
        p = params.get("perimeter", 2 * (w + h))
        a = params.get("area", w * h)
        u = params.get("unit", "cm")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(w), str(h), str(p), str(a), u, f"Perimeter = {p} {u}", f"Area = {a} {u}^2"]
        backend.draw_text(
            f"Perimeter vs Area: {w}{u} by {h}{u} Rectangle",
            bbox.x + 12.0, bbox.y_max - 20.0,
            font_size=12.5, color=PrimaryPalette.NAVY
        )
        labels.append(f"Perimeter vs Area: {w}{u} by {h}{u} Rectangle")

        # Draw central rectangle
        scale = min((bbox.width - 120.0) / w, (bbox.height - 80.0) / h)
        rw = w * scale
        rh = h * scale
        rx = bbox.x + 40.0
        ry = bbox.y + 25.0

        # Shaded area
        backend.draw_rect(rx, ry, rw, rh, fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.NAVY, stroke_width=2.0)
        # Inside area label
        backend.draw_text(f"Area = {a} {u}^2", rx + rw / 2.0, ry + rh / 2.0 - 5.0, font_size=12.0, color=PrimaryPalette.TEAL, align="center")

        # Perimeter dimension labels around boundary
        backend.draw_text(f"{w} {u}", rx + rw / 2.0, ry + rh + 4.0, font_size=11.5, color=PrimaryPalette.NAVY, align="center")
        backend.draw_text(f"{h} {u}", rx - 8.0, ry + rh / 2.0 - 4.0, font_size=11.5, color=PrimaryPalette.NAVY, align="right")

        # Right side summary card
        card_x = rx + rw + 25.0
        backend.draw_text(labels[5], card_x, ry + rh - 10.0, font_size=12.0, color=PrimaryPalette.AMBER)
        backend.draw_text(labels[6], card_x, ry + rh - 30.0, font_size=12.0, color=PrimaryPalette.TEAL)

        backend.record_evidence("RECTILINEAR_PERIMETER_AREA", params, len(labels) + 4, labels)

    @staticmethod
    def draw_volume_layers(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Renders rectangular prism volume as layer stack of unit cubes."""
        l = params.get("length", 4)
        w = params.get("width", 3)
        h = params.get("height", 2)
        cubes_per_layer = l * w
        total_cubes = cubes_per_layer * h

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(l), str(w), str(h), str(cubes_per_layer), str(total_cubes)]
        title = f"Volume by Layers: {l} x {w} x {h} = {total_cubes} unit cubes"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)
        labels.append(title)

        # Layer description
        layer_desc = f"{h} layers of {cubes_per_layer} cubes = {total_cubes} total"
        backend.draw_text(layer_desc, bbox.x + 12.0, bbox.y_max - 40.0, font_size=11.5, color=PrimaryPalette.TEAL)
        labels.append(layer_desc)

        # Draw layer isometric blocks
        ox = bbox.x + 60.0
        oy = bbox.y + 25.0
        cell_w = 20.0
        cell_h = 14.0

        for layer in range(h):
            ly = oy + layer * 24.0
            for r in range(w):
                for c in range(l):
                    px = ox + c * cell_w + r * 10.0
                    py = ly + r * 6.0
                    backend.draw_rect(px, py, cell_w - 2.0, cell_h - 2.0, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.NAVY, stroke_width=0.8)

        backend.record_evidence("VOLUME_CUBE_LAYERS", params, len(labels) + total_cubes, labels)

    @staticmethod
    def draw_angle(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Renders geometric angle with ray arrows and vertex arc."""
        deg = params.get("angle_degrees", 120)
        cls = params.get("classification", "OBTUSE")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(deg), cls, f"{deg} degrees ({cls})"]
        backend.draw_text(
            f"Angle: {labels[2]}",
            bbox.x + 12.0, bbox.y_max - 20.0,
            font_size=12.5, color=PrimaryPalette.NAVY
        )
        labels.append(f"Angle: {labels[2]}")

        vx = bbox.x + 60.0
        vy = bbox.y + 35.0
        ray_len = min(bbox.width - 120.0, bbox.height - 70.0)

        # Base horizontal ray
        backend.draw_arrow(vx, vy, vx + ray_len, vy, stroke=PrimaryPalette.NAVY, stroke_width=2.0)

        # Angled ray
        rad = math.radians(deg)
        ax = vx + ray_len * math.cos(rad)
        ay = vy + ray_len * math.sin(rad)
        backend.draw_arrow(vx, vy, ax, ay, stroke=PrimaryPalette.NAVY, stroke_width=2.0)

        # Arc
        arc_r = 25.0
        arc_pts = [(vx + arc_r * math.cos(math.radians(a)), vy + arc_r * math.sin(math.radians(a))) for a in range(0, int(deg) + 1, 10)]
        for i in range(len(arc_pts) - 1):
            backend.draw_line(arc_pts[i][0], arc_pts[i][1], arc_pts[i+1][0], arc_pts[i+1][1], stroke=PrimaryPalette.AMBER, stroke_width=1.5)

        # Angle degree label
        mid_rad = math.radians(deg / 2.0)
        backend.draw_text(f"{deg}°", vx + (arc_r + 14.0) * math.cos(mid_rad), vy + (arc_r + 14.0) * math.sin(mid_rad), font_size=12.0, color=PrimaryPalette.AMBER)

        backend.record_evidence("GEOMETRIC_ANGLE", params, len(labels) + 5, labels)
