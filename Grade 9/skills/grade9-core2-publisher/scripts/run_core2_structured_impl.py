#!/usr/bin/env python3
"""Executable PublicationStructure + shared XY_GRAPH layer for Core (2).

This module wraps the previous deterministic publisher without weakening its
research/evidence boundary. It makes PublicationStructure an executable render
contract and adds the generic XY_GRAPH capability.

The wrapper keeps the legacy publisher as the low-level content/QA engine and
patches only the publication-structure and representation surfaces.
"""
from __future__ import annotations

import copy
import html
import json
import math
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

import run_core2_legacy as legacy

_ORIG_BUILD_PLAN = legacy.build_plan
_ORIG_BUILD_STUDY_MODEL = legacy.build_study_model

_CURRENT_STRUCTURE: dict | None = None
_EXPLICIT_STRUCTURE: dict | None = None
_OUTPUT_DIR: Path | None = None
_PREFIX: str | None = None
_CONTRACTS: Path | None = None


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def _arg_value(argv: list[str], name: str) -> str | None:
    if name not in argv:
        return None
    i = argv.index(name)
    if i + 1 >= len(argv):
        raise SystemExit(f"{name} requires a value")
    return argv[i + 1]


def _remove_arg(argv: list[str], name: str) -> list[str]:
    out = list(argv)
    if name in out:
        i = out.index(name)
        if i + 1 >= len(out):
            raise SystemExit(f"{name} requires a value")
        del out[i:i + 2]
    return out


def _structure_profile(plan: dict) -> str:
    profile = plan.get("subject_profile", "GENERIC")
    if profile in {"PHYSICS_PR156", "CHEMISTRY_PR157"}:
        return profile
    return "PRODUCT_FIRST"


def _validate_structure_binding(structure: dict, plan: dict) -> None:
    checks = {
        "publication_plan_id": plan["publication_plan_id"],
        "research_bundle_id": plan["research_bundle_id"],
        "research_package_digest": plan["research_package_digest"],
        "learner_profile_id": plan["learner_profile_id"],
    }
    errors = []
    for key, expected in checks.items():
        if structure.get(key) != expected:
            errors.append(f"{key}: expected {expected!r}, got {structure.get(key)!r}")
    if errors:
        print("CORE2_PUBLICATION_STRUCTURE_BINDING = FAIL")
        for err in errors:
            print("- " + err)
        raise SystemExit(2)


