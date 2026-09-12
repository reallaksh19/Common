"""
Fractions Visual Primitives for Primary Mathematics V2.
Enforces equal partition geometry, shaded fraction consistency, and grounded comparisons.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PrimaryPalette,
    VectorRenderBackend
)


class FractionPrimitives:
    """Equal partition strips, comparisons, and addition models."""

    @staticmethod
    def draw_fraction_strip(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Renders an equal-partition fraction strip with shaded numerator parts."""
        num = params.get("numerator", 3)
        den = params.get("denominator", 4)
        label = params.get("label", f"{num}/{den}")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [str(num), str(den), label]
        backend.draw_text(
            f"Fraction Strip: {label}",
            bbox.x + 12.0, bbox.y_max - 20.0,
            font_size=12.5, color=PrimaryPalette.NAVY
        )

        strip_w = bbox.width - 40.0
        strip_h = 36.0
        sx = bbox.x + 20.0
        sy = bbox.y + (bbox.height - strip_h - 20.0) / 2.0

        part_w = strip_w / den

        for p in range(den):
            px = sx + p * part_w
            is_shaded = (p < num)
            fill_col = PrimaryPalette.ACCENT_BLUE if is_shaded else PrimaryPalette.LIGHT_BG

            backend.draw_rect(
                px, sy, part_w, strip_h,
                fill=fill_col, stroke=PrimaryPalette.NAVY, stroke_width=1.2
            )

            # Part label (e.g. 1/4)
            unit_frac = f"1/{den}"
            text_col = PrimaryPalette.WHITE if is_shaded else PrimaryPalette.SLATE
            backend.draw_text(
                unit_frac, px + part_w / 2.0, sy + strip_h / 2.0 - 4.0,
                font_size=11.0, color=text_col, align="center"
            )
            labels.append(unit_frac)

        backend.record_evidence("FRACTION_STRIP", params, len(labels) + den, labels)

    @staticmethod
    def draw_fraction_comparison(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """
        Renders two vertically aligned fraction strips with common benchmark line.
        e.g. 3/4 vs 2/3.
        """
        f1 = params.get("fraction_1", {"numerator": 3, "denominator": 4})
        f2 = params.get("fraction_2", {"numerator": 2, "denominator": 3})
        relation = params.get("relation", ">")

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [
            f"{f1['numerator']}/{f1['denominator']}",
            f"{f2['numerator']}/{f2['denominator']}",
            relation
        ]
        title = f"Comparing {labels[0]} {relation} {labels[1]}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=12.5, color=PrimaryPalette.NAVY)
        labels.append(title)

        strip_w = bbox.width - 120.0
        strip_h = 28.0
        sx = bbox.x + 90.0

        # Strip 1
        sy1 = bbox.y_max - 58.0
        backend.draw_text(f"{f1['numerator']}/{f1['denominator']}", sx - 15.0, sy1 + 8.0, font_size=13.0, color=PrimaryPalette.NAVY, align="right")
        p1_w = strip_w / f1["denominator"]
        for p in range(f1["denominator"]):
            px = sx + p * p1_w
            fill_col = PrimaryPalette.ACCENT_BLUE if p < f1["numerator"] else PrimaryPalette.WHITE
            backend.draw_rect(px, sy1, p1_w, strip_h, fill=fill_col, stroke=PrimaryPalette.NAVY, stroke_width=1.0)

        # Strip 2
        sy2 = sy1 - 38.0
        backend.draw_text(f"{f2['numerator']}/{f2['denominator']}", sx - 15.0, sy2 + 8.0, font_size=13.0, color=PrimaryPalette.NAVY, align="right")
        p2_w = strip_w / f2["denominator"]
        for p in range(f2["denominator"]):
            px = sx + p * p2_w
            fill_col = PrimaryPalette.AMBER if p < f2["numerator"] else PrimaryPalette.WHITE
            backend.draw_rect(px, sy2, p2_w, strip_h, fill=fill_col, stroke=PrimaryPalette.NAVY, stroke_width=1.0)

        backend.record_evidence("FRACTION_COMPARISON", params, len(labels) + 6, labels)

    @staticmethod
    def draw_fraction_addition(
        backend: VectorRenderBackend,
        bbox: BoundingBox,
        params: Dict[str, Any]
    ) -> None:
        """Visual representation of fraction addition (like or repartitioned)."""
        num1 = params.get("num1", 1)
        den1 = params.get("den1", 4)
        num2 = params.get("num2", 2)
        den2 = params.get("den2", 4)
        res_num = params.get("res_num", 3)
        res_den = params.get("res_den", 4)

        backend.draw_rect(
            bbox.x, bbox.y, bbox.width, bbox.height,
            fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )

        labels = [f"{num1}/{den1}", f"{num2}/{den2}", f"{res_num}/{res_den}"]
        title = f"{num1}/{den1} + {num2}/{den2} = {res_num}/{res_den}"
        backend.draw_text(title, bbox.x + 12.0, bbox.y_max - 20.0, font_size=13.0, color=PrimaryPalette.NAVY)
        labels.append(title)

        strip_w = bbox.width - 40.0
        strip_h = 32.0
        sx = bbox.x + 20.0
        sy = bbox.y + (bbox.height - strip_h - 20.0) / 2.0

        part_w = strip_w / res_den
        for p in range(res_den):
            px = sx + p * part_w
            if p < num1:
                fill_col = PrimaryPalette.ACCENT_BLUE
            elif p < (num1 + num2):
                fill_col = PrimaryPalette.AMBER
            else:
                fill_col = PrimaryPalette.LIGHT_BG
            backend.draw_rect(px, sy, part_w, strip_h, fill=fill_col, stroke=PrimaryPalette.NAVY, stroke_width=1.0)

        backend.record_evidence("FRACTION_ADDITION", params, len(labels) + res_den, labels)
