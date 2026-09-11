#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[
    str(D/'engine'),str(CHEM/'CoreAuthoring'/'engine'),str(CHEM/'AssessmentReview'/'engine'),
    str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine'),
    str(CHEM/'LearnerEvidence'/'engine'),str(CHEM/'LearnerStudy'/'engine')]
from build_chemistry_representations import build_bundle,validate_bundle,validate_registry,validate_notation,digest
from build_chemistry_core1 import build_plan,load_pck_registry
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
def redigest(b): b['bundle_digest']=''; b['bundle_digest']=digest(b,'bundle_digest'); return b
def primitive(reg,pid): return next(x for x in reg['primitives'] if x['primitive_id']==pid)

def build_upstream():
    A=CHEM/'AssessmentIntake'/'fixtures'; R=CHEM/'AssessmentReview'; S=CHEM/'AssessmentScope'; RS=CHEM/'ReasoningSemantics'; E=CHEM/'LearnerEvidence'; LS=CHEM/'LearnerStudy'; CA=CHEM/'CoreAuthoring'
    sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
    review_reg,manifest_digest=load_review_registry(R/'registry'/'chemistry-item-validity-registry.json')
    review=build_review(copy.deepcopy(sources),copy.deepcopy(questions),review_reg,load(R/'policies'/'chemistry-diagnostic-use-policy.json'),load(R/'registry'/'chemistry-qc-events.json'),registry_manifest_digest=manifest_digest)
    source_ledger=load(S/'registry'/'chemistry-source-obligation-ledger.json'); qbindings=load(S/'registry'/'chemistry-question-capability-bindings.json'); external=load(S/'registry'/'chemistry-external-corpus-classification.json'); authority=load(S/'authority'/'chemistry-canonical-authority.json')
    scope_bundle=build_scope(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(authority))
    semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),load(RS/'registry'/'chemistry-problem-family-registry.json'),load(RS/'registry'/'chemistry-reasoning-role-registry.json'),load(RS/'registry'/'chemistry-guide-demand-badge-policy.json'))
    obs=load(E/'registry'/'chemistry-observation-code-registry.json'); diag=load(E/'registry'/'chemistry-diagnostic-policy.json')
    no_attempt=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(obs),copy.deepcopy(diag))
    study_scope=derive_study_scope(copy.deepcopy(scope_bundle),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
    model=build_model(copy.deepcopy(study_scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(no_attempt),load(LS/'registry'/'chemistry-treatment-policy.json'),'CHEM-C-H-UPSTREAM')
    pck=load_pck_registry(); profile=load(CA/'registry'/'chemistry-instructional-authoring-profile.json'); completeness=load(CA/'registry'/'chemistry-core1-scope-completeness-policy.json'); problems=load(CA/'registry'/'chemistry-problem-authoring-profile.json')
    plan=build_plan(copy.deepcopy(model),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(profile),copy.deepcopy(completeness),copy.deepcopy(problems),'CHEM-C-H-CORE1')
    return plan,model

plan,model=build_upstream()
registry=load(D/'registry'/'chemistry-teaching-primitive-registry.json'); page_profile=load(D/'registry'/'chemistry-page-intent-profile.json'); notation=load(D/'registry'/'chemistry-notation-render-contract.json')
bundle=build_bundle(copy.deepcopy(plan),copy.deepcopy(model),copy.deepcopy(registry),copy.deepcopy(page_profile),copy.deepcopy(notation))
Draft202012Validator(load(D/'contracts'/'chemistry-representation-spec.schema.json')).validate(bundle['representations'][0])
for x in bundle['representations']: Draft202012Validator(load(D/'contracts'/'chemistry-representation-spec.schema.json')).validate(x)
assert bundle['summary']['renderer_invention_allowed'] is False
assert {x['capability_ref'] for x in bundle['representations']}=={x['capability_ref'] for x in model['capability_records']}

# 1 DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS
bad=copy.deepcopy(bundle); bad['representations'][0]['decorative']=True; redigest(bad)
expect('DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 2 VISUAL_WITHOUT_INSTRUCTIONAL_JOB
bad=copy.deepcopy(bundle); bad['representations'][0]['instructional_job']=''; redigest(bad)
expect('VISUAL_WITHOUT_INSTRUCTIONAL_JOB',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 3 VISUAL_WITHOUT_CAPABILITY_BINDING
bad=copy.deepcopy(bundle); bad['representations'][0]['capability_ref']='CAP-NOT-AUTHORIZED'; redigest(bad)
expect('VISUAL_WITHOUT_CAPABILITY_BINDING',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 4 RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING
bad=copy.deepcopy(bundle); bad['representations'][0]['chemical_entities']=bad['representations'][0]['chemical_entities']+['INVENTED_SPECIES']; redigest(bad)
expect('RENDERER_INVENTS_UNDECLARED_CHEMISTRY_MEANING',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 5 FORMULA_OR_CHARGE_DRIFTS_FROM_SEMANTIC_DATA
bad=copy.deepcopy(bundle); bad['representations'][0]['notation_tokens']=['Fe3+']; redigest(bad)
expect('FORMULA_OR_CHARGE_DRIFTS_FROM_SEMANTIC_DATA',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 6 PARTICLE_VIEW_IMPLIES_WRONG_COMPOSITION
badr=copy.deepcopy(registry); primitive(badr,'PARTICLE_MODEL_VIEW')['renderer_constraints'].remove('COMPOSITION_FROM_SOURCE_ONLY')
expect('PARTICLE_VIEW_IMPLIES_WRONG_COMPOSITION',lambda:validate_registry(badr))
# 7 STRUCTURE_SITE_IDENTITY_LOST
badr=copy.deepcopy(registry); primitive(badr,'STRUCTURE_SITE_ANNOTATION')['renderer_constraints'].remove('SITE_IDS_STABLE')
expect('STRUCTURE_SITE_IDENTITY_LOST',lambda:validate_registry(badr))
# 8 CONDITION_EXCEPTION_REQUIRED_BUT_NOT_VISIBLE
cap=next(r['capability_ref'] for r in model['capability_records'] if r['condition_exception_obligations'])
bad=copy.deepcopy(bundle); bad['representations']=[x for x in bad['representations'] if not (x['capability_ref']==cap and x['primitive_id']=='CONDITION_EXCEPTION_GATE')]; redigest(bad)
expect('CONDITION_EXCEPTION_REQUIRED_BUT_NOT_VISIBLE',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 9 APPARATUS_VIEW_INVENTS_OBSERVATION
badr=copy.deepcopy(registry); primitive(badr,'APPARATUS_METHOD_FLOW')['renderer_constraints'].remove('NO_INVENTED_OBSERVATION')
expect('APPARATUS_VIEW_INVENTS_OBSERVATION',lambda:validate_registry(badr))
# 10 CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED
cap=next(l['capability_ref'] for l in plan['lessons'] if l['lesson_mode']=='FULL_LEARNING' and l.get('misconception_repair'))
bad=copy.deepcopy(bundle); bad['representations']=[x for x in bad['representations'] if not (x['capability_ref']==cap and x['primitive_id']=='MINIMAL_CHEMISTRY_CONTRAST')]; redigest(bad)
expect('CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED',lambda:validate_bundle(bad,plan,model,registry,page_profile,notation))
# 11 ASCII_FALLBACK_MAKES_CHARGE_AMBIGUOUS
badn=copy.deepcopy(notation); badn['ascii_fallback_policy']='ALLOW_FLAT_ASCII'
expect('ASCII_FALLBACK_MAKES_CHARGE_AMBIGUOUS',lambda:validate_notation(badn))

# Deterministic replay and semantic trace closure.
again=build_bundle(copy.deepcopy(plan),copy.deepcopy(model),copy.deepcopy(registry),copy.deepcopy(page_profile),copy.deepcopy(notation))
assert json.dumps(bundle,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
for s in bundle['representations']:
    assert s['instructional_job'] and s['attention_target'] and s['learner_action_expected'] and s['accessibility_text']
    assert s['source_semantic_data']['source_obligation_refs'] or s['source_semantic_data']['assessment_question_refs']
print('CHEMISTRY C-H required falsifiers = 11 PASS')
print('CHEMISTRY C-H semantic teaching primitives = PASS')
print('CHEMISTRY C-H source-bound representation trace = PASS')
print('CHEMISTRY C-H notation safety = PASS')
print('CHEMISTRY C-H deterministic replay = PASS')
