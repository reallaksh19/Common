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
FORBIDDEN_CORE1_KNOWLEDGE_KEYS = {
    "student_knowledge_percent", "knowledge_percent", "learner_readiness_percent",
}
HELP_ORDER = ["H1_ORIENT", "H2_REPRESENT", "H3_PRINCIPLE", "H4_FIRST_MOVE"]
NAVY = HexColor("#17324D")
INK = HexColor("#20262D")
MUTED = HexColor("#66727D")
LINE = HexColor("#C8D1D8")
BLUE = HexColor("#EEF5FA")
AMBER = HexColor("#FFF5D9")
GREEN = HexColor("#EDF7EF")

CHEMISTRY_ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT_ROOT = CHEMISTRY_ROOT / "LearningBlueprint"
BLUEPRINT_ENGINE = BLUEPRINT_ROOT / "engine" / "validate_blueprint_v4.py"
BLUEPRINT_POLICY = BLUEPRINT_ROOT / "policies" / "v4-bucket-and-conditioning-policy.json"


def _load_blueprint_v4():
    spec = importlib.util.spec_from_file_location("chem_blueprint_v4", BLUEPRINT_ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError("CHEM_CORE1B_BLUEPRINT_V4_UNAVAILABLE")
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


def validate(inp: dict) -> dict[str, Any]:
    if inp.get("subject") != "CHEMISTRY" or inp.get("delivery_mode") != "STATIC":
        fail("CHEM_CORE1B_STATIC_BOUNDARY_INVALID")
    keys = set(walk_keys(inp))
    bad = FORBIDDEN_RUNTIME_KEYS.intersection(keys)
    if bad:
        fail("CHEM_B_LIVE_RUNTIME_FIELD_PRESENT")
    contaminated = FORBIDDEN_CORE1_KNOWLEDGE_KEYS.intersection(keys)
    if contaminated:
        fail("CHEM_CORE1B_KNOWLEDGE_CONTAMINATION")
    if inp.get("new_chemistry_refs"):
        fail("CHEM_B_NEW_CHEMISTRY_INTRODUCED")

    bucket = inp.get("instruction_bucket")
    if not isinstance(bucket, dict):
        fail("CHEM_CORE1B_BLUEPRINT_V4_BUCKET_REQUIRED")
    bucket_authority = BLUEPRINT_V4.validate_instruction_bucket(bucket)

    cap = inp.get("capability_ref")
    if cap not in set(inp.get("approved_capability_refs", [])):
        fail("CHEM_CORE1B_AUTHORITY_SCOPE_VIOLATION")
    fam = inp.get("problem_family_ref")
    if fam not in set(inp.get("approved_problem_family_refs", [])):
        fail("CHEM_CORE1B_AUTHORITY_SCOPE_VIOLATION")
    if not inp.get("task_prompt") or not inp.get("canonical_answer") or not inp.get("check"):
        fail("CHEM_CORE1B_ANSWER_CLOSURE_MISSING")
    help_rows = inp.get("help", [])
    levels = [x.get("level") for x in help_rows]
    if not levels or any(x not in HELP_ORDER for x in levels):
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")
    ranks = [HELP_ORDER.index(x) for x in levels]
    if ranks != sorted(ranks) or len(ranks) != len(set(ranks)):
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")
    if inp.get("help_mode") != "PROGRESSIVE_FIXED":
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")
    return bucket_authority


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


def render(inp: dict, pdf_path: Path, bucket_authority: dict[str, Any]) -> dict:
    W, H = A4
    m = 36
    bucket = inp["instruction_bucket"]
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    c.setTitle(inp["title"])

    c.setFillColor(NAVY)
    c.rect(0, H - 64, W, 64, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(m, H - 28, "Chemistry Core1B")
    c.setFont("Helvetica", 8.5)
    c.drawString(m, H - 46, "Open-ended concept self-tutor - attempt first, then reveal fixed help")

    _text(c, m, H - 94, inp["title"], W - 2*m, 11.2, "Helvetica-Bold", color=NAVY)
    _text(
        c, m, H - 114,
        f"{bucket['difficulty_badge']} bucket | {bucket['title']}",
        W - 2*m, 8.1, "Helvetica-Bold", color=MUTED,
    )
    if inp.get("representation_summary"):
        c.setFillColor(BLUE)
        c.roundRect(m, H - 218, W - 2*m, 82, 6, fill=1, stroke=0)
        _text(c, m+12, H-163, inp["representation_summary"], W-2*m-24, 9.2, "Helvetica-Bold")
        top = H - 243
    else:
        top = H - 148

    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(m, top-277, W-2*m, 277, 7, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(m+12, top-22, "OPEN-ENDED TASK")
    yy = _text(c, m+12, top-52, inp["task_prompt"], W-2*m-24, 10.0, "Helvetica-Bold", leading=13.2)
    yy -= 18
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(m+12, yy, "YOUR THINKING / WORK")
    c.setStrokeColor(LINE)
    for i in range(int(inp.get("workspace_lines", 5))):
        ly = yy - 25 - i*29
        if ly < top-262:
            break
        c.line(m+18, ly, W-m-18, ly)

    help_top = top - 302
    c.setFillColor(AMBER)
    c.roundRect(m, 48, W-2*m, help_top-48, 7, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9.7)
    c.drawString(m+12, help_top-20, "SELF-GUIDED HELP - read only after attempting")
    y = help_top - 45
    for row in inp["help"]:
        y = _text(c, m+14, y, f"{row['level'].replace('_',' ')}: {row['text']}", W-2*m-28, 8.4, "Helvetica-Bold" if row["level"] == "H1_ORIENT" else "Helvetica", leading=10.5)
        y -= 4
    y -= 3
    c.setFillColor(GREEN)
    c.roundRect(m+10, 58, W-2*m-20, max(92, y-58), 5, fill=1, stroke=0)
    _text(c, m+20, y-17, "CANONICAL / EXPECTED RESPONSE", W-2*m-40, 8.6, "Helvetica-Bold", color=NAVY)
    y2 = _text(c, m+20, y-37, inp["canonical_answer"], W-2*m-40, 8.5, "Helvetica-Bold", leading=10.8)
    if inp.get("explanation"):
        y2 = _text(c, m+20, y2-5, inp["explanation"], W-2*m-40, 8.2, leading=10.3)
    _text(c, m+20, y2-5, "CHECK: " + inp["check"], W-2*m-40, 8.2, "Helvetica-Bold", leading=10.3)

    c.save()
    data = pdf_path.read_bytes()
    return {
        "path": pdf_path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "pages": 1,
        "bucket_difficulty": bucket_authority["difficulty_badge"],
    }


def compile_product(inp: dict, out_dir: Path) -> dict:
    bucket_authority = validate(inp)
    out_dir.mkdir(parents=True, exist_ok=True)
    bucket = inp["instruction_bucket"]
    plan = {
        "schema_version": "1.1.0",
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "product_type": "CORE1B_SELF_TUTOR",
        "source_core1a_ref": inp["source_core1a_ref"],
        "capability_ref": inp["capability_ref"],
        "problem_family_ref": inp["problem_family_ref"],
        "bucket_id": bucket["bucket_id"],
        "subtopic_id": bucket["subtopic_id"],
        "difficulty_badge": bucket_authority["difficulty_badge"],
        "page_envelope_max": bucket_authority["max_pages"],
        "page_envelope_is_ceiling_not_quota": True,
        "research_mode": bucket_authority["research_mode"],
        "visual_jobs": bucket["visual_plan"]["visual_jobs"],
        "cognitive_moves": inp.get("cognitive_moves", []),
        "help_mode": "PROGRESSIVE_FIXED",
        "blueprint_control_axis": bucket_authority["control_axis"],
        "learner_knowledge_used_for_depth": False,
        "live_runtime_fields": "ABSENT",
    }
    plan["plan_digest"] = digest(plan)
    (out_dir / "core1b_plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    artifact = render(inp, out_dir / "chemistry_core1b.pdf", bucket_authority)
    audit = {
        "status": "PASS",
        "delivery_mode": "STATIC",
        "live_runtime_fields": "ABSENT",
        "new_chemistry_refs": [],
        "answer_closure": "PASS",
        "help_order": [x["level"] for x in inp["help"]],
        "blueprint_v4": bucket_authority,
        "bucket_id": bucket["bucket_id"],
        "learner_knowledge_used_for_depth": False,
        "artifact": artifact,
    }
    (out_dir / "core1b_quality_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
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
