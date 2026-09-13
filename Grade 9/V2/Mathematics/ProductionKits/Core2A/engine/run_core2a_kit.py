#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import jsonschema
HERE=Path(__file__).resolve(); MATH=HERE.parents[3]; PK=MATH/'ProductionKits'; COMMON=PK/'common'/'engine'; sys.path.insert(0,str(COMMON))
from production_primitives import route_task, validate_source_bundle, validate_bound_object, load_scaffold_profiles, build_scaffold_plan, validate_answer_contract, validate_provenance, build_blueprint_id, canonical
REQUIRED_ROLES={'CORE1A_BUCKET_PLAN','CORE2_PLAN'}; DEMAND_RANK={'EASY':1,'MEDIUM':2,'HARD':3}; STRUCTURAL_SLOTS={'HIDDEN_INFORMATION','REVERSED_TARGET','REPRESENTATION_SHIFT','PARAMETER_CONSTRAINT'}
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def norm(t): return re.sub(r'\s+',' ',str(t).strip().lower())
def bucket_maps(plan):
    by={b['bucket_id']:b for b in plan['buckets']}; qmap={}
    for b in plan['buckets']:
        for q in b.get('core2_question_refs') or []:
            if q in qmap and qmap[q]!=b['bucket_id']: raise ValueError('CORE2A_SOURCE_QUESTION_MULTI_BUCKET:'+q)
            qmap[q]=b['bucket_id']
    return by,qmap
def representative_page(pages): return sorted(pages,key=lambda p:(-DEMAND_RANK.get(p.get('guide_demand_badge',{}).get('label','EASY'),0),p['source_order']))[0]
def source_selection(purpose,bucket,pages_by_id):
    pages=sorted([pages_by_id[q] for q in bucket.get('core2_question_refs') or [] if q in pages_by_id],key=lambda p:p['source_order'])
    if not pages:return []
    if purpose=='PRACTICE':return pages
    if purpose in {'REVISION','COMPETITION'}:return [representative_page(pages)]
    return [pages[0]]
def source_question_spec(page,bucket_ref,scaffold,ans):
    h=page['hint_ladder']; reasoning=[str(x.get('mathematical_transition','')).strip() for x in page.get('reasoning_route',{}).get('steps',[]) if str(x.get('mathematical_transition','')).strip()]; working=[str(x) for x in page['solution_route'].get('steps') or []]; checks=[x if isinstance(x,str) else canonical(x) for x in page['solution_route'].get('verification_checks') or []]
    prov={'question_origin':'SOURCE_CORE2','display_inline':True,'learner_label':'Where this question came from','citations':[{'citation_kind':'CORE2_SOURCE','label':f"Core (2) {page['question_ref']}",'locator':page['question_ref'],'use':'SOURCE_TEXT','text_relation':'EXACT_SOURCE','url':None}],'official_past_question_claim':False,'verified_official_source_ref':page['source_ref']}; validate_provenance(prov)
    return {'question_id':page['question_ref'],'question_class':'SOURCE_CORE2','bucket_refs':[bucket_ref],'prompt':page['source_stem'],'source_order':page['source_order'],'scaffold_plan_ref':scaffold['scaffold_plan_id'],'provenance':prov,'answer_contract':ans,'learner_support':{'TRY IT FIRST':True,'SMALL CLUE':h['H1']['text'],'BIGGER CLUE':h['H2']['text'],'HOW DO I START?':h['H3']['text'],'THINK IT THROUGH':reasoning,'FULL WORKING':working,'QUICK CHECK':checks}}
