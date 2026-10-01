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

REPRESENTATION_KEYS=('formulas','charges','coefficients','states','conditions','structures','figures','observations','units')

def _normalized_representation(rep):
    return {k:list(rep.get(k,[])) for k in REPRESENTATION_KEYS}

def _authority_indexes(source_set,question_set):
    source={}
    for u in (source_set or {}).get('units',[]):
        ref='CO-'+u['source_unit_id']
        source[ref]={
            'authority_kind':'SOURCE_OBLIGATION',
            'authority_ref':ref,
            'source_locator':u['source_provenance']['source_locator'],
            'authority_digest':u['source_provenance']['source_digest'],
            'content':u['statement'],
            'representation':_normalized_representation(u['representation']),
        }
    assessment={}
    for q in (question_set or {}).get('questions',[]):
        base={
            'authority_kind':'ASSESSMENT_QUESTION',
            'source_locator':q['source_provenance']['source_locator'],
            'authority_digest':q['source_provenance']['source_digest'],
            'representation':_normalized_representation(q['representation']),
        }
        assessment[q['question_id']]={**base,'authority_ref':q['question_id'],'content':q['stem']}
        for p in q.get('subparts',[]):
            ref=f"{q['question_id']}.{p['part_id']}"
            assessment[ref]={**base,'authority_ref':ref,'content':p['stem']}
    return source,assessment

def _bind_practice_authority(record,source_index,assessment_index):
    for ref in record['source_obligation_refs']:
        if ref in source_index: return copy.deepcopy(source_index[ref])
    for ref in sorted(record['assessment_question_refs'],key=lambda x:(0 if '.' in x else 1,x)):
        if ref in assessment_index: return copy.deepcopy(assessment_index[ref])
    fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',record['capability_ref'])

def _representation_evidence(rep):
    parts=[]
    for key in REPRESENTATION_KEYS:
        vals=rep.get(key,[])
        if vals: parts.append(key.replace('_',' ')+' = '+', '.join(str(x) for x in vals))
    return '; '.join(parts) if parts else 'no additional representation token is recorded'

def _practice_prompt(cap,authority,problem_profile,stage):
    evidence=_representation_evidence(authority['representation'])
    return (problem_profile['prompt_templates'][cap]+' '
            +'Source-authorized instance: '+authority['content']+' '
            +'Concrete evidence: '+evidence+'. '
            +'Use only this evidence; if the source does not authorize a named conclusion, state that boundary explicitly. '
            +problem_profile['stage_modifiers'][stage])

def _expected_response(authority,record):
    cap=record['capability_ref']; rep=authority['representation']
    formulas=list(rep.get('formulas',[])); charges=list(rep.get('charges',[]))
    conditions=list(rep.get('conditions',[])); observations=list(rep.get('observations',[])); figures=list(rep.get('figures',[]))
    if cap=='CAP-CHECK-ATOM-CONSERVATION' and '2H₂ + O₂ → 2H₂O' in formulas:
        answer='For 2H₂ + O₂ → 2H₂O, H is 4 atoms on each side and O is 2 atoms on each side, so atom conservation passes.'
    elif cap=='CAP-PARSE-ION-CHARGE':
        answer='In SO₄²⁻, the subscript 4 counts oxygen atoms while the superscript 2− is the overall ion charge. Do not turn the charge into a subscript or coefficient.'
    elif cap=='CAP-READ-FORMULA':
        answer='CaCl₂ contains Ca and Cl with a subscript 2 on Cl; SO₄²⁻ contains S and O with a subscript 4 on O and an overall 2− charge.'
    elif cap=='CAP-PRESERVE-REACTION-CONDITION' and conditions:
        answer='The recorded condition is '+', '.join(conditions)+'. It belongs with the reaction arrow/process and must remain present when A → B is read or rewritten.'
    elif cap=='CAP-TRACK-REACTING-SPECIES' and formulas:
        answer='Track Zn to Zn²⁺ and Cu²⁺ to Cu. The species identities and charge changes must be followed before any role label is assigned.'
    elif cap=='CAP-ATTACH-SPECIES-ROLE' and formulas:
        answer='The equation lets you track Zn → Zn²⁺ and Cu²⁺ → Cu, but this source instance does not name the requested role. A specific role label is therefore not authorized from the supplied source evidence alone.'
    elif cap=='CAP-TRANSLATE-PARTICLE-SYMBOL':
        answer='The authorized symbolic identity is H₂O. The source records a particle-water figure but no particle count here, so preserve H₂O and do not invent a count that is not supplied.'
    elif cap=='CAP-SEPARATE-OBSERVATION-INFERENCE' and observations:
        answer='Observation: '+observations[0]+'. The source does not identify the precipitate composition or mechanism here, so any further inference must remain explicitly bounded.'
    elif cap=='CAP-CLASSIFY-CHANGE-EVIDENCE':
        answer='The source distinguishes a state change from evidence for a new substance and records gas evolution/colour change as observations, but it does not supply one concrete event to classify. Do not invent a single process classification.'
    elif cap=='CAP-CHECK-RULE-EXCEPTION':
        answer='The explicit exception must be checked before the default rule is applied. Because the source does not state the exception content here, no more specific apply/withhold decision is authorized.'
    elif cap=='CAP-READ-APPARATUS-METHOD' and figures:
        answer='The source identifies a '+figures[0]+' figure, but it does not supply the target property or observation needed to justify a specific property-to-method conclusion. State that boundary rather than inventing one.'
    elif cap=='CAP-VERIFY-CHEMICAL-REPRESENTATION':
        answer='One authorized verification is to check that the same chemical species identity is preserved in the representation; then verify the stated result only after that check passes.'
    else:
        answer='The source evidence is insufficient for a more specific conclusion; preserve the recorded evidence and state the unresolved boundary.'
    return 'Source-bound expected response: '+answer

