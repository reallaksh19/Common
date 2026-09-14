#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REG=ROOT/'registry'
load=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
sba=load(REG/'physics-core1a-motion-in-a-plane-sba-v1.json')
link=load(REG/'physics-core1a-core2-linkage.json')
audit=load(REG/'physics-core1a-motion-in-a-plane-sba23-source-audit-v1.json')
plan=load(REG/'physics-core1a-motion-in-a-plane-sba23-teaching-plan-v1.json')
manifest=load(REG/'build-manifests'/'M2D-SBA-23-v1.json')
pub=load(REG/'physics-core1a-motion-in-a-plane-sba-publication-index-v1.json')
state=load(REG/'physics-core1a-motion-in-a-plane-build-state-v1.json')
b=next(x for x in sba['buckets'] if x['bucket_id']=='M2D-SBA-23')
assert b['core2_primary_questions']==['Q15'] and b['core1a_homes']==['MOVING_LAUNCHER']
q=next(x for x in link['challenge_links'] if x['challenge_id']=='Q15')
assert q['core1a_concept_id']=='moving-launcher' and q['challenge_title']=='Moving launch source'
assert audit['release_decision']=='BLOCK' and audit['classification']=='SOURCE_EVIDENCE_INCOMPLETE'
assert audit['exact_source_body']['text'] is None and audit['exact_source_hint_ladder']['h1'] is None
assert plan['status']=='PROVISIONAL_TEACHING_MODEL_NOT_RELEASE_AUTHORITY'
assert len(plan['learning_atoms'])==8 and plan['core2_release']['Q15'].startswith('HELD_')
assert manifest['handoff']['advance_build_state'] is False
assert manifest['question_release'][0]['status']=='HELD_SOURCE_EVIDENCE_INCOMPLETE'
assert next(g for g in manifest['phase_gates'] if g['gate']=='G1_SOURCE_AND_CORE2_AUDIT')['status']=='BLOCKED'
assert next(g for g in manifest['phase_gates'] if g['gate']=='G4_CORE2_HINT_PRETEACH_AUDIT')['status']=='BLOCKED'
assert 'M2D-SBA-23' not in state['completed_active_buckets'] and state['next_active_bucket']=='M2D-SBA-23'
assert 'M2D-SBA-23' not in {r['bucket_id'] for r in pub['rows']}
print('SBA23 source-integrity gate: PASS (identity bound; release fails closed)')
