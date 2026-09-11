#!/usr/bin/env python3
import argparse, copy, hashlib, json
from collections import Counter
from pathlib import Path

D=Path(__file__).resolve().parents[1]
GENERIC_INSTANCE_PRIMITIVES={'MINIMAL_CHEMISTRY_CONTRAST','FORMULA_EQUATION_CHECK_STRIP'}
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def uniq(xs): return sorted(set(xs))
def primitive_supports_capability(p,cap): return cap in p['capability_refs'] or p['primitive_id'] in GENERIC_INSTANCE_PRIMITIVES

def validate_registry(reg):
    if reg.get('subject')!='CHEMISTRY': fail('VISUAL_WITHOUT_CAPABILITY_BINDING','registry subject')
    ps=reg['primitives']; by={p['primitive_id']:p for p in ps}
    if len(by)!=len(ps) or not set(reg['required_primitive_ids'])<=set(by): fail('VISUAL_WITHOUT_INSTRUCTIONAL_JOB','primitive coverage')
    for p in ps:
        if p.get('decorative') is not False: fail('DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS',p['primitive_id'])
        if not p.get('instructional_job') or not p.get('attention_target') or not p.get('learner_action'): fail('VISUAL_WITHOUT_INSTRUCTIONAL_JOB',p['primitive_id'])
        if not p.get('capability_refs'): fail('VISUAL_WITHOUT_CAPABILITY_BINDING',p['primitive_id'])
    if not {'COMPOSITION_FROM_SOURCE_ONLY','NO_LITERAL_PARTICLE_SIZE_CLAIM','NO_UNDECLARED_BONDING'}<=set(by['PARTICLE_MODEL_VIEW']['renderer_constraints']): fail('PARTICLE_VIEW_IMPLIES_WRONG_COMPOSITION')
    if 'SITE_IDS_STABLE' not in by['STRUCTURE_SITE_ANNOTATION']['renderer_constraints']: fail('STRUCTURE_SITE_IDENTITY_LOST')
    if 'CONDITION_VISIBLE' not in by['CONDITION_EXCEPTION_GATE']['renderer_constraints']: fail('CONDITION_EXCEPTION_REQUIRED_BUT_NOT_VISIBLE')
    if 'NO_INVENTED_OBSERVATION' not in by['APPARATUS_METHOD_FLOW']['renderer_constraints']: fail('APPARATUS_VIEW_INVENTS_OBSERVATION')
    if not {'TWO_CASES_REQUIRED','ONE_DECISIVE_FEATURE'}<=set(by['MINIMAL_CHEMISTRY_CONTRAST']['renderer_constraints']): fail('CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED')
    return by

def validate_notation(n):
    if n.get('ascii_fallback_policy')!='FORBID_AMBIGUOUS_FLAT_ASCII': fail('ASCII_FALLBACK_MAKES_CHARGE_AMBIGUOUS')
    if not {'H₂O₂','Fe³⁺','Cr₂O₇²⁻','e⁻'}<=set(n.get('required_examples',[])): fail('FORMULA_OR_CHARGE_DRIFTS_FROM_SEMANTIC_DATA','notation examples')
    if not {'Fe3+','Cr2O72-','e-'}<=set(n.get('ambiguous_ascii_examples_forbidden',[])): fail('ASCII_FALLBACK_MAKES_CHARGE_AMBIGUOUS','forbidden examples')
    return True

def choose_family(record):
    pf=[x for x in record['problem_family_refs'] if x.startswith('PF-')]
    return sorted(pf or record['problem_family_refs'])[0] if record['problem_family_refs'] else None

def primitive_ids_for(lesson,record,profile):
    ids=list(profile['primary_primitives_by_capability'].get(record['capability_ref'],[]))
    if not ids: fail('VISUAL_WITHOUT_CAPABILITY_BINDING',record['capability_ref']+':no page-intent primitive')
    if lesson['lesson_mode']=='FULL_LEARNING':
        if lesson.get('misconception_repair'): ids.append(profile['conditional_primitives']['MISCONCEPTION_REPAIR'])
        if record['verification_requirements']: ids.append(profile['conditional_primitives']['CHEMICAL_VERIFICATION'])
        if record['condition_exception_obligations']: ids.append('CONDITION_EXCEPTION_GATE')
    elif lesson['lesson_mode']=='CONCISE_VERIFY_ONLY': ids=ids[:profile['ready_mode_max_primary_primitives']]
    else: ids=ids[:profile['probe_mode_max_primary_primitives']]
    out=[]
    for x in ids:
        if x not in out: out.append(x)
    return out

