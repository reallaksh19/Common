#!/usr/bin/env python3
"""Review-grade, topic-neutral Chemistry PDF composition primitives.

This module owns page composition only. It may organize already-authorized learner
content, but it may not select representations, invent Chemistry, or change semantic
custody. All learner text still passes the existing learner-surface projection.
"""
from __future__ import annotations

from typing import Any

from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

import chemistry_visual_primitives as VP
from render_chemistry_learner_products import (
    BOLD,
    FONT,
    PAGE_H,
    PAGE_W,
    params_from_representation,
    public_text,
    register_fonts,
)

INK = HexColor("#18324A")
ACCENT = HexColor("#087E8B")
ACCENT_DARK = HexColor("#08616A")
ACCENT_PALE = HexColor("#EAF6F7")
BLUE_PALE = HexColor("#EEF4FA")
WARM_PALE = HexColor("#FFF6DF")
GREEN_PALE = HexColor("#EAF7F1")
ROSE_PALE = HexColor("#FFF0EE")
PAPER = HexColor("#FBFCFD")
LINE = HexColor("#D8E1E8")
MUTED = HexColor("#5E6E7C")

ROLE_LABELS = {
    "COVER": "START HERE",
    "ROUTE_OR_MAP": "ROUTE",
    "CONCEPT_EXPLANATION": "LEARN",
    "RULE_OR_DERIVATION": "BUILD THE RULE",
    "REPRESENTATION": "REPRESENT",
    "TTU_RECONSTRUCTION": "RECONSTRUCT",
    "WORKED_EXAMPLE": "WATCH ONE",
    "MISCONCEPTION_OR_BOUNDARY": "CHECK THE BOUNDARY",
    "PRACTICE": "PRACTISE",
    "QUESTION_EPISODE": "ATTEMPT",
    "WORKSPACE": "WORKSPACE",
    "SOLUTION": "CHECK",
    "SUMMARY_OR_HANDOUT": "REVIEW",
}

PANEL_FILLS = {
    "CONCEPT_PANEL": BLUE_PALE,
    "QUESTION_PANEL": WARM_PALE,
    "VISUAL_PANEL": ACCENT_PALE,
    "WORKSPACE_PANEL": PAPER,
    "CLUE_PANEL": BLUE_PALE,
    "ANSWER_PANEL": GREEN_PALE,
    "VERIFICATION_PANEL": ACCENT_PALE,
    "ACTION_PANEL": ROSE_PALE,
    "ROUTE_PANEL": ACCENT_PALE,
}