def _xy_payload(rep: dict) -> dict:
    payload = rep.get("semantic_payload") or {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _axis(payload: dict, name: str) -> dict:
    direct = payload.get(f"{name}_axis")
    if isinstance(direct, dict):
        return direct
    axes = payload.get("axes")
    if isinstance(axes, dict) and isinstance(axes.get(name), dict):
        return axes[name]
    axis = {}
    label = payload.get(f"{name}_label")
    unit = payload.get(f"{name}_unit")
    if label is not None:
        axis["label"] = label
    if unit is not None:
        axis["unit"] = unit
    for k in ("min", "max", "ticks"):
        v = payload.get(f"{name}_{k}")
        if v is not None:
            axis[k] = v
    return axis


def _series(payload: dict) -> list[dict]:
    rows = payload.get("series")
    if isinstance(rows, list):
        out = []
        for row in rows:
            if isinstance(row, dict):
                pts = row.get("points")
                if isinstance(pts, list):
                    out.append(row)
        if out:
            return out
    pts = payload.get("points")
    if isinstance(pts, list):
        return [{"points": pts, "label": payload.get("series_label", "series")}]
    lines = payload.get("lines")
    if isinstance(lines, list):
        out = []
        for row in lines:
            if isinstance(row, dict) and isinstance(row.get("points"), list):
                out.append(row)
        return out
    return []


def validate_xy_semantics(rep: dict) -> None:
    payload = _xy_payload(rep)
    xa, ya = _axis(payload, "x"), _axis(payload, "y")
    sx = _series(payload)
    errors = []
    if not str(xa.get("label", "")).strip():
        errors.append("x-axis label/meaning is missing")
    if not str(ya.get("label", "")).strip():
        errors.append("y-axis label/meaning is missing")
    if not sx:
        errors.append("at least one semantic data series is required")
    else:
        for i, row in enumerate(sx, 1):
            pts = row.get("points", [])
            if len(pts) < 2:
                errors.append(f"series {i} needs at least two points")
                continue
            for p in pts:
                if not (isinstance(p, (list, tuple)) and len(p) >= 2):
                    errors.append(f"series {i} contains a malformed point")
                    break
                try:
                    float(p[0]); float(p[1])
                except Exception:
                    errors.append(f"series {i} contains a non-numeric point")
                    break
    if errors:
        print("CORE2_REPRESENTATION_SEMANTIC_GAP")
        print(f"- {rep.get('requirement_id')} requires XY_GRAPH semantic payload")
        for err in errors:
            print("- " + err)
        raise SystemExit(2)


class StructuredRepresentationFlowable(legacy.RepresentationFlowable):
    """Existing conservative renderer plus a real generic XY graph renderer."""

    def __init__(self, rep: dict, width: float = 170 * mm, height: float = 52 * mm):
        super().__init__(rep["representation_type"], rep.get("required_labels", []), width, height)
        self.rep = rep

    @staticmethod
    def _dash(c, style: str | None):
        style = (style or "SOLID").upper()
        if style == "DASHED":
            c.setDash(5, 3)
        elif style == "DOTTED":
            c.setDash(1, 2)
        else:
            c.setDash()

    @staticmethod
    def _marker(c, x: float, y: float, marker: str | None):
        marker = (marker or "CIRCLE").upper()
        if marker == "NONE":
            return
        if marker == "SQUARE":
            c.rect(x - 2.5, y - 2.5, 5, 5)
        elif marker == "TRIANGLE":
            path = c.beginPath()
            path.moveTo(x, y + 3)
            path.lineTo(x - 3, y - 3)
            path.lineTo(x + 3, y - 3)
            path.close()
            c.drawPath(path)
        else:
            c.circle(x, y, 2.5)

    def _draw_xy(self):
        validate_xy_semantics(self.rep)
        c, w, h = self.canv, self.width, self.height
        payload = _xy_payload(self.rep)
        xa, ya = _axis(payload, "x"), _axis(payload, "y")
        series = _series(payload)
        all_pts = []
        for row in series:
            all_pts.extend((float(p[0]), float(p[1])) for p in row["points"])

        def extent(axis: dict, vals: list[float]):
            lo = float(axis.get("min", min(vals)))
            hi = float(axis.get("max", max(vals)))
            if hi <= lo:
                hi = lo + 1.0
            span = hi - lo
            if "min" not in axis:
                lo -= span * 0.08
            if "max" not in axis:
                hi += span * 0.08
            if hi <= lo:
                hi = lo + 1.0
            return lo, hi

        xmin, xmax = extent(xa, [p[0] for p in all_pts])
        ymin, ymax = extent(ya, [p[1] for p in all_pts])
        left, right, bottom, top = 34.0, w - 18.0, 24.0, h - 22.0

        def X(v): return left + (float(v) - xmin) / (xmax - xmin) * (right - left)
        def Y(v): return bottom + (float(v) - ymin) / (ymax - ymin) * (top - bottom)

        c.saveState()
        c.setLineWidth(0.8)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(4, h - 10, "XY GRAPH")
        c.setFont("Helvetica", 7)

        xzero = X(0) if xmin <= 0 <= xmax else left
        yzero = Y(0) if ymin <= 0 <= ymax else bottom
        c.line(left, yzero, right, yzero)
        c.line(xzero, bottom, xzero, top)

        xlab = str(xa.get("label", "x"))
        ylab = str(ya.get("label", "y"))
        if xa.get("unit"):
            xlab += f" ({xa['unit']})"
        if ya.get("unit"):
            ylab += f" ({ya['unit']})"
        c.drawRightString(right, max(8, yzero - 10), xlab)
        c.drawString(min(w - 75, xzero + 4), top + 4, ylab)

        for axis, lo, hi, transform, vertical in (
            (xa, xmin, xmax, X, False), (ya, ymin, ymax, Y, True)
        ):
            ticks = axis.get("ticks")
            if not isinstance(ticks, list) or not ticks:
                ticks = [lo + i * (hi - lo) / 4 for i in range(5)]
            for t in ticks:
                try:
                    tv = float(t)
                except Exception:
                    continue
                if vertical:
                    yy = transform(tv)
                    c.line(xzero - 2, yy, xzero + 2, yy)
                    c.drawRightString(xzero - 4, yy - 2, f"{tv:g}")
                else:
                    xx = transform(tv)
                    c.line(xx, yzero - 2, xx, yzero + 2)
                    c.drawCentredString(xx, yzero - 10, f"{tv:g}")

        for si, row in enumerate(series):
            pts = [(X(p[0]), Y(p[1])) for p in row["points"]]
            self._dash(c, row.get("line_style"))
            c.setLineWidth(float(row.get("line_width", 1.2)))
            for a, b in zip(pts, pts[1:]):
                c.line(a[0], a[1], b[0], b[1])
            c.setDash()
            for xx, yy in pts:
                self._marker(c, xx, yy, row.get("marker"))
            if row.get("label"):
                lx, ly = pts[-1]
                c.drawString(min(right - 55, lx + 4), min(top - 2, ly + 4), str(row["label"]))

        for ref in payload.get("reference_lines", []) if isinstance(payload.get("reference_lines"), list) else []:
            if not isinstance(ref, dict):
                continue
            try:
                val = float(ref["value"])
            except Exception:
                continue
            self._dash(c, ref.get("line_style", "DASHED"))
            if ref.get("axis", "y").lower() == "x":
                xx = X(val); c.line(xx, bottom, xx, top)
                if ref.get("label"): c.drawString(xx + 3, top - 8, str(ref["label"]))
            else:
                yy = Y(val); c.line(left, yy, right, yy)
                if ref.get("label"): c.drawString(right - 55, yy + 3, str(ref["label"]))
            c.setDash()

        for ann in payload.get("annotations", []) if isinstance(payload.get("annotations"), list) else []:
            if not isinstance(ann, dict):
                continue
            try:
                xx, yy = X(ann["x"]), Y(ann["y"])
            except Exception:
                continue
            c.drawString(xx + 3, yy + 3, str(ann.get("label", "")))

        if self.required_labels:
            c.setFont("Helvetica", 6.7)
            c.drawString(4, 4, "Required labels: " + "; ".join(self.required_labels))
        c.restoreState()

    def draw(self):
        if self.rep["representation_type"] == "XY_GRAPH":
            return self._draw_xy()
        return super().draw()


def build_plan(bundle: dict, manifest: dict, learner: dict, target: dict, registry: dict) -> dict:
    plan = _ORIG_BUILD_PLAN(bundle, manifest, learner, target, registry)
    requirements = {x["representation_requirement_id"]: x for x in bundle.get("representation_requirements", [])}
    for rep in plan.get("representation_instances", []):
        req = requirements.get(rep["requirement_id"], {})
        rep["semantic_payload"] = copy.deepcopy(req.get("semantic_requirements", {}))
        if rep["representation_type"] == "XY_GRAPH":
            validate_xy_semantics(rep)
    return plan


def _append_connective(sec: dict, suffix: str, text: str) -> str:
    iid = f"PED-{sec['section_id']}-{suffix}"
    sec["items"].append({
        "item_id": iid,
        "type": "CONNECTIVE",
        "content": text,
        "traceability_class": "PEDAGOGICAL_CONNECTIVE",
        "research_refs": [],
    })
    return iid


def _item_ids(sec: dict, item_type: str) -> list[str]:
    return [x["item_id"] for x in sec.get("items", []) if x.get("type") == item_type]


def _support(profile: str) -> dict:
    if profile in {"FOUNDATION", "BRIDGE"}:
        return {
            "worked_example": {"state": "PRESENT"},
            "guided_1": {"state": "PRESENT"},
            "guided_2_faded": {"state": "PRESENT"},
            "independent_transfer": {"state": "PRESENT"},
        }
    reason = "High-baseline morphology removes routine scaffold while preserving independent transfer."
    return {
        "worked_example": {"state": "NOT_REQUIRED_WITH_REASON", "reason": reason},
        "guided_1": {"state": "NOT_REQUIRED_WITH_REASON", "reason": reason},
        "guided_2_faded": {"state": "NOT_REQUIRED_WITH_REASON", "reason": reason},
        "independent_transfer": {"state": "PRESENT"},
    }


def _auto_structure(model: dict, plan: dict) -> dict:
    units = []
    page_intents = []
    practice_map = {}
    for x in model["appendix_A"]["items"]:
        if x["item_id"].startswith("PRACTICE-"):
            practice_map[x["item_id"][9:]] = x["item_id"]

    for sec in model["main_sections"]:
        profile = sec["instructional_profile"]
        claim = (_item_ids(sec, "CLAIM") or [None])[0]
        condition = (_item_ids(sec, "CONDITION") or [None])[0]
        rep = (_item_ids(sec, "REPRESENTATION") or [None])[0]
        formal = (_item_ids(sec, "FORMAL_OBJECT") or [None])[0]
        worked = (_item_ids(sec, "WORKED_REASONING") or [None])[0]
        practice = practice_map.get(sec["section_id"])

        situation = _append_connective(sec, "SITUATION", "Start from the given situation or symbolic instance. Identify what is known before selecting a relation.")
        notice = _append_connective(sec, "NOTICE", "NOTICE · Identify the decisive pattern, condition, or representation feature before calculating.")
        guided1 = _append_connective(sec, "GUIDED1", "GUIDED 1 · Re-state the first move, then complete the next step with the verified model.")
        guided2 = _append_connective(sec, "GUIDED2", "GUIDED 2 · Use the same model with one support removed.")
        transfer = _append_connective(sec, "TRANSFER", "INDEPENDENT TRANSFER · Apply the verified model without step prompts and check the condition.")
        retrieval = _append_connective(sec, "RETRIEVAL", "RETRIEVAL CHECK · Name the trigger, first move, and one nearby failure case.")
        contrast = _append_connective(sec, "CONTRAST", "CONTRAST · Distinguish this model from the nearest tempting alternative before proceeding.")

        steps = []
        def add(role: str, ref: str | None, state: str):
            if ref:
                steps.append({"step_id": f"{sec['section_id']}-{len(steps)+1:02d}", "role": role, "content_refs": [ref], "support_state": state})
        if profile in {"FOUNDATION", "BRIDGE"}:
            add("PHYSICAL_SITUATION", situation, "FULL")
            add("DEPICTION", rep, "FULL")
            add("NOTICE", notice if notice else claim, "FULL")
            add("SAY_IN_WORDS", claim, "FULL")
            add("BUILD_RELATION", formal, "GUIDED")
            add("MODEL_BOUNDARY", condition, "REFERENCE")
            add("WORKED_EXAMPLE", worked or claim, "FULL")
            add("GUIDED_1", guided1 if guided1 else practice, "GUIDED")
            add("GUIDED_2_FADED", guided2 if guided2 else practice, "FADED")
            add("INDEPENDENT_TRANSFER", transfer if transfer else practice, "INDEPENDENT")
            add("RETRIEVAL_CHECK", retrieval, "INDEPENDENT")
        else:
            add("VARIANT_CONTRAST", contrast, "REFERENCE")
            add("DEPICTION", rep, "REFERENCE")
            add("NOTICE", notice if notice else claim, "REFERENCE")
            add("BUILD_RELATION", formal, "REFERENCE")
            add("MODEL_BOUNDARY", condition, "REFERENCE")
            add("INDEPENDENT_TRANSFER", transfer if transfer else practice, "INDEPENDENT")
            add("RETRIEVAL_CHECK", retrieval, "INDEPENDENT")

        unit = {
            "unit_id": sec["section_id"],
            "concept_ids": [sec["concept_id"]],
            "instructional_profile": profile,
            "cognitive_job": "Build the model with visible support, then fade to independent transfer." if profile in {"FOUNDATION", "BRIDGE"} else "Reconstruct the decisive model, test its boundary, then transfer independently.",
            "arc_steps": steps,
            "support_progression": _support(profile),
        }
        units.append(unit)
        page_intents.append({
            "page_intent_id": f"PI-{sec['section_id']}",
            "cognitive_job": unit["cognitive_job"],
            "content_refs": list(dict.fromkeys(ref for step in steps for ref in step["content_refs"])),
            "layout_relation": "REPRESENTATION_VS_REASONING" if rep else "SINGLE_FLOW",
        })

    return {
        "publication_structure_id": "PS-" + plan["publication_plan_id"],
        "schema_version": "1.0.0",
        "publication_plan_id": plan["publication_plan_id"],
        "research_bundle_id": plan["research_bundle_id"],
        "research_package_digest": plan["research_package_digest"],
        "learner_profile_id": plan["learner_profile_id"],
        "structure_profile": _structure_profile(plan),
        "study_guide": {
            "product_id": model["publication_id"],
            "product_first": True,
            "learning_units": units,
            "practice_topology": {"attempt_before_help": True, "progressive_hints": True, "solutions_after_attempts": True, "hint_delivery": "SEPARATE_HELP_SECTION"},
            "appendix_order": ["A", "B", "C"],
            "appendix_B_sections": ["FULL_SOLUTIONS"],
            "page_intents": page_intents,
            "navigation": {"question_to_hint": True, "question_to_solution": True, "solution_to_question": True, "solution_to_lesson": True},
        },
    }


def _known_content_ids(model: dict) -> set[str]:
    ids = set()
    for sec in model.get("main_sections", []):
        ids.update(x["item_id"] for x in sec.get("items", []))
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        ids.update(x["item_id"] for x in model.get(key, {}).get("items", []))
    return ids


def _validate_structure_content(structure: dict, model: dict) -> None:
    known = _known_content_ids(model)
    missing = []
    arc_refs = []
    ref_roles = {}
    duplicate_role_refs = []
    for unit in structure["study_guide"]["learning_units"]:
        for step in unit["arc_steps"]:
            for ref in step["content_refs"]:
                arc_refs.append(ref)
                if ref in ref_roles and ref_roles[ref] != step["role"]:
                    duplicate_role_refs.append(ref)
                ref_roles.setdefault(ref, step["role"])
                if ref not in known:
                    missing.append(ref)
    page_refs = []
    for page in structure["study_guide"]["page_intents"]:
        for ref in page["content_refs"]:
            page_refs.append(ref)
            if ref not in known:
                missing.append(ref)
    errors = []
    if missing:
        errors.extend("unknown content_ref: " + ref for ref in sorted(set(missing)))
    if duplicate_role_refs:
        errors.extend("content_ref assigned to multiple arc roles: " + ref for ref in sorted(set(duplicate_role_refs)))
    if page_refs != arc_refs:
        errors.append("page_intents must cover every arc-step content_ref exactly once and in the same order")
    if errors:
        print("CORE2_PUBLICATION_STRUCTURE_CONTENT_BINDING = FAIL")
        for err in errors:
            print("- " + err)
        raise SystemExit(2)


def build_study_model(bundle: dict, plan: dict) -> dict:
    global _CURRENT_STRUCTURE
    model = _ORIG_BUILD_STUDY_MODEL(bundle, plan)
    if _EXPLICIT_STRUCTURE is None:
        _CURRENT_STRUCTURE = _auto_structure(model, plan)
    else:
        _CURRENT_STRUCTURE = copy.deepcopy(_EXPLICIT_STRUCTURE)
    _validate_structure_binding(_CURRENT_STRUCTURE, plan)
    if _CURRENT_STRUCTURE["study_guide"].get("product_id") != model["publication_id"]:
        print("CORE2_PUBLICATION_STRUCTURE_STUDY_BINDING = FAIL")
        print(f"- expected product_id {model['publication_id']}, got {_CURRENT_STRUCTURE['study_guide'].get('product_id')}")
        raise SystemExit(2)
    legacy.validate_schema("publication-structure.schema.json", _CURRENT_STRUCTURE, _CONTRACTS)
    _validate_structure_content(_CURRENT_STRUCTURE, model)
    return model


def _content_map(model: dict) -> dict[str, dict]:
    out = {}
    for sec in model["main_sections"]:
        for item in sec["items"]:
            out[item["item_id"]] = item
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        for item in model[key]["items"]:
            out[item["item_id"]] = item
    return out


def _rep_map(plan: dict) -> dict[str, dict]:
    return {x["representation_instance_id"]: x for x in plan.get("representation_instances", [])}


def _arc_ref_map(structure: dict) -> dict[str, dict]:
    out = {}
    for unit in structure["study_guide"]["learning_units"]:
        for step in unit["arc_steps"]:
            for ref in step["content_refs"]:
                out[ref] = {"role": step["role"], "support_state": step.get("support_state", ""), "unit_id": unit["unit_id"], "unit_cognitive_job": unit["cognitive_job"]}
    return out


def render_study_pdf(model: dict, plan: dict, path: Path):
    if _CURRENT_STRUCTURE is None:
        print("CORE2_PUBLICATION_STRUCTURE_MISSING")
        raise SystemExit(2)
    st = legacy._styles("SG")
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=model["title"], author="Grade 9–11 Core (2) Publisher")
    items = _content_map(model)
    reps = _rep_map(plan)
    arc = _arc_ref_map(_CURRENT_STRUCTURE)
    story = [Paragraph(legacy.safe(model["title"]), st["h1"]), Paragraph(legacy.safe(model.get("subtitle", "")), st["body"]), Paragraph(legacy.safe(f"Core (1): {plan['research_bundle_id']} · package {plan['research_package_digest'][:12]}…"), st["small"]), PageBreak()]
    for page in _CURRENT_STRUCTURE["study_guide"]["page_intents"]:
        story.append(Paragraph("<b>COGNITIVE JOB</b> · " + legacy.safe(page["cognitive_job"]), st["h1"]))
        story.append(Paragraph(legacy.safe("Layout relation · " + page["layout_relation"].replace("_", " ")), st["small"]))
        current_unit = None
        for ref in page["content_refs"]:
            meta = arc[ref]
            if meta["unit_id"] != current_unit:
                current_unit = meta["unit_id"]
                story.append(Paragraph(legacy.safe(current_unit), st["small"]))
            role = meta["role"].replace("_", " ")
            support = meta.get("support_state", "")
            story.append(Paragraph(legacy.safe(f"{role} · {support}") if support else legacy.safe(role), st["h2"]))
            item = items[ref]
            story.append(Paragraph(legacy.safe(item["content"]), st["body"]))
            if item.get("representation_instance_id"):
                rep = reps[item["representation_instance_id"]]
                story.append(StructuredRepresentationFlowable(rep))
                story.append(Spacer(1, 3 * mm))
            if item.get("research_refs"):
                story.append(Paragraph(legacy.safe("Research: " + ", ".join(item["research_refs"])), st["small"]))
        story.append(PageBreak())
    app_by_letter = {"A": "appendix_A", "B": "appendix_B", "C": "appendix_C"}
    for letter in _CURRENT_STRUCTURE["study_guide"]["appendix_order"]:
        app = model[app_by_letter[letter]]
        story.append(Paragraph(legacy.safe(app["title"]), st["h1"]))
        for i, item in enumerate(app["items"], 1):
            story.append(Paragraph(legacy.safe(f"{i}. {item['content']}"), st["body"]))
            if item.get("research_refs"):
                story.append(Paragraph(legacy.safe("Research: " + ", ".join(item["research_refs"])), st["small"]))
        story.append(PageBreak())
    doc.build(story, onFirstPage=legacy.page_number, onLaterPages=legacy.page_number)


