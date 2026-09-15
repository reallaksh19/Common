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
        self.assertEqual(rows[384]["ci_state"], "PASS")
        self.assertEqual(rows[387]["role"], "GENERIC_SOURCE_AUDIT_AND_ENGINEERING_WORKBENCH_V2")
        self.assertEqual(rows[387]["authority_class"], "ENGINEERING_CONTROL_PLANE_CANDIDATE")
        self.assertEqual(rows[387]["ci_state"], "PASS")
        self.assertEqual(rows[377]["disposition"], "SUPERSEDED_BY_387")
        self.assertEqual(rows[381]["disposition"], "SUPERSEDED_BY_387")
        self.assertEqual(rows[385]["authority_class"], "NON_AUTHORITATIVE_STRESS_TEST")

    def test_product_and_execution_siblings_have_explicit_retention_before_supersession(self):
        rows = {row["number"]: row for row in self.ledger["pull_requests"]}
        self.assertEqual(rows[360]["disposition"], "SUPERSEDED_BY_371")
        self.assertEqual(rows[360]["ci_state"], "MIGRATION_PASS")
        self.assertEqual(rows[362]["disposition"], "SUPERSEDED_BY_371_LINEAGE")
        self.assertEqual(rows[362]["ci_state"], "RETAINED_IN_371_ANCESTRY")

        migration = self.ledger["migration_evidence"]
        self.assertEqual(migration["360"]["target_pr"], 371)
        self.assertIn("GENERATION_ORCHESTRATION_CONTRACT", migration["360"]["controls_ported"])
        self.assertIn("ANSWER_CUSTODY", migration["360"]["controls_absorbed"])
        self.assertIn("HISTORICAL_EXACT_PRODUCT_CANDIDATE", migration["360"]["historical_only"])
        self.assertEqual(migration["362"]["target_pr"], 371)
        self.assertEqual(migration["362"]["retention_mode"], "GIT_ANCESTRY_AND_CURRENT_HEAD_FILES")
        for required in (
            "LearnerProduct/EXECUTION_CONTRACT.md",
            "LearnerProduct/policies/chemistry-answer-path-policy.json",
            "LearnerProduct/policies/chemistry-learner-render-policy.json",
            "LearnerProduct/engine/preflight_chemistry_learner_products.py",
        ):
            self.assertIn(required, migration["362"]["verified_current_head_files"])

    def test_supersession_requires_explicit_migration(self):
        preconditions = self.ledger["closure_preconditions"]
        for condition in ("PORT_LEDGER_COMPLETE", "NO_UNIQUE_GENERIC_CONTROL_LOST", "371_CONTROL_MIGRATION_CI_GREEN"):
            self.assertIn(condition, preconditions["360"])
        for condition in ("EXECUTION_MECHANICS_EXPLICITLY_RETAINED_IN_371_LINEAGE", "371_HEAD_CONTAINS_EXECUTION_CONTRACT_AND_PREFLIGHT"):
            self.assertIn(condition, preconditions["362"])
        for condition in ("GENERIC_SOURCE_HARDENING_REWRITTEN_ON_384_LINEAGE", "NO_REDOX_SPECIFIC_VALIDATOR_LOGIC_RETAINED", "387_GREEN"):
            self.assertIn(condition, preconditions["377"])
        for condition in ("TOPIC_NEUTRAL_CLOSURE_PORTED", "GENERIC_PRODUCT_SOURCE_SCOPE_PORTED", "CDAU_AND_PAL_CUSTODY_PORTED", "387_GREEN"):
            self.assertIn(condition, preconditions["381"])


if __name__ == "__main__":
    unittest.main()
