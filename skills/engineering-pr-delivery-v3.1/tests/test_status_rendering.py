from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from render_owner_status import render


def snapshot() -> dict:
    return {
        "schema_version": "relay-v3.1-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "generated_from": {"roadmap_revision": "RM-2"},
        "programme": {
            "programme_progress": 75,
            "accepted_progress": 40,
            "completed_work": ["WP-1"],
            "remaining_work": ["WP-2"],
            "evidence_backed_work": ["WP-1"],
        },
        "execution": {
            "lifecycle": "ACTIVE",
            "work_package": "WP-2",
            "ep": "EP-2",
            "lease": "LEASE.438.1",
            "custody_epoch": 2,
            "executor": "agent-a",
        },
        "evidence": {
            "latest_checkpoint": "CP-1",
            "latest_material_validation": {"result": "PASS"},
        },
        "controls": {
            "execution_blockers": [],
            "handover_blockers": ["CTRL-HO"],
            "delivery_blockers": [],
            "informational": ["CTRL-INFO"],
        },
        "delivery": {
            "pr": "#437",
            "issue": "#438",
            "lifecycle": "OPEN",
            "merge_authorized": False,
        },
        "next": {
            "immediate_material_action": "Validate.",
            "delivery_action": "none",
            "stop_conditions": ["relevant drift"],
        },
        "owner": {
            "outcome": "Ship safely.",
            "current_goal": "Validate current work.",
        },
        "handoff": {
            "zero_context_takeover_possible": True,
            "reconstruction_sources": ["relay/STATE.yaml", "relay/EVENTS.jsonl"],
        },
    }


def task_snapshot() -> dict:
    return {
        "schema_version": "relay-v3.1-task-snapshot",
        "authority": "DERIVED_READ_MODEL",
        "source_protocol": "V3_1",
        "identity": {"work_package": "WP-2", "ep": "EP-2"},
        "purpose": {"task_outcome": "Preserve completion semantics."},
        "programme_parent": {
            "repository": "example/repo",
            "number": 210,
            "title": "Programme",
            "url": "https://github.com/example/repo/issues/210",
        },
        "planning": {
            "state": "PRESENT",
            "provider_ref": "github:example/repo#232/comment-1",
            "revision": 1,
            "digest": "sha256:" + ("a" * 64),
            "observed_at": "2026-09-24T03:00:00Z",
            "expected_next_observable": {
                "statement": "Focused exact-head validation.",
                "evidence": ["test result"],
            },
        },
        "task_publications": [
            {
                "type": "IMPLEMENTATION_PLAN",
                "ref": "github:example/repo#232/comment-1",
                "observed_at": "2026-09-24T03:00:00Z",
                "summary": "Plan published.",
                "exact_head": None,
            }
        ],
        "current_task_progress": {
            "summary": {
                "complete": 6,
                "partial": 0,
                "pending": 2,
                "blocked": 0,
                "total": 8,
            }
        },
        "parent_issue_progress": {
            "summary": {
                "complete": 9,
                "partial": 1,
                "pending": 2,
                "blocked": 0,
                "deferred": 1,
                "not_applicable": 0,
                "unknown": 0,
                "total": 13,
            }
        },
        "offloads": [{"id": "OFFLOAD.438.1"}],
        "pending_items": [{"id": "PEND.438.1"}],
        "known_issues": [{"id": "KI.438.1"}],
        "next": {
            "immediate_action": "Complete the two pending criteria.",
            "next_value_frontier": "Issue-rooted serialization",
            "stop_conditions": ["programme reselection"],
        },
        "reconstruction_sources": ["relay/WORK/EP-2.yaml"],
    }


def improvement_view() -> dict:
    return {
        "schema_version": "relay-v3.1-improvement-view",
        "authority": "DERIVED_READ_MODEL",
        "source_protocol": "V3_1",
        "improvement": {
            "capability_added": [],
            "capability_strengthened": ["signed PDF warning"],
            "evidence_added": ["test PASS"],
            "understanding_improved": ["rewrite risk clarified"],
            "downstream_unlocked": [],
            "controls_resolved": [],
            "controls_created": [],
        },
        "roadmap_effect": {
            "concept_change": "NO_CONCEPT_CHANGE",
            "execution_disposition": "CONTINUE",
            "roadmap_revision": "RM-2",
        },
        "not_improved": ["merge authority"],
        "still_not_proved": ["local exact-head validation"],
        "new_questions": [],
        "reconstruction_sources": ["relay/CHECKPOINTS/CP-1.yaml"],
    }


class OwnerStatusRenderingTests(unittest.TestCase):
    def test_completion_report_keeps_programme_evidence_and_task_progress_distinct(self):
        text = render(snapshot(), task_snapshot(), improvement_view())
        self.assertIn("Authority: **DERIVED_READ_MODEL**", text)
        self.assertIn("Programme progress: **75%**", text)
        self.assertIn("Accepted evidence coverage: **40%**", text)
        self.assertIn("complete=6", text)
        self.assertIn("total=13", text)
        self.assertIn("Pending tracked items: 1", text)
        self.assertIn("Known issues: 1", text)
        self.assertIn("Capability strengthened: signed PDF warning", text)
        self.assertIn("Still not proved: local exact-head validation", text)
        self.assertIn("Handover diagnostics: CTRL-HO", text)
        self.assertIn("Task stop conditions: programme reselection", text)
        self.assertIn("Implementation plan: **PRESENT** rev 1", text)
        self.assertIn("Expected next observable: Focused exact-head validation.", text)
        self.assertIn("Programme parent: example/repo#210", text)
        self.assertIn("Task publications: 1", text)
        self.assertIn("Zero-context takeover possible: **YES**", text)

    def test_completion_report_rejects_non_derived_inputs(self):
        bad = snapshot()
        bad["authority"] = "AUTHORITATIVE"
        with self.assertRaisesRegex(ValueError, "DERIVED_READ_MODEL"):
            render(bad, task_snapshot(), improvement_view())

    def test_completion_report_rejects_wrong_read_model_kind(self):
        task = task_snapshot()
        task["schema_version"] = "relay-v3.1-snapshot"
        with self.assertRaisesRegex(ValueError, "relay-v3.1-task-snapshot"):
            render(snapshot(), task, improvement_view())


if __name__ == "__main__":
    unittest.main()
