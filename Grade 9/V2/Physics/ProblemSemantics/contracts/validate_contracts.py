#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parents[1]; PHYSICS=D.parent
sys.path.insert(0,str(D/'engine'))
from build_physics_problem_semantics import build_package, load

def schema(name): return load(D/'contracts'/name)
def check(s,obj,label):
    errs=sorted(Draft202012Validator(s).iter_errors(obj),key=lambda e:list(e.path))
    if errs: raise AssertionError(f"{label}: {errs[0].message} at {list(errs[0].path)}")
role=load(D/'registry/physics-reasoning-role-registry.json'); fam=load(D/'registry/physics-problem-family-registry.json'); ver=load(D/'registry/physics-verification-route-registry.json'); items=load(D/'registry/motion-item-semantics.json'); badge=load(D/'registry/guide-demand-badge-policy.json')
for f in fam['families']: check(schema('physics-problem-family.schema.json'),f,f['family_id'])
for r in ver['routes']: check(schema('physics-verification-route.schema.json'),r,r['verification_route_id'])
for p in items['profiles']: check(schema('physics-item-semantic-profile.schema.json'),p,p['item_ref'])
pkg=build_package(load(PHYSICS/'AssessmentIntake/fixtures/motion-question-set.fixture.json'),load(PHYSICS/'AssessmentIntake/fixtures/motion-topic-scope.fixture.json'),load(PHYSICS/'AssessmentReview/registry/physics-item-validity-registry.json'),load(PHYSICS/'AssessmentReview/policies/diagnostic-use-policy.json'),load(PHYSICS/'Canonical/registry/capabilities.json'),load(PHYSICS/'AssessmentScope/authority/physics-assessment-scope-authority.json'),load(PHYSICS/'AssessmentScope/registry/motion-question-scope-bindings.json'),role,fam,ver,items,badge)
for x in pkg['items']:
    check(schema('physics-reasoning-route.schema.json'),x['reasoning_route'],x['item_ref']+':route')
    check(schema('physics-model-validity-binding.schema.json'),x['model_validity_binding'],x['item_ref']+':validity')
    check(schema('physics-demand-vector.schema.json'),x['demand_vector'],x['item_ref']+':demand')
check(schema('physics-problem-semantics-package.schema.json'),pkg,'package')
print(f"PHYSICS P-D contract validation = {len(fam['families'])} families, {len(ver['routes'])} verification routes, {len(pkg['items'])} item semantics PASS")
