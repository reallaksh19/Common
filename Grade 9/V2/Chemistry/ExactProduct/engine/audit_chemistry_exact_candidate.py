#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path
import pymupdf

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()

def page_evidence(pdf):
    doc=pymupdf.open(pdf); pages=[]
    for i,p in enumerate(doc):
        text=p.get_text('text')
        pages.append({'page':i+1,'text':text,'image_count':len(p.get_images(full=True)),'drawing_count':len(p.get_drawings())})
    return pages

def audit(candidate_path,core1_pdf,core2_pdf,out_review):
    candidate=load(candidate_path); core1=page_evidence(core1_pdf); core2=page_evidence(core2_pdf)
    full='\n'.join(x['text'] for x in core1+core2)
    internal_tokens=['CAP-','CORE1-','A-CAP-','B-SOL-','CHEM-CONCEPT-','OBLIGATION_LEVEL:','OBLIGATION_REP:','CHECK_SPECIES_IDENTITY','CHECK_ATOMS','CHECK_CHARGE','CHECK_CONDITIONS','VERIFY_RESULT','ACTIVE_STUDY','FULL_LEARNING','READ_GIVEN','IDENTIFY_CHEMICAL_ENTITIES','TRANSLATE_REPRESENTATION','EXPLICIT_EXCEPTION','capability record']
    leaked=sorted({t for t in internal_tokens if t in full})
    translation=[x for x in core1 if 'Translate between particles and symbols' in x['text']]
    particle_q=[x for x in core2 if 'A particle diagram shows two separate H₂O particles.' in x['text']]
    realized=bool(translation and any(x['image_count']+x['drawing_count']>0 for x in translation) and particle_q and any(x['image_count']+x['drawing_count']>0 for x in particle_q))
    json_source_figure=any(('Source figure semantics' in x['text']) or ('"model": "PARTICLE_COUNT"' in x['text']) or ('"particles":' in x['text']) for x in core2)
    findings=[]
    if leaked: findings.append('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK: '+', '.join(leaked))
    if not realized: findings.append('MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED')
    if json_source_figure: findings.append('SOURCE_FIGURE_SEMANTICS_RENDERED_AS_TEXT_NOT_REALIZED_VISUAL')
    if findings: findings.append('MATURE_DESIGN_QUALITY_NOT_ESTABLISHED_BY_AI_PRE_REVIEW')
    candidate['machine_evidence']['macro_particle_symbolic_realized']=realized
    candidate['package_digest']=digest(candidate,'package_digest')
    Path(candidate_path).write_text(json.dumps(candidate,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    arts={x['product_id']:x for x in candidate['artifacts']}
    review={'review_id':'CHEM-C-L-AI-PRE-REVIEW-v1','schema_version':'1.0.0','subject':'CHEMISTRY','review_kind':'AI_PRE_REVIEW','reviewer_role':'AI_PRE_REVIEW','candidate_ref':candidate['candidate_id'],'package_digest':candidate['package_digest'],'core1_pdf_sha256':arts['CORE_STUDY_GUIDE']['sha256'],'core2_pdf_sha256':arts['EXAMSIDE_SOLUTION_TRANSFER_BOOK']['sha256'],'state':'FAIL' if findings else 'PASS','findings':findings,'production_claim':False}
    Path(out_review).write_text(json.dumps(review,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return candidate,review

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',required=True); ap.add_argument('--core1',required=True); ap.add_argument('--core2',required=True); ap.add_argument('--out-review',required=True); a=ap.parse_args(); c,r=audit(a.candidate,a.core1,a.core2,a.out_review); print(json.dumps({'package_digest':c['package_digest'],'ai_pre_review':r['state'],'findings':r['findings']},ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
