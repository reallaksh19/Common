#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from build_physics_engineering_gate_registry_v3 import build_registry, digest  # noqa: E402
from validate_engineering_gates_v3 import PhysicsEngineeringGateV3Error, validate  # noqa: E402


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def gate(doc: dict, gid: str) -> dict:
    return next(row for row in doc["gates"] if row["subtopic_id"] == gid)


def must_fail(doc: dict, code: str) -> None:
    try:
        validate(doc)
    except PhysicsEngineeringGateV3Error as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def physics_closure(doc: dict, roots: list[str]) -> set[str]:
    rows = {g["subtopic_id"]: g for g in doc["gates"]}
    seen: set[str] = set()
    def walk(gid: str) -> None:
        if gid in seen:
            return
        seen.add(gid)
        for prereq in rows[gid]["prerequisites"]:
            if prereq.startswith("PHY-"):
                walk(prereq)
    for root in roots:
        walk(root)
    return seen


REG = build_registry()
V2 = load("policy/physics-technical-engineering-gates.v2.json")
GRAV_V1 = load("policy/physics-technical-engineering-gates.gravity.v1.json")
BASE15 = {g["subtopic_id"] for g in V2["gates"]}
GRAVITY = {g["subtopic_id"] for g in GRAV_V1["gates"]}
SBA04 = {
    "PHY-M2D-VELOCITY-EVOLUTION",
    "PHY-M2D-VELOCITY-DIRECTION",
    "PHY-M2D-SPEED-MAGNITUDE",
    "PHY-M2D-SAME-HEIGHT-VELOCITY",
    "PHY-M2D-PERPENDICULAR-VELOCITY",
    "PHY-M2D-SPEED-AT-HEIGHT",
}
RELATIVE = {"PHY-M2D-RELATIVE-VELOCITY"}
WORK_ENERGY = {"PHY-WORK-ENERGY-POWER", "PHY-ENERGY-CONSERVATION-LAW"}
FULL = BASE15 | GRAVITY | SBA04 | RELATIVE | WORK_ENERGY
SBA23_CLOSURE = {"PHY-VEC-BASICS","PHY-VEC-ADD-SUB","PHY-VEC-COMPONENTS","PHY-M2D-PROJECTILE-COMPONENTS","PHY-M2D-SHARED-CLOCK","PHY-M2D-MOVING-LAUNCHER"}
GRAV_CLOSURE = {"PHY-VEC-BASICS","PHY-VEC-ADD-SUB","PHY-VEC-COMPONENTS","PHY-NLM-INTERACTION","PHY-NLM-FBD","PHY-NLM-FIRST-LAW","PHY-NLM-SECOND-LAW","PHY-NLM-THIRD-LAW","PHY-GRAV-FORCE","PHY-GRAV-FIELD"}
SBA04_CLOSURE = {"PHY-VEC-BASICS","PHY-VEC-ADD-SUB","PHY-VEC-COMPONENTS","PHY-M2D-PROJECTILE-COMPONENTS","PHY-M2D-SHARED-CLOCK"} | SBA04
RELATIVE_CLOSURE = {"PHY-VEC-BASICS","PHY-VEC-ADD-SUB","PHY-VEC-COMPONENTS","PHY-M2D-RELATIVE-VELOCITY"}
WORK_ENERGY_CLOSURE = {"PHY-VEC-BASICS","PHY-VEC-ADD-SUB","PHY-VEC-COMPONENTS","PHY-NLM-INTERACTION","PHY-NLM-FBD","PHY-NLM-FIRST-LAW","PHY-NLM-SECOND-LAW","PHY-WORK-ENERGY-POWER"}
CONSERVATION_CLOSURE = WORK_ENERGY_CLOSURE | {"PHY-NLM-NORMAL","PHY-NLM-FRICTION","PHY-ENERGY-CONSERVATION-LAW"}

# Deterministic canonical assembly and validator-derived readiness.
assert REG == build_registry()
assert digest(REG) == digest(build_registry())
report = validate(REG)
assert report["status"] == "PASS"
assert report["registry_id"] == "PHYSICS-TECHNICAL-ENGINEERING-GATES-V3"
assert report["gate_count"] == 26
assert report["all_engineering_ready"] is True
assert {x["gate_id"] for x in report["gate_states"]} == FULL
assert all("status" not in g for g in REG["gates"])

