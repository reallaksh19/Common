import importlib.util
import pathlib
import shutil
import subprocess
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "continuity_projection.py"
spec = importlib.util.spec_from_file_location("continuity_projection", MODULE_PATH)
cp = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(cp)

def base(material="b", semantic="a", delta=1):
    return cp.new_snapshot("owner/repo#10", [{"id":"UNIT-01","complete":True,"evidenced":True},{"id":"UNIT-02","complete":False,"evidenced":False}], "issuecomment-1", material, semantic, delta)

class ContinuityV32Tests(unittest.TestCase):
    def test_start_changes_state_not_progress(self):
        s = base(); started = cp.event(s, "implementation-start")
        self.assertEqual(started["state"], "IMPLEMENTING")
        self.assertEqual(started["progress"], s["progress"])
        self.assertEqual(started["observability"]["update_reason"], "IMPLEMENTATION_START")

    def test_evidence_cannot_lead_completion(self):
        with self.assertRaises(cp.ContinuityError):
            cp.progress([{"id":"A","complete":False,"evidenced":True}])

    def test_material_ahead_visible_without_progress_credit(self):
        s = base(delta=6)
        self.assertEqual(s["frontier"]["relation"], "MATERIAL_AHEAD")
        self.assertEqual(s["frontier"]["delta_commits"], 6)
        self.assertEqual(s["progress"]["progress_percent"], 50)

    def test_stream_loss_requires_recovery_evidence(self):
        s = cp.event(base(), "stream-loss")
        self.assertEqual(s["state"], "RECOVERING")
        self.assertTrue(s["recovery"]["recovery_evidence_required"])

    def test_third_loss_triggers_handover_once(self):
        s = base(); one = cp.event(s,"stream-loss"); two = cp.event(one,"stream-loss")
        three = cp.event(two,"stream-loss"); four = cp.event(three,"stream-loss")
        self.assertFalse(one["recovery"]["plan_for_handover_now"])
        self.assertFalse(two["recovery"]["plan_for_handover_now"])
        self.assertTrue(three["recovery"]["plan_for_handover_now"])
        self.assertFalse(four["recovery"]["plan_for_handover_now"])

    def test_recovery_evidence_aligns_frontier(self):
        s = cp.event(base(delta=6), "stream-loss")
        s = cp.event(s, "recovery-evidence", semantic_head="b", delta=0)
        self.assertFalse(s["recovery"]["recovery_evidence_required"])
        self.assertEqual(s["frontier"]["relation"], "ALIGNED")
        self.assertEqual(s["state"], "IMPLEMENTING")

    def test_unit_progress_supports_p_e_divergence(self):
        s = cp.event(base(), "unit-update", unit_id="UNIT-02", complete=True, evidenced=False)
        self.assertEqual(s["progress"]["progress_percent"], 100)
        self.assertEqual(s["progress"]["evidence_percent"], 50)
        s = cp.event(s, "unit-update", unit_id="UNIT-02", evidenced=True)
        self.assertEqual(s["progress"]["evidence_percent"], 100)

    def test_scoped_result_prevents_false_completion(self):
        with self.assertRaises(cp.ContinuityError):
            cp.event(base(), "task-result", scope="STEP", coverage="1/2", responsibility_complete=True)
        s = cp.event(base(), "task-result", scope="RESPONSIBILITY", coverage="2/2", responsibility_complete=True)
        self.assertEqual(s["state"], "COMPLETE")

    def test_title_projection_is_cache(self):
        s = cp.event(base(), "implementation-start")
        self.assertEqual(cp.title(s, "Task {P1% · E1% · OLD · ACTIVE}"), "Task {P50% · E50% · UNIT-02 · IMPLEMENTING}")

    def test_marked_comment_is_idempotent(self):
        md = cp.markdown(cp.event(base(),"implementation-start"))
        a = cp.marked("human", md); b = cp.marked(a, md)
        self.assertEqual(a,b); self.assertEqual(a.count(cp.START),1)

    def test_git_frontier_is_derived(self):
        if not shutil.which("git"): self.skipTest("git unavailable")
        with tempfile.TemporaryDirectory() as td:
            repo = pathlib.Path(td); subprocess.run(["git","init","-q",str(repo)],check=True)
            subprocess.run(["git","-C",str(repo),"config","user.email","relay@example.invalid"],check=True)
            subprocess.run(["git","-C",str(repo),"config","user.name","Relay Test"],check=True)
            (repo/"a").write_text("1"); subprocess.run(["git","-C",str(repo),"add","a"],check=True)
            subprocess.run(["git","-C",str(repo),"commit","-qm","one"],check=True)
            first=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
            (repo/"a").write_text("2"); subprocess.run(["git","-C",str(repo),"commit","-qam","two"],check=True)
            f=cp.git_frontier(repo, first)
            self.assertEqual(f["relation"],"MATERIAL_AHEAD"); self.assertEqual(f["delta_commits"],1)

    def test_provider_failure_is_observability_only(self):
        s = cp.new_snapshot("owner/repo#10",[{"id":"A"}],"plan","a","a",0,"owner/repo",10)
        old = cp.gh_json
        cp.gh_json = lambda *a, **k: (_ for _ in ()).throw(cp.ContinuityError("offline"))
        try: out = cp.sync_github(cp.event(s,"implementation-start"))
        finally: cp.gh_json = old
        self.assertEqual(out["observability"]["provider_sync"]["status"],"FAILED_OBSERVABILITY_ONLY")
        self.assertFalse(out["observability"]["provider_sync_failure_blocks_engineering"])

if __name__ == "__main__":
    unittest.main()
