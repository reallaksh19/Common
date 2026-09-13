#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def route(question_id:str, question_type:str, guide_demand:str, root:Path=ROOT):
    reg=load(root/'registry'/'physics-core2-scaffold-profiles-v1.json')
    matches=[p for p in reg['profiles'] if p['guide_demand']==guide_demand]
    if len(matches)!=1: raise ValueError('No unique Core2 scaffold profile')
    p=matches[0]
    return {'schema_version':'1.0.0','task_id':f'CORE2-TASK-{question_id}-{guide_demand}','question_id':question_id,'question_type':question_type,'guide_demand':guide_demand,'scaffold_profile_id':p['profile_id'],'required_inputs':['SOURCE_CONTRACT','ANSWER_CONTRACT','CORE1_LINK','SCAFFOLD_PROFILE'],'required_outputs':['TRANSFER_REPRESENTATION','VALIDATION_REPORT']}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--question',required=True); ap.add_argument('--type',choices=['MCQ','NUMERIC','FIGURE'],required=True); ap.add_argument('--guide',choices=['LOW','MEDIUM','HIGH'],required=True); ap.add_argument('--out',type=Path); a=ap.parse_args(); obj=route(a.question,a.type,a.guide); text=json.dumps(obj,indent=2); a.out.write_text(text+'\n') if a.out else print(text)
if __name__=='__main__': main()
