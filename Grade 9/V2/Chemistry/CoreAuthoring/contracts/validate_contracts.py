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
print('CHEMISTRY C-G contracts, promoted PCK and authoring profiles = PASS')
