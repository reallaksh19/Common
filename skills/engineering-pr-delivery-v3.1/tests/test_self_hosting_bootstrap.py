from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = SKILL_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from nomenclature import allocate_next_id
from programme_reconciliation import assess_boundary, require_boundary_ready
from protocol_default import resolve as resolve_protocol
from relay_can import evaluate
from relay_tx import activate_lease
from snapshot_projection import build as build_snapshot
from validate_foundation import validate, validate_authority
from v3lib import load_events, load_yaml


BASE = "93f480c5578885d71c9fefbdc2912c7b76945051"
ISSUE_REF = "reallaksh19/Common#438"
WRITE_PATH = "skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py"


def provider_observation(ep: dict) -> dict:
    parent = ep["parent_issue"]
    baseline = parent["baseline"]
    return {
        "schema_version": "relay-v3.1-parent-issue-observation",
        "authority": "DERIVED_PROVIDER_OBSERVATION",
        "provider": "GITHUB",
        "repository": parent["repository"],
        "issue_number": parent["number"],
        "title": parent["title"],
        "url": parent["url"],
        "state": "OPEN",
        "observed_at": "2026-09-23T09:45:00Z",
        "baseline": baseline,
        "current_contract": {
            "body_digest": baseline["body_digest"],
            "acceptance_items": [
                {
                    "id": item["id"],
                    "statement": item["statement"],
                    "state": "PENDING",
                    "evidence": [],
                    "provider_refs": ["Common#438"],
                }
                for item in baseline["acceptance_items"]
            ],
        },
        "updates": [],
        "disposition": "NO_CHANGE",
        "relationships": [],
        "handover_ledger": None,
    }


class SelfHostingBootstrapTests(unittest.TestCase):
    def test_live_common_authority_is_native_and_valid(self):
        protocol = resolve_protocol(REPO_ROOT)
        self.assertEqual("NATIVE", protocol["authority_mode"])
        self.assertEqual("ACTIVE", protocol["status"])
        self.assertEqual([], validate(REPO_ROOT))

        roadmap = load_yaml(REPO_ROOT / "relay/ROADMAP/ROADMAP.yaml")
        state = load_yaml(REPO_ROOT / "relay/STATE.yaml")
        ep = load_yaml(REPO_ROOT / "relay/WORK/EP.438.1.yaml")
        lease = load_yaml(REPO_ROOT / "relay/LEASES/LEASE.438.1.yaml")
        events, errors = load_events(REPO_ROOT / "relay/EVENTS.jsonl")

        self.assertEqual([], errors)
        self.assertEqual("WP.438", roadmap["work_packages"][0]["id"])
        self.assertEqual("ACTIVE", roadmap["work_packages"][0]["state"])
        self.assertEqual("EP.438.1", state["execution"]["ep"])
        self.assertEqual("LEASE.438.1", state["execution"]["lease"])
        self.assertEqual(1, state["execution"]["custody_epoch"])
        self.assertEqual("WP.438", ep["work_package"])
        self.assertEqual("LEASE.438.1", lease["id"])
        self.assertEqual("PROVENANCE_ONLY", events[0]["details"]["pre_bootstrap_history"])
        self.assertEqual("NONE", events[0]["details"]["historical_execution_authority"])
        self.assertFalse((REPO_ROOT / "relay/WORK/EP.438.0.yaml").exists())

    def test_live_authority_survives_generated_deletion_and_fenced_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            clone = Path(td) / "common"
            head = subprocess.check_output(
                ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
                text=True,
            ).strip()
            subprocess.check_call(
                ["git", "clone", "--quiet", "--no-hardlinks", str(REPO_ROOT), str(clone)]
            )
            subprocess.check_call(
                ["git", "-C", str(clone), "checkout", "--quiet", "--detach", head]
            )

            shutil.rmtree(clone / "relay/GENERATED")
            self.assertEqual([], validate_authority(clone))

            state = load_yaml(clone / "relay/STATE.yaml")
            ep = load_yaml(clone / "relay/WORK/EP.438.1.yaml")
            predecessor = load_yaml(clone / "relay/LEASES/LEASE.438.1.yaml")
            observation = provider_observation(ep)

            reconstructed = build_snapshot(clone, BASE)
            self.assertEqual("EP.438.1", reconstructed["execution"]["ep"])
            self.assertEqual("LEASE.438.1", reconstructed["execution"]["lease"])
            self.assertEqual(1, reconstructed["execution"]["custody_epoch"])
            self.assertEqual(["WP.438"], reconstructed["programme"]["remaining_work"])
            controls = load_yaml(clone / "relay/CONTROLS/controls.yaml")
            bootstrap_control = next(
                row
                for row in controls["controls"]
                if row["id"] == "CTRL-SELFHOST-438-001"
            )
            self.assertEqual("RESOLVED", bootstrap_control["state"])
            self.assertNotIn(
                "CTRL-SELFHOST-438-001",
                reconstructed["controls"]["execution_blockers"],
            )
            self.assertTrue(reconstructed["handoff"]["zero_context_takeover_possible"])
            self.assertTrue(reconstructed["next"]["immediate_material_action"])

            assessment = require_boundary_ready(
                assess_boundary(
                    ep["parent_issue"],
                    [observation],
                    boundary="RECOVERY_TAKEOVER",
                    selected_frontier_ref=ISSUE_REF,
                )
            )
            self.assertEqual("READY", assessment["status"])
            self.assertEqual("CONTINUE_CURRENT", assessment["continuation"])
            self.assertEqual(ISSUE_REF, assessment["executable_frontier"])

            renewed = datetime.fromisoformat(
                predecessor["custody"]["renewed_at"].replace("Z", "+00:00")
            )
            recovered_at = (
                renewed
                + timedelta(
                    seconds=int(predecessor["custody"]["recovery_after_seconds"]) + 1
                )
            ).isoformat().replace("+00:00", "Z")

            expected_tx_id = allocate_next_id(
                clone,
                kind="TX",
                root=438,
            )
            recovered = activate_lease(
                clone,
                tx_id=None,
                event_id=None,
                lease_id=None,
                executor_id="successor-agent",
                actor="successor-agent",
                method="DETERMINISTIC",
                qualification=None,
                owner_basis=None,
                branch=None,
                base_ref=BASE,
                recovery_takeover=True,
                expected_custody_epoch=1,
                recovery_observed_at=recovered_at,
                programme_issue_observations=[observation],
                selected_programme_ref=ISSUE_REF,
            )
            self.assertEqual("COMMITTED", recovered["status"])
            self.assertEqual(expected_tx_id, recovered["id"])

            state = load_yaml(clone / "relay/STATE.yaml")
            self.assertEqual(2, state["execution"]["custody_epoch"])
            self.assertEqual("LEASE.438.2", state["execution"]["lease"])
            old = load_yaml(clone / "relay/LEASES/LEASE.438.1.yaml")
            self.assertEqual("INVALIDATED", old["state"])

            stale = evaluate(
                clone,
                "MATERIAL_WRITE",
                path=WRITE_PATH,
                base_ref=BASE,
                expected_custody_epoch=1,
            )
            self.assertFalse(stale["allowed"], stale)
            self.assertIn("STALE_CUSTODY_EPOCH", stale["reason_codes"])

            events, errors = load_events(clone / "relay/EVENTS.jsonl")
            self.assertEqual([], errors)
            self.assertIn("RECOVERY_STARTED", [row["type"] for row in events])
            self.assertTrue(
                any(str(row["event_id"]).startswith("EVT.438.") for row in events)
            )


if __name__ == "__main__":
    unittest.main()
