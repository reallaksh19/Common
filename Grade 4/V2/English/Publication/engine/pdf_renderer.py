"""Measured ReportLab renderer for Grade-4 English V2 publication models.

The renderer lays out already-authored semantics. It does not create grammar rules,
hints, rubrics, misconceptions, or open-response truth.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

W, H = A4
M = 40
PURPLE = colors.HexColor("#6752DF")
NAVY = colors.HexColor("#17324D")
MUTED = colors.HexColor("#607890")
BORDER = colors.HexColor("#D5E1ED")
PALE_BLUE = colors.HexColor("#EAF4FF")
PALE_GREEN = colors.HexColor("#EAF8F2")
PALE_YELLOW = colors.HexColor("#FFF6CF")
PALE_PURPLE = colors.HexColor("#F0ECFF")
WHITE = colors.white


def _wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = str(text or "").split()
    out: list[str] = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out or [""]


def _text(c: canvas.Canvas, text: str, x: float, y: float, width: float, *, size: float = 10.5, leading: float = 14, bold: bool = False, color=NAVY, max_lines: int | None = None) -> float:
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFillColor(color)
    c.setFont(font, size)
    lines = _wrap(text, font, size, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def _card(c: canvas.Canvas, x: float, y_top: float, w: float, h: float, fill, title: str | None = None) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y_top - h, w, h, 10, fill=1, stroke=1)
    if title:
        _text(c, title, x + 12, y_top - 20, w - 24, size=11.2, bold=True)


def _header(c: canvas.Canvas, title: str, subtitle: str | None, page_no: int) -> float:
    c.setFillColor(PURPLE)
    c.roundRect(M, H - 120, W - 2 * M, 72, 18, fill=1, stroke=0)
    _text(c, title, M + 18, H - 82, W - 2 * M - 36, size=19, leading=21, bold=True, color=WHITE, max_lines=2)
    y = H - 142
    if subtitle:
        y = _text(c, subtitle, M, y, W - 2 * M, size=10.6, leading=14, color=MUTED, max_lines=3) - 4
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M, 20, str(page_no))
    return y


def _cover(c: canvas.Canvas, page: Mapping[str, Any], page_no: int) -> None:
    c.setFillColor(PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    _text(c, f"GRADE {page.get('grade', 4)} ENGLISH", M, H - 95, W - 2 * M, size=11, bold=True, color=WHITE)
    _text(c, page["title"], M, H - 145, W - 2 * M, size=28, leading=31, bold=True, color=WHITE, max_lines=3)
    _text(c, page.get("subtitle", ""), M, H - 260, W - 2 * M, size=13, leading=19, color=WHITE, max_lines=5)
    _card(c, M, H - 385, W - 2 * M, 124, PALE_YELLOW)
    _text(c, "Built from the supplied questions", M + 18, H - 420, W - 2 * M - 36, size=15, bold=True)
    _text(c, "Try → use the smallest helpful clue → do a fresh question by yourself.", M + 18, H - 450, W - 2 * M - 36, size=12, leading=17)
    _text(c, f"Source: {page.get('source_id', '')}", M + 18, H - 490, W - 2 * M - 36, size=9.5, color=MUTED)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M, 20, str(page_no))


def _chips(c: canvas.Canvas, labels: Sequence[str], x: float, y: float, width: float, *, size: float = 8.5, row_gap: float = 24) -> float:
    cx, cy = x, y
    for label in labels:
        text = str(label)
        tw = stringWidth(text, "Helvetica", size) + 18
        if cx + tw > x + width:
            cx = x
            cy -= row_gap
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER)
        c.roundRect(cx, cy - 15, tw, 19, 8, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica", size)
        c.drawCentredString(cx + tw / 2, cy - 9, text)
        cx += tw + 6
    return cy - 22


def _rep_height(rep_id: str) -> float:
    if rep_id == "CATEGORY_SORT_TABLE":
        return 205
    if rep_id in {"TRAVEL_BLOGGER_PLANNER", "MYSTERY_OBJECT_PLANNER", "STANZA_MEANING_MAP", "MULTI_CLUE_TABLE", "WRITING_CHECKLIST"}:
        return 150
    return 105


def _render_rep(c: canvas.Canvas, rep: Mapping[str, Any], x: float, y: float, w: float) -> float:
    rep_id = rep["representation_id"]
    p = rep.get("semantic_params") or {}
    h = _rep_height(rep_id)
    _card(c, x, y, w, h, colors.HexColor("#FBFDFF"), rep.get("label"))

    if rep_id == "ADJECTIVE_FAMILY_CARDS":
        cats = p.get("source_categories") or ["opinion", "size", "age", "shape", "colour", "origin", "material"]
        _chips(c, cats, x + 12, y - 40, w - 24)

    elif rep_id == "CATEGORY_SORT_TABLE":
        words = p.get("source_words") or []
        if words:
            _chips(c, words, x + 12, y - 40, w - 24, size=8.2, row_gap=23)
        cats = ["Opinion", "Size", "Age", "Shape", "Colour", "Origin", "Material"]
        left = x + 12
        table_top = y - 118 if words else y - 52
        colw = (w - 24) / len(cats)
        for i, cat in enumerate(cats):
            xx = left + i * colw
            c.setFillColor(PALE_BLUE)
            c.setStrokeColor(BORDER)
            c.rect(xx, table_top - 24, colw, 24, fill=1, stroke=1)
            c.setFillColor(NAVY)
            c.setFont("Helvetica-Bold", 6.5)
            c.drawCentredString(xx + colw / 2, table_top - 15, cat)
            c.setFillColor(WHITE)
            c.rect(xx, table_top - 66, colw, 42, fill=1, stroke=1)

    elif rep_id == "ADJECTIVE_ORDER_TRAIN":
        ordering = p.get("ordering") or ["OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL"]
        labels = list(ordering) + ["NOUN"]
        boxw = (w - 30) / len(labels)
        xx = x + 12
        for label in labels:
            c.setFillColor(PALE_PURPLE)
            c.setStrokeColor(BORDER)
            c.roundRect(xx, y - 78, boxw - 4, 34, 6, fill=1, stroke=1)
            c.setFillColor(NAVY)
            c.setFont("Helvetica-Bold", 6.4)
            c.drawCentredString(xx + (boxw - 4) / 2, y - 59, str(label).title())
            xx += boxw

    elif rep_id == "CONTRAST_PAIR":
        contrasts = p.get("contrasts") or [["example A", "example B"]]
        yy = y - 48
        for pair in contrasts[:2]:
            _text(c, f"{pair[0]}  ↔  {pair[1]}", x + 18, yy, w - 36, size=11, bold=True)
            yy -= 30

    elif rep_id in {"NOUN_PHRASE_BUILDER", "ANSWER_CLUE_CONNECTION", "CHOICE_REASON_FRAME", "TEXT_VS_MY_THINKING", "TRANSFER_THREAT_ACTION_TABLE", "CAUSE_EFFECT_CHAIN"}:
        labels = {
            "NOUN_PHRASE_BUILDER": ["describing word", "describing word", "noun"],
            "ANSWER_CLUE_CONNECTION": ["Answer", "Text clue", "Connection"],
            "CHOICE_REASON_FRAME": ["My choice", "Why it matters"],
            "TEXT_VS_MY_THINKING": ["What the text gives me", "What I think / connect"],
            "TRANSFER_THREAT_ACTION_TABLE": ["Species", "Threat", "What people can do"],
            "CAUSE_EFFECT_CHAIN": ["Cause", "What changes", "Effect"],
        }[rep_id]
        colw = (w - 30) / len(labels)
        xx = x + 12
        for label in labels:
            c.setFillColor(PALE_BLUE)
            c.setStrokeColor(BORDER)
            c.roundRect(xx, y - 82, colw - 4, 46, 6, fill=1, stroke=1)
            _text(c, label, xx + 7, y - 55, colw - 18, size=8.6, bold=True, max_lines=2)
            xx += colw

    elif rep_id in {"MYSTERY_OBJECT_PLANNER", "TRAVEL_BLOGGER_PLANNER", "STANZA_MEANING_MAP", "MULTI_CLUE_TABLE"}:
        labels = {
            "MYSTERY_OBJECT_PLANNER": ["What did I find?", "What is it like?", "Made of / from?", "Used for?"],
            "TRAVEL_BLOGGER_PLANNER": ["Opening", "What I see", "Zoom in", "How I feel"],
            "STANZA_MEANING_MAP": ["Stanza 1", "Stanza 2", "Stanza 3", "Stanza 4"],
            "MULTI_CLUE_TABLE": ["Clue 1", "Clue 2", "What the clues show together", "My answer"],
        }[rep_id]
        yy = y - 48
        for label in labels:
            c.setFillColor(WHITE)
            c.setStrokeColor(BORDER)
            c.roundRect(x + 14, yy - 24, w - 28, 29, 5, fill=1, stroke=1)
            _text(c, label, x + 22, yy - 6, w - 44, size=8.8, bold=True)
            yy -= 31

    elif rep_id == "WRITING_CHECKLIST":
        criteria = p.get("criteria") or []
        yy = y - 47
        for criterion in criteria[:6]:
            yy = _text(c, f"□ {criterion}", x + 18, yy, w - 36, size=9.4, leading=17)

    else:
        _text(c, "Use this visual to organise your thinking.", x + 16, y - 45, w - 32, size=9.5)

    return y - h - 8


def _study_page(c: canvas.Canvas, page: Mapping[str, Any], page_no: int) -> None:
    y = _header(c, page["title"], page.get("prompt"), page_no)
    reps = page.get("representations") or []
    rendered = 0
    for rep in reps:
        h = _rep_height(rep["representation_id"])
        if rendered >= 2 or y - h < 320:
            break
        y = _render_rep(c, rep, M, y, W - 2 * M)
        rendered += 1

    if page.get("source_boundary_required") and y > 275:
        _card(c, M, y, W - 2 * M, 62, PALE_YELLOW, "Stop and check the worksheet model")
        note = (page.get("ambiguity") or ["This word does not fit cleanly into the printed categories."])[0]
        _text(c, note, M + 14, y - 38, W - 2 * M - 28, size=9.2, leading=12, max_lines=2)
        y -= 72

    support = page.get("support") or {}
    if y > 215:
        _card(c, M, y, W - 2 * M, 112, PALE_PURPLE, "Need a clue?")
        yy = y - 34
        for key in ("H1", "H2"):
            hint = support.get(key) or {}
            yy = _text(c, f"{hint.get('child_label', key)}: {hint.get('prompt', '')}", M + 14, yy, W - 2 * M - 28, size=8.9, leading=11, bold=(key == "H1")) - 3
        h3 = support.get("H3") or {}
        _text(c, f"{h3.get('child_label', 'PICTURE IT')}: use {h3.get('representation_ref', '').replace('_', ' ').title()}", M + 14, yy, W - 2 * M - 28, size=8.9, leading=11)
        y -= 122

    retry = page.get("fresh_retry") or {}
    if y > 88:
        _card(c, M, y, W - 2 * M, 64, PALE_GREEN, "Fresh try — no hint")
        _text(c, retry.get("prompt", ""), M + 14, y - 35, W - 2 * M - 28, size=9.2, leading=12, max_lines=3)


def _workbook_page(c: canvas.Canvas, page: Mapping[str, Any], page_no: int) -> None:
    y = _header(c, page["title"], page.get("prompt"), page_no)
    reps = page.get("representations") or []
    if reps:
        y = _render_rep(c, reps[0], M, y, W - 2 * M)

    work_h = 105 if y > 390 else 82
    _card(c, M, y, W - 2 * M, work_h, WHITE, "Your work")
    line_count = 4 if work_h >= 100 else 3
    for i in range(line_count):
        c.setStrokeColor(BORDER)
        c.line(M + 16, y - 40 - i * 19, W - M - 16, y - 40 - i * 19)
    y -= work_h + 10

    support = page.get("support") or {}
    if y > 185:
        _card(c, M, y, W - 2 * M, 88, PALE_PURPLE, "Need a clue? Use only as much help as you need")
        yy = y - 32
        for key in ("H1", "H2"):
            hint = support.get(key) or {}
            yy = _text(c, f"{hint.get('child_label', key)}: {hint.get('prompt', '')}", M + 14, yy, W - 2 * M - 28, size=8.6, leading=11) - 3
        y -= 98

    retry = page.get("fresh_retry") or {}
    if y > 88:
        _card(c, M, y, W - 2 * M, 62, PALE_GREEN, "Try a new one by yourself")
        _text(c, retry.get("prompt", ""), M + 14, y - 34, W - 2 * M - 28, size=9.0, leading=11, max_lines=3)


def _teacher_page(c: canvas.Canvas, page: Mapping[str, Any], page_no: int) -> None:
    y = _header(c, page["title"], page.get("prompt"), page_no)
    response = page.get("response_demand") or {}

    _card(c, M, y, W - 2 * M, 96, PALE_BLUE, "What useful evidence looks like")
    yy = y - 35
    parts = page.get("expected_evidence") or page.get("rubric_criteria") or [response.get("response_structure_ref", "Use the response structure")]
    for item in parts[:5]:
        yy = _text(c, f"• {item}", M + 14, yy, W - 2 * M - 28, size=9.1, leading=12)
    y -= 106

    watches = page.get("misconception_watches") or []
    if watches:
        _card(c, M, y, W - 2 * M, 102, PALE_YELLOW, "If the same error repeats")
        yy = y - 35
        for item in watches[:4]:
            yy = _text(c, f"• {str(item).replace('_', ' ').title()}", M + 14, yy, W - 2 * M - 28, size=8.9, leading=12)
        y -= 112

    if page.get("source_boundary_required"):
        _card(c, M, y, W - 2 * M, 72, PALE_PURPLE, "Source boundary")
        note = (page.get("ambiguity") or ["Do not force-fit an unsupported category."])[0]
        _text(c, note, M + 14, y - 37, W - 2 * M - 28, size=8.9, leading=12, max_lines=2)
        y -= 82

    support = page.get("support") or {}
    if y > 145:
        _card(c, M, y, W - 2 * M, 120, PALE_GREEN, "Support, then fade")
        yy = y - 34
        for key in ("H1", "H2"):
            hint = support.get(key) or {}
            yy = _text(c, f"{key}: {hint.get('prompt', '')}", M + 14, yy, W - 2 * M - 28, size=8.7, leading=11) - 3
        retry = support.get("fresh_retry") or {}
        _text(c, f"Fresh H0 retry: {retry.get('prompt', '')}", M + 14, yy, W - 2 * M - 28, size=8.7, leading=11, bold=True, max_lines=3)


def render_publication_model(model: Mapping[str, Any], output_pdf_path: Path) -> Mapping[str, Any]:
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_pdf_path), pagesize=A4)
    for index, page in enumerate(model["pages"], start=1):
        if page["kind"] == "COVER":
            _cover(c, page, index)
        elif page["kind"] == "STUDY":
            _study_page(c, page, index)
        elif page["kind"] == "WORKBOOK":
            _workbook_page(c, page, index)
        elif page["kind"] == "TEACHER_KEY":
            _teacher_page(c, page, index)
        else:
            raise ValueError(f"unsupported publication page kind: {page['kind']}")
        c.showPage()
    c.save()
    return {"path": str(output_pdf_path), "page_count": len(model["pages"]), "document_kind": model["document_kind"]}
