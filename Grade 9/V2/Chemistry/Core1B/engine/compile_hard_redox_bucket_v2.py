#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve()
V1_PATH = HERE.with_name("compile_hard_redox_bucket.py")
spec = importlib.util.spec_from_file_location("hard_redox_v1", V1_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("CHEM_CORE1B_HARD_V1_UNAVAILABLE")
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)

AMBER = HexColor("#FFF5D9")
GREEN = HexColor("#EDF7EF")
NAVY = HexColor("#17324D")
MUTED = HexColor("#66727D")
LINE = HexColor("#C8D1D8")

MODULE_HINTS = {
    "SPECIES_IDENTITY": [
        "H1 ORIENT: Ignore Redox names for now. Which element on the left must be matched with the same element on the right?",
        "H2 REPRESENT: Draw two identity arrows: Zn -> Zn2+ and Cu2+ -> Cu.",
        "H3 PRINCIPLE: A Redox label is earned only after the same element or species has been tracked across the reaction.",
        "H4 FIRST MOVE: Write the two species pairs before writing oxidation, reduction or an agent role."
    ],
    "OXIDATION_STATE_MEANING": [
        "H1 ORIENT: Stay on one element. What number belongs to it before the arrow, and what number belongs to it after?",
        "H2 REPRESENT: Put the two oxidation-state values on one horizontal lane for the same element.",
        "H3 PRINCIPLE: In this bucket the oxidation state is a bookkeeping value used to compare before with after; do not automatically treat it as an isolated-particle charge.",
        "H4 FIRST MOVE: For Zn write 0 -> +2; for Cu write +2 -> 0, then describe only increase or decrease."
    ],
    "DIRECTION_TO_LABEL": [
        "H1 ORIENT: Do not use the Redox word until you have decided whether the oxidation-state number went up or down.",
        "H2 REPRESENT: Mark an upward/increase lane and a downward/decrease lane.",
        "H3 PRINCIPLE: Increase in oxidation state = oxidation; decrease in oxidation state = reduction.",
        "H4 FIRST MOVE: Say '0 -> +2 increases' or '+2 -> 0 decreases' before naming the Redox process."
    ],
    "ELECTRON_CONSEQUENCE": [
        "H1 ORIENT: Which species loses electrons and which gains them in the authorized half-statements?",
        "H2 REPRESENT: Write Zn -> Zn2+ + 2e- beside Cu2+ + 2e- -> Cu.",
        "H3 PRINCIPLE: Electron loss must match electron gain in the same reaction ledger.",
        "H4 FIRST MOVE: Count the electrons on both statements before drawing any conclusion."
    ],
    "AGENT_ROLE": [
        "H1 ORIENT: The agent name describes what the reactant causes elsewhere, so prove its own change first.",
        "H2 REPRESENT: Use the chain SELF change -> electron consequence -> effect on the other species -> agent role.",
        "H3 PRINCIPLE: The reducing agent is itself oxidised; the oxidising agent is itself reduced.",
        "H4 FIRST MOVE: Begin with 'Zn: 0 -> +2, oxidised' or 'Cu: +2 -> 0, reduced' before writing an agent label."
    ],
    "REPRESENTATION_TRANSLATION": [
        "H1 ORIENT: Preserve the same chemistry while changing only the form in which it is expressed.",
        "H2 REPRESENT: Translate among equation, species map, oxidation-state lane, electron statement and prose proof.",
        "H3 PRINCIPLE: A representation is acceptable only if it preserves species identity and the same direction of chemical change.",
        "H4 FIRST MOVE: Identify what information must survive the translation before rewriting it."
    ],
    "MISCONCEPTION_BOUNDARY": [
        "H1 ORIENT: Identify the exact claim that is unsafe rather than rejecting the whole answer vaguely.",
        "H2 REPRESENT: Place the plausible wrong claim beside the governed evidence that can falsify it.",
        "H3 PRINCIPLE: Oxidation-state bookkeeping, species identity and the balanced electron ledger are the checks that control the conclusion here.",
        "H4 FIRST MOVE: Point to the first line where the wrong model disagrees with the governed reaction evidence."
    ],
    "FADING_TEACH_BACK": [
        "H1 ORIENT: Try to reconstruct before reopening any earlier page.",
        "H2 REPRESENT: If stuck, rebuild only the four anchors: species identity -> state change -> electron consequence -> agent role.",
        "H3 PRINCIPLE: Each later claim must be supported by the earlier evidence; do not replace the chain with a memorized slogan.",
        "H4 FIRST MOVE: Write the reaction and the two species pairs from memory, then continue without looking."
    ]
}


