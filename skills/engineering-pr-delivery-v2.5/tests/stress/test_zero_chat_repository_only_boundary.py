from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import dump
from test_takeover_certification import attach_takeover,route_shape
from test_zero_chat_release_proof import setup_three_wp,complete_and_handoff
from relaylib import load_yaml
from takeoverlib import current_routes,yaml_digest
from cold_start_check import validate as cold_start
from validate_question_set import validate as question_sets
from validate_qualification_receipt import validate as qualifications
from validate_takeover_certification import validate as takeover,is_takeover_certified
from validate_zero_context_reconstruction import validate as zero_context
from zero_context_reconstruction import build as reconstruct


def active_contract(root:Path):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    ep_path=root/state["active_ep"]["path"]
    ep=load_yaml(ep_path)
    ids={
        "dstep":ep["repository_discovery"][0]["id"],
        "input":ep["inputs"][0]["id"],
        "bench":ep["benchmarks"][0]["id"],
        "step":ep["implementation_plan"][0]["id"],
        "ac":ep["acceptance"][0]["id"],
        "test":ep["validation"][0]["id"],
    }
    return state,ep_path,ep,ids


def answers_from_repository(qset:dict,ids:dict):
    questions={q["id"]:q for q in qset["questions"]}
    q2_payload=(questions["Q2"].get("payload") or {}).get("values") or {}
    payload_text=", ".join(f"{name}={item.get('value')} {item.get('units')}" for name,item in sorted(q2_payload.items()))
    mutation=questions["Q3"]["mutation"]
    q4=questions["Q4"]
    q5=questions["Q5"]
    return [
        {"id":"Q1","response":"Repository discovery identifies the active production path and authority.","outputs":{"production_entrypoint":ids["step"],"state_owner":"roadmap and active EP","authority_source":ids["input"],"downstream_consumer":ids["ac"]},"evidence":[ids["dstep"],ids["input"]]},
        {"id":"Q2","response":f"Repository QSET payload reconstructed independently: {payload_text}.","outputs":{"reconstruction_steps":["read QSET payload","normalize declared units","compare to repository benchmark"],"intermediate_result":payload_text,"expected_result":"matches repository benchmark contract"},"evidence":[ids["input"],ids["bench"]]},
        {"id":"Q3","response":"Repository QSET defines the mutation boundary and falsifier.","outputs":{"mutation_effect":mutation["condition"],"protected_invariant":mutation["protected_invariant"],"falsifier":mutation["falsifier"]},"evidence":[ids["input"],"EP anti_drift"]},
        {"id":"Q4","response":"Verification uses only the QSET-declared independent oracle.","outputs":{"independent_method":", ".join(q4["oracle_refs"]),"predicted_result":"result matches repository oracle","tolerance_or_exactness":"use benchmark contract exactness/tolerance"},"evidence":[ids["bench"],ids["test"]]},
        {"id":"Q5","response":"The first change is reconstructed from the QSET step reference and active EP.","outputs":{"first_change":q5["step_refs"][0],"predicted_before":f"{ids['ac']} incomplete","predicted_after":f"{ids['ac']} complete","verification":f"{ids['test']} + {ids['bench']}"},"evidence":[ids["step"],ids["ac"],ids["test"]]},
    ]


