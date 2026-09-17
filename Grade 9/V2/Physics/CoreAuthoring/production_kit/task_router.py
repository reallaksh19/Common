#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def route(treatment:str, prior:int, difficulty:str, root:Path=ROOT):
    reg=load(root/'registry'/'physics-core1-scaffold-profiles-v1.json')
    candidates=[p for p in reg['profiles'] if p['treatment']==treatment and (p['prior_knowledge_pct']==prior or treatment=='READY_VERIFY_ONLY')]
    if len(candidates)!=1: raise ValueError(f'No unique Core1 scaffold for {treatment=} {prior=}')
    profile=candidates[0]
    return {'schema_version':'1.0.0','task_id':f'CORE1-TASK-{treatment}-P{prior}-{difficulty}','treatment':treatment,'prior_knowledge_pct':prior,'difficulty':difficulty,'scaffold_profile_id':profile['profile_id'],'required_inputs':['SOURCE_CONTRACT','ANSWER_CONTRACT','SCAFFOLD_PROFILE'],'required_outputs':['LEARNING_REPRESENTATION','VALIDATION_REPORT']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--treatment',choices=['FULL_LEARNING','READY_VERIFY_ONLY','PROBE_FIRST'],required=True); ap.add_argument('--prior',type=int,choices=[20,50],default=20); ap.add_argument('--difficulty',choices=['D1','D2','D3','D4'],default='D2'); ap.add_argument('--out',type=Path)
    a=ap.parse_args(); obj=route(a.treatment,a.prior,a.difficulty); text=json.dumps(obj,indent=2)
    a.out.write_text(text+'\n') if a.out else print(text)
if __name__=='__main__': main()
