#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path

D=Path(__file__).resolve().parents[1]
DEMAND_KEYS=["representation_translation","chemical_entity_tracking","formula_charge_parsing","condition_exception_handling","conservation_reasoning","reaction_process_reasoning","classification_discrimination","experimental_inference","structure_recognition","hidden_condition_load","reasoning_chain_length","concept_combination","quantitative_execution_load","verification_demand","time_pressure"]

def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def uniq(xs):
    out=[]
    for x in xs:
        if x not in out: out.append(x)
    return out

def validate_source_bodies(corpus,bodies,classifications):
    if bodies.get('subject')!='CHEMISTRY' or bodies.get('corpus_ref')!=corpus['corpus_id']: fail('SOURCE_LINK_MISSING_OR_WRONG','body authority')
    candidates={x['candidate_id']:x for x in corpus['candidates']}; classes={x['candidate_id']:x for x in classifications['classifications']}; records={x['candidate_id']:x for x in bodies['records']}
    if len(candidates)!=corpus['candidate_count_declared'] or len(classes)!=len(candidates): fail('SOURCE_LINK_MISSING_OR_WRONG','denominator/classification mismatch')
    eligible={k for k,v in classes.items() if v['scope_status']=='ELIGIBLE_IN_SCOPE'}
    if set(records)!=eligible: fail('SOURCE_LINK_MISSING_OR_WRONG','source bodies must cover exactly eligible candidates')
    for cid,r in records.items():
        if r['candidate_source_digest']!=candidates[cid]['source_digest']: fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid+':candidate digest')
        if r['body_digest']!=digest(r,'body_digest'): fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid+':body digest')
        if not r['source_link']: fail('SOURCE_LINK_MISSING_OR_WRONG',cid)
        if not r['stem'] or len(r['options'])<2: fail('SOURCE_MC_OPTIONS_MISSING',cid)
        if r['figure_required'] and not r['figure_semantic']: fail('SOURCE_STRUCTURE_OR_FIGURE_LOST',cid)
    return candidates,classes,records,eligible

def family_for(classification,families):
    aliases=families['question_family_aliases']; qrefs=classification.get('problem_family_refs',[])
    if not qrefs or qrefs[0] not in aliases: fail('GENERIC_WORKSPACE_IGNORES_CHEMISTRY_SHAPE',classification['candidate_id']+':family')
    pf=aliases[qrefs[0]]; fam=next((x for x in families['families'] if x['family_id']==pf),None)
    if not fam: fail('GENERIC_WORKSPACE_IGNORES_CHEMISTRY_SHAPE',classification['candidate_id']+':family authority')
    return qrefs[0],fam

def guide_badge(fam,classification,badge_policy):
    dims={k:0 for k in DEMAND_KEYS}; dims.update(fam.get('demand_defaults',{})); route=fam['reasoning_route_template']
    dims['reasoning_chain_length']=max(dims['reasoning_chain_length'],1 if len(route)<=3 else 2 if len(route)<=5 else 3)
    dims['concept_combination']=max(dims['concept_combination'],min(3,max(0,len(classification.get('canonical_concept_refs',[]))-1)))
    if fam.get('condition_or_exception_requirements'):
        dims['condition_exception_handling']=max(dims['condition_exception_handling'],2); dims['hidden_condition_load']=max(dims['hidden_condition_load'],1)
    if fam.get('conservation_requirements'): dims['conservation_reasoning']=max(dims['conservation_reasoning'],2)
    if len(fam.get('representation_levels',[]))>1: dims['representation_translation']=max(dims['representation_translation'],2)
    score=sum(dims.values()); badge=next(x['badge'] for x in badge_policy['thresholds'] if score<=x['max_score'])
    return badge,dims

def concept_binding(qfamily,classification,concept_registry):
    m=concept_registry['mappings'].get(qfamily)
    if not m: fail('PRIMARY_SUPPORTS_NOT_DISTINGUISHED',classification['candidate_id']+':no concept map')
    if m['primary_concept_ref'] not in classification['canonical_concept_refs'] or m['primary_capability_ref'] not in classification['canonical_capability_refs']: fail('PRIMARY_SUPPORTS_NOT_DISTINGUISHED',classification['candidate_id']+':primary authority')
    if m['primary_concept_ref'] in m['supporting_concept_refs'] or m['primary_capability_ref'] in m['supporting_capability_refs']: fail('PRIMARY_SUPPORTS_NOT_DISTINGUISHED',classification['candidate_id']+':primary duplicated')
    return m

