#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()[:12].upper()
def build(f):
    t,s,a,p=f['task'],f['source_contract'],f['answer_contract'],f['scaffold_profile']
    if t['question_id']!=s['question_id'] or t['question_id']!=a['question_id']: raise ValueError('QUESTION_ID_DRIFT')
    if t['scaffold_profile_id']!=p['profile_id']: raise ValueError('SCAFFOLD_PROFILE_DRIFT')
    hints=f['hint_seed']; expected=p['hint_order']
    if [h['level'] for h in hints]!=expected: raise ValueError('HINT_ORDER_DRIFT')
    stages=f['representation_stages']
    if len(stages)<p['minimum_representation_stages']: raise ValueError('INSUFFICIENT_REPRESENTATION_STAGES')
    return {'schema_version':'1.0.0','representation_id':'CORE2-TR-'+digest({'q':t['question_id'],'src':s['source_digest']}),'task':t,'source_contract_ref':s['source_contract_id'],'answer_contract_ref':a['answer_contract_id'],'source_body':s['source_body'],'figure_semantics':s['figure_semantics'],'core1_link':f['core1_link'],'first_step_reference':f['first_step_reference'],'hints':hints,'representation_stages':stages,'solution':a['solution_steps'],'verification':a['verification_route']}
def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('fixture',type=Path); ap.add_argument('--out',type=Path); x=ap.parse_args(); obj=build(load(x.fixture)); text=json.dumps(obj,indent=2,ensure_ascii=False); x.out.write_text(text+'\n',encoding='utf-8') if x.out else print(text)
if __name__=='__main__': main()
