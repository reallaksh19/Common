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

ROOT = Path(__file__).resolve().parents[2]
BP_ENGINE = ROOT / "LearningBlueprint" / "engine" / "validate_blueprint_v4.py"

spec = importlib.util.spec_from_file_location("chem_blueprint_v4", BP_ENGINE)
if spec is None or spec.loader is None:
    raise RuntimeError("CHEM_CORE1B_BLUEPRINT_V4_UNAVAILABLE")
BP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BP)

NAVY = HexColor("#17324D")
INK = HexColor("#20262D")
MUTED = HexColor("#66727D")
LINE = HexColor("#C8D1D8")
BLUE = HexColor("#EEF5FA")
GREEN = HexColor("#EDF7EF")
AMBER = HexColor("#FFF5D9")
RED = HexColor("#FCEDEA")
TEAL = HexColor("#E9F6F3")
GRAY = HexColor("#F4F6F7")

FORBIDDEN_RUNTIME = {"learner_response", "attempt_history", "adaptive_branch", "mastery_update", "state_transition", "next_task"}
FORBIDDEN_KNOWLEDGE = {"knowledge_percent", "student_knowledge_percent", "learner_readiness_percent"}
EXPECTED_MODULES = [
    "SPECIES_IDENTITY", "OXIDATION_STATE_MEANING", "DIRECTION_TO_LABEL", "ELECTRON_CONSEQUENCE",
    "AGENT_ROLE", "REPRESENTATION_TRANSLATION", "MISCONCEPTION_BOUNDARY", "FADING_TEACH_BACK",
]


def fail(code: str) -> None:
    raise ValueError(code)


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def walk_keys(obj: Any):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from walk_keys(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_keys(value)


def validate(inp: dict) -> dict[str, Any]:
    if inp.get("subject") != "CHEMISTRY" or inp.get("delivery_mode") != "STATIC":
        fail("CHEM_CORE1B_HARD_STATIC_BOUNDARY_INVALID")
    keys = set(walk_keys(inp))
    if keys & FORBIDDEN_RUNTIME:
        fail("CHEM_B_LIVE_RUNTIME_FIELD_PRESENT")
    if keys & FORBIDDEN_KNOWLEDGE:
        fail("CHEM_CORE1B_KNOWLEDGE_CONTAMINATION")
    if inp.get("new_chemistry_refs"):
        fail("CHEM_B_NEW_CHEMISTRY_INTRODUCED")
    authority = BP.validate_instruction_bucket(inp.get("instruction_bucket", {}))
    if authority["difficulty_badge"] != "HARD" or authority["research_mode"] != "DEEP_REQUIRED":
        fail("CHEM_CORE1B_HARD_BUCKET_AUTHORITY_REQUIRED")
    modules = inp.get("module_sequence")
    if modules != EXPECTED_MODULES:
        fail("CHEM_CORE1B_HARD_MODULE_SEQUENCE_INVALID")
    if inp.get("pages_per_module") != 3 or inp.get("planned_pages") != 24:
        fail("CHEM_CORE1B_HARD_PAGE_PLAN_INVALID")
    if inp["planned_pages"] > authority["max_pages"]:
        fail("CHEM_CORE1B_HARD_PAGE_PLAN_EXCEEDS_V4_CEILING")
    if inp.get("representation_authority") != ["SYMBOLIC"]:
        fail("CHEM_CORE1B_HARD_REPRESENTATION_AUTHORITY_DRIFT")
    if len(inp.get("research_evidence", [])) < 4:
        fail("CHEM_CORE1B_HARD_RESEARCH_EVIDENCE_INCOMPLETE")
    facts = inp.get("governed_facts", {})
    required = {"reaction", "species_pairs", "oxidation_state_lanes", "electron_statements", "agent_roles", "governing_rules"}
    if not required.issubset(facts):
        fail("CHEM_CORE1B_HARD_GOVERNED_FACTS_INCOMPLETE")
    if facts["reaction"] != "Zn + Cu2+ -> Zn2+ + Cu":
        fail("CHEM_CORE1B_HARD_REACTION_AUTHORITY_DRIFT")
    return authority


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    out: list[str] = []
    for para in str(text).split("\n"):
        words = para.split()
        if not words:
            out.append("")
            continue
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if stringWidth(trial, font, size) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    return out


def text(c, x, y, value, width, size=9.0, font="Helvetica", leading=None, color=INK):
    leading = leading or size * 1.28
    c.setFillColor(color)
    c.setFont(font, size)
    yy = y
    for line in wrap(value, font, size, width):
        c.drawString(x, yy, line)
        yy -= leading
    return yy


def arrow(c, x1, y1, x2, y2):
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.2)
    c.line(x1, y1, x2, y2)
    c.line(x2, y2, x2-6, y2+3)
    c.line(x2, y2, x2-6, y2-3)


