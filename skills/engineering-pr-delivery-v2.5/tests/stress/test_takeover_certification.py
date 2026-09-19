from __future__ import annotations
import subprocess,sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import good,dump
from test_parallel_bootstrap import parallel_repo
from relaylib import load_yaml
from takeoverlib import current_routes,expected_basis,route_key
from validate_baton_readiness import validate as baton_readiness
from validate_discovery_receipt import validate_file as discovery_file
from validate_takeover_certification import validate as takeover,is_takeover_certified
from material_write_ready import evaluate as write_ready
from cold_start_check import validate as cold_start


def route_shape(route):
    return {"route_key":route_key(route),"mode":route.get("mode"),"execution_ref":route.get("execution_ref"),"ep_id":route.get("ep_id"),"ep_path":route.get("ep_path"),"plan_id":route.get("plan_id"),"plan_path":route.get("plan_path"),"lane_id":route.get("lane_id")}


def attach_takeover(root:Path,route=None,candidate="agent-B",preparer="agent-A",disc_id="DISC-1",tc_id="TC-1"):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");route=route or current_routes(root,state)[0];basis=expected_basis(root,state,route);ep=load_yaml(root/route["ep_path"])
    steps=[]
    for instruction in ep.get("repository_discovery",[]) or []:
        if instruction.get("receipt_required") is not True:continue
        outputs=[{"name":name,"value":f"observed {name}","basis":[f"repo:{route['ep_path']}#{instruction['id']}"]} for name in instruction.get("expected_outputs",[]) or []]
        steps.append({"id":instruction["id"],"status":"PASS","outputs":outputs,"basis":[f"repository discovery {instruction['id']}"]})
    disc={"schema_version":"relay-v2.5-discovery","id":disc_id,"candidate":{"agent_instance_id":candidate},"route":route_shape(route),"basis":{k:basis[k] for k in ("roadmap_id","roadmap_revision","relay_protocol_basis_ref","material_ref","ep_contract_digest","repo_profile_digest","predecessor_baton")},"steps":steps,"result":"PASS","conversation_context_used":False}
    disc_path=f"agents/relay/certifications/discovery/{disc_id}.yaml";dump(root/disc_path,disc)
    tc={"schema_version":"relay-v2.5-takeover-certification","id":tc_id,"candidate":{"agent_instance_id":candidate},"prepared_by":{"agent_instance_id":preparer},"evaluated_by":{"type":"DETERMINISTIC_VALIDATOR","identity":"validate_takeover_certification.py","basis":["semantic validators and exact receipt basis"]},"self_certification":{"allowed":False},"route":route_shape(route),"basis":{k:basis[k] for k in ("roadmap_id","roadmap_revision","relay_protocol_basis_ref","material_ref","ep_contract_digest","repo_profile_digest","predecessor_baton")},"discovery_receipt":{"id":disc_id,"path":disc_path},"qualification":{"required":False,"status":"NOT_REQUIRED","receipt_id":None,"receipt_path":None},"checks":{"baton_semantics":"PASS","repository_discovery":"PASS","route_grounding":"PASS","input_oracle_readiness":"PASS","scope_understood":"PASS","report_successor_contract":"PASS"},"result":"PASS","conversation_context_used":False}
    tc_path=f"agents/relay/certifications/takeover/{tc_id}.yaml";dump(root/tc_path,tc)
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");state.setdefault("takeover_admissions",[]).append({"route_key":route_key(route),"candidate":{"agent_instance_id":candidate},"discovery_receipt":{"id":disc_id,"path":disc_path},"certification":{"id":tc_id,"path":tc_path}});dump(root/"agents/relay/REPO_STATE.yaml",state)
    return disc,tc,route


def git(root:Path,*args):return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


