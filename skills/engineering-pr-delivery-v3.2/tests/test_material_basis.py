from __future__ import annotations

import subprocess
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

from material_basis import inspect
from test_relay_can import git, prepare_git


class MaterialBasisTests(unittest.TestCase):
    def _ep(self, root: Path):
        return yaml.safe_load((root / "relay/WORK/EP-TA-011.yaml").read_text(encoding="utf-8"))

    def test_coordination_only_commit_does_not_advance_material_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_sha, base_ref = prepare_git(root)
            first = inspect(root, self._ep(root), base_ref)
            self.assertEqual(base_sha, first["material_basis"]["head"])
            first_coordination = first["coordination_basis"]["head"]
            self.assertNotEqual(base_sha, first_coordination)

            marker = root / "relay/coordination-note.txt"
            marker.write_text("coordination only\n", encoding="utf-8")
            git(root, "add", "relay/coordination-note.txt")
            git(root, "commit", "-m", "coordination only")
            second = inspect(root, self._ep(root), base_ref)

            self.assertEqual(base_sha, second["material_basis"]["head"])
            self.assertNotEqual(first_coordination, second["coordination_basis"]["head"])
            self.assertEqual(
                first["material_basis"]["relevant_paths_digest"],
                second["material_basis"]["relevant_paths_digest"],
            )
            self.assertEqual(
                first["material_basis"]["dependency_digest"],
                second["material_basis"]["dependency_digest"],
            )

    def test_material_commit_advances_material_head_and_relevant_digest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            before = inspect(root, self._ep(root), base_ref)

            target = root / "skills/engineering-pr-delivery-v3.1/scripts/new_feature.py"
            target.write_text("VALUE = 2\n", encoding="utf-8")
            git(root, "add", "skills/engineering-pr-delivery-v3.1/scripts/new_feature.py")
            git(root, "commit", "-m", "material change")
            material_commit = git(root, "rev-parse", "HEAD")
            after = inspect(root, self._ep(root), base_ref)

            self.assertEqual(material_commit, after["material_basis"]["head"])
            self.assertEqual(material_commit, after["coordination_basis"]["head"])
            self.assertNotEqual(
                before["material_basis"]["relevant_paths_digest"],
                after["material_basis"]["relevant_paths_digest"],
            )

    def test_dependency_digest_changes_when_material_dependency_changes_on_execution_branch(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, base_ref = prepare_git(root)
            before = inspect(root, self._ep(root), base_ref)

            dependency = root / "deps/compiler.py"
            dependency.write_text("VERSION = 3\n", encoding="utf-8")
            git(root, "add", "deps/compiler.py")
            git(root, "commit", "-m", "dependency change")
            after = inspect(root, self._ep(root), base_ref)

            self.assertNotEqual(
                before["material_basis"]["dependency_digest"],
                after["material_basis"]["dependency_digest"],
            )
            self.assertEqual(
                after["material_basis"]["head"],
                after["coordination_basis"]["head"],
            )

    def test_unresolvable_base_is_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = inspect(root, self._ep(root), "missing-base")
            self.assertEqual("UNKNOWN", result["drift"]["classification"])
            self.assertIsNone(result["drift"]["to_base"])


if __name__ == "__main__":
    unittest.main()
