from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import good,dump,semantic_ep
from test_end_to_end_relay_certification import attach_clear_qrv
from test_takeover_certification import attach_takeover,route_shape
from relaylib import load_yaml
from takeoverlib import current_routes,yaml_digest
from cold_start_check import validate as cold_start
from validate_question_set import validate as question_sets
from validate_qualification_receipt import validate as qualifications
from validate_takeover_certification import validate as takeover,is_takeover_certified
from validate_zero_context_reconstruction import validate as zero_context
from zero_context_reconstruction import build as reconstruct


def _pct(earned,total):
    return round(earned*100.0/total,2) if total else 0.0


def _row(rows,row_id):
    return next(x for x in rows if x.get("id")==row_id)


def relay_ep(ep_id:str,wp:str,suffix:str,previous_checkpoint:str):
    ep=semantic_ep(ep_id=ep_id,wp=wp,write_path=f"src/{suffix.lower()}.py")
    ep["identity"]["previous_checkpoint"]=previous_checkpoint
    ids={"dstep":f"DSTEP-{suffix}","input":f"INPUT-{suffix}","bench":f"BENCH-{suffix}","step":f"STEP-{suffix}","ac":f"AC-{suffix}","test":f"TEST-{suffix}"}
    ep["repository_discovery"][0]["id"]=ids["dstep"]
    ep["inputs"][0]["id"]=ids["input"];ep["inputs"][0]["consumers"]=[ids["step"]]
    ep["benchmarks"][0]["id"]=ids["bench"];ep["benchmarks"][0]["verifies"]=[ids["ac"],ids["test"]]
    step=ep["implementation_plan"][0];step["id"]=ids["step"];step["inputs"]=[ids["input"]];step["acceptance"]=[ids["ac"]];step["tests"]=[ids["test"]]
    nxt=ep["next_work"]["steps"][0];nxt["inputs"]=[ids["input"]];nxt["tests"]=[ids["test"]];nxt["benchmarks"]=[ids["bench"]];nxt["acceptance"]=[ids["ac"]]
    ep["acceptance"][0]["id"]=ids["ac"];ep["acceptance"][0]["verification"]=[ids["test"],ids["bench"]]
    ep["validation"][0]["id"]=ids["test"];ep["validation"][0]["proves"]=[ids["ac"]]
    ep["context_capsule"]["roadmap_position"]=f"Phase 1 / {wp}"
    ep["context_capsule"]["why_this_work_exists"]=f"{wp} is the current dependency-qualified roadmap work package."
    ep["context_capsule"]["prior_owner_decisions"]=["ODR-RELAY"]
    ep["context_capsule"]["current_implementation_state"]=f"Predecessor checkpoint {previous_checkpoint} established the incoming basis."
    ep["context_capsule"]["known_problems"]=[f"{wp} remains incomplete until {ids['ac']} passes."]
    return ep,ids


def setup_three_wp(root:Path):
    roadmap,ep,progress,state=good(root)
    phase=roadmap["objectives"][0]["phases"][0]
    phase["work_packages"].extend([
        {"id":"WP-2","title":"Second relay work package","state":"PLANNED","definition":"DETAILED","execution_status":"WAITING","depends_on":["WP-1"]},
        {"id":"WP-3","title":"Third relay work package","state":"PLANNED","definition":"DETAILED","execution_status":"WAITING","depends_on":["WP-2"]},
    ])
    for bucket in (progress["overall"],progress["objectives"][0],progress["phases"][0]):
        bucket.update({"earned_weight":50,"total_weight":300,"percent":_pct(50,300)})
    progress["work_packages"].extend([
        {"id":"WP-2","earned_weight":0,"total_weight":100,"percent":0},
        {"id":"WP-3","earned_weight":0,"total_weight":100,"percent":0},
    ])
    state["progress"]["overall_percent"]=_pct(50,300);state["progress"]["phase_percent"]=_pct(50,300)
    odr={"schema_version":"relay-v2.5","id":"ODR-RELAY","decision":{"authority":"OWNER","kind":"AUTHORIZATION","statement":"Keep engineering changes inside the active roadmap work package and preserve protected roadmap authority.","source":"owner-source:synthetic-zero-chat-release"},"effects":{"requirement_disposition":"SATISFIED","grants_material_write_authority":False,"pending_items":[]},"impact":{"class":["LOCAL"]},"affected":{"objectives":["OBJ-1"],"phases":["PHASE-1"],"work_packages":["WP-1","WP-2","WP-3"],"execution_packages":[],"issues":[]},"required_reconciliation":[],"status":"APPLIED"}
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/REPO_STATE.yaml",state);dump(root/"agents/relay/roadmap/owner-decisions/ODR-RELAY.yaml",odr)


