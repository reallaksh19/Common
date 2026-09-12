#!/usr/bin/env python3
"""Fail-closed structural validator for Primary Math V2 architecture contracts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
FIXTURES = ROOT / "fixtures" / "cold_start_cases.json"

AUTHORITIES = ["#163", "#171", "#172", "#185", "#182", "#164"]
SCHEMAS = [
    "primary-math-input.schema.json",
    "concept-node.schema.json",
    "primary-math-skill-model.schema.json",
    "learning-design-plan.schema.json",
    "representation-plan.schema.json",
    "architecture-manifest.schema.json",
]
SCOPE_BASES = {
    "CURRICULUM_CONFIRMED",
    "QUESTION_SET_OBSERVED",
    "SCHOOL_CLASSWORK_OBSERVED",
    "COMMON_G4_5_CAPABILITY",
    "CURRICULUM_OVERLAY",
    "EXTENSION",
    "STRETCH",
    "MAPPING_PENDING",
    "SOURCE_NOT_PROVIDED",
}
CONCEPT_MODES = {
    "INTRODUCE",
    "CONNECT",
    "REPAIR",
    "PROBE",
    "PRACTISE",
    "RETRIEVE",
    "TRANSFER",
    "VERIFY",
    "REFERENCE",
}


def fail(msg: str) -> None:
    raise SystemExit(f"Primary Math V2 architecture validation failed: {msg}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def require(condition: bool, msg: str) -> None:
    if not condition:
        fail(msg)


def validate_docs() -> None:
    architecture = (ROOT / "PRIMARY_MATH_V2_ARCHITECTURE.md").read_text(encoding="utf-8")
    ownership = (ROOT / "SEMANTIC_OWNERSHIP.md").read_text(encoding="utf-8")
    authoring = (ROOT / "AUTHORING_FLOW.md").read_text(encoding="utf-8")
    combined = "\n".join([architecture, ownership, authoring])
    for pr in AUTHORITIES:
        require(pr in combined, f"Common authority {pr} is not linked in architecture docs")
    for token in [
        "PrimaryMathSkillModel",
        "ConceptMode",
        "PrimaryMathCore1StudyPlan",
        "PrimaryMathCore2CompanionPlan",
        "RepresentationPlan",
        "renderer_invention_allowed = false",
    ]:
        require(token in architecture, f"architecture missing required token: {token}")
    require("Grade 9 PRs are non-normative" in architecture, "Grade 9 non-authority boundary missing")


def validate_schemas() -> None:
    docs = {}
    for name in SCHEMAS:
        path = CONTRACTS / name
        require(path.exists(), f"missing schema {name}")
        obj = load_json(path)
        docs[name] = obj
        require(obj.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{name} must use JSON Schema 2020-12")
        require(obj.get("type") == "object", f"{name} must describe an object")

    concept = docs["concept-node.schema.json"]
    enum = set(concept["properties"]["scope_basis"]["enum"])
    require(enum == SCOPE_BASES, "concept-node scope basis enum drifted from architecture")

    learning = docs["learning-design-plan.schema.json"]
    mode_enum = set(learning["properties"]["modules"]["items"]["properties"]["concept_mode"]["enum"])
    require(mode_enum == CONCEPT_MODES, "ConceptMode enum drifted from architecture")

    manifest = docs["architecture-manifest.schema.json"]
    human = set(manifest["properties"]["human_review_status"]["required"])
    expected_human = {
        "SUBJECT_CORRECTNESS",
        "PEDAGOGICAL_DESIGN",
        "ASSESSMENT_DESIGN",
        "VISUAL_USABILITY",
        "CHILD_USABILITY",
        "MATURE_DESIGN_QUALITY",
    }
    require(human == expected_human, "human review gate set drifted")


def validate_cold_start_fixtures() -> None:
    data = load_json(FIXTURES)
    cases = data.get("cases") or []
    require(len(cases) == 4, "expected exactly four cold-start input combinations")
    by_id = {case["case_id"]: case for case in cases}
    expected_ids = {"QUESTION_ONLY", "QUESTION_PLUS_WORK", "QUESTION_PLUS_HINTS", "QUESTION_WORK_HINTS"}
    require(set(by_id) == expected_ids, "cold-start fixture IDs changed")

    combos = set()
    for case in cases:
        inp = case["input"]
        questions = ((inp.get("question_set") or {}).get("questions") or [])
        require(bool(questions), f"{case['case_id']} has no questions")
        has_work = "student_workout" in inp and inp["student_workout"] is not None
        has_hints = "topic_hints" in inp and inp["topic_hints"] is not None
        combos.add((has_work, has_hints))

        exp = case["expected"]
        require(exp["student_work_present"] == has_work, f"{case['case_id']} work-presence expectation mismatch")
        require(exp["topic_hints_present"] == has_hints, f"{case['case_id']} topic-hint expectation mismatch")
        require(exp["scope_basis"] in SCOPE_BASES, f"{case['case_id']} invalid scope basis")
        require(exp["concept_mode"] in CONCEPT_MODES, f"{case['case_id']} invalid ConceptMode")

        work_refs = exp.get("work_evidence_refs") or []
        if not has_work:
            require(not work_refs, f"{case['case_id']} fabricated work evidence without student_workout")
        else:
            observed_id = inp["student_workout"].get("work_evidence_id")
            require(observed_id in work_refs, f"{case['case_id']} did not preserve supplied work evidence ref")

        if exp["scope_basis"] in {"QUESTION_SET_OBSERVED", "SCHOOL_CLASSWORK_OBSERVED"}:
            require(not exp.get("universal_grade_claim", False), f"{case['case_id']} promoted observed scope to universal grade claim")

    require(combos == {(False, False), (True, False), (False, True), (True, True)}, "not all optional-input combinations are covered")


def main() -> int:
    validate_docs()
    validate_schemas()
    validate_cold_start_fixtures()
    print("Primary Math V2 architecture contracts and cold-start fixtures: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
