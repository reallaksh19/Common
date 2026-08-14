#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2: print("Usage: validate_bank.py master.json",file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); e=[]; p=d.get("project",{})
    if p.get("grade")!=9:e.append("project.grade must be 9")
    cs=d.get("concepts",[]); ids=[c.get("concept_id") for c in cs]; valid={x for x in ids if x}
    if len(ids)!=len(set(ids)):e.append("duplicate concept_id values found")
    qr=d.get("questions",{}); a=qr.get("anchors",[]); c=qr.get("core_calibrated",[]); h=qr.get("challenges",[]); qs=a+c+h; qids=[q.get("id") for q in qs]
    if len(qids)!=len(set(qids)):e.append("duplicate question IDs found")
    for q in qs:
        qid=q.get("id","<missing>"); pc=q.get("primary_concept_id")
        if not pc:e.append(f"{qid}: missing primary_concept_id")
        elif pc not in valid:e.append(f"{qid}: unknown primary_concept_id {pc}")
        if not q.get("provenance_class"):e.append(f"{qid}: missing provenance_class")
        if not q.get("question"):e.append(f"{qid}: missing question text")
    if p.get("core_question_count") is not None and len(a)+len(c)!=p["core_question_count"]:e.append("Core count mismatch")
    if p.get("challenge_question_count") is not None and len(h)!=p["challenge_question_count"]:e.append("Challenge count mismatch")
    if e:
        print("GRADE 9 BANK VALIDATION: FAIL"); [print("- "+x) for x in e]; return 1
    print("GRADE 9 BANK VALIDATION: PASS"); return 0
if __name__=="__main__": raise SystemExit(main())
