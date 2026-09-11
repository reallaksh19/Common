#!/usr/bin/env python3
import copy, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHYS=ROOT.parent; LI=PHYS/'LearnerIntelligence'; SS=PHYS/'StudySynthesis'
spec=importlib.util.spec_from_file_location('li',LI/'engine/derive_physics_state.py'); li=importlib.util.module_from_spec(spec); spec.loader.exec_module(li)
state=li.derive(li.load(LI/'fixtures/evidence.synthetic.json'),li.load(LI/'fixtures/inference_policy.synthetic.json'),li.load(LI/'fixtures/learner_intelligence_interface.synthetic.json'))
sys.path.insert(0,str(SS/'engine')); import synthesize_physics_study_model as ss
study=ss.synthesize(ss.load(SS/'fixtures/goal_scope.synthetic.json'),ss.load(SS/'fixtures/canonical_knowledge_set.synthetic.json'),state,ss.load(SS/'fixtures/study_policy.synthetic.json'))
sys.path.insert(0,str(ROOT/'engine')); import design_physics_learning as d; import select_runtime_support as rt
policy=d.load(ROOT/'fixtures/design_policy.synthetic.json'); plan=d.design(copy.deepcopy(study),copy.deepcopy(policy)); blocks=plan['blocks']; bm={b['role']:b for b in blocks if b['target_id']=='PHY-MOTION-PROPAGATE-STATE'}
reqs={r['requirement_id'] for x in study['learner_study_model']['target_decisions'] for r in x['study_requirements']}; assert reqs=={x['requirement_id'] for x in plan['obligation_coverage']}
sb={x['target_id']:(x['engagement_mode'],x['readiness_mode']) for x in study['learner_study_model']['target_decisions']}; pb={x['target_id']:(x['engagement_mode'],x['readiness_mode']) for x in plan['target_bindings']}; assert sb==pb and pb['PHY-MOTION-PROPAGATE-STATE'][1]=='REPAIR_BEFORE'
for t,p in [('PHY-PROJECTILE-COMPONENT-DECOMPOSITION','PHY-PROBE-APEX-COMPONENTS'),('PHY-SIGNED-DISPLACEMENT-INTERPRETATION','PHY-PROBE-SIGNED-DISPLACEMENT')]:
 xs=sorted([b for b in blocks if b['target_id']==t],key=lambda b:b['order']); assert xs[0]['role']=='DIAGNOSTIC_PROBE' and xs[0]['payload']['probe_ref']==p and xs[0]['payload']['correction_before_probe'] is False
assert bm['REPRESENTATION']['payload']['representation']=='BOUNDARY_STATE_TABLE' and 'continuous_state_variables' in bm['REPRESENTATION']['payload']['semantic_payload']
assert bm['WORKED_REASONING']['payload']['answer_only'] is False and len(bm['WORKED_REASONING']['payload']['reasoning_steps'])>=6
mc=bm['MINIMAL_CONTRAST']['payload']; assert len(mc['invariants'])>=5 and mc['focal_difference']=='boundary-state handoff only'
assert bm['GUIDED_ATTEMPT']['support_level']>bm['FADED_ATTEMPT']['support_level']>bm['INDEPENDENT_ATTEMPT']['support_level']
ind=bm['INDEPENDENT_ATTEMPT']['payload']; assert ind['conceptual_hint'] is False and ind['preselected_next_state'] is False
tr=bm['TRANSFER']['payload']; assert tr['numbers_only_change'] is False and len(tr['structural_changes'])>=2
assert bm['WORKED_REASONING']['payload']['verification_embedded'] is True and len(bm['VERIFICATION']['payload']['checks'])>=4
assert {'same system','same reference frame','same phase-1 terminal state','same boundary event'}<=set(mc['invariants'])
st={'schema_version':'1.0.0','design_id':plan['design_id'],'same_route_failures':2}; sel=rt.choose(plan,st); assert sel['support_id']=='H3' and sel['route']=='ROUTE_CHANGE' and any(x['support_id']=='H3' for x in plan['support_assets'])
assert 'same_route_failures' not in json.dumps(plan) and 'InteractionSupportState' not in json.dumps(plan)
x=plan['external_dependency_support'][0]; assert x['dependency_ref']=='SHARED-ARITHMETIC-EXECUTION' and x['semantics_owner']=='EXTERNAL_CANONICAL_DEPENDENCY'
for token in ('page_layout','renderer','pagination','page_position'): assert token not in json.dumps(plan)
assert 'PR #156' not in json.dumps(plan) and 'benchmark_reference' not in json.dumps(plan)
plan2=d.design(copy.deepcopy(study),copy.deepcopy(policy)); assert d.cb(plan)==d.cb(plan2)
s0,p0,pl0=map(lambda x:json.dumps(x,sort_keys=True),[study,policy,plan]); rt.choose(plan,st); assert [s0,p0,pl0]==[json.dumps(x,sort_keys=True) for x in [study,policy,plan]]
print('PHY-V2-04 Learning Design falsifiers = 20 PASS')
