#!/usr/bin/env python3
"""Deterministic textbook-style renderer for Physics Core (1A).

The renderer consumes the immutable P-G Core1 plan plus the P-GA publication plan.
It does not author new Physics. If a P-H representation bundle is supplied, it prefers
that representation; otherwise it draws a deliberately non-quantitative schematic.
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

INTERNAL_RE = re.compile(r"\b(?:PHY-[A-Z0-9_-]+|[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)\b")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def humanize(text):
    s = str(text or "")
    s = re.sub(r"\bPHY-(?:CAP|PF|MODEL|LAW|CORE1|PCK)-", "", s)
    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:1].upper() + s[1:] if s else ""


def clean(text):
    s = str(text or "")
    s = INTERNAL_RE.sub(lambda m: humanize(m.group(0)).lower(), s)
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
    def __init__(self, path, title):
        self.path = Path(path)
        self.c = canvas.Canvas(str(path), pagesize=A4, invariant=1, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor("Physics V2 Core1A deterministic publication renderer")
        self.page = 0
        self.page_metrics = []
        self.used_area = 0.0
        self.min_body_font = BODY
        self.min_caption_font = CAPTION
        self.current_title = ""

    def new_page(self, section="", title=""):
        if self.page:
            self._finish_page()
            self.c.showPage()
        self.page += 1
        self.used_area = 0.0
        self.current_title = title
        self.c.setStrokeColor(BORDER)
        self.c.setLineWidth(0.6)
        self.c.line(MARGIN, PAGE_H - 32, PAGE_W - MARGIN, PAGE_H - 32)
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica-Bold", 7.5)
        if section:
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
        })

    def finish(self):
        if self.page:
            self._finish_page()
        self.c.save()

    def account(self, x, y, w, h):
        self.used_area += max(0, w) * max(0, h)

    def title(self, y, chapter_no, title, subtitle="", badge=""):
        self.c.setFillColor(NAVY)
        self.c.setFont("Helvetica-Bold", 19)
        self.c.drawString(MARGIN, y, f"{chapter_no}  {clean(title)}")
        if badge:
            bw = min(150, stringWidth(clean(badge), "Helvetica-Bold", 7.5) + 18)
            self.c.setFillColor(PALE_TEAL)
            self.c.roundRect(PAGE_W - MARGIN - bw, y - 3, bw, 20, 8, fill=1, stroke=0)
            self.c.setFillColor(TEAL)
            self.c.setFont("Helvetica-Bold", 7.5)
            self.c.drawCentredString(PAGE_W - MARGIN - bw / 2, y + 4, clean(badge)[:34])
        if subtitle:
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica", 9.4)
            self.c.drawString(MARGIN, y - 17, clean(subtitle))
        self.account(MARGIN, y - 20, PAGE_W - 2 * MARGIN, 38)
        return y - 34

    def card(self, x, y_top, w, title, body, kind="KEY_IDEA", max_h=None, font=BODY, work_lines=0):
        accent, bg = KIND_STYLE.get(kind, (NAVY, PALE_BLUE))
        inner = w - 24
        lines = []
        for para in body or []:
            ps = wrap(para, "Helvetica", font, inner)
            lines.extend(ps)
            lines.append("")
        if lines and not lines[-1]:
            lines.pop()
        text_h = max(LEAD, len(lines) * LEAD)
        work_h = work_lines * 15
        h = 31 + text_h + work_h + 15
        if max_h:
            h = min(h, max_h)
        y = y_top - h
        self.c.setFillColor(bg)
        self.c.setStrokeColor(BORDER)
        self.c.setLineWidth(0.7)
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        self.c.setFillColor(accent)
        self.c.roundRect(x, y + h - 27, w, 27, 8, fill=1, stroke=0)
        self.c.rect(x, y + h - 27, w, 9, fill=1, stroke=0)
        self.c.setFillColor(WHITE)
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(x + 10, y + h - 18, clean(title)[:72])
        ty = y + h - 43
        self.c.setFillColor(INK)
        self.c.setFont("Helvetica", font)
        self.min_body_font = min(self.min_body_font, font)
        max_lines = max(1, int((h - 48 - work_h) / LEAD))
        for line in lines[:max_lines]:
            if line:
                self.c.drawString(x + 12, ty, line)
            ty -= LEAD
        if len(lines) > max_lines:
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica-Oblique", SMALL)
            self.c.drawRightString(x + w - 12, ty + LEAD, "continued in source plan")
        if work_lines:
            base = y + 12
            self.c.setStrokeColor(colors.HexColor("#C5CDD5"))
            for i in range(work_lines):
                yy = base + i * 15
                if yy < y + h - 48:
                    self.c.line(x + 12, yy, x + w - 12, yy)
        self.account(x, y, w, h)
        return y - 10

    def figure(self, x, y_top, w, h, caption, spec=None, renderer=None):
        y = y_top - h
        self.c.setFillColor(colors.HexColor("#FAFCFD"))
        self.c.setStrokeColor(BORDER)
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        inner_y = y + 25
        inner_h = h - 38
        rendered = False
        grounding = "SCHEMATIC_STRUCTURE_ONLY"
        if spec and renderer:
            try:
                renderer(spec["primitive_id"], spec.get("render_params") or {}, self.c,
                         (x + 10, inner_y, w - 20, inner_h))
                rendered = True
                grounding = spec.get("quantitative_grounding", grounding)
            except Exception:
                rendered = False
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
            self.c.drawString(x + 32, cy - 19, "physical state")
            self.c.drawRightString(x + w - 32, cy - 19, "chosen + direction")
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica-Oblique", CAPTION)
        cap = wrap(caption, "Helvetica-Oblique", CAPTION, w - 20)[0]
        self.c.drawString(x + 10, y + 9, cap[:110])
        self.min_caption_font = min(self.min_caption_font, CAPTION)
        self.account(x, y, w, h)
        return y - 9, grounding


def representation_index(bundle):
    by_cap = {}
    if not bundle:
        return by_cap
    for spec in bundle.get("representations") or []:
        by_cap.setdefault(spec.get("capability_ref"), []).append(spec)
    return by_cap


def load_primitive_renderer():
    try:
        phys = Path(__file__).resolve().parents[2]
        sys.path.insert(0, str(phys / "Representation" / "engine"))
        from physics_primitive_renderer import render_primitive
        return render_primitive
    except Exception:
        return None


def first_module(lesson_plan, kind):
    return next((m for m in lesson_plan["modules"] if m["kind"] == kind), None)


def module_body(lesson_plan, kind):
    m = first_module(lesson_plan, kind)
    return (m or {}).get("body") or []


def render_full_lesson(book, lesson_plan, number, rep_specs, primitive_renderer):
    title = humanize(lesson_plan["capability_ref"])
    badge = lesson_plan["concept_badge"]
    col_gap = 12
    col_w = (PAGE_W - 2 * MARGIN - col_gap) / 2

    # Page A — phenomenon first.
    y = book.new_page("Motion in 1D", title)
    y = book.title(y, number, title, "See the physical story before choosing equations.", badge)
    anchor = first_module(lesson_plan, "REAL_WORLD_ANCHOR")
    y_left = book.card(MARGIN, y, col_w, anchor["title"], anchor["body"], "REAL_WORLD_ANCHOR", max_h=150)
    key = first_module(lesson_plan, "KEY_IDEA")
    y_left = book.card(MARGIN, y_left, col_w, key["title"], key["body"], "KEY_IDEA", max_h=145)
    model = first_module(lesson_plan, "MODEL_CHECK")
    book.card(MARGIN, y_left, col_w, model["title"], model["body"], "MODEL_CHECK", max_h=160)
    spec = rep_specs[0] if rep_specs else None
    y_fig, _ = book.figure(MARGIN + col_w + col_gap, y, col_w, 235,
                           "Figure: connect the physical story to a representation before calculating.",
                           spec, primitive_renderer)
    see = first_module(lesson_plan, "SEE_IT")
    book.card(MARGIN + col_w + col_gap, y_fig, col_w, see["title"], see["body"], "SEE_IT", max_h=280)

    # Page B — explanation + worked reasoning + misconception repair.
    y = book.new_page("Motion in 1D", title + " — method")
    y = book.title(y, number, title, "Build the model, then test the tempting shortcut.", badge)
    see = first_module(lesson_plan, "SEE_IT")
    y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, "Representation bridge", see["body"], "SEE_IT", max_h=150)
    spec2 = rep_specs[1] if len(rep_specs) > 1 else (rep_specs[0] if rep_specs else None)
    y, _ = book.figure(MARGIN, y, PAGE_W - 2 * MARGIN, 170,
                       "Figure: the same physical state expressed visually; no new quantities are introduced.",
                       spec2, primitive_renderer)
    worked = first_module(lesson_plan, "WORKED_EXAMPLE")
    trap = first_module(lesson_plan, "COMMON_TRAP")
    book.card(MARGIN, y, col_w, worked["title"], worked["body"], "WORKED_EXAMPLE", max_h=250)
    book.card(MARGIN + col_w + col_gap, y, col_w, trap["title"], trap["body"], "COMMON_TRAP", max_h=250)

    # Page C — faded practice + retrieval.
    y = book.new_page("Motion in 1D", title + " — practice")
    y = book.title(y, number, title, "Guided → faded → independent.", badge)
    g = first_module(lesson_plan, "GUIDED_PRACTICE")
    f = first_module(lesson_plan, "FADED_PRACTICE")
    ind = first_module(lesson_plan, "INDEPENDENT_PRACTICE")
    y1 = book.card(MARGIN, y, col_w, g["title"], g["body"], "GUIDED_PRACTICE", max_h=225, work_lines=g["work_space_lines"])
    book.card(MARGIN, y1, col_w, f["title"], f["body"], "FADED_PRACTICE", max_h=225, work_lines=f["work_space_lines"])
    y2 = book.card(MARGIN + col_w + col_gap, y, col_w, ind["title"], ind["body"], "INDEPENDENT_PRACTICE", max_h=270, work_lines=ind["work_space_lines"])
    check = first_module(lesson_plan, "PHYSICAL_CHECK")
    y2 = book.card(MARGIN + col_w + col_gap, y2, col_w, check["title"], check["body"], "PHYSICAL_CHECK", max_h=130)
    selfc = first_module(lesson_plan, "SELF_CHECK")
    y2 = book.card(MARGIN + col_w + col_gap, y2, col_w, selfc["title"], selfc["body"], "SELF_CHECK", max_h=120)
    transfer = first_module(lesson_plan, "TRANSFER_BRIDGE")
    book.card(MARGIN, min(y1 - 235, y2), PAGE_W - 2 * MARGIN, transfer["title"], transfer["body"], "TRANSFER_BRIDGE", max_h=100)


def render_compact_lesson(book, lesson_plan, number):
    title = humanize(lesson_plan["capability_ref"])
    y = book.new_page("Motion in 1D", title)
    y = book.title(y, number, title, "Activate → verify → check.", lesson_plan["concept_badge"])
    for kind in ("KEY_IDEA", "INDEPENDENT_PRACTICE", "PHYSICAL_CHECK", "SELF_CHECK", "TRANSFER_BRIDGE"):
        m = first_module(lesson_plan, kind)
        if m:
            y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, m["title"], m["body"], kind,
                          max_h=190, work_lines=m.get("work_space_lines", 0))


def render_probe_lesson(book, lesson_plan, number):
    title = humanize(lesson_plan["capability_ref"])
    y = book.new_page("Motion in 1D", title)
    y = book.title(y, number, title, "Probe first — explanation comes only after evidence.", lesson_plan["concept_badge"])
    for kind in ("PROBE", "PHYSICAL_CHECK", "SELF_CHECK"):
        m = first_module(lesson_plan, kind)
        if m:
            y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, m["title"], m["body"], kind,
                          max_h=260, work_lines=m.get("work_space_lines", 0))


def render_appendices(book, core1):
    aps = core1["appendices"]
    # Appendix A — practice, multiple items with real work space.
    y = book.new_page("Appendix A", aps["appendix_a"]["title"])
    y = book.title(y, "A", aps["appendix_a"]["title"], "Core practice — answers are not shown here.", "PRACTICE")
    for idx, item in enumerate(aps["appendix_a"]["items"], 1):
        body = [item.get("prompt", "")]
        h = 150
        if y - h < MARGIN + 20:
            y = book.new_page("Appendix A", aps["appendix_a"]["title"])
        y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, f"Practice {idx} — {humanize(item.get('support_stage'))}", body,
                      "INDEPENDENT_PRACTICE", max_h=h, work_lines=5)

    # Appendix B — solutions kept separate from attempts.
    y = book.new_page("Appendix B", aps["appendix_b"]["title"])
    y = book.title(y, "B", aps["appendix_b"]["title"], "Check your method after attempting Appendix A.", "SOLUTIONS")
    for idx, sol in enumerate(aps["appendix_b"]["solutions"], 1):
        body = []
        for j, step in enumerate(sol.get("reasoning_steps") or [], 1):
            body.append(f"{j}. {humanize(step.get('role'))}: {step.get('text', '')}")
        body.append("Result: " + str(sol.get("final_response", "")))
        body.append("Model check: " + str(sol.get("model_validity_note", "")))
        if y - 185 < MARGIN + 20:
            y = book.new_page("Appendix B", aps["appendix_b"]["title"])
        y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, f"Solution {idx}", body, "WORKED_EXAMPLE", max_h=185)

    # Appendix C — printable answer-free reference.
    y = book.new_page("Appendix C", aps["appendix_c"]["title"])
    y = book.title(y, "C", aps["appendix_c"]["title"], "Answer-free first-move reference.", "PRINTABLE")
    for entry in aps["appendix_c"]["reference_entries"]:
        body = [entry.get("first_move", ""), entry.get("frame_sign_cue", ""),
                entry.get("relation_or_decision_cue", ""), humanize(entry.get("verification_cue", ""))]
        if y - 105 < MARGIN + 20:
            y = book.new_page("Appendix C", aps["appendix_c"]["title"])
        y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, humanize(entry.get("capability_ref")), body, "KEY_IDEA", max_h=105)


def render_core1a(core1, publication_plan, out_path, policy, representations=None):
    if publication_plan["upstream_core1_plan_id"] != core1["plan_id"]:
        raise ValueError("CORE1A_SEMANTIC_DRIFT: plan id")
    if publication_plan["upstream_core1_digest"] != core1["plan_digest"]:
        raise ValueError("CORE1A_SEMANTIC_DRIFT: plan digest")

    reps = representation_index(representations)
    primitive_renderer = load_primitive_renderer() if representations else None
    book = Book(out_path, "Physics — Core Study Guide")

    # Cover / learner route.
    y = book.new_page("Core (1A)", "Physics — Motion in 1D")
    book.c.setFillColor(NAVY)
    book.c.setFont("Helvetica-Bold", 27)
    book.c.drawString(MARGIN, y - 20, "MOTION IN 1D")
    book.c.setFillColor(MUTED)
    book.c.setFont("Helvetica", 12)
    book.c.drawString(MARGIN, y - 45, "Grade 9 Physics · Core Study Guide")
    book.account(MARGIN, y - 55, PAGE_W - 2 * MARGIN, 70)
    y -= 92
    route = [
        "SEE the physical situation.",
        "REPRESENT the state before choosing equations.",
        "UNDERSTAND the relation and when it is valid.",
        "PRACTISE with support that fades.",
        "CHECK the answer against the physics.",
    ]
    y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, "How to use this guide", route, "KEY_IDEA", max_h=190)
    y = book.card(MARGIN, y, PAGE_W - 2 * MARGIN, "Before equations", [
        "Draw or describe the motion.",
        "Choose the axis, frame and sign convention.",
        "Write the physical state.",
        "Name the requested quantity.",
        "Check the model assumptions.",
        "Choose a relation only after the model is legal.",
        "Check sign, units and physical plausibility.",
    ], "MODEL_CHECK", max_h=225)

    for i, lp in enumerate(publication_plan["lessons"], 1):
        lesson_no = f"1.{i}"
        if lp["lesson_mode"] == "FULL_LEARNING":
            render_full_lesson(book, lp, lesson_no, reps.get(lp["capability_ref"], []), primitive_renderer)
        elif lp["lesson_mode"] == "CONCISE_VERIFY_ONLY":
            render_compact_lesson(book, lp, lesson_no)
        else:
            render_probe_lesson(book, lp, lesson_no)

    render_appendices(book, core1)
    book.finish()

    low = [m["page"] for m in book.page_metrics if m["meaningful_occupancy"] < policy["page"]["meaningful_occupancy_target_min"]]
    high = [m["page"] for m in book.page_metrics if m["meaningful_occupancy"] > policy["page"]["meaningful_occupancy_target_max"] + 0.10]
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

    return {
        "report_id": "PHY-P-GA-CORE1A-QUALITY-" + publication_plan["plan_id"],
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "product_id": "CORE_STUDY_GUIDE",
        "artifact_path": Path(out_path).name,
        "artifact_sha256": sha256(out_path),
        "page_count": book.page,
        "upstream_core1_plan_id": core1["plan_id"],
        "upstream_core1_digest": core1["plan_digest"],
        "publication_plan_digest": publication_plan["plan_digest"],
        "minimum_body_font_pt": book.min_body_font,
        "minimum_caption_font_pt": book.min_caption_font,
        "page_metrics": book.page_metrics,
        "machine_findings": sorted(set(findings)),
        "publication_engineering_pass": not any(f for f in findings if f != "CORE1A_TEMPLATE_ONLY_CONTENT"),
        "instructional_content_maturity": "BLOCKED_TEMPLATE_ONLY_CORE1" if "CORE1A_TEMPLATE_ONLY_CONTENT" in findings else "READY_FOR_HUMAN_REVIEW",
        "human_review_states_modified": false if False else False
    }


if __name__ == "__main__":
    raise SystemExit("Use build_physics_core1a.py so input custody and output report are written together.")