class ReviewWriter:
    """Deterministic page composer with an inspectable semantic render trace."""

    def __init__(self, path, title: str, policy: dict[str, Any]):
        register_fonts()
        page = policy["page"]
        self.path = path
        self.margin = float(page["margin_pt"])
        self.body = float(page["body_font_pt"])
        self.leading = float(page["body_leading_pt"])
        self.question = float(page["question_font_pt"])
        self.question_leading = float(page["question_leading_pt"])
        self.small = float(page["small_label_font_pt"])
        self.section = float(page["section_heading_font_pt"])
        self.chapter = float(page["chapter_heading_font_pt"])
        self.minimum_font = 999.0
        self.c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), invariant=1, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor("Chemistry V2 review-grade deterministic renderer")
        self.page = 0
        self.y = 0.0
        self.current_role = "COVER"
        self.current_context = ""
        self.current_context_ref = None
        self.draw_ops: list[dict[str, Any]] = []
        self.primitives: list[dict[str, Any]] = []
        self.unavailable_primitives: list[dict[str, Any]] = []
        self.page_labels: list[dict[str, Any]] = []
        self.new_page("cover", role="COVER")

    @property
    def width(self) -> float:
        return PAGE_W - 2 * self.margin

    def _record(self, kind, x0, y0, x1, y1, text=None, font=None, ref=None):
        self.draw_ops.append({
            "page": self.page,
            "kind": kind,
            "x0": round(float(x0), 2),
            "y0": round(float(y0), 2),
            "x1": round(float(x1), 2),
            "y1": round(float(y1), 2),
            "text": text,
            "font_pt": font,
            "content_ref": ref,
        })
        if font is not None:
            self.minimum_font = min(self.minimum_font, float(font))

    def _redraw_nav_header(self, role: str) -> None:
        """Replace the physical nav label only while the page is still pristine."""
        band_h = 30.0
        right = ROLE_LABELS.get(role, public_text(role).upper())
        self.c.setFillColor(INK)
        self.c.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont(BOLD, self.small)
        self.c.drawString(self.margin, PAGE_H - 20.0, "CHEMISTRY")
        self.c.drawRightString(PAGE_W - self.margin, PAGE_H - 20.0, right)
        headers = [
            row for row in self.draw_ops
            if row.get("page") == self.page and row.get("kind") == "NAV_HEADER"
        ]
        if len(headers) != 1:
            raise ValueError("CHEM_REVIEW_NAV_HEADER_TRACE_INVALID")
        headers[0]["text"] = right

    def set_page_role(self, role: str) -> None:
        """Set a physical page role without permitting metadata-only role mutation.

        A pristine page may be assigned its intended role before semantic content is
        drawn; its nav header is redrawn in place. Once semantic content exists, a
        role transition starts a new physical page so visible navigation, render trace
        and page-role metadata cannot diverge.
        """
        role = str(role or "").strip()
        if not role:
            raise ValueError("CHEM_REVIEW_PAGE_ROLE_REQUIRED")
        if role == self.current_role:
            return
        semantic_ops = [
            row for row in self.draw_ops
            if row.get("page") == self.page
            and row.get("kind") not in {"NAV_HEADER", "FOOTER"}
        ]
        if not semantic_ops:
            self.current_role = role
            if self.page_labels:
                self.page_labels[-1]["role"] = role
            self._redraw_nav_header(role)
            return
        self.new_page("role transition", role=role)

    def _draw_continuation_header(self, context: str, ref=None) -> None:
        value = public_text(context)
        if not value:
            return
        inner_w = self.width - 28
        rows = self._wrap(value, BOLD, self.small, inner_w)
        row_leading = self.small + 4.0
        height = 18.0 + row_leading + len(rows) * row_leading + 10.0
        y0 = self.y - height
        self.c.setFillColor(BLUE_PALE)
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        self.c.roundRect(self.margin, y0, self.width, height, 7, fill=1, stroke=1)
        self.c.setFillColor(ACCENT_DARK)
        self.c.setFont(BOLD, self.small)
        label_y = self.y - 15.0
        self.c.drawString(self.margin + 14, label_y, "CONTINUING")
        self._record(
            "TEXT",
            self.margin + 14,
            label_y - self.small * .25,
            self.margin + 14 + stringWidth("CONTINUING", BOLD, self.small),
            label_y + self.small,
            "CONTINUING",
            self.small,
            ref,
        )
        self.c.setFillColor(INK)
        text_y = label_y - row_leading
        for row in rows:
            self.c.drawString(self.margin + 14, text_y, row)
            self._record(
                "TEXT",
                self.margin + 14,
                text_y - self.small * .25,
                self.margin + 14 + stringWidth(row, BOLD, self.small),
                text_y + self.small,
                row,
                self.small,
                ref,
            )
            text_y -= row_leading
        self._record("CONTINUATION_HEADER", self.margin, y0, self.margin + self.width, self.y, value, None, ref)
        self.y = y0 - 10.0

    def new_page(
        self,
        label: str,
        role: str | None = None,
        continuation_context: str | None = None,
        continuation_ref=None,
    ) -> None:
        if self.page:
            self.c.showPage()
        self.page += 1
        self.current_role = role or getattr(self, "current_role", "CONCEPT_EXPLANATION")
        if continuation_context is None:
            self.current_context = ""
            self.current_context_ref = None
        self.c.setFillColor(PAPER)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

        band_h = 30.0
        self.c.setFillColor(INK)
        self.c.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont(BOLD, self.small)
        left = "CHEMISTRY"
        right = ROLE_LABELS.get(self.current_role, public_text(label).upper())
        self.c.drawString(self.margin, PAGE_H - 20.0, left)
        self.c.drawRightString(PAGE_W - self.margin, PAGE_H - 20.0, right)
        self._record("NAV_HEADER", 0, PAGE_H - band_h, PAGE_W, PAGE_H, right, self.small)

        footer = f"Chemistry V2  •  {self.page}"
        self.c.setFillColor(MUTED)
        self.c.setFont(FONT, self.small)
        self.c.drawRightString(PAGE_W - self.margin, 22, footer)
        self._record(
            "FOOTER",
            PAGE_W - self.margin - stringWidth(footer, FONT, self.small),
            18,
            PAGE_W - self.margin,
            18 + self.small + 2,
            footer,
            self.small,
        )
        self.y = PAGE_H - band_h - 24.0
        self.page_labels.append({"page": self.page, "label": public_text(label), "role": self.current_role})
        if continuation_context:
            self._draw_continuation_header(continuation_context, continuation_ref)

    def ensure(
        self,
        height: float,
        label: str = "continuation",
        role: str | None = None,
        *,
        show_context: bool = True,
    ) -> None:
        if self.y - height < self.margin + 8:
            context = self.current_context if show_context else None
            context_ref = self.current_context_ref if show_context else None
            self.new_page(
                label,
                role=role or self.current_role,
                continuation_context=context,
                continuation_ref=context_ref,
            )

    def _wrap(self, text: str, font: str, size: float, width: float) -> list[str]:
        words = public_text(text).replace("\n", " \n ").split()
        lines: list[str] = []
        current = ""
        for word in words:
            if word == "\n":
                if current:
                    lines.append(current)
                    current = ""
                lines.append("")
                continue
            trial = (current + " " + word).strip()
            if stringWidth(trial, font, size) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]

    def line(self, text, size=None, font=FONT, indent=0.0, leading=None, ref=None):
        size = float(size or self.body)
        leading = float(leading or self.leading)
        rows = self._wrap(public_text(text), font, size, self.width - indent)
        self.ensure(len(rows) * leading + 4)
        self.c.setFillColor(INK)
        self.c.setFont(font, size)
        for row in rows:
            x = self.margin + indent
            self.c.drawString(x, self.y, row)
            width = stringWidth(row, font, size)
            self._record("TEXT", x, self.y - size * 0.25, x + width, self.y + size, row, size, ref)
            self.y -= leading
        self.y -= 3

    def heading(self, text, level=1, ref=None):
        value = public_text(text)
        size = self.chapter if level == 1 else self.section
        rows = self._wrap(value, BOLD, size, self.width - 20)
        height = len(rows) * (size + 5) + (16 if level == 1 else 12)
        follow_reserve = self.leading * (6.0 if level == 1 else 5.0)
        self.ensure(height + follow_reserve, value, show_context=False)
        self.current_context = value
        self.current_context_ref = ref
        if level == 1:
            self.c.setFillColor(ACCENT)
            self.c.roundRect(self.margin, self.y - 8, 7, height - 4, 3, fill=1, stroke=0)
            x = self.margin + 18
        else:
            self.c.setStrokeColor(ACCENT)
            self.c.setLineWidth(2.2)
            self.c.line(self.margin, self.y + 2, self.margin + 20, self.y + 2)
            x = self.margin
            self.y -= 7
        self.c.setFillColor(INK)
        self.c.setFont(BOLD, size)
        for row in rows:
            self.c.drawString(x, self.y, row)
            width = stringWidth(row, BOLD, size)
            self._record("TEXT", x, self.y - size * 0.25, x + width, self.y + size, row, size, ref)
            self.y -= size + 5
        self.y -= 8

    def label(self, text, ref=None):
        value = public_text(text).upper()
        width = min(self.width, stringWidth(value, BOLD, self.small) + 20)
        height = self.small + 11
        self.ensure(height + 5)
        y0 = self.y - height + 3
        self.c.setFillColor(ACCENT_PALE)
        self.c.roundRect(self.margin, y0, width, height, 5, fill=1, stroke=0)
        self.c.setFillColor(ACCENT_DARK)
        self.c.setFont(BOLD, self.small)
        self.c.drawString(self.margin + 10, y0 + 6, value)
        self._record("SECTION_LABEL", self.margin, y0, self.margin + width, y0 + height, value, self.small, ref)
        self.y = y0 - 7

    def para(self, text, ref=None):
        if text not in (None, ""):
            self.line(text, ref=ref)

    def bullets(self, values, ref=None):
        for value in values or []:
            rows = self._wrap(public_text(value), FONT, self.body, self.width - 25)
            self.ensure(len(rows) * self.leading + 5)
            self.c.setFillColor(ACCENT)
            self.c.circle(self.margin + 5, self.y + 3, 2.2, fill=1, stroke=0)
            self.c.setFillColor(INK)
            self.c.setFont(FONT, self.body)
            for idx, row in enumerate(rows):
                x = self.margin + 16
                self.c.drawString(x, self.y, row)
                self._record("TEXT", x, self.y - self.body * .25, x + stringWidth(row, FONT, self.body), self.y + self.body, row, self.body, ref)
                self.y -= self.leading
            self.y -= 2

    def _panel_text(self, title: str, text: Any, kind: str, ref=None, *, fill=None, bold_body=False):
        title = public_text(title)
        text = public_text(text)
        inner_w = self.width - 28
        rows = self._wrap(text, BOLD if bold_body else FONT, self.body, inner_w)
        title_rows = self._wrap(title.upper(), BOLD, self.small, inner_w)
        height = 16 + len(title_rows) * (self.small + 4) + len(rows) * self.leading + 16
        self.ensure(height + 8, title)
        y0 = self.y - height
        self.c.setFillColor(fill or PANEL_FILLS.get(kind, PAPER))
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.8)
        self.c.roundRect(self.margin, y0, self.width, height, 8, fill=1, stroke=1)
        self.c.setFillColor(ACCENT_DARK)
        self.c.setFont(BOLD, self.small)
        ty = self.y - 14
        for row in title_rows:
            self.c.drawString(self.margin + 14, ty, row)
            self._record("TEXT", self.margin + 14, ty - self.small * .25, self.margin + 14 + stringWidth(row, BOLD, self.small), ty + self.small, row, self.small, ref)
            ty -= self.small + 4
        self.c.setFillColor(INK)
        body_font = BOLD if bold_body else FONT
        self.c.setFont(body_font, self.body)
        ty -= 3
        for row in rows:
            self.c.drawString(self.margin + 14, ty, row)
            self._record("TEXT", self.margin + 14, ty - self.body * .25, self.margin + 14 + stringWidth(row, body_font, self.body), ty + self.body, row, self.body, ref)
            ty -= self.leading
        self._record(kind, self.margin, y0, self.margin + self.width, self.y, title, None, ref)
        self.y = y0 - 10

    def concept_panel(self, title: str, text: Any, ref=None):
        self._panel_text(title, text, "CONCEPT_PANEL", ref)

    def route_panel(self, title: str, text: Any, ref=None):
        self._panel_text(title, text, "ROUTE_PANEL", ref)

    def action_panel(self, title: str, text: Any, ref=None):
        self._panel_text(title, text, "ACTION_PANEL", ref)

    def clue_panel(self, title: str, text: Any, ref=None):
        self._panel_text(title, text, "CLUE_PANEL", ref)

    def answer_panel(self, title: str, text: Any, ref=None):
        self._panel_text(title, text, "ANSWER_PANEL", ref, bold_body=True)

    def verification_panel(self, title: str, text: Any, ref=None):
        self._panel_text(title, text, "VERIFICATION_PANEL", ref)

    def question_text(self, text, ref=None):
        value = public_text(text)
        inner_w = self.width - 32
        rows = self._wrap(value, BOLD, self.question, inner_w)
        height = len(rows) * self.question_leading + 28
        self.ensure(height + 9, "question", role="QUESTION_EPISODE")
        y0 = self.y - height
        self.c.setFillColor(WARM_PALE)
        self.c.setStrokeColor(HexColor("#E8C875"))
        self.c.setLineWidth(1.0)
        self.c.roundRect(self.margin, y0, self.width, height, 8, fill=1, stroke=1)
        self.c.setFillColor(INK)
        self.c.setFont(BOLD, self.question)
        ty = self.y - 17
        for row in rows:
            self.c.drawString(self.margin + 16, ty, row)
            self._record("TEXT", self.margin + 16, ty - self.question * .25, self.margin + 16 + stringWidth(row, BOLD, self.question), ty + self.question, row, self.question, ref)
            ty -= self.question_leading
        self._record("QUESTION_PANEL", self.margin, y0, self.margin + self.width, self.y, ref=ref)
        self.y = y0 - 10

    def rule(self):
        self.ensure(10)
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        self.c.line(self.margin, self.y, PAGE_W - self.margin, self.y)
        self._record("RULE", self.margin, self.y - .5, PAGE_W - self.margin, self.y + .5)
        self.y -= 12

    def workspace(self, lines=5, ref=None):
        lines = max(3, int(lines))
        height = 34 + lines * 20
        self.ensure(height + 10, "workspace", role="WORKSPACE")
        y0 = self.y - height
        self.c.setFillColor(PAPER)
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.9)
        self.c.roundRect(self.margin, y0, self.width, height, 8, fill=1, stroke=1)
        self.c.setFillColor(ACCENT_DARK)
        self.c.setFont(BOLD, self.small)
        self.c.drawString(self.margin + 14, self.y - 18, "YOUR WORK")
        self._record("TEXT", self.margin + 14, self.y - 21, self.margin + 90, self.y - 8, "YOUR WORK", self.small, ref)
        line_y = self.y - 42
        for _ in range(lines):
            self.c.setStrokeColor(LINE)
            self.c.setLineWidth(.55)
            self.c.line(self.margin + 14, line_y, PAGE_W - self.margin - 14, line_y)
            self._record("WORKSPACE_LINE", self.margin + 14, line_y - .5, PAGE_W - self.margin - 14, line_y + .5, ref=ref)
            line_y -= 20
        self._record("WORKSPACE_PANEL", self.margin, y0, self.margin + self.width, self.y, ref=ref)
        self.y = y0 - 10

    def primitive(self, rep, ref, extra=None):
        kind = rep["primitive_id"]
        params = params_from_representation(rep, extra)
        inner_w = self.width - 24
        try:
            primitive_h = float(VP.primitive_height(kind, params, inner_w))
        except VP.PrimitiveDataUnavailable as exc:
            self.unavailable_primitives.append({"page": self.page, "content_ref": ref, "representation_ref": rep["representation_id"], "primitive_id": kind, "reason": str(exc)})
            return False
        height = primitive_h + 34
        self.ensure(height + 10, "reasoning visual", role="REPRESENTATION")
        y0 = self.y - height
        self.c.setFillColor(ACCENT_PALE)
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(.8)
        self.c.roundRect(self.margin, y0, self.width, height, 8, fill=1, stroke=1)
        self.c.setFillColor(ACCENT_DARK)
        self.c.setFont(BOLD, self.small)
        self.c.drawString(self.margin + 12, self.y - 16, "CHEMISTRY MODEL")
        try:
            record = VP.render_primitive(kind, params, self.c, (self.margin + 12, y0 + 10, inner_w, primitive_h))
        except VP.PrimitiveDataUnavailable as exc:
            self.unavailable_primitives.append({"page": self.page, "content_ref": ref, "representation_ref": rep["representation_id"], "primitive_id": kind, "reason": str(exc)})
            return False
        self._record("VISUAL_PANEL", self.margin, y0, self.margin + self.width, self.y, ref=ref)
        self._record("PRIMITIVE", self.margin + 12, y0 + 10, self.margin + 12 + inner_w, y0 + 10 + primitive_h, ref=ref)
        self.primitives.append(dict(record, page=self.page, content_ref=ref, representation_ref=rep["representation_id"]))
        self.y = y0 - 10
        return True

    def finish(self):
        self.c.save()
        return {
            "pdf": self.path.name,
            "page_count": self.page,
            "minimum_visible_font_pt": round(self.minimum_font, 2),
            "page_size_pt": [round(PAGE_W, 3), round(PAGE_H, 3)],
            "draw_ops": self.draw_ops,
            "primitives": self.primitives,
            "unavailable_primitives": self.unavailable_primitives,
            "page_labels": self.page_labels,
            "composition_system": "CHEMISTRY_REVIEW_GRADE_V1",
        }
