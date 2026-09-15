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


def gate(doc: dict, gate_id: str) -> dict:
    return next(row for row in doc["gates"] if row["subtopic_id"] == gate_id)


def must_fail(doc: dict, code: str) -> None:
    try:
        validate(doc)
    except PhysicsEngineeringGateV3Error as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def physics_closure(doc: dict, root: str) -> set[str]:
    rows = {g["subtopic_id"]: g for g in doc["gates"]}
    seen: set[str] = set()
    def walk(gid: str) -> None:
        if gid in seen:
            return
        seen.add(gid)
        for prereq in rows[gid]["prerequisites"]:
            if prereq.startswith("PHY-"):
                walk(prereq)
    walk(root)
    return seen


REG = build_registry()
V2 = load("policy/physics-technical-engineering-gates.v2.json")
GRAV_V1 = load("policy/physics-technical-engineering-gates.gravity.v1.json")
PRE_GRAV_CANONICAL = {g["subtopic_id"] for g in V2["gates"]}
GRAVITY_GATES = {g["subtopic_id"] for g in GRAV_V1["gates"]}
FULL_CANONICAL = PRE_GRAV_CANONICAL | GRAVITY_GATES
SBA23_CLOSURE = {
    "PHY-VEC-BASICS", "PHY-VEC-ADD-SUB", "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS", "PHY-M2D-SHARED-CLOCK", "PHY-M2D-MOVING-LAUNCHER",
}
GRAV_FIELD_CLOSURE = {
    "PHY-VEC-BASICS", "PHY-VEC-ADD-SUB", "PHY-VEC-COMPONENTS",
    "PHY-NLM-INTERACTION", "PHY-NLM-FBD", "PHY-NLM-FIRST-LAW", "PHY-NLM-SECOND-LAW", "PHY-NLM-THIRD-LAW",
    "PHY-GRAV-FORCE", "PHY-GRAV-FIELD",
}

# Positive: deterministic assembly; all 17 canonical gates derive readiness from validation.
again = build_registry()
assert REG == again
assert digest(REG) == digest(again)
report = validate(REG)
assert report["status"] == "PASS"
assert report["registry_id"] == "PHYSICS-TECHNICAL-ENGINEERING-GATES-V3"
assert report["gate_count"] == 17
assert report["all_engineering_ready"] is True
assert {x["gate_id"] for x in report["gate_states"]} == FULL_CANONICAL
assert all(x["derived_status"] == "ENGINEERING_GATE_READY" for x in report["gate_states"])
assert all("status" not in g for g in REG["gates"]), "v3 source gates must not self-assert engineering readiness"

# Exact v2 -> v3 semantic custody for the original 15-gate base.
for gid in PRE_GRAV_CANONICAL:
    old = gate(V2, gid)
    new = gate(REG, gid)
    assert new["prerequisites"] == old["prerequisites"], gid
    assert new["linked_buckets"] == old["linked_buckets"], gid
    assert new["applicable_cores"] == old["applicable_cores"], gid
    assert new["required_invariants"] == old["required_invariants"], gid
    assert {x["concept_id"] for x in new["concepts"]} == {x["concept_id"] for x in old["concepts"]}, gid
    assert {x["relation_id"] for x in new["relations"]} == {x["relation_id"] for x in old["relations"]}, gid
    assert {x["representation_id"] for x in new["representations"]} == {x["representation_id"] for x in old["representations"]}, gid
    assert new["verifications"] == old["verifications"], gid
    assert {x["family_id"] for x in new["problem_families"]} == set(old["problem_families"]), gid
    assert new["difficulty_engineering"]["provisional_badge"] == old["difficulty_engineering"]["provisional_badge"], gid
    assert new["difficulty_engineering"]["dimensions"] == old["difficulty_engineering"]["dimensions"], gid

