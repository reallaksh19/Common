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

from relay_tx import (
    accept_checkpoint,
    activate_lease,
    close_task,
    export_local_execution,
    publish_handover,
    release_lease,
    resolve_control,
    sync_delivery,
)
from snapshot_projection import build as build_snapshot
from test_relay_can import prepare_git
from test_v3_foundation import base_objects, dump
from transactionlib import TransactionError
from v3lib import load_events, load_yaml
from validate_foundation import validate, validate_authority


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


def configure_delivery(root: Path, base_ref: str, *, lifecycle: str = "MERGED") -> Path:
    state_path = root / "relay/STATE.yaml"
    state = load_yaml(state_path)
    state["delivery"] = {
        "required": True,
        "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
    }
    dump(state_path, state)
    dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", build_snapshot(root, base_ref))
    observation = {
        "schema_version": "relay-v3-delivery-status",
        "authority": "PROVIDER_READBACK",
        "vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
        "observed_at": "2026-09-22T03:57:35Z",
        "provider_ref": "github:reallaksh19/Common#419",
        "lifecycle": lifecycle,
        "checks": "PASS",
        "review": "APPROVED",
        "mergeability": "MERGEABLE",
    }
    path = root / "provider-observation.yaml"
    dump(path, observation)
    return path


class RelayTransactionalCommandTests(unittest.TestCase):
    def test_activate_lease_transfers_exclusive_custody_and_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
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
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            old = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            new = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            state = load_yaml(root / "relay/STATE.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("RELEASED", old["state"])
            self.assertEqual("ACTIVE", new["state"])
            self.assertEqual("agent-y", new["executor"]["id"])
            self.assertEqual("LEASE-TA-011-02", state["execution"]["lease"])
            self.assertEqual("LEASE-TA-011-02", snapshot["execution"]["lease"])
            self.assertEqual("agent-y", snapshot["execution"]["executor"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            ids = [item["event_id"] for item in events]
            self.assertIn("EVT-ACTIVATE-001-REL", ids)
            self.assertIn("EVT-ACTIVATE-001", ids)
            self.assertEqual([], validate(root))

    def test_release_lease_atomically_enters_idle_state_and_refreshes_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = release_lease(
                root,
                tx_id="TX-RELEASE-001",
                event_id="EVT-RELEASE-001",
                actor="agent-x",
            )
            self.assertEqual("COMMITTED", result["status"])
            lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            state = load_yaml(root / "relay/STATE.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("RELEASED", lease["state"])
            self.assertEqual(
                {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None},
                state["execution"],
            )
            self.assertEqual("IDLE", snapshot["execution"]["lifecycle"])
            self.assertIsNone(snapshot["execution"]["lease"])
            self.assertEqual([], validate(root))

    def test_accept_checkpoint_publishes_immutable_checkpoint_state_and_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
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
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            self.assertTrue((root / "relay/CHECKPOINTS/CP-TA-011.yaml").exists())
            state = load_yaml(root / "relay/STATE.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("CP-TA-011", state["accepted"]["checkpoint"])
            self.assertEqual("CP-TA-011", snapshot["evidence"]["latest_checkpoint"])
            self.assertEqual([], validate(root))

            with self.assertRaisesRegex(TransactionError, "immutable"):
                accept_checkpoint(
                    root,
                    tx_id="TX-CP-002",
                    event_id="EVT-CP-002",
                    actor="agent-x",
                    checkpoint_path=incoming,
                    base_ref=base_ref,
                )

    def test_failed_checkpoint_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
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
                    base_ref=base_ref,
                )
            self.assertFalse((root / "relay/CHECKPOINTS/CP-TA-011.yaml").exists())

    def test_control_resolution_changes_control_event_and_snapshot_together(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            add_open_control(root)
            result = resolve_control(
                root,
                tx_id="TX-CONTROL-001",
                event_id="EVT-CONTROL-001",
                actor="agent-x",
                control_id="CTRL-TEST-001",
                evidence=["provider readback PASS"],
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            controls = load_yaml(root / "relay/CONTROLS/controls.yaml")
            row = [item for item in controls["controls"] if item["id"] == "CTRL-TEST-001"][0]
            self.assertEqual("RESOLVED", row["state"])
            self.assertEqual(["provider readback PASS"], row["resolution"]["evidence"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("EVT-CONTROL-001", [item["event_id"] for item in events])
            self.assertEqual([], validate(root))

    def test_handover_and_local_execution_are_generated_downstream_views(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            handover = publish_handover(
                root,
                tx_id="TX-HANDOVER-001",
                event_id="EVT-HANDOVER-001",
                actor="agent-x",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", handover["status"])
            text = (root / "relay/GENERATED/HANDOVER.md").read_text(encoding="utf-8")
            self.assertIn("Engineering Relay V3 Handover", text)
            self.assertIn("Reconstruction sources", text)

            local = export_local_execution(
                root,
                tx_id="TX-LOCAL-001",
                event_id="EVT-LOCAL-001",
                actor="agent-x",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", local["status"])
            package = load_yaml(root / "relay/GENERATED/LOCAL_EXECUTION.yaml")
            self.assertEqual("DERIVED_EXECUTION_PACKAGE", package["authority"])
            self.assertEqual("EP-TA-011", package["execution"]["ep"])
            self.assertEqual("Validate schemas.", package["next"]["first_action"])
            self.assertEqual([], validate(root))

    def test_sync_delivery_requires_provider_vehicle_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            observation = configure_delivery(root, base_ref)
            result = sync_delivery(
                root,
                tx_id="TX-DELIVERY-001",
                event_id="EVT-DELIVERY-001",
                actor="provider-sync",
                observation_path=observation,
            )
            self.assertEqual("COMMITTED", result["status"])
            persisted = load_yaml(root / "relay/GENERATED/DELIVERY_STATUS.yaml")
            self.assertEqual("PROVIDER_READBACK", persisted["authority"])
            self.assertEqual("MERGED", persisted["lifecycle"])

            wrong = load_yaml(observation)
            wrong["vehicle"]["number"] = 999
            wrong_path = root / "wrong-provider-observation.yaml"
            dump(wrong_path, wrong)
            with self.assertRaisesRegex(TransactionError, "does not match"):
                sync_delivery(
                    root,
                    tx_id="TX-DELIVERY-002",
                    event_id="EVT-DELIVERY-002",
                    actor="provider-sync",
                    observation_path=wrong_path,
                )

    def test_close_requires_completed_delivery_and_closes_atomically(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            observation = configure_delivery(root, base_ref, lifecycle="OPEN")
            sync_delivery(
                root,
                tx_id="TX-DELIVERY-OPEN",
                event_id="EVT-DELIVERY-OPEN",
                actor="provider-sync",
                observation_path=observation,
            )
            with self.assertRaisesRegex(TransactionError, "must be MERGED"):
                close_task(
                    root,
                    tx_id="TX-CLOSE-BLOCKED",
                    event_id="EVT-CLOSE-BLOCKED",
                    actor="owner",
                )

            merged = load_yaml(observation)
            merged["lifecycle"] = "MERGED"
            dump(observation, merged)
            sync_delivery(
                root,
                tx_id="TX-DELIVERY-MERGED",
                event_id="EVT-DELIVERY-MERGED",
                actor="provider-sync",
                observation_path=observation,
            )
            result = close_task(
                root,
                tx_id="TX-CLOSE-001",
                event_id="EVT-CLOSE-001",
                actor="owner",
            )
            self.assertEqual("COMMITTED", result["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            snapshot = load_yaml(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml")
            self.assertEqual("TERMINAL", state["execution"]["lifecycle"])
            self.assertEqual("RELEASED", lease["state"])
            self.assertEqual("TERMINAL", snapshot["execution"]["lifecycle"])
            self.assertEqual([], validate(root))

    def test_incomplete_transaction_blocks_all_authority_until_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            with self.assertRaises(TransactionError):
                activate_lease(
                    root,
                    tx_id="TX-ACTIVATE-FAIL",
                    event_id="EVT-ACTIVATE-FAIL",
                    lease_id="LEASE-TA-011-02",
                    executor_id="agent-y",
                    actor="owner",
                    method="DETERMINISTIC",
                    qualification=None,
                    owner_basis=None,
                    branch=None,
                    base_ref=base_ref,
                    fail_after=1,
                )
            errors = validate_authority(root)
            self.assertTrue(any("requires recovery" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
