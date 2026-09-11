#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import defaultdict
from pathlib import Path

D=Path(__file__).resolve().parents[1]
CHEM=D.parent
sys.path.insert(0,str(CHEM/'AssessmentIntake'/'engine'))
from build_chemistry_assessment_intake import verify_questions, verify_attempts  # noqa:E402


def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None,array=None,key=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    if array and key: x[array]=sorted(x[array],key=lambda r:r[key])
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def item_ref(attempt): return attempt['question_ref'] if attempt['part_ref'] is None else f"{attempt['question_ref']}.{attempt['part_ref']}"

def validate_evidence(ledger,attempts,question_set,semantics,review_bundle,registry):
    if ledger['ledger_digest']!=digest(ledger,'ledger_digest','observations','observation_id'): fail('LEARNER_EVIDENCE_LEDGER_DIGEST_MISMATCH')
    if ledger['subject']!='CHEMISTRY': fail('LEARNER_EVIDENCE_SUBJECT_MISMATCH')
    if ledger['attempt_set_ref']!=attempts['attempt_set_id']: fail('EVIDENCE_ATTEMPT_SET_MISMATCH')
    qids,parts=verify_questions(question_set); verify_attempts(attempts,qids,parts)
    attempt_by={a['attempt_id']:a for a in attempts['attempts']}
    sem_by={x['target_ref']:x for x in semantics['question_semantics']}
    review_by={x['item_ref']:x for x in review_bundle['question_reviews']}
    codes={x['code']:x for x in registry['codes']}
    if len(codes)!=len(registry['codes']): fail('DUPLICATE_OBSERVATION_CODE')
    seen=set()
    for o in ledger['observations']:
        if o['observation_id'] in seen: fail('DUPLICATE_REASONING_OBSERVATION',o['observation_id'])
        seen.add(o['observation_id'])
        if o['attempt_ref'] not in attempt_by: fail('OBSERVATION_WITHOUT_ATTEMPT',o['observation_id'])
        a=attempt_by[o['attempt_ref']]
        if item_ref(a)!=o['item_ref']: fail('OBSERVATION_ITEM_BINDING_MISMATCH',o['observation_id'])
        if o['item_ref'] not in sem_by or o['item_ref'] not in review_by: fail('OBSERVATION_WITHOUT_AUTHORITY',o['item_ref'])
        if o['observation_code'] not in codes: fail('UNKNOWN_CHEMISTRY_OBSERVATION_CODE',o['observation_code'])
        meta=codes[o['observation_code']]
        if meta['polarity']!=o['polarity']: fail('OBSERVATION_POLARITY_MISMATCH',o['observation_id'])
        route=sem_by[o['item_ref']]['reasoning_route']['steps']
        if meta['affects_chemistry_state']:
            roles=[x['role'] for x in route]
            if o['route_role'] not in roles: fail('OBSERVATION_ROUTE_ROLE_MISMATCH',o['observation_id'])
            if o['route_step_index'] is not None:
                if o['route_step_index']<1 or o['route_step_index']>len(route) or route[o['route_step_index']-1]['role']!=o['route_role']:
                    fail('OBSERVATION_ROUTE_STEP_MISMATCH',o['observation_id'])
            allowed=set()
            for step in route: allowed.update(step['capability_refs'])
            if not set(o['capability_refs']).issubset(allowed): fail('OBSERVATION_CAPABILITY_BINDING_MISMATCH',o['observation_id'])
    return attempt_by,sem_by,review_by,codes

