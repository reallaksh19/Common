#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; REG=ROOT/'registry'
load=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
sba=load(REG/'physics-core1a-motion-in-a-plane-sba-v1.json')
link=load(REG/'physics-core1a-core2-linkage.json')
audit=load(REG/'physics-core1a-motion-in-a-plane-sba23-source-audit-v1.json')
plan=load(REG/'physics-core1a-motion-in-a-plane-sba23-teaching-plan-v1.json')
transfer=load(REG/'physics-core1a-motion-in-a-plane-sba23-transfer-v1.json')
manifest=load(REG/'build-manifests'/'M2D-SBA-23-v1.json')
pub=load(REG/'physics-core1a-motion-in-a-plane-sba-publication-index-v1.json')
state=load(REG/'physics-core1a-motion-in-a-plane-build-state-v1.json')
schema=load(ROOT/'contracts'/'physics-core1a-sba-build-manifest.schema.json'); Draft202012Validator(schema).validate(manifest)
b=next(x for x in sba['buckets'] if x['bucket_id']=='M2D-SBA-23')
assert b['core2_primary_questions']==['Q15'] and b['core1a_homes']==['MOVING_LAUNCHER']
q=next(x for x in link['challenge_links'] if x['challenge_id']=='Q15')
assert q['core1a_concept_id']=='moving-launcher' and q['challenge_title']=='Moving launch source'
assert audit['release_decision']=='BLOCK' and audit['classification']=='SOURCE_EVIDENCE_INCOMPLETE'
assert audit['exact_source_body']['text'] is None and audit['exact_source_solution']['text'] is None
assert audit['exact_source_hint_ladder']['h1'] is None and audit['exact_source_hint_ladder']['h2'] is None and audit['exact_source_hint_ladder']['h3'] is None
provenance=audit['cross_pr_provenance_checked']
assert provenance['pull_request']==343
assert provenance['source_scan_status']=='CHAT_PROVIDED_NOT_REDISTRIBUTED'
assert provenance['revised_core2_pdf_status']=='GENERATED_CONVERSATION_ARTIFACT_NOT_REPOSITORY_FILE'
assert provenance['repo_generator_status']=='CONTRACT_ONLY_CHAT_SOURCE_NOT_EMBEDDED'
assert provenance['usable_as_exact_q15_authority'] is False
assert 'cannot close G1 or G4' in provenance['finding']
assert 'active Physics authority branch' in audit['next_required_evidence']
assert plan['status']=='PROVISIONAL_TEACHING_MODEL_NOT_RELEASE_AUTHORITY'
assert len(plan['learning_atoms'])==8 and plan['core2_release']['Q15'].startswith('HELD_')
r=transfer['transfer_routines'][0]
assert r['routine_id']=='M2D-SBA-23-R1' and r['core2_questions']==['Q15']
assert 'not the exact Q15 H1/H2/H3 ladder' in transfer['purpose']
assert manifest['handoff']['status']=='BLOCKED' and manifest['question_release'][0]['status']=='HELD'
assert next(g for g in manifest['phase_gates'] if g['gate']=='G1_SOURCE_AND_CORE2_AUDIT')['status']=='BLOCKED'
assert next(g for g in manifest['phase_gates'] if g['gate']=='G4_CORE2_HINT_PRETEACH_AUDIT')['status']=='BLOCKED'
assert manifest['qa']['hint_preteach_complete'] is False and manifest['qa']['pdf_preflight_complete'] is False
assert 'M2D-SBA-23' not in state['completed_active_buckets'] and state['next_active_bucket']=='M2D-SBA-23'
assert 'M2D-SBA-23' not in {row['bucket_id'] for row in pub['rows']}
print('SBA23 source-integrity gate: PASS (identity bound; cross-PR provenance checked; canonical manifest remains held)')
