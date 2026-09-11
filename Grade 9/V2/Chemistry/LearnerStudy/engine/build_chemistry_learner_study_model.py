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

def derive_study_scope(scope_bundle,source_ledger,qbindings,external,study_scope_id='CHEM-C-F-STUDY-SCOPE-v1'):
    if any(x.get('subject')!='CHEMISTRY' for x in [scope_bundle,source_ledger,qbindings,external]): fail('STUDY_SCOPE_SUBJECT_MISMATCH')
    s=[r for r in source_ledger['obligations'] if r['scope_status']==ELIGIBLE]
    q=[r for r in qbindings['bindings'] if r['scope_status']==ELIGIBLE]
    e=[r for r in external['classifications'] if r['scope_status']==ELIGIBLE]
    excluded=[r['candidate_id'] for r in external['classifications'] if r['scope_status']!=ELIGIBLE]
    caps=uniq([c for r in s+q+e for c in r['canonical_capability_refs']])
    out={'study_scope_id':study_scope_id,'schema_version':'1.0.0','subject':'CHEMISTRY','assessment_scope_ref':scope_bundle['bundle_id'],'assessment_scope_digest':scope_bundle['bundle_digest'],'declared_scope_ref':scope_bundle['declared_scope_ref'],'declared_scope_digest':scope_bundle['declared_scope_digest'],'required_source_obligation_refs':uniq([r['obligation_id'] for r in s]),'required_assessment_question_refs':uniq([r['item_ref'] for r in q]),'required_external_candidate_refs':uniq([r['candidate_id'] for r in e]),'excluded_external_candidate_refs':uniq(excluded),'required_capability_refs':caps,'scope_invariant':True,'study_scope_digest':''}
    out['study_scope_digest']=digest(out,'study_scope_digest'); return out

def collect_capability_authority(study_scope,source_ledger,qbindings,external,semantics):
    caps={c:{'source':set(),'questions':set(),'external':set(),'prereq':set(),'levels':set(),'requirements':set(),'entities':set(),'conditions':set(),'conservation':set(),'families':set(),'verification':set()} for c in study_scope['required_capability_refs']}
    ss={x['target_ref']:x for x in semantics['source_semantics']}; qs={x['target_ref']:x for x in semantics['question_semantics']}
    def semantic_add(a,sem):
        if not sem:return
        a['families'].add(sem['problem_family_ref']); a['verification'].update(sem['verification_route']['checkpoints'])
        for step in sem['reasoning_route']['steps']: a['conservation'].update(step['conservation_refs'])
        a['conditions'].update(sem['condition_validity']['required_conditions']); a['conditions'].update(sem['condition_validity']['required_exceptions'])
    for r in source_ledger['obligations']:
        if r['scope_status']!=ELIGIBLE: continue
        for c in r['canonical_capability_refs']:
            if c not in caps: continue
            a=caps[c]; a['source'].add(r['obligation_id']); a['prereq'].update(r['prerequisite_refs']); a['levels'].update(r['representation_levels']); a['requirements'].update(r['representation_requirements']); a['conditions'].update(r['condition_model_refs']); a['conditions'].update(r['required_exceptions']); semantic_add(a,ss.get(r['obligation_id']))
    for r in qbindings['bindings']:
        if r['scope_status']!=ELIGIBLE: continue
        for c in r['canonical_capability_refs']:
            if c not in caps: continue
            a=caps[c]; a['questions'].add(r['item_ref']); a['prereq'].update(r['prerequisite_capability_refs']); a['levels'].update(r['representation_levels']); a['requirements'].update(r['representation_demands']); a['entities'].update(r['chemical_entity_refs']); a['conditions'].update(r['conditions_exceptions']); a['conservation'].update(r['conservation_obligations']); a['families'].update(r['problem_family_refs']); a['verification'].update(r['verification_obligations']); semantic_add(a,qs.get(r['item_ref']))
    for r in external['classifications']:
        if r['scope_status']!=ELIGIBLE: continue
        for c in r['canonical_capability_refs']:
            if c not in caps: continue
            a=caps[c]; a['external'].add(r['candidate_id']); a['prereq'].update(r['prerequisite_capability_refs']); a['levels'].update(r['representation_levels']); a['requirements'].update(r['representation_demands']); a['families'].update(r['problem_family_refs'])
    for c,a in caps.items(): a['prereq'].discard(c)
    return caps

def future_obligations(cap,a):
    out={'DELAYED_INDEPENDENT_RECONSTRUCTION','NEAR_TRANSFER_NEW_INSTANCE','FAR_TRANSFER_NEW_CONTEXT','MIXED_DISCRIMINATION','FLUENCY_CHECK','TIMED_PERFORMANCE_CHECK'}
    if len(a['levels'])>1 or 'PARTICULATE' in a['levels'] or 'TRANSLATE' in cap: out.add('CROSS_REPRESENTATION_TRANSLATION')
    if a['conditions']: out.add('HIDDEN_CONDITION_OR_EXCEPTION')
    if cap in {'CAP-TRACK-REACTING-SPECIES','CAP-ATTACH-SPECIES-ROLE'}: out.add('NEW_EQUATION_SPECIES_ROLE')
    if a['conservation']: out.add('UNPROMPTED_CONSERVATION_VERIFICATION')
    if a['verification']: out.add('INDEPENDENT_CHEMICAL_VERIFICATION')
    return sorted(out)

