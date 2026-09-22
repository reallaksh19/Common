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

from plan_handover import plan_handover
from relay_can import evaluate
from relay_tx import (
    activate_lease,
    authorize_change_delta,
    propose_change_delta,
    reconcile_roadmap,
    record_change_hypothesis,
    record_recovery_reconstructed,
    renew_lease,
    verify_change_delta,
)
from test_handover_context import install_standalone, target_observation
from test_relay_can import WRITE_PATH, prepare_git
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

            renewed = renew_lease(
                root,
                tx_id="TX-RENEW-1",
                event_id="EVT-RENEW-1",
                actor="agent-x",
                expected_custody_epoch=1,
                base_ref=base_ref,
                renewed_at="2026-09-22T00:00:00Z",
            )
            self.assertEqual("COMMITTED", renewed["status"])

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
                    recovery_observed_at="2026-09-22T00:30:00Z",
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
                recovery_observed_at="2026-09-22T01:01:00Z",
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

    def test_fresh_handover_is_accepted_by_successor_not_merely_published(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            install_standalone(root)
            state = load_yaml(root / "relay/STATE.yaml")
            roadmap = load_yaml(root / state["roadmap"]["path"])
            reconciliation = {
                "schema_version": "relay-v3.1-roadmap-reconciliation",
                "authority": "PROPOSED_RECONCILIATION",
                "expected_revision": roadmap["revision"],
                "disposition": "NO_CHANGE",
                "basis": ["No roadmap concept change is required for this clean handover."],
                "roadmap_after": roadmap,
            }
            reconciliation_path = root / "handover-roadmap-reconciliation.yaml"
            dump(reconciliation_path, reconciliation)
            reconcile_roadmap(
                root,
                tx_id="TX-HANDOVER-ROADMAP",
                event_id="EVT-HANDOVER-ROADMAP",
                actor="agent-x",
                reconciliation_path=reconciliation_path,
                base_ref=base_ref,
            )
            plan_handover(
                root,
                tx_id="TX-HANDOVER-OFFER",
                event_id="EVT-HANDOVER-OFFER",
                actor="agent-x",
                target_path=target_observation(root),
                base_ref=base_ref,
                complex_mode=False,
            )

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
            accepted = [row for row in events if row["type"] == "HANDOVER_ACCEPTED"]
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
