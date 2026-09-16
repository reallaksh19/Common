from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
VALIDATOR_PATH = DESIGN / "validate_subject_adapter_interface_candidate.py"
INTERFACE_PATH = DESIGN / "stem-subject-adapter-interface.candidate.json"
INTERFACE_SCHEMA_PATH = DESIGN / "stem-subject-adapter-interface.candidate.schema.json"
RECEIPT_PATH = DESIGN / "mathematics-subject-adapter-equivalence.receipt.json"
RECEIPT_SCHEMA_PATH = DESIGN / "mathematics-subject-adapter-equivalence.receipt.schema.json"
C3_RECEIPT_PATH = DESIGN / "mathematics-generated-references.receipt.json"
CATALOG_PATH = DESIGN / "mathematics-architecture-catalog.candidate.json"
MATH_DOMAIN_SCHEMA_PATH = ROOT / "contracts" / "math-canonical-domain-registry.schema.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_validator():
    spec = importlib.util.spec_from_file_location("subject_adapter_candidate_validator", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SubjectAdapterInterfaceCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator_module = load_validator()
        cls.candidate = load_json(INTERFACE_PATH)
        cls.schema = load_json(INTERFACE_SCHEMA_PATH)
        cls.receipt = load_json(RECEIPT_PATH)
        cls.receipt_schema = load_json(RECEIPT_SCHEMA_PATH)
        cls.c3 = load_json(C3_RECEIPT_PATH)
        cls.catalog = load_json(CATALOG_PATH)
        cls.math_domain_schema = load_json(MATH_DOMAIN_SCHEMA_PATH)

    def violations(self, candidate: dict, *, c3: dict | None = None) -> list[str]:
        return self.validator_module.candidate_violations(
            candidate,
            schema=self.schema,
            c3_receipt=self.c3 if c3 is None else c3,
            catalog=self.catalog,
            math_domain_schema=self.math_domain_schema,
            require_paths=False,
        )

    def test_candidate_and_receipt_are_schema_valid_and_non_authoritative(self):
        candidate_errors = list(Draft202012Validator(self.schema).iter_errors(self.candidate))
        receipt_errors = list(Draft202012Validator(self.receipt_schema).iter_errors(self.receipt))
        self.assertEqual(candidate_errors, [], "; ".join(error.message for error in candidate_errors))
        self.assertEqual(receipt_errors, [], "; ".join(error.message for error in receipt_errors))
        self.assertEqual(self.candidate["authority"], "NONE")
        self.assertFalse(self.candidate["runtime_migration_authorized"])
        self.assertFalse(self.candidate["production_consumers_allowed"])
        self.assertEqual(self.receipt["authority"], "NONE")
        self.assertEqual(self.receipt["equivalence_status"], "PASS_DESIGN_PROJECTION_ONLY")
        self.assertFalse(self.receipt["runtime_migration_authorized"])

    def test_current_candidate_has_zero_equivalence_violations(self):
        self.assertEqual(self.validator_module.current_violations(), [])

    def test_mathematics_binds_every_core_operation_and_not_conditional_safety(self):
        operations = self.candidate["interface_operations"]
        core_ids = {
            row["operation_id"] for row in operations if row["requirement"] == "CORE"
        }
        conditional_ids = {
            row["operation_id"]
            for row in operations
            if row["requirement"] == "CONDITIONAL_SUBJECT_CAPABILITY"
        }
        binding_ids = {
            row["operation_id"] for row in self.candidate["mathematics_projection"]["operation_bindings"]
        }
        self.assertEqual(binding_ids, core_ids)
        self.assertEqual(conditional_ids, {"VALIDATE_SUBJECT_SAFETY"})
        self.assertFalse(binding_ids & conditional_ids)

    def test_mathematics_object_types_exactly_match_current_domain_registry(self):
        expected = set(self.math_domain_schema["$defs"]["assetType"]["enum"])
        actual = set(self.candidate["mathematics_projection"]["canonical_object_types"])
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 13)

    def test_every_math_binding_is_owned_by_referenced_c1_component(self):
        rows = {row["component_id"]: row for row in self.catalog["components"]}
        for binding in self.candidate["mathematics_projection"]["operation_bindings"]:
            with self.subTest(operation_id=binding["operation_id"]):
                declared: set[str] = set()
                for component_id in binding["component_ids"]:
                    self.assertIn(component_id, rows)
                    declared.update(rows[component_id]["evidence_paths"])
                for rel in binding["evidence_paths"]:
                    self.assertIn(rel, declared)
                    self.assertTrue((ROOT / rel).exists())

    def test_generic_operations_are_subject_neutral(self):
        raw = json.dumps(self.candidate["interface_operations"], sort_keys=True).lower()
        for forbidden in ("mathematics", "chemistry", "math-", "topic ==", "subtopic =="):
            self.assertNotIn(forbidden, raw)

    def test_chemistry_remains_unbound_design_stress_target_with_safety_reserved(self):
        chemistry = self.candidate["chemistry_stress_target"]
        self.assertEqual(chemistry["status"], "DESIGN_STRESS_TARGET_ONLY")
        self.assertEqual(chemistry["authority"], "NONE")
        self.assertFalse(chemistry["runtime_binding_present"])
        self.assertIsNone(chemistry["production_registry_ref"])
        self.assertIsNone(chemistry["production_validator_ref"])
        self.assertIn("LAB_SAFETY_AUTHORITY", chemistry["required_subject_specific_controls"])

    def test_unknown_component_and_undeclared_evidence_fail_closed(self):
        mutated = copy.deepcopy(self.candidate)
        binding = mutated["mathematics_projection"]["operation_bindings"][0]
        binding["component_ids"] = ["MATH-ARCH-NOT-REAL"]
        binding["evidence_paths"] = ["engine/not-declared-by-component.py"]
        violations = self.violations(mutated)
        self.assertTrue(any("unknown C1 component_id" in message for message in violations), violations)
        self.assertTrue(any("evidence path is not declared" in message for message in violations), violations)

    def test_math_object_vocabulary_drift_fails_closed(self):
        mutated = copy.deepcopy(self.candidate)
        mutated["mathematics_projection"]["canonical_object_types"].append("SYNTHETIC_OBJECT")
        violations = self.violations(mutated)
        self.assertTrue(any("must exactly match current domain registry" in message for message in violations), violations)

    def test_conditional_safety_cannot_be_silently_bound_into_mathematics(self):
        mutated = copy.deepcopy(self.candidate)
        synthetic = copy.deepcopy(mutated["mathematics_projection"]["operation_bindings"][0])
        synthetic["operation_id"] = "VALIDATE_SUBJECT_SAFETY"
        mutated["mathematics_projection"]["operation_bindings"].append(synthetic)
        violations = self.violations(mutated)
        self.assertTrue(any("bindings must equal CORE operations" in message for message in violations), violations)
        self.assertTrue(any("conditional subject capability" in message for message in violations), violations)

    def test_c3_gate_and_f007_are_preserved(self):
        self.assertEqual(self.c3["status"], "C3_GENERATED_REFERENCES_COMPLETE")
        self.assertEqual(self.c3["next_stage"], "C4_SUBJECT_ADAPTER_INTERFACE_READY")
        tracked = self.receipt["tracked_runtime_gap"]
        self.assertEqual(tracked["finding_id"], "C0-F007")
        self.assertEqual(tracked["classification"], "CURRENT + DOCUMENTED ONLY")
        self.assertFalse(tracked["runtime_auto_materialization_executable"])
        self.assertEqual(self.receipt["next_stage"], "C5_SUBTOPIC_INTELLIGENCE_LIBRARY_CONTRACTS_READY")

    def test_receipt_is_exactly_reproducible_from_current_inputs(self):
        self.assertEqual(self.receipt, self.validator_module.expected_receipt())
        custody = self.receipt["source_custody"]
        for path_key, sha_key in [
            ("interface_path", "interface_git_blob_sha"),
            ("interface_schema_path", "interface_schema_git_blob_sha"),
            ("c3_receipt_path", "c3_receipt_git_blob_sha"),
            ("catalog_path", "catalog_git_blob_sha"),
            ("mathematics_domain_schema_path", "mathematics_domain_schema_git_blob_sha"),
            ("validator_path", "validator_git_blob_sha"),
        ]:
            path = ROOT / custody[path_key]
            self.assertTrue(path.exists())
            self.assertEqual(custody[sha_key], self.validator_module.git_blob_sha(path))

    def test_schemas_reject_authority_runtime_or_chemistry_promotion(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["authority"] = "AUTHORITATIVE"
        candidate["runtime_migration_authorized"] = True
        candidate["chemistry_stress_target"]["runtime_binding_present"] = True
        candidate["chemistry_stress_target"]["production_registry_ref"] = "CHEM-REG-FAKE"
        errors = list(Draft202012Validator(self.schema).iter_errors(candidate))
        self.assertGreaterEqual(len(errors), 4)

        receipt = copy.deepcopy(self.receipt)
        receipt["authority"] = "AUTHORITATIVE"
        receipt["runtime_migration_authorized"] = True
        receipt["mathematics_validation_weakened"] = True
        receipt["tracked_runtime_gap"]["runtime_auto_materialization_executable"] = True
        receipt_errors = list(Draft202012Validator(self.receipt_schema).iter_errors(receipt))
        self.assertGreaterEqual(len(receipt_errors), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
