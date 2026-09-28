import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "rll_codex_worker.py"
SPEC = importlib.util.spec_from_file_location("rll_codex_worker", MODULE_PATH)
rll = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rll)


class CodexRllWorkerTests(unittest.TestCase):
    def test_branch_resume_requires_allowed_paths(self):
        issue = {
            "author": {"login": "owner"},
            "body": """RLL_EXECUTION_V1

transport: RLL-1
worker: codex-local
mode: BRANCH_RESUME
repository: owner/repo
branch: feature/work
base_sha: abc123
allow_material_write: true
""",
        }
        with self.assertRaises(rll.core.RllError):
            rll.parse_exec(issue, [], {"owner"})

    def test_branch_resume_parses_semicolon_allowed_paths(self):
        issue = {
            "author": {"login": "owner"},
            "body": """RLL_EXECUTION_V1

transport: RLL-1
worker: codex-local
mode: BRANCH_RESUME
repository: owner/repo
branch: feature/work
base_sha: abc123
allow_material_write: true
allowed_paths: src/a.js; validation/example.json
commit_message: bounded change
""",
        }
        result = rll.parse_exec(issue, [], {"owner"})
        self.assertEqual(["src/a.js", "validation/example.json"], result["allowed_paths"])
        self.assertEqual("bounded change", result["commit_message"])

    def test_path_confinement_accepts_children_only(self):
        self.assertTrue(rll.path_allowed("src/owned/a.js", ["src/owned"]))
        self.assertTrue(rll.path_allowed("src/owned", ["src/owned"]))
        self.assertFalse(rll.path_allowed("src/other/a.js", ["src/owned"]))

    def test_codex_read_only_invocation_uses_structured_output_and_scrubs_github_tokens(self):
        schema = Path("schema.json")

        def fake_run(argv, **kwargs):
            output = Path(argv[argv.index("-o") + 1])
            output.write_text(
                json.dumps({
                    "schema": "RLL_AGENT_RESULT_V1",
                    "transport_state": "REVIEW_READY",
                    "current": "done",
                    "next": "review",
                    "engineering_summary": "tests passed",
                    "evidence_body": "exact-head evidence",
                    "notes": [],
                }),
                encoding="utf-8",
            )
            self.assertIn("--json", argv)
            self.assertEqual("read-only", argv[argv.index("--sandbox") + 1])
            self.assertNotIn("GH_TOKEN", kwargs["env"])
            self.assertNotIn("GITHUB_TOKEN", kwargs["env"])
            return type("Completed", (), {
                "returncode": 0,
                "stdout": '{"type":"thread.started"}\n',
                "stderr": "",
            })()

        with patch.dict(os.environ, {"GH_TOKEN": "secret", "GITHUB_TOKEN": "secret"}, clear=False):
            with patch.object(rll.subprocess, "run", side_effect=fake_run):
                value = rll.codex(
                    Path("."),
                    "prompt",
                    schema,
                    "2m",
                    "read-only",
                    codex_home="/tmp/codex-rll",
                    codex_user=None,
                )
        self.assertEqual("REVIEW_READY", value["transport_state"])
        self.assertEqual(1, value["_event_count"])

    def test_native_windows_workspace_write_fails_closed(self):
        with patch.object(rll.sys, "platform", "win32"):
            with self.assertRaises(rll.core.RllError):
                rll.codex(
                    Path("."),
                    "prompt",
                    Path("schema.json"),
                    "2m",
                    "workspace-write",
                    codex_home=None,
                    codex_user=None,
                )

    def test_changed_path_confinement_rejects_outside_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            import subprocess
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "rll@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "RLL Test"], check=True)
            (root / "allowed.txt").write_text("base\n", encoding="utf-8")
            (root / "blocked.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "base"], check=True, capture_output=True)
            (root / "blocked.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaises(rll.core.RllError):
                rll.assert_changed_paths_allowed(root, ["allowed.txt"])

    def test_codex_launcher_contains_no_merge_release_or_force_push(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        for token in (
            '"pr", "merge"',
            '"release", "create"',
            '"issue", "delete"',
            '"repo", "delete"',
            "--force",
        ):
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
