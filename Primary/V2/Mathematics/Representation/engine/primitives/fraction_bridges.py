"""Primary Math V2 fraction bridge primitives needed by exact acceptance cases."""
from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Any, Dict

from Primary.V2.Mathematics.Representation.engine.base import BoundingBox, PrimaryPalette, VectorRenderBackend


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


class FractionBridgePrimitives:
    @staticmethod
    def draw_fraction_number_line(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        fractions = params.get("fractions") or []
        if not fractions:
            raise ValueError("FRACTION_NUMBER_LINE requires fractions")
        denominators = [int(pair[1]) for pair in fractions]
        common_den = 1
        for den in denominators:
            if den <= 0:
                raise ValueError("fraction denominator must be positive")
            common_den = _lcm(common_den, den)
        if common_den > 48:
            raise ValueError("fraction number-line denominator too large for Primary rendering")

        values = [Fraction(int(n), int(d)) for n, d in fractions]
        if any(v < 0 or v > 1 for v in values):
            raise ValueError("fraction number-line fixture expects values between 0 and 1")

        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        backend.draw_text("Same value on a number line", bbox.x + 12, bbox.y_max - 20, font_size=12.5, color=PrimaryPalette.NAVY)
        x0 = bbox.x + 35
        x1 = bbox.x_max - 35
        y = bbox.y + bbox.height * 0.48
        backend.draw_line(x0, y, x1, y, stroke=PrimaryPalette.NAVY, stroke_width=1.5)
        labels = ["0", "1"]
        backend.draw_text("0", x0, y - 18, font_size=10.5, color=PrimaryPalette.SLATE, align="center")
        backend.draw_text("1", x1, y - 18, font_size=10.5, color=PrimaryPalette.SLATE, align="center")
        for i in range(common_den + 1):
            x = x0 + (x1 - x0) * (i / common_den)
            backend.draw_line(x, y - 5, x, y + 5, stroke=PrimaryPalette.SLATE, stroke_width=0.8)

        grouped: Dict[Fraction, list[str]] = {}
        for (n, d), value in zip(fractions, values):
            grouped.setdefault(value, []).append(f"{n}/{d}")
        for value, names in grouped.items():
            x = x0 + (x1 - x0) * float(value)
            backend.draw_circle(x, y, 4.5, fill=PrimaryPalette.ACCENT_BLUE, stroke=PrimaryPalette.NAVY)
            label = " = ".join(names)
            backend.draw_text(label, x, y + 15, font_size=10.5, color=PrimaryPalette.NAVY, align="center")
            labels.append(label)

        backend.record_evidence("FRACTION_NUMBER_LINE", params, len(labels) + common_den + 2, labels)

    @staticmethod
    def draw_fraction_addition_repartition(backend: VectorRenderBackend, bbox: BoundingBox, params: Dict[str, Any]) -> None:
        left = params.get("left") or [1, 2]
        right = params.get("right") or [1, 4]
        result = params.get("result") or [3, 4]
        l = Fraction(int(left[0]), int(left[1]))
        r = Fraction(int(right[0]), int(right[1]))
        res = Fraction(int(result[0]), int(result[1]))
        if l + r != res:
            raise ValueError("fraction addition relation is invalid")
        common_den = _lcm(l.denominator, r.denominator)
        left_common = l.numerator * (common_den // l.denominator)
        right_common = r.numerator * (common_den // r.denominator)
        result_common = res.numerator * (common_den // res.denominator)
        if left_common + right_common != result_common:
            raise ValueError("repartitioned fraction addition does not close")

        backend.draw_rect(bbox.x, bbox.y, bbox.width, bbox.height, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0)
        equation = f"{left[0]}/{left[1]} = {left_common}/{common_den};  {left_common}/{common_den} + {right_common}/{common_den} = {result_common}/{common_den}"
        backend.draw_text("Repartition to same-size parts", bbox.x + 12, bbox.y_max - 20, font_size=12.5, color=PrimaryPalette.NAVY)
        backend.draw_text(equation, bbox.x + 12, bbox.y_max - 42, font_size=11.5, color=PrimaryPalette.SLATE)

        sx = bbox.x + 25
        sy = bbox.y + 30
        strip_w = bbox.width - 50
        strip_h = 34
        part_w = strip_w / common_den
        for i in range(common_den):
            if i < left_common:
                fill = PrimaryPalette.ACCENT_BLUE
            elif i < left_common + right_common:
                fill = PrimaryPalette.AMBER
            else:
                fill = PrimaryPalette.LIGHT_BG
            backend.draw_rect(sx + i * part_w, sy, part_w, strip_h, fill=fill, stroke=PrimaryPalette.NAVY, stroke_width=1.0)
        labels = [f"{left[0]}/{left[1]}", f"{right[0]}/{right[1]}", f"{result[0]}/{result[1]}", equation]
        backend.record_evidence("FRACTION_ADDITION_REPARTITION", params, len(labels) + common_den, labels)
