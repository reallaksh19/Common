#!/usr/bin/env python3
import copy, importlib.util, json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("eng",BASE/"engine"/"build_chemistry_assessment_intake.py")
eng=importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
load=lambda n: json.loads((BASE/"fixtures"/n).read_text(encoding="utf-8"))
S=load("mixed-chemistry-source.fixture.json"); Q=load("mixed-chemistry-question-set.fixture.json")
C=load("mixed-chemistry-external-corpus.fixture.json"); T=load("mixed-chemistry-topic-scope.fixture.json")
A=load("mixed-chemistry-attempt-set.fixture.json")
count=0
def ok(name):
    global count; count+=1; print("PASS",name)
def expect(name,fn,token):
    try: fn()
    except Exception as e:
        assert token in str(e),(name,str(e)); ok(name)
    else: raise AssertionError(name+" did not fail")
o=eng.build(S,Q,C,T,A,"TEST")
assert o["attempt_mode"]=="PRESENT" and o["binding_summary"]["question_count"]==14 and o["binding_summary"]["corpus_candidate_count"]==6; ok("baseline")
n=eng.build(S,Q,C,T,None,"NOATT"); assert n["attempt_mode"]=="ABSENT" and n["attempt_set_ref"] is None; ok("attempt optional")
q=copy.deepcopy(Q); q["questions"][0]["representation"]["charges"]=[]; expect("charge drift detected",lambda:eng.build(S,q,C,T,A,"X"),"QUESTION_SOURCE_DIGEST_MISMATCH")
q=copy.deepcopy(Q); q["questions"][0]["options"].pop(); expect("MCQ option loss",lambda:eng.build(S,q,C,T,A,"X"),"MCQ_OPTION_LOST")
q=copy.deepcopy(Q); q["questions"][13]["subparts"].pop(); expect("subpart loss",lambda:eng.build(S,q,C,T,A,"X"),"QUESTION_PART_MERGED")
q=copy.deepcopy(Q); q["questions"][1]["representation"]["figures"]=[]; expect("figure dependency loss",lambda:eng.build(S,q,C,T,A,"X"),"FIGURE_DEPENDENCY_DROPPED")
s=copy.deepcopy(S); s["units"][0]["statement"]="silently changed"; expect("source assertion mutation",lambda:eng.build(s,Q,C,T,A,"X"),"SOURCE_UNIT_DIGEST_MISMATCH")
c=copy.deepcopy(C); c["candidate_count_declared"]=5; expect("corpus denominator mismatch",lambda:eng.build(S,Q,c,T,A,"X"),"EXTERNAL_CORPUS_DENOMINATOR_MISMATCH")
a=copy.deepcopy(A); a["attempts"][0]["question_ref"]="CQ99"; a["attempt_set_digest"]=eng.digest(a,"attempt_set_digest","attempts","attempt_id"); expect("attempt wrong item",lambda:eng.build(S,Q,C,T,a,"X"),"ATTEMPT_BOUND_TO_WRONG_ITEM")
q=copy.deepcopy(Q); q["questions"]=list(reversed(q["questions"])); assert eng.digest(q,"question_set_digest","questions","question_id")==Q["question_set_digest"]; ok("question reorder identity stable")
s=copy.deepcopy(S); s["units"]=list(reversed(s["units"])); assert eng.digest(s,"source_set_digest","units","source_unit_id")==S["source_set_digest"]; ok("source reorder identity stable")
assert "QUESTION:CQ13" in o["source_quality_summary"]["low_confidence_refs"] and "CORPUS:EXT06" in o["source_quality_summary"]["low_confidence_refs"]; ok("low-confidence preserved")
print("TOTAL_PASS",count)