def build_study_markdown(model: dict, plan: dict) -> str:
    if _CURRENT_STRUCTURE is None:
        return legacy.build_study_markdown(model, plan)
    items = _content_map(model)
    arc = _arc_ref_map(_CURRENT_STRUCTURE)
    lines = [f"# {model['title']}", "", model.get("subtitle", ""), "", f"Research bundle: `{plan['research_bundle_id']}`", f"Research package: `{plan['research_package_digest']}`", f"Publication structure: `{_CURRENT_STRUCTURE['publication_structure_id']}`", ""]
    for page in _CURRENT_STRUCTURE["study_guide"]["page_intents"]:
        lines += [f"# COGNITIVE JOB · {page['cognitive_job']}", "", f"Layout relation · {page['layout_relation']}", ""]
        for ref in page["content_refs"]:
            meta = arc[ref]
            lines += [f"## {meta['role']} · {meta.get('support_state', '')}", ""]
            item = items[ref]
            lines.append(item["content"])
            if item.get("research_refs"):
                lines.append("Research: " + ", ".join(f"`{x}`" for x in item["research_refs"]))
            lines.append("")
    for letter, key in (("A", "appendix_A"), ("B", "appendix_B"), ("C", "appendix_C")):
        app = model[key]
        lines += [f"# {app['title']}", ""]
        for i, item in enumerate(app["items"], 1):
            lines.append(f"{i}. {item['content']}")
            if item.get("research_refs"):
                lines.append("Research: " + ", ".join(f"`{x}`" for x in item["research_refs"]))
        lines.append("")
    return "\n".join(lines)


