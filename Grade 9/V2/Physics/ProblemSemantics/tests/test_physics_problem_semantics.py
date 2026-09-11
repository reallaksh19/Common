#!/usr/bin/env python3
import copy, sys
from pathlib import Path
D=Path(__file__).resolve().parents[1]; PHYSICS=D.parent
sys.path.insert(0,str(D/'engine'))
from build_physics_problem_semantics import build_package, load, dwo, validate_badge_assignment
Q=load(PHYSICS/'AssessmentIntake/fixtures/motion-question-set.fixture.json'); S=load(PHYSICS/'AssessmentIntake/fixtures/motion-topic-scope.fixture.json'); R=load(PHYSICS/'AssessmentReview/registry/physics-item-validity-registry.json'); P=load(PHYSICS/'AssessmentReview/policies/diagnostic-use-policy.json'); C=load(PHYSICS/'Canonical/registry/capabilities.json'); A=load(PHYSICS/'AssessmentScope/authority/physics-assessment-scope-authority.json'); B=load(PHYSICS/'AssessmentScope/registry/motion-question-scope-bindings.json')
ROLE=load(D/'registry/physics-reasoning-role-registry.json'); FAM=load(D/'registry/physics-problem-family-registry.json'); VER=load(D/'registry/physics-verification-route-registry.json'); ITEM=load(D/'registry/motion-item-semantics.json'); BADGE=load(D/'registry/guide-demand-badge-policy.json')
def run(role=ROLE,fam=FAM,ver=VER,item=ITEM,badge=BADGE): return build_package(Q,S,R,P,C,A,B,role,fam,ver,item,badge)
def redigest(x,k): x[k]=''; x[k]=dwo(x,k)
def expect(code,fn):
    try: fn()
    except ValueError as e:
        got=str(e).split(':',1)[0]
        if got!=code: raise AssertionError(f"expected {code}, got {e}") from e
        return
    raise AssertionError(f"expected {code}")
def family(reg,fid): return next(x for x in reg['families'] if x['family_id']==fid)
def profile(reg,item): return next(x for x in reg['profiles'] if x['item_ref']==item)
pkg=run(); by={x['item_ref']:x for x in pkg['items']}
assert len(by)==17 and pkg['attempt_data_consumed'] is False and pkg['learner_support_independent'] is True
assert by['Q8']['graph_operations']==['SIGNED_AREA']
assert {'IDENTIFY_PHASES','PROPAGATE_STATE','CHECK_CONTINUITY_OR_BOUNDARY'}<=set(s['role'] for s in by['Q10']['reasoning_route']['steps'])
assert by['Q11']['reference_frame']['frame_text']=='common ground frame'
assert by['Q13']['resolution_status']=='BLOCKED' and by['Q13']['graph_operations']==['UNRESOLVED_DUE_SOURCE'] and by['Q13']['guide_demand_badge']['label'] is None
assert by['Q14']['resolution_status']=='BLOCKED' and by['Q14']['validity_state']=='REVIEW_REQUIRED'
assert all(x['demand_vector']['psychometric_claim'] is False and x['guide_demand_badge']['psychometric_claim'] is False for x in by.values())

f=copy.deepcopy(FAM); z=family(f,'PHY-PF-PATH-VS-CHORD'); z['reasoning_route_template'][0]['hint_text']='try this'; redigest(z,'family_digest'); redigest(f,'registry_digest')
expect('REASONING_ROUTE_EQUALS_HINT_COPY',lambda:run(fam=f))
f=copy.deepcopy(FAM); z=family(f,'PHY-PF-PATH-VS-CHORD'); z['reasoning_route_template'][0]['final_answer']='42'; redigest(z,'family_digest'); redigest(f,'registry_digest')
expect('REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY',lambda:run(fam=f))
i=copy.deepcopy(ITEM); p=profile(i,'Q1'); p['difficulty']='HARD'; redigest(p,'profile_digest'); redigest(i,'registry_digest')
expect('DIFFICULTY_UNEXPLAINED_SCALAR',lambda:run(item=i))
# Direct hard-label guard: a shallow route cannot be labeled HARD even if a scalar score would suggest it.
expect('HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE',lambda:validate_badge_assignment('HARD',by['Q1']['demand_vector'],{'steps':by['Q1']['reasoning_route']['steps'][:2]},[],BADGE,'Q1'))
i=copy.deepcopy(ITEM); i['profiles']=[x for x in i['profiles'] if x['item_ref']!='Q2']; redigest(i,'registry_digest')
expect('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',lambda:run(item=i))
f=copy.deepcopy(FAM); z=family(f,'PHY-PF-FREE-FALL'); z['reasoning_route_template']=[s for s in z['reasoning_route_template'] if s['role']!='CHECK_MODEL_VALIDITY']; redigest(z,'family_digest'); redigest(f,'registry_digest')
expect('MODEL_VALIDITY_ROUTE_MISSING',lambda:run(fam=f))
v=copy.deepcopy(VER); v['routes']=[r for r in v['routes'] if r['family_ref']!='PHY-PF-XT-SLOPE']; redigest(v,'registry_digest')
expect('VERIFICATION_ROUTE_MISSING',lambda:run(ver=v))
f=copy.deepcopy(FAM); z=family(f,'PHY-PF-EQUAL-DISTANCE-AVERAGE-SPEED'); z['reference_frame_requirements']={'required':True,'sign_convention_required':True,'frame_kind':'EXPLICIT_OR_GRAPH_DEFINED'}; redigest(z,'family_digest'); redigest(f,'registry_digest')
expect('FRAME_DEPENDENT_ITEM_WITHOUT_FRAME_BINDING',lambda:run(fam=f))
f=copy.deepcopy(FAM); z=family(f,'PHY-PF-MULTIPHASE-KINEMATICS'); z['reasoning_route_template']=[s for s in z['reasoning_route_template'] if s['role']!='PROPAGATE_STATE']; redigest(z,'family_digest'); redigest(f,'registry_digest')
expect('MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF',lambda:run(fam=f))
i=copy.deepcopy(ITEM); p=profile(i,'Q8'); p['graph_operations']=['HEIGHT']; redigest(p,'profile_digest'); redigest(i,'registry_digest')
expect('GRAPH_ROUTE_COLLAPSES_HEIGHT_SLOPE_AREA',lambda:run(item=i))
pkg2=run(); assert pkg==pkg2
print('PHYSICS P-D problem-semantics falsifiers = 10 PASS + deterministic replay PASS')