# Exact v2 -> v3 identity preservation for the original 15 gates.
for gid in BASE15:
    old, new = gate(V2, gid), gate(REG, gid)
    assert new["prerequisites"] == old["prerequisites"], gid
    assert new["linked_buckets"] == old["linked_buckets"], gid
    assert new["applicable_cores"] == old["applicable_cores"], gid
    assert new["required_invariants"] == old["required_invariants"], gid
    assert {x["concept_id"] for x in new["concepts"]} == {x["concept_id"] for x in old["concepts"]}, gid
    assert {x["relation_id"] for x in new["relations"]} == {x["relation_id"] for x in old["relations"]}, gid
    assert {x["representation_id"] for x in new["representations"]} == {x["representation_id"] for x in old["representations"]}, gid
    assert new["verifications"] == old["verifications"], gid
    assert {x["family_id"] for x in new["problem_families"]} == set(old["problem_families"]), gid
    assert new["difficulty_engineering"] == old["difficulty_engineering"], gid

# Exact Gravity v1 extension -> canonical v3 identity preservation.
for gid in GRAVITY:
    old, new = gate(GRAV_V1, gid), gate(REG, gid)
    assert new["prerequisites"] == old["prerequisites"], gid
    assert new["applicable_cores"] == old["applicable_cores"], gid
    assert new["required_invariants"] == old["required_invariants"], gid
    assert {x["concept_id"] for x in new["concepts"]} == {x["concept_id"] for x in old["concepts"]}, gid
    assert {x["relation_id"] for x in new["relations"]} == {x["relation_id"] for x in old["relations"]}, gid
    assert {x["representation_id"] for x in new["representations"]} == {x["representation_id"] for x in old["representations"]}, gid
    assert new["verifications"] == old["verifications"], gid
    assert {x["family_id"] for x in new["problem_families"]} == set(old["problem_families"]), gid
    assert new["difficulty_engineering"] == old["difficulty_engineering"], gid

# SBA04 gates are source-derived from the real bucket and all carry explicit bucket custody.
for gid in SBA04:
    g = gate(REG, gid)
    assert g["scope_state"] == "ACTIVE"
    assert "M2D-SBA-04" in g["linked_buckets"]
    assert any(a["source_ref"].startswith("Core1A/registry/physics-core1a-motion-in-a-plane-sba04-20pct-v1.json") for a in g["authority_basis"])
    assert g["reasoning_sequence"] and g["required_transformations"] and g["misconceptions"] and g["problem_families"]

# Generic relative velocity is source-defined from the pinned PR383 discovery, not a case fixture.
relative = gate(REG, "PHY-M2D-RELATIVE-VELOCITY")
assert relative["scope_state"] == "ACTIVE"
assert relative["linked_buckets"] == []
assert relative["prerequisites"] == ["PHY-VEC-ADD-SUB", "PHY-VEC-COMPONENTS"]
assert any(a["source_ref"].endswith("#PHY-KIN-RELATIVE-2D") for a in relative["authority_basis"])
assert {r["relation_id"] for r in relative["relations"]} == {"EQ-M2D-RELATIVE-VELOCITY", "EQ-M2D-RIVER-CROSSING-TIME", "EQ-M2D-RIVER-DRIFT"}

# Work-Energy growth uses generic V3 semantics, including balance and reference checks.
work = gate(REG, "PHY-WORK-ENERGY-POWER")
conservation = gate(REG, "PHY-ENERGY-CONSERVATION-LAW")
assert work["scope_state"] == "ACTIVE"
assert conservation["scope_state"] == "ACTIVE"
assert conservation["prerequisites"] == ["PHY-WORK-ENERGY-POWER", "PHY-NLM-FRICTION"]
assert {"ENERGY_ACCOUNTING", "REFERENCE_CONSISTENCY"}.issubset(set(conservation["verifications"]))

# Subject growth may not pollute older scoped closures.
assert physics_closure(REG, ["PHY-M2D-MOVING-LAUNCHER"]) == SBA23_CLOSURE
assert physics_closure(REG, ["PHY-GRAV-FIELD"]) == GRAV_CLOSURE
assert physics_closure(REG, sorted(SBA04)) == SBA04_CLOSURE
assert physics_closure(REG, ["PHY-M2D-RELATIVE-VELOCITY"]) == RELATIVE_CLOSURE
assert physics_closure(REG, ["PHY-WORK-ENERGY-POWER"]) == WORK_ENERGY_CLOSURE
assert physics_closure(REG, ["PHY-ENERGY-CONSERVATION-LAW"]) == CONSERVATION_CLOSURE

# Shared problem-family IDs are legal cross-gate linkage, semantic authority IDs are not.
assert "PF-NLM-INCLINE" in {x["family_id"] for x in gate(REG, "PHY-NLM-SECOND-LAW")["problem_families"]}
assert "PF-NLM-INCLINE" in {x["family_id"] for x in gate(REG, "PHY-NLM-NORMAL")["problem_families"]}

