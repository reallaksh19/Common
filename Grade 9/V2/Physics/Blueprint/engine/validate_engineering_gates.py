#!/usr/bin/env python3
"""Deterministic validator for the Physics Technical Engineering Gate Registry.

Enforces schema contracts, global ID uniqueness, prerequisite graph validity,
cross-reference integrity, subtopic physics invariants, and fail-closed readiness.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaValidationError

ROOT = Path(__file__).resolve().parents[1]


class EngineeringGateValidationError(Exception):
    """Structured validation error with stable machine-readable code."""
    def __init__(self, code: str, message: str, context: dict | None = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.context = context or {}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_gate_schema(registry: dict) -> None:
    schema_path = ROOT / "contracts" / "physics-technical-engineering-gate.schema.json"
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    try:
        validator.validate(registry)
    except SchemaValidationError as e:
        raise EngineeringGateValidationError("ENG_GATE_SCHEMA_VIOLATION", str(e), {"path": list(e.path)})


def validate_global_invariants(registry: dict) -> None:
    seen_subtopics: set[str] = set()
    seen_concepts: set[str] = set()
    seen_equations: set[str] = set()
    seen_reps: set[str] = set()
    seen_misconceptions: set[str] = set()

    for gate in registry["subtopic_gates"]:
        sub_id = gate["subtopic_id"]
        if sub_id in seen_subtopics:
            raise EngineeringGateValidationError("ENG_GATE_DUPLICATE_ID", f"Duplicate subtopic ID: {sub_id}")
        seen_subtopics.add(sub_id)

        for c in gate["technical_core"]:
            cid = c["concept_id"]
            if cid in seen_concepts:
                raise EngineeringGateValidationError("ENG_GATE_DUPLICATE_ID", f"Duplicate concept ID: {cid}")
            seen_concepts.add(cid)

        for eq in gate["mandatory_equations"]:
            eid = eq["equation_id"]
            if eid in seen_equations:
                raise EngineeringGateValidationError("ENG_GATE_DUPLICATE_ID", f"Duplicate equation ID: {eid}")
            seen_equations.add(eid)

        for rep in gate["representations"]:
            rid = rep["representation_id"]
            if rid in seen_reps:
                raise EngineeringGateValidationError("ENG_GATE_DUPLICATE_ID", f"Duplicate representation ID: {rid}")
            seen_reps.add(rid)

        for m in gate["misconceptions"]:
            mid = m["misconception_id"]
            if mid in seen_misconceptions:
                raise EngineeringGateValidationError("ENG_GATE_DUPLICATE_ID", f"Duplicate misconception ID: {mid}")
            seen_misconceptions.add(mid)

    # Cross-subtopic prerequisite integrity
    for gate in registry["subtopic_gates"]:
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("PHY-") and prereq not in seen_subtopics:
                raise EngineeringGateValidationError(
                    "ENG_GATE_UNRESOLVED_PREREQUISITE",
                    f"Subtopic {gate['subtopic_id']} has unresolved prerequisite {prereq}"
                )

    _validate_dependency_cycles(registry)


def _validate_dependency_cycles(registry: dict) -> None:
    gates = {gate["subtopic_id"]: gate for gate in registry["subtopic_gates"]}
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(gate_id: str) -> None:
        if gate_id in visited:
            return
        if gate_id in visiting:
            raise EngineeringGateValidationError(
                "ENG_GATE_DEPENDENCY_CYCLE",
                f"Dependency cycle detected involving {gate_id}",
            )
        visiting.add(gate_id)
        for prereq in gates.get(gate_id, {}).get("prerequisite_ids", []):
            if isinstance(prereq, str) and prereq.startswith("PHY-"):
                walk(prereq)
        visiting.remove(gate_id)
        visited.add(gate_id)

    for gate_id in gates:
        walk(gate_id)


def validate_subtopic_invariants(gate: dict) -> None:
    sub_id = gate["subtopic_id"]

    # 1. Identity & Readiness
    if not sub_id.startswith("PHY-"):
        raise EngineeringGateValidationError("ENG_GATE_INVALID_SUBTOPIC_ID", f"Invalid subtopic ID format: {sub_id}")
    if gate.get("maturity") != "ENGINEERING":
        raise EngineeringGateValidationError("ENG_GATE_MATURITY_OVERREACH", f"Maturity must be ENGINEERING, got {gate.get('maturity')}")

    # 2. Cross-reference integrity for problem families
    defined_fams = {f["family_id"] for f in gate.get("problem_families", [])}
    for lfid in gate.get("linked_problem_family_ids", []):
        if lfid not in defined_fams:
            raise EngineeringGateValidationError(
                "ENG_GATE_CROSS_REFERENCE_INTEGRITY_FAIL",
                f"Linked problem family {lfid} not defined in problem_families of {sub_id}"
            )

    # 3. Specific Physics Invariant Gates
    concept_ids = {c["concept_id"] for c in gate.get("technical_core", [])}
    equation_ids = {e["equation_id"] for e in gate.get("mandatory_equations", [])}
    misc_ids = {m["misconception_id"] for m in gate.get("misconceptions", [])}
    prereq_ids = set(gate.get("prerequisite_ids", []))

    if sub_id == "PHY-VEC-BASICS":
        if "CON-VEC-SCALAR-DEF" not in concept_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_REQUIRED_CONCEPT", "PHY-VEC-BASICS requires explicit scalar definition (CON-VEC-SCALAR-DEF)")
        if "CON-VEC-VECTOR-DEF" not in concept_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_REQUIRED_CONCEPT", "PHY-VEC-BASICS requires explicit vector definition (CON-VEC-VECTOR-DEF)")

    elif sub_id == "PHY-VEC-COMPONENTS":
        if "CON-VEC-SIGN-CONVENTION" not in concept_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_REQUIRED_CONCEPT", "PHY-VEC-COMPONENTS requires explicit sign/frame convention (CON-VEC-SIGN-CONVENTION)")
        if "EQ-VEC-RECON-MAG" not in equation_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_MANDATORY_EQUATION", "PHY-VEC-COMPONENTS requires resultant reconstruction equation (EQ-VEC-RECON-MAG)")

    elif sub_id == "PHY-NLM-FIRST-LAW":
        if "MISC-NLM-REST-NO-FORCE" not in misc_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_MISCONCEPTION_TRAP", "PHY-NLM-FIRST-LAW requires equilibrium misconception trap (MISC-NLM-REST-NO-FORCE)")

    elif sub_id == "PHY-NLM-SECOND-LAW":
        if "PHY-NLM-FBD" not in prereq_ids:
            raise EngineeringGateValidationError("ENG_GATE_UNRESOLVED_PREREQUISITE", "PHY-NLM-SECOND-LAW requires prior Free-Body Diagram isolation (PHY-NLM-FBD)")
        if "EQ-NLM-NEWTON2-COMP-X" not in equation_ids or "EQ-NLM-NEWTON2-COMP-Y" not in equation_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_MANDATORY_EQUATION", "PHY-NLM-SECOND-LAW requires axis-wise F=ma equations")

    elif sub_id == "PHY-NLM-THIRD-LAW":
        if "MISC-NLM-NORMAL-WEIGHT-PAIR" not in misc_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_MISCONCEPTION_TRAP", "PHY-NLM-THIRD-LAW requires same-body third-law trap (MISC-NLM-NORMAL-WEIGHT-PAIR)")

    elif sub_id == "PHY-NLM-NORMAL":
        if "CON-NLM-NORMAL-NOT-ALWAYS-MG" not in concept_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_REQUIRED_CONCEPT", "PHY-NLM-NORMAL requires normal != mg concept (CON-NLM-NORMAL-NOT-ALWAYS-MG)")

    elif sub_id == "PHY-NLM-TENSION":
        if "MISC-NLM-TENSION-EQUALS-WEIGHT" not in misc_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_MISCONCEPTION_TRAP", "PHY-NLM-TENSION requires Atwood tension!=mg trap (MISC-NLM-TENSION-EQUALS-WEIGHT)")

    elif sub_id == "PHY-NLM-FRICTION":
        if "EQ-NLM-STATIC-INEQUALITY" not in equation_ids:
            raise EngineeringGateValidationError("ENG_GATE_MISSING_MANDATORY_EQUATION", "PHY-NLM-FRICTION requires static inequality equation (EQ-NLM-STATIC-INEQUALITY)")

    # 4. Difficulty Profile Invariants
    dp = gate["difficulty_profile"]
    dims = [
        "prerequisite_depth", "element_interactivity", "inferential_jump_severity",
        "representation_translation", "model_discrimination", "sign_or_frame_sensitivity",
        "multi_step_dependency", "abstraction", "misconception_density", "synthesis"
    ]
    for d in dims:
        if not (0 <= dp.get(d, -1) <= 3):
            raise EngineeringGateValidationError("ENG_GATE_INVALID_DIFFICULTY_PROFILE", f"Dimension {d} must be 0-3")
    if dp.get("maturity") != "ENGINEERING":
        raise EngineeringGateValidationError("ENG_GATE_INVALID_DIFFICULTY_PROFILE", "Difficulty profile maturity must be ENGINEERING")

    # 5. Release Checklist: All must be True for ENGINEERING_GATE_READY
    rc = gate["release_checklist"]
    if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
        for req_field, status in rc.items():
            if status is not True:
                raise EngineeringGateValidationError(
                    "ENG_GATE_RELEASE_CHECKLIST_INCOMPLETE",
                    f"Release checklist field {req_field} must be True for READY gate in {sub_id}"
                )


def validate(registry: dict) -> list[str]:
    validate_gate_schema(registry)
    validate_global_invariants(registry)
    validated_subtopics = []
    for gate in registry["subtopic_gates"]:
        validate_subtopic_invariants(gate)
        validated_subtopics.append(gate["subtopic_id"])
    return validated_subtopics


# True mutation-based falsifier battery:
def run_falsification_battery():
    registry_path = ROOT / "policy" / "physics-technical-engineering-gates.v1.json"
    clean_registry = load_json(registry_path)

    def expect_rejection(mutated: dict, expected_code: str):
        try:
            validate(mutated)
        except EngineeringGateValidationError as err:
            if err.code != expected_code:
                raise AssertionError(f"Expected code {expected_code}, got {err.code}: {err.message}")
            return
        except Exception as err:
            raise AssertionError(f"Expected EngineeringGateValidationError [{expected_code}], got {type(err).__name__}: {err}")
        raise AssertionError(f"Expected validator rejection with code [{expected_code}], but validation passed!")

    # 1. VEC-FAIL-01: Direction / sign convention omitted in PHY-VEC-COMPONENTS
    bad1 = copy.deepcopy(clean_registry)
    vec_comp = next(g for g in bad1["subtopic_gates"] if g["subtopic_id"] == "PHY-VEC-COMPONENTS")
    vec_comp["technical_core"] = [c for c in vec_comp["technical_core"] if c["concept_id"] != "CON-VEC-SIGN-CONVENTION"]
    expect_rejection(bad1, "ENG_GATE_MISSING_REQUIRED_CONCEPT")

    # 2. VEC-FAIL-02: Missing resultant reconstruction equation in PHY-VEC-COMPONENTS
    bad2 = copy.deepcopy(clean_registry)
    vec_comp2 = next(g for g in bad2["subtopic_gates"] if g["subtopic_id"] == "PHY-VEC-COMPONENTS")
    vec_comp2["mandatory_equations"] = [e for e in vec_comp2["mandatory_equations"] if e["equation_id"] != "EQ-VEC-RECON-MAG"]
    expect_rejection(bad2, "ENG_GATE_MISSING_MANDATORY_EQUATION")

    # 3. VEC-FAIL-03: Scalar / vector distinction blurred in PHY-VEC-BASICS
    bad3 = copy.deepcopy(clean_registry)
    vec_basics = next(g for g in bad3["subtopic_gates"] if g["subtopic_id"] == "PHY-VEC-BASICS")
    vec_basics["technical_core"] = [c for c in vec_basics["technical_core"] if c["concept_id"] != "CON-VEC-SCALAR-DEF"]
    expect_rejection(bad3, "ENG_GATE_MISSING_REQUIRED_CONCEPT")

    # 4. NLM-FAIL-01: Second Law without prior isolated FBD prerequisite
    bad4 = copy.deepcopy(clean_registry)
    nlm2 = next(g for g in bad4["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-SECOND-LAW")
    nlm2["prerequisite_ids"] = [p for p in nlm2["prerequisite_ids"] if p != "PHY-NLM-FBD"]
    expect_rejection(bad4, "ENG_GATE_UNRESOLVED_PREREQUISITE")

    # 5. NLM-FAIL-02: Third-law action-reaction pairs on same body misconception missing
    bad5 = copy.deepcopy(clean_registry)
    nlm3 = next(g for g in bad5["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-THIRD-LAW")
    nlm3["misconceptions"] = [m for m in nlm3["misconceptions"] if m["misconception_id"] != "MISC-NLM-NORMAL-WEIGHT-PAIR"]
    expect_rejection(bad5, "ENG_GATE_MISSING_MISCONCEPTION_TRAP")

    # 6. NLM-FAIL-03: Normal force assumed equal to mg automatically
    bad6 = copy.deepcopy(clean_registry)
    norm = next(g for g in bad6["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-NORMAL")
    norm["technical_core"] = [c for c in norm["technical_core"] if c["concept_id"] != "CON-NLM-NORMAL-NOT-ALWAYS-MG"]
    expect_rejection(bad6, "ENG_GATE_MISSING_REQUIRED_CONCEPT")

    # 7. NLM-FAIL-04: Equilibrium treated as absence of forces rather than net a=0
    bad7 = copy.deepcopy(clean_registry)
    nlm1 = next(g for g in bad7["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-FIRST-LAW")
    nlm1["misconceptions"] = [m for m in nlm1["misconceptions"] if m["misconception_id"] != "MISC-NLM-REST-NO-FORCE"]
    expect_rejection(bad7, "ENG_GATE_MISSING_MISCONCEPTION_TRAP")

    # 8. NLM-FAIL-05: Static friction equated blindly to mu_s * N without inequality
    bad8 = copy.deepcopy(clean_registry)
    frict = next(g for g in bad8["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-FRICTION")
    frict["mandatory_equations"] = [e for e in frict["mandatory_equations"] if e["equation_id"] != "EQ-NLM-STATIC-INEQUALITY"]
    expect_rejection(bad8, "ENG_GATE_MISSING_MANDATORY_EQUATION")

    # 9. NLM-FAIL-06: Atwood hanging tension asserted as T = mg under acceleration
    bad9 = copy.deepcopy(clean_registry)
    tens = next(g for g in bad9["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-TENSION")
    tens["misconceptions"] = [m for m in tens["misconceptions"] if m["misconception_id"] != "MISC-NLM-TENSION-EQUALS-WEIGHT"]
    expect_rejection(bad9, "ENG_GATE_MISSING_MISCONCEPTION_TRAP")

    # 10. CROSS-FAIL-01: Problem family ID in linked_problem_family_ids not defined
    bad10 = copy.deepcopy(clean_registry)
    conn = next(g for g in bad10["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-CONNECTED")
    conn["linked_problem_family_ids"].append("PF-NLM-ORPHAN-FAMILY")
    expect_rejection(bad10, "ENG_GATE_CROSS_REFERENCE_INTEGRITY_FAIL")

    # 11. GLOBAL-FAIL-01: Duplicate concept ID across distinct subtopics
    bad11 = copy.deepcopy(clean_registry)
    bad11["subtopic_gates"][0]["technical_core"].append({
        "concept_id": bad11["subtopic_gates"][1]["technical_core"][0]["concept_id"],
        "canonical_statement": "Duplicate statement across subtopics for falsifier test.",
        "why_required": "Must fail uniqueness test.",
        "failure_if_omitted": "Fails global invariant."
    })
    expect_rejection(bad11, "ENG_GATE_DUPLICATE_ID")

    # 12. CHECKLIST-FAIL-01: Incomplete release checklist marked as ENGINEERING_GATE_READY
    bad12 = copy.deepcopy(clean_registry)
    bad12["subtopic_gates"][0]["release_checklist"]["provenance_verified"] = False
    expect_rejection(bad12, "ENG_GATE_RELEASE_CHECKLIST_INCOMPLETE")

    print("Physics Technical Engineering Gate falsification battery: PASS (all 12 mutation falsifiers caught by production validator)")


if __name__ == "__main__":
    reg = load_json(ROOT / "policy" / "physics-technical-engineering-gates.v1.json")
    subtopics = validate(reg)
    print(f"Validated {len(subtopics)} Physics Technical Engineering subtopic gates: PASS")
    run_falsification_battery()
