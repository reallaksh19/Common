import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_engineering_closure import compile_closure, digest  # noqa: E402
from compile_chemistry_product_engineering_custody import compile_product_custody  # noqa: E402
from validate_pal_engineering_ready import validate_pal_engineering_ready  # noqa: E402
from validate_product_source_scope import validate_product_source_scope  # noqa: E402


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


REQUEST_REL = "product_authority/redox/core1a/engineering-request.v2.json"
MANIFEST_REL = "product_authority/redox/core1a/engineering-manifest.v2.json"
EXTENSION_REL = "product_authority/redox/core1a/grade-extension-authorization.v1.json"
SCOPE_REL = "product_authority/redox/core1a/product-source-scope.v2.json"
AUDIT_REL = "source_audits/redox/production-source-audit.v2.json"
AUTHORITY_REL = "golden/v7/core1a-study-note-redox-authority.json"
CCBOM_REL = "golden/v7/ccbom-redox.json"
REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"


class RedoxCore1AProductAuthorityV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request = load(REQUEST_REL)
        cls.manifest = load(MANIFEST_REL)
        cls.extension = load(EXTENSION_REL)
        cls.scope = load(SCOPE_REL)
        cls.audit = load(AUDIT_REL)
        cls.authority = load(AUTHORITY_REL)
        cls.ccbom = load(CCBOM_REL)
        cls.registry = load(REGISTRY_REL)
        cls.audit_payloads = {AUDIT_REL: cls.audit}

    def test_explicit_grade_extension_matches_scope_contract(self):
        self.assertEqual(self.extension["status"], "AUTHORIZED")
        self.assertEqual(self.extension["subtopic_id"], self.scope["subtopic_id"])
        self.assertEqual(self.extension["learner_grade"], self.scope["learner_grade"])
        self.assertEqual(self.extension["program_context"], self.scope["program_context"])
        self.assertEqual(set(self.extension["authorized_scope_tiers"]), set(self.scope["authorized_scope_tiers"]))
        self.assertEqual(set(self.extension["held_scope_tiers"]), set(self.scope["held_scope_tiers"]))
        self.assertIn(self.extension["authorization_id"], self.scope["extension_authority_ref"])
        self.assertEqual(self.extension["source_audit_ref"], self.scope["source_audit_ref"])

    def test_scope_binds_exact_production_audit_digest(self):
        self.assertEqual(self.scope["source_audit_digest"], digest(self.audit))
        result = validate_product_source_scope(self.scope, self.audit, self.authority, self.registry)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["source_audit_role"], "PRODUCTION_SOURCE_AUDIT")
        self.assertEqual(result["authorized_scope_tiers"], ["FORMAL_G11", "FOUNDATION_G10"])
        self.assertEqual(result["held_scope_tiers"], ["EXTENDED_G11"])

    def test_workbench_closure_derives_full_prerequisite_chain(self):
        receipt = compile_closure(
            self.request,
            self.manifest,
            registry=self.registry,
            source_audit_payloads=self.audit_payloads,
        )
        self.assertEqual(receipt["closure_status"], "READY")
        self.assertEqual(receipt["counts"]["production_source_audit_count"], 1)
        self.assertEqual(receipt["counts"]["stress_source_audit_count"], 0)
        self.assertIn("CHEM-REDOX-OXIDATION", receipt["closure_gate_ids"])
        self.assertIn("CHEM-ION-VALENCY", receipt["closure_gate_ids"])
        self.assertIn("CHEM-EQ-BALANCING", receipt["closure_gate_ids"])
        external = {row["dependency_id"]: row for row in receipt["external_dependency_states"]}
        self.assertEqual(external["MATH-BASIC-ARITHMETIC"]["status"], "RESOLVED_BY_OWNER_SCOPE")

    def test_exact_product_custody_and_pal_pass(self):
        custody = compile_product_custody(
            self.request,
            self.manifest,
            self.ccbom,
            self.scope,
            self.authority,
            registry=self.registry,
            source_audit_payloads=self.audit_payloads,
        )
        self.assertEqual(custody["status"], "ENGINEERING_CUSTODY_READY")
        self.assertEqual(custody["ccbom_digest"], digest(self.ccbom))
        self.assertEqual(custody["product_scope_contract_digest"], digest(self.scope))
        self.assertEqual(custody["product_authority_digest"], digest(self.authority))
        pal = validate_pal_engineering_ready(
            self.request,
            self.manifest,
            self.ccbom,
            self.scope,
            self.authority,
            custody,
            registry=self.registry,
            source_audit_payloads=self.audit_payloads,
        )
        self.assertEqual(pal["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
