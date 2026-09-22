from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from status_publication import apply, evaluate, load_policy
from test_relay_can import prepare_git


class StatusPublicationTests(unittest.TestCase):
    def install_policy(self, root: Path, **overrides) -> None:
        policy, _ = load_policy(root)
        for key, value in overrides.items():
            policy[key] = value
        path = root / "relay/CONFIG/status-publication.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")

    def test_initial_status_is_due_then_apply_clears_it(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            self.install_policy(root)
            first = evaluate(root)
            self.assertTrue(first["publication_due"], first)
            self.assertIn("INITIAL_STATUS", first["reasons"])

            recorded = apply(root, note="Initial child status published.")
            self.assertIn("recorded", recorded)
            second = evaluate(root)
            self.assertFalse(second["publication_due"], second)

    def test_material_volume_threshold_is_enforced_from_child_cursor(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            policy, _ = load_policy(root)
            policy["score_threshold"] = 999
            policy["volume_triggers"]["material_lines_changed"] = 3
            policy["volume_triggers"]["material_files_touched"] = 99
            policy["volume_triggers"]["material_files_created"] = 99
            policy["volume_triggers"]["material_commits"] = 99
            path = root / "relay/CONFIG/status-publication.yaml"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")
            apply(root, note="baseline")

            target = root / "skills/engineering-pr-delivery-v3/scripts/base.py"
            target.write_text("VALUE = 2\nA = 1\nB = 2\nC = 3\n", encoding="utf-8")
            result = evaluate(root)
            self.assertTrue(result["publication_due"], result)
            self.assertIn("MATERIAL_LINES_THRESHOLD", result["reasons"])

    def test_pre_action_publication_is_bound_to_current_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            self.install_policy(root)
            apply(root, note="baseline")
            due = evaluate(root, action="CHECKPOINT")
            self.assertTrue(due["publication_due"], due)
            self.assertIn("BEFORE_CHECKPOINT", due["reasons"])
            apply(root, action="CHECKPOINT", note="pre-checkpoint status published")
            clear = evaluate(root, action="CHECKPOINT")
            self.assertFalse(clear["publication_due"], clear)

    def test_ui_and_default_policy_are_present(self):
        policy = yaml.safe_load((ROOT / "config/status-publication.default.yaml").read_text(encoding="utf-8"))
        self.assertEqual(300, policy["volume_triggers"]["material_lines_changed"])
        html = (ROOT / "ui/status-publication-policy.html").read_text(encoding="utf-8")
        self.assertIn("Status publication policy", html)
        self.assertIn("Download YAML", html)


if __name__ == "__main__":
    unittest.main()
