#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; P=R.parent/'Publication'
sys.path.insert(0,str(R/'engine')); from build_review_package import build
sys.path.insert(0,str(P/'engine')); from build_semantic_product import build as build_product
load=lambda p:json.loads(Path(p).read_text())
baseline=load(R/'fixtures/baseline_candidate.synthetic.json'); findings=load(R/'fixtures/ai_pre_review_findings.synthetic.json')
design=load(P/'fixtures/design_result.synthetic.json') if (P/'fixtures/design_result.synthetic.json').exists() else None
if design is None:
    raise SystemExit('reference review test requires generated design fixture via workflow')
product=build_product(design,load(Path(__file__).parents[2]/'Canonical/registry/diagnostic_probes.json'))
manifest={'artifact_sha256':'1'*64,'quality_states':{'PUBLICATION_ENGINEERING':'PASS','SUBJECT_CORRECTNESS':'PENDING','PEDAGOGY_USABILITY':'PENDING','VISUAL_USABILITY':'PENDING','BENCHMARK_COMPARATIVE_VALIDATION':'NOT_RUN'}}
pkg=build(baseline,findings,manifest,product); assert [f['status'] for f in pkg['findings'][:4]]==['RESOLVED']*4; assert pkg['findings'][4]['status']=='OBSERVED_HUMAN_REVIEW_REQUIRED'; assert not pkg['release_evidence_eligible']
def fail(fn):
    try: fn(); return False
    except Exception: return True
b=copy.deepcopy(baseline); b['artifact_sha256']='0'*64; assert fail(lambda:build(b,findings,manifest,product))
f=copy.deepcopy(findings); f[0]['review_class']='HUMAN'; assert fail(lambda:build(baseline,f,manifest,product))
m=copy.deepcopy(manifest); m['quality_states']['SUBJECT_CORRECTNESS']='PASS'; assert fail(lambda:build(baseline,findings,m,product))
p=copy.deepcopy(product); p5=next(x for x in p['content_items'] if x['content_id']=='PC05'); p5['metadata'].pop('table_headers'); assert next(x for x in build(baseline,findings,manifest,p)['findings'] if x['finding_id']=='PHY-R01')['status']=='OPEN'
p=copy.deepcopy(product); p8=next(x for x in p['content_items'] if x['content_id']=='PC08'); p8['metadata']['worked_trace_values']=[]; assert next(x for x in build(baseline,findings,manifest,p)['findings'] if x['finding_id']=='PHY-R02')['status']=='OPEN'
p=copy.deepcopy(product); p11=next(x for x in p['content_items'] if x['content_id']=='PC11'); p11['metadata']['support_level']=1; assert next(x for x in build(baseline,findings,manifest,p)['findings'] if x['finding_id']=='PHY-R03')['status']=='OPEN'
p=copy.deepcopy(product); p13=next(x for x in p['content_items'] if x['content_id']=='PC13'); p13['metadata']['numbers_only_change']=True; assert next(x for x in build(baseline,findings,manifest,p)['findings'] if x['finding_id']=='PHY-R04')['status']=='OPEN'
assert pkg['quality_states']['VISUAL_USABILITY']=='PENDING'
assert pkg['findings'][4]['status']!='RESOLVED'
assert all(f['artifact_sha256']==baseline['artifact_sha256'] for f in findings)
print('PHY-V2-06 review falsifiers = 10 PASS')
