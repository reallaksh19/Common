#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BP = ROOT / "Grade 9" / "V2" / "Chemistry" / "LearningBlueprint"
sys.path.insert(0, str(BP / "engine"))

from compile_chemistry_engineering_closure import digest  # noqa: E402
from compile_chemistry_product_engineering_custody import compile_product_custody  # noqa: E402
from validate_pal_engineering_ready import validate_pal_engineering_ready  # noqa: E402
from validate_product_source_scope import validate_product_source_scope  # noqa: E402

AUTHORITY_REL = "golden/v7/core1a-study-note-redox-authority.json"
CCBOM_REL = "golden/v7/ccbom-redox.json"
TTU_REL = "golden/v5/core1a-hard-study-product.json"
SDU_REL = "golden/v6/sdu-hard-redox.json"
CONCEPT_TTU_REL = "golden/v6/concept-ttu-core1a-redox.json"
SELF_HELP_REL = "golden/v6/self-help-core1a-redox.json"
STUDY_POLICY_REL = "policies/v7-core1a-study-note-sufficiency-policy.json"
REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"
AUDIT_REL = "source_audits/redox/production-source-audit.v2.json"
REQUEST_REL = "product_authority/redox/core1a/engineering-request.v2.json"
MANIFEST_REL = "product_authority/redox/core1a/engineering-manifest.v2.json"
EXTENSION_REL = "product_authority/redox/core1a/grade-extension-authorization.v1.json"
SCOPE_REL = "product_authority/redox/core1a/product-source-scope.v2.json"

FONT = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"
INK = colors.HexColor("#20252B")
MUTED = colors.HexColor("#606A73")
LINE = colors.HexColor("#CBD2D8")
PANEL = colors.HexColor("#F4F6F7")
PANEL_2 = colors.HexColor("#EAEFF2")
ACCENT = colors.HexColor("#234E52")
ACCENT_LIGHT = colors.HexColor("#E8F1F1")
WARN = colors.HexColor("#6B3D2E")
WARN_BG = colors.HexColor("#F7ECE8")
PRACTICE_BG = colors.HexColor("#F3F1E8")
ANSWER_BG = colors.HexColor("#EEF2EC")


def jload(rel: str) -> dict:
    return json.loads((BP / rel).read_text(encoding="utf-8"))


def register_fonts() -> None:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if not regular.exists() or not bold.exists():
        raise RuntimeError("DejaVu Sans fonts are required for Chemistry notation")
    pdfmetrics.registerFont(TTFont(FONT, str(regular)))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(bold)))


def ptxt(value) -> str:
    return escape(str(value)).replace("\n", "<br/>")


def styles():
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=ss["Title"], fontName=FONT_BOLD, fontSize=21, leading=25, textColor=INK, alignment=TA_LEFT, spaceAfter=3.5*mm),
        "subtitle": ParagraphStyle("subtitle", parent=ss["BodyText"], fontName=FONT, fontSize=9.8, leading=13.2, textColor=MUTED, spaceAfter=3*mm),
        "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontName=FONT_BOLD, fontSize=14.5, leading=18, textColor=ACCENT, spaceBefore=3.2*mm, spaceAfter=1.8*mm, keepWithNext=True),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontName=FONT_BOLD, fontSize=10.3, leading=12.5, textColor=INK, spaceBefore=1*mm, spaceAfter=1*mm),
        "body": ParagraphStyle("body", parent=ss["BodyText"], fontName=FONT, fontSize=9.1, leading=12.3, textColor=INK, spaceAfter=1.1*mm),
        "small": ParagraphStyle("small", parent=ss["BodyText"], fontName=FONT, fontSize=7.25, leading=9.2, textColor=MUTED, spaceAfter=0.6*mm),
        "eq": ParagraphStyle("eq", parent=ss["BodyText"], fontName=FONT_BOLD, fontSize=12.8, leading=16, textColor=INK, alignment=TA_CENTER),
        "badge": ParagraphStyle("badge", parent=ss["BodyText"], fontName=FONT_BOLD, fontSize=7.0, leading=8.4, textColor=ACCENT),
    }


def bullets(items, st):
    return [Paragraph("• " + ptxt(item), st["body"]) for item in items]


