#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
SKILL = HERE.parents[1]
SCRIPTS = SKILL / "scripts"
EXAMPLES = SKILL / "examples" / "task-snapshot"
sys.path.insert(0, str(SCRIPTS))

from render_task_snapshot import render  # noqa: E402
from v3lib import validate_schema  # noqa: E402


class TaskSnapshotGoldenExamplesTests(unittest.TestCase):
    def load_case(self, name: str) -> dict:
        return json.loads((EXAMPLES / f"{name}.json").read_text(encoding="utf-8"))

    def assert_valid(self, name: str) -> dict:
        value = self.load_case(name)
        errors = validate_schema("task-snapshot", value, name)
        self.assertEqual([], errors)
        return value

    def test_all_examples_validate(self):
        for path in sorted(EXAMPLES.glob("*.json")):
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual([], validate_schema("task-snapshot", value, path.name))

    def test_review_ready_parent_open_is_not_reported_done(self):
        text = render(self.assert_valid("review-ready-parent-open"))
        self.assertIn("#215 PARTIAL", text)
        self.assertIn("5/6 criteria satisfied — 83.3% unweighted coverage", text)
        self.assertIn("4/5 criteria satisfied — 80% unweighted coverage", text)
        self.assertIn("REVIEW_READY — PR #237", text)
        self.assertIn("SIBLING_WORKSTREAM=1", text)
        self.assertIn("#233 producer result", text)
        self.assertNotIn("#215 COMPLETE", text)

    def test_merged_child_can_be_complete_while_programme_is_open(self):
        text = render(self.assert_valid("merged-child-parent-open"))
        self.assertIn("#232 COMPLETE", text)
        self.assertIn("4/4 criteria satisfied — 100% unweighted coverage", text)
        self.assertIn("MERGED — PR #235", text)
        self.assertIn("| Programme contribution | PARTIAL | 4/5 criteria satisfied — 80% unweighted coverage |", text)
        self.assertIn("[OPEN]", text)

    def test_not_run_infrastructure_is_not_code_failure(self):
        text = render(self.assert_valid("not-run-infrastructure"))
        self.assertIn("#302 PARTIAL", text)
        self.assertIn("required exact-head certification is NOT_RUN", text)
        self.assertIn("INFRASTRUCTURE=2", text)
        self.assertIn("DRAFT — PR #304", text)
        self.assertIn("UNKNOWN — no mapped denominator", text)
        self.assertNotIn("| Verification | FAIL |", text)

    def test_active_task_remains_partial(self):
        text = render(self.assert_valid("active-task"))
        self.assertIn("#101 PARTIAL", text)
        self.assertIn("1/2 criteria satisfied — 50% unweighted coverage", text)

    def test_complete_task_is_unambiguously_complete(self):
        text = render(self.assert_valid("complete-task"))
        self.assertIn("#201 COMPLETE", text)
        self.assertIn("| Child/work-issue acceptance | SATISFIED | 1/1 criteria satisfied — 100% unweighted coverage |", text)
        self.assertIn("| Programme contribution | SATISFIED | 1/1 criteria satisfied — 100% unweighted coverage |", text)
        self.assertIn("MERGED — PR #202", text)

    def test_delivery_stack_renders_without_replacing_primary_delivery(self):
        task = self.assert_valid("active-task")
        task["delivery_stack"] = [
            {
                "pr": 99,
                "url": "https://github.com/example/repo/pull/99",
                "title": "Parent slice",
                "lifecycle": "DRAFT",
                "relationship": "STACK_PARENT",
                "base": "base-a",
                "head": "head-a",
                "mergeability": "MERGEABLE",
                "note": "Earlier slice",
            },
            {
                "pr": 101,
                "url": "https://github.com/example/repo/pull/101",
                "title": "Current slice",
                "lifecycle": "DRAFT",
                "relationship": "PRIMARY",
                "base": "base-b",
                "head": "head-b",
                "mergeability": "MERGEABLE",
                "note": None,
            },
        ]
        self.assertEqual([], validate_schema("task-snapshot", task, "stacked-active-task"))
        text = render(task)
        self.assertIn("### Delivery stack", text)
        self.assertIn("| STACK_PARENT | #99 | DRAFT | base-a | head-a | Earlier slice |", text)
        self.assertIn("| PRIMARY | #101 | DRAFT | base-b | head-b | - |", text)

if __name__ == "__main__":
    unittest.main()
