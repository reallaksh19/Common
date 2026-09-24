from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_task_binding import owned_issue_from_body, validate_binding, validate_event


class TaskBindingValidationTests(unittest.TestCase):
    def _write_snapshot(self, root: Path, *, issue: int = 265, head: str = "head-270") -> None:
        path = root / "relay/GENERATED/tasks/ISSUE-265.snapshot.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        value = {
            "parent_issue": {"number": issue},
            "identity": {"issue": issue},
            "material": {"current_head": head},
            "delivery": {
                "pr": 270,
                "lifecycle": "DRAFT",
                "head": head,
            },
            "delivery_stack": [
                {
                    "pr": 266,
                    "lifecycle": "DRAFT",
                    "relationship": "STACK_PARENT",
                    "head": "head-266",
                },
                {
                    "pr": 270,
                    "lifecycle": "DRAFT",
                    "relationship": "PRIMARY",
                    "head": head,
                },
            ],
        }
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def test_owned_issue_marker_prefers_explicit_ownership(self):
        self.assertEqual(265, owned_issue_from_body("Issue ownership remains #265."))
        self.assertEqual(265, owned_issue_from_body("Closes #265"))
        self.assertIsNone(owned_issue_from_body("Related to #265"))

    def test_stack_binding_accepts_exact_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_snapshot(root)
            self.assertEqual([], validate_binding(root, 265, 270, "head-270"))

    def test_missing_issue_snapshot_fails(self):
        with tempfile.TemporaryDirectory() as td:
            errors = validate_binding(Path(td), 265, 270, "head-270")
            self.assertIn("no Task Snapshot", errors[0])

    def test_stale_head_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_snapshot(root, head="old-head")
            errors = validate_binding(root, 265, 270, "new-head")
            self.assertIn("not exact head", errors[0])

    def test_pull_request_event_uses_owned_issue_marker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_snapshot(root)
            event = {
                "number": 270,
                "pull_request": {
                    "number": 270,
                    "body": "Issue ownership remains #265.",
                    "head": {"sha": "head-270"},
                },
            }
            ok, messages = validate_event(root, event)
            self.assertTrue(ok, messages)

    def test_unowned_pr_is_skipped(self):
        ok, messages = validate_event(
            Path("."),
            {
                "number": 1,
                "pull_request": {
                    "number": 1,
                    "body": "Infrastructure cleanup only.",
                    "head": {"sha": "abc"},
                },
            },
        )
        self.assertTrue(ok)
        self.assertTrue(messages[0].startswith("SKIP:"))


if __name__ == "__main__":
    unittest.main()
