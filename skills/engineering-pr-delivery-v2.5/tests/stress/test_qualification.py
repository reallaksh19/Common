from __future__ import annotations
import sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[2]/"scripts"));sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent))
from test_core import good,dump
from test_takeover_certification import attach_takeover,route_shape
from relaylib import load_yaml
from takeoverlib import current_routes,yaml_digest
from validate_question_set import validate as question_sets
from validate_qualification_receipt import validate as qualifications
from validate_takeover_certification import validate as takeover
from validate_baton_readiness import validate as baton
from validate_ep_semantics import validate as ep_semantics


def questions(mode="QUANTITATIVE"):
    return [
        {"id":"Q1","focus":"PRODUCTION_PATH","anchors":["WP-1","INPUT-1"],"prompt":"Trace the actual incoming production path and authority source.","required_output_keys":["production_entrypoint","state_owner","authority_source","downstream_consumer"],"evidence_required":True},
        {"id":"Q2","focus":"ENGINEERING_PROBLEM","anchors":["WP-1","INPUT-1","AC-1"],"prompt":"Reconstruct the engineering result from the supplied payload.","reconstruction_mode":mode,"payload":{"source":"synthetic qualified payload","values":{"load_N":{"value":1000,"units":"N"},"length_mm":{"value":200,"units":"mm"}}},"required_output_keys":["reconstruction_steps","intermediate_result","expected_result"],"evidence_required":True},
        {"id":"Q3","focus":"BOUNDARIES_INVARIANTS","anchors":["WP-1","AC-1"],"prompt":"Apply a stale-authority mutation and state the invariant and falsifier.","mutation":{"condition":"Change the authoritative input revision after discovery.","protected_invariant":"Execution must never use a stale authority revision.","falsifier":"Production write occurs while discovered authority revision differs from current revision."},"required_output_keys":["mutation_effect","protected_invariant","falsifier"],"evidence_required":True},
        {"id":"Q4","focus":"VERIFICATION","anchors":["AC-1","TEST-1","BENCH-1"],"prompt":"Verify the result independently from production implementation.","oracle_refs":["BENCH-1"],"independence_requirement":"Use the frozen oracle rather than production implementation logic.","required_output_keys":["independent_method","predicted_result","tolerance_or_exactness"],"evidence_required":True},
        {"id":"Q5","focus":"FIRST_SAFE_SLICE","anchors":["STEP-1","AC-1","TEST-1"],"prompt":"Name the first bounded change and predicted before/after verification.","step_refs":["STEP-1"],"required_output_keys":["first_change","predicted_before","predicted_after","verification"],"evidence_required":True},
    ]


def answers():
    return [
        {"id":"Q1","response":"Production reads the roadmap-backed policy through the active EP path.","outputs":{"production_entrypoint":"STEP-1 target","state_owner":"roadmap/EP contract","authority_source":"INPUT-1 source","downstream_consumer":"AC-1 result"},"evidence":["EP-1:DSTEP-1","INPUT-1"]},
        {"id":"Q2","response":"Reconstructed the supplied 1000 N / 200 mm synthetic payload independently.","outputs":{"reconstruction_steps":["resolve payload","apply frozen synthetic relation"],"intermediate_result":"payload normalized with declared units","expected_result":"matches BENCH-1 expected result"},"evidence":["QSET payload","BENCH-1"]},
        {"id":"Q3","response":"A stale authority revision must remove write readiness before production change.","outputs":{"mutation_effect":"certification becomes stale","protected_invariant":"no stale-authority write","falsifier":"write occurs with mismatched authority revision"},"evidence":["INPUT-1 stale_if","EP anti_drift"]},
        {"id":"Q4","response":"Use the frozen golden oracle independently of implementation.","outputs":{"independent_method":"BENCH-1 frozen golden","predicted_result":"result matches frozen synthetic oracle","tolerance_or_exactness":"exact synthetic comparison"},"evidence":["BENCH-1","TEST-1"]},
        {"id":"Q5","response":"Implement STEP-1 only, then run TEST-1 and compare BENCH-1.","outputs":{"first_change":"STEP-1 bounded target only","predicted_before":"AC-1 unsatisfied","predicted_after":"AC-1 satisfied","verification":"TEST-1 + BENCH-1"},"evidence":["STEP-1","AC-1","TEST-1"]},
    ]


