from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from render_owner_stats import render


class OwnerStatsTests(unittest.TestCase):
    def test_stats_are_pointwise_and_separate_programme_categories(self):
        snapshot = {
            "generated_from": {"roadmap_revision": "RM-1"},
            "owner": {"outcome": "Outcome", "current_goal": "Goal"},
            "programme": {"programme_progress": 60.0, "accepted_progress": 40.0},
            "execution": {"ep": "EP-1", "lease": "LEASE-1"},
            "evidence": {"latest_checkpoint": "CP-1"},
            "material": {"head": "abc1234"},
            "next": {"immediate_material_action": "Implement X", "delivery_action": "Update PR"},
        }
        task = {
            "parent_issue_progress": {
                "checklist": [
                    {"id": "P-1", "statement": "Done item", "state": "COMPLETE", "evidence": ["issue#1"]},
                    {"id": "P-2", "statement": "Blocked item", "state": "BLOCKED", "evidence": []},
                ]
            },
            "current_task_progress": {
                "checklist": [
                    {"id": "AC-1", "statement": "Task criterion", "state": "PENDING", "evidence": []},
                ]
            },
            "pending_items": [{"id": "PEND-1", "status": "OPEN", "statement": "Pending evidence"}],
            "known_issues": [{"id": "KI-1", "status": "OPEN", "statement": "Known limitation"}],
            "offloads": [{"id": "OFFLOAD-1", "status": "ACTIVE", "task": "Run local suite"}],
        }
        reconciliation = {
            "parents": [
                {"ref": "example/project#10", "title": "Completed parent", "ownership": "LANDED"},
                {"ref": "example/project#11", "title": "Live child", "ownership": "STILL_REAL"},
                {"ref": "example/project#12", "title": "Deferred child", "ownership": "DEFERRED"},
            ],
            "programme_frontier": ["example/project#11"],
            "execution_blocked": [],
            "acceptance_debt": [],
            "delivery_governance_debt": ["example/project#10"],
            "deferred_or_future": ["example/project#12"],
        }
        ledger = {
            "ep_index": [
                {
                    "ep": "EP-1",
                    "work_package": "WP-1",
                    "status": "ACTIVE",
                    "continuation": "CURRENT",
                    "checkpoint": "CP-1",
                    "lease": "LEASE-1",
                }
            ],
            "accepted_truth": {"checkpoint": "CP-1", "accepted_head": "abc1234"},
            "material": {"working_head": "def5678", "status": "UNACCEPTED_DELTA_PRESENT"},
        }

        text = render(snapshot, task, reconciliation, ledger)
        self.assertIn("# Engineering Relay V3.1 — Detailed Stats", text)
        self.assertIn("## Parent / sub-issue programme set", text)
        self.assertIn("[x] **example/project#10** — LANDED", text)
        self.assertIn("[ ] **example/project#11** — STILL_REAL", text)
        self.assertIn("[-] **example/project#12** — DEFERRED", text)
        self.assertIn("[!] **P-2** — BLOCKED", text)
        self.assertIn("Programme frontier: ['example/project#11']", text)
        self.assertIn("Delivery / governance debt: ['example/project#10']", text)
        self.assertIn("UNACCEPTED_DELTA_PRESENT", text)


if __name__ == "__main__":
    unittest.main()
