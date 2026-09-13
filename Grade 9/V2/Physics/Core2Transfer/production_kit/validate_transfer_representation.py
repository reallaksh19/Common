#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def norm(s): return ' '.join(str(s).lower().split())
def validate(rep,f,root:Path=ROOT):
    schemas={
        'source':load(root/'contracts'/'physics-core2-source-contract.schema.json'),
        'answer':load(root/'contracts'/'physics-core2-answer-contract.schema.json'),
        'task':load(root/'contracts'/'physics-core2-production-task.schema.json'),
        'representation':load(root/'contracts'/'physics-core2-transfer-representation.schema.json')
    }
    Draft202012Validator(schemas['source']).validate(f['source_contract']); Draft202012Validator(schemas['answer']).validate(f['answer_contract']); Draft202012Validator(schemas['task']).validate(f['task']); Draft202012Validator(schemas['representation']).validate(rep)
    src,ans,p=f['source_contract'],f['answer_contract'],f['scaffold_profile']
    if rep['source_body']!=src['source_body']: raise AssertionError('SOURCE_BODY_REWRITTEN')
    if rep['figure_semantics']!=src['figure_semantics']: raise AssertionError('SOURCE_FIGURE_LOST')
    if len(rep['representation_stages'])<p['minimum_representation_stages']: raise AssertionError('INSUFFICIENT_REPRESENTATION_STAGES')
    if [h['level'] for h in rep['hints']]!=p['hint_order']: raise AssertionError('HINT_LADDER_COLLAPSES')
    forbidden=[ans['canonical_answer'],*ans['forbidden_hint_tokens']]
    for h in rep['hints']:
        text=norm(h['text'])
        for token in forbidden:
            if token and norm(token) in text: raise AssertionError(f'HINT_REVEALS_ANSWER:{h["level"]}:{token}')
    h1=norm(rep['hints'][0]['text']); h2=norm(rep['hints'][1]['text']); h3=norm(rep['hints'][2]['text'])
    if any(x in h1 for x in ['=', 'substitute', 'calculate']): raise AssertionError('H1_NOTICE_SKIPPED')
    if any(x in h2 for x in ['substitute','answer is','option ']): raise AssertionError('H2_TOO_SPECIFIC')
    if any(x in h3 for x in ['answer is','option ']): raise AssertionError('H3_REVEALS_RESULT')
    if not rep['core1_link']['lesson_ref'] or not rep['core1_link']['capability_ref']: raise AssertionError('CORE1_LINK_MISSING')
    if src['production_claim'] and 'synthetic' in src['provenance_note'].lower(): raise AssertionError('SYNTHETIC_CORPUS_CLAIMED_AS_PRODUCTION')
    return {'status':'PASS','representation_id':rep['representation_id'],'checks':['SCHEMAS','TASK_CONTRACT','REPRESENTATION_CONTRACT','SOURCE_CUSTODY','HINT_GRADATION','ANSWER_NONLEAKAGE','CORE1_LINK','REPRESENTATION_DEPTH']}
def main():
    import argparse
    from build_transfer_representation import build
    ap=argparse.ArgumentParser(); ap.add_argument('fixture',type=Path); a=ap.parse_args(); f=load(a.fixture); print(json.dumps(validate(build(f),f),indent=2))
if __name__=='__main__': main()