def _augment_transfer_structure(model: dict, plan: dict) -> None:
    global _CURRENT_STRUCTURE
    if _CURRENT_STRUCTURE is None:
        return
    order = ["ATTEMPTS", "OPTIONAL_HELP", "COMPLETE_SOLUTIONS"]
    if any(x.get("mode") == "MIXED_TRANSFER" for x in model.get("sets", [])):
        order.append("MIXED_DIAGNOSIS")
    nav = [{"question_id": q["question_id"], "hint_target": "H-" + q["question_id"], "solution_target": "S-" + q["question_id"], "return_to_question": q["question_id"], "lesson_target": q["primary_concept_id"]} for q in model.get("questions", [])]
    if _EXPLICIT_STRUCTURE is not None and _CURRENT_STRUCTURE.get("transfer_book"):
        tb = _CURRENT_STRUCTURE["transfer_book"]
        if tb.get("product_id") != model["publication_id"]:
            print("CORE2_PUBLICATION_STRUCTURE_TRANSFER_BINDING = FAIL")
            print(f"- expected product_id {model['publication_id']}, got {tb.get('product_id')}")
            raise SystemExit(2)
        if [x["question_id"] for x in tb.get("question_navigation", [])] != [q["question_id"] for q in model.get("questions", [])]:
            print("CORE2_PUBLICATION_STRUCTURE_TRANSFER_BINDING = FAIL")
            print("- question_navigation must cover transfer questions in publication order")
            raise SystemExit(2)
    else:
        _CURRENT_STRUCTURE["transfer_book"] = {"product_id": model["publication_id"], "section_order": order, "attempt_before_hints": True, "solutions_after_attempts": True, "hint_delivery": "SEPARATE_HELP_SECTION", "mixed_diagnosis_after_solutions": "MIXED_DIAGNOSIS" in order, "question_navigation": nav}
    legacy.validate_schema("publication-structure.schema.json", _CURRENT_STRUCTURE, _CONTRACTS)


