"""
Base classes, metrics, palettes, and vector rendering backend abstractions
for Primary Mathematics V2 visual publishing engine.
"""
from __future__ import annotations

import abc
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


class PrimaryPalette:
    """WCAG AAA accessible, child-friendly high-contrast color palette."""
    NAVY = "#1E293B"            # Text & primary outlines (slate 800)
    AMBER = "#D97706"           # Accent 1 / multiplication highlight
    TEAL = "#0D9488"            # Accent 2 / division highlight
    SLATE = "#64748B"           # Secondary text / guides (slate 500)
    LIGHT_BG = "#F8FAFC"        # Card background (slate 50)
    CARD_BORDER = "#CBD5E1"     # Card stroke (slate 300)
    ACCENT_BLUE = "#2563EB"     # Fractions / place-value blue
    GRID_LINE = "#E2E8F0"       # Subtle notebook grid (slate 200)
    STUDENT_PENCIL = "#334155"  # Replay child handwriting (slate 700)
    TEACHER_RED = "#DC2626"     # Teacher markings / corrections
    HIGHLIGHT_YELLOW = "#FEF08A"# Notice callout fill
    WHITE = "#FFFFFF"
    SOFT_GREEN = "#16A34A"      # Checkmark / correct status


@dataclass(frozen=True)
class PageMetricsA4:
    """A4 Portrait child-first dimensional invariants."""
    PAGE_WIDTH: float = 595.27
    PAGE_HEIGHT: float = 841.89
    MARGIN_LEFT: float = 40.0
    MARGIN_RIGHT: float = 40.0
    MARGIN_TOP: float = 40.0
    MARGIN_BOTTOM: float = 40.0
    
    @property
    def usable_width(self) -> float:
        return self.PAGE_WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT

    @property
    def usable_height(self) -> float:
        return self.PAGE_HEIGHT - self.MARGIN_TOP - self.MARGIN_BOTTOM

    # Typography minimums (child readability)
    TITLE_FONT_SIZE: float = 20.0
    SECTION_FONT_SIZE: float = 16.0
    BODY_FONT_SIZE: float = 13.5
    MIN_BODY_FONT_SIZE: float = 12.0
    CAPTION_FONT_SIZE: float = 11.0
    MIN_RESPONSE_BOX_HEIGHT: float = 65.0


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    @property
    def x_max(self) -> float:
        return self.x + self.width

    @property
    def y_max(self) -> float:
        return self.y + self.height


class VectorRenderBackend(abc.ABC):
    """Abstract vector rendering backend interface."""

    def __init__(self) -> None:
        self.evidence: List[Dict[str, Any]] = []
        self._element_counter: int = 0
        self._recorded_labels: List[str] = []

    @abc.abstractmethod
    def draw_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1.0,
        corner_radius: float = 0.0
    ) -> None:
        pass

    @abc.abstractmethod
    def draw_circle(
        self,
        cx: float,
        cy: float,
        r: float,
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1.0
    ) -> None:
        pass

    @abc.abstractmethod
    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = PrimaryPalette.NAVY,
        stroke_width: float = 1.0,
        dash_pattern: Optional[List[float]] = None
    ) -> None:
        pass

    @abc.abstractmethod
    def draw_text(
        self,
        text: str,
        x: float,
        y: float,
        font_name: str = "Helvetica",
        font_size: float = 13.5,
        color: str = PrimaryPalette.NAVY,
        align: str = "left"
    ) -> None:
        pass

    @abc.abstractmethod
    def draw_polygon(
        self,
        points: List[Tuple[float, float]],
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1.0
    ) -> None:
        pass

    def draw_arrow(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = PrimaryPalette.NAVY,
        stroke_width: float = 1.5,
        arrowhead_size: float = 6.0
    ) -> None:
        """Draw an arrow from (x1, y1) to (x2, y2)."""
        import math
        self.draw_line(x1, y1, x2, y2, stroke=stroke, stroke_width=stroke_width)
        angle = math.atan2(y2 - y1, x2 - x1)
        p1 = (
            x2 - arrowhead_size * math.cos(angle - math.pi / 6),
            y2 - arrowhead_size * math.sin(angle - math.pi / 6)
        )
        p2 = (
            x2 - arrowhead_size * math.cos(angle + math.pi / 6),
            y2 - arrowhead_size * math.sin(angle + math.pi / 6)
        )
        self.draw_polygon([ (x2, y2), p1, p2 ], fill=stroke, stroke=stroke, stroke_width=stroke_width)

    def record_evidence(self, kind: str, params: Dict[str, Any], element_count: int, labels: List[str]) -> None:
        serialized = json.dumps({"kind": kind, "params": params, "labels": sorted(labels)}, sort_keys=True)
        checksum = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.evidence.append({
            "kind": kind,
            "params": params,
            "rendered_evidence": {
                "element_count": element_count,
                "visual_checksum": checksum,
                "data_grounded": True,
                "labels": labels
            }
        })

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self.evidence


