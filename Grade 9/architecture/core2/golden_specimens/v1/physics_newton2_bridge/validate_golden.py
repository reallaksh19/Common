#!/usr/bin/env python3
"""Semantic and custody checks for the first mature Core2 Physics golden specimen.

This is intentionally stricter than schema validity.  It encodes the qualities
we want a cold-start authoring agent to imitate, while leaving subject/pedagogy
human approval explicitly separate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE2 = ROOT.parents[2]
CONTRACTS = CORE2 / "contracts" / "v1"
SCRIPTS = ROOT.parents[4] / "skills" / "grade9-core2-publisher" / "scripts"
sys.path.insert(0, str(CONTRACTS))
sys.path.insert(0, str(SCRIPTS))

import check_learning_design  # noqa: E402
import run_core2_legacy as legacy  # noqa: E402


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def material_items(study: dict):
    for section in study["main_sections"]:
        for item in section["items"]:
            if item["traceability_class"] == "MATERIAL":
                yield item
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        for item in study[key]["items"]:
            if item["traceability_class"] == "MATERIAL":
                yield item


def main() -> int:
    errors: list[str] = []
    design = load("learning_design.json")
    study = load("study_guide.json")
    structure = load("publication_structure.json")

    errors.extend("LearningDesign schema: " + e for e in check_learning_design.validate_schema(design))
    errors.extend("LearningDesign semantic: " + e for e in check_learning_design.validate_semantics(design))

    for schema_name, obj in (
        ("study-guide.schema.json", study),
        ("publication-structure.schema.json", structure),
    ):
        try:
            legacy.validate_schema(schema_name, obj, CONTRACTS)
        except SystemExit as exc:
            errors.append(f"{schema_name} rejected with exit {exc.code}")

    required_caps = {
        cap["capability_id"]
        for unit in design["learning_units"]
        for cap in unit["learner_capabilities"]
        if cap["required"]
    }
    used_caps = {
        ref
        for item in material_items(study)
        for ref in item.get("learning_design_refs", [])
    }
    if required_caps - used_caps:
        errors.append("required capabilities missing MATERIAL implementation: " + ", ".join(sorted(required_caps - used_caps)))
    if used_caps - {
        cap["capability_id"]
        for unit in design["learning_units"]
        for cap in unit["learner_capabilities"]
    }:
        errors.append("StudyGuide contains unknown learning_design_refs")

    main_material = {
        item["item_id"]
        for section in study["main_sections"]
        for item in section["items"]
        if item["traceability_class"] == "MATERIAL"
    }
    arc_refs = [
        ref
        for unit in structure["study_guide"]["learning_units"]
        for step in unit["arc_steps"]
        for ref in step["content_refs"]
    ]
    page_refs = [
        ref
        for intent in structure["study_guide"]["page_intents"]
        for ref in intent["content_refs"]
    ]
    if len(arc_refs) != len(set(arc_refs)):
        errors.append("a learner item is assigned to more than one arc role")
    if set(arc_refs) != main_material:
        errors.append("main-section MATERIAL set does not exactly equal structured arc content")
    if page_refs != arc_refs:
        errors.append("page-intent order does not exactly equal arc-step order")

    all_text = "\n".join(item["content"] for section in study["main_sections"] for item in section["items"])
    generic_replay_phrases = (
        "Start from the given situation or symbolic instance",
        "Use the same model with one support removed",
        "Apply the verified model without step prompts",
        "Name the trigger, first move, and one nearby failure case",
    )
    for phrase in generic_replay_phrases:
        if phrase in all_text:
            errors.append(f"generic engineering-replay prose leaked into mature golden: {phrase!r}")

    formal = next((item for section in study["main_sections"] for item in section["items"] if item["item_id"] == "ITEM-PHY-N2-REL-FORMAL"), None)
    if not formal:
        errors.append("missing Newton-II formal reconstruction item")
    else:
        formal_text = formal["content"].lower()
        for marker in ("f_net = m a", "net force", "selected system", "mass", "acceleration", "newtons"):
            if marker not in formal_text:
                errors.append(f"NO_NAKED_FORMALISM failed; formal item missing {marker!r}")

    repair = next((item for section in study["main_sections"] for item in section["items"] if item["item_id"] == "ITEM-PHY-N2-REL-MIS"), None)
    if not repair or not all(term in repair["content"].lower() for term in ("applied force", "net force", "friction", "3 m/s")):
        errors.append("misconception repair must diagnose applied-force-as-net-force and execute the corrected model")

    for unit in design["learning_units"]:
        ids = unit["practice_progression"]
        expected = {ids["worked_example_id"], ids["guided_1_id"], ids["guided_2_id"], ids["independent_id"]}
        present = {item["item_id"] for section in study["main_sections"] for item in section["items"]}
        if not expected <= present:
            errors.append(f"{unit['unit_id']}: declared fading task IDs are not all authored")

    g1 = next(item for section in study["main_sections"] for item in section["items"] if item["item_id"] == "ITEM-PHY-N2-REL-G1")
    g2 = next(item for section in study["main_sections"] for item in section["items"] if item["item_id"] == "ITEM-PHY-N2-REL-G2")
    independent = next(item for section in study["main_sections"] for item in section["items"] if item["item_id"] == "ITEM-PHY-N2-REL-IND")
    if "first step is supplied" not in g1["content"].lower():
        errors.append("guided_1 does not visibly implement its first-step support")
    if "no equation or first step is given" not in g2["content"].lower():
        errors.append("guided_2 does not visibly remove first-step support")
    if "without a supplied force diagram or first-step cue" not in independent["content"].lower():
        errors.append("independent transfer does not visibly remove representation/first-step support")
    if not all(term in independent["content"].lower() for term in ("unknown", "resisting force", "justify")):
        errors.append("independent transfer is not reverse/model-selection reasoning")

    if design["exam_bridge"]["question_families"]:
        errors.append("golden invents exam question families not present in frozen Core1 ExamDemandProfile")
    for unit in design["learning_units"]:
        if unit["transfer_design"].get("question_family_refs"):
            errors.append(f"{unit['unit_id']}: transfer claims an unsupported exam question family")

    appendix_b = {item["item_id"]: item for item in study["appendix_B"]["items"]}
    for q in ("Q1", "Q2", "Q3"):
        for tier in ("H1", "H2", "H3"):
            if f"B-PHY-N2-{q}-{tier}" not in appendix_b:
                errors.append(f"Appendix B missing {q} {tier}")
        if f"B-PHY-N2-{q}-SOL" not in appendix_b:
            errors.append(f"Appendix B missing {q} complete solution")

    if study["appendix_C"]["answer_leakage_detected"] is not False or not study["appendix_C"]["standalone_usable"]:
        errors.append("Appendix C standalone/no-answer-leakage contract is not explicit")

    if errors:
        print("PHYSICS_NEWTON2_MATURE_GOLDEN = FAIL")
        for error in errors:
            print("- " + error)
        return 1

    print("PHYSICS_NEWTON2_MATURE_GOLDEN_SCHEMA = PASS")
    print("LEARNING_DESIGN_TO_MATERIAL_COVERAGE = PASS")
    print("PR156_SRU_NO_NAKED_FORMALISM = PASS")
    print("PR156_SRU_MISCONCEPTION_REPAIR = PASS")
    print("CONCRETE_SUPPORT_FADING = PASS")
    print("NON_ISOMORPHIC_REVERSE_TRANSFER = PASS")
    print("UNSUPPORTED_EXAM_FAMILY_INVENTION = PASS")
    print("APPENDIX_A_B_C_PEDAGOGY = PASS")
    print("PHYSICS_NEWTON2_MATURE_GOLDEN = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
