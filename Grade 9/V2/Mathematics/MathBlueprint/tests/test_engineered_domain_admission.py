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
from validate_engineered_domain_admission import (  # noqa: E402
    MathematicsEngineeredDomainAdmissionError,
    validate,
)

TECH_REGISTRY = load("policies/mathematics-technical-engineering-gates.v1.json")


def synthetic_domain_registry() -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "registry_id": "MATH-REG-SYNTHETIC-001",
        "run_ref": "RUN:SYNTHETIC",
        "source_manifest_refs": ["GT:SYNTHETIC"],
        "join_refs": ["J:SYNTHETIC"],
        "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
        "assets": [{
            "asset_id": "REG-MATH-CON-SYNTHETIC",
            "asset_type": "CONCEPT",
            "subtopic_id": "BP-SCOPE-001",
            "title": "Synthetic canonical concept",
            "authority_class": "CORE1_SEMANTIC",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": ["GT:SYNTHETIC"],
            "core1_refs": ["K:SYNTHETIC"],
            "core2_refs": [],
            "validation_refs": ["V:SYNTHETIC"],
            "join_ref": "J:SYNTHETIC",
            "depends_on": [],
            "payload": {
                "statement": "Synthetic semantic object used only to test generic Engineering admission.",
                "prerequisite_refs": [],
                "implications": ["Admission logic must not depend on a remembered mathematics topic."]
            },
            "provenance_note": "Synthetic case-neutral registry for Engineering admission tests."
        }]
    }


def runtime_bundle(consumer: str = "CANONICAL_DOMAIN_REGISTRY"):
    registry = copy.deepcopy(TECH_REGISTRY)
    gate_id = registry["subtopic_gates"][0]["subtopic_id"]
    request = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": "MATH-ENG-REQ-DOMAIN-ADMISSION",
        "scope_kind": "ENGINEERING_GATE",
        "scope_refs": [gate_id],
        "engineering_depth": "STANDARD",
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }
    manifest = resolve_manifest(request, registry)
    receipt = compile_closure(request, manifest, registry)
    binding = compile_binding(request, manifest, receipt, consumer)
    admission = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "admission_id": "MATH-ENG-DOMAIN-ADMISSION-SYNTHETIC",
        "domain_registry_ref": "runtime://domain-registry",
        "engineering_request_ref": "runtime://engineering-request",
        "engineering_manifest_ref": "runtime://engineering-manifest",
        "engineering_binding_ref": "runtime://engineering-binding",
        "subtopic_gate_map": [{"subtopic_id": "BP-SCOPE-001", "engineering_gate_id": gate_id}],
    }
    return admission, synthetic_domain_registry(), request, manifest, binding, registry, receipt


class EngineeredDomainAdmissionTests(unittest.TestCase):
    def test_generic_domain_admission_requires_current_engineering_closure(self):
        admission, domain, request, manifest, binding, registry, _ = runtime_bundle()
        result = validate(admission, domain_registry=domain, engineering_request=request, engineering_manifest=manifest, engineering_binding=binding, technical_registry=registry)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["technical_authorization"], "ALLOWED")
        self.assertEqual(result["publication_authorization"], "NOT_IMPLIED")

    def test_unmapped_domain_subtopic_fails(self):
        admission, domain, request, manifest, binding, registry, _ = runtime_bundle()
        admission["subtopic_gate_map"] = []
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_request=request, engineering_manifest=manifest, engineering_binding=binding, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_ADMISSION_SCHEMA")

    def test_gate_outside_current_closure_fails(self):
        admission, domain, request, manifest, binding, registry, receipt = runtime_bundle()
        outside = next((g["subtopic_id"] for g in registry["subtopic_gates"] if g["subtopic_id"] not in set(receipt["transitive_gate_ids"])), None)
        if outside is None:
            self.skipTest("all gates are inside selected closure")
        admission["subtopic_gate_map"][0]["engineering_gate_id"] = outside
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_request=request, engineering_manifest=manifest, engineering_binding=binding, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_GATE_OUTSIDE_CLOSURE")

    def test_wrong_downstream_consumer_fails(self):
        admission, domain, request, manifest, _, registry, receipt = runtime_bundle()
        binding = compile_binding(request, manifest, receipt, "SDU")
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_request=request, engineering_manifest=manifest, engineering_binding=binding, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_WRONG_CONSUMER")

    def test_structurally_invalid_domain_registry_fails_first(self):
        admission, domain, request, manifest, binding, registry, _ = runtime_bundle()
        domain["assets"][0]["core1_refs"] = []
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_request=request, engineering_manifest=manifest, engineering_binding=binding, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_REGISTRY_INVALID")


if __name__ == "__main__":
    unittest.main()
