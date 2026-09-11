#!/usr/bin/env python3
import copy, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHYS=ROOT.parent; LI=PHYS/'LearnerIntelligence'
spec=importlib.util.spec_from_file_location('li',LI/'engine/derive_physics_state.py'); li=importlib.util.module_from_spec(spec); spec.loader.exec_module(li)
state=li.derive(li.load(LI/'fixtures/evidence.synthetic.json'),li.load(LI/'fixtures/inference_policy.synthetic.json'),li.load(LI/'fixtures/learner_intelligence_interface.synthetic.json'))
sys.path.insert(0,str(ROOT/'engine')); import synthesize_physics_study_model as m
g=m.load(ROOT/'fixtures/goal_scope.synthetic.json'); c=m.load(ROOT/'fixtures/canonical_knowledge_set.synthetic.json'); p=m.load(ROOT/'fixtures/study_policy.synthetic.json')
def run(goal=None,cks=None,st=None,policy=None): return m.synthesize(copy.deepcopy(goal or g),copy.deepcopy(cks or c),copy.deepcopy(st or state),copy.deepcopy(policy or p))
def dec(o,t): return next(x for x in o['learner_study_model']['target_decisions'] if x['target_id']==t)
a=run(); assert a['status']=='PASS'
q=dec(a,'PHY-PROJECTILE-COMPONENT-DECOMPOSITION'); assert q['engagement_mode']=='VERIFY_ONLY' and q['source_capability_state']=='READY'
q=dec(a,'PHY-MODEL-SELECTION'); assert q['engagement_mode']=='USE_AS_ENTRY_POINT' and q['readiness_mode']=='READY'
q=dec(a,'PHY-MOTION-PROPAGATE-STATE'); assert q['engagement_mode']=='ACTIVE_STUDY' and q['readiness_mode']=='REPAIR_BEFORE' and q['source_capability_state']=='REPAIR_REQUIRED'
assert 'KINEMATICS=WEAK' not in json.dumps(a) and 'PHYSICS=WEAK' not in json.dumps(a)
q=dec(a,'PHY-PROJECTILE-COMPONENT-DECOMPOSITION'); assert q['readiness_mode']=='PROBE_FIRST' and q['probe_refs']==['PHY-PROBE-APEX-COMPONENTS']
q=dec(a,'PHY-SIGNED-DISPLACEMENT-INTERPRETATION'); assert q['readiness_mode']=='PROBE_FIRST' and q['probe_refs']==['PHY-PROBE-SIGNED-DISPLACEMENT']
x=a['learner_study_model']['external_dependency_decisions']; assert len(x)==1 and x[0]['dependency_ref']=='SHARED-ARITHMETIC-EXECUTION' and x[0]['semantics_owner']=='EXTERNAL_CANONICAL_DEPENDENCY'
cc=copy.deepcopy(c); cc['refs'].remove('PHY-PHYSICAL-VALIDATION'); o=run(cks=cc); assert o['status']=='BLOCKED' and any(z['gap_type']=='CANONICAL_KNOWLEDGE_GAP' for z in o['gaps'])
ss=copy.deepcopy(state); next(x for x in ss['capability_states'] if x['capability_ref']=='PHY-MODEL-SELECTION')['evidence_refs']=[]; o=run(st=ss); assert o['status']=='BLOCKED' and any(z['gap_type']=='LEARNER_STATE_REASON_GAP' for z in o['gaps'])
ss=copy.deepcopy(state); ss['raw_attempts']=[]
try: run(st=ss); raise AssertionError('raw attempts accepted')
except ValueError: pass
pp=copy.deepcopy(p); pp['benchmark_inputs']=['PR #156']
try: run(policy=pp); raise AssertionError('benchmark accepted')
except Exception: pass
bad=copy.deepcopy(a['learner_study_model']); bad['hint_ladder']=[]; assert m.find_forbidden_output(bad)
bad=copy.deepcopy(a['learner_study_model']); bad['page_layout']={}; assert m.find_forbidden_output(bad)
for d in a['learner_study_model']['target_decisions']:
 assert d['canonical_refs'] and d['learner_state_reason_refs']
 for r in d['study_requirements']: assert r['canonical_refs'] and r['learner_state_reason_refs']
assert dec(a,'PHY-STATE-VARIABLE-MEANING')['source_capability_state']=='READY' and dec(a,'PHY-MODEL-SELECTION')['source_capability_state']=='READY'
b=run(); assert m.canonical_bytes(a)==m.canonical_bytes(b)
g0,c0,s0,p0=map(lambda x:json.dumps(x,sort_keys=True),[g,c,state,p]); run(); assert [g0,c0,s0,p0]==[json.dumps(x,sort_keys=True) for x in [g,c,state,p]]
print('PHY-V2-03 StudyModel falsifiers = 17 PASS')
