#!/usr/bin/env python3
import argparse, copy, hashlib, importlib.util, json
from collections import Counter
from pathlib import Path

D=Path(__file__).resolve().parents[1]

def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def uniq(xs): return sorted(set(xs))

def load_pck_registry(path=None):
    p=Path(path) if path else D/'registry'/'chemistry_promoted_pck.py'
    spec=importlib.util.spec_from_file_location('chemistry_promoted_pck',p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod.build_registry()

def validate_pck_registry(reg):
    x=copy.deepcopy(reg); got=x.pop('registry_digest',None)
    if got!=hashlib.sha256(canonical(x).encode()).hexdigest(): fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY','registry digest')
    seen=set()
    for a in reg['assets']:
        if a['asset_id'] in seen: fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY','duplicate '+a['asset_id'])
        seen.add(a['asset_id']); y=copy.deepcopy(a); d=y.pop('asset_digest',None)
        if d!=hashlib.sha256(canonical(y).encode()).hexdigest(): fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',a['asset_id']+':digest')
        auth=a.get('promotion_authority') or {}
        if auth.get('promotion_state')!='PROMOTED_PILOT' or auth.get('authority_class')!='REPOSITORY_PROGRAMME_PILOT_AUTHORITY' or auth.get('final_product_release_blocked') is not True: fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',a['asset_id'])
        if auth.get('subject_expert_release_state')!='NOT_GRANTED' or auth.get('pedagogy_expert_release_state')!='NOT_GRANTED': fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',a['asset_id']+':release boundary')
        if a.get('raw_mature_reference_used') is not False: fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',a['asset_id']+':raw reference')
    return True

def family_ref(record):
    pf=[x for x in record['problem_family_refs'] if x.startswith('PF-')]
    refs=pf or record['problem_family_refs']
    if not refs: fail('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',record['capability_ref'])
    return sorted(refs)[0]

def select_pck(record,reg,profile):
    cap=record['capability_ref']; primary_family=profile['primary_pck_family_by_capability'].get(cap)
    generic=[a for a in reg['assets'] if cap in a['capability_refs'] and not a['topic_scope_refs']]
    primary=next((a for a in generic if a['family']==primary_family),None)
    if not primary: fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',cap+':no primary promoted asset')
    support=[a for a in generic if a['family'] in profile['support_pck_families'] and a['asset_id']!=primary['asset_id']]
    return primary,support

def verification(record,primary): return list(record['verification_requirements'] or primary['verification_method'])
def attempt(cap,stage,prompt,record,problem_profile,lesson_id):
    return {'attempt_id':f'{lesson_id}-{stage}','support_stage':stage,'prompt':prompt+' '+problem_profile['stage_modifiers'][stage],'representation_spec':uniq(record['representation_level_obligations']+record['representation_requirement_obligations'])}
def problem(cap,record,primary,problem_profile,lesson_id):
    fam=family_ref(record); prompt=problem_profile['prompt_templates'][cap]
    return {'instance_id':f'{lesson_id}-WORKED-NEW','source_class':'NEW_AUTHORED_CORE1','problem_family_ref':fam,'primary_capability_ref':cap,'prompt':prompt+' Work on a newly authored source-authorized instance rather than an original external transfer item.','representation_spec':uniq(record['representation_level_obligations']+record['representation_requirement_obligations']),'surface_variation':'representation_reframing_and_cue_change','external_candidate_refs':[],'reasoning_steps':list(problem_profile['solution_reasoning_templates'][cap]),'verification_steps':verification(record,primary)}

def build_lesson(record,reg,profile,problem_profile):
    cap=record['capability_ref']; primary,support=select_pck(record,reg,profile); mode=profile['lesson_mode_by_treatment'][record['treatment']]; lesson_id='CORE1-'+cap
    pck_refs=[primary['asset_id']]+[a['asset_id'] for a in support]; first=next((a for a in support if a['family']=='FIRST_MOVE_DECISION_SUPPORT'),primary); contrast=next((a for a in support if a['family']=='MISCONCEPTION_MINIMAL_CONTRAST'),primary)
    base=problem_profile['prompt_templates'][cap]; ver=verification(record,primary)
    trace={'source_obligation_refs':list(record['source_obligation_refs']),'assessment_question_refs':list(record['assessment_question_refs']),'external_candidate_refs':list(record['external_candidate_refs']),'problem_family_refs':list(record['problem_family_refs'])}
    if mode=='FULL_LEARNING':
        rep=list(primary['particle_symbolic_representation_path'])+[f'OBLIGATION_LEVEL:{x}' for x in record['representation_level_obligations']]+[f'OBLIGATION_REP:{x}' for x in record['representation_requirement_obligations']]
        mis={'wrong_model':primary['common_wrong_model'],'why_plausible':'The shortcut can look sufficient because it uses a familiar surface cue before the decisive chemical evidence is checked.','minimal_contrast':contrast['minimal_contrast'],'repair_steps':list(contrast['repair_route']),'retry_prompt':base+' Retry after applying the repaired model to a close but newly authored instance.'}
        return {'lesson_id':lesson_id,'capability_ref':cap,'treatment':record['treatment'],'lesson_mode':mode,'pck_asset_refs':uniq(pck_refs),'content_roles':list(profile['content_roles_by_mode'][mode]),'scope_trace':trace,'activation':'Identify the target and state the first chemically meaningful move: '+first['reconstruction_route'][0],'familiar_macro_anchor':primary['familiar_macro_anchor'],'representation_path':rep,'ordinary_language_explanation':primary['ordinary_language_bridge'],'rule_model_condition':primary['rule_model_condition_cue'],'reconstruction_steps':list(primary['reconstruction_route']),'worked_example':problem(cap,record,primary,problem_profile,lesson_id),'concept_helper':first['ordinary_language_bridge'],'misconception_repair':mis,'guided_attempt':attempt(cap,'GUIDED',base,record,problem_profile,lesson_id),'faded_attempt':attempt(cap,'FADED',base,record,problem_profile,lesson_id),'independent_attempt':attempt(cap,'INDEPENDENT',base,record,problem_profile,lesson_id),'verification_steps':ver,'transfer_bridge':'Transfer family: '+primary['transfer_family']+'. Original external transfer remains reserved for Core2.','condition_exception_obligations':list(record['condition_exception_obligations'])}
    if mode=='CONCISE_VERIFY_ONLY':
        return {'lesson_id':lesson_id,'capability_ref':cap,'treatment':record['treatment'],'lesson_mode':mode,'pck_asset_refs':uniq(pck_refs),'content_roles':list(profile['content_roles_by_mode'][mode]),'scope_trace':trace,'activation':'Brief activation: '+first['reconstruction_route'][0],'familiar_macro_anchor':'','representation_path':[f'OBLIGATION_LEVEL:{x}' for x in record['representation_level_obligations']],'ordinary_language_explanation':'','rule_model_condition':'','reconstruction_steps':[],'worked_example':None,'concept_helper':'','misconception_repair':None,'guided_attempt':None,'faded_attempt':None,'independent_attempt':attempt(cap,'INDEPENDENT',base,record,problem_profile,lesson_id),'verification_steps':ver,'transfer_bridge':'Continue without reteaching after the independent verification check.','condition_exception_obligations':list(record['condition_exception_obligations'])}
    return {'lesson_id':lesson_id,'capability_ref':cap,'treatment':record['treatment'],'lesson_mode':'PROBE','pck_asset_refs':uniq(pck_refs),'content_roles':list(profile['content_roles_by_mode']['PROBE']),'scope_trace':trace,'activation':'Collect decisive evidence before choosing repair or study depth.','familiar_macro_anchor':'','representation_path':[f'PROBE_REP:{x}' for x in record['representation_level_obligations']],'ordinary_language_explanation':'','rule_model_condition':'','reconstruction_steps':[],'worked_example':None,'concept_helper':'','misconception_repair':None,'guided_attempt':None,'faded_attempt':None,'independent_attempt':attempt(cap,'PROBE',base,record,problem_profile,lesson_id),'verification_steps':ver,'transfer_bridge':'No transfer escalation until the probe is interpreted.','condition_exception_obligations':list(record['condition_exception_obligations'])}

def build_appendices(lessons,records,reg,problem_profile,completeness):
    rec_by={r['capability_ref']:r for r in records}; asset_by={a['asset_id']:a for a in reg['assets']}; items=[]; solutions=[]
    for l in lessons:
        r=rec_by[l['capability_ref']]; primary=asset_by[l['pck_asset_refs'][0]]; fam=family_ref(r); stages=['GUIDED','FADED','INDEPENDENT'] if l['lesson_mode']=='FULL_LEARNING' else ['INDEPENDENT'] if l['lesson_mode']=='CONCISE_VERIFY_ONLY' else ['PROBE']
        for i,stage in enumerate(stages,1):
            iid=f"A-{l['capability_ref']}-{stage}"; prompt=problem_profile['prompt_templates'][l['capability_ref']]+' '+problem_profile['stage_modifiers'][stage]; sol=f'B-SOL-{iid}'
            items.append({'item_id':iid,'source_class':'NEW_AUTHORED_CORE1','problem_family_ref':fam,'primary_capability_ref':l['capability_ref'],'supports_capability_refs':[],'support_stage':stage,'scored':stage!='PROBE','prompt':prompt,'representation_spec':uniq(r['representation_level_obligations']+r['representation_requirement_obligations']),'external_candidate_refs':[],'solution_ref':sol})
            solutions.append({'solution_id':sol,'item_ref':iid,'primary_capability_ref':l['capability_ref'],'reasoning_steps':list(problem_profile['solution_reasoning_templates'][l['capability_ref']]),'verification_steps':verification(r,primary),'final_response':'A complete response states the relevant chemical evidence or rule, executes the recorded reasoning route, and gives the conclusion only after the required checks pass.','condition_exception_note':'Preserve and apply: '+', '.join(r['condition_exception_obligations']) if r['condition_exception_obligations'] else 'No additional condition/exception is required by this capability record.'})
    hand=[]
    for l in lessons:
        r=rec_by[l['capability_ref']]; primary=asset_by[l['pck_asset_refs'][0]]; first=next((asset_by[x] for x in l['pck_asset_refs'] if asset_by[x]['family']=='FIRST_MOVE_DECISION_SUPPORT'),primary); ver=verification(r,primary)
        hand.append({'capability_ref':l['capability_ref'],'first_move':first['reconstruction_route'][0],'rule_or_decision_cue':primary['rule_model_condition_cue'],'verification_cue':ver[0]})
    return {'appendix_a':{'title':'Appendix A — Core Practice','present':True,'items':items},'appendix_b':{'title':'Appendix B — Core Solutions','present':True,'solutions':solutions},'appendix_c':{'title':'Appendix C — Printable Handout','present':True,'answer_free':True,'supported_capability_refs':uniq([l['capability_ref'] for l in lessons]),'introduced_capability_refs':[],'reference_entries':hand,'print_constraints':list(completeness['appendix_c_print_constraints'])}}

def build_plan(study_model,study_scope,pck_registry,profile,completeness,problem_profile,plan_id='CHEM-C-G-CORE1-PLAN-v1'):
    validate_pck_registry(pck_registry)
    if study_model['subject']!='CHEMISTRY' or study_scope['subject']!='CHEMISTRY': fail('CORE1_IS_ONLY_A_REPAIR_MEMO','subject')
    if study_model['study_scope_digest']!=study_scope['study_scope_digest']: fail('CORE1_IS_ONLY_A_REPAIR_MEMO','scope drift')
    lessons=[build_lesson(r,pck_registry,profile,problem_profile) for r in study_model['capability_records']]
    appendices=build_appendices(lessons,study_model['capability_records'],pck_registry,problem_profile,completeness)
    out={'plan_id':plan_id,'schema_version':'1.0.0','subject':'CHEMISTRY','study_model_ref':study_model['study_model_id'],'study_model_digest':study_model['study_model_digest'],'study_scope_ref':study_scope['study_scope_id'],'study_scope_digest':study_scope['study_scope_digest'],'pck_registry_ref':pck_registry['registry_id'],'authoring_profile_ref':profile['profile_id'],'lessons':lessons,'appendices':appendices,'external_transfer_unspoiled':True,'scope_complete':True,'release_authority_state':'PILOT_ONLY_HUMAN_EXPERT_RELEASE_NOT_GRANTED','plan_digest':''}
    out['plan_digest']=digest(out,'plan_digest'); validate_plan(out,study_model,study_scope,pck_registry,profile,completeness,problem_profile); return out

def validate_plan(plan,study_model,study_scope,pck_registry,profile,completeness,problem_profile):
    validate_pck_registry(pck_registry)
    if plan['plan_digest']!=digest(plan,'plan_digest'): fail('CORE1_IS_ONLY_A_REPAIR_MEMO','plan digest')
    required=set(study_scope['required_capability_refs']); lessons={l['capability_ref']:l for l in plan['lessons']}
    if len(lessons)!=len(plan['lessons']) or set(lessons)!=required: fail('CORE1_IS_ONLY_A_REPAIR_MEMO')
    recs={r['capability_ref']:r for r in study_model['capability_records']}; assets={a['asset_id']:a for a in pck_registry['assets']}
    for cap,l in lessons.items():
        r=recs[cap]
        if not l['pck_asset_refs'] or any(x not in assets for x in l['pck_asset_refs']): fail('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',cap)
        if l['condition_exception_obligations']!=r['condition_exception_obligations']: fail('CONDITION_EXCEPTION_DROPPED',cap)
        if l['lesson_mode']=='FULL_LEARNING':
            if not l['representation_path'] or (('CROSS_REPRESENTATION_TRANSLATION' in r['future_evidence_obligations'] or len(r['representation_level_obligations'])>1) and not all('OBLIGATION_LEVEL:'+x in l['representation_path'] for x in r['representation_level_obligations'])): fail('FULL_LEARNING_TREATMENT_WITHOUT_REPRESENTATION_TRANSLATION',cap)
            if not l['ordinary_language_explanation'] or len(l['reconstruction_steps'])<2 or l['worked_example'] is None: fail('NAKED_RULE_COUNTS_AS_CONCEPT_TEACHING',cap)
            m=l['misconception_repair']
            if not m or not m['repair_steps'] or not m['retry_prompt']: fail('MISCONCEPTION_WARNING_WITHOUT_REPAIR',cap)
            w=l['worked_example']
            if w['source_class']!='NEW_AUTHORED_CORE1' or w['external_candidate_refs']: fail('CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE',cap)
            if not w['problem_family_ref']: fail('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',cap)
            if not w['verification_steps'] or not l['verification_steps']: fail('CHEMICAL_CHECK_REDUCED_TO_ANSWER_ONLY',cap)
        elif l['lesson_mode']=='CONCISE_VERIFY_ONLY':
            if l['content_roles']!=profile['content_roles_by_mode']['CONCISE_VERIFY_ONLY'] or l['worked_example'] is not None or l['guided_attempt'] is not None or l['faded_attempt'] is not None or l['misconception_repair'] is not None: fail('READY_CONTENT_PADDED_INTO_FULL_RETEACH',cap)
        elif l['lesson_mode']=='PROBE':
            if l['worked_example'] is not None or l['guided_attempt'] is not None or l['faded_attempt'] is not None: fail('READY_CONTENT_PADDED_INTO_FULL_RETEACH',cap+':probe overteach')
    aps=plan.get('appendices',{})
    if 'appendix_a' not in aps or not aps['appendix_a'].get('present'): fail('APPENDIX_A_MISSING')
    if 'appendix_b' not in aps or not aps['appendix_b'].get('present'): fail('APPENDIX_B_MISSING')
    if 'appendix_c' not in aps or not aps['appendix_c'].get('present'): fail('APPENDIX_C_MISSING')
    aitems=aps['appendix_a']['items']; bsol=aps['appendix_b']['solutions']; hand=aps['appendix_c']
    if {x['primary_capability_ref'] for x in aitems}!=required: fail('CORE1_IS_ONLY_A_REPAIR_MEMO','Appendix A coverage')
    for x in aitems:
        if x['source_class']!='NEW_AUTHORED_CORE1' or x['external_candidate_refs']: fail('APPENDIX_A_USES_EXACT_EXAMSIDE_TRANSFER',x['item_id'])
        if not x['problem_family_ref']: fail('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',x['item_id'])
    if {x['item_ref'] for x in bsol}!={x['item_id'] for x in aitems} or len(bsol)!=len(aitems): fail('APPENDIX_B_INCOMPLETE')
    for x in bsol:
        if not x['reasoning_steps'] or not x['verification_steps']: fail('CHEMICAL_CHECK_REDUCED_TO_ANSWER_ONLY',x['solution_id'])
    if hand.get('answer_free') is not True: fail('HANDOUT_CONTAINS_ANSWERS')
    if hand.get('introduced_capability_refs') or set(hand.get('supported_capability_refs',[]))!=required or {x['capability_ref'] for x in hand.get('reference_entries',[])}!=required: fail('HANDOUT_INTRODUCES_NEW_CHEMISTRY')
    return True

def main():
    ap=argparse.ArgumentParser();
    for x in ['study-model','study-scope','instructional-profile','completeness-policy','problem-profile','out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); reg=load_pck_registry(); out=build_plan(load(a.study_model),load(a.study_scope),reg,load(a.instructional_profile),load(a.completeness_policy),load(a.problem_profile)); Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
