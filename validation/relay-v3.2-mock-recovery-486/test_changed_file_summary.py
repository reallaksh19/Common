import importlib.util
import json
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name("changed_file_summary.py")
spec = importlib.util.spec_from_file_location("mock_changed_file_summary", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class CommitAContractTests(unittest.TestCase):
    def test_parse_accepts_path_array_and_normalizes_separators(self):
        raw = json.dumps(["src/app.py", "docs\\guide.md", "README"])
        self.assertEqual(
            module.parse_changed_paths(raw),
            ["src/app.py", "docs/guide.md", "README"],
        )

    def test_parse_rejects_malformed_json(self):
        with self.assertRaisesRegex(module.InputContractError, "invalid JSON"):
            module.parse_changed_paths("[")

    def test_parse_rejects_non_array(self):
        with self.assertRaisesRegex(module.InputContractError, "JSON array"):
            module.parse_changed_paths('{"path": "a.py"}')

    def test_parse_rejects_non_string_or_empty_items(self):
        for raw in ('["a.py", 3]', '["a.py", "  "]'):
            with self.subTest(raw=raw):
                with self.assertRaises(module.InputContractError):
                    module.parse_changed_paths(raw)

    def test_extension_counts_are_deterministic(self):
        paths = ["src/A.PY", "src/b.py", "docs/readme.MD", "LICENSE"]
        self.assertEqual(
            module.extension_counts(paths),
            {".md": 1, ".py": 2, "<no_extension>": 1},
        )


if __name__ == "__main__":
    unittest.main()
