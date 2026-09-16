from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parent))
from test_parallel_bootstrap import parallel_repo,ep,dump
from validate_parallel_replan import validate as parallel_replan
from validate_ep_self_contained import validate_ep_data


def checkpoint_a():
    return {
        "schema_version":"relay-v2.5","checkpoint_id":"CP-A","ep_id":"EP-A",
        "roadmap_basis":{"roadmap_id":"RM-P","revision":"RM-1"},
        "execution_basis":{"material_ref":"abc"},
        "implementation_result":{"completed_steps":["STEP-1"],"files_changed":["src/a"]},
        "acceptance_results":[{"id":"AC-1","status":"PASS"}],
        "validation_results":[{"id":"TEST-1","status":"PASS","basis_ref":"abc"}],
        "quality_findings":[],"discoveries":[],
        "roadmap_reconciliation":{"result":"STATUS_UPDATE"},
        "successor":{"mode":"JOIN","frontier_work_package":None,"ep_id":None,"parallel_plan":"PLAN-P1","lane_id":"LANE-A","join_id":None,"lanes":[]},
    }


def serial_replan_repo(root:Path):
    roadmap,plan,state=parallel_repo(root)
    wps=roadmap["objectives"][0]["phases"][0]["work_packages"]
    wps[0]["state"]="COMPLETE";wps[0]["execution_status"]="TERMINAL"
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap)
    dump(root/"agents/relay/checkpoints/CP-A.yaml",checkpoint_a())

    unresolved=[{"id":"AC-1","state":"NOT_RUN","basis":["EP-B"]}]
    evidence=[{"id":"TEST-1","status":"NOT_RUN","basis_ref":"abc","reason":"Original lane route became invalid before execution."}]
    replacement=ep("EP-B2","agent/lane-b2","WP-B","src/b")
    replacement["identity"]["previous_replan"]="REPLAN-P2"
    replacement["replan_inheritance"]={"from_replan":"REPLAN-P2","unresolved_acceptance":unresolved,"evidence":evidence}
    dump(root/"agents/relay/execution-packages/EP-B2.yaml",replacement)

    receipt={
        "schema_version":"relay-v2.5-parallel-replan","id":"REPLAN-P2",
        "predecessor_plan":{"id":"PLAN-P1","path":"agents/relay/parallel/PLAN-P1.yaml"},
        "trigger":{"type":"LANE_INVALIDATED","lane_id":"LANE-B","reason":"Lane B route is stale and cannot safely continue.","basis":["DRIFT-B"]},
        "lane_dispositions":[
            {"lane_id":"LANE-A","work_package":"WP-A","disposition":"COMPLETE","checkpoint":{"id":"CP-A","path":"agents/relay/checkpoints/CP-A.yaml"}},
            {"lane_id":"LANE-B","work_package":"WP-B","disposition":"INVALIDATED","basis":["DRIFT-B"],"unresolved_acceptance":unresolved,"evidence":evidence,"transfer_to_work_package":"WP-B"},
        ],
        "roadmap_reconciliation":{"roadmap_revision":"RM-1","frontier_after":["WP-B"]},
        "successor_route":{"mode":"SERIAL","work_package":"WP-B","ep_id":"EP-B2","ep_path":"agents/relay/execution-packages/EP-B2.yaml","parallel_plan_id":None,"parallel_plan_path":None},
    }
    dump(root/"agents/relay/parallel/REPLAN-P2.yaml",receipt)

    state.update({
        "relay_state":"ACTIVE",
        "current_position":{"objective":"OBJ","phase":"PHASE","work_package":"WP-B","work_packages":[]},
        "execution_policy":{"mode":"SERIAL"},
        "active_ep":{"id":"EP-B2","path":"agents/relay/execution-packages/EP-B2.yaml","state":"ACTIVE"},
        "last_checkpoint":{"id":"NONE","path":None},
        "predecessor_join":{"id":None,"path":None},
        "predecessor_replan":{"id":"REPLAN-P2","path":"agents/relay/parallel/REPLAN-P2.yaml"},
    })
    state["status_planes"]["execution"].update({"state":"ACTIVE","can_continue":True,"material_authority":"WRITE","next_action":"Execute only replacement EP-B2."})
    state["projection"].update({"execution_ref":"EP-B2","state":"NOT_REQUIRED","required":False})
    dump(root/"agents/relay/REPO_STATE.yaml",state)
    return receipt,replacement


class ParallelReplanStressTests(unittest.TestCase):
    def test_partial_lane_invalidation_can_collapse_to_one_serial_replacement(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);serial_replan_repo(root)
            self.assertEqual([],parallel_replan(root)[0])

    def test_completed_sibling_checkpoint_cannot_disappear_from_replan(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);receipt,_=serial_replan_repo(root)
            receipt["lane_dispositions"]=receipt["lane_dispositions"][1:]
            dump(root/"agents/relay/parallel/REPLAN-P2.yaml",receipt)
            self.assertTrue(any("cover every predecessor lane" in x for x in parallel_replan(root)[0]))

    def test_replacement_ep_must_inherit_invalidated_acceptance_and_evidence_exactly(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,replacement=serial_replan_repo(root)
            replacement["replan_inheritance"]["evidence"][0]["status"]="PASS"
            dump(root/"agents/relay/execution-packages/EP-B2.yaml",replacement)
            self.assertTrue(any("inheritance mismatch for evidence" in x for x in parallel_replan(root)[0]))

    def test_replanned_ep_has_one_predecessor_baton(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,replacement=serial_replan_repo(root)
            replacement["identity"]["previous_checkpoint"]="CP-A"
            errors=validate_ep_data(root,replacement,"replacement") [0]
            self.assertTrue(any("only one of previous_checkpoint, previous_join, previous_replan" in x for x in errors))

if __name__=="__main__":unittest.main()