# Generic/base falsifiers retained.
bad=copy.deepcopy(REG); gate(bad,"PHY-VEC-COMPONENTS")["required_invariants"].remove("INV-VEC-COMPONENT-SIGNS"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); g=gate(bad,"PHY-VEC-COMPONENTS"); g["relations"]=[r for r in g["relations"] if r["relation_id"]!="EQ-VEC-RECONSTRUCT"]; must_fail(bad,"PHY_GATE_REQUIRED_RELATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-VEC-ADD-SUB")["concepts"][0]["concept_id"]="CON-VEC-SCALAR-VECTOR"; must_fail(bad,"PHY_GATE_DUPLICATE_ASSET_ID")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["prerequisites"].append("PHY-M2D-NOT-REAL"); must_fail(bad,"PHY_GATE_PREREQUISITE_UNKNOWN")
bad=copy.deepcopy(REG); gate(bad,"PHY-VEC-BASICS")["prerequisites"].append("PHY-M2D-MOVING-LAUNCHER"); must_fail(bad,"PHY_GATE_DEPENDENCY_CYCLE")
bad=copy.deepcopy(REG); gate(bad,"PHY-VEC-BASICS")["concepts"][0]["authority_ref"]=99; must_fail(bad,"PHY_GATE_AUTHORITY_REF_INVALID")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-PROJECTILE-COMPONENTS")["relations"][0]["symbols"][0]["unit_dimension"]=""; must_fail(bad,"PHY_GATE_SCHEMA_VIOLATION")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-PROJECTILE-COMPONENTS")["model_conditions"][0]["required_for_relations"]=["EQ-NOT-REAL"]; must_fail(bad,"PHY_GATE_MODEL_CONDITION_BINDING_INVALID")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["representations"][0]["relation_bindings"]=["EQ-NOT-REAL"]; must_fail(bad,"PHY_GATE_REPRESENTATION_BINDING_INVALID")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["representations"][0]["must_not_imply"]=[]; must_fail(bad,"PHY_GATE_SCHEMA_VIOLATION")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["reasoning_sequence"][2]["depends_on"]=["RS-NOT-REAL"]; must_fail(bad,"PHY_GATE_REASONING_DEPENDENCY_INVALID")
bad=copy.deepcopy(REG); g=gate(bad,"PHY-M2D-MOVING-LAUNCHER"); g["reasoning_sequence"][1]["sequence"]=3; g["reasoning_sequence"][2]["sequence"]=2; must_fail(bad,"PHY_GATE_REASONING_ORDER_INVALID")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["problem_families"][0]["required_representation"]="REP-NOT-REAL"; must_fail(bad,"PHY_GATE_PROBLEM_FAMILY_INVALID")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["misconceptions"][0]["required_counterexample"]=""; must_fail(bad,"PHY_GATE_SCHEMA_VIOLATION")
bad=copy.deepcopy(REG); gate(bad,"PHY-VEC-BASICS")["difficulty_engineering"]["maturity"]="EMPIRICAL_VALIDATED"; must_fail(bad,"PHY_GATE_SCHEMA_VIOLATION")
bad=copy.deepcopy(REG); gate(bad,"PHY-VEC-BASICS")["authority_basis"].append({"claim_class":"SOURCE_SCOPE_HELD","source_ref":"HELD:test","claim_scope":"test hold"}); must_fail(bad,"PHY_GATE_SOURCE_SCOPE_HELD")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["linked_buckets"].remove("M2D-SBA-23"); must_fail(bad,"PHY_GATE_REQUIRED_BUCKET_BINDING_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-MOVING-LAUNCHER")["verifications"].remove("LIMITING_CASE"); must_fail(bad,"PHY_GATE_REQUIRED_VERIFICATION_MISSING")
bad=copy.deepcopy(REG); bad["gates"]=[g for g in bad["gates"] if g["subtopic_id"]!="PHY-M2D-SHARED-CLOCK"]; must_fail(bad,"PHY_GATE_CANONICAL_SET_MISMATCH")

