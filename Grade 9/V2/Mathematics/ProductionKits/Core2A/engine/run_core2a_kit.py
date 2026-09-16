#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, json, re, sys
from pathlib import Path
import jsonschema

HERE=Path(__file__).resolve(); MATH=HERE.parents[3]; PK=MATH/'ProductionKits'; COMMON=PK/'common'/'engine'; MB_ENGINE=MATH/'MathBlueprint'/'engine'
sys.path.insert(0,str(COMMON)); sys.path.insert(0,str(MB_ENGINE))
from production_primitives import route_task, validate_source_bundle, validate_bound_object, load_scaffold_profiles, build_scaffold_plan, validate_answer_contract, validate_provenance, build_blueprint_id, canonical, digest
from validate_self_teaching_generation_spec import validate_generation_spec
from validate_canonical_domain_registry import validate_registry
from producer_governance import core2a_receipt
from emit_stage_governance import write_receipt
from engineering_product_custody import load_custody, stamp_receipt, custody_summary

REQUIRED_ROLES={'CORE1A_BUCKET_PLAN','CORE2_PLAN'}
DEMAND_RANK={'EASY':1,'MEDIUM':2,'HARD':3}
SOURCE_BADGE_DEMAND={'EASY':'M0_DIRECT','MEDIUM':'M1_CONTROLLED_VARIATION','HARD':'M3_INVERSE_TARGET'}
STRUCTURAL_SLOTS={'HIDDEN_INFORMATION','REVERSED_TARGET','REPRESENTATION_SHIFT','PARAMETER_CONSTRAINT'}
DEMAND_LEVELS=[
    'M0_DIRECT','M1_CONTROLLED_VARIATION','M2_REPRESENTATION_TRANSFER','M3_INVERSE_TARGET',
    'M4_HIDDEN_STRUCTURE','M5_METHOD_DISCRIMINATION','M6_FAMILY_DISCRIMINATION',
    'M7_MULTI_STEP_SYNTHESIS','M8_MIXED_COMPETITIVE',
]
SLOT_DEMAND={
    'GUIDED_DIRECT':'M0_DIRECT',
    'NEAR_TRANSFER':'M1_CONTROLLED_VARIATION',
    'REPRESENTATION_VARIATION':'M2_REPRESENTATION_TRANSFER',
    'REPRESENTATION_SHIFT':'M2_REPRESENTATION_TRANSFER',
    'REVERSED_TARGET':'M3_INVERSE_TARGET',
    'HIDDEN_INFORMATION':'M4_HIDDEN_STRUCTURE',
    'PARAMETER_CONSTRAINT':'M4_HIDDEN_STRUCTURE',
    'MIXED_SYNTHESIS':'M7_MULTI_STEP_SYNTHESIS',
}

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def norm(t): return re.sub(r'\s+',' ',str(t).strip().lower())

def load_knowledge_support_profiles(path):
    data=load(path); out={}
    for row in data.get('profiles') or []:
        pid=row.get('profile_id')
        if not pid or pid in out: raise ValueError('CORE2A_KNOWLEDGE_SUPPORT_PROFILE_INVALID:'+str(pid))
        out[pid]=row
    required={'FOUNDATION_GUIDED','STANDARD_GUIDED','REDUCED_SUPPORT','ADVANCED_APPLIED'}
    if set(out)!=required: raise ValueError('CORE2A_KNOWLEDGE_SUPPORT_PROFILE_COVERAGE_DRIFT')
    return out

def apply_knowledge_support_profile(scaffold,profile_id,profiles):
    if profile_id not in profiles: raise ValueError('CORE2A_KNOWLEDGE_SUPPORT_PROFILE_MISSING:'+str(profile_id))
    out=copy.deepcopy(scaffold); overrides=copy.deepcopy(profiles[profile_id]['settings'])
    out['settings'].update(overrides)
    out['knowledge_support_profile']=profile_id
    out['scaffold_plan_id']='MATH-SCF-'+digest({'base':scaffold,'knowledge_support_profile':profile_id,'overrides':overrides})[:16]
    return out

def demand_index(level):
    if level not in DEMAND_LEVELS: raise ValueError('CORE2A_DEMAND_LEVEL_INVALID:'+str(level))
    return DEMAND_LEVELS.index(level)

def candidate_demand_level(item):
    slot=item.get('slot')
    if slot not in SLOT_DEMAND: raise ValueError('CORE2A_CANDIDATE_SLOT_DEMAND_UNMAPPED:'+str(slot))
    return SLOT_DEMAND[slot]