def make_spec(i,primitive,lesson,record,notation):
    entities=list(record['chemical_entity_species_obligations']); conditions=list(record['condition_exception_obligations']); roles=[]
    if primitive['primitive_id']=='SPECIES_ROLE_MAP': roles=['REACTANT_SPECIES','CHANGING_SPECIES','SPECTATOR_IF_PRESENT','PRODUCT_SPECIES']
    semantic={'source_obligation_refs':list(record['source_obligation_refs']),'assessment_question_refs':list(record['assessment_question_refs']),'representation_levels':list(record['representation_level_obligations']),'representation_requirements':list(record['representation_requirement_obligations']),'chemical_entities':entities,'condition_exception_context':conditions,'verification_requirements':list(record['verification_requirements'])}
    contrast=lesson['lesson_id'] if primitive['primitive_id']=='MINIMAL_CHEMISTRY_CONTRAST' else None
    accessibility=primitive['accessibility_pattern']+(' Chemical entities: '+', '.join(entities)+'.' if entities else '')+(' Conditions/exceptions: '+', '.join(conditions)+'.' if conditions else '')
    return {'representation_id':f"REP-{lesson['capability_ref']}-{i:02d}-{primitive['primitive_id']}",'primitive_id':primitive['primitive_id'],'capability_ref':lesson['capability_ref'],'problem_family_ref':choose_family(record),'instructional_job':primitive['instructional_job'],'attention_target':primitive['attention_target'],'translation_obligation':primitive['translation_obligation'],'chemical_entities':entities,'species_roles':roles,'representation_level_from':primitive['representation_level_from'],'representation_level_to':primitive['representation_level_to'],'condition_exception_context':conditions,'source_semantic_data':semantic,'learner_action_expected':primitive['learner_action'],'misconception_or_contrast_ref':contrast,'accessibility_text':accessibility,'renderer_constraints':uniq(primitive['renderer_constraints']+['NOTATION_CONTRACT:'+notation['contract_id']]),'notation_tokens':entities,'decorative':False}

def build_bundle(core1_plan,study_model,registry,profile,notation,bundle_id='CHEM-C-H-REPRESENTATIONS-v1'):
    by=validate_registry(registry); validate_notation(notation)
    if core1_plan['study_model_digest']!=study_model['study_model_digest']: fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING','study model drift')
    recs={r['capability_ref']:r for r in study_model['capability_records']}; reps=[]
    for lesson in core1_plan['lessons']:
        r=recs[lesson['capability_ref']]
        for i,pid in enumerate(primitive_ids_for(lesson,r,profile),1):
            if pid not in by: fail('VISUAL_WITHOUT_INSTRUCTIONAL_JOB',pid)
            p=by[pid]
            if not primitive_supports_capability(p,lesson['capability_ref']): fail('VISUAL_WITHOUT_CAPABILITY_BINDING',pid+':'+lesson['capability_ref'])
            if p['topic_scope_refs'] and not any(x in lesson['pck_asset_refs'] for x in []):
                # Topic-scoped primitives are selected only through an explicit page-intent mapping for a topic capability.
                if lesson['capability_ref'] not in {'CAP-TRACK-OXIDATION-STATE'} and pid not in {'SELF_OTHER_AGENT_FRAME','SPLIT_CONVERGE_TOPOLOGY'}: fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',pid)
            reps.append(make_spec(i,p,lesson,r,notation))
    counts=Counter(x['primitive_id'] for x in reps)
    out={'bundle_id':bundle_id,'schema_version':'1.0.0','subject':'CHEMISTRY','core1_plan_ref':core1_plan['plan_id'],'core1_plan_digest':core1_plan['plan_digest'],'study_model_ref':study_model['study_model_id'],'study_model_digest':study_model['study_model_digest'],'primitive_registry_ref':registry['registry_id'],'page_intent_profile_ref':profile['profile_id'],'notation_contract_ref':notation['contract_id'],'representations':reps,'summary':{'representation_count':len(reps),'capability_count':len(set(x['capability_ref'] for x in reps)),'primitive_counts':dict(sorted(counts.items())),'renderer_invention_allowed':False},'bundle_digest':''}
    out['bundle_digest']=digest(out,'bundle_digest'); validate_bundle(out,core1_plan,study_model,registry,profile,notation); return out