def validate_candidate(item,purpose,buckets):
    if purpose not in item['eligible_purposes']: raise ValueError('CORE2A_CANDIDATE_WRONG_PURPOSE:'+item['candidate_id'])
    if any(r not in buckets for r in item['bucket_refs']): raise ValueError('CORE2A_CANDIDATE_UNKNOWN_BUCKET:'+item['candidate_id'])
    taught=set(); [taught.update(buckets[r]['member_capability_refs']) for r in item['bucket_refs']]; extra=sorted(set(item['required_capability_refs'])-taught)
    if extra: raise ValueError('CORE2A_UNTAUGHT_MATH_REQUIRED:'+item['candidate_id']+':'+','.join(extra))
    validate_answer_contract(item['answer_contract']); validate_provenance(item['provenance'],purpose)
    if item['novelty_check']['status']!='PASS': raise ValueError('CORE2A_NEAR_COPY_CHECK_FAILED:'+item['candidate_id'])
    full=[norm(x) for x in item['full_working']]
    for label,text in item['staged_help'].items():
        nt=norm(text)
        if not nt: raise ValueError(f"CORE2A_HELP_EMPTY:{item['candidate_id']}:{label}")
        if nt in full: raise ValueError(f"CORE2A_HINT_DISCLOSES_SOLUTION:{item['candidate_id']}:{label}")
    ca=item['answer_contract'].get('canonical_answer')
    if isinstance(ca,(str,int,float)) and str(ca).strip():
        a=norm(ca)
        if len(a)>=2 and any(a in norm(v) for v in item['staged_help'].values()): raise ValueError('CORE2A_HINT_DISCLOSES_ANSWER:'+item['candidate_id'])
    if purpose=='COMPETITION' and not any(c.get('citation_kind')=='COMPETITION_BENCHMARK' for c in item['provenance']['citations']): raise ValueError('CORE2A_COMPETITION_BENCHMARK_MISSING:'+item['candidate_id'])
def check_candidate_coverage(purpose,buckets,candidates):
    if purpose=='REVISION': return
    by={bid:[] for bid in buckets}
    for c in candidates:
        for bid in c['bucket_refs']:
            if bid in by: by[bid].append(c)
    missing=[]
    for bid,rows in by.items():
        if purpose=='STARTER':
            if not any(x['slot']=='GUIDED_DIRECT' for x in rows): missing.append(bid+':GUIDED_DIRECT')
        elif purpose=='PRACTICE':
            if not any(x['slot'] in {'NEAR_TRANSFER','REPRESENTATION_VARIATION','GUIDED_DIRECT'} for x in rows): missing.append(bid+':PRACTICE_FRESH')
        elif purpose=='COMPETITION':
            if not any(x['slot']=='NEAR_TRANSFER' for x in rows): missing.append(bid+':NEAR_TRANSFER')
            if not any(x['slot'] in STRUCTURAL_SLOTS for x in rows): missing.append(bid+':STRUCTURAL_VARIATION')
    if missing: raise ValueError('CORE2A_PURPOSE_CANDIDATE_COVERAGE_GAP:'+','.join(missing))
def derived_revision_prompts(bucket):
    prompts=[f"Without looking back, explain this idea in your own words: {bucket['bucket_invariant']['text']}"]
    if bucket.get('learning_atoms'): prompts.append('Which clue in a question would tell you to use this idea rather than a nearby method?')
    return prompts