def build_snapshot(scope_bundle,review_bundle,semantics,question_set,registry,policy,attempts=None,ledger=None,snapshot_id='CHEM-C-E-SNAPSHOT'):
    if scope_bundle['subject']!='CHEMISTRY' or semantics['subject']!='CHEMISTRY': fail('DIAGNOSTIC_SUBJECT_MISMATCH')
    eligible_sem=[x for x in semantics['question_semantics'] if x['scope_status']=='ELIGIBLE_IN_SCOPE']
    capability_refs=sorted({cap for rec in eligible_sem for step in rec['reasoning_route']['steps'] for cap in step['capability_refs']})
    state={cap:{'capability_ref':cap,'state':'UNKNOWN','confidence':0.0,'positive_evidence_refs':[],'negative_evidence_refs':[]} for cap in capability_refs}
    scope_ref=scope_bundle['scope_reconciliation']['declared_topic_scope_ref']
    scope_digest=scope_bundle['scope_reconciliation']['declared_topic_scope_digest']
    if attempts is None:
        if ledger is not None: fail('EVIDENCE_PRESENT_WITHOUT_ATTEMPT_SET')
        return {'snapshot_id':snapshot_id,'subject':'CHEMISTRY','assessment_scope_ref':scope_ref,'assessment_scope_digest':scope_digest,'attempt_mode':'ABSENT','scope_unchanged':True,'support_policy':policy['no_attempt_support_policy'],'capability_states':list(state.values()),'diagnostic_cases':[],'probe_requirements':['PROBE_FIRST_IF_TREATMENT_DEPENDS_ON_STATE']}
    if ledger is None: fail('ATTEMPT_PRESENT_WITHOUT_EVIDENCE_LEDGER')
    _,sem_by,review_by,codes=validate_evidence(ledger,attempts,question_set,semantics,review_bundle,registry)
    min_conf=policy['minimum_confidence_for_state']
    cases_by_code=defaultdict(list); processed=[]; probes=[]
    for o in ledger['observations']:
        meta=codes[o['observation_code']]; effective=min(o['observation_confidence'],o['extraction_confidence'],o['transcription_confidence'])
        sem=sem_by[o['item_ref']]; review=review_by[o['item_ref']]
        disposition='CREDITED' if o['polarity']=='POSITIVE' else 'NEGATIVE_EVIDENCE'
        if sem['scope_status']!='ELIGIBLE_IN_SCOPE' or (o['polarity']=='NEGATIVE' and review['diagnostic_use']=='EXCLUDE_FROM_NEGATIVE_INFERENCE'):
            disposition='IGNORED_INVALID_ITEM'
        elif effective<min_conf:
            disposition='LOW_CONFIDENCE_PROBE_REQUIRED'
        elif o['polarity']=='NEGATIVE' and not review['diagnostic_constraints']['negative_inference_allowed']:
            disposition='IGNORED_INVALID_ITEM'
        elif not meta['affects_chemistry_state']:
            disposition='SHARED_EXECUTION_ERROR_LOCALIZED'
        if disposition=='CREDITED':
            for cap in o['capability_refs']:
                if cap in state:
                    state[cap]['positive_evidence_refs'].append(o['observation_id']); state[cap]['confidence']=max(state[cap]['confidence'],effective)
        elif disposition=='NEGATIVE_EVIDENCE':
            for cap in o['capability_refs']:
                if cap in state:
                    state[cap]['negative_evidence_refs'].append(o['observation_id']); state[cap]['confidence']=max(state[cap]['confidence'],effective)
            cases_by_code[o['observation_code']].append((o,effective,meta))
        elif disposition=='LOW_CONFIDENCE_PROBE_REQUIRED':
            cases_by_code[o['observation_code']].append((o,effective,meta)); probes.append(meta['probe_family'])
        elif disposition=='IGNORED_INVALID_ITEM':
            cases_by_code['IGNORED:'+o['observation_code']].append((o,effective,meta))
        elif disposition=='SHARED_EXECUTION_ERROR_LOCALIZED':
            cases_by_code['SHARED:'+o['observation_code']].append((o,effective,meta))
        processed.append({'observation_ref':o['observation_id'],'item_ref':o['item_ref'],'observation_code':o['observation_code'],'effective_confidence':effective,'disposition':disposition})
    for s in state.values():
        p=bool(s['positive_evidence_refs']); n=bool(s['negative_evidence_refs'])
        s['state']='MIXED' if p and n else 'DEMONSTRATED' if p else 'EVIDENCE_OF_DIFFICULTY' if n else 'UNKNOWN'
    cases=[]
    for key,items in sorted(cases_by_code.items()):
        first,_,meta=items[0]; ev=[x[0]['observation_id'] for x in items]; conf=max(x[1] for x in items)
        if key.startswith('IGNORED:'):
            status='IGNORED_INVALID_ITEM'; probe=None; rationale='Upstream item integrity/diagnostic-use or scope blocks negative learner inference.'
        elif key.startswith('SHARED:'):
            status='HYPOTHESIS'; probe=None; rationale='Shared arithmetic/execution failure is localized and does not erase demonstrated Chemistry reasoning.'
        else:
            high={x[0]['attempt_ref'] for x in items if x[1]>=min_conf}
            if len(high)>=policy['confirmed_misconception_min_independent_negative_evidence']:
                status='CONFIRMED'; probe=None; rationale='Independent high-confidence negative evidence meets the confirmation threshold.'
            else:
                status='PROBE_REQUIRED'; probe=meta['probe_family']; probes.append(meta['probe_family']); rationale='Evidence is insufficient for a confirmed misconception; targeted probing is required.'
        cases.append({'case_id':f"CASE-{first['observation_code']}",'subject':'CHEMISTRY','hypothesis_code':first['observation_code'],'capability_refs':sorted({c for x in items for c in x[0]['capability_refs']}),'evidence_refs':ev,'status':status,'confidence':conf,'probe_requirement':probe,'rationale':rationale})
    snapshot={'snapshot_id':snapshot_id,'subject':'CHEMISTRY','assessment_scope_ref':scope_ref,'assessment_scope_digest':scope_digest,'attempt_mode':'PRESENT','scope_unchanged':True,'support_policy':policy['attempt_support_policy'],'capability_states':[state[k] for k in sorted(state)],'diagnostic_cases':cases,'probe_requirements':sorted(set(probes))}
    return {'snapshot':snapshot,'processed_evidence':processed,'attempt_set_ref':attempts['attempt_set_id'],'evidence_ledger_ref':ledger['ledger_id']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--scope-bundle',required=True); ap.add_argument('--review-bundle',required=True); ap.add_argument('--semantics',required=True); ap.add_argument('--question-set',required=True); ap.add_argument('--observation-registry',required=True); ap.add_argument('--diagnostic-policy',required=True); ap.add_argument('--attempts'); ap.add_argument('--evidence'); ap.add_argument('--out',required=True); a=ap.parse_args()
    result=build_snapshot(load(a.scope_bundle),load(a.review_bundle),load(a.semantics),load(a.question_set),load(a.observation_registry),load(a.diagnostic_policy),load(a.attempts) if a.attempts else None,load(a.evidence) if a.evidence else None)
    Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
