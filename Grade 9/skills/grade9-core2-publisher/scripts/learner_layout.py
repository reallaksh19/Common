#!/usr/bin/env python3
"""Learner-first Study Guide layout policy layered over physical-page custody.

This module owns presentation-only composition decisions. It deliberately does
not alter StudyGuide semantics, PublicationStructure, LearningDesign, or
PhysicalPageMap custody.

For deterministic engineering replays, adjacent generated representation items
whose text is only machine requirement metadata are rendered side by side. Each
representation retains its own content_ref and physical bounding box. Mature
authored representation prose is never collapsed by this rule.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer

import physical_page_runtime as base


class GeneratedRepresentationRow(Flowable):
    """Two generated schematics in one row with independent custody records."""

    def __init__(
        self,
        left_child,
        left_item: dict,
        right_child,
        right_item: dict,
        tracker: base.PlacementTracker,
        page_intent_id: str,
        gap: float = 6 * mm,
    ):
        super().__init__()
        self.entries = [(left_child, left_item), (right_child, right_item)]
        self.tracker = tracker
        self.page_intent_id = page_intent_id
        self.gap = gap
        self.width = 0.0
        self.height = 0.0
        self._child_sizes: list[tuple[float, float]] = []

    def wrap(self, avail_width, avail_height):
        column_width = max(1.0, (avail_width - self.gap) / 2.0)
        self._child_sizes = [
            child.wrap(column_width, avail_height)
            for child, _item in self.entries
        ]
        self.width = avail_width
        self.height = max(height for _width, height in self._child_sizes)
        return self.width, self.height

    def drawOn(self, canv, x, y, _sW=0):
        """Draw children at absolute page coordinates and record those boxes."""
        page = canv.getPageNumber()
        child_x = x
        for index, ((child, item), (width, height)) in enumerate(zip(self.entries, self._child_sizes)):
            self.tracker.add_content(
                self.page_intent_id,
                item["item_id"],
                item.get("learning_design_refs", []),
                page,
                child_x,
                y,
                width,
                height,
            )
            child.drawOn(canv, child_x, y)
            child_x += width + (self.gap if index == 0 else 0.0)

    def draw(self):
        # drawOn owns both composition and absolute custody instrumentation.
        return None


def _pairable_generated_representation(item: dict) -> bool:
    return bool(item.get("representation_instance_id") and base._generated_representation_metadata(item))


def make_study_renderer(impl):
    """Return tracked Study Guide renderer with learner-first representation composition."""

    def render(model: dict, plan: dict, path: Path):
        structure = impl._CURRENT_STRUCTURE
        if structure is None:
            print("CORE2_PUBLICATION_STRUCTURE_MISSING")
            raise SystemExit(2)

        tracker = base.PlacementTracker()
        st = impl.legacy._styles("SG")
        doc = SimpleDocTemplate(
            str(path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
            title=model["title"],
            author="Grade 9–11 Core (2) Publisher",
        )
        items = impl._content_map(model)
        reps = impl._rep_map(plan)
        arc = base._arc_metadata(structure)
        story: list[Flowable] = [
            Paragraph(impl.legacy.safe(model["title"]), st["h1"]),
            Paragraph(impl.legacy.safe(model.get("subtitle", "")), st["body"]),
            PageBreak(),
        ]

        for page_intent in structure["study_guide"]["page_intents"]:
            iid = page_intent["page_intent_id"]
            story.append(
                base.TrackedFlowable(
                    Paragraph(impl.legacy.safe(page_intent["cognitive_job"]), st["h1"]),
                    tracker,
                    iid,
                    intent_heading=True,
                )
            )

            previous_heading: tuple[str, str] | None = None
            refs = page_intent["content_refs"]
            index = 0
            while index < len(refs):
                ref = refs[index]
                meta = arc[ref]
                item = items[ref]
                role = meta.get("learner_visible_heading") or meta["role"].replace("_", " ")
                support = meta.get("support_state", "")
                heading_key = (role, support)
                if heading_key != previous_heading:
                    if not base._content_carries_role_cue(meta, item):
                        heading = f"{role} · {support}" if support else role
                        story.append(Paragraph(impl.legacy.safe(heading), st["h2"]))
                    previous_heading = heading_key

                if _pairable_generated_representation(item) and index + 1 < len(refs):
                    next_ref = refs[index + 1]
                    next_item = items[next_ref]
                    next_meta = arc[next_ref]
                    same_step_surface = (
                        next_meta.get("role") == meta.get("role")
                        and next_meta.get("support_state", "") == support
                    )
                    if same_step_surface and _pairable_generated_representation(next_item):
                        left = impl.StructuredRepresentationFlowable(reps[item["representation_instance_id"]])
                        right = impl.StructuredRepresentationFlowable(reps[next_item["representation_instance_id"]])
                        story.append(
                            GeneratedRepresentationRow(
                                left,
                                item,
                                right,
                                next_item,
                                tracker,
                                iid,
                            )
                        )
                        story.append(Spacer(1, 3 * mm))
                        index += 2
                        continue

                if not base._generated_representation_metadata(item):
                    story.append(
                        base._tracked(
                            Paragraph(impl.legacy.safe(item["content"]), st["body"]),
                            tracker,
                            iid,
                            item,
                        )
                    )
                if item.get("representation_instance_id"):
                    rep = reps[item["representation_instance_id"]]
                    story.append(base._tracked(impl.StructuredRepresentationFlowable(rep), tracker, iid, item))
                    story.append(Spacer(1, 3 * mm))
                index += 1

            story.append(PageBreak())

        app_by_letter = {"A": "appendix_A", "B": "appendix_B", "C": "appendix_C"}
        for letter in structure["study_guide"]["appendix_order"]:
            app = model[app_by_letter[letter]]
            story.append(Paragraph(impl.legacy.safe(app["title"]), st["h1"]))
            for i, item in enumerate(app["items"], 1):
                story.append(Paragraph(impl.legacy.safe(f"{i}. {item['content']}"), st["body"]))
            story.append(PageBreak())

        doc.build(story, onFirstPage=impl.legacy.page_number, onLaterPages=impl.legacy.page_number)
        page_map = base.build_page_map(model, structure, path, tracker)
        contracts = Path(__file__).resolve().parents[3] / "architecture" / "core2" / "contracts" / "v1"
        impl.legacy.validate_schema("physical-page-map.schema.json", page_map, contracts)
        out = base.page_map_path_for(path)
        impl.legacy.write_json(out, page_map)
        print("PHYSICAL_PAGE_MAP_EMITTED = PASS")

    return render
