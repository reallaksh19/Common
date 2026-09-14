#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

FORBIDDEN_RUNTIME_KEYS = {
    "learner_response", "attempt_history", "state_transition", "next_task",
    "adaptive_branch", "runtime_hint", "repair_route", "mastery_update",
}
HELP_ORDER = [
    "H1_ORIENT", "H2_STRUCTURE", "H3_REPRESENTATION", "H4_PRINCIPLE",
    "H5_FIRST_MOVE", "H6_PARTIAL_PATH", "H7_FULL_SOLUTION", "H8_VERIFY_REFLECT",
]
NAVY = HexColor("#17324D")
INK = HexColor("#20262D")
MUTED = HexColor("#66727D")
LINE = HexColor("#C8D1D8")
BLUE = HexColor("#EEF5FA")
AMBER = HexColor("#FFF5D9")
GREEN = HexColor("#EDF7EF")
TEAL = HexColor("#E9F6F3")

CHEMISTRY_ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT_ROOT = CHEMISTRY_ROOT / "LearningBlueprint"
BLUEPRINT_ENGINE = BLUEPRINT_ROOT / "engine" / "validate_blueprint_v4.py"
BLUEPRINT_POLICY = BLUEPRINT_ROOT / "policies" / "v4-bucket-and-conditioning-policy.json"


