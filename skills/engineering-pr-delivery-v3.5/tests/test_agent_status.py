from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_status import render
from v3lib import validate_schema


def sample() -> dict:
    return {
        "schema_version": "relay-v3.1-agent-status",
        "authority": "DERIVED_EXECUTION_CONTINUITY",
        "marker": "AGENT_STATUS_V1",
        "agent": {
            "executor": "primary-agent",
            "custody_epoch": 2,
            "continuation": "RECOVERY",
            "status": "ACTIVE",
        },
        "protocol_basis": {
            "protocol": "V3.1",
            "common_sha": "a" * 40,
            "two_pass_revision": "TPG-2P-2026-09-28-R3",
        },
        "responsibility": {"issue": 477, "ep": "EP-477", "work_package": "WP-477"},
        "plan": {
            "implementation_plan": "github:example/repo#477/comment-plan",
            "plan_revision": 2,
            "latest_plan_update": "github:example/repo#477/comment-plan-update",
            "latest_task_evidence": None,
            "latest_task_result": None,
        },
        "material": {
            "branch": "issue-477/v31-intent-provenance-authoring",
            "primary_pr": 478,
            "base": "base-sha",
            "head": "head-sha",
        },
        "current": "Finish execution-continuity indexing without changing task authority.",
        "completed": [
            {
                "id": "STEP-477-06",
                "statement": "AGENT_STATUS_V1 contract exists.",
                "evidence": ["PR #478"],
            }
        ],
        "further_tasks": [
            {
                "id": "FT-477-1",
                "state": "ACTIVE",
                "statement": "Project continuity into Task Snapshot/Handover.",
                "depends_on": "STEP-477-06",
                "unblock_condition": None,
                "expected_evidence": "continuity projection regression",
                "target": "PR #478",
                "evidence": [],
                "reason_class": "CURRENT_TASK",
            }
        ],
        "pending_items": [],
        "reasoning_refs": ["CX-477-01"],
        "offloads": [],
        "rll": {
            "transport": "NONE",
            "state": "NOT_ACTIVE",
            "execution_ref": None,
            "worker_state_ref": None,
            "engineering_result": "NOT_RUN",
        },
        "delivery": {
            "lifecycle": "DRAFT",
            "relationship": "PRIMARY",
            "related_prs": [
                {
                    "pr": 478,
                    "relationship": "PRIMARY",
                    "lifecycle": "DRAFT",
                    "head": "head-sha",
                }
            ],
        },
        "handover": {
            "predecessor_status_ref": "github:example/repo#477/comment-old-status",
            "successor_first_action": [
                "Refresh live V3.1.",
                "Revalidate FT-477-1 against current PR/head.",
            ],
        },
        "negative_knowledge": [
            "AGENT_STATUS_V1 is not task authority.",
            "RLL transport is not engineering PASS.",
        ],
        "updated_at": "2026-09-28T11:30:00Z",
    }


class AgentStatusTests(unittest.TestCase):
    def test_schema_and_render(self):
        value = sample()
        self.assertEqual([], validate_schema("agent-status", value, "agent-status"))
        text = render(value)
        self.assertTrue(text.startswith("AGENT_STATUS_V1\n"))
        self.assertIn("AUTHORITY: DERIVED_EXECUTION_CONTINUITY", text)
        self.assertIn("custody_epoch: 2", text)
        self.assertIn("continuation: RECOVERY", text)
        self.assertIn("FT-477-1", text)
        self.assertIn("predecessor_status_ref:", text)

    def test_ft_is_continuity_not_required_when_complete(self):
        value = sample()
        value["agent"]["status"] = "COMPLETE"
        value["further_tasks"] = []
        self.assertEqual([], validate_schema("agent-status", value, "agent-status-complete"))
        text = render(value)
        self.assertIn("None within this responsibility.", text)

    def test_invalid_ft_identity_fails(self):
        value = sample()
        value["further_tasks"][0]["id"] = "EP-477"
        errors = validate_schema("agent-status", value, "agent-status-invalid-ft")
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
