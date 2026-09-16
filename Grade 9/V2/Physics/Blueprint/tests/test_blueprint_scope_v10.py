#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'))
from compile_scoped_evidence import ScopedEvidenceError,compile_scoped_evidence
from governor import route,route_scoped

def load(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def envelope():return load('fixtures/stress-tests/relative-motion-grade9-cbse.scope.v1.json')
def test_topic_route_remains_core2_first():assert route(load('topics/motion-in-a-plane.v1.json')['evidence'])['final_route']=='CORE2_FIRST'
def test_relative_motion_scoped_route_is_derived_from_target_evidence():
 r=compile_scoped_evidence(envelope());assert r['assessment_coverage']['state']=='VERIFIED_NO_TARGET_DEMAND';assert r['evidence']['metrics']['QE']['value']==0 and r['evidence']['metrics']['QR']['value']==0;d=route_scoped(r)['routing_decision'];assert d['final_route']=='CORE1_FIRST';assert d['matched_rule_id']=='ROUTE-C1-STRONG-SOURCE-SPARSE-QUESTIONS'
def test_cbse_request_without_repository_authority_is_held():assert compile_scoped_evidence(envelope())['curriculum_status']=='HELD_INSUFFICIENT_AUTHORITY'
def test_scoped_receipt_tamper_is_rejected():
 r=compile_scoped_evidence(envelope());r['evidence']['metrics']['QE']['value']=4
 try:route_scoped(r)
 except AssertionError as e:assert str(e).startswith('ROUTING_EVIDENCE_SCOPE_MISMATCH')
 else:raise AssertionError('TAMPERED_SCOPED_EVIDENCE_WAS_ROUTED')
def test_repository_assertion_is_executable_not_narrative():
 bad=deepcopy(envelope());bad['repository_assertions'][0]['contains_all'].append('TOKEN_THAT_DOES_NOT_EXIST')
 try:compile_scoped_evidence(bad)
 except ScopedEvidenceError as e:assert str(e).startswith('SCOPED_EVIDENCE_ASSERTION_FAILED')
 else:raise AssertionError('MISSING_REPOSITORY_EVIDENCE_DID_NOT_FAIL')
def main():
 tests=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
 for t in tests:t()
 print(f'Blueprint V10 scoped-evidence tests: PASS ({len(tests)} tests)')
if __name__=='__main__':main()
