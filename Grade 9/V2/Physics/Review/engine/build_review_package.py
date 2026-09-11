#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
load=lambda p:json.loads(Path(p).read_text())
sha=lambda o:hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def check(product,cid):
    return next(x for x in product['content_items'] if x['content_id']==cid)

def build(baseline,findings,revised_manifest,revised_product):
    if baseline['artifact_sha256']!='9aa9638bede5810087829eb0a8f7762b3dd201974f20c3389479e9bb2c72a1ee':
        raise ValueError('wrong review baseline')
    if any(f['artifact_sha256']!=baseline['artifact_sha256'] or f['review_class']!='AI_PRE_REVIEW' for f in findings):
        raise ValueError('finding not bound to exact AI_PRE_REVIEW baseline')
    p5=check(revised_product,'PC05'); p8=check(revised_product,'PC08'); p9=check(revised_product,'PC09'); p10=check(revised_product,'PC10'); p11=check(revised_product,'PC11'); p13=check(revised_product,'PC13'); p14=check(revised_product,'PC14')
    evidence={
      'PHY-R01': len(p5['metadata'].get('table_headers',[]))==4 and len(p5['metadata'].get('table_rows',[]))>=2,
      'PHY-R02': p8['metadata'].get('state_handoff_explicit') is True and len(p8['metadata'].get('worked_trace_values',[]))>=3,
      'PHY-R03': [p9['metadata'].get('support_level'),p10['metadata'].get('support_level'),p11['metadata'].get('support_level')]==[2,1,0] and p11['metadata'].get('conceptual_hints')==[] and len(p11['body'])>=3,
      'PHY-R04': p13['metadata'].get('numbers_only_change') is False and len(p13['metadata'].get('structural_changes',[]))>=3 and p14['metadata'].get('fresh_task') is True and len(p14['body'])>=3,
      'PHY-R05': False
    }
    outfind=[]
    for f in findings:
        g=dict(f)
        g['status']='RESOLVED' if evidence[f['finding_id']] else ('OBSERVED_HUMAN_REVIEW_REQUIRED' if f['finding_id']=='PHY-R05' else 'OPEN')
        outfind.append(g)
    q=revised_manifest['quality_states']
    if any(q[x]!='PENDING' for x in ('SUBJECT_CORRECTNESS','PEDAGOGY_USABILITY','VISUAL_USABILITY')):
        raise ValueError('AI pre-review cannot promote human quality gates')
    seed={'baseline':baseline['artifact_sha256'],'revised':revised_manifest['artifact_sha256'],'findings':outfind}
    return {'schema_version':'1.0.0','review_package_id':'PHY-REVIEW-'+sha(seed)[:14].upper(),'baseline_artifact_sha256':baseline['artifact_sha256'],'revised_artifact_sha256':revised_manifest['artifact_sha256'],'review_class':'AI_PRE_REVIEW','findings':outfind,'quality_states':q,'release_evidence_eligible':False}

def main():
    a=argparse.ArgumentParser(); a.add_argument('--baseline',required=True); a.add_argument('--findings',required=True); a.add_argument('--revised-manifest',required=True); a.add_argument('--revised-product',required=True); a.add_argument('--out',required=True); x=a.parse_args()
    r=build(load(x.baseline),load(x.findings),load(x.revised_manifest),load(x.revised_product)); Path(x.out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'review_package_id':r['review_package_id'],'release_evidence_eligible':False},sort_keys=True))
if __name__=='__main__': main()
