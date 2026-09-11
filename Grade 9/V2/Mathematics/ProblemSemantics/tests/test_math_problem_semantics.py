#!/usr/bin/env python3
import copy, json, sys, tempfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]; MATH=D.parent
sys.path.insert(0,str(D/"engine"))
from build_math_problem_semantics import build_package, validate_family_registry, validate_profiles, derive_badge, dwo, load_family_registry

def L(p): return json.loads(Path(p).read_text())
Q=L(MATH/"AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json")
S=L(MATH/"AssessmentIntake/fixtures/mixed-grade9-topic-scope.fixture.json")
RR=L(MATH/"AssessmentReview/registry/assessment-item-validity-registry.json")
RP=L(MATH/"AssessmentReview/policies/diagnostic-use-policy.json")
A=L(MATH/"AssessmentScope/authority/math-assessment-scope-authority.json")
B=L(MATH/"AssessmentScope/registry/mixed-grade9-question-scope-bindings.json")
ROLE=L(D/"registry/math-reasoning-role-registry.json")
FAM=load_family_registry(D/"registry/math-problem-family-registry.json")
VER=L(D/"registry/math-verification-route-registry.json")
ITEM=L(D/"registry/mixed-grade9-item-semantics.json")
POL=L(D/"registry/guide-demand-badge-policy.json")

def reseal(x,k): x[k]=dwo(x,k); return x

def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code), (code,str(e)); return
    raise AssertionError(f"expected {code}")

P=build_package(Q,S,RR,RP,A,B,ROLE,FAM,VER,ITEM,POL)
rows={x["item_ref"]:x for x in P["assessment_item_semantics"]}
assert len(rows)==17
assert rows['Q9']['validity_state']=='UNDERDETERMINED'
assert rows['Q9']['diagnostic_use']=='POSITIVE_EVIDENCE_ONLY'
assert rows['Q12']['primary_family_ref']=='MATH-PF-EQUILATERAL-COORDINATE'
assert rows['Q14']['primary_family_ref']=='MATH-PF-RIVER-CURRENT-SYSTEM'
assert all(x['reasoning_route']['learner_support_independent'] for x in rows.values())
assert all(x['demand_vector']['psychometric_claim'] is False and x['guide_demand_badge']['psychometric_claim'] is False for x in rows.values())
assert rows['Q10']['guide_demand_badge']['label']=='HARD'
assert rows['Q12']['guide_demand_badge']['label']=='HARD'
assert rows['Q14']['guide_demand_badge']['label']=='HARD'

# REASONING_ROUTE_EQUALS_HINT_COPY / SOLUTION_SUMMARY
bad=copy.deepcopy(FAM); bad['families'][0]['reasoning_route_template'][0]['hint_text']='look here'; reseal(bad['families'][0],'family_digest'); reseal(bad,'registry_digest')
expect('REASONING_ROUTE_EQUALS_HINT_COPY',lambda: build_package(Q,S,RR,RP,A,B,ROLE,bad,VER,ITEM,POL))
bad=copy.deepcopy(FAM); bad['families'][0]['reasoning_route_template'][0]['solution_text']='full answer'; reseal(bad['families'][0],'family_digest'); reseal(bad,'registry_digest')
expect('REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY',lambda: build_package(Q,S,RR,RP,A,B,ROLE,bad,VER,ITEM,POL))

# PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY
bad=copy.deepcopy(ITEM); bad['profiles']=[x for x in bad['profiles'] if x['item_ref']!='Q7']; reseal(bad,'registry_digest')
expect('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',lambda: build_package(Q,S,RR,RP,A,B,ROLE,FAM,VER,bad,POL))

# VERIFICATION_ROUTE_MISSING
bad=copy.deepcopy(VER); bad['routes']=[x for x in bad['routes'] if x['verification_route_id']!='MATH-VR-LINE-INTERCEPT']; reseal(bad,'registry_digest')
expect('VERIFICATION_ROUTE_MISSING',lambda: build_package(Q,S,RR,RP,A,B,ROLE,FAM,bad,ITEM,POL))

# DIFFICULTY_UNEXPLAINED_SCALAR is prevented structurally/policy-wise: vectors are multi-dimensional evidence, never a difficulty field.
def no_difficulty_key(x):
    if isinstance(x,dict): return all(k not in {'difficulty','overall_difficulty'} and no_difficulty_key(v) for k,v in x.items())
    if isinstance(x,list): return all(no_difficulty_key(v) for v in x)
    return True
assert all(no_difficulty_key(x) for x in [ITEM,POL,P])

# HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE
q=copy.deepcopy(rows['Q10']['demand_vector']); route=copy.deepcopy(rows['Q10']['reasoning_route']); route['steps']=route['steps'][:2]
b=derive_badge(q,route,rows['Q10']['verification_route_refs'],{**POL,'rules':{**POL['rules'],'easy_max_score':0,'medium_max_score':0}})
assert b['label']!='HARD'

# M-C family identity cannot silently drift.
bad=copy.deepcopy(FAM); bad['families'][0]['family_id']='MATH-PF-INVENTED'; reseal(bad['families'][0],'family_digest'); reseal(bad,'registry_digest')
expect('PROBLEM_FAMILY_IDENTITY_COVERAGE',lambda: build_package(Q,S,RR,RP,A,B,ROLE,bad,VER,ITEM,POL))

# deterministic replay
P2=build_package(Q,S,RR,RP,A,B,ROLE,FAM,VER,ITEM,POL)
assert json.dumps(P,sort_keys=True,separators=(',',':'))==json.dumps(P2,sort_keys=True,separators=(',',':'))
print('MATH M-D problem semantics falsifiers PASS')
