import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "policies" / "pr370-control-migration.v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PR370ControlMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.migration = load(MIGRATION)
        cls.rows = {row["control_id"]: row for row in cls.migration["controls"]}

    def test_generic_b_layer_controls_have_current_targets(self):
        required = {
            "STATIC_ONLY_B_LAYER_BOUNDARY",
            "NO_NEW_CHEMISTRY_IN_B_LAYER",
            "CORE1B_DEPTH_INDEPENDENT_OF_LEARNER_PERCENT",
            "CORE1B_UPSTREAM_CAPABILITY_FAMILY_AND_REPRESENTATION_CUSTODY",
            "CORE1B_MODULE_SPECIFIC_HINT_LADDERS",
            "CORE2B_SUPPORT_ONLY_CONDITIONING",
            "CORE2B_CORE2A_LEGAL_ITEM_AND_SOURCE_IDENTITY_CUSTODY",
            "PROGRESSIVE_FIXED_HELP_AND_ANSWER_CLOSURE",
        }
        for control_id in required:
            self.assertIn(control_id, self.rows)
            self.assertNotEqual(self.rows[control_id]["target_ref"], "NONE")

    def test_product_implementations_and_topic_exemplars_are_not_authority(self):
        self.assertEqual(self.rows["B_LAYER_REPORTLAB_RENDERERS_AND_LAYOUT"]["disposition"], "REGRESSION_IMPLEMENTATION_ONLY")
        self.assertEqual(self.rows["TOPIC_SPECIFIC_HARD_DEEP_PRODUCT_EXEMPLAR"]["disposition"], "STRESS_REGRESSION_ONLY")
        self.assertEqual(self.rows["PR370_GOLDEN_INPUTS_AND_EMITTED_PRODUCTS"]["disposition"], "REGRESSION_EVIDENCE_ONLY")
        for control_id in (
            "B_LAYER_REPORTLAB_RENDERERS_AND_LAYOUT",
            "TOPIC_SPECIFIC_HARD_DEEP_PRODUCT_EXEMPLAR",
            "PR370_GOLDEN_INPUTS_AND_EMITTED_PRODUCTS",
        ):
            self.assertEqual(self.rows[control_id]["target_ref"], "NONE")

    def test_source_branch_was_green_before_supersession(self):
        source = self.migration["source_head_verification"]
        self.assertEqual(source["head_sha"], "42b051f242ca830b72773eda506da0988ad3c771")
        self.assertEqual(source["workflow_state"], "PASS")
        self.assertTrue(self.migration["status"].startswith("MIGRATION_COMPLETE"))


if __name__ == "__main__":
    unittest.main()
