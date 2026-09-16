"""Receipts certify reviewed realized content, never a student's mastery."""

from __future__ import annotations

from .contracts import digest, require, strings, text, unique, verify_file


SECTION_KINDS = {"EXPLANATION", "REPRESENTATION", "WORKED", "GUIDED", "FADED", "INDEPENDENT_TASK", "CHECK", "EQUATION", "MISCONCEPTION", "RECONSTRUCTION"}


def validate_manuscript(manuscript: dict, plan: dict, context: dict) -> dict:
    sections = unique(manuscript.get("sections", []), "section_id", "SECTION_ID_DUPLICATE")
    require(bool(sections), "REALIZED_MANUSCRIPT_REQUIRED")
    obligations = {x["obligation_id"] for x in plan["treatments"]}
    covered = set()
    for section in sections.values():
        require(section.get("kind") in SECTION_KINDS, "SECTION_KIND_INVALID")
        text(section.get("content"), "REALIZED_SECTION_CONTENT_REQUIRED")
        refs = strings(section.get("obligation_ids"), "SECTION_OBLIGATION_REQUIRED")
        require(set(refs) <= obligations, "SECTION_UNKNOWN_OBLIGATION")
        strings(section.get("capability_ids"), "SECTION_CAPABILITY_REQUIRED")
        require(set(section["capability_ids"]) <= set(context["capability_ids"]), "SECTION_UNKNOWN_CAPABILITY")
        covered.update(refs)
        if section["kind"] == "REPRESENTATION":
            verify_file(context["artifact_root"], section.get("asset", {}))
            text(section.get("alt_text"), "REPRESENTATION_ALT_TEXT_REQUIRED")
    require(covered == obligations, "MANUSCRIPT_OBLIGATION_COVERAGE")
    require(any(x["kind"] == "RECONSTRUCTION" for x in sections.values()), "MANUSCRIPT_RECONSTRUCTION_REQUIRED")
    for treatment in plan["treatments"]:
        oid = treatment["obligation_id"]
        kinds = {x["kind"] for x in sections.values() if oid in x["obligation_ids"]}
        require("EXPLANATION" in kinds, "OBLIGATION_EXPLANATION_MISSING", oid)
        for planned, realized in (("equation", "EQUATION"), ("representation", "REPRESENTATION"),
                                  ("misconception", "MISCONCEPTION")):
            require(not treatment.get(planned) or realized in kinds, "PLANNED_COMPONENT_NOT_REALIZED", oid)
    return manuscript


def validate_content_review(review: dict, manuscript_packet: dict, actor: str) -> dict:
    require(actor != manuscript_packet["actor"], "MANUSCRIPT_SELF_REVIEW")
    require(review.get("manuscript_digest") == manuscript_packet["digest"], "CONTENT_REVIEW_STALE")
    sections = unique(manuscript_packet["payload"]["sections"], "section_id", "SECTION_ID_DUPLICATE")
    rows = unique(review.get("sections", []), "section_id", "CONTENT_REVIEW_DUPLICATE")
    require(set(rows) == set(sections), "CONTENT_REVIEW_COVERAGE")
    for sid, row in rows.items():
        require(row.get("section_digest") == digest(sections[sid]), "CONTENT_REVIEW_SECTION_CHANGED")
        require(row.get("decision") in {"ACCEPT", "REWORK"}, "CONTENT_REVIEW_DECISION_REQUIRED")
        for field in ("subject_check", "pedagogy_check", "source_basis"):
            text(row.get(field), "CONTENT_REVIEW_REASON_REQUIRED")
        if sections[sid]["kind"] == "REPRESENTATION":
            text(row.get("actual_visual_check"), "ACTUAL_VISUAL_REVIEW_REQUIRED")
    require(review.get("new_semantic_claims") == [], "CONTENT_REVIEW_NEW_CLAIMS")
    return review


def compile_receipts(packets: dict, context: dict) -> dict:
    manuscript = packets["MANUSCRIPT"]
    review = packets["CONTENT_REVIEW"]
    require(all(x["decision"] == "ACCEPT" for x in review["payload"]["sections"]), "TEACHING_CONTENT_REWORK_REQUIRED")
    sections = manuscript["payload"]["sections"]
    rows = []
    for cap in context["capability_ids"]:
        relevant = [x for x in sections if cap in x["capability_ids"]]
        by_kind = {}
        for row in relevant:
            by_kind.setdefault(row["kind"], []).append({"section_id": row["section_id"], "sha256": digest(row)})
        require("EXPLANATION" in by_kind, "CAPABILITY_EXPLANATION_MISSING", cap)
        rows.append({"capability_id": cap, "support": by_kind,
                     "learner_mastery": "NOT_OBSERVED"})
    return {"manuscript_digest": manuscript["digest"], "content_review_digest": review["digest"],
            "request_digest": context["request_digest"], "capabilities": rows,
            "receipt_kind": "REVIEWED_MANUSCRIPT_SUPPORT", "human_release_authorized": False}


def supports(receipts: dict, capabilities: list[str], support_mode: str) -> list[str]:
    rows = {x["capability_id"]: x for x in receipts["capabilities"]}
    needed = {"EXPLANATION", "WORKED"}
    if support_mode == "INDEPENDENT":
        needed |= {"FADED", "INDEPENDENT_TASK", "CHECK"}
    missing = []
    for cap in capabilities:
        kinds = set(rows.get(cap, {}).get("support", {}))
        missing.extend(f"{cap}:{kind}" for kind in sorted(needed - kinds))
    return missing
