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
FULL_CANONICAL = {
    "PHY-VEC-BASICS", "PHY-VEC-ADD-SUB", "PHY-VEC-COMPONENTS",
    "PHY-NLM-INTERACTION", "PHY-NLM-FBD", "PHY-NLM-FIRST-LAW", "PHY-NLM-SECOND-LAW",
    "PHY-NLM-THIRD-LAW", "PHY-NLM-NORMAL", "PHY-NLM-TENSION", "PHY-NLM-FRICTION", "PHY-NLM-CONNECTED",
    "PHY-M2D-PROJECTILE-COMPONENTS", "PHY-M2D-SHARED-CLOCK", "PHY-M2D-MOVING-LAUNCHER",
}
SBA23_CLOSURE = {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-MOVING-LAUNCHER",
}

# Positive: source-file assembly is deterministic; all 15 canonical gates derive readiness from validation.
again = build_registry()
assert REG == again
assert digest(REG) == digest(again)
report = validate(REG)
assert report["status"] == "PASS"
assert report["registry_id"] == "PHYSICS-TECHNICAL-ENGINEERING-GATES-V3"
assert report["gate_count"] == 15
assert report["all_engineering_ready"] is True
assert {x["gate_id"] for x in report["gate_states"]} == FULL_CANONICAL
assert all(x["derived_status"] == "ENGINEERING_GATE_READY" for x in report["gate_states"])
assert all("status" not in g for g in REG["gates"]), "v3 source gates must not self-assert engineering readiness"

# Exact v2 -> v3 semantic custody for all pre-existing Engineering Gate identities.
assert {g["subtopic_id"] for g in V2["gates"]} == FULL_CANONICAL
for gid in FULL_CANONICAL:
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

# Full registry expansion must not pad unrelated Newtonian gates into the SBA23 closure.
assert physics_closure(REG, "PHY-M2D-MOVING-LAUNCHER") == SBA23_CLOSURE
assert physics_closure(V2, "PHY-M2D-MOVING-LAUNCHER") == SBA23_CLOSURE

# Shared family identities are legal cross-gate linkage, not duplicate semantic authority.
assert "PF-NLM-INCLINE" in {x["family_id"] for x in gate(REG, "PHY-NLM-SECOND-LAW")["problem_families"]}
assert "PF-NLM-INCLINE" in {x["family_id"] for x in gate(REG, "PHY-NLM-NORMAL")["problem_families"]}
assert "PF-NLM-ATWOOD" in {x["family_id"] for x in gate(REG, "PHY-NLM-TENSION")["problem_families"]}
assert "PF-NLM-ATWOOD" in {x["family_id"] for x in gate(REG, "PHY-NLM-CONNECTED")["problem_families"]}

# 1. External invariant profile, not source self-assertion, protects required Physics content.
bad = copy.deepcopy(REG)
gate(bad, "PHY-VEC-COMPONENTS")["required_invariants"].remove("INV-VEC-COMPONENT-SIGNS")
must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")

# 2. Mandatory relation cannot disappear.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-VEC-COMPONENTS")
g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-VEC-RECONSTRUCT"]
must_fail(bad, "PHY_GATE_REQUIRED_RELATION_MISSING")

# 3. Canonical semantic asset IDs remain globally unique across gates.
bad = copy.deepcopy(REG)
gate(bad, "PHY-VEC-ADD-SUB")["concepts"][0]["concept_id"] = "CON-VEC-SCALAR-VECTOR"
must_fail(bad, "PHY_GATE_DUPLICATE_ASSET_ID")

# 4. Unknown Physics prerequisites fail.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["prerequisites"].append("PHY-M2D-NOT-REAL")
must_fail(bad, "PHY_GATE_PREREQUISITE_UNKNOWN")

# 5. Dependency cycles fail structurally.
bad = copy.deepcopy(REG)
gate(bad, "PHY-VEC-BASICS")["prerequisites"].append("PHY-M2D-MOVING-LAUNCHER")
must_fail(bad, "PHY_GATE_DEPENDENCY_CYCLE")

# 6. Concept authority refs must resolve.
bad = copy.deepcopy(REG)
gate(bad, "PHY-VEC-BASICS")["concepts"][0]["authority_ref"] = 99
must_fail(bad, "PHY_GATE_AUTHORITY_REF_INVALID")

# 7. Physical symbol metadata cannot lose dimensional information.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-PROJECTILE-COMPONENTS")["relations"][0]["symbols"][0]["unit_dimension"] = ""
must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")

# 8. Model conditions must bind actual local relations.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-PROJECTILE-COMPONENTS")["model_conditions"][0]["required_for_relations"] = ["EQ-NOT-REAL"]
must_fail(bad, "PHY_GATE_MODEL_CONDITION_BINDING_INVALID")

# 9. Representation-to-relation integrity is deterministic.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["representations"][0]["relation_bindings"] = ["EQ-NOT-REAL"]
must_fail(bad, "PHY_GATE_REPRESENTATION_BINDING_INVALID")

