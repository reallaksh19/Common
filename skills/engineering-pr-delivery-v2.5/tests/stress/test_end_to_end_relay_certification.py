from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import good,dump,semantic_ep,quality_contract
from test_parallel_bootstrap import parallel_repo
from test_roadmap_continuity import continuity_repo
from test_projection_generation_recovery import stale_projection,readiness
from test_takeover_certification import attach_takeover
from relaylib import load_yaml
from takeoverlib import yaml_digest,current_routes
from qualitylib import router_snapshot
from cold_start_check import validate as cold_start
from validate_takeover_certification import validate as takeover,is_takeover_certified
from validate_zero_context_reconstruction import validate as zero_context
from zero_context_reconstruction import build as reconstruct


def attach_clear_qrv(root:Path,ep_id:str,qid:str):
    ep_path=root/f"agents/relay/execution-packages/{ep_id}.yaml";ep=load_yaml(ep_path);qpath=root/f"agents/relay/quality/{qid}.yaml"
    applicable=[x.get("blueprint") for x in (ep.get("quality") or {}).get("applicable",[]) or []]
    qrv={"schema_version":"relay-v2.5-quality-review","quality_review_id":qid,"ep":{"id":ep_id,"path":str(ep_path.relative_to(root)),"contract_digest":yaml_digest(ep_path)},"roadmap_revision":(ep.get("roadmap_source") or {}).get("roadmap_revision"),"material_ref":(ep.get("git_basis") or {}).get("material_ref"),"reviewer":{"type":"DETERMINISTIC_VALIDATOR","identity":"wp09-synthetic-quality"},"router_snapshot":router_snapshot(ep),"procedure_results":[{"blueprint":bp,"result":"CLEAR","evidence":[f"{bp} clear on synthetic relay basis"]} for bp in applicable],"findings":[],"overall_state":"CLEAR","execution_effect":{"blocks_execution":False,"blocking_findings":[]},"owner_report":{"summary":"Applicable procedures are clear for relay handoff.","visible_risks":[],"decisions_required":[]},"successor_handover":{"unresolved_findings":[],"follow_up":[]}}
    dump(qpath,qrv);return {"id":qid,"path":str(qpath.relative_to(root)),"digest":yaml_digest(qpath)}


def handoff_same_frontier(root:Path,cp_id:str,next_ep_id:str):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");active=state["active_ep"];from_ep_id=active["id"];from_ep=load_yaml(root/active["path"]);qptr=attach_clear_qrv(root,from_ep_id,f"QRV-{cp_id}")
    material=(from_ep.get("git_basis") or {}).get("material_ref")
    cp={"schema_version":"relay-v2.5","checkpoint_id":cp_id,"ep_id":from_ep_id,"roadmap_basis":{"roadmap_id":(from_ep.get("roadmap_source") or {}).get("roadmap_id"),"revision":(from_ep.get("roadmap_source") or {}).get("roadmap_revision")},"execution_basis":{"material_ref":material},"implementation_result":{"summary":f"{from_ep_id} completed its bounded handoff slice."},"acceptance_results":[{"id":"AC-1","status":"IN_PROGRESS","basis_ref":material}],"validation_results":[{"id":"TEST-1","status":"PASS","basis_ref":material}],"quality_review":qptr,"quality_findings":[],"discoveries":[],"known_limitations":[],"remaining_work":["Continue the same roadmap frontier under the successor EP."],"roadmap_reconciliation":{"result":"NO_ROADMAP_CHANGE"},"successor":{"mode":"SERIAL","frontier_work_package":"WP-1","ep_id":next_ep_id,"parallel_plan":None,"lane_id":None,"lanes":[]}}
    cp_path=root/f"agents/relay/checkpoints/{cp_id}.yaml";dump(cp_path,cp)
    successor=semantic_ep(next_ep_id,wp="WP-1");successor["identity"]["previous_checkpoint"]=cp_id;successor["context_capsule"]["current_implementation_state"]=f"Predecessor {from_ep_id} checkpointed durable partial progress in {cp_id}.";successor["context_capsule"]["known_problems"]=["The remaining bounded implementation step is not yet complete."]
    ep_path=root/f"agents/relay/execution-packages/{next_ep_id}.yaml";dump(ep_path,successor)
    state["active_ep"]={"id":next_ep_id,"path":str(ep_path.relative_to(root)),"state":"ACTIVE"};state["last_checkpoint"]={"id":cp_id,"path":str(cp_path.relative_to(root))};state["takeover_admissions"]=[];state["projection"]["execution_ref"]=next_ep_id;state["status_planes"]["evidence"]={"state":"PARTIAL","summary":f"{cp_id} retained predecessor evidence; successor work remains.","not_run":[]};state["status_planes"]["execution"]["next_action"]="Execute the successor EP from repository state only.";dump(root/"agents/relay/REPO_STATE.yaml",state)
    progress=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml");progress.setdefault("execution_packages",[]).append({"id":next_ep_id,"earned_weight":50,"total_weight":100,"percent":50});dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress)
    return cp,successor


