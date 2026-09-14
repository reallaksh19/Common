#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_b_layer_boundary import validate_boundary  # noqa: E402

load = lambda p: json.loads(p.read_text(encoding="utf-8"))
POLICY = load(ROOT / "policy" / "b-layer-runtime-boundary.v1.json")
ARCH = load(ROOT / "policy" / "architecture.v1.json")
BINDINGS = load(ROOT / "policy" / "role-bindings.v1.json")
PASSES = []


def expect(code, fn):
    try:
        fn()
    except AssertionError as exc:
        assert str(exc).startswith(code), (code, str(exc))
        PASSES.append(code)
        return
    raise AssertionError("expected " + code)


validate_boundary(POLICY, ARCH, BINDINGS)
PASSES.append("B_LAYER_BOUNDARY_BASELINE_VALID")

p = copy.deepcopy(POLICY)
p["learner_evidence"]["state_may_not_be_synthesized_from_unit_configuration"] = False
expect("UNIT_CONFIGURATION_MASQUERADES_AS_LEARNER_EVIDENCE", lambda: validate_boundary(p, ARCH, BINDINGS))

p = copy.deepcopy(POLICY)
p["handoffs"]["core2a_to_core2b_requires_legal_pool_ref_and_digest"] = False
expect("CORE2B_LEGAL_POOL_CUSTODY_MISSING", lambda: validate_boundary(p, ARCH, BINDINGS))

p = copy.deepcopy(POLICY)
p["transfer_selection"]["per_required_capability_state_required"] = False
expect("CORE2B_PER_CAPABILITY_EVIDENCE_MISSING", lambda: validate_boundary(p, ARCH, BINDINGS))

p = copy.deepcopy(POLICY)
p["transfer_selection"]["scalar_transfer_rank_may_not_be_sole_authorizer"] = False
expect("CORE2B_SCALAR_TRANSFER_RANK_OVERREACH", lambda: validate_boundary(p, ARCH, BINDINGS))

p = copy.deepcopy(POLICY)
p["transfer_selection"]["discrimination_and_synthesis_are_independent_dimensions"] = False
expect("CORE2B_DISCRIMINATION_SYNTHESIS_COLLAPSED", lambda: validate_boundary(p, ARCH, BINDINGS))

p = copy.deepcopy(POLICY)
p["repair_loop"]["repair_request_may_not_mutate_core1a_authority"] = False
expect("B_LAYER_REPAIR_MUTATES_A_LAYER", lambda: validate_boundary(p, ARCH, BINDINGS))

b = copy.deepcopy(BINDINGS)
b["roles"]["CORE1B"]["authority"] = "LEARNER_TEACHING_AUTHORITY"
expect("B_LAYER_AUTHORITY_BOUNDARY_WEAK:CORE1B", lambda: validate_boundary(POLICY, ARCH, b))

print(f"Blueprint B-layer boundary tests: PASS ({len(PASSES)} tests)")
