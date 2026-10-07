import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
SCRIPTS = ROOT / "scripts"
REFERENCES = ROOT / "references"
sys.path.insert(0, str(SCRIPTS))

from coordlib import load_yaml
from p3_integration_qualification import (
    CHECK_IDS,
    compile_qualification,
    validate_result,
    validate_result_shape,
    validate_source,
)


SOURCE_PATH = REFERENCES / "p3-i-integration-source.yaml"


def git(*args):
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


class Phase3IntegrationQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_yaml(SOURCE_PATH)
        cls.candidate_sha = git("rev-parse", "HEAD")
        cls.result = compile_qualification(
            cls.source,
            cls.candidate_sha,
            1,
            "prod/527-p3-i-full-solo-role-replay",
            REPO_ROOT,
        )

    def test_p3i_source_contract_is_valid(self):
        self.assertEqual([], validate_source(self.source))

    def test_p3i_result_shape_and_matrix_are_valid(self):
        self.assertEqual([], validate_result_shape(self.result))
        self.assertEqual(list(CHECK_IDS), [row["id"] for row in self.result["lanes"]])
        self.assertTrue(all(row["passed"] for row in self.result["lanes"]))
        self.assertEqual(20, self.result["accounting"]["passed"])
        self.assertEqual(0, self.result["accounting"]["failed"])
        self.assertEqual(0, self.result["accounting"]["clean_false_blocks"])
        self.assertEqual("QUALIFIED", self.result["qualification_status"])

    def test_p3i_clean_control_preserves_non_authoritative_semantics(self):
        clean = self.result["clean_control"]
        self.assertEqual("NOT_FALSIFIED", clean["project_falsification_status"])
        self.assertNotEqual("PASS", clean["project_falsification_status"])
        self.assertEqual("ADVANCE_ELIGIBLE", clean["gate_disposition"])
        self.assertEqual("REQUEST_STAGE_ADVANCE", clean["kernel_action"])
        self.assertFalse(clean["lifecycle_transition_performed"])
        self.assertEqual("NONE", self.result["principal_independence"])
        self.assertFalse(any(self.result["authority_boundaries"].values()))

    def test_p3i_required_adversarial_routes_are_observed(self):
        lanes = {row["id"]: row for row in self.result["lanes"]}
        self.assertIn("gate=REPLAY", lanes["P3I-02"]["observed"])
        self.assertEqual("REJECTED", lanes["P3I-03"]["observed"])
        self.assertIn("gate=REPLAY", lanes["P3I-04"]["observed"])
        self.assertIn("project=FALSIFIED", lanes["P3I-05"]["observed"])
        self.assertIn("gate=REPAIR", lanes["P3I-09"]["observed"])
        self.assertIn("gate=REPLAY", lanes["P3I-10"]["observed"])
        self.assertIn("gate=ESCALATE", lanes["P3I-11"]["observed"])
        self.assertEqual("gate=REPLAY", lanes["P3I-12"]["observed"])
        self.assertEqual("gate=REPLAY", lanes["P3I-13"]["observed"])
        self.assertEqual("gate=ADVANCE_ELIGIBLE", lanes["P3I-14"]["observed"])
        self.assertEqual("kernel=REQUEST_STAGE_ADVANCE", lanes["P3I-15"]["observed"])
        self.assertIn("reason=CAPABILITY_MISSING", lanes["P3I-16"]["observed"])
        self.assertEqual("REJECTED_UNBOUND", lanes["P3I-17"]["observed"])
        self.assertEqual("no forbidden authority true", lanes["P3I-18"]["observed"])
        self.assertEqual("P2-I=QUALIFIED", lanes["P3I-19"]["observed"])

    def test_p3i_stored_result_cannot_self_certify(self):
        errors = validate_result(self.result)
        self.assertTrue(
            any("source-bound exact-head P3-I replay is required" in row for row in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
