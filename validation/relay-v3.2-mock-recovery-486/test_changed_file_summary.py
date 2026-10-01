import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name("changed_file_summary.py")
spec = importlib.util.spec_from_file_location("mock_changed_file_summary", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class ChangedFileSummaryTests(unittest.TestCase):
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

    def test_unique_directories_are_sorted_and_deduplicated(self):
        paths = [
            "src/app.py",
            "docs/guide.md",
            "src/helpers/tool.py",
            "README",
            "docs/other.md",
            "win\\nested\\file.txt",
        ]
        self.assertEqual(
            module.unique_directories(paths),
            [".", "docs", "src", "src/helpers", "win/nested"],
        )

    def test_summarize_combines_all_declared_output_fields(self):
        paths = ["src/app.py", "docs/guide.MD", "README"]
        self.assertEqual(
            module.summarize(paths),
            {
                "total_file_count": 3,
                "extensions": {".md": 1, ".py": 1, "<no_extension>": 1},
                "directories": [".", "docs", "src"],
            },
        )

    def test_empty_array_has_zero_count_and_empty_aggregates(self):
        self.assertEqual(
            module.summarize(module.parse_changed_paths("[]")),
            {"total_file_count": 0, "extensions": {}, "directories": []},
        )

    def test_cli_reads_stdin_and_emits_json(self):
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH)],
            input='["src/a.py", "README"]',
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "total_file_count": 2,
                "extensions": {".py": 1, "<no_extension>": 1},
                "directories": [".", "src"],
            },
        )
        self.assertEqual(result.stderr, "")

    def test_cli_reads_named_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = pathlib.Path(tmpdir) / "changed.json"
            input_path.write_text('["pkg/a.py"]', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(input_path)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["directories"], ["pkg"])

    def test_cli_reports_contract_errors_without_traceback(self):
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH)],
            input='{"path": "src/a.py"}',
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("error: input must be a JSON array", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_cli_reports_file_read_errors_without_traceback(self):
        missing = MODULE_PATH.with_name("does-not-exist.json")
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(missing)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
