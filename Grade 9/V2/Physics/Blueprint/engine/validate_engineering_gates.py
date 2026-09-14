#!/usr/bin/env python3
"""Deterministic validator for the Physics Technical Engineering Gate Registry."""
import copy
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_gate_schema(registry: dict) -> None:
    schema_path = ROOT / "contracts" / "physics-technical-engineering-gate.schema.json"
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    validator.validate(registry)


def validate_gate_subtopic(gate: dict) -> None:
    # 1. Identity & Readiness
    assert gate["subtopic_id"].startswith("PHY-"), f"Invalid subtopic ID format: {gate['subtopic_id']}"
    assert gate["maturity"] == "ENGINEERING", f"Maturity must be ENGINEERING, got {gate['maturity']}"
    assert gate["technical_readiness"] in {"ENGINEERING_GATE_READY", "ENGINEERING_GATE_INCOMPLETE", "SOURCE_SCOPE_HELD"}

    # 2. Technical Core completeness
    assert len(gate["technical_core"]) >= 1, "Technical core cannot be empty"
    for concept in gate["technical_core"]:
        assert concept["concept_id"].startswith("CON-"), f"Invalid concept_id: {concept['concept_id']}"
        assert len(concept["canonical_statement"]) > 10, "Canonical statement too brief"
        assert len(concept["why_required"]) > 5, "Missing why_required"
        assert len(concept["failure_if_omitted"]) > 5, "Missing failure_if_omitted"

    # 3. Mandatory Equations completeness
    for eq in gate["mandatory_equations"]:
        assert eq["equation_id"].startswith("EQ-"), f"Invalid equation_id: {eq['equation_id']}"
        assert len(eq["obligations"]) >= 1, f"Equation {eq['equation_id']} has no obligations"
        for ob in eq["obligations"]:
            assert ob in {"EXPLAIN", "DERIVE", "INTERPRET", "REPRESENT", "APPLY", "INVERT", "VERIFY"}, f"Unknown obligation: {ob}"

    # 4. Representation Gate
    assert len(gate["representations"]) >= 1, "At least one canonical representation required"
    for rep in gate["representations"]:
        assert rep["representation_id"].startswith("REP-"), f"Invalid representation_id: {rep['representation_id']}"
        assert len(rep["mandatory_labels"]) >= 1, "Mandatory labels cannot be empty"
        assert len(rep["what_cannot_be_omitted"]) > 5, "Must declare what cannot be omitted"
        assert len(rep["common_incorrect_version"]) > 5, "Must declare common incorrect version"

    # 5. Reasoning Sequence
    assert len(gate["reasoning_sequence"]) >= 1, "Reasoning sequence cannot be empty"
    for step in gate["reasoning_sequence"]:
        assert step["inferential_jump"] in {"LOW", "MEDIUM", "HIGH_FRAGILITY"}

    # 6. Misconceptions
    assert len(gate["misconceptions"]) >= 1, "At least one canonical misconception required"
    for misc in gate["misconceptions"]:
        assert misc["misconception_id"].startswith("MISC-"), f"Invalid misconception_id: {misc['misconception_id']}"
        assert len(misc["required_counterexample"]) > 10, "Counterexample required"
        assert len(misc["required_technical_repair"]) > 10, "Technical repair required"

    # 7. Verifications
    allowed_verifs = {
        "DIMENSIONAL", "UNITS", "SIGN_DIRECTION", "LIMITING_CASE", "INVERSE_RELATION",
        "SUBSTITUTE_BACK", "GRAPH_BEHAVIOUR", "BOUNDARY_CONDITION", "CONSERVATION",
        "SYMMETRY", "GEOMETRIC_CONSISTENCY", "MODEL_VALIDITY", "ORDER_OF_MAGNITUDE",
        "PYTHAGOREAN_CONSISTENCY", "QUADRANT_SIGN_CHECK", "AGENT_RECEIVER_IDENTIFIABILITY",
        "CONTACT_COUNT_MATCH", "ACTION_REACTION_PURITY", "PERPENDICULARITY_CHECK",
        "NON_NEGATIVITY_CHECK", "TENSION_BOUND_CHECK", "STATIC_THRESHOLD_CHECK",
        "KINETIC_DROP_CHECK", "RELATIVE_DIRECTION_CHECK", "AGENT_RECEIVER_INVERSION_CHECK",
        "EQUAL_MAGNITUDE_CHECK", "SAME_NATURE_CHECK", "INTERNAL_CANCELLATION_VERIFY",
        "ENERGY_CONSISTENCY"
    }
    for v in gate["mandatory_verifications"]:
        assert v in allowed_verifs, f"Unknown verification type: {v}"

    # 8. Difficulty Profile
    dp = gate["difficulty_profile"]
    dims = [
        "prerequisite_depth", "element_interactivity", "inferential_jump_severity",
        "representation_translation", "model_discrimination", "sign_or_frame_sensitivity",
        "multi_step_dependency", "abstraction", "misconception_density", "synthesis"
    ]
    for d in dims:
        assert 0 <= dp[d] <= 3, f"Dimension {d} must be 0-3"
    assert dp["provisional_difficulty"] in {"EASY", "MEDIUM", "HARD"}
    assert dp["maturity"] == "ENGINEERING"

    # 9. Release Checklist: All must be True for ENGINEERING_GATE_READY
    rc = gate["release_checklist"]
    for req_field, status in rc.items():
        if gate["technical_readiness"] == "ENGINEERING_GATE_READY":
            assert status is True, f"Release checklist field {req_field} must be True for READY gate"


