#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_technical_gate_binding import BindingValidationError, load, validate  # noqa: E402

BINDING = load("topics/m2d-sba23-technical-gate-binding.v1.json")


def must_fail(doc, code):
    try:
        validate(doc)
    except BindingValidationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


# Positive: technical readiness can close while frozen Q15 source custody remains held.
result = validate(BINDING)
assert result["status"] == "PASS"
assert result["bucket_id"] == "M2D-SBA-23"
assert result["primary_gate_id"] == "PHY-M2D-MOVING-LAUNCHER"
assert result["source_item_status"] == "SOURCE_HELD"
assert set(result["gate_closure"]) == {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-MOVING-LAUNCHER",
}

# Falsifier 1: an upstream vector prerequisite cannot be silently omitted.
bad = copy.deepcopy(BINDING)
bad["declared_gate_closure"].remove("PHY-VEC-ADD-SUB")
must_fail(bad, "E_BIND_CLOSURE_MISMATCH")

# Falsifier 2: unrelated technical gates cannot be padded into the closure.
bad = copy.deepcopy(BINDING)
bad["declared_gate_closure"].append("PHY-NLM-FBD")
must_fail(bad, "E_BIND_CLOSURE_MISMATCH")

# Falsifier 3: unknown primary gate is fail-closed.
bad = copy.deepcopy(BINDING)
bad["primary_gate_id"] = "PHY-M2D-NOT-REAL"
must_fail(bad, "E_BIND_PRIMARY_UNKNOWN")

# Falsifier 4: a fully ready closure cannot be mislabelled as blocked without changing upstream gate state.
bad = copy.deepcopy(BINDING)
bad["status"] = "TECHNICAL_GATE_BLOCKED"
must_fail(bad, "E_BIND_STATUS_MISMATCH")

print("Physics SBA23 technical-gate binding: PASS (closure + authority-boundary falsifiers)")
