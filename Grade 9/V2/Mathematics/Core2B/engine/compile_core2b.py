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

from producer_governance import core2b_receipt
from emit_stage_governance import write_receipt
from engineering_product_custody import load_custody, stamp_receipt, custody_summary
from validate_canonical_domain_registry import validate_registry

LEVELS = [
    "M0_DIRECT", "M1_CONTROLLED_VARIATION", "M2_REPRESENTATION_TRANSFER",
    "M3_INVERSE_TARGET", "M4_HIDDEN_STRUCTURE", "M5_METHOD_DISCRIMINATION",
    "M6_FAMILY_DISCRIMINATION", "M7_MULTI_STEP_SYNTHESIS", "M8_MIXED_COMPETITIVE",
]
SUPPORT_MODES = {"FOUNDATION_HIGH_SUPPORT", "GUIDED", "STANDARD", "CHALLENGE_MINIMAL"}
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


def _validate_calibration(doc: dict) -> None:
    cal = doc.get("generation_calibration")
    if not cal:
        fail("CORE2B_GENERATION_CALIBRATION_MISSING")
    if cal.get("support_mode") not in SUPPORT_MODES:
        fail("CORE2B_SUPPORT_MODE_INVALID", str(cal.get("support_mode")))
    basis = cal.get("calibration_basis") or {}
    btype = basis.get("type")
    if btype == "KNOWLEDGE_PERCENT":
        for key in ("learner_knowledge_percent", "knowledge_source_ref", "calibration_policy_ref"):
            if basis.get(key) in (None, ""):
                fail("CORE2B_KNOWLEDGE_BINDING_INCOMPLETE", key)
        rows = basis.get("capability_knowledge") or []
        if not rows:
            fail("CORE2B_CAPABILITY_KNOWLEDGE_REQUIRED")
        refs = [x.get("capability_ref") for x in rows]
        if len(refs) != len(set(refs)):
            fail("CORE2B_CAPABILITY_KNOWLEDGE_DUPLICATE")
    elif btype == "OWNER_OVERRIDE":
        if not basis.get("owner_ref") or not basis.get("reason"):
            fail("CORE2B_OWNER_OVERRIDE_INCOMPLETE")
    else:
        fail("CORE2B_CALIBRATION_BASIS_INVALID", str(btype))


def _validate_custody(item: dict) -> None:
    for key in ("answer_contract_ref", "learner_source_label", "source_ref", "source_relation", "origin"):
        if item.get(key) in (None, ""):
            fail("CORE2B_QUESTION_CUSTODY_INCOMPLETE", f"{item.get('item_id')}:{key}")
    if not str(item.get("answer_check", "")).strip():
        fail("CORE2B_QUESTION_ANSWER_MISSING", str(item.get("item_id")))
    origin = item["origin"]
    relation = item["source_relation"]
    if origin == "SOURCE_CORE2":
        if not item.get("source_question_no") or relation != "EXACT_SOURCE":
            fail("CORE2B_SOURCE_IDENTITY_BROKEN", item["item_id"])
        if item.get("parent_question_refs"):
            fail("CORE2B_SOURCE_PARENT_VARIANT_FORBIDDEN", item["item_id"])
    elif origin == "GENERATED_ORIGINAL":
        if item.get("source_question_no") is not None or relation == "EXACT_SOURCE":
            fail("CORE2B_GENERATED_MASQUERADES_AS_SOURCE", item["item_id"])
        if relation in {"FADING_ANCHOR", "STRUCTURAL_SIBLING", "FAR_TRANSFER_SIBLING"} and not item.get("parent_question_refs"):
            fail("CORE2B_GENERATED_LINEAGE_MISSING", item["item_id"])
    else:
        fail("CORE2B_QUESTION_ORIGIN_INVALID", str(origin))
    if item.get("official_past_question_claim") and not item.get("verified_official_source_ref"):
        fail("CORE2B_UNVERIFIED_OFFICIAL_CLAIM", item["item_id"])


