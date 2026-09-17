#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'contracts' / 'physics-core1a-subtopic-bucket.schema.json').read_text(encoding='utf-8'))
REGISTRY = json.loads((ROOT / 'registry' / 'physics-core1a-motion-in-a-plane-sba-v1.json').read_text(encoding='utf-8'))
PROFILE = json.loads((ROOT / 'registry' / 'physics-core1a-motion-in-a-plane-sba22-20pct-v1.json').read_text(encoding='utf-8'))
TRANSFER = json.loads((ROOT / 'registry' / 'physics-core1a-motion-in-a-plane-sba22-transfer-v1.json').read_text(encoding='utf-8'))
MANIFEST = json.loads((ROOT / 'registry' / 'build-manifests' / 'M2D-SBA-22-v1.json').read_text(encoding='utf-8'))
POLICY = json.loads((ROOT / 'registry' / 'physics-core1a-publication-policy.json').read_text(encoding='utf-8'))
INDEX = json.loads((ROOT / 'registry' / 'physics-core1a-motion-in-a-plane-sba-publication-index-v1.json').read_text(encoding='utf-8'))

Draft202012Validator.check_schema(SCHEMA)
Draft202012Validator(SCHEMA).validate(PROFILE)

canonical = next(b for b in REGISTRY['buckets'] if b['bucket_id']=='M2D-SBA-22')
assert canonical['intrinsic_difficulty']=='D3'
assert canonical['source_basis']==['SRC-GPRACTICE']
assert canonical['core2_primary_questions']==['Q05','Q26']
assert canonical['prerequisite_buckets']==['M2D-SBA-03']

bucket = PROFILE['buckets'][0]
assert bucket['bucket_id']=='M2D-SBA-22'
assert bucket['core2_primary_questions']==['Q05','Q26']
p = bucket['profiles'][0]
assert p['prior_knowledge_pct']==20 and p['pathway']=='FOUNDATION_PATH'
assert len(p['learning_atoms'])==8
assert max(a['visual_stage_count'] for a in p['learning_atoms']) >= 5
assert {a['atom_id'] for a in p['learning_atoms']} == {f'M2D-SBA-22{c}' for c in 'ABCDEFGH'}
coverage={q['question_id']:q for q in p['core2_hint_coverage']}
assert set(coverage)=={'Q05','Q26'}
for q in coverage.values():
    assert q['release_prerequisite_buckets']==[]
    assert [r['rung'] for r in q['hint_rungs']]==['H1','H2','H3']
    assert all(r['pre_taught'] is True for r in q['hint_rungs'])

routine_schema={'type':'array','items':SCHEMA['$defs']['transferRoutine']}
Draft202012Validator(routine_schema).validate(TRANSFER['transfer_routines'])
routines={r['routine_id']:r for r in TRANSFER['transfer_routines']}
assert set(routines)=={'M2D-SBA-22-R1','M2D-SBA-22-R2'}
assert routines['M2D-SBA-22-R1']['core2_questions']==['Q05']
assert routines['M2D-SBA-22-R2']['core2_questions']==['Q26']
for r in routines.values():
    assert len(r['method_steps'])>=4
    assert r['independent_practice']['prompt'] and r['independent_practice']['answer_check']
    assert [h['rung'] for h in r['hint_ladder']]==['H1','H2','H3']
    assert len(r['readiness_checks'])>=4
    assert r['release_prerequisite_buckets']==[]

assert MANIFEST['primary_questions']==['Q05','Q26']
assert MANIFEST['question_load']=={'count':2,'class':'LOW','minimum_transfer_families':2}
assert {q['question_id'] for q in MANIFEST['question_release']}=={'Q05','Q26'}
assert all(q['status']=='RELEASED' for q in MANIFEST['question_release'])
assert set(MANIFEST['transfer_routines'])==set(routines)
assert MANIFEST['publication_plan']['independent_practice_policy']=='ATTEMPT_BEFORE_HINTS'
assert MANIFEST['publication_plan']['hint_delivery_policy']=='NEXT_PAGE'
assert MANIFEST['publication_plan']['readiness_gate_policy']=='RECOGNISE_REPRESENT_FIRST_MOVE_FINISH'
assert MANIFEST['phase_gates'][-1]['status'] in {'IN_PROGRESS','PASS'}
if MANIFEST['handoff']['status']=='COMPLETE':
    assert MANIFEST['phase_gates'][-1]['status']=='PASS'
    assert MANIFEST['qa']['ci_passed'] is True

rows={row['bucket_id']:row for row in INDEX['rows']}
assert rows['M2D-SBA-22']['core2_primary_questions']==['Q05','Q26']
assert rows['M2D-SBA-22']['core1a_teaching_home']==['PROJECTILE_TIMED_EVENTS']
assert rows['M2D-SBA-22']['origin']=='Level-I practice'
assert rows['M2D-SBA-22']['state'] in {'IN_PROGRESS','BUILT'}

page=POLICY['page']
assert page['page_section_heading_max_pt']<=16.0
assert page['long_page_heading_max_pt']<=14.5
assert POLICY['learner_ui']['professionalisation_may_not_remove_instructional_functions'] is True

notes=' '.join(MANIFEST['handoff']['notes']).lower()
assert 'level-i practice' in notes and 'timed-events theory section' in notes

print('SBA22 timed-event transfer and professional-lossless checks passed.')
