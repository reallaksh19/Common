from __future__ import annotations

import unittest

from render_owner_status import render


class OwnerStatusRenderingTests(unittest.TestCase):
    def test_existing_quantitative_views_are_rendered_without_new_authority(self):
        snapshot = {
            "generated_from": {"roadmap_revision": "RM-2"},
            "programme": {"accepted_progress": 40},
            "execution": {"lifecycle": "ACTIVE", "work_package": "WP-2", "ep": "EP-2", "lease": "LEASE-2", "executor": "agent-a"},
            "controls": {"execution_blockers": [], "handover_blockers": [], "delivery_blockers": [], "informational": []},
            "delivery": {"pr": "#1", "issue": "#2", "lifecycle": "OPEN", "merge_authorized": False},
            "next": {"immediate_material_action": "Validate.", "delivery_action": "none"},
            "owner": {"outcome": "Ship safely.", "current_goal": "Validate current work."},
        }
        task = {
            "current_task_progress": {"summary": {"complete": 6, "partial": 0, "pending": 2, "blocked": 0, "total": 8}},
            "parent_issue_progress": {"summary": {"complete": 9, "partial": 1, "pending": 2, "blocked": 0, "deferred": 0, "not_applicable": 0, "unknown": 0, "total": 12}},
            "pending_items": [],
            "known_issues": [],
        }
        improvement = {
            "improvement": {
                "capability_added": [],
                "capability_strengthened": ["signed PDF warning"],
                "evidence_added": ["test PASS"],
                "understanding_improved": ["rewrite risk clarified"],
                "downstream_unlocked": [],
            },
            "still_not_proved": ["local exact-head validation"],
            "new_questions": [],
        }
        text = render(snapshot, task, improvement)
        self.assertIn("complete=6", text)
        self.assertIn("total=12", text)
        self.assertIn("Capability strengthened: 1", text)
        self.assertIn("Still not proved: 1", text)


if __name__ == "__main__":
    unittest.main()