# Newtonian model falsifiers retained.
bad=copy.deepcopy(REG); gate(bad,"PHY-NLM-FBD")["required_invariants"].remove("INV-NLM-SYSTEM-SELECTED-FIRST"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-NLM-SECOND-LAW")["prerequisites"].remove("PHY-NLM-FBD"); must_fail(bad,"PHY_GATE_REQUIRED_PREREQUISITE_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-NLM-THIRD-LAW")["required_invariants"].remove("INV-NLM-THIRD-DISTINCT-BODIES"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-NLM-NORMAL")["required_invariants"].remove("INV-NLM-NORMAL-NOT-ALWAYS-MG"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-NLM-TENSION")["required_invariants"].remove("INV-NLM-TENSION-STRING-MODEL"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); g=gate(bad,"PHY-NLM-FRICTION"); g["relations"]=[r for r in g["relations"] if r["relation_id"]!="EQ-NLM-STATIC-INEQUALITY"]; must_fail(bad,"PHY_GATE_REQUIRED_RELATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-NLM-CONNECTED")["required_invariants"].remove("INV-NLM-INTERNAL-EXTERNAL-DISTINCTION"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); fam=copy.deepcopy(gate(bad,"PHY-NLM-TENSION")["problem_families"][0]); gate(bad,"PHY-NLM-TENSION")["problem_families"].append(fam); must_fail(bad,"PHY_GATE_PROBLEM_FAMILY_INVALID")

# Gravity falsifiers retained.
bad=copy.deepcopy(REG); gate(bad,"PHY-GRAV-FIELD")["required_invariants"].remove("INV-GRAV-FIELD-INVERSE-SQUARE"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); g=gate(bad,"PHY-GRAV-FIELD"); g["relations"]=[r for r in g["relations"] if r["relation_id"]!="EQ-GRAV-FIELD-SUPERPOSITION"]; must_fail(bad,"PHY_GATE_REQUIRED_RELATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-GRAV-FORCE")["prerequisites"].remove("PHY-NLM-THIRD-LAW"); must_fail(bad,"PHY_GATE_REQUIRED_PREREQUISITE_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-GRAV-FIELD")["verifications"].remove("SYMMETRY"); must_fail(bad,"PHY_GATE_REQUIRED_VERIFICATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-GRAV-FORCE")["relations"][0]["symbols"][4]["unit_dimension"]=""; must_fail(bad,"PHY_GATE_SCHEMA_VIOLATION")

# Generic relative-velocity falsifiers.
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-RELATIVE-VELOCITY")["required_invariants"].remove("INV-M2D-RELATIVE-VELOCITY-SUBTRACTION"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); g=gate(bad,"PHY-M2D-RELATIVE-VELOCITY"); g["relations"]=[r for r in g["relations"] if r["relation_id"]!="EQ-M2D-RIVER-CROSSING-TIME"]; must_fail(bad,"PHY_GATE_REQUIRED_RELATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-RELATIVE-VELOCITY")["prerequisites"].remove("PHY-VEC-COMPONENTS"); must_fail(bad,"PHY_GATE_REQUIRED_PREREQUISITE_MISSING")

# Work-Energy verification and applicability falsifiers.
bad=copy.deepcopy(REG); gate(bad,"PHY-ENERGY-CONSERVATION-LAW")["verifications"].remove("ENERGY_ACCOUNTING"); must_fail(bad,"PHY_GATE_REQUIRED_VERIFICATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-ENERGY-CONSERVATION-LAW")["verifications"].remove("REFERENCE_CONSISTENCY"); must_fail(bad,"PHY_GATE_REQUIRED_VERIFICATION_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-ENERGY-CONSERVATION-LAW")["required_invariants"].remove("INV-WEP-MECH-CONSERVATION-CONDITIONAL"); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-WORK-ENERGY-POWER")["prerequisites"].remove("PHY-NLM-SECOND-LAW"); must_fail(bad,"PHY_GATE_REQUIRED_PREREQUISITE_MISSING")

# SBA04 technical-gate falsifiers: one per new capability plus bucket custody.
for gid, invariant in [
    ("PHY-M2D-VELOCITY-EVOLUTION","INV-M2D-APEX-VY-ZERO-NOT-GZERO"),
    ("PHY-M2D-VELOCITY-DIRECTION","INV-M2D-DIRECTION-SIGN-FROM-VY"),
    ("PHY-M2D-SPEED-MAGNITUDE","INV-M2D-APEX-SPEED-EQUALS-ABS-VX"),
    ("PHY-M2D-SAME-HEIGHT-VELOCITY","INV-M2D-SAME-HEIGHT-VELOCITY-DIFFERENT"),
    ("PHY-M2D-PERPENDICULAR-VELOCITY","INV-M2D-PERP-DOT-ZERO"),
    ("PHY-M2D-SPEED-AT-HEIGHT","INV-M2D-HEIGHT-ORIGIN-DECLARED"),
]:
    bad=copy.deepcopy(REG); gate(bad,gid)["required_invariants"].remove(invariant); must_fail(bad,"PHY_GATE_REQUIRED_INVARIANT_MISSING")

bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-VELOCITY-EVOLUTION")["linked_buckets"].remove("M2D-SBA-04"); must_fail(bad,"PHY_GATE_REQUIRED_BUCKET_BINDING_MISSING")
bad=copy.deepcopy(REG); gate(bad,"PHY-M2D-PERPENDICULAR-VELOCITY")["relations"][0]["symbols"][0]["reference_frame_role"]=""; must_fail(bad,"PHY_GATE_SCHEMA_VIOLATION")

print("Physics Technical Engineering Gates v3: PASS (26-gate custody + Work-Energy verification ontology + scoped-closure invariance + mutation falsifiers)")