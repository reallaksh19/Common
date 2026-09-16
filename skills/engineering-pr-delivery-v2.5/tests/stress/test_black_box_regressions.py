from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import good
from test_parallel_bootstrap import parallel_repo
from validate_projection_convergence import validate as projection
from validate_drift_receipt import validate as drift
from validate_owner_decision import validate_file as owner_decision
from validate_state_planes import validate as state_planes
from resolve_execution_route import resolve
from validate_checkpoint import validate_file as checkpoint


def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def required_projection(state="PENDING",execution_ref="EP-1",receipt=None,basis=None):
    return {"required":True,"state":state,"operation_id":"PROJ-OP-1","target":"issue:synthetic-active-handover","roadmap_revision":"RM-0001","execution_ref":execution_ref,"receipt":receipt,"basis":basis or []}

class BlackBoxRegressionTests(unittest.TestCase):
    def test_pending_required_projection_is_recoverable_but_not_handover_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root)
            s["projection"]=required_projection()
            s["relay_readiness"]={"baton_ready":True,"projection_ready":False,"handover_ready":False,"reasons":["Issue projection pending"]}
            dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],projection(root)[0])
            s["relay_readiness"]["handover_ready"]=True;dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("handover_ready" in x for x in projection(root)[0]))

    def test_published_unconfirmed_projection_survives_crash_without_duplicate_readiness(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root)
            s["projection"]=required_projection("PUBLISHED_UNCONFIRMED",receipt="external-receipt-17")
            s["relay_readiness"]={"baton_ready":True,"projection_ready":False,"handover_ready":False,"reasons":["Publication observed but not yet reconciled"]}
            dump(root/"agents/relay/REPO_STATE.yaml",s)
            errors,warnings=projection(root);self.assertEqual([],errors);self.assertTrue(any("operation_id" in x for x in warnings))
            self.assertEqual("PROJ-OP-1",s["projection"]["operation_id"])

    def test_in_sync_projection_requires_receipt_basis_and_current_execution_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,_,_,s=good(root)
            s["projection"]=required_projection("IN_SYNC",execution_ref="EP-OLD",receipt="external-receipt-17",basis=["verified:synthetic"])
            s["relay_readiness"]={"baton_ready":True,"projection_ready":True,"handover_ready":True,"reasons":[]}
            dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("execution_ref" in x for x in projection(root)[0]))
            s["projection"]["execution_ref"]="EP-1";s["projection"]["receipt"]=None;dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertTrue(any("receipt" in x for x in projection(root)[0]))

    def test_parallel_route_resolves_from_checked_out_branch_and_rejects_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_repo(root)
            result=resolve(root,branch="agent/lane-a",worktree="wt-a")
            self.assertEqual("EP-A",result["ep_id"]);self.assertEqual("LANE-A",result["lane_id"])
            with self.assertRaises(ValueError):resolve(root,branch="agent/unknown",worktree="unknown")

    def test_disjoint_drift_receipt_can_preserve_ep_but_overlap_removes_write_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,s=good(root)
            receipt={"schema_version":"relay-v2.5-drift","from_base":"base-1","to_base":"base-2","classification":"DISJOINT","changed_paths":["docs/unrelated.md"],"affected_scope":[],"rationale":"Observed base drift changes only an unrelated domain.","qualification":{"basis":[],"confirmation":"NOT_REQUIRED","confirmation_basis":[]}}
            dump(root/"agents/relay/drift/DRIFT-1.yaml",receipt);ep["git_basis"]["drift_receipt"]="agents/relay/drift/DRIFT-1.yaml";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertEqual([],drift(root)[0])
            receipt["classification"]="OVERLAPPING";receipt["affected_scope"]=["src/a.py"];receipt["qualification"]={"basis":[],"confirmation":"REQUIRED","confirmation_basis":[]};dump(root/"agents/relay/drift/DRIFT-1.yaml",receipt)
            self.assertTrue(any("material_authority WRITE is invalid" in x for x in drift(root)[0]))
            s["status_planes"]["execution"]["material_authority"]="READ_ONLY";dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],drift(root)[0])

    def test_qualified_boundary_drift_requires_confirmation_before_write(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,ep,_,s=good(root)
            receipt={"schema_version":"relay-v2.5-drift","from_base":"base-1","to_base":"base-2","classification":"WITHIN_QUALIFIED_BOUNDARY","changed_paths":["src/adjacent.py"],"affected_scope":["adjacent subsystem"],"rationale":"Material drift does not change the bounded production trace, invariants, or verification contract.","qualification":{"basis":["QSCOPE-1"],"confirmation":"DEFERRED_PENDING","confirmation_basis":["ODR-DEF-1"]}}
            dump(root/"agents/relay/drift/DRIFT-2.yaml",receipt);ep["git_basis"]["drift_receipt"]="agents/relay/drift/DRIFT-2.yaml";dump(root/"agents/relay/execution-packages/EP-1.yaml",ep)
            self.assertTrue(any("material_authority must be READ_ONLY" in x for x in drift(root)[0]))
            s["status_planes"]["execution"].update({"material_authority":"READ_ONLY","can_continue":True,"next_action":"Perform read-only reconciliation while confirmation remains pending."});dump(root/"agents/relay/REPO_STATE.yaml",s)
            self.assertEqual([],drift(root)[0]);self.assertEqual([],state_planes(root)[0])

    def test_owner_deferral_does_not_satisfy_requirement_or_grant_write_authority(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"ODR.yaml"
            odr={"schema_version":"relay-v2.5","id":"ODR-DEF-1","decision":{"authority":"OWNER","kind":"DEFERRAL","statement":"Defer independent confirmation to a later relay leg.","source":"owner-message:synthetic"},"effects":{"requirement_disposition":"PENDING_NOT_SATISFIED","grants_material_write_authority":False,"pending_items":["CONFIRM-1"]},"impact":{"class":["LOCAL"]},"affected":{"objectives":[],"phases":[],"work_packages":[],"execution_packages":[],"issues":[]},"required_reconciliation":[],"status":"APPLIED"}
            dump(path,odr);self.assertEqual([],owner_decision(path)[0])
            odr["effects"]["requirement_disposition"]="SATISFIED";odr["effects"]["grants_material_write_authority"]=True;dump(path,odr)
            errors=owner_decision(path)[0];self.assertTrue(any("PENDING_NOT_SATISFIED" in x for x in errors));self.assertTrue(any("must not grant" in x for x in errors))

    def test_checkpoint_pass_evidence_must_match_exact_material_basis(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"CP.yaml"
            cp={"schema_version":"relay-v2.5","checkpoint_id":"CP-1","ep_id":"EP-1","roadmap_basis":{"roadmap_id":"RM","revision":"RM-1"},"execution_basis":{"material_ref":"head-A"},"implementation_result":{},"acceptance_results":[],"validation_results":[{"id":"TEST-1","status":"PASS","basis_ref":"head-B"}],"quality_findings":[],"discoveries":[],"roadmap_reconciliation":{"result":"NO_ROADMAP_CHANGE"},"successor":{"mode":"NONE","frontier_work_package":None,"ep_id":None,"parallel_plan":None,"lanes":[]}}
            dump(path,cp);self.assertTrue(any("basis_ref" in x for x in checkpoint(path)[0]))
            cp["validation_results"][0]["basis_ref"]="head-A";dump(path,cp);self.assertEqual([],checkpoint(path)[0])

if __name__=="__main__":unittest.main()
