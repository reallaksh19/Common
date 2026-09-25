from __future__ import annotations

import subprocess
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


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


class TaskBindingValidationTests(unittest.TestCase):
    def _write_snapshot(
        self,
        root: Path,
        *,
        issue: int = 265,
        head: str = "head-270",
        common_sha: str | None = None,
        two_pass_revision: str = "TPG-2P-2026-09-25-R1",
    ) -> None:
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
        if common_sha is not None:
            value["protocol_basis"] = {
                "protocol": "V3.1",
                "common_repository": "reallaksh19/Common",
                "common_sha": common_sha,
                "two_pass_revision": two_pass_revision,
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
            self.assertIn("not current material basis", errors[0])

    def test_coordination_only_commit_after_material_head_is_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _git(root, "init")
            _git(root, "config", "user.email", "relay@example.invalid")
            _git(root, "config", "user.name", "Relay Test")
            (root / "product.txt").write_text("material\n", encoding="utf-8")
            _git(root, "add", "product.txt")
            _git(root, "commit", "-m", "material")
            material_head = _git(root, "rev-parse", "HEAD")

            self._write_snapshot(root, head=material_head)
            _git(root, "add", "relay/GENERATED/tasks/ISSUE-265.snapshot.yaml")
            _git(root, "commit", "-m", "coordination snapshot")
            current_head = _git(root, "rev-parse", "HEAD")

            self.assertEqual([], validate_binding(root, 265, 270, current_head))

            (root / "product.txt").write_text("changed material\n", encoding="utf-8")
            _git(root, "add", "product.txt")
            _git(root, "commit", "-m", "new material")
            newer_head = _git(root, "rev-parse", "HEAD")
            errors = validate_binding(root, 265, 270, newer_head)
            self.assertIn("not current material basis", errors[0])

    def test_live_protocol_basis_is_required_when_requested(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            live_sha = "a" * 40
            self._write_snapshot(root, common_sha=live_sha)
            self.assertEqual(
                [],
                validate_binding(
                    root,
                    265,
                    270,
                    "head-270",
                    expected_common_sha=live_sha,
                    expected_two_pass_revision="TPG-2P-2026-09-25-R1",
                ),
            )

            stale = "b" * 40
            errors = validate_binding(
                root,
                265,
                270,
                "head-270",
                expected_common_sha=stale,
                expected_two_pass_revision="TPG-2P-2026-09-25-R1",
            )
            self.assertIn("not on the live V3.1 protocol basis", errors[0])
            self.assertTrue(any("stale" in row for row in errors))

    def test_missing_protocol_basis_fails_when_live_basis_is_required(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_snapshot(root)
            errors = validate_binding(
                root,
                265,
                270,
                "head-270",
                expected_common_sha="c" * 40,
                expected_two_pass_revision="TPG-2P-2026-09-25-R1",
            )
            self.assertIn("not on the live V3.1 protocol basis", errors[0])
            self.assertTrue(any("missing protocol_basis" in row for row in errors))

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