def choose_treatment(cap,state,probe_caps,downstream,policy,attempt_mode):
    if cap in probe_caps or state=='MIXED': return 'PROBE_FIRST'
    if state=='DEMONSTRATED': return 'READY_VERIFY_ONLY'
    if state=='EVIDENCE_OF_DIFFICULTY': return policy['prerequisite_difficulty_treatment'] if downstream.get(cap) else policy['state_to_treatment'][state]
    treatment=policy['state_to_treatment'][state]
    if attempt_mode=='ABSENT' and treatment in policy['no_attempt_forbidden_treatments']: fail('NO_ATTEMPT_FORCES_REPAIR',cap)
    return treatment

def build_model(study_scope,source_ledger,qbindings,external,semantics,learner_snapshot,policy,study_model_id='CHEM-C-F-STUDY-MODEL-v1'):
    snap=learner_snapshot.get('snapshot',learner_snapshot)
    if snap['subject']!='CHEMISTRY' or policy['subject']!='CHEMISTRY': fail('STUDY_MODEL_SUBJECT_MISMATCH')
    if snap['assessment_scope_digest']!=study_scope['declared_scope_digest']: fail('LEARNER_STATE_SCOPE_DRIFT')
    auth=collect_capability_authority(study_scope,source_ledger,qbindings,external,semantics)
    states={x['capability_ref']:x for x in snap['capability_states']}
    downstream=defaultdict(set)
    for c,a in auth.items():
        for p in a['prereq']:
            if p in auth and p!=c: downstream[p].add(c)
    probe_caps={c for case in snap['diagnostic_cases'] if case['status'] in policy['diagnostic_probe_override_statuses'] for c in case['capability_refs']}
    records=[]; longitudinal=[]
    for cap in study_scope['required_capability_refs']:
        a=auth[cap]; state=states.get(cap,{'state':'UNKNOWN'})['state']; treatment=choose_treatment(cap,state,probe_caps,downstream,policy,snap['attempt_mode']); fut=future_obligations(cap,a)
        rationale={'READY_VERIFY_ONLY':'Current evidence supports brief activation and an independent check; required scope remains present.','ACTIVE_STUDY':'Required source/assessment scope remains teachable without inventing a learner weakness.','REPAIR_BEFORE':'Evidence indicates difficulty in a prerequisite used by downstream required Chemistry capabilities.','REPAIR_IN_UNIT':'Evidence indicates localized difficulty that can be repaired inside this required capability.','PROBE_FIRST':'Current evidence is mixed, low-confidence, or diagnostically insufficient; resolve it before committing to repair.'}[treatment]
        rec={'capability_ref':cap,'source_obligation_refs':uniq(a['source']),'assessment_question_refs':uniq(a['questions']),'external_candidate_refs':uniq(a['external']),'prerequisite_refs':uniq(a['prereq']),'learner_state_ref':snap['snapshot_id'],'learner_state':state,'treatment':treatment,'priority':policy['priority_by_treatment'][treatment],'sequencing_rationale':rationale,'supporting_downstream_refs':uniq(downstream.get(cap,set())),'required_pck_jobs':list(policy['required_pck_jobs_by_treatment'][treatment]),'representation_level_obligations':uniq(a['levels']),'representation_requirement_obligations':uniq(a['requirements']),'chemical_entity_species_obligations':uniq(a['entities']),'condition_exception_obligations':uniq(a['conditions']),'conservation_obligations':uniq(a['conservation']),'problem_family_refs':uniq(a['families']),'verification_requirements':uniq(a['verification']),'future_evidence_obligations':fut,'source_trace_status':'DIRECT_SOURCE_REQUIRED' if a['source'] else 'ASSESSMENT_AUTHORIZED_WITHIN_SCOPE'}
        records.append(rec)
        longitudinal.append({'capability_ref':cap,'dimensions':{'acquisition':'CURRENT_EVIDENCE' if state!='UNKNOWN' else 'OPEN','independent_reconstruction':'OPEN','delayed_retention':'OPEN','near_transfer':'OPEN','far_transfer':'OPEN','mixed_discrimination':'OPEN','representation_translation':'OPEN' if ('CROSS_REPRESENTATION_TRANSLATION' in fut) else 'NOT_APPLICABLE','condition_exception_discrimination':'OPEN' if a['conditions'] else 'NOT_APPLICABLE','fluency':'OPEN','timed_performance':'OPEN'},'future_evidence_obligations':fut})
    counts=Counter(r['treatment'] for r in records)
    out={'study_model_id':study_model_id,'schema_version':'1.0.0','subject':'CHEMISTRY','study_scope_ref':study_scope['study_scope_id'],'study_scope_digest':study_scope['study_scope_digest'],'learner_snapshot_ref':snap['snapshot_id'],'attempt_mode':snap['attempt_mode'],'treatment_policy_ref':policy['policy_id'],'capability_records':records,'longitudinal_initializations':longitudinal,'summary':{'required_capability_count':len(records),'treatment_counts':dict(sorted(counts.items())),'scope_complete':True,'source_trace_complete':True,'out_of_scope_external_included':0},'study_model_digest':''}
    out['study_model_digest']=digest(out,'study_model_digest'); validate_model(out,study_scope,source_ledger,qbindings,external,semantics,policy); return out

