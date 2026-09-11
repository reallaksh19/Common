#!/usr/bin/env python3
"""Render the canonical ALG-03 student pack and teacher key."""

from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Spacer,
    Table, TableStyle, KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PDFs"
STUDENT = OUT / "ALG03_Student_Pack_v1.pdf"
TEACHER = OUT / "ALG03_Teacher_Key_v1.pdf"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DV", FONT))
pdfmetrics.registerFont(TTFont("DV-Bold", FONT_BOLD))


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="DV-Bold", fontSize=22,
                                leading=27, textColor=colors.HexColor("#183153"), alignment=TA_CENTER,
                                spaceAfter=12),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName="DV", fontSize=11,
                                   leading=16, textColor=colors.HexColor("#49627A"), alignment=TA_CENTER),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="DV-Bold", fontSize=16,
                             leading=20, textColor=colors.HexColor("#183153"), spaceBefore=8, spaceAfter=7),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="DV-Bold", fontSize=12.5,
                             leading=16, textColor=colors.HexColor("#176B87"), spaceBefore=7, spaceAfter=4),
        "h3": ParagraphStyle("h3", parent=base["Heading3"], fontName="DV-Bold", fontSize=10.5,
                             leading=14, textColor=colors.HexColor("#2D4356"), spaceBefore=5, spaceAfter=3),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="DV", fontSize=8.4,
                               leading=11.2, textColor=colors.HexColor("#202A33"), spaceAfter=3.5),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName="DV", fontSize=8.2,
                                 leading=10.8, leftIndent=10, firstLineIndent=-6, spaceAfter=2.5),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="DV", fontSize=7.2,
                                leading=9.2, textColor=colors.HexColor("#425466")),
    }


S = styles()


def inline(text):
    text = html.escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"<font name='DV-Bold'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    return text


def markdown_story(path, start_h1_on_new_page=False):
    lines = path.read_text(encoding="utf-8").splitlines()
    story, para, table = [], [], []

    def flush_para():
        if para:
            story.append(Paragraph(inline(" ".join(para)), S["body"]))
            para.clear()

    def flush_table():
        if not table:
            return
        rows = [[Paragraph(inline(c), S["small"]) for c in row] for row in table
                if not all(set(c.strip()) <= {"-", ":"} for c in row)]
        if rows:
            widths = [(A4[0] - 36 * mm) / max(len(r) for r in rows)] * max(len(r) for r in rows)
            t = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F3F7")),
                ("FONTNAME", (0, 0), (-1, 0), "DV-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B7C9D6")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(KeepTogether([t, Spacer(1, 4)]))
        table.clear()

    first_h1 = True
    in_code = False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            flush_para(); flush_table(); in_code = not in_code; continue
        if in_code:
            story.append(Paragraph(inline(line) or "&#160;", S["small"])); continue
        if line.startswith("|") and line.endswith("|"):
            flush_para(); table.append([x.strip() for x in line.strip("|").split("|")]); continue
        flush_table()
        if not line.strip():
            flush_para(); continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            flush_para()
            level, title = len(m.group(1)), m.group(2)
            if level == 1 and start_h1_on_new_page and not first_h1:
                story.append(PageBreak())
            story.append(Paragraph(inline(title), S[f"h{level}"]))
            first_h1 = False
        elif re.match(r"^[-*]\s+", line):
            flush_para(); story.append(Paragraph("• " + inline(re.sub(r"^[-*]\s+", "", line)), S["bullet"]))
        elif re.match(r"^\d+[.)]\s+", line):
            flush_para(); story.append(Paragraph(inline(line), S["bullet"]))
        elif line.startswith("---"):
            flush_para(); story.append(Spacer(1, 5))
        else:
            para.append(line)
    flush_para(); flush_table()
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D6E1E8")); canvas.line(18 * mm, 13 * mm, A4[0] - 18 * mm, 13 * mm)
    canvas.setFont("DV", 7); canvas.setFillColor(colors.HexColor("#607789"))
    canvas.drawString(18 * mm, 8.5 * mm, "IOQM Grade 9 | Polynomials, Roots, Vieta & Remainders")
    canvas.drawRightString(A4[0] - 18 * mm, 8.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def deterministic_canvas(*args, **kwargs):
    kwargs["invariant"] = 1
    return Canvas(*args, **kwargs)


def build(path, title, subtitle, sources):
    doc = BaseDocTemplate(str(path), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                          topMargin=15*mm, bottomMargin=17*mm, title=title, author="IOQM Grade 9")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(PageTemplate(id="main", frames=frame, onPage=footer))
    story = [Spacer(1, 34*mm), Paragraph(title, S["title"]), Paragraph(subtitle, S["subtitle"]),
             Spacer(1, 18*mm), Paragraph("RECONNECT → DISCOVER → MAKE SENSE → TRY → DIAGNOSE → FADE → ADOPT → TRANSFER", S["subtitle"]), PageBreak()]
    for i, src in enumerate(sources):
        if i:
            story.append(PageBreak())
        story.extend(markdown_story(ROOT / src))
    doc.build(story, canvasmaker=deterministic_canvas)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build(STUDENT, "Polynomials, Roots, Vieta & Remainders",
          "Student Assimilation Pack | Representation before calculation",
          ["02_Assimilation_Book.md", "03_First_Step_Reference.md",
           "04_Recognition_and_First_Line_Lab.md", "05_Practice_and_Transfer_Bank.md",
           "06_H0_Mastery_Test.md"])
    build(TEACHER, "Polynomials, Roots, Vieta & Remainders - Teacher Diagnostic Key",
          "Diagnostic routes, hint ladder and verified answers", ["Teacher_Diagnostic_Key.md"])


if __name__ == "__main__":
    main()