def header(c, page_no: int, module: str, title: str):
    W, H = A4
    c.setFillColor(NAVY)
    c.rect(0, H-62, W, 62, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(36, H-27, "Chemistry Core1B | HARD Redox Tutor")
    c.setFont("Helvetica", 8.2)
    c.drawString(36, H-44, f"{module.replace('_',' ')} | attempt first, then use the smallest help needed")
    c.drawRightString(W-36, H-44, f"{page_no}/24")
    text(c, 36, H-88, title, W-72, 11.0, "Helvetica-Bold", color=NAVY)


def footer(c):
    W, _ = A4
    c.setStrokeColor(LINE)
    c.line(36, 22, W-36, 22)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.0)
    c.drawString(36, 10, "Static self-tutor | Core1A authority unchanged | No learner response is observed")


def visual(c, kind: str, y: float, facts: dict):
    W, _ = A4
    x, w = 48, W-96
    c.setFillColor(BLUE)
    c.roundRect(x, y-96, w, 90, 6, fill=1, stroke=0)
    if kind == "SPECIES_MAP":
        text(c, x+12, y-26, "SAME ELEMENT ACROSS THE REACTION", w-24, 8.2, "Helvetica-Bold", color=NAVY)
        text(c, x+22, y-57, "Zn", 50, 12, "Helvetica-Bold")
        arrow(c, x+76, y-53, x+180, y-53)
        text(c, x+195, y-57, "Zn2+", 70, 12, "Helvetica-Bold")
        text(c, x+300, y-57, "Cu2+", 70, 12, "Helvetica-Bold")
        arrow(c, x+360, y-53, x+430, y-53)
        text(c, x+445, y-57, "Cu", 50, 12, "Helvetica-Bold")
    elif kind == "DUAL_LANE":
        text(c, x+12, y-24, "OXIDATION-STATE LANES", w-24, 8.2, "Helvetica-Bold", color=NAVY)
        text(c, x+22, y-53, "Zn: 0", 75, 11, "Helvetica-Bold")
        arrow(c, x+105, y-49, x+195, y-49)
        text(c, x+210, y-53, "+2", 40, 11, "Helvetica-Bold")
        text(c, x+300, y-53, "Cu: +2", 75, 11, "Helvetica-Bold")
        arrow(c, x+382, y-49, x+450, y-49)
        text(c, x+465, y-53, "0", 30, 11, "Helvetica-Bold")
    elif kind == "ELECTRON_PAIR":
        text(c, x+12, y-24, "ELECTRON CONSEQUENCE", w-24, 8.2, "Helvetica-Bold", color=NAVY)
        text(c, x+25, y-53, facts["electron_statements"][0], 210, 10.5, "Helvetica-Bold")
        text(c, x+290, y-53, facts["electron_statements"][1], 220, 10.5, "Helvetica-Bold")
        text(c, x+155, y-78, "2e- lost = 2e- gained", 250, 9.2, "Helvetica-Bold", color=NAVY)
    elif kind == "CHAIN":
        labels = ["species identity", "state change", "electron consequence", "agent role"]
        xx = x+8
        for i, lab in enumerate(labels):
            c.setFillColor(GREEN if i < 3 else AMBER)
            c.roundRect(xx, y-67, 112, 40, 5, fill=1, stroke=0)
            text(c, xx+7, y-45, lab, 98, 7.8, "Helvetica-Bold", color=NAVY)
            if i < 3:
                arrow(c, xx+114, y-47, xx+132, y-47)
            xx += 126
    elif kind == "ERROR_CONTRAST":
        c.setFillColor(RED)
        c.roundRect(x+10, y-80, 230, 58, 5, fill=1, stroke=0)
        text(c, x+20, y-42, "WRONG: role first, self-change guessed later", 210, 8.2, "Helvetica-Bold")
        c.setFillColor(GREEN)
        c.roundRect(x+260, y-80, 245, 58, 5, fill=1, stroke=0)
        text(c, x+270, y-42, "CORRECT: prove self-change -> conclude role", 225, 8.2, "Helvetica-Bold")
    else:
        text(c, x+12, y-38, facts["reaction"], w-24, 13, "Helvetica-Bold", color=NAVY)


