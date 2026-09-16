from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parent))
from resolve_execution_route import resolve
from test_parallel_replan import parallel_replan_repo


class ParallelReplanRoutingStressTests(unittest.TestCase):
    def test_superseded_parallel_plan_branch_cannot_resolve_after_replan(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_replan_repo(root)
            with self.assertRaisesRegex(ValueError,"matched \\[\\]"):
                resolve(root,branch="agent/lane-b",worktree=None)

    def test_superseded_parallel_plan_worktree_cannot_resolve_after_replan(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_replan_repo(root)
            with self.assertRaisesRegex(ValueError,"matched \\[\\]"):
                resolve(root,branch=None,worktree="/tmp/wt-b")

    def test_only_new_parallel_plan_lane_is_returned(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_replan_repo(root)
            route=resolve(root,branch="agent/lane-b1",worktree=None)
            self.assertEqual("PLAN-P2",route["plan_id"])
            self.assertEqual("LANE-B1",route["lane_id"])
            self.assertEqual("EP-B1",route["ep_id"])

if __name__=="__main__":unittest.main()
