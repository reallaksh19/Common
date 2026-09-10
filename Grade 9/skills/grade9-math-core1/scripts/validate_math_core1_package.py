#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import fitz

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dir',required=True,type=Path); ap.add_argument('--prefix',required=True); a=ap.parse_args()
    d=a.dir; p=a.prefix; errors=[]
    names={
      'bundle':d/f'{p}_Research_Bundle.json','manifest':d/f'{p}_Research_Bundle_Manifest.json','md':d/f'{p}_Research_Core.md','pdf':d/f'{p}_Research_Core.pdf','source':d/f'{p}_Source_Ledger.json'}
    for k,path in names.items():
        if not path.exists(): errors.append(f'missing {k}: {path.name}')
    if errors:
        print('MATH_CORE1_PACKAGE = FAIL'); [print('- '+x) for x in errors]; return 1
    bundle=json.loads(names['bundle'].read_text()); manifest=json.loads(names['manifest'].read_text()); source=json.loads(names['source'].read_text())
    if bundle.get('project',{}).get('subject')!='MATHEMATICS': errors.append('bundle subject is not MATHEMATICS')
    if bundle.get('research_bundle_id')!=manifest.get('research_bundle_id'): errors.append('manifest bundle id mismatch')
    arts=manifest.get('artifacts',[]); by={(x.get('role'),x.get('path')):x for x in arts}
    expected=[('RESEARCH_BUNDLE',names['bundle']),('RESEARCH_CORE_MD',names['md']),('RESEARCH_CORE_PDF',names['pdf']),('SOURCE_LEDGER',names['source'])]
    for role,path in expected:
        rec=by.get((role,path.name))
        if not rec: errors.append(f'manifest missing {role} {path.name}')
        elif rec.get('sha256')!=sha(path): errors.append(f'hash mismatch for {path.name}')
    if bundle.get('source_ledger_ref',{}).get('sha256')!=sha(names['source']): errors.append('bundle source_ledger_ref hash mismatch')
    md=names['md'].read_text(encoding='utf-8')
    material=[x['claim_id'] for x in bundle.get('research_claims',[])]+[x['representation_requirement_id'] for x in bundle.get('representation_requirements',[])]+[x['id'] for x in bundle.get('equation_or_reaction_objects',[])]+[x['worked_reasoning_id'] for x in bundle.get('worked_reasoning',[])]
    missing_md=[x for x in material if x not in md]
    if missing_md: errors.append('MD missing material ids: '+', '.join(missing_md))
    doc=fitz.open(names['pdf']); text='\n'.join(page.get_text() for page in doc); page_count=len(doc); doc.close()
    missing_pdf=[x for x in material if x not in text]
    if missing_pdf: errors.append('PDF missing material ids: '+', '.join(missing_pdf))
    serialized=json.dumps(bundle)
    for token in ('baseline_profile','learner_profile','B30','B50','B80','Appendix A','Appendix B','Appendix C'):
        if token in serialized: errors.append(f'learner/publication token leaked into ResearchBundle: {token}')
    if bundle.get('status')=='READY_FOR_PUBLISH' and any(x.get('blocking') for x in bundle.get('unresolved_items',[])): errors.append('READY_FOR_PUBLISH contains blocking unresolved items')
    if errors:
        print('MATH_CORE1_PACKAGE = FAIL'); [print('- '+x) for x in errors]; return 1
    print('MATH_CORE1_PACKAGE = PASS')
    print(f'PDF_PAGES = {page_count}')
    print('MATERIAL_VIEW_RECONCILIATION = PASS')
    print('BXX_SEPARATION = PASS')
    print('ARTIFACT_HASH_BINDING = PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