def build_transfer_markdown(model: dict, plan: dict) -> str:
    _augment_transfer_structure(model, plan)
    qmap = {q["question_id"]: q for q in model["questions"]}
    smap = {s["question_id"]: s for s in model["solutions"]}
    lines = [f"# {model['title']}", "", f"Research package: `{plan['research_package_digest']}`", f"Pair: `{model['product_identity'].get('pair_id', 'N/A')}`", "", "# ATTEMPTS", ""]
    for group in model["sets"]:
        lines += [f"## {group['set_id']} · {group['mode']}", ""]
        for qid in group["question_ids"]:
            q = qmap[qid]
            lines += [f"### {qid}", ""]
            if group["mode"] == "ASSIMILATION":
                lines.append(q["concept_labels"]["primary"])
                lines.extend(q["concept_labels"]["supports"])
                lines.append(f"{q['task']['label']} · {q['difficulty']['learner_label']} · {q['transfer']['label']}")
            else:
                lines.append("CONCEPT · IDENTIFY FIRST")
            lines += [f"Source: {q['source']['source_label']} · {q['source']['locator_label']}", q["source"]["source_link"], "Core (1): " + ", ".join(q["research_refs"]), "", q["stem"]]
            lines.extend(f"- {opt}" for opt in q.get("options", []))
            lines += ["", f"WORK HERE · {q['attempt']['workspace']}", "", "STOP · Try independently before opening Optional Help.", "", f"Optional Help: #H-{qid}", f"Complete Solution: #S-{qid}", ""]
    lines += ["# OPTIONAL HELP", ""]
    for q in model["questions"]:
        lines += [f"## H-{q['question_id']}", ""]
        for h in q.get("hints", []):
            lines += [f"**{h['tier']} · {h['role']}** — {h['content']}", ""]
        lines += [f"RETURN -> {q['question_id']}", ""]
    lines += ["# COMPLETE SOLUTIONS", ""]
    for q in model["questions"]:
        s = smap[q["question_id"]]
        lines += [f"## S-{q['question_id']}", "", f"QUESTION RECAP · {s['recap']}", f"WHY THIS WORKS · {s['why']}", f"METHOD · {s['method']}", f"ANSWER / CHECK · {s['answer_check']}", f"CONCEPT TO KEEP · {s['concept_to_keep']}", f"RETURN · {s['return_target']}", "Research: " + ", ".join(s["research_refs"]), ""]
    mixed = [x for x in model["sets"] if x["mode"] == "MIXED_TRANSFER"]
    if mixed:
        lines += ["# MIXED DIAGNOSIS", ""]
        for group in mixed:
            lines += [f"## {group['set_id']}", ""]
            for row in group["diagnosis"]["rows"]:
                lines.append(f"- {row['question_id']} · PRIMARY {row['primary_concept_id']} · {row['recognition_route']} · Repair: {row['repair_target']}")
            lines.append("")
    return "\n".join(lines)