def payload_flowables(payload, st):
    if isinstance(payload, str):
        return [Paragraph(ptxt(payload), st["body"])]
    if isinstance(payload, list):
        return bullets(payload, st)
    if isinstance(payload, dict):
        rows = []
        for key, value in payload.items():
            if isinstance(value, list):
                value = "; ".join(str(x) for x in value)
            rows.append([
                Paragraph("<b>" + ptxt(key.replace("_", " ").title()) + "</b>", st["body"]),
                Paragraph(ptxt(value), st["body"]),
            ])
        table = Table(rows, colWidths=[39*mm, 125*mm], hAlign="LEFT", repeatRows=0)
        table.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("GRID", (0,0), (-1,-1), 0.35, LINE),
            ("BACKGROUND", (0,0), (0,-1), PANEL_2),
            ("LEFTPADDING", (0,0), (-1,-1), 2.3*mm),
            ("RIGHTPADDING", (0,0), (-1,-1), 2.3*mm),
            ("TOPPADDING", (0,0), (-1,-1), 1.5*mm),
            ("BOTTOMPADDING", (0,0), (-1,-1), 1.5*mm),
        ]))
        return [table]
    return [Paragraph(ptxt(payload), st["body"])]


def box(title, content, st, bg=PANEL, border=LINE):
    if isinstance(content, Flowable):
        content = [content]
    title_p = Paragraph(ptxt(title), st["h2"])
    table = Table([[title_p], [content]], colWidths=[168*mm], hAlign="LEFT", splitByRow=True)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.7, border),
        ("LEFTPADDING", (0,0), (-1,-1), 4*mm),
        ("RIGHTPADDING", (0,0), (-1,-1), 4*mm),
        ("TOPPADDING", (0,0), (-1,-1), 2.1*mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2.1*mm),
    ]))
    return table


def equation_box(text, st):
    table = Table([[Paragraph(ptxt(text), st["eq"]) ]], colWidths=[168*mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PANEL),
        ("BOX", (0,0), (-1,-1), 0.7, LINE),
        ("TOPPADDING", (0,0), (-1,-1), 4*mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4*mm),
    ]))
    return table


def representation(payload, rtype, st):
    if not isinstance(payload, dict):
        return box("Representation", payload_flowables(payload, st), st, bg=ACCENT_LIGHT)
    rows = []
    for key, value in payload.items():
        if isinstance(value, list):
            value = " | ".join(str(x) for x in value)
        rows.append([
            Paragraph("<b>" + ptxt(key.replace("_", " ").title()) + "</b>", st["body"]),
            Paragraph(ptxt(value), st["body"]),
        ])
    label = {
        "OXIDATION_STATE_LANE": "Oxidation-state lane",
        "ELECTRON_LEDGER": "Electron ledger",
        "SELF_OTHER_AGENT_MAP": "Self-change to agent-role map",
        "SPECIES_IDENTITY_MAP": "Species identity map",
    }.get(rtype, "Representation")
    t = Table(rows, colWidths=[38*mm, 126*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), 0.45, LINE),
        ("BACKGROUND", (0,0), (0,-1), ACCENT_LIGHT),
        ("LEFTPADDING", (0,0), (-1,-1), 2.6*mm),
        ("RIGHTPADDING", (0,0), (-1,-1), 2.6*mm),
        ("TOPPADDING", (0,0), (-1,-1), 2.2*mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2.2*mm),
    ]))
    return box(label, [t], st, bg=colors.white, border=ACCENT)


