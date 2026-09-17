#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_mathematics_engineering_workbench import (  # noqa: E402
    compile_binding,
    compile_closure,
    load,
    resolve_manifest,
)
from validate_mathematics_engineering_binding import (  # noqa: E402
    MathematicsEngineeringBindingError,
    validate,
)

REGISTRY = load("policies/mathematics-technical-engineering-gates.v1.json")


def first_gate_id(registry: dict = REGISTRY) -> str:
    return registry["subtopic_gates"][0]["subtopic_id"]


def request_for(gate_id: str, suffix: str = "BIND") -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": f"MATH-ENG-REQ-{suffix}",
        "scope_kind": "ENGINEERING_GATE",
        "scope_refs": [gate_id],
        "engineering_depth": "STANDARD",
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }


def current_bundle(registry: dict | None = None):
    registry = registry or copy.deepcopy(REGISTRY)
    request = request_for(first_gate_id(registry))
    manifest = resolve_manifest(request, registry)
    receipt = compile_closure(request, manifest, registry)
    binding = compile_binding(request, manifest, receipt, "CANONICAL_DOMAIN_REGISTRY")
    return request, manifest, receipt, binding, registry


class MathematicsEngineeringBindingTests(unittest.TestCase):
    def test_runtime_binding_revalidates_current_engineering_authority(self):
        request, manifest, _, binding, registry = current_bundle()
        result = validate(binding, request, manifest, registry)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["technical_authorization"], "ALLOWED")
        self.assertEqual(result["publication_authorization"], "NOT_IMPLIED")

    def test_registry_change_stales_runtime_binding(self):
        request, manifest, _, binding, registry = current_bundle()
        registry["subtopic_gates"][0]["learner_title"] += " revised"
        with self.assertRaises(MathematicsEngineeringBindingError) as ctx:
            validate(binding, request, manifest, registry)
        self.assertIn(ctx.exception.code, {"MATH_ENG_BIND_RECEIPT_DIGEST_MISMATCH", "MATH_ENG_BIND_REGISTRY_DIGEST_MISMATCH"})

    def test_scope_change_stales_runtime_binding(self):
        request, manifest, _, binding, registry = current_bundle()
        if len(registry["subtopic_gates"]) < 2:
            self.skipTest("need at least two gates")
        request2 = request_for(registry["subtopic_gates"][1]["subtopic_id"], "BIND2")
        manifest2 = resolve_manifest(request2, registry)
        with self.assertRaises(MathematicsEngineeringBindingError):
            validate(binding, request2, manifest2, registry)

    def test_incomplete_authoritative_gate_cannot_be_consumed(self):
        request, manifest, _, binding, registry = current_bundle()
        target = registry["subtopic_gates"][0]
        target["technical_readiness"] = "ENGINEERING_GATE_INCOMPLETE"
        target["release_checklist"][next(iter(target["release_checklist"]))] = False
        with self.assertRaises(MathematicsEngineeringBindingError) as ctx:
            validate(binding, request, manifest, registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_BIND_CLOSURE_BLOCKED")


if __name__ == "__main__":
    unittest.main()
