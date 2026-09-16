#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
REPO = ROOT.parents[3]
sys.path[:0] = [
    str(ROOT / "engine"),
    str(PHYS / "AssessmentScope" / "engine"),
]

from compile_physics_engineering_readiness import (  # noqa: E402
    PhysicsColdStartEngineeringError,
    compile_physics_engineering_readiness,
    require_problem_semantics,
)
from evaluate_readiness import EngineeringGateError  # noqa: E402
from reconcile_physics_assessment_scope import reconcile  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_without(value, field):
    clone = copy.deepcopy(value)
    clone.pop(field, None)
    return hashlib.sha256(canonical(clone)).hexdigest()


def authority(name):
    manifest = load(PHYS / "GENERATION_AUTHORITY_MANIFEST.json")
    return load(REPO / manifest["authorities"][name])


Q = authority("question_set")
TOPIC = authority("declared_topic_scope")
REVIEW = authority("item_validity_registry")
REVIEW_POLICY = authority("diagnostic_use_policy")
CANON = authority("canonical_capabilities")
AUTH = authority("scope_authority")
BIND = authority("scope_bindings")
ENG_BIND = load(ROOT / "registry" / "physics-engineering-scope-bindings.v1.json")

scope_model, _, _, _ = reconcile(Q, TOPIC, REVIEW, REVIEW_POLICY, CANON, AUTH, BIND)

# Positive: exact P-C authority compiles a deterministic Engineering Gate envelope for P-D.
ready = compile_physics_engineering_readiness(scope_model, AUTH, ENG_BIND)
assert ready["authority_layer"] == "ENGINEERING_GATE"
assert ready["required_consumer"] == "PROBLEM_SEMANTICS"
assert ready["consumer_status"] == "ALLOWED"
assert ready["readiness_envelope"]["consumer_permissions"]["PROBLEM_SEMANTICS"]["status"] == "ALLOWED"
assert ready["readiness_envelope"]["publication_authorization"] == "NOT_IMPLIED"
assert ready["engineering_manifest"]["scope_kind"] == "ASSESSMENT_SCOPE"
assert ready["engineering_manifest"]["topic_id"] is None
assert ready["engineering_manifest"]["downstream_consumers"] == ["PROBLEM_SEMANTICS"]
assert ready["required_capability_refs"] == sorted(set(scope_model["assessed_capability_refs"]) | set(scope_model["required_prerequisite_capability_refs"]))
assert ready["technical_gate_requirement_state"] == "NOT_REQUIRED_FOR_THIS_SCOPE"
assert ready["engineering_manifest"]["required_gate_ids"] == []
assert ready["engineering_closure"]["counts"]["direct_gate_count"] == 0
require_problem_semantics(ready)
assert compile_physics_engineering_readiness(copy.deepcopy(scope_model), copy.deepcopy(AUTH), copy.deepcopy(ENG_BIND)) == ready

# Every canonical P-C capability must have an explicit route; adding a new capability cannot silently inherit memory.
bad = copy.deepcopy(ENG_BIND)
bad["bindings"] = bad["bindings"][:-1]
bad["registry_digest"] = digest_without(bad, "registry_digest")
try:
    compile_physics_engineering_readiness(scope_model, AUTH, bad)
except PhysicsColdStartEngineeringError as exc:
    assert exc.code == "ENGINEERING_SCOPE_BINDING_COVERAGE_MISMATCH", exc
else:
    raise AssertionError("missing canonical capability binding was accepted")

# Same registry ID with mutated content and stale digest is rejected.
bad = copy.deepcopy(ENG_BIND)
bad["bindings"][0]["rationale"] += " mutated"
try:
    compile_physics_engineering_readiness(scope_model, AUTH, bad)
except PhysicsColdStartEngineeringError as exc:
    assert exc.code == "ENGINEERING_SCOPE_BINDING_DIGEST_MISMATCH", exc
else:
    raise AssertionError("stale scope-binding digest was accepted")

# A declared technical route must point to a real active registry identity; no guessed gate IDs.
bad = copy.deepcopy(ENG_BIND)
projectile = next(row for row in bad["bindings"] if row["capability_ref"] == "PHY-CAP-PROJECTILE-COMPONENTS")
projectile["engineering_gate_ids"] = ["PHY-M2D-NOT-A-REAL-GATE"]
bad["registry_digest"] = digest_without(bad, "registry_digest")
try:
    compile_physics_engineering_readiness(scope_model, AUTH, bad)
except PhysicsColdStartEngineeringError as exc:
    assert exc.code == "ENGINEERING_SCOPE_GATE_UNKNOWN", exc
else:
    raise AssertionError("unknown Engineering Gate was accepted")