def render_object(obj, st, realized, question_ids, source_labels):
    realized.add(obj["object_id"])
    if obj.get("question_id"):
        question_ids.append(obj["question_id"])
    if obj.get("learner_source_display"):
        source_labels.append(obj["learner_source_display"])

    cls = obj["object_class"]
    payload = obj["learner_payload"]
    if cls == "EQUATION":
        return [equation_box(str(payload), st), Spacer(1, 1.5*mm)]
    if cls == "REPRESENTATION":
        return [representation(payload, obj.get("representation_type"), st), Spacer(1, 1.5*mm)]
    if cls == "MISCONCEPTION_REPAIR" and isinstance(payload, dict):
        rows = [
            [Paragraph("<b>Common wrong move</b>", st["body"]), Paragraph(ptxt(payload.get("wrong_model", "")), st["body"])],
            [Paragraph("<b>Repair</b>", st["body"]), Paragraph(ptxt(payload.get("repair", "")), st["body"])],
        ]
        t = Table(rows, colWidths=[39*mm, 125*mm], hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), WARN_BG),
            ("BOX", (0,0), (-1,-1), 0.7, WARN),
            ("INNERGRID", (0,0), (-1,-1), 0.3, LINE),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 2.5*mm),
            ("RIGHTPADDING", (0,0), (-1,-1), 2.5*mm),
            ("TOPPADDING", (0,0), (-1,-1), 1.8*mm),
            ("BOTTOMPADDING", (0,0), (-1,-1), 1.8*mm),
        ]))
        return [t, Spacer(1, 1.5*mm)]
    if cls in {"GUIDED_PRACTICE", "INDEPENDENT_PRACTICE"}:
        content = payload_flowables(payload, st)
        if obj.get("learner_source_display"):
            content += [Spacer(1, 0.6*mm), Paragraph(ptxt(obj["learner_source_display"]), st["small"])]
        title = "Try it - " + str(obj.get("practice_level", "practice")).title()
        return [box(title, content, st, bg=PRACTICE_BG), Spacer(1, 1.6*mm)]
    if cls == "ANSWER":
        return [box("Answer check", payload_flowables(payload, st), st, bg=ANSWER_BG), Spacer(1, 1.6*mm)]
    if cls == "WORKED_EXAMPLE":
        return [box("Worked example", payload_flowables(payload, st), st, bg=ACCENT_LIGHT), Spacer(1, 1.5*mm)]
    if cls == "VERIFICATION":
        return [box("Verification", payload_flowables(payload, st), st, bg=ANSWER_BG), Spacer(1, 1.5*mm)]
    labels = {
        "MEANING": "Meaning",
        "RULE": "Rule",
        "REASONING_CHAIN": "How to reason",
    }
    return [box(labels.get(cls, cls.replace("_", " ").title()), payload_flowables(payload, st), st), Spacer(1, 1.4*mm)]


def render_ttu(ttu, st):
    initial = payload_flowables(ttu.get("initial_state", {}), st)
    intro = [Paragraph(ptxt(ttu.get("learner_action", "")), st["body"]), Spacer(1, 0.8*mm)] + initial
    hints = []
    for i, hint in enumerate(ttu.get("hint_ladder", []), 1):
        hints.append(Paragraph(f"<b>Hint {i}.</b> {ptxt(hint.get('hint_text', ''))}", st["body"]))
    completed = payload_flowables(ttu.get("canonical_complete_state", {}), st)
    return [
        Paragraph("Reconstruct the model", st["h2"]),
        box("Your reconstruction", intro, st, bg=colors.white, border=ACCENT),
        Spacer(1, 1.2*mm),
        box("Hints", hints, st, bg=ACCENT_LIGHT),
        Spacer(1, 1.2*mm),
        box("Check your reconstruction", completed, st, bg=ANSWER_BG),
        Spacer(1, 0.8*mm),
        Paragraph("Verification: " + ptxt(ttu.get("verification_rule", "")), st["body"]),
        Spacer(1, 1.8*mm),
    ]


