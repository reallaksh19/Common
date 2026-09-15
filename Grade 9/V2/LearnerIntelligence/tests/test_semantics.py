#!/usr/bin/env python3
from pathlib import Path
import copy, importlib.util, json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('derive_state',ROOT/'engine/derive_state.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
load=lambda n: json.loads((ROOT/'fixtures'/n).read_text(encoding='utf-8'))
ledger=load('learner_evidence.synthetic.json'); obs=load('observations.synthetic.json'); reg=load('canonical_refs.synthetic.json'); dp=load('diagnostic_policy.synthetic.json'); sp=load('state_policy.synthetic.json'); tp=load('temporal_policy.synthetic.json'); ASOF='2026-09-11T00:00:00+00:00'
def derive(**kw): return m.derive(kw.get('ledger',ledger),kw.get('observations',obs),kw.get('registry',reg),kw.get('diagnostic_policy',dp),kw.get('state_policy',sp),kw.get('temporal_policy',tp),kw.get('as_of',ASOF))
a=derive(); b=derive(); assert m.canonical_bytes(a)==m.canonical_bytes(b)
states={x['capability_ref']:x for x in a['snapshot']['capability_states']}; assert states['SYN-MATH-MODELLING']['state']=='DEVELOPING'; assert states['SYN-SHARED-SYMBOLIC']['state']=='REPAIR_REQUIRED'; assert states['SYN-SHARED-SYMBOLIC']['evidence_summary']['independent_failure']==2
assert any(x['capability_ref']=='SYN-SHARED-SYMBOLIC' and x['causal_status']=='CANDIDATE_NOT_CAUSE' for x in a['snapshot']['cross_subject_candidates']); assert states['SYN-PHYS-STATE']['state']=='UNKNOWN'
cases={x['target_capability_ref']:x for x in a['snapshot']['diagnostic_cases']}; assert cases['SYN-PHYS-STATE']['probe_required'] is True; assert cases['SYN-PHYS-STATE']['recommended_probe_refs']==['SYN-PROBE-STATE']; assert 'SYN-CHEM-RELATION' not in states
assert 'work_steps' not in json.dumps(a['publication_planning_view']); assert a['publication_planning_view']['privacy_class']=='MINIMIZED'
one=[x for x in copy.deepcopy(obs) if x['observation_id']!='O3']; x=m.derive(ledger,one,reg,dp,sp,tp,ASOF); st={r['capability_ref']:r['state'] for r in x['snapshot']['capability_states']}; assert st['SYN-SHARED-SYMBOLIC']=='DEVELOPING'
guided=copy.deepcopy(obs); guided.append({'observation_id':'OG','attempt_id':'A1','subject':'MATHEMATICS','capability_ref':'SYN-MATH-MODELLING','evidence_class':'GUIDED_SUCCESS','verification':{'method':'HUMAN_REVIEW','result':'PASS'},'confidence':'HIGH'}); x=m.derive(ledger,guided,reg,dp,sp,tp,ASOF); row={r['capability_ref']:r for r in x['snapshot']['capability_states']}['SYN-MATH-MODELLING']; assert row['evidence_summary']['independent_success']==1 and row['evidence_summary']['guided_success']==1
bad=copy.deepcopy(obs); bad[0]['capability_ref']='NOT-CANONICAL'
try: m.derive(ledger,bad,reg,dp,sp,tp,ASOF); raise AssertionError('unknown canonical ref accepted')
except ValueError as e: assert 'unknown canonical' in str(e)
badledger=copy.deepcopy(ledger); badledger['production_evidence']=True
try: derive(ledger=badledger); raise AssertionError('synthetic fixture accepted')
except ValueError as e: assert 'synthetic fixture' in str(e)
later=derive(as_of='2026-09-30T00:00:00+00:00'); assert later['snapshot']['snapshot_digest']!=a['snapshot']['snapshot_digest']; assert any(r['capability_ref']=='SYN-CHEM-RELATION' for r in later['snapshot']['capability_states'])
for payload in ({'teaching_sequence':['x']},{'notes':'REPAIR_BEFORE unit'}):
    try: m.assert_descriptive_projection(payload); raise AssertionError('decision accepted')
    except ValueError: pass
badp=copy.deepcopy(dp); badp['allow_unobserved_psychological_cause_inference']=True
try: derive(diagnostic_policy=badp); raise AssertionError('psychological inference enabled')
except ValueError: pass
try: m.derive(ledger,obs,reg,dp,sp,tp,None); raise AssertionError('missing as_of accepted')
except Exception: pass
print('V2_LEARNER_INTELLIGENCE_SEMANTIC_FALSIFIERS = PASS')
