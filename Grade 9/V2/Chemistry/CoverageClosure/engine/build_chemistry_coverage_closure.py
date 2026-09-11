#!/usr/bin/env python3
import argparse, copy, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ELIGIBLE='ELIGIBLE_IN_SCOPE'

def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def uniq(xs): return sorted(set(xs))

def _by(xs,key):
    out=defaultdict(list)
    for x in xs: out[x[key]].append(x)
    return out

def validate_event(e,core2_plan,policy):
    if e.get('subject')!='CHEMISTRY': fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS','subject')
    if e.get('event_digest')!=digest(e,'event_digest'): fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',e.get('event_id','digest'))
    pages={p['question_ref']:p for p in core2_plan['pages']}
    if e['question_ref'] not in pages: fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',e['question_ref'])
    if e['primary_capability_ref']!=pages[e['question_ref']]['primary_capability_ref']: fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',e['event_id']+':capability')
    if e['support_state']=='SOLUTION_EXPOSED' and not e['solution_exposed']: fail('SOLUTION_EXPOSED_RECORDED_AS_MASTERY',e['event_id']+':flag')
    if e['solution_exposed'] and e['support_state']!='SOLUTION_EXPOSED': fail('SOLUTION_EXPOSED_RECORDED_AS_MASTERY',e['event_id']+':state')
    if e['support_state'] not in policy['support_states']: fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',e['event_id']+':support')
    return True

def make_learner_update(e,policy):
    pos=uniq([x['dimension'] for x in e['dimension_evidence'] if x['result']=='SUCCESS'])
    neg=uniq([x['dimension'] for x in e['dimension_evidence'] if x['result']=='FAILURE'])
    blocked=e['diagnostic_use'] in set(policy['negative_inference_blocked_for'])
    independent=(e['support_state']=='INDEPENDENT_SUCCESS' and e['final_answer_correct'] and e['chemistry_reasoning_valid'] and not e['solution_exposed'])
    if e['support_state']=='SOLUTION_EXPOSED' or e['solution_exposed']:
        state='NO_MASTERY_UPDATE'; mastery=False; independent=False
        rationale='Solution exposure is recorded as exposure, not mastery evidence.'
    elif independent:
        state='CURRENT_DEMONSTRATED_INDEPENDENT'; mastery=True
        rationale='Independent success with valid Chemistry reasoning supports the current episode only.'
    elif e['support_state'] in {'H1_SUCCESS','H2_SUCCESS','H3_SUCCESS'} and e['final_answer_correct'] and e['chemistry_reasoning_valid']:
        state='CURRENT_SUPPORTED_SUCCESS'; mastery=False
        rationale='Success occurred after support; support level is preserved and is not relabelled independent.'
    elif e['final_answer_correct'] and not e['chemistry_reasoning_valid']:
        state='PARTIAL_OR_INVALID_REASONING'; mastery=False
        rationale='A correct final answer with invalid Chemistry reasoning cannot establish full capability success.'
    elif e['support_state']=='INCORRECT_AFTER_SUPPORT' and not blocked:
        state='DIFFICULTY_EVIDENCE'; mastery=False
        rationale='Incorrect performance after support contributes negative evidence under the active diagnostic-use policy.'
    else:
        state='NO_UPDATE'; mastery=False
        rationale='The event does not authorize a mastery or negative-state update.'
    out={'update_id':'LSU-'+e['event_id'],'schema_version':'1.0.0','subject':'CHEMISTRY','event_ref':e['event_id'],'question_ref':e['question_ref'],'capability_ref':e['primary_capability_ref'],'support_state':e['support_state'],'current_episode_state':state,'independent_success':independent,'mastery_claim':mastery,'positive_dimensions':pos,'negative_dimensions':neg,'negative_inference_applied':bool(neg) and not blocked and state=='DIFFICULTY_EVIDENCE','rationale':rationale,'update_digest':''}
    out['update_digest']=digest(out,'update_digest')
    return out

def build_learner_updates(events,core2_plan,policy):
    ids=set(); out=[]
    for e in events:
        if e['event_id'] in ids: fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS','duplicate '+e['event_id'])
        ids.add(e['event_id']); validate_event(e,core2_plan,policy); out.append(make_learner_update(e,policy))
    return out

