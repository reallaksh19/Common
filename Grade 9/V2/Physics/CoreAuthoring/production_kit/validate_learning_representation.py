#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def validate(rep, fixture, root:Path=ROOT):
    schemas={
        'source': load(root/'contracts'/'physics-core1-source-contract.schema.json'),
        'answer': load(root/'contracts'/'physics-core1-answer-contract.schema.json'),
        'task': load(root/'contracts'/'physics-core1-production-task.schema.json'),
        'representation': load(root/'contracts'/'physics-core1-learning-representation.schema.json'),
    }
    Draft202012Validator(schemas['source']).validate(fixture['source_contract'])
    Draft202012Validator(schemas['answer']).validate(fixture['answer_contract'])
    Draft202012Validator(schemas['task']).validate(fixture['task'])
    Draft202012Validator(schemas['representation']).validate(rep)
    if fixture['task'].get('treatment') not in {'FULL_LEARNING','READY_VERIFY_ONLY','PROBE_FIRST'}: raise AssertionError('BAD_TASK_TREATMENT')
    profile=fixture['scaffold_profile']; kinds={s['kind'] for s in rep['sections']}
    missing=set(profile['required_kinds'])-kinds
    if missing: raise AssertionError('MISSING_REQUIRED_KINDS:'+','.join(sorted(missing)))
    if sum(s['visual_stages'] for s in rep['sections']) < profile['minimum_visual_stages']: raise AssertionError('INSUFFICIENT_VISUAL_STAGING')
    if rep['practice_ladder']!=profile['practice_ladder']: raise AssertionError('PRACTICE_LADDER_DRIFT')
    if fixture['source_contract']['external_candidate_refs']: raise AssertionError('CORE2_TRANSFER_LEAKAGE_IN_CORE1')
    if fixture['task']['treatment']=='READY_VERIFY_ONLY' and any(k in kinds for k in {'SEE','REALIZE','UNDERSTAND'}): raise AssertionError('READY_VERIFY_RETAUGHT')
    if fixture['task']['treatment']=='PROBE_FIRST' and kinds!={'PROBE'}: raise AssertionError('PROBE_FIRST_RETAUGHT')
    if not rep['transfer_bridge']['do_not_leak_external_items']: raise AssertionError('TRANSFER_CUSTODY_LOST')
    return {'status':'PASS','representation_id':rep['representation_id'],'checks':['SCHEMAS','TASK_CONTRACT','REPRESENTATION_CONTRACT','TREATMENT','SCAFFOLD','VISUAL_STAGING','PRACTICE_LADDER','TRANSFER_CUSTODY']}

def main():
    import argparse
    from build_learning_representation import build
    ap=argparse.ArgumentParser(); ap.add_argument('fixture',type=Path); a=ap.parse_args(); f=load(a.fixture); print(json.dumps(validate(build(f),f),indent=2))
if __name__=='__main__': main()