def attempt(cap,stage,record,problem_profile,lesson_id,authority):
    return {'attempt_id':f'{lesson_id}-{stage}','support_stage':stage,'prompt':_practice_prompt(cap,authority,problem_profile,stage),'representation_spec':uniq(record['representation_level_obligations']+record['representation_requirement_obligations']),'instance_authority':copy.deepcopy(authority),'instance_digest':digest(authority)}
def problem(cap,record,primary,problem_profile,lesson_id,authority):
    fam=family_ref(record)
    return {'instance_id':f'{lesson_id}-WORKED-NEW','source_class':'NEW_AUTHORED_CORE1','problem_family_ref':fam,'primary_capability_ref':cap,'prompt':_practice_prompt(cap,authority,problem_profile,'GUIDED'),'representation_spec':uniq(record['representation_level_obligations']+record['representation_requirement_obligations']),'surface_variation':'representation_reframing_and_cue_change','external_candidate_refs':[],'reasoning_steps':list(problem_profile['solution_reasoning_templates'][cap]),'verification_steps':verification(record,primary),'instance_authority':copy.deepcopy(authority),'instance_digest':digest(authority),'final_response':_expected_response(authority,record)}

def build_lesson(record,reg,profile,problem_profile,authority):
    cap=record['capability_ref']; primary,support=select_pck(record,reg,profile); mode=profile['lesson_mode_by_treatment'][record['treatment']]; lesson_id='CORE1-'+cap
    pck_refs=[primary['asset_id']]+[a['asset_id'] for a in support]; first=next((a for a in support if a['family']=='FIRST_MOVE_DECISION_SUPPORT'),primary); contrast=next((a for a in support if a['family']=='MISCONCEPTION_MINIMAL_CONTRAST'),primary)
    base=problem_profile['prompt_templates'][cap]; ver=verification(record,primary)
    trace={'source_obligation_refs':list(record['source_obligation_refs']),'assessment_question_refs':list(record['assessment_question_refs']),'external_candidate_refs':list(record['external_candidate_refs']),'problem_family_refs':list(record['problem_family_refs'])}
    if mode=='FULL_LEARNING':
        rep=list(primary['particle_symbolic_representation_path'])+[f'OBLIGATION_LEVEL:{x}' for x in record['representation_level_obligations']]+[f'OBLIGATION_REP:{x}' for x in record['representation_requirement_obligations']]
        mis={'wrong_model':primary['common_wrong_model'],'why_plausible':'The shortcut can look sufficient because it uses a familiar surface cue before the decisive chemical evidence is checked.','minimal_contrast':contrast['minimal_contrast'],'repair_steps':list(contrast['repair_route']),'retry_prompt':_practice_prompt(cap,authority,problem_profile,'FADED')+' Retry after applying the repaired model.'}
        return {'lesson_id':lesson_id,'capability_ref':cap,'treatment':record['treatment'],'lesson_mode':mode,'pck_asset_refs':uniq(pck_refs),'content_roles':list(profile['content_roles_by_mode'][mode]),'scope_trace':trace,'activation':'Identify the target and state the first chemically meaningful move: '+first['reconstruction_route'][0],'familiar_macro_anchor':primary['familiar_macro_anchor'],'representation_path':rep,'ordinary_language_explanation':primary['ordinary_language_bridge'],'rule_model_condition':primary['rule_model_condition_cue'],'reconstruction_steps':list(primary['reconstruction_route']),'worked_example':problem(cap,record,primary,problem_profile,lesson_id,authority),'concept_helper':first['ordinary_language_bridge'],'misconception_repair':mis,'guided_attempt':attempt(cap,'GUIDED',record,problem_profile,lesson_id,authority),'faded_attempt':attempt(cap,'FADED',record,problem_profile,lesson_id,authority),'independent_attempt':attempt(cap,'INDEPENDENT',record,problem_profile,lesson_id,authority),'verification_steps':ver,'transfer_bridge':'Transfer family: '+primary['transfer_family']+'. Original external transfer remains reserved for Core2.','condition_exception_obligations':list(record['condition_exception_obligations'])}
    if mode=='CONCISE_VERIFY_ONLY':
        return {'lesson_id':lesson_id,'capability_ref':cap,'treatment':record['treatment'],'lesson_mode':mode,'pck_asset_refs':uniq(pck_refs),'content_roles':list(profile['content_roles_by_mode'][mode]),'scope_trace':trace,'activation':'Brief activation: '+first['reconstruction_route'][0],'familiar_macro_anchor':'','representation_path':[f'OBLIGATION_LEVEL:{x}' for x in record['representation_level_obligations']],'ordinary_language_explanation':'','rule_model_condition':'','reconstruction_steps':[],'worked_example':None,'concept_helper':'','misconception_repair':None,'guided_attempt':None,'faded_attempt':None,'independent_attempt':attempt(cap,'INDEPENDENT',record,problem_profile,lesson_id,authority),'verification_steps':ver,'transfer_bridge':'Continue without reteaching after the independent verification check.','condition_exception_obligations':list(record['condition_exception_obligations'])}
    return {'lesson_id':lesson_id,'capability_ref':cap,'treatment':record['treatment'],'lesson_mode':'PROBE','pck_asset_refs':uniq(pck_refs),'content_roles':list(profile['content_roles_by_mode']['PROBE']),'scope_trace':trace,'activation':'Collect decisive evidence before choosing repair or study depth.','familiar_macro_anchor':'','representation_path':[f'PROBE_REP:{x}' for x in record['representation_level_obligations']],'ordinary_language_explanation':'','rule_model_condition':'','reconstruction_steps':[],'worked_example':None,'concept_helper':'','misconception_repair':None,'guided_attempt':None,'faded_attempt':None,'independent_attempt':attempt(cap,'PROBE',record,problem_profile,lesson_id,authority),'verification_steps':ver,'transfer_bridge':'No transfer escalation until the probe is interpreted.','condition_exception_obligations':list(record['condition_exception_obligations'])}

