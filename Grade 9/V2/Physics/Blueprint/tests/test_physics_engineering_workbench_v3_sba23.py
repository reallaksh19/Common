#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from compile_engineering_closure import EngineeringClosureError, compile_closure, load  # noqa: E402
from compile_engineering_passport import compile_passport  # noqa: E402
from validate_ccu_engineering_ready import validate_engineered_ccu  # noqa: E402

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


# v3 is now a real Workbench source: derived readiness, same exact SBA23 closure.
v3 = compile_closure(REQUEST, V3_MANIFEST)
assert v3["closure_status"] == "READY"
assert v3["registry_ref"] == "GENERATED:physics-technical-engineering-gates.v3-sba23"
assert set(v3["transitive_gate_ids"]) == EXPECTED
assert v3["counts"] == {
    "direct_gate_count": 1,
    "transitive_gate_count": 6,
    "ready_gate_count": 6,
    "blocked_gate_count": 0,
}
assert all(x["status"] == "ENGINEERING_GATE_READY" for x in v3["gate_states"])
assert v3["source_item_status"] == "SOURCE_HELD"

# Enriched Passport is a projection of current validated registry + exact receipt, never a second authority source.
passport = compile_passport(REQUEST, v3)
assert passport["schema_version"] == "2.0.0"
assert passport["technical_state"] == "ENGINEERING_READY"
assert passport["registry_digest"] == v3["registry_digest"]
assert passport["publication_authorization"] == "NOT_IMPLIED"
assert passport["source_item_status"] == "SOURCE_HELD"
assert passport["ccu_technical_authorization"] == "ALLOWED"
assert all(row["status"] == "PASS" for row in passport["technical_coverage"].values())
assert passport["technical_coverage"]["concepts"]["count"] >= 1
assert passport["technical_coverage"]["representations"]["count"] >= 1
assert passport["technical_coverage"]["transformations"]["count"] >= 1
assert passport["direct_gate_profiles"] == [{
    "gate_id": "PHY-M2D-MOVING-LAUNCHER",
    "provisional_badge": "HARD",
    "maturity": "ENGINEERING",
    "dimensions": {
        "prerequisite_depth": 3,
        "element_interactivity": 3,
        "inferential_jump_severity": 3,
        "representation_translation": 3,
        "model_discrimination": 3,
        "sign_or_frame_sensitivity": 3,
        "multi_step_dependency": 3,
        "abstraction": 3,
        "misconception_density": 3,
        "synthesis": 3,
    },
}]
assert any(x["hotspot_type"] == "INFERENTIAL_JUMP" and x["ref"] == "RS-M2D-ML-FRAME-CONVERSION" for x in passport["fragility_hotspots"])
assert any(x["hotspot_type"] == "DIFFICULTY_DIMENSION" and x["ref"] == "sign_or_frame_sensitivity" for x in passport["fragility_hotspots"])

# Exact CCU boundary operates on the v3 closure without weakening source custody.
ccu = validate_engineered_ccu(REQUEST, V3_MANIFEST, CCU)
assert ccu["status"] == "PASS"
assert ccu["engineering_gate_count"] == 6
assert ccu["engineering_closure_digest"] == v3["closure_digest"]
assert ccu["source_item_status"] == "SOURCE_HELD"

# Legacy v2 manifest remains valid during migration and proves closure equivalence.
v2 = compile_closure(REQUEST, V2_MANIFEST)
assert v2["closure_status"] == "READY"
assert set(v2["transitive_gate_ids"]) == EXPECTED
assert [x["gate_id"] for x in v2["gate_states"]] == [x["gate_id"] for x in v3["gate_states"]]
legacy_passport = compile_passport(REQUEST, v2)
assert legacy_passport["schema_version"] == "1.0.0"
assert "technical_coverage" not in legacy_passport

# v3 DRAFT is a derived engineering blocker; no source status field can self-promote it.
bad = build_registry()
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["scope_state"] = "DRAFT"
blocked = compile_closure(REQUEST, V3_MANIFEST, registry=bad)
assert blocked["closure_status"] == "BLOCKED"
assert any(x["gate_id"] == "PHY-M2D-MOVING-LAUNCHER" and x["status"] == "ENGINEERING_GATE_INCOMPLETE" for x in blocked["gate_states"])
assert any(x["code"] == "E_ENG_GATE_NOT_READY" for x in blocked["blockers"])

# SOURCE_SCOPE_HELD is independently visible and blocks CCU technical authorization.
bad = build_registry()
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["scope_state"] = "SOURCE_SCOPE_HELD"
blocked = compile_closure(REQUEST, V3_MANIFEST, registry=bad)
assert blocked["closure_status"] == "BLOCKED"
assert any(x["status"] == "SOURCE_SCOPE_HELD" for x in blocked["gate_states"])

# Invalid active technical content fails before any closure receipt can be issued.
bad = build_registry()
gate(bad, "PHY-M2D-MOVING-LAUNCHER")["required_invariants"].remove("INV-M2D-GALILEAN-ADD-BEFORE-PROJECTILE")
must_closure_error(REQUEST, V3_MANIFEST, "E_ENG_REGISTRY_INVALID", registry=bad)

# v2 extension mechanism cannot be silently attached to the generated v3 registry.
bad_manifest = copy.deepcopy(V3_MANIFEST)
bad_manifest["gate_extension_refs"] = ["policy/physics-technical-engineering-gates.v2.json"]
must_closure_error(REQUEST, bad_manifest, "E_ENG_GATE_EXTENSION_INVALID")

print("Physics Engineering Workbench v3 SBA23: PASS (derived v3 readiness + enriched passport + v2 equivalence + CCU boundary)")