def page_specs(inp: dict) -> list[dict[str, str]]:
    f = inp["governed_facts"]
    r = f["reaction"]
    specs = [
        ("SPECIES_IDENTITY", "Retrieve the reaction structure", f"Without using oxidation or reduction words, map the same elements across {r}.", "SPECIES_MAP", "Zn maps to Zn2+; Cu in Cu2+ maps to Cu. Identity is tracked before any Redox label.", "Could another learner follow the same element from left to right?"),
        ("SPECIES_IDENTITY", "Commit before naming a role", "Why is it unsafe to begin by calling Zn a reducing agent? Write the evidence that must come first.", "CHAIN", "The role is a conclusion. First prove what happens to Zn itself, then connect that self-change to the effect on Cu2+.", "Does your explanation begin with evidence rather than a remembered label?"),
        ("SPECIES_IDENTITY", "Diagnose the shortcut", "A learner says 'Zn is the reducing agent because metals usually reduce other things.' What is missing from this argument?", "ERROR_CONTRAST", "The argument lacks reaction-specific self-change evidence. Track Zn -> Zn2+ and its oxidation-state change before assigning a role.", "Would the reasoning still work if the reagent name were unfamiliar?"),

        ("OXIDATION_STATE_MEANING", "What does the number track?", "Use the two lanes to state what an oxidation-state number is doing in this proof. Do not treat the number as a free-standing particle picture.", "DUAL_LANE", "The oxidation state is used as a bookkeeping value for the same element before and after the reaction so the direction of Redox change can be proved.", "Have you kept oxidation state distinct from an automatic claim about isolated-particle charge?"),
        ("OXIDATION_STATE_MEANING", "Construct the Zn lane", "Write the before and after oxidation state for Zn, then describe only the numerical direction of change.", "DUAL_LANE", "Zn: 0 -> +2; the value increases.", "Did you compare Zn with Zn, not Zn with Cu?"),
        ("OXIDATION_STATE_MEANING", "Construct the Cu lane", "Write the before and after oxidation state for Cu, then describe only the numerical direction of change.", "DUAL_LANE", "Cu: +2 -> 0; the value decreases.", "Did you keep species identity fixed while comparing the numbers?"),

        ("DIRECTION_TO_LABEL", "Build the Redox rule from direction", "From the two lanes, write the rule connecting increase/decrease to oxidation/reduction.", "DUAL_LANE", "Increase in oxidation state -> oxidation. Decrease in oxidation state -> reduction.", "Can you state the rule without mentioning Zn or Cu?"),
        ("DIRECTION_TO_LABEL", "Apply the rule to both elements", "Use the rule you just built to label Zn and Cu in the reaction.", "DUAL_LANE", "Zn is oxidised because 0 -> +2 increases. Cu2+ is reduced because +2 -> 0 decreases.", "Does each label agree with the direction on its lane?"),
        ("DIRECTION_TO_LABEL", "Reverse the inference", "If you are told Zn is oxidised, which lane is compatible: 0 -> +2 or +2 -> 0? Explain rather than choosing by memory.", "DUAL_LANE", "0 -> +2 is compatible because oxidation corresponds to an increase in oxidation state.", "Could you reject the other lane using the rule alone?"),

        ("ELECTRON_CONSEQUENCE", "Write the Zn electron statement", "Translate the Zn self-change into the authorized electron statement.", "ELECTRON_PAIR", f"{f['electron_statements'][0]}. Zn loses 2e-.", "Are electrons on the product side for the species that loses them?"),
        ("ELECTRON_CONSEQUENCE", "Write the Cu2+ electron statement", "Translate the Cu2+ self-change into the authorized electron statement.", "ELECTRON_PAIR", f"{f['electron_statements'][1]}. Cu2+ gains 2e-.", "Are electrons on the reactant side for the species that gains them?"),
        ("ELECTRON_CONSEQUENCE", "Close the electron ledger", "Use both half-statements to give one numerical consistency check for the reaction.", "ELECTRON_PAIR", "2e- are lost by Zn and 2e- are gained by Cu2+; the electron ledger closes.", "Does electron loss equal electron gain?"),

        ("AGENT_ROLE", "Build the Zn role from evidence", "Complete the chain: Zn self-change -> effect on Cu2+ -> agent role.", "CHAIN", "Zn is oxidised and loses electrons; those electrons reduce Cu2+. Therefore Zn is the reducing agent.", "Did the agent label appear only after the self-change and other-species effect?"),
        ("AGENT_ROLE", "Build the Cu2+ role from evidence", "Complete the chain: Cu2+ self-change -> relation to Zn -> agent role.", "CHAIN", "Cu2+ is reduced and gains electrons supplied by Zn. Therefore Cu2+ is the oxidising agent.", "Does the role agree with Cu2+ being reduced?"),
        ("AGENT_ROLE", "Correct the classic reversal", "Evaluate: 'Zn is the reducing agent because Zn gets reduced.' Rewrite the statement as a valid proof.", "ERROR_CONTRAST", "The claim is wrong because Zn is oxidised, not reduced. Zn: 0 -> +2, loses 2e-, reduces Cu2+, therefore Zn is the reducing agent.", "Have you corrected both the self-change and the reason for the agent name?"),

        ("REPRESENTATION_TRANSLATION", "Equation -> species map", f"Start only from {r}. Produce the species-identity map that must exist before oxidation-state work begins.", "SPECIES_MAP", "Zn -> Zn2+ and Cu2+ -> Cu.", "Does every tracked line refer to the same element on both sides?"),
        ("REPRESENTATION_TRANSLATION", "Lanes -> chemical prose", "Translate Zn: 0 -> +2 and Cu: +2 -> 0 into two complete chemical sentences without using arrows.", "DUAL_LANE", "Zn undergoes an increase in oxidation state and is oxidised. Cu undergoes a decrease in oxidation state and Cu2+ is reduced.", "Did the prose preserve the numerical direction?"),
        ("REPRESENTATION_TRANSLATION", "Prose -> proof chain", "From 'Zn is oxidised; Cu2+ is reduced', reconstruct the missing symbolic evidence and electron consequence.", "CHAIN", "Zn: 0 -> +2 and Zn -> Zn2+ + 2e-. Cu: +2 -> 0 and Cu2+ + 2e- -> Cu.", "Could your proof be checked without trusting the prose labels?"),

        ("MISCONCEPTION_BOUNDARY", "Oxidation state is not automatically ion charge", "A learner says: 'Oxidation state and ionic charge always mean exactly the same thing.' Why is that unsafe as a general rule, and what is the safe use in this bucket?", "ERROR_CONTRAST", "Oxidation state is a bookkeeping value used here to track Redox change. Do not automatically treat it as the actual charge on an isolated particle in every chemical context.", "Did you state the safe bookkeeping use without inventing a new particle model?"),
        ("MISCONCEPTION_BOUNDARY", "Oxidation and reduction are paired here", "Could this reaction be described as Zn being oxidised while nothing is reduced? Use the electron ledger to decide.", "ELECTRON_PAIR", "No. In this reaction the 2e- lost by Zn are gained by Cu2+; Zn oxidation and Cu2+ reduction are paired in the same electron-transfer ledger.", "Did you use the balanced electron statements rather than a slogan?"),
        ("MISCONCEPTION_BOUNDARY", "Spot the identity error", "A learner compares Zn: 0 with Cu: 0 and concludes 'no change'. Diagnose the exact reasoning failure.", "SPECIES_MAP", "The learner compared different elements. Oxidation-state change must track the same element before and after: Zn with Zn, Cu with Cu.", "Does your repair begin by restoring species identity?"),

        ("FADING_TEACH_BACK", "Minimal cue: rebuild the proof", f"Using only {r}, write the complete four-link Redox proof with no supplied lane labels.", "CHAIN", "Zn -> Zn2+; 0 -> +2; Zn is oxidised and loses 2e-; therefore Zn is the reducing agent. Cu2+ -> Cu; +2 -> 0; Cu2+ is reduced and gains 2e-; therefore Cu2+ is the oxidising agent.", "Did you include identity, state change, electron consequence and agent role?"),
        ("FADING_TEACH_BACK", "Teach it back without the diagram", "Explain to another learner why 'reducing agent' does not mean 'the substance that is reduced'. Use the reaction as evidence.", "ERROR_CONTRAST", "The reducing agent causes reduction elsewhere and is itself oxidised. Here Zn is oxidised from 0 to +2, supplies electrons that reduce Cu2+, and therefore acts as the reducing agent.", "Could your explanation correct the misconception without relying on a memorized slogan?"),
        ("FADING_TEACH_BACK", "Final retrieval and self-check", "Close the page above this panel. From memory, reconstruct the reaction, both oxidation-state lanes, both electron statements and both agent roles. Then reopen and check each link.", "CHAIN", "Reaction: Zn + Cu2+ -> Zn2+ + Cu. Zn: 0 -> +2, oxidised, Zn -> Zn2+ + 2e-, reducing agent. Cu: +2 -> 0, reduced, Cu2+ + 2e- -> Cu, oxidising agent.", "Can you reproduce every link without looking, and does 2e- lost equal 2e- gained?"),
    ]
    return [
        {"page_no": i+1, "module": row[0], "title": row[1], "prompt": row[2], "visual": row[3], "answer": row[4], "check": row[5]}
        for i, row in enumerate(specs)
    ]