def build(root:Path,trigger="PHASE_CHANGED",candidate="agent-B",evaluator="agent-Q"):
    good(root);ep_path=root/"agents/relay/execution-packages/EP-1.yaml";ep=load_yaml(ep_path);qpath="agents/relay/certifications/qualification/QSET-1.yaml"
    boundary={"required":True,"trigger":trigger,"from_phase":"PHASE-0" if trigger=="PHASE_CHANGED" else "PHASE-1","to_phase":"PHASE-1","changed_dimensions":["PRODUCTION_PATH"],"basis":["synthetic material qualification boundary"],"question_set":{"id":"QSET-1","path":qpath}}
    ep["qualification_boundary"]=boundary;dump(ep_path,ep)
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");route=current_routes(root,state)[0];shape=route_shape(route);shape.update({"roadmap_revision":"RM-0001","work_package":"WP-1","ep_contract_digest":yaml_digest(ep_path)})
    qset={"schema_version":"relay-v2.5-question-set","id":"QSET-1","route":shape,"boundary":{k:boundary[k] for k in ("trigger","from_phase","to_phase","changed_dimensions","basis")},"questions":questions(),"prepared_by":{"agent_instance_id":"agent-A"}}
    dump(root/qpath,qset)
    _,tc,_=attach_takeover(root,candidate=candidate,preparer="agent-A")
    qual_path="agents/relay/certifications/qualification/QUAL-1.yaml"
    qual={"schema_version":"relay-v2.5-qualification","id":"QUAL-1","candidate":{"agent_instance_id":candidate},"question_set":{"id":"QSET-1","path":qpath},"route":shape,"answers":answers(),"evaluated_by":{"type":"INDEPENDENT_AGENT","identity":evaluator,"basis":["independent review of Q1-Q5 against QSET-1 and EP-1"]},"evaluations":[{"id":qid,"status":"PASS","basis":[f"independent {qid} evaluation"]} for qid in ("Q1","Q2","Q3","Q4","Q5")],"self_evaluation":{"allowed":False},"result":"PASS","conversation_context_used":False}
    dump(root/qual_path,qual)
    tc["qualification"]={"required":True,"status":"PASS","receipt_id":"QUAL-1","receipt_path":qual_path,"receipt_digest":yaml_digest(root/qual_path)};dump(root/"agents/relay/certifications/takeover/TC-1.yaml",tc)
    return qset,qual,tc


class QualificationStressTests(unittest.TestCase):
    def test_phase_change_qualification_allows_current_tc(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);build(root)
            self.assertEqual([],question_sets(root)[0]);self.assertEqual([],qualifications(root)[0]);self.assertEqual([],takeover(root)[0]);self.assertEqual([],baton(root)[0])

    def test_same_phase_material_boundary_requires_fresh_qualification(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);build(root,"MATERIAL_QUALIFICATION_BOUNDARY_CHANGED")
            self.assertEqual([],question_sets(root)[0]);self.assertEqual([],qualifications(root)[0]);self.assertEqual([],takeover(root)[0])

    def test_quantitative_q2_requires_concrete_values(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);q,_,_=build(root);q["questions"][1]["payload"]["values"]={};dump(root/"agents/relay/certifications/qualification/QSET-1.yaml",q)
            self.assertTrue(any("QUANTITATIVE" in x for x in question_sets(root)[0]))

    def test_q3_requires_exact_falsifier(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);q,_,_=build(root);q["questions"][2]["mutation"]["falsifier"]="";dump(root/"agents/relay/certifications/qualification/QSET-1.yaml",q)
            self.assertTrue(any("falsifier" in x for x in question_sets(root)[0]))

    def test_candidate_cannot_prepare_own_question_set(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);q,_,_=build(root);q["prepared_by"]["agent_instance_id"]="agent-B";dump(root/"agents/relay/certifications/qualification/QSET-1.yaml",q)
            self.assertTrue(any("cannot prepare" in x for x in qualifications(root)[0]))

    def test_answer_must_supply_required_structured_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,qual,_=build(root);qual["answers"][3]["outputs"].pop("predicted_result");dump(root/"agents/relay/certifications/qualification/QUAL-1.yaml",qual)
            self.assertTrue(any("predicted_result" in x for x in qualifications(root)[0]))

    def test_independent_evaluator_cannot_be_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,qual,_=build(root);qual["evaluated_by"]["identity"]="agent-B";dump(root/"agents/relay/certifications/qualification/QUAL-1.yaml",qual)
            self.assertTrue(any("cannot be the candidate" in x for x in qualifications(root)[0]))

    def test_qual_change_invalidates_tc_digest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);_,qual,_=build(root);qual["answers"][0]["response"]="Changed after TC issuance";dump(root/"agents/relay/certifications/qualification/QUAL-1.yaml",qual)
            self.assertTrue(any("receipt_digest" in x for x in takeover(root)[0]))

    def test_three_pass_complete_makes_follow_on_qset_not_applicable(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);good(root)
            ep_path=root/"agents/relay/execution-packages/EP-1.yaml";ep=load_yaml(ep_path)
            ep["qualification_boundary"]={
                "required":False,
                "trigger":"PHASE_CHANGED",
                "from_phase":"PHASE-0",
                "to_phase":"PHASE-1",
                "changed_dimensions":["PRODUCTION_PATH"],
                "basis":["THREE_PASS_COMPLETE: completed standalone Prompt 3 for current task"],
                "not_applicable_reason":"THREE_PASS_COMPLETE",
                "question_set":None,
            }
            dump(ep_path,ep)
            self.assertEqual([],ep_semantics(root)[0])
            self.assertEqual([],question_sets(root)[0])
            attach_takeover(root,candidate="agent-B",preparer="agent-B")
            self.assertEqual([],takeover(root)[0])

if __name__=="__main__":unittest.main()
