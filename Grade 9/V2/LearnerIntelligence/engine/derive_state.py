#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENGINE_VERSION='2.0.0'
FORBIDDEN_DECISION_TOKENS={'reteach','repair_before','repair_in_unit','compress','include_contrast','expand_bridge','study_priority','teaching_sequence','use_representation','next_support_ceiling','page_layout','hint_rung','practice_count','study_decision','teaching_decision'}

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def parse_time(value: str) -> datetime:
    if not value: raise ValueError('explicit as_of is required')
    dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    if dt.tzinfo is None: raise ValueError('timestamps must be timezone-aware')
    return dt.astimezone(timezone.utc)

def assert_descriptive_projection(value: Any) -> None:
    def walk(obj: Any):
        if isinstance(obj, dict):
            for k,v in obj.items():
                lk=k.lower().replace('-','_')
                if any(tok in lk for tok in FORBIDDEN_DECISION_TOKENS): raise ValueError(f'descriptive projection contains downstream decision field: {k}')
                walk(v)
        elif isinstance(obj, list):
            for v in obj: walk(v)
        elif isinstance(obj, str):
            lv=obj.lower().replace('-','_').replace(' ','_')
            if any(tok in lv for tok in FORBIDDEN_DECISION_TOKENS): raise ValueError(f'descriptive projection contains downstream decision value: {obj}')
    walk(value)

def _registry_index(registry):
    rows=registry.get('capabilities',[]); idx={r['capability_id']:r for r in rows}
    if len(idx)!=len(rows): raise ValueError('duplicate canonical capability_id')
    return idx

def _filter_ledger(ledger, as_of, temporal):
    if temporal['rule']!='INCLUDE_EVIDENCE_OCCURRED_ON_OR_BEFORE_AS_OF': raise ValueError('unsupported temporal rule')
    cutoff=parse_time(as_of); out={k:v for k,v in ledger.items() if k!='sessions'}; out['sessions']=[]
    for s in ledger.get('sessions',[]):
        occurred=s.get('occurred_at')
        if not occurred:
            if temporal['undated_evidence']=='REJECT': raise ValueError('undated evidence rejected by temporal policy')
            continue
        if parse_time(occurred)<=cutoff: out['sessions'].append(s)
    out['sessions']=sorted(out['sessions'],key=lambda s:(s['occurred_at'],s['session_id']))
    return out

def _attempt_index(ledger):
    idx={}
    for s in ledger.get('sessions',[]):
        for a in s.get('attempts',[]):
            if a['attempt_id'] in idx: raise ValueError('duplicate attempt_id')
            idx[a['attempt_id']]={'session':s,'attempt':a}
    return idx

def _state_for(stats, policy):
    success=stats['independent_success']; failure=stats['independent_failure']; transfer=stats['transfer_success']; delayed=stats['delayed_success']
    if failure>=policy['repair_independent_failure_min']: return 'REPAIR_REQUIRED', ('HIGH' if failure>policy['repair_independent_failure_min'] else 'MEDIUM')
    if success>=policy['robust_independent_success_min'] and failure==0 and ((transfer+delayed)>0 or not policy['robust_requires_transfer_or_delayed']): return 'ROBUST','HIGH'
    if success>=policy['ready_independent_success_min'] and failure==0: return 'READY','MEDIUM'
    if success>0: return policy['single_success_state'],'LOW'
    if failure==1: return policy['single_failure_state'],'LOW'
    return 'UNKNOWN','LOW'

