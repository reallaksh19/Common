#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]; sys.path.insert(0,str(ROOT/'engine'))
from compile_scoped_evidence import compile_scoped_evidence
from governor import route_scoped
from compile_engineering_closure import compile_closure
from compile_domain_prerequisite_closure import compile_domain_prerequisite_closure
from compile_join import compile_join

def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(v:Any)->str:return 'sha256:'+hashlib.sha256(canonical(v)).hexdigest()
def load(rel):
 p=ROOT/rel
 if not p.exists():raise AssertionError('STRESS_TEST_REF_MISSING:'+rel)
 return json.loads(p.read_text(encoding='utf-8'))
def exists_ref(rel):return bool(rel and (ROOT/rel).exists())
def core(status,blockers=None):return {'status':status,'blockers':sorted(set(blockers or []))}

def compile_stress_test(request):
 Draft202012Validator(load('contracts/seven-core-stress-test-request.schema.json')).validate(request)
 envelope=load(request['scope_envelope_ref'])
 if int(request['grade'])!=int(envelope['grade']) or request['requested_curriculum']!=envelope['requested_curriculum']:raise AssertionError('STRESS_TEST_SCOPE_REQUEST_MISMATCH')
 scoped=compile_scoped_evidence(envelope); routing=route_scoped(scoped)['routing_decision']
 eng_request=load(request['engineering_request_ref']); eng_manifest=load(request['engineering_manifest_ref']); engineering=compile_closure(eng_request,eng_manifest)
 if set(scoped['required_gate_ids'])!=set(eng_manifest['required_gate_ids']):raise AssertionError('STRESS_TEST_SCOPE_ENGINEERING_GATE_MISMATCH')
 domain=compile_domain_prerequisite_closure(engineering,[load(r) for r in request['domain_authority_refs']]); join=compile_join(load(request['join_spec_ref']),assessment_coverage=scoped['assessment_coverage'])
 route_value=routing['final_route']; eng_ready=engineering['closure_status']=='READY'; semantic_present=scoped['evidence']['sources']['semantic_source']['availability']!='ABSENT'; curriculum_ready=scoped['curriculum_status']=='SUPPORTED_BY_REPOSITORY_AUTHORITY'; domain_ready=domain['closure_status']=='READY'; control_present=exists_ref(request.get('control_state_ref')); core1a_release=exists_ref(request.get('core1a_release_ref')); core1b_release=exists_ref(request.get('core1b_release_ref')); core2a_pool=exists_ref(request.get('core2a_legal_pool_ref')); exact_product=exists_ref(request.get('exact_product_ref')); coverage_state=scoped['assessment_coverage']['state']
 cores={}; cores['CORE0']=core('PASS_ROUTING_ONLY' if route_value!='BLOCK' else 'BLOCKED_ROUTING',[] if route_value!='BLOCK' else ['ROUTING_BLOCK'])
 b=[]
 if not eng_ready:b.append('TECHNICAL_ENGINEERING_NOT_READY')
 if not semantic_present:b.append('TARGET_SEMANTIC_AUTHORITY_ABSENT')
 if not curriculum_ready:b.append('G_DOMAIN_CURRICULUM_AUTHORITY_HELD')
 cores['CORE1']=core('PREPARED_NOT_RELEASED' if eng_ready and semantic_present else 'BLOCKED',b)
 b=[]
 if not eng_ready:b.append('TECHNICAL_ENGINEERING_NOT_READY')
 if not join['assimilation_ready']:b.append('JOIN_NOT_ASSIMILATION_READY')
 if not domain_ready:b.append('EXTERNAL_DOMAIN_PREREQUISITES_HELD')
 if not control_present:b.append('MISSING_GOVERNED_CONTROL_STATE')
 if not curriculum_ready:b.append('G_DOMAIN_CURRICULUM_AUTHORITY_HELD')
 cores['CORE1A']=core('READY_FOR_STAGE_MACHINE' if not b else 'BLOCKED_BEFORE_STAGE_RELEASE',b)
 cores['CORE1B']=core('READY_FOR_RUNTIME' if core1a_release and core1b_release else 'NOT_INSTANTIATED',[] if core1a_release and core1b_release else ['NO_RELEASED_CORE1A_AUTHORITY'])
 cores['CORE2']=core('HELD_VERIFIED_NO_TARGET_DEMAND') if coverage_state=='VERIFIED_NO_TARGET_DEMAND' else core('READY_FOR_CUSTODY') if coverage_state=='DEMANDS_PRESENT' else core('BLOCKED_COVERAGE_UNKNOWN',['TARGET_ASSESSMENT_COVERAGE_UNKNOWN'])
 core2_has_item=coverage_state=='DEMANDS_PRESENT'; cores['CORE2A']=core('READY_FOR_LEGAL_POOL' if core2_has_item and core2a_pool else 'NOT_INSTANTIATED_NO_LEGAL_ITEM',[] if core2_has_item and core2a_pool else ['NO_LEGAL_TARGET_ITEM']); cores['CORE2B']=core('READY_FOR_TRANSFER' if core2a_pool and core1b_release else 'NOT_INSTANTIATED_UPSTREAM',[] if core2a_pool and core1b_release else ['CORE2A_OR_CORE1B_RELEASE_MISSING'])
 downstream={'CCU':'READY' if core1a_release or core2a_pool else 'NOT_INSTANTIATED','CDAU':'READY' if (core1a_release and core1b_release) or core2a_pool else 'NOT_INSTANTIATED','SDU':'READY' if core1a_release else 'NOT_ISSUED','LAU':'READY' if core2a_pool else 'NOT_ISSUED','CONCEPT_TTU':'READY' if core1a_release else 'NOT_INSTANTIATED','PROBLEM_TTU':'READY' if core2a_pool else 'NOT_INSTANTIATED','PUBLICATION':'READY' if core1a_release and curriculum_ready and domain_ready else 'BLOCKED','HUMAN_REVIEW':'READY' if exact_product else 'NOT_RUN'}
 violations=[]; forbidden={'PASS_BY_NONFABRICATION','PASS_FAIL_CLOSED_DIFFERENTIATION'}
 for n,s in cores.items():
  if s['status'] in forbidden:violations.append('FORBIDDEN_SURROGATE_PASS_LABEL:'+n)
 if cores['CORE2A']['status']=='READY_FOR_LEGAL_POOL' and cores['CORE2']['status']!='READY_FOR_CUSTODY':violations.append('CORE2A_READY_WITHOUT_CORE2_CUSTODY')
 if cores['CORE2B']['status']=='READY_FOR_TRANSFER' and (not core2a_pool or not core1b_release):violations.append('CORE2B_READY_WITHOUT_REQUIRED_UPSTREAM')
 if downstream['PUBLICATION']=='READY' and not core1a_release:violations.append('PUBLICATION_READY_WITHOUT_CORE1A_RELEASE')
 if route_value=='CORE2_FIRST' and coverage_state=='VERIFIED_NO_TARGET_DEMAND' and scoped['scope_kind']!='TOPIC':violations.append('TARGET_ROUTE_REUSED_TOPIC_QUESTION_RICHNESS')
 receipt={'schema_version':'1.0.0','stress_test_id':request['stress_test_id'],'subject':'PHYSICS','grade':request['grade'],'requested_curriculum':request['requested_curriculum'],'scope':{'kind':scoped['scope_kind'],'ref':scoped['scope_ref'],'topic_id':scoped['topic_id'],'scope_digest':scoped['scope_digest'],'scoped_evidence_receipt_digest':scoped['receipt_digest']},'curriculum_status':scoped['curriculum_status'],'routing':{'target_route':route_value,'matched_rule_id':routing['matched_rule_id'],'scope_consistent':True},'engineering':{'closure_status':engineering['closure_status'],'closure_digest':engineering['closure_digest'],'gate_states':engineering['gate_states']},'domain_prerequisites':{'closure_status':domain['closure_status'],'closure_digest':domain['closure_digest'],'prerequisites':domain['prerequisites']},'join':{'join_status':join['join_status'],'assimilation_ready':join['assimilation_ready'],'assessment_coverage_state':coverage_state,'join_digest':join['join_digest']},'cores':cores,'downstream':downstream,'architecture_violations':sorted(set(violations)),'final_verdict':'STRESS_TEST_PASS' if not violations else 'STRESS_TEST_FAIL','receipt_digest':''}
 receipt['receipt_digest']=digest({k:v for k,v in receipt.items() if k!='receipt_digest'}); Draft202012Validator(load('contracts/seven-core-stress-test-receipt.schema.json')).validate(receipt); return receipt

def main():
 ap=argparse.ArgumentParser();ap.add_argument('request',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args();r=compile_stress_test(json.loads(a.request.read_text(encoding='utf-8')));t=json.dumps(r,indent=2,ensure_ascii=False)+'\n';a.out.write_text(t,encoding='utf-8') if a.out else print(t,end='')
if __name__=='__main__':main()
