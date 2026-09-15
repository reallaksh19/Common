#!/usr/bin/env python3
"""Deterministic validator for the Mathematics Technical Engineering Gate Registry.

Enforces schema contracts, global ID uniqueness, prerequisite graph validity,
cross-reference integrity, subtopic mathematical invariants, and fail-closed readiness.
The canonical registry is a deterministic composition of the generated v1 base and
its exact digest-bound Engineering extensions.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaValidationError

from engineering_registry_composition import (
    BASE_REGISTRY_REL,
    load_canonical_engineering_registry,
)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REGISTRY_PATH = ROOT / BASE_REGISTRY_REL


class MathematicsEngineeringGateValidationError(Exception):
    """Structured validation error with stable machine-readable code."""
    def __init__(self, code: str, message: str, context: dict | None = None):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message
        self.context = context or {}


def load_json(path: Path) -> dict:
    path = Path(path)
    if path.resolve() == CANONICAL_REGISTRY_PATH.resolve():
        return load_canonical_engineering_registry(path)
    return json.loads(path.read_text(encoding="utf-8"))


def validate_gate_schema(registry: dict) -> None:
    schema_path = ROOT / "contracts" / "mathematics-technical-engineering-gate.schema.json"
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    try:
        validator.validate(registry)
    except SchemaValidationError as e:
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_SCHEMA_VIOLATION", str(e), {"path": list(e.path)}
        )


def validate_global_invariants(registry: dict) -> None:
    seen_subtopics: set[str] = set()
    seen_concepts: set[str] = set()
    seen_equations: set[str] = set()
    seen_reps: set[str] = set()
    seen_misconceptions: set[str] = set()

    for gate in registry["subtopic_gates"]:
        sub_id = gate["subtopic_id"]
        if sub_id in seen_subtopics:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_DUPLICATE_ID", f"Duplicate subtopic ID: {sub_id}"
            )
        seen_subtopics.add(sub_id)

        for c in gate["technical_core"]:
            cid = c["concept_id"]
            if cid in seen_concepts:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_DUPLICATE_ID", f"Duplicate concept ID: {cid}"
                )
            seen_concepts.add(cid)

        for eq in gate["mandatory_equations"]:
            eid = eq["equation_id"]
            if eid in seen_equations:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_DUPLICATE_ID", f"Duplicate equation ID: {eid}"
                )
            seen_equations.add(eid)

        for rep in gate["representations"]:
            rid = rep["representation_id"]
            if rid in seen_reps:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_DUPLICATE_ID", f"Duplicate representation ID: {rid}"
                )
            seen_reps.add(rid)

        for m in gate["misconceptions"]:
            mid = m["misconception_id"]
            if mid in seen_misconceptions:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_DUPLICATE_ID", f"Duplicate misconception ID: {mid}"
                )
            seen_misconceptions.add(mid)

    for gate in registry["subtopic_gates"]:
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("MATH-") and prereq not in seen_subtopics:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_UNRESOLVED_PREREQUISITE",
                    f"Subtopic {gate['subtopic_id']} has unresolved prerequisite {prereq}",
                )
            if prereq == gate["subtopic_id"]:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_UNRESOLVED_PREREQUISITE",
                    f"Subtopic {gate['subtopic_id']} has self-dependency",
                )


def validate_subtopic_invariants(gate: dict) -> None:
    sub_id = gate["subtopic_id"]

    if not sub_id.startswith("MATH-"):
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_INVALID_SUBTOPIC_ID", f"Invalid subtopic ID format: {sub_id}"
        )
    if gate.get("maturity") != "ENGINEERING":
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_MATURITY_OVERREACH",
            f"Maturity must be ENGINEERING, got {gate.get('maturity')}",
        )

    defined_fams = {f["family_id"] for f in gate.get("problem_families", [])}
    for lfid in gate.get("linked_problem_family_ids", []):
        if lfid not in defined_fams:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_CROSS_REFERENCE_INTEGRITY_FAIL",
                f"Linked problem family {lfid} not defined in problem_families of {sub_id}",
            )

    concept_ids = {c["concept_id"] for c in gate.get("technical_core", [])}
    equation_ids = {e["equation_id"] for e in gate.get("mandatory_equations", [])}
    representation_ids = {r["representation_id"] for r in gate.get("representations", [])}
    misc_ids = {m["misconception_id"] for m in gate.get("misconceptions", [])}
    prereq_ids = set(gate.get("prerequisite_ids", []))

    if sub_id == "MATH-NUM-RADICALS":
        if "CON-MATH-PRINCIPAL-SQUARE-ROOT-ABS" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-NUM-RADICALS requires principal square root non-negativity concept (CON-MATH-PRINCIPAL-SQUARE-ROOT-ABS)",
            )
        if "EQ-MATH-RADICAL-IDENTITY" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-NUM-RADICALS requires radical identity equation (EQ-MATH-RADICAL-IDENTITY)",
            )

    elif sub_id == "MATH-ALG-POLYNOMIALS":
        if "CON-MATH-FACTOR-THEOREM" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-ALG-POLYNOMIALS requires factor theorem concept (CON-MATH-FACTOR-THEOREM)",
            )
        if "MISC-MATH-FRESHMANS-DREAM" not in misc_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MISCONCEPTION_TRAP",
                "MATH-ALG-POLYNOMIALS requires Freshman's dream trap (MISC-MATH-FRESHMANS-DREAM)",
            )

    elif sub_id == "MATH-LIN-EQUATIONS":
        if "CON-MATH-LINEAR-SYSTEM-CONSISTENCY" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-LIN-EQUATIONS requires linear system consistency concept (CON-MATH-LINEAR-SYSTEM-CONSISTENCY)",
            )
        if "EQ-MATH-RATIO-CONSISTENCY" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-LIN-EQUATIONS requires ratio consistency equation (EQ-MATH-RATIO-CONSISTENCY)",
            )

    elif sub_id == "MATH-QUAD-EQUATIONS":
        if "MATH-ALG-POLYNOMIALS" not in prereq_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_UNRESOLVED_PREREQUISITE",
                "MATH-QUAD-EQUATIONS requires polynomial prerequisite (MATH-ALG-POLYNOMIALS)",
            )
        if "CON-MATH-QUAD-NONZERO-LEAD" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-QUAD-EQUATIONS requires non-zero leading coefficient concept (CON-MATH-QUAD-NONZERO-LEAD)",
            )
        if "EQ-MATH-QUAD-FORMULA" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-QUAD-EQUATIONS requires quadratic formula (EQ-MATH-QUAD-FORMULA)",
            )

    elif sub_id == "MATH-GEO-COORDINATES":
        if "CON-MATH-VERTICAL-SLOPE-UNDEFINED" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-GEO-COORDINATES requires vertical slope undefined concept (CON-MATH-VERTICAL-SLOPE-UNDEFINED)",
            )
        if "EQ-MATH-DISTANCE-FORMULA" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-GEO-COORDINATES requires distance formula (EQ-MATH-DISTANCE-FORMULA)",
            )

    elif sub_id == "MATH-GEO-EUCLID-FOUNDATIONS":
        if "CON-MATH-EUCLID-AXIOM-POSTULATE-DISTINCTION" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-GEO-EUCLID-FOUNDATIONS requires the axiom/postulate distinction concept",
            )
        if "EQ-MATH-EUCLID-CLASSIFICATION" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-GEO-EUCLID-FOUNDATIONS requires its formal classification relation",
            )
        if "REP-MATH-EUCLID-CLASSIFICATION-TABLE" not in representation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_REPRESENTATION",
                "MATH-GEO-EUCLID-FOUNDATIONS requires the definition-classification table representation",
            )
        if "MISC-MATH-EUCLID-AXIOM-POSTULATE-PROOF" not in misc_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MISCONCEPTION_TRAP",
                "MATH-GEO-EUCLID-FOUNDATIONS requires the proof-status misconception repair",
            )

    elif sub_id == "MATH-GEO-TRIANGLES":
        if "CON-MATH-CONGRUENCE-CRITERIA" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-GEO-TRIANGLES requires congruence criteria concept (CON-MATH-CONGRUENCE-CRITERIA)",
            )
        if "MISC-MATH-SSA-CONGRUENCE-FALLACY" not in misc_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MISCONCEPTION_TRAP",
                "MATH-GEO-TRIANGLES requires SSA fallacy trap (MISC-MATH-SSA-CONGRUENCE-FALLACY)",
            )
        if "REP-MATH-GEOMETRIC-TWO-COLUMN-PROOF" not in representation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_REPRESENTATION",
                "MATH-GEO-TRIANGLES requires two-column proof representation (REP-MATH-GEOMETRIC-TWO-COLUMN-PROOF)",
            )

    elif sub_id == "MATH-TRIG-RATIOS":
        if "CON-MATH-TRIG-ACUTE-DOMAIN" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-TRIG-RATIOS requires acute domain concept (CON-MATH-TRIG-ACUTE-DOMAIN)",
            )
        if "EQ-MATH-PYTHAGOREAN-TRIG-IDENTITY" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-TRIG-RATIOS requires Pythagorean identity (EQ-MATH-PYTHAGOREAN-TRIG-IDENTITY)",
            )

    elif sub_id == "MATH-GEO-CIRCLES":
        if "CON-MATH-TANGENT-RADIUS-PERPENDICULAR" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-GEO-CIRCLES requires tangent-radius perpendicularity concept (CON-MATH-TANGENT-RADIUS-PERPENDICULAR)",
            )
        if "EQ-MATH-CYCLIC-QUAD-SUPPLEMENTARY" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-GEO-CIRCLES requires cyclic quad supplementary equation (EQ-MATH-CYCLIC-QUAD-SUPPLEMENTARY)",
            )

    elif sub_id == "MATH-MENS-SURFACES":
        if "CON-MATH-COMPOSITE-INTERFACE-EXCLUSION" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-MENS-SURFACES requires interface exclusion concept (CON-MATH-COMPOSITE-INTERFACE-EXCLUSION)",
            )
        if "EQ-MATH-VOLUME-CONSERVATION" not in equation_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MANDATORY_EQUATION",
                "MATH-MENS-SURFACES requires volume conservation equation (EQ-MATH-VOLUME-CONSERVATION)",
            )

    elif sub_id == "MATH-STAT-PROBABILITY":
        if "CON-MATH-PROBABILITY-BOUNDS" not in concept_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_REQUIRED_CONCEPT",
                "MATH-STAT-PROBABILITY requires probability bounds concept (CON-MATH-PROBABILITY-BOUNDS)",
            )
        if "MISC-MATH-PROBABILITY-OUT-OF-BOUNDS" not in misc_ids:
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_MISSING_MISCONCEPTION_TRAP",
                "MATH-STAT-PROBABILITY requires probability bounds trap (MISC-MATH-PROBABILITY-OUT-OF-BOUNDS)",
            )

    dp = gate["difficulty_profile"]
    dims = [
        "prerequisite_depth", "element_interactivity", "inferential_jump_severity",
        "representation_translation", "model_discrimination", "sign_or_frame_sensitivity",
        "multi_step_dependency", "abstraction", "misconception_density", "synthesis",
    ]
    for d in dims:
        if not (0 <= dp.get(d, -1) <= 3):
            raise MathematicsEngineeringGateValidationError(
                "MATH_GATE_INVALID_DIFFICULTY_PROFILE", f"Dimension {d} must be 0-3"
            )
    if dp.get("maturity") != "ENGINEERING":
        raise MathematicsEngineeringGateValidationError(
            "MATH_GATE_INVALID_DIFFICULTY_PROFILE",
            "Difficulty profile maturity must be ENGINEERING",
        )

    rc = gate["release_checklist"]
    if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
        for req_field, status in rc.items():
            if status is not True:
                raise MathematicsEngineeringGateValidationError(
                    "MATH_GATE_RELEASE_CHECKLIST_INCOMPLETE",
                    f"Release checklist field {req_field} must be True for READY gate in {sub_id}",
                )


def validate(registry: dict) -> list[str]:
    validate_gate_schema(registry)
    validate_global_invariants(registry)
    validated_subtopics = []
    for gate in registry["subtopic_gates"]:
        validate_subtopic_invariants(gate)
        validated_subtopics.append(gate["subtopic_id"])
    return validated_subtopics


def run_falsification_battery() -> None:
    clean_registry = load_json(CANONICAL_REGISTRY_PATH)

    def expect_rejection(mutated: dict, expected_code: str) -> None:
        try:
            validate(mutated)
        except MathematicsEngineeringGateValidationError as err:
            if err.code != expected_code:
                raise AssertionError(
                    f"Expected code {expected_code}, got {err.code}: {err.message}"
                )
            return
        except Exception as err:
            raise AssertionError(
                f"Expected MathematicsEngineeringGateValidationError [{expected_code}], got {type(err).__name__}: {err}"
            )
        raise AssertionError(
            f"Expected validator rejection with code [{expected_code}], but validation passed!"
        )

    bad1 = copy.deepcopy(clean_registry)
    rad = next(g for g in bad1["subtopic_gates"] if g["subtopic_id"] == "MATH-NUM-RADICALS")
    rad["technical_core"] = [c for c in rad["technical_core"] if c["concept_id"] != "CON-MATH-PRINCIPAL-SQUARE-ROOT-ABS"]
    expect_rejection(bad1, "MATH_GATE_MISSING_REQUIRED_CONCEPT")

    bad2 = copy.deepcopy(clean_registry)
    quad = next(g for g in bad2["subtopic_gates"] if g["subtopic_id"] == "MATH-QUAD-EQUATIONS")
    quad["technical_core"] = [c for c in quad["technical_core"] if c["concept_id"] != "CON-MATH-QUAD-NONZERO-LEAD"]
    expect_rejection(bad2, "MATH_GATE_MISSING_REQUIRED_CONCEPT")

    bad3 = copy.deepcopy(clean_registry)
    geo = next(g for g in bad3["subtopic_gates"] if g["subtopic_id"] == "MATH-GEO-COORDINATES")
    geo["technical_core"] = [c for c in geo["technical_core"] if c["concept_id"] != "CON-MATH-VERTICAL-SLOPE-UNDEFINED"]
    expect_rejection(bad3, "MATH_GATE_MISSING_REQUIRED_CONCEPT")

    bad4 = copy.deepcopy(clean_registry)
    coord = next(g for g in bad4["subtopic_gates"] if g["subtopic_id"] == "MATH-GEO-COORDINATES")
    coord["mandatory_equations"] = [e for e in coord["mandatory_equations"] if e["equation_id"] != "EQ-MATH-DISTANCE-FORMULA"]
    expect_rejection(bad4, "MATH_GATE_MISSING_MANDATORY_EQUATION")

    bad5 = copy.deepcopy(clean_registry)
    poly = next(g for g in bad5["subtopic_gates"] if g["subtopic_id"] == "MATH-ALG-POLYNOMIALS")
    poly["misconceptions"] = [m for m in poly["misconceptions"] if m["misconception_id"] != "MISC-MATH-FRESHMANS-DREAM"]
    expect_rejection(bad5, "MATH_GATE_MISSING_MISCONCEPTION_TRAP")

    bad6 = copy.deepcopy(clean_registry)
    tri = next(g for g in bad6["subtopic_gates"] if g["subtopic_id"] == "MATH-GEO-TRIANGLES")
    tri["misconceptions"] = [m for m in tri["misconceptions"] if m["misconception_id"] != "MISC-MATH-SSA-CONGRUENCE-FALLACY"]
    expect_rejection(bad6, "MATH_GATE_MISSING_MISCONCEPTION_TRAP")

    bad7 = copy.deepcopy(clean_registry)
    prob = next(g for g in bad7["subtopic_gates"] if g["subtopic_id"] == "MATH-STAT-PROBABILITY")
    prob["misconceptions"] = [m for m in prob["misconceptions"] if m["misconception_id"] != "MISC-MATH-PROBABILITY-OUT-OF-BOUNDS"]
    expect_rejection(bad7, "MATH_GATE_MISSING_MISCONCEPTION_TRAP")

    bad8 = copy.deepcopy(clean_registry)
    quad8 = next(g for g in bad8["subtopic_gates"] if g["subtopic_id"] == "MATH-QUAD-EQUATIONS")
    quad8["prerequisite_ids"] = [p for p in quad8["prerequisite_ids"] if p != "MATH-ALG-POLYNOMIALS"]
    expect_rejection(bad8, "MATH_GATE_UNRESOLVED_PREREQUISITE")

    bad9 = copy.deepcopy(clean_registry)
    tri9 = next(g for g in bad9["subtopic_gates"] if g["subtopic_id"] == "MATH-GEO-TRIANGLES")
    tri9["representations"] = [{
        "representation_id": "REP-MATH-GENERIC-PLACEHOLDER",
        "representation_type": "GEOMETRIC_TWO_COLUMN_PROOF",
        "name": "Generic Placeholder Representation",
        "math_encoded": "Generic proof schema without two-column statements and reasons",
        "mandatory_labels": ["Statement", "Reason"],
        "what_cannot_be_omitted": "Mandatory proof steps",
        "common_incorrect_version": "Missing step justifications",
        "verification_method": "Check",
    }]
    expect_rejection(bad9, "MATH_GATE_MISSING_MANDATORY_REPRESENTATION")

    bad10 = copy.deepcopy(clean_registry)
    rad10 = next(g for g in bad10["subtopic_gates"] if g["subtopic_id"] == "MATH-NUM-RADICALS")
    rad10["linked_problem_family_ids"].append("PF-MATH-ORPHAN-FAMILY")
    expect_rejection(bad10, "MATH_GATE_CROSS_REFERENCE_INTEGRITY_FAIL")

    bad11 = copy.deepcopy(clean_registry)
    bad11["subtopic_gates"][0]["technical_core"].append({
        "concept_id": bad11["subtopic_gates"][1]["technical_core"][0]["concept_id"],
        "canonical_statement": "Duplicate statement across subtopics for falsifier test.",
        "why_required": "Must fail uniqueness test.",
        "failure_if_omitted": "Fails global invariant.",
    })
    expect_rejection(bad11, "MATH_GATE_DUPLICATE_ID")

    bad12 = copy.deepcopy(clean_registry)
    bad12["subtopic_gates"][0]["release_checklist"]["provenance_verified"] = False
    expect_rejection(bad12, "MATH_GATE_RELEASE_CHECKLIST_INCOMPLETE")

    euclid = lambda doc: next(g for g in doc["subtopic_gates"] if g["subtopic_id"] == "MATH-GEO-EUCLID-FOUNDATIONS")

    bad13 = copy.deepcopy(clean_registry)
    e13 = euclid(bad13)
    e13["technical_core"] = [c for c in e13["technical_core"] if c["concept_id"] != "CON-MATH-EUCLID-AXIOM-POSTULATE-DISTINCTION"]
    expect_rejection(bad13, "MATH_GATE_MISSING_REQUIRED_CONCEPT")

    bad14 = copy.deepcopy(clean_registry)
    e14 = euclid(bad14)
    e14["mandatory_equations"] = [e for e in e14["mandatory_equations"] if e["equation_id"] != "EQ-MATH-EUCLID-CLASSIFICATION"]
    expect_rejection(bad14, "MATH_GATE_MISSING_MANDATORY_EQUATION")

    bad15 = copy.deepcopy(clean_registry)
    e15 = euclid(bad15)
    e15["representations"] = [r for r in e15["representations"] if r["representation_id"] != "REP-MATH-EUCLID-CLASSIFICATION-TABLE"]
    expect_rejection(bad15, "MATH_GATE_MISSING_MANDATORY_REPRESENTATION")

    bad16 = copy.deepcopy(clean_registry)
    e16 = euclid(bad16)
    e16["misconceptions"] = [m for m in e16["misconceptions"] if m["misconception_id"] != "MISC-MATH-EUCLID-AXIOM-POSTULATE-PROOF"]
    expect_rejection(bad16, "MATH_GATE_MISSING_MISCONCEPTION_TRAP")

    print(
        "Mathematics Technical Engineering Gate falsification battery: PASS "
        "(all 16 mutation falsifiers caught by production validator)"
    )


if __name__ == "__main__":
    reg = load_json(CANONICAL_REGISTRY_PATH)
    subtopics = validate(reg)
    print(f"Validated {len(subtopics)} Mathematics Technical Engineering subtopic gates: PASS")
    run_falsification_battery()
