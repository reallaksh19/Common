#!/usr/bin/env python3
"""Deterministic validator for the Chemistry Technical Engineering Gate Registry.

Enforces schema contracts, global ID uniqueness, prerequisite graph validity,
cross-reference integrity, subtopic chemistry invariants, and fail-closed readiness.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaValidationError

ROOT = Path(__file__).resolve().parents[1]


class ChemistryEngineeringGateValidationError(Exception):
    """Structured validation error with stable machine-readable code."""
    def __init__(self, code: str, message: str, context: dict | None = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.context = context or {}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_gate_schema(registry: dict) -> None:
    schema_path = ROOT / "contracts" / "chemistry-technical-engineering-gate.schema.json"
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    try:
        validator.validate(registry)
    except SchemaValidationError as e:
        raise ChemistryEngineeringGateValidationError("CHEM_GATE_SCHEMA_VIOLATION", str(e), {"path": list(e.path)})


def validate_global_invariants(registry: dict) -> None:
    seen_subtopics: set[str] = set()
    seen_concepts: set[str] = set()
    seen_equations: set[str] = set()
    seen_reps: set[str] = set()
    seen_misconceptions: set[str] = set()

    for gate in registry["subtopic_gates"]:
        sub_id = gate["subtopic_id"]
        if sub_id in seen_subtopics:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_DUPLICATE_ID", f"Duplicate subtopic ID: {sub_id}")
        seen_subtopics.add(sub_id)

        for c in gate["technical_core"]:
            cid = c["concept_id"]
            if cid in seen_concepts:
                raise ChemistryEngineeringGateValidationError("CHEM_GATE_DUPLICATE_ID", f"Duplicate concept ID: {cid}")
            seen_concepts.add(cid)

        for eq in gate["mandatory_equations"]:
            eid = eq["equation_id"]
            if eid in seen_equations:
                raise ChemistryEngineeringGateValidationError("CHEM_GATE_DUPLICATE_ID", f"Duplicate equation ID: {eid}")
            seen_equations.add(eid)

        for rep in gate["representations"]:
            rid = rep["representation_id"]
            if rid in seen_reps:
                raise ChemistryEngineeringGateValidationError("CHEM_GATE_DUPLICATE_ID", f"Duplicate representation ID: {rid}")
            seen_reps.add(rid)

        for m in gate["misconceptions"]:
            mid = m["misconception_id"]
            if mid in seen_misconceptions:
                raise ChemistryEngineeringGateValidationError("CHEM_GATE_DUPLICATE_ID", f"Duplicate misconception ID: {mid}")
            seen_misconceptions.add(mid)

    # Cross-subtopic prerequisite integrity
    for gate in registry["subtopic_gates"]:
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("CHEM-") and prereq not in seen_subtopics:
                raise ChemistryEngineeringGateValidationError(
                    "CHEM_GATE_UNRESOLVED_PREREQUISITE",
                    f"Subtopic {gate['subtopic_id']} has unresolved prerequisite {prereq}"
                )


def validate_subtopic_invariants(gate: dict) -> None:
    sub_id = gate["subtopic_id"]

    # 1. Identity & Readiness
    if not sub_id.startswith("CHEM-"):
        raise ChemistryEngineeringGateValidationError("CHEM_GATE_INVALID_SUBTOPIC_ID", f"Invalid subtopic ID format: {sub_id}")
    if gate.get("maturity") != "ENGINEERING":
        raise ChemistryEngineeringGateValidationError("CHEM_GATE_MATURITY_OVERREACH", f"Maturity must be ENGINEERING, got {gate.get('maturity')}")

    # 2. Cross-reference integrity for problem families
    defined_fams = {f["family_id"] for f in gate.get("problem_families", [])}
    for lfid in gate.get("linked_problem_family_ids", []):
        if lfid not in defined_fams:
            raise ChemistryEngineeringGateValidationError(
                "CHEM_GATE_CROSS_REFERENCE_INTEGRITY_FAIL",
                f"Linked problem family {lfid} not defined in problem_families of {sub_id}"
            )

    # 3. Specific Chemistry Invariant Gates
    concept_ids = {c["concept_id"] for c in gate.get("technical_core", [])}
    equation_ids = {e["equation_id"] for e in gate.get("mandatory_equations", [])}
    representation_ids = {r["representation_id"] for r in gate.get("representations", [])}
    misc_ids = {m["misconception_id"] for m in gate.get("misconceptions", [])}
    prereq_ids = set(gate.get("prerequisite_ids", []))

    if sub_id == "CHEM-SYM-LITERACY":
        if "CON-CHEM-SUBSCRIPT-VS-COEFF" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-SYM-LITERACY requires subscript vs coefficient concept (CON-CHEM-SUBSCRIPT-VS-COEFF)")
        if "EQ-CHEM-ATOMIC-COMP" not in equation_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MANDATORY_EQUATION", "CHEM-SYM-LITERACY requires atomic composition equation (EQ-CHEM-ATOMIC-COMP)")

    elif sub_id == "CHEM-ION-VALENCY":
        if "CON-CHEM-POLYATOMIC-IONS" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-ION-VALENCY requires polyatomic ion concept (CON-CHEM-POLYATOMIC-IONS)")
        if "MISC-CHEM-POLYATOMIC-SUBSCRIPT-NO-BRACKET" not in misc_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MISCONCEPTION_TRAP", "CHEM-ION-VALENCY requires polyatomic subscript bracket trap (MISC-CHEM-POLYATOMIC-SUBSCRIPT-NO-BRACKET)")

    elif sub_id == "CHEM-FORMULA-CONSTRUCTION":
        if "CON-CHEM-ELECTRONEUTRALITY" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-FORMULA-CONSTRUCTION requires electroneutrality concept (CON-CHEM-ELECTRONEUTRALITY)")
        if "EQ-CHEM-ELECTRONEUTRALITY" not in equation_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MANDATORY_EQUATION", "CHEM-FORMULA-CONSTRUCTION requires electroneutrality equation (EQ-CHEM-ELECTRONEUTRALITY)")

    elif sub_id == "CHEM-EQ-BALANCING":
        if "CHEM-FORMULA-CONSTRUCTION" not in prereq_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_UNRESOLVED_PREREQUISITE", "CHEM-EQ-BALANCING requires prior formula construction prerequisite (CHEM-FORMULA-CONSTRUCTION)")
        if "CON-CHEM-COEFFICIENT-ONLY-BALANCING" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-EQ-BALANCING requires coefficient-only balancing concept (CON-CHEM-COEFFICIENT-ONLY-BALANCING)")
        if "EQ-CHEM-ATOM-BALANCE" not in equation_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MANDATORY_EQUATION", "CHEM-EQ-BALANCING requires atom conservation equation (EQ-CHEM-ATOM-BALANCE)")

    elif sub_id == "CHEM-STATE-SYMBOLS":
        if "CON-CHEM-AQ-VS-LIQUID" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-STATE-SYMBOLS requires aqueous vs liquid distinction (CON-CHEM-AQ-VS-LIQUID)")
        if "EQ-CHEM-PRECIPITATION-STATE" not in equation_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MANDATORY_EQUATION", "CHEM-STATE-SYMBOLS requires state-annotated precipitation equation (EQ-CHEM-PRECIPITATION-STATE)")

    elif sub_id == "CHEM-REACTION-CONDITIONS":
        if "CON-CHEM-CONDITION-SPECIFICATION" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-REACTION-CONDITIONS requires reaction condition specification (CON-CHEM-CONDITION-SPECIFICATION)")

    elif sub_id == "CHEM-REP-TRANSLATION":
        if "CON-CHEM-JOHNSTONE-TRIANGLE" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-REP-TRANSLATION requires Johnstone triplet concept (CON-CHEM-JOHNSTONE-TRIANGLE)")
        if "REP-CHEM-JOHNSTONE-TRIPLET" not in representation_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MANDATORY_REPRESENTATION", "CHEM-REP-TRANSLATION requires triplet representation (REP-CHEM-JOHNSTONE-TRIPLET)")

    elif sub_id == "CHEM-CALC-STOICHIOMETRY":
        if "EQ-CHEM-MOLE-CONVERSION" not in equation_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MANDATORY_EQUATION", "CHEM-CALC-STOICHIOMETRY requires mole conversion equation (EQ-CHEM-MOLE-CONVERSION)")
        if "MISC-CHEM-MASS-RATIO-COEFFICIENT" not in misc_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MISCONCEPTION_TRAP", "CHEM-CALC-STOICHIOMETRY requires mass-ratio misconception trap (MISC-CHEM-MASS-RATIO-COEFFICIENT)")

    elif sub_id == "CHEM-ACID-BASE-IONS":
        if "CON-CHEM-ARRHENIUS-IONIZATION" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-ACID-BASE-IONS requires Arrhenius aqueous ionization concept (CON-CHEM-ARRHENIUS-IONIZATION)")
        if "MISC-CHEM-DRY-ACID-ACTIVE" not in misc_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MISCONCEPTION_TRAP", "CHEM-ACID-BASE-IONS requires dry acid misconception trap (MISC-CHEM-DRY-ACID-ACTIVE)")

    elif sub_id == "CHEM-REDOX-OXIDATION":
        if "CON-CHEM-AGENT-INVERSION" not in concept_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_REQUIRED_CONCEPT", "CHEM-REDOX-OXIDATION requires agent role inversion concept (CON-CHEM-AGENT-INVERSION)")
        if "MISC-CHEM-OXIDIZING-AGENT-OXIDIZED" not in misc_ids:
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_MISSING_MISCONCEPTION_TRAP", "CHEM-REDOX-OXIDATION requires oxidizing agent trap (MISC-CHEM-OXIDIZING-AGENT-OXIDIZED)")

    # 4. Difficulty Profile Invariants
    dp = gate["difficulty_profile"]
    dims = [
        "prerequisite_depth", "element_interactivity", "inferential_jump_severity",
        "representation_translation", "model_discrimination", "sign_or_frame_sensitivity",
        "multi_step_dependency", "abstraction", "misconception_density", "synthesis"
    ]
    for d in dims:
        if not (0 <= dp.get(d, -1) <= 3):
            raise ChemistryEngineeringGateValidationError("CHEM_GATE_INVALID_DIFFICULTY_PROFILE", f"Dimension {d} must be 0-3")
    if dp.get("maturity") != "ENGINEERING":
        raise ChemistryEngineeringGateValidationError("CHEM_GATE_INVALID_DIFFICULTY_PROFILE", "Difficulty profile maturity must be ENGINEERING")

    # 5. Release Checklist: All must be True for ENGINEERING_GATE_READY
    rc = gate["release_checklist"]
    if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
        for req_field, status in rc.items():
            if status is not True:
                raise ChemistryEngineeringGateValidationError(
                    "CHEM_GATE_RELEASE_CHECKLIST_INCOMPLETE",
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
    registry_path = ROOT / "policies" / "chemistry-technical-engineering-gates.v1.json"
    clean_registry = load_json(registry_path)

    def expect_rejection(mutated: dict, expected_code: str):
        try:
            validate(mutated)
        except ChemistryEngineeringGateValidationError as err:
            if err.code != expected_code:
                raise AssertionError(f"Expected code {expected_code}, got {err.code}: {err.message}")
            return
        except Exception as err:
            raise AssertionError(f"Expected ChemistryEngineeringGateValidationError [{expected_code}], got {type(err).__name__}: {err}")
        raise AssertionError(f"Expected validator rejection with code [{expected_code}], but validation passed!")

    # 1. CHEM-FAIL-01: Balancing by subscript alteration allowed (missing coefficient-only concept in CHEM-EQ-BALANCING)
    bad1 = copy.deepcopy(clean_registry)
    bal = next(g for g in bad1["subtopic_gates"] if g["subtopic_id"] == "CHEM-EQ-BALANCING")
    bal["technical_core"] = [c for c in bal["technical_core"] if c["concept_id"] != "CON-CHEM-COEFFICIENT-ONLY-BALANCING"]
    expect_rejection(bad1, "CHEM_GATE_MISSING_REQUIRED_CONCEPT")

    # 2. CHEM-FAIL-02: Dry acid activity misconception omitted in CHEM-ACID-BASE-IONS
    bad2 = copy.deepcopy(clean_registry)
    acid = next(g for g in bad2["subtopic_gates"] if g["subtopic_id"] == "CHEM-ACID-BASE-IONS")
    acid["misconceptions"] = [m for m in acid["misconceptions"] if m["misconception_id"] != "MISC-CHEM-DRY-ACID-ACTIVE"]
    expect_rejection(bad2, "CHEM_GATE_MISSING_MISCONCEPTION_TRAP")

    # 3. CHEM-FAIL-03: Electroneutrality omitted in CHEM-FORMULA-CONSTRUCTION
    bad3 = copy.deepcopy(clean_registry)
    form = next(g for g in bad3["subtopic_gates"] if g["subtopic_id"] == "CHEM-FORMULA-CONSTRUCTION")
    form["technical_core"] = [c for c in form["technical_core"] if c["concept_id"] != "CON-CHEM-ELECTRONEUTRALITY"]
    expect_rejection(bad3, "CHEM_GATE_MISSING_REQUIRED_CONCEPT")

    # 4. CHEM-FAIL-04: Mole conversion equation omitted in CHEM-CALC-STOICHIOMETRY
    bad4 = copy.deepcopy(clean_registry)
    stoich = next(g for g in bad4["subtopic_gates"] if g["subtopic_id"] == "CHEM-CALC-STOICHIOMETRY")
    stoich["mandatory_equations"] = [e for e in stoich["mandatory_equations"] if e["equation_id"] != "EQ-CHEM-MOLE-CONVERSION"]
    expect_rejection(bad4, "CHEM_GATE_MISSING_MANDATORY_EQUATION")

    # 5. CHEM-FAIL-05: Polyatomic ion subscript bracket trap omitted in CHEM-ION-VALENCY
    bad5 = copy.deepcopy(clean_registry)
    ion = next(g for g in bad5["subtopic_gates"] if g["subtopic_id"] == "CHEM-ION-VALENCY")
    ion["misconceptions"] = [m for m in ion["misconceptions"] if m["misconception_id"] != "MISC-CHEM-POLYATOMIC-SUBSCRIPT-NO-BRACKET"]
    expect_rejection(bad5, "CHEM_GATE_MISSING_MISCONCEPTION_TRAP")

    # 6. CHEM-FAIL-06: Liquid vs aqueous distinction omitted in CHEM-STATE-SYMBOLS
    bad6 = copy.deepcopy(clean_registry)
    state = next(g for g in bad6["subtopic_gates"] if g["subtopic_id"] == "CHEM-STATE-SYMBOLS")
    state["technical_core"] = [c for c in state["technical_core"] if c["concept_id"] != "CON-CHEM-AQ-VS-LIQUID"]
    expect_rejection(bad6, "CHEM_GATE_MISSING_REQUIRED_CONCEPT")

    # 7. CHEM-FAIL-07: Oxidizing agent inversion trap omitted in CHEM-REDOX-OXIDATION
    bad7 = copy.deepcopy(clean_registry)
    redox = next(g for g in bad7["subtopic_gates"] if g["subtopic_id"] == "CHEM-REDOX-OXIDATION")
    redox["misconceptions"] = [m for m in redox["misconceptions"] if m["misconception_id"] != "MISC-CHEM-OXIDIZING-AGENT-OXIDIZED"]
    expect_rejection(bad7, "CHEM_GATE_MISSING_MISCONCEPTION_TRAP")

    # 8. CHEM-FAIL-08: Equation balancing stripped of formula construction prerequisite
    bad8 = copy.deepcopy(clean_registry)
    bal8 = next(g for g in bad8["subtopic_gates"] if g["subtopic_id"] == "CHEM-EQ-BALANCING")
    bal8["prerequisite_ids"] = [p for p in bal8["prerequisite_ids"] if p != "CHEM-FORMULA-CONSTRUCTION"]
    expect_rejection(bad8, "CHEM_GATE_UNRESOLVED_PREREQUISITE")

    # 9. CHEM-FAIL-09: Johnstone triplet representation omitted in CHEM-REP-TRANSLATION
    bad9 = copy.deepcopy(clean_registry)
    rep = next(g for g in bad9["subtopic_gates"] if g["subtopic_id"] == "CHEM-REP-TRANSLATION")
    rep["representations"] = [{
        "representation_id": "REP-CHEM-GENERIC-PLACEHOLDER",
        "representation_type": "JOHNSTONE_TRIPLET_DIAGRAM",
        "name": "Generic Placeholder Representation",
        "chemistry_encoded": "Generic diagram without triplet bindings",
        "mandatory_labels": ["Label A"],
        "what_cannot_be_omitted": "Mandatory components",
        "common_incorrect_version": "Missing Triplet alignment",
        "verification_method": "Check"
    }]
    expect_rejection(bad9, "CHEM_GATE_MISSING_MANDATORY_REPRESENTATION")

    # 10. CHEM-FAIL-10: Problem family ID in linked_problem_family_ids not defined
    bad10 = copy.deepcopy(clean_registry)
    sym = next(g for g in bad10["subtopic_gates"] if g["subtopic_id"] == "CHEM-SYM-LITERACY")
    sym["linked_problem_family_ids"].append("PF-CHEM-ORPHAN-FAMILY")
    expect_rejection(bad10, "CHEM_GATE_CROSS_REFERENCE_INTEGRITY_FAIL")

    # 11. CHEM-FAIL-11: Duplicate concept ID across distinct subtopics
    bad11 = copy.deepcopy(clean_registry)
    bad11["subtopic_gates"][0]["technical_core"].append({
        "concept_id": bad11["subtopic_gates"][1]["technical_core"][0]["concept_id"],
        "canonical_statement": "Duplicate statement across subtopics for falsifier test.",
        "why_required": "Must fail uniqueness test.",
        "failure_if_omitted": "Fails global invariant."
    })
    expect_rejection(bad11, "CHEM_GATE_DUPLICATE_ID")

    # 12. CHEM-FAIL-12: Incomplete release checklist marked as ENGINEERING_GATE_READY
    bad12 = copy.deepcopy(clean_registry)
    bad12["subtopic_gates"][0]["release_checklist"]["provenance_verified"] = False
    expect_rejection(bad12, "CHEM_GATE_RELEASE_CHECKLIST_INCOMPLETE")

    print("Chemistry Technical Engineering Gate falsification battery: PASS (all 12 mutation falsifiers caught by production validator)")


if __name__ == "__main__":
    reg = load_json(ROOT / "policies" / "chemistry-technical-engineering-gates.v1.json")
    subtopics = validate(reg)
    print(f"Validated {len(subtopics)} Chemistry Technical Engineering subtopic gates: PASS")
    run_falsification_battery()
