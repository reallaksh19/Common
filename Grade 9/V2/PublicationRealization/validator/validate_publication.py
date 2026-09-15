#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical_bytes(o): return (json.dumps(o,sort_keys=True,separators=(",",":"))+"\n").encode()
def package_digest(a): return sha(canonical_bytes(sorted(a,key=lambda x:(x["role"],x["path"]))))

def validate(product,structure,pmap,audit,manifest,pdf,target):
    material=[x["content_id"] for x in product["content_items"] if x["materiality"]=="MATERIAL"]
    srefs=[r for p in structure["page_intents"] for r in p["content_refs"]]
    if sorted(material)!=sorted(srefs) or len(srefs)!=len(set(srefs)): raise ValueError("semantic material custody failure")
    placements=pmap["content_placements"]; prefs=[x["content_ref"] for x in placements]
    if sorted(srefs)!=sorted(prefs) or len(prefs)!=len(set(prefs)): raise ValueError("structure to placement custody failure")
    if not pmap.get("actual_placement_evidence"): raise ValueError("planned placement is not physical evidence")
    w=target["paper"]["width_pt"]; h=target["paper"]["height_pt"]
    for x in placements:
        if not (0 <= x["x0"] < x["x1"] <= w and 0 <= x["y0"] < x["y1"] <= h): raise ValueError("out of bounds placement")
        if x["fragment_kind"]=="CONTINUATION":
            pi=next(p for p in pmap["page_intents"] if p["page_intent_id"]==x["page_intent_id"])
            if x["page"] not in pi["continuation_pages"] or not pi["split"]: raise ValueError("orphan continuation")
    for pi in pmap["page_intents"]:
        actual=sorted({x["page"] for x in placements if x["page_intent_id"]==pi["page_intent_id"]})
        if actual!=sorted(pi["physical_pages"]): raise ValueError("page intent reconciliation failure")
    pdfsha=sha(pdf)
    if pdfsha!=pmap["artifact_sha256"] or pdfsha!=audit["artifact_evidence"]["sha256"]: raise ValueError("artifact hash drift")
    cand=[x for x in manifest["artifacts"] if x["role"]=="CANDIDATE_PDF"]
    if len(cand)!=1 or cand[0]["sha256"]!=pdfsha or cand[0]["bytes"]!=len(pdf): raise ValueError("manifest pdf binding failure")
    if any(x["path"]=="publication_manifest.json" for x in manifest["artifacts"]): raise ValueError("self-referential manifest")
    if manifest["package_digest"]!=package_digest(manifest["artifacts"]): raise ValueError("package digest mismatch")
    qs=audit["quality_states"]
    if qs!={"subject_correctness":"PENDING","pedagogy_usability":"PENDING","visual_usability":"PENDING","benchmark_comparative_validation":"NOT_RUN"}:
        raise ValueError("engineering pass illegally implies downstream quality")
    if audit["publication_engineering"]!="PASS": raise ValueError("engineering audit not pass")
    return True

def validate_dir(out, product_path, target_path):
    out=Path(out); product=load(product_path); target=load(target_path)
    return validate(product,load(out/"publication_structure.json"),load(out/"physical_page_map.json"),load(out/"publication_audit.json"),load(out/"publication_manifest.json"),(out/"candidate.pdf").read_bytes(),target)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); ap.add_argument("--product",required=True); ap.add_argument("--target",required=True)
    a=ap.parse_args(); validate_dir(a.out,a.product,a.target); print("V2-06 independent publication validation: PASS")
if __name__=="__main__": main()