def _questions(ids:dict,wp:str):
    return [
        {"id":"Q1","focus":"PRODUCTION_PATH","anchors":[wp,ids["input"]],"prompt":"Trace the incoming production path and authority source.","required_output_keys":["production_entrypoint","state_owner","authority_source","downstream_consumer"],"evidence_required":True},
        {"id":"Q2","focus":"ENGINEERING_PROBLEM","anchors":[wp,ids["input"],ids["ac"]],"prompt":"Reconstruct the synthetic engineering payload independently.","reconstruction_mode":"QUANTITATIVE","payload":{"source":"synthetic zero-chat qualification payload","values":{"load_N":{"value":1000,"units":"N"},"length_mm":{"value":200,"units":"mm"}}},"required_output_keys":["reconstruction_steps","intermediate_result","expected_result"],"evidence_required":True},
        {"id":"Q3","focus":"BOUNDARIES_INVARIANTS","anchors":[wp,ids["ac"]],"prompt":"State the stale-authority mutation, protected invariant and falsifier.","mutation":{"condition":"Change the authoritative input revision after discovery.","protected_invariant":"No engineering write may use stale authority.","falsifier":"A write occurs after the discovered authority revision no longer matches current authority."},"required_output_keys":["mutation_effect","protected_invariant","falsifier"],"evidence_required":True},
        {"id":"Q4","focus":"VERIFICATION","anchors":[ids["ac"],ids["test"],ids["bench"]],"prompt":"Verify independently using the frozen oracle.","oracle_refs":[ids["bench"]],"independence_requirement":"Use the frozen oracle rather than implementation logic.","required_output_keys":["independent_method","predicted_result","tolerance_or_exactness"],"evidence_required":True},
        {"id":"Q5","focus":"FIRST_SAFE_SLICE","anchors":[ids["step"],ids["ac"],ids["test"]],"prompt":"Name the exact first bounded change and predicted verification.","step_refs":[ids["step"]],"required_output_keys":["first_change","predicted_before","predicted_after","verification"],"evidence_required":True},
    ]


def _answers(ids:dict):
    return [
        {"id":"Q1","response":"The candidate traced the active EP path from repository state.","outputs":{"production_entrypoint":ids["step"],"state_owner":"roadmap and active EP","authority_source":ids["input"],"downstream_consumer":ids["ac"]},"evidence":[ids["dstep"],ids["input"]]},
        {"id":"Q2","response":"The candidate reconstructed the 1000 N / 200 mm payload independently.","outputs":{"reconstruction_steps":["resolve payload","normalize declared units","compare to frozen oracle"],"intermediate_result":"declared payload normalized","expected_result":"matches frozen synthetic oracle"},"evidence":[ids["input"],ids["bench"]]},
        {"id":"Q3","response":"A stale authority revision removes write readiness.","outputs":{"mutation_effect":"certification becomes stale","protected_invariant":"no stale-authority write","falsifier":"write with mismatched authority revision"},"evidence":[ids["input"],"EP anti_drift"]},
        {"id":"Q4","response":"The frozen oracle is evaluated independently of implementation.","outputs":{"independent_method":ids["bench"],"predicted_result":"result matches frozen synthetic oracle","tolerance_or_exactness":"exact synthetic comparison"},"evidence":[ids["bench"],ids["test"]]},
        {"id":"Q5","response":"Execute only the first bounded step and verify immediately.","outputs":{"first_change":ids["step"],"predicted_before":f"{ids['ac']} incomplete","predicted_after":f"{ids['ac']} complete","verification":f"{ids['test']} + {ids['bench']}"},"evidence":[ids["step"],ids["ac"],ids["test"]]},
    ]


