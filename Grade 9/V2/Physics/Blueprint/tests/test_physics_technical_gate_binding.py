#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from compile_engineering_closure import compile_closure  # noqa: E402
from validate_technical_gate_binding import BindingValidationError, load, validate, validate_v3  # noqa: E402

BINDING = load("topics/m2d-sba23-technical-gate-binding.v3.json")
LEGACY_V2 = load("topics/m2d-sba23-technical-gate-binding.v2.json")
LEGACY_V1 = load("topics/m2d-sba23-technical-gate-binding.v1.json")
EXPECTED = {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-MOVING-LAUNCHER",
}


def must_fail(doc, code):
    try:
        validate(doc)
    except BindingValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def must_fail_v3(doc, registry, code):
    try:
        validate_v3(doc, registry=registry)
    except BindingValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


# Active positive: v3 binds exact scoped closure authority while whole-registry identity is provenance only.
result = validate(BINDING)
assert result["status"] == "PASS"
assert result["binding_mode"] == "SCOPED_WORKBENCH_CLOSURE_RECEIPT"
assert result["bucket_id"] == "M2D-SBA-23"
assert result["primary_gate_id"] == "PHY-M2D-MOVING-LAUNCHER"
assert result["source_item_status"] == "SOURCE_HELD"
assert set(result["gate_closure"]) == EXPECTED
assert result["closure_receipt_id"] == "ENG-CLOSURE-M2D-SBA23-V3"
assert result["scoped_closure_digest"] == BINDING["scoped_closure_digest"]
assert result["aggregate_registry_custody"] == "PROVENANCE_ONLY"
assert "registry_digest" not in BINDING
assert "closure_receipt_digest" not in BINDING
assert "closure_logic_digest" not in BINDING
assert "declared_gate_closure" not in BINDING
assert "status" not in BINDING

# Falsifier 1: scoped custody cannot be stale or hand-edited.
bad = copy.deepcopy(BINDING)
bad["scoped_closure_digest"] = "sha256:" + "0" * 64
must_fail(bad, "E_BIND_SCOPED_CLOSURE_DIGEST_MISMATCH")

# Falsifier 2: unrelated subject-registry change alters provenance but not this scoped authority.
request = load(BINDING["engineering_request_ref"])
manifest = load(BINDING["engineering_manifest_ref"])
baseline = compile_closure(request, manifest)
grown = build_registry()
unrelated = next(g for g in grown["gates"] if g["subtopic_id"] == "PHY-ENERGY-CONSERVATION-LAW")
unrelated["title"] += " [unrelated registry-growth probe]"
mutated = compile_closure(request, manifest, registry=grown)
assert mutated["registry_digest"] != baseline["registry_digest"]
assert mutated["scoped_closure_digest"] == baseline["scoped_closure_digest"]
growth_result = validate_v3(BINDING, registry=grown)
assert growth_result["scoped_closure_digest"] == BINDING["scoped_closure_digest"]

# Falsifier 3: changing a gate inside the reachable closure must invalidate scoped custody.
scoped_change = build_registry()
scoped_gate = next(g for g in scoped_change["gates"] if g["subtopic_id"] == "PHY-VEC-BASICS")
scoped_gate["title"] += " [scoped mutation probe]"
must_fail_v3(BINDING, scoped_change, "E_BIND_SCOPED_CLOSURE_DIGEST_MISMATCH")

# Falsifier 4: a binding cannot point at a bucket different from the Workbench manifest scope.
bad = copy.deepcopy(BINDING)
bad["bucket_id"] = "M2D-SBA-OTHER"
must_fail(bad, "E_BIND_BUCKET_SCOPE_MISMATCH")

# Falsifier 5: primary gate must be one of the exact direct Workbench requirements.
bad = copy.deepcopy(BINDING)
bad["primary_gate_id"] = "PHY-VEC-BASICS"
must_fail(bad, "E_BIND_PRIMARY_NOT_DIRECT")

# v2 remains readable as a historical contract, but its aggregate-sensitive pinned receipt is
# intentionally stale after unrelated canonical registry growth. This is why active custody moved to v3.
must_fail(LEGACY_V2, "E_BIND_RECEIPT_DIGEST_MISMATCH")

# v1 remains readable and explicitly labelled legacy.
legacy_result = validate(LEGACY_V1)
assert legacy_result["status"] == "PASS"
assert legacy_result["binding_mode"] == "LEGACY_DECLARED_CLOSURE"
assert set(legacy_result["gate_closure"]) == EXPECTED

# Legacy manual closure drift still fails while v1 remains supported.
bad = copy.deepcopy(LEGACY_V1)
bad["declared_gate_closure"].remove("PHY-VEC-ADD-SUB")
must_fail(bad, "E_BIND_CLOSURE_MISMATCH")

print("Physics SBA23 technical-gate binding: PASS (scope-stable v3 custody + subject-growth invariance + v2/v1 regression)")
