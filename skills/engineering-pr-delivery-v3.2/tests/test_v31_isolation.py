from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V31IsolationTests(unittest.TestCase):
    def test_v31_does_not_link_back_to_v3_skill_tree(self):
        forbidden = "skills/" + "engineering-pr-delivery-v3/"
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if forbidden in text:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders)

    def test_v31_tree_contains_no_symlinks(self):
        symlinks = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_symlink()]
        self.assertEqual([], symlinks)


if __name__ == "__main__":
    unittest.main()