def prepare_qualification(root:Path,ep_id:str,ids:dict,preparer:str):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep_path=root/state["active_ep"]["path"];ep=load_yaml(ep_path);suffix=ep_id.split("-")[-1];qset_id=f"QSET-{suffix}";qset_path=f"agents/relay/certifications/qualification/{qset_id}.yaml"
    ep["qualification_boundary"]={"required":True,"trigger":"MATERIAL_QUALIFICATION_BOUNDARY_CHANGED","from_phase":"PHASE-1","to_phase":"PHASE-1","changed_dimensions":["PRODUCTION_PATH","INPUT_AUTHORITY","VERIFICATION_ORACLE"],"basis":["Incoming work package has a new production path, input authority use and verification boundary."],"question_set":{"id":qset_id,"path":qset_path}}
    dump(ep_path,ep)
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");route=current_routes(root,state)[0];shape=route_shape(route);shape.update({"roadmap_revision":"RM-0001","work_package":ep["roadmap_source"]["work_package"],"ep_contract_digest":yaml_digest(ep_path)})
    qset={"schema_version":"relay-v2.5-question-set","id":qset_id,"route":shape,"boundary":{"trigger":"MATERIAL_QUALIFICATION_BOUNDARY_CHANGED","from_phase":"PHASE-1","to_phase":"PHASE-1","changed_dimensions":["PRODUCTION_PATH","INPUT_AUTHORITY","VERIFICATION_ORACLE"],"basis":["Incoming work package has a new production path, input authority use and verification boundary."]},"questions":_questions(ids,ep["roadmap_source"]["work_package"]),"prepared_by":{"agent_instance_id":preparer}}
    dump(root/qset_path,qset)
    return qset_id,qset_path,shape


def certify(root:Path,ep_id:str,ids:dict,candidate:str,preparer:str,evaluator:str):
    qset_id,qset_path,shape=prepare_qualification(root,ep_id,ids,preparer)
    disc_id=f"DISC-{candidate.split('-')[-1]}";tc_id=f"TC-{candidate.split('-')[-1]}";qual_id=f"QUAL-{candidate.split('-')[-1]}"
    disc,tc,route=attach_takeover(root,candidate=candidate,preparer=preparer,disc_id=disc_id,tc_id=tc_id)
    qual_path=f"agents/relay/certifications/qualification/{qual_id}.yaml"
    qual={"schema_version":"relay-v2.5-qualification","id":qual_id,"candidate":{"agent_instance_id":candidate},"question_set":{"id":qset_id,"path":qset_path},"route":shape,"answers":_answers(ids),"evaluated_by":{"type":"INDEPENDENT_AGENT","identity":evaluator,"basis":[f"Independent repository-only evaluation of {qset_id} against {ep_id}."]},"evaluations":[{"id":qid,"status":"PASS","basis":[f"independent {qid} evaluation from repository evidence"]} for qid in ("Q1","Q2","Q3","Q4","Q5")],"self_evaluation":{"allowed":False},"result":"PASS","conversation_context_used":False}
    dump(root/qual_path,qual)
    tc["qualification"]={"required":True,"status":"PASS","receipt_id":qual_id,"receipt_path":qual_path,"receipt_digest":yaml_digest(root/qual_path)}
    dump(root/f"agents/relay/certifications/takeover/{tc_id}.yaml",tc)
    return disc,qual,tc,route