def core1_links(binding,classification,core1_plan,profile):
    lessons={x['capability_ref']:x for x in core1_plan['lessons']}; caps=uniq([binding['primary_capability_ref']]+binding['supporting_capability_refs'])
    out=[]
    for cap in caps:
        if cap not in lessons: continue
        title=profile['core1_titles'].get(cap)
        if not title: fail('OPAQUE_CORE1_LINK_ONLY',cap)
        out.append({'lesson_id':lessons[cap]['lesson_id'],'learner_title':title,'capability_ref':cap})
    if not out: fail('OPAQUE_CORE1_LINK_ONLY',classification['candidate_id'])
    return out

def visual_specs(cid,qfamily,binding,body,profile,primitive_registry):
    by={x['primitive_id']:x for x in primitive_registry['primitives']}; pid=profile['visual_primitive_by_family'][qfamily]
    if pid not in by or binding['primary_capability_ref'] not in by[pid]['capability_refs']: fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid+':visual authority')
    p=by[pid]; out=[{'visual_id':f'VIS-{cid}-{pid}','visual_kind':'TEACHING_PRIMITIVE','primitive_id':pid,'instructional_job':p['instructional_job'],'source_bound':True,'source_semantic_data':{'candidate_id':cid,'stem':body['stem'],'condition_text':body['condition_text'],'figure_semantic':body['figure_semantic']}}]
    if body['figure_required']:
        out.insert(0,{'visual_id':f'VIS-{cid}-SOURCE-FIGURE','visual_kind':'SOURCE_FIGURE','primitive_id':None,'instructional_job':'Preserve the source-required figure exactly enough for the original transfer item to remain attemptable.','source_bound':True,'source_semantic_data':copy.deepcopy(body['figure_semantic'])})
    return out

def make_page(classification,body,core1_plan,families,badge_policy,transfer_badges,concept_registry,profile,primitive_registry,notation):
    cid=classification['candidate_id']; qfamily,fam=family_for(classification,families); binding=concept_binding(qfamily,classification,concept_registry)
    if qfamily not in profile['workspace_by_family'] or qfamily not in profile['hints_by_family'] or qfamily not in profile['solution_steps_by_family']: fail('GENERIC_WORKSPACE_IGNORES_CHEMISTRY_SHAPE',cid)
    hints=profile['hints_by_family'][qfamily]; badge,dims=guide_badge(fam,classification,badge_policy); option_text=next(x['text'] for x in body['options'] if x['label']==body['answer_key'])
    condition_check='Preserve and verify the recorded condition: '+body['condition_text']+'.' if body['condition_text'] else 'No additional condition or exception is recorded for this source item.'
    route=list(fam['reasoning_route_template']); verification=list(profile['verification_by_family'][qfamily])
    page={'question_ref':cid,'source_ref':body['candidate_source_digest'],'source_year':body['source_year'],'source_session':body['source_session'],'source_shift':body['source_shift'],'scope_status':'ELIGIBLE_IN_SCOPE','source_qc_status':body['source_qc_status'],'source_stem':body['stem'],'source_options':copy.deepcopy(body['options']),'source_subparts':copy.deepcopy(body['subparts']),'source_figure_required':body['figure_required'],'source_figure_semantic':copy.deepcopy(body['figure_semantic']),'source_condition_text':body['condition_text'],'source_states':copy.deepcopy(body['states']),'source_units':copy.deepcopy(body['units']),'primary_concept_ref':binding['primary_concept_ref'],'primary_capability_ref':binding['primary_capability_ref'],'supporting_concept_refs':copy.deepcopy(binding['supporting_concept_refs']),'supporting_capability_refs':copy.deepcopy(binding['supporting_capability_refs']),'problem_family_ref':fam['family_id'],'demand_vector_ref':f"CHEM-C-I-DEMAND-{cid}",'guide_demand_badge':{'label':badge,'policy_ref':badge_policy['policy_id'],'semantic_class':'GUIDE_ASSIGNED_REASONING_DEMAND','psychometric_claim':False,'source_difficulty':None},'transfer_badge':transfer_badges['transfer_badges'][0],'source_badges':{'source':'SYNTHETIC_EXTERNAL_CORPUS','year':str(body['source_year']),'session':body['source_session'],'shift':body['source_shift']},'core1_lesson_refs':core1_links(binding,classification,core1_plan,profile),'workspace_spec':{'workspace_type':qfamily,'fields':copy.deepcopy(profile['workspace_by_family'][qfamily])},'hint_ladder':{'h0_attempt_first':profile['h0_text'],'support_revealed_initially':False,'h1_notice':hints['H1_NOTICE'],'h2_rule_model_representation':hints['H2_RULE_MODEL_REPRESENTATION'],'h3_start':hints['H3_START']},'reasoning_route':route,'reasoning_route_ref':f"CHEM-C-D-{fam['family_id']}-{cid}",'solution_route':{'reasoning_steps':copy.deepcopy(profile['solution_steps_by_family'][qfamily]),'verification_steps':verification,'final_answer':body['answer_key'],'chemical_language_response':option_text,'condition_exception_check':condition_check},'verification_route':verification,'visual_specs':visual_specs(cid,qfamily,binding,body,profile,primitive_registry),'source_link':body['source_link'],'source_fidelity':{'candidate_source_digest':body['candidate_source_digest'],'source_body_digest':body['body_digest'],'options_preserved':True,'figure_preserved':True,'condition_preserved':True,'notation_contract_ref':notation['contract_id']},'page_digest':''}
    page['page_digest']=digest(page,'page_digest'); return page,dims

