#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATH = HERE.parents[1]
MB_ENGINE = MATH / "MathBlueprint" / "engine"
if str(MB_ENGINE) not in sys.path:
    sys.path.insert(0, str(MB_ENGINE))

from producer_governance import core1b_receipt
from emit_stage_governance import write_receipt
from engineering_product_custody import load_custody, stamp_receipt, custody_summary
from validate_canonical_domain_registry import validate_registry

LIVE_FIELDS = {
    "attempts", "learner_evidence", "state_transition", "next_task",
    "repair_map", "runtime_hint", "adaptive_branch", "learner_response",
}
ALLOWED_BLOCKS = {
    "METHOD_COMPARISON", "ERROR_CONTRAST", "CONTROLLED_VARIATION",
    "COMPLETION", "FADED", "CLOSE_INDEPENDENT", "ANSWER_CHECK",
}
FORBIDDEN_LEARNER_TOKENS = {
    "capability_ref", "learner_state", "runtime", "repair route",
    "state transition", "next task", "evidence state",
}
PEDAGOGY_MODE = "OPEN_ENDED"
LEARNER_ROLE = "RECONSTRUCT_AND_CONSOLIDATE"
HELP_SEQUENCE = [
    "MEANING_HELP", "REPRESENTATION_HELP", "CONCEPT_HELP",
    "FIRST_MOVE_HELP", "PROCEDURE_HELP", "ANSWER_VERIFICATION",
]


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _derived_badge(dimensions: dict) -> str:
    score = sum(dimensions.values()) / (4 * len(dimensions)) * 100
    return "EASY" if score <= 32 else "MEDIUM" if score <= 65 else "HARD"


def _validate_difficulty(doc: dict) -> None:
    row = doc.get("difficulty_governance")
    if not row:
        fail("CORE1B_DIFFICULTY_GOVERNANCE_MISSING")
    expected = {"EASY": (10, "NONE"), "MEDIUM": (20, "TARGETED"), "HARD": (30, "DEEP")}
    badge = row.get("operational_badge")
    if badge not in expected:
        fail("CORE1B_DIFFICULTY_BADGE_INVALID", str(badge))
    pages, research = expected[badge]
    if row.get("page_ceiling") != pages or row.get("research_level") != research:
        fail("CORE1B_DIFFICULTY_CONSEQUENCE_DRIFT")
    if row.get("badge_authority") in {"DERIVED", "VALIDATED_DERIVED"}:
        if _derived_badge(row.get("derived_dimensions") or {}) != badge:
            fail("CORE1B_DERIVED_DIFFICULTY_MISMATCH")
    if not row.get("evidence_refs"):
        fail("CORE1B_DIFFICULTY_EVIDENCE_MISSING")


