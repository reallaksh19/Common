#!/usr/bin/env python3
"""Deterministic learner-facing Physics product renderer (Core1 study guide + Core2 transfer book).

Two products, never three: Appendix C is a section of the Core study guide, not a
separate PDF. Every figure is drawn through the P-H ``render_primitive`` interface, so
the same draw-time vector-operation evidence and physical-page custody apply to the
learner products as to the P-H representation proof.
"""
import hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve()
PHYS = HERE.parents[2]
sys.path[:0] = [str(PHYS / "Representation" / "engine")]

from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: E402
from physics_primitive_renderer import (  # noqa: E402
    render_primitive, TracingCanvas, FONT_NAME, FONT_BOLD, Palette, draw_card_box,
)
from physics_page_custody import reconciliation_errors  # noqa: E402

PAGE_W, PAGE_H = 595.2756, 841.8898
MARGIN = 42
BODY = 8.6
LEAD = 11.6
FIG_H = 132


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(o, field=None):
    x = dict(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


import re  # noqa: E402

# Every internal identifier shape that must never reach a learner page. The P-L gate
# re-scans the extracted PDF text for these, so the sanitizer and the gate agree.
INTERNAL_REF_RE = re.compile(
    r"\bPHY-(?:CAP|PF|MODEL|LAW|CORE1|CORE2|P-[A-L])[A-Z0-9\-]*|"
    r"\b(?:REP|PI|A|B-SOL)-[A-Z0-9\-]{4,}|"
    r"\bPHY-EXT\d+\b"
)
INTERNAL_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
PHRASE_REPLACEMENTS = [
    ("Original external transfer items remain reserved for Core2.",
     "Attempt the transfer questions only after this unit."),
    ("original external transfer items stay reserved for Core2",
     "attempt the transfer questions only after this unit"),
    ("Work a newly authored instance of this family",
     "Work this practice instance"),
    ("Authored Core1 instance for", "Practice instance for"),
    ("Core1", "this guide"),
    ("Core2", "the transfer book"),
    ("StudyModel", "study plan"),
    ("P-D", "the reasoning route"),
    ("P-F", "the study plan"),
]


def human(ref):
    """Turn an internal ref into learner-facing wording."""
    text = str(ref or "")
    for prefix in ("PHY-CAP-", "PHY-PF-", "PHY-MODEL-", "PHY-LAW-", "PHY-CORE2-", "PHY-CORE1-",
                   "PHY-EXT", "REP-", "OBLIGATION_LEVEL:", "OBLIGATION_REP:", "REQUIRED:", "PROBE:"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    text = text.replace("_", " ").replace("-", " ").strip().lower()
    return text[:1].upper() + text[1:] if text else ""


def learner_text(text):
    """Sanitize any string on its way to a learner page.

    Internal identifiers and SCREAMING_SNAKE tokens are engineering vocabulary. A learner
    page that shows them is the defect the Chemistry C-L remediation had to fix, so the
    Physics product renderer removes them at the single point where text reaches the page.
    """
    s = str(text or "")
    for old, new in PHRASE_REPLACEMENTS:
        s = s.replace(old, new)
    s = INTERNAL_REF_RE.sub(lambda m: human(m.group(0)).lower(), s)
    s = INTERNAL_TOKEN_RE.sub(lambda m: m.group(0).replace("_", " ").lower(), s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s


def residual_internal_tokens(text):
    """Whatever the sanitizer would still let through. Used by the P-L learner-surface gate."""
    s = str(text or "")
    return sorted(set(INTERNAL_REF_RE.findall(s)) | set(INTERNAL_TOKEN_RE.findall(s)))


def learner_params(params):
    """Sanitize a figure's render parameters for a learner page.

    The P-H representation proof is an engineering artifact and may show internal refs.
    A learner product may not, and figure labels are drawn by the primitive renderer
    rather than through ProductWriter, so they are sanitized here on the way in.
    """
    def walk(value):
        if isinstance(value, str):
            return learner_text(value)
        if isinstance(value, dict):
            return {k: walk(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [walk(v) for v in value]
        return value

    return walk(dict(params or {}))


def wrap(text, font, size, width):
    words = str(text or "").split()
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


class ProductWriter:
    """Canvas wrapper that records draw-time placement evidence for every block."""

    def __init__(self, path, title, product_id):
        self.path = Path(path)
        self.product_id = product_id
        self.c = rl_canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), invariant=1, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor("Physics V2 deterministic learner-product renderer")
        self.page = 0
        self.y = 0
        self.placements = []
        self.intents = []
        self.page_refs = {}
        self.min_font = BODY
        self.new_page()

    # ---------------------------------------------------------------- layout
    def new_page(self):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.page_refs[self.page] = []
        self.y = PAGE_H - MARGIN
        self.c.setFont(FONT_BOLD, 7)
        self.c.setFillColor(Palette.TEXT_MUTED)
        self.c.drawRightString(PAGE_W - MARGIN, PAGE_H - 26, f"PHYSICS | {self.page}")
        self.c.setStrokeColor(Palette.BORDER_LIGHT)
        self.c.setLineWidth(0.6)
        self.c.line(MARGIN, PAGE_H - 32, PAGE_W - MARGIN, PAGE_H - 32)
        self.y = PAGE_H - 48

    def ensure(self, height):
        if self.y - height < MARGIN + 14:
            self.new_page()

    # ------------------------------------------------------------- text bits
    def heading(self, text, size=13, colour=None):
        self.ensure(size + 16)
        self.c.setFont(FONT_BOLD, size)
        self.c.setFillColor(colour or Palette.PHYSICS_DARK)
        self.c.drawString(MARGIN, self.y, learner_text(text))
        self.y -= size + 8
        self.min_font = min(self.min_font, size)

    def subheading(self, text):
        self.ensure(20)
        self.c.setFont(FONT_BOLD, 9.4)
        self.c.setFillColor(Palette.TEXT_PRIMARY)
        self.c.drawString(MARGIN, self.y, learner_text(text))
        self.y -= 14
        self.min_font = min(self.min_font, 9.4)

    def para(self, text, indent=0, size=BODY, font=FONT_NAME, colour=None):
        text = learner_text(text)
        if not text:
            return
        width = PAGE_W - 2 * MARGIN - indent
        for line in wrap(text, font, size, width):
            self.ensure(LEAD + 2)
            self.c.setFont(font, size)
            self.c.setFillColor(colour or Palette.TEXT_SECONDARY)
            self.c.drawString(MARGIN + indent, self.y, line)
            self.y -= LEAD
        self.y -= 3
        self.min_font = min(self.min_font, size)

    def bullets(self, items, indent=10):
        for item in items or []:
            self.para("- " + str(item), indent=indent)

    def numbered(self, items, indent=10):
        for i, item in enumerate(items or [], 1):
            self.para(f"{i}. {item}", indent=indent)

    # ------------------------------------------------------------- evidence
    def figure(self, spec, intent_id):
        self.ensure(FIG_H + 10)
        y = self.y - FIG_H
        evidence = render_primitive(
            spec["primitive_id"], learner_params(spec["render_params"]), self.c,
            (MARGIN, y, PAGE_W - 2 * MARGIN, FIG_H)
        )
        if evidence["vector_ops"] < spec["minimum_vector_ops"]:
            fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
                 f"{spec['representation_id']}:{evidence['vector_ops']}")
        self.placements.append({
            "content_ref": spec["representation_id"],
            "page_intent_id": intent_id,
            "primitive": spec["primitive_id"],
            "page": self.page,
            "fragment_kind": "START",
            "x0": MARGIN, "y0": y, "x1": PAGE_W - MARGIN, "y1": y + FIG_H,
            "ink_bbox": evidence["ink_bbox"],
            "vector_ops": evidence["vector_ops"],
            "text_ops": evidence["text_ops"],
            "op_histogram": evidence["op_histogram"],
            "quantitative_grounding": spec["quantitative_grounding"],
        })
        self.page_refs[self.page].append(spec["representation_id"])
        self.y = y - 10
        return self.page

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

    def save(self):
        self.c.save()
        data = self.path.read_bytes()
        metrics = []
        for p in range(1, self.page + 1):
            refs = self.page_refs.get(p, [])
            violations = sum(
                1 for x in self.placements
                if x["page"] == p and x["ink_bbox"] and not (
                    x["x0"] - 14 <= x["ink_bbox"]["x0"] and x["ink_bbox"]["x1"] <= x["x1"] + 14
                    and x["y0"] - 14 <= x["ink_bbox"]["y0"] and x["ink_bbox"]["y1"] <= x["y1"] + 14)
            )
            metrics.append({"page": p, "semantic_content_refs": refs, "orphan_continuation": False,
                            "bounds_violations": violations,
                            "underfill_disposition": "ACCEPTABLE"})
        page_map = {
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
            "page_metrics": metrics,
            "realization_summary": {
                "figure_count": len(self.placements),
                "total_vector_ops": sum(p["vector_ops"] for p in self.placements),
                "total_text_ops": sum(p["text_ops"] for p in self.placements),
                "label_only_figure_count": sum(1 for p in self.placements if p["vector_ops"] <= 0),
                "source_grounded_figure_count": sum(
                    1 for p in self.placements if p["quantitative_grounding"] == "SOURCE_QUANTITIES"),
            },
            "minimum_font_pt": self.min_font,
            "page_map_digest": "",
        }
        page_map["page_map_digest"] = digest(page_map, "page_map_digest")
        return data, page_map


# ------------------------------------------------------------ Core1 product


def render_core_study_guide(core1_plan, bundle, out_path, title="Physics — Core Study Guide"):
    specs_by_cap = {}
    for spec in bundle["representations"]:
        specs_by_cap.setdefault(spec["capability_ref"], []).append(spec)

    w = ProductWriter(out_path, title, "CORE_STUDY_GUIDE")
    w.heading(title, size=17)
    w.para("This guide teaches every capability the source assessment requires. Each unit follows the "
           "same route: see the physical situation, realize the representation, understand the relation "
           "and the condition that makes it valid, then verify the result.")
    w.para("Appendix A gives practice, Appendix B gives full solutions, and Appendix C is a printable "
           "answer-free handout.")

    sections = ["MAIN_TEACHING"]
    for lesson in core1_plan["lessons"]:
        cap = lesson["capability_ref"]
        intent = w.open_intent("PI-" + cap, cap)
        w.heading(human(cap), size=12)
        if lesson["lesson_mode"] == "FULL_LEARNING":
            w.subheading("See")
            w.para(lesson["see_phenomenon_anchor"])
            w.para(lesson["see_phase"])
            if lesson["see_system_frame_sign"]:
                w.para(lesson["see_system_frame_sign"])
            for spec in specs_by_cap.get(cap, []):
                if spec["page_intent_phase"] == "SEE":
                    w.figure(spec, intent["page_intent_id"])
            w.subheading("Realize")
            w.para(lesson["realize_phase"])
            w.numbered(lesson["realize_reconstruction_steps"])
            for spec in specs_by_cap.get(cap, []):
                if spec["page_intent_phase"] == "REALIZE":
                    w.figure(spec, intent["page_intent_id"])
            w.subheading("Understand")
            w.para(lesson["understand_phase"])
            w.para(lesson["understand_relation_and_validity"])
            w.para(lesson["ordinary_language_explanation"])
            for spec in specs_by_cap.get(cap, []):
                if spec["page_intent_phase"] == "UNDERSTAND":
                    w.figure(spec, intent["page_intent_id"])
            worked = lesson["worked_example"]
            if worked:
                w.subheading("Worked example")
                w.para(worked["prompt"])
                w.numbered([f"{human(s['role'])}: {s['text']}" for s in worked["reasoning_steps"]])
            repair = lesson["misconception_repair"]
            if repair:
                w.subheading("A shortcut that stops working")
                w.para(repair["wrong_model"])
                w.para(repair["why_plausible"])
                w.para(repair["minimal_contrast"])
                w.numbered(repair["repair_steps"])
            w.subheading("Try it")
            for stage in ("guided_attempt", "faded_attempt", "independent_attempt"):
                attempt = lesson[stage]
                if attempt:
                    w.para(f"{human(attempt['support_stage'])}: {attempt['prompt']}")
        else:
            w.subheading("Activate and check")
            w.para(lesson["activation"])
            if lesson["independent_attempt"]:
                w.para(lesson["independent_attempt"]["prompt"])
            for spec in specs_by_cap.get(cap, []):
                w.figure(spec, intent["page_intent_id"])
        w.subheading("Check before you accept the answer")
        w.bullets([human(v) for v in lesson["verification_steps"]])
        w.para(lesson["transfer_bridge"])
        w.close_intent(intent)

    aps = core1_plan["appendices"]
    w.new_page()
    w.heading(aps["appendix_a"]["title"], size=14)
    sections.append("APPENDIX_A_CORE_PRACTICE")
    numbering = {}
    for n, item in enumerate(aps["appendix_a"]["items"], 1):
        numbering[item["item_id"]] = n
        w.subheading(f"Practice {n} — {human(item['support_stage'])} "
                     f"({human(item['primary_capability_ref'])})")
        w.para(item["prompt"])

    w.new_page()
    w.heading(aps["appendix_b"]["title"], size=14)
    sections.append("APPENDIX_B_CORE_SOLUTIONS")
    for sol in aps["appendix_b"]["solutions"]:
        w.subheading(f"Solution {numbering.get(sol['item_ref'], '?')} "
                     f"({human(sol['primary_capability_ref'])})")
        w.numbered([f"{human(s['role'])}: {s['text']}" for s in sol["reasoning_steps"]])
        w.bullets([human(v) for v in sol["verification_steps"]])
        w.para(sol["final_response"])
        w.para(sol["model_validity_note"])

    w.new_page()
    w.heading(aps["appendix_c"]["title"], size=14)
    sections.append("APPENDIX_C_PRINTABLE_HANDOUT")
    w.para("Answer-free reference. Print this page on its own.")
    for entry in aps["appendix_c"]["reference_entries"]:
        w.subheading(human(entry["capability_ref"]))
        w.bullets([entry["first_move"], entry["frame_sign_cue"],
                   entry["relation_or_decision_cue"], human(entry["verification_cue"])])

    data, page_map = w.save()
    return data, page_map, sections


# ------------------------------------------------------------ Core2 product


def render_transfer_book(core2_plan, out_path, title="Physics — Transfer & Solution Book"):
    w = ProductWriter(out_path, title, "TRANSFER_SOLUTION_BOOK")
    w.heading(title, size=17)
    w.para("Each page is an original transfer question. Use the hints in order only if you are stuck: "
           "the first tells you what to notice, the second names the model, the third gives only the "
           "first move. The full solution follows.")

    w.heading("First-step reference", size=13)
    for entry in core2_plan["first_step_reference"]:
        w.subheading(human(entry["problem_family_ref"]))
        w.para(entry["first_move"])

    for n, page in enumerate(core2_plan["transfer_pages"], 1):
        w.new_page()
        w.heading(f"Transfer question {n} — {human(page['core1_linkage']['primary_capability_ref'])}",
                  size=12)
        w.para(f"Scaffolding level: {human(page['guide_demand_badge'])}.")
        w.subheading("Question")
        w.para(page["stem"])
        for option in page["options"]:
            w.para(f"({option['label']}) {option['text']}", indent=12)
        w.subheading("Hints")
        for hint in page["hint_ladder"]:
            w.para(f"{hint['level'].split('_')[0]} — {hint['text']}", indent=8)
        w.subheading("Solution")
        for section in page["solution"]["sections"]:
            w.para(f"{human(section['section'])}: {section['text']}")
        w.bullets([human(v) for v in page["solution"]["verification_steps"]])
        w.para("This question practises the same skill taught in the study guide unit on "
               f"{human(page['core1_linkage']['primary_capability_ref']).lower()}.")

    data, page_map = w.save()
    return data, page_map, ["TRANSFER_QUESTIONS", "HINT_LADDERS", "FULL_SOLUTIONS"]


def audit_product(page_map, data, minimum_by_primitive, minimum_font_pt=5.5):
    if sha_bytes(data) != page_map["artifact_sha256"]:
        fail("EXACT_ARTIFACT_HASH_MISMATCH", page_map["physical_page_map_id"])
    if page_map["page_map_digest"] != digest(page_map, "page_map_digest"):
        fail("PHYSICAL_PAGE_CUSTODY_FAILURE", "page map digest")
    errors = reconciliation_errors(page_map, page_map["page_width_pt"], page_map["page_height_pt"],
                                   minimum_by_primitive, 14)
    if errors:
        fail("PHYSICAL_PAGE_CUSTODY_FAILURE", "; ".join(errors[:5]))
    if page_map["realization_summary"]["label_only_figure_count"]:
        fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", page_map["physical_page_map_id"])
    if page_map["minimum_font_pt"] < minimum_font_pt:
        fail("MIN_FONT_SIZE_FAILURE", str(page_map["minimum_font_pt"]))
    return True
