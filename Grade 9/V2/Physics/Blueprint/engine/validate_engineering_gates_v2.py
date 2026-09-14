#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


class GateValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def fail(code: str, message: str):
    raise GateValidationError(code, message)


EXPECTED = {
    "PHY-VEC-BASICS": {
        "invariants": {"INV-VEC-SCALAR-VECTOR-DISTINCTION", "INV-VEC-MAGNITUDE-NONNEGATIVE", "INV-VEC-DIRECTION-REFERENCE"},
        "concepts": {"CON-VEC-SCALAR-VECTOR", "CON-VEC-DIRECTION-REFERENCE"},
        "relations": {"EQ-VEC-MAGNITUDE-NONNEGATIVE"},
        "representations": {"REP-VEC-DIRECTED-SEGMENT"},
    },
    "PHY-VEC-ADD-SUB": {
        "invariants": {"INV-VEC-HEAD-TO-TAIL", "INV-VEC-SUBTRACTION-NEGATIVE", "INV-VEC-RESULTANT-MEANING"},
        "relations": {"EQ-VEC-SUM"},
        "representations": {"REP-VEC-HEAD-TO-TAIL"},
    },
    "PHY-VEC-COMPONENTS": {
        "invariants": {"INV-VEC-AXES-DECLARED", "INV-VEC-COMPONENT-SIGNS", "INV-VEC-COMPONENT-TO-RESULTANT"},
        "concepts": {"CON-VEC-SIGN-CONVENTION", "CON-VEC-RESULTANT-RECONSTRUCTION"},
        "relations": {"EQ-VEC-COMPONENTS", "EQ-VEC-RECONSTRUCT"},
        "representations": {"REP-VEC-COMPONENT-TRIANGLE"},
    },
    "PHY-NLM-INTERACTION": {
        "invariants": {"INV-NLM-FORCE-HAS-AGENT-RECEIVER", "INV-NLM-CONTACT-VS-NONCONTACT"},
        "concepts": {"CON-NLM-AGENT-RECEIVER"},
        "representations": {"REP-NLM-INTERACTION-LINK"},
    },
    "PHY-NLM-FBD": {
        "invariants": {"INV-NLM-SYSTEM-SELECTED-FIRST", "INV-NLM-FBD-FORCES-ON-SYSTEM-ONLY", "INV-NLM-FBD-COMPLETE"},
        "concepts": {"CON-NLM-SYSTEM-BOUNDARY"},
        "representations": {"REP-NLM-FBD"},
    },
    "PHY-NLM-FIRST-LAW": {
        "invariants": {"INV-NLM-EQUILIBRIUM-A-ZERO", "INV-NLM-ZERO-NET-FORCE-NOT-ZERO-VELOCITY", "INV-NLM-INERTIAL-FRAME"},
        "relations": {"EQ-NLM-EQUILIBRIUM"},
    },
    "PHY-NLM-SECOND-LAW": {
        "invariants": {"INV-NLM-FBD-BEFORE-EQUATION", "INV-NLM-AXIS-WISE-SUM-F", "INV-NLM-SAME-SYSTEM-SAME-AXES"},
        "relations": {"EQ-NLM-SECOND-X", "EQ-NLM-SECOND-Y"},
        "representations": {"REP-NLM-FBD-AXES"},
        "prerequisites": {"PHY-NLM-FBD", "PHY-VEC-COMPONENTS"},
    },
    "PHY-NLM-THIRD-LAW": {
        "invariants": {"INV-NLM-THIRD-DISTINCT-BODIES", "INV-NLM-THIRD-EQUAL-OPPOSITE", "INV-NLM-THIRD-SAME-INTERACTION"},
        "concepts": {"CON-NLM-PAIR-DIFFERENT-BODIES"},
        "relations": {"EQ-NLM-THIRD"},
    },
    "PHY-NLM-NORMAL": {
        "invariants": {"INV-NLM-NORMAL-PERPENDICULAR", "INV-NLM-NORMAL-NOT-ALWAYS-MG"},
        "concepts": {"CON-NLM-NORMAL-NOT-ALWAYS-MG"},
    },
    "PHY-NLM-TENSION": {
        "invariants": {"INV-NLM-TENSION-STRING-MODEL", "INV-NLM-TENSION-NOT-ALWAYS-MG", "INV-NLM-CONSTRAINT-KINEMATICS"},
        "concepts": {"CON-NLM-TENSION-MODEL"},
    },
    "PHY-NLM-FRICTION": {
        "invariants": {"INV-NLM-STATIC-FRICTION-INEQUALITY", "INV-NLM-FRICTION-OPPOSES-RELATIVE-TENDENCY", "INV-NLM-KINETIC-AFTER-SLIDING"},
        "concepts": {"CON-NLM-STATIC-FRICTION-ADAPTIVE"},
        "relations": {"EQ-NLM-STATIC-INEQUALITY", "EQ-NLM-KINETIC-FRICTION"},
    },
    "PHY-NLM-CONNECTED": {
        "invariants": {"INV-NLM-CONNECTED-SYSTEM-CHOICE", "INV-NLM-INTERNAL-EXTERNAL-DISTINCTION", "INV-NLM-CONSTRAINT-CONSISTENCY"},
        "relations": {"EQ-NLM-CONNECTED-SYSTEM"},
    },
    "PHY-M2D-PROJECTILE-COMPONENTS": {
        "invariants": {"INV-M2D-FRAME-DECLARED", "INV-M2D-LAUNCH-COMPONENTS-SIGNED", "INV-M2D-GRAVITY-VERTICAL-ONLY"},
        "relations": {"EQ-M2D-X", "EQ-M2D-Y"},
        "representations": {"REP-M2D-PROJECTILE-COMPONENTS"},
        "prerequisites": {"PHY-VEC-COMPONENTS"},
    },
    "PHY-M2D-SHARED-CLOCK": {
        "invariants": {"INV-M2D-SHARED-CLOCK", "INV-M2D-SAME-EVENT-STATE"},
        "concepts": {"CON-M2D-SHARED-CLOCK"},
        "relations": {"EQ-M2D-SHARED-TIME"},
        "verifications": {"SHARED_CLOCK"},
    },
    "PHY-M2D-MOVING-LAUNCHER": {
        "invariants": {"INV-M2D-VELOCITY-FRAMES-NAMED", "INV-M2D-GALILEAN-ADD-BEFORE-PROJECTILE", "INV-M2D-INHERITED-HORIZONTAL-MOTION", "INV-M2D-ZERO-SOURCE-LIMIT"},
        "concepts": {"CON-M2D-FRAME-NAMING", "CON-M2D-INHERITED-MOTION"},
        "relations": {"EQ-M2D-GALILEAN-ADD"},
        "representations": {"REP-M2D-FRAME-VELOCITY-TRIANGLE"},
        "prerequisites": {"PHY-VEC-COMPONENTS", "PHY-M2D-PROJECTILE-COMPONENTS", "PHY-M2D-SHARED-CLOCK"},
        "linked_buckets": {"M2D-SBA-23"},
        "verifications": {"INVERSE_RELATION", "LIMITING_CASE", "SHARED_CLOCK"},
    },
}


