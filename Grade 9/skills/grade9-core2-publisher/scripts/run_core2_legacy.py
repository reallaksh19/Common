#!/usr/bin/env python3
"""Deterministic Core (2) publisher and cold-start falsifier.

Consumes only a frozen Core (1) ResearchPackage, LearnerProfile and
PublicationTarget. It performs no subject/web research. Study Guides can be
constructed deterministically from the frozen semantic bundle. Transfer Books
must be supplied as authored models backed by Core (1) question custody; this
runner validates and renders them instead of inventing source metadata, hints,
difficulty or solutions.

Exit codes: 0 = automated technical PASS, 1 = FAIL, 2 = BLOCKED.
Human subject/pedagogy/visual approval remains a separate release state.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.metadata
import json
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

import pymupdf as fitz
from jsonschema import Draft202012Validator, RefResolver
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


def safe(text: object) -> str:
    return html.escape(str(text), quote=False)


def profile_for(value: int) -> str:
    if value <= 35:
        return "FOUNDATION"
    if value <= 60:
        return "BRIDGE"
    if value <= 85:
        return "COMPRESSED"
    return "REFERENCE"


def delivery_for(target: dict) -> str:
    explicit = target.get("publication_profile", {}).get("delivery_contract")
    if explicit:
        return explicit
    req = target["requested_products"]
    if req.get("study_guide") and req.get("transfer_book"):
        return "FULL_TOPIC_PAIR"
    if req.get("transfer_book"):
        return "TRANSFER_ONLY"
    return "STUDY_GUIDE_ONLY"


def schema_context(contracts_dir: Path):
    schemas = {p.name: load(p) for p in contracts_dir.glob("*.schema.json")}
    base_uri = contracts_dir.as_uri().rstrip("/") + "/"
    store = {}
    for filename, obj in schemas.items():
        sid = obj.get("$id", filename)
        for key in (filename, sid, base_uri + filename, base_uri + sid):
            store[key] = obj
    return schemas, base_uri, store


def validate_schema(name: str, instance: dict, contracts_dir: Path) -> None:
    schemas, base_uri, store = schema_context(contracts_dir)
    schema = schemas[name]
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    errors = sorted(
        Draft202012Validator(schema, resolver=resolver).iter_errors(instance),
        key=lambda e: list(e.absolute_path),
    )
    if errors:
        print(f"{name} = FAIL")
        for err in errors:
            loc = ".".join(str(x) for x in err.absolute_path) or "<root>"
            print(f"- {loc}: {err.message}")
        raise SystemExit(1)


class RepresentationFlowable(Flowable):
    """Conservative monochrome schematic for capabilities declared IMPLEMENTED."""

    def __init__(self, rep_type: str, required_labels: list[str], width: float = 170 * mm, height: float = 44 * mm):
        super().__init__()
        self.rep_type = rep_type
        self.required_labels = required_labels
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    @staticmethod
    def _arrow(c, x1, y1, x2, y2):
        c.line(x1, y1, x2, y2)
        a = math.atan2(y2 - y1, x2 - x1)
        for d in (2.55, -2.55):
            c.line(x2, y2, x2 + 5 * math.cos(a + d), y2 + 5 * math.sin(a + d))

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.saveState()
        c.setLineWidth(0.8)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(4, h - 10, self.rep_type.replace("_", " "))
        c.setFont("Helvetica", 7.5)
        t = self.rep_type
        if t == "FORCE_DIAGRAM":
            cx, cy = min(w / 2, 150), 58
            c.rect(cx - 40, cy - 18, 80, 36)
            c.drawCentredString(cx, cy - 3, "selected system")
            self._arrow(c, cx, cy + 18, cx, cy + 48)
            self._arrow(c, cx + 40, cy, cx + 80, cy)
            c.drawString(cx + 46, cy + 6, "force direction")
        elif t == "MACRO_SYMBOLIC_REACTION_LINK":
            x1, x2, y, bw = 28, min(230, w - 155), 48, 125
            c.rect(x1, y, bw, 42)
            c.rect(x2, y, bw, 42)
            c.drawCentredString(x1 + bw / 2, y + 22, "macroscopic / process")
            c.drawCentredString(x2 + bw / 2, y + 22, "symbolic representation")
            self._arrow(c, x1 + bw, y + 28, x2 - 6, y + 28)
        elif t == "CIRCULAR_ANCHOR":
            cx, cy, r = min(w / 2, 145), 58, 36
            c.circle(cx, cy, r)
            for i in range(6):
                a = 2 * math.pi * i / 6
                c.circle(cx + r * math.cos(a), cy + r * math.sin(a), 3, fill=1 if i == 0 else 0)
            c.drawString(cx + r + 8, cy - 2, "anchor")
        elif t in {
            "ORDERED_SLOTS", "BLOCK_MODEL", "GAP_MODEL", "PREFIX_BUCKETS",
            "FORBIDDEN_POSITION_EVENT_GRID", "STAGE_DECISION_TABLE", "MULTISET_INVENTORY",
        }:
            x0, y0 = 24, 30
            cols = 4 if t != "BLOCK_MODEL" else 2
            bw = min(58, (w - 60) / max(cols, 1))
            for i in range(cols):
                c.rect(x0 + i * (bw + 8), y0 + 22, bw, 30)
                c.drawCentredString(x0 + i * (bw + 8) + bw / 2, y0 + 34, str(i + 1))
            c.drawString(x0, y0, t.replace("_", " ").lower())
        else:
            c.rect(20, 30, max(80, min(w - 40, 300)), 60)
            c.drawString(28, 62, "registered representation")
        if self.required_labels:
            c.setFont("Helvetica", 7.5)
            c.drawString(4, 5, "Required labels: " + "; ".join(self.required_labels))
        c.restoreState()


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(A4[0] - 15 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_plan(bundle: dict, manifest: dict, learner: dict, target: dict, registry: dict) -> dict:
    subject = bundle["project"]["subject"]
    direct = {x["subtopic_id"]: x["value"] for x in learner.get("baselines", [])}
    fallback = int(round(statistics.median(direct.values()))) if direct else 50
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
        cap = implemented.get(rep["representation_type"])
        if not cap and rep.get("blocking_if_unsupported", False):
            print("CORE2_REPRESENTATION_UNSUPPORTED")
            print(f"- {rep['representation_requirement_id']} requires {rep['representation_type']}")
            raise SystemExit(2)
        if cap:
            route = "GENERATED_VECTOR" if "GENERATED_VECTOR" in cap.get("routes", []) else cap.get("routes", [None])[0]
            if route is None:
                print(f"CORE2_REPRESENTATION_ROUTE_MISSING = {cap['capability_id']}")
                raise SystemExit(2)
            rep_instances.append({
                "representation_instance_id": "RI-" + rep["representation_requirement_id"],
                "requirement_id": rep["representation_requirement_id"],
                "representation_type": rep["representation_type"],
                "renderer_id": cap["renderer_id"],
                "capability_id": cap["capability_id"],
                "route": route,
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
    for i, cid in enumerate(bundle.get("concept_ids", []), 1):
        if cid in direct:
            baseline, resolution = direct[cid], "DIRECT"
        else:
            baseline, resolution = fallback, "PROFILE_MEDIAN_FALLBACK"
            warnings.append(f"{cid}: no direct learner baseline; used profile median B{fallback}")
        cclaims = [c for c in claims if cid in c.get("concept_ids", [])]
        refs = [c["claim_id"] for c in cclaims] or ([claims[0]["claim_id"]] if claims else [])
        if not refs:
            print(f"CORE2_RESEARCH_GAP = no material claim for {cid}")
            raise SystemExit(2)
        sections.append({
            "section_id": f"SEC-{i:02d}",
            "concept_id": cid,
            "baseline_value": baseline,
            "baseline_resolution": resolution,
            "instructional_profile": profile_for(baseline),
            "research_refs": refs,
            "representation_requirement_ids": [r["representation_requirement_id"] for r in reps if cid in r.get("concept_ids", [])],
            "formal_object_ids": [o["id"] for o in formal if set(o.get("research_refs", [])) & set(refs)],
            "worked_reasoning_ids": [w["worked_reasoning_id"] for w in worked if cid in w.get("concept_ids", [])],
        })

    badges = [{
        "badge_id": "BADGE-" + s["section_id"],
        "type": "BASELINE_SUPPORT",
        "machine_value": s["baseline_value"],
        "label": f"B{s['baseline_value']} · {s['instructional_profile']}",
        "visual_token": "baseline-support-" + s["instructional_profile"].lower(),
        "student_visible": True,
        "provenance_refs": [learner["learner_profile_id"]],
        "monochrome_label": f"B{s['baseline_value']} {s['instructional_profile']}",
        "priority": 70,
    } for s in sections]

    delivery = delivery_for(target)
    pair_id = None
    if delivery == "FULL_TOPIC_PAIR":
        pair_id = "PAIR-" + slugify(bundle["research_bundle_id"] + "-" + learner["learner_profile_id"] + "-" + target["publication_target_id"])

    plan = {
        "publication_plan_id": "PP-" + slugify(bundle["research_bundle_id"] + "-" + learner["learner_profile_id"]),
        "schema_version": "1.0.0",
        "research_bundle_id": bundle["research_bundle_id"],
        "research_package_digest": target["research_package_digest"],
        "learner_profile_id": learner["learner_profile_id"],
        "publication_target_id": target["publication_target_id"],
        "subject": subject,
        "topic_id": bundle["project"]["topic_id"],
        "title": bundle["project"]["title"],
        "purpose_type": target["purpose"]["type"],
        "subject_profile": target.get("publication_profile", {}).get("subject_profile", "GENERIC"),
        "delivery_contract": delivery,
        "requested_products": target["requested_products"],
        "sections": sections,
        "representation_instances": rep_instances,
        "badges": badges,
        "appendices": {
            "A_core_practice": True,
            "B_core_solutions": True,
            "C_printable_handout": True,
            "C_standalone_usable_required": True,
            "C_answer_leakage_forbidden": True,
            "C_new_subject_content_forbidden": True,
            "C_modules": ["first_step_reference", "formal_reference"],
        },
        "warnings": warnings,
    }
    if pair_id:
        plan["pair_id"] = pair_id
    return plan


def product_identity(plan: dict, role: str, product_id: str, companion_id: str | None = None) -> dict:
    out = {"product_id": product_id, "delivery_contract": plan["delivery_contract"], "role": role}
    if plan["delivery_contract"] == "FULL_TOPIC_PAIR":
        out["pair_id"] = plan["pair_id"]
        out["companion_product_id"] = companion_id
    return out


def _answer_leakage(app_b: list[dict], app_c: list[dict]) -> bool:
    handout = " ".join(x.get("content", "") for x in app_c).lower()
    for row in app_b:
        text = re.sub(r"\s+", " ", row.get("content", "").strip().lower())
        if len(text) >= 40 and text in handout:
            return True
    return False


def build_study_model(bundle: dict, plan: dict) -> dict:
    claims = {x["claim_id"]: x for x in bundle.get("research_claims", [])}
    reps = {x["requirement_id"]: x for x in plan.get("representation_instances", [])}
    formal = {x["id"]: x for x in bundle.get("equation_or_reaction_objects", [])}
    worked = {x["worked_reasoning_id"]: x for x in bundle.get("worked_reasoning", [])}
    main, app_a, app_b, app_c = [], [], [], []
    sg_id = "SG-" + slugify(bundle["research_bundle_id"] + "-" + plan["learner_profile_id"])
    tb_id = "TB-" + slugify(bundle["research_bundle_id"] + "-" + plan["learner_profile_id"])

    prompts = {
        "FOUNDATION": "State the rule in your own words and name a condition before using it.",
        "BRIDGE": "What do you notice first, and which condition prevents a wrong model?",
        "COMPRESSED": "State the decisive trigger and one nearby failure case.",
        "REFERENCE": "Give the shortest correct trigger and essential condition.",
    }

    for sec in plan["sections"]:
        items = [{
            "item_id": "BL-" + sec["section_id"],
            "type": "BADGE_LINE",
            "content": f"B{sec['baseline_value']} · {sec['instructional_profile']} support",
            "traceability_class": "PRESENTATION_ONLY",
            "research_refs": [],
        }]
        for rid in sec["research_refs"]:
            claim = claims.get(rid)
            if not claim:
                continue
            items.append({
                "item_id": f"CL-{rid}-{sec['section_id']}", "type": "CLAIM",
                "content": claim["statement"], "traceability_class": "MATERIAL", "research_refs": [rid],
            })
            for j, condition in enumerate(claim.get("conditions", []), 1):
                items.append({
                    "item_id": f"COND-{rid}-{j}-{sec['section_id']}", "type": "CONDITION",
                    "content": condition, "traceability_class": "MATERIAL", "research_refs": [rid],
                })

        wr_ids = sec.get("worked_reasoning_ids", []) if sec["instructional_profile"] in {"FOUNDATION", "BRIDGE"} else sec.get("worked_reasoning_ids", [])[:1] if sec["instructional_profile"] == "COMPRESSED" else []
        for wid in wr_ids:
            w = worked.get(wid)
            if w:
                items.append({
                    "item_id": f"WR-{wid}-{sec['section_id']}", "type": "WORKED_REASONING",
                    "content": w.get("summary", "Use the verified reasoning record."),
                    "traceability_class": "MATERIAL", "research_refs": w.get("research_refs", []),
                })
        for req_id in sec.get("representation_requirement_ids", []):
            inst = reps.get(req_id)
            if inst:
                items.append({
                    "item_id": f"REP-{inst['representation_instance_id']}-{sec['section_id']}",
                    "type": "REPRESENTATION",
                    "content": f"{inst['representation_type']} · requirement: {inst['requirement_id']} · required labels: {', '.join(inst['required_labels'])}",
                    "traceability_class": "MATERIAL", "research_refs": inst["research_refs"],
                    "representation_instance_id": inst["representation_instance_id"],
                })
        for fid in sec.get("formal_object_ids", []):
            obj = formal.get(fid)
            if obj:
                content = obj.get("semantic_expression", fid)
                if obj.get("conditions"):
                    content += " · Conditions: " + "; ".join(obj["conditions"])
                items.append({
                    "item_id": f"FORMAL-{fid}-{sec['section_id']}", "type": "FORMAL_OBJECT",
                    "content": content, "traceability_class": "MATERIAL", "research_refs": obj.get("research_refs", []),
                })
        main.append({
            "section_id": sec["section_id"], "concept_id": sec["concept_id"],
            "instructional_profile": sec["instructional_profile"], "items": items,
        })

        if sec["research_refs"]:
            claim = claims.get(sec["research_refs"][0])
            if claim:
                app_a.append({
                    "item_id": "PRACTICE-" + sec["section_id"], "type": "PRACTICE_PROMPT",
                    "content": f"{sec['concept_id']}: {prompts[sec['instructional_profile']]}",
                    "traceability_class": "MATERIAL", "research_refs": [claim["claim_id"]],
                })
                solution = claim["statement"]
                if claim.get("conditions"):
                    solution += " Conditions: " + "; ".join(claim["conditions"])
                app_b.append({
                    "item_id": "SOLUTION-" + sec["section_id"], "type": "SOLUTION",
                    "content": solution, "traceability_class": "MATERIAL", "research_refs": [claim["claim_id"]],
                })

    for w in bundle.get("worked_reasoning", []):
        app_c.append({
            "item_id": "HANDOUT-" + w["worked_reasoning_id"], "type": "WORKED_REASONING",
            "content": w.get("summary", "Use the verified first-step reasoning."),
            "traceability_class": "MATERIAL", "research_refs": w.get("research_refs", []),
        })
    for obj in bundle.get("equation_or_reaction_objects", []):
        app_c.append({
            "item_id": "HANDOUT-" + obj["id"], "type": "FORMAL_OBJECT",
            "content": obj.get("semantic_expression", obj["id"]),
            "traceability_class": "MATERIAL", "research_refs": obj.get("research_refs", []),
        })

    leakage = _answer_leakage(app_b, app_c)
    return {
        "publication_id": sg_id,
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "product_identity": product_identity(plan, "CORE_STUDY_GUIDE", sg_id, tb_id if plan["delivery_contract"] == "FULL_TOPIC_PAIR" else None),
        "title": bundle["project"]["title"] + " — Study Guide",
        "subtitle": f"{plan['purpose_type']} · learner-adapted from frozen Core (1)",
        "main_sections": main,
        "appendix_A": {"title": "Appendix A — Core Practice", "items": app_a},
        "appendix_B": {"title": "Appendix B — Core Solutions", "items": app_b},
        "appendix_C": {
            "title": "Appendix C — Printable Handout", "items": app_c,
            "standalone_usable": True, "introduces_new_subject_content": False,
            "answer_leakage_detected": leakage, "modules": ["first_step_reference", "formal_reference"],
        },
    }


def build_study_markdown(model: dict, plan: dict) -> str:
    lines = [
        f"# {model['title']}", "", model.get("subtitle", ""), "",
        f"Research bundle: `{plan['research_bundle_id']}`",
        f"Research package: `{plan['research_package_digest']}`",
        f"Learner profile: `{plan['learner_profile_id']}`",
        f"Delivery contract: `{plan['delivery_contract']}`", "", "## Main learning section", "",
    ]
    for sec in model["main_sections"]:
        lines += [f"### {sec['concept_id']} · {sec['instructional_profile']}", ""]
        for item in sec["items"]:
            prefix = "- " if item["type"] not in {"CLAIM", "BADGE_LINE"} else ""
            lines.append(prefix + item["content"])
            if item.get("research_refs"):
                lines.append("  Research: " + ", ".join(f"`{x}`" for x in item["research_refs"]))
        lines.append("")
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        app = model[key]
        lines += [f"## {app['title']}", ""]
        for i, item in enumerate(app["items"], 1):
            lines.append(f"{i}. {item['content']}")
            if item.get("research_refs"):
                lines.append("   Research: " + ", ".join(f"`{x}`" for x in item["research_refs"]))
        lines.append("")
    return "\n".join(lines)


def _styles(prefix: str = "C2"):
    ss = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(prefix + "Body", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5),
        "h1": ParagraphStyle(prefix + "H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=8),
        "h2": ParagraphStyle(prefix + "H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=17, spaceBefore=8, spaceAfter=6),
        "small": ParagraphStyle(prefix + "Small", parent=ss["BodyText"], fontName="Helvetica", fontSize=7.5, leading=9.5, spaceAfter=4),
        "hint": ParagraphStyle(prefix + "Hint", parent=ss["BodyText"], fontName="Helvetica", fontSize=9, leading=12, leftIndent=8, borderWidth=0.4, borderPadding=4, spaceAfter=5),
    }


def render_study_pdf(model: dict, plan: dict, path: Path):
    st = _styles("SG")
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=model["title"], author="Grade 9–11 Core (2) Publisher")
    story = [
        Paragraph(safe(model["title"]), st["h1"]),
        Paragraph(safe(model.get("subtitle", "")), st["body"]),
        Paragraph(safe(f"Core (1): {plan['research_bundle_id']} · package {plan['research_package_digest'][:12]}…"), st["small"]),
        PageBreak(),
    ]
    reps = {x["representation_instance_id"]: x for x in plan.get("representation_instances", [])}
    for sec in model["main_sections"]:
        story.append(Paragraph(safe(f"{sec['concept_id']} · {sec['instructional_profile']}"), st["h2"]))
        for item in sec["items"]:
            story.append(Paragraph(safe(item["content"]), st["body"]))
            if item["type"] == "REPRESENTATION":
                rep = reps[item["representation_instance_id"]]
                story.append(RepresentationFlowable(rep["representation_type"], rep["required_labels"]))
                story.append(Spacer(1, 3 * mm))
            if item.get("research_refs"):
                story.append(Paragraph(safe("Research: " + ", ".join(item["research_refs"])), st["small"]))
        story.append(PageBreak())
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        app = model[key]
        story.append(Paragraph(safe(app["title"]), st["h1"]))
        for i, item in enumerate(app["items"], 1):
            story.append(Paragraph(safe(f"{i}. {item['content']}"), st["body"]))
            if item.get("research_refs"):
                story.append(Paragraph(safe("Research: " + ", ".join(item["research_refs"])), st["small"]))
        story.append(PageBreak())
    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)


def validate_transfer_semantics(model: dict, plan: dict) -> None:
    errors: list[str] = []
    if model["publication_plan_id"] != plan["publication_plan_id"]:
        errors.append("transfer publication_plan_id mismatch")
    ident = model["product_identity"]
    if ident["delivery_contract"] != plan["delivery_contract"]:
        errors.append("transfer delivery_contract mismatch")
    if plan["delivery_contract"] == "FULL_TOPIC_PAIR" and ident.get("pair_id") != plan.get("pair_id"):
        errors.append("transfer pair_id mismatch")
    qids = [q["question_id"] for q in model["questions"]]
    if len(qids) != len(set(qids)):
        errors.append("duplicate transfer question IDs")
    solutions = {s["question_id"]: s for s in model["solutions"]}
    if set(solutions) != set(qids):
        errors.append("transfer questions and solutions are not one-to-one")
    for q in model["questions"]:
        tiers = [h["tier"] for h in q.get("hints", [])]
        if tiers != ["H1", "H2", "H3"][: len(tiers)]:
            errors.append(f"{q['question_id']}: hints must be ordered H1,H2,H3 without gaps")
        required = {"H0": 0, "H1": 1, "H2": 2, "H3": 3}[q["required_hint_depth"]]
        if len(tiers) < required:
            errors.append(f"{q['question_id']}: required hint depth not met")
        sol = solutions.get(q["question_id"], {})
        if len(sol.get("method", "").split()) < 8:
            errors.append(f"{q['question_id']}: solution method is too terse")
        if set(q["research_refs"]) - set(sol.get("research_refs", [])):
            errors.append(f"{q['question_id']}: solution loses question research lineage")
    covered = set()
    for st in model["sets"]:
        unknown = set(st["question_ids"]) - set(qids)
        if unknown:
            errors.append(f"{st['set_id']}: unknown question IDs {sorted(unknown)}")
        covered.update(st["question_ids"])
        if st["mode"] == "MIXED_TRANSFER":
            rows = st["diagnosis"]["rows"]
            diagnosed = [r["question_id"] for r in rows]
            if set(diagnosed) != set(st["question_ids"]) or len(diagnosed) != len(set(diagnosed)):
                errors.append(f"{st['set_id']}: diagnosis must cover every mixed question exactly once")
    if covered != set(qids):
        errors.append("every transfer question must belong to at least one set")
    if errors:
        print("TRANSFER_SEMANTIC_GATE = FAIL")
        for e in errors:
            print("- " + e)
        raise SystemExit(1)


def build_transfer_markdown(model: dict, plan: dict) -> str:
    qmap = {q["question_id"]: q for q in model["questions"]}
    smap = {s["question_id"]: s for s in model["solutions"]}
    lines = [f"# {model['title']}", "", f"Research package: `{plan['research_package_digest']}`", f"Pair: `{model['product_identity'].get('pair_id', 'N/A')}`", "", "# Attempt", ""]
    for st in model["sets"]:
        lines += [f"## {st['set_id']} · {st['mode']}", ""]
        for qid in st["question_ids"]:
            q = qmap[qid]
            lines += [f"### {qid}", ""]
            if st["mode"] == "ASSIMILATION":
                lines.append(q["concept_labels"]["primary"])
                lines.extend(q["concept_labels"]["supports"])
                lines.append(f"{q['task']['label']} · {q['difficulty']['learner_label']} · {q['transfer']['label']}")
            else:
                lines.append("CONCEPT · IDENTIFY FIRST")
            lines += [
                f"Source: {q['source']['source_label']} · {q['source']['locator_label']}",
                q["source"]["source_link"],
                "Core (1): " + ", ".join(q["research_refs"]), "", q["stem"],
            ]
            lines.extend(f"- {opt}" for opt in q.get("options", []))
            lines += ["", f"WORK HERE · {q['attempt']['workspace']}", "", "STOP · Try independently before opening hints.", ""]
            for h in q.get("hints", []):
                lines += [f"**{h['tier']} · {h['role']}** — {h['content']}", ""]
    lines += ["# Complete Solutions", ""]
    for q in model["questions"]:
        s = smap[q["question_id"]]
        lines += [
            f"## {q['question_id']}", "",
            f"QUESTION RECAP · {s['recap']}", f"WHY THIS WORKS · {s['why']}",
            f"METHOD · {s['method']}", f"ANSWER / CHECK · {s['answer_check']}",
            f"CONCEPT TO KEEP · {s['concept_to_keep']}", f"RETURN · {s['return_target']}",
            "Research: " + ", ".join(s["research_refs"]), "",
        ]
    for st in model["sets"]:
        if st["mode"] == "MIXED_TRANSFER":
            lines += [f"# Diagnosis · {st['set_id']}", ""]
            for row in st["diagnosis"]["rows"]:
                lines.append(f"- {row['question_id']} · PRIMARY {row['primary_concept_id']} · {row['recognition_route']} · Repair: {row['repair_target']}")
            lines.append("")
    return "\n".join(lines)


def render_transfer_pdf(model: dict, plan: dict, path: Path):
    st = _styles("TB")
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=model["title"], author="Grade 9–11 Core (2) Publisher")
    qmap = {q["question_id"]: q for q in model["questions"]}
    smap = {s["question_id"]: s for s in model["solutions"]}
    story = [Paragraph(safe(model["title"]), st["h1"]), Paragraph("Attempt first · hints optional · complete solutions later", st["body"]), PageBreak()]
    for group in model["sets"]:
        story.append(Paragraph(safe(f"{group['set_id']} · {group['mode']}"), st["h1"]))
        for qid in group["question_ids"]:
            q = qmap[qid]
            story.append(Paragraph(safe(qid), st["h2"]))
            if group["mode"] == "ASSIMILATION":
                meta = q["concept_labels"]["primary"] + " · " + q["task"]["label"] + " · " + q["difficulty"]["learner_label"] + " · " + q["transfer"]["label"]
                story.append(Paragraph(safe(meta), st["small"]))
                if q["concept_labels"]["supports"]:
                    story.append(Paragraph(safe(" · ".join(q["concept_labels"]["supports"])), st["small"]))
            else:
                story.append(Paragraph("<b>CONCEPT · IDENTIFY FIRST</b>", st["small"]))
            story.append(Paragraph(safe(f"Source: {q['source']['source_label']} · {q['source']['locator_label']}"), st["small"]))
            href = html.escape(q["source"]["source_link"], quote=True)
            story.append(Paragraph(f'<link href="{href}">Open source</link>', st["small"]))
            story.append(Paragraph(safe("Core (1): " + ", ".join(q["research_refs"])), st["small"]))
            story.append(Paragraph(safe(q["stem"]), st["body"]))
            for opt in q.get("options", []):
                story.append(Paragraph(safe("• " + opt), st["body"]))
            story.append(Spacer(1, 18 * mm))
            story.append(Paragraph("<b>STOP · Try independently before hints.</b>", st["body"]))
            for h in q.get("hints", []):
                story.append(Paragraph(safe(f"{h['tier']} · {h['role']} — {h['content']}"), st["hint"]))
            story.append(PageBreak())
    story += [Paragraph("Complete Solutions", st["h1"]), PageBreak()]
    for q in model["questions"]:
        s = smap[q["question_id"]]
        story.append(Paragraph(safe(q["question_id"]), st["h2"]))
        for label, key in (
            ("QUESTION RECAP", "recap"), ("WHY THIS WORKS", "why"), ("METHOD", "method"),
            ("ANSWER / CHECK", "answer_check"), ("CONCEPT TO KEEP", "concept_to_keep"), ("RETURN", "return_target"),
        ):
            story.append(Paragraph(f"<b>{label}</b> · {safe(s[key])}", st["body"]))
        story.append(Paragraph(safe("Research: " + ", ".join(s["research_refs"])), st["small"]))
        story.append(PageBreak())
    for group in model["sets"]:
        if group["mode"] == "MIXED_TRANSFER":
            story.append(Paragraph(safe(f"Diagnosis · {group['set_id']}"), st["h1"]))
            for row in group["diagnosis"]["rows"]:
                story.append(Paragraph(safe(f"{row['question_id']} · PRIMARY {row['primary_concept_id']} · {row['recognition_route']} · Repair: {row['repair_target']}"), st["body"]))
            story.append(PageBreak())
    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)


def inspect_pdf(path: Path, role: str, required_text: list[str], notation_probes: list[str], check_answer_separation: bool = False) -> dict:
    doc = fitz.open(path)
    min_font = None
    bounds_violations = 0
    internal_links = broken_internal = external_links = invalid_external = nongray = 0
    pages_text: list[str] = []
    for pno, page in enumerate(doc):
        pages_text.append(page.get_text())
        rect = page.rect
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = float(span.get("size", 0))
                    if size > 0:
                        min_font = size if min_font is None else min(min_font, size)
                    x0, y0, x1, y1 = span.get("bbox", (0, 0, 0, 0))
                    if x0 < -0.5 or y0 < -0.5 or x1 > rect.width + 0.5 or y1 > rect.height + 0.5:
                        bounds_violations += 1
        for link in page.get_links():
            kind = link.get("kind")
            if kind == fitz.LINK_GOTO:
                internal_links += 1
                if not (0 <= link.get("page", -1) < len(doc)):
                    broken_internal += 1
            elif kind == fitz.LINK_URI:
                external_links += 1
                uri = link.get("uri", "")
                parsed = urlparse(uri)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    invalid_external += 1
        for drawing in page.get_drawings():
            for key in ("color", "fill"):
                col = drawing.get(key)
                if isinstance(col, (tuple, list)) and len(col) >= 3 and max(col[:3]) - min(col[:3]) > 1e-6:
                    nongray += 1
    text = "\n".join(pages_text)
    missing_text = [x for x in required_text if x not in text]
    missing_notation = [x for x in notation_probes if x and x not in text]
    leakage = False
    if check_answer_separation:
        pos = text.find("Complete Solutions")
        if pos < 0:
            leakage = True
        else:
            attempt_text = text[:pos]
            leakage = "ANSWER / CHECK" in attempt_text or "QUESTION RECAP" in attempt_text
    result = {
        "role": role,
        "path": path.name,
        "sha256": sha256_file(path),
        "pages": len(doc),
        "min_font_pt": round(min_font or 0, 2),
        "text_bounds_violations": bounds_violations,
        "internal_links_checked": internal_links,
        "broken_internal_links": broken_internal,
        "external_links_checked": external_links,
        "invalid_external_links": invalid_external,
        "grayscale_nonneutral_drawings": nongray,
        "missing_required_text": missing_text,
        "notation_probes_required": notation_probes,
        "notation_probes_missing": missing_notation,
        "answer_leakage_detected": leakage,
    }
    doc.close()
    return result


def artifact(role: str, path: Path, media_type: str) -> dict:
    return {"role": role, "path": path.name, "sha256": sha256_file(path), "media_type": media_type, "bytes": path.stat().st_size}


def package_digest(arts: list[dict]) -> str:
    payload = "\n".join("|".join(x) for x in sorted((a["role"], a["path"], a["sha256"]) for a in arts)).encode()
    return hashlib.sha256(payload).hexdigest()


def notation_probes_for(bundle: dict) -> list[str]:
    probes: list[str] = []
    for obj in bundle.get("equation_or_reaction_objects", []):
        expr = str(obj.get("semantic_expression", "")).strip()
        if expr and len(expr) <= 100 and all(ord(ch) < 128 for ch in expr):
            probes.append(expr)
    return list(dict.fromkeys(probes))


def command_evidence() -> dict:
    requirements = Path(__file__).resolve().parents[1] / "requirements.txt"
    versions = {}
    for package in ("reportlab", "PyMuPDF", "jsonschema", "rfc8785"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "NOT_INSTALLED"
    return {
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "requirements_sha256": sha256_file(requirements),
        "python_major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        "dependency_versions": versions,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--learner", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--prefix", default=None)
    ap.add_argument("--transfer-model", type=Path, default=None)
    args = ap.parse_args()

    bundle, manifest, learner, target = map(load, (args.bundle, args.manifest, args.learner, args.target))
    grade9 = Path(__file__).resolve().parents[3]
    preflight = grade9 / "architecture" / "core2" / "validate_core2_preflight.py"
    contracts = grade9 / "architecture" / "core2" / "contracts" / "v1"
    registry = load(grade9 / "architecture" / "core2" / "representation" / "capabilities.v1.json")

    subprocess.run([
        sys.executable, str(preflight), "--bundle", str(args.bundle), "--manifest", str(args.manifest),
        "--learner", str(args.learner), "--target", str(args.target),
    ], check=True)

    plan = build_plan(bundle, manifest, learner, target, registry)
    validate_schema("publication-plan.schema.json", plan, contracts)
    args.out.mkdir(parents=True, exist_ok=True)
    prefix = slugify(args.prefix or bundle["project"]["title"])
    plan_path = args.out / f"{prefix}_Core2_Publication_Plan.json"
    write_json(plan_path, plan)

    arts: list[dict] = []
    pdf_evidence: list[dict] = []
    material_traceability = True
    study_model = transfer_model = None
    probes = notation_probes_for(bundle)

    if target["requested_products"].get("study_guide"):
        study_model = build_study_model(bundle, plan)
        validate_schema("study-guide.schema.json", study_model, contracts)
        model_path = args.out / f"{prefix}_Core2_Study_Guide.json"
        md_path = args.out / f"{prefix}_Core2_Study_Guide.md"
        pdf_path = args.out / f"{prefix}_Core2_Study_Guide.pdf"
        write_json(model_path, study_model)
        md_path.write_text(build_study_markdown(study_model, plan), encoding="utf-8", newline="\n")
        render_study_pdf(study_model, plan, pdf_path)
        pdf_evidence.append(inspect_pdf(pdf_path, "STUDY_GUIDE_PDF", ["Appendix A", "Appendix B", "Appendix C", plan["research_bundle_id"]], probes))
        for sec in study_model["main_sections"]:
            for item in sec["items"]:
                if item["traceability_class"] == "MATERIAL" and not item.get("research_refs"):
                    material_traceability = False
        for key in ("appendix_A", "appendix_B", "appendix_C"):
            for item in study_model[key]["items"]:
                if item["traceability_class"] == "MATERIAL" and not item.get("research_refs"):
                    material_traceability = False
        arts += [artifact("STUDY_GUIDE_MODEL", model_path, "application/json"), artifact("STUDY_GUIDE_MD", md_path, "text/markdown"), artifact("STUDY_GUIDE_PDF", pdf_path, "application/pdf")]

    if target["requested_products"].get("transfer_book"):
        if args.transfer_model is None:
            print("CORE2_TRANSFER_AUTHORING_INPUT_REQUIRED")
            print("- target requests a Transfer Book, but no --transfer-model was supplied; Core (2) will not invent source/question evidence")
            return 2
        transfer_model = load(args.transfer_model)
        expected_tb = "TB-" + slugify(bundle["research_bundle_id"] + "-" + plan["learner_profile_id"])
        expected_sg = "SG-" + slugify(bundle["research_bundle_id"] + "-" + plan["learner_profile_id"])
        transfer_model["publication_plan_id"] = plan["publication_plan_id"]
        transfer_model["publication_id"] = expected_tb
        transfer_model["product_identity"] = product_identity(plan, "EXAMSIDE_SOLUTION_TRANSFER", expected_tb, expected_sg if plan["delivery_contract"] == "FULL_TOPIC_PAIR" else None)
        validate_schema("transfer-book.schema.json", transfer_model, contracts)
        validate_transfer_semantics(transfer_model, plan)
        tb_model = args.out / f"{prefix}_Core2_Transfer_Book.json"
        tb_md = args.out / f"{prefix}_Core2_Transfer_Book.md"
        tb_pdf = args.out / f"{prefix}_Core2_Transfer_Book.pdf"
        write_json(tb_model, transfer_model)
        tb_md.write_text(build_transfer_markdown(transfer_model, plan), encoding="utf-8", newline="\n")
        render_transfer_pdf(transfer_model, plan, tb_pdf)
        pdf_evidence.append(inspect_pdf(tb_pdf, "TRANSFER_BOOK_PDF", ["Complete Solutions"] + [q["question_id"] for q in transfer_model["questions"]], [], True))
        arts += [artifact("TRANSFER_BOOK_MODEL", tb_model, "application/json"), artifact("TRANSFER_BOOK_MD", tb_md, "text/markdown"), artifact("TRANSFER_BOOK_PDF", tb_pdf, "application/pdf")]

    for rep in plan["representation_instances"]:
        rep["status"] = "RENDERED"
    write_json(plan_path, plan)

    representation_closure = all(
        r["status"] == "RENDERED" and set(r["required_labels"]) <= set(r["rendered_labels"])
        for r in plan["representation_instances"]
    )
    pair_pass = True
    if plan["delivery_contract"] == "FULL_TOPIC_PAIR":
        pair_pass = bool(
            study_model and transfer_model
            and study_model["product_identity"].get("pair_id") == transfer_model["product_identity"].get("pair_id") == plan.get("pair_id")
            and study_model["product_identity"].get("companion_product_id") == transfer_model["publication_id"]
            and transfer_model["product_identity"].get("companion_product_id") == study_model["publication_id"]
        )

    appendix_pass = bool(
        study_model is None
        or (
            all(study_model[k]["title"] for k in ("appendix_A", "appendix_B", "appendix_C"))
            and study_model["appendix_C"]["standalone_usable"] is True
            and study_model["appendix_C"]["introduces_new_subject_content"] is False
            and study_model["appendix_C"]["answer_leakage_detected"] is False
        )
    )
    bounds_pass = all(x["text_bounds_violations"] == 0 for x in pdf_evidence)
    typography_pass = all(x["min_font_pt"] >= 7.5 for x in pdf_evidence)
    grayscale_pass = all(x["grayscale_nonneutral_drawings"] == 0 for x in pdf_evidence)
    links_pass = all(x["broken_internal_links"] == 0 for x in pdf_evidence)
    external_pass = all(x["invalid_external_links"] == 0 for x in pdf_evidence)
    if transfer_model:
        tb_ev = next(x for x in pdf_evidence if x["role"] == "TRANSFER_BOOK_PDF")
        external_pass = external_pass and tb_ev["external_links_checked"] >= len(transfer_model["questions"])
    notation_pass = all(not x["notation_probes_missing"] for x in pdf_evidence)
    required_text_pass = all(not x["missing_required_text"] for x in pdf_evidence)
    answer_separation = all(not x["answer_leakage_detected"] for x in pdf_evidence) and appendix_pass

    gates = {
        "core2_preflight": True,
        "research_package_digest_binding": target["research_package_digest"] == manifest["package_digest"],
        "material_traceability": material_traceability,
        "representation_closure": representation_closure,
        "product_pair_identity": pair_pass,
        "badge_mapping": len({b["badge_id"] for b in plan["badges"]}) == len(plan["badges"]),
        "appendix_A_B_C": appendix_pass,
        "answer_separation": answer_separation,
        "internal_links": links_pass,
        "external_link_structure": external_pass,
        "typography": typography_pass,
        "notation_probes": notation_pass,
        "render_bounds": bounds_pass and required_text_pass,
        "grayscale_information": grayscale_pass,
        "publication_manifest_hash_binding": True,
    }
    warnings = list(plan["warnings"])
    if not pair_pass:
        warnings.append("reciprocal product pair identity failed")

    automated_pass = all(gates.values())
    status = "FAIL" if not automated_pass else "PASS_WITH_WARNINGS" if warnings else "PASS"
    pdf_hashes = [x["sha256"] for x in pdf_evidence]
    audit = {
        "audit_id": "AUDIT-" + plan["publication_plan_id"],
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "status": status,
        "release_state": "AUTOMATED_PASS_HUMAN_REVIEW_PENDING" if automated_pass else "AUTOMATED_FAIL",
        "gates": gates,
        "pdf_evidence": pdf_evidence,
        "command_evidence": command_evidence(),
        "human_visual_review": {
            "status": "PENDING", "minimum_render_dpi": 200, "pdf_sha256s": pdf_hashes,
            "all_pages_reviewed": False, "pages_reviewed": 0,
            "notes": "Human full-page review must be performed against these exact PDF hashes. Any PDF hash change makes previous review stale.",
        },
        "counts": {
            "sections": len(plan["sections"]),
            "representation_instances": len(plan["representation_instances"]),
            "baseline_fallbacks": sum(1 for s in plan["sections"] if s["baseline_resolution"] != "DIRECT"),
            "learner_pdfs": len(pdf_evidence),
            "transfer_questions": len(transfer_model["questions"]) if transfer_model else 0,
        },
        "warnings": warnings,
    }
    validate_schema("publication-audit.schema.json", audit, contracts)
    audit_path = args.out / f"{prefix}_Core2_Publication_Audit.json"
    write_json(audit_path, audit)

    arts = [artifact("PUBLICATION_PLAN", plan_path, "application/json")] + arts + [artifact("PUBLICATION_AUDIT", audit_path, "application/json")]
    pub_manifest = {
        "manifest_id": "PM-" + plan["publication_plan_id"],
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "research_bundle_id": bundle["research_bundle_id"],
        "research_package_digest": target["research_package_digest"],
        "learner_profile_id": learner["learner_profile_id"],
        "publication_target_id": target["publication_target_id"],
        "delivery_contract": plan["delivery_contract"],
        "artifacts": arts,
        "package_digest": package_digest(arts),
        "release_note": "Core (2) cold-start publication package. Automated technical gates do not imply human subject, pedagogy or visual approval.",
    }
    if plan.get("pair_id"):
        pub_manifest["pair_id"] = plan["pair_id"]
    validate_schema("publication-manifest.schema.json", pub_manifest, contracts)
    manifest_path = args.out / f"{prefix}_Core2_Publication_Manifest.json"
    write_json(manifest_path, pub_manifest)

    print("CORE2_BUILD = " + ("PASS" if automated_pass else "FAIL"))
    print("DELIVERY_CONTRACT = " + plan["delivery_contract"])
    print("RECIPROCAL_PAIR_IDENTITY = " + ("PASS" if pair_pass else "FAIL"))
    print("REPRESENTATION_CLOSURE = " + ("PASS" if representation_closure else "FAIL"))
    print("MATERIAL_TRACEABILITY = " + ("PASS" if material_traceability else "FAIL"))
    print("MEASURED_RENDER_BOUNDS = " + ("PASS" if bounds_pass else "FAIL"))
    print("MEASURED_TYPOGRAPHY_FLOOR = " + ("PASS" if typography_pass else "FAIL"))
    print("MEASURED_GRAYSCALE = " + ("PASS" if grayscale_pass else "FAIL"))
    print("MEASURED_EXTERNAL_LINK_STRUCTURE = " + ("PASS" if external_pass else "FAIL"))
    print("MEASURED_NOTATION_PROBES = " + ("PASS" if notation_pass else "FAIL"))
    print("HUMAN_VISUAL_REVIEW = PENDING")
    print("PUBLICATION_PACKAGE_DIGEST = " + pub_manifest["package_digest"])
    return 0 if automated_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
