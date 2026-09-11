#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads(Path(p).read_text())
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def schema(n): return load(ROOT/'contracts'/n)
def val(o,n): Draft202012Validator(schema(n)).validate(o)

def validate_dir(out):
    out=Path(out); product=load(out/'learner_semantic_product.json'); structure=load(out/'publication_structure.json'); page_map=load(out/'physical_page_map.json'); audit=load(out/'publication_audit.json'); manifest=load(out/'publication_manifest.json')
    val(product,'math-learner-semantic-product.schema.json'); val(structure,'math-publication-structure.schema.json'); val(page_map,'math-physical-page-map.schema.json'); val(audit,'math-publication-audit.schema.json'); val(manifest,'math-publication-manifest.schema.json')
    pdf=(out/'candidate.pdf').read_bytes(); sha=hashlib.sha256(pdf).hexdigest()
    if not pdf.startswith(b'%PDF-') or b'%%EOF' not in pdf[-1024:]: raise ValueError('invalid PDF header/trailer')
    if sha!=page_map['artifact_sha256'] or sha!=audit['artifact_sha256'] or sha!=manifest['artifact_sha256']: raise ValueError('artifact hash mismatch')
    material=[x['content_id'] for x in product['content_items'] if x['materiality']=='MATERIAL']
    struct=[r for p in structure['page_intents'] for r in p['content_refs']]; placed=[p['content_ref'] for p in page_map['content_placements']]
    if sorted(material)!=sorted(struct) or len(struct)!=len(set(struct)): raise ValueError('structure material custody failure')
    if sorted(material)!=sorted(placed) or len(placed)!=len(set(placed)): raise ValueError('physical material custody failure')
    if not page_map['actual_placement_evidence']: raise ValueError('planned placement cannot substitute for actual evidence')
    W,H=595.2755905511812,841.8897637795277
    for p in page_map['content_placements']:
        if not (0<=p['x0']<p['x1']<=W and 0<=p['y0']<p['y1']<=H): raise ValueError('placement out of bounds')
        if p['fragment_kind']!='START': raise ValueError('orphan continuation/unsupported fragment')
    desc={'artifact_sha256':manifest['artifact_sha256'],'semantic_product_sha256':manifest['semantic_product_sha256'],'publication_structure_sha256':manifest['publication_structure_sha256'],'physical_page_map_sha256':manifest['physical_page_map_sha256'],'publication_audit_sha256':manifest['publication_audit_sha256']}
    if manifest['semantic_product_sha256']!=sha_obj(product) or manifest['publication_structure_sha256']!=sha_obj(structure) or manifest['physical_page_map_sha256']!=sha_obj(page_map) or manifest['publication_audit_sha256']!=sha_obj(audit): raise ValueError('manifest component digest mismatch')
    if manifest['package_digest']!=sha_obj(desc): raise ValueError('package digest drift/self-reference')
    q=manifest['quality_states']
    if q!={'PUBLICATION_ENGINEERING':'PASS','SUBJECT_CORRECTNESS':'PENDING','PEDAGOGY_USABILITY':'PENDING','VISUAL_USABILITY':'PENDING','BENCHMARK_COMPARATIVE_VALIDATION':'NOT_RUN'}: raise ValueError('quality firewall violation')
    by={x['content_id']:x for x in product['content_items']}
    if not by['C05']['metadata'].get('one_legal_operation_per_line'): raise ValueError('worked reasoning lost legal-operation discipline')
    if not by['C04']['metadata'].get('prediction_before_resolution') or not by['C04']['metadata'].get('focal_distinction'): raise ValueError('minimal contrast incomplete')
    if not (by['C06']['support_level']>by['C07']['support_level']>by['C08']['support_level']): raise ValueError('fading not material')
    if by['C08']['metadata'].get('conceptual_hints'): raise ValueError('independent attempt contains hint')
    if by['C14']['metadata'].get('explanation_before_probe') is not False: raise ValueError('probe-first violation')
    if by['C16']['metadata'].get('number_only') is not False: raise ValueError('number-only transfer')
    if by['C17']['metadata'].get('prompted') is not False: raise ValueError('completion check must be self-initiated')
    return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); validate_dir(a.out); print('MATH-V2-05 independent candidate audit = PASS')
if __name__=='__main__': main()