def build_appendices(lessons,records,reg,problem_profile,completeness,source_set,question_set):
    rec_by={r['capability_ref']:r for r in records}; asset_by={a['asset_id']:a for a in reg['assets']}; items=[]; solutions=[]
    source_index,assessment_index=_authority_indexes(source_set,question_set)
    for l in lessons:
        r=rec_by[l['capability_ref']]; primary=asset_by[l['pck_asset_refs'][0]]; fam=family_ref(r); stages=['GUIDED','FADED','INDEPENDENT'] if l['lesson_mode']=='FULL_LEARNING' else ['INDEPENDENT'] if l['lesson_mode']=='CONCISE_VERIFY_ONLY' else ['PROBE']
        authority=_bind_practice_authority(r,source_index,assessment_index); instance_digest=digest(authority)
        for i,stage in enumerate(stages,1):
            iid=f"A-{l['capability_ref']}-{stage}"; prompt=_practice_prompt(l['capability_ref'],authority,problem_profile,stage); sol=f'B-SOL-{iid}'
            items.append({'item_id':iid,'source_class':'NEW_AUTHORED_CORE1','problem_family_ref':fam,'primary_capability_ref':l['capability_ref'],'supports_capability_refs':[],'support_stage':stage,'scored':stage!='PROBE','prompt':prompt,'representation_spec':uniq(r['representation_level_obligations']+r['representation_requirement_obligations']),'external_candidate_refs':[],'instance_authority':copy.deepcopy(authority),'instance_digest':instance_digest,'solution_ref':sol})
            solutions.append({'solution_id':sol,'item_ref':iid,'primary_capability_ref':l['capability_ref'],'instance_digest':instance_digest,'reasoning_steps':list(problem_profile['solution_reasoning_templates'][l['capability_ref']]),'verification_steps':verification(r,primary),'final_response':_expected_response(authority,r),'condition_exception_note':'Preserve and apply: '+', '.join(r['condition_exception_obligations']) if r['condition_exception_obligations'] else 'No additional condition/exception is required by this capability record.'})
    hand=[]
    for l in lessons:
        r=rec_by[l['capability_ref']]; primary=asset_by[l['pck_asset_refs'][0]]; first=next((asset_by[x] for x in l['pck_asset_refs'] if asset_by[x]['family']=='FIRST_MOVE_DECISION_SUPPORT'),primary); ver=verification(r,primary)
        hand.append({'capability_ref':l['capability_ref'],'first_move':first['reconstruction_route'][0],'rule_or_decision_cue':primary['rule_model_condition_cue'],'verification_cue':ver[0]})
    return {'appendix_a':{'title':'Appendix A — Core Practice','present':True,'items':items},'appendix_b':{'title':'Appendix B — Core Solutions','present':True,'solutions':solutions},'appendix_c':{'title':'Appendix C — Printable Handout','present':True,'answer_free':True,'supported_capability_refs':uniq([l['capability_ref'] for l in lessons]),'introduced_capability_refs':[],'reference_entries':hand,'print_constraints':list(completeness['appendix_c_print_constraints'])}}

