#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1];PHYS=ROOT.parent
sys.path[:0]=[str(ROOT/"engine"),str(PHYS/"Core2A"/"engine"),str(PHYS/"Core1B"/"engine")]
from core2b_runtime import *
from run_physics_core2a import compile_core2a
from core1b_runtime import build_release_receipt

def load(p):return json.loads(Path(p).read_text())
def schema(name):
    s=load(ROOT/"contracts"/name);Draft202012Validator.check_schema(s);return Draft202012Validator(s)
C2A_RUN=load(PHYS/"Core2A"/"golden"/"projectile-event"/"core2a-input.json");POOL,_=compile_core2a(C2A_RUN)
G=PHYS/"Core1B"/"golden"/"projectile-vertical-event";REG=load(PHYS/"Core1B"/"registry"/"projectile-vertical-event-atoms-v1.json");AUTH=load(G/"core1a-authority.json");UNIT=load(G/"core1b-unit.json");EVENTS=load(G/"observed-events.json");RECEIPT=build_release_receipt(UNIT,REG,AUTH,EVENTS)
HINT=load(ROOT/"policies"/"physics-core2b-hint-policy.json");ERRORS=load(ROOT/"policies"/"physics-core2b-error-taxonomy.json")
SESSION_V=schema("physics-core2b-session.schema.json");ATTEMPT_V=schema("physics-core2b-attempt-event.schema.json");RETRIEVAL_V=schema("physics-core2b-retrieval-state.schema.json")

def expect(code,fn):
    try:fn()
    except Core2BRuntimeError as e:assert str(e).startswith(code),(code,str(e));return
    raise AssertionError("expected "+code)

def make_session():
    source=POOL["source_items"][0];near=next(x for x in POOL["generated_items"] if x["challenge_id"]=="PHY-C2A-GOLDEN-NEAR-01");rev=next(x for x in POOL["generated_items"] if x["challenge_id"]=="PHY-C2A-GOLDEN-STRUCT-01")
    return {"schema_version":"1.0.0","session_id":"PHY-C2B-INTEGRATION-001","subject":"PHYSICS","purpose":"COMPETITIVE_EXAM","learner_profile_ref":"PHY-LS-P20-DEMO","core2a_binding":{"legal_pool_ref":POOL["product_id"],"legal_pool_digest":digest(POOL)},"capability_bindings":[{"capability_ref":RECEIPT["capability_id"],"problem_family_ref":RECEIPT["problem_family_ref"],"core1b_release_ref":RECEIPT["receipt_id"],"core1b_release_digest":RECEIPT["receipt_digest"],"transfer_events":[]}],"item_overlays":[{"core2a_item_ref":source["item_id"],"display_transfer_label":"T0_DIRECT","structural_distance":"DIRECT","representation_change":False,"model_discrimination":False,"multi_step_bridge":False,"synthesis":False,"competitive_mixing":False,"required_representation":"EVENT_TIMELINE"},{"core2a_item_ref":near["item_id"],"display_transfer_label":"T1_NEAR_TRANSFER","structural_distance":"NEAR","representation_change":False,"model_discrimination":False,"multi_step_bridge":False,"synthesis":False,"competitive_mixing":False,"required_representation":None},{"core2a_item_ref":rev["item_id"],"display_transfer_label":"T3_REVERSED_TARGET","structural_distance":"REVERSED","representation_change":False,"model_discrimination":False,"multi_step_bridge":False,"synthesis":False,"competitive_mixing":False,"required_representation":None}],"retrieval_state":{"schema_version":"1.0.0","retrieval_count":0,"success_streak":0,"next_due_bucket":"MEDIUM","hint_dependence":"NONE","representation_success":[],"last_event_ref":None,"last_event_sequence":0,"previous_state_digest":None,"state_digest":"0"*64}}

S=make_session();SESSION_V.validate(S);RETRIEVAL_V.validate(S["retrieval_state"])
RMAP={RECEIPT["receipt_id"]:RECEIPT};validate_session(S,POOL,RMAP,HINT)
elig=eligible_items(S,POOL,RMAP,HINT);assert {x["overlay"]["display_transfer_label"] for x in elig}=={"T0_DIRECT","T1_NEAR_TRANSFER"}
assert choose_next_item(S,POOL,RMAP,HINT)["overlay"]["display_transfer_label"]=="T1_NEAR_TRANSFER"

