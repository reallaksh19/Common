#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_mathematics_engineering_workbench import (  # noqa: E402
    MathematicsEngineeringWorkbenchError,
    compile_closure,
    compile_passport,
    digest,
    load,
)

REQUEST = load("fixtures/engineering-workbench/quad-equations-request.v1.json")
MANIFEST = load("fixtures/engineering-workbench/quad-equations-manifest.v1.json")
REGISTRY = load("policies/mathematics-technical-engineering-gates.v1.json")
PROFILE = load("policies/mathematics-engineering-gate-invariants.v1.json")


def gate(doc: dict, gate_id: str) -> dict:
    return next(g for g in doc["subtopic_gates"] if g["subtopic_id"] == gate_id)


class MathematicsEngineeringWorkbenchTests(unittest.TestCase):
    def test_quadratic_closure_is_validator_derived(self):
        receipt = compile_closure(REQUEST, MANIFEST, copy.deepcopy(REGISTRY), PROFILE)
        self.assertEqual(receipt["closure_status"], "READY")
        self.assertEqual(receipt["direct_gate_ids"], ["MATH-QUAD-EQUATIONS"])
        self.assertEqual(
            receipt["transitive_gate_ids"],
            ["MATH-NUM-RADICALS", "MATH-ALG-POLYNOMIALS", "MATH-QUAD-EQUATIONS"],
        )
        self.assertEqual(receipt["counts"]["ready_gate_count"], 3)
        self.assertEqual(receipt["counts"]["transitive_gate_count"], 3)
        self.assertTrue(all(x["declared_technical_readiness_ignored"] for x in receipt["gate_states"]))
        self.assertTrue(all(x["declared_release_checklist_ignored"] for x in receipt["gate_states"]))
        passport = compile_passport(REQUEST, receipt)
        self.assertEqual(passport["technical_state"], "ENGINEERING_READY")
        self.assertEqual(passport["gate_count"], 3)
        self.assertEqual(passport["ccu_technical_authorization"], "ALLOWED")
        self.assertEqual(passport["publication_authorization"], "NOT_IMPLIED")

    def test_self_declared_incomplete_cannot_demote_valid_gate(self):
        registry = copy.deepcopy(REGISTRY)
        quad = gate(registry, "MATH-QUAD-EQUATIONS")
        quad["technical_readiness"] = "ENGINEERING_GATE_INCOMPLETE"
        quad["release_checklist"]["reasoning_chain_complete"] = False
        receipt = compile_closure(REQUEST, MANIFEST, registry, PROFILE)
        state = next(x for x in receipt["gate_states"] if x["gate_id"] == "MATH-QUAD-EQUATIONS")
        self.assertEqual(state["derived_status"], "ENGINEERING_GATE_READY")
        self.assertEqual(receipt["closure_status"], "READY")

    def test_self_declared_ready_cannot_rescue_missing_workbench_requirement(self):
        registry = copy.deepcopy(REGISTRY)
        quad = gate(registry, "MATH-QUAD-EQUATIONS")
        quad["technical_readiness"] = "ENGINEERING_GATE_READY"
        for key in quad["release_checklist"]:
            quad["release_checklist"][key] = True
        quad["reasoning_sequence"] = quad["reasoning_sequence"][:1]
        receipt = compile_closure(REQUEST, MANIFEST, registry, PROFILE)
        state = next(x for x in receipt["gate_states"] if x["gate_id"] == "MATH-QUAD-EQUATIONS")
        self.assertEqual(state["derived_status"], "ENGINEERING_GATE_INCOMPLETE")
        self.assertIn("MATH_ENG_REASONING_SEQUENCE_INCOMPLETE", state["failure_codes"])
        self.assertEqual(receipt["closure_status"], "BLOCKED")

    def test_core_role_mix_is_not_a_technical_readiness_proxy(self):
        receipt = compile_closure(REQUEST, MANIFEST, copy.deepcopy(REGISTRY), PROFILE)
        quad = gate(REGISTRY, "MATH-QUAD-EQUATIONS")
        roles = {x["target_core_role"] for x in quad["required_transformations"]}
        self.assertNotIn("CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION", roles)
        state = next(x for x in receipt["gate_states"] if x["gate_id"] == "MATH-QUAD-EQUATIONS")
        self.assertEqual(state["derived_status"], "ENGINEERING_GATE_READY")

    def test_external_invariant_profile_is_authority(self):
        profile = copy.deepcopy(PROFILE)
        profile["required_gates"]["MATH-QUAD-EQUATIONS"]["required_concepts"].append("CON-MATH-NOT-PRESENT")
        receipt = compile_closure(REQUEST, MANIFEST, copy.deepcopy(REGISTRY), profile)
        state = next(x for x in receipt["gate_states"] if x["gate_id"] == "MATH-QUAD-EQUATIONS")
        self.assertEqual(state["derived_status"], "ENGINEERING_GATE_INCOMPLETE")
        self.assertIn("MATH_ENG_REQUIRED_CONCEPT_MISSING", state["failure_codes"])

    def test_source_scope_hold_blocks_closure(self):
        registry = copy.deepcopy(REGISTRY)
        quad = gate(registry, "MATH-QUAD-EQUATIONS")
        quad["provenance"]["source_scope"] = "HELD_SCOPE"
        receipt = compile_closure(REQUEST, MANIFEST, registry, PROFILE)
        state = next(x for x in receipt["gate_states"] if x["gate_id"] == "MATH-QUAD-EQUATIONS")
        self.assertEqual(state["derived_status"], "SOURCE_SCOPE_HELD")
        self.assertEqual(receipt["closure_status"], "BLOCKED")

    def test_subject_guard_rejects_non_math_request(self):
        request = copy.deepcopy(REQUEST)
        request["subject"] = "PHYSICS"
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            compile_closure(request, MANIFEST, copy.deepcopy(REGISTRY), PROFILE)
        self.assertEqual(ctx.exception.code, "MATH_ENG_REQUEST_SCHEMA")

    def test_unknown_direct_gate_fails_closed(self):
        manifest = copy.deepcopy(MANIFEST)
        manifest["direct_gate_ids"] = ["MATH-FAKE-GATE"]
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            compile_closure(REQUEST, manifest, copy.deepcopy(REGISTRY), PROFILE)
        self.assertEqual(ctx.exception.code, "MATH_ENG_GATE_UNKNOWN")

    def test_dependency_cycle_fails_closed(self):
        registry = copy.deepcopy(REGISTRY)
        poly = gate(registry, "MATH-ALG-POLYNOMIALS")
        poly["prerequisite_ids"].append("MATH-QUAD-EQUATIONS")
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            compile_closure(REQUEST, MANIFEST, registry, PROFILE)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DEPENDENCY_CYCLE")

    def test_receipt_digest_changes_when_registry_changes(self):
        receipt = compile_closure(REQUEST, MANIFEST, copy.deepcopy(REGISTRY), PROFILE)
        registry = copy.deepcopy(REGISTRY)
        gate(registry, "MATH-NUM-RADICALS")["learner_title"] += " (revised)"
        changed = compile_closure(REQUEST, MANIFEST, registry, PROFILE)
        self.assertNotEqual(receipt["registry_digest"], changed["registry_digest"])
        self.assertNotEqual(digest(receipt), digest(changed))


if __name__ == "__main__":
    unittest.main()
