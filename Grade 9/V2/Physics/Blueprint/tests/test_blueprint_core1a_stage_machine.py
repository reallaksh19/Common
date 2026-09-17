#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from copy import deepcopy
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"engine"))
from compile_core1a_stage_run import compile_stage_run
from compile_join import compile_join
from resolve_control_state import resolve_control_state
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def policy():return load(ROOT/"policy"/"core1a-stage-machine.v1.json")
def spec():return load(ROOT/"fixtures"/"core1a"/"stage-run-ready.json")
def join():return compile_join(load(ROOT/"fixtures"/"join"/"join-ready.json"))
def control():return resolve_control_state(load(ROOT/"fixtures"/"control-state"/"m2d-p20-first-study.json"),load(ROOT/"policy"/"purpose-contracts.v1.json"))
def assert_fails(s,code,j=None,c=None):
    try:compile_stage_run(s,j or join(),c or control(),policy())
    except AssertionError as e:assert str(e).startswith(code),str(e)
    else:raise AssertionError("EXPECTED_FAILURE:"+code)
def test_full_pass_releases_manuscript():o=compile_stage_run(spec(),join(),control(),policy());assert o["manuscript_gate"]=="RELEASED" and o["next_stage"]=="1A12_MANUSCRIPT"
def test_partial_prefix_points_to_next_stage():s=spec();s["stage_results"]=s["stage_results"][:3];o=compile_stage_run(s,join(),control(),policy());assert o["manuscript_gate"]=="IN_PROGRESS" and o["next_stage"]=="1A3_COGNITIVE_TRANSFORMATION"
def test_stage_order_is_strict():s=spec();s["stage_results"][2],s["stage_results"][3]=s["stage_results"][3],s["stage_results"][2];assert_fails(s,"CORE1A_STAGE_ORDER_DRIFT")
def test_blocked_stage_stops_later_stages():s=spec();s["stage_results"][3]["status"]="BLOCKED";s["stage_results"][3]["notes"]=["Cognitive transformation unresolved."];assert_fails(s,"CORE1A_STAGE_AFTER_BLOCK")
def test_blocked_prefix_blocks_gate():s=spec();s["stage_results"]=s["stage_results"][:4];s["stage_results"][3]["status"]="BLOCKED";s["stage_results"][3]["notes"]=["Cognitive transformation unresolved."];o=compile_stage_run(s,join(),control(),policy());assert o["manuscript_gate"]=="BLOCKED" and o["next_stage"] is None
def test_pass_stage_requires_artifact_and_evidence():
    s=spec();s["stage_results"][0]["artifact_refs"]=[];assert_fails(s,"CORE1A_PASS_STAGE_ARTIFACT_REQUIRED");s=spec();s["stage_results"][0]["evidence_refs"]=[];assert_fails(s,"CORE1A_PASS_STAGE_EVIDENCE_REQUIRED")
def test_unresolved_required_jumps_block_manuscript():s=spec();s["unresolved_required_jump_count"]=2;o=compile_stage_run(s,join(),control(),policy());assert o["manuscript_gate"]=="BLOCKED" and "UNRESOLVED_REQUIRED_JUMPS:2" in o["block_reasons"]
def test_join_must_be_ready():j=join();j["join_status"]="JOIN_BLOCKED";j["assimilation_ready"]=False;assert_fails(spec(),"CORE1A_JOIN_NOT_READY",j=j)
def test_exact_upstream_digests_are_bound():
    s=spec();s["join_digest"]="0"*64;assert_fails(s,"CORE1A_JOIN_BINDING_DRIFT");s=spec();s["control_digest"]="0"*64;assert_fails(s,"CORE1A_CONTROL_STATE_BINDING_DRIFT")
def test_schema_validates_release():o=compile_stage_run(spec(),join(),control(),policy());Draft202012Validator(load(ROOT/"contracts"/"core1a-stage-run.schema.json")).validate(o)
def test_digest_deterministic():assert compile_stage_run(spec(),join(),control(),policy())["stage_run_digest"]==compile_stage_run(deepcopy(spec()),join(),control(),policy())["stage_run_digest"]
def main():
    ts=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for t in ts:t()
    print(f"Blueprint Core1A stage-machine tests: PASS ({len(ts)} tests)")
if __name__=="__main__":main()
