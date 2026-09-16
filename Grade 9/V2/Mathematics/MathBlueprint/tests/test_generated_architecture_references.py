from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
GENERATOR_PATH = DESIGN / "generate_mathematics_architecture_references.py"
CATALOG_PATH = DESIGN / "mathematics-architecture-catalog.candidate.json"
MANIFEST_PATH = DESIGN / "generated" / "mathematics-architecture-reference-index.generated.json"
MARKDOWN_PATH = DESIGN / "generated" / "MATHEMATICS_ARCHITECTURE_REFERENCES.generated.md"
MANIFEST_SCHEMA_PATH = DESIGN / "mathematics-architecture-generated-references.schema.json"
RECEIPT_PATH = DESIGN / "mathematics-generated-references.receipt.json"
RECEIPT_SCHEMA_PATH = DESIGN / "mathematics-generated-references.receipt.schema.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_generator():
    spec = importlib.util.spec_from_file_location("math_arch_reference_generator", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GeneratedArchitectureReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()
        cls.catalog = load_json(CATALOG_PATH)
        cls.manifest = load_json(MANIFEST_PATH)
        cls.receipt = load_json(RECEIPT_PATH)
        cls.markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
        cls.manifest_schema = load_json(MANIFEST_SCHEMA_PATH)
        cls.receipt_schema = load_json(RECEIPT_SCHEMA_PATH)

    def test_generated_manifest_and_receipt_are_schema_valid_and_non_authoritative(self):
        manifest_errors = list(Draft202012Validator(self.manifest_schema).iter_errors(self.manifest))
        receipt_errors = list(Draft202012Validator(self.receipt_schema).iter_errors(self.receipt))
        self.assertEqual(manifest_errors, [], "; ".join(error.message for error in manifest_errors))
        self.assertEqual(receipt_errors, [], "; ".join(error.message for error in receipt_errors))
        self.assertEqual(self.manifest["authority"], "NONE")
        self.assertEqual(self.manifest["semantic_change"], "NONE")
        self.assertEqual(self.manifest["publication_authorization"], "NOT_IMPLIED")
        self.assertEqual(self.receipt["authority"], "NONE")
        self.assertFalse(self.receipt["production_consumers_allowed"])

    def test_committed_generated_outputs_are_exactly_current(self):
        expected_manifest, expected_markdown, expected_receipt = self.generator.expected_outputs()
        self.assertEqual(self.manifest, expected_manifest)
        self.assertEqual(self.markdown, expected_markdown)
        self.assertEqual(self.receipt, expected_receipt)

    def test_reference_rows_are_exact_catalog_projection(self):
        expected_components, expected_references = self.generator.project_catalog(self.catalog)
        self.assertEqual(self.manifest["components"], expected_components)
        self.assertEqual(self.manifest["references"], expected_references)
        self.assertEqual(self.manifest["component_count"], len(expected_components))
        self.assertEqual(
            self.manifest["reference_counts"],
            {kind: len(expected_references[kind]) for kind in self.generator.REFERENCE_KINDS},
        )

    def test_all_generated_reference_paths_exist_and_match_declared_kind(self):
        for kind, rows in self.manifest["references"].items():
            for row in rows:
                with self.subTest(kind=kind, path=row["path"]):
                    self.assertTrue((ROOT / row["path"]).exists())
                    self.assertEqual(self.generator.classify_evidence_path(row["path"]), kind)

    def test_future_catalog_component_projects_without_topic_branch(self):
        mutated = copy.deepcopy(self.catalog)
        synthetic = copy.deepcopy(mutated["components"][0])
        synthetic["component_id"] = "MATH-ARCH-SYNTHETIC-FUTURE"
        synthetic["name"] = "Synthetic future architecture component"
        synthetic["evidence_paths"] = [
            "contracts/math-routing-plan.schema.json",
            "policies/math-self-teaching-policy.json",
            "engine/validate_publication_bundle.py",
            "tests/test_design_authority_boundary.py",
        ]
        synthetic["responsibility"] = "Proves C3 reference generation extends through catalog data without topic-specific generator code."
        mutated["components"].append(synthetic)

        components, references = self.generator.project_catalog(mutated, require_paths=False)
        self.assertTrue(any(row["component_id"] == synthetic["component_id"] for row in components))
        for kind in self.generator.REFERENCE_KINDS:
            self.assertTrue(
                any(row["component_id"] == synthetic["component_id"] for row in references[kind]),
                kind,
            )

    def test_non_validator_compiler_is_not_silently_classified_as_validator(self):
        self.assertIsNone(
            self.generator.classify_evidence_path("engine/compile_mathematics_engineering_workbench.py")
        )
        self.assertEqual(
            self.generator.classify_evidence_path("engine/validate_mathematics_engineering_gates.py"),
            "VALIDATOR",
        )

    def test_source_custody_matches_exact_current_design_inputs(self):
        custody = self.manifest["source_custody"]
        for path_key, sha_key in [
            ("catalog_path", "catalog_git_blob_sha"),
            ("catalog_schema_path", "catalog_schema_git_blob_sha"),
            ("c2_receipt_path", "c2_receipt_git_blob_sha"),
            ("generator_path", "generator_git_blob_sha"),
        ]:
            path = ROOT / custody[path_key]
            self.assertTrue(path.exists())
            self.assertEqual(custody[sha_key], self.generator.git_blob_sha(path))

    def test_schemas_reject_authority_or_publication_promotion(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["authority"] = "AUTHORITATIVE"
        manifest["publication_authorization"] = "ALLOWED"
        manifest_errors = list(Draft202012Validator(self.manifest_schema).iter_errors(manifest))
        self.assertGreaterEqual(len(manifest_errors), 2)

        receipt = copy.deepcopy(self.receipt)
        receipt["authority"] = "AUTHORITATIVE"
        receipt["production_consumers_allowed"] = True
        receipt["tracked_runtime_gap"]["runtime_auto_materialization_executable"] = True
        receipt_errors = list(Draft202012Validator(self.receipt_schema).iter_errors(receipt))
        self.assertGreaterEqual(len(receipt_errors), 3)

    def test_c3_preserves_f007_and_advances_only_to_c4_design_gate(self):
        self.assertEqual(self.receipt["status"], "C3_GENERATED_REFERENCES_COMPLETE")
        self.assertEqual(self.receipt["catalog_semantics"], "CLASSIFICATION_ONLY_UNCHANGED")
        self.assertEqual(self.receipt["tracked_runtime_gap"]["finding_id"], "C0-F007")
        self.assertEqual(
            self.receipt["tracked_runtime_gap"]["classification"],
            "CURRENT + DOCUMENTED ONLY",
        )
        self.assertFalse(
            self.receipt["tracked_runtime_gap"]["runtime_auto_materialization_executable"]
        )
        self.assertEqual(self.receipt["next_stage"], "C4_SUBJECT_ADAPTER_INTERFACE_READY")
        self.assertIn("DESIGN / NON-NORMATIVE / GENERATED", self.markdown)
        self.assertIn("C0-F007 remains `CURRENT + DOCUMENTED ONLY`", self.markdown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
