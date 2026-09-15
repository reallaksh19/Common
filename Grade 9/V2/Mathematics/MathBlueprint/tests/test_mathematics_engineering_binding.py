#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_mathematics_engineering_workbench import compile_closure, digest, load  # noqa: E402
from validate_mathematics_engineering_binding import (  # noqa: E402
    MathematicsEngineeringBindingError,
    validate,
)

REQUEST_REF = "fixtures/engineering-workbench/quad-equations-request.v1.json"
MANIFEST_REF = "fixtures/engineering-workbench/quad-equations-manifest.v1.json"
REQUEST = load(REQUEST_REF)
MANIFEST = load(MANIFEST_REF)
REGISTRY = load("policies/mathematics-technical-engineering-gates.v1.json")
PROFILE = load("policies/mathematics-engineering-gate-invariants.v1.json")


def gate(doc: dict, gate_id: str) -> dict:
    return next(g for g in doc["subtopic_gates"] if g["subtopic_id"] == gate_id)


def make_binding(registry: dict | None = None, profile: dict | None = None) -> dict:
    registry = registry or copy.deepcopy(REGISTRY)
    profile = profile or copy.deepcopy(PROFILE)
    receipt = compile_closure(REQUEST, MANIFEST, registry, profile)
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "binding_id": "MATH-ENG-BIND-QUAD-001",
        "request_ref": REQUEST_REF,
        "manifest_ref": MANIFEST_REF,
        "closure_receipt_id": receipt["receipt_id"],
        "closure_receipt_digest": digest(receipt),
        "registry_digest": receipt["registry_digest"],
        "invariant_profile_digest": receipt["invariant_profile_digest"],
        "downstream_consumer": "CANONICAL_DOMAIN_REGISTRY"
    }


class MathematicsEngineeringBindingTests(unittest.TestCase):
    def test_exact_current_closure_binding_passes(self):
        binding = make_binding()
        result = validate(binding, copy.deepcopy(REGISTRY), copy.deepcopy(PROFILE))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["technical_authorization"], "ALLOWED")
        self.assertEqual(result["publication_authorization"], "NOT_IMPLIED")

    def test_stale_registry_binding_fails(self):
        binding = make_binding()
        registry = copy.deepcopy(REGISTRY)
        gate(registry, "MATH-NUM-RADICALS")["learner_title"] += " revised"
        with self.assertRaises(MathematicsEngineeringBindingError) as ctx:
            validate(binding, registry, copy.deepcopy(PROFILE))
        self.assertIn(ctx.exception.code, {"MATH_ENG_BIND_RECEIPT_DIGEST_MISMATCH", "MATH_ENG_BIND_REGISTRY_DIGEST_MISMATCH"})

    def test_stale_invariant_profile_binding_fails(self):
        binding = make_binding()
        profile = copy.deepcopy(PROFILE)
        profile["authority_rule"] += " revised"
        with self.assertRaises(MathematicsEngineeringBindingError) as ctx:
            validate(binding, copy.deepcopy(REGISTRY), profile)
        self.assertIn(ctx.exception.code, {"MATH_ENG_BIND_RECEIPT_DIGEST_MISMATCH", "MATH_ENG_BIND_PROFILE_DIGEST_MISMATCH"})

    def test_blocked_current_closure_cannot_be_consumed(self):
        binding = make_binding()
        registry = copy.deepcopy(REGISTRY)
        quad = gate(registry, "MATH-QUAD-EQUATIONS")
        quad["reasoning_sequence"] = quad["reasoning_sequence"][:1]
        with self.assertRaises(MathematicsEngineeringBindingError) as ctx:
            validate(binding, registry, copy.deepcopy(PROFILE))
        self.assertEqual(ctx.exception.code, "MATH_ENG_BIND_CLOSURE_BLOCKED")


if __name__ == "__main__":
    unittest.main()
