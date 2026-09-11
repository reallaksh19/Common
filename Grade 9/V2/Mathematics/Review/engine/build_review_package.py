#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path

FORBIDDEN=('PR #156','PR #157','benchmark_template','benchmark_reference','benchmark_page')
EXPECTED_QUALITY={
  'PUBLICATION_ENGINEERING':'PASS',
  'SUBJECT_CORRECTNESS':'PENDING',
  'PEDAGOGY_USABILITY':'PENDING',
  'VISUAL_USABILITY':'PENDING',
  'BENCHMARK_COMPARATIVE_VALIDATION':'NOT_RUN'
}

def load(p): return json.loads(Path(p).read_text())
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()

def verify_revision(product,page_map):
    by={x['content_id']:x for x in product['content_items']}
    if not any('Proposed move:' in s for s in by['C02']['body']): raise ValueError('prediction task still lacks concrete proposed move')
    if not (any(s.startswith('Move A:') for s in by['C04']['body']) and any(s.startswith('Move B:') for s in by['C04']['body'])): raise ValueError('equality contrast still descriptive-only')
    if not (any(s.startswith('Expansion A:') for s in by['C11']['body']) and any(s.startswith('Expansion B:') for s in by['C11']['body'])): raise ValueError('binomial contrast still descriptive-only')
    c17=' '.join(by['C17']['body']).lower()
    if not any(ch.isdigit() for ch in c17) or '=' not in c17: raise ValueError('completion evidence still lacks concrete task')
    if any(w in c17 for w in ('check','verify','verification','substitut','equivalence')): raise ValueError('completion task cues verification')
    if page_map.get('page_count',99)>5: raise ValueError('visual consolidation finding not addressed')
    pages={p['content_ref']:p['page'] for p in page_map['content_placements']}
    if pages.get('C14')==pages.get('C15'): raise ValueError('probe and separate strength check remain visually grouped')

def build(baseline,findings_doc,revision_plan,policy,revised_manifest,revised_product,revised_page_map):
    baseline_sha=baseline['artifact_sha256']
    findings=copy.deepcopy(findings_doc['findings'])
    decisions=copy.deepcopy(revision_plan['decisions'])
    if policy.get('benchmark_inputs'): raise ValueError('benchmark inputs forbidden')
    txt=json.dumps({'findings':findings,'decisions':decisions,'policy':policy})
    if any(t in txt for t in FORBIDDEN): raise ValueError('benchmark/reference contamination')
    for f in findings:
        if f['artifact_sha256']!=baseline_sha: raise ValueError('finding not bound to exact baseline artifact')
        if f['reviewer_class']!='AI_PRE_REVIEW': raise ValueError('this package expects AI pre-review findings only')
    by_dec={d['finding_id']:d for d in decisions}
    for f in findings:
        if f['severity'] in ('CRITICAL','MAJOR') and (f['finding_id'] not in by_dec or by_dec[f['finding_id']]['disposition']!='FIX'):
            raise ValueError('major/critical finding lacks FIX disposition')
    if revised_manifest['quality_states']!=EXPECTED_QUALITY: raise ValueError('human gate or benchmark state promoted without authority')
    verify_revision(revised_product,revised_page_map)
    revised_sha=revised_manifest['artifact_sha256']
    resolved=[]; enriched=[]
    for d in decisions:
        d=copy.deepcopy(d); d['revised_artifact_sha256']=revised_sha; enriched.append(d)
    by_dec={d['finding_id']:d for d in enriched}
    for f in findings:
        f['status']='CLOSED_FIXED'; f['revision_ref']=by_dec[f['finding_id']]['decision_id']; f['revised_artifact_sha256']=revised_sha; resolved.append(f)
    unresolved=sum(1 for f in resolved if f['severity'] in ('CRITICAL','MAJOR') and f['status']=='OPEN')
    summary={
      'schema_version':'1.0.0','baseline_artifact_sha256':baseline_sha,'revised_artifact_sha256':revised_sha,
      'ai_pre_review_status':'REVISIONS_VERIFIED_HUMAN_REVIEW_PENDING' if unresolved==0 else 'OPEN_FINDINGS',
      'unresolved_major_count':unresolved,
      'human_review_evidence':{'SUBJECT':0,'PEDAGOGY':0,'VISUAL':0},
      'quality_states':copy.deepcopy(EXPECTED_QUALITY)
    }
    components={'resolved_findings_sha256':sha_obj(resolved),'revision_decisions_sha256':sha_obj(enriched),'quality_review_summary_sha256':sha_obj(summary)}
    package={'schema_version':'1.0.0','revision_ref':revision_plan['revision_ref'],'baseline_artifact_sha256':baseline_sha,'revised_artifact_sha256':revised_sha,**components,'package_digest':sha_obj(components)}
    return resolved,enriched,summary,package

def main():
    ap=argparse.ArgumentParser()
    for n in ('baseline','findings','revision-plan','policy','revised-manifest','revised-product','revised-page-map','out'): ap.add_argument('--'+n,required=True)
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    args=vars(a)
    resolved,decisions,summary,package=build(load(args['baseline']),load(args['findings']),load(args['revision_plan']),load(args['policy']),load(args['revised_manifest']),load(args['revised_product']),load(args['revised_page_map']))
    for name,obj in [('review_findings.resolved.json',resolved),('revision_decisions.json',decisions),('quality_review_summary.json',summary),('review_package.json',package)]:
        (out/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__': main()
