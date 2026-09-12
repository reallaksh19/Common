#!/usr/bin/env python3
"""Validate the Primary Math V2 authoring/concept engine cold-start contract."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from Primary.V2.Mathematics.CoreSkills.engine.author import AuthoringError, author

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "authoring" / "cold_start_cases.json"
AUTHOR_SOURCE = ROOT / "engine" / "author.py"


def fail(message: str) -> None:
    raise SystemExit(f"Primary Math V2 authoring validation failed: {message}")


def expect_error(payload, code: str) -> None:
    try:
        author(payload)
    except AuthoringError as exc:
        if exc.code != code:
            fail(f"expected {code}, got {exc.code}: {exc.message}")
        return
    fail(f"expected {code}, but authoring succeeded")


def validate_positive_cases() -> None:
    corpus = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if len(corpus.get("cases", [])) != 4:
        fail("cold-start corpus must contain exactly four input-combination cases")

    seen = set()
    for case in corpus["cases"]:
        case_id = case["case_id"]
        seen.add(case_id)
        result = author(case["input"])
        expected = case["expect"]

        skill_model = result["skill_model"]
        concepts = skill_model["concepts"]
        if not concepts:
            fail(f"{case_id}: no concepts")
        if any(c.get("universal_grade_claim") for c in concepts):
            fail(f"{case_id}: authoring promoted active scope to universal grade truth")
        if len(skill_model.get("work_evidence_refs", [])) != expected["work_evidence_count"]:
            fail(f"{case_id}: work evidence count mismatch")
        if len(result.get("diagnostic_objects", [])) != expected["diagnostic_count"]:
            fail(f"{case_id}: diagnostic count mismatch")
        if not any(expected["capability"] in c.get("capability_refs", []) for c in concepts):
            fail(f"{case_id}: expected capability {expected['capability']} missing")

        modes = set(result["authoring_trace"]["concept_modes"].values())
        if expected["concept_mode"] not in modes:
            fail(f"{case_id}: expected mode {expected['concept_mode']}, got {sorted(modes)}")

        if not result["core1_plan"]["modules"] or not result["core2_plan"]["modules"]:
            fail(f"{case_id}: Core1/Core2 plan empty")
        if not result["representation_plan"]["representations"]:
            fail(f"{case_id}: representation plan empty")
        for rep in result["representation_plan"]["representations"]:
            if not rep.get("validator_refs"):
                fail(f"{case_id}: representation without validator refs")

        core1_ids = {m["module_id"] for m in result["core1_plan"]["modules"]}
        for module in result["core2_plan"]["modules"]:
            if module.get("core1_module_ref") not in core1_ids:
                fail(f"{case_id}: Core2 module lacks stable Core1 semantic link")

        if case_id == "QUESTION_ONLY":
            if skill_model.get("work_evidence_refs") or result.get("diagnostic_objects"):
                fail("question-only case fabricated learner work/diagnosis")
        if case_id == "QUESTION_PLUS_TOPIC_HINTS":
            # Topic hints may label, but may not add or remove canonical capability truth.
            observed = set(case["input"]["question_set"]["questions"][0]["evidence"]["capability_refs"])
            planned = set(concepts[0]["capability_refs"])
            if observed != planned:
                fail("topic hints mutated capability scope")
        if case_id == "QUESTION_PLUS_WORK":
            if result["diagnostic_objects"][0].get("focal_feature") != "QUOTIENT_ZERO_REQUIRED":
                fail("diagnostic focal feature lost")
        if case_id == "ALL_THREE":
            if "UNIT_CHAIN_CONVERSION_SKIPPED" not in concepts[0].get("error_signature_refs", []):
                fail("bounded work error signature not preserved")

    required = {"QUESTION_ONLY", "QUESTION_PLUS_WORK", "QUESTION_PLUS_TOPIC_HINTS", "ALL_THREE"}
    if seen != required:
        fail(f"cold-start case names mismatch: {seen}")


def validate_falsifiers() -> None:
    corpus = json.loads(FIXTURE.read_text(encoding="utf-8"))
    base = corpus["cases"][0]["input"]

    raw_only = copy.deepcopy(base)
    raw_only["question_set"]["questions"][0].pop("evidence")
    expect_error(raw_only, "SEMANTIC_EVIDENCE_REQUIRED")

    bad_cap = copy.deepcopy(base)
    bad_cap["question_set"]["questions"][0]["evidence"]["capability_refs"].append("NOT_A_CAPABILITY")
    expect_error(bad_cap, "UNKNOWN_CAPABILITY_REF")

    bad_pf = copy.deepcopy(base)
    bad_pf["question_set"]["questions"][0]["evidence"]["problem_family_refs"].append("PF_KEYWORD_EACH_MEANS_MULTIPLY")
    expect_error(bad_pf, "UNKNOWN_PROBLEM_FAMILY_REF")

    bad_rt = copy.deepcopy(base)
    bad_rt["question_set"]["questions"][0]["evidence"]["translation_refs"].append("RT_INVENTED_BRIDGE")
    expect_error(bad_rt, "UNKNOWN_REPRESENTATION_TRANSLATION_REF")

    curriculum_no_authority = copy.deepcopy(base)
    ev = curriculum_no_authority["question_set"]["questions"][0]["evidence"]
    ev["scope_basis"] = "CURRICULUM_CONFIRMED"
    ev["authority_ref"] = None
    expect_error(curriculum_no_authority, "CURRICULUM_CONFIRMED_WITHOUT_AUTHORITY_REF")

    universalize = copy.deepcopy(base)
    universalize["question_set"]["questions"][0]["evidence"]["universal_grade_claim"] = True
    expect_error(universalize, "QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE")

    work_case = corpus["cases"][1]["input"]
    teacher_merge = copy.deepcopy(work_case)
    teacher_merge["student_workout"]["work_evidence"][0]["teacher_correction_as_child_original"] = True
    expect_error(teacher_merge, "TEACHER_CORRECTION_COUNTED_AS_CHILD_EVIDENCE")

    bad_probe = copy.deepcopy(work_case)
    bad_probe["student_workout"]["work_evidence"][0]["diagnostic"]["competing_hypotheses"] = [
        {"hypothesis_id": "ONLY-ONE", "durable_trait": False}
    ]
    expect_error(bad_probe, "PROBE_MODE_WITHOUT_COMPETING_HYPOTHESES")

    erased_substep = copy.deepcopy(work_case)
    erased_substep["student_workout"]["work_evidence"][0]["correct_substeps_preserved"] = False
    expect_error(erased_substep, "INCORRECT_FINAL_ERASES_CORRECT_SUBSTEP")


def validate_publisher_independence() -> None:
    text = AUTHOR_SOURCE.read_text(encoding="utf-8").lower()
    forbidden = ["import reportlab", "publication.engine", "representation.engine", "pagemetrics", "boundingbox"]
    leaks = [token for token in forbidden if token in text]
    if leaks:
        fail(f"authoring engine leaked publisher dependency: {leaks}")


def main() -> None:
    validate_positive_cases()
    validate_falsifiers()
    validate_publisher_independence()
    print("Primary Math V2 authoring engine: cold-start cases and falsifiers PASS")


if __name__ == "__main__":
    main()
