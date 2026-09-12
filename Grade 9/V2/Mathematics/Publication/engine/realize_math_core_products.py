#!/usr/bin/env python3
"""Realize the two Mathematics learner products from real M-chain JSON.

Inputs are the actual outputs of the M-A -> M-J chain:

    MathCore1StudyPlan          (M-H, Core1Authoring)
    MathCore2TransferPlan       (M-I, Core2Transfer)
    MathCoverageClosurePackage  (M-J, CoverageClosure)
    Math PCK candidate bundle   (M-G, InstructionalKnowledge)
    Math teaching primitives    (M-H, RepresentationSemantics)

Outputs, per product:

    <product>.pdf               exact artifact
    publication_structure.json  page intents and content custody
    physical_page_map.json      placement evidence read back from real draw calls
    publication_audit.json      machine checks
    publication_manifest.json   hash-bound package descriptor

Custody discipline is adopted from the MATH-V2-05/PR #161 publication lineage:
every MATERIAL content item must be placed exactly once, every placement is
recorded from the coordinates actually used to draw, and the manifest binds the
exact PDF sha256. Figures are realized through `math_primitive_adapter`, which
delegates to the shared visual primitives package and refuses to draw any
numeric literal the source item did not declare.

This renderer reports `PUBLICATION_ENGINEERING` only. Subject correctness,
pedagogy, assessment design and visual usability stay PENDING here and are
decided by M-L.
"""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdfcanvas

HERE = Path(__file__).resolve().parent
MATH = HERE.parents[1]
SHARED = MATH.parent / "Shared" / "MasterTemplates"
for path in (str(HERE), str(SHARED)):
    if path not in sys.path:
        sys.path.insert(0, path)

from math_primitive_adapter import (  # noqa: E402
    SUPPORTED_KINDS,
    derive_params,
    library_binding,
    render_primitive,
    suggest_height,
)
from primitives import (  # noqa: E402
    FONT_BOLD,
    FONT_NAME,
    FONT_OBLIQUE,
    Palette,
    draw_card_box,
    draw_pill_badge,
)

PAGE_W, PAGE_H = A4
MARGIN = 40
BANNER_H = 46
CONTENT_TOP = PAGE_H - MARGIN - BANNER_H - 14
CONTENT_BOTTOM = MARGIN + 22
CONTENT_W = PAGE_W - 2 * MARGIN

PRODUCTS = ("CORE1_STUDY_GUIDE", "CORE2_TRANSFER_BOOK")

FALSIFIERS = (
    "RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT",
    "TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
    "MATERIAL_CONTENT_NOT_PLACED",
    "PLACEMENT_OUT_OF_PAGE_BOUNDS",
    "ARTIFACT_HASH_NOT_BOUND",
    "SOURCE_QUESTION_SHAPE_DRIFT",
    "PROVISIONAL_PRODUCT_CLAIMED_RELEASE_LEGAL",
    "PUBLICATION_ENGINEERING_CLAIMED_AS_SUBJECT_PASS",
)

# Representation-path token -> canonical teaching primitive. Subject-wide, keyed
# on declared representation identities, never on a topic.
PATH_TO_PRIMITIVE = (
    ("SLOPE_TRIANGLE_VIEW", "SLOPE_TRIANGLE_VIEW"),
    ("SLOPE_RATIO", "SLOPE_TRIANGLE_VIEW"),
    ("UNIT_RATE", "SLOPE_TRIANGLE_VIEW"),
    ("COORDINATE_PLANE", "COORDINATE_PLANE"),
    ("ORDERED_PAIR", "COORDINATE_PLANE"),
    ("CARTESIAN_AXIS_CONSTRAINT", "COORDINATE_PLANE"),
    ("GEOMETRIC_DISTANCE_RELATION", "COORDINATE_PLANE"),
    ("UNORDERED_PAIR_MODEL", "COMBINATORIAL_SLOT_MODEL"),
    ("COMBINATORIAL_SLOT_MODEL", "COMBINATORIAL_SLOT_MODEL"),
    ("ANGLE_RELATION", "PARALLEL_MEET_CONTRAST"),
    ("SYSTEM_OF_LINEAR_EQUATIONS", "ALIGNED_TRANSFORMATION_STACK"),
    ("SYMBOLIC_LINEAR_EQUATION", "ALIGNED_TRANSFORMATION_STACK"),
    ("PARAMETER_CONDITION", "ALIGNED_TRANSFORMATION_STACK"),
    ("RATE_CONTEXT_MODEL", "SIDE_BY_SIDE_METHOD_VIEW"),
)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value, omit=None):
    value = copy.deepcopy(value)
    if omit and isinstance(value, dict):
        value.pop(omit, None)
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def fail(code, detail=""):
    raise ValueError(f"{code}:{detail}" if detail else code)