def complete_and_handoff(root:Path,cp_id:str,next_ep_id:str,next_wp:str,suffix:str,preparer:str):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");from_ep=load_yaml(root/state["active_ep"]["path"]);from_ep_id=from_ep["identity"]["ep_id"];current_wp=from_ep["roadmap_source"]["work_package"];current_ac=from_ep["acceptance"][0]["id"];current_test=from_ep["validation"][0]["id"];current_step=from_ep["implementation_plan"][0]["id"]
    qptr=attach_clear_qrv(root,from_ep_id,f"QRV-{cp_id}");material=from_ep["git_basis"]["material_ref"]
    cp={"schema_version":"relay-v2.5","checkpoint_id":cp_id,"ep_id":from_ep_id,"roadmap_basis":{"roadmap_id":"RM-T","revision":"RM-0001"},"execution_basis":{"material_ref":material},"implementation_result":{"summary":f"{from_ep_id} completed {current_wp} on its bounded material basis."},"acceptance_results":[{"id":current_ac,"status":"PASS","basis_ref":material}],"validation_results":[{"id":current_test,"status":"PASS","basis_ref":material}],"quality_review":qptr,"quality_findings":[],"discoveries":[],"known_limitations":[],"remaining_work":[f"Execute {next_wp} under {next_ep_id}."],"roadmap_reconciliation":{"result":"STATUS_UPDATE"},"successor":{"mode":"SERIAL","frontier_work_package":next_wp,"ep_id":next_ep_id,"parallel_plan":None,"join_id":None,"lane_id":None,"lanes":[]}}
    cp_path=root/f"agents/relay/checkpoints/{cp_id}.yaml";dump(cp_path,cp)
    roadmap=load_yaml(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml");wps=roadmap["objectives"][0]["phases"][0]["work_packages"]
    by_id={x["id"]:x for x in wps};by_id[current_wp].update({"state":"COMPLETE","execution_status":"TERMINAL"});by_id[next_wp].update({"state":"ACTIVE","execution_status":"ACTIVE"})
    successor,ids=relay_ep(next_ep_id,next_wp,suffix,cp_id);ep_path=root/f"agents/relay/execution-packages/{next_ep_id}.yaml";dump(ep_path,successor)
    progress=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml");_row(progress["work_packages"],current_wp).update({"earned_weight":100,"percent":100});_row(progress["execution_packages"],from_ep_id).update({"earned_weight":100,"percent":100});_row(progress["implementation_steps"],current_step).update({"earned_weight":100,"percent":100});_row(progress["acceptance_criteria"],current_ac).update({"status":"COMPLETE","earned_weight":100,"percent":100,"basis":[cp_id]})
    progress["execution_packages"].append({"id":next_ep_id,"earned_weight":0,"total_weight":100,"percent":0});progress["implementation_steps"].append({"id":ids["step"],"ep_id":next_ep_id,"earned_weight":0,"total_weight":100,"percent":0});progress["acceptance_criteria"].append({"id":ids["ac"],"ep_id":next_ep_id,"status":"NOT_STARTED","earned_weight":0,"total_weight":100,"percent":0,"basis":[next_ep_id]})
    completed=sum(100 for x in wps if x.get("state")=="COMPLETE");total=300
    for bucket in (progress["overall"],progress["objectives"][0],progress["phases"][0]):bucket.update({"earned_weight":completed,"total_weight":total,"percent":_pct(completed,total)})
    state["current_position"]["work_package"]=next_wp;state["active_ep"]={"id":next_ep_id,"path":str(ep_path.relative_to(root)),"state":"ACTIVE"};state["last_checkpoint"]={"id":cp_id,"path":str(cp_path.relative_to(root))};state["takeover_admissions"]=[];state["projection"]["execution_ref"]=next_ep_id;state["progress"].update({"overall_percent":_pct(completed,total),"phase_percent":_pct(completed,total),"ep_percent":0});state["status_planes"]["execution"]={"state":"ACTIVE","can_continue":True,"material_authority":"WRITE","next_action":f"Execute {next_ep_id} from repository state only."};state["status_planes"]["evidence"]={"state":"PARTIAL","summary":f"{cp_id} proves {current_wp}; {next_wp} remains.","not_run":[]};state["relay_readiness"]={"baton_ready":True,"projection_ready":True,"handover_ready":True,"reasons":[]}
    dump(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml",roadmap);dump(root/"agents/relay/roadmap/PROGRESS.yaml",progress);dump(root/"agents/relay/REPO_STATE.yaml",state)
    prepare_qualification(root,next_ep_id,ids,preparer)
    return ids


class ZeroChatReleaseProofTests(unittest.TestCase):
    def test_agent_a_b_c_release_proof_crosses_completed_work_packages_with_qualification(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);setup_three_wp(root)
            b_ids=complete_and_handoff(root,"CP-A","EP-B","WP-2","B","agent-A")
            self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0])
            b_view=reconstruct(root)["routes"][0];self.assertEqual("WP-2",b_view["roadmap_position"]["ep_position"]["work_package"]);self.assertEqual("CP-A",b_view["predecessor_established"]["checkpoint_id"]);self.assertTrue(any(x.get("id")=="ODR-RELAY" for x in b_view["owner_decisions"]))
            disc_b,qual_b,tc_b,route_b=certify(root,"EP-B",b_ids,"agent-B","agent-A","independent-reviewer-B")
            self.assertFalse(disc_b["conversation_context_used"]);self.assertFalse(qual_b["conversation_context_used"]);self.assertFalse(tc_b["conversation_context_used"]);self.assertEqual([],question_sets(root)[0]);self.assertEqual([],qualifications(root)[0]);self.assertEqual([],takeover(root)[0]);self.assertTrue(is_takeover_certified(root,route_b,"agent-B")[0])
            c_ids=complete_and_handoff(root,"CP-B","EP-C","WP-3","C","agent-B")
            roadmap=load_yaml(root/"agents/relay/roadmap/OVERALL_ROADMAP.yaml");wps={x["id"]:x for x in roadmap["objectives"][0]["phases"][0]["work_packages"]};self.assertEqual("COMPLETE",wps["WP-2"]["state"])
            self.assertEqual([],cold_start(root)[0]);self.assertEqual([],zero_context(root)[0])
            c_view=reconstruct(root)["routes"][0];self.assertEqual("CP-B",c_view["predecessor_established"]["checkpoint_id"]);self.assertEqual("WP-3",c_view["roadmap_position"]["ep_position"]["work_package"]);self.assertFalse(reconstruct(root)["conversation_context_required"])
            self.assertTrue(c_view["why_task_exists"]);self.assertTrue(c_view["owner_decisions"]);self.assertTrue(c_view["remaining_uncertain"]);self.assertTrue(c_view["input_authority_editability"]);self.assertTrue(c_view["benchmarks_oracles"]);self.assertTrue(c_view["scope"]["allowed"]);self.assertTrue(c_view["scope"]["protected"]);self.assertTrue(c_view["scope"]["prohibited"]);self.assertTrue(c_view["quality_obligations"]);self.assertTrue(c_view["evidence"]);self.assertTrue(c_view["tests_required"]);self.assertTrue(c_view["acceptance"]);self.assertTrue(c_view["first_implementation_action"]);self.assertTrue(c_view["stale_conditions"]);self.assertTrue(c_view["next_work"])
            disc_c,qual_c,tc_c,route_c=certify(root,"EP-C",c_ids,"agent-C","agent-B","independent-reviewer-C")
            self.assertFalse(disc_c["conversation_context_used"]);self.assertFalse(qual_c["conversation_context_used"]);self.assertFalse(tc_c["conversation_context_used"]);self.assertEqual([],question_sets(root)[0]);self.assertEqual([],qualifications(root)[0]);self.assertEqual([],takeover(root)[0]);self.assertTrue(is_takeover_certified(root,route_c,"agent-C")[0]);self.assertEqual([],cold_start(root)[0])

if __name__=="__main__":unittest.main()
