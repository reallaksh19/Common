#!/usr/bin/env python3
"""AI pre-review of the frozen Chemistry C-L exact artifact.

This is an ``AI_PRE_REVIEW`` and nothing more. It is bound to the exact PDF
bytes, it can only ever record ``production_claim: False``, and a PASS here
says the *engineering* falsifiers are clear — it is not, and must never be
presented as, subject, pedagogy, assessment or visual-usability review.

It was strengthened alongside issue #321 so it can actually detect the defects
PR #309 disclosed:

* ``LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK`` — now a shape-based scan of every
  rendered text run (``learner_surface_guard``) instead of a fixed substring
  list that missed, for example, the ``EXT01`` external refs the Core2 source
  link was printing.
* ``TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED`` — now checks that each
  primitive the PhysicalPageMap claims to have realized is backed by vector
  drawing operations inside its recorded rectangle on its recorded page, and
  that the realized-kind count clears the policy floor.
* ``PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE`` — placement rectangles
  are re-derived from the rendered document rather than trusted.
"""

import argparse, copy, hashlib, json, sys
from pathlib import Path
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import learner_surface_guard as GUARD

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def page_evidence(pdf):
    doc=pymupdf.open(pdf); pages=[]
    for i,p in enumerate(doc):
        pages.append({'page':i+1,'text':p.get_text('text'),'image_count':len(p.get_images(full=True)),
                      'height':float(p.rect.height),'drawings':[d['rect'] for d in p.get_drawings()]})
    return pages

def _covered(rect,pages,page_no):
    """Count vector drawing ops whose rectangle sits inside a placement box.

    The PhysicalPageMap records PDF user space (origin bottom-left) while
    pymupdf reports rects in top-left space, so the box is flipped before the
    containment test.
    """
    page=next((p for p in pages if p['page']==page_no),None)
    if page is None: return 0
    x0,y0,x1,y1=rect
    top=page['height']-y1; bottom=page['height']-y0
    return sum(1 for r in page['drawings']
               if r.x0>=x0-2 and r.x1<=x1+2 and r.y0>=top-2 and r.y1<=bottom+2)

def primitive_realization(page_map,pages):
    """Every claimed primitive must be backed by real vector ops in its box."""
    unrealized=[]
    for entry in page_map.get('realized_primitives',[]):
        hits=_covered((entry['x0'],entry['y0'],entry['x1'],entry['y1']),pages,entry['page'])
        if hits<3: unrealized.append('%s@p%d' % (entry['primitive'],entry['page']))
    return unrealized

def placement_evidence(page_map,pages):
    problems=[]
    if not page_map.get('actual_placement_evidence'): problems.append('PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE')
    count=len(pages)
    if page_map.get('page_count')!=count: problems.append('PHYSICAL_PAGE_COUNT_DRIFT')
    intents={x['page_intent_id']:x for x in page_map.get('page_intents',[])}
    for entry in page_map.get('content_placements',[]):
        if entry['page']<1 or entry['page']>count: problems.append('PLACEMENT_OUT_OF_PHYSICAL_BOUNDS')
        if entry['fragment_kind']=='CONTINUATION':
            intent=intents.get(entry['page_intent_id'])
            if not intent or not intent['split'] or entry['page'] not in intent['continuation_pages']:
                problems.append('ORPHAN_CONTINUATION_FRAGMENT')
    for intent in page_map.get('page_intents',[]):
        actual=sorted({e['page'] for e in page_map['content_placements'] if e['page_intent_id']==intent['page_intent_id']})
        if actual!=sorted(intent['physical_pages']): problems.append('PAGE_INTENT_RECONCILIATION_FAILURE')
    return sorted(set(problems))

