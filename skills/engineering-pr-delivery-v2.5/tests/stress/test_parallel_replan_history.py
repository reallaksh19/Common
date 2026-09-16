from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parent))
from test_parallel_bootstrap import ep,dump
from test_parallel_replan import parallel_replan_repo
from validate_parallel_replan import validate as parallel_replan


def checkpoint_b1():
    return {
        "schema_version":"relay-v2.5","checkpoint_id":"CP-B1","ep_id":"EP-B1",
        "roadmap_basis":{"roadmap_id":"RM-P","revision":"RM-1"},
        "execution_basis":{"material_ref":"abc"},
        "implementation_result":{"completed_steps":["STEP-1"],"files_changed":["src/b1"]},
        "acceptance_results":[{"id":"AC-1","status":"PASS"}],
        "validation_results":[{"id":"TEST-1","status":"PASS","basis_ref":"abc"}],
        "quality_findings":[],"discoveries":[],"roadmap_reconciliation":{"result":"STATUS_UPDATE"},
        "successor":{"mode":"JOIN","frontier_work_package":None,"ep_id":None,"parallel_plan":"PLAN-P2","lane_id":"LANE-B1","join_id":None,"lanes":[]},
    }


def second_replan_repo(root:Path):
    parallel_replan_repo(root)
    import yaml
    roadmap=yaml.safe_load((root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml").read_text())
    state=yaml.safe_load((root/"agents/relay/REPO_STATE.yaml").read_text())
    wps=roadmap["objectives"][0]["phases"][0]["work_packages"]
    by_id={x["id"]:x for x in wps}
    by_id["WP-B1"]["state"]="COMPLETE";by_id["WP-B1"]["execution_status"]="TERMINAL"
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap)
    dump(root/"agents/relay/checkpoints/CP-B1.yaml",checkpoint_b1())

    acc=[{"id":"AC-B2-R3","state":"NOT_RUN","basis":["EP-B2","AC-B2-R3"]}]
    ev=[{"id":"TEST-B2-R3","status":"NOT_RUN","basis_ref":"abc","reason":"Second-generation lane route invalidated before execution."}]
    replacement=ep("EP-B2-R3","agent/lane-b2-r3","WP-B2","src/b2")
    replacement["identity"]["previous_replan"]="REPLAN-P3"
    replacement["replan_inheritance"]={"from_replan":"REPLAN-P3","unresolved_acceptance":acc,"evidence":ev}
    dump(root/"agents/relay/execution-packages/EP-B2-R3.yaml",replacement)

    replan3={
        "schema_version":"relay-v2.5-parallel-replan","id":"REPLAN-P3",
        "predecessor_plan":{"id":"PLAN-P2","path":"agents/relay/parallel/PLAN-P2.yaml"},
        "trigger":{"type":"LANE_INVALIDATED","lane_id":"LANE-B2","reason":"Second-generation lane B2 route is stale.","basis":["DRIFT-B2-R3"]},
        "lane_dispositions":[
            {"lane_id":"LANE-B1","work_package":"WP-B1","disposition":"COMPLETE","checkpoint":{"id":"CP-B1","path":"agents/relay/checkpoints/CP-B1.yaml"}},
            {"lane_id":"LANE-B2","work_package":"WP-B2","disposition":"INVALIDATED","basis":["DRIFT-B2-R3"],"unresolved_acceptance":acc,"evidence":ev,"transfers":[{"work_package":"WP-B2","unresolved_acceptance":acc,"evidence":ev}]},
        ],
        "roadmap_reconciliation":{"roadmap_revision":"RM-1","frontier_after":["WP-B2"]},
        "successor_route":{"mode":"SERIAL","work_package":"WP-B2","ep_id":"EP-B2-R3","ep_path":"agents/relay/execution-packages/EP-B2-R3.yaml","parallel_plan_id":None,"parallel_plan_path":None},
    }
    dump(root/"agents/relay/parallel/REPLAN-P3.yaml",replan3)

    state.update({
        "relay_state":"ACTIVE",
        "current_position":{"objective":"OBJ","phase":"PHASE","work_package":"WP-B2","work_packages":[]},
        "execution_policy":{"mode":"SERIAL"},
        "active_ep":{"id":"EP-B2-R3","path":"agents/relay/execution-packages/EP-B2-R3.yaml","state":"ACTIVE"},
        "last_checkpoint":{"id":"NONE","path":None},"predecessor_join":{"id":None,"path":None},
        "predecessor_replan":{"id":"REPLAN-P3","path":"agents/relay/parallel/REPLAN-P3.yaml"},
    })
    state["status_planes"]["execution"].update({"state":"ACTIVE","can_continue":True,"material_authority":"WRITE","next_action":"Execute only EP-B2-R3."})
    state["projection"].update({"execution_ref":"EP-B2-R3","state":"NOT_REQUIRED","required":False})
    dump(root/"agents/relay/REPO_STATE.yaml",state)
    return replan3


class ParallelReplanHistoryStressTests(unittest.TestCase):
    def test_two_generation_replan_chain_is_recoverable(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);second_replan_repo(root);self.assertEqual([],parallel_replan(root)[0])

    def test_missing_historical_replan_receipt_breaks_chain(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);second_replan_repo(root);(root/"agents/relay/parallel/REPLAN-P2.yaml").unlink();self.assertTrue(any("history missing receipt" in x for x in parallel_replan(root)[0]))

    def test_historical_replan_must_point_forward_to_plan_that_cites_it(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);second_replan_repo(root)
            import yaml
            path=root/"agents/relay/parallel/REPLAN-P2.yaml";data=yaml.safe_load(path.read_text());data["successor_route"]["parallel_plan_id"]="PLAN-WRONG";dump(path,data)
            self.assertTrue(any("successor route does not point to plan PLAN-P2" in x for x in parallel_replan(root)[0]))

    def test_replan_history_cycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);second_replan_repo(root)
            import yaml
            path=root/"agents/relay/parallel/PLAN-P2.yaml";data=yaml.safe_load(path.read_text());data["previous_replan"]="REPLAN-P3";data["previous_replan_path"]="agents/relay/parallel/REPLAN-P3.yaml";dump(path,data)
            self.assertTrue(any("cycle detected" in x for x in parallel_replan(root)[0]))

if __name__=="__main__":unittest.main()
