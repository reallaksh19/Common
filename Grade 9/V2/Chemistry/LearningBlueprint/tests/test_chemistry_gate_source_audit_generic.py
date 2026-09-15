import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from validate_chemistry_gate_source_audit import (  # noqa: E402
    ChemistrySourceAuditError,
    validate,
)


AUDIT_PATH = ROOT / "stress_tests" / "redox" / "source-audit.v2.json"
REGISTRY_PATH = ROOT / "policies" / "chemistry-technical-engineering-gates.v1.json"
SCHEMA_PATH = ROOT / "contracts" / "chemistry-gate-source-audit.schema.json"
VALIDATOR_PATH = ROOT / "engine" / "validate_chemistry_gate_source_audit.py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class GenericChemistrySourceAuditTests(unittest.TestCase):
    def setUp(self):
        self.audit = load(AUDIT_PATH)
        self.registry = load(REGISTRY_PATH)

    def assert_code(self, expected, fn):
        with self.assertRaises(ChemistrySourceAuditError) as ctx:
            fn()
        self.assertEqual(ctx.exception.code, expected)

    def test_stress_fixture_passes_without_authority_effect(self):
        result = validate(self.audit, self.registry)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["audit_role"], "STRESS_TEST_SOURCE_AUDIT")
        self.assertEqual(result["authority_effect"], "NONE_STRESS_TEST_ONLY")
        self.assertEqual(
            result["coverage_requirements"],
            ["CONCEPT", "EQUATION", "TRANSFORMATION"],
        )

    def test_unknown_source_layer_fails(self):
        bad = copy.deepcopy(self.audit)
        bad["asset_bindings"][0]["authority_layer_ids"] = ["SRC-NOT-DECLARED"]
        self.assert_code(
            "CHEM_SOURCE_AUDIT_UNRESOLVED_SOURCE_REF",
            lambda: validate(bad, self.registry),
        )

    def test_unknown_scope_tier_fails(self):
        bad = copy.deepcopy(self.audit)
        bad["asset_bindings"][0]["scope_tier_id"] = "UNDECLARED_TIER"
        self.assert_code(
            "CHEM_SOURCE_AUDIT_UNRESOLVED_SCOPE_TIER",
            lambda: validate(bad, self.registry),
        )

    def test_missing_concept_binding_fails_complete_coverage(self):
        bad = copy.deepcopy(self.audit)
        bad["asset_bindings"] = [
            row
            for row in bad["asset_bindings"]
            if row["asset_ref"] != "CON-CHEM-OXIDATION-STATE-RULES"
        ]
        self.assert_code(
            "CHEM_SOURCE_AUDIT_ASSET_COVERAGE",
            lambda: validate(bad, self.registry),
        )

    def test_transformation_binding_is_derived_from_generic_gate_fields(self):
        bad = copy.deepcopy(self.audit)
        target = next(
            row for row in bad["asset_bindings"] if row["asset_kind"] == "TRANSFORMATION"
        )
        target["asset_ref"] = "TOPIC_SPECIFIC_SHORTCUT"
        self.assert_code(
            "CHEM_SOURCE_AUDIT_ASSET_COVERAGE",
            lambda: validate(bad, self.registry),
        )

    def test_unknown_gate_fails(self):
        bad = copy.deepcopy(self.audit)
        bad["gate_id"] = "CHEM-UNKNOWN-GATE"
        self.assert_code(
            "CHEM_SOURCE_AUDIT_GATE_MISSING",
            lambda: validate(bad, self.registry),
        )

    def test_generic_contract_and_validator_have_no_stress_topic_logic(self):
        generic_text = (
            SCHEMA_PATH.read_text(encoding="utf-8")
            + "\n"
            + VALIDATOR_PATH.read_text(encoding="utf-8")
        ).lower()
        for forbidden in ("redox", "mno4", "oil rig", "permanganate"):
            self.assertNotIn(forbidden, generic_text)

    def test_stress_fixture_cannot_be_relabelled_as_ground_truth(self):
        self.assertEqual(self.audit["audit_role"], "STRESS_TEST_SOURCE_AUDIT")
        result = validate(self.audit, self.registry)
        self.assertNotIn("CANONICAL", result["authority_effect"])
        self.assertNotIn("GROUND_TRUTH", result["authority_effect"])


if __name__ == "__main__":
    unittest.main()
