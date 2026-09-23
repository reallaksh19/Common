from __future__ import annotations

import shutil
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

from intelligence_projection import build_improvement, build_task
from programme_reconciliation import assess_boundary, require_boundary_ready
from relay_can import evaluate
from relay_tx import activate_lease, record_recovery_reconstructed
from snapshot_projection import build as build_snapshot
from test_handover_context import install_parent_issue, parent_issue_observation
from test_relay_can import WRITE_PATH, prepare_git
from v3lib import load_events, load_yaml
from validate_foundation import validate, validate_authority


class ArchitecturePreservationTests(unittest.TestCase):
    def test_generated_state_can_be_destroyed_and_reconstructed_from_durable_truth(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            before_snapshot = build_snapshot(root, base_ref)
            before_task = build_task(root, base_ref)
            before_improvement = build_improvement(root)
            before_write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(before_write["allowed"], before_write)

            generated = root / "relay/GENERATED"
            shutil.rmtree(generated)

            # Generated read models are disposable. Their loss may make the full
            # repository projection incomplete, but durable authority remains valid
            # and synchronous authorization must not depend on them.
            self.assertEqual([], validate_authority(root))
            conformance_errors = validate(root)
            self.assertTrue(
                any("SNAPSHOT: cannot load" in item for item in conformance_errors),
                conformance_errors,
            )

            after_write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertEqual(before_write["allowed"], after_write["allowed"])
            self.assertEqual(before_write["reason_codes"], after_write["reason_codes"])

            after_snapshot = build_snapshot(root, base_ref)
            after_task = build_task(root, base_ref)
            after_improvement = build_improvement(root)

            # Reconstructed programme, custody, evidence and task truth are stable.
            for key in ("owner", "programme", "execution", "scope", "evidence", "controls", "delivery", "next"):
                self.assertEqual(before_snapshot[key], after_snapshot[key], key)
            for key in ("identity", "purpose", "lineage", "scope", "execution", "acceptance", "knowledge_state", "preserve", "next"):
                self.assertEqual(before_task[key], after_task[key], key)
            for key in ("task", "checkpoint", "from", "to", "improvement", "roadmap_effect", "still_not_proved"):
                self.assertEqual(before_improvement[key], after_improvement[key], key)

            state = load_yaml(root / "relay/STATE.yaml")
            snapshot_path = root / str((state.get("generated") or {}).get("snapshot"))
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            import yaml
            snapshot_path.write_text(
                yaml.safe_dump(after_snapshot, sort_keys=False),
                encoding="utf-8",
            )
            self.assertEqual([], validate(root))

    def test_zero_context_successor_reconstructs_and_takes_fenced_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            baseline = install_parent_issue(root, number=1771)
            live_parent = parent_issue_observation(
                baseline=baseline,
                number=1771,
                state="OPEN",
                disposition="NO_CHANGE",
                acceptance_state="PENDING",
            )

            started = activate_lease(
                root,
                tx_id=None,
                event_id=None,
                lease_id=None,
                executor_id="agent-x",
                actor="agent-x",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
            )
            self.assertEqual("COMMITTED", started["status"])
            self.assertEqual("TX.1771.1", started["id"])
            state = load_yaml(root / "relay/STATE.yaml")
            predecessor_id = state["execution"]["lease"]
            self.assertEqual("LEASE.1771.1", predecessor_id)
            predecessor = load_yaml(root / "relay/LEASES" / f"{predecessor_id}.yaml")
            renewed_at = datetime.fromisoformat(
                predecessor["custody"]["renewed_at"].replace("Z", "+00:00")
            )

            shutil.rmtree(root / "relay/GENERATED")

            reconstructed_snapshot = build_snapshot(root, base_ref)
            reconstructed_task = build_task(root, base_ref, live_parent)
            assessment = require_boundary_ready(
                assess_boundary(
                    reconstructed_task.get("parent_issue"),
                    [live_parent],
                    boundary="RECOVERY_TAKEOVER",
                    selected_frontier_ref="example/project#1771",
                )
            )

            self.assertEqual("READY", assessment["status"])
            self.assertEqual("CONTINUE_CURRENT", assessment["continuation"])
            self.assertEqual(
                "example/project#1771",
                assessment["executable_frontier"],
            )
            self.assertEqual(
                "EP-TA-011",
                reconstructed_snapshot["execution"]["ep"],
            )
            self.assertEqual(
                "CP-TA-010",
                reconstructed_snapshot["evidence"]["latest_checkpoint"],
            )
            self.assertIn(
                "WP-TA-109",
                reconstructed_snapshot["programme"]["remaining_work"],
            )
            self.assertTrue(
                (reconstructed_task.get("next") or {}).get("immediate_action")
            )

            recovered_at = (renewed_at + timedelta(minutes=6)).isoformat().replace(
                "+00:00",
                "Z",
            )
            recovered = activate_lease(
                root,
                tx_id=None,
                event_id=None,
                lease_id=None,
                executor_id="agent-y",
                actor="agent-y",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=base_ref,
                recovery_takeover=True,
                expected_custody_epoch=1,
                recovery_observed_at=recovered_at,
                programme_issue_observations=[live_parent],
                selected_programme_ref="example/project#1771",
            )
            self.assertEqual("COMMITTED", recovered["status"])
            self.assertEqual("TX.1771.2", recovered["id"])

            state = load_yaml(root / "relay/STATE.yaml")
            self.assertEqual(2, state["execution"]["custody_epoch"])
            self.assertEqual("LEASE.1771.2", state["execution"]["lease"])
            old_lease = load_yaml(root / "relay/LEASES" / f"{predecessor_id}.yaml")
            self.assertEqual("INVALIDATED", old_lease["state"])

            stale = evaluate(
                root,
                "MATERIAL_WRITE",
                path=WRITE_PATH,
                base_ref=base_ref,
                expected_custody_epoch=1,
            )
            self.assertFalse(stale["allowed"], stale)
            self.assertIn("STALE_CUSTODY_EPOCH", stale["reason_codes"])

            reconstructed = record_recovery_reconstructed(
                root,
                tx_id="TX-PRESERVE-RECOVERY-DONE",
                event_id="EVT-PRESERVE-RECOVERY-DONE",
                actor="agent-y",
                evidence=[
                    "programme frontier reconstructed from durable authority + provider observation",
                    "generated state absent before fenced recovery",
                ],
                expected_custody_epoch=2,
            )
            self.assertEqual("COMMITTED", reconstructed["status"])
            events, errors = load_events(root / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("RECOVERY_STARTED", [row["type"] for row in events])
            self.assertIn("RECOVERY_RECONSTRUCTED", [row["type"] for row in events])
            canonical_event_ids = [
                row["event_id"] for row in events if str(row["event_id"]).startswith("EVT.1771.")
            ]
            self.assertEqual(
                ["EVT.1771.1", "EVT.1771.2", "EVT.1771.3", "EVT.1771.4", "EVT.1771.5"],
                canonical_event_ids,
            )

    def test_generated_snapshot_cannot_grant_authority_missing_from_durable_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            state_path = root / "relay/STATE.yaml"
            state = load_yaml(state_path)
            state["execution"] = {
                "lifecycle": "IDLE",
                "ep": None,
                "lease": None,
                "route": None,
            }
            import yaml
            state_path.write_text(yaml.safe_dump(state, sort_keys=False), encoding="utf-8")

            # Leave the generated snapshot untouched: it still claims ACTIVE.
            denied = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertFalse(denied["allowed"], denied)
            self.assertIn("NO_ACTIVE_EXECUTION", denied["reason_codes"])
            self.assertIn("NO_ACTIVE_LEASE", denied["reason_codes"])

    def test_preservation_contract_keeps_execution_safety_outside_provider_projection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)

            # Provider/read-model absence is coordination quality, not execution
            # authority. Product writes remain governed by durable custody, scope
            # and material drift only.
            for name in (
                "HANDOVER_CONTEXT.yaml",
                "HANDOVER_LEDGER.yaml",
                "HANDOVER_PROVIDER_STATUS.yaml",
                "PARENT_RELAY_SUMMARY.md",
                "TASK_SNAPSHOT.yaml",
                "IMPROVEMENT_VIEW.yaml",
            ):
                path = root / "relay/GENERATED" / name
                if path.exists():
                    path.unlink()

            allowed = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref=base_ref)
            self.assertTrue(allowed["allowed"], allowed)


if __name__ == "__main__":
    unittest.main()
