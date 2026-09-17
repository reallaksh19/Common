#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from compile_engineering_closure import V3_REGISTRY_REF, compile_closure, load  # noqa: E402
from compile_engineering_passport import compile_passport  # noqa: E402

REQUEST = load("fixtures/engineering-workbench/m2d-sba04-request.v1.json")
MANIFEST = load("fixtures/engineering-workbench/m2d-sba04-manifest.v3.json")

DIRECT = {
    "PHY-M2D-VELOCITY-EVOLUTION",
    "PHY-M2D-VELOCITY-DIRECTION",
    "PHY-M2D-SPEED-MAGNITUDE",
    "PHY-M2D-SAME-HEIGHT-VELOCITY",
    "PHY-M2D-PERPENDICULAR-VELOCITY",
    "PHY-M2D-SPEED-AT-HEIGHT",
}
EXPECTED = {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    *DIRECT,
}
UNRELATED = {
    "PHY-M2D-MOVING-LAUNCHER", "PHY-GRAV-FORCE", "PHY-GRAV-FIELD",
    "PHY-NLM-INTERACTION", "PHY-NLM-FBD", "PHY-NLM-FIRST-LAW", "PHY-NLM-SECOND-LAW",
    "PHY-NLM-THIRD-LAW", "PHY-NLM-NORMAL", "PHY-NLM-TENSION", "PHY-NLM-FRICTION", "PHY-NLM-CONNECTED",
}


def gate(registry: dict, gate_id: str) -> dict:
    return next(row for row in registry["gates"] if row["subtopic_id"] == gate_id)


receipt = compile_closure(REQUEST, MANIFEST)
assert receipt["closure_status"] == "READY"
assert receipt["registry_ref"] == V3_REGISTRY_REF
assert set(receipt["direct_gate_ids"]) == DIRECT
assert set(receipt["transitive_gate_ids"]) == EXPECTED
assert set(receipt["transitive_gate_ids"]).isdisjoint(UNRELATED)
assert receipt["counts"] == {"direct_gate_count": 6, "transitive_gate_count": 11, "ready_gate_count": 11, "blocked_gate_count": 0}
assert all(row["status"] == "ENGINEERING_GATE_READY" for row in receipt["gate_states"])
assert receipt["source_item_status"] == "SOURCE_READY"
assert receipt["manifest_digest"].startswith("sha256:")

# Passport projects technical diagnostics only; global Engineering Gate owns consumer permission.
passport = compile_passport(REQUEST, receipt)
assert passport["schema_version"] == "2.0.0"
assert passport["technical_state"] == "ENGINEERING_READY"
assert passport["registry_digest"] == receipt["registry_digest"]
assert passport["source_item_status"] == "SOURCE_READY"
assert passport["consumer_authorization"] == "NOT_EVALUATED"
assert passport["publication_authorization"] == "NOT_IMPLIED"
assert all(row["status"] == "PASS" for row in passport["technical_coverage"].values())
assert {row["gate_id"] for row in passport["direct_gate_profiles"]} == DIRECT
assert all(row["provisional_badge"] == "HARD" for row in passport["direct_gate_profiles"])
assert any(row["hotspot_type"] == "INFERENTIAL_JUMP" for row in passport["fragility_hotspots"])

bad_registry = build_registry()
gate(bad_registry, "PHY-M2D-PERPENDICULAR-VELOCITY")["scope_state"] = "DRAFT"
blocked = compile_closure(REQUEST, MANIFEST, registry=bad_registry)
assert blocked["closure_status"] == "BLOCKED"
assert any(row["gate_id"] == "PHY-M2D-PERPENDICULAR-VELOCITY" and row["status"] == "ENGINEERING_GATE_INCOMPLETE" for row in blocked["gate_states"])

bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["required_gate_ids"].append("PHY-M2D-MOVING-LAUNCHER")
polluted = compile_closure(REQUEST, bad_manifest)
assert "PHY-M2D-MOVING-LAUNCHER" in polluted["transitive_gate_ids"]
assert set(receipt["transitive_gate_ids"]) == EXPECTED

print("Physics Engineering Workbench v3 SBA04: PASS (exact technical closure; Passport diagnostic only)")
