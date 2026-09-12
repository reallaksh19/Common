"""Document-level English V2 StudyJourney publisher.

The composer consumes StudyJourneyPlan in authored block order. It may paginate,
style and realize a declared representation_ref; it may not invent teaching
content, examples, hints, rubrics or source categories.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

import sys

STUDY_ENGINE = Path(__file__).resolve().parents[2] / "StudyDesign" / "engine"
if str(STUDY_ENGINE) not in sys.path:
    sys.path.insert(0, str(STUDY_ENGINE))
from study_journey import validate_study_journey  # type: ignore  # noqa: E402

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
PALE_PINK = colors.HexColor("#FFF0EC")
WHITE = colors.white

BLOCK_STYLE = {
    "NAVIGATION": (PALE_BLUE, colors.HexColor("#5A8FC8")),
    "CONCEPT": (PALE_BLUE, colors.HexColor("#4A82C2")),
    "SOURCE_RULE": (PALE_YELLOW, colors.HexColor("#C39A18")),
    "VOCABULARY": (PALE_BLUE, colors.HexColor("#4A82C2")),
    "TEXT_ANALYSIS": (PALE_BLUE, colors.HexColor("#4A82C2")),
    "READING_ROUTINE": (PALE_PURPLE, PURPLE),
    "SOURCE_BOUNDARY": (PALE_YELLOW, colors.HexColor("#C39A18")),
    "WORKED_EXAMPLE": (PALE_GREEN, colors.HexColor("#2F8D70")),
    "ANNOTATED_MODEL": (PALE_GREEN, colors.HexColor("#2F8D70")),
    "CONTRAST": (PALE_PINK, colors.HexColor("#D66A57")),
    "MISCONCEPTION_CHECK": (PALE_PINK, colors.HexColor("#D66A57")),
    "GUIDED_PRACTICE": (PALE_PURPLE, PURPLE),
    "HINT_LADDER": (PALE_PURPLE, PURPLE),
    "DIAGNOSTIC_PROBE": (PALE_YELLOW, colors.HexColor("#C39A18")),
    "INDEPENDENT_RETRY": (WHITE, NAVY),
    "TRANSFER": (WHITE, NAVY),
    "RETRIEVAL": (WHITE, NAVY),
    "RUBRIC": (PALE_GREEN, colors.HexColor("#2F8D70")),
    "ANSWER_CHECK": (PALE_GREEN, colors.HexColor("#2F8D70")),
    "REFERENCE": (PALE_BLUE, colors.HexColor("#4A82C2")),
    "SELF_CHECK": (PALE_GREEN, colors.HexColor("#2F8D70")),
}


def _wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = str(text or "").split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines or [""]


def _paragraph(c: canvas.Canvas, text: str, x: float, y: float, width: float, *, size: float = 10.5, leading: float = 14, bold: bool = False, color=NAVY) -> float:
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size); c.setFillColor(color)
    for line in _wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def _rep(c: canvas.Canvas, rep: str | None, params: Mapping[str, Any], x: float, y: float, w: float, h: float) -> None:
    if not rep:
        return
    c.setFillColor(colors.HexColor("#FBFDFF")); c.setStrokeColor(BORDER)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x + 10, y + h - 16, rep.replace("_", " ").title())

    if rep == "ADJECTIVE_ORDER_TRAIN":
        order = list(params.get("ordering") or ["OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL", "NOUN"])
        bw = (w - 20) / max(1, len(order))
        for i, label in enumerate(order):
            bx = x + 10 + i * bw
            c.setFillColor(PALE_PURPLE); c.setStrokeColor(BORDER)
            c.roundRect(bx, y + 20, bw - 4, 28, 5, fill=1, stroke=1)
            c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 6.4)
            c.drawCentredString(bx + (bw - 4) / 2, y + 36, str(label).title())
        return
    if rep in {"ANSWER_CLUE_CONNECTION", "TRANSFER_THREAT_ACTION_TABLE", "CHOICE_REASON_FRAME", "TEXT_VS_MY_THINKING", "CAUSE_EFFECT_CHAIN"}:
        labels = {
            "ANSWER_CLUE_CONNECTION": ["Answer", "Text clue", "Connection"],
            "TRANSFER_THREAT_ACTION_TABLE": ["Species", "Threat", "Action to help"],
            "CHOICE_REASON_FRAME": ["My choice", "Why it matters"],
            "TEXT_VS_MY_THINKING": ["What the text says", "My thinking / knowledge"],
            "CAUSE_EFFECT_CHAIN": ["Cause", "What changes", "Effect"],
        }[rep]
        bw = (w - 20) / len(labels)
        for i, label in enumerate(labels):
            bx = x + 10 + i * bw
            c.setFillColor(PALE_BLUE); c.setStrokeColor(BORDER)
            c.roundRect(bx, y + 18, bw - 5, 34, 5, fill=1, stroke=1)
            _paragraph(c, label, bx + 6, y + 39, bw - 17, size=7.8, leading=9, bold=True)
        return
    if rep in {"MYSTERY_OBJECT_PLANNER", "TRAVEL_BLOGGER_PLANNER", "STANZA_MEANING_MAP", "MULTI_CLUE_TABLE", "CATEGORY_SORT_TABLE"}:
        labels = {
            "MYSTERY_OBJECT_PLANNER": ["Object", "Useful details", "Made of / from", "Possible use"],
            "TRAVEL_BLOGGER_PLANNER": ["Opening", "What I see", "Zoom in", "How I feel"],
            "STANZA_MEANING_MAP": ["Part 1", "Part 2", "Part 3", "Part 4"],
            "MULTI_CLUE_TABLE": ["Clue 1", "Clue 2", "Together they show", "My answer"],
            "CATEGORY_SORT_TABLE": ["Opinion", "Size", "Age", "Shape", "Colour", "Origin", "Material"],
        }[rep]
        bw = (w - 20) / len(labels)
        for i, label in enumerate(labels):
            bx = x + 10 + i * bw
            c.setStrokeColor(BORDER); c.setFillColor(WHITE)
            c.rect(bx, y + 16, bw - 4, 42, fill=1, stroke=1)
            c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 6.6)
            c.drawCentredString(bx + (bw - 4) / 2, y + 44, label)
        return
    if rep == "CONTRAST_PAIR":
        contrasts = list(params.get("contrasts") or [["A", "B"]])
        yy = y + h - 34
        for pair in contrasts[:2]:
            _paragraph(c, f"{pair[0]}   ↔   {pair[1]}", x + 16, yy, w - 32, size=10, bold=True)
            yy -= 24
        return
    if rep in {"ADJECTIVE_FAMILY_CARDS", "NOUN_PHRASE_BUILDER", "WRITING_CHECKLIST"}:
        labels = {
            "ADJECTIVE_FAMILY_CARDS": ["Opinion", "Size", "Age", "Shape", "Colour", "Origin", "Material"],
            "NOUN_PHRASE_BUILDER": ["describing word", "describing word", "noun"],
            "WRITING_CHECKLIST": ["opening", "6+ adjectives", "visible details", "correct order"],
        }[rep]
        bw = (w - 20) / len(labels)
        for i, label in enumerate(labels):
            bx = x + 10 + i * bw
            c.setFillColor(PALE_BLUE); c.setStrokeColor(BORDER)
            c.roundRect(bx, y + 20, bw - 4, 28, 5, fill=1, stroke=1)
            c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 6.6)
            c.drawCentredString(bx + (bw - 4) / 2, y + 36, label)
        return

    _paragraph(c, "Use this thinking tool to organise the idea.", x + 14, y + h - 38, w - 28, size=9.2)


class EnglishStudyJourneyComposer:
    """Render authored StudyJourney blocks without authoring missing pedagogy."""

    def render(self, plan: Mapping[str, Any], output_pdf_path: Path, *, audience: str = "STUDENT") -> Tuple[str, Mapping[str, Any]]:
        validation = validate_study_journey(plan)
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(output_pdf_path), pagesize=A4)
        page_count = 0
        rendered_blocks = 0

        def new_page(object_title: str, object_index: int, continued: bool = False) -> float:
            nonlocal page_count
            if page_count:
                c.showPage()
            page_count += 1
            c.setFillColor(PURPLE); c.roundRect(M, H - 120, W - 2 * M, 70, 18, fill=1, stroke=0)
            label = f"{object_index}. {object_title}" + (" — continued" if continued else "")
            _paragraph(c, label, M + 18, H - 82, W - 2 * M - 36, size=18, leading=20, bold=True, color=WHITE)
            c.setFillColor(MUTED); c.setFont("Helvetica", 8); c.drawRightString(W - M, 20, str(page_count))
            return H - 140

        for object_index, obj in enumerate(plan["learning_objects"], start=1):
            cur = new_page(str(obj["title"]), object_index)
            c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 8.5); c.drawString(M, cur, "LEARNING GOAL")
            cur = _paragraph(c, str(obj["learning_goal"]), M, cur - 16, W - 2 * M, size=11.2, leading=15) - 12

            for block in obj["blocks"]:
                block_audience = str(block["audience"])
                if audience == "STUDENT" and block_audience == "ADULT":
                    continue
                if audience == "ADULT" and block_audience == "STUDENT":
                    continue

                btype = str(block["block_type"])
                fill, accent = BLOCK_STYLE[btype]
                body = str(block.get("body") or "")
                prompt = str(block.get("learner_prompt") or "")
                solution = str(block.get("solution_text") or "")
                rep = block.get("representation_ref")
                params = block.get("semantic_params") or {}
                visibility = str(block.get("answer_visibility") or "HIDDEN")

                text_lines = len(_wrap(body, "Helvetica", 10.2, W - 2 * M - 28))
                prompt_lines = len(_wrap(prompt, "Helvetica", 10.2, W - 2 * M - 28)) if prompt else 0
                sol_lines = len(_wrap(solution, "Helvetica", 10.0, W - 2 * M - 28)) if solution and visibility in {"WORKED_EXAMPLE", "ANSWER_KEY_ONLY"} else 0
                rep_h = 82 if rep else 0
                response_h = 65 if btype in {"GUIDED_PRACTICE", "INDEPENDENT_RETRY", "TRANSFER", "RETRIEVAL"} else 0
                block_h = 58 + text_lines * 14 + prompt_lines * 14 + sol_lines * 14 + rep_h + response_h
                block_h = max(block_h, 112)

                if cur - block_h < 55:
                    cur = new_page(str(obj["title"]), object_index, True)

                y = cur - block_h
                c.setFillColor(fill); c.setStrokeColor(accent); c.roundRect(M, y, W - 2 * M, block_h, 9, fill=1, stroke=1)
                c.setFillColor(accent); c.setFont("Helvetica-Bold", 8.2); c.drawString(M + 14, cur - 19, btype.replace("_", " "))
                c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 13.2); c.drawString(M + 14, cur - 39, str(block["title"]))
                tcur = cur - 55
                if body:
                    tcur = _paragraph(c, body, M + 14, tcur, W - 2 * M - 28, size=10.2, leading=14) - 5
                if prompt:
                    c.setFillColor(accent); c.setFont("Helvetica-Bold", 8.5); c.drawString(M + 14, tcur, "YOUR TURN")
                    tcur = _paragraph(c, prompt, M + 14, tcur - 14, W - 2 * M - 28, size=10.2, leading=14) - 5
                if solution and visibility == "WORKED_EXAMPLE":
                    c.setFillColor(accent); c.setFont("Helvetica-Bold", 8.5); c.drawString(M + 14, tcur, "WORKED THINKING")
                    tcur = _paragraph(c, solution, M + 14, tcur - 14, W - 2 * M - 28, size=10.0, leading=13) - 5
                if rep:
                    ry = y + response_h + 10
                    _rep(c, str(rep), params, M + 14, ry, W - 2 * M - 28, rep_h - 14)
                if response_h:
                    c.setFillColor(WHITE); c.setStrokeColor(BORDER)
                    c.roundRect(M + 14, y + 10, W - 2 * M - 28, response_h - 18, 6, fill=1, stroke=1)
                    c.setFillColor(MUTED); c.setFont("Helvetica", 8.2)
                    c.drawString(M + 24, y + response_h - 27, "Write / draw your thinking here")
                    for i in range(2):
                        c.line(M + 24, y + 24 + i * 15, W - M - 24, y + 24 + i * 15)

                rendered_blocks += 1
                cur = y - 12

        c.save()
        return str(output_pdf_path), {
            "journey_id": plan["journey_id"],
            "validation": validation,
            "audience": audience,
            "page_count": page_count,
            "rendered_block_count": rendered_blocks,
            "publisher_invention_allowed": False,
        }


def render_study_journey(plan: Mapping[str, Any], output_pdf_path: Path, *, audience: str = "STUDENT") -> Tuple[str, Mapping[str, Any]]:
    return EnglishStudyJourneyComposer().render(plan, output_pdf_path, audience=audience)
