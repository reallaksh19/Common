import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()