def validate_bundle(bundle,core1_plan,study_model,registry,profile,notation):
    by=validate_registry(registry); validate_notation(notation)
    if bundle['bundle_digest']!=digest(bundle,'bundle_digest'): fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING','bundle digest')
    if bundle['core1_plan_digest']!=core1_plan['plan_digest'] or bundle['study_model_digest']!=study_model['study_model_digest']: fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING','authority drift')
    recs={r['capability_ref']:r for r in study_model['capability_records']}; lessons={l['capability_ref']:l for l in core1_plan['lessons']}; grouped={c:[] for c in recs}
    for s in bundle['representations']:
        if s.get('decorative') is not False: fail('DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS',s.get('representation_id','unknown'))
        if not s.get('instructional_job') or not s.get('attention_target') or not s.get('learner_action_expected'): fail('VISUAL_WITHOUT_INSTRUCTIONAL_JOB',s.get('representation_id','unknown'))
        cap=s.get('capability_ref')
        if cap not in recs: fail('VISUAL_WITHOUT_CAPABILITY_BINDING',s.get('representation_id','unknown'))
        grouped[cap].append(s); p=by.get(s['primitive_id'])
        if not p or not primitive_supports_capability(p,cap): fail('VISUAL_WITHOUT_CAPABILITY_BINDING',s['primitive_id'])
        if s['instructional_job']!=p['instructional_job'] or s['attention_target']!=p['attention_target']: fail('VISUAL_WITHOUT_INSTRUCTIONAL_JOB',s['representation_id'])
        r=recs[cap]
        if set(s['chemical_entities'])!=set(r['chemical_entity_species_obligations']) or set(s['source_semantic_data']['chemical_entities'])!=set(r['chemical_entity_species_obligations']): fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',s['representation_id'])
        if set(s['condition_exception_context'])!=set(r['condition_exception_obligations']) or set(s['source_semantic_data']['condition_exception_context'])!=set(r['condition_exception_obligations']): fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',s['representation_id']+':condition')
        if set(s['notation_tokens'])!=set(r['chemical_entity_species_obligations']): fail('FORMULA_OR_CHARGE_DRIFTS_FROM_SEMANTIC_DATA',s['representation_id'])
        if set(s['source_semantic_data']['source_obligation_refs'])!=set(r['source_obligation_refs']) or set(s['source_semantic_data']['assessment_question_refs'])!=set(r['assessment_question_refs']): fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',s['representation_id']+':trace')
        if set(s['source_semantic_data']['representation_levels'])!=set(r['representation_level_obligations']) or set(s['source_semantic_data']['representation_requirements'])!=set(r['representation_requirement_obligations']): fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',s['representation_id']+':representation authority')
        if not set(p['renderer_constraints'])<=set(s['renderer_constraints']):
            if s['primitive_id'] in {'PARTICLE_MODEL_VIEW','MACRO_PARTICLE_SYMBOLIC_BRIDGE'}: fail('PARTICLE_VIEW_IMPLIES_WRONG_COMPOSITION',s['representation_id'])
            if s['primitive_id']=='APPARATUS_METHOD_FLOW': fail('APPARATUS_VIEW_INVENTS_OBSERVATION',s['representation_id'])
            if s['primitive_id']=='MINIMAL_CHEMISTRY_CONTRAST': fail('CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED',s['representation_id'])
            fail('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',s['representation_id']+':renderer constraints')
    for cap,r in recs.items():
        if not grouped.get(cap): fail('VISUAL_WITHOUT_CAPABILITY_BINDING',cap+':no representation')
        pids={x['primitive_id'] for x in grouped[cap]}; lesson=lessons[cap]
        if r['condition_exception_obligations'] and 'CONDITION_EXCEPTION_GATE' not in pids: fail('CONDITION_EXCEPTION_REQUIRED_BUT_NOT_VISIBLE',cap)
        if lesson['lesson_mode']=='FULL_LEARNING' and lesson.get('misconception_repair') and 'MINIMAL_CHEMISTRY_CONTRAST' not in pids: fail('CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED',cap)
        if cap=='CAP-TRANSLATE-PARTICLE-SYMBOL' and not ({'PARTICLE_MODEL_VIEW','MACRO_PARTICLE_SYMBOLIC_BRIDGE'}<=pids): fail('PARTICLE_VIEW_IMPLIES_WRONG_COMPOSITION',cap)
    return True

def main():
    ap=argparse.ArgumentParser()
    for x in ['core1-plan','study-model','primitive-registry','page-intent-profile','notation-contract','out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); out=build_bundle(load(a.core1_plan),load(a.study_model),load(a.primitive_registry),load(a.page_intent_profile),load(a.notation_contract)); Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
