#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[
 str(D/'engine'),str(CHEM/'CoreAuthoring'/'engine'),str(CHEM/'AssessmentReview'/'engine'),
 str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine'),
 str(CHEM/'LearnerEvidence'/'engine'),str(CHEM/'LearnerStudy'/'engine')]
from build_chemistry_core2_transfer import build_plan,validate_plan,digest
from build_chemistry_core1 import build_plan as build_core1,load_pck_registry
from review_chemistry_assessment import build_review,load_registry as load_review_registry
from build_chemistry_scope import build_scope
from build_chemistry_reasoning_semantics import build_semantics
from infer_chemistry_learner_evidence import build_snapshot
from build_chemistry_learner_study_model import derive_study_scope,build_model

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError('expected '+code)
def page(plan,cid): return next(x for x in plan['pages'] if x['question_ref']==cid)
def redigest_page(p): p['page_digest']=''; p['page_digest']=digest(p,'page_digest')
def redigest_plan(p): p['plan_digest']=''; p['plan_digest']=digest(p,'plan_digest'); return p

def upstream():
    A=CHEM/'AssessmentIntake'/'fixtures'; R=CHEM/'AssessmentReview'; S=CHEM/'AssessmentScope'; RS=CHEM/'ReasoningSemantics'; E=CHEM/'LearnerEvidence'; LS=CHEM/'LearnerStudy'; CA=CHEM/'CoreAuthoring'
    sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
    review_reg,manifest_digest=load_review_registry(R/'registry'/'chemistry-item-validity-registry.json')
    review=build_review(copy.deepcopy(sources),copy.deepcopy(questions),review_reg,load(R/'policies'/'chemistry-diagnostic-use-policy.json'),load(R/'registry'/'chemistry-qc-events.json'),registry_manifest_digest=manifest_digest)
    source_ledger=load(S/'registry'/'chemistry-source-obligation-ledger.json'); qbindings=load(S/'registry'/'chemistry-question-capability-bindings.json'); external=load(S/'registry'/'chemistry-external-corpus-classification.json'); authority=load(S/'authority'/'chemistry-canonical-authority.json')
    scope=build_scope(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(authority))
    families=load(RS/'registry'/'chemistry-problem-family-registry.json'); guide=load(RS/'registry'/'chemistry-guide-demand-badge-policy.json')
    semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(families),load(RS/'registry'/'chemistry-reasoning-role-registry.json'),copy.deepcopy(guide))
    no_attempt=build_snapshot(copy.deepcopy(scope),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),load(E/'registry'/'chemistry-observation-code-registry.json'),load(E/'registry'/'chemistry-diagnostic-policy.json'))
    study_scope=derive_study_scope(copy.deepcopy(scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
    model=build_model(copy.deepcopy(study_scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(no_attempt),load(LS/'registry'/'chemistry-treatment-policy.json'),'CHEM-C-I-UPSTREAM')
    pck=load_pck_registry(); core_profile=load(CA/'registry'/'chemistry-instructional-authoring-profile.json'); completeness=load(CA/'registry'/'chemistry-core1-scope-completeness-policy.json'); problems=load(CA/'registry'/'chemistry-problem-authoring-profile.json')
    core1=build_core1(copy.deepcopy(model),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(core_profile),copy.deepcopy(completeness),copy.deepcopy(problems),'CHEM-C-I-CORE1')
    return corpus,external,model,core1,families,guide

corpus,external,model,core1,families,guide=upstream()
bodies=load(D/'fixtures'/'chemistry-external-transfer-source.fixture.json'); transfer=load(D/'registry'/'chemistry-transfer-badge-policy.json'); concepts=load(D/'registry'/'chemistry-concept-segregation.json'); profile=load(D/'registry'/'chemistry-core2-authoring-profile.json'); primitives=load(CHEM/'Representation'/'registry'/'chemistry-teaching-primitive-registry.json'); notation=load(CHEM/'Representation'/'registry'/'chemistry-notation-render-contract.json')
args=(corpus,external,bodies,core1,model,families,guide,transfer,concepts,profile,primitives,notation)
plan=build_plan(*copy.deepcopy(args))
assert len(plan['pages'])==5 and plan['summary']['source_candidate_denominator']==6
assert plan['excluded_candidate_refs']==['EXT06']
assert [x['question_ref'] for x in plan['pages']]==['EXT01','EXT02','EXT03','EXT04','EXT05']
assert all(x['hint_ladder']['support_revealed_initially'] is False for x in plan['pages'])
assert all(x['primary_concept_ref'] not in x['supporting_concept_refs'] for x in plan['pages'])
assert all(x['core1_lesson_refs'] and all(y['learner_title'] for y in x['core1_lesson_refs']) for x in plan['pages'])

# Contract validation of the actual semantic product.
Draft202012Validator(load(D/'contracts'/'chemistry-core2-transfer-plan.schema.json')).validate(plan)
page_schema=Draft202012Validator(load(D/'contracts'/'chemistry-transfer-question-page.schema.json'))
hint_schema=Draft202012Validator(load(D/'contracts'/'chemistry-hint-ladder.schema.json'))
link_schema=Draft202012Validator(load(D/'contracts'/'chemistry-core1-core2-linkage.schema.json'))
sol_schema=Draft202012Validator(load(D/'contracts'/'chemistry-solution-verification.schema.json'))
concept_schema=Draft202012Validator(load(D/'contracts'/'chemistry-concept-segregation.schema.json'))
for p in plan['pages']:
    page_schema.validate(p); hint_schema.validate(p['hint_ladder']); sol_schema.validate(p['solution_route'])
    for l in p['core1_lesson_refs']: link_schema.validate(l)
    concept_schema.validate({'primary_concept_ref':p['primary_concept_ref'],'primary_capability_ref':p['primary_capability_ref'],'supporting_concept_refs':p['supporting_concept_refs'],'supporting_capability_refs':p['supporting_capability_refs']})

# 1 HINT_EQUALS_SOLUTION
bad=copy.deepcopy(plan); x=page(bad,'EXT01'); x['hint_ladder']['h2_rule_model_representation']=x['solution_route']['chemical_language_response']; redigest_page(x); redigest_plan(bad)
expect('HINT_EQUALS_SOLUTION',lambda:validate_plan(bad,*args))
# 2 H1_DISCLOSES_H3
bad=copy.deepcopy(plan); x=page(bad,'EXT02'); x['hint_ladder']['h1_notice']=x['hint_ladder']['h3_start']; redigest_page(x); redigest_plan(bad)
expect('H1_DISCLOSES_H3',lambda:validate_plan(bad,*args))
# 3 REASONING_ROUTE_EQUALS_HINT_COPY
bad=copy.deepcopy(plan); x=page(bad,'EXT03'); h=x['hint_ladder']; x['reasoning_route']=[h['h1_notice'],h['h2_rule_model_representation'],h['h3_start']]; redigest_page(x); redigest_plan(bad)
expect('REASONING_ROUTE_EQUALS_HINT_COPY',lambda:validate_plan(bad,*args))
# 4 SOURCE_MC_OPTIONS_MISSING
bad=copy.deepcopy(plan); x=page(bad,'EXT01'); x['source_options']=x['source_options'][:-1]; redigest_page(x); redigest_plan(bad)
expect('SOURCE_MC_OPTIONS_MISSING',lambda:validate_plan(bad,*args))
# 5 SOURCE_STRUCTURE_OR_FIGURE_LOST
bad=copy.deepcopy(plan); x=page(bad,'EXT02'); x['visual_specs']=[v for v in x['visual_specs'] if v['visual_kind']!='SOURCE_FIGURE']; redigest_page(x); redigest_plan(bad)
expect('SOURCE_STRUCTURE_OR_FIGURE_LOST',lambda:validate_plan(bad,*args))
# 6 FORMULA_CHARGE_STATE_CONDITION_DRIFT
bad=copy.deepcopy(plan); x=page(bad,'EXT05'); x['source_stem']=x['source_stem'].replace('Cu²⁺','Cu⁺'); redigest_page(x); redigest_plan(bad)
expect('FORMULA_CHARGE_STATE_CONDITION_DRIFT',lambda:validate_plan(bad,*args))
# 7 GENERIC_WORKSPACE_IGNORES_CHEMISTRY_SHAPE
bad=copy.deepcopy(plan); x=page(bad,'EXT03'); x['workspace_spec']={'workspace_type':'GENERIC','fields':['________','________','________']}; redigest_page(x); redigest_plan(bad)
expect('GENERIC_WORKSPACE_IGNORES_CHEMISTRY_SHAPE',lambda:validate_plan(bad,*args))
# 8 OPAQUE_CORE1_LINK_ONLY
bad=copy.deepcopy(plan); x=page(bad,'EXT04'); x['core1_lesson_refs'][0]['learner_title']=x['core1_lesson_refs'][0]['lesson_id']; redigest_page(x); redigest_plan(bad)
expect('OPAQUE_CORE1_LINK_ONLY',lambda:validate_plan(bad,*args))
# 9 PRIMARY_SUPPORTS_NOT_DISTINGUISHED
bad=copy.deepcopy(plan); x=page(bad,'EXT01'); x['supporting_concept_refs'].append(x['primary_concept_ref']); redigest_page(x); redigest_plan(bad)
expect('PRIMARY_SUPPORTS_NOT_DISTINGUISHED',lambda:validate_plan(bad,*args))
# 10 MULTIPLE_PRIMARY_OWNERS
bad=copy.deepcopy(plan); bad['pages'].append(copy.deepcopy(bad['pages'][0])); redigest_plan(bad)
expect('MULTIPLE_PRIMARY_OWNERS',lambda:validate_plan(bad,*args))
# 11 HARD_BADGE_WITHOUT_DEEPER_REASONING_STRUCTURE
bad=copy.deepcopy(plan); badfamilies=copy.deepcopy(families); fam=next(f for f in badfamilies['families'] if f['family_id']=='PF-FORMULA_CHARGE_PARSE'); fam['reasoning_route_template']=fam['reasoning_route_template'][:3]; x=page(bad,'EXT01'); x['reasoning_route']=copy.deepcopy(fam['reasoning_route_template']); x['guide_demand_badge']['label']='DEEP'; redigest_page(x); redigest_plan(bad); badguide=copy.deepcopy(guide); badguide['thresholds']=[{'badge':'FOUNDATION','max_score':0},{'badge':'STANDARD','max_score':0},{'badge':'DEEP','max_score':100},{'badge':'VERY_DEEP','max_score':999}]
expect('HARD_BADGE_WITHOUT_DEEPER_REASONING_STRUCTURE',lambda:validate_plan(bad,corpus,external,bodies,core1,model,badfamilies,badguide,transfer,concepts,profile,primitives,notation))
# 12 GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC
bad=copy.deepcopy(plan); x=page(bad,'EXT03'); x['guide_demand_badge']['psychometric_claim']=True; redigest_page(x); redigest_plan(bad)
expect('GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC',lambda:validate_plan(bad,*args))
# 13 ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE
badcore=copy.deepcopy(core1); target=next(l for l in badcore['lessons'] if l.get('worked_example')); target['worked_example']['external_candidate_refs']=['EXT01']
expect('ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE',lambda:validate_plan(plan,corpus,external,bodies,badcore,model,families,guide,transfer,concepts,profile,primitives,notation))
# 14 SOLUTION_IS_ANSWER_ONLY
bad=copy.deepcopy(plan); x=page(bad,'EXT05'); x['solution_route']['reasoning_steps']=[]; redigest_page(x); redigest_plan(bad)
expect('SOLUTION_IS_ANSWER_ONLY',lambda:validate_plan(bad,*args))
# 15 SOURCE_LINK_MISSING_OR_WRONG
bad=copy.deepcopy(plan); x=page(bad,'EXT04'); x['source_link']='fixture://wrong'; redigest_page(x); redigest_plan(bad)
expect('SOURCE_LINK_MISSING_OR_WRONG',lambda:validate_plan(bad,*args))

again=build_plan(*copy.deepcopy(args))
assert json.dumps(plan,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-I required falsifiers = 15 PASS')
print('CHEMISTRY C-I eligible transfer placement = 5/5 PASS')
print('CHEMISTRY C-I H0/H1/H2/H3 separation = PASS')
print('CHEMISTRY C-I source fidelity and Core1 linkage = PASS')
print('CHEMISTRY C-I complete solution/verification = PASS')
print('CHEMISTRY C-I deterministic replay = PASS')