def build_longitudinal(study_model,updates,policy,update_id='CHEM-C-J-LONGITUDINAL-v1'):
    initial={x['capability_ref']:x for x in study_model['longitudinal_initializations']}
    bycap=_by(updates,'capability_ref'); records=[]
    for cap in sorted(initial):
        base=initial[cap]; us=bycap.get(cap,[])
        states=[u['current_episode_state'] for u in us]
        if 'CURRENT_DEMONSTRATED_INDEPENDENT' in states: current='CURRENT_DEMONSTRATED_INDEPENDENT'
        elif 'CURRENT_SUPPORTED_SUCCESS' in states: current='CURRENT_SUPPORTED_SUCCESS'
        elif 'PARTIAL_OR_INVALID_REASONING' in states: current='PARTIAL_OR_INVALID_REASONING'
        elif 'DIFFICULTY_EVIDENCE' in states: current='DIFFICULTY_EVIDENCE'
        elif 'NO_MASTERY_UPDATE' in states: current='NO_MASTERY_UPDATE'
        else: current='NO_EVENT'
        dims=copy.deepcopy(base['dimensions'])
        if current=='CURRENT_DEMONSTRATED_INDEPENDENT':
            dims['acquisition']='CURRENT_DEMONSTRATED_INDEPENDENT'; dims['independent_reconstruction']='CURRENT_EPISODE_SUCCESS'
        elif current=='CURRENT_SUPPORTED_SUCCESS': dims['acquisition']='CURRENT_SUPPORTED_SUCCESS'
        elif current=='PARTIAL_OR_INVALID_REASONING': dims['acquisition']='PARTIAL_OR_INVALID_REASONING'
        elif current=='DIFFICULTY_EVIDENCE': dims['acquisition']='EVIDENCE_OF_DIFFICULTY'
        future=list(base['future_evidence_obligations']); owners=[{'obligation_ref':x,'owner':policy['longitudinal_owner']} for x in future]
        records.append({'capability_ref':cap,'current_episode_state':current,'dimension_states':dims,'remaining_future_evidence_obligations':future,'obligation_owners':owners})
    out={'update_id':update_id,'schema_version':'1.0.0','subject':'CHEMISTRY','study_model_ref':study_model['study_model_id'],'records':records,'update_digest':''}
    out['update_digest']=digest(out,'update_digest'); return out

def build_source_matrix(source_ledger,study_model,core1_plan,representation_bundle,matrix_id='CHEM-C-J-SOURCE-MATRIX-v1'):
    lessons=core1_plan['lessons']; aitems=core1_plan['appendices']['appendix_a']['items']; bsols=core1_plan['appendices']['appendix_b']['solutions']; hand=set(core1_plan['appendices']['appendix_c']['supported_capability_refs']); reps=representation_bundle['representations']
    b_by_item={x['item_ref']:x['solution_id'] for x in bsols}; records=[]
    for o in source_ledger['obligations']:
        caps=set(o['canonical_capability_refs'])
        if o['scope_status']!=ELIGIBLE:
            records.append({'obligation_ref':o['obligation_id'],'scope_status':o['scope_status'],'capability_refs':sorted(caps),'concept_refs':list(o['canonical_concept_refs']),'core1_lesson_refs':[],'appendix_a_item_refs':[],'appendix_b_solution_refs':[],'appendix_c_capability_refs':[],'representation_refs':[],'condition_exception_refs':uniq(o['condition_model_refs']+o['required_exceptions']),'closure_status':'NOT_REQUIRED_OUT_OF_SCOPE'})
            continue
        lrefs=uniq([l['lesson_id'] for l in lessons if o['obligation_id'] in l['scope_trace']['source_obligation_refs']]); arefs=uniq([a['item_id'] for a in aitems if a['primary_capability_ref'] in caps]); brefs=uniq([b_by_item[a] for a in arefs if a in b_by_item]); hrefs=uniq([c for c in caps if c in hand]); rrefs=uniq([r['representation_id'] for r in reps if r['capability_ref'] in caps])
        records.append({'obligation_ref':o['obligation_id'],'scope_status':o['scope_status'],'capability_refs':sorted(caps),'concept_refs':list(o['canonical_concept_refs']),'core1_lesson_refs':lrefs,'appendix_a_item_refs':arefs,'appendix_b_solution_refs':brefs,'appendix_c_capability_refs':hrefs,'representation_refs':rrefs,'condition_exception_refs':uniq(o['condition_model_refs']+o['required_exceptions']),'closure_status':'PASS'})
    req=[r for r in records if r['scope_status']==ELIGIBLE]
    out={'matrix_id':matrix_id,'schema_version':'1.0.0','subject':'CHEMISTRY','source_ledger_ref':source_ledger['ledger_id'],'records':records,'summary':{'source_obligation_total':len(records),'required_total':len(req),'closed_required_total':sum(r['closure_status']=='PASS' for r in req),'out_of_scope_total':sum(r['scope_status']!=ELIGIBLE for r in records)},'matrix_digest':''}
    out['matrix_digest']=digest(out,'matrix_digest'); return out

