from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from relay_tx import accept_local_execution_result, export_local_execution
from test_handover_context import install_parent_issue
from test_relay_can import prepare_git
from test_v3_foundation import dump
from transactionlib import TransactionError
from v3lib import canonical_digest, load_events, load_yaml


class LocalExecutionContractTests(unittest.TestCase):
    def test_export_is_recipient_ready_and_result_returns_to_owner(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_parent_issue(root, number=1771)
            subprocess.check_call(
                ["git", "-C", str(root), "remote", "add", "origin", "https://github.com/example/project.git"]
            )
            tx = export_local_execution(
                root,
                tx_id="TX-LOCAL-CONTRACT",
                event_id="EVT-LOCAL-CONTRACT",
                actor="agent-x",
                base_ref=base_ref,
                commands=["python -m unittest tests.test_signed_pdf"],
                return_sub_issue="https://github.com/example/project/issues/202",
            )
            self.assertEqual("COMMITTED", tx["status"])

            package = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION.yaml")
            request = package["request"]
            self.assertEqual("LOCAL.1771.1", request["id"])
            self.assertEqual(request["id"], package["return_contract"]["request_id"])
            self.assertEqual(package["material"]["head"], request["exact_basis"]["material_head"])
            self.assertTrue(request["preflight"])
            self.assertTrue(request["steps"])
            self.assertIn("observed_head", package["return_contract"]["required_fields"])
            rendered = (root / "relay/GENERATED/LOCAL_EXECUTION.md").read_text(encoding="utf-8")
            self.assertIn("Local Execution Request", rendered)
            self.assertIn(request["exact_basis"]["material_head"], rendered)
            self.assertIn("HEAD_MISMATCH", rendered)
            self.assertIn("python -m unittest tests.test_signed_pdf", rendered)
            self.assertEqual("python -m unittest tests.test_signed_pdf", request["steps"][0]["command"])
            self.assertEqual("https://github.com/example/project.git", package["repository"]["clone_url"])
            self.assertIn("git clone https://github.com/example/project.git", rendered)
            self.assertEqual(
                "https://github.com/example/project/issues/202",
                package["provider_return"]["target_sub_issue"],
            )
            self.assertIn("Provider sub-issue update", rendered)
            self.assertIn("https://github.com/example/project/issues/202", rendered)
            self.assertIn("Return exactly this contract", rendered)
            self.assertIn("originating owner resumes responsibility", rendered)

            result = {
                "schema_version": "relay-v3.1-local-execution-result",
                "authority": "EXTERNAL_EXECUTION_EVIDENCE",
                "request_id": request["id"],
                "status": "PASS",
                "observed_head": request["exact_basis"]["material_head"],
                "environment": {"os": "test"},
                "command_results": [],
                "failures": [],
                "artifacts": [],
            }
            result_path = root / "local-result.yaml"
            dump(result_path, result)
            returned = accept_local_execution_result(
                root,
                tx_id="TX-LOCAL-RETURN",
                event_id="EVT-LOCAL-RETURN",
                actor="local-agent",
                result_path=result_path,
            )
            self.assertEqual("COMMITTED", returned["status"])
            persisted = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION_RESULT.yaml")
            self.assertEqual("PASS", persisted["status"])
            first_digest = canonical_digest(result)
            first_evidence = (
                root
                / "relay/EVIDENCE/local"
                / request["id"]
                / f"{first_digest.split(':', 1)[-1]}.yaml"
            )
            self.assertTrue(first_evidence.exists())
            self.assertEqual("PASS", load_yaml(first_evidence)["status"])

            second = dict(result)
            second["status"] = "FAIL"
            second["failures"] = ["synthetic second return"]
            second_path = root / "local-result-second.yaml"
            dump(second_path, second)
            second_returned = accept_local_execution_result(
                root,
                tx_id="TX-LOCAL-RETURN-SECOND",
                event_id="EVT-LOCAL-RETURN-SECOND",
                actor="local-agent",
                result_path=second_path,
            )
            self.assertEqual("COMMITTED", second_returned["status"])
            self.assertEqual("PASS", load_yaml(first_evidence)["status"])
            self.assertEqual(
                "FAIL",
                load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION_RESULT.yaml")["status"],
            )

            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            returned_events = [row for row in events if row["type"] == "LOCAL_EXECUTION_RETURNED"]
            self.assertEqual(2, len(returned_events))
            for row in returned_events:
                evidence_path = (row.get("details") or {}).get("evidence_path")
                self.assertTrue(evidence_path)
                self.assertTrue((root / evidence_path).exists())

    def test_non_mismatch_result_cannot_return_from_wrong_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            export_local_execution(
                root,
                tx_id="TX-LOCAL-WRONG-HEAD",
                event_id="EVT-LOCAL-WRONG-HEAD",
                actor="agent-x",
                base_ref=base_ref,
            )
            package = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION.yaml")
            result = {
                "schema_version": "relay-v3.1-local-execution-result",
                "authority": "EXTERNAL_EXECUTION_EVIDENCE",
                "request_id": package["request"]["id"],
                "status": "PASS",
                "observed_head": "deadbeef",
                "environment": {"os": "test"},
                "command_results": [],
                "failures": [],
                "artifacts": [],
            }
            path = root / "wrong-head.yaml"
            dump(path, result)
            with self.assertRaisesRegex(TransactionError, "observed_head"):
                accept_local_execution_result(
                    root,
                    tx_id="TX-LOCAL-WRONG-RETURN",
                    event_id="EVT-LOCAL-WRONG-RETURN",
                    actor="local-agent",
                    result_path=path,
                )


if __name__ == "__main__":
    unittest.main()