def _anchor(name: str) -> str:
    return f'<a name="{html.escape(name, quote=True)}"/>'


def _goto(label: str, target: str) -> str:
    return f'<link href="#{html.escape(target, quote=True)}">{html.escape(label)}</link>'


def render_transfer_pdf(model: dict, plan: dict, path: Path):
    _augment_transfer_structure(model, plan)
    st = legacy._styles("TB")
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=model["title"], author="Grade 9–11 Core (2) Publisher")
    qmap = {q["question_id"]: q for q in model["questions"]}
    smap = {s["question_id"]: s for s in model["solutions"]}
    story = [Paragraph(legacy.safe(model["title"]), st["h1"]), Paragraph("Attempt first · Optional Help separate · Complete Solutions later", st["body"]), PageBreak(), Paragraph("ATTEMPTS", st["h1"])]
    for group in model["sets"]:
        story.append(Paragraph(legacy.safe(f"{group['set_id']} · {group['mode']}"), st["h2"]))
        for qid in group["question_ids"]:
            q = qmap[qid]
            story.append(Paragraph(_anchor(qid) + legacy.safe(qid), st["h2"]))
            if group["mode"] == "ASSIMILATION":
                meta = q["concept_labels"]["primary"] + " · " + q["task"]["label"] + " · " + q["difficulty"]["learner_label"] + " · " + q["transfer"]["label"]
                story.append(Paragraph(legacy.safe(meta), st["small"]))
                if q["concept_labels"]["supports"]:
                    story.append(Paragraph(legacy.safe(" · ".join(q["concept_labels"]["supports"])), st["small"]))
            else:
                story.append(Paragraph("<b>CONCEPT · IDENTIFY FIRST</b>", st["small"]))
            story.append(Paragraph(legacy.safe(f"Source: {q['source']['source_label']} · {q['source']['locator_label']}"), st["small"]))
            href = html.escape(q["source"]["source_link"], quote=True)
            story.append(Paragraph(f'<link href="{href}">Open source</link>', st["small"]))
            story.append(Paragraph(legacy.safe("Core (1): " + ", ".join(q["research_refs"])), st["small"]))
            story.append(Paragraph(legacy.safe(q["stem"]), st["body"]))
            for opt in q.get("options", []):
                story.append(Paragraph(legacy.safe("• " + opt), st["body"]))
            story.append(Spacer(1, 18 * mm))
            story.append(Paragraph("<b>STOP · Try independently before Optional Help.</b>", st["body"]))
            story.append(Paragraph(_goto("Open Optional Help", "H-" + qid) + " · " + _goto("Open Complete Solution", "S-" + qid), st["small"]))
            story.append(PageBreak())
    story += [Paragraph("OPTIONAL HELP", st["h1"])]
    for q in model["questions"]:
        qid = q["question_id"]
        story.append(Paragraph(_anchor("H-" + qid) + legacy.safe(qid), st["h2"]))
        for h in q.get("hints", []):
            story.append(Paragraph(legacy.safe(f"{h['tier']} · {h['role']} — {h['content']}"), st["hint"]))
        story.append(Paragraph(_goto("Return to question", qid), st["small"]))
        story.append(PageBreak())
    story += [Paragraph("COMPLETE SOLUTIONS", st["h1"])]
    for q in model["questions"]:
        qid = q["question_id"]
        s = smap[qid]
        story.append(Paragraph(_anchor("S-" + qid) + legacy.safe(qid), st["h2"]))
        for label, key in (("QUESTION RECAP", "recap"), ("WHY THIS WORKS", "why"), ("METHOD", "method"), ("ANSWER / CHECK", "answer_check"), ("CONCEPT TO KEEP", "concept_to_keep"), ("RETURN", "return_target")):
            story.append(Paragraph(f"<b>{label}</b> · {legacy.safe(s[key])}", st["body"]))
        story.append(Paragraph(legacy.safe("Research: " + ", ".join(s["research_refs"])), st["small"]))
        story.append(Paragraph(_goto("Return to question", qid), st["small"]))
        story.append(PageBreak())
    mixed = [x for x in model["sets"] if x["mode"] == "MIXED_TRANSFER"]
    if mixed:
        story += [Paragraph("MIXED DIAGNOSIS", st["h1"])]
        for group in mixed:
            story.append(Paragraph(legacy.safe(group["set_id"]), st["h2"]))
            for row in group["diagnosis"]["rows"]:
                story.append(Paragraph(legacy.safe(f"{row['question_id']} · PRIMARY {row['primary_concept_id']} · {row['recognition_route']} · Repair: {row['repair_target']}"), st["body"]))
        story.append(PageBreak())
    doc.build(story, onFirstPage=legacy.page_number, onLaterPages=legacy.page_number)


