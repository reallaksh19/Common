import ast
import json
import unittest
from pathlib import Path

BLUEPRINT = Path(__file__).resolve().parents[1]
CHEMISTRY = BLUEPRINT.parent
POLICY_PATH = BLUEPRINT / "policies" / "topic-stress-test-boundary.v1.json"
LEDGER_PATH = CHEMISTRY / "Governance" / "chemistry-pr-consolidation.v1.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def named_tokens(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        yield node.name
    elif isinstance(node, ast.Name):
        yield node.id
    elif isinstance(node, ast.arg):
        yield node.arg
    elif isinstance(node, ast.Attribute):
        yield node.attr


class ArchitectureGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load_json(POLICY_PATH)
        cls.ledger = load_json(LEDGER_PATH)
        cls.stress_tokens = {row["topic_id"].lower() for row in cls.policy["stress_topics"]}

    def test_redox_is_explicitly_non_authoritative(self):
        redox = next(x for x in self.policy["stress_topics"] if x["topic_id"] == "REDOX")
        self.assertEqual(redox["role"], "STRESS_TEST")
        self.assertEqual(redox["authority_status"], "NON_AUTHORITATIVE_FIXTURE")
        for forbidden in ("GROUND_TRUTH", "CANONICAL_AUTHORITY", "GENERIC_ENGINE_BRANCH_KEY", "DEFAULT_POLICY_BASIS"):
            self.assertIn(forbidden, redox["forbidden_uses"])

    def test_generic_engine_has_no_topic_named_symbols_or_branching(self):
        findings = []
        for path in sorted((BLUEPRINT / "engine").rglob("*.py")):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                for name in named_tokens(node):
                    for token in self.stress_tokens:
                        if token in name.lower():
                            findings.append(f"TOPIC_NAMED_GENERIC_SYMBOL:{path.relative_to(CHEMISTRY)}:{name}")
                if isinstance(node, (ast.If, ast.IfExp, ast.Compare, ast.Match)):
                    segment = (ast.get_source_segment(source, node) or "").lower()
                    for token in self.stress_tokens:
                        if token in segment:
                            findings.append(f"TOPIC_NAMED_GENERIC_BRANCH:{path.relative_to(CHEMISTRY)}:{token}")
        self.assertEqual(findings, [], "\n".join(findings))

    def test_generic_engine_does_not_read_committed_fixture_paths(self):
        findings = []
        forbidden = ("/golden/", "golden/", "/fixtures/", "fixtures/", "/stress_tests/", "stress_tests/")
        for path in sorted((BLUEPRINT / "engine").rglob("*.py")):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value.replace("\\", "/").lower()
                    if any(fragment in value for fragment in forbidden):
                        findings.append(f"GENERIC_ENGINE_FIXTURE_PATH_DEPENDENCY:{path.relative_to(CHEMISTRY)}:{node.value}")
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imported = (ast.get_source_segment(source, node) or "").replace("\\", "/").lower()
                    if any(fragment.strip("/") in imported for fragment in forbidden):
                        findings.append(f"GENERIC_ENGINE_FIXTURE_IMPORT:{path.relative_to(CHEMISTRY)}:{imported}")
        self.assertEqual(findings, [], "\n".join(findings))

    def test_pr_ledger_has_one_active_engineering_control_plane(self):
        rows = {row["number"]: row for row in self.ledger["pull_requests"]}
        self.assertEqual(self.ledger["target_active_stack"], [371, 384, 387, 385])
        self.assertEqual(rows[371]["authority_class"], "BLUEPRINT_PRODUCT_AND_GOVERNANCE_AUTHORITY")
        self.assertEqual(rows[371]["ci_state"], "PASS_GOVERNANCE_INTEGRATED")
        self.assertEqual(rows[384]["ci_state"], "PASS")
        self.assertEqual(rows[387]["role"], "GENERIC_SOURCE_AUDIT_AND_ENGINEERING_WORKBENCH_V2")
        self.assertEqual(rows[387]["authority_class"], "ENGINEERING_CONTROL_PLANE_CANDIDATE")
        self.assertEqual(rows[387]["ci_state"], "PASS")
        self.assertEqual(rows[377]["disposition"], "SUPERSEDED_BY_387")
        self.assertEqual(rows[381]["disposition"], "SUPERSEDED_BY_387")
        self.assertEqual(rows[385]["authority_class"], "NON_AUTHORITATIVE_STRESS_TEST")

    def test_closed_siblings_have_explicit_retention_or_migration(self):
        rows = {row["number"]: row for row in self.ledger["pull_requests"]}
        self.assertEqual(rows[322]["disposition"], "SUPERSEDED_BY_371_LINEAGE")
        self.assertEqual(rows[346]["disposition"], "SUPERSEDED_BY_371_LINEAGE")
        self.assertEqual(rows[360]["disposition"], "SUPERSEDED_BY_371")
        self.assertEqual(rows[362]["disposition"], "SUPERSEDED_BY_371_LINEAGE")
        self.assertEqual(rows[370]["disposition"], "SUPERSEDED_BY_371_STATIC_B_LAYER_BOUNDARY")
        self.assertEqual(rows[375]["disposition"], "CLOSED_REGRESSION_PROOF")
        self.assertEqual(rows[386]["disposition"], "SUPERSEDED_BY_371_GOVERNANCE_INTEGRATION")
        self.assertEqual(rows[386]["ci_state"], "MIGRATION_PASS")

        migration = self.ledger["migration_evidence"]
        self.assertEqual(migration["322_346"]["verification_state"], "RETENTION_COMPLETE_CI_PASS")
        self.assertEqual(migration["360"]["target_pr"], 371)
        self.assertIn("GENERATION_ORCHESTRATION_CONTRACT", migration["360"]["controls_ported"])
        self.assertEqual(migration["362"]["retention_mode"], "GIT_ANCESTRY_AND_CURRENT_HEAD_FILES")
        self.assertEqual(migration["370"]["target_pr"], 371)
        self.assertIn("CORE1B_MODULE_SPECIFIC_HINT_LADDERS", migration["370"]["controls_ported"])
        self.assertIn("TOPIC_SPECIFIC_HARD_DEEP_PRODUCT_EXEMPLAR", migration["370"]["regression_only"])
        self.assertFalse(migration["375"]["unique_generic_control_found"])
        self.assertEqual(migration["386"]["target_pr"], 371)
        self.assertEqual(migration["386"]["target_governance_workflow_state"], "PASS")
        self.assertEqual(migration["386"]["target_blueprint_matrix_state"], "V0_V7_PASS")
        self.assertEqual(migration["386"]["stale_reference_corrected"], "TARGET_STACK_USES_387_NOT_381")

    def test_supersession_requires_explicit_migration(self):
        preconditions = self.ledger["closure_preconditions"]
        for key in ("322_346", "360", "362", "370", "375", "377", "381", "386", "385"):
            self.assertIn(key, preconditions)
            self.assertTrue(preconditions[key])
        for condition in ("TOPIC_STRESS_FIREWALL_PORTED_TO_371", "CONSOLIDATION_LEDGER_PORTED_TO_371", "GOVERNANCE_TEST_AND_WORKFLOW_GREEN_ON_371"):
            self.assertIn(condition, preconditions["386"])

    def test_governance_integration_state_is_explicit(self):
        self.assertEqual(self.ledger["status"], "GOVERNANCE_INTEGRATION_COMPLETE")
        row = next(x for x in self.ledger["pull_requests"] if x["number"] == 386)
        self.assertEqual(row["ci_state"], "MIGRATION_PASS")


if __name__ == "__main__":
    unittest.main()