def render_page(c, spec: dict, facts: dict):
    W, H = A4
    header(c, spec["page_no"], spec["module"], spec["title"])
    visual(c, spec["visual"], H-115, facts)

    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(36, H-470, W-72, 235, 7, fill=1, stroke=1)
    text(c, 48, H-263, "OPEN-ENDED TASK", W-96, 9.5, "Helvetica-Bold", color=NAVY)
    yy = text(c, 48, H-290, spec["prompt"], W-96, 9.8, "Helvetica-Bold", leading=13)
    yy -= 12
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 8.0)
    c.drawString(48, yy, "YOUR THINKING / WORK")
    c.setStrokeColor(LINE)
    for i in range(4):
        c.line(54, yy-26-i*31, W-54, yy-26-i*31)

    c.setFillColor(AMBER)
    c.roundRect(36, 210, W-72, 120, 7, fill=1, stroke=0)
    text(c, 48, 307, "SELF-GUIDED HELP - use only if stuck", W-96, 9.2, "Helvetica-Bold", color=NAVY)
    hints = [
        "H1 ORIENT: Track the same species or element before naming a Redox role.",
        "H2 REPRESENT: Use a species map, oxidation-state lane, electron statement or proof chain as appropriate.",
        "H3 PRINCIPLE: Increase = oxidation; decrease = reduction; SELF change is evidence, role is conclusion.",
        "H4 FIRST MOVE: Write the first evidence line before any agent label."
    ]
    y = 286
    for hint in hints:
        y = text(c, 50, y, hint, W-100, 7.9, leading=9.6)
        y -= 2

    c.setFillColor(GREEN)
    c.roundRect(36, 48, W-72, 146, 7, fill=1, stroke=0)
    text(c, 48, 175, "CANONICAL RESPONSE", W-96, 8.7, "Helvetica-Bold", color=NAVY)
    y = text(c, 48, 154, spec["answer"], W-96, 8.4, "Helvetica-Bold", leading=10.6)
    text(c, 48, y-6, "CHECK: " + spec["check"], W-96, 8.1, "Helvetica-Bold", leading=10.2)
    footer(c)


