import inspect
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STRESS = ROOT / "stress_tests" / "redox" / "four_core"
sys.path.insert(0, str(STRESS))

import build_redox_four_core_governed as governed_fixture  # noqa: E402
import build_redox_four_core_stress as fixture_support  # noqa: E402
from build_redox_four_core_governed import build_stress  # noqa: E402

LOCAL_INSTANCE = "CHEM-SEM-INSTANCE-REDOX-ZN-CU-v1"
LOCAL_AUTHORITY = "CORE1A-STUDY-NOTE-REDOX-STATE-AGENT-v1"


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

    def test_every_mode_uses_the_blueprint_local_semantic_instance(self):
        result = self.build()
        self.assertEqual(result["representation_semantic_authority_ref"], LOCAL_AUTHORITY)
        for mode, product in result["products"].items():
            self.assertEqual(product["representation_semantic_instance_refs"], [LOCAL_INSTANCE], mode)
            self.assertEqual(product["representation_bundle_summary"]["semantic_instance_count"], 1, mode)

    def test_stress_manifest_binds_current_repository_authority_digests(self):
        result = self.build()
        inputs = result["input_digests"]
        self.assertIn("golden/v7/core1a-study-note-redox-authority.json", inputs)
        self.assertIn("source_audits/redox/production-source-audit.v2.json", inputs)
        self.assertIn("policies/chemistry-technical-engineering-gates.v1.json", inputs)
        self.assertIn("../Representation/registry/chemistry-electron-transfer-primitive-extension.v1.json", inputs)
        self.assertIn("../Representation/registry/chemistry-electron-transfer-intent-extension.v1.json", inputs)
        self.assertIn("../Representation/registry/chemistry-electron-transfer-runtime-facts.v1.json", inputs)
        self.assertEqual(result["representation_authority_mode"], "GOVERNED_INTENT_PLUS_LOCAL_SEMANTIC_INSTANCE_FACTS")
        self.assertFalse(result["fixture_authored_representation_semantics"])
        self.assertTrue(all(value.startswith("sha256:") and len(value) == 71 for value in inputs.values()))

    def test_active_redox_entrypoint_does_not_author_representation_science(self):
        source = inspect.getsource(governed_fixture).lower()
        forbidden = (
            "source_semantic_data",
            "primitive_id =",
            "oxidation_states =",
            "re.findall(",
            "meaning_of_symbols",
            "parse_equation(",
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)

    def test_fixture_support_has_no_retired_representation_authority_path(self):
        source = inspect.getsource(fixture_support).lower()
        forbidden = (
            "def build_stress(",
            "def make_representation_plan(",
            "def engineering_electron_state_records(",
            "compile_core_representation_bundle",
            "source_semantic_data",
            "meaning_of_symbols",
            "parse_equation",
            "oxidation_states",
            "primitive_id =",
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)


if __name__ == "__main__":
    unittest.main()