def ascii_safe(text):
    """ReportLab base-14 fonts are Latin-1; keep learner text renderable."""
    replacements = {
        "−": "-", "–": "-", "—": "-", "×": "x", "÷": "/",
        "≤": "<=", "≥": ">=", "≠": "!=", "°": " deg",
        "Δ": "delta ", "→": "->", "‘": "'", "’": "'",
        "“": '"', "”": '"', "²": "^2", "³": "^3",
        "√": "sqrt", "≈": "~=", "±": "+/-", "…": "...",
    }
    out = str(text)
    for bad, good in replacements.items():
        out = out.replace(bad, good)
    return out.encode("latin-1", "replace").decode("latin-1")


# ---------------------------------------------------------------------------
# Layout primitives
# ---------------------------------------------------------------------------
class ProductCanvas:
    """A paginating canvas that records the real coordinates of every block."""

    def __init__(self, path, product_role, title, subtitle):
        self.c = pdfcanvas.Canvas(str(path), pagesize=A4, invariant=1, pageCompression=0)
        self.c.setTitle(title)
        self.c.setAuthor("Grade 9 V2 Mathematics generation chain")
        self.c.setSubject(product_role)
        self.c.setCreator("realize_math_core_products")
        self.product_role = product_role
        self.title = title
        self.subtitle = subtitle
        self.page = 0
        self.page_intent_id = None
        self.y = 0
        self.placements = []
        self.page_intents = []

    def start_page(self, intent_id, heading, sub):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.page_intent_id = intent_id
        self.page_intents.append(
            {"page_intent_id": intent_id, "page_number": self.page, "title": ascii_safe(heading), "content_refs": []}
        )
        c = self.c
        c.setFillColor(Palette.MATH_DARK)
        c.rect(0, PAGE_H - MARGIN - BANNER_H, PAGE_W, BANNER_H, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont(FONT_BOLD, 14)
        c.drawString(MARGIN, PAGE_H - MARGIN - 20, ascii_safe(heading)[:78])
        c.setFont(FONT_NAME, 7.6)
        c.drawString(MARGIN, PAGE_H - MARGIN - 34, ascii_safe(sub)[:120])
        c.setFont(FONT_NAME, 7)
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN - 20, f"{self.product_role}  |  page {self.page}")
        c.setFillColor(Palette.TEXT_MUTED)
        c.setFont(FONT_OBLIQUE, 6.2)
        c.drawCentredString(PAGE_W / 2, MARGIN - 12, ascii_safe(self.subtitle)[:150])
        self.y = CONTENT_TOP

    def ensure(self, height, intent_id, heading, sub):
        if self.page == 0 or self.y - height < CONTENT_BOTTOM:
            self.start_page(intent_id, heading, sub)

    def record(self, content_ref, kind, x, y, w, h, extra=None):
        if x < 0 or y < 0 or x + w > PAGE_W or y + h > PAGE_H:
            fail("PLACEMENT_OUT_OF_PAGE_BOUNDS", content_ref)
        row = {
            "content_ref": content_ref,
            "page_intent_id": self.page_intent_id,
            "page": self.page,
            "primitive": kind,
            "x0": round(float(x), 2),
            "y0": round(float(y), 2),
            "x1": round(float(x + w), 2),
            "y1": round(float(y + h), 2),
            "fragment_kind": "START",
        }
        if extra:
            row.update(extra)
        self.placements.append(row)
        self.page_intents[-1]["content_refs"].append(content_ref)
        return row

    def wrap(self, text, font, size, width):
        words = ascii_safe(text).split()
        lines, cur = [], ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.c.stringWidth(trial, font, size) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines or [""]

    def text_block(self, content_ref, title, paragraphs, intent, heading, sub, badges=None, accent=None):
        body = []
        for para in paragraphs:
            body.extend(self.wrap(para, FONT_NAME, 8, CONTENT_W - 28))
        height = 34 + len(body) * 11 + (18 if badges else 0)
        self.ensure(height, intent, heading, sub)
        x, y = MARGIN, self.y - height
        draw_card_box(self.c, x, y, CONTENT_W, height, title=ascii_safe(title),
                      title_color=accent or Palette.MATH_DARK)
        ty = y + height - 30
        self.c.setFont(FONT_NAME, 8)
        self.c.setFillColor(Palette.TEXT_PRIMARY)
        for line in body:
            self.c.drawString(x + 14, ty, line)
            ty -= 11
        if badges:
            bx = x + 14
            for badge in badges[:6]:
                used = draw_pill_badge(self.c, bx, y + 12, ascii_safe(str(badge))[:34], Palette.MATH_LIGHT,
                                       Palette.MATH_DARK, font_size=6.4, height=13)
                bx += used + 6
        self.y = y - 10
        return self.record(content_ref, "TEXT_BLOCK", x, y, CONTENT_W, height)

    def figure(self, content_ref, kind, params, intent, heading, sub, height=None):
        height = height or suggest_height(kind, params)
        self.ensure(height, intent, heading, sub)
        x, y = MARGIN, self.y - height
        evidence = render_primitive(kind, params, self.c, (x, y, CONTENT_W, height))
        self.y = y - 10
        return self.record(
            content_ref, kind, x, y, CONTENT_W, height,
            extra={
                "figure": True,
                "data_grounding": evidence["data_grounding"],
                "vector_geometry": evidence["vector_geometry"],
                "library_binding": library_binding(kind),
            },
        )

    def save(self):
        if self.page:
            self.c.showPage()
        self.c.save()


