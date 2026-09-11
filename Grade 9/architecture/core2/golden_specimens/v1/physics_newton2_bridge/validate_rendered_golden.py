#!/usr/bin/env python3
"""Reopen the exact mature Physics golden and verify learning semantics survived render."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pymupdf as fitz


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--golden", type=Path, required=True)
    args = ap.parse_args()

    d, p, golden = args.dir, args.prefix, args.golden
    errors: list[str] = []
    pdf_path = d / f"{p}_Core2_Study_Guide.pdf"
    page_map_path = d / f"{p}_Core2_Physical_Page_Map.json"
    manifest_path = d / f"{p}_Core2_Publication_Manifest.json"
    audit_path = d / f"{p}_Core2_Publication_Audit.json"
    for path in (pdf_path, page_map_path, manifest_path, audit_path):
        if not path.exists():
            errors.append(f"missing rendered golden artifact: {path.name}")
    if errors:
        print("PHYSICS_NEWTON2_RENDERED_GOLDEN = FAIL")
        for error in errors:
            print("- " + error)
        return 1

    design = load(golden / "learning_design.json")
    study = load(golden / "study_guide.json")
    structure = load(golden / "publication_structure.json")
    page_map = load(page_map_path)
    manifest = load(manifest_path)
    audit = load(audit_path)

    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    doc.close()
    text = norm("\n".join(pages))

    required_learner_cues = (
        "Newton's Second Law",
        "Start with the trolley",
        "NOTICE",
        "Say the model in words",
        "WORKED",
        "GUIDED 1",
        "GUIDED 2",
        "INDEPENDENT TRANSFER",
        "RETRIEVAL CHECK",
        "MISCONCEPTION REPAIR",
        "F_net = m a",
        "Appendix A",
        "Appendix B",
        "Appendix C",
    )
    for cue in required_learner_cues:
        if cue not in text:
            errors.append(f"final PDF lost required learner cue: {cue}")

    forbidden_machine_surface = (
        "R-PHY-LM-",
        "RREP-PHY-",
        "RB-G9-PHY-",
        "PP-RB-G9-PHY-",
        "SEC-01",
        "SEC-02",
        "representation requirement",
        "Layout relation",
    )
    for marker in forbidden_machine_surface:
        if marker in text:
            errors.append(f"machine/internal identifier leaked into learner PDF: {marker}")

    generic_replay_phrases = (
        "Start from the given situation or symbolic instance",
        "Use the same model with one support removed",
        "Apply the verified model without step prompts",
        "Name the trigger, first move, and one nearby failure case",
    )
    for phrase in generic_replay_phrases:
        if phrase in text:
            errors.append(f"generic replay prose leaked into mature PDF: {phrase}")

    appendix_a = text.find("Appendix A")
    appendix_b = text.find("Appendix B")
    appendix_c = text.find("Appendix C")
    if not (0 <= appendix_a < appendix_b < appendix_c):
        errors.append("final PDF does not preserve Appendix A -> B -> C order")
    q1_solution = text.find("Q1 solution")
    if q1_solution >= 0 and appendix_b >= 0 and q1_solution < appendix_b:
        errors.append("Appendix A leaks Q1 solution before optional help/solutions")
    for q in ("Q1", "Q2", "Q3"):
        positions = [text.find(f"{q} H{tier}") for tier in (1, 2, 3)]
        sol = text.find(f"{q} solution")
        if any(pos < 0 for pos in positions) or sol < 0 or not (positions[0] < positions[1] < positions[2] < sol):
            errors.append(f"{q}: final PDF does not preserve H1 -> H2 -> H3 -> complete solution order")

    required_caps = {
        cap["capability_id"]
        for unit in design["learning_units"]
        for cap in unit["learner_capabilities"]
        if cap["required"]
    }
    physically_bound_caps = {
        ref
        for placement in page_map["content_placements"]
        for ref in placement.get("learning_design_refs", [])
    }
    missing_caps = sorted(required_caps - physically_bound_caps)
    if missing_caps:
        errors.append("required LearningDesign capabilities never reach physical main-section placement: " + ", ".join(missing_caps))

    main_material = {
        item["item_id"]
        for section in study["main_sections"]
        for item in section["items"]
        if item["traceability_class"] == "MATERIAL"
    }
    placed = {row["content_ref"] for row in page_map["content_placements"]}
    if main_material - placed:
        errors.append("rendered golden lost main MATERIAL content refs: " + ", ".join(sorted(main_material - placed)))

    intent_ids = {row["page_intent_id"] for row in page_map["page_intents"]}
    expected_intents = {row["page_intent_id"] for row in structure["study_guide"]["page_intents"]}
    if intent_ids != expected_intents:
        errors.append("rendered PhysicalPageMap does not cover the exact authored page-intent set")
    if any(row.get("orphan_continuation") for row in page_map["page_metrics"]):
        errors.append("rendered golden contains an orphan continuation page")
    if any(row.get("underfill_disposition") == "PATHOLOGICAL" for row in page_map["page_metrics"]):
        errors.append("rendered golden contains pathological underfill")

    roles = [row["role"] for row in manifest["artifacts"]]
    for role in ("LEARNING_DESIGN", "STUDY_GUIDE_MODEL", "PUBLICATION_STRUCTURE", "PHYSICAL_PAGE_MAP", "STUDY_GUIDE_PDF", "PUBLICATION_AUDIT"):
        if roles.count(role) != 1:
            errors.append(f"manifest must contain exactly one {role}; found {roles.count(role)}")

    if audit.get("gates", {}).get("physical_page_custody") is not True:
        errors.append("physical_page_custody release gate is not true")
    if audit.get("gates", {}).get("physical_page_morphology") is not True:
        errors.append("physical_page_morphology release gate is not true")
    if audit.get("human_visual_review", {}).get("status") != "PENDING":
        errors.append("golden must not claim human visual approval before an exact-artifact review")
    if audit.get("release_state") == "HUMAN_REVIEW_PASS":
        errors.append("golden prematurely claims human review PASS")

    if design["exam_bridge"]["question_families"]:
        errors.append("rendered golden invents exam family evidence not present in scoped Core1")

    if errors:
        print("PHYSICS_NEWTON2_RENDERED_GOLDEN = FAIL")
        for error in errors:
            print("- " + error)
        return 1

    print(f"PHYSICS_NEWTON2_RENDERED_GOLDEN_PAGES = {len(pages)}")
    print("LEARNING_DESIGN_TO_PHYSICAL_PAGE_CUSTODY = PASS")
    print("LEARNER_SURFACE_NO_MACHINE_ID_LEAKAGE = PASS")
    print("LEARNER_SURFACE_NO_GENERIC_REPLAY_PROSE = PASS")
    print("ATTEMPT_HINT_SOLUTION_ORDER = PASS")
    print("EXACT_ARTIFACT_PR156_STYLE_CUES = PASS")
    print("HUMAN_REVIEW_CLAIM = PENDING")
    print("PHYSICS_NEWTON2_RENDERED_GOLDEN = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
