#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = ROOT.parents[3]


class ScopedEvidenceError(Exception):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def repo_path(rel: str) -> Path:
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_REF_OUTSIDE_REPOSITORY")
    path = REPO / p
    if not path.exists() or not path.is_file():
        raise ScopedEvidenceError("SCOPED_EVIDENCE_REF_MISSING:" + rel)
    return path


def load_repo_json(rel: str) -> dict[str, Any]:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))


def validate_schema(name: str, value: dict[str, Any]) -> None:
    Draft202012Validator(load_schema(name)).validate(value)


def _verify_assertions(envelope: dict[str, Any]) -> None:
    for row in envelope["repository_assertions"]:
        text = repo_path(row["path"]).read_text(encoding="utf-8")
        missing = [needle for needle in row["contains_all"] if needle not in text]
        if missing:
            raise ScopedEvidenceError("SCOPED_EVIDENCE_ASSERTION_FAILED:" + row["path"] + ":" + ",".join(missing))


def _metric(value: int, basis: str) -> dict[str, Any]:
    return {"value": int(value), "basis": basis}


def compile_scoped_evidence(envelope: dict[str, Any]) -> dict[str, Any]:
    validate_schema("scoped-execution-envelope.schema.json", envelope)
    _verify_assertions(envelope)
    topic = load_repo_json(envelope["topic_blueprint_ref"])
    if topic.get("topic_id") != envelope["topic_id"]: raise ScopedEvidenceError("SCOPED_EVIDENCE_TOPIC_MISMATCH")
    if int(topic.get("grade")) != int(envelope["grade"]): raise ScopedEvidenceError("SCOPED_EVIDENCE_GRADE_MISMATCH")
    for ref in envelope["semantic_evidence_refs"] + envelope["curriculum_authority_refs"] + envelope["assessment_coverage"]["evidence_refs"]: repo_path(ref)
    corpus_path = repo_path(envelope["assessment_corpus_ref"])
    coverage=envelope["assessment_coverage"]; state=coverage["state"]; matched=int(coverage["matched_target_item_count"]); issues=list(coverage.get("unresolved_issues") or [])
    if state=="VERIFIED_NO_TARGET_DEMAND" and matched!=0: raise ScopedEvidenceError("SCOPED_EVIDENCE_ZERO_DEMAND_COUNT_MISMATCH")
    if state=="DEMANDS_PRESENT" and matched<1: raise ScopedEvidenceError("SCOPED_EVIDENCE_PRESENT_DEMAND_COUNT_REQUIRED")
    if state=="COVERAGE_UNKNOWN" and not issues: raise ScopedEvidenceError("SCOPED_EVIDENCE_UNKNOWN_REQUIRES_ISSUE")
    parent=copy.deepcopy(topic["evidence"]); evidence=copy.deepcopy(parent)
    evidence["ground_truth_refs"]=list(dict.fromkeys([envelope["topic_blueprint_ref"],envelope["assessment_corpus_ref"]]+envelope["semantic_evidence_refs"]+coverage["evidence_refs"]+envelope["curriculum_authority_refs"]))
    pm=parent["metrics"]; ps=parent["sources"]; has_semantic=bool(envelope["semantic_evidence_refs"])
    if has_semantic:
        evidence["sources"]["semantic_source"]=copy.deepcopy(ps["semantic_source"]); evidence["sources"]["semantic_source"]["notes"]=list(evidence["sources"]["semantic_source"].get("notes") or [])+["Scoped semantic evidence is bound to exact repository refs for this execution envelope."]; ss=int(pm["SS"]["value"])
    else:
        evidence["sources"]["semantic_source"]={"availability":"ABSENT","authority_strength":0,"granularity":"NONE","integrity_state":"NOT_APPLICABLE","notes":["No target-scoped semantic evidence refs were supplied."]}; ss=0
    if state=="VERIFIED_NO_TARGET_DEMAND":
        evidence["sources"]["question_corpus"]={"availability":"ABSENT","authority_strength":0,"granularity":"DETAILED","count":0,"integrity_state":"NOT_APPLICABLE","notes":["Target-scoped corpus audit verified zero matching demand items; topic-wide question richness is not inherited."]}; evidence["sources"]["answer_key"]={"availability":"ABSENT","authority_strength":0,"granularity":"NONE","count":0,"integrity_state":"NOT_APPLICABLE","notes":["No target demand item exists, so no target answer-key demand is projected."]}; qe=qr=0; ua=int(pm["UA"]["value"])
    elif state=="DEMANDS_PRESENT":
        evidence["sources"]["question_corpus"]=copy.deepcopy(ps["question_corpus"]); evidence["sources"]["question_corpus"]["count"]=matched; evidence["sources"]["answer_key"]=copy.deepcopy(ps["answer_key"]); qe=int(pm["QE"]["value"]); qr=int(pm["QR"]["value"]); ua=int(pm["UA"]["value"])
    else:
        evidence["sources"]["question_corpus"]={"availability":"PARTIAL","authority_strength":0,"granularity":"NONE","count":matched,"integrity_state":"AMBIGUOUS","notes":issues}; evidence["sources"]["answer_key"]={"availability":"PARTIAL","authority_strength":0,"granularity":"NONE","integrity_state":"AMBIGUOUS","notes":issues}; qe=qr=0; ua=max(3,int(pm["UA"]["value"]))
    evidence["metrics"]={"SA":_metric(int(pm["SA"]["value"]),"Scope authority cannot be strengthened by narrowing; inherited as the parent-topic ceiling."),"SS":_metric(ss,"Semantic strength is inherited only when exact target-scoped semantic evidence refs exist."),"QE":_metric(qe,"Question evidence is target-scoped; verified zero target demand forces QE=0."),"QR":_metric(qr,"Demand resolution is target-scoped; verified zero target demand forces QR=0."),"UA":_metric(ua,"Unknown target coverage raises uncertainty; otherwise parent uncertainty is retained."),"CI":_metric(int(pm["CI"]["value"]),"Conflict severity is not reduced by scope projection without a separate adjudication.")}
    validate_schema("evidence-state.schema.json",evidence)
    scope_descriptor={"subject":envelope["subject"],"grade":envelope["grade"],"scope_kind":envelope["scope_kind"],"topic_id":envelope["topic_id"],"scope_ref":envelope["scope_ref"],"requested_curriculum":envelope["requested_curriculum"],"required_gate_ids":envelope["required_gate_ids"]}; scope_digest=digest(scope_descriptor)
    assessment_coverage={"state":state,"matched_target_item_count":matched,"scope_digest":scope_digest,"corpus_digest":file_digest(corpus_path),"evidence_refs":list(coverage["evidence_refs"]),"unresolved_issues":issues}
    curriculum_status="SUPPORTED_BY_REPOSITORY_AUTHORITY" if envelope["requested_curriculum"]=="REPOSITORY_GOVERNED_PHYSICS" or envelope["curriculum_authority_refs"] else "HELD_INSUFFICIENT_AUTHORITY"
    receipt={"schema_version":"1.0.0","receipt_id":envelope["envelope_id"].replace("SCOPE-PHY-","SCOPED-EVIDENCE-PHY-",1),"derivation":"SCOPED_EVIDENCE_COMPILER_V1","scope_kind":envelope["scope_kind"],"scope_ref":envelope["scope_ref"],"topic_id":envelope["topic_id"],"grade":envelope["grade"],"requested_curriculum":envelope["requested_curriculum"],"curriculum_status":curriculum_status,"required_gate_ids":list(envelope["required_gate_ids"]),"parent_topic_blueprint_ref":envelope["topic_blueprint_ref"],"parent_topic_blueprint_digest":str(topic["topic_blueprint_digest"]),"scope_digest":scope_digest,"assessment_coverage":assessment_coverage,"evidence":evidence,"evidence_digest":digest(evidence),"repository_assertion_count":len(envelope["repository_assertions"]),"receipt_digest":""}
    receipt["receipt_digest"]=digest({k:v for k,v in receipt.items() if k!="receipt_digest"}); validate_schema("scoped-evidence-receipt.schema.json",receipt); return receipt


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("envelope",type=Path); ap.add_argument("--out",type=Path); a=ap.parse_args(); result=compile_scoped_evidence(json.loads(a.envelope.read_text(encoding="utf-8"))); text=json.dumps(result,indent=2,ensure_ascii=False)+"\n"; a.out.write_text(text,encoding="utf-8") if a.out else print(text,end="")
if __name__=="__main__": main()