def ids(items, key):
    return {item[key] for item in items}


def require_subset(gate_id: str, category: str, actual: set[str], expected: set[str]):
    missing = expected - actual
    if missing:
        fail("E_GATE_INVARIANT_MISSING", f"{gate_id} missing {category}: {sorted(missing)}")


def validate(registry: dict) -> list[str]:
    try:
        schema = load("contracts/physics-technical-engineering-gate-v2.schema.json")
        jsonschema.validate(registry, schema)
    except jsonschema.ValidationError as exc:
        fail("E_GATE_SCHEMA", exc.message)

    if registry["maturity"] != "ENGINEERING":
        fail("E_GATE_MATURITY", "technical engineering registry may not claim validated maturity")

    gates = registry["gates"]
    gate_map = {g["subtopic_id"]: g for g in gates}
    if len(gate_map) != len(gates):
        fail("E_GATE_DUPLICATE_ID", "duplicate subtopic_id")

    missing_canonical = set(EXPECTED) - set(gate_map)
    if missing_canonical:
        fail("E_GATE_CANONICAL_SET", f"missing absorbed canonical gates: {sorted(missing_canonical)}")

    global_ids: dict[str, str] = {}
    relation_ids = set()
    for gate in gates:
        for key, prefix_key in [("concepts", "concept_id"), ("relations", "relation_id"), ("representations", "representation_id"), ("misconceptions", "misconception_id")]:
            for item in gate[key]:
                value = item[prefix_key]
                if value in global_ids:
                    fail("E_GATE_DUPLICATE_ASSET_ID", f"{value} appears in both {global_ids[value]} and {gate['subtopic_id']}")
                global_ids[value] = gate["subtopic_id"]
                if key == "relations":
                    relation_ids.add(value)

    for gate in gates:
        gid = gate["subtopic_id"]
        authority = gate["authority_basis"]
        if any(a["claim_class"] == "SOURCE_SCOPE_HELD" for a in authority) and gate["status"] == "ENGINEERING_GATE_READY":
            fail("E_GATE_SCOPE_HELD_READY", f"{gid} is READY while authority scope is held")

        for c in gate["concepts"]:
            if c["authority_ref"] >= len(authority):
                fail("E_GATE_AUTHORITY_REF", f"{gid} concept {c['concept_id']} has invalid authority_ref")

        for prereq in gate["prerequisites"]:
            if prereq.startswith("PHY-") and prereq not in gate_map:
                fail("E_GATE_MISSING_PREREQ", f"{gid} references missing prerequisite {prereq}")

        for rep in gate["representations"]:
            unknown = set(rep["relation_bindings"]) - relation_ids
            if unknown:
                fail("E_GATE_REP_BINDING", f"{gid} representation {rep['representation_id']} references unknown relations {sorted(unknown)}")

        if gate["difficulty_engineering"]["maturity"] != "ENGINEERING":
            fail("E_GATE_DIFFICULTY_MATURITY", f"{gid} difficulty may not claim empirical validation")

        spec = EXPECTED.get(gid, {})
        require_subset(gid, "invariants", set(gate["required_invariants"]), spec.get("invariants", set()))
        require_subset(gid, "concepts", ids(gate["concepts"], "concept_id"), spec.get("concepts", set()))
        require_subset(gid, "relations", ids(gate["relations"], "relation_id"), spec.get("relations", set()))
        require_subset(gid, "representations", ids(gate["representations"], "representation_id"), spec.get("representations", set()))
        require_subset(gid, "prerequisites", set(gate["prerequisites"]), spec.get("prerequisites", set()))
        require_subset(gid, "linked_buckets", set(gate["linked_buckets"]), spec.get("linked_buckets", set()))
        require_subset(gid, "verifications", set(gate["verifications"]), spec.get("verifications", set()))

        # Semantic release checks that cannot be satisfied by a boolean self-assertion.
        if gate["status"] == "ENGINEERING_GATE_READY":
            if not gate["concepts"] or not gate["representations"] or not gate["reasoning_sequence"] or not gate["misconceptions"] or not gate["verifications"] or not gate["problem_families"]:
                fail("E_GATE_INCOMPLETE_READY", f"{gid} is READY but a mandatory technical section is empty")

    return [g["subtopic_id"] for g in gates]


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "policy/physics-technical-engineering-gates.v2.json"
    registry = load(rel)
    gate_ids = validate(registry)
    print(json.dumps({"status":"PASS","registry_id":registry["registry_id"],"gate_count":len(gate_ids),"gates":gate_ids}, indent=2))


if __name__ == "__main__":
    main()
