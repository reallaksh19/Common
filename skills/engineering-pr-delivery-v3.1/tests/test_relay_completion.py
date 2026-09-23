from __future__ import annotations

import copy
import sys
from datetime import datetime, timedelta
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from plan_handover import plan_handover
from relay_can import evaluate
from relay_tx import (
    activate_lease,
    authorize_change_delta,
    propose_change_delta,
    publish_handover,
    reconcile_roadmap,
    record_change_hypothesis,
    record_recovery_reconstructed,
    renew_lease,
    verify_change_delta,
)
from test_handover_context import install_standalone, target_observation
from test_relay_can import WRITE_PATH, prepare_git
from test_relay_tx import accept_current_checkpoint_and_reconcile
from test_v3_foundation import DIGEST, dump
from transactionlib import TransactionError
from v3lib import load_events, load_yaml
from validate_foundation import validate


class RelayCompletionTests(unittest.TestCase):
    def test_epoch_fences_stale_runner_and_expiry_allows_on_demand_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            first = activate_lease(
                root,
                tx_id="TX-EPOCH-START",
                event_id="EVT-EPOCH-START",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", first["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual(1, state["execution"]["custody_epoch"])

            missing = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertFalse(missing["allowed"], missing)
            self.assertIn("CUSTODY_EPOCH_REQUIRED", missing["reason_codes"])
            current = evaluate(
                root,
                "MATERIAL_WRITE",
                path=WRITE_PATH,
                base_ref=base_ref,
                expected_custody_epoch=1,
            )
            self.assertTrue(current["allowed"], current)

            current_lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            renewal_basis = current_lease["custody"]["renewed_at"]
            renewed = renew_lease(
                root,
                tx_id="TX-RENEW-1",
                event_id="EVT-RENEW-1",
                actor="agent-x",
                expected_custody_epoch=1,
                base_ref=base_ref,
                renewed_at=renewal_basis,
            )
            self.assertEqual("COMMITTED", renewed["status"])
            renewal_dt = datetime.fromisoformat(renewal_basis.replace("Z", "+00:00"))
            self.assertEqual(300, current_lease["custody"]["recovery_after_seconds"])
            early_observation = (renewal_dt + timedelta(minutes=4)).isoformat().replace("+00:00", "Z")
            eligible_observation = (renewal_dt + timedelta(minutes=6)).isoformat().replace("+00:00", "Z")

            with self.assertRaisesRegex(TransactionError, "RECOVERY_NOT_ELIGIBLE"):
                activate_lease(
                    root,
                    tx_id="TX-RECOVERY-EARLY",
                    event_id="EVT-RECOVERY-EARLY",
                    lease_id="LEASE-TA-011-03",
                    executor_id="agent-y",
                    actor="agent-y",
                    method="DETERMINISTIC",
                    qualification=None,
                    owner_basis=None,
                    branch=None,
                    base_ref=base_ref,
                    recovery_takeover=True,
                    expected_custody_epoch=1,
                    recovery_observed_at=early_observation,
                )

            recovered = activate_lease(
                root,
                tx_id="TX-RECOVERY-OK",
                event_id="EVT-RECOVERY-OK",
                lease_id="LEASE-TA-011-03",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                expected_custody_epoch=1,
                recovery_observed_at=eligible_observation,
            )
            self.assertEqual("COMMITTED", recovered["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual(2, state["execution"]["custody_epoch"])
            old = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            self.assertEqual("INVALIDATED", old["state"])

            stale = evaluate(
                root,
                "MATERIAL_WRITE",
                path=WRITE_PATH,
                base_ref=base_ref,
                expected_custody_epoch=1,
            )
            self.assertFalse(stale["allowed"], stale)
            self.assertIn("STALE_CUSTODY_EPOCH", stale["reason_codes"])

            reconstruction = record_recovery_reconstructed(
                root,
                tx_id="TX-RECOVERY-DONE",
                event_id="EVT-RECOVERY-DONE",
                actor="agent-y",
                evidence=["diff CP-TA-010..working-head reviewed", "returned offloads reclassified"],
                expected_custody_epoch=2,
            )
            self.assertEqual("COMMITTED", reconstruction["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("RECOVERY_STARTED", [row["type"] for row in events])
            self.assertIn("RECOVERY_RECONSTRUCTED", [row["type"] for row in events])

    def test_governed_activity_automatically_renews_current_executor_liveness(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            activate_lease(
                root,
                tx_id="TX-LIVE-START",
                event_id="EVT-LIVE-START",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            lease_path = root / "relay/LEASES/LEASE-TA-011-02.yaml"
            lease = load_yaml(lease_path)
            old = "2026-09-22T00:00:00Z"
            lease["custody"]["renewed_at"] = old
            dump(lease_path, lease)

            result = record_change_hypothesis(
                root,
                tx_id="TX-LIVE-ACTIVITY",
                event_id="EVT-LIVE-ACTIVITY",
                actor="agent-x",
                change_id="CHANGE-LIVE-001",
                statement="Governed engineering activity should renew current custody liveness.",
                basis=["current EP analysis"],
                expected_custody_epoch=1,
            )
            self.assertEqual("COMMITTED", result["status"])
            renewed = load_yaml(lease_path)
            self.assertGreater(
                datetime.fromisoformat(renewed["custody"]["renewed_at"].replace("Z", "+00:00")),
                datetime.fromisoformat(old.replace("Z", "+00:00")),
            )
            self.assertEqual(1, renewed["custody"]["epoch"])
            self.assertIn("activity_basis", renewed["custody"])

    def test_time_only_recovery_refuses_when_material_changed_since_last_activity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            activate_lease(
                root,
                tx_id="TX-MATERIAL-LIVE-START",
                event_id="EVT-MATERIAL-LIVE-START",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            lease = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            renewed = datetime.fromisoformat(
                lease["custody"]["renewed_at"].replace("Z", "+00:00")
            )
            material = root / "skills/engineering-pr-delivery-v3.1/scripts/base.py"
            material.write_text(
                material.read_text(encoding="utf-8") + "\n# unaccepted active material\n",
                encoding="utf-8",
            )
            expired = (renewed + timedelta(minutes=6)).isoformat().replace("+00:00", "Z")

            with self.assertRaisesRegex(
                TransactionError,
                "UNACCEPTED_MATERIAL_ACTIVITY_PRESENT",
            ):
                activate_lease(
                    root,
                    tx_id="TX-MATERIAL-LIVE-RECOVERY",
                    event_id="EVT-MATERIAL-LIVE-RECOVERY",
                    lease_id="LEASE-TA-011-03",
                    executor_id="agent-y",
                    actor="agent-y",
                    method="DETERMINISTIC",
                    qualification=None,
                    owner_basis=None,
                    branch=None,
                    base_ref=base_ref,
                    recovery_takeover=True,
                    expected_custody_epoch=1,
                    recovery_observed_at=expired,
                )

    def test_terminal_session_evidence_allows_immediate_fenced_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            activate_lease(
                root,
                tx_id="TX-SESSION-START",
                event_id="EVT-SESSION-START",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            old = load_yaml(root / "relay/LEASES/LEASE-TA-011-02.yaml")
            renewed = datetime.fromisoformat(
                old["custody"]["renewed_at"].replace("Z", "+00:00")
            )
            observation_time = (renewed + timedelta(minutes=1)).isoformat().replace("+00:00", "Z")
            recovery_observation = {
                "schema_version": "relay-v3.1-recovery-observation",
                "authority": "DERIVED_PROVIDER_OBSERVATION",
                "provider": "TEST_SESSION_PROVIDER",
                "provider_ref": "session://agent-x/run-1/terminated",
                "lease_id": "LEASE-TA-011-02",
                "executor_id": "agent-x",
                "custody_epoch": 1,
                "session_state": "TERMINATED",
                "observed_at": observation_time,
            }

            recovered = activate_lease(
                root,
                tx_id="TX-SESSION-RECOVERY",
                event_id="EVT-SESSION-RECOVERY",
                lease_id="LEASE-TA-011-03",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                expected_custody_epoch=1,
                recovery_observed_at=observation_time,
                recovery_observation=recovery_observation,
            )
            self.assertEqual("COMMITTED", recovered["status"])
            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual(2, state["execution"]["custody_epoch"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            started = [row for row in events if row["type"] == "RECOVERY_STARTED"][-1]
            self.assertEqual("TERMINAL_SESSION_CONFIRMED", started["details"]["recovery_reason"])
            self.assertTrue(started["details"]["terminal_observation_digest"])
            self.assertIn(
                "session://agent-x/run-1/terminated",
                started["basis"],
            )

    def test_handover_publication_requires_committed_plan(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            with self.assertRaisesRegex(TransactionError, "fresh HANDOVER_CONTEXT"):
                publish_handover(
                    root,
                    tx_id="TX-HANDOVER-PUBLISH-WITHOUT-PLAN",
                    event_id="EVT-HANDOVER-PUBLISH-WITHOUT-PLAN",
                    actor="agent-x",
                    base_ref=base_ref,
                )

    def test_handover_requires_plan_then_publish_before_successor_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            accept_current_checkpoint_and_reconcile(root, base_ref)
            plan_handover(
                root,
                tx_id="TX-HANDOVER-OFFER",
                event_id="EVT-HANDOVER-OFFER",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
            )

            with self.assertRaisesRegex(TransactionError, "fresh handover is unavailable"):
                activate_lease(
                    root,
                    tx_id="TX-HANDOVER-EARLY",
                    event_id="EVT-HANDOVER-EARLY",
                    lease_id="LEASE-TA-011-02",
                    executor_id="agent-y",
                    actor="agent-y",
                    method="DETERMINISTIC",
                    qualification=None,
                    owner_basis=None,
                    branch=None,
                    base_ref=base_ref,
                )

            published = publish_handover(
                root,
                tx_id="TX-HANDOVER-PUBLISH",
                event_id="EVT-HANDOVER-PUBLISH",
                actor="agent-x",
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", published["status"])

            result = activate_lease(
                root,
                tx_id="TX-HANDOVER-ACCEPT",
                event_id="EVT-HANDOVER-ACCEPT",
                lease_id="LEASE-TA-011-02",
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", result["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            published_events = [row for row in events if row["type"] == "HANDOVER_PUBLISHED"]
            accepted = [row for row in events if row["type"] == "HANDOVER_ACCEPTED"]
            self.assertEqual(1, len(published_events))
            self.assertEqual(1, len(accepted))
            self.assertEqual("LEASE-TA-011-02", accepted[0]["subject"])
            granted = [row for row in events if row["event_id"] == "EVT-HANDOVER-ACCEPT"][0]
            self.assertEqual("HANDOFF", granted["details"]["continuation"])

    def test_confirmed_change_delta_cannot_reconcile_roadmap_before_owner_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            record_change_hypothesis(
                root,
                tx_id="TX-CHANGE-REC",
                event_id="EVT-CHANGE-REC",
                actor="agent-x",
                change_id="CHANGE-014",
                statement="The current work package framing should be updated.",
                basis=["Prompt 1 independent reasoning", "relay/ROADMAP/ROADMAP.yaml"],
            )
            verify_change_delta(
                root,
                tx_id="TX-CHANGE-VERIFY",
                event_id="EVT-CHANGE-VERIFY",
                actor="agent-x",
                change_id="CHANGE-014",
                status="CONFIRMED",
                evidence=["src/example.py proves the current boundary"],
                falsifiers_checked=["No independent ownership split is required."],
            )

            proposal = {
                "disposition": "UPDATE",
                "source": {"work_package": "WP-TA-109", "parent_issue": None},
                "retain": {"acceptance": ["AC-1"]},
                "transfer": {},
                "proposed_target": None,
                "rationale": "The same work identity remains correct but its framing should improve.",
            }
            proposal_path = root / "proposal.yaml"
            dump(proposal_path, proposal)
            propose_change_delta(
                root,
                tx_id="TX-CHANGE-PROPOSE",
                event_id="EVT-CHANGE-PROPOSE",
                actor="agent-x",
                change_id="CHANGE-014",
                proposal_path=proposal_path,
                authorization_required="OWNER",
            )

            state = load_yaml(root / "relay/STATE.yaml")
            roadmap_path = root / state["roadmap"]["path"]
            roadmap = load_yaml(roadmap_path)
            after = copy.deepcopy(roadmap)
            after["revision"] = "RM-0013"
            current_wp = [row for row in after["work_packages"] if row["id"] == "WP-TA-109"][0]
            current_wp["title"] = "Current work — verified improved framing"
            reconciliation = {
                "schema_version": "relay-v3.1-roadmap-reconciliation",
                "authority": "PROPOSED_RECONCILIATION",
                "expected_revision": "RM-0012",
                "disposition": "UPDATE_WORK_PACKAGE",
                "basis": ["CHANGE-014 verified"],
                "roadmap_after": after,
            }
            reconciliation_path = root / "roadmap-reconciliation.yaml"
            dump(reconciliation_path, reconciliation)
            change_path = root / "relay/CHANGES/CHANGE-014.yaml"

            with self.assertRaisesRegex(TransactionError, "requires granted Owner authority"):
                reconcile_roadmap(
                    root,
                    tx_id="TX-CHANGE-APPLY-DENIED",
                    event_id="EVT-CHANGE-APPLY-DENIED",
                    actor="agent-x",
                    reconciliation_path=reconciliation_path,
                    base_ref=base_ref,
                    change_delta_path=change_path,
                )

            authorize_change_delta(
                root,
                tx_id="TX-CHANGE-AUTH",
                event_id="EVT-CHANGE-AUTH",
                actor="owner",
                change_id="CHANGE-014",
                granted=True,
                direct_utterance_digest=DIGEST,
                session_timestamp="2026-09-22T16:00:00Z",
            )
            applied = reconcile_roadmap(
                root,
                tx_id="TX-CHANGE-APPLY",
                event_id="EVT-CHANGE-APPLY",
                actor="agent-x",
                reconciliation_path=reconciliation_path,
                base_ref=base_ref,
                change_delta_path=change_path,
            )
            self.assertEqual("COMMITTED", applied["status"])
            delta = load_yaml(change_path)
            self.assertEqual("APPLIED", delta["application"]["status"])
            self.assertEqual("RM-0012", delta["application"]["roadmap_before"])
            self.assertEqual("RM-0013", delta["application"]["roadmap_after"])
            self.assertEqual([], validate(root))


if __name__ == "__main__":
    unittest.main()