# ---------------------------------------------------------------------------
# Content model
# ---------------------------------------------------------------------------
def primitive_for_path(representation_path, registry_names):
    for token, kind in PATH_TO_PRIMITIVE:
        if token in {str(x).upper() for x in representation_path}:
            if kind in registry_names or kind == "COMBINATORIAL_SLOT_MODEL":
                return kind
    return "ALIGNED_TRANSFORMATION_STACK"


def pck_pseudo_page(asset):
    """Declared-source view of a PCK asset, for the grounding gate."""
    strings = [asset["anchor"], asset["ordinary_language_bridge"], asset["worked_example_family"], asset["transfer_family"]]
    strings += list(asset["reconstruction_route"]) + list(asset["repair_route"]) + list(asset["verification_method"])
    strings += list(asset["applicability_conditions"]) + list(asset["known_limitations"])
    strings += list(asset["minimal_contrast"].values()) + list(asset["misconception_discriminator"].values())
    strings += list(asset["representation_path"]) + list(asset["fading_dimensions"])
    return {
        "source_stem": asset["anchor"],
        "source_givens": [{"text": s} for s in strings],
        "source_options": [],
        "source_units": [],
        "source_subparts": [],
        "solution_route": {"steps": list(asset["reconstruction_route"]), "final_answer": {}},
    }


def core1_spec(kind, asset, job):
    """Build a representation spec for a Core1 figure from PCK asset data."""
    contrast = asset["minimal_contrast"]
    discriminator = asset["misconception_discriminator"]
    payloads = {
        "COORDINATE_PLANE": {
            "points": list(asset["representation_path"]),
            "axes": ["x-axis", "y-axis"],
            "relations": [asset["worked_example_family"], asset["transfer_family"]],
        },
        "SLOPE_TRIANGLE_VIEW": {
            "point_a": "anchor point",
            "point_b": "second declared point",
            "delta_x": "change in input",
            "delta_y": "change in output",
            "ratio": asset["anchor"],
            "points": list(asset["representation_path"]),
            "axes": ["x-axis", "y-axis"],
            "relations": [asset["worked_example_family"]],
        },
        "COMBINATORIAL_SLOT_MODEL": {
            "slots": [
                {"label": step_label(i), "choices": ascii_safe(step)[:20], "note": ""}
                for i, step in enumerate(asset["reconstruction_route"][:4])
            ]
        },
        "PARALLEL_MEET_CONTRAST": {
            "angle_sum_cases": [contrast["shared_structure"], contrast["focal_distinction"]],
            "boundary": contrast["decisive_feature"],
            "outcomes": [discriminator["candidate_wrong_model"], discriminator["decisive_response"]],
        },
        "ALIGNED_TRANSFORMATION_STACK": {
            "states": list(asset["reconstruction_route"]),
            "operations": list(asset["representation_path"]),
            "invariant": asset["anchor"],
        },
        "SIDE_BY_SIDE_METHOD_VIEW": {
            "left_method": list(asset["reconstruction_route"])[:3],
            "right_method": list(asset["repair_route"])[:3],
            "comparison_invariant": asset["anchor"],
        },
        "CORRECT_WRONG_TRANSFORMATION_CONTRAST": {
            "correct_case": [contrast["shared_structure"], contrast["decisive_feature"]],
            "wrong_case": [discriminator["candidate_wrong_model"], contrast["focal_distinction"]],
            "discriminator": discriminator["probe"],
        },
        "EQUIVALENCE_BALANCE_VIEW": {
            "left_state": asset["reconstruction_route"][0],
            "operation": contrast["focal_distinction"],
            "right_state": asset["reconstruction_route"][-1],
            "invariant": asset["anchor"],
        },
    }
    payload = payloads.get(kind) or payloads["ALIGNED_TRANSFORMATION_STACK"]
    return {
        "source_semantic_data": {"payload": payload, "declared_claims": [asset["anchor"]]},
        "accessibility_text": f"{kind.replace('_', ' ').title()} for {asset['asset_id']}: {asset['anchor']}",
        "attention_target": job,
        "capability_ref": asset["capability_refs"][0],
    }


