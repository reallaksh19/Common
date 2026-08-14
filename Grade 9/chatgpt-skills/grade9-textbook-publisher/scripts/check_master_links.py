#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2: print("Usage: check_master_links.py master.json",file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); e=[]; cs=d.get("concepts",[]); cids={c.get("concept_id") for c in cs if c.get("concept_id")}; qr=d.get("questions",{}); qs=qr.get("anchors",[])+qr.get("core_calibrated",[])+qr.get("challenges",[]); qids={q.get("id") for q in qs if q.get("id")}
    for q in qs:
        qid=q.get("id","<missing>"); pc=q.get("primary_concept_id")
        if pc not in cids:e.append(f"{qid}: primary concept {pc!r} not found")
    for c in cs:
        cid=c.get("concept_id","<missing>")
        for f in ("primary_anchor_ids","same_level_question_ids","challenge_question_ids"):
            for qid in c.get(f,[]):
                if qid not in qids:e.append(f"{cid}: {f} references missing question {qid}")
    if e:
        print("GRADE 9 MASTER LINK CHECK: FAIL"); [print("- "+x) for x in e]; return 1
    print("GRADE 9 MASTER LINK CHECK: PASS"); return 0
if __name__=="__main__": raise SystemExit(main())