def validate_model(model,study_scope,source_ledger,qbindings,external,semantics,policy):
    if study_scope['study_scope_digest']!=digest(study_scope,'study_scope_digest'): fail('STUDY_SCOPE_DIGEST_MISMATCH')
    if model['study_model_digest']!=digest(model,'study_model_digest'): fail('STUDY_MODEL_DIGEST_MISMATCH')
    if model['study_scope_ref']!=study_scope['study_scope_id'] or model['study_scope_digest']!=study_scope['study_scope_digest']: fail('LEARNER_WEAKNESS_SHRINKS_REQUIRED_SCOPE')
    auth=collect_capability_authority(study_scope,source_ledger,qbindings,external,semantics); recs={r['capability_ref']:r for r in model['capability_records']}
    if len(recs)!=len(model['capability_records']) or set(recs)!=set(study_scope['required_capability_refs']): fail('LEARNER_WEAKNESS_SHRINKS_REQUIRED_SCOPE')
    noneligible={r['candidate_id'] for r in external['classifications'] if r['scope_status']!=ELIGIBLE}
    longs={x['capability_ref']:x for x in model['longitudinal_initializations']}
    if set(longs)!=set(recs): fail('ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL','longitudinal coverage')
    for cap,r in recs.items():
        a=auth[cap]
        if set(r['source_obligation_refs'])!=a['source']: fail('STUDYMODEL_WITHOUT_SOURCE_TRACE',cap)
        if set(r['assessment_question_refs'])!=a['questions']: fail('LEARNER_WEAKNESS_SHRINKS_REQUIRED_SCOPE',cap)
        if set(r['external_candidate_refs'])!=a['external'] or set(r['external_candidate_refs'])&noneligible: fail('OUT_OF_SCOPE_PYQ_EXPANDS_CORE1',cap)
        if set(r['condition_exception_obligations'])!=a['conditions']: fail('SOURCE_EXCEPTION_DROPPED_FROM_STUDYMODEL',cap)
        if set(r['representation_level_obligations'])!=a['levels'] or set(r['representation_requirement_obligations'])!=a['requirements']: fail('REPRESENTATION_TRANSLATION_DROPPED_FROM_STUDYMODEL',cap)
        if set(r['conservation_obligations'])!=a['conservation']: fail('CONSERVATION_REQUIREMENT_DROPPED_FROM_STUDYMODEL',cap)
        if model['attempt_mode']=='ABSENT' and r['treatment'] in policy['no_attempt_forbidden_treatments']: fail('NO_ATTEMPT_FORCES_REPAIR',cap)
        if r['learner_state']=='DEMONSTRATED' and r['treatment']!='READY_VERIFY_ONLY': fail('UPSTREAM_CHEMISTRY_STRENGTH_RELABELLED_WEAK_TO_SUPPORT_REPAIR',cap)
        if r['treatment']=='READY_VERIFY_ONLY' and r['required_pck_jobs']!=policy['required_pck_jobs_by_treatment']['READY_VERIFY_ONLY']: fail('READY_CAPABILITY_FULLY_RETAUGHT_FOR_PAGE_DENSITY',cap)
        if longs[cap]['dimensions']['delayed_retention']!='OPEN': fail('ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL',cap)
    if model['summary']['required_capability_count']!=len(recs) or not model['summary']['scope_complete'] or not model['summary']['source_trace_complete']: fail('LEARNER_WEAKNESS_SHRINKS_REQUIRED_SCOPE','summary')
    return True

def main():
    ap=argparse.ArgumentParser()
    for x in ['scope-bundle','source-ledger','question-bindings','external-classifications','semantics','learner-snapshot','treatment-policy','scope-out','model-out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); scope=derive_study_scope(load(a.scope_bundle),load(a.source_ledger),load(a.question_bindings),load(a.external_classifications)); model=build_model(scope,load(a.source_ledger),load(a.question_bindings),load(a.external_classifications),load(a.semantics),load(a.learner_snapshot),load(a.treatment_policy)); Path(a.scope_out).write_text(json.dumps(scope,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8'); Path(a.model_out).write_text(json.dumps(model,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
