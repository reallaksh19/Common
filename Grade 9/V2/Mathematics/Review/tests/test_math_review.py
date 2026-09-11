#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'engine'))
from build_review_package import build, EXPECTED_QUALITY

def load(n): return json.loads((ROOT/'fixtures'/n).read_text())
baseline=load('baseline_candidate.synthetic.json'); findings=load('ai_pre_review_findings.synthetic.json'); plan=load('revision_plan.synthetic.json'); policy=load('review_policy.synthetic.json')
product=json.loads(Path('/tmp/revised_product.json').read_text()) if Path('/tmp/revised_product.json').exists() else {
 'content_items':[
  {'content_id':'C02','body':['Equation: 3x + 5 = 23','Proposed move: 3x = 18']},
  {'content_id':'C04','body':['Move A: legal','Move B: illegal']},
  {'content_id':'C11','body':['Expansion A: x^2 - 6x + 9','Expansion B: x^2 + 9']},
  {'content_id':'C17','body':['Solve 7 - 3(2x - 1) = 2x + 12.','When finished, stop.']}
 ]
}
page_map={'page_count':5,'content_placements':[{'content_ref':'C14','page':5},{'content_ref':'C15','page':3}]}
manifest={'artifact_sha256':'a'*64,'quality_states':copy.deepcopy(EXPECTED_QUALITY)}
r1=build(baseline,findings,plan,policy,manifest,product,page_map); r2=build(baseline,findings,plan,policy,manifest,product,page_map)
assert json.dumps(r1,sort_keys=True)==json.dumps(r2,sort_keys=True)
assert r1[2]['human_review_evidence']=={'SUBJECT':0,'PEDAGOGY':0,'VISUAL':0}
assert r1[2]['quality_states']['SUBJECT_CORRECTNESS']=='PENDING'
assert r1[2]['quality_states']['PEDAGOGY_USABILITY']=='PENDING'
assert r1[2]['quality_states']['VISUAL_USABILITY']=='PENDING'
assert r1[2]['quality_states']['BENCHMARK_COMPARATIVE_VALIDATION']=='NOT_RUN'

def item(prod, content_id):
    return next(x for x in prod['content_items'] if x['content_id']==content_id)

def must_fail(mutator):
    b=copy.deepcopy(baseline); f=copy.deepcopy(findings); p=copy.deepcopy(plan); pol=copy.deepcopy(policy); m=copy.deepcopy(manifest); prod=copy.deepcopy(product); pm=copy.deepcopy(page_map)
    mutator(b,f,p,pol,m,prod,pm)
    try: build(b,f,p,pol,m,prod,pm); raise AssertionError('falsifier accepted')
    except ValueError: pass
must_fail(lambda b,f,p,pol,m,prod,pm: f['findings'][0].update(artifact_sha256='b'*64))
must_fail(lambda b,f,p,pol,m,prod,pm: p['decisions'].__setitem__(slice(None),[d for d in p['decisions'] if d['finding_id']!='MATH-RF-001']))
must_fail(lambda b,f,p,pol,m,prod,pm: m['quality_states'].__setitem__('SUBJECT_CORRECTNESS','PASS'))
must_fail(lambda b,f,p,pol,m,prod,pm: item(prod,'C02').__setitem__('body',['No concrete move']))
must_fail(lambda b,f,p,pol,m,prod,pm: item(prod,'C17').__setitem__('body',['Solve x=1 and check it']))
must_fail(lambda b,f,p,pol,m,prod,pm: pm.__setitem__('page_count',6))
must_fail(lambda b,f,p,pol,m,prod,pm: next(x for x in pm['content_placements'] if x['content_ref']=='C15').__setitem__('page',5))
must_fail(lambda b,f,p,pol,m,prod,pm: pol['benchmark_inputs'].append('PR #156'))
print('MATH-V2-06 review falsifiers = 8 PASS')
