#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

LEVELS = [
    "M0_DIRECT", "M1_CONTROLLED_VARIATION", "M2_REPRESENTATION_TRANSFER",
    "M3_INVERSE_TARGET", "M4_HIDDEN_STRUCTURE", "M5_METHOD_DISCRIMINATION",
    "M6_FAMILY_DISCRIMINATION", "M7_MULTI_STEP_SYNTHESIS", "M8_MIXED_COMPETITIVE",
]
LIVE_FIELDS = {
    "attempts", "learner_response", "state_transition", "next_task", "retry",
    "runtime_hint", "retrieval_schedule", "repair_handoff", "adaptive_branch",
}
FORBIDDEN_LEARNER_TOKENS = {
    "core2a_legal_item_ids", "capability_ref", "state transition",
    "next task", "runtime hint", "repair handoff", "evidence ceiling",
}
PEDAGOGY_MODE = "OPEN_ENDED"
LEARNER_ROLE = "SELECT_TRANSFER_DISCRIMINATE_SYNTHESIZE"
HELP_SEQUENCE = [
    "RECOGNITION_HELP", "CONCEPT_HELP", "REPRESENTATION_HELP",
    "FIRST_MOVE_HELP", "METHOD_HELP", "ANSWER_VERIFICATION",
]


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _reject_live_fields(value, path="root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in LIVE_FIELDS:
                fail("CORE2B_LIVE_RUNTIME_FIELD_FORBIDDEN", f"{path}.{key}")
            _reject_live_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _reject_live_fields(child, f"{path}[{i}]")


def _transfer_focus(level: str) -> str:
    return {
        "M0_DIRECT": "Recognise the familiar structure without being told the formula name.",
        "M1_CONTROLLED_VARIATION": "Identify the one changed feature and what should remain invariant.",
        "M2_REPRESENTATION_TRANSFER": "Translate between representations before choosing the method.",
        "M3_INVERSE_TARGET": "Work backward from the target and identify which relation must be inverted.",
        "M4_HIDDEN_STRUCTURE": "Find the familiar mathematical structure hidden by the surface wording.",
        "M5_METHOD_DISCRIMINATION": "Choose the efficient method and justify why the alternatives are less suitable.",
        "M6_FAMILY_DISCRIMINATION": "Classify the underlying problem family from structure rather than labels.",
        "M7_MULTI_STEP_SYNTHESIS": "Coordinate multiple known ideas while keeping intermediate goals explicit.",
        "M8_MIXED_COMPETITIVE": "Synthesize across families under reduced cue visibility and higher novelty.",
    }[level]


def _self_guided_frame(item: dict) -> dict:
    help_map = {
        "RECOGNITION_HELP": "Ignore the surface story for a moment. What quantities, constraints, or invariants are actually present?",
        "CONCEPT_HELP": "Name the mathematical relationship that connects the known information to the target.",
        "REPRESENTATION_HELP": "Redraw, tabulate, parameterise, or rewrite the information so the hidden structure becomes visible.",
        "FIRST_MOVE_HELP": "Write only the first relation or transformation that makes progress; do not complete the solution yet.",
        "METHOD_HELP": "Compare the plausible methods and choose the one that exposes the structure with the least unnecessary work.",
        "ANSWER_VERIFICATION": "After solving, use the answer check and independently verify with substitution, a second representation, or a boundary/consistency check.",
    }
    return {
        "attempt_first": True,
        "transfer_focus": _transfer_focus(item["demand_level"]),
        "help_sequence": list(HELP_SEQUENCE),
        "help": help_map,
        "authored_support": list(item.get("support", [])),
        "answer_check": item.get("answer_check", ""),
        "concept_level_not_solution_dump": True,
    }


def validate(doc: dict) -> None:
    _reject_live_fields(doc)
    if not doc.get("core2a_authority_ref") or not doc.get("core2a_legal_item_ids"):
        fail("CORE2B_CORE2A_AUTHORITY_MISSING")
    ceiling = doc.get("max_demand_level")
    if ceiling not in LEVELS:
        fail("CORE2B_COMPILE_CEILING_INVALID", str(ceiling))
    ceiling_i = LEVELS.index(ceiling)
    legal = set(doc["core2a_legal_item_ids"])
    approved = set(doc.get("approved_capability_refs", []))
    items = doc.get("items", [])
    if not items:
        fail("CORE2B_EMPTY_SELECTION")

    for item in items:
        item_id = item.get("item_id")
        if item_id not in legal:
            fail("CORE2B_ITEM_NOT_CORE2A_LEGAL", str(item_id))
        level = item.get("demand_level")
        if level not in LEVELS:
            fail("CORE2B_DEMAND_LEVEL_INVALID", str(level))
        if LEVELS.index(level) > ceiling_i:
            fail("CORE2B_TRANSFER_EXCEEDS_COMPILE_CEILING", f"{item_id}:{level}>{ceiling}")
        refs = set(item.get("capability_refs", []))
        if not refs or not refs.issubset(approved):
            fail("CORE2B_UNAPPROVED_CAPABILITY_REF", ",".join(sorted(refs - approved)))
        if not str(item.get("stem", "")).strip():
            fail("CORE2B_OPEN_QUESTION_MISSING", str(item_id))
        if LEVELS.index(level) >= LEVELS.index("M5_METHOD_DISCRIMINATION") and item.get("family_label_visible"):
            fail("CORE2B_FAMILY_LABEL_LEAK", item_id)
        learner_text = "\n".join([
            str(item.get("stem", "")),
            *[str(x) for x in item.get("support", [])],
            str(item.get("answer_check", "")),
        ]).lower()
        for token in FORBIDDEN_LEARNER_TOKENS:
            if token in learner_text:
                fail("CORE2B_INTERNAL_METADATA_LEAK", token)


def compile_plan(doc: dict) -> dict:
    validate(doc)
    level_index = {level: i for i, level in enumerate(LEVELS)}
    ordered = sorted(doc["items"], key=lambda x: (level_index[x["demand_level"]], x["item_id"]))
    items = []
    for source in ordered:
        item = copy.deepcopy(source)
        item["self_guided_frame"] = _self_guided_frame(item)
        items.append(item)
    payload = {
        "schema_version": "2.0.0",
        "subject": "MATHEMATICS",
        "delivery_mode": "STATIC",
        "pedagogy_mode": PEDAGOGY_MODE,
        "learner_role": LEARNER_ROLE,
        "product_role": "CORE2B_TRANSFER",
        "governing_question": "Can the learner recognize, select and transfer the mathematics when the surface changes and the method is not named?",
        "self_guided_help_sequence": list(HELP_SEQUENCE),
        "source_core2a_authority_ref": doc["core2a_authority_ref"],
        "purpose": doc["purpose"],
        "compile_ceiling": doc["max_demand_level"],
        "capability_refs": list(doc["approved_capability_refs"]),
        "title": doc["title"],
        "items": items,
        "quality_audit": {
            "status": "PASS",
            "live_runtime_fields": "ABSENT",
            "open_ended_self_guided": True,
            "attempt_precedes_explanation": True,
            "all_items_core2a_legal": True,
            "ceiling_respected": True,
            "discrimination_labels_hidden": True,
            "concept_level_help_present": True,
        },
    }
    payload["plan_id"] = "MATH-C2B-" + digest(payload)[:16]
    return payload


def render_pdf(plan: dict, path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="C2BTitle", parent=styles["Title"], fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="C2BH2", parent=styles["Heading2"], fontSize=11.5, leading=14, textColor=colors.HexColor("#17324D"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="C2BBody", parent=styles["BodyText"], fontSize=9.5, leading=13, spaceAfter=5))
    styles.add(ParagraphStyle(name="C2BHelp", parent=styles["BodyText"], fontSize=8.8, leading=12, leftIndent=10, spaceAfter=4))
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=42)
    story = [
        Paragraph(plan["title"], styles["C2BTitle"]),
        Paragraph(f"{plan['purpose'].title()} open-ended transfer workbook", styles["C2BBody"]),
        Paragraph("Attempt before using help. The method/family may be deliberately hidden.", styles["C2BBody"]),
        Spacer(1, 8),
    ]
    for i, item in enumerate(plan["items"], 1):
        story.append(Paragraph(f"{i}. {item.get('learner_label', 'Try it first')}", styles["C2BH2"]))
        story.append(Paragraph("<b>ATTEMPT FIRST</b>", styles["C2BBody"]))
        story.append(Paragraph(item["stem"], styles["C2BBody"]))
        frame = item["self_guided_frame"]
        story.append(Paragraph(f"<b>Transfer focus:</b> {frame['transfer_focus']}", styles["C2BHelp"]))
        for label in frame["help_sequence"][:-1]:
            story.append(Paragraph(f"<b>{label.replace('_',' ').title()}:</b> {frame['help'][label]}", styles["C2BHelp"]))
        for support in frame.get("authored_support", []):
            story.append(Paragraph(f"<b>Authored support:</b> {support}", styles["C2BHelp"]))
        if item.get("answer_check"):
            story.append(Paragraph(f"<b>Answer + verification:</b> {item['answer_check']}", styles["C2BBody"]))
        story.append(Spacer(1, 8))
    doc.build(story)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pdf")
    args = ap.parse_args()
    doc = json.loads(Path(args.input).read_text(encoding="utf-8"))
    plan = compile_plan(doc)
    Path(args.out).write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.pdf:
        render_pdf(plan, Path(args.pdf))
    print(plan["plan_id"])


if __name__ == "__main__":
    main()
