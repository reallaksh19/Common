#!/usr/bin/env python3
"""Learner-first Study Guide layout policy layered over physical-page custody.

This module owns presentation decisions without weakening semantic custody.
Support states remain in PublicationStructure/LearningDesign; learner pages show
instructional cues rather than machine authoring-state labels.

A StudyGuide representation item may carry a Core2-owned per-use
``representation_payload``.  The payload instantiates the frozen Core1
representation requirement for the particular learner example (for example,
trolley + push right + friction left) without changing Core1 subject truth.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer

import physical_page_runtime as base


class GeneratedRepresentationRow(Flowable):
    """Two generated replay schematics in one row with independent custody."""

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
        self._child_sizes = [child.wrap(column_width, avail_height) for child, _item in self.entries]
        self.width = avail_width
        self.height = max(height for _width, height in self._child_sizes)
        return self.width, self.height

    def drawOn(self, canv, x, y, _sW=0):
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
        return None


class LearnerForceDiagram(Flowable):
    """Concrete monochrome force diagram instantiated by a StudyGuide item."""

    DIRECTIONS = {"LEFT", "RIGHT", "UP", "DOWN"}

    def __init__(self, payload: dict, width: float = 170 * mm, height: float = 46 * mm):
        super().__init__()
        self.payload = payload
        self.width = width
        self.height = height
        self._validate()

    def _validate(self) -> None:
        system = self.payload.get("selected_system_label")
        forces = self.payload.get("forces")
        errors = []
        if not isinstance(system, str) or not system.strip():
            errors.append("selected_system_label is required")
        if not isinstance(forces, list) or not forces:
            errors.append("at least one force is required")
        else:
            for index, force in enumerate(forces, 1):
                if not isinstance(force.get("label"), str) or not force["label"].strip():
                    errors.append(f"force {index} requires a label")
                if force.get("direction") not in self.DIRECTIONS:
                    errors.append(f"force {index} direction must be one of {sorted(self.DIRECTIONS)}")
        if errors:
            print("CORE2_LEARNER_REPRESENTATION_PAYLOAD = FAIL")
            for error in errors:
                print("- " + error)
            raise SystemExit(2)

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    @staticmethod
    def _arrow(c, x1, y1, x2, y2):
        c.line(x1, y1, x2, y2)
        angle = math.atan2(y2 - y1, x2 - x1)
        for delta in (2.55, -2.55):
            c.line(x2, y2, x2 + 5 * math.cos(angle + delta), y2 + 5 * math.sin(angle + delta))

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.saveState()
        c.setLineWidth(0.9)
        c.setFont("Helvetica-Bold", 8.5)
        system = self.payload["selected_system_label"].strip()
        c.drawString(4, h - 10, f"FORCE DIAGRAM · system: {system}")

        cx, cy = w / 2, h / 2 - 5
        box_w, box_h = min(90, w * 0.22), 32
        c.rect(cx - box_w / 2, cy - box_h / 2, box_w, box_h)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(cx, cy - 3, system)

        positive = str(self.payload.get("positive_direction", "")).upper()
        c.setFont("Helvetica", 7.5)
        if positive in {"LEFT", "RIGHT"}:
            label = "+ direction: right" if positive == "RIGHT" else "+ direction: left"
            c.drawString(6, h - 25, label)
        elif positive in {"UP", "DOWN"}:
            label = "+ direction: up" if positive == "UP" else "+ direction: down"
            c.drawString(6, h - 25, label)

        for force in self.payload["forces"]:
            direction = force["direction"]
            label = force["label"].strip()
            magnitude = str(force.get("magnitude_text", "")).strip()
            shown = f"{label} · {magnitude}" if magnitude else label
            if direction == "RIGHT":
                x1, y1, x2, y2 = cx + box_w / 2, cy, min(w - 80, cx + box_w / 2 + 92), cy
                self._arrow(c, x1, y1, x2, y2)
                c.drawString(x1 + 8, y1 + 8, shown)
            elif direction == "LEFT":
                x1, y1, x2, y2 = cx - box_w / 2, cy, max(80, cx - box_w / 2 - 92), cy
                self._arrow(c, x1, y1, x2, y2)
                text_w = c.stringWidth(shown, "Helvetica", 7.5)
                c.drawString(max(4, x2 - text_w), y1 + 8, shown)
            elif direction == "UP":
                x1, y1, x2, y2 = cx, cy + box_h / 2, cx, min(h - 28, cy + box_h / 2 + 38)
                self._arrow(c, x1, y1, x2, y2)
                c.drawString(x1 + 7, y2 - 2, shown)
            elif direction == "DOWN":
                x1, y1, x2, y2 = cx, cy - box_h / 2, cx, max(10, cy - box_h / 2 - 38)
                self._arrow(c, x1, y1, x2, y2)
                c.drawString(x1 + 7, y2, shown)

        c.restoreState()


def _pairable_generated_representation(item: dict) -> bool:
    return bool(
        item.get("representation_instance_id")
        and not item.get("representation_payload")
        and base._generated_representation_metadata(item)
    )


def _representation_flowable(impl, rep: dict, item: dict):
    payload = item.get("representation_payload")
    if rep.get("representation_type") == "FORCE_DIAGRAM" and payload:
        return LearnerForceDiagram(payload)
    return impl.StructuredRepresentationFlowable(rep)


def _content_carries_visible_role(meta: dict, item: dict) -> bool:
    if base._content_carries_role_cue(meta, item):
        return True
    if meta.get("learner_visible_heading"):
        return False
    role = meta.get("role", "")
    cues = {
        "NOTICE": ("NOTICE",),
        "WORKED_EXAMPLE": ("WORKED", "WORKED EXAMPLE"),
        "GUIDED_1": ("GUIDED 1",),
        "GUIDED_2_FADED": ("GUIDED 2",),
        "INDEPENDENT_TRANSFER": ("INDEPENDENT TRANSFER",),
        "RETRIEVAL_CHECK": ("RETRIEVAL CHECK",),
        "MISCONCEPTION_REPAIR": ("MISCONCEPTION REPAIR",),
        "MODEL_BOUNDARY": ("MODEL BOUNDARY",),
        "VARIANT_CONTRAST": ("CONTRAST", "VARIANT CONTRAST"),
    }.get(role, ())
    text = re.sub(r"\s+", " ", str(item.get("content", ""))).strip().upper()
    return any(text.startswith(cue) for cue in cues)


def make_study_renderer(impl):
    """Return tracked Study Guide renderer with learner-first presentation."""

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

            previous_heading: str | None = None
            refs = page_intent["content_refs"]
            index = 0
            while index < len(refs):
                ref = refs[index]
                meta = arc[ref]
                item = items[ref]
                role = meta.get("learner_visible_heading") or meta["role"].replace("_", " ")
                support = meta.get("support_state", "")
                if role != previous_heading:
                    if not _content_carries_visible_role(meta, item):
                        story.append(Paragraph(impl.legacy.safe(role), st["h2"]))
                    previous_heading = role

                if _pairable_generated_representation(item) and index + 1 < len(refs):
                    next_ref = refs[index + 1]
                    next_item = items[next_ref]
                    next_meta = arc[next_ref]
                    same_step_surface = (
                        next_meta.get("role") == meta.get("role")
                        and next_meta.get("support_state", "") == support
                    )
                    if same_step_surface and _pairable_generated_representation(next_item):
                        left = _representation_flowable(impl, reps[item["representation_instance_id"]], item)
                        right = _representation_flowable(impl, reps[next_item["representation_instance_id"]], next_item)
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
                    story.append(base._tracked(_representation_flowable(impl, rep, item), tracker, iid, item))
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
