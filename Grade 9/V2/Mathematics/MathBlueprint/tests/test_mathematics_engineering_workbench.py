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
    compile_registry_proof,
    digest,
    load,
    resolve_manifest,
)

REGISTRY = load("policies/mathematics-technical-engineering-gates.v1.json")


def gate_ids(registry: dict = REGISTRY) -> list[str]:
    return [gate["subtopic_id"] for gate in registry["subtopic_gates"]]


def gate(registry: dict, gate_id: str) -> dict:
    return next(row for row in registry["subtopic_gates"] if row["subtopic_id"] == gate_id)


def request_for_gate(gate_id: str, suffix: str = "TEST", depth: str = "STANDARD") -> dict:
    safe = gate_id.replace("-", "_")
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": f"MATH-ENG-REQ-{suffix}_{safe}",
        "scope_kind": "ENGINEERING_GATE",
        "scope_refs": [gate_id],
        "engineering_depth": depth,
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }


def request_for_bucket(bucket_id: str, suffix: str = "BUCKET", depth: str = "STANDARD") -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": f"MATH-ENG-REQ-{suffix}",
        "scope_kind": "BUCKET",
        "scope_refs": [bucket_id],
        "engineering_depth": depth,
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }


class MathematicsEngineeringWorkbenchTests(unittest.TestCase):
    def test_registry_proof_is_generated_from_every_current_gate(self):
        proof = compile_registry_proof(copy.deepcopy(REGISTRY))
        ids = gate_ids()
        self.assertEqual(proof["gate_count"], len(ids))
        self.assertEqual({row["gate_id"] for row in proof["gate_proofs"]}, set(ids))
        self.assertEqual(proof["ready_gate_count"], len(ids))
        self.assertEqual(proof["blocked_gate_ids"], [])
        self.assertTrue(proof["all_registry_gates_blueprint_admissible"])

    def test_every_gate_resolves_by_exact_registry_identity(self):
        for gate_id in gate_ids():
            request = request_for_gate(gate_id)
            manifest = resolve_manifest(request, copy.deepcopy(REGISTRY))
            self.assertEqual(manifest["resolution_mode"], "GATE_IDENTITY")
            self.assertEqual(manifest["direct_gate_ids"], [gate_id])
            receipt = compile_closure(request, manifest, copy.deepcopy(REGISTRY))
            self.assertEqual(receipt["direct_gate_ids"], [gate_id])
            self.assertIn(gate_id, receipt["transitive_gate_ids"])
            self.assertEqual(receipt["technical_authorization"], "ALLOWED")
            passport = compile_passport(request, manifest, receipt)
            self.assertEqual(passport["blueprint_technical_authorization"], "ALLOWED")

    def test_every_registry_bucket_resolves_only_from_linked_buckets(self):
        buckets = sorted({b for g in REGISTRY["subtopic_gates"] for b in g.get("linked_buckets", [])})
        self.assertTrue(buckets)
        for index, bucket_id in enumerate(buckets):
            request = request_for_bucket(bucket_id, f"BUCKET_{index}")
            manifest = resolve_manifest(request, copy.deepcopy(REGISTRY))
            expected = [
                g["subtopic_id"]
                for g in REGISTRY["subtopic_gates"]
                if bucket_id in set(g.get("linked_buckets") or [])
            ]
            self.assertEqual(manifest["resolution_mode"], "REGISTRY_LINKED_BUCKET")
            self.assertEqual(manifest["direct_gate_ids"], expected)

    def test_unknown_scope_has_no_fuzzy_or_memory_fallback(self):
        request = request_for_bucket("BUCKET-NOT-IN-REGISTRY")
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(request, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "MATH_ENG_SCOPE_UNMAPPED")

    def test_manifest_cannot_override_registry_resolution(self):
        ids = gate_ids()
        request = request_for_gate(ids[0], "FORGED")
        manifest = resolve_manifest(request, copy.deepcopy(REGISTRY))
        manifest["direct_gate_ids"] = [ids[-1]]
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            compile_closure(request, manifest, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "MATH_ENG_MANIFEST_STALE_OR_FORGED")

    def test_authoritative_incomplete_gate_blocks_blueprint(self):
        registry = copy.deepcopy(REGISTRY)
        target_id = gate_ids(registry)[0]
        target = gate(registry, target_id)
        target["technical_readiness"] = "ENGINEERING_GATE_INCOMPLETE"
        first_check = next(iter(target["release_checklist"]))
        target["release_checklist"][first_check] = False
        request = request_for_gate(target_id, "INCOMPLETE")
        manifest = resolve_manifest(request, registry)
        receipt = compile_closure(request, manifest, registry)
        state = next(row for row in receipt["gate_states"] if row["gate_id"] == target_id)
        self.assertEqual(state["authoritative_technical_readiness"], "ENGINEERING_GATE_INCOMPLETE")
        self.assertFalse(state["blueprint_admissible"])
        self.assertEqual(receipt["closure_status"], "BLOCKED")
        self.assertEqual(receipt["technical_authorization"], "BLOCKED")

    def test_ready_gate_with_broken_engineering_checklist_is_rejected_upstream(self):
        registry = copy.deepcopy(REGISTRY)
        target_id = gate_ids(registry)[0]
        target = gate(registry, target_id)
        target["technical_readiness"] = "ENGINEERING_GATE_READY"
        first_check = next(iter(target["release_checklist"]))
        target["release_checklist"][first_check] = False
        request = request_for_gate(target_id, "BROKEN_READY")
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(request, registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_REGISTRY_INVALID")

    def test_research_depth_is_a_generic_stricter_contract(self):
        registry = copy.deepcopy(REGISTRY)
        target_id = gate_ids(registry)[0]
        target = gate(registry, target_id)
        target["model_conditions"] = []

        standard = request_for_gate(target_id, "DEPTH_STANDARD", "STANDARD")
        standard_manifest = resolve_manifest(standard, registry)
        standard_receipt = compile_closure(standard, standard_manifest, registry)
        self.assertEqual(standard_receipt["technical_authorization"], "ALLOWED")

        research = request_for_gate(target_id, "DEPTH_RESEARCH", "RESEARCH")
        research_manifest = resolve_manifest(research, registry)
        research_receipt = compile_closure(research, research_manifest, registry)
        state = next(row for row in research_receipt["gate_states"] if row["gate_id"] == target_id)
        self.assertIn("MATH_ENG_DEPTH_MODEL_CONDITIONS_INSUFFICIENT", state["failure_codes"])
        self.assertEqual(research_receipt["technical_authorization"], "BLOCKED")
        passport = compile_passport(research, research_manifest, research_receipt, registry)
        self.assertEqual(passport["engineering_depth"], "RESEARCH")
        self.assertEqual(passport["blueprint_technical_authorization"], "BLOCKED")

    def test_subject_guard_rejects_non_math_before_resolution(self):
        request = request_for_gate(gate_ids()[0], "SUBJECT")
        request["subject"] = "PHYSICS"
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(request, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "MATH_ENG_REQUEST_SCHEMA")

    def test_dependency_cycle_is_rejected_by_upstream_engineering_validation(self):
        registry = copy.deepcopy(REGISTRY)
        child = next((g for g in registry["subtopic_gates"] if g.get("prerequisite_ids")), None)
        if child is None:
            self.skipTest("registry contains no prerequisite edges")
        parent_id = next(p for p in child["prerequisite_ids"] if p.startswith("MATH-"))
        gate(registry, parent_id)["prerequisite_ids"].append(child["subtopic_id"])
        request = request_for_gate(child["subtopic_id"], "CYCLE")
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(request, registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_REGISTRY_INVALID")

    def test_receipt_custody_changes_when_authoritative_registry_changes(self):
        target_id = gate_ids()[0]
        request = request_for_gate(target_id, "DIGEST")
        registry_a = copy.deepcopy(REGISTRY)
        manifest_a = resolve_manifest(request, registry_a)
        receipt_a = compile_closure(request, manifest_a, registry_a)

        registry_b = copy.deepcopy(REGISTRY)
        gate(registry_b, target_id)["learner_title"] += " revised"
        manifest_b = resolve_manifest(request, registry_b)
        receipt_b = compile_closure(request, manifest_b, registry_b)

        self.assertNotEqual(receipt_a["registry_digest"], receipt_b["registry_digest"])
        self.assertNotEqual(digest(receipt_a), digest(receipt_b))
        self.assertEqual(receipt_a["validator_contract_digest"], receipt_b["validator_contract_digest"])


if __name__ == "__main__":
    unittest.main()
