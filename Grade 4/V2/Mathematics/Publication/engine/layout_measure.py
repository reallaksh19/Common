"""Intrinsic measurement helpers for Grade 4 Math V2 publication.

Publication components measure before drawing. No learner-facing text is shrunk
to make a page fit; a component either reports the required height or publication
fails/page-breaks before rendering it.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class PublicationLayoutError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise PublicationLayoutError(code, message)


def wrapped_line_count(text: str, width: float, font_size: float, *, width_factor: float = 0.55) -> int:
    _require(width > 0, "PUBLICATION_MEASURE_WIDTH_INVALID", str(width))
    _require(font_size >= 9.5, "LEARNER_FONT_MIN", f"font_size={font_size}")
    if not str(text or ""):
        return 0
    chars_per_line = max(int(width / max(font_size * width_factor, 1.0)), 1)
    lines = 0
    for paragraph in str(text).splitlines() or [""]:
        lines += max(1, int(math.ceil(max(len(paragraph), 1) / chars_per_line)))
    return lines


def paragraph_height(
    text: str,
    width: float,
    *,
    font_size: float = 12.5,
    line_height: float = 16.0,
    padding_bottom: float = 0.0,
) -> float:
    _require(line_height >= font_size, "PUBLICATION_LINE_HEIGHT_INVALID", f"{line_height} < {font_size}")
    return wrapped_line_count(text, width, font_size) * line_height + padding_bottom


def assert_component_fits_page(component_name: str, height: float, usable_height: float) -> None:
    _require(height > 0, "PUBLICATION_COMPONENT_HEIGHT_INVALID", f"{component_name}: {height}")
    _require(
        height <= usable_height,
        "PUBLICATION_COMPONENT_TALLER_THAN_PAGE",
        f"{component_name}: required={height:.1f}, usable={usable_height:.1f}",
    )
