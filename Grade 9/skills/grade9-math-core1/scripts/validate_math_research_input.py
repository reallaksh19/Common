#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

FORBIDDEN_TOKENS=("baseline_profile","learner_profile","publication_target","bxx","appendix","hint_level","h0","h1","h2","h3")

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def walk_keys(obj, path=''):
    if isinstance(obj,dict):
        for k,v in obj.items():
            yield path+'.'+k if path else k
            yield from walk_keys(v,path+'.'+k if path else k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): yield from walk_keys(v,f'{path}[{i}]')

def validate(data):
    e=[]
    if data.get('project',{}).get('subject')!='MATHEMATICS': e.append('project.subject must be MATHEMATICS')
    if not data.get('scope_graph',{}).get('canonical_registry_versions'): e.append('ScopeGraph needs canonical_registry_versions')
    concept_ids=set(data.get('concept_ids',[])); included=set(data.get('scope_graph',{}).get('included_nodes',[]))
    missing=concept_ids-included
    if missing: e.append('concept_ids missing from ScopeGraph included_nodes: '+', '.join(sorted(missing)))
    for keypath in walk_keys(data):
        low=keypath.lower()
        if any(tok in low for tok in FORBIDDEN_TOKENS): e.append('Core (1) research input contains downstream learner/publication field: '+keypath)
    sources={s.get('source_id') for s in data.get('source_ledger',{}).get('sources',[])}
    claims=data.get('research_claims',[]); claim_ids={c.get('claim_id') for c in claims}
    covered=set()
    for c in claims:
        for cid in c.get('concept_ids',[]):
            if cid not in concept_ids: e.append(f"claim {c.get('claim_id')} references out-of-scope concept {cid}")
            covered.add(cid)
        if data.get('status')=='READY_FOR_PUBLISH' and c.get('traceability_class','').startswith('MATERIAL_'):
            if c.get('verification_status')!='VERIFIED': e.append(f"material claim {c.get('claim_id')} is not VERIFIED")
            if not c.get('source_refs'): e.append(f"material claim {c.get('claim_id')} has no source_refs")
        for s in c.get('source_refs',[]):
            if s not in sources: e.append(f"claim {c.get('claim_id')} references unknown source {s}")
    if data.get('status')=='READY_FOR_PUBLISH':
        for cid in sorted(concept_ids-covered): e.append(f"included concept {cid} has no research claim")
        for cand in data.get('scope_graph',{}).get('project_candidates',[]):
            if cand.get('status') in {'RESEARCH_CANDIDATE','SUBJECT_AUTHORITY_REVIEW'}: e.append(f"unpromoted project candidate {cand.get('candidate_id')}")
        for u in data.get('unresolved_items',[]):
            if u.get('blocking'): e.append(f"blocking unresolved item {u.get('unresolved_id')}")
    for r in data.get('representation_requirements',[]):
        rid=r.get('representation_requirement_id')
        if r.get('subject')!='MATHEMATICS': e.append(f"representation {rid} subject must be MATHEMATICS")
        if not r.get('semantic_requirements'): e.append(f"representation {rid} lacks semantic_requirements")
        for cid in r.get('concept_ids',[]):
            if cid not in concept_ids: e.append(f"representation {rid} references out-of-scope concept {cid}")
        for ref in r.get('research_refs',[]):
            if ref not in claim_ids: e.append(f"representation {rid} references unknown claim {ref}")
    for obj in data.get('equation_or_reaction_objects',[]):
        for ref in obj.get('research_refs',[]):
            if ref not in claim_ids: e.append(f"formal object {obj.get('id')} references unknown claim {ref}")
    for wr in data.get('worked_reasoning',[]):
        for ref in wr.get('research_refs',[]):
            if ref not in claim_ids: e.append(f"worked reasoning {wr.get('worked_reasoning_id')} references unknown claim {ref}")
    supported=set(data.get('research_context',{}).get('supported_exam_demand_profile_ids',[]))
    attached={x.get('exam_demand_profile_id') for x in data.get('exam_demand_profiles',[])}
    if supported-attached: e.append('supported exam demand profiles missing attached objects: '+', '.join(sorted(supported-attached)))
    q=data.get('question_evidence_ledger')
    if q:
        rows=q.get('rows',[])
        if q.get('candidate_denominator')!=len(rows): e.append('QuestionEvidenceLedger candidate_denominator does not equal rows')
        if any(r.get('disposition')=='REVIEW' for r in rows): e.append('QuestionEvidenceLedger contains REVIEW rows')
    return e

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input',type=Path); a=ap.parse_args(); d=load(a.input); e=validate(d)
    if e:
        print('MATH_CORE1_RESEARCH_INPUT = FAIL')
        for x in e: print('- '+x)
        return 1
    print('MATH_CORE1_RESEARCH_INPUT = PASS')
    print('BXX_SEPARATION = PASS')
    print('CONCEPT_CLAIM_COVERAGE = PASS')
    print('MATH_REFERENCE_CLOSURE = PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
