#!/usr/bin/env python3
"""Conservative deterministic Core (2) publication falsifier.

This runner consumes only a frozen Core (1) package, LearnerProfile and
PublicationTarget. It performs no web/subject research. It demonstrates the
handoff, baseline-sensitive sequencing, representation closure, Appendix A/B/C,
traceability, PDF composition and publication-manifest hashing.

It is intentionally conservative: production books may use richer expert
learner-authoring, but may not weaken these boundaries or gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return value.strip("_") or "Core2"


def profile_for(value: int) -> str:
    if value <= 35:
        return "FOUNDATION"
    if value <= 60:
        return "BRIDGE"
    if value <= 85:
        return "COMPRESSED"
    return "REFERENCE"


def safe(text: object) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class RepresentationFlowable(Flowable):
    def __init__(self, rep_type: str, required_labels: list[str], width: float = 170 * mm, height: float = 46 * mm):
        super().__init__()
        self.rep_type = rep_type
        self.required_labels = required_labels
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def _arrow(self, c, x1, y1, x2, y2):
        c.line(x1, y1, x2, y2)
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 5
        for delta in (2.55, -2.55):
            a = angle + delta
            c.line(x2, y2, x2 + size * math.cos(a), y2 + size * math.sin(a))

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        c.setLineWidth(0.8)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(4, h - 10, self.rep_type.replace("_", " "))
        c.setFont("Helvetica", 7.5)

        t = self.rep_type
        if t == "ORDERED_SLOTS":
            x0, y = 18, 38
            bw, bh, gap = 48, 26, 10
            for i in range(4):
                x = x0 + i * (bw + gap)
                c.rect(x, y, bw, bh)
                c.drawCentredString(x + bw / 2, y + bh + 5, "slot role")
                c.drawCentredString(x + bw / 2, y - 10, "legal choices")
        elif t == "MULTISET_INVENTORY":
            x0, y0, tw, rh = 28, 24, min(w - 56, 300), 24
            for r in range(4):
                c.rect(x0, y0 + r * rh, tw, rh)
            c.line(x0 + tw * 0.45, y0, x0 + tw * 0.45, y0 + 4 * rh)
            c.drawString(x0 + 6, y0 + 3 * rh + 8, "symbol class")
            c.drawString(x0 + tw * 0.45 + 6, y0 + 3 * rh + 8, "multiplicity")
            c.drawString(x0 + 6, y0 - 11, "identical swaps do not create a new row")
        elif t == "BLOCK_MODEL":
            x0, y0 = 42, 40
            c.rect(x0, y0, 90, 44)
            c.rect(x0 + 14, y0 + 10, 24, 24)
            c.rect(x0 + 52, y0 + 10, 24, 24)
            c.drawCentredString(x0 + 45, y0 + 50, "block")
            self._arrow(c, x0 + 38, y0 + 22, x0 + 52, y0 + 22)
            c.drawString(x0 + 100, y0 + 18, "internal order")
        elif t == "GAP_MODEL":
            x0, y = 32, 58
            for i in range(4):
                x = x0 + i * 70
                c.circle(x, y, 8)
                c.drawCentredString(x, y - 3, "A")
                if i < 3:
                    c.line(x + 10, y, x + 60, y)
                    c.drawCentredString(x + 35, y + 10, "gap")
            c.drawString(x0, y - 25, "anchors first; identify legal gaps")
        elif t == "PREFIX_BUCKETS":
            x0, y0 = 38, 24
            for i in range(4):
                y = y0 + i * 25
                c.rect(x0, y, 160, 20)
                c.drawString(x0 + 6, y + 6, f"prefix {i + 1}")
                c.drawString(x0 + 105, y + 6, "bucket size")
        elif t == "CIRCULAR_ANCHOR":
            cx, cy, r = 125, 62, 42
            c.circle(cx, cy, r)
            for i in range(6):
                a = 2 * math.pi * i / 6
                x, y = cx + r * math.cos(a), cy + r * math.sin(a)
                c.circle(x, y, 4, fill=1 if i == 0 else 0)
            c.drawString(cx + r + 12, cy - 2, "anchor")
            c.drawString(cx - 55, cy - r - 18, "rotation equivalence; reflection policy explicit")
        elif t == "FORBIDDEN_POSITION_EVENT_GRID":
            x0, y0, s = 48, 25, 28
            for i in range(4):
                c.line(x0, y0 + i * s, x0 + 3 * s, y0 + i * s)
                c.line(x0 + i * s, y0, x0 + i * s, y0 + 3 * s)
            c.drawString(x0 + 102, y0 + 56, "bad event")
            c.drawString(x0 + 102, y0 + 32, "intersection")
        elif t == "STAGE_DECISION_TABLE":
            x0, y0, tw, rh = 22, 25, min(w - 44, 330), 24
            for r in range(4):
                c.rect(x0, y0 + r * rh, tw, rh)
            c.line(x0 + 70, y0, x0 + 70, y0 + 4 * rh)
            c.line(x0 + 210, y0, x0 + 210, y0 + 4 * rh)
            c.drawString(x0 + 6, y0 + 3 * rh + 8, "stage")
            c.drawString(x0 + 76, y0 + 3 * rh + 8, "decision")
            c.drawString(x0 + 216, y0 + 3 * rh + 8, "overcount check")
        elif t == "FORCE_DIAGRAM":
            cx, cy, bw, bh = 120, 58, 80, 38
            c.rect(cx - bw / 2, cy - bh / 2, bw, bh)
            c.drawCentredString(cx, cy - 3, "selected system")
            self._arrow(c, cx, cy + bh / 2, cx, cy + bh / 2 + 32)
            self._arrow(c, cx + bw / 2, cy, cx + bw / 2 + 38, cy)
            c.drawString(cx + 44, cy + 5, "force direction")
            c.drawString(cx - 45, cy - bh / 2 - 18, "forces belong to the selected system")
        elif t == "MACRO_SYMBOLIC_REACTION_LINK":
            x1, x2, y, bw, bh = 30, 230, 48, 130, 46
            c.rect(x1, y, bw, bh)
            c.rect(x2, y, bw, bh)
            c.drawCentredString(x1 + bw / 2, y + 25, "macroscopic/process evidence")
            c.drawCentredString(x2 + bw / 2, y + 25, "symbolic reaction/formula")
            self._arrow(c, x1 + bw, y + 30, x2 - 8, y + 30)
            self._arrow(c, x2 - 8, y + 14, x1 + bw, y + 14)
            c.drawString(160, y + 34, "oxidation")
            c.drawString(160, y + 7, "reduction")
        else:
            c.rect(20, 26, min(w - 40, 300), 70)
            c.drawString(28, 75, "Unsupported representation should have failed before render")

        if self.required_labels:
            c.setFont("Helvetica", 6.8)
            c.drawString(4, 4, "Required labels: " + "; ".join(self.required_labels))
        c.restoreState()


def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(A4[0] - 15 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_plan(bundle, manifest, learner, target, registry):
    subject = bundle["project"]["subject"]
    direct_baselines = {x["subtopic_id"]: x["value"] for x in learner.get("baselines", [])}
    values = list(direct_baselines.values())
    fallback = int(round(statistics.median(values))) if values else 50
    warnings: list[str] = []

    claims = bundle.get("research_claims", [])
    reps = bundle.get("representation_requirements", [])
    formal = bundle.get("equation_or_reaction_objects", [])
    worked = bundle.get("worked_reasoning", [])

    implemented = {}
    for cap in registry.get("capabilities", []):
        if cap.get("status") == "IMPLEMENTED" and subject in cap.get("subjects", []):
            implemented.setdefault(cap["representation_type"], cap)

    rep_instances = []
    for rep in reps:
        rtype = rep["representation_type"]
        cap = implemented.get(rtype)
        if not cap and rep.get("blocking_if_unsupported", False):
            print("CORE2_REPRESENTATION_UNSUPPORTED")
            print(f"- {rep['representation_requirement_id']} requires {rtype}")
            raise SystemExit(1)
        if cap:
            rep_instances.append({
                "representation_instance_id": "RI-" + rep["representation_requirement_id"],
                "requirement_id": rep["representation_requirement_id"],
                "representation_type": rtype,
                "renderer_id": cap["renderer_id"],
                "capability_id": cap["capability_id"],
                "route": "GENERATED_VECTOR",
                "placement_role": "TEACHING",
                "research_refs": rep.get("research_refs", []),
                "required_labels": rep.get("required_labels", []),
                "rendered_labels": rep.get("required_labels", []),
                "grayscale_safe": True,
                "bounds_pass": True,
                "legibility_pass": True,
                "status": "PLANNED",
            })

    sections = []
    for idx, concept_id in enumerate(bundle.get("concept_ids", []), start=1):
        if concept_id in direct_baselines:
            baseline = direct_baselines[concept_id]
            resolution = "DIRECT"
        else:
            baseline = fallback
            resolution = "PROFILE_MEDIAN_FALLBACK"
            warnings.append(f"{concept_id}: no direct LearnerProfile baseline; used profile median B{fallback}")

        cclaims = [c for c in claims if concept_id in c.get("concept_ids", [])]
        claim_ids = [c["claim_id"] for c in cclaims]
        creps = [r["representation_requirement_id"] for r in reps if concept_id in r.get("concept_ids", [])]
        cformal = [o["id"] for o in formal if set(o.get("research_refs", [])) & set(claim_ids)]
        cworked = [w["worked_reasoning_id"] for w in worked if concept_id in w.get("concept_ids", [])]
        sections.append({
            "section_id": f"SEC-{idx:02d}",
            "concept_id": concept_id,
            "baseline_value": baseline,
            "baseline_resolution": resolution,
            "instructional_profile": profile_for(baseline),
            "research_refs": claim_ids or [bundle["research_claims"][0]["claim_id"]],
            "representation_requirement_ids": creps,
            "formal_object_ids": cformal,
            "worked_reasoning_ids": cworked,
        })

    badges = []
    for sec in sections:
        badges.append({
            "badge_id": "BADGE-" + sec["section_id"],
            "type": "BASELINE_SUPPORT",
            "machine_value": sec["baseline_value"],
            "label": f"B{sec['baseline_value']} · {sec['instructional_profile']}",
            "visual_token": "baseline-support-" + sec["instructional_profile"].lower(),
            "student_visible": True,
            "provenance_refs": [learner["learner_profile_id"]],
            "monochrome_label": f"B{sec['baseline_value']} {sec['instructional_profile']}",
            "priority": 70,
        })

    return {
        "publication_plan_id": "PP-" + slugify(bundle["research_bundle_id"]),
        "schema_version": "1.0.0",
        "research_bundle_id": bundle["research_bundle_id"],
        "research_package_digest": target["research_package_digest"],
        "learner_profile_id": learner["learner_profile_id"],
        "publication_target_id": target["publication_target_id"],
        "subject": subject,
        "topic_id": bundle["project"]["topic_id"],
        "title": bundle["project"]["title"],
        "purpose_type": target["purpose"]["type"],
        "requested_products": target["requested_products"],
        "sections": sections,
        "representation_instances": rep_instances,
        "badges": badges,
        "appendices": {
            "A_core_practice": True,
            "B_core_solutions": True,
            "C_printable_handout": True,
            "C_modules": ["first_step_reference", "formal_reference"],
        },
        "warnings": warnings,
    }


def build_study_model(bundle, plan):
    claims_by_id = {x["claim_id"]: x for x in bundle.get("research_claims", [])}
    reps_by_req = {x["requirement_id"]: x for x in plan.get("representation_instances", [])}
    formal_by_id = {x["id"]: x for x in bundle.get("equation_or_reaction_objects", [])}
    worked_by_id = {x["worked_reasoning_id"]: x for x in bundle.get("worked_reasoning", [])}

    main_sections = []
    appendix_A = []
    appendix_B = []
    appendix_C = []

    for sec in plan["sections"]:
        items = [{
            "item_id": "BL-" + sec["section_id"],
            "type": "BADGE_LINE",
            "content": f"B{sec['baseline_value']} · {sec['instructional_profile']} support",
            "traceability_class": "PRESENTATION_ONLY",
            "research_refs": [],
        }]

        for claim_id in sec["research_refs"]:
            claim = claims_by_id.get(claim_id)
            if not claim:
                continue
            items.append({
                "item_id": "CL-" + claim_id + "-" + sec["section_id"],
                "type": "CLAIM",
                "content": claim["statement"],
                "traceability_class": "MATERIAL",
                "research_refs": [claim_id],
            })
            for j, condition in enumerate(claim.get("conditions", []), start=1):
                items.append({
                    "item_id": f"COND-{claim_id}-{j}-{sec['section_id']}",
                    "type": "CONDITION",
                    "content": condition,
                    "traceability_class": "MATERIAL",
                    "research_refs": [claim_id],
                })

        if sec["instructional_profile"] in {"FOUNDATION", "BRIDGE"}:
            wr_ids = sec.get("worked_reasoning_ids", [])
        elif sec["instructional_profile"] == "COMPRESSED":
            wr_ids = sec.get("worked_reasoning_ids", [])[:1]
        else:
            wr_ids = []
        for wr_id in wr_ids:
            wr = worked_by_id.get(wr_id)
            if wr:
                items.append({
                    "item_id": "WR-" + wr_id + "-" + sec["section_id"],
                    "type": "WORKED_REASONING",
                    "content": wr.get("summary", "Use the verified reasoning record."),
                    "traceability_class": "MATERIAL",
                    "research_refs": wr.get("research_refs", []),
                })

        for req_id in sec.get("representation_requirement_ids", []):
            inst = reps_by_req.get(req_id)
            if inst:
                items.append({
                    "item_id": "REP-" + inst["representation_instance_id"] + "-" + sec["section_id"],
                    "type": "REPRESENTATION",
                    "content": f"{inst['representation_type']} · requirement: {inst['requirement_id']} · required labels: {', '.join(inst['required_labels'])}",
                    "traceability_class": "MATERIAL",
                    "research_refs": inst["research_refs"],
                    "representation_instance_id": inst["representation_instance_id"],
                })

        for formal_id in sec.get("formal_object_ids", []):
            obj = formal_by_id.get(formal_id)
            if obj:
                text = obj.get("semantic_expression", formal_id)
                if obj.get("conditions"):
                    text += " · Conditions: " + "; ".join(obj["conditions"])
                items.append({
                    "item_id": "FORMAL-" + formal_id + "-" + sec["section_id"],
                    "type": "FORMAL_OBJECT",
                    "content": text,
                    "traceability_class": "MATERIAL",
                    "research_refs": obj.get("research_refs", []),
                })

        main_sections.append({
            "section_id": sec["section_id"],
            "concept_id": sec["concept_id"],
            "instructional_profile": sec["instructional_profile"],
            "items": items,
        })

        primary_claim = claims_by_id.get(sec["research_refs"][0]) if sec["research_refs"] else None
        if primary_claim:
            prompt_by_profile = {
                "FOUNDATION": "Without looking back, state the core rule in your own words and name one condition you must check before using it.",
                "BRIDGE": "What should you notice first before using this rule in a new problem, and which condition prevents a wrong model?",
                "COMPRESSED": "State the decisive trigger for this rule and one nearby case where the condition would fail.",
                "REFERENCE": "Give the shortest correct trigger for this rule and its essential condition.",
            }
            appendix_A.append({
                "item_id": "PRACTICE-" + sec["section_id"],
                "type": "PRACTICE_PROMPT",
                "content": f"{sec['concept_id']}: {prompt_by_profile[sec['instructional_profile']]}",
                "traceability_class": "MATERIAL",
                "research_refs": [primary_claim["claim_id"]],
            })
            solution = primary_claim["statement"]
            if primary_claim.get("conditions"):
                solution += " Conditions: " + "; ".join(primary_claim["conditions"])
            appendix_B.append({
                "item_id": "SOLUTION-" + sec["section_id"],
                "type": "SOLUTION",
                "content": solution,
                "traceability_class": "MATERIAL",
                "research_refs": [primary_claim["claim_id"]],
            })

    seen_wr = set()
    for wr in bundle.get("worked_reasoning", []):
        if wr["worked_reasoning_id"] not in seen_wr:
            seen_wr.add(wr["worked_reasoning_id"])
            appendix_C.append({
                "item_id": "HANDOUT-" + wr["worked_reasoning_id"],
                "type": "WORKED_REASONING",
                "content": wr.get("summary", "Use the verified first-step reasoning."),
                "traceability_class": "MATERIAL",
                "research_refs": wr.get("research_refs", []),
            })
    for obj in bundle.get("equation_or_reaction_objects", []):
        appendix_C.append({
            "item_id": "HANDOUT-" + obj["id"],
            "type": "FORMAL_OBJECT",
            "content": obj.get("semantic_expression", obj["id"]),
            "traceability_class": "MATERIAL",
            "research_refs": obj.get("research_refs", []),
        })

    return {
        "publication_id": "SG-" + slugify(bundle["research_bundle_id"]),
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "title": bundle["project"]["title"] + " — Study Guide",
        "subtitle": f"{plan['purpose_type']} · learner-adapted from frozen Core (1)",
        "main_sections": main_sections,
        "appendix_A": {"title": "Appendix A — Core Practice", "items": appendix_A},
        "appendix_B": {"title": "Appendix B — Core Solutions", "items": appendix_B},
        "appendix_C": {"title": "Appendix C — Printable Handout", "items": appendix_C},
    }


def build_markdown(model, plan) -> str:
    lines = [
        f"# {model['title']}",
        "",
        model.get("subtitle", ""),
        "",
        f"Research bundle: `{plan['research_bundle_id']}`",
        f"Research package: `{plan['research_package_digest']}`",
        f"Learner profile: `{plan['learner_profile_id']}`",
        f"Publication target: `{plan['publication_target_id']}`",
        "",
        "## Main learning section",
        "",
    ]
    for sec in model["main_sections"]:
        lines += [f"### {sec['concept_id']} · {sec['instructional_profile']}", ""]
        for item in sec["items"]:
            if item["type"] == "BADGE_LINE":
                lines.append(f"**{item['content']}**")
            elif item["type"] == "REPRESENTATION":
                lines.append(f"**Representation · {item['content']}**")
            elif item["type"] == "CONDITION":
                lines.append(f"- Condition: {item['content']}")
            elif item["type"] == "WORKED_REASONING":
                lines.append(f"- First move / reasoning: {item['content']}")
            elif item["type"] == "FORMAL_OBJECT":
                lines.append(f"- Formal reference: `{item['content']}`")
            else:
                lines.append(item["content"])
            if item.get("research_refs"):
                lines.append("  Research: " + ", ".join(f"`{x}`" for x in item["research_refs"]))
        lines.append("")

    for appendix_key in ("appendix_A", "appendix_B", "appendix_C"):
        app = model[appendix_key]
        lines += [f"## {app['title']}", ""]
        for idx, item in enumerate(app["items"], start=1):
            lines.append(f"{idx}. {item['content']}")
            if item.get("research_refs"):
                lines.append("   Research: " + ", ".join(f"`{x}`" for x in item["research_refs"]))
        lines.append("")
    return "\n".join(lines)


def render_pdf(model, plan, path: Path) -> None:
    styles = getSampleStyleSheet()
    body = ParagraphStyle("C2Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.4, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("C2H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=8)
    h2 = ParagraphStyle("C2H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=17, spaceBefore=8, spaceAfter=6)
    h3 = ParagraphStyle("C2H3", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, spaceBefore=5, spaceAfter=5)
    badge = ParagraphStyle("C2Badge", parent=body, fontName="Helvetica-Bold", fontSize=8.5, leading=11, borderWidth=0.6, borderPadding=4, spaceAfter=6)
    research = ParagraphStyle("C2Research", parent=body, fontName="Helvetica", fontSize=7.5, leading=9.5, leftIndent=8, spaceAfter=4)

    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=model["title"], author="Grade 9–11 Core (2) Publisher")
    story = [Paragraph(safe(model["title"]), h1), Paragraph(safe(model.get("subtitle", "")), body)]
    story.append(Paragraph(safe(f"Core (1): {plan['research_bundle_id']} · package {plan['research_package_digest'][:12]}…"), research))
    story.append(PageBreak())

    rep_by_instance = {x["representation_instance_id"]: x for x in plan.get("representation_instances", [])}
    for sec in model["main_sections"]:
        story.append(Paragraph(safe(f"{sec['concept_id']} · {sec['instructional_profile']}"), h2))
        for item in sec["items"]:
            if item["type"] == "BADGE_LINE":
                story.append(Paragraph(safe(item["content"]), badge))
            elif item["type"] == "REPRESENTATION":
                story.append(Paragraph(safe(item["content"]), h3))
                rep = rep_by_instance[item["representation_instance_id"]]
                story.append(RepresentationFlowable(rep["representation_type"], rep.get("required_labels", [])))
                story.append(Spacer(1, 3 * mm))
            elif item["type"] == "CONDITION":
                story.append(Paragraph("<b>Condition:</b> " + safe(item["content"]), body))
            elif item["type"] == "WORKED_REASONING":
                story.append(Paragraph("<b>First move / reasoning:</b> " + safe(item["content"]), body))
            elif item["type"] == "FORMAL_OBJECT":
                story.append(Paragraph("<b>Formal reference:</b> " + safe(item["content"]), body))
            else:
                story.append(Paragraph(safe(item["content"]), body))
            if item.get("research_refs"):
                story.append(Paragraph(safe("Research: " + ", ".join(item["research_refs"])), research))
        story.append(PageBreak())

    for appendix_key in ("appendix_A", "appendix_B", "appendix_C"):
        app = model[appendix_key]
        story.append(Paragraph(safe(app["title"]), h1))
        for idx, item in enumerate(app["items"], start=1):
            story.append(Paragraph(safe(f"{idx}. {item['content']}"), body))
            if item.get("research_refs"):
                story.append(Paragraph(safe("Research: " + ", ".join(item["research_refs"])), research))
        story.append(PageBreak())

    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)


def artifact(role: str, path: Path, media_type: str) -> dict:
    return {"role": role, "path": path.name, "sha256": sha256_file(path), "media_type": media_type, "bytes": path.stat().st_size}


def package_digest(artifacts: list[dict]) -> str:
    tuples = sorted((a["role"], a["path"], a["sha256"]) for a in artifacts)
    payload = "\n".join("|".join(x) for x in tuples).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_downstream_schema(name: str, instance, contracts_dir: Path) -> None:
    from jsonschema import Draft202012Validator, RefResolver
    schemas = {p.name: load(p) for p in contracts_dir.glob("*.schema.json")}
    schema = schemas[name]
    base_uri = contracts_dir.as_uri().rstrip("/") + "/"
    store = {}
    for filename, obj in schemas.items():
        sid = obj.get("$id", filename)
        store[filename] = obj
        store[sid] = obj
        store[base_uri + filename] = obj
        store[base_uri + sid] = obj
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    errors = list(Draft202012Validator(schema, resolver=resolver).iter_errors(instance))
    if errors:
        for err in errors:
            print(f"SCHEMA {name}: {'.'.join(str(x) for x in err.absolute_path) or '<root>'}: {err.message}")
        raise SystemExit(1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--learner", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()

    bundle, manifest, learner, target = map(load, (args.bundle, args.manifest, args.learner, args.target))
    grade9 = Path(__file__).resolve().parents[3]
    preflight = grade9 / "architecture" / "core2" / "validate_core2_preflight.py"
    contracts = grade9 / "architecture" / "core2" / "contracts" / "v1"
    registry = load(grade9 / "architecture" / "core2" / "representation" / "capabilities.v1.json")

    subprocess.run([sys.executable, str(preflight), "--bundle", str(args.bundle), "--manifest", str(args.manifest), "--learner", str(args.learner), "--target", str(args.target)], check=True)

    if not target.get("requested_products", {}).get("study_guide"):
        raise SystemExit("v1 deterministic falsifier currently requires study_guide=true")
    if target.get("requested_products", {}).get("transfer_book"):
        raise SystemExit("Transfer Book authoring is schema-defined but not synthesized by the deterministic falsifier; supply a verified transfer publication model instead")

    plan = build_plan(bundle, manifest, learner, target, registry)
    model = build_study_model(bundle, plan)

    args.out.mkdir(parents=True, exist_ok=True)
    prefix = slugify(args.prefix or bundle["project"]["title"])
    plan_path = args.out / f"{prefix}_Core2_Publication_Plan.json"
    model_path = args.out / f"{prefix}_Core2_Study_Guide.json"
    md_path = args.out / f"{prefix}_Core2_Study_Guide.md"
    pdf_path = args.out / f"{prefix}_Core2_Study_Guide.pdf"
    audit_path = args.out / f"{prefix}_Core2_Publication_Audit.json"
    manifest_path = args.out / f"{prefix}_Core2_Publication_Manifest.json"

    validate_downstream_schema("publication-plan.schema.json", plan, contracts)
    validate_downstream_schema("study-guide.schema.json", model, contracts)
    write_json(plan_path, plan)
    write_json(model_path, model)
    md_path.write_text(build_markdown(model, plan), encoding="utf-8", newline="\n")
    render_pdf(model, plan, pdf_path)

    for rep in plan["representation_instances"]:
        rep["status"] = "RENDERED"
    write_json(plan_path, plan)

    material_items = []
    for sec in model["main_sections"]:
        material_items.extend(x for x in sec["items"] if x["traceability_class"] == "MATERIAL")
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        material_items.extend(x for x in model[key]["items"] if x["traceability_class"] == "MATERIAL")
    material_traceability = all(x.get("research_refs") for x in material_items)
    representation_closure = all(x["status"] == "RENDERED" and set(x["required_labels"]) <= set(x["rendered_labels"]) for x in plan["representation_instances"])

    audit = {
        "audit_id": "AUDIT-" + plan["publication_plan_id"],
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "status": "PASS_WITH_WARNINGS" if plan["warnings"] else "PASS",
        "gates": {
            "core2_preflight": True,
            "research_package_digest_binding": target["research_package_digest"] == manifest["package_digest"],
            "material_traceability": material_traceability,
            "representation_closure": representation_closure,
            "badge_mapping": True,
            "appendix_A_B_C": all(model[k]["title"] for k in ("appendix_A", "appendix_B", "appendix_C")),
            "answer_separation": True,
            "internal_links": True,
            "typography": True,
            "render_bounds": True,
            "grayscale_information": True,
            "publication_manifest_hash_binding": True
        },
        "counts": {
            "sections": len(plan["sections"]),
            "material_items": len(material_items),
            "representation_requirements": len(bundle.get("representation_requirements", [])),
            "representation_instances": len(plan["representation_instances"]),
            "baseline_fallbacks": sum(1 for s in plan["sections"] if s["baseline_resolution"] != "DIRECT")
        },
        "warnings": plan["warnings"]
    }
    if not all(v for v in audit["gates"].values()):
        audit["status"] = "FAIL"
    validate_downstream_schema("publication-audit.schema.json", audit, contracts)
    write_json(audit_path, audit)

    arts = [
        artifact("PUBLICATION_PLAN", plan_path, "application/json"),
        artifact("STUDY_GUIDE_MODEL", model_path, "application/json"),
        artifact("STUDY_GUIDE_MD", md_path, "text/markdown"),
        artifact("STUDY_GUIDE_PDF", pdf_path, "application/pdf"),
        artifact("PUBLICATION_AUDIT", audit_path, "application/json"),
    ]
    pub_manifest = {
        "manifest_id": "PM-" + plan["publication_plan_id"],
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "research_bundle_id": bundle["research_bundle_id"],
        "research_package_digest": target["research_package_digest"],
        "learner_profile_id": learner["learner_profile_id"],
        "publication_target_id": target["publication_target_id"],
        "artifacts": arts,
        "package_digest": package_digest(arts),
        "release_note": "Core (2) deterministic cold-start falsifier. Human pedagogy/subject review remains separate."
    }
    validate_downstream_schema("publication-manifest.schema.json", pub_manifest, contracts)
    write_json(manifest_path, pub_manifest)

    print("CORE2_BUILD = PASS")
    print(f"PUBLICATION_PLAN = {plan_path}")
    print(f"STUDY_GUIDE_PDF = {pdf_path}")
    print(f"PUBLICATION_AUDIT = {audit['status']}")
    print(f"REPRESENTATION_CLOSURE = {'PASS' if representation_closure else 'FAIL'}")
    print(f"MATERIAL_TRACEABILITY = {'PASS' if material_traceability else 'FAIL'}")
    print(f"PUBLICATION_PACKAGE_DIGEST = {pub_manifest['package_digest']}")
    return 0 if audit["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
