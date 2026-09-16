#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from copy import deepcopy
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'))
from compile_join import compile_join

def golden():return json.loads((ROOT/'fixtures/join/join-ready.json').read_text())
def zero_demand():return json.loads((ROOT/'fixtures/join/relative-motion-verified-no-demand.v1.json').read_text())
def coverage(state='VERIFIED_NO_TARGET_DEMAND'):return {'state':state,'matched_target_item_count':0,'scope_digest':'sha256:'+'1'*64,'corpus_digest':'sha256:'+'2'*64,'evidence_refs':['EVIDENCE-REF'],'unresolved_issues':[] if state=='VERIFIED_NO_TARGET_DEMAND' else ['Target coverage has not been established.']}
def assert_fails(spec,code,assessment_coverage=None):
 try:compile_join(spec,assessment_coverage=assessment_coverage)
 except AssertionError as e:assert str(e).startswith(code),str(e)
 else:raise AssertionError('EXPECTED_FAILURE:'+code)
def test_ready_join():
 p=compile_join(golden());assert p['join_status']=='JOIN_READY' and p['assimilation_ready'] is True and p['critical_conflicts']==[] and p['demand_claim_count']==2 and 'assessment_coverage' not in p
def test_schema_validates_golden():Draft202012Validator(json.loads((ROOT/'contracts/join-packet.schema.json').read_text())).validate(compile_join(golden()))
def test_required_contradiction_blocks():
 s=golden();s['reconciliations'][0]['status']='CONTRADICTED';s['reconciliations'][0]['unresolved_issues']=['Source and semantic claim disagree on the event condition.'];p=compile_join(s);assert p['join_status']=='JOIN_BLOCKED' and p['assimilation_ready'] is False
def test_nonblocking_unknown_is_hold_not_block():
 s=golden();s['reconciliations'][1]['status']='UNKNOWN';s['reconciliations'][1]['criticality']='NON_BLOCKING';s['reconciliations'][1]['unresolved_issues']=['Insufficient evidence.'];p=compile_join(s);assert p['join_status']=='JOIN_READY_WITH_HOLDS' and p['assimilation_ready'] is True
def test_every_demand_must_be_reconciled_exactly_once():
 s=golden();s['reconciliations']=s['reconciliations'][:1];assert_fails(s,'JOIN_DEMAND_COVERAGE_GAP');s=golden();s['reconciliations'].append(deepcopy(s['reconciliations'][0]));assert_fails(s,'JOIN_DUPLICATE_DEMAND_RECONCILIATION')
def test_unknown_knowledge_ref_fails():s=golden();s['reconciliations'][0]['knowledge_claim_refs'].append('K-NOT-DECLARED');assert_fails(s,'JOIN_UNKNOWN_KNOWLEDGE_REF')
def test_confirmed_requires_semantic_grounding():s=golden();s['reconciliations'][0]['knowledge_claim_refs']=[];assert_fails(s,'JOIN_SEMANTIC_GROUNDING_REQUIRED')
def test_ready_requires_assimilation_obligation():s=golden();s['reconciliations'][0]['assimilation_obligations']=[];assert_fails(s,'JOIN_ASSIMILATION_OBLIGATION_REQUIRED')
def test_unresolved_requires_issue_record():s=golden();s['reconciliations'][0]['status']='MISSING';s['reconciliations'][0]['unresolved_issues']=[];assert_fails(s,'JOIN_UNRESOLVED_ISSUE_REQUIRED')
def test_validation_session_is_mandatory():s=golden();s['validation_session_refs']=[];assert_fails(s,'JOIN_VALIDATION_SESSION_REQUIRED')
def test_digest_is_deterministic_under_reconciliation_order():
 a=golden();b=golden();b['reconciliations']=list(reversed(b['reconciliations']));assert compile_join(a)['join_digest']==compile_join(b)['join_digest']
def test_verified_zero_demand_is_ready_without_fabricating_demand():
 p=compile_join(zero_demand(),assessment_coverage=coverage());assert p['demand_claim_count']==0 and p['items']==[] and p['join_status']=='JOIN_READY_NO_CORE2_DEMAND' and p['assimilation_ready'] is True;Draft202012Validator(json.loads((ROOT/'contracts/join-packet.schema.json').read_text())).validate(p)
def test_zero_demand_without_coverage_proof_fails():assert_fails(zero_demand(),'JOIN_ASSESSMENT_COVERAGE_STATE_INVALID')
def test_unknown_coverage_blocks_not_passes():
 p=compile_join(zero_demand(),assessment_coverage=coverage('COVERAGE_UNKNOWN'));assert p['join_status']=='JOIN_BLOCKED' and p['assimilation_ready'] is False and p['critical_conflicts'][0]['status']=='UNKNOWN'
def test_demand_bearing_join_rejects_zero_demand_coverage():assert_fails(golden(),'JOIN_ASSESSMENT_COVERAGE_DEMAND_MISMATCH',coverage())
def main():
 ts=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
 for t in ts:t()
 print(f'Blueprint join tests: PASS ({len(ts)} tests)')
if __name__=='__main__':main()