def build_external_matrix(corpus,classifications,core2_plan,matrix_id='CHEM-C-J-EXTERNAL-MATRIX-v1'):
    classes={x['candidate_id']:x for x in classifications['classifications']}; pages=_by(core2_plan['pages'],'question_ref'); records=[]
    for c in sorted(corpus['candidates'],key=lambda x:x['source_order']):
        cid=c['candidate_id']; cl=classes[cid]; ps=pages.get(cid,[])
        if cl['scope_status']==ELIGIBLE:
            if len(ps)==1: placement='PLACED'
            elif not ps: placement='MISSING'
            else: placement='DUPLICATE'
            source='PASS' if len(ps)==1 and bool(ps[0].get('source_link')) and ps[0].get('source_fidelity',{}).get('candidate_source_digest')==c['source_digest'] else 'NOT_REQUIRED'
            hints='PASS' if len(ps)==1 and all(ps[0].get('hint_ladder',{}).get(k) for k in ['h0_attempt_first','h1_notice','h2_rule_model_representation','h3_start']) else 'NOT_REQUIRED'
            sol='PASS' if len(ps)==1 and ps[0].get('solution_route',{}).get('reasoning_steps') and ps[0].get('solution_route',{}).get('verification_steps') else 'NOT_REQUIRED'
        else:
            placement='UNRESOLVED_VALID' if cl['scope_status']=='SOURCE_UNRESOLVED' else 'EXCLUDED_VALID'; source=hints=sol='NOT_REQUIRED'
        records.append({'candidate_ref':cid,'scope_status':cl['scope_status'],'scope_reason':cl['scope_reason'],'primary_unit':cl['primary_learner_unit'],'core2_page_refs':[p['question_ref'] for p in ps],'primary_concept_refs':[p['primary_concept_ref'] for p in ps],'source_link_status':source,'hint_support_status':hints,'solution_status':sol,'placement_status':placement})
    eligible=[r for r in records if r['scope_status']==ELIGIBLE]; status_counts=Counter(r['scope_status'] for r in records); units=Counter(r['primary_unit'] for r in eligible)
    out={'matrix_id':matrix_id,'schema_version':'1.0.0','subject':'CHEMISTRY','corpus_ref':corpus['corpus_id'],'classification_ref':classifications['classification_id'],'records':records,'summary':{'candidate_total':len(records),'scope_status_counts':dict(sorted(status_counts.items())),'eligible_total':len(eligible),'eligible_by_primary_unit':dict(sorted(units.items())),'placed_unique_total':sum(r['placement_status']=='PLACED' for r in eligible),'missing_total':sum(r['placement_status']=='MISSING' for r in eligible),'duplicate_primary_total':sum(r['placement_status']=='DUPLICATE' for r in eligible),'source_link_failures':sum(r['source_link_status']!='PASS' for r in eligible),'hint_support_failures':sum(r['hint_support_status']!='PASS' for r in eligible),'solution_failures':sum(r['solution_status']!='PASS' for r in eligible)},'matrix_digest':''}
    out['matrix_digest']=digest(out,'matrix_digest'); return out

