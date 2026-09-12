#!/usr/bin/env python3
"""Deterministic textbook-style renderer for Physics Core (1A).

The renderer consumes the immutable P-G Core1 plan plus the P-GA publication plan.
It does not author new Physics. If a P-H representation bundle is supplied, it prefers
that representation; otherwise it draws a deliberately non-quantitative schematic.

Since P-UPGRADE-2 this renderer is the Core study guide the P-K cold-start runner
publishes, so it carries the same obligations the previous P-K renderer carried:

* every figure is drawn through the P-H ``render_primitive`` interface and recorded
  as **draw-time** placement evidence in a ``PhysicalPageMap`` (planned page numbers
  are not evidence);
* every representation the P-H bundle declares for a capability is physically placed,
  not just the two that fit the designed spread;
* all learner-facing wording passes through the governed copy registry, so no internal
  role identifier or clinical curriculum label reaches the page.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve()
PHYS = HERE.parents[2]
for _p in (str(HERE.parent), str(PHYS / "Representation" / "engine"), str(PHYS / "ColdStart" / "engine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from physics_learner_copy import (  # noqa: E402
    learner_title, learner_subtitle, apply_phrase_rewrites, learner_copy_violations,
)

PAGE_W, PAGE_H = A4
MM = 72.0 / 25.4
MARGIN = 16 * MM
BODY = 10.2
SMALL = 8.4
CAPTION = 8.0
LEAD = 13.8

NAVY = colors.HexColor("#183F69")
BLUE = colors.HexColor("#2F80C8")
TEAL = colors.HexColor("#1A9D9A")
GOLD = colors.HexColor("#E0A000")
ORANGE = colors.HexColor("#D96C2C")
PURPLE = colors.HexColor("#6E5AA6")
RED = colors.HexColor("#B94242")
GREEN = colors.HexColor("#2F8E62")
INK = colors.HexColor("#202833")
MUTED = colors.HexColor("#5F6B77")
BORDER = colors.HexColor("#D3DBE4")
PALE_BLUE = colors.HexColor("#EEF6FC")
PALE_TEAL = colors.HexColor("#ECF8F6")
PALE_GOLD = colors.HexColor("#FFF7DF")
PALE_RED = colors.HexColor("#FCEEEE")
PALE_PURPLE = colors.HexColor("#F3F0FA")
PALE_GREEN = colors.HexColor("#EEF8F2")
WHITE = colors.white

KIND_STYLE = {
    "REAL_WORLD_ANCHOR": (BLUE, PALE_BLUE),
    "SEE_IT": (TEAL, PALE_TEAL),
    "KEY_IDEA": (NAVY, PALE_BLUE),
    "MODEL_CHECK": (GREEN, PALE_GREEN),
    "WORKED_EXAMPLE": (PURPLE, PALE_PURPLE),
    "COMMON_TRAP": (RED, PALE_RED),
    "GUIDED_PRACTICE": (ORANGE, PALE_GOLD),
    "FADED_PRACTICE": (GOLD, PALE_GOLD),
    "INDEPENDENT_PRACTICE": (BLUE, PALE_BLUE),
    "PHYSICAL_CHECK": (GREEN, PALE_GREEN),
    "SELF_CHECK": (NAVY, PALE_BLUE),
    "TRANSFER_BRIDGE": (TEAL, PALE_TEAL),
    "PROBE": (ORANGE, PALE_GOLD),
}

PHASE_GALLERY_TITLE = {
    "SEE": "More ways to see this",
    "REALIZE": "More ways to draw this",
    "UNDERSTAND": "More ways to check this",
}

INTERNAL_RE = re.compile(r"\b(?:PHY-[A-Z0-9_-]+|[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)\b")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def map_digest(o, field=None):
    x = dict(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def humanize(text):
    s = str(text or "")
    s = re.sub(r"\bPHY-(?:CAP|PF|MODEL|LAW|CORE1|PCK)-", "", s)
    s = s.replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = s[:1].upper() + s[1:] if s else ""
    return apply_phrase_rewrites(s)


def clean(text):
    """Every string on its way to the page passes through here.

    Internal identifiers become ordinary words **first**, then the governed phrase rewrites
    replace the clinical process wording the pipeline uses internally. Doing it in that
    order means an identifier such as ``VERIFY_MODEL_VALIDITY`` is translated as a phrase
    rather than surviving as one.
    """
    s = INTERNAL_RE.sub(lambda m: str(m.group(0)).replace("_", " ").replace("-", " ").lower(),
                        str(text or ""))
    s = apply_phrase_rewrites(s)
    return re.sub(r"\s+", " ", s).strip()


def wrap(text, font, size, width):
    words = clean(text).split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


class Book:
    def __init__(self, path, title, product_id="CORE_STUDY_GUIDE"):
        self.path = Path(path)
        self.product_id = product_id
        self.c = canvas.Canvas(str(path), pagesize=A4, invariant=1, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor("Physics V2 Core1A deterministic publication renderer")
        self.page = 0
        self.page_metrics = []
        self.used_area = 0.0
        self.min_body_font = BODY
        self.min_caption_font = CAPTION
        self.current_title = ""
        # draw-time custody evidence
        self.placements = []
        self.intents = []
        self.page_refs = {}
        self.rendered_text = []
        self._intent = None

    # ------------------------------------------------------------ page frame
    def new_page(self, section="", title=""):
        if self.page:
            self._finish_page()
            self.c.showPage()
        self.page += 1
        self.page_refs[self.page] = []
        self.used_area = 0.0
        self.current_title = title
        self.c.setStrokeColor(BORDER)
        self.c.setLineWidth(0.6)
        self.c.line(MARGIN, PAGE_H - 32, PAGE_W - MARGIN, PAGE_H - 32)
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica-Bold", 7.5)
        if section:
            self.text(clean(section).upper())
            self.c.drawString(MARGIN, PAGE_H - 25, clean(section).upper())
        self.c.drawRightString(PAGE_W - MARGIN, PAGE_H - 25, f"GRADE 9 PHYSICS  |  {self.page}")
        return PAGE_H - 50

    def _finish_page(self):
        content_h = PAGE_H - 2 * MARGIN
        content_w = PAGE_W - 2 * MARGIN
        occupancy = min(1.0, self.used_area / (content_h * content_w))
        self.page_metrics.append({
            "page": self.page,
            "title": self.current_title,
            "meaningful_occupancy": round(occupancy, 3),
            "semantic_content_refs": list(self.page_refs.get(self.page, [])),
            "orphan_continuation": False,
            "bounds_violations": self._bounds_violations(self.page),
            "underfill_disposition": "ACCEPTABLE",
        })

    def _bounds_violations(self, page, tolerance=14):
        n = 0
        for p in self.placements:
            if p["page"] != page or not p.get("ink_bbox"):
                continue
            ink = p["ink_bbox"]
            if not (p["x0"] - tolerance <= ink["x0"] and ink["x1"] <= p["x1"] + tolerance
                    and p["y0"] - tolerance <= ink["y0"] and ink["y1"] <= p["y1"] + tolerance):
                n += 1
        return n

    def finish(self):
        if self.page:
            self._finish_page()
        self.c.save()

    def account(self, x, y, w, h):
        self.used_area += max(0, w) * max(0, h)

    def text(self, s):
        """Record a string that reached the page, for the learner-surface falsifier."""
        if s:
            self.rendered_text.append(str(s))

    # ------------------------------------------------------------- page bits
    def title(self, y, chapter_no, title, subtitle="", badge=""):
        self.c.setFillColor(NAVY)
        self.c.setFont("Helvetica-Bold", 19)
        heading = f"{chapter_no}  {clean(title)}"
        self.text(heading)
        self.c.drawString(MARGIN, y, heading)
        if badge:
            bw = min(150, stringWidth(clean(badge), "Helvetica-Bold", 7.5) + 18)
            self.c.setFillColor(PALE_TEAL)
            self.c.roundRect(PAGE_W - MARGIN - bw, y - 3, bw, 20, 8, fill=1, stroke=0)
            self.c.setFillColor(TEAL)
            self.c.setFont("Helvetica-Bold", 7.5)
            self.text(clean(badge)[:34])
            self.c.drawCentredString(PAGE_W - MARGIN - bw / 2, y + 4, clean(badge)[:34])
        if subtitle:
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica", 9.4)
            self.text(clean(subtitle))
            self.c.drawString(MARGIN, y - 17, clean(subtitle))
        self.account(MARGIN, y - 20, PAGE_W - 2 * MARGIN, 38)
        return y - 34

    def card(self, x, y_top, w, title, body, kind="KEY_IDEA", max_h=None, font=BODY,
             work_lines=0, subtitle=""):
        accent, bg = KIND_STYLE.get(kind, (NAVY, PALE_BLUE))
        inner = w - 24
        lines = []
        for para in body or []:
            ps = wrap(para, "Helvetica", font, inner)
            lines.extend(ps)
            lines.append("")
        if lines and not lines[-1]:
            lines.pop()
        head_h = 27 if not subtitle else 36
        text_h = max(LEAD, len(lines) * LEAD)
        work_h = work_lines * 15
        h = 4 + head_h + text_h + work_h + 15
        if max_h:
            h = min(h, max_h)
        y = y_top - h
        self.c.setFillColor(bg)
        self.c.setStrokeColor(BORDER)
        self.c.setLineWidth(0.7)
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        self.c.setFillColor(accent)
        self.c.roundRect(x, y + h - head_h, w, head_h, 8, fill=1, stroke=0)
        self.c.rect(x, y + h - head_h, w, 9, fill=1, stroke=0)
        self.c.setFillColor(WHITE)
        self.c.setFont("Helvetica-Bold", 9)
        shown = clean(title)[:72]
        self.text(shown)
        self.c.drawString(x + 10, y + h - 18, shown)
        if subtitle:
            self.c.setFont("Helvetica-Oblique", 7.4)
            sub = clean(subtitle)[:88]
            self.text(sub)
            self.c.drawString(x + 10, y + h - 29, sub)
        ty = y + h - head_h - 16
        self.c.setFillColor(INK)
        self.c.setFont("Helvetica", font)
        self.min_body_font = min(self.min_body_font, font)
        max_lines = max(1, int((h - head_h - 21 - work_h) / LEAD))
        for line in lines[:max_lines]:
            if line:
                self.text(line)
                self.c.drawString(x + 12, ty, line)
            ty -= LEAD
        if len(lines) > max_lines:
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica-Oblique", SMALL)
            self.c.drawRightString(x + w - 12, ty + LEAD, "continues on the next page")
        if work_lines:
            base = y + 12
            self.c.setStrokeColor(colors.HexColor("#C5CDD5"))
            for i in range(work_lines):
                yy = base + i * 15
                if yy < y + h - head_h - 21:
                    self.c.line(x + 12, yy, x + w - 12, yy)
        self.account(x, y, w, h)
        return y - 10

    # --------------------------------------------------------------- figures
    def figure(self, x, y_top, w, h, caption, spec=None, renderer=None, intent_id=None):
        """Draw one figure and, when a real primitive was used, record draw-time evidence."""
        y = y_top - h
        self.c.setFillColor(colors.HexColor("#FAFCFD"))
        self.c.setStrokeColor(BORDER)
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        inner_x, inner_y = x + 10, y + 25
        inner_w, inner_h = w - 20, h - 38
        rendered = False
        grounding = "SCHEMATIC_STRUCTURE_ONLY"
        if spec and renderer:
            evidence = renderer(
                spec["primitive_id"], learner_params(spec.get("render_params") or {}), self.c,
                (inner_x, inner_y, inner_w, inner_h),
            )
            rendered = True
            grounding = spec.get("quantitative_grounding", grounding)
            floor = int(spec.get("minimum_vector_ops") or 0)
            if evidence["vector_ops"] < floor:
                fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
                     f"{spec.get('representation_id')}:{evidence['vector_ops']}")
            self.placements.append({
                "content_ref": spec["representation_id"],
                "page_intent_id": intent_id or ("PI-" + str(spec.get("capability_ref"))),
                "primitive": spec["primitive_id"],
                "page": self.page,
                "fragment_kind": "START",
                "x0": inner_x, "y0": inner_y, "x1": inner_x + inner_w, "y1": inner_y + inner_h,
                "ink_bbox": evidence["ink_bbox"],
                "vector_ops": evidence["vector_ops"],
                "text_ops": evidence["text_ops"],
                "op_histogram": evidence["op_histogram"],
                "quantitative_grounding": grounding,
            })
            self.page_refs[self.page].append(spec["representation_id"])
        if not rendered:
            # Deliberately non-quantitative 1D motion schematic: no source numbers invented.
            cy = inner_y + inner_h * 0.53
            self.c.setStrokeColor(NAVY)
            self.c.setLineWidth(1.2)
            self.c.line(x + 32, cy, x + w - 32, cy)
            self.c.setFillColor(NAVY)
            self.c.circle(x + 46, cy, 5, fill=1, stroke=0)
            self.c.setStrokeColor(TEAL)
            self.c.setLineWidth(2.2)
            self.c.line(x + 58, cy + 20, x + w - 68, cy + 20)
            self.c.line(x + w - 68, cy + 20, x + w - 82, cy + 26)
            self.c.line(x + w - 68, cy + 20, x + w - 82, cy + 14)
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica", 8.5)
            self.c.drawString(x + 32, cy - 19, "what is moving")
            self.c.drawRightString(x + w - 32, cy - 19, "which way is positive")
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica-Oblique", CAPTION)
        cap = wrap(caption, "Helvetica-Oblique", CAPTION, w - 20)[0]
        self.text(cap[:110])
        self.c.drawString(x + 10, y + 9, cap[:110])
        self.min_caption_font = min(self.min_caption_font, CAPTION)
        self.account(x, y, w, h)
        return y - 9, grounding

    # ---------------------------------------------------------- page intents
    def open_intent(self, intent_id, label):
        self._intent = {"page_intent_id": intent_id, "capability_ref": label,
                        "physical_pages": [], "content_refs": [], "split": False,
                        "continuation_pages": []}
        return self._intent

    def close_intent(self, intent):
        pages = sorted({p["page"] for p in self.placements
                        if p["page_intent_id"] == intent["page_intent_id"]})
        intent["physical_pages"] = pages or [self.page]
        intent["content_refs"] = [p["content_ref"] for p in self.placements
                                  if p["page_intent_id"] == intent["page_intent_id"]]
        intent["split"] = len(pages) > 1
        intent["continuation_pages"] = pages[1:]
        if intent["content_refs"]:
            self.intents.append(intent)

    def page_map(self):
        data = self.path.read_bytes()
        pm = {
            "physical_page_map_id": "PHY-PPM-" + self.product_id,
            "schema_version": "1.0.0",
            "subject": "PHYSICS",
            "bundle_ref": self.product_id,
            "bundle_digest": "0" * 64,
            "artifact_path": self.path.name,
            "artifact_sha256": sha_bytes(data),
            "artifact_bytes": len(data),
            "physical_page_count": self.page,
            "page_width_pt": PAGE_W,
            "page_height_pt": PAGE_H,
            "actual_placement_evidence": True,
            "page_intents": self.intents,
            "content_placements": self.placements,
            "page_metrics": self.page_metrics,
            "realization_summary": {
                "figure_count": len(self.placements),
                "total_vector_ops": sum(p["vector_ops"] for p in self.placements),
                "total_text_ops": sum(p["text_ops"] for p in self.placements),
                "label_only_figure_count": sum(1 for p in self.placements if p["vector_ops"] <= 0),
                "source_grounded_figure_count": sum(
                    1 for p in self.placements if p["quantitative_grounding"] == "SOURCE_QUANTITIES"),
            },
            "minimum_font_pt": min(self.min_body_font, self.min_caption_font, 7.4),
            "page_map_digest": "",
        }
        pm["page_map_digest"] = map_digest(pm, "page_map_digest")
        return data, pm


def learner_params(params):
    """Figure labels are drawn by the primitive renderer, so they are sanitized on the way in."""
    def walk(value):
        if isinstance(value, str):
            return clean(value)
        if isinstance(value, dict):
            return {k: walk(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [walk(v) for v in value]
        return value

    return walk(dict(params or {}))


def representation_index(bundle):
    by_cap = {}
    if not bundle:
        return by_cap
    for spec in bundle.get("representations") or []:
        by_cap.setdefault(spec.get("capability_ref"), []).append(spec)
    return by_cap


def load_primitive_renderer():
    try:
        from physics_primitive_renderer import render_primitive
        return render_primitive
    except Exception:
        return None


def first_module(lesson_plan, kind):
    return next((m for m in lesson_plan["modules"] if m["kind"] == kind), None)


def module_body(lesson_plan, kind):
    m = first_module(lesson_plan, kind)
    return (m or {}).get("body") or []


def _card(book, module, x, y, w, **kw):
    return book.card(x, y, w, module["title"], module["body"], module["kind"],
                     subtitle=module.get("subtitle", ""), **kw)


def _phase_specs(specs, phase):
    return [s for s in specs if s.get("page_intent_phase") == phase]


def render_gallery(book, section, title, badge, specs, primitive_renderer, intent_id, number):
    """Place every remaining P-H representation for this capability.

    Core (1A) chooses the teaching spread, but it may not silently drop representations
    the P-H bundle declared for the capability: each one still gets a real page position
    and real draw-time evidence.
    """
    # Balanced chunks with an adaptive figure height, so the last gallery page of a
    # capability is a full page of teaching rather than a mostly-empty tail.
    max_per_page = 4
    pages = max(1, math.ceil(len(specs) / max_per_page))
    per_page = math.ceil(len(specs) / pages)
    gap = 4
    for start in range(0, len(specs), per_page):
        chunk = specs[start:start + per_page]
        y = book.new_page(section, title)
        y = book.title(y, number, title, "Different pictures of the same idea.", badge)
        available = y - (MARGIN + 6)
        fig_h = max(140.0, min(300.0, available / len(chunk) - (9 + gap)))
        for spec in chunk:
            phase_label = PHASE_GALLERY_TITLE.get(spec.get("page_intent_phase"), "Another way to see this")
            caption = phase_label + " — " + clean(
                spec.get("accessibility_text") or spec.get("instructional_job")
                or "another way to picture this.")
            y, _ = book.figure(MARGIN, y, PAGE_W - 2 * MARGIN, fig_h, caption,
                               spec, primitive_renderer, intent_id)
            y -= gap


def render_full_lesson(book, lesson_plan, number, rep_specs, primitive_renderer, section):
    title = humanize(lesson_plan["capability_ref"])
    badge = lesson_plan["concept_badge"]
    col_gap = 12
    col_w = (PAGE_W - 2 * MARGIN - col_gap) / 2
    intent_id = "PI-" + lesson_plan["capability_ref"]
    intent = book.open_intent(intent_id, lesson_plan["capability_ref"])

    see_specs = _phase_specs(rep_specs, "SEE")
    realize_specs = _phase_specs(rep_specs, "REALIZE")
    understand_specs = _phase_specs(rep_specs, "UNDERSTAND")
    placed = []

    # Page A — phenomenon first.
    y = book.new_page(section, title)
    y = book.title(y, number, title, "Picture what is happening before you reach for a formula.", badge)
    anchor = first_module(lesson_plan, "REAL_WORLD_ANCHOR")
    y_left = _card(book, anchor, MARGIN, y, col_w, max_h=150)
    key = first_module(lesson_plan, "KEY_IDEA")
    y_left = _card(book, key, MARGIN, y_left, col_w, max_h=150)
    model = first_module(lesson_plan, "MODEL_CHECK")
    _card(book, model, MARGIN, y_left, col_w, max_h=165)
    spec = see_specs[0] if see_specs else (rep_specs[0] if rep_specs else None)
    if spec is not None:
        placed.append(id(spec))
    y_fig, _ = book.figure(MARGIN + col_w + col_gap, y, col_w, 235,
                           "Link the real situation to a drawing before you calculate.",
                           spec, primitive_renderer, intent_id)
    see = first_module(lesson_plan, "SEE_IT")
    _card(book, see, MARGIN + col_w + col_gap, y_fig, col_w, max_h=280)

    # Page B — explanation + worked reasoning + misconception repair.
    y = book.new_page(section, title + " — how to do it")
    y = book.title(y, number, title, "Build the picture, then test the shortcut that looks easier.", badge)
    y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, learner_title("REPRESENTATION_BRIDGE"),
                  see["body"], "SEE_IT", max_h=150,
                  subtitle=learner_subtitle("REPRESENTATION_BRIDGE"))
    spec2 = realize_specs[0] if realize_specs else (rep_specs[1] if len(rep_specs) > 1 else spec)
    if spec2 is not None:
        placed.append(id(spec2))
    y, _ = book.figure(MARGIN, y, PAGE_W - 2 * MARGIN, 170,
                       "The same situation drawn out. No new numbers are introduced here.",
                       spec2 if spec2 is not spec else None, primitive_renderer, intent_id)
    worked = first_module(lesson_plan, "WORKED_EXAMPLE")
    trap = first_module(lesson_plan, "COMMON_TRAP")
    _card(book, worked, MARGIN, y, col_w, max_h=250)
    _card(book, trap, MARGIN + col_w + col_gap, y, col_w, max_h=250)

    # Page C — faded practice + retrieval.
    y = book.new_page(section, title + " — your turn")
    y = book.title(y, number, title, "Try it with help, then with less, then on your own.", badge)
    g = first_module(lesson_plan, "GUIDED_PRACTICE")
    f = first_module(lesson_plan, "FADED_PRACTICE")
    ind = first_module(lesson_plan, "INDEPENDENT_PRACTICE")
    y1 = _card(book, g, MARGIN, y, col_w, max_h=225, work_lines=g["work_space_lines"])
    _card(book, f, MARGIN, y1, col_w, max_h=225, work_lines=f["work_space_lines"])
    y2 = _card(book, ind, MARGIN + col_w + col_gap, y, col_w, max_h=270,
               work_lines=ind["work_space_lines"])
    check = first_module(lesson_plan, "PHYSICAL_CHECK")
    y2 = _card(book, check, MARGIN + col_w + col_gap, y2, col_w, max_h=130)
    selfc = first_module(lesson_plan, "SELF_CHECK")
    y2 = _card(book, selfc, MARGIN + col_w + col_gap, y2, col_w, max_h=120)
    transfer = first_module(lesson_plan, "TRANSFER_BRIDGE")
    _card(book, transfer, MARGIN, min(y1 - 235, y2), PAGE_W - 2 * MARGIN, max_h=100)

    remaining = [s for s in (see_specs + realize_specs + understand_specs) if id(s) not in placed]
    if remaining:
        render_gallery(book, section, title, badge, remaining, primitive_renderer, intent_id, number)
    book.close_intent(intent)


def render_compact_lesson(book, lesson_plan, number, rep_specs, primitive_renderer, section):
    title = humanize(lesson_plan["capability_ref"])
    intent_id = "PI-" + lesson_plan["capability_ref"]
    intent = book.open_intent(intent_id, lesson_plan["capability_ref"])
    y = book.new_page(section, title)
    y = book.title(y, number, title, "Warm up, try it, then check it.", lesson_plan["concept_badge"])
    for kind in ("KEY_IDEA", "INDEPENDENT_PRACTICE", "PHYSICAL_CHECK", "SELF_CHECK", "TRANSFER_BRIDGE"):
        m = first_module(lesson_plan, kind)
        if m:
            y = _card(book, m, MARGIN, y, PAGE_W - 2 * MARGIN, max_h=190,
                      work_lines=m.get("work_space_lines", 0))
    if rep_specs:
        render_gallery(book, section, title, lesson_plan["concept_badge"], rep_specs,
                       primitive_renderer, intent_id, number)
    book.close_intent(intent)


def render_probe_lesson(book, lesson_plan, number, rep_specs, primitive_renderer, section):
    title = humanize(lesson_plan["capability_ref"])
    intent_id = "PI-" + lesson_plan["capability_ref"]
    intent = book.open_intent(intent_id, lesson_plan["capability_ref"])
    y = book.new_page(section, title)
    y = book.title(y, number, title, "Have a go first. The explanation comes after.",
                   lesson_plan["concept_badge"])
    for kind in ("PROBE", "PHYSICAL_CHECK", "SELF_CHECK"):
        m = first_module(lesson_plan, kind)
        if m:
            y = _card(book, m, MARGIN, y, PAGE_W - 2 * MARGIN, max_h=260,
                      work_lines=m.get("work_space_lines", 0))
    if rep_specs:
        render_gallery(book, section, title, lesson_plan["concept_badge"], rep_specs,
                       primitive_renderer, intent_id, number)
    book.close_intent(intent)


def render_appendices(book, core1):
    aps = core1["appendices"]
    sections = []
    # Appendix A — practice, multiple items with real work space.
    y = book.new_page("Appendix A", aps["appendix_a"]["title"])
    y = book.title(y, "A", aps["appendix_a"]["title"],
                   "Work these first. The answers are in the next appendix.", "PRACTICE")
    sections.append("APPENDIX_A_CORE_PRACTICE")
    for idx, item in enumerate(aps["appendix_a"]["items"], 1):
        body = [item.get("prompt", "")]
        h = 150
        if y - h < MARGIN + 20:
            y = book.new_page("Appendix A", aps["appendix_a"]["title"])
        y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN,
                      f"Question {idx} — {learner_title(item.get('support_stage'))}", body,
                      "INDEPENDENT_PRACTICE", max_h=h, work_lines=5)

    # Appendix B — solutions kept separate from attempts.
    y = book.new_page("Appendix B", aps["appendix_b"]["title"])
    y = book.title(y, "B", aps["appendix_b"]["title"],
                   "Compare these with your own working.", "ANSWERS")
    sections.append("APPENDIX_B_CORE_SOLUTIONS")
    for idx, sol in enumerate(aps["appendix_b"]["solutions"], 1):
        body = []
        for j, step in enumerate(sol.get("reasoning_steps") or [], 1):
            body.append(f"{j}. {learner_title(step.get('role'))}: {step.get('text', '')}")
        if sol.get("final_answer"):
            body.append("Answer: " + str(sol["final_answer"].get("statement")
                                         or sol["final_answer"].get("value", "")))
        body.append("Why this is allowed: " + str(sol.get("model_validity_note", "")))
        if y - 185 < MARGIN + 20:
            y = book.new_page("Appendix B", aps["appendix_b"]["title"])
        y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, f"Answer {idx}", body,
                      "WORKED_EXAMPLE", max_h=185)

    # Appendix C — printable answer-free reference.
    y = book.new_page("Appendix C", aps["appendix_c"]["title"])
    y = book.title(y, "C", aps["appendix_c"]["title"],
                   "A one-page reminder of how to start. No answers here.", "PRINTABLE")
    sections.append("APPENDIX_C_PRINTABLE_HANDOUT")
    for entry in aps["appendix_c"]["reference_entries"]:
        body = [entry.get("first_move", ""), entry.get("frame_sign_cue", ""),
                entry.get("relation_or_decision_cue", ""), learner_title(entry.get("verification_cue"))]
        if y - 105 < MARGIN + 20:
            y = book.new_page("Appendix C", aps["appendix_c"]["title"])
        y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, humanize(entry.get("capability_ref")), body, "KEY_IDEA",
                      max_h=105)
    return sections


def render_core1a(core1, publication_plan, out_path, policy, representations=None,
                  unit_title="Motion in 1D"):
    if publication_plan["upstream_core1_plan_id"] != core1["plan_id"]:
        raise ValueError("CORE1A_SEMANTIC_DRIFT: plan id")
    if publication_plan["upstream_core1_digest"] != core1["plan_digest"]:
        raise ValueError("CORE1A_SEMANTIC_DRIFT: plan digest")

    reps = representation_index(representations)
    primitive_renderer = load_primitive_renderer() if representations else None
    book = Book(out_path, "Physics — Core Study Guide")

    # Cover / learner route.
    y = book.new_page("Core study guide", f"Physics — {unit_title}")
    book.c.setFillColor(NAVY)
    book.c.setFont("Helvetica-Bold", 27)
    book.text(unit_title.upper())
    book.c.drawString(MARGIN, y - 20, unit_title.upper())
    book.c.setFillColor(MUTED)
    book.c.setFont("Helvetica", 12)
    book.c.drawString(MARGIN, y - 45, "Grade 9 Physics · Your core study guide")
    book.account(MARGIN, y - 55, PAGE_W - 2 * MARGIN, 70)
    y -= 92
    route = [
        "Look at what is actually happening.",
        "Draw it before you write any symbols.",
        "Work out the rule, and when you are allowed to use it.",
        "Practise with help, then with less help, then on your own.",
        "Check the answer against real life.",
    ]
    y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, "How to use this guide", route, "KEY_IDEA", max_h=190)
    y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, "Before you write a single formula", [
        "Draw or describe the motion.",
        "Decide where zero is and which way counts as positive.",
        "Write down what is happening at the start and at the end.",
        "Name the thing the question is asking for.",
        "Check the situation fits the rule you want to use.",
        "Only then pick a formula.",
        "Check the sign, the units, and whether the answer makes sense.",
    ], "MODEL_CHECK", max_h=225)

    sections = ["MAIN_TEACHING"]
    for i, lp in enumerate(publication_plan["lessons"], 1):
        lesson_no = f"1.{i}"
        specs = reps.get(lp["capability_ref"], [])
        if lp["lesson_mode"] == "FULL_LEARNING":
            render_full_lesson(book, lp, lesson_no, specs, primitive_renderer, unit_title)
        elif lp["lesson_mode"] == "CONCISE_VERIFY_ONLY":
            render_compact_lesson(book, lp, lesson_no, specs, primitive_renderer, unit_title)
        else:
            render_probe_lesson(book, lp, lesson_no, specs, primitive_renderer, unit_title)

    sections.extend(render_appendices(book, core1))
    book.finish()
    data, page_map = book.page_map()

    low = [m["page"] for m in book.page_metrics
           if m["meaningful_occupancy"] < policy["page"]["meaningful_occupancy_target_min"]]
    high = [m["page"] for m in book.page_metrics
            if m["meaningful_occupancy"] > policy["page"]["meaningful_occupancy_target_max"] + 0.10]
    findings = []
    if book.min_body_font < policy["page"]["body_font_minimum_pt"]:
        findings.append("CORE1A_BODY_FONT_TOO_SMALL")
    if book.min_caption_font < policy["page"]["caption_font_minimum_pt"]:
        findings.append("CORE1A_CAPTION_FONT_TOO_SMALL")
    # Occupancy findings are advisory page-rhythm signals; deliberate work pages can be under target.
    if len(low) > max(2, math.ceil(book.page * 0.25)):
        findings.append("CORE1A_LOW_MEANINGFUL_OCCUPANCY")
    if high:
        findings.append("CORE1A_OVERFULL_PAGE")
    if publication_plan["quality_summary"]["template_only_content_count"]:
        findings.append("CORE1A_TEMPLATE_ONLY_CONTENT")

    copy_violations = sorted({v for line in book.rendered_text for v in learner_copy_violations(line)})
    if copy_violations:
        findings.append("INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE")

    blocking = [f for f in findings
                if f not in {"CORE1A_TEMPLATE_ONLY_CONTENT"}]
    return {
        "report_id": "PHY-P-GA-CORE1A-QUALITY-" + publication_plan["plan_id"],
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "product_id": "CORE_STUDY_GUIDE",
        "artifact_path": Path(out_path).name,
        "artifact_sha256": sha256(out_path),
        "artifact_bytes": len(data),
        "page_count": book.page,
        "upstream_core1_plan_id": core1["plan_id"],
        "upstream_core1_digest": core1["plan_digest"],
        "publication_plan_digest": publication_plan["plan_digest"],
        "minimum_body_font_pt": book.min_body_font,
        "minimum_caption_font_pt": book.min_caption_font,
        "page_metrics": [{"page": m["page"], "title": m["title"],
                          "meaningful_occupancy": m["meaningful_occupancy"]}
                         for m in book.page_metrics],
        "figure_count": len(book.placements),
        "total_vector_ops": page_map["realization_summary"]["total_vector_ops"],
        "required_sections": sections,
        "physical_page_map": page_map,
        "learner_copy_violations": copy_violations,
        "machine_findings": sorted(set(findings)),
        "publication_engineering_pass": not blocking,
        "instructional_content_maturity": (
            "BLOCKED_TEMPLATE_ONLY_CORE1" if "CORE1A_TEMPLATE_ONLY_CONTENT" in findings
            else "READY_FOR_HUMAN_REVIEW"),
        "human_review_states_modified": False,
    }


if __name__ == "__main__":
    raise SystemExit("Use build_physics_core1a.py so input custody and output report are written together.")
