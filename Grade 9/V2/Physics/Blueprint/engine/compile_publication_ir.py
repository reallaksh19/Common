#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from collections import Counter
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
def canonical(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v:Any)->str:return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()
def compile_publication_ir(spec,policy):
    if policy.get("semantic_authority")!="UPSTREAM_ONLY" or policy.get("renderer_authority")!="COMPOSITION_ONLY":raise AssertionError("PUBLICATION_AUTHORITY_POLICY_DRIFT")
    artifacts={}
    semantic={}
    required=[]
    for a in spec.get("upstream_artifacts") or []:
        ref=a.get("artifact_ref")
        if ref in artifacts:raise AssertionError("PUBLICATION_DUPLICATE_UPSTREAM_ARTIFACT:"+str(ref))
        if a.get("release_state")!="RELEASED":raise AssertionError("PUBLICATION_UPSTREAM_NOT_RELEASED:"+str(ref))
        artifacts[ref]=a
        for s in a.get("semantic_units") or []:
            key=s.get("semantic_ref")
            if key in semantic:raise AssertionError("PUBLICATION_SEMANTIC_REF_COLLISION:"+str(key))
            semantic[key]={**s,"role":a.get("role"),"artifact_ref":ref}
            if s.get("required"):required.append(key)
    if not artifacts or not semantic:raise AssertionError("PUBLICATION_UPSTREAM_AUTHORITY_REQUIRED")
    requested=spec.get("publication_units") or []
    counts=Counter(str(x.get("semantic_ref")) for x in requested)
    missing=sorted(x for x in required if counts[x]==0);dups=sorted(x for x in required if counts[x]>1)
    if missing:raise AssertionError("PUBLICATION_REQUIRED_REF_MISSING:"+",".join(missing))
    if dups:raise AssertionError("PUBLICATION_REQUIRED_REF_DUPLICATED:"+",".join(dups))
    units=[];unknown=[];mismatches=[];rep_bad=[]
    for i,row in enumerate(requested,1):
        ref=str(row.get("semantic_ref","")).strip()
        if ref not in semantic:unknown.append(ref);continue
        src=semantic[ref]
        if row.get("source_role")!=src["role"] or row.get("source_artifact_ref")!=src["artifact_ref"]:raise AssertionError("PUBLICATION_SOURCE_ROLE_DRIFT:"+ref)
        if row.get("content_digest")!=src.get("content_digest"):mismatches.append(ref)
        allowed=set(src.get("authorized_representation_refs") or []);used=set(row.get("representation_refs") or [])
        if not used.issubset(allowed):rep_bad.append(ref)
        units.append({"unit_id":f"PUBUNIT-PHY-{i:04d}","source_role":src["role"],"source_artifact_ref":src["artifact_ref"],"semantic_ref":ref,"content_digest":row["content_digest"],"surface_kind":row["surface_kind"],"representation_refs":sorted(used)})
    if unknown:raise AssertionError("PUBLICATION_UNKNOWN_SEMANTIC_REF:"+",".join(sorted(unknown)))
    if mismatches:raise AssertionError("PUBLICATION_CONTENT_DIGEST_MISMATCH:"+",".join(sorted(mismatches)))
    if rep_bad:raise AssertionError("PUBLICATION_REPRESENTATION_NOT_AUTHORIZED:"+",".join(sorted(rep_bad)))
    audit={"required_semantic_ref_count":len(required),"placed_required_ref_count":len(required),"missing_refs":[],"duplicate_refs":[],"unknown_refs":[],"digest_mismatches":[],"representation_violations":[],"status":"PASS"}
    upstream=[{"role":a["role"],"artifact_ref":a["artifact_ref"],"artifact_digest":a["artifact_digest"],"release_state":"RELEASED"} for a in spec["upstream_artifacts"]]
    out={"schema_version":"1.0.0","publication_ir_id":spec["publication_ir_id"],"topic_id":spec["topic_id"],"product_mode":spec["product_mode"],"authority_boundary":{"semantic_authority":"UPSTREAM_ONLY","renderer_authority":"COMPOSITION_ONLY","renderer_may_introduce_semantic_claims":False,"renderer_may_substitute_representation":False},"upstream_artifacts":upstream,"units":units,"lossless_audit":audit};out["publication_ir_digest"]=digest(out);return out
def main():
    import argparse
    from jsonschema import Draft202012Validator
    ap=argparse.ArgumentParser();ap.add_argument("spec",type=Path);ap.add_argument("--out",type=Path);a=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding="utf-8"));out=compile_publication_ir(load(a.spec),load(ROOT/"policy"/"publication-boundary.v1.json"));Draft202012Validator(load(ROOT/"contracts"/"publication-ir.schema.json")).validate(out);text=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(text,encoding="utf-8")
    else:print(text,end="")
if __name__=="__main__":main()
