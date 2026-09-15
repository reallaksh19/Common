#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_technical_gate_binding import BindingValidationError, load, validate  # noqa: E402

BINDING = load("topics/m2d-sba23-technical-gate-binding.v2.json")
LEGACY = load("topics/m2d-sba23-technical-gate-binding.v1.json")
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


# Positive: v2 binding owns no manual closure/readiness copy; it custodies the exact Workbench receipt.
result = validate(BINDING)
assert result["status"] == "PASS"
assert result["binding_mode"] == "EXACT_WORKBENCH_CLOSURE_RECEIPT"
assert result["bucket_id"] == "M2D-SBA-23"
assert result["primary_gate_id"] == "PHY-M2D-MOVING-LAUNCHER"
assert result["source_item_status"] == "SOURCE_HELD"
assert set(result["gate_closure"]) == EXPECTED
assert result["closure_receipt_id"] == "ENG-CLOSURE-M2D-SBA23-V3"
assert result["closure_receipt_digest"] == BINDING["closure_receipt_digest"]
assert result["closure_logic_digest"] == BINDING["closure_logic_digest"]
assert result["registry_digest"] == BINDING["registry_digest"]
assert "declared_gate_closure" not in BINDING
assert "status" not in BINDING

# Falsifier 1: full receipt custody cannot be stale or hand-edited.
bad = copy.deepcopy(BINDING)
bad["closure_receipt_digest"] = "sha256:" + "0" * 64
must_fail(bad, "E_BIND_RECEIPT_DIGEST_MISMATCH")

# Falsifier 2: closure-logic digest is independently custodied.
bad = copy.deepcopy(BINDING)
bad["closure_logic_digest"] = "sha256:" + "1" * 64
must_fail(bad, "E_BIND_CLOSURE_DIGEST_MISMATCH")

# Falsifier 3: exact engineering registry digest cannot drift.
bad = copy.deepcopy(BINDING)
bad["registry_digest"] = "sha256:" + "2" * 64
must_fail(bad, "E_BIND_REGISTRY_DIGEST_MISMATCH")

# Falsifier 4: a binding cannot point at a bucket different from the Workbench manifest scope.
bad = copy.deepcopy(BINDING)
bad["bucket_id"] = "M2D-SBA-OTHER"
must_fail(bad, "E_BIND_BUCKET_SCOPE_MISMATCH")

# Falsifier 5: primary gate must be one of the exact direct Workbench requirements.
bad = copy.deepcopy(BINDING)
bad["primary_gate_id"] = "PHY-VEC-BASICS"
must_fail(bad, "E_BIND_PRIMARY_NOT_DIRECT")

# Migration regression: legacy v1 remains readable but is explicitly labelled legacy.
legacy_result = validate(LEGACY)
assert legacy_result["status"] == "PASS"
assert legacy_result["binding_mode"] == "LEGACY_DECLARED_CLOSURE"
assert set(legacy_result["gate_closure"]) == EXPECTED

# Legacy manual closure drift still fails while v1 remains supported.
bad = copy.deepcopy(LEGACY)
bad["declared_gate_closure"].remove("PHY-VEC-ADD-SUB")
must_fail(bad, "E_BIND_CLOSURE_MISMATCH")

print("Physics SBA23 technical-gate binding: PASS (exact Workbench receipt custody + stale-binding falsifiers + v1 regression)")