def _load_blueprint_v4():
    spec = importlib.util.spec_from_file_location("chem_blueprint_v4", BLUEPRINT_ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError("CHEM_CORE2B_BLUEPRINT_V4_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BLUEPRINT_V4 = _load_blueprint_v4()


def fail(code: str) -> None:
    raise ValueError(code)


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def walk_keys(obj: Any):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_keys(v)


def load_blueprint_policy() -> dict[str, Any]:
    return json.loads(BLUEPRINT_POLICY.read_text(encoding="utf-8"))


def validate(inp: dict) -> dict[str, Any]:
    if inp.get("subject") != "CHEMISTRY" or inp.get("delivery_mode") != "STATIC":
        fail("CHEM_CORE2B_STATIC_BOUNDARY_INVALID")
    if FORBIDDEN_RUNTIME_KEYS.intersection(set(walk_keys(inp))):
        fail("CHEM_B_LIVE_RUNTIME_FIELD_PRESENT")
    if inp.get("new_chemistry_refs"):
        fail("CHEM_B_NEW_CHEMISTRY_INTRODUCED")

    conditioning = inp.get("learner_conditioning")
    if not isinstance(conditioning, dict):
        fail("CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED")
    conditioning_authority = BLUEPRINT_V4.validate_core2_conditioning(conditioning, load_blueprint_policy())
    support = conditioning_authority.get("resolved_support_profile", {})
    entry = support.get("hint_entry_level")
    if entry not in HELP_ORDER[:6]:
        fail("CHEM_CORE2B_SUPPORT_PROFILE_INVALID")
    if support.get("solution_delay") not in {"AFTER_HINT_LADDER", "AFTER_FULL_ATTEMPT"}:
        fail("CHEM_CORE2B_SUPPORT_PROFILE_INVALID")

    selected = inp.get("selected_item_id")
    if selected not in set(inp.get("legal_core2a_item_ids", [])):
        fail("CHEM_CORE2B_ITEM_NOT_CORE2A_LEGAL")
    item = inp.get("source_item", {})
    if item.get("item_id") != selected:
        fail("CHEM_CORE2B_SOURCE_IDENTITY_DRIFT")
    required = ["source_locator", "stem", "canonical_answer", "problem_family_ref", "provenance_class"]
    if any(not item.get(k) for k in required):
        fail("CHEM_CORE2B_SOURCE_IDENTITY_DRIFT")
    if inp.get("question_mode") != "FROZEN_SOURCE_ITEM":
        fail("CHEM_CORE2B_SOURCE_IDENTITY_DRIFT")
    levels = [x.get("level") for x in inp.get("help", [])]
    if levels != HELP_ORDER:
        fail("CHEM_CORE2B_HELP_ORDER_INVALID")
    if not inp.get("full_solution") or not inp.get("verify_reflect"):
        fail("CHEM_CORE2B_ANSWER_CLOSURE_MISSING")
    if inp.get("help_mode") != "PROGRESSIVE_FIXED":
        fail("CHEM_CORE2B_HELP_ORDER_INVALID")
    return conditioning_authority


def _wrap(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in str(text).split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if stringWidth(trial, font, size) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def _text(c, x, y, text, width, size=9.2, font="Helvetica", leading=None, color=INK):
    leading = leading or size * 1.28
    c.setFillColor(color)
    c.setFont(font, size)
    yy = y
    for line in _wrap(text, font, size, width):
        c.drawString(x, yy, line)
        yy -= leading
    return yy


def _header(c, subtitle: str):
    W, H = A4
    m = 36
    c.setFillColor(NAVY)
    c.rect(0, H-64, W, 64, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(m, H-28, "Chemistry Core2B")
    c.setFont("Helvetica", 8.5)
    c.drawString(m, H-46, subtitle)


def _visible_help(inp: dict, conditioning_authority: dict[str, Any]) -> list[dict[str, Any]]:
    entry = conditioning_authority["resolved_support_profile"]["hint_entry_level"]
    start = HELP_ORDER.index(entry)
    return inp["help"][start:6]


def _attempt_prompt(support: dict[str, Any]) -> str:
    density = support.get("support_density")
    if density == "HIGH":
        return "Before solving: state the target, separate the decisive evidence from surface cues, and make a representation before choosing the first move."
    if density == "MEDIUM":
        return "Before solving: state what is being asked, identify the decisive evidence, and choose a representation."
    if density == "LOW":
        return "Before solving: write a short plan and commit to a first move."
    return "Attempt independently. Commit to a plan before opening help."


def _draw_solution(c, inp: dict, y_top: float) -> float:
    W, _ = A4
    m = 36
    item = inp["source_item"]
    c.setFillColor(GREEN)
    c.roundRect(m, y_top-150, W-2*m, 140, 6, fill=1, stroke=0)
    _text(c, m+12, y_top-30, "H7 FULL SOLUTION", W-2*m-24, 9.2, "Helvetica-Bold", color=NAVY)
    yy = _text(c, m+12, y_top-52, inp["full_solution"], W-2*m-24, 8.5, leading=10.6)
    _text(c, m+12, yy-7, f"Canonical answer: {item['canonical_answer']}", W-2*m-24, 8.5, "Helvetica-Bold")
    return y_top - 162


def _draw_verify(c, inp: dict, y_top: float) -> None:
    W, _ = A4
    m = 36
    c.setFillColor(TEAL)
    c.roundRect(m, max(42, y_top-108), W-2*m, 100, 6, fill=1, stroke=0)
    _text(c, m+12, y_top-30, "H8 VERIFY / REFLECT", W-2*m-24, 9.0, "Helvetica-Bold", color=NAVY)
    _text(c, m+12, y_top-52, inp["verify_reflect"], W-2*m-24, 8.5, "Helvetica-Bold", leading=10.6)


def render(inp: dict, pdf_path: Path, conditioning_authority: dict[str, Any]) -> dict:
    W, H = A4
    m = 36
    item = inp["source_item"]
    support = conditioning_authority["resolved_support_profile"]
    solution_delay = support["solution_delay"]
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    c.setTitle(f"Chemistry Core2B {item['item_id']}")

    # Attempt page: same frozen item, compile-time support envelope only.
    _header(c, "Attempt first - method/family label intentionally withheld")
    c.setFillColor(BLUE)
    c.roundRect(m, H-150, W-2*m, 62, 6, fill=1, stroke=0)
    _text(c, m+12, H-112, f"Source: {item['source_locator']}", W-2*m-24, 8.8, "Helvetica-Bold")
    _text(c, m, H-180, item["stem"], W-2*m, 11.0, "Helvetica-Bold", leading=14.2, color=NAVY)
    _text(c, m, H-270, _attempt_prompt(support), W-2*m, 9.2, "Helvetica-Bold")

    y0 = H - 315
    if support.get("representation_support") == "SUPPLIED":
        representation = next(x["text"] for x in inp["help"] if x["level"] == "H3_REPRESENTATION")
        c.setFillColor(AMBER)
        c.roundRect(m, y0-58, W-2*m, 50, 5, fill=1, stroke=0)
        _text(c, m+10, y0-25, "STARTER REPRESENTATION: " + representation, W-2*m-20, 8.4, "Helvetica-Bold", leading=10.3)
        y0 -= 72

    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.3)
    c.drawString(m, y0, "YOUR ATTEMPT")
    c.setStrokeColor(LINE)
    for i in range(int(inp.get("workspace_lines", 10))):
        y = y0 - 30 - i*31
        if y < 82:
            break
        c.line(m+10, y, W-m-10, y)
    c.setFillColor(AMBER)
    c.roundRect(m, 42, W-2*m, 48, 6, fill=1, stroke=0)
    _text(c, m+12, 72, "Stop here until you have made a genuine attempt. The next page reveals only the support authorized by the learner-conditioning profile.", W-2*m-24, 8.5, "Helvetica-Bold")
    c.showPage()

    # Progressive help page. Lower support can intentionally skip early hints.
    _header(c, "Progressive fixed help - use the smallest available hint that restarts reasoning")
    y = H - 95
    visible_help = _visible_help(inp, conditioning_authority)
    for row in visible_help:
        fill = BLUE if row["level"] in {"H1_ORIENT", "H2_STRUCTURE", "H3_REPRESENTATION"} else AMBER
        c.setFillColor(fill)
        c.roundRect(m, y-58, W-2*m, 50, 5, fill=1, stroke=0)
        _text(c, m+10, y-25, f"{row['level'].replace('_',' ')}: {row['text']}", W-2*m-20, 8.5, "Helvetica-Bold" if row["level"] == visible_help[0]["level"] else "Helvetica", leading=10.5)
        y -= 64

    if solution_delay == "AFTER_HINT_LADDER":
        y = _draw_solution(c, inp, y)
        _draw_verify(c, inp, y)
        c.showPage()
        pages = 2
    else:
        c.setFillColor(AMBER)
        c.roundRect(m, 52, W-2*m, 62, 6, fill=1, stroke=0)
        _text(c, m+12, 88, "Do not turn the page until you have completed a full attempt using only the support above.", W-2*m-24, 8.7, "Helvetica-Bold")
        c.showPage()
        _header(c, "Full answer closure - open only after the full attempt")
        y = _draw_solution(c, inp, H - 100)
        _draw_verify(c, inp, y)
        c.showPage()
        pages = 3

    c.save()
    data = pdf_path.read_bytes()
    return {
        "path": pdf_path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "pages": pages,
        "support_density": support.get("support_density"),
        "hint_entry_level": support.get("hint_entry_level"),
        "solution_delay": solution_delay,
    }


def compile_product(inp: dict, out_dir: Path) -> dict:
    conditioning_authority = validate(inp)
    out_dir.mkdir(parents=True, exist_ok=True)
    item = inp["source_item"]
    conditioning = inp["learner_conditioning"]
    plan = {
        "schema_version": "1.1.0",
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "product_type": "CORE2B_SELF_TUTOR",
        "source_core2a_ref": inp["source_core2a_ref"],
        "selected_item_id": inp["selected_item_id"],
        "problem_family_ref": item["problem_family_ref"],
        "purpose": inp["purpose"],
        "difficulty_dimensions": inp.get("difficulty_dimensions", {}),
        "conditioning_mode": conditioning_authority["mode"],
        "resolved_support_profile": conditioning_authority["resolved_support_profile"],
        "help_mode": "PROGRESSIVE_FIXED",
        "live_runtime_fields": "ABSENT",
        "question_mode": "FROZEN_SOURCE_ITEM",
        "blueprint_control_axis": "LEARNER_CONDITIONING",
    }
    if conditioning_authority["mode"] == "KNOWLEDGE_PERCENT":
        plan["knowledge_percent"] = conditioning_authority["knowledge_percent"]
        plan["knowledge_interpretation"] = conditioning_authority["knowledge_interpretation"]
    else:
        plan["owner_override_auditable"] = True
        plan["resolved_demand_profile"] = conditioning_authority["resolved_demand_profile"]
    plan["plan_digest"] = digest(plan)
    (out_dir / "core2b_plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    artifact = render(inp, out_dir / "chemistry_core2b.pdf", conditioning_authority)
    audit = {
        "status": "PASS",
        "delivery_mode": "STATIC",
        "live_runtime_fields": "ABSENT",
        "question_mode": "FROZEN_SOURCE_ITEM",
        "selected_item_id": inp["selected_item_id"],
        "answer_closure": "PASS",
        "help_order": HELP_ORDER,
        "conditioning_mode": conditioning_authority["mode"],
        "resolved_support_profile": conditioning_authority["resolved_support_profile"],
        "blueprint_v4": conditioning_authority,
        "artifact": artifact,
    }
    if conditioning_authority["mode"] == "KNOWLEDGE_PERCENT":
        audit["knowledge_percent"] = conditioning_authority["knowledge_percent"]
    else:
        audit["owner_override_auditable"] = True
        audit["fabricated_knowledge_percent"] = False
    (out_dir / "core2b_quality_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    return audit


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    audit = compile_product(load(args.input), Path(args.out_dir))
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
