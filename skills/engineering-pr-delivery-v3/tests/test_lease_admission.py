from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from lease_admission import AdmissionError, build_native_lease
from test_v3_foundation import DIGEST, dump, materialize
from v3lib import validate_schema


class LeaseAdmissionTests(unittest.TestCase):
    def test_deterministic_admission_builds_one_native_lease(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            lease = build_native_lease(
                root,
                lease_id="LEASE-NEXT-001",
                executor_id="agent-x",
                method="DETERMINISTIC",
            )
            self.assertEqual("relay-v3-lease", lease["schema_version"])
            self.assertEqual("DETERMINISTIC", lease["admission"]["method"])
            self.assertFalse(lease["admission"]["qualification"]["required"])
            self.assertEqual([], lease["admission"]["qualification"]["evidence"])
            self.assertIn("MATERIAL_WRITE", lease["authority"]["actions"])
            self.assertNotIn("MERGE", lease["authority"]["actions"])
            self.assertEqual([], validate_schema("lease", lease, "LEASE"))


    def test_lease_id_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            with self.assertRaisesRegex(AdmissionError, "unsafe characters"):
                build_native_lease(
                    root,
                    lease_id="LEASE-../ESCAPE",
                    executor_id="agent-x",
                    method="DETERMINISTIC",
                )

    def test_required_qualification_rejects_deterministic_admission(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            ep_path = root / "relay/WORK/EP-TA-011.yaml"
            ep = yaml.safe_load(ep_path.read_text(encoding="utf-8"))
            ep["admission_policy"] = {
                "qualification": "REQUIRED",
                "question_policy": "Q1_Q5",
            }
            dump(ep_path, ep)
            with self.assertRaisesRegex(AdmissionError, "requires qualification"):
                build_native_lease(
                    root,
                    lease_id="LEASE-NEXT-002",
                    executor_id="agent-x",
                    method="DETERMINISTIC",
                )

    def test_qualified_admission_binds_evidence_inside_lease(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            ep_path = root / "relay/WORK/EP-TA-011.yaml"
            ep = yaml.safe_load(ep_path.read_text(encoding="utf-8"))
            ep["admission_policy"] = {
                "qualification": "REQUIRED",
                "question_policy": "Q1_Q5",
            }
            dump(ep_path, ep)
            lease = build_native_lease(
                root,
                lease_id="LEASE-NEXT-003",
                executor_id="agent-x",
                method="QUALIFIED",
                qualification={
                    "qset": "QSET-V3-001",
                    "evaluator": "reviewer-y",
                    "evidence": ["Q1-Q5 PASS", "repository-only reconstruction"],
                },
            )
            q = lease["admission"]["qualification"]
            self.assertTrue(q["required"])
            self.assertEqual("QSET-V3-001", q["qset"])
            self.assertEqual("reviewer-y", q["evaluator"])
            self.assertEqual("PASS", q["result"])
            self.assertEqual(2, len(q["evidence"]))

    def test_qualified_admission_rejects_self_evaluation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            with self.assertRaisesRegex(AdmissionError, "cannot be the execution candidate"):
                build_native_lease(
                    root,
                    lease_id="LEASE-NEXT-004",
                    executor_id="agent-x",
                    method="QUALIFIED",
                    qualification={
                        "qset": "QSET-V3-001",
                        "evaluator": "agent-x",
                        "evidence": ["self asserted"],
                    },
                )

    def test_exclusive_active_lease_blocks_other_executor(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            with self.assertRaisesRegex(AdmissionError, "ACTIVE lease for another executor"):
                build_native_lease(
                    root,
                    lease_id="LEASE-NEXT-005",
                    executor_id="agent-y",
                    method="DETERMINISTIC",
                )

    def test_owner_override_is_bounded_and_not_delivery_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            lease = build_native_lease(
                root,
                lease_id="LEASE-OVERRIDE-001",
                executor_id="agent-x",
                method="OWNER_OVERRIDE",
                owner_basis={
                    "direct_utterance_digest": DIGEST,
                    "session_timestamp": "2026-09-22T03:29:06Z",
                },
                branch="fix/bounded-owner-work",
            )
            self.assertEqual("OWNER_OVERRIDE", lease["admission"]["method"])
            self.assertFalse(lease["admission"]["repository_only"])
            self.assertIn("MATERIAL_WRITE", lease["authority"]["actions"])
            self.assertNotIn("MERGE", lease["authority"]["actions"])
            self.assertNotIn("RELEASE", lease["authority"]["actions"])
            self.assertIn("MERGE", lease["scope"]["prohibited"])
            self.assertEqual([], validate_schema("lease", lease, "LEASE"))


if __name__ == "__main__":
    unittest.main()
