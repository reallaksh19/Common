from __future__ import annotations

import copy
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

from relay_tx import accept_checkpoint, activate_lease, release_lease, resolve_control
from test_v3_foundation import base_objects, dump, materialize
from transactionlib import TransactionError
from v3lib import load_events
from validate_foundation import validate_authority


def add_open_control(root: Path) -> None:
    path = root / "relay/CONTROLS/controls.yaml"
    controls = yaml.safe_load(path.read_text(encoding="utf-8"))
    controls["controls"].append({
        "id": "CTRL-TEST-001",
        "kind": "DELIVERY",
        "state": "OPEN",
        "source": {"type": "VALIDATOR", "ref": "synthetic"},
        "condition": "Synthetic delivery obligation.",
        "blocks": ["PR_READY"],
        "permits": ["MATERIAL_WRITE"],
        "resolution": {"condition": "Evidence supplied.", "evidence": []},
    })
    dump(path, controls)


class RelayTransactionalCommandTests(unittest.TestCase):
    def test_activate_lease_transfers_exclusive_custody_in_one_transaction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            result = activate_lease(
                root,
                tx_id="TX-ACTIVATE-001",
                event_id="EVT-ACTIVATE-001",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="owner",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
            )
            self.assertEqual("COMMITTED", result["status"])
            old = yaml.safe_load((root / "relay/LEASES/LEASE-TA-011-01.yaml").read_text(encoding="utf-8"))
            new = yaml.safe_load((root / "relay/LEASES/LEASE-TA-011-02.yaml").read_text(encoding="utf-8"))
            state = yaml.safe_load((root / "relay/STATE.yaml").read_text(encoding="utf-8"))
            self.assertEqual("RELEASED", old["state"])
            self.assertEqual("ACTIVE", new["state"])
            self.assertEqual("agent-y", new["executor"]["id"])
            self.assertEqual("LEASE-TA-011-02", state["execution"]["lease"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            ids = [item["event_id"] for item in events]
            self.assertIn("EVT-ACTIVATE-001-REL", ids)
            self.assertIn("EVT-ACTIVATE-001", ids)
            self.assertEqual([], validate_authority(root))

    def test_release_lease_atomically_enters_idle_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            result = release_lease(
                root,
                tx_id="TX-RELEASE-001",
                event_id="EVT-RELEASE-001",
                actor="agent-x",
            )
            self.assertEqual("COMMITTED", result["status"])
            lease = yaml.safe_load((root / "relay/LEASES/LEASE-TA-011-01.yaml").read_text(encoding="utf-8"))
            state = yaml.safe_load((root / "relay/STATE.yaml").read_text(encoding="utf-8"))
            self.assertEqual("RELEASED", lease["state"])
            self.assertEqual(
                {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None},
                state["execution"],
            )
            self.assertEqual([], validate_authority(root))

    def test_accept_checkpoint_publishes_immutable_checkpoint_and_state_pointer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint["id"] = "CP-TA-011"
            checkpoint["ep"] = "EP-TA-011"
            incoming = root / "incoming-checkpoint.yaml"
            dump(incoming, checkpoint)

            result = accept_checkpoint(
                root,
                tx_id="TX-CP-001",
                event_id="EVT-CP-001",
                actor="agent-x",
                checkpoint_path=incoming,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertTrue((root / "relay/CHECKPOINTS/CP-TA-011.yaml").exists())
            state = yaml.safe_load((root / "relay/STATE.yaml").read_text(encoding="utf-8"))
            self.assertEqual("CP-TA-011", state["accepted"]["checkpoint"])
            self.assertEqual([], validate_authority(root))

            with self.assertRaisesRegex(TransactionError, "immutable"):
                accept_checkpoint(
                    root,
                    tx_id="TX-CP-002",
                    event_id="EVT-CP-002",
                    actor="agent-x",
                    checkpoint_path=incoming,
                )

    def test_failed_checkpoint_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            _, _, _, _, template, *_ = base_objects()
            checkpoint = copy.deepcopy(template)
            checkpoint["id"] = "CP-TA-011"
            checkpoint["ep"] = "EP-TA-011"
            checkpoint["acceptance"][0]["result"] = "FAIL"
            incoming = root / "incoming-checkpoint.yaml"
            dump(incoming, checkpoint)
            with self.assertRaisesRegex(TransactionError, "every criterion PASS"):
                accept_checkpoint(
                    root,
                    tx_id="TX-CP-FAIL",
                    event_id="EVT-CP-FAIL",
                    actor="agent-x",
                    checkpoint_path=incoming,
                )
            self.assertFalse((root / "relay/CHECKPOINTS/CP-TA-011.yaml").exists())

    def test_control_resolution_changes_control_and_event_together(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialize(root)
            add_open_control(root)
            result = resolve_control(
                root,
                tx_id="TX-CONTROL-001",
                event_id="EVT-CONTROL-001",
                actor="agent-x",
                control_id="CTRL-TEST-001",
                evidence=["provider readback PASS"],
            )
            self.assertEqual("COMMITTED", result["status"])
            controls = yaml.safe_load((root / "relay/CONTROLS/controls.yaml").read_text(encoding="utf-8"))
            row = [item for item in controls["controls"] if item["id"] == "CTRL-TEST-001"][0]
            self.assertEqual("RESOLVED", row["state"])
            self.assertEqual(["provider readback PASS"], row["resolution"]["evidence"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("EVT-CONTROL-001", [item["event_id"] for item in events])


if __name__ == "__main__":
    unittest.main()