# P-C authority mutation cannot be hidden behind a recomputed downstream request.
bad_auth = copy.deepcopy(AUTH)
bad_auth["capabilities"][0]["title"] += " drift"
try:
    compile_physics_engineering_readiness(scope_model, bad_auth, ENG_BIND)
except PhysicsColdStartEngineeringError as exc:
    assert exc.code == "ENGINEERING_SCOPE_AUTHORITY_DIGEST_MISMATCH", exc
else:
    raise AssertionError("scope-authority drift was accepted")

# An unbound capability in the exact P-C scope fails closed even if its ID looks syntactically plausible.
bad_scope = copy.deepcopy(scope_model)
bad_scope["assessed_capability_refs"].append("PHY-CAP-UNDECLARED-NEW-CAPABILITY")
bad_scope["assessed_capability_refs"] = sorted(set(bad_scope["assessed_capability_refs"]))
bad_scope["scope_model_digest"] = digest_without(bad_scope, "scope_model_digest")
try:
    compile_physics_engineering_readiness(bad_scope, AUTH, ENG_BIND)
except PhysicsColdStartEngineeringError as exc:
    assert exc.code == "ENGINEERING_SCOPE_CAPABILITY_UNBOUND", exc
else:
    raise AssertionError("unbound P-C capability was accepted")

# Zero-dedicated-gate scopes are valid only through explicit upstream-authority bindings.
upstream_cap = next(row["capability_ref"] for row in ENG_BIND["bindings"] if row["authority_route"] == "UPSTREAM_SCOPE_AUTHORITY")
zero_scope = copy.deepcopy(scope_model)
zero_scope["assessed_capability_refs"] = [upstream_cap]
zero_scope["required_prerequisite_capability_refs"] = []
zero_scope["scope_model_digest"] = digest_without(zero_scope, "scope_model_digest")
zero = compile_physics_engineering_readiness(zero_scope, AUTH, ENG_BIND)
assert zero["technical_gate_requirement_state"] == "NOT_REQUIRED_FOR_THIS_SCOPE"
assert zero["engineering_manifest"]["required_gate_ids"] == []
assert zero["engineering_closure"]["counts"] == {
    "direct_gate_count": 0,
    "transitive_gate_count": 0,
    "ready_gate_count": 0,
    "blocked_gate_count": 0,
}
assert zero["engineering_closure"]["closure_status"] == "READY"
assert zero["consumer_status"] == "ALLOWED"
require_problem_semantics(zero)

# A scope with a real technical gate uses the same generic path. Technical closure can be READY while
# consumption remains BLOCKED because an external-domain prerequisite has no provider-owned receipt.
gated_scope = copy.deepcopy(scope_model)
gated_scope["assessed_capability_refs"] = ["PHY-CAP-PROJECTILE-COMPONENTS"]
gated_scope["required_prerequisite_capability_refs"] = []
gated_scope["scope_model_digest"] = digest_without(gated_scope, "scope_model_digest")
gated = compile_physics_engineering_readiness(gated_scope, AUTH, ENG_BIND)
assert gated["technical_gate_requirement_state"] == "REQUIRED_AND_READY"
assert gated["engineering_manifest"]["required_gate_ids"] == ["PHY-M2D-PROJECTILE-COMPONENTS"]
assert gated["engineering_closure"]["counts"]["direct_gate_count"] == 1
assert gated["engineering_closure"]["counts"]["transitive_gate_count"] >= 1
assert gated["engineering_closure"]["closure_status"] == "READY"
assert gated["domain_closure"]["closure_status"] == "HELD"
assert any(row["prerequisite_id"] == "MATH-TRIG-RIGHT" for row in gated["domain_closure"]["prerequisites"])
assert gated["consumer_status"] == "BLOCKED"
assert gated["readiness_envelope"]["dimensions"]["external_prerequisites"] == "HELD"
try:
    require_problem_semantics(gated)
except EngineeringGateError as exc:
    assert exc.code == "E_ENG_GATE_CONSUMER_BLOCKED", exc
else:
    raise AssertionError("consumer proceeded despite unresolved external-domain prerequisite")

# Generic adapter code may not recognize case IDs, topic names or question IDs.
text = (ROOT / "engine" / "compile_physics_engineering_readiness.py").read_text(encoding="utf-8")
for forbidden in ("M2D-SBA-04", "M2D-SBA-05", "Q14", "Q27", "Relative Motion", "Thermodynamics"):
    assert forbidden not in text, f"CASE_LITERAL_LEAK:{forbidden}"

print("Physics cold-start Engineering readiness: PASS (explicit zero-gate scopes + gated external holds remain visible and fail closed at consumption)")