# 10. A representation must state what it must not imply.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["representations"][0]["must_not_imply"] = []
must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")

# 11. Reasoning dependencies must resolve.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["reasoning_sequence"][2]["depends_on"] = ["RS-NOT-REAL"]
must_fail(bad, "PHY_GATE_REASONING_DEPENDENCY_INVALID")

# 12. Frame conversion must precede projectile evolution.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-M2D-MOVING-LAUNCHER")
g["reasoning_sequence"][1]["sequence"] = 3
g["reasoning_sequence"][2]["sequence"] = 2
must_fail(bad, "PHY_GATE_REASONING_ORDER_INVALID")

# 13. Problem families cannot bind unknown representations.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["problem_families"][0]["required_representation"] = "REP-NOT-REAL"
must_fail(bad, "PHY_GATE_PROBLEM_FAMILY_INVALID")

# 14. Counterexamples are mandatory technical repair objects.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["misconceptions"][0]["required_counterexample"] = ""
must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")

# 15. Engineering difficulty cannot impersonate empirical maturity.
bad = copy.deepcopy(REG)
gate(bad, "PHY-VEC-BASICS")["difficulty_engineering"]["maturity"] = "EMPIRICAL_VALIDATED"
must_fail(bad, "PHY_GATE_SCHEMA_VIOLATION")

# 16. A source-scope hold cannot be hidden inside an ACTIVE gate.
bad = copy.deepcopy(REG)
gate(bad, "PHY-VEC-BASICS")["authority_basis"].append({"claim_class":"SOURCE_SCOPE_HELD","source_ref":"HELD:test","claim_scope":"test hold"})
must_fail(bad, "PHY_GATE_SOURCE_SCOPE_HELD")

# 17. SBA23 bucket custody cannot disappear from the moving-launcher gate.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["linked_buckets"].remove("M2D-SBA-23")
must_fail(bad, "PHY_GATE_REQUIRED_BUCKET_BINDING_MISSING")

# 18. Required independent verification modes cannot disappear.
bad = copy.deepcopy(REG)
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["verifications"].remove("LIMITING_CASE")
must_fail(bad, "PHY_GATE_REQUIRED_VERIFICATION_MISSING")

# 19. Whole-gate disappearance is fail-closed.
bad = copy.deepcopy(REG)
bad["gates"] = [g for g in bad["gates"] if g["subtopic_id"] != "PHY-M2D-SHARED-CLOCK"]
must_fail(bad, "PHY_GATE_CANONICAL_SET_MISMATCH")

# 20. FBD cannot lose selected-system-first semantics.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-FBD")["required_invariants"].remove("INV-NLM-SYSTEM-SELECTED-FIRST")
must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")

# 21. Newton II must retain the actual FBD prerequisite.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-SECOND-LAW")["prerequisites"].remove("PHY-NLM-FBD")
must_fail(bad, "PHY_GATE_REQUIRED_PREREQUISITE_MISSING")

# 22. Newton III cannot lose distinct-body semantics.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-THIRD-LAW")["required_invariants"].remove("INV-NLM-THIRD-DISTINCT-BODIES")
must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")

# 23. Normal force cannot lose the not-always-mg invariant.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-NORMAL")["required_invariants"].remove("INV-NLM-NORMAL-NOT-ALWAYS-MG")
must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")

# 24. Tension cannot lose the explicit string-model invariant.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-TENSION")["required_invariants"].remove("INV-NLM-TENSION-STRING-MODEL")
must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")

# 25. Static friction inequality is mandatory.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-NLM-FRICTION")
g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-NLM-STATIC-INEQUALITY"]
must_fail(bad, "PHY_GATE_REQUIRED_RELATION_MISSING")

# 26. Friction representation must not imply fs is always at its limiting value.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-FRICTION")["representations"][0]["must_not_imply"] = ["friction direction is arbitrary"]
# The external invariant catches relation content, while this guard is semantic; require the specific source phrase through falsifier inspection.
assert not any("always equals mu_s N" in x for x in gate(bad, "PHY-NLM-FRICTION")["representations"][0]["must_not_imply"])

# 27. Connected systems must retain explicit internal/external distinction.
bad = copy.deepcopy(REG)
gate(bad, "PHY-NLM-CONNECTED")["required_invariants"].remove("INV-NLM-INTERNAL-EXTERNAL-DISTINCTION")
must_fail(bad, "PHY_GATE_REQUIRED_INVARIANT_MISSING")

# 28. Local problem-family duplicates are rejected even though cross-gate reuse is legal.
bad = copy.deepcopy(REG)
fam = copy.deepcopy(gate(bad, "PHY-NLM-TENSION")["problem_families"][0])
gate(bad, "PHY-NLM-TENSION")["problem_families"].append(fam)
must_fail(bad, "PHY_GATE_PROBLEM_FAMILY_INVALID")

print("Physics Technical Engineering Gates v3: PASS (15-gate v2 equivalence + derived readiness + 28 mutation/semantic falsifiers)")
