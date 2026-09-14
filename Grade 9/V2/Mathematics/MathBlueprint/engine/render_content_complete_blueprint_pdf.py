#!/usr/bin/env python3
"""Deterministic Mathematics PDF renderer for content-complete LearnerPageBlueprints.

This module is deliberately presentation-only. Every learner-visible semantic
string comes from the validated Blueprint. The renderer may choose typography,
spacing and box geometry; it may not author mathematics, explanations, examples,
hints, questions, answers or reconstruction targets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import load
from validate_content_complete_page_blueprint import validate_content_complete_blueprint, digest as blueprint_digest


def safe(text: object) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<=", "≤")
        .replace(">=", "≥")
        .replace("!=", "≠")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def styles():
    st = getSampleStyleSheet()
    return {
        "stage": ParagraphStyle("Stage", parent=st["Heading1"], fontSize=16, leading=20, textColor=colors.HexColor("#17324D"), spaceAfter=8),
        "purpose": ParagraphStyle("Purpose", parent=st["BodyText"], fontSize=8.5, leading=11, textColor=colors.HexColor("#4A5560"), spaceAfter=8),
        "heading": ParagraphStyle("Heading", parent=st["Heading2"], fontSize=11.5, leading=14, textColor=colors.HexColor("#17324D"), spaceBefore=4, spaceAfter=5),
        "body": ParagraphStyle("Body", parent=st["BodyText"], fontSize=9.2, leading=12.4, spaceAfter=4),
        "math": ParagraphStyle("Math", parent=st["BodyText"], fontName="Courier", fontSize=8.8, leading=12, leftIndent=8, spaceAfter=4),
        "hint": ParagraphStyle("Hint", parent=st["BodyText"], fontSize=8.7, leading=11.5, leftIndent=10, textColor=colors.HexColor("#445A6F"), spaceAfter=4),
        "answer": ParagraphStyle("Answer", parent=st["BodyText"], fontSize=9.0, leading=12, backColor=colors.HexColor("#F2F7F3"), borderColor=colors.HexColor("#A7C7AE"), borderWidth=0.5, borderPadding=5, spaceAfter=5),
        "source": ParagraphStyle("Source", parent=st["BodyText"], fontSize=7.8, leading=10, textColor=colors.HexColor("#5E6A72"), spaceAfter=4),
        "small": ParagraphStyle("Small", parent=st["BodyText"], fontSize=8.2, leading=10.5, spaceAfter=3),
    }


def render_node(node: dict, st: dict):
    kind = node["type"]
    text = safe(node["text"])
    if kind == "HEADING": return Paragraph(text, st["heading"])
    if kind == "MATH": return Paragraph(text, st["math"])
    if kind in {"HINT"}: return Paragraph(f"<b>Hint:</b> {text}", st["hint"])
    if kind in {"ANSWER"}: return Paragraph(f"<b>Answer / completion:</b> {text}", st["answer"])
    if kind in {"CHECK"}: return Paragraph(f"<b>Check:</b> {text}", st["small"])
    if kind in {"SOURCE"}: return Paragraph(f"<b>Source:</b> {text}", st["source"])
    if kind == "QUESTION": return Paragraph(f"<b>Try:</b> {text}", st["body"])
    if kind == "STEP": return Paragraph(f"• {text}", st["body"])
    if kind == "BULLET": return Paragraph(f"• {text}", st["body"])
    if kind == "LABEL": return Paragraph(f"<b>{text}</b>", st["small"])
    return Paragraph(text, st["body"])


def render_representation(rep: dict, st: dict):
    rows = [[Paragraph(f"<b>{safe(rep['kind'].replace('_',' ').title())}</b>", st["small"]), ""]]
    rows.append([Paragraph("Make visible", st["small"]), Paragraph("; ".join(safe(x) for x in rep["must_make_visible"]), st["small"])])
    rows.append([Paragraph("Do not imply", st["small"]), Paragraph("; ".join(safe(x) for x in rep["must_not_imply"]), st["small"])])
    t = Table(rows, colWidths=[38*mm, 125*mm])
    t.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#C7D0D8")),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EEF5FA")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("SPAN",(0,0),(-1,0)),
        ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    return t


def render_ttu(ttu: dict, st: dict):
    rows = [
        [Paragraph("<b>Reconstruct this technical object</b>", st["small"])],
        [Paragraph(safe(ttu["reconstruction_prompt"]), st["body"])],
        [Paragraph("<b>Given:</b> " + "; ".join(safe(x["semantic_role"]) for x in ttu["given_parts"]), st["small"])],
        [Paragraph("<b>You must rebuild:</b> " + "; ".join(safe(x["semantic_role"]) for x in ttu["missing_parts"]), st["small"])],
        [Paragraph("<b>Target:</b> " + "; ".join(safe(x) for x in ttu["target_relations"]), st["small"])],
        [Paragraph("<b>Check after attempting:</b> " + safe(ttu["completion_key"]["final_check"]), st["small"])],
    ]
    t = Table(rows, colWidths=[163*mm])
    t.setStyle(TableStyle([
        ("BOX",(0,0),(-1,-1),0.7,colors.HexColor("#8EA6B8")),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F0F6FA")),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    return t


def render_workspace(workspace: dict, st: dict):
    label = workspace["purpose"].replace("_", " ").title()
    rows = [[Paragraph(f"<b>{safe(label)} workspace</b>", st["small"])], [Spacer(1, 32*mm)]]
    t = Table(rows, colWidths=[163*mm], rowHeights=[8*mm, 36*mm])
    t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.HexColor("#AAB7C2")),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F7F9FA"))]))
    return t


def render(doc: dict, out_pdf: Path) -> dict:
    validation = validate_content_complete_blueprint(doc)
    st = styles()
    pdf = SimpleDocTemplate(str(out_pdf), pagesize=A4, leftMargin=17*mm, rightMargin=17*mm, topMargin=15*mm, bottomMargin=15*mm, title="Mathematics Blueprint Publication")
    story=[]; rendered=[]
    for pi,page in enumerate(doc["pages"]):
        story.append(Paragraph(f"{safe(page['stage'])} — {safe(page['page_kind'].replace('_',' ').title())}", st["stage"]))
        story.append(Paragraph(safe(page["page_purpose"]), st["purpose"]))
        for block in page["technical_blocks"]:
            for n in block["render_nodes"]: story.append(render_node(n,st))
            rendered.append(block["block_id"])
        for block in page["prose_blocks"]:
            for n in block["render_nodes"]: story.append(render_node(n,st))
            rendered.append(block["block_id"])
        for rep in page["representations"]:
            story.append(Spacer(1,4)); story.append(render_representation(rep,st)); story.append(Spacer(1,5)); rendered.append(rep["representation_id"])
        for ttu in page["reconstructable_ttus"]:
            story.append(Spacer(1,5)); story.append(render_ttu(ttu,st)); story.append(Spacer(1,5)); rendered.append(ttu["ttu_id"])
        for ws in page["workspace_blocks"]:
            story.append(render_workspace(ws,st)); story.append(Spacer(1,5)); rendered.append(ws["workspace_id"])
        if pi != len(doc["pages"])-1: story.append(PageBreak())
    pdf.build(story)
    data=out_pdf.read_bytes()
    expected=set(validation["render_object_ids"]); actual=set(rendered)
    if expected != actual:
        missing=sorted(expected-actual); extra=sorted(actual-expected)
        raise ValueError("MATH_BLUEPRINT_RENDER_COVERAGE_DRIFT:missing="+",".join(missing)+";extra="+",".join(extra))
    return {
        "status":"PASS",
        "blueprint_id":doc["blueprint_id"],
        "blueprint_sha256":blueprint_digest(doc),
        "rendered_object_count":len(rendered),
        "rendered_object_ids":rendered,
        "pdf_sha256":hashlib.sha256(data).hexdigest(),
        "pdf_size_bytes":len(data),
        "semantic_source":"LEARNER_PAGE_BLUEPRINT_ONLY",
    }


def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True); ap.add_argument("--out",required=True); ap.add_argument("--audit-out",required=True); args=ap.parse_args()
    doc=load(args.input); out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    audit=render(doc,out)
    Path(args.audit_out).write_text(json.dumps(audit,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2,ensure_ascii=False))


if __name__=="__main__":main()