def validate(doc: dict) -> None:
    _reject_live_fields(doc)
    _validate_calibration(doc)
    if not doc.get("core2a_authority_ref") or not doc.get("core2a_legal_item_ids"):
        fail("CORE2B_CORE2A_AUTHORITY_MISSING")
    ceiling = doc.get("max_demand_level")
    if ceiling not in LEVELS:
        fail("CORE2B_COMPILE_CEILING_INVALID", str(ceiling))
    ceiling_i = LEVELS.index(ceiling)
    legal = set(doc["core2a_legal_item_ids"])
    approved = set(doc.get("approved_capability_refs", []))
    basis = doc["generation_calibration"]["calibration_basis"]
    known_caps = {x["capability_ref"] for x in basis.get("capability_knowledge", [])} if basis["type"] == "KNOWLEDGE_PERCENT" else approved
    items = doc.get("items", [])
    if not items:
        fail("CORE2B_EMPTY_SELECTION")
    seen = set()
    for item in items:
        item_id = item.get("item_id")
        if item_id in seen:
            fail("CORE2B_DUPLICATE_ITEM_ID", str(item_id))
        seen.add(item_id)
        parent = item.get("core2a_item_ref")
        if parent not in legal:
            fail("CORE2B_ITEM_NOT_CORE2A_LEGAL", str(parent))
        level = item.get("demand_level")
        if level not in LEVELS:
            fail("CORE2B_DEMAND_LEVEL_INVALID", str(level))
        if LEVELS.index(level) > ceiling_i:
            fail("CORE2B_TRANSFER_EXCEEDS_COMPILE_CEILING", f"{item_id}:{level}>{ceiling}")
        refs = set(item.get("capability_refs", []))
        if not refs or not refs.issubset(approved):
            fail("CORE2B_UNAPPROVED_CAPABILITY_REF", ",".join(sorted(refs - approved)))
        if basis["type"] == "KNOWLEDGE_PERCENT" and not refs.issubset(known_caps):
            fail("CORE2B_ITEM_CAPABILITY_KNOWLEDGE_MISSING", ",".join(sorted(refs - known_caps)))
        if not str(item.get("stem", "")).strip():
            fail("CORE2B_OPEN_QUESTION_MISSING", str(item_id))
        if LEVELS.index(level) >= LEVELS.index("M5_METHOD_DISCRIMINATION") and item.get("family_label_visible"):
            fail("CORE2B_FAMILY_LABEL_LEAK", item_id)
        _validate_custody(item)
        learner_text = "\n".join([str(item.get("stem", "")), *[str(x) for x in item.get("support", [])], str(item.get("answer_check", ""))]).lower()
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
        "schema_version": "2.1.0",
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
        "generation_calibration": copy.deepcopy(doc["generation_calibration"]),
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
            "learner_calibration_bound": True,
            "question_custody_complete": True,
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
    story = [Paragraph(plan["title"], styles["C2BTitle"]), Paragraph(f"{plan['purpose'].title()} open-ended transfer workbook", styles["C2BBody"]), Paragraph("Attempt before using help. The method/family may be deliberately hidden.", styles["C2BBody"]), Spacer(1, 8)]
    for i, item in enumerate(plan["items"], 1):
        story.append(Paragraph(f"{i}. {item.get('learner_label', 'Try it first')}", styles["C2BH2"])); story.append(Paragraph("<b>ATTEMPT FIRST</b>", styles["C2BBody"])); story.append(Paragraph(item["stem"], styles["C2BBody"]))
        story.append(Paragraph(f"<b>Source:</b> {item['learner_source_label']}", styles["C2BHelp"]))
        frame = item["self_guided_frame"]; story.append(Paragraph(f"<b>Transfer focus:</b> {frame['transfer_focus']}", styles["C2BHelp"]))
        for label in frame["help_sequence"][:-1]: story.append(Paragraph(f"<b>{label.replace('_',' ').title()}:</b> {frame['help'][label]}", styles["C2BHelp"]))
        for support in frame.get("authored_support", []): story.append(Paragraph(f"<b>Authored support:</b> {support}", styles["C2BHelp"]))
        story.append(Paragraph(f"<b>Answer + verification:</b> {item['answer_check']}", styles["C2BBody"])); story.append(Spacer(1, 8))
    doc.build(story)


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--input", required=True); ap.add_argument("--out", required=True); ap.add_argument("--pdf"); ap.add_argument("--domain-registry"); ap.add_argument("--engineering-admission"); ap.add_argument("--governance-out"); args = ap.parse_args()
    source = json.loads(Path(args.input).read_text(encoding="utf-8")); plan = compile_plan(source)
    registry = json.loads(Path(args.domain_registry).read_text(encoding="utf-8")) if args.domain_registry else None
    if registry is not None: validate_registry(registry)
    engineering_custody = load_custody(args.engineering_admission, registry)
    receipt = core2b_receipt(source, plan, registry=registry)
    receipt = stamp_receipt(receipt, engineering_custody)
    Path(args.out).write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    gov_path = Path(args.governance_out) if args.governance_out else Path(args.out).with_suffix(".governance.json"); write_receipt(receipt, gov_path)
    if args.pdf: render_pdf(plan, Path(args.pdf))
    print(json.dumps({"plan_id":plan["plan_id"],"governance_receipt_ref":receipt["receipt_id"],"governance_release_state":receipt["release_state"],"engineering_custody":custody_summary(engineering_custody)}))


if __name__ == "__main__":
    main()