def _reject_live_fields(value, path="root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in LIVE_FIELDS:
                fail("CORE1B_LIVE_RUNTIME_FIELD_FORBIDDEN", f"{path}.{key}")
            _reject_live_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _reject_live_fields(child, f"{path}[{i}]")


def _self_guided_frame(block: dict) -> dict | None:
    kind = block["kind"]
    if kind == "ANSWER_CHECK":
        return None
    common = {
        "MEANING_HELP": "State what the unknown represents and what information is fixed before calculating.",
        "REPRESENTATION_HELP": "Draw, tabulate, or symbolically organise the objects and constraints so the relationship becomes visible.",
        "CONCEPT_HELP": "Name the governing idea or invariant and state the condition that makes it valid.",
        "FIRST_MOVE_HELP": "Write only the first mathematical relation you would use; do not finish the calculation yet.",
        "PROCEDURE_HELP": "Carry out one justified transformation at a time, keeping variable meanings and constraints unchanged.",
        "ANSWER_VERIFICATION": "Compare with the answer/check section and verify numerically, symbolically, or through the representation.",
    }
    focus = {
        "METHOD_COMPARISON": "Before reading either method, predict which structural feature makes one route shorter.",
        "ERROR_CONTRAST": "Test the proposed shortcut or claim before correcting it; identify the condition that failed.",
        "CONTROLLED_VARIATION": "Identify the one changed feature and predict what should remain invariant before solving.",
        "COMPLETION": "Reconstruct the missing structure from the meaning of the quantities, not by guessing the next algebra line.",
        "FADED": "Use the smallest remaining scaffold and rebuild the omitted steps yourself.",
        "CLOSE_INDEPENDENT": "Choose the representation, governing relation, and first move without being told the method.",
    }[kind]
    return {
        "attempt_first": True,
        "open_question": block.get("learner_text", ""),
        "reconstruction_focus": focus,
        "help_sequence": list(HELP_SEQUENCE),
        "help": common,
        "visual_clue": "Make the constraint and the varying quantity visible before compressing the situation into symbols.",
        "concept_level_not_solution_dump": True,
    }


def validate(doc: dict) -> None:
    _reject_live_fields(doc)
    _validate_difficulty(doc)
    if not doc.get("core1a_authority_ref") or not doc.get("approved_capability_refs"):
        fail("CORE1B_UPSTREAM_AUTHORITY_MISSING")
    approved = set(doc["approved_capability_refs"])
    blocks = doc.get("blocks", [])
    if not blocks:
        fail("CORE1B_REQUIRED_COMPARISON_MISSING")
    kinds = []
    for block in blocks:
        kind = block.get("kind")
        if kind not in ALLOWED_BLOCKS:
            fail("CORE1B_UNKNOWN_BLOCK", str(kind))
        kinds.append(kind)
        refs = set(block.get("capability_refs", []))
        if not refs or not refs.issubset(approved):
            fail("CORE1B_UNAPPROVED_CAPABILITY_REF", ",".join(sorted(refs - approved)))
        if block.get("new_math_refs"):
            fail("CORE1B_NEW_MATH_NOT_ALLOWED", block.get("block_id", ""))
        if kind != "ANSWER_CHECK" and not str(block.get("learner_text", "")).strip():
            fail("CORE1B_OPEN_QUESTION_MISSING", block.get("block_id", ""))
        learner_text = "\n".join([str(block.get("title", "")), str(block.get("learner_text", "")), *[str(x) for x in block.get("math_lines", [])]]).lower()
        for token in FORBIDDEN_LEARNER_TOKENS:
            if token in learner_text:
                fail("CORE1B_INTERNAL_METADATA_LEAK", token)
        if kind == "CONTROLLED_VARIATION":
            for row in block.get("rows", []):
                if len(row.get("changed_features", [])) > 1:
                    fail("CORE1B_VARIATION_CHANGES_MULTIPLE_CRITICAL_FEATURES", block.get("block_id", ""))
    if not ({"METHOD_COMPARISON", "ERROR_CONTRAST"} & set(kinds)):
        fail("CORE1B_REQUIRED_COMPARISON_MISSING")
    if not ({"COMPLETION", "FADED"} & set(kinds)):
        fail("CORE1B_FADING_OR_COMPLETION_MISSING")
    if "CLOSE_INDEPENDENT" not in kinds:
        fail("CORE1B_CLOSE_INDEPENDENT_MISSING")
    if "ANSWER_CHECK" not in kinds:
        fail("CORE1B_ANSWER_CHECK_MISSING")


def compile_plan(doc: dict) -> dict:
    validate(doc)
    blocks = []
    for source in doc["blocks"]:
        block = copy.deepcopy(source)
        frame = _self_guided_frame(block)
        if frame is not None:
            block["self_guided_frame"] = frame
        blocks.append(block)
    payload = {
        "schema_version": "2.1.0",
        "subject": "MATHEMATICS",
        "delivery_mode": "STATIC",
        "pedagogy_mode": PEDAGOGY_MODE,
        "learner_role": LEARNER_ROLE,
        "product_role": "CORE1B_CONSOLIDATION",
        "governing_question": "Can the learner reconstruct and independently use what was taught?",
        "self_guided_help_sequence": list(HELP_SEQUENCE),
        "source_core1a_authority_ref": doc["core1a_authority_ref"],
        "source_learner_treatment": doc.get("learner_treatment"),
        "difficulty_governance": copy.deepcopy(doc["difficulty_governance"]),
        "capability_refs": list(doc["approved_capability_refs"]),
        "title": doc["title"],
        "blocks": blocks,
        "quality_audit": {
            "status": "PASS",
            "live_runtime_fields": "ABSENT",
            "open_ended_self_guided": True,
            "attempt_precedes_explanation": True,
            "concept_level_help_present": True,
            "difficulty_governance_present": True,
            "comparison_present": True,
            "completion_or_fading_present": True,
            "close_independent_present": True,
            "answer_check_present": True,
        },
    }
    payload["plan_id"] = "MATH-C1B-" + digest(payload)[:16]
    return payload


def render_pdf(plan: dict, path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="C1BTitle", parent=styles["Title"], fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="C1BH2", parent=styles["Heading2"], fontSize=12, leading=15, textColor=colors.HexColor("#17324D"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="C1BBody", parent=styles["BodyText"], fontSize=9.5, leading=13, spaceAfter=5))
    styles.add(ParagraphStyle(name="C1BHelp", parent=styles["BodyText"], fontSize=8.8, leading=12, leftIndent=10, spaceAfter=4))
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=42)
    story = [Paragraph(plan["title"], styles["C1BTitle"]), Paragraph("Open-ended self-guided consolidation", styles["C1BBody"]), Paragraph("Try first. Use only as much help as you need. Check after you have reconstructed the idea.", styles["C1BBody"]), Spacer(1, 8)]
    for block in plan["blocks"]:
        story.append(Paragraph(block["title"], styles["C1BH2"]))
        frame = block.get("self_guided_frame")
        if frame:
            story.append(Paragraph("<b>TRY / PREDICT FIRST</b>", styles["C1BBody"])); story.append(Paragraph(frame["open_question"], styles["C1BBody"])); story.append(Paragraph(f"<b>Focus:</b> {frame['reconstruction_focus']}", styles["C1BHelp"]))
            for label in frame["help_sequence"][:-1]: story.append(Paragraph(f"<b>{label.replace('_',' ').title()}:</b> {frame['help'][label]}", styles["C1BHelp"]))
        elif block.get("learner_text"): story.append(Paragraph(block["learner_text"], styles["C1BBody"]))
        if block.get("math_lines"):
            story.append(Paragraph("<b>Scaffold / worked resolution</b>", styles["C1BBody"])); [story.append(Paragraph(f"<b>{line}</b>", styles["C1BBody"])) for line in block.get("math_lines", [])]
        if block.get("columns") and block.get("rows"):
            table_data = [block["columns"]] + [[str(row.get(k, "")) for k in block["columns"]] for row in block["rows"]]
            t = Table(table_data, repeatRows=1); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EEF5FA")), ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#C7D0D8")), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8), ("VALIGN", (0,0), (-1,-1), "TOP")]))
            story.append(t)
        story.append(Spacer(1, 8))
    doc.build(story)


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--input", required=True); ap.add_argument("--out", required=True); ap.add_argument("--pdf"); ap.add_argument("--domain-registry"); ap.add_argument("--engineering-admission"); ap.add_argument("--governance-out"); args = ap.parse_args()
    source = json.loads(Path(args.input).read_text(encoding="utf-8")); plan = compile_plan(source)
    registry = json.loads(Path(args.domain_registry).read_text(encoding="utf-8")) if args.domain_registry else None
    if registry is not None: validate_registry(registry)
    engineering_custody = load_custody(args.engineering_admission, registry)
    receipt = core1b_receipt(source, plan, registry=registry)
    receipt = stamp_receipt(receipt, engineering_custody)
    Path(args.out).write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    gov_path = Path(args.governance_out) if args.governance_out else Path(args.out).with_suffix(".governance.json")
    write_receipt(receipt, gov_path)
    if args.pdf: render_pdf(plan, Path(args.pdf))
    print(json.dumps({"plan_id":plan["plan_id"],"governance_receipt_ref":receipt["receipt_id"],"governance_release_state":receipt["release_state"],"engineering_custody":custody_summary(engineering_custody)}))


if __name__ == "__main__":
    main()