def build_plan(study_model,study_scope,pck_registry,profile,completeness,problem_profile,plan_id='CHEM-C-G-CORE1-PLAN-v1',source_set=None,question_set=None):
    validate_pck_registry(pck_registry)
    if study_model['subject']!='CHEMISTRY' or study_scope['subject']!='CHEMISTRY': fail('CORE1_IS_ONLY_A_REPAIR_MEMO','subject')
    if study_model['study_scope_digest']!=study_scope['study_scope_digest']: fail('CORE1_IS_ONLY_A_REPAIR_MEMO','scope drift')
    source_index,assessment_index=_authority_indexes(source_set,question_set)
    lesson_authority={r['capability_ref']:_bind_practice_authority(r,source_index,assessment_index) for r in study_model['capability_records']}
    lessons=[build_lesson(r,pck_registry,profile,problem_profile,lesson_authority[r['capability_ref']]) for r in study_model['capability_records']]
    appendices=build_appendices(lessons,study_model['capability_records'],pck_registry,problem_profile,completeness,source_set,question_set)
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
            if not w.get('instance_authority') or w.get('instance_digest')!=digest(w['instance_authority']): fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',cap+':worked example')
            if not w.get('final_response','').startswith('Source-bound expected response:'): fail('CORE1_SOLUTION_NOT_INSTANCE_BOUND',cap+':worked example')
            generic='Source-bound expected response: '+w['instance_authority']['content']+' Evidence to preserve:'
            if w['final_response'].startswith(generic): fail('CORE1_SOLUTION_NOT_INSTANCE_BOUND',cap+':worked example source restatement')
            for attempt_key in ['guided_attempt','faded_attempt','independent_attempt']:
                a=l.get(attempt_key)
                if a and (not a.get('instance_authority') or a.get('instance_digest')!=digest(a['instance_authority'])):
                    fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',cap+':'+attempt_key)
        elif l['lesson_mode']=='CONCISE_VERIFY_ONLY':
            if l['content_roles']!=profile['content_roles_by_mode']['CONCISE_VERIFY_ONLY'] or l['worked_example'] is not None or l['guided_attempt'] is not None or l['faded_attempt'] is not None or l['misconception_repair'] is not None: fail('READY_CONTENT_PADDED_INTO_FULL_RETEACH',cap)
            a=l.get('independent_attempt')
            if not a or not a.get('instance_authority') or a.get('instance_digest')!=digest(a['instance_authority']): fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',cap+':independent_attempt')
        elif l['lesson_mode']=='PROBE':
            if l['worked_example'] is not None or l['guided_attempt'] is not None or l['faded_attempt'] is not None: fail('READY_CONTENT_PADDED_INTO_FULL_RETEACH',cap+':probe overteach')
            a=l.get('independent_attempt')
            if not a or not a.get('instance_authority') or a.get('instance_digest')!=digest(a['instance_authority']): fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',cap+':probe')
    aps=plan.get('appendices',{})
    if 'appendix_a' not in aps or not aps['appendix_a'].get('present'): fail('APPENDIX_A_MISSING')
    if 'appendix_b' not in aps or not aps['appendix_b'].get('present'): fail('APPENDIX_B_MISSING')
    if 'appendix_c' not in aps or not aps['appendix_c'].get('present'): fail('APPENDIX_C_MISSING')
    aitems=aps['appendix_a']['items']; bsol=aps['appendix_b']['solutions']; hand=aps['appendix_c']
    if {x['primary_capability_ref'] for x in aitems}!=required: fail('CORE1_IS_ONLY_A_REPAIR_MEMO','Appendix A coverage')
    item_by={x['item_id']:x for x in aitems}
    for x in aitems:
        if x['source_class']!='NEW_AUTHORED_CORE1' or x['external_candidate_refs']: fail('APPENDIX_A_USES_EXACT_EXAMSIDE_TRANSFER',x['item_id'])
        if not x['problem_family_ref']: fail('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',x['item_id'])
        auth=x.get('instance_authority')
        if not auth or x.get('instance_digest')!=digest(auth): fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',x['item_id'])
        rec=recs[x['primary_capability_ref']]
        allowed=set(rec['source_obligation_refs'])|set(rec['assessment_question_refs'])
        if auth.get('authority_ref') not in allowed: fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',x['item_id']+':authority')
        if not auth.get('content') or not auth.get('source_locator') or len(auth.get('authority_digest',''))!=64: fail('CORE1_PRACTICE_INSTANCE_AUTHORITY_MISSING',x['item_id']+':content')
    if {x['item_ref'] for x in bsol}!={x['item_id'] for x in aitems} or len(bsol)!=len(aitems): fail('APPENDIX_B_INCOMPLETE')
    item_by_id={x['item_id']:x for x in aitems}
    for x in bsol:
        if not x['reasoning_steps'] or not x['verification_steps']: fail('CHEMICAL_CHECK_REDUCED_TO_ANSWER_ONLY',x['solution_id'])
        item=item_by_id.get(x['item_ref'])
        if item is None or x.get('instance_digest')!=item.get('instance_digest'):
            fail('CORE1_SOLUTION_NOT_INSTANCE_BOUND',x['solution_id']+': instance digest')
        generic=('Source-bound expected response: '+item['instance_authority']['content']+' Evidence to preserve:')
        if x.get('final_response','').startswith(generic):
            fail('CORE1_SOLUTION_NOT_INSTANCE_BOUND',x['solution_id']+': generic source restatement')
        item=item_by.get(x['item_ref'])
        if not item or x.get('instance_digest')!=item.get('instance_digest'): fail('APPENDIX_B_INSTANCE_MISMATCH',x['solution_id'])
        if not x.get('final_response') or x['final_response'].startswith('A complete response states the relevant chemical evidence'): fail('APPENDIX_B_GENERIC_SOLUTION',x['solution_id'])
    if hand.get('answer_free') is not True: fail('HANDOUT_CONTAINS_ANSWERS')
    if hand.get('introduced_capability_refs') or set(hand.get('supported_capability_refs',[]))!=required or {x['capability_ref'] for x in hand.get('reference_entries',[])}!=required: fail('HANDOUT_INTRODUCES_NEW_CHEMISTRY')
    return True

def main():
    ap=argparse.ArgumentParser();
    for x in ['study-model','study-scope','instructional-profile','completeness-policy','problem-profile','sources','questions','out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); reg=load_pck_registry(); out=build_plan(load(a.study_model),load(a.study_scope),reg,load(a.instructional_profile),load(a.completeness_policy),load(a.problem_profile),source_set=load(a.sources),question_set=load(a.questions)); Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
