from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from intelligence_projection import build_task
from material_basis import inspect as inspect_material_basis
from relay_tx import activate_lease, record_continuation, record_recovery_reconstructed
from snapshot_projection import build as build_snapshot
from test_relay_can import prepare_git
from test_v3_foundation import dump
from transactionlib import TransactionError
from v3lib import canonical_digest, load_events, load_yaml


class ContinuationReceiptTests(unittest.TestCase):
    def _prepare(self, root: Path) -> tuple[str, dict, dict]:
        _base_sha, base_ref = prepare_git(root)
        state_path = root / "relay/STATE.yaml"
        state = load_yaml(state_path)
        state["execution"]["custody_epoch"] = 1
        dump(state_path, state)

        ep = load_yaml(root / "relay/WORK/EP-TA-011.yaml")
        lease_path = root / "relay/LEASES/LEASE-TA-011-01.yaml"
        lease = load_yaml(lease_path)
        activity = inspect_material_basis(root, ep, base_ref)["material_basis"]
        lease["custody"] = {
            "epoch": 1,
            "granted_at": "2026-09-23T12:00:00Z",
            "renewed_at": "2026-09-23T12:00:00Z",
            "recovery_after_seconds": 300,
            "recovery_policy": "TAKEOVER_AFTER_EXPIRY",
            "activity_basis": {
                "relevant_worktree_digest": activity["relevant_paths_digest"],
                "dependency_worktree_digest": activity["dependency_digest"],
                "material_head": activity["head"],
                "base_ref": base_ref,
            },
        }
        dump(lease_path, lease)
        dump(root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml", build_snapshot(root, base_ref))
        return base_ref, ep, activity

    def _receipt(self, ep: dict, activity: dict) -> dict:
        return {
            "schema_version": "relay-v3.1-continuation",
            "id": "CONT-TEST-001",
            "authority": "CONTINUATION_EVIDENCE",
            "recorded_at": "2026-09-23T12:01:00Z",
            "ep": {"id": ep["id"], "digest": canonical_digest(ep)},
            "custody": {
                "lease": "LEASE-TA-011-01",
                "epoch": 1,
                "executor": "agent-x",
            },
            "goal": {
                "issue": None,
                "issue_baseline_digest": None,
                "acceptance_focus": ["AC-1"],
            },
            "activity": {
                "current_action": "Run the next focused falsifier.",
                "why": "It advances AC-1 without changing accepted truth.",
            },
            "material": {
                "branch": "exec",
                "head": activity["head"],
                "recoverability": "DURABLE_REMOTE",
            },
            "progress": {
                "completed_since_checkpoint": ["Validated the first schema edge."],
                "discoveries": ["The next failure boundary is recoverable."],
                "attempted_and_rejected": ["Treating WIP as checkpoint truth."],
                "unresolved": ["Run the next falsifier."],
            },
            "next": {
                "immediate_action": "Run the next focused falsifier.",
                "stop_conditions": ["Do not cross protected scope."],
            },
        }

    def test_records_immutable_mid_ep_continuation_and_projects_it(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_ref, ep, activity = self._prepare(root)
            receipt = self._receipt(ep, activity)
            incoming = root / "continuation.yaml"
            dump(incoming, receipt)

            result = record_continuation(
                root,
                tx_id="TX-CONT-001",
                event_id="EVT-CONT-001",
                actor="agent-x",
                continuation_path=incoming,
                expected_custody_epoch=1,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])

            durable = root / "relay/CONTINUITY/EP-TA-011/CONT-TEST-001.yaml"
            self.assertTrue(durable.exists())
            self.assertEqual(receipt, load_yaml(durable))

            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            event = [row for row in events if row["type"] == "CONTINUATION_RECORDED"][-1]
            self.assertEqual("EP-TA-011", event["subject"])
            self.assertEqual("CONT-TEST-001", event["details"]["receipt"])

            task = build_task(root, base_ref)
            self.assertEqual("CONT-TEST-001", task["continuity"]["receipt"])
            self.assertEqual(["AC-1"], task["continuity"]["acceptance_focus"])
            self.assertEqual("CP-TA-010", load_yaml(root / "relay/STATE.yaml")["accepted"]["checkpoint"])

    def test_local_helper_cannot_author_continuation_for_current_custodian(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_ref, ep, activity = self._prepare(root)
            receipt = self._receipt(ep, activity)
            incoming = root / "continuation.yaml"
            dump(incoming, receipt)

            with self.assertRaisesRegex(
                TransactionError,
                "only the current lease executor may record continuation",
            ):
                record_continuation(
                    root,
                    tx_id="TX-CONT-HELPER",
                    event_id="EVT-CONT-HELPER",
                    actor="local-helper",
                    continuation_path=incoming,
                    expected_custody_epoch=1,
                    base_ref=base_ref,
                )

            self.assertFalse(
                (root / "relay/CONTINUITY/EP-TA-011/CONT-TEST-001.yaml").exists()
            )
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertNotIn(
                "CONTINUATION_RECORDED",
                [row["type"] for row in events],
            )

    def test_recovery_binds_predecessor_latest_continuation_without_changing_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_ref, ep, activity = self._prepare(root)
            receipt = self._receipt(ep, activity)
            incoming = root / "continuation.yaml"
            dump(incoming, receipt)
            record_continuation(
                root,
                tx_id="TX-CONT-RECOVERY",
                event_id="EVT-CONT-RECOVERY",
                actor="agent-x",
                continuation_path=incoming,
                expected_custody_epoch=1,
                base_ref=base_ref,
            )

            predecessor = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            renewed_at = datetime.fromisoformat(
                predecessor["custody"]["renewed_at"].replace("Z", "+00:00")
            )
            observed_at = (
                renewed_at + timedelta(minutes=6)
            ).isoformat().replace("+00:00", "Z")

            recovered = activate_lease(
                root,
                tx_id="TX-CONT-RECOVER",
                event_id="EVT-CONT-RECOVER",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                expected_custody_epoch=1,
                recovery_observed_at=observed_at,
            )
            self.assertEqual("COMMITTED", recovered["status"])

            reconstructed = record_recovery_reconstructed(
                root,
                tx_id="TX-CONT-RECONSTRUCT",
                event_id="EVT-CONT-RECONSTRUCT",
                actor="agent-y",
                evidence=["working material and continuation receipt reviewed"],
                expected_custody_epoch=2,
            )
            self.assertEqual("COMMITTED", reconstructed["status"])

            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            event = [
                row for row in events
                if row["type"] == "RECOVERY_RECONSTRUCTED"
            ][-1]
            predecessor_continuation = event["details"]["predecessor_continuation"]
            self.assertEqual(
                "CONT-TEST-001",
                predecessor_continuation["receipt"],
            )
            self.assertEqual(
                "relay/CONTINUITY/EP-TA-011/CONT-TEST-001.yaml",
                predecessor_continuation["path"],
            )
            self.assertIn(
                predecessor_continuation["path"],
                event["basis"],
            )
            self.assertIn(
                predecessor_continuation["digest"],
                event["basis"],
            )
            self.assertEqual(
                "CP-TA-010",
                load_yaml(root / "relay/STATE.yaml")["accepted"]["checkpoint"],
            )

    def test_recovery_reconstruction_fails_closed_on_tampered_continuation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_ref, ep, activity = self._prepare(root)
            receipt = self._receipt(ep, activity)
            incoming = root / "continuation.yaml"
            dump(incoming, receipt)
            record_continuation(
                root,
                tx_id="TX-CONT-TAMPER",
                event_id="EVT-CONT-TAMPER",
                actor="agent-x",
                continuation_path=incoming,
                expected_custody_epoch=1,
                base_ref=base_ref,
            )

            durable = root / "relay/CONTINUITY/EP-TA-011/CONT-TEST-001.yaml"
            tampered = load_yaml(durable)
            tampered["next"]["immediate_action"] = "tampered successor instruction"
            dump(durable, tampered)

            predecessor = load_yaml(root / "relay/LEASES/LEASE-TA-011-01.yaml")
            renewed_at = datetime.fromisoformat(
                predecessor["custody"]["renewed_at"].replace("Z", "+00:00")
            )
            observed_at = (
                renewed_at + timedelta(minutes=6)
            ).isoformat().replace("+00:00", "Z")
            activate_lease(
                root,
                tx_id="TX-CONT-TAMPER-RECOVER",
                event_id="EVT-CONT-TAMPER-RECOVER",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                expected_custody_epoch=1,
                recovery_observed_at=observed_at,
            )

            with self.assertRaisesRegex(
                TransactionError,
                "RECOVERY_CONTINUATION_DIGEST_MISMATCH",
            ):
                record_recovery_reconstructed(
                    root,
                    tx_id="TX-CONT-TAMPER-RECONSTRUCT",
                    event_id="EVT-CONT-TAMPER-RECONSTRUCT",
                    actor="agent-y",
                    evidence=["attempted reconstruction"],
                    expected_custody_epoch=2,
                )

    def test_rejects_goal_drift_outside_ep_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_ref, ep, activity = self._prepare(root)
            receipt = self._receipt(ep, activity)
            receipt["goal"]["acceptance_focus"] = ["AC-NOT-IN-EP"]
            incoming = root / "continuation.yaml"
            dump(incoming, receipt)

            with self.assertRaisesRegex(TransactionError, "CONTINUATION_ACCEPTANCE_FOCUS_UNKNOWN"):
                record_continuation(
                    root,
                    tx_id="TX-CONT-002",
                    event_id="EVT-CONT-002",
                    actor="agent-x",
                    continuation_path=incoming,
                    expected_custody_epoch=1,
                    base_ref=base_ref,
                )
            self.assertFalse(
                (root / "relay/CONTINUITY/EP-TA-011/CONT-TEST-001.yaml").exists()
            )


if __name__ == "__main__":
    unittest.main()
