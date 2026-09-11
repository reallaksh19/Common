#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'contracts'
def load(p): return json.loads(Path(p).read_text())
def val(o,n): Draft202012Validator(load(C/n)).validate(o)
def choose(plan,state):
    val(plan,'physics-learning-design-plan.schema.json'); val(state,'interaction-support-state.schema.json')
    if state['design_id']!=plan['design_id']: raise ValueError('design identity mismatch')
    before=json.dumps(plan,sort_keys=True)
    wanted='H3' if state['same_route_failures']>=2 else ('H2' if state['same_route_failures']==1 else 'H1')
    asset=next((x for x in plan['support_assets'] if x['support_id']==wanted),None)
    if not asset: raise ValueError('runtime support asset not pre-approved')
    out={'schema_version':'1.0.0','design_id':plan['design_id'],'support_id':asset['support_id'],'support_type':asset['support_type'],'route':asset['route'],'runtime_mutated_design':False}
    val(out,'support-selection.schema.json')
    if json.dumps(plan,sort_keys=True)!=before: raise AssertionError('runtime mutated frozen design')
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--design',required=True); ap.add_argument('--state',required=True); ap.add_argument('--out',required=True); a=ap.parse_args(); r=choose(load(a.design),load(a.state)); Path(a.out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