def certify_from_repository(root:Path,candidate:str,preparer:str,evaluator:str):
    state,ep_path,ep,ids=active_contract(root)
    boundary=ep["qualification_boundary"]
    qptr=boundary["question_set"]
    qset=load_yaml(root/qptr["path"])
    route=current_routes(root,state)[0]
    shape=route_shape(route)
    shape.update({"roadmap_revision":ep["roadmap_source"]["roadmap_revision"],"work_package":ep["roadmap_source"]["work_package"],"ep_contract_digest":yaml_digest(ep_path)})
    suffix=candidate.split("-")[-1]
    disc_id=f"DISC-{suffix}";tc_id=f"TC-{suffix}";qual_id=f"QUAL-{suffix}"
    disc,tc,_=attach_takeover(root,candidate=candidate,preparer=preparer,disc_id=disc_id,tc_id=tc_id)
    qual_path=f"agents/relay/certifications/qualification/{qual_id}.yaml"
    qual={
        "schema_version":"relay-v2.5-qualification",
        "id":qual_id,
        "candidate":{"agent_instance_id":candidate},
        "question_set":{"id":qptr["id"],"path":qptr["path"]},
        "route":shape,
        "answers":answers_from_repository(qset,ids),
        "evaluated_by":{"type":"INDEPENDENT_AGENT","identity":evaluator,"basis":[f"Independent repository-only evaluation of {qptr['id']} against {ep['identity']['ep_id']}."]},
        "evaluations":[{"id":qid,"status":"PASS","basis":[f"repository-only {qid} evaluation"]} for qid in ("Q1","Q2","Q3","Q4","Q5")],
        "self_evaluation":{"allowed":False},
        "result":"PASS",
        "conversation_context_used":False,
    }
    dump(root/qual_path,qual)
    tc["qualification"]={"required":True,"status":"PASS","receipt_id":qual_id,"receipt_path":qual_path,"receipt_digest":yaml_digest(root/qual_path)}
    dump(root/f"agents/relay/certifications/takeover/{tc_id}.yaml",tc)
    return disc,qual,tc,route


class ZeroChatRepositoryOnlyBoundaryTests(unittest.TestCase):
    def test_b_and_c_use_only_repository_state_after_handoff(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);setup_three_wp(root)

            # Agent A writes CP-A / EP-B / QSET-B. Ignore all in-memory return data.
            complete_and_handoff(root,"CP-A","EP-B","WP-2","B","agent-A")
            self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0])
            b_view=reconstruct(root)["routes"][0]
            self.assertEqual("CP-A",b_view["predecessor_established"]["checkpoint_id"])
            disc_b,qual_b,tc_b,route_b=certify_from_repository(root,"agent-B","agent-A","independent-reviewer-B")
            self.assertFalse(disc_b["conversation_context_used"]);self.assertFalse(qual_b["conversation_context_used"]);self.assertFalse(tc_b["conversation_context_used"])
            self.assertEqual([],question_sets(root)[0]);self.assertEqual([],qualifications(root)[0]);self.assertEqual([],takeover(root)[0]);self.assertTrue(is_takeover_certified(root,route_b,"agent-B")[0])

            # Agent B writes CP-B / EP-C / QSET-C. Again ignore all returned handoff data.
            complete_and_handoff(root,"CP-B","EP-C","WP-3","C","agent-B")
            self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0])
            c_view=reconstruct(root)["routes"][0]
            self.assertEqual("CP-B",c_view["predecessor_established"]["checkpoint_id"])
            self.assertFalse(reconstruct(root)["conversation_context_required"])
            self.assertTrue(c_view["owner_decisions"]);self.assertTrue(c_view["input_authority_editability"]);self.assertTrue(c_view["benchmarks_oracles"]);self.assertTrue(c_view["quality_obligations"]);self.assertTrue(c_view["tests_required"]);self.assertTrue(c_view["acceptance"]);self.assertTrue(c_view["first_implementation_action"]);self.assertTrue(c_view["stale_conditions"]);self.assertTrue(c_view["next_work"])
            disc_c,qual_c,tc_c,route_c=certify_from_repository(root,"agent-C","agent-B","independent-reviewer-C")
            self.assertFalse(disc_c["conversation_context_used"]);self.assertFalse(qual_c["conversation_context_used"]);self.assertFalse(tc_c["conversation_context_used"])
            self.assertEqual([],question_sets(root)[0]);self.assertEqual([],qualifications(root)[0]);self.assertEqual([],takeover(root)[0]);self.assertTrue(is_takeover_certified(root,route_c,"agent-C")[0])

if __name__=="__main__":unittest.main()