def build_capability_records(source_ledger,study_model,core1_plan,representation_bundle,core2_plan,longitudinal):
    source_concepts=defaultdict(set)
    for o in source_ledger['obligations']:
        if o['scope_status']==ELIGIBLE:
            for cap in o['canonical_capability_refs']: source_concepts[cap].update(o['canonical_concept_refs'])
    lessons={l['capability_ref']:l for l in core1_plan['lessons']}; a_by=_by(core1_plan['appendices']['appendix_a']['items'],'primary_capability_ref'); b_by={x['item_ref']:x for x in core1_plan['appendices']['appendix_b']['solutions']}; hand=set(core1_plan['appendices']['appendix_c']['supported_capability_refs']); reps=_by(representation_bundle['representations'],'capability_ref'); pages=core2_plan['pages']; long={x['capability_ref']:x for x in longitudinal['records']}
    records=[]
    for r in study_model['capability_records']:
        cap=r['capability_ref']; l=lessons.get(cap); pgs=[p for p in pages if cap==p['primary_capability_ref'] or cap in p['supporting_capability_refs']]; a=a_by.get(cap,[])
        records.append({'capability_ref':cap,'source_obligation_refs':list(r['source_obligation_refs']),'assessment_question_refs':list(r['assessment_question_refs']),'external_candidate_refs':list(r['external_candidate_refs']),'prerequisite_refs':list(r['prerequisite_refs']),'representation_refs':uniq([x['representation_id'] for x in reps.get(cap,[])]),'condition_exception_refs':list(r['condition_exception_obligations']),'problem_family_refs':list(r['problem_family_refs']),'core1_lesson_ref':l['lesson_id'] if l else '','core1_worked_example_ref':(l.get('worked_example') or {}).get('instance_id') if l else None,'appendix_a_item_refs':uniq([x['item_id'] for x in a]),'appendix_b_solution_refs':uniq([b_by[x['item_id']]['solution_id'] for x in a if x['item_id'] in b_by]),'appendix_c_supported':cap in hand,'core2_page_refs':uniq([p['question_ref'] for p in pgs]),'hint_support_refs':uniq([p['question_ref'] for p in pgs if p.get('hint_ladder')]),'reasoning_route_refs':uniq([p['reasoning_route_ref'] for p in pgs]),'solution_refs':uniq([p['question_ref'] for p in pgs if p.get('solution_route',{}).get('reasoning_steps')]),'verification_refs':uniq([p['question_ref'] for p in pgs if p.get('verification_route')]),'future_evidence_obligations':list(r['future_evidence_obligations']),'longitudinal_owner':long[cap]['obligation_owners'][0]['owner'] if long.get(cap) and long[cap]['obligation_owners'] else '','closure_status':'PASS'})
        if a and not source_concepts.get(cap): fail('APPENDIX_A_WITHOUT_PRIMARY_CONCEPT',cap)
    return records

def build_closure(source_ledger,corpus,classifications,study_model,core1_plan,representation_bundle,core2_plan,problem_families,events,policy,closure_id='CHEM-C-J-PUBLICATION-CLOSURE-v1'):
    updates=build_learner_updates(events,core2_plan,policy); longitudinal=build_longitudinal(study_model,updates,policy); sm=build_source_matrix(source_ledger,study_model,core1_plan,representation_bundle); em=build_external_matrix(corpus,classifications,core2_plan); caps=build_capability_records(source_ledger,study_model,core1_plan,representation_bundle,core2_plan,longitudinal)
    out={'closure_id':closure_id,'schema_version':'1.0.0','subject':'CHEMISTRY','source_matrix_ref':sm['matrix_id'],'external_matrix_ref':em['matrix_id'],'source_matrix':sm,'external_matrix':em,'capability_records':caps,'learner_state_updates':updates,'longitudinal_update':longitudinal,'summary':{'required_capability_count':len(caps),'source_obligations_required':sm['summary']['required_total'],'source_obligations_closed':sm['summary']['closed_required_total'],'external_candidates_total':em['summary']['candidate_total'],'eligible_external_total':em['summary']['eligible_total'],'eligible_external_placed_unique':em['summary']['placed_unique_total'],'transfer_event_count':len(events),'learner_state_update_count':len(updates),'longitudinal_capability_count':len(longitudinal['records']),'blocking_failures':0,'status':'PASS'},'closure_digest':''}
    out['closure_digest']=digest(out,'closure_digest'); validate_closure(out,source_ledger,corpus,classifications,study_model,core1_plan,representation_bundle,core2_plan,problem_families,events,policy); return out