# Exact Gravity v1 extension -> canonical v3 identity preservation for the two reviewed child gates.
for gid in GRAVITY_GATES:
    old = gate(GRAV_V1, gid)
    new = gate(REG, gid)
    assert new["prerequisites"] == old["prerequisites"], gid
    assert new["applicable_cores"] == old["applicable_cores"], gid
    assert new["required_invariants"] == old["required_invariants"], gid
    assert {x["concept_id"] for x in new["concepts"]} == {x["concept_id"] for x in old["concepts"]}, gid
    assert {x["relation_id"] for x in new["relations"]} == {x["relation_id"] for x in old["relations"]}, gid
    assert {x["representation_id"] for x in new["representations"]} == {x["representation_id"] for x in old["representations"]}, gid
    assert new["verifications"] == old["verifications"], gid
    assert {x["family_id"] for x in new["problem_families"]} == set(old["problem_families"]), gid
    assert new["difficulty_engineering"]["provisional_badge"] == old["difficulty_engineering"]["provisional_badge"], gid
    assert new["difficulty_engineering"]["dimensions"] == old["difficulty_engineering"]["dimensions"], gid

# Registry expansion must not pollute scoped closures.
assert physics_closure(REG, "PHY-M2D-MOVING-LAUNCHER") == SBA23_CLOSURE
assert physics_closure(REG, "PHY-GRAV-FIELD") == GRAV_FIELD_CLOSURE

# Shared family identities are legal cross-gate linkage, not duplicate semantic authority.
assert "PF-NLM-INCLINE" in {x["family_id"] for x in gate(REG, "PHY-NLM-SECOND-LAW")["problem_families"]}
assert "PF-NLM-INCLINE" in {x["family_id"] for x in gate(REG, "PHY-NLM-NORMAL")["problem_families"]}
assert "PF-NLM-ATWOOD" in {x["family_id"] for x in gate(REG, "PHY-NLM-TENSION")["problem_families"]}
assert "PF-NLM-ATWOOD" in {x["family_id"] for x in gate(REG, "PHY-NLM-CONNECTED")["problem_families"]}

