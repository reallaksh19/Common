"""Strict Core1 publication from AuthoringLearningHandoff.

This is the canonical Grade-4 Core1 route. It does not translate validated
learning representation plans back into legacy renderer-local section schemas.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from reportlab.pdfgen import canvas

from Primary.V2.Mathematics.Representation.engine.base import (
    BoundingBox,
    PageMetricsA4,
    PrimaryPalette,
    ReportLabBackend,
)
from Primary.V2.Mathematics.Publication.engine.authoring_handoff_adapter import AuthoringHandoffAdapter
from Primary.V2.Mathematics.Publication.engine.core1_components import (
    PrimaryVisualComponent,
    WorkSurfaceComponent,
)
from Primary.V2.Mathematics.Publication.engine.custody import PublicationCustodyTracker
from Primary.V2.Mathematics.Publication.engine.learning_representation_adapter import LearningRepresentationAdapter


class Core1LearningRepresentationComposer:
    """One validated learning item per page, visual-first and work-surface aware."""

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

        for item_index, item in enumerate(items):
            custody.new_page()
            if item_index > 0:
                c.showPage()

            cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP
            module_id = str(item["module_id"])
            plan = item["learning_representation_plan"]
            LearningRepresentationAdapter.validate_plan(plan)

            header_h = 58.0
            backend.draw_rect(
                self.metrics.MARGIN_LEFT,
                cur_y - header_h,
                self.metrics.usable_width,
                header_h,
                fill=PrimaryPalette.LIGHT_BG,
                stroke=PrimaryPalette.CARD_BORDER,
                corner_radius=6.0,
            )
            backend.draw_text(title, self.metrics.MARGIN_LEFT + 14.0, cur_y - 25.0, font_size=18.0, color=PrimaryPalette.NAVY)
            backend.draw_text(f"Grade {grade_level} | {topic}", self.metrics.MARGIN_LEFT + 14.0, cur_y - 45.0, font_size=12.0, color=PrimaryPalette.SLATE)
            custody.record_element("CORE1_HEADER", module_id, self.metrics.MARGIN_LEFT, cur_y - header_h, self.metrics.usable_width, header_h)
            cur_y -= header_h + 18.0

            concept_title = str(item.get("concept_title") or module_id)
            backend.draw_text(concept_title, self.metrics.MARGIN_LEFT, cur_y, font_size=17.0, color=PrimaryPalette.NAVY)
            cur_y -= 22.0

            objective = str(item.get("objective") or "").strip()
            if objective:
                backend.draw_paragraph(objective, self.metrics.MARGIN_LEFT, cur_y, width=self.metrics.usable_width, font_size=12.5, color=PrimaryPalette.SLATE)
                cur_y -= 36.0

            learner_action = str(item.get("learner_action") or "").strip()
            if learner_action:
                backend.draw_text("Your job", self.metrics.MARGIN_LEFT, cur_y, font_size=12.0, color=PrimaryPalette.TEAL)
                cur_y -= 17.0
                backend.draw_paragraph(learner_action, self.metrics.MARGIN_LEFT, cur_y, width=self.metrics.usable_width, font_size=12.5, color=PrimaryPalette.NAVY)
                cur_y -= 38.0

            visual = plan["primary_visual"]
            visual_h = PrimaryVisualComponent.measure(visual, self.metrics.usable_width)
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
            cur_y -= visual_h + 18.0

            surface = LearningRepresentationAdapter.work_surface(plan)
            if surface is not None:
                backend.draw_text("Work it out", self.metrics.MARGIN_LEFT, cur_y, font_size=14.0, color=PrimaryPalette.NAVY)
                cur_y -= 18.0
                surface_h = WorkSurfaceComponent.measure(surface, self.metrics.usable_width)
                if cur_y - surface_h < self.metrics.MARGIN_BOTTOM:
                    c.showPage()
                    custody.new_page()
                    cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP
                    backend.draw_text(f"{concept_title} — Work it out", self.metrics.MARGIN_LEFT, cur_y, font_size=16.0, color=PrimaryPalette.NAVY)
                    cur_y -= 24.0
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
                if cur_y - response_h < self.metrics.MARGIN_BOTTOM:
                    c.showPage()
                    custody.new_page()
                    cur_y = self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP
                backend.draw_text("My work", self.metrics.MARGIN_LEFT, cur_y, font_size=13.0, color=PrimaryPalette.SLATE)
                cur_y -= 16.0
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

        if not items:
            custody.new_page()
            backend.draw_text("No guided Core1 modules to publish.", self.metrics.MARGIN_LEFT, self.metrics.PAGE_HEIGHT - self.metrics.MARGIN_TOP, font_size=12.0, color=PrimaryPalette.SLATE)

        c.save()
        pdf_sha256 = custody.compute_pdf_hash(output_pdf_path)
        record = custody.export_custody_record(pdf_sha256)
        record["core1_handoff"] = {
            "handoff_id": handoff.get("handoff_id"),
            "planned_module_count": core1["planned_module_count"],
            "independent_probe_module_ids": core1["independent_probe_module_ids"],
            "publisher_invention_allowed": False,
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