def build_candidate_spec(item,scaffold):
    return {'question_id':item['candidate_id'],'question_class':'GENERATED_CHALLENGE','bucket_refs':item['bucket_refs'],'slot':item['slot'],'prompt':item['prompt'],'scaffold_plan_ref':scaffold['scaffold_plan_id'],'provenance':item['provenance'],'answer_contract':item['answer_contract'],'learner_support':{'TRY IT FIRST':True,'SMALL CLUE':item['staged_help']['small_clue'],'BIGGER CLUE':item['staged_help']['bigger_clue'],'HOW DO I START?':item['staged_help']['how_do_i_start'],'THINK IT THROUGH':item['think_it_through'],'FULL WORKING':item['full_working'],'QUICK CHECK':item['quick_check']},'novelty_check':item['novelty_check']}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--intent',required=True); ap.add_argument('--source-bundle',required=True); ap.add_argument('--core1a-bucket-plan',required=True); ap.add_argument('--core2-plan',required=True); ap.add_argument('--core2-answer-contracts',required=True); ap.add_argument('--candidate-set'); ap.add_argument('--scaffold-profiles',default=str(PK/'common'/'profiles'/'scaffold-profiles.json')); ap.add_argument('--out-dir',required=True); a=ap.parse_args()
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); intent=load(a.intent); routed=route_task(intent); (out/'routing_result.json').write_text(json.dumps(routed,indent=2)+'\n',encoding='utf-8')
    if routed['status']!='ROUTED': print(routed['question']); raise SystemExit(2)
    if routed['stage']!='CORE2A': raise ValueError('CORE2A_KIT_WRONG_STAGE')
    purpose=routed['purpose']; bundle=load(a.source_bundle); validate_source_bundle(bundle,REQUIRED_ROLES); c1a=load(a.core1a_bucket_plan); c2=load(a.core2_plan)
    validate_bound_object(bundle,'CORE1A_BUCKET_PLAN',c1a,ref_fields=('bucket_plan_id',),digest_fields=('plan_digest',)); validate_bound_object(bundle,'CORE2_PLAN',c2,ref_fields=('plan_id',),digest_fields=('plan_digest',))
    source_answers={x['question_ref']:x for x in load(a.core2_answer_contracts)['answers']}
    for p in c2['pages']:
        if p['question_ref'] not in source_answers: raise ValueError('CORE2A_SOURCE_ANSWER_CONTRACT_MISSING:'+p['question_ref'])
        validate_answer_contract(source_answers[p['question_ref']])
    buckets,_=bucket_maps(c1a); pages={p['question_ref']:p for p in c2['pages']}; profiles=load_scaffold_profiles(a.scaffold_profiles); candidates=[]
    if a.candidate_set:
        cand_doc=load(a.candidate_set); schema=load(PK/'Core2A'/'contracts'/'math-core2a-candidate-set.schema.json'); jsonschema.validate(cand_doc,schema); candidates=[x for x in cand_doc['items'] if purpose in x['eligible_purposes']]
    if purpose in {'STARTER','PRACTICE','COMPETITION'} and not candidates: raise ValueError('CORE2A_PURPOSE_CANDIDATES_REQUIRED:'+purpose)
    for c in candidates: validate_candidate(c,purpose,buckets)
    check_candidate_coverage(purpose,buckets,candidates)
    sections=[]; specs=[]; selected_count=0; scaffolds={}
    for bid,b in buckets.items():
        sc=build_scaffold_plan(purpose,profiles,bid); scaffolds[bid]=sc; selected=source_selection(purpose,b,pages); ids=[p['question_ref'] for p in selected]; selected_count+=len(ids)
        recall=derived_revision_prompts(b) if purpose=='REVISION' else []
        if purpose=='STARTER': recall=[f"Start here: {b['bucket_invariant']['text']}"]+[f"Say this in your own words before solving: {x['text']}" for x in (b.get('learning_atoms') or [])[:2]]
        refs=[x['candidate_id'] for x in candidates if bid in x['bucket_refs']]
        sections.append({'bucket_ref':bid,'title':b['title'],'invariant':b['bucket_invariant']['text'],'scaffold_plan':sc,'selected_source_question_refs':ids,'recall_prompts':recall,'generated_candidate_refs':refs})
        for p in selected: specs.append(source_question_spec(p,bid,sc,source_answers[p['question_ref']]))
    for c in candidates: specs.append(build_candidate_spec(c,scaffolds[c['bucket_refs'][0]]))
    if purpose=='PRACTICE' and selected_count!=len(c2['pages']): raise ValueError('CORE2A_PRACTICE_DROPPED_SOURCE_ITEM')
    bp={'stage':'CORE2A','purpose':purpose,'source_bundle_ref':bundle['bundle_id'],'sections':sections,'question_specs':specs,'audit_requirements':['PURPOSE_EXPLICIT','SOURCE_CORE2_FIDELITY','ANSWER_CONTRACT_PASS','HINT_DISCLOSURE_PASS','INLINE_PROVENANCE','TAUGHT_SCOPE_ONLY','PURPOSE_DIFFERENTIATION_PASS']}; bp['blueprint_id']=build_blueprint_id(bp)
    (out/'core2a_product_blueprint.json').write_text(json.dumps(bp,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); audit={'kit_id':'MATH-PRODUCTION-KIT-CORE2A-v1','status':'PASS','purpose':purpose,'bucket_count':len(buckets),'selected_source_question_count':selected_count,'generated_candidate_count':len(candidates),'blueprint_ref':bp['blueprint_id'],'same_as_core2':False}; (out/'core2a_kit_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8'); print(json.dumps(audit,indent=2))
if __name__=='__main__': main()