def step_label(index):
    return ["first", "second", "third", "fourth"][index] if index < 4 else f"step {index + 1}"


def verification_line(check):
    """Render a verification check as a learner instruction, not a raw record."""
    if isinstance(check, str):
        return check
    if isinstance(check, dict):
        target = check.get("mathematical_target") or check.get("check_type") or check.get("check_id") or ""
        condition = check.get("acceptance_condition") or check.get("obligation_ref") or ""
        text = f"{target}: {condition}" if target and condition else (condition or target)
        return text or json.dumps(check, sort_keys=True)
    return str(check)


SLOPE_CAPABILITY_TOKENS = ("SLOPE", "COLLINEAR", "RATE", "EXTRAPOLATION")


def core2_figure_kinds(page):
    """Decide which primitive realizes each representation spec on a page.

    Core2 sometimes selects the same primitive for two distinct representation
    requirements. Rather than drawing the identical figure twice, a repeated
    coordinate frame is promoted to the slope-triangle realization when the page
    declares a slope-shaped capability and enough declared numeric points exist;
    otherwise the repeat is merged into the first figure.
    """
    from math_primitive_adapter import declared_points  # local import keeps the seam single-entry

    slope_page = any(
        token in cap for cap in page["capability_refs"] for token in SLOPE_CAPABILITY_TOKENS
    )
    numeric_points = len(declared_points(page))
    seen = {}
    rows = []
    for spec in page["representation_plan"]["representations"]:
        kind = spec["primitive_id"].removeprefix("MATH-TP-").removesuffix("-v1")
        if kind not in SUPPORTED_KINDS:
            fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", spec["primitive_id"])
        key = (kind, canon((spec.get("source_semantic_data") or {}).get("payload")))
        if key in seen:
            if kind == "COORDINATE_PLANE" and slope_page and numeric_points >= 2:
                rows.append((spec, "SLOPE_TRIANGLE_VIEW", []))
                seen[("SLOPE_TRIANGLE_VIEW", key[1])] = len(rows) - 1
                continue
            rows[seen[key]][2].append(spec["representation_id"])
            continue
        seen[key] = len(rows)
        rows.append((spec, kind, []))
    return rows