def page_header_footer(canvas, doc, title):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(LINE)
    canvas.line(16*mm, h-10*mm, w-16*mm, h-10*mm)
    canvas.setFont(FONT_BOLD, 7.2)
    canvas.setFillColor(ACCENT)
    canvas.drawString(16*mm, h-7.2*mm, "Chemistry - Core1A - Redox")
    canvas.setFont(FONT, 6.8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(w-16*mm, h-7.2*mm, title[:58])
    canvas.line(16*mm, 9.5*mm, w-16*mm, 9.5*mm)
    canvas.setFont(FONT, 6.8)
    canvas.drawString(16*mm, 6.5*mm, "Blueprint-derived study notes")
    canvas.drawRightString(w-16*mm, 6.5*mm, str(doc.page))
    canvas.restoreState()


def assert_extension(extension, scope, audit):
    if extension["status"] != "AUTHORIZED":
        raise RuntimeError("Grade-extension authority is not AUTHORIZED")
    if extension["source_audit_ref"] != scope["source_audit_ref"]:
        raise RuntimeError("Grade-extension authority binds a different source audit")
    if set(extension["authorized_scope_tiers"]) != set(scope["authorized_scope_tiers"]):
        raise RuntimeError("Grade-extension authority does not match authorized source tiers")
    if set(extension["held_scope_tiers"]) != set(scope["held_scope_tiers"]):
        raise RuntimeError("Grade-extension authority does not match held source tiers")
    if extension["authorization_id"] not in scope["extension_authority_ref"]:
        raise RuntimeError("Product scope does not bind exact grade-extension authorization")
    if scope["source_audit_digest"] != digest(audit):
        raise RuntimeError("Product source-scope contract has stale production-audit digest")


def build(out_pdf: Path, out_manifest: Path):
    register_fonts()
    st = styles()
    authority = jload(AUTHORITY_REL)
    ccbom = jload(CCBOM_REL)
    ttu_doc = jload(TTU_REL)
    sdu = jload(SDU_REL)
    concept_ttu = jload(CONCEPT_TTU_REL)
    self_help = jload(SELF_HELP_REL)
    study_policy = jload(STUDY_POLICY_REL)
    registry = jload(REGISTRY_REL)
    audit = jload(AUDIT_REL)
    request = jload(REQUEST_REL)
    manifest = jload(MANIFEST_REL)
    extension = jload(EXTENSION_REL)
    scope = jload(SCOPE_REL)

    assert_extension(extension, scope, audit)
    scope_result = validate_product_source_scope(scope, audit, authority, registry)
    audit_payloads = {AUDIT_REL: audit}
    custody = compile_product_custody(
        request, manifest, ccbom, scope, authority,
        registry=registry, source_audit_payloads=audit_payloads,
    )
    pal = validate_pal_engineering_ready(
        request, manifest, ccbom, scope, authority, custody,
        registry=registry, source_audit_payloads=audit_payloads,
    )
    if custody["status"] != "ENGINEERING_CUSTODY_READY" or pal["status"] != "PASS":
        raise RuntimeError("Engineering custody/PAL did not authorize product rendering")

    ttu_map = {x["ttu_id"]: x for x in ttu_doc.get("reconstructable_ttus", [])}
    required_ttu_ids = authority["reconstructable_ttu_refs"]
    missing_ttu = [x for x in required_ttu_ids if x not in ttu_map]
    if missing_ttu:
        raise RuntimeError(f"Missing reconstructable TTU definitions: {missing_ttu}")

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_manifest.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(out_pdf), pagesize=A4,
        leftMargin=16*mm, rightMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm,
        title="Core1A Redox Study Notes", author="Current Chemistry Blueprint",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(
        id="page", frames=[frame],
        onPage=lambda c, d: page_header_footer(c, d, authority["subtopic_title"]),
    )])

    story = []
    realized = set()
    realized_ttus = []
    question_ids = []
    source_labels = []

    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Redox Reactions", st["title"]))
    story.append(Paragraph(ptxt(authority["subtopic_title"]), st["subtitle"]))
    badges = [
        "Core1A",
        "Difficulty: " + authority["difficulty_badge"],
        "Grade 9 competitive foundation",
        "Scope: " + ", ".join(scope["authorized_scope_tiers"]),
    ]
    badge_table = Table([[Paragraph(ptxt(x), st["badge"]) for x in badges]], colWidths=[42*mm]*4, hAlign="LEFT")
    badge_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT_LIGHT),
        ("BOX", (0,0), (-1,-1), 0.5, LINE),
        ("INNERGRID", (0,0), (-1,-1), 0.25, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 2*mm),
        ("RIGHTPADDING", (0,0), (-1,-1), 2*mm),
        ("TOPPADDING", (0,0), (-1,-1), 1.8*mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1.8*mm),
    ]))
    story += [badge_table, Spacer(1, 2.5*mm)]

    story.append(Paragraph("Study route", st["h1"]))
    route_rows = []
    for i, atom in enumerate(authority["learning_atoms"], 1):
        route_rows.append([
            Paragraph(f"<b>{i}</b>", st["body"]),
            Paragraph(ptxt(atom["learner_title"]), st["body"]),
        ])
    route = Table(route_rows, colWidths=[11*mm, 153*mm], hAlign="LEFT")
    route.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LINEBELOW", (0,0), (-1,-2), 0.3, LINE),
        ("BACKGROUND", (0,0), (0,-1), PANEL_2),
        ("LEFTPADDING", (0,0), (-1,-1), 2.4*mm),
        ("RIGHTPADDING", (0,0), (-1,-1), 2.4*mm),
        ("TOPPADDING", (0,0), (-1,-1), 1.7*mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1.7*mm),
    ]))
    story += [route, Spacer(1, 2.2*mm)]
    route_text = "Track identity, assign and compare oxidation state, infer the electron consequence, then attach the agent role."
    story.append(box("Reasoning sequence", [Paragraph(route_text, st["body"])], st, bg=ACCENT_LIGHT))
    story.append(Spacer(1, 2*mm))

    objects_by_atom = {a["atom_id"]: [] for a in authority["learning_atoms"]}
    for obj in authority["content_objects"]:
        objects_by_atom[obj["learning_atom_id"]].append(obj)
    order = {
        "MEANING": 1, "RULE": 2, "EQUATION": 3, "REPRESENTATION": 4,
        "REASONING_CHAIN": 5, "WORKED_EXAMPLE": 6, "MISCONCEPTION_REPAIR": 7,
        "VERIFICATION": 8, "GUIDED_PRACTICE": 9, "INDEPENDENT_PRACTICE": 9,
        "ANSWER": 10,
    }
    ttu_by_owner = {t["owner_id"]: t for t in ttu_map.values() if t["ttu_id"] in required_ttu_ids}
    owner_alias = {"LA-OS-TRACK": "LA-REDOX-STATE-CHANGE-002", "LA-AGENT-ROLE": "LA-REDOX-AGENT-003"}
    ttu_by_atom = {owner_alias.get(k, k): v for k, v in ttu_by_owner.items()}

    for idx, atom in enumerate(authority["learning_atoms"], 1):
        story.append(Paragraph(f"{idx}. {ptxt(atom['learner_title'])}", st["h1"]))
        atom_objs = sorted(objects_by_atom[atom["atom_id"]], key=lambda o: (order.get(o["object_class"], 50), o["object_id"]))
        answer_objs = [o for o in atom_objs if o["object_class"] == "ANSWER"]
        non_answers = [o for o in atom_objs if o["object_class"] != "ANSWER"]
        for obj in non_answers:
            story.extend(render_object(obj, st, realized, question_ids, source_labels))
        if atom["atom_id"] in ttu_by_atom:
            ttu = ttu_by_atom[atom["atom_id"]]
            realized_ttus.append(ttu["ttu_id"])
            story.extend(render_ttu(ttu, st))
        for obj in answer_objs:
            story.extend(render_object(obj, st, realized, question_ids, source_labels))
        story.append(Spacer(1, 1.5*mm))

    story.append(Paragraph("Final consistency checks", st["h1"]))
    checks = [
        concept_ttu["canonical_expert_state"]["verification"]["electron_balance"],
        concept_ttu["canonical_expert_state"]["verification"]["role_check"],
    ]
    story.append(box("Verify before you move on", bullets(checks, st), st, bg=ANSWER_BG))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph("Source note", st["h2"]))
    story.append(Paragraph(ptxt(authority["scope_statement"]), st["small"]))

    doc.build(story)

    required_ids = {o["object_id"] for o in authority["content_objects"]}
    if realized != required_ids:
        raise RuntimeError(f"Content realization mismatch missing={sorted(required_ids-realized)} extra={sorted(realized-required_ids)}")
    if set(realized_ttus) != set(required_ttu_ids):
        raise RuntimeError("Reconstructable TTU realization mismatch")

    build_manifest = {
        "schema_version": "2.0.0",
        "product": "CORE1A",
        "subtopic_id": authority["subtopic_id"],
        "authority_id": authority["authority_id"],
        "authority_digest": digest(authority),
        "ccbom_id": ccbom["ccbom_id"],
        "ccbom_digest": digest(ccbom),
        "sdu_digest": digest(sdu),
        "concept_ttu_id": concept_ttu["ttu_id"],
        "concept_ttu_digest": digest(concept_ttu),
        "self_help_closure_id": self_help["closure_id"],
        "self_help_digest": digest(self_help),
        "study_policy_id": study_policy["policy_id"],
        "study_policy_digest": digest(study_policy),
        "engineering_request_id": request["request_id"],
        "engineering_manifest_id": manifest["manifest_id"],
        "production_source_audit_id": audit["audit_id"],
        "production_source_audit_digest": digest(audit),
        "grade_extension_authorization_id": extension["authorization_id"],
        "grade_extension_authorization_digest": digest(extension),
        "source_scope_contract_id": scope["scope_contract_id"],
        "source_scope_digest": digest(scope),
        "scope_validation": scope_result,
        "engineering_custody": custody,
        "pal_validation": pal,
        "realized_content_object_ids": sorted(realized),
        "realized_ttu_ids": sorted(realized_ttus),
        "practice_question_ids": question_ids,
        "practice_source_labels": source_labels,
        "forbidden_internal_terms": authority["learner_surface_policy"]["forbidden_internal_terms"],
        "held_scope_tiers": scope["held_scope_tiers"],
        "held_detection_tokens": [x for guard in scope["held_transformation_guards"] for x in guard["detection_tokens"]],
        "pagination_mode": study_policy["pagination"]["mode"],
    }
    out_manifest.write_text(json.dumps(build_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "out/core1a_redox_blueprint_proof.pdf"))
    parser.add_argument("--manifest", default=str(HERE / "out/core1a_redox_blueprint_proof.manifest.json"))
    args = parser.parse_args()
    build(Path(args.out), Path(args.manifest))
    print(args.out)


if __name__ == "__main__":
    main()