def source_demand_level(page):
    explicit=page.get('demand_level')
    if explicit:
        if explicit not in DEMAND_LEVELS: raise ValueError('CORE2A_SOURCE_DEMAND_LEVEL_INVALID:'+str(explicit))
        return explicit
    badge=page.get('guide_demand_badge',{}).get('label','EASY')
    if badge not in SOURCE_BADGE_DEMAND: raise ValueError('CORE2A_SOURCE_GUIDE_BADGE_UNMAPPED:'+str(badge))
    return SOURCE_BADGE_DEMAND[badge]

def candidate_within_ceiling(item,ceiling):
    return demand_index(candidate_demand_level(item)) <= demand_index(ceiling)

def bucket_maps(plan):
    by={}; qmap={}
    for b in plan['buckets']:
        bid=b['bucket_id']
        if bid in by: raise ValueError('CORE2A_BUCKET_ID_DUPLICATE:'+bid)
        by[bid]=b
        for q in b.get('core2_question_refs') or []:
            qmap.setdefault(q,[]).append(bid)
    return by,qmap

def representative_page(pages): return sorted(pages,key=lambda p:(-DEMAND_RANK.get(p.get('guide_demand_badge',{}).get('label','EASY'),0),p['source_order']))[0]
def source_selection(purpose,bucket,pages_by_id):
    pages=sorted([pages_by_id[q] for q in bucket.get('core2_question_refs') or [] if q in pages_by_id],key=lambda p:p['source_order'])
    if not pages:return []
    if purpose=='PRACTICE':return pages
    if purpose in {'REVISION','COMPETITION'}:return [representative_page(pages)]
    return [pages[0]]

def unique_selected_source_ids(selected_by_bucket,pages_by_id):
    ids={qid for refs in selected_by_bucket.values() for qid in refs}
    return sorted(ids,key=lambda q:(pages_by_id[q]['source_order'],q))

def source_question_spec(page,bucket_refs,scaffold,ans,required_capability_refs):
    h=page['hint_ladder']; reasoning=[str(x.get('mathematical_transition','')).strip() for x in page.get('reasoning_route',{}).get('steps',[]) if str(x.get('mathematical_transition','')).strip()]; working=[str(x) for x in page['solution_route'].get('steps') or []]; checks=[x if isinstance(x,str) else canonical(x) for x in page['solution_route'].get('verification_checks') or []]
    prov={'question_origin':'SOURCE_CORE2','display_inline':True,'learner_label':'Where this question came from','citations':[{'citation_kind':'CORE2_SOURCE','label':f"Core (2) {page['question_ref']}",'locator':page['question_ref'],'use':'SOURCE_TEXT','text_relation':'EXACT_SOURCE','url':None}],'official_past_question_claim':False,'verified_official_source_ref':page['source_ref']}; validate_provenance(prov)
    return {'question_id':page['question_ref'],'question_class':'SOURCE_CORE2','source_question_no':page['question_ref'],'bucket_refs':list(bucket_refs),'required_capability_refs':list(required_capability_refs),'demand_level':source_demand_level(page),'prompt':page['source_stem'],'source_order':page['source_order'],'scaffold_plan_ref':scaffold['scaffold_plan_id'],'provenance':prov,'answer_contract':ans,'learner_support':{'TRY IT FIRST':True,'SMALL CLUE':h['H1']['text'],'BIGGER CLUE':h['H2']['text'],'HOW DO I START?':h['H3']['text'],'THINK IT THROUGH':reasoning,'FULL WORKING':working,'QUICK CHECK':checks}}

