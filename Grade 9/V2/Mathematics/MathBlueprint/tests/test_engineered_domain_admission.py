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


def _asset(asset_id: str, subtopic_id: str, ref: str) -> dict:
    return {
        "asset_id": asset_id,
        "asset_type": "CONCEPT",
        "subtopic_id": subtopic_id,
        "title": "Synthetic canonical concept " + subtopic_id,
        "authority_class": "CORE1_SEMANTIC",
        "admission_status": "ADMITTED",
        "confidence": "HIGH",
        "ground_truth_refs": ["GT:" + ref],
        "core1_refs": ["K:" + ref],
        "core2_refs": [],
        "validation_refs": ["V:" + ref],
        "join_ref": "J:SYNTHETIC",
        "depends_on": [],
        "payload": {
            "statement": "Synthetic semantic object used only to test generic Engineering admission.",
            "prerequisite_refs": [],
            "implications": ["Admission logic must not depend on a remembered mathematics topic."],
        },
        "provenance_note": "Synthetic case-neutral registry for Engineering admission tests.",
    }


def synthetic_domain_registry() -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "registry_id": "MATH-REG-SYNTHETIC-001",
        "run_ref": "RUN:SYNTHETIC",
        "source_manifest_refs": ["GT:SYNTHETIC"],
        "join_refs": ["J:SYNTHETIC"],
        "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
        "assets": [
            _asset("REG-MATH-CON-SYNTHETIC-A", "BP-SCOPE-001", "A"),
            _asset("REG-MATH-CON-SYNTHETIC-B", "BP-SCOPE-002", "B"),
        ],
    }


def _authorization(gate_id: str, suffix: str, consumer: str = "CANONICAL_DOMAIN_REGISTRY") -> tuple[dict, dict, dict, dict]:
    registry = copy.deepcopy(TECH_REGISTRY)
    request = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": "MATH-ENG-REQ-DOMAIN-" + suffix,
        "scope_kind": "ENGINEERING_GATE",
        "scope_refs": [gate_id],
        "engineering_depth": "STANDARD",
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }
    manifest = resolve_manifest(request, registry)
    receipt = compile_closure(request, manifest, registry)
    binding = compile_binding(request, manifest, receipt, consumer)
    return request, manifest, binding, receipt


def runtime_bundle():
    registry = copy.deepcopy(TECH_REGISTRY)
    gate_ids = [row["subtopic_id"] for row in registry["subtopic_gates"][:2]]
    injected = {}
    auth_rows = []
    map_rows = []
    for i, gate_id in enumerate(gate_ids, 1):
        auth_id = f"MATH-ENG-AUTH-SYNTHETIC-{i}"
        request, manifest, binding, receipt = _authorization(gate_id, f"SYNTHETIC-{i}")
        injected[auth_id] = {"request": request, "manifest": manifest, "binding": binding}
        auth_rows.append({
            "authorization_id": auth_id,
            "engineering_request_ref": f"runtime://request/{i}",
            "engineering_manifest_ref": f"runtime://manifest/{i}",
            "engineering_binding_ref": f"runtime://binding/{i}",
        })
        map_rows.append({
            "subtopic_id": f"BP-SCOPE-00{i}",
            "gate_bindings": [{"engineering_gate_id": gate_id, "authorization_ref": auth_id}],
        })
    admission = {
        "schema_version": "2.0.0",
        "subject": "MATHEMATICS",
        "admission_id": "MATH-ENG-DOMAIN-ADMISSION-SYNTHETIC",
        "domain_registry_ref": "runtime://domain-registry",
        "authorizations": auth_rows,
        "subtopic_gate_map": map_rows,
    }
    return admission, synthetic_domain_registry(), injected, registry


class EngineeredDomainAdmissionTests(unittest.TestCase):
    def test_multiple_bounded_authorizations_cover_domain(self):
        admission, domain, injected, registry = runtime_bundle()
        result = validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["technical_authorization"], "ALLOWED")
        self.assertEqual(result["publication_authorization"], "NOT_IMPLIED")
        self.assertEqual(result["mapped_subtopic_count"], 2)
        self.assertEqual(len(result["authorization_custody"]), 2)
        self.assertEqual(len(result["authorized_direct_gate_ids"]), 2)

    def test_unmapped_domain_subtopic_fails(self):
        admission, domain, injected, registry = runtime_bundle()
        admission["subtopic_gate_map"] = admission["subtopic_gate_map"][:1]
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_SUBTOPIC_COVERAGE_MISMATCH")

    def test_unknown_authorization_ref_fails(self):
        admission, domain, injected, registry = runtime_bundle()
        admission["subtopic_gate_map"][0]["gate_bindings"][0]["authorization_ref"] = "MATH-ENG-AUTH-NOT-PRESENT"
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_AUTHORIZATION_REF_UNKNOWN")

    def test_prerequisite_only_gate_cannot_be_semantic_admission_target(self):
        admission, domain, injected, registry = runtime_bundle()
        second_auth = admission["authorizations"][1]["authorization_id"]
        second_bundle = injected[second_auth]
        second_receipt = compile_closure(second_bundle["request"], second_bundle["manifest"], registry)
        prereq = next(g for g in second_receipt["transitive_gate_ids"] if g not in set(second_receipt["direct_gate_ids"]))
        admission["subtopic_gate_map"][1]["gate_bindings"][0]["engineering_gate_id"] = prereq
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_GATE_NOT_DIRECTLY_AUTHORIZED")

    def test_unused_direct_gate_authority_fails(self):
        admission, domain, injected, registry = runtime_bundle()
        first_auth = admission["authorizations"][0]["authorization_id"]
        second_gate = admission["subtopic_gate_map"][1]["gate_bindings"][0]["engineering_gate_id"]
        request, manifest, binding, _ = _authorization(second_gate, "REPLACEMENT")
        injected[first_auth] = {"request": request, "manifest": manifest, "binding": binding}
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertIn(ctx.exception.code, {"MATH_ENG_DOMAIN_DIRECT_GATE_AUTHORIZATION_OVERLAP", "MATH_ENG_DOMAIN_GATE_NOT_DIRECTLY_AUTHORIZED"})

    def test_duplicate_authorization_id_fails(self):
        admission, domain, injected, registry = runtime_bundle()
        admission["authorizations"][1]["authorization_id"] = admission["authorizations"][0]["authorization_id"]
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_DUPLICATE_AUTHORIZATION_ID")

    def test_wrong_downstream_consumer_in_any_bundle_fails(self):
        admission, domain, injected, registry = runtime_bundle()
        auth_id = admission["authorizations"][1]["authorization_id"]
        gate_id = admission["subtopic_gate_map"][1]["gate_bindings"][0]["engineering_gate_id"]
        request, manifest, binding, _ = _authorization(gate_id, "WRONG-CONSUMER", "SDU")
        injected[auth_id] = {"request": request, "manifest": manifest, "binding": binding}
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_WRONG_CONSUMER")

    def test_stale_one_of_multiple_bindings_fails(self):
        admission, domain, injected, registry = runtime_bundle()
        auth_id = admission["authorizations"][1]["authorization_id"]
        injected[auth_id]["binding"] = copy.deepcopy(injected[auth_id]["binding"])
        injected[auth_id]["binding"]["registry_digest"] = "sha256:" + "0" * 64
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_BINDING_INVALID")

    def test_structurally_invalid_domain_registry_fails_first(self):
        admission, domain, injected, registry = runtime_bundle()
        domain["assets"][0]["core1_refs"] = []
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=domain, engineering_authorizations=injected, technical_registry=registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_REGISTRY_INVALID")


if __name__ == "__main__":
    unittest.main()
