#!/usr/bin/env python3
"""Audit produced bytes as well as model declarations. Visual review remains separate."""
import json,sys,hashlib,re
from pathlib import Path
import fitz
from pypdf import PdfReader
from validate_v2 import validate
def audit(model,pdf):
    d=json.loads(Path(model).read_text());out=validate(d);doc=fitz.open(pdf)
    layout=json.loads(Path(pdf).with_suffix('.layout.json').read_text());badlinks=[];overlap=[];outside=[]
    for pn,p in enumerate(doc,1):
        for link in p.get_links():
            if link['kind']==fitz.LINK_GOTO and not 0<=link['page']<len(doc):badlinks.append([pn,link])
        words=p.get_text('words')
        for a in words:
            if a[0]<0 or a[1]<0 or a[2]>p.rect.width or a[3]>p.rect.height:outside.append([pn,a[4]])
        for i,a in enumerate(words):
            for b in words[i+1:]:
                if a[5:7]==b[5:7]:continue
                ix=min(a[2],b[2])-max(a[0],b[0]);iy=min(a[3],b[3])-max(a[1],b[1])
                if ix>1.0 and iy>1.0 and ix*iy>0.15*min((a[2]-a[0])*(a[3]-a[1]),(b[2]-b[0])*(b[3]-b[1])):
                    overlap.append({'page':pn,'a':a[4],'b':b[4],'overlap':[round(ix,2),round(iy,2)]})
    expected_links=len(layout['links'])+len(layout.get('external_links',[]));actual_links=sum(len(p.get_links()) for p in doc)
    assert actual_links==expected_links,'PDF link annotation count differs from render manifest'
    reader=PdfReader(pdf);page_ids={p.indirect_reference.idnum:i for i,p in enumerate(reader.pages)}
    for pn,p in enumerate(reader.pages,1):
        expected=[r for r in layout['links'] if r['page']==pn]
        annots=[a.get_object() for a in p.get('/Annots',[]) if a.get_object().get('/Subtype')=='/Link']
        actual=[a for a in annots if '/Dest' in a]
        assert len(expected)==len(actual),'annotation count on page'
        for r,a in zip(expected,actual):
            assert '/Dest' in a and a['/Dest'][0].idnum in page_ids,'unresolved PDF reference'
            assert page_ids[a['/Dest'][0].idnum]==layout['destinations'][r['target']]-1,'wrong actual PDF destination'
        uris=[a['/A']['/URI'] for a in annots if '/A' in a and a['/A'].get('/S')=='/URI']
        assert uris==[r['url'] for r in layout.get('external_links',[]) if r['page']==pn],'source URI lost or changed'
    alltext='\n'.join(p.get_text() for p in doc)
    qb=d['questions'];all_qs=qb['anchors']+qb['core_calibrated']+qb['challenges']
    for q in all_qs:
        for prefix in ['', 'hint-', 'solution-']:assert prefix+q['id'] in layout['destinations'],'missing question/hint/solution'
    solution_pages=[v for k,v in layout['destinations'].items() if k.startswith('solution-')]
    last_question=max(layout['destinations'][q['id']] for q in all_qs)
    assert min(solution_pages)>last_question,'answers before questions finish'
    if d['product']=='core':
        assert 'Appendix A' in alltext and 'Appendix B' in alltext,'missing appendix heading'
        assert min(solution_pages)>layout['destinations']['handout'],'solutions must follow handout'
    assert 'PLACEHOLDER' not in alltext and 'Planned figure' not in alltext,'placeholder leak'
    regionfonts=[r['size'] for r in layout['regions'] if r['kind']=='text']
    out.update(pages=len(doc),links=actual_links,broken_links=badlinks,text_overlap_findings=overlap,outside_page=outside,minimum_text_role_size=min(regionfonts),figure_occurrences=sum(r['kind']=='figure' for r in layout['regions']),pdf_sha256=hashlib.sha256(Path(pdf).read_bytes()).hexdigest(),model_sha256=hashlib.sha256(Path(model).read_bytes()).hexdigest(),visual_review='SEPARATE_REVIEW_REQUIRED')
    assert not outside,'words outside PDF bounds'
    # Report overlap findings for inspection; a real collision blocks release.
    return out
if __name__=='__main__':
    out=audit(sys.argv[1],sys.argv[2]);target=Path(sys.argv[2]).with_suffix('.audit.json');target.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
    sys.exit(bool(out['text_overlap_findings']))