def validate_source_question_scope(page,bucket_refs,buckets):
    taught=set()
    for bid in bucket_refs: taught.update(buckets[bid]['member_capability_refs'])
    required=set(page.get('capability_refs') or [])
    extra=sorted(required-taught)
    if extra: raise ValueError('CORE2A_SOURCE_UNTAUGHT_MATH_REQUIRED:'+page['question_ref']+':'+','.join(extra))

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
    parents=list(item['novelty_check'].get('compared_to_refs') or [])
    return {'question_id':item['candidate_id'],'question_class':'GENERATED_CHALLENGE','bucket_refs':item['bucket_refs'],'required_capability_refs':list(item['required_capability_refs']),'slot':item['slot'],'demand_level':candidate_demand_level(item),'prompt':item['prompt'],'scaffold_plan_ref':scaffold['scaffold_plan_id'],'provenance':item['provenance'],'answer_contract':item['answer_contract'],'parent_question_refs':parents,'source_relation':'FRESH_ORIGINAL','learner_source_label':'Generated original practice','learner_support':{'TRY IT FIRST':True,'SMALL CLUE':item['staged_help']['small_clue'],'BIGGER CLUE':item['staged_help']['bigger_clue'],'HOW DO I START?':item['staged_help']['how_do_i_start'],'THINK IT THROUGH':item['think_it_through'],'FULL WORKING':item['full_working'],'QUICK CHECK':item['quick_check']},'novelty_check':item['novelty_check']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--intent',required=True); ap.add_argument('--generation-spec',required=True); ap.add_argument('--source-bundle',required=True); ap.add_argument('--core1a-bucket-plan',required=True); ap.add_argument('--core2-plan',required=True); ap.add_argument('--core2-answer-contracts',required=True); ap.add_argument('--candidate-set'); ap.add_argument('--domain-registry'); ap.add_argument('--engineering-admission'); ap.add_argument('--scaffold-profiles',default=str(PK/'common'/'profiles'/'scaffold-profiles.json')); ap.add_argument('--knowledge-support-profiles',default=str(PK/'common'/'profiles'/'knowledge-support-profiles.json')); ap.add_argument('--out-dir',required=True); a=ap.parse_args()
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); intent=load(a.intent); routed=route_task(intent); (out/'routing_result.json').write_text(json.dumps(routed,indent=2)+'\n',encoding='utf-8')
    if routed['status']!='ROUTED': print(routed['question']); raise SystemExit(2)
    if routed['stage']!='CORE2A': raise ValueError('CORE2A_KIT_WRONG_STAGE')
    purpose=routed['purpose']

    gen=load(a.generation_spec); validate_generation_spec(gen); cal=gen['core2_calibration']
    if cal['purpose']!=purpose: raise ValueError('CORE2A_PURPOSE_CALIBRATION_MISMATCH:'+str(cal['purpose'])+'!='+str(purpose))
    calibration_mode='KNOWLEDGE_PERCENT' if cal['learner_knowledge_percent'] is not None else 'OWNER_WAIVER'
    c2a_ceiling=cal['resolved_core2a_max_demand_level']; support_profile=cal['resolved_core2a_support_profile']
    registry=load(a.domain_registry) if a.domain_registry else None
    if registry is not None: validate_registry(registry)
    engineering_custody=load_custody(a.engineering_admission,registry)

    bundle=load(a.source_bundle); validate_source_bundle(bundle,REQUIRED_ROLES); c1a=load(a.core1a_bucket_plan); c2=load(a.core2_plan)
    validate_bound_object(bundle,'CORE1A_BUCKET_PLAN',c1a,ref_fields=('bucket_plan_id',),digest_fields=('plan_digest',)); validate_bound_object(bundle,'CORE2_PLAN',c2,ref_fields=('plan_id',),digest_fields=('plan_digest',))
    source_answers={x['question_ref']:x for x in load(a.core2_answer_contracts)['answers']}
    for p in c2['pages']:
        if p['question_ref'] not in source_answers: raise ValueError('CORE2A_SOURCE_ANSWER_CONTRACT_MISSING:'+p['question_ref'])
        validate_answer_contract(source_answers[p['question_ref']])
    buckets,qmap=bucket_maps(c1a); pages={p['question_ref']:p for p in c2['pages']}; profiles=load_scaffold_profiles(a.scaffold_profiles); knowledge_profiles=load_knowledge_support_profiles(a.knowledge_support_profiles); candidates=[]; dropped_by_ceiling=[]
    for qid,refs in qmap.items():
        if qid in pages: validate_source_question_scope(pages[qid],refs,buckets)
    if a.candidate_set:
        cand_doc=load(a.candidate_set); schema=load(PK/'Core2A'/'contracts'/'math-core2a-candidate-set.schema.json'); jsonschema.validate(cand_doc,schema)
        eligible=[x for x in cand_doc['items'] if purpose in x['eligible_purposes']]
        for item in eligible:
            if candidate_within_ceiling(item,c2a_ceiling): candidates.append(item)
            else: dropped_by_ceiling.append({'candidate_id':item['candidate_id'],'demand_level':candidate_demand_level(item)})
    if purpose in {'STARTER','PRACTICE','COMPETITION'} and not candidates: raise ValueError('CORE2A_CALIBRATION_REMOVED_REQUIRED_CANDIDATES:'+purpose)
    for c in candidates:
        if not candidate_within_ceiling(c,c2a_ceiling): raise ValueError('CORE2A_CANDIDATE_EXCEEDS_KNOWLEDGE_CEILING:'+c['candidate_id'])
        validate_candidate(c,purpose,buckets)
    check_candidate_coverage(purpose,buckets,candidates)

    sections=[]; specs=[]; scaffolds={}; selected_by_bucket={}
    for bid,b in buckets.items():
        base_sc=build_scaffold_plan(purpose,profiles,bid); sc=apply_knowledge_support_profile(base_sc,support_profile,knowledge_profiles); scaffolds[bid]=sc
        selected=source_selection(purpose,b,pages); ids=[p['question_ref'] for p in selected]; selected_by_bucket[bid]=ids
        recall=derived_revision_prompts(b) if purpose=='REVISION' else []
        if purpose=='STARTER': recall=[f"Start here: {b['bucket_invariant']['text']}"]+[f"Say this in your own words before solving: {x['text']}" for x in (b.get('learning_atoms') or [])[:2]]
        refs=[x['candidate_id'] for x in candidates if bid in x['bucket_refs']]
        sections.append({'bucket_ref':bid,'title':b['title'],'invariant':b['bucket_invariant']['text'],'scaffold_plan':sc,'selected_source_question_refs':ids,'recall_prompts':recall,'generated_candidate_refs':refs})

    selected_ids=unique_selected_source_ids(selected_by_bucket,pages); selected_count=len(selected_ids)
    for qid in selected_ids:
        bucket_refs=qmap.get(qid) or []
        if not bucket_refs: raise ValueError('CORE2A_SELECTED_SOURCE_WITHOUT_BUCKET:'+qid)
        page=pages[qid]; required=page.get('capability_refs') or sorted({cap for bid in bucket_refs for cap in buckets[bid]['member_capability_refs']})
        specs.append(source_question_spec(page,bucket_refs,scaffolds[bucket_refs[0]],source_answers[qid],required))
    for c in candidates: specs.append(build_candidate_spec(c,scaffolds[c['bucket_refs'][0]]))
    if purpose=='PRACTICE' and selected_count!=len(c2['pages']): raise ValueError('CORE2A_PRACTICE_DROPPED_SOURCE_ITEM')

    calibration={'mode':calibration_mode,'knowledge_percent_source_ref':cal['knowledge_percent_source_ref'],'knowledge_calibration_policy_ref':cal['knowledge_calibration_policy_ref'],'owner_waiver_ref':cal['owner_waiver']['owner_ref'] if cal['owner_waiver'] else None,'core2a_support_profile':support_profile,'core2a_max_demand_level':c2a_ceiling,'core2b_max_demand_level':cal['resolved_core2b_max_demand_level']}
    bp={'stage':'CORE2A','purpose':purpose,'source_bundle_ref':bundle['bundle_id'],'generation_calibration':calibration,'sections':sections,'question_specs':specs,'audit_requirements':['PURPOSE_EXPLICIT','KNOWLEDGE_OR_OWNER_CALIBRATION_PASS','CORE2A_DEMAND_CEILING_PASS','SOURCE_CORE2_FIDELITY','ANSWER_CONTRACT_PASS','HINT_DISCLOSURE_PASS','INLINE_PROVENANCE','TAUGHT_SCOPE_ONLY','PURPOSE_DIFFERENTIATION_PASS','MULTI_BUCKET_SOURCE_MEMBERSHIP_SAFE']}; bp['blueprint_id']=build_blueprint_id(bp)
    (out/'core2a_product_blueprint.json').write_text(json.dumps(bp,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

    receipt_pages=[]
    for p in c2['pages']:
        row=copy.deepcopy(p); row['answer_contract_ref']='ANS-'+p['question_ref']+'-'+digest(source_answers[p['question_ref']])[:12]; receipt_pages.append(row)
    receipt=core2a_receipt(bp,gen,registry=registry,all_source_pages=receipt_pages)
    receipt=stamp_receipt(receipt,engineering_custody)
    write_receipt(receipt,out/'core2a_governance_receipt.json')

    audit={'kit_id':'MATH-PRODUCTION-KIT-CORE2A-v5','status':'PASS','purpose':purpose,'calibration_mode':calibration_mode,'core2a_support_profile':support_profile,'core2a_max_demand_level':c2a_ceiling,'core2b_max_demand_level':cal['resolved_core2b_max_demand_level'],'bucket_count':len(buckets),'selected_source_question_count':selected_count,'multi_bucket_source_question_count':sum(1 for refs in qmap.values() if len(refs)>1),'generated_candidate_count':len(candidates),'generated_candidates_dropped_by_ceiling':dropped_by_ceiling,'blueprint_ref':bp['blueprint_id'],'governance_receipt_ref':receipt['receipt_id'],'governance_release_state':receipt['release_state'],'engineering_custody':custody_summary(engineering_custody),'same_as_core2':False}; (out/'core2a_kit_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8'); print(json.dumps(audit,indent=2))

if __name__=='__main__': main()