def core1_unspoiled(core1_plan,eligible):
    for l in core1_plan['lessons']:
        w=l.get('worked_example') or {}
        if set(w.get('external_candidate_refs',[])) & eligible: return False
    for x in core1_plan['appendices']['appendix_a']['items']:
        if set(x.get('external_candidate_refs',[])) & eligible: return False
    return True

def build_plan(corpus,classifications,bodies,core1_plan,study_model,families,badge_policy,transfer_badges,concept_registry,profile,primitive_registry,notation,plan_id='CHEM-C-I-CORE2-PLAN-v1'):
    candidates,classes,records,eligible=validate_source_bodies(corpus,bodies,classifications)
    if core1_plan['study_model_digest']!=study_model['study_model_digest']: fail('OPAQUE_CORE1_LINK_ONLY','Core1/study authority drift')
    if transfer_badges.get('psychometric_claim_allowed') is not False: fail('GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC','policy')
    if not core1_unspoiled(core1_plan,eligible): fail('ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE')
    pages=[]; demand={}
    for cid in sorted(eligible,key=lambda x:candidates[x]['source_order']):
        p,d=make_page(classes[cid],records[cid],core1_plan,families,badge_policy,transfer_badges,concept_registry,profile,primitive_registry,notation); pages.append(p); demand[p['demand_vector_ref']]=d
    excluded=[cid for cid in candidates if cid not in eligible]
    out={'plan_id':plan_id,'schema_version':'1.0.0','subject':'CHEMISTRY','corpus_ref':corpus['corpus_id'],'corpus_digest':corpus['corpus_digest'],'classification_ref':classifications['classification_id'],'core1_plan_ref':core1_plan['plan_id'],'core1_plan_digest':core1_plan['plan_digest'],'study_model_ref':study_model['study_model_id'],'study_model_digest':study_model['study_model_digest'],'guide_badge_policy_ref':badge_policy['policy_id'],'transfer_badge_policy_ref':transfer_badges['policy_id'],'concept_segregation_ref':concept_registry['registry_id'],'notation_contract_ref':notation['contract_id'],'pages':pages,'excluded_candidate_refs':excluded,'summary':{'source_candidate_denominator':len(candidates),'eligible_candidate_count':len(eligible),'placed_page_count':len(pages),'excluded_or_unresolved_count':len(excluded),'unique_primary_placement':True,'attempt_first':True,'external_transfer_unspoiled':True,'psychometric_claims':False},'plan_digest':''}
    out['plan_digest']=digest(out,'plan_digest'); validate_plan(out,corpus,classifications,bodies,core1_plan,study_model,families,badge_policy,transfer_badges,concept_registry,profile,primitive_registry,notation); return out