# ---------------------------------------------------------------------------
# Core1 study guide
# ---------------------------------------------------------------------------
def render_core1(plan, assets_by_id, registry_names, out_path):
    provisional = plan["release_class"] != "PRODUCTION"
    subtitle = (
        "Candidate learner product. Publication engineering only; subject, pedagogy, assessment and visual review PENDING."
    )
    doc = ProductCanvas(out_path, "CORE1_STUDY_GUIDE", "Mathematics Core 1 Study Guide", subtitle)
    material = []

    doc.start_page("PAGE-C1-00", "Mathematics Core 1 Study Guide", "How to use this guide")
    doc.text_block(
        "C1-COVER",
        "What this guide is",
        [
            "This guide teaches every capability your assessment actually required. "
            "Each lesson names the capability, anchors the idea, rebuilds it step by step, "
            "contrasts it with the mistake it is most often confused with, and ends with verification.",
            f"Plan reference {plan['core1_study_plan_id']} covers "
            f"{len(plan['lessons'])} capabilities drawn from study model {plan['study_model_ref']}.",
            "Worked instances are newly authored from the problem family. They are never a copy of "
            "an assessment question; the original questions belong to the Core 2 transfer book.",
        ],
        "PAGE-C1-00",
        "Mathematics Core 1 Study Guide",
        "How to use this guide",
        badges=[f"release class: {plan['release_class']}", f"PCK expert review: {plan['pck_authority']['expert_review_state']}"],
    )
    material.append("C1-COVER")

    authority = plan["pck_authority"]
    doc.text_block(
        "C1-AUTHORITY",
        "Review state of the teaching knowledge behind this guide",
        [
            "The pedagogical content knowledge used here cleared the M-G promotion pipeline under "
            "AI-assisted reference review and repository scope authority.",
            f"Subject expert review: {authority['expert_review_state']}. "
            f"Pedagogy expert review: {authority['expert_review_state']}. "
            f"Release-legal: {'yes' if authority['release_legal'] else 'no'}.",
            "Until those reviews are completed by authorized human reviewers this document is a "
            "candidate for review, not a validated learner product.",
        ],
        "PAGE-C1-00",
        "Mathematics Core 1 Study Guide",
        "How to use this guide",
        accent=Palette.WARNING,
    )
    material.append("C1-AUTHORITY")

    for index, lesson in enumerate(sorted(plan["lessons"], key=lambda x: x["capability_ref"]), 1):
        intent = f"PAGE-C1-{index:02d}"
        heading = f"{index}. {lesson['learner_title']}"
        sub = f"{lesson['capability_ref']}  |  treatment {lesson['treatment']}"
        doc.start_page(intent, heading, sub)

        asset_ids = [a for a in lesson["pck_asset_refs"] if a in assets_by_id]
        asset = assets_by_id[asset_ids[0]] if asset_ids else None

        ref = f"C1-{lesson['lesson_id']}-ANCHOR"
        doc.text_block(
            ref,
            "Anchor idea",
            [asset["anchor"] if asset else "Activate and verify this capability before moving on.",
             asset["ordinary_language_bridge"] if asset else ""],
            intent, heading, sub,
            badges=lesson["instructional_sequence"][:6],
        )
        material.append(ref)

        if asset:
            kind = primitive_for_path(asset["representation_path"], registry_names)
            spec = core1_spec(kind, asset, "REPRESENT")
            params = derive_params(kind, spec, pck_pseudo_page(asset))
            ref = f"C1-{lesson['lesson_id']}-FIG1"
            doc.figure(ref, kind, params, intent, heading, sub)
            material.append(ref)

            ref = f"C1-{lesson['lesson_id']}-RECONSTRUCT"
            doc.text_block(
                ref,
                "Rebuild it step by step",
                [f"{i + 1}. {step}" for i, step in enumerate(asset["reconstruction_route"])],
                intent, heading, sub,
            )
            material.append(ref)

            spec = core1_spec("CORRECT_WRONG_TRANSFORMATION_CONTRAST", asset, "DISCRIMINATE_CASES")
            params = derive_params("CORRECT_WRONG_TRANSFORMATION_CONTRAST", spec, pck_pseudo_page(asset))
            ref = f"C1-{lesson['lesson_id']}-FIG2"
            doc.figure(ref, "CORRECT_WRONG_TRANSFORMATION_CONTRAST", params, intent, heading, sub)
            material.append(ref)

            ref = f"C1-{lesson['lesson_id']}-REPAIR"
            doc.text_block(
                ref,
                "If it goes wrong",
                [asset["misconception_discriminator"]["candidate_wrong_model"],
                 "Probe: " + asset["misconception_discriminator"]["probe"]]
                + [f"- {step}" for step in asset["repair_route"]],
                intent, heading, sub, accent=Palette.DANGER,
            )
            material.append(ref)

        ref = f"C1-{lesson['lesson_id']}-PRACTICE"
        practice = [
            f"{plan_row['instance_role']}: author a new instance of {plan_row['problem_family_ref']} "
            f"(source reuse is forbidden)."
            for plan_row in lesson["problem_authoring_plans"]
        ] or ["This capability is already secure; activate it and verify rather than reteaching it."]
        doc.text_block(ref, "Practice ladder", practice, intent, heading, sub)
        material.append(ref)

        ref = f"C1-{lesson['lesson_id']}-VERIFY"
        doc.text_block(
            ref,
            "Verify before you move on",
            [f"- {v}" for v in lesson["verification_requirements"]]
            + ([f"- {v}" for v in asset["verification_method"]] if asset else []),
            intent, heading, sub, accent=Palette.SUCCESS,
        )
        material.append(ref)

    doc.save()
    return doc, material, provisional