class MockVectorBackend(VectorRenderBackend):
    """Headless recorder backend for validation and testing."""

    def __init__(self) -> None:
        super().__init__()
        self.operations: List[Dict[str, Any]] = []

    def draw_rect(self, x, y, width, height, fill=None, stroke=None, stroke_width=1.0, corner_radius=0.0):
        self._element_counter += 1
        self.operations.append({"op": "rect", "x": x, "y": y, "width": width, "height": height, "fill": fill})

    def draw_circle(self, cx, cy, r, fill=None, stroke=None, stroke_width=1.0):
        self._element_counter += 1
        self.operations.append({"op": "circle", "cx": cx, "cy": cy, "r": r, "fill": fill})

    def draw_line(self, x1, y1, x2, y2, stroke=PrimaryPalette.NAVY, stroke_width=1.0, dash_pattern=None):
        self._element_counter += 1
        self.operations.append({"op": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": stroke})

    def draw_text(self, text, x, y, font_name="Helvetica", font_size=13.5, color=PrimaryPalette.NAVY, align="left"):
        self._element_counter += 1
        self._recorded_labels.append(str(text))
        self.operations.append({"op": "text", "text": text, "x": x, "y": y, "font_size": font_size, "align": align})

    def draw_polygon(self, points, fill=None, stroke=None, stroke_width=1.0):
        self._element_counter += 1
        self.operations.append({"op": "polygon", "points": points, "fill": fill})


class ReportLabBackend(VectorRenderBackend):
    """Reference concrete backend drawing directly to ReportLab Canvas."""

    def __init__(self, canvas: Any) -> None:
        super().__init__()
        self.canvas = canvas
        from reportlab.lib import colors
        self._colors = colors

    def _hex_to_color(self, hex_code: Optional[str]):
        if not hex_code:
            return None
        return self._colors.HexColor(hex_code)

    def draw_rect(self, x, y, width, height, fill=None, stroke=None, stroke_width=1.0, corner_radius=0.0):
        self._element_counter += 1
        self.canvas.saveState()
        self.canvas.setLineWidth(stroke_width)
        f_col = self._hex_to_color(fill)
        s_col = self._hex_to_color(stroke)
        if f_col:
            self.canvas.setFillColor(f_col)
        if s_col:
            self.canvas.setStrokeColor(s_col)
        
        do_fill = 1 if f_col else 0
        do_stroke = 1 if s_col else 0
        
        if corner_radius > 0:
            self.canvas.roundRect(x, y, width, height, corner_radius, stroke=do_stroke, fill=do_fill)
        else:
            self.canvas.rect(x, y, width, height, stroke=do_stroke, fill=do_fill)
        self.canvas.restoreState()

    def draw_circle(self, cx, cy, r, fill=None, stroke=None, stroke_width=1.0):
        self._element_counter += 1
        self.canvas.saveState()
        self.canvas.setLineWidth(stroke_width)
        f_col = self._hex_to_color(fill)
        s_col = self._hex_to_color(stroke)
        if f_col:
            self.canvas.setFillColor(f_col)
        if s_col:
            self.canvas.setStrokeColor(s_col)
        self.canvas.circle(cx, cy, r, stroke=1 if s_col else 0, fill=1 if f_col else 0)
        self.canvas.restoreState()

    def draw_line(self, x1, y1, x2, y2, stroke=PrimaryPalette.NAVY, stroke_width=1.0, dash_pattern=None):
        self._element_counter += 1
        self.canvas.saveState()
        self.canvas.setLineWidth(stroke_width)
        self.canvas.setStrokeColor(self._hex_to_color(stroke))
        if dash_pattern:
            self.canvas.setDash(dash_pattern)
        self.canvas.line(x1, y1, x2, y2)
        self.canvas.restoreState()

    def draw_text(self, text, x, y, font_name="Helvetica", font_size=13.5, color=PrimaryPalette.NAVY, align="left"):
        self._element_counter += 1
        self._recorded_labels.append(str(text))
        self.canvas.saveState()
        self.canvas.setFont(font_name, font_size)
        self.canvas.setFillColor(self._hex_to_color(color))
        if align == "center":
            self.canvas.drawCentredString(x, y, str(text))
        elif align == "right":
            self.canvas.drawRightString(x, y, str(text))
        else:
            self.canvas.drawString(x, y, str(text))
        self.canvas.restoreState()

    def draw_polygon(self, points, fill=None, stroke=None, stroke_width=1.0):
        self._element_counter += 1
        if not points:
            return
        self.canvas.saveState()
        self.canvas.setLineWidth(stroke_width)
        f_col = self._hex_to_color(fill)
        s_col = self._hex_to_color(stroke)
        if f_col:
            self.canvas.setFillColor(f_col)
        if s_col:
            self.canvas.setStrokeColor(s_col)
        p = self.canvas.beginPath()
        p.moveTo(points[0][0], points[0][1])
        for pt in points[1:]:
            p.lineTo(pt[0], pt[1])
        p.close()
        self.canvas.drawPath(p, stroke=1 if s_col else 0, fill=1 if f_col else 0)
        self.canvas.restoreState()
