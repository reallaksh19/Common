#!/usr/bin/env python3
import importlib.util, json
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
for name in ['chemistry-promoted-pck.schema.json','chemistry-core1-study-plan.schema.json','chemistry-core1-lesson.schema.json','chemistry-core-appendix-contract.schema.json']:
    Draft202012Validator.check_schema(load(D/'contracts'/name))
spec=importlib.util.spec_from_file_location('pck',D/'registry'/'chemistry_promoted_pck.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); registry=mod.build_registry()
Draft202012Validator(load(D/'contracts'/'chemistry-promoted-pck.schema.json')).validate(registry)
families={a['family'] for a in registry['assets']}
required={'MACRO_PARTICLE_SYMBOLIC_TRANSLATION','FORMULA_ANATOMY_AND_CHARGE','SUBSCRIPT_COEFFICIENT_CHARGE_DISCRIMINATION','CONSERVATION_ATOM_CHARGE_SPECIES','RULE_PRIORITY_AND_EXCEPTION','OBSERVATION_EVIDENCE_CLAIM','REACTION_PROCESS_CLASSIFICATION','SPECIES_ROLE_AND_SPECTATOR','STRUCTURE_SITE_REASONING','PRACTICAL_METHOD_PROPERTY_LINK','CHEMICAL_VERIFICATION','MISCONCEPTION_MINIMAL_CONTRAST','FIRST_MOVE_DECISION_SUPPORT'}
assert required<=families
redox={'REDOX_OXIDATION_STATE_LANES','REDOX_SELF_OTHER_AGENT_LOGIC','REDOX_SPLIT_CONVERGE_TOPOLOGY'}
assert redox<=families and all(a['topic_scope_refs']==['REDOX'] for a in registry['assets'] if a['family'] in redox)
profile=load(D/'registry'/'chemistry-instructional-authoring-profile.json'); completeness=load(D/'registry'/'chemistry-core1-scope-completeness-policy.json'); problems=load(D/'registry'/'chemistry-problem-authoring-profile.json')
assert profile['external_transfer_policy']=='ORIGINAL_EXTERNAL_TRANSFER_IS_CORE2_ONLY'
assert completeness['required_appendices']==['A','B','C'] and completeness['handout_answers_forbidden'] is True
assert problems['required_source_class']=='NEW_AUTHORED_CORE1' and problems['problem_family_binding_required'] is True
import sys
sys.path.insert(0,str(D/'engine'))
from validate_chemistry_instructional_depth import load_helper_profile, validate_helper_profile, load_depth_profile
helper=load_helper_profile(); validate_helper_profile(helper); depth=load_depth_profile()
# Every promoted PCK family a lesson can select must have a learner-directed,
# actionable first move; otherwise the Core 1 helper falls back to author voice.
missing=sorted(families-set(helper['first_move_by_pck_family']))
assert not missing,missing
assert {'WRITE_RELATION','WRITE_SPECIES_OR_FORMULA','COUNT_FEATURE','CANCEL_UNIT','COMPARE_QUANTITY','TEST_DEFINITION','VERIFY_RESULT'}<=set(helper['helper_intent_classes'])
assert 'NON_ACTIONABLE_HINT' in helper['falsifiers']
roles={r['role'] for r in depth['required_spine_roles']}
assert {'CANONICAL_MODEL','ORDINARY_LANGUAGE_EXPLANATION','TECHNICAL_RECONSTRUCTION','WORKED_EXAMPLE','MISCONCEPTION_REPAIR','GUIDED_ATTEMPT','FADED_ATTEMPT','INDEPENDENT_ATTEMPT','CHEMICAL_VERIFICATION','TRANSFER'}<=roles
copy_titles=load(D/'registry'/'chemistry-learner-copy-titles.json')
assert copy_titles['resolution_policy']=='FAIL_CLOSED_NEVER_PRINT_INTERNAL_ROLE'
print('CHEMISTRY C-G contracts, promoted PCK and authoring profiles = PASS')
print('CHEMISTRY C-G helper-pedagogy profile = %d intent classes, %d per-family first moves PASS'%(len(helper['helper_intent_classes']),len(helper['first_move_by_pck_family'])))
print('CHEMISTRY C-G Core1 depth profile = %d spine roles PASS'%len(roles))
print('CHEMISTRY C-G learner-copy title registry = %d mapped roles PASS'%len(copy_titles['titles']))
