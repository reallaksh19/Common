import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "rll_worker.py"
SPEC = importlib.util.spec_from_file_location("rll_worker", MODULE_PATH)
rll = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rll)


class RllWorkerTests(unittest.TestCase):
    def test_choose_issue_prefers_single_active_then_oldest_ready(self):
        self.assertEqual(9, rll.choose([{"number": 9}], [{"number": 1}])["number"])
        ready = [
            {"number": 8, "createdAt": "2026-09-26T02:00:00Z"},
            {"number": 7, "createdAt": "2026-09-26T01:00:00Z"},
        ]
        self.assertEqual(7, rll.choose([], ready)["number"])
        self.assertIsNone(rll.choose([], []))
        with self.assertRaises(rll.RllError):
            rll.choose([{"number": 1}, {"number": 2}], [])

    def test_branch_resume_execution_envelope(self):
        issue = {
            "author": {"login": "owner"},
            "body": """RLL_EXECUTION_V1

transport: RLL-1
worker: antigravity-local
mode: BRANCH_RESUME
repository: owner/repo
branch: feature/work
base_sha: abc123
allow_material_write: true
"""
        }
        result = rll.parse_exec(issue, [], {"owner"})
        self.assertEqual("BRANCH_RESUME", result["mode"])
        self.assertEqual("feature/work", result["branch"])
        self.assertTrue(result["write"])

    def test_issue_body_execution_envelope_requires_authorized_author(self):
        issue = {
            "author": {"login": "stranger"},
            "body": """RLL_EXECUTION_V1

transport: RLL-1
worker: antigravity-local
mode: BRANCH_RESUME
repository: owner/repo
branch: feature/work
base_sha: abc123
allow_material_write: true
""",
        }
        with self.assertRaises(rll.RllError):
            rll.parse_exec(issue, [], {"owner"})

    def test_exact_head_envelope_is_read_only(self):
        issue = {"body": ""}
        comments = [{
            "user": {"login": "owner"},
            "body": """RLL_EXECUTION_V1

transport: RLL-1
worker: antigravity-local
mode: EXACT_HEAD_EVIDENCE
repository: owner/repo
head_sha: deadbeef
base_sha: abc123
allow_material_write: false
""",
        }]
        result = rll.parse_exec(issue, comments, {"owner"})
        self.assertEqual("deadbeef", result["head_sha"])
        self.assertFalse(result["write"])

        comments[0]["body"] = comments[0]["body"].replace("false", "true")
        with self.assertRaises(rll.RllError):
            rll.parse_exec(issue, comments, {"owner"})

    def test_directive_filter_requires_authorized_structured_comment(self):
        comments = [
            {"id": 1, "user": {"login": "stranger"}, "body": "RELAY_DIRECTIVE_V1\nsequence: 1\nissue: 42\naction: CANCEL"},
            {"id": 2, "user": {"login": "owner"}, "body": "please cancel this"},
            {"id": 3, "user": {"login": "owner"}, "body": "RELAY_DIRECTIVE_V1\nsequence: 2\nissue: 42\naction: PAUSE"},
            {"id": 4, "user": {"login": "owner"}, "body": "RELAY_DIRECTIVE_V1\nsequence: 3\nissue: 99\naction: CANCEL"},
        ]
        rows = rll.directives(comments, 42, {"owner"}, 0)
        self.assertEqual([(2, "PAUSE", "")], rows)
        self.assertEqual([], rll.directives(comments, 42, {"owner"}, 2))

    def test_duplicate_directive_sequence_is_rejected(self):
        comments = [
            {"id": 1, "user": {"login": "owner"}, "body": "RELAY_DIRECTIVE_V1\nsequence: 5\nissue: 42\naction: CONTINUE"},
            {"id": 2, "user": {"login": "owner"}, "body": "RELAY_DIRECTIVE_V1\nsequence: 5\nissue: 42\naction: PAUSE"},
        ]
        with self.assertRaises(rll.RllError):
            rll.directives(comments, 42, {"owner"}, 0)

    def test_worker_state_roundtrip(self):
        state = {
            "worker": "antigravity-local",
            "issue": 42,
            "state": "ACTIVE",
            "phase": "IMPLEMENT",
            "mode": "BRANCH_RESUME",
            "branch": "feature/work",
            "base_sha": "abc",
            "material_head": "def",
            "lease_epoch": 3,
            "lease_until": "2026-09-26T04:30:00Z",
            "last_directive_sequence": 7,
            "current": "testing",
            "next": "certification",
        }
        body = rll.render(state, "common-sha", "TPG-2P-2026-09-25-R1")
        parsed = rll.parse_state(body)
        for key in (
            "worker", "issue", "state", "phase", "mode", "branch",
            "base_sha", "material_head", "lease_epoch", "lease_until",
            "last_directive_sequence", "current", "next",
        ):
            self.assertEqual(state[key], parsed[key], key)

    def test_pause_and_resume_control_transport_not_engineering(self):
        state = {
            "state": "ACTIVE", "phase": "IMPLEMENT", "lease_until": "future",
            "last_directive_sequence": 0, "current": "work", "next": "test",
        }
        invoke, _ = rll.apply_dirs(state, [(1, "PAUSE", "")])
        self.assertFalse(invoke)
        self.assertEqual("RETRY_WAIT", state["state"])
        self.assertEqual("PAUSED_BY_DIRECTIVE", state["phase"])
        invoke, _ = rll.apply_dirs(state, [(2, "RESUME", "continue bounded work")])
        self.assertTrue(invoke)
        self.assertEqual("ACTIVE", state["state"])
        self.assertEqual(2, state["last_directive_sequence"])

    def test_pause_persists_until_authorized_resume(self):
        state = {
            "state": "RETRY_WAIT",
            "phase": "PAUSED_BY_DIRECTIVE",
            "lease_until": None,
            "last_directive_sequence": 1,
            "current": "paused",
            "next": "await resume",
        }
        invoke, notes = rll.apply_dirs(state, [])
        self.assertFalse(invoke)
        self.assertEqual([], notes)
        self.assertEqual("PAUSED_BY_DIRECTIVE", state["phase"])

        invoke, notes = rll.apply_dirs(
            state,
            [(2, "RESUME", "continue the existing bounded plan")],
        )
        self.assertTrue(invoke)
        self.assertEqual("ACTIVE", state["state"])
        self.assertEqual(2, state["last_directive_sequence"])

    def test_review_ready_requires_clean_tree_and_evidence_url(self):
        envelope = {"mode": "BRANCH_RESUME", "branch": "feature/work"}
        base = {
            "material_head": "",
            "state": "ACTIVE",
            "phase": "IMPLEMENT",
            "lease_until": "future",
            "current": "",
            "next": "",
        }
        result = {
            "transport_state": "REVIEW_READY",
            "current": "done",
            "next": "review",
            "evidence_comment_url": None,
        }
        rll.apply_result(base, result, {"head": "abc", "branch": "feature/work", "clean": True}, envelope)
        self.assertEqual("ACTIVE", base["state"])
        self.assertEqual("POSTFLIGHT", base["phase"])

    def test_exact_head_result_rejects_head_movement(self):
        envelope = {"mode": "EXACT_HEAD_EVIDENCE", "head_sha": "expected"}
        state = {
            "material_head": "",
            "state": "ACTIVE",
            "phase": "IMPLEMENT",
            "lease_until": "future",
            "current": "",
            "next": "",
        }
        result = {
            "transport_state": "REVIEW_READY",
            "current": "done",
            "next": "review",
            "evidence_comment_url": "https://github.com/owner/repo/issues/42#issuecomment-1",
        }
        rll.apply_result(
            state,
            result,
            {"head": "moved", "branch": "", "clean": True},
            envelope,
        )
        self.assertEqual("ESCALATION_REQUIRED", state["state"])
        self.assertEqual("HEAD_MISMATCH", state["phase"])

    def test_exact_head_workspace_is_dedicated_and_detached(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            root.mkdir()
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "rll@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "RLL Test"], check=True)
            (root / "file.txt").write_text("baseline\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "file.txt"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "baseline"], check=True, capture_output=True)
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True,
            ).stdout.strip()
            worktree = rll.prepare_exact_head_workspace(
                root,
                {"head_sha": head},
                data,
                42,
            )
            self.assertNotEqual(root, worktree)
            self.assertEqual(head, rll.observe(worktree)["head"])
            self.assertEqual("", rll.observe(worktree)["branch"])
            self.assertTrue(rll.observe(worktree)["clean"])

    def test_current_pid_mutex_blocks_second_worker(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp) / "worker.lock"
            lock.mkdir()
            (lock / "owner.json").write_text(json.dumps({"pid": os.getpid()}), encoding="utf-8")
            with self.assertRaises(rll.RllError):
                with rll.Mutex(lock):
                    pass

    def test_headless_result_requires_successful_structured_output(self):
        payload = {
            "status": "SUCCESS",
            "structured_output": {
                "schema": "RLL_RUN_RESULT_V1",
                "transport_state": "ACTIVE",
                "current": "working",
                "next": "test",
                "evidence_comment_url": None,
                "engineering_summary": "",
                "notes": [],
            },
        }
        completed = type("Completed", (), {
            "returncode": 0,
            "stdout": json.dumps(payload),
            "stderr": "",
        })()
        with patch.object(rll, "cmd", return_value=completed):
            result = rll.agy(
                Path("."),
                "prompt",
                Path("schema.json"),
                "2h",
                "high",
            )
        self.assertEqual("ACTIVE", result["transport_state"])

    def test_headless_permission_denial_becomes_transport_retry_error(self):
        payload = {
            "status": "SUCCESS",
            "structured_output": {
                "schema": "RLL_RUN_RESULT_V1",
                "transport_state": "REVIEW_READY",
                "current": "done",
                "next": "review",
                "evidence_comment_url": "https://example.invalid/evidence",
                "engineering_summary": "claimed complete",
                "notes": [],
            },
        }
        completed = type("Completed", (), {
            "returncode": 0,
            "stdout": json.dumps(payload),
            "stderr": "tool permission denied; requires approval",
        })()
        with patch.object(rll, "cmd", return_value=completed):
            with self.assertRaises(rll.RllError):
                rll.agy(Path("."), "prompt", Path("schema.json"), "2h", "high")

    def test_rll_contract_schemas_are_valid_json(self):
        schema_root = Path(__file__).resolve().parents[1] / "schemas"
        expected = {
            "rll-execution.schema.json": "RLL_EXECUTION_V1",
            "rll-worker-state.schema.json": "RLL_WORKER_STATE_V1",
            "rll-directive.schema.json": "RELAY_DIRECTIVE_V1",
            "rll-run-result.schema.json": "RLL_RUN_RESULT_V1",
        }
        for filename, title in expected.items():
            value = json.loads((schema_root / filename).read_text(encoding="utf-8"))
            self.assertEqual(title, value["title"])
            self.assertEqual("object", value["type"])

    def test_launcher_contains_no_merge_release_or_delete_provider_operation(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = [
            '"pr","merge"',
            '"release","create"',
            '"issue","delete"',
            '"repo","delete"',
        ]
        for token in forbidden:
            self.assertNotIn(token, source)


    def test_codex_source_write_command_is_schema_bound_and_workspace_scoped(self):
        payload = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "ACTIVE",
            "current": "working",
            "next": "test",
            "evidence_comment_url": None,
            "evidence_markdown": "",
            "engineering_summary": "",
            "notes": [],
        }
        completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        calls = []
        def fake_cmd(argv, cwd=None, check=True, timeout=None, env=None):
            calls.append((argv, cwd, check, timeout))
            output = Path(argv[argv.index("--output-last-message") + 1])
            output.write_text(json.dumps(payload), encoding="utf-8")
            return completed
        with patch.object(rll, "cmd", side_effect=fake_cmd):
            result = rll.codex(Path("."), "prompt", Path("schema.json"), "30m", "high", True)
        argv = calls[0][0]
        self.assertEqual("codex", argv[0])
        self.assertEqual(["--ask-for-approval", "never", "exec"], argv[1:4])
        self.assertIn("--output-schema", argv)
        self.assertIn("--output-last-message", argv)
        self.assertEqual("workspace-write", argv[argv.index("--sandbox") + 1])
        self.assertIn("--json", argv)
        self.assertIn('approvals_reviewer="user"', argv)
        self.assertIn('web_search="disabled"', argv)
        self.assertIn('sandbox_workspace_write.network_access=false', argv)
        self.assertEqual("ACTIVE", result["transport_state"])

    def test_codex_exact_head_uses_read_only_sandbox(self):
        payload = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "ACTIVE",
            "current": "working",
            "next": "review",
            "evidence_comment_url": None,
            "engineering_summary": "",
            "notes": [],
        }
        completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        seen = {}
        def fake_cmd(argv, cwd=None, check=True, timeout=None, env=None):
            seen["argv"] = argv
            Path(argv[argv.index("--output-last-message") + 1]).write_text(json.dumps(payload), encoding="utf-8")
            return completed
        with patch.object(rll, "cmd", side_effect=fake_cmd):
            rll.codex(Path("."), "prompt", Path("schema.json"), "2h", "high", False)
        self.assertEqual("read-only", seen["argv"][seen["argv"].index("--sandbox") + 1])

    def test_codex_rejects_missing_or_invalid_output_file(self):
        completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        with patch.object(rll, "cmd", return_value=completed):
            with self.assertRaises(rll.RllError):
                rll.codex(Path("."), "prompt", Path("schema.json"), "10s", "high", True)

    def test_codex_rejects_nonzero_exit_even_with_possible_output(self):
        completed = type("Completed", (), {"returncode": 7, "stdout": "", "stderr": "provider error"})()
        with patch.object(rll, "cmd", return_value=completed):
            with self.assertRaises(rll.RllError):
                rll.codex(Path("."), "prompt", Path("schema.json"), "10s", "high", True)

    def test_validate_run_result_accepts_executor_evidence_markdown(self):
        value = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "REVIEW_READY",
            "current": "done",
            "next": "review",
            "evidence_comment_url": None,
            "evidence_markdown": "focused tests PASS",
            "engineering_summary": "focused PASS",
            "notes": [],
        }
        self.assertEqual(value, rll.validate_run_result(value))

    def test_publish_executor_evidence_binds_observed_material_head(self):
        value = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "REVIEW_READY",
            "current": "done",
            "next": "review",
            "evidence_comment_url": None,
            "evidence_markdown": "focused tests PASS",
            "engineering_summary": "focused PASS",
            "notes": [],
        }
        with patch.object(rll, "ghj", return_value={"html_url": "https://example.invalid/evidence"}) as api:
            result = rll.publish_executor_evidence(
                "owner/repo", 42, value,
                {"head": "abc123", "branch": "feature/work", "clean": True},
                "codex",
            )
        self.assertEqual("https://example.invalid/evidence", result["evidence_comment_url"])
        joined = " ".join(api.call_args.args)
        self.assertIn("abc123", joined)
        self.assertIn("focused tests PASS", joined)

    def test_duration_seconds_is_bounded_and_explicit(self):
        self.assertEqual(7200, rll.duration_seconds("2h"))
        self.assertEqual(1800, rll.duration_seconds("30m"))
        self.assertEqual(45, rll.duration_seconds("45s"))
        with self.assertRaises(rll.RllError):
            rll.duration_seconds("0h")


    def test_publish_executor_evidence_refuses_dirty_review_ready(self):
        value = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "REVIEW_READY",
            "current": "done",
            "next": "review",
            "evidence_comment_url": None,
            "evidence_markdown": "claimed evidence",
            "engineering_summary": "",
            "notes": [],
        }
        with patch.object(rll, "ghj") as api:
            result = rll.publish_executor_evidence(
                "owner/repo", 42, value,
                {"head": "abc", "branch": "feature/work", "clean": False},
                "codex",
            )
        api.assert_not_called()
        self.assertIsNone(result["evidence_comment_url"])

    def test_cmd_timeout_is_transport_error(self):
        with patch.object(
            rll.subprocess,
            "run",
            side_effect=rll.subprocess.TimeoutExpired(["codex"], 5),
        ):
            with self.assertRaises(rll.RllError):
                rll.cmd(["codex"], timeout=5)

    def test_run_executor_dispatches_codex(self):
        with patch.object(rll, "codex", return_value={"ok": True}) as selected:
            result = rll.run_executor(
                "codex", Path("."), "prompt", Path("schema.json"), "10s", "high", True
            )
        self.assertEqual({"ok": True}, result)
        selected.assert_called_once()

    def test_codex_branch_resume_requires_allowed_paths(self):
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
allowed_paths: src/owned; validation/example.json
commit_message: bounded codex change
""",
        }
        value = rll.parse_exec(issue, [], {"owner"})
        self.assertEqual(["src/owned", "validation/example.json"], value["allowed_paths"])
        self.assertEqual("bounded codex change", value["commit_message"])

    def test_codex_prompt_embeds_issue_context_and_forbids_provider_control(self):
        issue = {"number": 42, "title": "Bounded task", "body": "Do the bounded work."}
        comments = [{"user": {"login": "owner"}, "body": "TASK_NOTE\nkeep scope"}]
        envelope = {
            "mode": "BRANCH_RESUME",
            "base_sha": "abc",
            "branch": "feature/work",
            "head_sha": None,
            "write": True,
            "allowed_paths": ["src/owned"],
        }
        text = rll.prompt("owner/repo", 42, envelope, [], "codex", issue, comments)
        self.assertIn("DURABLE ISSUE CONTEXT", text)
        self.assertIn("Do the bounded work.", text)
        self.assertIn("Do not invoke gh", text)
        self.assertIn("Do not commit, push, rebase, merge", text)
        self.assertIn("src/owned", text)

    def test_codex_scrubs_github_token_environment(self):
        payload = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "ACTIVE",
            "current": "working",
            "next": "test",
            "evidence_comment_url": None,
            "engineering_summary": "",
            "notes": [],
        }
        completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        seen = {}
        def fake_cmd(argv, cwd=None, check=True, timeout=None, env=None):
            seen["env"] = env
            Path(argv[argv.index("--output-last-message") + 1]).write_text(
                json.dumps(payload), encoding="utf-8"
            )
            return completed
        with patch.dict(
            os.environ,
            {"GH_TOKEN": "secret", "GITHUB_TOKEN": "secret", "GH_ENTERPRISE_TOKEN": "secret"},
            clear=False,
        ):
            with patch.object(rll, "cmd", side_effect=fake_cmd):
                rll.codex(Path("."), "prompt", Path("schema.json"), "10s", "high", False)
        self.assertNotIn("GH_TOKEN", seen["env"])
        self.assertNotIn("GITHUB_TOKEN", seen["env"])
        self.assertNotIn("GH_ENTERPRISE_TOKEN", seen["env"])

    def test_codex_native_windows_write_fails_closed(self):
        with patch.object(rll.sys, "platform", "win32"):
            with self.assertRaises(rll.RllError):
                rll.codex(Path("."), "prompt", Path("schema.json"), "10s", "high", True)

    def test_allowed_path_confinement_rejects_escape(self):
        self.assertTrue(rll.path_allowed("src/owned/a.js", ["src/owned"]))
        self.assertFalse(rll.path_allowed("src/other/a.js", ["src/owned"]))
        with self.assertRaises(rll.RllError):
            rll.normalize_allowed_paths("../escape")


    def test_codex_isolated_user_uses_dedicated_home(self):
        payload = {
            "schema": "RLL_RUN_RESULT_V1",
            "transport_state": "ACTIVE",
            "current": "working",
            "next": "test",
            "evidence_comment_url": None,
            "engineering_summary": "",
            "notes": [],
        }
        completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        seen = {}
        def fake_cmd(argv, cwd=None, check=True, timeout=None, env=None):
            seen["argv"] = argv
            Path(argv[argv.index("--output-last-message") + 1]).write_text(
                json.dumps(payload), encoding="utf-8"
            )
            return completed
        with patch.object(rll, "cmd", side_effect=fake_cmd):
            rll.codex(
                Path("."), "prompt", Path("schema.json"), "10s", "high", False,
                "rll-codex", "/home/rll-codex/.codex-rll",
            )
        self.assertEqual(["sudo", "-n", "-u", "rll-codex", "env"], seen["argv"][:5])
        self.assertIn("CODEX_HOME=/home/rll-codex/.codex-rll", seen["argv"])
        self.assertIn("HOME=/home/rll-codex", seen["argv"])


if __name__ == "__main__":
    unittest.main()