def validate_closure(cl,source_ledger,corpus,classifications,study_model,core1_plan,representation_bundle,core2_plan,problem_families,events,policy):
    if cl['closure_digest']!=digest(cl,'closure_digest'): fail('SUMMARY_COUNTERS_NOT_DERIVED_FROM_RECORDS','closure digest')
    sm=cl['source_matrix']; em=cl['external_matrix']
    if sm['matrix_digest']!=digest(sm,'matrix_digest') or em['matrix_digest']!=digest(em,'matrix_digest'): fail('SUMMARY_COUNTERS_NOT_DERIVED_FROM_RECORDS','matrix digest')
    source_by={x['obligation_ref']:x for x in sm['records']}; eligible=[o for o in source_ledger['obligations'] if o['scope_status']==ELIGIBLE]
    for o in eligible:
        r=source_by.get(o['obligation_id'])
        if not r or not r['core1_lesson_refs'] or not r['appendix_a_item_refs'] or not r['representation_refs']: fail('SOURCE_OBLIGATION_WITHOUT_CORE1_COVERAGE',o['obligation_id'])
        if len(r['appendix_b_solution_refs'])!=len(r['appendix_a_item_refs']): fail('APPENDIX_A_WITHOUT_APPENDIX_B_SOLUTION',o['obligation_id'])
        if not set(o['canonical_capability_refs'])<=set(r['appendix_c_capability_refs']): fail('APPENDIX_C_REQUIRED_SUPPORT_MISSING',o['obligation_id'])
    ext_by={x['candidate_ref']:x for x in em['records']}; classes={x['candidate_id']:x for x in classifications['classifications']}
    for cid,c in classes.items():
        r=ext_by.get(cid)
        if c['scope_status']==ELIGIBLE:
            if not r or r['placement_status']=='MISSING': fail('ELIGIBLE_EXTERNAL_QUESTION_WITHOUT_CORE2_TRANSFER',cid)
            if r['placement_status']=='DUPLICATE' or len(r['core2_page_refs'])!=1 or len(r['primary_concept_refs'])!=1: fail('DUPLICATE_PRIMARY_PLACEMENT',cid)
            if r['source_link_status']!='PASS' or r['hint_support_status']!='PASS' or r['solution_status']!='PASS': fail('ELIGIBLE_EXTERNAL_QUESTION_WITHOUT_CORE2_TRANSFER',cid+':support')
    expected_em=build_external_matrix(corpus,classifications,core2_plan)
    if em['summary']!=expected_em['summary'] or em['records']!=expected_em['records']: fail('SUMMARY_COUNTERS_NOT_DERIVED_FROM_RECORDS','external matrix')
    expected_sm=build_source_matrix(source_ledger,study_model,core1_plan,representation_bundle)
    if sm['summary']!=expected_sm['summary']: fail('SUMMARY_COUNTERS_NOT_DERIVED_FROM_RECORDS','source matrix')
    fams={x['family_id'] for x in problem_families['families']}; cap_by={x['capability_ref']:x for x in cl['capability_records']}; model_by={x['capability_ref']:x for x in study_model['capability_records']}; lessons={x['capability_ref']:x for x in core1_plan['lessons']}
    if set(cap_by)!=set(model_by): fail('SOURCE_OBLIGATION_WITHOUT_CORE1_COVERAGE','capability set')
    for cap,m in model_by.items():
        r=cap_by[cap]
        if not r['core1_lesson_ref'] or cap not in lessons: fail('SOURCE_OBLIGATION_WITHOUT_CORE1_COVERAGE',cap)
        if not r['appendix_a_item_refs'] or len(r['appendix_b_solution_refs'])!=len(r['appendix_a_item_refs']): fail('APPENDIX_A_WITHOUT_APPENDIX_B_SOLUTION',cap)
        if not r['appendix_c_supported']: fail('APPENDIX_C_REQUIRED_SUPPORT_MISSING',cap)
        if (m['representation_level_obligations'] or m['representation_requirement_obligations']) and not r['representation_refs']: fail('REQUIRED_REPRESENTATION_WITHOUT_SEMANTIC_PRIMITIVE',cap)
        if any(x not in fams and not x.startswith('QF-') for x in r['problem_family_refs']): fail('REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY',cap)
        if m['condition_exception_obligations']:
            l=lessons[cap]
            if set(l['condition_exception_obligations'])!=set(m['condition_exception_obligations']): fail('CONDITION_EXCEPTION_OBLIGATION_DISAPPEARS',cap)
            reps=[x for x in representation_bundle['representations'] if x['capability_ref']==cap]
            if not reps or not any(set(m['condition_exception_obligations'])<=set(x['condition_exception_context']) for x in reps): fail('CONDITION_EXCEPTION_OBLIGATION_DISAPPEARS',cap+':representation')
        for p in [x for x in core2_plan['pages'] if x['question_ref'] in r['core2_page_refs']]:
            if p['problem_family_ref'] not in fams or not p['reasoning_route_ref']: fail('REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY',p['question_ref'])
    ev={e['event_id']:e for e in events}; ups={u['event_ref']:u for u in cl['learner_state_updates']}
    if set(ev)!=set(ups): fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS')
    for eid,e in ev.items():
        u=ups[eid]
        if u['update_digest']!=digest(u,'update_digest'): fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',eid+':digest')
        expected=make_learner_update(e,policy)
        if e['support_state']=='H3_SUCCESS' and (u['independent_success'] or u['current_episode_state']=='CURRENT_DEMONSTRATED_INDEPENDENT'): fail('H3_SUCCESS_RECORDED_AS_INDEPENDENT_SUCCESS',eid)
        if e['support_state']=='SOLUTION_EXPOSED' and (u['mastery_claim'] or u['current_episode_state']!='NO_MASTERY_UPDATE'): fail('SOLUTION_EXPOSED_RECORDED_AS_MASTERY',eid)
        expected_pos=set(x['dimension'] for x in e['dimension_evidence'] if x['result']=='SUCCESS')
        if not expected_pos<=set(u['positive_dimensions']): fail('ARITHMETIC_FAILURE_ERASES_RULE_SELECTION_SUCCESS',eid)
        if e['final_answer_correct'] and not e['chemistry_reasoning_valid'] and (u['mastery_claim'] or u['current_episode_state']=='CURRENT_DEMONSTRATED_INDEPENDENT'): fail('CORRECT_ANSWER_WITH_INVALID_CHEMISTRY_RECORDED_AS_FULL_SUCCESS',eid)
        if e['diagnostic_use'] in policy['negative_inference_blocked_for'] and u['negative_inference_applied']: fail('NEGATIVE_EVIDENCE_FROM_EXCLUDED_ITEM',eid)
        for k in ['current_episode_state','independent_success','mastery_claim','positive_dimensions','negative_dimensions','negative_inference_applied']:
            if u[k]!=expected[k]: fail('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',eid+':'+k)
    long=cl['longitudinal_update']
    if long['update_digest']!=digest(long,'update_digest'): fail('LONGITUDINAL_OBLIGATION_DISAPPEARS','digest')
    long_by={x['capability_ref']:x for x in long['records']}; initial={x['capability_ref']:x for x in study_model['longitudinal_initializations']}
    if set(long_by)!=set(initial): fail('LONGITUDINAL_OBLIGATION_DISAPPEARS','capability coverage')
    for cap,b in initial.items():
        r=long_by[cap]; init=set(b['future_evidence_obligations']); rem=set(r['remaining_future_evidence_obligations'])
        if init!=rem: fail('CURRENT_SUCCESS_ERASES_FUTURE_RETRIEVAL',cap)
        owners={x['obligation_ref']:x['owner'] for x in r['obligation_owners']}
        if set(owners)!=init or any(not owners[x] for x in init): fail('LONGITUDINAL_OBLIGATION_DISAPPEARS',cap)
    expected_summary={'required_capability_count':len(cap_by),'source_obligations_required':len(eligible),'source_obligations_closed':sum(source_by[o['obligation_id']]['closure_status']=='PASS' for o in eligible),'external_candidates_total':len(corpus['candidates']),'eligible_external_total':sum(x['scope_status']==ELIGIBLE for x in classes.values()),'eligible_external_placed_unique':sum(x['placement_status']=='PLACED' for x in em['records'] if x['scope_status']==ELIGIBLE),'transfer_event_count':len(events),'learner_state_update_count':len(cl['learner_state_updates']),'longitudinal_capability_count':len(long['records']),'blocking_failures':0,'status':'PASS'}
    if cl['summary']!=expected_summary: fail('SUMMARY_COUNTERS_NOT_DERIVED_FROM_RECORDS','publication summary')
    return True

def main():
    ap=argparse.ArgumentParser()
    for x in ['source-ledger','corpus','external-classifications','study-model','core1-plan','representation-bundle','core2-plan','problem-families','events','policy','out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); ev=load(a.events); out=build_closure(load(a.source_ledger),load(a.corpus),load(a.external_classifications),load(a.study_model),load(a.core1_plan),load(a.representation_bundle),load(a.core2_plan),load(a.problem_families),ev['events'],load(a.policy)); Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
