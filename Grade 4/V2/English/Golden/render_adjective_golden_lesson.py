#!/usr/bin/env python3
"""Render the Grade 4 English adjective golden child-facing lesson PDF."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "adjective-golden-lesson.v1.draft.json"
DEFAULT_OUT = ROOT / "adjective-golden-lesson.v1.draft.pdf"

PAGE_W, PAGE_H = A4

INK = colors.HexColor("#243043")
MUTED = colors.HexColor("#5B6573")
LINE = colors.HexColor("#D9DEE7")
PALE = colors.HexColor("#F5F7FA")
BLUE = colors.HexColor("#DDEBFF")
GREEN = colors.HexColor("#E4F4E9")
YELLOW = colors.HexColor("#FFF2C8")
PINK = colors.HexColor("#FBE4EA")
STAR_FILL = colors.HexColor("#FFE17A")
WHITE = colors.white

CATEGORY_FILLS = [BLUE, PINK, GREEN, YELLOW, BLUE, PINK, GREEN, YELLOW, BLUE]


def draw_star(c, cx, cy, r_outer=8, r_inner=3.5, fill=STAR_FILL):
    pts = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    path = c.beginPath()
    path.moveTo(*pts[0])
    for pt in pts[1:]:
        path.lineTo(*pt)
    path.close()
    c.setFillColor(fill)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.drawPath(path, fill=1, stroke=1)


def para(c, text, x, y_top, width, font_size=11, leading=None, bold=False, color=INK, align=TA_LEFT):
    style = ParagraphStyle(
        name="p",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=font_size,
        leading=leading or font_size * 1.28,
        textColor=color,
        alignment=align,
        spaceAfter=0,
    )
    p = Paragraph(text, style)
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y_top - h)
    return h


def rounded_box(c, x, y, w, h, fill=WHITE, stroke=LINE, radius=8, line_width=1):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(line_width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def page_header(c, spec, page, page_no, margin_l, margin_r, top):
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin_l, top, page["page_role"].replace("_", " "))
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - margin_r, top, f"Adjectives - {page_no}/{len(spec['pages'])}")

    title_y = top - 14
    h = para(c, page["title"], margin_l, title_y, PAGE_W - margin_l - margin_r, font_size=22, leading=25, bold=True)
    goal_y = title_y - h - 8
    h2 = para(c, page["goal"], margin_l, goal_y, PAGE_W - margin_l - margin_r, font_size=12, leading=15, color=MUTED)
    return goal_y - h2 - 14


def footer(c, margin_l, margin_r, bottom):
    c.setStrokeColor(LINE)
    c.line(margin_l, bottom + 16, PAGE_W - margin_r, bottom + 16)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(margin_l, bottom + 5, "Find -> Classify -> Star extra words -> Order -> Read aloud")


def response_lines(c, x, y_top, w, count, gap=20):
    c.setStrokeColor(colors.HexColor("#AEB7C3"))
    c.setLineWidth(0.8)
    for i in range(count):
        y = y_top - i * gap
        c.line(x, y, x + w, y)


def draw_action(c, page, x, y, w):
    action = page["action"]
    space = action.get("response_space", "NONE")
    heights = {"NONE": 54, "SMALL": 82, "MEDIUM": 112, "LARGE": 148, "FULL_WIDTH": 180, "HALF_PAGE": 220}
    h = heights[space]
    rounded_box(c, x, y - h, w, h, fill=colors.HexColor("#FCFCFD"), stroke=colors.HexColor("#B9C2CE"), radius=10, line_width=1.2)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 12, y - 20, "YOUR TURN")
    text_y = y - 34
    used = para(c, action["instruction"], x + 12, text_y, w - 24, font_size=12, leading=15, bold=True)
    cursor = text_y - used - 8

    if "prompt" in action:
        para(c, f"<b>{action['prompt']}</b>", x + 12, cursor, w - 24, font_size=14, leading=17)
        cursor -= 28
    if "items" in action:
        text = "   /   ".join(action["items"])
        para(c, f"<b>{text}</b>" + (f"   +   <b>{action['noun']}</b>" if action.get("noun") else ""), x + 12, cursor, w - 24, font_size=13, leading=16)
        cursor -= 30

    if space == "SMALL":
        response_lines(c, x + 14, y - h + 24, w - 28, 1)
    elif space == "MEDIUM":
        response_lines(c, x + 14, y - h + 56, w - 28, 3)
    elif space == "LARGE":
        response_lines(c, x + 14, y - h + 78, w - 28, 4)
    elif space == "HALF_PAGE":
        response_lines(c, x + 14, y - h + 150, w - 28, 7, gap=19)
    return h


def draw_noun_phrase_builder(c, visual, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(MUTED)
    c.drawString(x + 14, y - 22, "NOUN PHRASE BUILDER")
    words = visual["phrase"].split()
    total = sum(stringWidth(word, "Helvetica-Bold", 20) + 18 for word in words)
    cx = x + (w - total) / 2
    cy = y - 80
    for word in words:
        is_noun = word == visual["noun"]
        bw = stringWidth(word, "Helvetica-Bold", 20) + 18
        rounded_box(c, cx, cy - 20, bw, 42, fill=GREEN if is_noun else BLUE, stroke=LINE, radius=8)
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(INK)
        c.drawCentredString(cx + bw / 2, cy - 4, word)
        c.setFont("Helvetica", 9)
        c.setFillColor(MUTED)
        c.drawCentredString(cx + bw / 2, cy - 16, "NOUN" if is_noun else "DESCRIBING WORD")
        cx += bw + 8


def draw_category_cards(c, spec, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    cards = spec["category_cards"]
    cols = 3
    gap = 8
    card_w = (w - 28 - gap * (cols - 1)) / cols
    card_h = 58
    start_x = x + 14
    start_y = y - 16
    for i, card in enumerate(cards):
        row = i // cols
        col = i % cols
        bx = start_x + col * (card_w + gap)
        by = start_y - row * (card_h + gap) - card_h
        rounded_box(c, bx, by, card_w, card_h, fill=CATEGORY_FILLS[i], stroke=colors.HexColor("#CAD1DA"), radius=8)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(bx + 9, by + card_h - 18, card["label"])
        para(c, card["question"], bx + 9, by + card_h - 25, card_w - 18, font_size=10.5, leading=12.8, color=MUTED)


def draw_order_train(c, spec, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    cards = spec["category_cards"]
    car_w = (w - 30) / 3
    car_h = 42
    gap_y = 8
    for i, card in enumerate(cards):
        row = i // 3
        col = i % 3
        bx = x + 10 + col * car_w
        by = y - 18 - row * (car_h + gap_y) - car_h
        rounded_box(c, bx, by, car_w - 7, car_h, fill=CATEGORY_FILLS[i], stroke=colors.HexColor("#CAD1DA"), radius=7)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(bx + (car_w - 7) / 2, by + 22, f"{i+1}. {card['label']}")
        if col < 2:
            c.setStrokeColor(MUTED)
            c.line(bx + car_w - 4, by + 21, bx + car_w + 2, by + 21)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(x + w - 14, y - h + 12, "... then NOUN")


def draw_classify_and_order(c, visual, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    para(c, "Start with the scrambled words:", x + 14, y - 16, w - 28, font_size=10.5, bold=True)
    para(c, "  /  ".join(visual["scrambled"]) + f"  +  {visual['noun']}", x + 14, y - 38, w - 28, font_size=14, bold=True)
    mapping = [("fascinating", "Opinion"), ("new", "Age"), ("round", "Shape"), ("plastic", "Material")]
    cy = y - 78
    for i, (word, cat) in enumerate(mapping):
        bx = x + 14 + (i % 2) * (w / 2 - 8)
        by = cy - (i // 2) * 44
        rounded_box(c, bx, by - 28, w / 2 - 22, 32, fill=[PINK, YELLOW, GREEN, BLUE][i], stroke=LINE, radius=6)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(bx + 8, by - 8, word)
        c.setFont("Helvetica", 9.5)
        c.drawRightString(bx + w / 2 - 32, by - 8, cat)
    phrase = " ".join([*visual["ordered"], visual["noun"]])
    para(c, f"<b>Whole phrase:</b> {phrase}", x + 14, y - h + 30, w - 28, font_size=13, leading=16)


def draw_boundary_phrase(c, visual, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 14, y - 20, "BOOK BOXES + STAR WORD")
    items = visual["items"]
    gap = 7
    box_w = (w - 28 - gap * (len(items) - 1)) / len(items)
    by = y - 82
    for i, item in enumerate(items):
        bx = x + 14 + i * (box_w + gap)
        if item.get("boundary"):
            rounded_box(c, bx, by - 26, box_w, 52, fill=WHITE, stroke=colors.HexColor("#D7B62A"), radius=8, line_width=1.5)
            draw_star(c, bx + box_w / 2, by + 8, 7.5, 3.3)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(bx + box_w / 2, by - 9, item["word"])
            c.setFont("Helvetica", 9.2)
            c.setFillColor(MUTED)
            c.drawCentredString(bx + box_w / 2, by - 21, "EXTRA DESCRIBING WORD")
        else:
            idx = ["NUMBER", "OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL", "PURPOSE"].index(item["category"])
            rounded_box(c, bx, by - 26, box_w, 52, fill=CATEGORY_FILLS[idx], stroke=LINE, radius=8)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(bx + box_w / 2, by + 2, item["word"])
            c.setFont("Helvetica", 9.2)
            c.setFillColor(MUTED)
            c.drawCentredString(bx + box_w / 2, by - 15, item["category"].title())
    phrase = " ".join([*visual["ordered"], visual["noun"]])
    rounded_box(c, x + 14, y - h + 18, w - 28, 46, fill=WHITE, stroke=colors.HexColor("#B9C2CE"), radius=7)
    para(c, f"<b>Whole phrase:</b> {phrase}", x + 26, y - h + 52, w - 52, font_size=13, leading=16)


def draw_practice_phrase(c, visual, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    para(c, "Words to sort:", x + 14, y - 16, w - 28, font_size=10.5, bold=True)
    para(c, "  /  ".join(visual["scrambled"]) + f"  +  {visual['noun']}", x + 14, y - 40, w - 28, font_size=15, bold=True)
    para(c, "Use the box questions. Put a star beside any word with no book box.", x + 14, y - 72, w - 28, font_size=10.5, leading=13, color=MUTED)
    for i, word in enumerate(visual["scrambled"]):
        bx = x + 14 + (i % 2) * (w / 2 - 8)
        by = y - 110 - (i // 2) * 46
        rounded_box(c, bx, by - 28, w / 2 - 22, 34, fill=WHITE, stroke=LINE, radius=6)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(INK)
        c.drawString(bx + 9, by - 9, word)
        c.setStrokeColor(colors.HexColor("#AEB7C3"))
        c.line(bx + 88, by - 10, bx + w / 2 - 34, by - 10)


def draw_routine_strip(c, visual, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    steps = visual["steps"]
    gap = 7
    bw = (w - 28 - gap * (len(steps) - 1)) / len(steps)
    by = y - 78
    for i, step in enumerate(steps):
        bx = x + 14 + i * (bw + gap)
        rounded_box(c, bx, by - 30, bw, 58, fill=[BLUE, GREEN, YELLOW, PINK][i % 4], stroke=LINE, radius=8)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(INK)
        c.drawCentredString(bx + bw / 2, by + 5, str(i + 1))
        para(c, step, bx + 6, by - 4, bw - 12, font_size=10.5, leading=12.5, bold=True, align=TA_CENTER)


def draw_review_checklist(c, visual, x, y, w, h):
    rounded_box(c, x, y - h, w, h, fill=PALE)
    steps = visual["steps"]
    cy = y - 28
    for step in steps:
        c.setStrokeColor(colors.HexColor("#8F9AA8"))
        c.rect(x + 18, cy - 9, 10, 10, fill=0, stroke=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x + 38, cy - 7, step)
        cy -= 28


def draw_visual(c, spec, page, x, y, w, h):
    visual = page["instructional_visual"]
    kind = visual["type"]
    if kind == "NOUN_PHRASE_BUILDER":
        draw_noun_phrase_builder(c, visual, x, y, w, h)
    elif kind == "CATEGORY_CARDS":
        draw_category_cards(c, spec, x, y, w, h)
    elif kind == "ORDER_TRAIN":
        draw_order_train(c, spec, x, y, w, h)
    elif kind == "CLASSIFY_AND_ORDER":
        draw_classify_and_order(c, visual, x, y, w, h)
    elif kind == "BOUNDARY_PHRASE":
        draw_boundary_phrase(c, visual, x, y, w, h)
    elif kind == "PRACTICE_PHRASE":
        draw_practice_phrase(c, visual, x, y, w, h)
    elif kind == "ROUTINE_STRIP":
        draw_routine_strip(c, visual, x, y, w, h)
    elif kind == "REVIEW_CHECKLIST":
        draw_review_checklist(c, visual, x, y, w, h)
    else:
        raise ValueError(f"Unknown visual type: {kind}")


def render(spec_path: Path, out_path: Path):
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    profile = spec["output_profile"]
    margin_l = profile["margin_inner_mm"] * mm
    margin_r = profile["margin_outer_mm"] * mm
    margin_t = profile["margin_top_mm"] * mm
    margin_b = profile["margin_bottom_mm"] * mm
    usable_w = PAGE_W - margin_l - margin_r

    c = canvas.Canvas(str(out_path), pagesize=A4)
    c.setTitle("Grade 4 English - Adjective Golden Lesson V1 Draft")
    c.setAuthor("Grade 4 English draft publishing fixture")

    for page_no, page in enumerate(spec["pages"], 1):
        c.setFillColor(WHITE)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        top = PAGE_H - margin_t + 3
        content_top = page_header(c, spec, page, page_no, margin_l, margin_r, top)

        chunks = page.get("explanation_chunks", [])
        cursor = content_top
        if chunks:
            rounded_box(c, margin_l, cursor - 54, usable_w, 54, fill=WHITE, stroke=LINE, radius=8)
            if len(chunks) == 1:
                para(c, chunks[0], margin_l + 12, cursor - 13, usable_w - 24, font_size=10.8, leading=13.5)
            else:
                text = " &nbsp;&nbsp; ".join(f"<b>{i+1}.</b> {chunk}" for i, chunk in enumerate(chunks))
                para(c, text, margin_l + 12, cursor - 10, usable_w - 24, font_size=10.5, leading=13.1)
            cursor -= 66

        visual_h = 194 if page["instructional_visual"]["type"] not in {"CATEGORY_CARDS", "ORDER_TRAIN"} else 220
        draw_visual(c, spec, page, margin_l, cursor, usable_w, visual_h)
        cursor -= visual_h + 14

        remaining = cursor - (margin_b + 24)
        action_h_target = {"NONE": 54, "SMALL": 82, "MEDIUM": 112, "LARGE": 148, "FULL_WIDTH": 180, "HALF_PAGE": 220}[page["action"]["response_space"]]
        if remaining < action_h_target:
            # Keep the page readable instead of shrinking type to force a fit.
            action_h_target = max(remaining, 70)
        draw_action(c, page, margin_l, cursor, usable_w)
        footer(c, margin_l, margin_r, margin_b - 2)
        c.showPage()

    c.save()


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    render(SPEC_PATH, out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
