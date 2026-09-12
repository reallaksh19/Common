#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
ENG=D/'engine'
sys.path.insert(0,str(ENG))
from build_chemistry_representations import validate_registry, validate_notation
from bind_chemistry_visual_obligations import validate_taxonomy

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

schema=load(D/'contracts'/'chemistry-representation-spec.schema.json')
Draft202012Validator.check_schema(schema)
registry=load(D/'registry'/'chemistry-teaching-primitive-registry.json')
profile=load(D/'registry'/'chemistry-page-intent-profile.json')
notation=load(D/'registry'/'chemistry-notation-render-contract.json')
by=validate_registry(registry); validate_notation(notation)
required=set(registry['required_primitive_ids'])
assert required<=set(by)
assert profile['subject']=='CHEMISTRY' and notation['subject']=='CHEMISTRY'
assert set(profile['conditional_primitives'].values())<=set(by)
for cap,pids in profile['primary_primitives_by_capability'].items():
    assert pids, cap
    for pid in pids:
        assert pid in by,(cap,pid)
        assert cap in by[pid]['capability_refs'],(cap,pid)
taxonomy=load(D.parent/'AssessmentScope'/'registry'/'chemistry-capability-taxonomy.json')
authority=load(D.parent/'AssessmentScope'/'authority'/'chemistry-canonical-authority.json')
instructional=load(D.parent/'CoreAuthoring'/'registry'/'chemistry-instructional-authoring-profile.json')
obligation=load(D/'registry'/'chemistry-visual-obligation-profile.json')
validate_taxonomy(taxonomy,authority,registry,profile,instructional)
assert obligation['subject']=='CHEMISTRY'
assert obligation['renderer_invention_allowed'] is False and obligation['renderer_selection_forbidden'] is True
assert obligation['global_realization_is_not_local_compliance'] is True
assert obligation['unrealized_policy']=='RECORD_AS_UNREALIZED_NEVER_SUBSTITUTE_TEXT_OR_INVENTED_VALUE'
assert set(obligation['obligation_scopes'])=={'CORE1_LESSON','CORE2_QUESTION'}
assert {'visual_obligations_required','visual_obligations_realized','questions_requiring_visual','questions_with_required_visual'}==set(obligation['candidate_counters'])
assert {'VISUAL_OBLIGATION_MISSING','WRONG_VISUAL_FAMILY','TEXT_ONLY_WHEN_VISUAL_REQUIRED'}<=set(obligation['falsifiers'])
pending={p['primitive_id'] for p in registry['primitives'] if p['renderer_realization']=='RENDERER_PENDING_FAIL_CLOSED'}
assert pending and pending<=set(by)
print('CHEMISTRY C-H representation schema = PASS')
print('CHEMISTRY C-H primitive registry = %d primitives (%d renderer-pending, fail closed) PASS'%(len(registry['primitives']),len(pending)))
print('CHEMISTRY C-H page-intent profile = PASS')
print('CHEMISTRY C-H notation contract = PASS')
print('CHEMISTRY capability taxonomy = %d capabilities PASS'%len(taxonomy['capabilities']))
print('CHEMISTRY C-H visual-obligation profile = PASS')