class TakeoverCertificationStressTests(unittest.TestCase):
    def test_baton_can_be_ready_before_any_candidate_exists(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            self.assertEqual([],baton_readiness(root)[0]);state=load_yaml(root/"agents/relay/REPO_STATE.yaml");self.assertTrue(state["relay_readiness"]["baton_ready"]);self.assertEqual([],state["takeover_admissions"])
            route=current_routes(root,state)[0];certified,_=is_takeover_certified(root,route,"agent-B");self.assertFalse(certified)

    def test_zero_context_candidate_can_be_independently_certified(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);attach_takeover(root)
            self.assertEqual([],takeover(root)[0]);self.assertEqual([],baton_readiness(root)[0]);self.assertEqual([],cold_start(root)[0])
            route=current_routes(root,load_yaml(root/"agents/relay/REPO_STATE.yaml"))[0];certified,errors=is_takeover_certified(root,route,"agent-B");self.assertTrue(certified,errors)

    def test_candidate_may_assemble_own_tc_when_deterministically_evaluated(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);attach_takeover(root,candidate="agent-B",preparer="agent-B")
            self.assertEqual([],takeover(root)[0])

    def test_candidate_cannot_be_its_own_independent_tc_evaluator(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);_,tc,_=attach_takeover(root,candidate="agent-B",preparer="agent-B")
            tc["evaluated_by"]={"type":"INDEPENDENT_AGENT","identity":"agent-B","basis":["candidate cannot independently evaluate itself"]}
            path=root/"agents/relay/certifications/takeover/TC-1.yaml";dump(path,tc)
            self.assertTrue(any("independent evaluator cannot be the candidate" in x for x in takeover(root)[0]))

    def test_ep_contract_change_invalidates_existing_certification(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);attach_takeover(root);ep_path=root/"agents/relay/execution-packages/EP-1.yaml";ep=load_yaml(ep_path);ep["inputs"][0]["description"]="Changed contract meaning after certification";dump(ep_path,ep)
            self.assertTrue(any("ep_contract_digest" in x for x in takeover(root)[0]))

    def test_discovery_receipt_must_cover_exact_expected_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);disc,_,route=attach_takeover(root);disc["steps"][0]["outputs"]=disc["steps"][0]["outputs"][:1];path=root/"agents/relay/certifications/discovery/DISC-1.yaml";dump(path,disc)
            errors=discovery_file(root,path,load_yaml(root/"agents/relay/REPO_STATE.yaml"),route,"agent-B")[0];self.assertTrue(any("exactly cover" in x for x in errors))

    def test_qualification_boundary_cannot_be_bypassed_by_tc(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);ep_path=root/"agents/relay/execution-packages/EP-1.yaml";ep=load_yaml(ep_path);ep["qualification_boundary"]={"required":True};dump(ep_path,ep);attach_takeover(root)
            self.assertTrue(any("incoming EP requires qualification but TC does not" in x for x in takeover(root)[0]))

    def test_parallel_certification_is_route_scoped(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_repo(root);state=load_yaml(root/"agents/relay/REPO_STATE.yaml");routes=current_routes(root,state);attach_takeover(root,routes[0],"agent-B","agent-A","DISC-A","TC-A");attach_takeover(root,routes[1],"agent-C","agent-A","DISC-B","TC-B")
            self.assertEqual([],takeover(root)[0]);state=load_yaml(root/"agents/relay/REPO_STATE.yaml");routes=current_routes(root,state);self.assertTrue(is_takeover_certified(root,routes[0],"agent-B")[0]);self.assertFalse(is_takeover_certified(root,routes[0],"agent-C")[0]);self.assertTrue(is_takeover_certified(root,routes[1],"agent-C")[0])

    def test_material_write_ready_is_live_and_candidate_specific(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            subprocess.check_call(["git","-C",str(root),"init","-b","main"],stdout=subprocess.DEVNULL);git(root,"config","user.email","synthetic@example.test");git(root,"config","user.name","Synthetic Relay");git(root,"add",".");git(root,"commit","-m","base")
            base=git(root,"rev-parse","HEAD");git(root,"checkout","-b","agent/test")
            ep_path=root/"agents/relay/execution-packages/EP-1.yaml";ep=load_yaml(ep_path);ep["identity"]["base_ref"]=base;ep["git_basis"]["material_ref"]=base;ep["git_basis"]["base_observed_ref"]=base;dump(ep_path,ep);git(root,"add",str(ep_path.relative_to(root)));git(root,"commit","-m","bind material basis")
            before=write_ready(root,"agent-B",branch="agent/test",worktree=str(root));self.assertFalse(before["material_write_ready"]);self.assertFalse(before["candidate_certified"]);self.assertEqual("WRITE",before["route_material_authority"])
            attach_takeover(root,candidate="agent-B",preparer="agent-B");out=write_ready(root,"agent-B",branch="agent/test",worktree=str(root));self.assertTrue(out["material_write_ready"],out);self.assertTrue(out["candidate_certified"]);self.assertEqual("WRITE",out["route_material_authority"])
            wrong=write_ready(root,"agent-C",branch="agent/test",worktree=str(root));self.assertFalse(wrong["material_write_ready"])
            state=load_yaml(root/"agents/relay/REPO_STATE.yaml");state["status_planes"]["stop"]={"active":True,"category":"OWNER_DECISION_REQUIRED","reason":"Synthetic stop","basis":["ODR-X"]};state["status_planes"]["execution"]["can_continue"]=False;state["status_planes"]["execution"]["material_authority"]="READ_ONLY";dump(root/"agents/relay/REPO_STATE.yaml",state);stopped=write_ready(root,"agent-B",branch="agent/test",worktree=str(root));self.assertFalse(stopped["material_write_ready"])

if __name__=="__main__":unittest.main()