def derive(ledger, observations, registry, diagnostic_policy, state_policy, temporal_policy, as_of):
    if diagnostic_policy.get('allow_unobserved_psychological_cause_inference') is not False: raise ValueError('psychological-cause inference must be prohibited')
    if diagnostic_policy.get('guided_success_counts_as_independent') is not False: raise ValueError('guided success cannot count as independent')
    if diagnostic_policy.get('preserve_upstream_success') is not True: raise ValueError('positive-evidence preservation is mandatory')
    if ledger.get('privacy_class')=='PUBLIC_SYNTHETIC' and ledger.get('production_evidence') is True: raise ValueError('synthetic fixture cannot be production learner evidence')
    reg=_registry_index(registry); filtered=_filter_ledger(ledger,as_of,temporal_policy); attempts=_attempt_index(filtered)
    included=[]; stats=defaultdict(lambda:defaultdict(int)); subjects=defaultdict(set); obs_refs=defaultdict(list)
    class_key={'INDEPENDENT_SUCCESS':'independent_success','INDEPENDENT_FAILURE':'independent_failure','GUIDED_SUCCESS':'guided_success','GUIDED_FAILURE':'guided_failure','TRANSFER_SUCCESS':'transfer_success','TRANSFER_FAILURE':'transfer_failure','DELAYED_SUCCESS':'delayed_success','DELAYED_FAILURE':'delayed_failure','AMBIGUOUS':'ambiguous'}
    for obs in observations:
        if obs['attempt_id'] not in attempts: continue
        cap=obs['capability_ref']
        if cap not in reg: raise ValueError(f'unknown canonical capability reference: {cap}')
        definition=reg[cap]
        if definition.get('scope')=='SUBJECT' and definition.get('subject')!=obs['subject']: raise ValueError(f'subject mismatch for capability {cap}')
        ec=obs['evidence_class']
        if ec not in class_key: raise ValueError(f'unknown evidence class: {ec}')
        included.append(obs); subjects[cap].add(obs['subject']); obs_refs[cap].append(obs['observation_id']); stats[cap][class_key[ec]]+=1
    cases=[]; capability_states=[]; count_keys=['independent_success','independent_failure','guided_success','guided_failure','transfer_success','transfer_failure','delayed_success','delayed_failure','ambiguous']
    for cap in sorted(stats):
        row=stats[cap]; counts={k:int(row.get(k,0)) for k in count_keys}; state,confidence=_state_for(counts,state_policy); ambiguous=counts['ambiguous']>0; failures=counts['independent_failure']
        if ambiguous or failures:
            cases.append({'diagnostic_case_id':f"CASE-{digest([cap,sorted(obs_refs[cap]),diagnostic_policy['version']])[:16]}",'target_capability_ref':cap,'observation_refs':sorted(obs_refs[cap]),'status':'OPEN' if ambiguous else 'SUSPECTED','evidence_strength':'WEAK' if failures<=1 else ('MODERATE' if failures==2 else 'STRONG'),'hypotheses':[],'probe_required':ambiguous,'recommended_probe_refs':sorted(reg[cap].get('diagnostic_probe_refs',[])) if ambiguous else [],'policy_ref':f"{diagnostic_policy['policy_id']}@{diagnostic_policy['version']}"})
        capability_states.append({'capability_ref':cap,'state':state,'confidence':confidence,'subjects_seen':sorted(subjects[cap]),'evidence_summary':counts})
    recurrence=[]
    for cap in sorted(stats):
        definition=reg[cap]; row=stats[cap]
        if definition.get('scope')=='SHARED' and row.get('independent_failure',0)>=state_policy['cross_subject_candidate_min_failures'] and len(subjects[cap])>=state_policy['cross_subject_candidate_min_subjects']:
            recurrence.append({'capability_ref':cap,'subjects_seen':sorted(subjects[cap]),'failure_count':row['independent_failure'],'classification':'CROSS_SUBJECT_RECURRING_FAILURE_CANDIDATE','causal_status':'CANDIDATE_NOT_CAUSE'})
    inputs={'evidence_digest':digest(filtered),'observation_digest':digest(sorted(included,key=lambda x:x['observation_id'])),'canonical_registry_version':registry['registry_version'],'diagnostic_policy_version':diagnostic_policy['version'],'state_policy_version':state_policy['version'],'temporal_policy_version':temporal_policy['version']}
    snapshot_body={'schema_version':'2.0.0','learner_ref':ledger['learner_ref'],'privacy_class':ledger['privacy_class'],'as_of':as_of,'inputs':inputs,'capability_states':capability_states,'diagnostic_cases':sorted(cases,key=lambda x:x['diagnostic_case_id']),'cross_subject_candidates':recurrence}
    snap_digest=digest(snapshot_body); snapshot={'snapshot_id':f'LI-SNAPSHOT-{snap_digest[:20]}',**snapshot_body,'snapshot_digest':snap_digest}
    research_body={'snapshot_ref':snapshot['snapshot_id'],'snapshot_digest':snap_digest,'privacy_class':ledger['privacy_class'],'capability_states':capability_states,'diagnostic_cases':snapshot['diagnostic_cases'],'cross_subject_candidates':recurrence}; assert_descriptive_projection(research_body)
    rv_digest=digest(research_body); research={'view_id':f'LI-RESEARCH-{rv_digest[:20]}',**research_body,'view_digest':rv_digest}
    probe_reqs=[{'diagnostic_case_ref':c['diagnostic_case_id'],'capability_ref':c['target_capability_ref'],'probe_required':c['probe_required'],'recommended_probe_refs':c['recommended_probe_refs']} for c in snapshot['diagnostic_cases'] if c['probe_required']]
    publication_body={'snapshot_ref':snapshot['snapshot_id'],'snapshot_digest':snap_digest,'privacy_class':'MINIMIZED','capability_states':[{'capability_ref':x['capability_ref'],'state':x['state'],'confidence':x['confidence']} for x in capability_states],'probe_requirements':probe_reqs}; assert_descriptive_projection(publication_body)
    pv_digest=digest(publication_body); publication={'view_id':f'LI-PUBLICATION-{pv_digest[:20]}',**publication_body,'view_digest':pv_digest}
    return {'snapshot':snapshot,'research_learner_view':research,'publication_planning_view':publication}

def main():
    p=argparse.ArgumentParser()
    for name in ['ledger','observations','registry','diagnostic-policy','state-policy','temporal-policy']: p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--as-of',required=True); p.add_argument('--out',type=Path); a=p.parse_args()
    result=derive(load_json(a.ledger),load_json(a.observations),load_json(a.registry),load_json(a.diagnostic_policy),load_json(a.state_policy),load_json(a.temporal_policy),a.as_of)
    text=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.out: a.out.write_text(text,encoding='utf-8')
    else: print(text,end='')
if __name__=='__main__': main()
