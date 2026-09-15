"""Canonical document-level StudyJourney publisher for Grade 4 Math V2.

This composer consumes StudyJourneyPlan. It preserves block order, source
question identity, answer visibility and hint policy. Typed representations and
staged H1/H2/H3 support are measured before drawing. Publication does not infer
pedagogy and never shrinks learner text to force content into a fixed box.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from reportlab.pdfgen import canvas

from Grade4.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PageMetricsA4,
    PrimaryPalette,
    ReportLabBackend,
)
from Grade4.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive
from Grade4.V2.Mathematics.Publication.engine.custody import PublicationCustodyTracker
from Grade4.V2.Mathematics.Publication.engine.layout_measure import (
    assert_component_fits_page,
    paragraph_height,
)
from Grade4.V2.Mathematics.Publication.engine.staged_hint_layout import StagedHintComponent
from Grade4.V2.Mathematics.StudyDesign.engine.study_journey import validate_study_journey


BLOCK_STYLE = {
    "SEE_DISCOVER": (PrimaryPalette.LIGHT_BG, PrimaryPalette.ACCENT_BLUE),
    "NOTICE": (PrimaryPalette.HIGHLIGHT_YELLOW, PrimaryPalette.AMBER),
    "CONNECT": (PrimaryPalette.LIGHT_BG, PrimaryPalette.TEAL),
    "WORKED_EXAMPLE": (PrimaryPalette.LIGHT_BG, PrimaryPalette.ACCENT_BLUE),
    "GUIDED_TRY": (PrimaryPalette.LIGHT_BG, PrimaryPalette.TEAL),
    "INDEPENDENT_TRY": (PrimaryPalette.WHITE, PrimaryPalette.NAVY),
    "ERROR_ANALYSIS": (PrimaryPalette.LIGHT_BG, PrimaryPalette.AMBER),
    "TRANSFER": (PrimaryPalette.LIGHT_BG, PrimaryPalette.ACCENT_BLUE),
    "RETRIEVAL": (PrimaryPalette.WHITE, PrimaryPalette.NAVY),
    "REFERENCE": (PrimaryPalette.LIGHT_BG, PrimaryPalette.TEAL),
    "SELF_CHECK": (PrimaryPalette.WHITE, PrimaryPalette.TEAL),
}


class StudyJourneyComposer:
    HEADER_H = 54.0
    GAP = 12.0
    QUESTION_INNER_PAD = 14.0

    def __init__(self) -> None:
        self.metrics = PageMetricsA4()

    @staticmethod
    def _question_height(question: Mapping[str, Any], width: float) -> float:
        prompt = str(question.get("prompt") or "")
        hint = question.get("hint_contract") or {}
        answer = question.get("answer_contract") or {}
        h = 26.0 + paragraph_height(prompt, width, font_size=11.0, line_height=14.5)

        stages = list(hint.get("stages") or [])
        if stages:
            h += 10.0 + StagedHintComponent.measure(stages, width, list(hint.get("thinking_path") or []))
            extra_hint = str(hint.get("hint_text") or "").strip()
            if extra_hint:
                h += 8.0 + paragraph_height(extra_hint, width, font_size=10.5, line_height=14.0)
        elif str(hint.get("modality") or "NONE") != "NONE":
            hint_text = str(hint.get("hint_text") or "")
            h += 20.0 + paragraph_height(hint_text or "Use the visual model below.", width, font_size=10.5, line_height=14.0)

        if str(answer.get("check_route") or "") == "INLINE":
            h += 20.0 + paragraph_height(str(answer.get("answer_text") or ""), width, font_size=11.0, line_height=14.5)
        else:
            h += 24.0
        return h + 10.0

    def render(self, plan: Mapping[str, Any], output_pdf_path: Path) -> Tuple[str, Dict[str, Any]]:
        validation = validate_study_journey(plan)
        c = canvas.Canvas(str(output_pdf_path), pagesize=(self.metrics.PAGE_WIDTH, self.metrics.PAGE_HEIGHT))
        backend = ReportLabBackend(c)
        custody = PublicationCustodyTracker()
        page_count = 0
        staged_hint_count = 0

        def new_page(module_title: str, module_index: int) -> float:
            nonlocal page_count
            if page_count:
                c.showPage()
            custody.new_page()
            page_count += 1
            top = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP
            backend.draw_rect(
                self.metrics.MARGIN_LEFT,
                top - self.HEADER_H,
                self.metrics.usable_width,
                self.HEADER_H,
                fill=PrimaryPalette.NAVY,
                stroke=PrimaryPalette.NAVY,
                corner_radius=8.0,
            )
            backend.draw_text(
                f"{module_index}. {module_title}",
                self.metrics.MARGIN_LEFT + 14.0,
                top - 34.0,
                font_size=18.0,
                color=PrimaryPalette.WHITE,
            )
            return top - self.HEADER_H - self.GAP

        for module_index, module in enumerate(plan["modules"], start=1):
            cur = new_page(str(module["title"]), module_index)
            goal = str(module["learning_goal"])
            goal_h = paragraph_height(goal, self.metrics.usable_width, font_size=12.0, line_height=16.0, padding_bottom=8.0)
            backend.draw_text("LEARNING GOAL", self.metrics.MARGIN_LEFT, cur, font_size=9.5, color=PrimaryPalette.TEAL)
            cur -= 14.0
            used = backend.draw_paragraph(
                goal,
                self.metrics.MARGIN_LEFT,
                cur,
                width=self.metrics.usable_width,
                font_size=12.0,
                color=PrimaryPalette.SLATE,
                line_height=16.0,
            )
            cur -= max(used, goal_h - 8.0) + self.GAP

            for block in module["blocks"]:
                block_type = str(block["block_type"])
                fill, accent = BLOCK_STYLE[block_type]
                body = str(block.get("body") or "")
                legacy_prompt = str(block.get("learner_prompt") or "")
                solution = str(block.get("solution_text") or "")
                visibility = str(block.get("answer_visibility") or "HIDDEN")
                rep = block.get("representation")
                questions = list(block.get("questions") or [])
                inner_width = self.metrics.usable_width - 28.0

                text_h = 42.0 + paragraph_height(body, inner_width, font_size=11.0, line_height=14.5)
                if questions:
                    text_h += sum(self._question_height(q, inner_width) for q in questions)
                elif legacy_prompt:
                    text_h += paragraph_height(legacy_prompt, inner_width, font_size=11.0, line_height=14.5) + 12.0
                if not questions and visibility in {"WORKED_EXAMPLE", "ANSWER_KEY_ONLY"} and solution:
                    text_h += paragraph_height(solution, inner_width, font_size=11.0, line_height=14.5) + 14.0
                rep_h = 150.0 if rep else 0.0
                response_h = 76.0 if block_type in {"GUIDED_TRY", "INDEPENDENT_TRY", "TRANSFER", "RETRIEVAL"} else 0.0
                block_h = text_h + rep_h + response_h + 18.0
                assert_component_fits_page(str(block.get("block_id") or block_type), block_h, self.metrics.usable_height - self.HEADER_H - self.GAP)

                if cur - block_h < self.metrics.MARGIN_BOTTOM:
                    cur = new_page(str(module["title"]) + " - continued", module_index)

                y = cur - block_h
                backend.draw_rect(self.metrics.MARGIN_LEFT, y, self.metrics.usable_width, block_h, fill=fill, stroke=accent, corner_radius=7.0)
                backend.draw_text(block_type.replace("_", " "), self.metrics.MARGIN_LEFT + 14.0, cur - 19.0, font_size=9.0, color=accent)
                backend.draw_text(str(block["title"]), self.metrics.MARGIN_LEFT + 14.0, cur - 39.0, font_size=13.5, color=PrimaryPalette.NAVY)
                tcur = cur - 48.0
                if body:
                    used = backend.draw_paragraph(body, self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=11.0, color=PrimaryPalette.SLATE, line_height=14.5)
                    tcur -= used + 8.0

                if questions:
                    for q in questions:
                        display_ref = str(q["display_ref"])
                        prompt = str(q["prompt"])
                        hint = q.get("hint_contract") or {}
                        answer = q.get("answer_contract") or {}
                        backend.draw_text(display_ref, self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=10.5, color=accent)
                        tcur -= 15.0
                        used = backend.draw_paragraph(prompt, self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=11.0, color=PrimaryPalette.NAVY, line_height=14.5)
                        custody.record_element("STUDY_QUESTION", str(q["question_id"]), self.metrics.MARGIN_LEFT + 14.0, tcur - used, inner_width, used + 22.0)
                        tcur -= used + 10.0

                        stages = list(hint.get("stages") or [])
                        if stages:
                            support = StagedHintComponent.render(
                                backend,
                                stages,
                                x=self.metrics.MARGIN_LEFT + 14.0,
                                top_y=tcur,
                                width=inner_width,
                                thinking_path=list(hint.get("thinking_path") or []),
                            )
                            staged_hint_count += len(stages)
                            for idx, box in enumerate(support["stage_boxes"], start=1):
                                custody.record_element(
                                    "STUDY_HINT_STAGE",
                                    f"{q['question_id']}-H{idx}",
                                    box.x,
                                    box.y,
                                    box.width,
                                    box.height,
                                )
                            for idx, box in enumerate(support["path_boxes"], start=1):
                                custody.record_element(
                                    "STUDY_THINKING_PATH_STEP",
                                    f"{q['question_id']}-TP{idx}",
                                    box.x,
                                    box.y,
                                    box.width,
                                    box.height,
                                )
                            tcur -= float(support["height"]) + 8.0
                            extra_hint = str(hint.get("hint_text") or "").strip()
                            if extra_hint:
                                backend.draw_text("EXTRA CLUE", self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=9.0, color=PrimaryPalette.AMBER)
                                tcur -= 13.0
                                used = backend.draw_paragraph(extra_hint, self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=10.5, color=PrimaryPalette.SLATE, line_height=14.0)
                                tcur -= used + 7.0
                        elif str(hint.get("modality") or "NONE") != "NONE":
                            modality = str(hint["modality"])
                            backend.draw_text(f"HINT - {modality}", self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=9.0, color=PrimaryPalette.AMBER)
                            tcur -= 14.0
                            hint_text = str(hint.get("hint_text") or "Look at the visual model below.")
                            used = backend.draw_paragraph(hint_text, self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=10.5, color=PrimaryPalette.SLATE, line_height=14.0)
                            tcur -= used + 7.0

                        route = str(answer.get("check_route") or "")
                        if route == "INLINE":
                            backend.draw_text("ANSWER", self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=9.0, color=PrimaryPalette.TEAL)
                            tcur -= 14.0
                            used = backend.draw_paragraph(str(answer.get("answer_text") or ""), self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=11.0, color=PrimaryPalette.NAVY, line_height=14.5)
                            tcur -= used + 8.0
                        else:
                            route_label = route.replace("_", " ").title()
                            backend.draw_text(f"CHECK AFTER TRYING: {route_label} - {answer.get('answer_ref')}", self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=9.5, color=PrimaryPalette.TEAL)
                            tcur -= 18.0
                elif legacy_prompt:
                    backend.draw_text("TRY", self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=9.5, color=PrimaryPalette.TEAL)
                    tcur -= 14.0
                    used = backend.draw_paragraph(legacy_prompt, self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=11.0, color=PrimaryPalette.NAVY, line_height=14.5)
                    tcur -= used + 8.0

                if not questions and visibility in {"WORKED_EXAMPLE", "ANSWER_KEY_ONLY"} and solution:
                    backend.draw_text("SOLUTION" if visibility == "WORKED_EXAMPLE" else "ANSWER CHECK", self.metrics.MARGIN_LEFT + 14.0, tcur, font_size=9.5, color=accent)
                    tcur -= 14.0
                    used = backend.draw_paragraph(solution, self.metrics.MARGIN_LEFT + 14.0, tcur, width=inner_width, font_size=11.0, color=PrimaryPalette.NAVY, line_height=14.5)
                    tcur -= used + 8.0

                if rep:
                    rep_box = BoundingBox(self.metrics.MARGIN_LEFT + 14.0, y + response_h + 12.0, inner_width, rep_h - 20.0)
                    render_primitive(str(rep["kind"]), dict(rep["params"]), backend, rep_box)
                    custody.record_element("STUDY_REPRESENTATION", str(block["block_id"]), rep_box.x, rep_box.y, rep_box.width, rep_box.height)

                if response_h:
                    rx = self.metrics.MARGIN_LEFT + 14.0
                    ry = y + 12.0
                    backend.draw_rect(rx, ry, inner_width, response_h - 20.0, fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.GRID_LINE, corner_radius=5.0)
                    custody.record_element("STUDY_RESPONSE", str(block["block_id"]), rx, ry, inner_width, response_h - 20.0)

                custody.record_element("STUDY_BLOCK", str(block["block_id"]), self.metrics.MARGIN_LEFT, y, self.metrics.usable_width, block_h)
                cur = y - self.GAP

        c.save()
        pdf_sha = custody.compute_pdf_hash(output_pdf_path)
        record = custody.export_custody_record(pdf_sha)
        record["study_journey"] = {
            "journey_id": plan.get("journey_id"),
            "validation": validation,
            "publisher_invention_allowed": False,
            "source_question_anchor_required": True,
            "answer_contract_required": True,
            "intrinsic_staged_hint_layout": True,
            "staged_hint_stage_count": staged_hint_count,
            "page_count": page_count,
        }
        return pdf_sha, record


def render_study_journey(plan: Mapping[str, Any], output_pdf_path: Path) -> Tuple[str, Dict[str, Any]]:
    return StudyJourneyComposer().render(plan, output_pdf_path)