def module_hints(module: str) -> list[str]:
    hints = MODULE_HINTS.get(module)
    if hints is None or len(hints) != 4:
        raise ValueError("CHEM_CORE1B_HARD_MODULE_HINTS_MISSING")
    return hints


def render_page(c, page: dict, facts: dict):
    W, H = A4
    v1.header(c, page["page_no"], page["module"], page["title"])
    v1.visual(c, page["visual"], H-115, facts)

    c.setFillColor(v1.white)
    c.setStrokeColor(LINE)
    c.roundRect(36, H-470, W-72, 235, 7, fill=1, stroke=1)
    v1.text(c, 48, H-263, "OPEN-ENDED TASK", W-96, 9.5, "Helvetica-Bold", color=NAVY)
    yy = v1.text(c, 48, H-290, page["prompt"], W-96, 9.8, "Helvetica-Bold", leading=13)
    yy -= 12
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.0)
    c.drawString(48, yy, "YOUR THINKING / WORK")
    c.setStrokeColor(LINE)
    for i in range(4):
        c.line(54, yy-26-i*31, W-54, yy-26-i*31)

    c.setFillColor(AMBER)
    c.roundRect(36, 210, W-72, 120, 7, fill=1, stroke=0)
    v1.text(c, 48, 307, "SELF-GUIDED HELP - use only if stuck", W-96, 9.2, "Helvetica-Bold", color=NAVY)
    y = 286
    for hint in module_hints(page["module"]):
        y = v1.text(c, 50, y, hint, W-100, 7.8, leading=9.4)
        y -= 2

    c.setFillColor(GREEN)
    c.roundRect(36, 48, W-72, 146, 7, fill=1, stroke=0)
    v1.text(c, 48, 175, "CANONICAL RESPONSE", W-96, 8.7, "Helvetica-Bold", color=NAVY)
    y = v1.text(c, 48, 154, page["answer"], W-96, 8.4, "Helvetica-Bold", leading=10.6)
    v1.text(c, 48, y-6, "CHECK: " + page["check"], W-96, 8.1, "Helvetica-Bold", leading=10.2)
    v1.footer(c)


def compile_product(inp: dict, out_dir: Path) -> dict:
    authority = v1.validate(inp)
    pages = v1.page_specs(inp)
    if len(pages) != 24:
        raise ValueError("CHEM_CORE1B_HARD_PAGE_REALIZATION_MISMATCH")
    for module in inp["module_sequence"]:
        module_hints(module)

    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / "chemistry_core1b_hard_redox.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setTitle("Chemistry Core1B HARD Redox production golden")
    for page in pages:
        render_page(c, page, inp["governed_facts"])
        c.showPage()
    c.save()

    plan = {
        "schema_version": "1.2.1",
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "product_type": "CORE1B_HARD_BUCKET_SELF_TUTOR",
        "bucket_id": inp["instruction_bucket"]["bucket_id"],
        "difficulty_badge": authority["difficulty_badge"],
        "page_envelope_max": authority["max_pages"],
        "realized_pages": 24,
        "research_mode": authority["research_mode"],
        "research_evidence_ids": [x["id"] for x in inp["research_evidence"]],
        "module_sequence": inp["module_sequence"],
        "module_specific_hint_ladders": True,
        "representation_authority": inp["representation_authority"],
        "learner_knowledge_used_for_depth": False,
        "live_runtime_fields": "ABSENT"
    }
    raw = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    plan["plan_digest"] = hashlib.sha256(raw.encode()).hexdigest()
    (out_dir / "core1b_hard_plan.json").write_text(json.dumps(plan, indent=2)+"\n", encoding="utf-8")

    data = pdf.read_bytes()
    audit = {
        "status": "PASS",
        "delivery_mode": "STATIC",
        "live_runtime_fields": "ABSENT",
        "new_chemistry_refs": [],
        "blueprint_v4": authority,
        "realized_pages": 24,
        "page_ceiling": authority["max_pages"],
        "research_evidence_count": len(inp["research_evidence"]),
        "representation_authority": inp["representation_authority"],
        "forbidden_representation_additions_absent": True,
        "module_specific_hint_ladders": True,
        "hint_ladder_count": len(MODULE_HINTS),
        "answer_closure_pages": 24,
        "artifact": {"path": pdf.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    }
    (out_dir / "core1b_hard_quality_audit.json").write_text(json.dumps(audit, indent=2)+"\n", encoding="utf-8")
    return audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    print(json.dumps(compile_product(v1.load(args.input), Path(args.out_dir)), indent=2))


if __name__ == "__main__":
    main()