def validate_plan(plan,corpus,classifications,bodies,core1_plan,study_model,families,badge_policy,transfer_badges,concept_registry,profile,primitive_registry,notation):
    candidates,classes,records,eligible=validate_source_bodies(corpus,bodies,classifications)
    if plan['plan_digest']!=digest(plan,'plan_digest'): fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT','plan digest')
    if plan['corpus_digest']!=corpus['corpus_digest'] or plan['core1_plan_digest']!=core1_plan['plan_digest'] or plan['study_model_digest']!=study_model['study_model_digest']: fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT','authority digest')
    if not core1_unspoiled(core1_plan,eligible): fail('ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE')
    pages=plan['pages']; refs=[p['question_ref'] for p in pages]
    if len(refs)!=len(set(refs)) or set(refs)!=eligible: fail('MULTIPLE_PRIMARY_OWNERS')
    if set(plan['excluded_candidate_refs'])!=set(candidates)-eligible: fail('MULTIPLE_PRIMARY_OWNERS','denominator placement')
    fam_by={x['family_id']:x for x in families['families']}; prim_by={x['primitive_id']:x for x in primitive_registry['primitives']}
    for p in pages:
        cid=p['question_ref']; body=records[cid]; cl=classes[cid]; qfamily,fam=family_for(cl,families); binding=concept_binding(qfamily,cl,concept_registry)
        if p['page_digest']!=digest(p,'page_digest'): fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid+':page digest')
        if p['scope_status']!='ELIGIBLE_IN_SCOPE': fail('MULTIPLE_PRIMARY_OWNERS',cid+':scope')
        if p['source_ref']!=body['candidate_source_digest'] or p['source_link']!=body['source_link'] or not p['source_link']: fail('SOURCE_LINK_MISSING_OR_WRONG',cid)
        if p['source_stem']!=body['stem'] or p['source_subparts']!=body['subparts'] or p['source_condition_text']!=body['condition_text'] or p['source_states']!=body['states'] or p['source_units']!=body['units']: fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid)
        if p['source_options']!=body['options']: fail('SOURCE_MC_OPTIONS_MISSING',cid)
        if p['source_figure_required']!=body['figure_required'] or p['source_figure_semantic']!=body['figure_semantic']: fail('SOURCE_STRUCTURE_OR_FIGURE_LOST',cid)
        if body['figure_required']:
            figs=[v for v in p['visual_specs'] if v['visual_kind']=='SOURCE_FIGURE']
            if len(figs)!=1 or figs[0]['source_semantic_data']!=body['figure_semantic']: fail('SOURCE_STRUCTURE_OR_FIGURE_LOST',cid)
        if p['primary_concept_ref']!=binding['primary_concept_ref'] or p['primary_capability_ref']!=binding['primary_capability_ref'] or set(p['supporting_concept_refs'])!=set(binding['supporting_concept_refs']) or set(p['supporting_capability_refs'])!=set(binding['supporting_capability_refs']) or p['primary_concept_ref'] in p['supporting_concept_refs'] or p['primary_capability_ref'] in p['supporting_capability_refs']: fail('PRIMARY_SUPPORTS_NOT_DISTINGUISHED',cid)
        expected_links=core1_links(binding,cl,core1_plan,profile)
        if p['core1_lesson_refs']!=expected_links or any(not x['learner_title'] or x['learner_title']==x['lesson_id'] for x in p['core1_lesson_refs']): fail('OPAQUE_CORE1_LINK_ONLY',cid)
        if p['workspace_spec']!={'workspace_type':qfamily,'fields':profile['workspace_by_family'][qfamily]}: fail('GENERIC_WORKSPACE_IGNORES_CHEMISTRY_SHAPE',cid)
        h=p['hint_ladder']; texts=[h['h1_notice'],h['h2_rule_model_representation'],h['h3_start']]
        if not h['h0_attempt_first'] or h['support_revealed_initially'] is not False: fail('H1_DISCLOSES_H3',cid+':attempt first')
        if len(set(texts))<3 or h['h3_start'].strip().lower() in h['h1_notice'].strip().lower(): fail('H1_DISCLOSES_H3',cid)
        sol=p['solution_route']; soltexts=sol['reasoning_steps']+[sol['final_answer'],sol['chemical_language_response']]
        if any(t.strip()==s.strip() for t in texts for s in soltexts): fail('HINT_EQUALS_SOLUTION',cid)
        if p['reasoning_route']==texts or p['reasoning_route']==[h['h1_notice'],h['h2_rule_model_representation'],h['h3_start']]: fail('REASONING_ROUTE_EQUALS_HINT_COPY',cid)
        if p['reasoning_route']!=fam['reasoning_route_template'] or p['problem_family_ref']!=fam['family_id']: fail('REASONING_ROUTE_EQUALS_HINT_COPY',cid+':route authority')
        badge=p['guide_demand_badge']; expected_badge,_=guide_badge(fam,cl,badge_policy)
        if badge['label']!=expected_badge or badge['policy_ref']!=badge_policy['policy_id'] or badge['semantic_class']!='GUIDE_ASSIGNED_REASONING_DEMAND' or badge['psychometric_claim'] is not False: fail('GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC',cid)
        if badge['label'] in {'DEEP','VERY_DEEP'} and len(p['reasoning_route'])<4: fail('HARD_BADGE_WITHOUT_DEEPER_REASONING_STRUCTURE',cid)
        if p['transfer_badge'] not in transfer_badges['transfer_badges']: fail('GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC',cid+':transfer badge')
        if len(sol['reasoning_steps'])<2 or not sol['verification_steps'] or not sol['final_answer'] or not sol['chemical_language_response']: fail('SOLUTION_IS_ANSWER_ONLY',cid)
        if sol['verification_steps']!=p['verification_route'] or p['verification_route']!=profile['verification_by_family'][qfamily]: fail('SOLUTION_IS_ANSWER_ONLY',cid+':verification')
        if body['condition_text'] and body['condition_text'] not in sol['condition_exception_check']: fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid+':condition solution')
        teaching=[v for v in p['visual_specs'] if v['visual_kind']=='TEACHING_PRIMITIVE']
        if not teaching or teaching[0]['primitive_id']!=profile['visual_primitive_by_family'][qfamily] or teaching[0]['primitive_id'] not in prim_by: fail('SOURCE_STRUCTURE_OR_FIGURE_LOST',cid+':teaching representation')
        sf=p['source_fidelity']
        if sf['candidate_source_digest']!=body['candidate_source_digest'] or sf['source_body_digest']!=body['body_digest'] or not all([sf['options_preserved'],sf['figure_preserved'],sf['condition_preserved']]) or sf['notation_contract_ref']!=notation['contract_id']: fail('FORMULA_CHARGE_STATE_CONDITION_DRIFT',cid+':fidelity')
    s=plan['summary']
    if s['source_candidate_denominator']!=len(candidates) or s['eligible_candidate_count']!=len(eligible) or s['placed_page_count']!=len(pages) or s['excluded_or_unresolved_count']!=len(candidates)-len(eligible): fail('MULTIPLE_PRIMARY_OWNERS','summary')
    if s['psychometric_claims'] is not False or transfer_badges.get('psychometric_claim_allowed') is not False: fail('GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC','summary')
    return True

def main():
    ap=argparse.ArgumentParser()
    for x in ['corpus','classifications','source-bodies','core1-plan','study-model','family-registry','guide-badge-policy','transfer-badge-policy','concept-registry','authoring-profile','primitive-registry','notation-contract','out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); out=build_plan(load(a.corpus),load(a.classifications),load(a.source_bodies),load(a.core1_plan),load(a.study_model),load(a.family_registry),load(a.guide_badge_policy),load(a.transfer_badge_policy),load(a.concept_registry),load(a.authoring_profile),load(a.primitive_registry),load(a.notation_contract)); Path(a.out).write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
