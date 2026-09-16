#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'))
from compile_scoped_evidence import ScopedEvidenceError,compile_scoped_evidence,resolve_curriculum_binding
from governor import route,route_scoped

def load(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def envelope():return load('fixtures/stress-tests/relative-motion-grade9-cbse.scope.v1.json')
def test_topic_route_remains_core2_first():assert route(load('topics/motion-in-a-plane.v1.json')['evidence'])['final_route']=='CORE2_FIRST'
def test_relative_motion_scoped_route_is_derived_from_target_evidence():
 r=compile_scoped_evidence(envelope());assert r['assessment_coverage']['state']=='VERIFIED_NO_TARGET_DEMAND';assert r['evidence']['metrics']['QE']['value']==0 and r['evidence']['metrics']['QR']['value']==0;d=route_scoped(r)['routing_decision'];assert d['final_route']=='CORE1_FIRST';assert d['matched_rule_id']=='ROUTE-C1-STRONG-SOURCE-SPARSE-QUESTIONS'
def test_cbse_request_without_repository_authority_is_held():
 r=compile_scoped_evidence(envelope());assert r['curriculum_status']=='HELD_INSUFFICIENT_AUTHORITY';assert r['curriculum_binding']['state']=='UNBOUND';assert r['curriculum_binding']['binding_id'] is None
def test_arbitrary_curriculum_ref_cannot_authorize_scope_without_exact_binding():
 bad=deepcopy(envelope());bad['curriculum_authority_refs']=['Grade 9/V2/Physics/Blueprint/engineering-gates/motion-in-2d/PHY-M2D-RELATIVE-VELOCITY.v3.json']
 r=compile_scoped_evidence(bad);assert r['curriculum_status']=='HELD_INSUFFICIENT_AUTHORITY';assert r['curriculum_binding']['state']=='UNBOUND'
def test_exact_binding_rejects_existing_file_that_is_not_curriculum_authority_record():
 e=deepcopy(envelope());ref='Grade 9/V2/Physics/Blueprint/engineering-gates/motion-in-2d/PHY-M2D-RELATIVE-VELOCITY.v3.json';e['curriculum_authority_refs']=[ref]
 registry={'schema_version':'1.0.0','registry_id':'PHYSICS-CURRICULUM-SCOPE-BINDINGS-V1','subject':'PHYSICS','selector_semantics':'EXACT_GRADE_CURRICULUM_SCOPE_AND_GATE_SET','bindings':[{'binding_id':'PHY-CURR-BIND-SYNTHETIC-V1','grade':9,'curriculum':'CBSE','scope_kind':'SUBTOPIC','scope_ref':'PHY-M2D-RELATIVE-VELOCITY','required_gate_ids':['PHY-M2D-RELATIVE-VELOCITY'],'classification':'CURRICULUM_REQUIRED','authority_refs':[ref],'state':'CONFIRMED'}]}
 try:resolve_curriculum_binding(e,registry)
 except ScopedEvidenceError as x:assert str(x).startswith('SCOPED_EVIDENCE_CURRICULUM_AUTHORITY_RECORD_INVALID')
 else:raise AssertionError('NON_CURRICULUM_JSON_AUTHORIZED_EXACT_BINDING')
def test_semantic_curriculum_authority_record_must_match_exact_scope_and_gate_set():
 ref='Grade 9/V2/Physics/Blueprint/provenance/curriculum/PHY-CURR-AUTH-CBSE-G9-WORK-ENERGY-2026-V1.json'
 e={'requested_curriculum':'CBSE','grade':9,'scope_kind':'SUBTOPIC','scope_ref':'PHY-WEP-G9-ENERGY-ACCOUNTING-CONSERVATION','required_gate_ids':['PHY-WORK-ENERGY-POWER','PHY-ENERGY-CONSERVATION-LAW'],'curriculum_authority_refs':[ref]}
 binding={'binding_id':'PHY-CURR-BIND-WEP-G9-CBSE-V1','grade':9,'curriculum':'CBSE','scope_kind':'SUBTOPIC','scope_ref':'PHY-WEP-G9-ENERGY-ACCOUNTING-CONSERVATION','required_gate_ids':['PHY-WORK-ENERGY-POWER','PHY-ENERGY-CONSERVATION-LAW'],'classification':'CURRICULUM_REQUIRED','authority_refs':[ref],'state':'CONFIRMED'}
 registry={'schema_version':'1.0.0','registry_id':'PHYSICS-CURRICULUM-SCOPE-BINDINGS-V1','subject':'PHYSICS','selector_semantics':'EXACT_GRADE_CURRICULUM_SCOPE_AND_GATE_SET','bindings':[binding]}
 bound=resolve_curriculum_binding(e,registry);assert bound['state']=='BOUND_CONFIRMED';assert bound['binding_id']=='PHY-CURR-BIND-WEP-G9-CBSE-V1'
 mutated=deepcopy(e);mutated['required_gate_ids']=['PHY-WORK-ENERGY-POWER'];assert resolve_curriculum_binding(mutated,registry)['state']=='UNBOUND'
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
