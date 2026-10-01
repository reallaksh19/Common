import importlib.util
import pathlib
import shutil
import subprocess
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "continuity_projection.py"
spec = importlib.util.spec_from_file_location("continuity_projection", MODULE_PATH)
cp = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(cp)


def base(material="b", semantic="a", delta=1):
    return cp.new_snapshot(
        "owner/repo#10",
        [
            {"id": "UNIT-01", "complete": True, "evidenced": True},
            {"id": "UNIT-02", "complete": False, "evidenced": False},
        ],
        "issuecomment-1",
        material,
        semantic,
        delta,
    )


class ContinuityV32Tests(unittest.TestCase):
    def test_start_changes_state_not_progress(self):
        snapshot = base()
        started = cp.event(snapshot, "implementation-start")
        self.assertEqual(started["state"], "IMPLEMENTING")
        self.assertEqual(started["progress"], snapshot["progress"])
        self.assertEqual(
            started["observability"]["update_reason"],
            "IMPLEMENTATION_START",
        )

    def test_evidence_cannot_lead_completion(self):
        with self.assertRaises(cp.ContinuityError):
            cp.progress([{"id": "A", "complete": False, "evidenced": True}])

    def test_material_ahead_visible_without_progress_credit(self):
        snapshot = base(delta=6)
        self.assertEqual(snapshot["frontier"]["relation"], "MATERIAL_AHEAD")
        self.assertEqual(snapshot["frontier"]["delta_commits"], 6)
        self.assertEqual(snapshot["progress"]["progress_percent"], 50)

    def test_stream_loss_requires_recovery_evidence(self):
        snapshot = cp.event(base(), "stream-loss")
        self.assertEqual(snapshot["state"], "RECOVERING")
        self.assertTrue(snapshot["recovery"]["recovery_evidence_required"])

    def test_third_loss_triggers_handover_once(self):
        snapshot = base()
        one = cp.event(snapshot, "stream-loss")
        two = cp.event(one, "stream-loss")
        three = cp.event(two, "stream-loss")
        four = cp.event(three, "stream-loss")
        self.assertFalse(one["recovery"]["plan_for_handover_now"])
        self.assertFalse(two["recovery"]["plan_for_handover_now"])
        self.assertTrue(three["recovery"]["plan_for_handover_now"])
        self.assertFalse(four["recovery"]["plan_for_handover_now"])

    def test_recovery_evidence_stays_pending_until_provider_readback(self):
        snapshot = cp.event(base(delta=6), "stream-loss")
        pending = cp.event(
            snapshot,
            "recovery-evidence",
            claim="Reconciled changed material.",
            not_yet_proved="Remaining regression suite.",
            open_work="UNIT-02",
            owner_decision="NONE",
            next="Run focused tests.",
        )
        self.assertEqual(pending["state"], "EVIDENCING")
        self.assertTrue(pending["recovery"]["recovery_evidence_required"])
        self.assertEqual(pending["frontier"]["relation"], "MATERIAL_AHEAD")
        self.assertIsNotNone(pending["recovery"]["recovery_evidence"])

    def test_recovery_sync_posts_and_reads_back_before_clearing(self):
        snapshot = cp.new_snapshot(
            "owner/repo#10",
            [{"id": "A", "complete": False, "evidenced": False}],
            "plan",
            "b",
            "a",
            1,
            "owner/repo",
            10,
        )
        snapshot = cp.event(snapshot, "stream-loss")
        snapshot = cp.event(snapshot, "recovery-evidence", claim="Recovered.")
        calls = []
        store = {
            "issue": {"title": "Task", "number": 10},
            "comments": [],
        }

        old_json = cp.gh_json
        old_patch = cp.gh_patch
        old_post = cp.gh_post
        old_comments = cp.gh_comments

        def fake_json(*args):
            endpoint = args[-1]
            calls.append(("GET", endpoint))
            if endpoint == "repos/owner/repo/issues/10":
                return dict(store["issue"])
            if endpoint.startswith("repos/owner/repo/issues/comments/"):
                cid = int(endpoint.rsplit("/", 1)[1])
                return next(row for row in store["comments"] if row["id"] == cid)
            raise AssertionError(endpoint)

        def fake_post(endpoint, payload):
            calls.append(("POST", endpoint))
            cid = 100 + len(store["comments"])
            row = {"id": cid, "body": payload["body"]}
            store["comments"].append(row)
            return dict(row)

        def fake_patch(endpoint, payload):
            calls.append(("PATCH", endpoint))
            if endpoint == "repos/owner/repo/issues/10":
                store["issue"]["title"] = payload["title"]
                return dict(store["issue"])
            cid = int(endpoint.rsplit("/", 1)[1])
            row = next(row for row in store["comments"] if row["id"] == cid)
            row.update(payload)
            return dict(row)

        def fake_comments(repo, issue):
            self.assertEqual((repo, issue), ("owner/repo", 10))
            return [dict(row) for row in store["comments"]]

        cp.gh_json = fake_json
        cp.gh_post = fake_post
        cp.gh_patch = fake_patch
        cp.gh_comments = fake_comments
        try:
            synced = cp.sync_github(snapshot)
        finally:
            cp.gh_json = old_json
            cp.gh_post = old_post
            cp.gh_patch = old_patch
            cp.gh_comments = old_comments

        recovery_rows = [
            row
            for row in store["comments"]
            if "TASK_EVIDENCE — RECOVERY" in row["body"]
        ]
        self.assertEqual(len(recovery_rows), 1)
        self.assertFalse(synced["recovery"]["recovery_evidence_required"])
        self.assertEqual(synced["state"], "IMPLEMENTING")
        self.assertEqual(synced["frontier"]["relation"], "ALIGNED")
        self.assertEqual(
            synced["frontier"]["semantic_evidence_head"],
            synced["frontier"]["material_head"],
        )
        self.assertEqual(
            synced["recovery"]["recovery_evidence"]["provider_comment_id"],
            recovery_rows[0]["id"],
        )
        recovery_post_index = calls.index(
            ("POST", "repos/owner/repo/issues/10/comments")
        )
        recovery_read_index = calls.index(
            (
                "GET",
                f"repos/owner/repo/issues/comments/{recovery_rows[0]['id']}",
            )
        )
        self.assertLess(recovery_post_index, recovery_read_index)

    def test_unit_progress_supports_p_e_divergence(self):
        snapshot = cp.event(
            base(),
            "unit-update",
            unit_id="UNIT-02",
            complete=True,
            evidenced=False,
        )
        self.assertEqual(snapshot["progress"]["progress_percent"], 100)
        self.assertEqual(snapshot["progress"]["evidence_percent"], 50)
        snapshot = cp.event(
            snapshot,
            "unit-update",
            unit_id="UNIT-02",
            evidenced=True,
        )
        self.assertEqual(snapshot["progress"]["evidence_percent"], 100)

    def test_scoped_result_prevents_false_completion(self):
        with self.assertRaises(cp.ContinuityError):
            cp.event(
                base(),
                "task-result",
                scope="STEP",
                coverage="1/2",
                responsibility_complete=True,
            )
        snapshot = cp.event(
            base(),
            "task-result",
            scope="RESPONSIBILITY",
            coverage="2/2",
            responsibility_complete=True,
        )
        self.assertEqual(snapshot["state"], "COMPLETE")

    def test_title_projection_is_cache(self):
        snapshot = cp.event(base(), "implementation-start")
        self.assertEqual(
            cp.title(snapshot, "Task {P1% · E1% · OLD · ACTIVE}"),
            "Task {P50% · E50% · UNIT-02 · IMPLEMENTING}",
        )

    def test_marked_comment_is_idempotent(self):
        rendered = cp.markdown(cp.event(base(), "implementation-start"))
        first = cp.marked("human", rendered)
        second = cp.marked(first, rendered)
        self.assertEqual(first, second)
        self.assertEqual(first.count(cp.START), 1)

    def test_git_frontier_is_derived(self):
        if not shutil.which("git"):
            self.skipTest("git unavailable")
        with tempfile.TemporaryDirectory() as td:
            repo = pathlib.Path(td)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "relay@example.invalid"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Relay Test"],
                check=True,
            )
            (repo / "a").write_text("1")
            subprocess.run(["git", "-C", str(repo), "add", "a"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "one"], check=True)
            first = subprocess.check_output(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                text=True,
            ).strip()
            (repo / "a").write_text("2")
            subprocess.run(["git", "-C", str(repo), "commit", "-qam", "two"], check=True)
            observed = cp.git_frontier(repo, first)
            self.assertEqual(observed["relation"], "MATERIAL_AHEAD")
            self.assertEqual(observed["delta_commits"], 1)

    def test_provider_failure_is_observability_only(self):
        snapshot = cp.new_snapshot(
            "owner/repo#10",
            [{"id": "A"}],
            "plan",
            "a",
            "a",
            0,
            "owner/repo",
            10,
        )
        old_json = cp.gh_json
        cp.gh_json = lambda *args, **kwargs: (_ for _ in ()).throw(
            cp.ContinuityError("offline")
        )
        try:
            out = cp.sync_github(cp.event(snapshot, "implementation-start"))
        finally:
            cp.gh_json = old_json
        self.assertEqual(
            out["observability"]["provider_sync"]["status"],
            "FAILED_OBSERVABILITY_ONLY",
        )
        self.assertFalse(
            out["observability"]["provider_sync_failure_blocks_engineering"]
        )


if __name__ == "__main__":
    unittest.main()