def make_idle(root:Path):
    roadmap,ep,progress,state=good(root);wp=roadmap["objectives"][0]["phases"][0]["work_packages"][0];wp["state"]="PLANNED";wp["definition"]="OWNER_REVIEW_REQUIRED";wp["execution_status"]="WAITING"
    state["relay_state"]="IDLE";state["active_ep"]={"id":"NONE","path":None,"state":"NONE"};state["current_position"]["work_package"]="NONE";state["takeover_admissions"]=[];state["status_planes"]["execution"]={"state":"IDLE","can_continue":False,"material_authority":"NONE","next_action":"Wait for the roadmap work package to become sufficiently defined."};state["projection"]["execution_ref"]="NONE";state["progress"]["ep_percent"]=0;state["relay_readiness"]={"baton_ready":True,"projection_ready":True,"handover_ready":True,"reasons":[]}
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/REPO_STATE.yaml",state)


def make_terminal(root:Path):
    roadmap,ep,progress,state=good(root);obj=roadmap["objectives"][0];phase=obj["phases"][0];wp=phase["work_packages"][0];obj["state"]="COMPLETE";phase["state"]="COMPLETE";wp["state"]="COMPLETE";wp["execution_status"]="TERMINAL"
    progress["overall"].update({"earned_weight":100,"percent":100});progress["objectives"][0].update({"earned_weight":100,"percent":100});progress["phases"][0].update({"earned_weight":100,"percent":100});progress["work_packages"][0].update({"earned_weight":100,"percent":100});progress["execution_packages"][0].update({"earned_weight":100,"percent":100});progress["implementation_steps"][0].update({"earned_weight":100,"percent":100});progress["acceptance_criteria"][0].update({"status":"COMPLETE","earned_weight":100,"percent":100})
    state["relay_state"]="TERMINAL";state["active_ep"]={"id":"NONE","path":None,"state":"NONE"};state["current_position"]["work_package"]="NONE";state["takeover_admissions"]=[];state["progress"].update({"overall_percent":100,"phase_percent":100,"ep_percent":0});state["status_planes"]["execution"]={"state":"COMPLETE","can_continue":False,"material_authority":"NONE","next_action":"No material work remains; preserve terminal evidence."};state["status_planes"]["evidence"]={"state":"COMPLETE","summary":"All synthetic roadmap work is complete.","not_run":[]};state["projection"]["execution_ref"]="NONE";state["relay_readiness"]={"baton_ready":True,"projection_ready":True,"handover_ready":True,"reasons":[]}
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/REPO_STATE.yaml",state)


class EndToEndRelayCertificationTests(unittest.TestCase):
    def test_agent_a_to_b_to_c_zero_chat_relay(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            handoff_same_frontier(root,"CP-A","EP-B")
            self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0])
            b_view=reconstruct(root)["routes"][0];self.assertEqual("CP-A",(b_view["predecessor_established"] or {}).get("checkpoint_id"));self.assertTrue(b_view["input_authority_editability"]);self.assertTrue(b_view["benchmarks_oracles"]);self.assertTrue(b_view["first_implementation_action"])
            attach_takeover(root,candidate="agent-B",preparer="agent-A",disc_id="DISC-B",tc_id="TC-B");self.assertEqual([],takeover(root)[0]);route=current_routes(root,load_yaml(root/"agents/relay/REPO_STATE.yaml"))[0];self.assertTrue(is_takeover_certified(root,route,"agent-B")[0])
            handoff_same_frontier(root,"CP-B","EP-C")
            self.assertEqual([],cold_start(root)[0]);c_view=reconstruct(root)["routes"][0];self.assertEqual("CP-B",(c_view["predecessor_established"] or {}).get("checkpoint_id"));self.assertFalse(reconstruct(root)["conversation_context_required"])
            self.assertTrue(c_view["why_task_exists"]);self.assertIn("roadmap_position",c_view);self.assertIn("owner_decisions",c_view);self.assertTrue(c_view["remaining_uncertain"]);self.assertTrue(c_view["input_authority_editability"]);self.assertTrue(c_view["benchmarks_oracles"]);self.assertTrue(c_view["scope"]["protected"]);self.assertTrue(c_view["evidence"]);self.assertTrue(c_view["tests_required"]);self.assertTrue(c_view["acceptance"]);self.assertTrue(c_view["first_implementation_action"]);self.assertTrue(c_view["stale_conditions"]);self.assertTrue(c_view["next_work"])
            attach_takeover(root,candidate="agent-C",preparer="agent-B",disc_id="DISC-C",tc_id="TC-C");self.assertEqual([],takeover(root)[0]);route=current_routes(root,load_yaml(root/"agents/relay/REPO_STATE.yaml"))[0];self.assertTrue(is_takeover_certified(root,route,"agent-C")[0]);self.assertEqual([],cold_start(root)[0])

    def test_lifecycle_cold_start_certification_matrix(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root);self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0])
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);continuity_repo(root,disposition="RECONCILE_REQUIRED",changed=True);self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0]);self.assertEqual("RECONCILING",reconstruct(root)["active_ep_state"])
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);parallel_repo(root);self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0]);self.assertEqual(2,len(reconstruct(root)["routes"]))
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);continuity_repo(root);state=load_yaml(root/"agents/relay/REPO_STATE.yaml");state["projection"]=stale_projection();state["relay_readiness"]=readiness(False);state["relay_readiness"]["reasons"]=["External projection is stale"];dump(root/"agents/relay/REPO_STATE.yaml",state);self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0]);self.assertEqual("STALE",reconstruct(root)["projection"]["state"])
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);make_idle(root);self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0]);self.assertTrue(reconstruct(root)["no_active_work"])
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);make_terminal(root);self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0]);self.assertTrue(reconstruct(root)["no_active_work"])

if __name__=="__main__":unittest.main()
