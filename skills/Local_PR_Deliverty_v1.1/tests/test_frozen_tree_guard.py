from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import frozen_tree_guard as g  # noqa: E402

try:
    import yaml  # noqa: F401

    HAVE_YAML = True
except ImportError:  # pragma: no cover
    HAVE_YAML = False

F = g.FROZEN_PREFIX
A = F + "scripts/new_tool.py"
B = F + "SKILL.md"


def amendment(paths, authorized=True, basis="Owner instruction 2026-10-07"):
    return {
        "schema": g.SCHEMA,
        "amendments": [{"id": "AMEND-1", "owner_authorized": authorized, "owner_basis": basis, "allowed_paths": list(paths)}],
    }


class AllowedPathsTests(unittest.TestCase):
    def test_no_manifest_amends_nothing(self):
        self.assertEqual(set(), g.allowed_paths(None))

    def test_only_owner_authorised_amendments_are_honoured(self):
        self.assertEqual({A}, g.allowed_paths(amendment([A])))
        self.assertEqual(set(), g.allowed_paths(amendment([A], authorized=False)))

    def test_authorised_amendment_must_cite_an_owner_basis(self):
        with self.assertRaises(g.AmendmentError):
            g.allowed_paths(amendment([A], basis=""))

    def test_globs_traversal_and_outside_paths_are_rejected(self):
        for bad in (F + "scripts/*.py", F + "../x", "skills/other/x.py", "/abs", F.rstrip("/"), g.MANIFEST_PATH, F + "a\\b"):
            with self.subTest(path=bad), self.assertRaises(g.AmendmentError):
                g.allowed_paths(amendment([bad]))

    def test_wrong_schema_and_duplicate_ids_are_rejected(self):
        with self.assertRaises(g.AmendmentError):
            g.allowed_paths({"schema": "something-else", "amendments": []})
        doc = amendment([A])
        doc["amendments"].append(dict(doc["amendments"][0]))
        with self.assertRaises(g.AmendmentError):
            g.allowed_paths(doc)

    def test_violations_ignore_paths_outside_the_frozen_tree(self):
        self.assertEqual([B], g.violations([B, "skills/engineering-pr-delivery-v3.5/x.py"], {A}))
        self.assertEqual([], g.violations([A], {A}))


@unittest.skipUnless(HAVE_YAML, "PyYAML unavailable")
class GitBackedGuardTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.git("init", "-q")
        self.git("config", "user.email", "guard@example.invalid")
        self.git("config", "user.name", "Guard Test")
        self.write(B, "frozen\n")
        self.write("other.txt", "x\n")
        self.base = self.commit("base")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], text=True, capture_output=True, check=True).stdout.strip()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def manifest(self, doc):
        import yaml

        self.write(g.MANIFEST_PATH, yaml.safe_dump(doc))

    def test_unchanged_tree_passes(self):
        self.write("other.txt", "changed\n")
        head = self.commit("outside")
        self.assertEqual((0, []), g.check(self.root, self.base, head))

    def test_unlisted_change_fails_by_default(self):
        self.write(B, "edited\n")
        head = self.commit("edit frozen")
        self.assertEqual((1, [B]), g.check(self.root, self.base, head))

    def test_a_pr_cannot_authorise_its_own_edit(self):
        self.manifest(amendment([A]))
        self.write(A, "new tool\n")
        head = self.commit("add manifest and edit in one PR")
        self.assertEqual((1, [A]), g.check(self.root, self.base, head))

    def test_listed_paths_pass_once_the_manifest_is_in_the_base(self):
        self.manifest(amendment([A]))
        base = self.commit("land the amendment first")
        self.write(A, "new tool\n")
        head = self.commit("amended change")
        self.assertEqual((0, []), g.check(self.root, base, head))

    def test_listing_one_path_does_not_unfreeze_the_rest(self):
        self.manifest(amendment([A]))
        base = self.commit("land the amendment first")
        self.write(A, "new tool\n")
        self.write(B, "sneaky edit\n")
        head = self.commit("amended change plus an unlisted edit")
        self.assertEqual((1, [B]), g.check(self.root, base, head))

    def test_deletions_and_renames_of_frozen_files_fail(self):
        (self.root / B).unlink()
        head = self.commit("delete frozen file")
        self.assertEqual((1, [B]), g.check(self.root, self.base, head))

    def test_unauthorised_amendment_in_base_is_not_honoured(self):
        self.manifest(amendment([A], authorized=False))
        base = self.commit("recorded but not authorised")
        self.write(A, "new tool\n")
        head = self.commit("edit")
        self.assertEqual((1, [A]), g.check(self.root, base, head))

    def test_malformed_base_manifest_fails_closed(self):
        self.manifest({"schema": g.SCHEMA, "amendments": [{"id": "X", "owner_authorized": True, "owner_basis": "b", "allowed_paths": [F + "*"]}]})
        base = self.commit("malformed")
        self.write(A, "new tool\n")
        head = self.commit("edit")
        code, bad = g.check(self.root, base, head)
        self.assertEqual(1, code)
        self.assertTrue(bad[0].startswith("base amendment manifest rejected"))
        self.assertIn(A, bad)

    def test_cli_exit_codes(self):
        self.write(B, "edited\n")
        self.commit("edit frozen")
        self.assertEqual(1, g.main(["--base", self.base, "--repo-root", str(self.root)]))
        self.assertEqual(0, g.main(["--base", self.git("rev-parse", "HEAD"), "--repo-root", str(self.root)]))


if __name__ == "__main__":
    unittest.main()
