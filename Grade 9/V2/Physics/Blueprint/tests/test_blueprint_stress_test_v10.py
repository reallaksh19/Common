#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator,ValidationError
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'))
from compile_seven_core_stress_test import compile_stress_test

def load(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def request():return load('fixtures/stress-tests/relative-motion-grade9-cbse.request.v1.json')
def test_request_cannot_assert_final_verdict():
 r=request();r['final_verdict']='STRESS_TEST_PASS'
 try:Draft202012Validator(load('contracts/seven-core-stress-test-request.schema.json')).validate(r)
 except ValidationError:pass
 else:raise AssertionError('STRESS_REQUEST_ALLOWED_SELF_ASSERTED_VERDICT')
def test_relative_motion_stress_receipt_is_machine_derived():
 r=compile_stress_test(request());Draft202012Validator(load('contracts/seven-core-stress-test-receipt.schema.json')).validate(r);assert r['final_verdict']=='STRESS_TEST_PASS';assert r['routing']['target_route']=='CORE1_FIRST';assert r['join']['join_status']=='JOIN_READY_NO_CORE2_DEMAND';assert r['cores']['CORE2']['status']=='HELD_VERIFIED_NO_TARGET_DEMAND';assert r['cores']['CORE2A']['status']=='NOT_INSTANTIATED_NO_LEGAL_ITEM';assert r['cores']['CORE1A']['status']=='BLOCKED_BEFORE_STAGE_RELEASE';assert 'JOIN_NOT_ASSIMILATION_READY' not in r['cores']['CORE1A']['blockers'];assert 'MISSING_GOVERNED_CONTROL_STATE' in r['cores']['CORE1A']['blockers'];assert 'EXTERNAL_DOMAIN_PREREQUISITES_HELD' in r['cores']['CORE1A']['blockers'];assert r['downstream']['CCU']=='NOT_INSTANTIATED';assert r['downstream']['CDAU']=='NOT_INSTANTIATED';assert r['downstream']['SDU']=='NOT_ISSUED';assert r['downstream']['LAU']=='NOT_ISSUED';assert r['architecture_violations']==[]
def test_external_math_is_held_not_silently_promoted():
 r=compile_stress_test(request());rows={x['prerequisite_id']:x['status'] for x in r['domain_prerequisites']['prerequisites']};assert rows['MATH-GEO-2D']=='HELD_NO_DOMAIN_RECEIPT';assert rows['MATH-TRIG-RIGHT']=='HELD_NO_DOMAIN_RECEIPT';assert r['domain_prerequisites']['closure_status']=='HELD'
def test_no_surrogate_pass_labels_exist():
 r=compile_stress_test(request());s={v['status'] for v in r['cores'].values()};assert 'PASS_BY_NONFABRICATION' not in s and 'PASS_FAIL_CLOSED_DIFFERENTIATION' not in s
def main():
 tests=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
 for t in tests:t()
 print(f'Blueprint V10 seven-core stress tests: PASS ({len(tests)} tests)')
if __name__=='__main__':main()
