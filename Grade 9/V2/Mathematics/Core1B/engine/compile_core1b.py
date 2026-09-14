#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

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
                fail("CORE1B_LIVE_RUNTIME_FIELD_FORBIDDEN", f"{path}.{key}")
            _reject_live_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _reject_live_fields(child, f"{path}[{i}]")


def validate(doc: dict) -> None:
    _reject_live_fields(doc)
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
        learner_text = "\n".join([
            str(block.get("title", "")),
            str(block.get("learner_text", "")),
            *[str(x) for x in block.get("math_lines", [])],
        ]).lower()
        for token in FORBIDDEN_LEARNER_TOKENS:
            if token in learner_text:
                fail("CORE1B_INTERNAL_METADATA_LEAK", token)
        if kind == "CONTROLLED_VARIATION":
            for row in block.get("rows", []):
                changed = row.get("changed_features", [])
                if len(changed) > 1:
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
    payload = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "delivery_mode": "STATIC",
        "product_role": "CORE1B_CONSOLIDATION",
        "source_core1a_authority_ref": doc["core1a_authority_ref"],
        "source_learner_treatment": doc.get("learner_treatment"),
        "capability_refs": list(doc["approved_capability_refs"]),
        "title": doc["title"],
        "blocks": doc["blocks"],
        "quality_audit": {
            "status": "PASS",
            "live_runtime_fields": "ABSENT",
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
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="C1BTitle", parent=styles["Title"], fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="C1BH2", parent=styles["Heading2"], fontSize=12, leading=15, textColor=colors.HexColor("#17324D"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="C1BBody", parent=styles["BodyText"], fontSize=9.5, leading=13, spaceAfter=5))
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=42)
    story = [Paragraph(plan["title"], styles["C1BTitle"]), Paragraph("Static consolidation workbook", styles["C1BBody"]), Spacer(1, 8)]
    for block in plan["blocks"]:
        story.append(Paragraph(block["title"], styles["C1BH2"]))
        if block.get("learner_text"):
            story.append(Paragraph(block["learner_text"], styles["C1BBody"]))
        for line in block.get("math_lines", []):
            story.append(Paragraph(f"<b>{line}</b>", styles["C1BBody"]))
        if block.get("columns") and block.get("rows"):
            table_data = [block["columns"]] + [[str(row.get(k, "")) for k in block["columns"]] for row in block["rows"]]
            t = Table(table_data, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EEF5FA")),
                ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#C7D0D8")),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE", (0,0), (-1,-1), 8),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
            ]))
            story.append(t)
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