# ---------------------------------------------------------------------------
# Core2 transfer book
# ---------------------------------------------------------------------------
def render_core2(plan, registry_names, out_path):
    subtitle = (
        "Candidate learner product. Attempt each original question first; support stays hidden until you do."
    )
    doc = ProductCanvas(out_path, "CORE2_TRANSFER_BOOK", "Mathematics Core 2 Transfer Book", subtitle)
    material = []

    doc.start_page("PAGE-C2-00", "Mathematics Core 2 Transfer Book", "How to use this book")
    doc.text_block(
        "C2-COVER",
        "What this book is",
        [
            "Every question here is your original assessment question, reproduced exactly. "
            "Attempt it before reading anything below it.",
            "If you are stuck, use the hints in order. H1 tells you what to notice, H2 which method or "
            "representation to choose, H3 the first executable step. None of them is the answer.",
            f"Plan reference {plan['plan_id']} covers {plan['summary']['question_count']} questions "
            f"linked to Core 1 in mode {plan['core1_linkage_mode']}.",
        ],
        "PAGE-C2-00",
        "Mathematics Core 2 Transfer Book",
        "How to use this book",
        badges=[f"release class: {plan['release_class']}", f"release legal: {'yes' if plan['summary']['release_legal'] else 'no'}"],
    )
    material.append("C2-COVER")

    for page in plan["pages"]:
        qid = page["question_ref"]
        intent = f"PAGE-C2-{qid}"
        heading = f"{qid}. {page['problem_family_ref'].removeprefix('MATH-PF-').replace('-', ' ').title()}"
        badge = page["guide_demand_badge"]
        sub = f"{', '.join(page['capability_refs'])}  |  guide demand {badge['label']} (not a psychometric claim)"
        doc.start_page(intent, heading, sub)

        stem = [page["source_stem"]]
        stem += [f"{g['given_id']}: {g['text']}" for g in page.get("source_givens", [])]
        stem += [f"({chr(97 + i)}) {o['text']}" for i, o in enumerate(page.get("source_options", []))]
        for sub_part in page.get("source_subparts", []) or []:
            stem.append(sub_part.get("text", "") if isinstance(sub_part, dict) else str(sub_part))
        ref = f"C2-{qid}-QUESTION"
        doc.text_block(ref, "Original question - attempt this first", stem, intent, heading, sub)
        material.append(ref)

        ref = f"C2-{qid}-WORKSPACE"
        doc.text_block(
            ref, "Your working",
            [f"{field}" for field in page["workspace_spec"]["fields"]],
            intent, heading, sub,
        )
        material.append(ref)

        for spec, kind, merged in core2_figure_kinds(page):
            params = derive_params(kind, spec, page)
            ref = f"C2-{qid}-{spec['representation_id']}"
            row = doc.figure(ref, kind, params, intent, heading, sub)
            if merged:
                row["merged_representation_refs"] = sorted(merged)
            material.append(ref)

        hints = page["hint_ladder"]
        ref = f"C2-{qid}-HINTS"
        doc.text_block(
            ref, "Hints - use only if you are stuck",
            [f"H1 ({hints['H1']['job']}): {hints['H1']['text']}",
             f"H2 ({hints['H2']['job']}): {hints['H2']['text']}",
             f"H3 ({hints['H3']['job']}): {hints['H3']['text']}"],
            intent, heading, sub, accent=Palette.WARNING,
        )
        material.append(ref)

        route = page["solution_route"]
        ref = f"C2-{qid}-SOLUTION"
        body = [f"{i + 1}. {step}" for i, step in enumerate(route["steps"])]
        body += [f"Check: {verification_line(check)}" for check in route["verification_checks"]]
        safety = page["assessment_safety"]
        if safety["validity_state"] != "VALID":
            body.append(
                f"Item note: this question is {safety['validity_state'].replace('_', ' ').lower()}; "
                "a wrong answer here is not read as a weakness."
            )
        doc.text_block(ref, "Worked reasoning and verification", body, intent, heading, sub, accent=Palette.SUCCESS)
        material.append(ref)

        links = ", ".join(link["learner_title"] for link in page["core1_lesson_refs"])
        ref = f"C2-{qid}-LINK"
        doc.text_block(
            ref, "If this was hard, study these Core 1 lessons",
            [links or "No Core 1 lesson is linked to this question."],
            intent, heading, sub,
        )
        material.append(ref)

    doc.save()
    return doc, material