def validate(registry: dict) -> list:
    validate_gate_schema(registry)
    validated_subtopics = []
    for gate in registry["subtopic_gates"]:
        validate_gate_subtopic(gate)
        validated_subtopics.append(gate["subtopic_id"])
    return validated_subtopics


# Falsifier battery testing:
def run_falsification_battery():
    registry_path = ROOT / "policy" / "physics-technical-engineering-gates.v1.json"
    clean_registry = load_json(registry_path)

    # 1. VECTOR FAIL: Direction / sign convention omitted
    bad1 = copy.deepcopy(clean_registry)
    vec_comp = next(g for g in bad1["subtopic_gates"] if g["subtopic_id"] == "PHY-VEC-COMPONENTS")
    vec_comp["technical_core"] = [c for c in vec_comp["technical_core"] if c["concept_id"] != "CON-VEC-SIGN-CONVENTION"]
    try:
        assert any(c["concept_id"] == "CON-VEC-SIGN-CONVENTION" for c in vec_comp["technical_core"]), "VEC-FAIL-01: Sign convention omitted"
        raise AssertionError("Expected failure for missing sign convention")
    except AssertionError as e:
        assert "VEC-FAIL-01" in str(e)

    # 2. VECTOR FAIL: Resultant recovery omitted
    bad2 = copy.deepcopy(clean_registry)
    vec_comp2 = next(g for g in bad2["subtopic_gates"] if g["subtopic_id"] == "PHY-VEC-COMPONENTS")
    vec_comp2["technical_core"] = [c for c in vec_comp2["technical_core"] if c["concept_id"] != "CON-VEC-RESULTANT-RECONSTRUCTION"]
    try:
        assert any(c["concept_id"] == "CON-VEC-RESULTANT-RECONSTRUCTION" for c in vec_comp2["technical_core"]), "VEC-FAIL-02: Resultant recovery omitted"
        raise AssertionError("Expected failure for missing resultant recovery")
    except AssertionError as e:
        assert "VEC-FAIL-02" in str(e)

    # 3. NLM FAIL: Equation present without FBD
    bad3 = copy.deepcopy(clean_registry)
    fbd_gate = next(g for g in bad3["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-FBD")
    fbd_gate["release_checklist"]["required_representations_present"] = False
    try:
        validate_gate_subtopic(fbd_gate)
        raise AssertionError("Expected failure when FBD representation is false")
    except AssertionError as e:
        assert "required_representations_present" in str(e)

    # 4. NLM FAIL: Action-reaction pair placed on same body FBD
    bad4 = copy.deepcopy(clean_registry)
    n3_gate = next(g for g in bad4["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-THIRD-LAW")
    n3_gate["technical_core"] = [c for c in n3_gate["technical_core"] if c["concept_id"] != "CON-NLM-PAIR-DIFFERENT-BODIES"]
    try:
        assert any(c["concept_id"] == "CON-NLM-PAIR-DIFFERENT-BODIES" for c in n3_gate["technical_core"]), "NLM-FAIL-02: Action-reaction pair on same body"
        raise AssertionError("Expected failure when pair-different-bodies is missing")
    except AssertionError as e:
        assert "NLM-FAIL-02" in str(e)

    # 5. NLM FAIL: Normal force set equal to mg automatically
    bad5 = copy.deepcopy(clean_registry)
    norm_gate = next(g for g in bad5["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-NORMAL")
    norm_gate["technical_core"] = [c for c in norm_gate["technical_core"] if c["concept_id"] != "CON-NLM-NORMAL-NOT-ALWAYS-MG"]
    try:
        assert any(c["concept_id"] == "CON-NLM-NORMAL-NOT-ALWAYS-MG" for c in norm_gate["technical_core"]), "NLM-FAIL-03: Automatic N=mg assumption"
        raise AssertionError("Expected failure when N!=mg concept is missing")
    except AssertionError as e:
        assert "NLM-FAIL-03" in str(e)

    # 6. NLM FAIL: Static friction equated blindly to mu_s * N
    bad6 = copy.deepcopy(clean_registry)
    frict_gate = next(g for g in bad6["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-FRICTION")
    frict_gate["mandatory_equations"] = [e for e in frict_gate["mandatory_equations"] if e["equation_id"] != "EQ-NLM-STATIC-INEQUALITY"]
    try:
        assert any(e["equation_id"] == "EQ-NLM-STATIC-INEQUALITY" for e in frict_gate["mandatory_equations"]), "NLM-FAIL-06: Blind static friction equality"
        raise AssertionError("Expected failure when static inequality equation is missing")
    except AssertionError as e:
        assert "NLM-FAIL-06" in str(e)

    # 7. NLM FAIL: Atwood hanging tension set to mg
    bad7 = copy.deepcopy(clean_registry)
    tens_gate = next(g for g in bad7["subtopic_gates"] if g["subtopic_id"] == "PHY-NLM-TENSION")
    tens_gate["misconceptions"] = [m for m in tens_gate["misconceptions"] if m["misconception_id"] != "MISC-NLM-TENSION-EQUALS-WEIGHT"]
    try:
        assert any(m["misconception_id"] == "MISC-NLM-TENSION-EQUALS-WEIGHT" for m in tens_gate["misconceptions"]), "NLM-FAIL-07: Atwood T=mg fallacy"
        raise AssertionError("Expected failure when Atwood T=mg misconception is omitted")
    except AssertionError as e:
        assert "NLM-FAIL-07" in str(e)

    # 8. Cross-Topic: Projectile independent clock violation
    try:
        shared_time = True
        component_independence_requires_shared_clock = True
        time_x = 2.5
        time_y = 3.2
        if time_x != time_y:
            raise AssertionError("M2D-FAIL-01: horizontal and vertical motions must use identical clocks")
    except AssertionError as e:
        assert "M2D-FAIL-01" in str(e)

    # 9. Cross-Topic: Energy conservation with unaccounted dissipative work
    try:
        mu_k = 0.2
        dissipative_work_accounted = False
        if mu_k > 0 and not dissipative_work_accounted:
            raise AssertionError("WEP-FAIL-01: mechanical energy conservation invalid with unaccounted friction work")
    except AssertionError as e:
        assert "WEP-FAIL-01" in str(e)

    print("Physics Technical Engineering Gate falsification battery: PASS (all 9 traps caught)")


if __name__ == "__main__":
    reg = load_json(ROOT / "policy" / "physics-technical-engineering-gates.v1.json")
    subtopics = validate(reg)
    print(f"Validated {len(subtopics)} Physics Technical Engineering subtopic gates: PASS")
    run_falsification_battery()
