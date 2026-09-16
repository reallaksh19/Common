import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STRESS = ROOT / "stress_tests" / "redox" / "four_core"
sys.path.insert(0, str(STRESS))

from build_redox_four_core_stress import build_stress  # noqa: E402


class RedoxFourCoreStressTests(unittest.TestCase):
    def build(self):
        with tempfile.TemporaryDirectory() as td:
            return build_stress(Path(td), render=False)

    def test_current_blueprint_compiles_all_four_core_custodies_without_render_dependencies(self):
        result = self.build()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(set(result["products"]), {"CORE1A", "CORE1B", "CORE2A", "CORE2B"})
        self.assertFalse(result["held_transform_realized_by_any_core"])
        self.assertEqual(result["products"]["CORE1A"]["render_status"], "NOT_RENDERED")
        self.assertEqual(len(result["products"]["CORE1A"]["scope_units"]), 4)
        self.assertEqual(len(result["products"]["CORE1B"]["scope_units"]), 1)
        self.assertEqual(len(result["products"]["CORE2A"]["scope_units"]), 1)
        self.assertEqual(len(result["products"]["CORE2B"]["scope_units"]), 1)

    def test_held_core1b_balancing_transformation_remains_absent(self):
        result = self.build()
        held = set(result["held_transformation_fingerprints"])
        self.assertTrue(held)
        self.assertFalse(held & set(result["products"]["CORE1B"]["realized_transformations"]))
        self.assertTrue(any(
            "AGENT_ASSIGNMENT" in ref
            for ref in result["products"]["CORE1A"]["realized_transformations"]
        ))

    def test_problem_family_semantic_polarity_survives_fixture_projection(self):
        result = self.build()
        projection = result["problem_family_projection"]
        self.assertEqual(projection["semantic_role_trace"]["first_technical_move"], "METHOD_STEP")
        self.assertEqual(projection["semantic_role_trace"]["common_fatal_error"], "ERROR_TO_AVOID")
        self.assertTrue(projection["method_steps"])
        self.assertTrue(projection["common_fatal_errors"])
        self.assertFalse(set(projection["method_steps"]) & set(projection["common_fatal_errors"]))

    def test_engineering_representation_is_bound_and_used_in_every_declared_core_payload(self):
        result = self.build()
        for mode, product in result["products"].items():
            closure = product["representation_closure"]
            self.assertEqual(closure["status"], "PASS", mode)
            self.assertTrue(closure["defined_representation_refs"], mode)
            self.assertTrue(closure["used_representation_refs"], mode)
            self.assertTrue(closure["realized_engineering_representation_refs"], mode)
            self.assertGreaterEqual(closure["binding_count"], 1, mode)
        core1a = result["products"]["CORE1A"]["representation_closure"]
        self.assertEqual(
            core1a["required_engineering_representation_refs"],
            core1a["realized_engineering_representation_refs"],
        )

    def test_stress_manifest_binds_current_repository_authority_digests(self):
        result = self.build()
        inputs = result["input_digests"]
        self.assertIn("golden/v7/core1a-study-note-redox-authority.json", inputs)
        self.assertIn("source_audits/redox/production-source-audit.v2.json", inputs)
        self.assertIn("policies/chemistry-technical-engineering-gates.v1.json", inputs)
        self.assertIn("../Representation/registry/chemistry-electron-transfer-primitive-extension.v1.json", inputs)
        self.assertTrue(all(value.startswith("sha256:") and len(value) == 71 for value in inputs.values()))


if __name__ == "__main__":
    unittest.main()