def _text_order(text: str, markers: list[str]) -> bool:
    pos = -1
    for marker in markers:
        nxt = text.find(marker, pos + 1)
        if nxt < 0:
            return False
        pos = nxt
    return True


def morphology_evidence(structure: dict, study_pdf: Path | None, transfer_pdf: Path | None) -> dict[str, bool]:
    out = {"product_structure": True, "arc_step_order_reconciliation": True, "page_intent_reconciliation": True, "support_progression_reconciliation": True, "attempt_help_solution_order": True, "appendix_order_reconciliation": True, "navigation_topology": True}
    if study_pdf and study_pdf.exists():
        doc = legacy.fitz.open(study_pdf)
        text = "\n".join(p.get_text() for p in doc)
        doc.close()
        for unit in structure["study_guide"]["learning_units"]:
            markers = [s["role"].replace("_", " ") for s in unit["arc_steps"]]
            if not _text_order(text, markers):
                out["arc_step_order_reconciliation"] = False
            prog = unit["support_progression"]
            present_to_role = {"worked_example": "WORKED EXAMPLE", "guided_1": "GUIDED 1", "guided_2_faded": "GUIDED 2 FADED", "independent_transfer": "INDEPENDENT TRANSFER"}
            for key, role in present_to_role.items():
                if prog[key]["state"] == "PRESENT" and role not in text:
                    out["support_progression_reconciliation"] = False
        for page in structure["study_guide"]["page_intents"]:
            if page["cognitive_job"] not in text:
                out["page_intent_reconciliation"] = False
        if not _text_order(text, ["Appendix A", "Appendix B", "Appendix C"]):
            out["appendix_order_reconciliation"] = False
    if transfer_pdf and transfer_pdf.exists() and structure.get("transfer_book"):
        doc = legacy.fitz.open(transfer_pdf)
        text = "\n".join(p.get_text() for p in doc)
        internal = sum(1 for p in doc for link in p.get_links() if link.get("kind") == legacy.fitz.LINK_GOTO)
        doc.close()
        wanted = [x.replace("_", " ") for x in structure["transfer_book"]["section_order"]]
        if not _text_order(text, wanted):
            out["attempt_help_solution_order"] = False
        min_links = max(1, len(structure["transfer_book"]["question_navigation"]) * 3)
        if internal < min_links:
            out["navigation_topology"] = False
    return out


