#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from compile_engineering_closure import EngineeringClosureError, V3_REGISTRY_REF, compile_closure, load  # noqa: E402
from compile_engineering_passport import compile_passport  # noqa: E402
from compile_engineering_readiness import compile_readiness  # noqa: E402
from validate_ccu_engineering_ready import EngineeringCCUError, validate_engineered_ccu  # noqa: E402

REQUEST = load("fixtures/engineering-workbench/m2d-sba23-request.v1.json")
V2_MANIFEST = load("fixtures/engineering-workbench/m2d-sba23-manifest.v1.json")
V3_MANIFEST = load("fixtures/engineering-workbench/m2d-sba23-manifest.v3.json")
CCU = load("topics/m2d-sba23-ccu.v1.json")
EXPECTED = {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-MOVING-LAUNCHER",
}


def gate(registry: dict, gate_id: str) -> dict:
    return next(row for row in registry["gates"] if row["subtopic_id"] == gate_id)


def must_closure_error(request: dict, manifest: dict, code: str, **kwargs) -> None:
    try:
        compile_closure(request, manifest, **kwargs)
    except EngineeringClosureError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


v3 = compile_closure(REQUEST, V3_MANIFEST)
assert v3["closure_status"] == "READY"
assert v3["registry_ref"] == V3_REGISTRY_REF
assert set(v3["transitive_gate_ids"]) == EXPECTED
assert v3["counts"] == {
    "direct_gate_count": 1,
    "transitive_gate_count": 6,
    "ready_gate_count": 6,
    "blocked_gate_count": 0,
}
assert all(x["status"] == "ENGINEERING_GATE_READY" for x in v3["gate_states"])
assert v3["source_item_status"] == "SOURCE_HELD"
assert v3["manifest_digest"].startswith("sha256:")

passport = compile_passport(REQUEST, v3)
assert passport["schema_version"] == "2.0.0"
assert passport["technical_state"] == "ENGINEERING_READY"
assert passport["registry_digest"] == v3["registry_digest"]
assert passport["publication_authorization"] == "NOT_IMPLIED"
assert passport["source_item_status"] == "SOURCE_HELD"
assert passport["consumer_authorization"] == "NOT_EVALUATED"
assert all(row["status"] == "PASS" for row in passport["technical_coverage"].values())

# Canonical consumer authority is the global Engineering Gate envelope, not the diagnostic Passport.
engineering, domain, envelope = compile_readiness(REQUEST, V3_MANIFEST)
assert engineering["closure_status"] == "READY"
assert domain["closure_status"] == "HELD"
assert envelope["authority_layer"] == "ENGINEERING_GATE"
assert envelope["overall_state"] == "BLOCKED"
assert set(envelope["consumer_permissions"]) == set(V3_MANIFEST["downstream_consumers"])
assert envelope["consumer_permissions"]["CCU"]["status"] == "BLOCKED"
assert envelope["dimensions"]["external_prerequisites"] == "HELD"
try:
    validate_engineered_ccu(REQUEST, V3_MANIFEST, CCU)
except EngineeringCCUError as exc:
    assert exc.code == "E_CCU_ENGINEERING_BLOCKED"
else:
    raise AssertionError("declared consumer bypassed global Engineering Gate authority")

v2 = compile_closure(REQUEST, V2_MANIFEST)
assert v2["closure_status"] == "READY"
assert set(v2["transitive_gate_ids"]) == EXPECTED
assert [x["gate_id"] for x in v2["gate_states"]] == [x["gate_id"] for x in v3["gate_states"]]
legacy_passport = compile_passport(REQUEST, v2)
assert legacy_passport["schema_version"] == "1.0.0"
assert legacy_passport["consumer_authorization"] == "NOT_EVALUATED"
assert "technical_coverage" not in legacy_passport

bad = build_registry()
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["scope_state"] = "DRAFT"
blocked = compile_closure(REQUEST, V3_MANIFEST, registry=bad)
assert blocked["closure_status"] == "BLOCKED"
assert any(x["gate_id"] == "PHY-M2D-MOVING-LAUNCHER" and x["status"] == "ENGINEERING_GATE_INCOMPLETE" for x in blocked["gate_states"])
assert any(x["code"] == "E_ENG_GATE_NOT_READY" for x in blocked["blockers"])

bad = build_registry()
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["scope_state"] = "SOURCE_SCOPE_HELD"
blocked = compile_closure(REQUEST, V3_MANIFEST, registry=bad)
assert blocked["closure_status"] == "BLOCKED"
assert any(x["status"] == "SOURCE_SCOPE_HELD" for x in blocked["gate_states"])

bad = build_registry()
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["required_invariants"].remove("INV-M2D-GALILEAN-ADD-BEFORE-PROJECTILE")
must_closure_error(REQUEST, V3_MANIFEST, "E_ENG_REGISTRY_INVALID", registry=bad)

bad_manifest = copy.deepcopy(V3_MANIFEST)
bad_manifest["gate_extension_refs"] = ["policy/physics-technical-engineering-gates.v2.json"]
must_closure_error(REQUEST, bad_manifest, "E_ENG_GATE_EXTENSION_INVALID")

print("Physics Engineering Workbench v3 SBA23: PASS (diagnostic Passport; global Engineering Gate owns consumer authority)")
