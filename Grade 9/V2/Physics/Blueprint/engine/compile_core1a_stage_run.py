#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
def canonical(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v:Any)->str:return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()
def compile_stage_run(spec,join_packet,control_state,policy):
    if join_packet.get("topic_id")!=spec.get("topic_id") or control_state.get("topic_id")!=spec.get("topic_id"): raise AssertionError("CORE1A_TOPIC_BINDING_DRIFT")
    if not join_packet.get("assimilation_ready") or join_packet.get("join_status")=="JOIN_BLOCKED": raise AssertionError("CORE1A_JOIN_NOT_READY")
    if spec.get("join_ref")!=join_packet.get("join_id") or spec.get("join_digest")!=join_packet.get("join_digest"): raise AssertionError("CORE1A_JOIN_BINDING_DRIFT")
    if spec.get("control_state_ref")!=control_state.get("control_state_id") or spec.get("control_digest")!=control_state.get("control_digest"): raise AssertionError("CORE1A_CONTROL_STATE_BINDING_DRIFT")
    stages=policy["pre_manuscript_stages"];results=list(spec.get("stage_results") or [])
    if len(results)>len(stages): raise AssertionError("CORE1A_TOO_MANY_PRE_MANUSCRIPT_STAGES")
    block_reasons=[];seen_block=False
    for i,row in enumerate(results):
        expected=stages[i]
        if row.get("stage")!=expected: raise AssertionError("CORE1A_STAGE_ORDER_DRIFT:"+expected)
        status=row.get("status")
        if status not in {"PASS","BLOCKED"}: raise AssertionError("CORE1A_STAGE_STATUS_INVALID:"+expected)
        if seen_block: raise AssertionError("CORE1A_STAGE_AFTER_BLOCK:"+expected)
        if status=="PASS":
            if not row.get("artifact_refs"): raise AssertionError("CORE1A_PASS_STAGE_ARTIFACT_REQUIRED:"+expected)
            if not row.get("evidence_refs"): raise AssertionError("CORE1A_PASS_STAGE_EVIDENCE_REQUIRED:"+expected)
        else:
            seen_block=True;notes=[str(x).strip() for x in (row.get("notes") or []) if str(x).strip()]
            if not notes: raise AssertionError("CORE1A_BLOCK_REASON_REQUIRED:"+expected)
            block_reasons.append(expected+":"+notes[0])
    unresolved=int(spec.get("unresolved_required_jump_count",0))
    if seen_block:gate="BLOCKED";next_stage=None
    elif len(results)<len(stages):gate="IN_PROGRESS";next_stage=stages[len(results)]
    elif unresolved!=policy["rules"]["unresolved_required_jump_count_must_equal"]:gate="BLOCKED";next_stage=None;block_reasons.append("UNRESOLVED_REQUIRED_JUMPS:"+str(unresolved))
    else:gate="RELEASED";next_stage=policy["manuscript_stage"]
    out={"schema_version":"1.0.0","run_id":spec["run_id"],"topic_id":spec["topic_id"],"join_ref":join_packet["join_id"],"join_digest":join_packet["join_digest"],"control_state_ref":control_state["control_state_id"],"control_digest":control_state["control_digest"],"stage_results":results,"unresolved_required_jump_count":unresolved,"manuscript_gate":gate,"next_stage":next_stage,"block_reasons":block_reasons};out["stage_run_digest"]=digest(out);return out
def main():
    import argparse
    from jsonschema import Draft202012Validator
    ap=argparse.ArgumentParser();ap.add_argument("spec",type=Path);ap.add_argument("--join",type=Path,required=True);ap.add_argument("--control-state",type=Path,required=True);ap.add_argument("--out",type=Path);a=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding="utf-8"));out=compile_stage_run(load(a.spec),load(a.join),load(a.control_state),load(ROOT/"policy"/"core1a-stage-machine.v1.json"));Draft202012Validator(load(ROOT/"contracts"/"core1a-stage-run.schema.json")).validate(out);text=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(text,encoding="utf-8")
    else:print(text,end="")
if __name__=="__main__":main()