# ---------------------------------------------------------------------------
# Custody
# ---------------------------------------------------------------------------
def build_custody(doc, material, pdf_path, product_role, upstream):
    placed = [row["content_ref"] for row in doc.placements]
    missing = sorted(set(material) - set(placed))
    if missing:
        fail("MATERIAL_CONTENT_NOT_PLACED", ",".join(missing[:3]))
    duplicated = sorted({ref for ref in placed if placed.count(ref) > 1})
    if duplicated:
        fail("MATERIAL_CONTENT_NOT_PLACED", "duplicate:" + ",".join(duplicated[:3]))

    figures = [row for row in doc.placements if row.get("figure")]
    if not figures:
        fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", product_role)
    vector_figures = [row for row in figures if row.get("vector_geometry")]

    pdf_bytes = Path(pdf_path).read_bytes()
    artifact_sha = sha_bytes(pdf_bytes)
    if not pdf_bytes.startswith(b"%PDF-") or b"%%EOF" not in pdf_bytes[-2048:]:
        fail("ARTIFACT_HASH_NOT_BOUND", product_role)

    structure = {
        "structure_id": "MATH-CORE-STRUCTURE-" + digest({"role": product_role, "intents": doc.page_intents})[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "product_role": product_role,
        "upstream": upstream,
        "page_intents": doc.page_intents,
    }
    page_map = {
        "page_map_id": "MATH-CORE-PAGEMAP-" + digest({"role": product_role, "p": doc.placements})[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "product_role": product_role,
        "artifact_path": Path(pdf_path).name,
        "artifact_sha256": artifact_sha,
        "page_count": doc.page,
        "actual_placement_evidence": True,
        "figure_count": len(figures),
        "vector_figure_count": len(vector_figures),
        "content_placements": doc.placements,
    }
    checks = {
        "MATERIAL_CUSTODY": "PASS",
        "PLACEMENTS_IN_BOUNDS": "PASS",
        "ACTUAL_PLACEMENT_EVIDENCE": "PASS",
        "PDF_HEADER_TRAILER": "PASS",
        "ARTIFACT_HASH_BOUND": "PASS",
        "TEACHING_PRIMITIVES_REALIZED": "PASS",
        "M_CHAIN_INPUT_BOUND": "PASS" if upstream.get("core1_plan_digest") or upstream.get("core2_plan_digest") else "FAIL",
    }
    audit = {
        "audit_id": "MATH-CORE-AUDIT-" + digest({"role": product_role, "sha": artifact_sha})[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "product_role": product_role,
        "artifact_sha256": artifact_sha,
        "checks": checks,
        "publication_engineering": "PASS" if all(v == "PASS" for v in checks.values()) else "FAIL",
        "quality_states": {
            "PUBLICATION_ENGINEERING": "PASS" if all(v == "PASS" for v in checks.values()) else "FAIL",
            "SUBJECT_CORRECTNESS": "PENDING",
            "PEDAGOGICAL_DESIGN": "PENDING",
            "ASSESSMENT_DESIGN": "PENDING",
            "VISUAL_USABILITY": "PENDING",
            "MATURE_DESIGN_QUALITY": "PENDING",
            "REFERENCE_COMPARABILITY": "NOT_RUN",
        },
    }
    descriptor = {
        "artifact_sha256": artifact_sha,
        "publication_structure_sha256": digest(structure),
        "physical_page_map_sha256": digest(page_map),
        "publication_audit_sha256": digest(audit),
        "upstream_digest": digest(upstream),
    }
    manifest = {
        "manifest_id": "MATH-CORE-MANIFEST-" + digest(descriptor)[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "product_role": product_role,
        "artifact_path": Path(pdf_path).name,
        "release_legal": bool(upstream.get("release_legal")),
        "upstream": upstream,
        **descriptor,
        "package_digest": digest(descriptor),
        "quality_states": audit["quality_states"],
    }
    if manifest["release_legal"] and upstream.get("pck_expert_review_state") != "PASS":
        fail("PROVISIONAL_PRODUCT_CLAIMED_RELEASE_LEGAL", product_role)
    if manifest["quality_states"]["SUBJECT_CORRECTNESS"] == "PASS":
        fail("PUBLICATION_ENGINEERING_CLAIMED_AS_SUBJECT_PASS", product_role)
    return structure, page_map, audit, manifest


def realize(core1_plan, core2_plan, closure, candidate_assets, primitive_registry, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if core1_plan.get("subject") != "MATHEMATICS" or core2_plan.get("subject") != "MATHEMATICS":
        fail("RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT", "subject")
    if not core1_plan.get("lessons") or not core2_plan.get("pages"):
        fail("RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT", "empty plan")
    if core1_plan["plan_digest"] != digest(core1_plan, "plan_digest"):
        fail("RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT", "core1 digest")
    if core2_plan["plan_digest"] != digest(core2_plan, "plan_digest"):
        fail("RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT", "core2 digest")

    registry_names = {p["canonical_name"] for p in primitive_registry["primitives"]}
    unrealized = sorted(registry_names - set(SUPPORTED_KINDS))
    if unrealized:
        fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", ",".join(unrealized))
    assets_by_id = {a["asset_id"]: a for a in candidate_assets}

    authority = core1_plan["pck_authority"]
    upstream_common = {
        "core1_plan_ref": core1_plan["core1_study_plan_id"],
        "core1_plan_digest": core1_plan["plan_digest"],
        "core2_plan_ref": core2_plan["plan_id"],
        "core2_plan_digest": core2_plan["plan_digest"],
        "coverage_package_ref": closure["package_id"],
        "coverage_package_digest": closure["package_digest"],
        "teaching_primitive_registry_ref": primitive_registry["registry_id"],
        "core1_release_class": core1_plan["release_class"],
        "core2_release_class": core2_plan["release_class"],
        "pck_expert_review_state": authority["expert_review_state"],
        "release_legal": bool(authority["release_legal"] and core2_plan["summary"]["release_legal"]),
    }

    results = {}
    core1_pdf = out_dir / "core1_study_guide.pdf"
    doc, material, _ = render_core1(core1_plan, assets_by_id, registry_names, core1_pdf)
    results["CORE1_STUDY_GUIDE"] = (core1_pdf,) + build_custody(
        doc, material, core1_pdf, "CORE1_STUDY_GUIDE", dict(upstream_common)
    )

    core2_pdf = out_dir / "core2_transfer_book.pdf"
    doc, material = render_core2(core2_plan, registry_names, core2_pdf)
    results["CORE2_TRANSFER_BOOK"] = (core2_pdf,) + build_custody(
        doc, material, core2_pdf, "CORE2_TRANSFER_BOOK", dict(upstream_common)
    )

    artifacts = []
    for role in PRODUCTS:
        pdf_path, structure, page_map, audit, manifest = results[role]
        base = out_dir / role.lower()
        base.mkdir(parents=True, exist_ok=True)
        (base / "publication_structure.json").write_text(json.dumps(structure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (base / "physical_page_map.json").write_text(json.dumps(page_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (base / "publication_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (base / "publication_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        artifacts.append(
            {
                "artifact_role": role,
                "media_type": "application/pdf",
                "artifact_sha256": manifest["artifact_sha256"],
                "manifest_digest": digest(manifest),
            }
        )

    result = {
        "realization_id": "MATH-CORE-REALIZATION-" + digest({"a": artifacts, "u": upstream_common})[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "status": "READY",
        "upstream": upstream_common,
        "artifacts": sorted(artifacts, key=lambda x: x["artifact_role"]),
        "artifact_set_digest": digest(sorted(artifacts, key=lambda x: x["artifact_role"])),
        "publication_engineering": "PASS",
        "release_legal": upstream_common["release_legal"],
        "human_review_states": {
            "SUBJECT_CORRECTNESS": "PENDING",
            "PEDAGOGICAL_DESIGN": "PENDING",
            "ASSESSMENT_DESIGN": "PENDING",
            "VISUAL_USABILITY": "PENDING",
        },
    }
    (out_dir / "realization_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result, results


def main():
    ap = argparse.ArgumentParser(description="Render the Mathematics Core1/Core2 learner products from M-chain JSON.")
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--core2-plan", required=True)
    ap.add_argument("--coverage-closure", required=True)
    ap.add_argument("--pck-candidates", default=str(MATH / "InstructionalKnowledge" / "registry" / "math-pck-candidates.json"))
    ap.add_argument("--primitive-registry", default=str(MATH / "RepresentationSemantics" / "registry" / "math-teaching-primitive-registry.json"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sys.path.insert(0, str(MATH / "Core1Authoring" / "engine"))
    from author_math_core1 import load_candidate_bundle

    _, candidate_assets = load_candidate_bundle(args.pck_candidates)
    result, _ = realize(
        load(args.core1_plan), load(args.core2_plan), load(args.coverage_closure),
        candidate_assets, load(args.primitive_registry), args.out,
    )
    print(json.dumps({k: v for k, v in result.items() if k != "upstream"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
