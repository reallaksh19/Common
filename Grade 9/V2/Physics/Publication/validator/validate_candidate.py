#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'contracts'
def load(p): return json.loads(Path(p).read_text())
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sh_obj(o): return hashlib.sha256(canon(o)).hexdigest()
def sh_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate(o,n): Draft202012Validator(load(C/n)).validate(o)
def run(out):
    out=Path(out)
    product=load(out/'learner_semantic_product.json'); design=load(out/'source_learning_design.json'); struct=load(out/'publication_structure.json')
    pm=load(out/'physical_page_map.json'); audit=load(out/'publication_audit.json'); man=load(out/'publication_manifest.json'); pdf=out/'candidate.pdf'
    for o,n in [(product,'physics-learner-semantic-product.schema.json'),(struct,'physics-publication-structure.schema.json'),(pm,'physics-physical-page-map.schema.json'),(audit,'physics-publication-audit.schema.json'),(man,'physics-publication-manifest.schema.json')]: validate(o,n)
    actual=sh_file(pdf)
    if actual!=pm['artifact_sha256'] or actual!=audit['artifact_sha256'] or actual!=man['artifact_sha256']: raise ValueError('exact artifact hash drift')
    if len(PdfReader(str(pdf)).pages)!=pm['page_count']: raise ValueError('PDF page count mismatch')
    ids=[i['content_id'] for i in product['content_items'] if i['materiality']=='MATERIAL']
    srefs=[r for p in struct['page_intents'] for r in p['content_refs']]
    prefs=[p['content_ref'] for p in pm['content_placements']]
    if sorted(ids)!=sorted(srefs) or len(srefs)!=len(set(srefs)): raise ValueError('semantic -> structure custody failure')
    if sorted(ids)!=sorted(prefs) or len(prefs)!=len(set(prefs)): raise ValueError('semantic -> physical placement custody failure')
    pages={p['page_intent_id']:p['page_number'] for p in struct['page_intents']}
    for p in pm['content_placements']:
        if not p['renderer_emitted']: raise ValueError('placement is not renderer-emitted')
        if p['page_intent_id'] not in pages or pages[p['page_intent_id']]!=p['page']: raise ValueError('page intent drift')
        if not (0<=p['x0']<p['x1']<=595.5 and 0<=p['y0']<p['y1']<=842): raise ValueError('placement out of bounds')
    known={b['block_id'] for b in design['blocks']}
    for i in product['content_items']:
        if not set(i['source_design_block_ids'])<=known: raise ValueError('unknown source design block')
    desc={'artifact_sha256':actual,'semantic_product_sha256':sh_obj(product),'publication_structure_sha256':sh_obj(struct),'physical_page_map_sha256':sh_obj(pm),'publication_audit_sha256':sh_obj(audit),'source_learning_design_sha256':sh_obj(design)}
    if any(man[k]!=v for k,v in desc.items()) or man['package_digest']!=sh_obj(desc): raise ValueError('manifest/package digest drift')
    q=man['quality_states']
    if q!={'PUBLICATION_ENGINEERING':'PASS','SUBJECT_CORRECTNESS':'PENDING','PEDAGOGY_USABILITY':'PENDING','VISUAL_USABILITY':'PENDING','BENCHMARK_COMPARATIVE_VALIDATION':'NOT_RUN'}: raise ValueError('quality firewall breached')
    order={cid:n for n,cid in enumerate(srefs)}
    for probe,cid,cap in [('PHY-PROBE-APEX-COMPONENTS','PC01','PHY-PROJECTILE-COMPONENT-DECOMPOSITION'),('PHY-PROBE-SIGNED-DISPLACEMENT','PC02','PHY-SIGNED-DISPLACEMENT-INTERPRETATION')]:
        probe_item=next(i for i in product['content_items'] if i['content_id']==cid)
        if probe_item['metadata'].get('probe_ref')!=probe or probe_item['metadata'].get('correction_before_probe') is not False: raise ValueError('probe-first semantics lost')
        for i in product['content_items']:
            if i['content_id']!=cid and cap in i['canonical_refs'] and order[i['content_id']]<order[cid]: raise ValueError('correction/content precedes probe')
    print('PHY-V2-05 independent exact-byte/material audit = PASS')
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); run(a.out)
