import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM = ROOT.parent
POLICY = ROOT / "policies" / "product-control-consolidation.v1.json"
MIGRATION = ROOT / "policies" / "pr360-control-migration.v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ProductControlConsolidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load(POLICY)
        cls.migration = load(MIGRATION)

    def test_orchestration_is_fail_closed(self):
        o = self.policy["orchestration"]
        self.assertTrue(o["machine_readable_stage_contract_required"])
        self.assertTrue(o["silent_stage_skipping_forbidden"])
        self.assertTrue(o["not_applicable_requires_reason"])
        self.assertTrue(o["undeclared_stage_forbidden"])
        self.assertTrue(o["dependency_order_must_validate"])
        self.assertIn("falsifiers", o["stage_fields_required"])

    def test_denominator_is_evidence_derived_and_frozen_before_authoring(self):
        d = self.policy["source_denominator_custody"]
        self.assertTrue(d["freeze_before_authoring_required"])
        self.assertEqual(d["authoring_requires"], "FROZEN_ITEM_LEDGER")
        self.assertTrue(d["counter_values_must_be_derived_from_declared_evidence"])
        self.assertTrue(d["evidence_digest_required"])
        self.assertTrue(d["unresolved_values_must_be_recorded_not_inferred"])
        for key in ("TOTAL_SCANNED", "ELIGIBLE_IN_SCOPE", "PLACED_UNIQUE", "MISSING", "DUPLICATE_PRIMARY"):
            self.assertIn(key, d["required_counters"])

    def test_visual_obligations_are_local_not_global(self):
        v = self.policy["visual_obligations"]
        self.assertEqual(v["obligation_locality"], "CONTENT_REFERENCE")
        self.assertTrue(v["global_realization_does_not_satisfy_local_obligation"])
        self.assertTrue(v["renderer_selection_forbidden"])
        self.assertTrue(v["renderer_invention_forbidden"])
        self.assertTrue(v["text_substitution_for_required_visual_forbidden"])

    def test_learner_projection_fails_closed(self):
        p = self.policy["learner_surface_projection"]
        self.assertTrue(p["unmapped_internal_role_must_fail_closed"])
        self.assertTrue(p["fallback_prettification_of_internal_identifiers_forbidden"])
        self.assertTrue(p["internal_identifier_spellings_remain_machine_stable"])
        self.assertTrue(p["actionable_helper_required"])
        self.assertTrue(p["method_name_only_helper_is_not_actionable"])

    def test_legibility_separates_floor_target_and_density(self):
        l = self.policy["legibility_assurance"]
        self.assertTrue(l["engineering_font_floor_separate_from_learner_target"])
        self.assertTrue(l["role_level_measurement_required"])
        self.assertTrue(l["page_density_gate_required"])
        self.assertGreater(l["minimum_leading_ratio"], 1.0)
        self.assertLess(l["maximum_text_coverage_ratio"], 1.0)
        self.assertTrue(l["uncontrolled_shared_primitive_text_must_be_measured_not_silently_claimed_compliant"])

    def test_current_lineage_retains_absorbed_answer_and_execution_controls(self):
        execution = (CHEM / "LearnerProduct" / "EXECUTION_CONTRACT.md").read_text(encoding="utf-8")
        answers = load(CHEM / "LearnerProduct" / "policies" / "chemistry-answer-path-policy.json")
        language = load(CHEM / "LearnerProduct" / "policies" / "chemistry-learner-language-policy.json")
        render = load(CHEM / "LearnerProduct" / "policies" / "chemistry-learner-render-policy.json")
        v7 = load(ROOT / "policies" / "v7-product-assurance-policy.json")
        self.assertIn("Silent skipping is forbidden", execution)
        self.assertIn("C-LP-01 FREEZE_SOURCE_DENOMINATOR", execution)
        self.assertIn("C-LP-21 VALIDATE_ANSWER_CLOSURE", execution)
        self.assertEqual(answers["governing_rule"], "NO_LEARNER_FACING_QUESTION_WITHOUT_A_CHECKABLE_ANSWER_PATH")
        self.assertTrue(v7["question_custody"]["every_question_requires_answer_closure"])
        self.assertIn("actionability_rule", language)
        self.assertTrue(render["preflight"]["pdf_parse_required"])
        self.assertTrue(render["answer_visibility"]["no_question_without_answer_path"])

    def test_pr360_migration_has_no_unclassified_generic_control(self):
        rows = {row["control_id"]: row for row in self.migration["controls"]}
        expected = {
            "GENERATION_ORCHESTRATION_CONTRACT", "SOURCE_DENOMINATOR_FREEZE", "CAPABILITY_TAXONOMY_BREADTH",
            "LOCAL_VISUAL_OBLIGATION_CLOSURE", "HELPER_PEDAGOGY_ACTIONABILITY", "ANSWER_CUSTODY",
            "FAIL_CLOSED_LEARNER_ROLE_PROJECTION", "ROLE_LEVEL_LEGIBILITY_AND_DENSITY", "HISTORICAL_EXACT_PRODUCT_CANDIDATE",
        }
        self.assertEqual(set(rows), expected)
        for row in rows.values():
            if row["disposition"] == "PORTED_AS_GENERIC_INVARIANT":
                self.assertNotEqual(row["target_ref"], "NONE")
        self.assertEqual(rows["HISTORICAL_EXACT_PRODUCT_CANDIDATE"]["disposition"], "REGRESSION_EVIDENCE_ONLY")
        self.assertEqual(self.migration["status"], "MIGRATION_COMPLETE")
        self.assertEqual(self.migration["verification"]["v7_product_assurance"], "PASS")
        self.assertEqual(self.migration["verification"]["blueprint_v0_v6_regression_matrix"], "PASS")


if __name__ == "__main__":
    unittest.main()
