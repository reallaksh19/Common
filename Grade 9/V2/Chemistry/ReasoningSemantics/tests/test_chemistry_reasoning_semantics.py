#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path.insert(0,str(D/'engine'))
from build_chemistry_reasoning_semantics import build_semantics

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError(f'expected {code}')
S=CHEM/'AssessmentScope'/'registry'; R=D/'registry'
source=load(S/'chemistry-source-obligation-ledger.json'); questions=load(S/'chemistry-question-capability-bindings.json')
families=load(R/'chemistry-problem-family-registry.json'); roles=load(R/'chemistry-reasoning-role-registry.json'); badges=load(R/'chemistry-guide-demand-badge-policy.json')
def run(f=None,q=None,b=None): return build_semantics(copy.deepcopy(source),copy.deepcopy(q if q is not None else questions),copy.deepcopy(f if f is not None else families),copy.deepcopy(roles),copy.deepcopy(b if b is not None else badges))
bundle=run()
assert bundle['summary']=={'source_record_count':12,'question_record_count':17,'eligible_question_count':14,'reasoning_route_is_hint_independent':True,'difficulty_scalar_is_not_authority':True}
for rec in bundle['question_semantics']:
    if rec['scope_status']=='ELIGIBLE_IN_SCOPE':
        assert rec['guide_demand_badge'] in {'FOUNDATION','STANDARD','DEEP','VERY_DEEP'}
        assert rec['reasoning_route']['learner_support_independent'] is True
        assert rec['verification_route']['status']=='CLOSED'
# 1 REASONING_ROUTE_EQUALS_HINT_COPY
bad=copy.deepcopy(families); bad['families'][0]['reasoning_route_template']=['H1_NOTICE']; expect('REASONING_ROUTE_EQUALS_HINT_COPY',lambda:run(f=bad))
# 2 REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY
bad=copy.deepcopy(families); bad['families'][0]['reasoning_route_template']=['SOLUTION_SUMMARY']; expect('REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY',lambda:run(f=bad))
# 3 DIFFICULTY_UNEXPLAINED_SCALAR
bad=copy.deepcopy(badges); bad['prohibited_bases']=['SOURCE_DIFFICULTY_ONLY']; expect('DIFFICULTY_UNEXPLAINED_SCALAR',lambda:run(b=bad))
# 4 HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE
bad=copy.deepcopy(families); f=next(x for x in bad['families'] if x['family_id']=='PF-FORMULA_CHARGE_PARSE'); f['reasoning_route_template']=['READ_GIVEN','PARSE_FORMULA_OR_EQUATION','VERIFY_RESULT']; f['demand_defaults']={k:3 for k in ['representation_translation','chemical_entity_tracking','formula_charge_parsing','condition_exception_handling','conservation_reasoning','reaction_process_reasoning','classification_discrimination','experimental_inference','structure_recognition','hidden_condition_load','reasoning_chain_length','concept_combination','quantitative_execution_load','verification_demand','time_pressure']}; expect('HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE',lambda:run(f=bad))
# 5 PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY
bad=copy.deepcopy(families); bad['question_family_aliases'].pop('QF-FORMULA-PARSING'); bad['capability_family_defaults'].pop('CAP-PARSE-ION-CHARGE',None); bad['capability_family_defaults'].pop('CAP-READ-FORMULA',None); expect('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',lambda:run(f=bad))
# 6 CONDITION_EXCEPTION_ROUTE_MISSING
bad=copy.deepcopy(questions); next(x for x in bad['bindings'] if x['item_ref']=='CQ07')['conditions_exceptions']=[]; expect('CONDITION_EXCEPTION_ROUTE_MISSING',lambda:run(q=bad))
# 7 VERIFICATION_ROUTE_MISSING
bad=copy.deepcopy(families); next(x for x in bad['families'] if x['family_id']=='PF-FORMULA_CHARGE_PARSE')['verification_route']=[]; expect('VERIFICATION_ROUTE_MISSING',lambda:run(f=bad))
# 8 MACRO_PARTICLE_SYMBOLIC_TRANSLATION_COLLAPSED
bad=copy.deepcopy(questions); next(x for x in bad['bindings'] if x['item_ref']=='CQ02')['representation_levels']=['SYMBOLIC']; expect('MACRO_PARTICLE_SYMBOLIC_TRANSLATION_COLLAPSED',lambda:run(q=bad))
# 9 CONSERVATION_REQUIREMENT_DROPPED
bad=copy.deepcopy(questions); next(x for x in bad['bindings'] if x['item_ref']=='CQ03')['conservation_obligations']=[]; expect('CONSERVATION_REQUIREMENT_DROPPED',lambda:run(q=bad))
# 10 EXPERIMENTAL_OBSERVATION_AND_CLAIM_COLLAPSED
bad=copy.deepcopy(families); next(x for x in bad['families'] if x['family_id']=='PF-EVIDENCE_TO_CLAIM')['entity_roles']=['OBSERVATION']; expect('EXPERIMENTAL_OBSERVATION_AND_CLAIM_COLLAPSED',lambda:run(f=bad))
# 11 STRUCTURE_DEPENDENCY_DROPPED
bad=copy.deepcopy(families); next(x for x in bad['families'] if x['family_id']=='PF-STRUCTURE_SITE_REASONING')['representation_requirements']=[]; expect('STRUCTURE_DEPENDENCY_DROPPED',lambda:run(f=bad))
# 12 REAGENT_MEMORIZATION_REPLACES_EQUATION_REASONING
bad=copy.deepcopy(families); next(x for x in bad['families'] if x['family_id']=='PF-AGENT_ROLE_ASSIGNMENT')['transfer_boundaries']=['use familiar reagent names']; expect('REAGENT_MEMORIZATION_REPLACES_EQUATION_REASONING',lambda:run(f=bad))
again=run(); assert json.dumps(bundle,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-D required falsifiers = 12 PASS')
print('CHEMISTRY C-D baseline = 12 source + 17 question semantic records')
print('CHEMISTRY C-D eligible question routes = 14')
print('CHEMISTRY C-D deterministic replay = PASS')