bad=copy.deepcopy(S);bad["core2a_binding"]["legal_pool_digest"]="0"*64
expect("CORE2B_CORE2A_LEGAL_POOL_BINDING_MISMATCH",lambda:validate_session(bad,POOL,RMAP,HINT))
bad=copy.deepcopy(S);bad["item_overlays"][2]["structural_distance"]="DIRECT"
expect("CORE2B_TRANSFER_DEMAND_DRIFT",lambda:validate_session(bad,POOL,RMAP,HINT))
bad=copy.deepcopy(S);bad["item_overlays"][1]["representation_change"]=True
expect("CORE2B_REPRESENTATION_SHIFT_NOT_AUTHORIZED_UPSTREAM",lambda:validate_session(bad,POOL,RMAP,HINT))
bad=copy.deepcopy(S);bad["capability_bindings"]=[]
assert eligible_items(bad,POOL,RMAP,HINT)==[]

transfer={"event_id":"C2B-EVT-TRANSFER-0001","event_sequence":1,"item_ref":S["item_overlays"][1]["core2a_item_ref"],"outcome":"PASS","dimensions":["STRUCTURAL_DISTANCE"],"representation_used":None,"hint_level_used":"NO_HINT","delayed_retrieval":False,"evidence_ref":"repo:Core2B/integration/near-pass","evidence_digest":"2"*64}
transfer["event_digest"]=digest(transfer);advanced=copy.deepcopy(S);advanced["capability_bindings"][0]["transfer_events"]=[transfer];SESSION_V.validate(advanced)
assert choose_next_item(advanced,POOL,RMAP,HINT)["overlay"]["display_transfer_label"]=="T3_REVERSED_TARGET"

attempt={"schema_version":"1.0.0","event_id":"C2B-ATTEMPT-0001","event_sequence":1,"item_ref":S["item_overlays"][2]["core2a_item_ref"],"outcome":"INCORRECT","hint_level_used":"NO_HINT","response_evidence":{"model_selected":None,"applicability_statement":None,"first_move":None,"final_answer":None,"physical_check":None},"representation_used":"VY_T_GRAPH","declared_error_hypotheses":[],"evidence_ref":"repo:Core2B/attempt/1","evidence_digest":"3"*64};attempt["event_digest"]=digest(attempt);ATTEMPT_V.validate(attempt)
h=classify_attempt_hypothesis(attempt,ERRORS);assert h["classification_state"]=="HYPOTHESIS" and h["confidence"]=="LOW"
repair=build_core1b_repair_request(S["learner_profile_ref"],RECEIPT["capability_id"],attempt["item_ref"],h,ERRORS);assert repair and repair["authority_mutation_allowed"] is False
current=S["retrieval_state"];new=update_retrieval_state(current,attempt);RETRIEVAL_V.validate(new);assert new["last_event_sequence"]==1 and "VY_T_GRAPH" not in new["representation_success"]

correct=copy.deepcopy(attempt);correct["event_id"]="C2B-ATTEMPT-0002";correct["event_sequence"]=2;correct["outcome"]="CORRECT";correct["event_digest"]=digest_without(correct,"event_digest");ATTEMPT_V.validate(correct);new2=update_retrieval_state(new,correct);RETRIEVAL_V.validate(new2);assert new2["last_event_sequence"]==2 and "VY_T_GRAPH" in new2["representation_success"]

heavy=copy.deepcopy(correct);heavy["event_id"]="C2B-ATTEMPT-0003";heavy["event_sequence"]=3;heavy["hint_level_used"]="FULL_SOLUTION";heavy["representation_used"]="VECTOR_COMPONENTS_2D";heavy["event_digest"]=digest_without(heavy,"event_digest");ATTEMPT_V.validate(heavy);new3=update_retrieval_state(new2,heavy);RETRIEVAL_V.validate(new3);assert "VECTOR_COMPONENTS_2D" not in new3["representation_success"]

gap=copy.deepcopy(heavy);gap["event_id"]="C2B-ATTEMPT-GAP";gap["event_sequence"]=5;gap["event_digest"]=digest_without(gap,"event_digest")
expect("CORE2B_ATTEMPT_SEQUENCE_NOT_APPEND_ONLY",lambda:update_retrieval_state(new3,gap))
print("Physics Core2B runtime tests: PASS (13 guards + schema validation + real Core2A/Core1B integration)")
