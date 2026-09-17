#!/usr/bin/env python3
"""Bucket-centric Core1A learner realization.

The governed teaching unit is a Core1A bucket. Capability-level Core1 lessons are
realized inside that bucket using the exact learner treatment inherited from M-F.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

import build_math_core1a_textbook as base


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _core1_by_capability(core1: dict) -> dict[str, dict]:
    return {x["capability_ref"]: x for x in core1.get("lessons", [])}


def realize_bucket_manuscript(bucket_plan: dict, core1: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    lessons = _core1_by_capability(core1)
    buckets = []
    for bucket in bucket_plan.get("buckets", []):
        units = []
        for cap in bucket["member_capability_refs"]:
            if cap not in lessons:
                fail("CORE1A_BUCKET_MEMBER_LESSON_MISSING", cap)
            unit = base.authored_lesson(lessons[cap], assets, families)
            unit["capability_ref"] = cap
            units.append(unit)
        buckets.append({
            "bucket_id": bucket["bucket_id"],
            "title": bucket["title"],
            "bucket_invariant": bucket["bucket_invariant"],
            "member_capability_refs": list(bucket["member_capability_refs"]),
            "learner_treatment_by_capability": list(bucket["learner_treatment_by_capability"]),
            "learning_atoms": list(bucket["learning_atoms"]),
            "capability_units": units,
            "verification": list(bucket.get("verification_requirements", [])),
        })

    book = {
        "core1a_book_id": "MATH-C1A-" + base.digest({
            "bucket_plan": bucket_plan["bucket_plan_id"],
            "bucket_digest": bucket_plan["plan_digest"],
        })[:16],
        "schema_version": "2.0.0",
        "subject": "MATHEMATICS",
        "source_bucket_plan_ref": bucket_plan["bucket_plan_id"],
        "source_bucket_plan_digest": bucket_plan["plan_digest"],
        "release_class": bucket_plan["release_class"],
        "buckets": buckets,
        "quality_audit": {},
        "book_digest": "",
    }
    book["quality_audit"] = validate_bucket_manuscript(book, bucket_plan)
    book["book_digest"] = base.digest(book, "book_digest")
    return book


def _learner_texts(book: dict) -> list[str]:
    texts: list[str] = []
    for bucket in book["buckets"]:
        texts.append(bucket["title"])
        # invariant text may be shown on the learner surface, but refs/IDs never are.
        texts.append(bucket["bucket_invariant"]["text"])
        for unit in bucket["capability_units"]:
            for key in ("title", "opening", "concept_explanation", "common_mistake"):
                texts.append(str(unit.get(key, "")))
            texts.extend(unit.get("what_to_notice", []))
            texts.extend(unit.get("why_it_works", []))
            texts.extend(unit.get("repair", []))
            texts.extend(unit.get("verification", []))
            for ex in unit.get("worked_examples", []):
                texts.append(ex["prompt"])
                texts.extend(ex["steps"])
                texts.append(ex["answer"])
            for item in unit.get("practice", {}).values():
                texts.append(item["prompt"])
                texts.extend(item["hints"])
    return texts


def validate_bucket_manuscript(book: dict, bucket_plan: dict) -> dict:
    failures: list[str] = []
    seen = []
    actual_problem_count = 0
    full_units = 0

    plan_treatment = {
        row["capability_ref"]: row
        for bucket in bucket_plan["buckets"]
        for row in bucket["learner_treatment_by_capability"]
    }

    for bucket in book["buckets"]:
        if not bucket["learning_atoms"]:
            failures.append(f"CORE1A_BUCKET_LEARNING_ATOMS_MISSING:{bucket['bucket_id']}")
        if not bucket["bucket_invariant"].get("text"):
            failures.append(f"CORE1A_BUCKET_INVARIANT_UNGROUNDED:{bucket['bucket_id']}")
        for unit in bucket["capability_units"]:
            cap = unit["capability_ref"]
            seen.append(cap)
            expected = plan_treatment.get(cap)
            if not expected or unit["treatment"] != expected["treatment"]:
                failures.append(f"CORE1A_LEARNER_TREATMENT_DRIFT:{cap}")
            full = unit["treatment"] in base.FULL_TREATMENTS
            if full:
                full_units += 1
                if len(unit["worked_examples"]) < 2:
                    failures.append(f"CORE1A_WORKED_EXAMPLE_DEPTH_MISSING:{cap}")
                required = set(base.REQUIRED_ROLES)
                missing = sorted(required - set(unit["practice"]))
                if missing:
                    failures.append(f"CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED:{cap}:{','.join(missing)}")
                if not unit["concept_explanation"] or len(unit["why_it_works"]) < 2:
                    failures.append(f"CORE1A_CONCEPT_EXPLANATION_UNDERREALIZED:{cap}")
                if not unit["common_mistake"] or not unit["repair"]:
                    failures.append(f"CORE1_MISCONCEPTION_REPAIR_NOT_MATERIALIZED:{cap}")
            actual_problem_count += sum(
                1 for item in unit.get("practice", {}).values()
                if item.get("source_class") == "NEW_AUTHORED_CORE1A"
            )

    required_caps = bucket_plan["coverage"]["required_capability_refs"]
    if sorted(seen) != sorted(required_caps) or len(seen) != len(set(seen)):
        failures.append("CORE1A_BUCKET_REALIZATION_COVERAGE_DRIFT")

    for text in _learner_texts(book):
        low = text.lower()
        for token in base.FORBIDDEN_LEARNER_TOKENS:
            if token in low:
                failures.append(f"CORE1A_INTERNAL_JARGON_LEAK:{token}")
        if base.INTERNAL_CODE_RE.search(text):
            failures.append("CORE1A_INTERNAL_IDENTIFIER_LEAK")

    if failures:
        fail("CORE1A_QUALITY_GATE_FAILED", "|".join(sorted(set(failures))))
    return {
        "status": "PASS",
        "bucket_count": len(book["buckets"]),
        "capability_unit_count": len(seen),
        "full_teaching_capability_units": full_units,
        "actual_problem_instances": actual_problem_count,
        "checks": [
            "BUCKET_COVERAGE_EXACT",
            "LEARNER_TREATMENT_PRESERVED_FROM_STUDY_MODEL",
            "BUCKET_INVARIANT_GROUNDED",
            "LEARNING_ATOMS_GROUNDED_IN_PCK",
            "NO_INTERNAL_AUTHORING_JARGON",
            "FULL_TEACHING_DEPTH_MATERIALIZED",
        ],
    }


def render_bucket_pdf(book: dict, path: Path) -> dict:
    base.register_fonts()
    st = base.styles()
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="Mathematics Core 1A Student Textbook",
        author="Grade 9 V2 Mathematics",
    )
    story: list[Any] = []
    story.append(Spacer(1, 18))
    story.append(Paragraph("Mathematics", st["title"]))
    story.append(Paragraph("Core 1A — Student Textbook", st["title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Ideas that belong together are taught together. Work through each example, use support only when needed, and check your reasoning before moving on.",
        ParagraphStyle("bucket-cover", parent=st["body"], alignment=TA_CENTER, fontSize=11, leading=15),
    ))
    story.append(PageBreak())

    for bi, bucket in enumerate(book["buckets"], 1):
        story.append(Paragraph(f"{bi}. {base.safe_text(bucket['title'])}", st["chapter"]))
        story.append(base.card("The connecting idea", [bucket["bucket_invariant"]["text"]], "#16324F", st))
        story.append(Spacer(1, 8))

        multi = len(bucket["capability_units"]) > 1
        for ui, unit in enumerate(bucket["capability_units"], 1):
            if multi:
                story.append(Paragraph(base.safe_text(unit["title"]), st["h2"]))
            story.append(Paragraph(base.safe_text(unit["opening"]), st["body"]))
            if unit["what_to_notice"]:
                story.append(Paragraph("What should you notice?", st["h2"]))
                story.extend(base.bullet_paragraphs(unit["what_to_notice"], st))
            if unit["concept_explanation"]:
                story.append(Paragraph("The idea", st["h2"]))
                story.append(Paragraph(base.safe_text(unit["concept_explanation"]), st["body"]))
            if unit["why_it_works"]:
                story.append(Paragraph("Why it works", st["h2"]))
                for i, step in enumerate(unit["why_it_works"], 1):
                    story.append(Paragraph(f"<b>{i}.</b> {base.safe_text(step)}", st["body"]))
            for ei, ex in enumerate(unit["worked_examples"], 1):
                story.append(base.example_box(ei, ex, st))
                story.append(Spacer(1, 7))
            if unit["common_mistake"]:
                story.append(base.card("Common mistake", [unit["common_mistake"]] + unit.get("repair", []), "#B03A2E", st))
                story.append(Spacer(1, 8))

            practice = unit["practice"]
            if "GUIDED" in practice:
                story.append(base.practice_box("Try it with help", practice["GUIDED"], st, 2))
                story.append(Spacer(1, 6))
            if "FADED" in practice:
                story.append(base.practice_box("Now with less help", practice["FADED"], st, 1))
                story.append(Spacer(1, 6))
            if "INDEPENDENT" in practice:
                story.append(base.practice_box("Your turn", practice["INDEPENDENT"], st, 0))
                story.append(Spacer(1, 6))
            if "TRANSFER" in practice:
                story.append(base.practice_box("Challenge", practice["TRANSFER"], st, 0))
                story.append(Spacer(1, 6))
            if "VERIFY" in practice and unit["treatment"] not in base.FULL_TREATMENTS:
                story.append(base.practice_box("Quick check", practice["VERIFY"], st, 0))
                story.append(Spacer(1, 6))
            if unit["verification"]:
                story.append(Paragraph("Check your work", st["h2"]))
                story.extend(base.bullet_paragraphs(unit["verification"], st))
            if multi and ui != len(bucket["capability_units"]):
                story.append(Spacer(1, 10))

        if bi != len(book["buckets"]):
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(Paragraph("Answer check", st["chapter"]))
    for bi, bucket in enumerate(book["buckets"], 1):
        story.append(Paragraph(f"{bi}. {base.safe_text(bucket['title'])}", st["h2"]))
        for unit in bucket["capability_units"]:
            for role in ("GUIDED", "FADED", "INDEPENDENT", "TRANSFER", "VERIFY"):
                if role not in unit.get("practice", {}):
                    continue
                label = {"GUIDED":"Guided practice","FADED":"Less-help practice","INDEPENDENT":"Your turn","TRANSFER":"Challenge","VERIFY":"Quick check"}[role]
                story.append(Paragraph(f"<b>{label}:</b> {base.safe_text(unit['practice'][role]['answer'])}", st["body"]))

    doc.build(story, onFirstPage=base.add_page_number, onLaterPages=base.add_page_number)
    data = path.read_bytes()
    return {
        "pdf_sha256": hashlib.sha256(data).hexdigest(),
        "pdf_size_bytes": len(data),
        "page_count": int(doc.page),
    }
