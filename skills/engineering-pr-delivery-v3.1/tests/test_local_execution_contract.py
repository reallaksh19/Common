from __future__ import annotations

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
from test_relay_can import prepare_git
from test_v3_foundation import dump
from transactionlib import TransactionError
from v3lib import load_events, load_yaml


class LocalExecutionContractTests(unittest.TestCase):
    def test_export_is_recipient_ready_and_result_returns_to_owner(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            tx = export_local_execution(
                root,
                tx_id="TX-LOCAL-CONTRACT",
                event_id="EVT-LOCAL-CONTRACT",
                actor="agent-x",
                base_ref=base_ref,
                commands=["python -m unittest tests.test_signed_pdf"],
            )
            self.assertEqual("COMMITTED", tx["status"])

            package = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION.yaml")
            request = package["request"]
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
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("LOCAL_EXECUTION_RETURNED", [row["type"] for row in events])

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