def compile_product(inp: dict, out_dir: Path) -> dict:
    authority = validate(inp)
    pages = page_specs(inp)
    if len(pages) != inp["planned_pages"]:
        fail("CHEM_CORE1B_HARD_PAGE_REALIZATION_MISMATCH")
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / "chemistry_core1b_hard_redox.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setTitle("Chemistry Core1B HARD Redox production golden")
    for page in pages:
        render_page(c, page, inp["governed_facts"])
        c.showPage()
    c.save()

    plan = {
        "schema_version": "1.2.0",
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "product_type": "CORE1B_HARD_BUCKET_SELF_TUTOR",
        "bucket_id": inp["instruction_bucket"]["bucket_id"],
        "difficulty_badge": authority["difficulty_badge"],
        "page_envelope_max": authority["max_pages"],
        "realized_pages": len(pages),
        "research_mode": authority["research_mode"],
        "research_evidence_ids": [x["id"] for x in inp["research_evidence"]],
        "module_sequence": inp["module_sequence"],
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
        "realized_pages": len(pages),
        "page_ceiling": authority["max_pages"],
        "research_evidence_count": len(inp["research_evidence"]),
        "representation_authority": inp["representation_authority"],
        "forbidden_representation_additions_absent": True,
        "answer_closure_pages": len(pages),
        "artifact": {"path": pdf.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    }
    (out_dir / "core1b_hard_quality_audit.json").write_text(json.dumps(audit, indent=2)+"\n", encoding="utf-8")
    return audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    print(json.dumps(compile_product(load(args.input), Path(args.out_dir)), indent=2))


if __name__ == "__main__":
    main()
