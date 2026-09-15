import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from validate_chemistry_gate_source_audit import validate as validate_source_audit  # noqa: E402
from validate_product_source_scope import digest, validate_product_source_scope  # noqa: E402

REGISTRY = json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))
PRODUCTION_AUDIT = json.loads((ROOT / "source_audits/redox/production-source-audit.v2.json").read_text(encoding="utf-8"))
STRESS_AUDIT = json.loads((ROOT / "stress_tests/redox/source-audit.v2.json").read_text(encoding="utf-8"))
AUTHORITY = json.loads((ROOT / "golden/v7/core1a-study-note-redox-authority.json").read_text(encoding="utf-8"))


def make_scope():
    return {
        "schema_version": "2.0.0",
        "scope_contract_id": "CHEM-PRODUCT-SCOPE-REDOX-CORE1A-PRODUCTION-V2",
        "gate_id": PRODUCTION_AUDIT["gate_id"],
        "subtopic_id": AUTHORITY["subtopic_id"],
        "source_audit_ref": "source_audits/redox/production-source-audit.v2.json",
        "source_audit_digest": digest(PRODUCTION_AUDIT),
        "learner_grade": 9,
        "program_context": "COMPETITIVE_FOUNDATION_EXTENSION",
        "authorized_scope_tiers": ["FOUNDATION_G10", "FORMAL_G11"],
        "held_scope_tiers": ["EXTENDED_G11"],
        "extension_authority_ref": AUTHORITY["authority_id"],
        "extension_reason": "Grade 9 competitive-foundation product explicitly uses the governed Class X foundation plus formal Class XI oxidation-state/electron/agent reasoning while holding formal balancing depth.",
        "learning_atom_scope_assignments": [
            {"learning_atom_id": "LA-REDOX-TRACK-001", "scope_tier": "FOUNDATION_G10"},
            {"learning_atom_id": "LA-REDOX-STATE-CHANGE-002", "scope_tier": "FORMAL_G11"},
            {"learning_atom_id": "LA-REDOX-ELECTRON-002", "scope_tier": "FORMAL_G11"},
            {"learning_atom_id": "LA-REDOX-AGENT-003", "scope_tier": "FORMAL_G11"}
        ],
        "held_transformation_guards": [
            {
                "fingerprint": "HALF_REACTIONS->BALANCED_OVERALL_REDOX|CORE1B_GENERATIVE_RECONSTRUCTION",
                "detection_tokens": ["MnO4", "permanganate", "acidic medium"]
            }
        ],
        "status": "SCOPE_CONTRACT_READY"
    }


class RedoxProductionSourceAuditV2Tests(unittest.TestCase):
    def test_production_audit_is_distinct_from_stress_fixture(self):
        self.assertNotEqual(PRODUCTION_AUDIT["audit_id"], STRESS_AUDIT["audit_id"])
        self.assertEqual(PRODUCTION_AUDIT["audit_role"], "PRODUCTION_SOURCE_AUDIT")
        self.assertEqual(STRESS_AUDIT["audit_role"], "STRESS_TEST_SOURCE_AUDIT")
        self.assertNotEqual(digest(PRODUCTION_AUDIT), digest(STRESS_AUDIT))

    def test_production_audit_validates_with_source_scope_effect(self):
        result = validate_source_audit(PRODUCTION_AUDIT, REGISTRY)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["audit_status"], "SOURCE_HARDENED")
        self.assertEqual(result["audit_role"], "PRODUCTION_SOURCE_AUDIT")
        self.assertEqual(result["authority_effect"], "SOURCE_SCOPE_EVIDENCE_ONLY")
        self.assertEqual(result["gate_id"], "CHEM-REDOX-OXIDATION")
        self.assertEqual(result["source_layer_count"], 4)
        self.assertEqual(result["scope_tier_count"], 3)
        self.assertEqual(result["asset_binding_count"], 6)

    def test_production_sources_are_explicit_and_not_stress_fixture_authority(self):
        refs = "\n".join(PRODUCTION_AUDIT["effective_provenance"]["source_references"])
        self.assertIn("ncert.nic.in/textbook.php?jesc1=1-11", refs)
        self.assertIn("ncert.nic.in/pdf/syllabus/desm_s_Chemistry.pdf", refs)
        self.assertIn("ncert.nic.in/textbook.php?kech1=2-8", refs)
        self.assertNotIn("stress_tests/", refs)
        for layer in PRODUCTION_AUDIT["source_layers"]:
            self.assertNotIn("stress_tests/", layer["source_ref"])

    def test_agent_role_is_derived_not_falsely_source_quoted(self):
        row = next(
            item for item in PRODUCTION_AUDIT["asset_bindings"]
            if item["asset_ref"] == "CON-CHEM-AGENT-INVERSION"
        )
        self.assertEqual(row["claim_class"], "STANDARD_CHEMISTRY_DERIVED")
        self.assertIn("SRC-STANDARD-REDOX-DERIVATION-PROD", row["authority_layer_ids"])

    def test_extended_balancing_is_source_authorized_but_product_held(self):
        row = next(
            item for item in PRODUCTION_AUDIT["asset_bindings"]
            if item["asset_ref"].startswith("HALF_REACTIONS->BALANCED_OVERALL_REDOX")
        )
        self.assertEqual(row["scope_tier_id"], "EXTENDED_G11")
        self.assertEqual(row["claim_class"], "SOURCE_SCOPE_HELD")

    def test_current_core1a_scope_passes_against_production_audit(self):
        result = validate_product_source_scope(make_scope(), PRODUCTION_AUDIT, AUTHORITY, REGISTRY)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["source_audit_role"], "PRODUCTION_SOURCE_AUDIT")
        self.assertEqual(result["authorized_scope_tiers"], ["FORMAL_G11", "FOUNDATION_G10"])
        self.assertEqual(result["held_scope_tiers"], ["EXTENDED_G11"])
        self.assertEqual(result["learning_atom_count"], 4)
        self.assertEqual(result["held_guard_count"], 1)


if __name__ == "__main__":
    unittest.main()