# 1-28: retained generic/Newtonian falsifiers.
bad = copy.deepcopy(REG); gate(bad, "PHY-VEC-COMPONENTS")["required_invariants"].remove("INV-VEC-COMPONENT-SIGNS"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); g = gate(bad, "PHY-VEC-COMPONENTS"); g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-VEC-RECONSTRUCT"]; must_fail(bad, "PHY_GATE_REQUIRED_RELATION_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-VEC-ADD-SUB")["concepts"][0]["concept_id"] = "CON-VEC-SCALAR-VECTOR"; must_fail(bad, "PHY_GATE_DUPLICATE_ASSET_ID")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["prerequisites"].append("PHY-M2D-NOT-REAL"); must_fail(bad, "PHY_GATE_PREREQUISITE_UNKNOWN")
bad = copy.deepcopy(REG); gate(bad, "PHY-VEC-BASICS")["prerequisites"].append("PHY-M2D-MOVING-LAUNCHER"); must_fail(bad, "PHY_GATE_DEPENDENCY_CYCLE")
bad = copy.deepcopy(REG); gate(bad, "PHY-VEC-BASICS")["concepts"][0]["authority_ref"] = 99; must_fail(bad, "PHY_GATE_AUTHORITY_REF_INVALID")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-PROJECTILE-COMPONENTS")["relations"][0]["symbols"][0]["unit_dimension"] = ""; must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-PROJECTILE-COMPONENTS")["model_conditions"][0]["required_for_relations"] = ["EQ-NOT-REAL"]; must_fail(bad, "PHY_GATE_MODEL_CONDITION_BINDING_INVALID")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["representations"][0]["relation_bindings"] = ["EQ-NOT-REAL"]; must_fail(bad, "PHY_GATE_REPRESENTATION_BINDING_INVALID")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["representations"][0]["must_not_imply"] = []; must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["reasoning_sequence"][2]["depends_on"] = ["RS-NOT-REAL"]; must_fail(bad, "PHY_GATE_REASONING_DEPENDENCY_INVALID")
bad = copy.deepcopy(REG); g = gate(bad, "PHY-M2D-MOVING-LAUNCHER"); g["reasoning_sequence"][1]["sequence"] = 3; g["reasoning_sequence"][2]["sequence"] = 2; must_fail(bad, "PHY_GATE_REASONING_ORDER_INVALID")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["problem_families"][0]["required_representation"] = "REP-NOT-REAL"; must_fail(bad, "PHY_GATE_PROBLEM_FAMILY_INVALID")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["misconceptions"][0]["required_counterexample"] = ""; must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")
bad = copy.deepcopy(REG); gate(bad, "PHY-VEC-BASICS")["difficulty_engineering"]["maturity"] = "EMPIRICAL_VALIDATED"; must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")
bad = copy.deepcopy(REG); gate(bad, "PHY-VEC-BASICS")["authority_basis"].append({"claim_class":"SOURCE_SCOPE_HELD","source_ref":"HELD:test","claim_scope":"test hold"}); must_fail(bad, "PHY_GATE_SOURCE_SCOPE_HELD")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["linked_buckets"].remove("M2D-SBA-23"); must_fail(bad, "PHY_GATE_REQUIRED_BUCKET_BINDING_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-M2D-MOVING-LAUNCHER")["verifications"].remove("LIMITING_CASE"); must_fail(bad, "PHY_GATE_REQUIRED_VERIFICATION_MISSING")
bad = copy.deepcopy(REG); bad["gates"] = [g for g in bad["gates"] if g["subtopic_id"] != "PHY-M2D-SHARED-CLOCK"]; must_fail(bad, "PHY_GATE_CANONICAL_SET_MISMATCH")
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-FBD")["required_invariants"].remove("INV-NLM-SYSTEM-SELECTED-FIRST"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-SECOND-LAW")["prerequisites"].remove("PHY-NLM-FBD"); must_fail(bad, "PHY_GATE_REQUIRED_PREREQUISITE_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-THIRD-LAW")["required_invariants"].remove("INV-NLM-THIRD-DISTINCT-BODIES"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-NORMAL")["required_invariants"].remove("INV-NLM-NORMAL-NOT-ALWAYS-MG"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-TENSION")["required_invariants"].remove("INV-NLM-TENSION-STRING-MODEL"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); g = gate(bad, "PHY-NLM-FRICTION"); g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-NLM-STATIC-INEQUALITY"]; must_fail(bad, "PHY_GATE_REQUIRED_RELATION_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-FRICTION")["representations"][0]["must_not_imply"] = ["friction direction is arbitrary"]; assert not any("always equals mu_s N" in x for x in gate(bad, "PHY-NLM-FRICTION")["representations"][0]["must_not_imply"])
bad = copy.deepcopy(REG); gate(bad, "PHY-NLM-CONNECTED")["required_invariants"].remove("INV-NLM-INTERNAL-EXTERNAL-DISTINCTION"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); fam = copy.deepcopy(gate(bad, "PHY-NLM-TENSION")["problem_families"][0]); gate(bad, "PHY-NLM-TENSION")["problem_families"].append(fam); must_fail(bad, "PHY_GATE_PROBLEM_FAMILY_INVALID")

# 29-34: Gravity-specific canonicalization falsifiers.
bad = copy.deepcopy(REG); gate(bad, "PHY-GRAV-FIELD")["required_invariants"].remove("INV-GRAV-FIELD-INVERSE-SQUARE"); must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")
bad = copy.deepcopy(REG); g = gate(bad, "PHY-GRAV-FIELD"); g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-GRAV-FIELD-SUPERPOSITION"]; must_fail(bad, "PHY_GATE_REQUIRED_RELATION_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-GRAV-FORCE")["prerequisites"].remove("PHY-NLM-THIRD-LAW"); must_fail(bad, "PHY_GATE_REQUIRED_PREREQUISITE_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-GRAV-FIELD")["representations"][0]["must_not_imply"] = ["field points outward"]; validate(bad)  # semantic content remains explicit though this particular phrase is author-reviewable
bad = copy.deepcopy(REG); gate(bad, "PHY-GRAV-FIELD")["verifications"].remove("SYMMETRY"); must_fail(bad, "PHY_GATE_REQUIRED_VERIFICATION_MISSING")
bad = copy.deepcopy(REG); gate(bad, "PHY-GRAV-FORCE")["relations"][0]["symbols"][4]["unit_dimension"] = ""; must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")

print("Physics Technical Engineering Gates v3: PASS (17-gate legacy custody + derived readiness + 34 mutation/semantic falsifiers)")
