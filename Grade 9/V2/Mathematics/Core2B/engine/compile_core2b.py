#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
    payload = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "delivery_mode": "STATIC",
        "product_role": "CORE2B_TRANSFER",
        "source_core2a_authority_ref": doc["core2a_authority_ref"],
        "purpose": doc["purpose"],
        "compile_ceiling": doc["max_demand_level"],
        "capability_refs": list(doc["approved_capability_refs"]),
        "title": doc["title"],
        "items": ordered,
        "quality_audit": {
            "status": "PASS",
            "live_runtime_fields": "ABSENT",
            "all_items_core2a_legal": True,
            "ceiling_respected": True,
            "discrimination_labels_hidden": True,
        },
    }
    payload["plan_id"] = "MATH-C2B-" + digest(payload)[:16]
    return payload


def render_pdf(plan: dict, path: Path) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="C2BTitle", parent=styles["Title"], fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="C2BH2", parent=styles["Heading2"], fontSize=11.5, leading=14, textColor=colors.HexColor("#17324D"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="C2BBody", parent=styles["BodyText"], fontSize=9.5, leading=13, spaceAfter=5))
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=42)
    story = [
        Paragraph(plan["title"], styles["C2BTitle"]),
        Paragraph(f"{plan['purpose'].title()} transfer workbook", styles["C2BBody"]),
        Spacer(1, 8),
    ]
    for i, item in enumerate(plan["items"], 1):
        story.append(Paragraph(f"{i}. {item.get('learner_label', 'Try it first')}", styles["C2BH2"]))
        story.append(Paragraph(item["stem"], styles["C2BBody"]))
        for support in item.get("support", []):
            story.append(Paragraph(support, styles["C2BBody"]))
        if item.get("answer_check"):
            story.append(Paragraph(f"<b>Answer check:</b> {item['answer_check']}", styles["C2BBody"]))
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
