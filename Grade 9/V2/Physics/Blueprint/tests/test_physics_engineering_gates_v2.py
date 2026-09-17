#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_engineering_gates_v2 import GateValidationError, load, validate  # noqa: E402

REG = load("policy/physics-technical-engineering-gates.v2.json")


def gate(doc, gate_id):
    return next(g for g in doc["gates"] if g["subtopic_id"] == gate_id)


def must_fail(doc, code):
    try:
        validate(doc)
    except GateValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


# Positive: the absorbed + hardened registry is production-validator clean.
ids = validate(REG)
assert len(ids) == 15
assert "PHY-VEC-COMPONENTS" in ids
assert "PHY-NLM-FBD" in ids
assert "PHY-M2D-MOVING-LAUNCHER" in ids

# Mutation 1: vector sign convention cannot disappear.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-VEC-COMPONENTS")
g["required_invariants"].remove("INV-VEC-COMPONENT-SIGNS")
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 2: component -> resultant reconstruction relation is mandatory.
# Removing it first breaks the representation-to-relation binding, which is the stronger/earlier deterministic failure.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-VEC-COMPONENTS")
g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-VEC-RECONSTRUCT"]
must_fail(bad, "E_GATE_REP_BINDING")

# Mutation 3: NLM may not proceed without the actual FBD representation contract.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-NLM-FBD")
g["representations"] = [{"representation_id":"REP-NLM-DUMMY","representation_type":"DECORATIVE","mandatory_elements":["box"],"forbidden_omissions":["box"],"relation_bindings":[]}]
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 4: Newton III must retain distinct-body semantics.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-NLM-THIRD-LAW")
g["required_invariants"].remove("INV-NLM-THIRD-DISTINCT-BODIES")
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 5: normal force may not silently collapse to N=mg as the general model.
# This gate has one canonical concept, so deleting it is rejected by the schema before the gate-specific concept check.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-NLM-NORMAL")
g["concepts"] = [c for c in g["concepts"] if c["concept_id"] != "CON-NLM-NORMAL-NOT-ALWAYS-MG"]
must_fail(bad, "E_GATE_SCHEMA")

# Mutation 6: static-friction inequality must survive.
# The FBD is explicitly bound to that relation, so removing the relation first breaks the stronger representation binding invariant.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-NLM-FRICTION")
g["relations"] = [r for r in g["relations"] if r["relation_id"] != "EQ-NLM-STATIC-INEQUALITY"]
must_fail(bad, "E_GATE_REP_BINDING")

# Mutation 7: second law must depend on an FBD and component competence.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-NLM-SECOND-LAW")
g["prerequisites"].remove("PHY-NLM-FBD")
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 8: same-event projectile motion cannot lose its shared clock.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-M2D-SHARED-CLOCK")
g["required_invariants"].remove("INV-M2D-SHARED-CLOCK")
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 9: moving-launcher problems require frame conversion before projectile evolution.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-M2D-MOVING-LAUNCHER")
g["required_invariants"].remove("INV-M2D-GALILEAN-ADD-BEFORE-PROJECTILE")
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 10: SBA-23 binding cannot disappear from its technical gate.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-M2D-MOVING-LAUNCHER")
g["linked_buckets"].remove("M2D-SBA-23")
must_fail(bad, "E_GATE_INVARIANT_MISSING")

# Mutation 11: representation/relation references are cross-checked.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-M2D-MOVING-LAUNCHER")
g["representations"][0]["relation_bindings"] = ["EQ-NONEXISTENT"]
must_fail(bad, "E_GATE_REP_BINDING")

# Mutation 12: internal Physics prerequisite references must resolve.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-M2D-MOVING-LAUNCHER")
g["prerequisites"].append("PHY-M2D-NOT-REAL")
must_fail(bad, "E_GATE_MISSING_PREREQ")

# Mutation 13: source-scope hold cannot be self-declared READY.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-VEC-BASICS")
g["authority_basis"].append({"claim_class":"SOURCE_SCOPE_HELD","source_ref":"HELD:test","claim_scope":"test hold"})
must_fail(bad, "E_GATE_SCOPE_HELD_READY")

# Mutation 14: engineering difficulty cannot impersonate empirical validation.
bad = copy.deepcopy(REG)
g = gate(bad, "PHY-VEC-BASICS")
g["difficulty_engineering"]["maturity"] = "VALIDATED"
must_fail(bad, "E_GATE_SCHEMA")

# Mutation 15: absorbed canonical set is fail-closed; a whole gate cannot vanish silently.
bad = copy.deepcopy(REG)
bad["gates"] = [g for g in bad["gates"] if g["subtopic_id"] != "PHY-NLM-TENSION"]
must_fail(bad, "E_GATE_CANONICAL_SET")

print("Physics Technical Engineering Gates v2: PASS (production validator + 15 mutation falsifiers)")
