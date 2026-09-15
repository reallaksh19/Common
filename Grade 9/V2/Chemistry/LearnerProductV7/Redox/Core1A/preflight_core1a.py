#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path

import fitz

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
BP=ROOT/"Grade 9"/"V2"/"Chemistry"/"LearningBlueprint"


def norm(s: str) -> str:
    s=unicodedata.normalize("NFKC",s).replace("–","-").replace("—","-")
    return re.sub(r"\s+"," ",s).strip().lower()


def load(rel: str): return json.loads((BP/rel).read_text(encoding="utf-8"))


def coverage(page: fitz.Page) -> float:
    rects=[]
    for b in page.get_text("blocks"):
        r=fitz.Rect(b[:4])
        if r.width>1 and r.height>1: rects.append(r)
    for d in page.get_drawings():
        r=d.get("rect")
        if r and r.width>1 and r.height>1: rects.append(r)
    if not rects: return 0.0
    pr=page.rect; cols,rows=48,68; used=0
    cw,ch=pr.width/cols,pr.height/rows
    for iy in range(rows):
        y0=iy*ch; y1=y0+ch
        for ix in range(cols):
            cell=fitz.Rect(ix*cw,y0,ix*cw+cw,y1)
            if any(cell.intersects(r) for r in rects): used+=1
    return used/(cols*rows)


def main():
    p=argparse.ArgumentParser(); p.add_argument("pdf"); p.add_argument("manifest"); a=p.parse_args()
    pdf=Path(a.pdf); manifest=json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    authority=load("golden/v7/core1a-study-note-redox-authority.json")
    ttu_doc=load("golden/v5/core1a-hard-study-product.json")
    scope=load("fixtures/engineering-workbench/redox-product-source-scope.v1.json")
    audit=load("policies/chemistry-redox-source-audit.v1.json")

    required={x["object_id"] for x in authority["content_objects"]}
    realized=set(manifest["realized_content_object_ids"])
    assert realized==required, f"content realization mismatch missing={sorted(required-realized)} extra={sorted(realized-required)}"
    assert set(manifest["realized_ttu_ids"])==set(authority["reconstructable_ttu_refs"]), "TTU closure mismatch"
    assert manifest["engineering_custody"]["status"]=="ENGINEERING_CUSTODY_READY"
    assert manifest["pal_validation"]["status"]=="PASS"
    assert manifest["product"]=="CORE1A"
    assert manifest["authority_id"]==authority["authority_id"]
    assert manifest["source_scope_contract_id"]==scope["scope_contract_id"]

    doc=fitz.open(pdf)
    assert 1 <= doc.page_count <= 30, f"page count {doc.page_count} outside HARD ceiling"
    all_text="\n".join(p.get_text("text") for p in doc)
    ntext=norm(all_text)
    assert len(ntext)>1500, "learner product text is unexpectedly thin"

    forbidden=list(authority["learner_surface_policy"]["forbidden_internal_terms"])+audit["learner_surface_policy"]["forbidden_surface_labels"]
    leaks=[term for term in forbidden if norm(term) in ntext]
    assert not leaks, f"learner-surface jargon leak: {leaks}"

    held_tokens=[x for g in scope["held_transformation_guards"] for x in g["detection_tokens"]]
    held_leaks=[tok for tok in held_tokens if norm(tok) in ntext]
    assert not held_leaks, f"held source-scope content leaked: {held_leaks}"

    for source in manifest["practice_source_labels"]:
        assert norm(source) in ntext, f"practice source not learner-visible: {source}"
    assert "answers and checks" in ntext, "answer closure section missing"

    ratios=[]
    for i,page in enumerate(doc):
        txt=norm(page.get_text("text"))
        assert len(txt)>80, f"page {i+1} is effectively blank"
        r=coverage(page); ratios.append(r)
        assert r>=0.43, f"page {i+1} active technical area too low: {r:.3f}"
    assert sum(ratios)/len(ratios)>=0.54, f"mean active technical area too low: {sum(ratios)/len(ratios):.3f}"

    # The two serialized reconstruction experiences must visibly expose blanks and their verification path.
    assert "reconstruct the model" in ntext
    assert "[blank]" in ntext or "____" in ntext
    assert "verification:" in ntext

    result={"status":"PASS","pages":doc.page_count,"mean_active_area":round(sum(ratios)/len(ratios),3),"page_active_area":[round(x,3) for x in ratios],"content_objects":len(realized),"ttus":len(manifest["realized_ttu_ids"]),"practice_questions":len(manifest["practice_question_ids"])}
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()