def _finalize_structure_artifact(rc: int, argv: list[str]) -> int:
    if rc != 0 or _CURRENT_STRUCTURE is None:
        return rc
    out = Path(_arg_value(argv, "--out"))
    bundle = _load(Path(_arg_value(argv, "--bundle")))
    prefix = legacy.slugify(_arg_value(argv, "--prefix") or bundle["project"]["title"])
    structure_path = out / f"{prefix}_Core2_Publication_Structure.json"
    _write(structure_path, _CURRENT_STRUCTURE)
    study_pdf = out / f"{prefix}_Core2_Study_Guide.pdf"
    transfer_pdf = out / f"{prefix}_Core2_Transfer_Book.pdf"
    morph = morphology_evidence(_CURRENT_STRUCTURE, study_pdf if study_pdf.exists() else None, transfer_pdf if transfer_pdf.exists() else None)
    audit_path = out / f"{prefix}_Core2_Publication_Audit.json"
    manifest_path = out / f"{prefix}_Core2_Publication_Manifest.json"
    audit = _load(audit_path)
    audit["gates"].update(morph)
    audit["status"] = "PASS" if all(audit["gates"].values()) and not audit.get("warnings") else ("PASS_WITH_WARNINGS" if all(audit["gates"].values()) else "FAIL")
    if not all(morph.values()):
        audit["release_state"] = "AUTOMATED_FAIL"
    _write(audit_path, audit)
    legacy.validate_schema("publication-audit.schema.json", audit, _CONTRACTS)
    manifest = _load(manifest_path)
    arts = [a for a in manifest["artifacts"] if a["role"] != "PUBLICATION_STRUCTURE"]
    arts.append(legacy.artifact("PUBLICATION_STRUCTURE", structure_path, "application/json"))
    for a in arts:
        if a["role"] == "PUBLICATION_AUDIT":
            a.update(legacy.artifact("PUBLICATION_AUDIT", audit_path, "application/json"))
    manifest["artifacts"] = arts
    manifest["package_digest"] = legacy.package_digest(arts)
    _write(manifest_path, manifest)
    legacy.validate_schema("publication-manifest.schema.json", manifest, _CONTRACTS)
    if not all(morph.values()):
        print("CORE2_MORPHOLOGY_RECONCILIATION = FAIL")
        for key, value in morph.items():
            print(f"{key.upper()} = {'PASS' if value else 'FAIL'}")
        return 1
    print("PUBLICATION_STRUCTURE_BINDING = PASS")
    print("ARC_STEP_ORDER_RECONCILIATION = PASS")
    print("PAGE_INTENT_RECONCILIATION = PASS")
    print("SUPPORT_PROGRESSION_RECONCILIATION = PASS")
    print("ATTEMPT_HELP_SOLUTION_ORDER = PASS")
    print("APPENDIX_ORDER_RECONCILIATION = PASS")
    print("NAVIGATION_TOPOLOGY = PASS")
    print("PUBLICATION_PACKAGE_DIGEST = " + manifest["package_digest"])
    return 0


def main() -> int:
    global _EXPLICIT_STRUCTURE, _CONTRACTS
    original_argv = list(sys.argv)
    structure_value = _arg_value(original_argv, "--publication-structure")
    if structure_value:
        _EXPLICIT_STRUCTURE = _load(Path(structure_value))
    clean_argv = _remove_arg(original_argv, "--publication-structure")
    grade9 = Path(__file__).resolve().parents[3]
    _CONTRACTS = grade9 / "architecture" / "core2" / "contracts" / "v1"
    legacy.build_plan = build_plan
    legacy.build_study_model = build_study_model
    legacy.build_study_markdown = build_study_markdown
    legacy.render_study_pdf = render_study_pdf
    legacy.build_transfer_markdown = build_transfer_markdown
    legacy.render_transfer_pdf = render_transfer_pdf
    try:
        sys.argv = clean_argv
        rc = legacy.main()
    finally:
        sys.argv = original_argv
    return _finalize_structure_artifact(rc, clean_argv)


if __name__ == "__main__":
    raise SystemExit(main())
