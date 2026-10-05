from __future__ import annotations

import copy
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

from relay_tx import reconcile_roadmap
from test_relay_can import prepare_git
from test_v3_foundation import dump
from transactionlib import TransactionError
from v3lib import load_yaml


class RoadmapReconciliationTests(unittest.TestCase):
    def test_reconciliation_updates_existing_roadmap_transactionally(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            roadmap_path = root / "relay/ROADMAP/ROADMAP.yaml"
            current = load_yaml(roadmap_path)
            after = copy.deepcopy(current)
            after["revision"] = "RM-RECONCILED"
            after["work_packages"][0]["title"] = "Reconciled work"
            request = {
                "schema_version": "relay-v3.1-roadmap-reconciliation",
                "authority": "PROPOSED_RECONCILIATION",
                "expected_revision": current["revision"],
                "disposition": "UPDATE_WORK_PACKAGE",
                "basis": ["accepted execution evidence"],
                "roadmap_after": after,
            }
            request_path = root / "roadmap-reconciliation.yaml"
            dump(request_path, request)
            result = reconcile_roadmap(
                root,
                tx_id="TX-RM-001",
                event_id="EVT-RM-001",
                actor="agent-x",
                reconciliation_path=request_path,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual("RM-RECONCILED", state["roadmap"]["revision"])
            self.assertEqual("Reconciled work", load_yaml(roadmap_path)["work_packages"][0]["title"])

    def test_no_change_cannot_hide_a_roadmap_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            current = load_yaml(root / "relay/ROADMAP/ROADMAP.yaml")
            after = copy.deepcopy(current)
            after["work_packages"][0]["title"] = "Sneaky mutation"
            request = {
                "schema_version": "relay-v3.1-roadmap-reconciliation",
                "authority": "PROPOSED_RECONCILIATION",
                "expected_revision": current["revision"],
                "disposition": "NO_CHANGE",
                "basis": ["no change claimed"],
                "roadmap_after": after,
            }
            request_path = root / "roadmap-reconciliation.yaml"
            dump(request_path, request)
            with self.assertRaisesRegex(TransactionError, "cannot mutate"):
                reconcile_roadmap(
                    root,
                    tx_id="TX-RM-002",
                    event_id="EVT-RM-002",
                    actor="agent-x",
                    reconciliation_path=request_path,
                    base_ref=base_ref,
                )


if __name__ == "__main__":
    unittest.main()
