#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()[:12].upper()

def build(fixture:dict):
    task,src,ans,profile=fixture['task'],fixture['source_contract'],fixture['answer_contract'],fixture['scaffold_profile']
    if task['treatment']!=src['treatment']: raise ValueError('TREATMENT_DRIFT')
    if task['scaffold_profile_id']!=profile['profile_id']: raise ValueError('SCAFFOLD_PROFILE_DRIFT')
    sections=[]
    for kind in profile['required_kinds']:
        seed=fixture['authoring_seed'].get(kind)
        if not seed: raise ValueError(f'MISSING_AUTHORING_SEED:{kind}')
        sections.append({'kind':kind,'title':seed['title'],'content':seed['content'],'visual_stages':seed.get('visual_stages',0)})
    return {'schema_version':'1.0.0','representation_id':'CORE1-LR-'+digest({'task':task['task_id'],'src':src['source_contract_id']}),'task':task,'source_contract_ref':src['source_contract_id'],'answer_contract_ref':ans['answer_contract_id'],'sections':sections,'practice_ladder':profile['practice_ladder'],'verification':ans['verification_route']+[ans['units_or_dimensions_check']],'transfer_bridge':{'problem_family_ref':src['problem_family_ref'],'first_move':fixture['transfer_first_move'],'do_not_leak_external_items':True}}

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('fixture',type=Path); ap.add_argument('--out',type=Path); a=ap.parse_args(); obj=build(load(a.fixture)); text=json.dumps(obj,indent=2,ensure_ascii=False); a.out.write_text(text+'\n',encoding='utf-8') if a.out else print(text)
if __name__=='__main__': main()
