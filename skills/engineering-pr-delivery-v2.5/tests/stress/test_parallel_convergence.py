from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parent))
from test_parallel_bootstrap import parallel_repo,ep,dump
from validate_parallel_join import validate as parallel_join
from validate_checkpoint_linkage import validate as checkpoint_linkage
from cold_start_check import validate as cold_start

def lane_cp(cp_id,ep_id,lane_id,plan_id="PLAN-P1"):
    return {"schema_version":"relay-v2.5","checkpoint_id":cp_id,"ep_id":ep_id,"roadmap_basis":{"roadmap_id":"RM-P","revision":"RM-1"},"execution_basis":{"material_ref":"abc"},"implementation_result":{"completed_steps":["STEP-1"],"files_changed":[]},"acceptance_results":[],"validation_results":[],"quality_findings":[],"discoveries":[],"roadmap_reconciliation":{"result":"STATUS_UPDATE"},"successor":{"mode":"JOIN","frontier_work_package":None,"ep_id":None,"parallel_plan":plan_id,"lane_id":lane_id,"lanes":[]}}
def converge(root:Path):
    roadmap,plan,state=parallel_repo(root);phase=roadmap["objectives"][0]["phases"][0];a,b,integrate=phase["work_packages"];a["state"]="COMPLETE";a["execution_status"]="TERMINAL";b["state"]="COMPLETE";b["execution_status"]="TERMINAL";integrate["state"]="ACTIVE";integrate["execution_status"]="ACTIVE";integration_ep=ep("EP-I","agent/integration","WP-I","src/integration");integration_ep["identity"]["previous_join"]="JOIN-P1"
    join={"schema_version":"relay-v2.5","id":"JOIN-P1","parallel_plan":{"id":"PLAN-P1","path":"agents/relay/parallel/PLAN-P1.yaml"},"roadmap_revision":"RM-1","lane_checkpoints":[{"lane_id":"LANE-A","work_package":"WP-A","checkpoint_id":"CP-A","checkpoint_path":"agents/relay/checkpoints/CP-A.yaml"},{"lane_id":"LANE-B","work_package":"WP-B","checkpoint_id":"CP-B","checkpoint_path":"agents/relay/checkpoints/CP-B.yaml"}],"integration":{"work_package":"WP-I","ep_id":"EP-I","ep_path":"agents/relay/execution-packages/EP-I.yaml"},"state":"READY"}
    state["relay_state"]="ACTIVE";state["current_position"]={"objective":"OBJ","phase":"PHASE","work_package":"WP-I","work_packages":[]};state["execution_policy"]={"mode":"SERIAL"};state["active_ep"]={"id":"EP-I","path":"agents/relay/execution-packages/EP-I.yaml","state":"ACTIVE"};state["last_checkpoint"]={"id":"NONE","path":None};state["predecessor_join"]={"id":"JOIN-P1","path":"agents/relay/parallel/JOIN-P1.yaml"};state["status_planes"]["execution"]={"state":"ACTIVE","can_continue":True,"material_authority":"WRITE","next_action":"Execute the integration EP after all lane checkpoints converge."};state["projection"].update({"execution_ref":"EP-I"});state["progress"].update({"overall_percent":50,"phase_percent":50,"ep_percent":0})
    progress=yaml.safe_load((root/"agents/relay/roadmap/PROGRESS.yaml").read_text());progress["overall"].update({"earned_weight":100,"total_weight":200,"percent":50});progress["objectives"][0].update({"earned_weight":100,"total_weight":200,"percent":50});progress["phases"][0].update({"earned_weight":100,"total_weight":200,"percent":50});bywp={x["id"]:x for x in progress["work_packages"]};bywp["WP-A"].update({"earned_weight":100,"total_weight":100,"percent":100});bywp["WP-B"].update({"earned_weight":100,"total_weight":100,"percent":100});bywp["WP-I"].update({"earned_weight":0,"total_weight":100,"percent":0});progress["execution_packages"]=[{"id":"EP-I","earned_weight":0,"total_weight":100,"percent":0}];progress["implementation_steps"]=[{"id":"STEP-1","ep_id":"EP-I","earned_weight":0,"total_weight":100,"percent":0}];progress["acceptance_criteria"]=[{"id":"AC-1","ep_id":"EP-I","status":"NOT_STARTED","earned_weight":0,"total_weight":100,"percent":0,"basis":[]}]
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/execution-packages/EP-I.yaml",integration_ep);dump(root/"agents/relay/checkpoints/CP-A.yaml",lane_cp("CP-A","EP-A","LANE-A"));dump(root/"agents/relay/checkpoints/CP-B.yaml",lane_cp("CP-B","EP-B","LANE-B"));dump(root/"agents/relay/parallel/JOIN-P1.yaml",join);return roadmap,plan,state,join
class ParallelConvergenceStressTests(unittest.TestCase):
    def test_parallel_join_becomes_cold_startable_serial_integration(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);converge(root);self.assertEqual([],parallel_join(root)[0]);self.assertEqual([],checkpoint_linkage(root)[0]);self.assertEqual([],cold_start(root)[0])
    def test_join_fails_if_one_lane_checkpoint_is_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);converge(root);(root/"agents/relay/checkpoints/CP-B.yaml").unlink();self.assertTrue(any("lane checkpoint missing" in x for x in parallel_join(root)[0]))
    def test_join_fails_before_all_lane_work_packages_are_complete(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);roadmap,_,_,_=converge(root);roadmap["objectives"][0]["phases"][0]["work_packages"][1]["state"]="ACTIVE";roadmap["objectives"][0]["phases"][0]["work_packages"][1]["execution_status"]="ACTIVE";dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);errors=parallel_join(root)[0];self.assertTrue(any("sole computed frontier" in x or "requires lane work package COMPLETE" in x for x in errors))
    def test_join_fails_if_integration_ep_does_not_bind_join(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);converge(root);path=root/"agents/relay/execution-packages/EP-I.yaml";data=yaml.safe_load(path.read_text());data["identity"]["previous_join"]="JOIN-WRONG";dump(path,data);self.assertTrue(any("previous_join" in x for x in parallel_join(root)[0]))
if __name__=="__main__":unittest.main()
