from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import good
from test_parallel_bootstrap import parallel_repo
from validate_projection_convergence import validate as projection
from validate_drift_receipt import validate as drift
from resolve_execution_route import resolve
from validate_checkpoint import validate_file as checkpoint


def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

class BlackBoxRegressionTests(unittest.TestCase):
    def test_pending_required_projection_is_recoverable_but_not_handover_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root)
            s["projection"]={"required":True,"state":"PENDING","roadmap_revision":"RM-0001","execution_ref":"EP-1","basis":[]}
            s["relay_readiness"]={"repository_ready":True,"projection_ready":False,"handover_ready":False,"reasons":["Issue projection pending"]}
            dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],projection(root)[0])
            s["relay_readiness"]["handover_ready"]=True;dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("handover_ready" in x for x in projection(root)[0]))

    def test_in_sync_projection_must_bind_current_execution_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root)
            s["projection"]={"required":True,"state":"IN_SYNC","roadmap_revision":"RM-0001","execution_ref":"EP-OLD","basis":["issue-comment:synthetic"]}
            s["relay_readiness"]={"repository_ready":True,"projection_ready":True,"handover_ready":True,"reasons":[]}
            dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("execution_ref" in x for x in projection(root)[0]))

    def test_parallel_route_resolves_from_checked_out_branch_and_rejects_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_repo(root)
            result=resolve(root,branch="agent/lane-a",worktree="wt-a")
            self.assertEqual("EP-A",result["ep_id"]);self.assertEqual("LANE-A",result["lane_id"])
            with self.assertRaises(ValueError):resolve(root,branch="agent/unknown",worktree="unknown")

    def test_disjoint_drift_receipt_can_preserve_ep_but_overlap_invalidates_it(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,_=good(root)
            receipt={"schema_version":"relay-v2.5-drift","from_base":"base-1","to_base":"base-2","classification":"DISJOINT","changed_paths":["docs/unrelated.md"],"affected_scope":[],"rationale":"Observed base drift changes only an unrelated domain."}
            dump(root/"agents/relay/drift/DRIFT-1.yaml",receipt);ep["git_basis"]["drift_receipt"]="agents/relay/drift/DRIFT-1.yaml";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertEqual([],drift(root)[0])
            receipt["classification"]="OVERLAPPING";receipt["affected_scope"]=["src/a.py"];dump(root/"agents/relay/drift/DRIFT-1.yaml",receipt)
            self.assertTrue(any("must be reconciled" in x for x in drift(root)[0]))

    def test_checkpoint_pass_evidence_must_match_exact_material_basis(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"CP.yaml"
            cp={"schema_version":"relay-v2.5","checkpoint_id":"CP-1","ep_id":"EP-1","roadmap_basis":{"roadmap_id":"RM","revision":"RM-1"},"execution_basis":{"material_ref":"head-A"},"implementation_result":{},"acceptance_results":[],"validation_results":[{"id":"TEST-1","status":"PASS","basis_ref":"head-B"}],"quality_findings":[],"discoveries":[],"roadmap_reconciliation":{"result":"NO_ROADMAP_CHANGE"},"successor":{"mode":"NONE","frontier_work_package":None,"ep_id":None,"parallel_plan":None,"lanes":[]}}
            dump(path,cp);self.assertTrue(any("basis_ref" in x for x in checkpoint(path)[0]))
            cp["validation_results"][0]["basis_ref"]="head-A";dump(path,cp);self.assertEqual([],checkpoint(path)[0])

if __name__=="__main__":unittest.main()
