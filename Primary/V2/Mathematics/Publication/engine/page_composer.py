"""
Child-First A4 Page Composer for Primary Mathematics V2.
Renders Core 1 Study Guide and Core 2 Companion PDFs with strict readability,
generous response boxes, pagination over shrinking, and physical custody tracking.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from reportlab.pdfgen import canvas

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PageMetricsA4,
    PrimaryPalette,
    ReportLabBackend
)
from Primary.V2.Mathematics.Representation.engine.primitives.dispatcher import render_primitive
from Primary.V2.Mathematics.Publication.engine.custody import PublicationCustodyTracker
from Primary.V2.Mathematics.Publication.engine.surface_guard import LearnerSurfaceGuard
from Primary.V2.Mathematics.Publication.engine.learning_representation_adapter import (
    LearningRepresentationAdapter,
)
from Primary.V2.Mathematics.Publication.engine.learning_representation_components import (
    HintCardComponent,
    ThinkingPathComponent,
)


class PrimaryPageComposer:
    """Renders Core 1 and Core 2 child-first A4 publications."""

    def __init__(self) -> None:
        self.metrics = PageMetricsA4()
        self.guard = LearnerSurfaceGuard()

    def render_core1_study_guide(
        self,
        study_guide_plan: Dict[str, Any],
        output_pdf_path: Path
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Renders Core 1 Study Guide PDF.
        Returns (pdf_sha256, custody_record).
        """
        c = canvas.Canvas(str(output_pdf_path), pagesize=(self.metrics.PAGE_WIDTH, self.metrics.PAGE_HEIGHT))
        custody = PublicationCustodyTracker()
        custody.new_page()

        backend = ReportLabBackend(c)

        cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP

        def check_overflow(required_height: float) -> None:
            nonlocal cur_y
            if cur_y - required_height < self.metrics.MARGIN_BOTTOM:
                c.showPage()
                custody.new_page()
                cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP

        title = study_guide_plan.get("title", "Primary Mathematics Core 1 Study Guide")
        topic = study_guide_plan.get("topic", "Multiplication & Division")
        grade = study_guide_plan.get("grade_level", 4)

        header_h = 60.0
        check_overflow(header_h)
        backend.draw_rect(
            self.metrics.MARGIN_LEFT, cur_y - header_h,
            self.metrics.usable_width, header_h,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )
        backend.draw_text(title, self.metrics.MARGIN_LEFT + 15.0, cur_y - 28.0, font_size=self.metrics.TITLE_FONT_SIZE, color=PrimaryPalette.NAVY)
        backend.draw_text(f"Grade {grade} | {topic}", self.metrics.MARGIN_LEFT + 15.0, cur_y - 48.0, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.SLATE)
        custody.record_element("HEADER", "HDR-001", self.metrics.MARGIN_LEFT, cur_y - header_h, self.metrics.usable_width, header_h)
        cur_y -= (header_h + 20.0)

        modules = study_guide_plan.get("modules", [])
        for mod in modules:
            mod_title = mod.get("title", "Core Module")
            check_overflow(40.0)
            backend.draw_text(mod_title, self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.SECTION_FONT_SIZE, color=PrimaryPalette.NAVY)
            cur_y -= 25.0

            sections = mod.get("sections", [])
            for sec in sections:
                sec_type = sec.get("section_type", "NOTICE")
                sec_title = sec.get("title", "")
                sec_content = sec.get("content", "")
                prim_call = sec.get("primitive_call")

                if prim_call:
                    prim_h = 160.0
                    check_overflow(prim_h + 30.0)
                    backend.draw_text(f"• {sec_title}", self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.NAVY)
                    cur_y -= 20.0
                    bbox = BoundingBox(x=self.metrics.MARGIN_LEFT, y=cur_y - prim_h, width=self.metrics.usable_width, height=prim_h)
                    render_primitive(prim_call["kind"], prim_call["params"], backend, bbox)
                    custody.record_element("PRIMITIVE", prim_call["kind"], bbox.x, bbox.y, bbox.width, bbox.height)
                    cur_y -= (prim_h + 20.0)
                else:
                    import textwrap
                    char_width = self.metrics.BODY_FONT_SIZE * 0.55
                    chars_per_line = max(int((self.metrics.usable_width - 24.0) / char_width), 1)
                    lines_c = len(textwrap.wrap(str(sec_content), width=chars_per_line)) if sec_content else 1
                    box_h = 35.0 + (lines_c * 16.0)

                    check_overflow(box_h + 15.0)
                    fill_c = PrimaryPalette.HIGHLIGHT_YELLOW if sec_type == "NOTICE" else PrimaryPalette.WHITE
                    backend.draw_rect(
                        self.metrics.MARGIN_LEFT, cur_y - box_h,
                        self.metrics.usable_width, box_h,
                        fill=fill_c, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
                    )
                    backend.draw_text(sec_title, self.metrics.MARGIN_LEFT + 12.0, cur_y - 20.0, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.NAVY)
                    backend.draw_paragraph(sec_content, self.metrics.MARGIN_LEFT + 12.0, cur_y - 40.0, width=self.metrics.usable_width - 24.0, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.STUDENT_PENCIL)
                    custody.record_element("SECTION", sec_type, self.metrics.MARGIN_LEFT, cur_y - box_h, self.metrics.usable_width, box_h)
                    cur_y -= (box_h + 15.0)

            resp_h = self.metrics.MIN_RESPONSE_BOX_HEIGHT + 20.0
            check_overflow(resp_h + 20.0)
            backend.draw_text("My Working Space:", self.metrics.MARGIN_LEFT, cur_y, font_size=12.0, color=PrimaryPalette.SLATE)
            cur_y -= 16.0
            backend.draw_rect(
                self.metrics.MARGIN_LEFT, cur_y - resp_h,
                self.metrics.usable_width, resp_h,
                fill=PrimaryPalette.WHITE, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0, corner_radius=4.0
            )
            custody.record_element("RESPONSE_BOX", "RESP-001", self.metrics.MARGIN_LEFT, cur_y - resp_h, self.metrics.usable_width, resp_h)
            cur_y -= (resp_h + 25.0)

        c.save()
        pdf_sha256 = custody.compute_pdf_hash(output_pdf_path)
        custody_record = custody.export_custody_record(pdf_sha256)
        return pdf_sha256, custody_record

    def render_core2_companion(
        self,
        companion_plan: Dict[str, Any],
        output_pdf_path: Path
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Renders Core 2 Companion PDF.
        Appendix A: Practice Batches (RECONNECT, BUILD, CHOOSE, MIX, TRANSFER, RETRIEVE)
        Appendix B: visual Hint Ladders & independent retry when a LearningRepresentationPlan is attached.
        Appendix C: Visual Quick Reference decision aid.
        """
        c = canvas.Canvas(str(output_pdf_path), pagesize=(self.metrics.PAGE_WIDTH, self.metrics.PAGE_HEIGHT))
        custody = PublicationCustodyTracker()
        custody.new_page()

        backend = ReportLabBackend(c)
        cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP

        def check_overflow(required_height: float) -> None:
            nonlocal cur_y
            if cur_y - required_height < self.metrics.MARGIN_BOTTOM:
                c.showPage()
                custody.new_page()
                cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP

        comp_id = companion_plan.get("companion_id", "PrimaryMathCore2Companion")
        linked_c1 = companion_plan.get("linked_core1_id", "C1-MOD-01")

        header_h = 55.0
        check_overflow(header_h)
        backend.draw_rect(
            self.metrics.MARGIN_LEFT, cur_y - header_h,
            self.metrics.usable_width, header_h,
            fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
        )
        backend.draw_text("Core 2 Learning Companion", self.metrics.MARGIN_LEFT + 15.0, cur_y - 25.0, font_size=self.metrics.TITLE_FONT_SIZE, color=PrimaryPalette.NAVY)
        backend.draw_text(f"Semantic Link: {linked_c1} (No physical page hardcoding)", self.metrics.MARGIN_LEFT + 15.0, cur_y - 45.0, font_size=11.5, color=PrimaryPalette.TEAL)
        custody.record_element("COMPANION_HEADER", comp_id, self.metrics.MARGIN_LEFT, cur_y - header_h, self.metrics.usable_width, header_h)
        cur_y -= (header_h + 20.0)

        app_a = companion_plan.get("appendix_a", {})
        batches = app_a.get("batches", [])
        check_overflow(35.0)
        backend.draw_text("Appendix A — Practice Batches", self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.SECTION_FONT_SIZE, color=PrimaryPalette.NAVY)
        cur_y -= 25.0

        for b in batches:
            b_title = b.get("title", "Batch")
            role = b.get("practice_role", "BUILD")
            items = b.get("items", [])

            check_overflow(30.0)
            backend.draw_text(f"• {b_title} [{role}]", self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.AMBER)
            cur_y -= 20.0

            for itm in items:
                p_text = itm.get("prompt", "")
                import textwrap
                char_width = self.metrics.BODY_FONT_SIZE * 0.55
                chars_per_line = max(int((self.metrics.usable_width - 15.0) / char_width), 1)
                lines_c = len(textwrap.wrap(str(p_text), width=chars_per_line)) if p_text else 1
                prompt_h = lines_c * 16.0

                check_overflow(prompt_h + 30.0)
                backend.draw_paragraph(f"Q: {p_text}", self.metrics.MARGIN_LEFT + 15.0, cur_y, width=self.metrics.usable_width - 15.0, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.NAVY)
                cur_y -= prompt_h + 2.0
                backend.draw_line(self.metrics.MARGIN_LEFT + 15.0, cur_y, self.metrics.usable_width + self.metrics.MARGIN_LEFT - 15.0, cur_y, stroke=PrimaryPalette.GRID_LINE, stroke_width=1.0)
                cur_y -= 15.0

        c.showPage()
        custody.new_page()
        cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP

        app_b = companion_plan.get("appendix_b", {})
        ladders = app_b.get("ladders", [])
        backend.draw_text("Appendix B — Hint Ladder & Solutions", self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.SECTION_FONT_SIZE, color=PrimaryPalette.NAVY)
        cur_y -= 25.0

        for lad in ladders:
            learning_plan = lad.get("learning_representation_plan")
            if learning_plan:
                cards = LearningRepresentationAdapter.build_hint_cards(learning_plan)
                path_steps = LearningRepresentationAdapter.build_thinking_path(learning_plan)
                item_id = str(lad.get("item_id", learning_plan.get("task_ref", "Item")))

                check_overflow(28.0)
                backend.draw_text(f"Problem: {item_id}", self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.NAVY)
                cur_y -= 22.0

                for card in cards:
                    card_h = HintCardComponent.measure(card, self.metrics.usable_width)
                    check_overflow(card_h + 10.0)
                    card_box = BoundingBox(
                        x=self.metrics.MARGIN_LEFT,
                        y=cur_y - card_h,
                        width=self.metrics.usable_width,
                        height=card_h,
                    )
                    placements = HintCardComponent.render(backend, card_box, card)
                    custody.record_element(
                        "VISUAL_HINT_CARD",
                        f"{item_id}:{card['level']}",
                        card_box.x, card_box.y, card_box.width, card_box.height,
                    )
                    for placement in placements:
                        if placement.kind == "HINT_VISUAL":
                            custody.record_element(
                                "HINT_VISUAL",
                                placement.ref,
                                placement.bbox.x,
                                placement.bbox.y,
                                placement.bbox.width,
                                placement.bbox.height,
                            )
                    cur_y -= card_h + 10.0

                path_h = ThinkingPathComponent.measure(path_steps, self.metrics.usable_width)
                check_overflow(path_h + 32.0)
                backend.draw_text("My Thinking Path", self.metrics.MARGIN_LEFT, cur_y, font_size=13.0, color=PrimaryPalette.NAVY)
                cur_y -= 18.0
                path_box = BoundingBox(
                    x=self.metrics.MARGIN_LEFT,
                    y=cur_y - path_h,
                    width=self.metrics.usable_width,
                    height=path_h,
                )
                ThinkingPathComponent.render(backend, path_box, path_steps)
                custody.record_element("THINKING_PATH", item_id, path_box.x, path_box.y, path_box.width, path_box.height)
                cur_y -= path_h + 16.0

                fresh_prompt = str(lad.get("fresh_independent_retry_H0", "")).strip()
                if not fresh_prompt:
                    raise ValueError("FRESH_H0_PROMPT_REQUIRED_FOR_LEARNER_PUBLICATION")
                import textwrap
                char_width = self.metrics.BODY_FONT_SIZE * 0.55
                chars_per_line = max(int((self.metrics.usable_width - 24.0) / char_width), 1)
                line_count = max(1, len(textwrap.wrap(fresh_prompt, width=chars_per_line)))
                fresh_h = 36.0 + line_count * 16.0
                check_overflow(fresh_h + 18.0)
                backend.draw_rect(
                    self.metrics.MARGIN_LEFT,
                    cur_y - fresh_h,
                    self.metrics.usable_width,
                    fresh_h,
                    fill=PrimaryPalette.WHITE,
                    stroke=PrimaryPalette.SOFT_GREEN,
                    corner_radius=6.0,
                )
                backend.draw_text("FRESH H0 — NO HINTS", self.metrics.MARGIN_LEFT + 12.0, cur_y - 18.0, font_size=12.0, color=PrimaryPalette.SOFT_GREEN)
                backend.draw_paragraph(fresh_prompt, self.metrics.MARGIN_LEFT + 12.0, cur_y - 38.0, width=self.metrics.usable_width - 24.0, font_size=12.0, color=PrimaryPalette.NAVY)
                custody.record_element("FRESH_H0", item_id, self.metrics.MARGIN_LEFT, cur_y - fresh_h, self.metrics.usable_width, fresh_h)
                cur_y -= fresh_h + 20.0
                continue

            # Backward-compatible legacy text-only path. New Primary V2 production
            # should attach LearningRepresentationPlan and use the branch above.
            import textwrap

            def measure(text, font_size):
                if not text:
                    return 0
                cw = font_size * 0.55
                cpl = max(int((self.metrics.usable_width - 24.0) / cw), 1)
                return len(textwrap.wrap(str(text), width=cpl)) * 16.0

            h1 = lad.get('H1_notice', '')
            h2 = lad.get('H2_remember', '')
            h3 = lad.get('H3_represent', '')
            h0 = lad.get('fresh_independent_retry_H0', '')

            h1_h = measure(f"H1 (Notice): {h1}", 12.0)
            h2_h = measure(f"H2 (Remember): {h2}", 12.0)
            h3_h = measure(f"H3 (Represent): {h3}", 12.0)
            h0_h = measure(f"Fresh H0 Independent Retry: {h0}", 12.5)

            lad_h = 30.0 + h1_h + h2_h + h3_h + h0_h + 20.0

            check_overflow(lad_h + 10.0)
            backend.draw_rect(
                self.metrics.MARGIN_LEFT, cur_y - lad_h,
                self.metrics.usable_width, lad_h,
                fill=PrimaryPalette.LIGHT_BG, stroke=PrimaryPalette.CARD_BORDER, corner_radius=6.0
            )
            backend.draw_text(f"Problem: {lad.get('item_id', 'Item')}", self.metrics.MARGIN_LEFT + 12.0, cur_y - 20.0, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.NAVY)

            sy = cur_y - 42.0
            backend.draw_paragraph(f"H1 (Notice): {h1}", self.metrics.MARGIN_LEFT + 12.0, sy, width=self.metrics.usable_width - 24.0, font_size=12.0, color=PrimaryPalette.SLATE)
            sy -= h1_h
            backend.draw_paragraph(f"H2 (Remember): {h2}", self.metrics.MARGIN_LEFT + 12.0, sy, width=self.metrics.usable_width - 24.0, font_size=12.0, color=PrimaryPalette.SLATE)
            sy -= h2_h
            backend.draw_paragraph(f"H3 (Represent): {h3}", self.metrics.MARGIN_LEFT + 12.0, sy, width=self.metrics.usable_width - 24.0, font_size=12.0, color=PrimaryPalette.ACCENT_BLUE)
            sy -= h3_h
            backend.draw_paragraph(f"Fresh H0 Independent Retry: {h0}", self.metrics.MARGIN_LEFT + 12.0, sy, width=self.metrics.usable_width - 24.0, font_size=12.5, color=PrimaryPalette.SOFT_GREEN)

            custody.record_element("HINT_LADDER", lad.get("item_id", "LAD"), self.metrics.MARGIN_LEFT, cur_y - lad_h, self.metrics.usable_width, lad_h)
            cur_y -= (lad_h + 20.0)

        c.showPage()
        custody.new_page()
        cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP

        app_c = companion_plan.get("appendix_c", {})
        c_title = app_c.get("title", "Appendix C — Visual Quick Reference")
        aid_name = app_c.get("decision_aid_name", "Decision Aid")
        prim_call = app_c.get("primitive_call")

        backend.draw_text(c_title, self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.SECTION_FONT_SIZE, color=PrimaryPalette.NAVY)
        cur_y -= 25.0
        backend.draw_text(f"Decision Aid: {aid_name} (Visual Flow Model)", self.metrics.MARGIN_LEFT, cur_y, font_size=self.metrics.BODY_FONT_SIZE, color=PrimaryPalette.AMBER)
        cur_y -= 25.0

        if prim_call:
            prim_h = 240.0
            bbox = BoundingBox(x=self.metrics.MARGIN_LEFT, y=cur_y - prim_h, width=self.metrics.usable_width, height=prim_h)
            render_primitive(prim_call["kind"], prim_call["params"], backend, bbox)
            custody.record_element("APPENDIX_C_AID", aid_name, bbox.x, bbox.y, bbox.width, bbox.height)
            cur_y -= (prim_h + 20.0)

        c.save()
        pdf_sha256 = custody.compute_pdf_hash(output_pdf_path)
        custody_record = custody.export_custody_record(pdf_sha256)
        return pdf_sha256, custody_record