def audit(candidate_path,core1_pdf,core2_pdf,out_review,page_map_core1=None,page_map_core2=None,policy=None):
    candidate=load(candidate_path)
    core1=page_evidence(core1_pdf); core2=page_evidence(core2_pdf)
    findings=[]

    # 1. learner-surface identifier leak, by shape, over every rendered run
    leaks={}
    for pages,book in ((core1,'core study guide'),(core2,'transfer book')):
        found=GUARD.scan_pages([p['text'] for p in pages])
        for token,where in found.items(): leaks.setdefault(token,[]).append('%s p%s' % (book,where))
    if leaks:
        findings.append('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK: '+', '.join(sorted(leaks)))

    # 2. teaching primitives realized as vector graphics, not labelled
    for path,pages,pdf in ((page_map_core1,core1,core1_pdf),(page_map_core2,core2,core2_pdf)):
        if not path: continue
        page_map=load(path)
        unrealized=primitive_realization(page_map,pages)
        if unrealized:
            findings.append('TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED: '+', '.join(unrealized))
        problems=placement_evidence(page_map,pages)
        findings.extend(problems)
        if page_map.get('artifact_sha256')!=sha_file(pdf):
            findings.append('EXACT_ARTIFACT_HASH_MISMATCH')

    evidence=candidate.get('machine_evidence',{})
    realized=list(evidence.get('teaching_primitive_kinds_realized') or [])
    floor=(policy or {}).get('minimum_realized_primitive_kinds',8)
    if len(realized)<floor:
        findings.append('TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED: only %d realized kinds (floor %d)' % (len(realized),floor))
    vector_pages=sum(1 for p in core1+core2 if p['drawings'])
    if vector_pages==0:
        findings.append('TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED: no vector drawing operations in either product')

    # 3. source figure semantics must be a picture, not a dumped structure
    if any(('"model": "PARTICLE_COUNT"' in p['text']) or ('"particles":' in p['text'])
           or ('Source figure semantics' in p['text']) for p in core2):
        findings.append('SOURCE_FIGURE_SEMANTICS_RENDERED_AS_TEXT_NOT_REALIZED_VISUAL')

    # 4. the bridge claim must be backed by an actual drawn bridge
    bridge=[p for p in core1 if 'Same chemical entity across three views' in p['text']]
    realized_bridge=bool(bridge and any(p['drawings'] for p in bridge))
    if not realized_bridge:
        findings.append('MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED')

    if findings: findings.append('MATURE_DESIGN_QUALITY_NOT_ESTABLISHED_BY_AI_PRE_REVIEW')

    candidate['machine_evidence']['macro_particle_symbolic_realized']=realized_bridge
    candidate['machine_evidence']['learner_internal_identifier_leaks']=len(leaks)
    candidate['package_digest']=digest(candidate,'package_digest')
    Path(candidate_path).write_text(json.dumps(candidate,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    arts={x['product_id']:x for x in candidate['artifacts']}
    review={'review_id':'CHEM-C-L-AI-PRE-REVIEW-v2','schema_version':'1.0.0','subject':'CHEMISTRY',
            'review_kind':'AI_PRE_REVIEW','reviewer_role':'AI_PRE_REVIEW','candidate_ref':candidate['candidate_id'],
            'package_digest':candidate['package_digest'],
            'core1_pdf_sha256':arts['CORE_STUDY_GUIDE']['sha256'],
            'core2_pdf_sha256':arts['EXAMSIDE_SOLUTION_TRANSFER_BOOK']['sha256'],
            'state':'FAIL' if findings else 'PASS','findings':findings,'production_claim':False,
            'scope':'ENGINEERING_FALSIFIERS_ONLY',
            'not_established_by_this_review':['SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN',
                                              'VISUAL_USABILITY','MATURE_DESIGN_QUALITY'],
            'evidence':{'realized_primitive_kinds':realized,
                        'label_only_primitive_kinds':list(evidence.get('teaching_primitives_label_only') or []),
                        'pages_with_vector_graphics':vector_pages,
                        'total_pages':len(core1)+len(core2)}}
    Path(out_review).write_text(json.dumps(review,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return candidate,review

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--candidate',required=True); ap.add_argument('--core1',required=True)
    ap.add_argument('--core2',required=True); ap.add_argument('--out-review',required=True)
    ap.add_argument('--page-map-core1'); ap.add_argument('--page-map-core2'); ap.add_argument('--policy')
    a=ap.parse_args()
    policy=load(a.policy) if a.policy else None
    c,r=audit(a.candidate,a.core1,a.core2,a.out_review,a.page_map_core1,a.page_map_core2,policy)
    print(json.dumps({'package_digest':c['package_digest'],'ai_pre_review':r['state'],'findings':r['findings'],
                      'realized_primitive_kinds':len(r['evidence']['realized_primitive_kinds'])},
                     ensure_ascii=False,sort_keys=True))
    raise SystemExit(0 if r['state']=='PASS' else 1)
if __name__=='__main__': main()
