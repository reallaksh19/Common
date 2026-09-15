import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM = ROOT.parent
POLICY_PATH = ROOT / "policies" / "legacy-foundation-retention.v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class LegacyFoundationRetentionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load(POLICY_PATH)
        cls.p346 = cls.policy["source_prs"]["346"]
        cls.p322 = cls.policy["source_prs"]["322"]

    def test_pr346_handoff_is_explicitly_historical_non_authority(self):
        self.assertEqual(self.p346["disposition"], "INHERITED_HISTORICAL_AUTHORING_HANDOFF")
        self.assertEqual(self.p346["authority_effect"], "NONE_HISTORICAL_EVIDENCE_ONLY")
        for forbidden in (
            "CURRENT_SOURCE_DENOMINATOR",
            "CURRENT_GROUND_TRUTH",
            "CANONICAL_DOMAIN_AUTHORITY",
            "GENERIC_ENGINE_BRANCH_KEY",
            "DEFAULT_PRODUCT_POLICY",
        ):
            self.assertIn(forbidden, self.p346["forbidden_uses"])

        manifest = load(CHEM / "AuthoringHandoff" / "NCERT-Core-Workbench" / "HANDOFF_MANIFEST.json")
        self.assertEqual(manifest["status"], "DRAFT_WORKING_HANDOFF")
        self.assertGreater(len(manifest["topics"]), 0)
        self.assertIn("topic names and retained-question counts in HANDOFF_MANIFEST.json", self.p346["historical_only"])

    def test_pr346_generic_controls_are_owned_by_current_lineage(self):
        absorbed = self.p346["generic_controls_already_absorbed"]
        self.assertIn("product-control-consolidation.v1.json#source_denominator_custody", absorbed["source_denominator_freeze"])
        self.assertIn("product-control-consolidation.v1.json#visual_obligations", absorbed["local_visual_obligations"])
        self.assertIn("chemistry-answer-path-policy.json", absorbed["answer_path_closure"])
        self.assertIn("preflight_chemistry_learner_products.py", absorbed["rendered_page_inspection"])

    def test_pr322_publication_engineering_infrastructure_is_present(self):
        self.assertEqual(self.p322["disposition"], "INHERITED_PUBLICATION_ENGINEERING_INFRASTRUCTURE")
        self.assertEqual(self.p322["authority_effect"], "PUBLICATION_ENGINEERING_ONLY")
        required = [
            CHEM / "ExactProduct" / "engine" / "chemistry_notation.py",
            CHEM / "ExactProduct" / "engine" / "chemistry_visual_primitives.py",
            CHEM / "ExactProduct" / "engine" / "learner_surface_guard.py",
            CHEM / "ExactProduct" / "validator" / "validate_chemistry_custody.py",
            CHEM / "ExactProduct" / "registry" / "chemistry-exact-product-quality-policy.json",
        ]
        for path in required:
            self.assertTrue(path.exists(), str(path))

    def test_pr322_retains_independent_physical_and_surface_custody(self):
        custody = (CHEM / "ExactProduct" / "validator" / "validate_chemistry_custody.py").read_text(encoding="utf-8")
        guard = (CHEM / "ExactProduct" / "engine" / "learner_surface_guard.py").read_text(encoding="utf-8")
        notation = (CHEM / "ExactProduct" / "engine" / "chemistry_notation.py").read_text(encoding="utf-8")

        self.assertIn("EXACT_ARTIFACT_HASH_MISMATCH", custody)
        self.assertIn("PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE", custody)
        self.assertIn("ORPHAN_CONTINUATION_FRAGMENT", custody)
        self.assertIn("MasterTemplates.VisualSemanticValidator", custody)
        self.assertIn("LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK", guard)
        self.assertIn("Redox, conservation, acid-base and every other reaction type are handled as data", notation)

    def test_pr322_machine_gate_cannot_substitute_for_human_gates(self):
        quality = load(CHEM / "ExactProduct" / "registry" / "chemistry-exact-product-quality-policy.json")
        required_states = set(quality["required_quality_states"])
        for state in self.p322["human_gates_remain_independent"]:
            self.assertIn(state, required_states)
        self.assertIn("MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS", quality["release_falsifiers"])
        self.assertIn("HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT", quality["release_falsifiers"])

    def test_historical_exact_candidate_is_not_current_authority(self):
        self.assertIn("CHEM-C-L-EXACT-CANDIDATE-A PDF bytes", self.p322["historical_only"])
        self.assertIn("CURRENT_CANONICAL_PRODUCT", self.p322["forbidden_uses"])
        candidate_dir = CHEM / "ExactProduct" / "candidates" / "CHEM-C-L-EXACT-CANDIDATE-A"
        self.assertTrue(candidate_dir.exists())
        self.assertTrue((candidate_dir / "FROZEN_MANIFEST.json").exists())

    def test_current_blueprint_engines_do_not_depend_on_legacy_handoff_or_candidate_paths(self):
        findings = []
        forbidden_fragments = (
            "authoringhandoff/",
            "ncert-core-workbench",
            "exactproduct/candidates/",
            "chem-c-l-exact-candidate-a",
        )
        for path in sorted((ROOT / "engine").rglob("*.py")):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value.replace("\\", "/").lower()
                    if any(fragment in value for fragment in forbidden_fragments):
                        findings.append(f"LEGACY_AUTHORITY_DEPENDENCY:{path.name}:{node.value}")
        self.assertEqual(findings, [], "\n".join(findings))

    def test_retention_status_is_explicit(self):
        self.assertEqual(self.policy["status"], "RETENTION_CLASSIFIED_PENDING_CI")
        self.assertIn("CLOSING_SOURCE_PRS_DOES_NOT_DELETE_INHERITED_FILES_OR_RECOVERABLE_BRANCHES", self.policy["global_invariants"])


if __name__ == "__main__":
    unittest.main()
