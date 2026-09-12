"""Strict Core1 publication from AuthoringLearningHandoff.

This is the canonical Grade-4 Core1 route. It does not translate validated
learning representation plans back into legacy renderer-local section schemas.
Every block is measured before drawing; learner-facing text is never shrunk to
repair page fit.
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
from Grade4.V2.Mathematics.Publication.engine.authoring_handoff_adapter import AuthoringHandoffAdapter
from Grade4.V2.Mathematics.Publication.engine.core1_components import (
    PrimaryVisualComponent,
    WorkSurfaceComponent,
)
from Grade4.V2.Mathematics.Publication.engine.custody import PublicationCustodyTracker
from Grade4.V2.Mathematics.Publication.engine.layout_measure import (
    assert_component_fits_page,
    paragraph_height,
)
from Grade4.V2.Mathematics.Publication.engine.learning_representation_adapter import LearningRepresentationAdapter


class Core1LearningRepresentationComposer:
    """Measured, visual-first Core1 publication from validated learning plans."""

    HEADER_H = 58.0
    BLOCK_GAP = 16.0

    def __init__(self) -> None:
        self.metrics = PageMetricsA4()

    def render(
        self,
        handoff: Mapping[str, Any],
        output_pdf_path: Path,
        *,
        title: str = "Grade 4 Mathematics Study Guide",
        topic: str = "Mathematics",
        grade_level: int = 4,
    ) -> Tuple[str, Dict[str, Any]]:
        core1 = AuthoringHandoffAdapter.build_core1_items(handoff)
        items = list(core1["items"])

        c = canvas.Canvas(str(output_pdf_path), pagesize=(self.metrics.PAGE_WIDTH, self.metrics.PAGE_HEIGHT))
        backend = ReportLabBackend(c)
        custody = PublicationCustodyTracker()
        page_count = 0
        source_notes: list[dict[str, str]] = []

        def start_page(continuation: str | None = None) -> float:
            nonlocal page_count
            if page_count > 0:
                c.showPage()
            custody.new_page()
            page_count += 1
            cur = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP
            if continuation:
                backend.draw_text(continuation, self.metrics.MARGIN_LEFT, cur, font_size=16.0, color=PrimaryPalette.NAVY)
                cur -= 26.0
            return cur

        def ensure_space(cur_y: float, required_h: float, name: str, continuation: str | None = None) -> float:
            assert_component_fits_page(name, required_h, self.metrics.usable_height)
            if cur_y - required_h < self.metrics.MARGIN_BOTTOM:
                return start_page(continuation)
            return cur_y

        for item in items:
            cur_y = start_page()
            module_id = str(item["module_id"])
            plan = item["learning_representation_plan"]
            LearningRepresentationAdapter.validate_plan(plan)

            backend.draw_rect(
                self.metrics.MARGIN_LEFT,
                cur_y - self.HEADER_H,
                self.metrics.usable_width,
                self.HEADER_H,
                fill=PrimaryPalette.LIGHT_BG,
                stroke=PrimaryPalette.CARD_BORDER,
                corner_radius=6.0,
            )
            backend.draw_text(title, self.metrics.MARGIN_LEFT + 14.0, cur_y - 25.0, font_size=18.0, color=PrimaryPalette.NAVY)
            backend.draw_text(f"Grade {grade_level} | {topic}", self.metrics.MARGIN_LEFT + 14.0, cur_y - 45.0, font_size=12.0, color=PrimaryPalette.SLATE)
            custody.record_element("CORE1_HEADER", module_id, self.metrics.MARGIN_LEFT, cur_y - self.HEADER_H, self.metrics.usable_width, self.HEADER_H)
            cur_y -= self.HEADER_H + self.BLOCK_GAP

            concept_title = str(item.get("concept_title") or module_id)
            title_h = paragraph_height(concept_title, self.metrics.usable_width, font_size=17.0, line_height=21.0, padding_bottom=6.0)
            cur_y = ensure_space(cur_y, title_h, "CORE1_CONCEPT_TITLE")
            consumed = backend.draw_paragraph(
                concept_title,
                self.metrics.MARGIN_LEFT,
                cur_y,
                width=self.metrics.usable_width,
                font_size=17.0,
                color=PrimaryPalette.NAVY,
                line_height=21.0,
            )
            cur_y -= max(consumed, title_h - 6.0) + 6.0

            learner_prompt = str(plan.get("learner_prompt") or "").strip()
            objective = str(item.get("objective") or "").strip()
            prompt_text = learner_prompt or objective
            if prompt_text:
                prompt_h = paragraph_height(prompt_text, self.metrics.usable_width, font_size=13.5, line_height=18.0, padding_bottom=10.0)
                cur_y = ensure_space(cur_y, prompt_h, "CORE1_LEARNER_PROMPT", f"{concept_title} - continued")
                consumed = backend.draw_paragraph(
                    prompt_text,
                    self.metrics.MARGIN_LEFT,
                    cur_y,
                    width=self.metrics.usable_width,
                    font_size=13.5,
                    color=PrimaryPalette.NAVY,
                    line_height=18.0,
                )
                custody.record_element(
                    "CORE1_LEARNER_PROMPT",
                    module_id,
                    self.metrics.MARGIN_LEFT,
                    cur_y - max(consumed, prompt_h - 10.0),
                    self.metrics.usable_width,
                    max(consumed, prompt_h - 10.0),
                )
                cur_y -= max(consumed, prompt_h - 10.0) + 10.0

            learner_action = str(item.get("learner_action") or "").strip()
            if learner_action:
                action_text = learner_action
                action_h = 18.0 + paragraph_height(action_text, self.metrics.usable_width, font_size=12.0, line_height=15.5, padding_bottom=8.0)
                cur_y = ensure_space(cur_y, action_h, "CORE1_LEARNER_ACTION", f"{concept_title} - continued")
                backend.draw_text("TRY", self.metrics.MARGIN_LEFT, cur_y, font_size=12.0, color=PrimaryPalette.TEAL)
                cur_y -= 17.0
                consumed = backend.draw_paragraph(
                    action_text,
                    self.metrics.MARGIN_LEFT,
                    cur_y,
                    width=self.metrics.usable_width,
                    font_size=12.0,
                    color=PrimaryPalette.SLATE,
                    line_height=15.5,
                )
                cur_y -= max(consumed, action_h - 26.0) + 8.0

            visual = plan["primary_visual"]
            visual_h = PrimaryVisualComponent.measure(visual, self.metrics.usable_width)
            cur_y = ensure_space(cur_y, visual_h, "CORE1_PRIMARY_VISUAL", f"{concept_title} - visual")
            visual_box = BoundingBox(
                x=self.metrics.MARGIN_LEFT,
                y=cur_y - visual_h,
                width=self.metrics.usable_width,
                height=visual_h,
            )
            PrimaryVisualComponent.render(backend, visual_box, visual)
            custody.record_element(
                "CORE1_PRIMARY_VISUAL",
                str(visual.get("visual_state_id") or module_id),
                visual_box.x, visual_box.y, visual_box.width, visual_box.height,
            )
            cur_y -= visual_h + self.BLOCK_GAP

            surface = LearningRepresentationAdapter.work_surface(plan)
            if surface is not None:
                surface_h = WorkSurfaceComponent.measure(surface, self.metrics.usable_width)
                total_h = 22.0 + surface_h
                cur_y = ensure_space(cur_y, total_h, "CORE1_WORK_SURFACE", f"{concept_title} - work it out")
                backend.draw_text("WORK IT OUT", self.metrics.MARGIN_LEFT, cur_y, font_size=13.5, color=PrimaryPalette.NAVY)
                cur_y -= 20.0
                surface_box = BoundingBox(
                    x=self.metrics.MARGIN_LEFT,
                    y=cur_y - surface_h,
                    width=self.metrics.usable_width,
                    height=surface_h,
                )
                WorkSurfaceComponent.render(backend, surface_box, surface)
                custody.record_element(
                    "CORE1_WORK_SURFACE",
                    str(surface.get("surface_id") or module_id),
                    surface_box.x, surface_box.y, surface_box.width, surface_box.height,
                )
            else:
                response_h = 170.0
                total_h = 20.0 + response_h
                cur_y = ensure_space(cur_y, total_h, "CORE1_RESPONSE_BOX", f"{concept_title} - my work")
                backend.draw_text("MY WORK", self.metrics.MARGIN_LEFT, cur_y, font_size=12.5, color=PrimaryPalette.SLATE)
                cur_y -= 18.0
                response_box = BoundingBox(
                    x=self.metrics.MARGIN_LEFT,
                    y=cur_y - response_h,
                    width=self.metrics.usable_width,
                    height=response_h,
                )
                backend.draw_rect(
                    response_box.x, response_box.y, response_box.width, response_box.height,
                    fill=PrimaryPalette.WHITE,
                    stroke=PrimaryPalette.GRID_LINE,
                    stroke_width=1.0,
                    corner_radius=5.0,
                )
                custody.record_element("CORE1_RESPONSE_BOX", module_id, response_box.x, response_box.y, response_box.width, response_box.height)

            if plan.get("source_note"):
                source_notes.append({"module_id": module_id, "note": str(plan["source_note"])})

        if not items:
            cur_y = start_page()
            backend.draw_text("No guided Core1 modules to publish.", self.metrics.MARGIN_LEFT, cur_y, font_size=12.0, color=PrimaryPalette.SLATE)

        c.save()
        pdf_sha256 = custody.compute_pdf_hash(output_pdf_path)
        record = custody.export_custody_record(pdf_sha256)
        record["core1_handoff"] = {
            "handoff_id": handoff.get("handoff_id"),
            "planned_module_count": core1["planned_module_count"],
            "independent_probe_module_ids": core1["independent_probe_module_ids"],
            "source_notes": source_notes,
            "publisher_invention_allowed": False,
            "legacy_sections_used": False,
        }
        return pdf_sha256, record


def render_core1_from_authoring_handoff(
    handoff: Mapping[str, Any],
    output_pdf_path: Path,
    *,
    title: str = "Grade 4 Mathematics Study Guide",
    topic: str = "Mathematics",
    grade_level: int = 4,
) -> Tuple[str, Dict[str, Any]]:
    return Core1LearningRepresentationComposer().render(
        handoff,
        output_pdf_path,
        title=title,
        topic=topic,
        grade_level=grade_level,
    )
