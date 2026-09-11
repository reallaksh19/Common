#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

PAGE_W,PAGE_H=A4; MARGIN=40
FORBIDDEN=('PR #156','PR156','benchmark_template','benchmark_reference','benchmark_page','mature_reference')
WORKSPACE={'DIAGNOSTIC_PROBE_PANEL':3,'GUIDED_WORKSPACE':3,'FADED_WORKSPACE':3,'INDEPENDENT_WORKSPACE':5,'COMPLETION_EVIDENCE_PANEL':5}
EXTRA={'DIAGNOSTIC_PROBE_PANEL':42,'BOUNDARY_STATE_TABLE':102,'GUIDED_WORKSPACE':42,'FADED_WORKSPACE':42,'INDEPENDENT_WORKSPACE':70,'COMPLETION_EVIDENCE_PANEL':70,'MINIMAL_CONTRAST_PANEL':18,'WORKED_REASONING_TRACE':18}

def load(p): return json.loads(Path(p).read_text())
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_obj(o): return sha_bytes(canonical(o))

def wrap(text,font='Helvetica',size=9.2,max_width=490):
    words=str(text).split(); lines=[]; cur=''
    for word in words:
        trial=(cur+' '+word).strip()
        if stringWidth(trial,font,size)<=max_width: cur=trial
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines or ['']

def build_structure(product,policy):
    material=[i['content_id'] for i in product['content_items'] if i['materiality']=='MATERIAL']
    seen=[]; intents=[]
    for n,g in enumerate(policy['page_groups'],1):
        seen.extend(g['content_refs'])
        intents.append({'page_intent_id':f'PAGE-{n:02d}','page_number':n,'title':g['title'],'content_refs':g['content_refs']})
    if sorted(seen)!=sorted(material) or len(seen)!=len(set(seen)): raise ValueError('every MATERIAL item must appear exactly once in structure')
    return {'schema_version':'1.0.0','structure_id':'PHY-PUB-STRUCTURE-SYN-002','semantic_product_ref':product['semantic_product_id'],'page_intents':intents}

def panel_height(item):
    lines=sum(len(wrap(x)) for x in item['body'])
    return max(78,48+lines*11.5+EXTRA.get(item['primitive'],0))

def draw_state_table(c,item,x,y,w):
    headers=item['metadata'].get('table_headers',[]); rows=item['metadata'].get('table_rows',[])
    if len(headers)!=4 or len(rows)<2: raise ValueError('BOUNDARY_STATE_TABLE requires four headers and at least two rows')
    left=x+12; total=w-24; widths=[0.15*total,0.24*total,0.25*total,0.36*total]; row_h=29
    top=y; bottom=top-row_h*(1+len(rows))
    c.setLineWidth(0.6); c.rect(left,bottom,total,top-bottom,stroke=1,fill=0)
    xpos=left
    for cw in widths[:-1]: xpos+=cw; c.line(xpos,bottom,xpos,top)
    for r in range(1,1+len(rows)): c.line(left,top-r*row_h,left+total,top-r*row_h)
    c.setFont('Helvetica-Bold',7.2); xpos=left
    for h,cw in zip(headers,widths):
        c.drawString(xpos+4,top-17,str(h)); xpos+=cw
    c.setFont('Helvetica',6.8)
    for ridx,row in enumerate(rows):
        xpos=left; rtop=top-(ridx+1)*row_h
        for text,cw in zip(row,widths):
            lines=wrap(str(text),size=6.8,max_width=cw-8)[:2]
            ty=rtop-11
            for line in lines: c.drawString(xpos+4,ty,line); ty-=9
            xpos+=cw
    return bottom-8

def draw_panel(c,item,intent,y):
    h=panel_height(item); x=MARGIN; w=PAGE_W-2*MARGIN; y0=y-h
    if y0<MARGIN: raise ValueError(f'content {item["content_id"]} does not fit page')
    c.setLineWidth(0.8); c.roundRect(x,y0,w,h,5,stroke=1,fill=0)
    c.setFont('Helvetica-Bold',11.2); c.drawString(x+10,y-17,item['title'])
    ty=y-34; c.setFont('Helvetica',9.2)
    for para in item['body']:
        for line in wrap(para,size=9.2,max_width=w-20): c.drawString(x+10,ty,line); ty-=11.5
        ty-=2.5
    if item['primitive']=='BOUNDARY_STATE_TABLE':
        ty=draw_state_table(c,item,x,ty-2,w)
    else:
        for _ in range(WORKSPACE.get(item['primitive'],0)):
            c.line(x+12,ty-2,x+w-12,ty-2); ty-=14
    c.setFont('Helvetica-Oblique',6.2); c.drawRightString(x+w-7,y0+6,f"{item['content_id']} | {item['primitive']}")
    return {'content_ref':item['content_id'],'page_intent_id':intent['page_intent_id'],'primitive':item['primitive'],
            'page':intent['page_number'],'x0':round(x,2),'y0':round(y0,2),'x1':round(x+w,2),'y1':round(y,2),
            'fragment_kind':'START','renderer_emitted':True}, y0-9

def render(product,structure,pdf):
    items={i['content_id']:i for i in product['content_items']}; placements=[]
    c=canvas.Canvas(str(pdf),pagesize=A4,invariant=1,pageCompression=0)
    c.setTitle('PHY-V2-06 reviewed Physics learner candidate'); c.setAuthor('V2 deterministic publication renderer')
    for intent in structure['page_intents']:
        c.setFont('Helvetica-Bold',15.5); c.drawString(MARGIN,PAGE_H-34,intent['title'])
        c.setFont('Helvetica',7.2); c.drawRightString(PAGE_W-MARGIN,PAGE_H-32,f"PHY-V2-06 | page {intent['page_number']}")
        y=PAGE_H-53
        for ref in intent['content_refs']:
            p,y=draw_panel(c,items[ref],intent,y); placements.append(p)
        c.showPage()
    c.save(); return placements

def quality():
    return {'PUBLICATION_ENGINEERING':'PASS','SUBJECT_CORRECTNESS':'PENDING','PEDAGOGY_USABILITY':'PENDING','VISUAL_USABILITY':'PENDING','BENCHMARK_COMPARATIVE_VALIDATION':'NOT_RUN'}

def realize(product,target,policy,design_plan,out):
    blob=json.dumps({'product':product,'target':target,'policy':policy})
    if target.get('benchmark_inputs') or policy.get('benchmark_inputs') or any(t in blob for t in FORBIDDEN): raise ValueError('benchmark/reference producer input forbidden')
    if product['learning_design_id']!=design_plan['design_id'] or product['learning_design_digest']!=design_plan['static_design_digest']: raise ValueError('LearningDesign identity mismatch')
    known={b['block_id'] for b in design_plan['blocks']}
    for item in product['content_items']:
        if not set(item['source_design_block_ids'])<=known: raise ValueError('unknown source design block')
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    structure=build_structure(product,policy)
    pdf=out/'candidate.pdf'; placements=render(product,structure,pdf); art_sha=sha_bytes(pdf.read_bytes())
    page_map={'schema_version':'1.0.0','page_map_id':'PHY-PHYSICAL-PAGE-MAP-SYN-002','artifact_path':'candidate.pdf','artifact_sha256':art_sha,
              'page_count':len(structure['page_intents']),'actual_placement_evidence':True,'content_placements':placements}
    audit={'schema_version':'1.0.0','audit_id':'PHY-PUB-AUDIT-SYN-002','artifact_sha256':art_sha,
           'checks':{'MATERIAL_CUSTODY':'PASS','PLACEMENTS_IN_BOUNDS':'PASS','ACTUAL_PLACEMENT_EVIDENCE':'PASS','ARTIFACT_HASH_BOUND':'PASS','SOURCE_DESIGN_BOUND':'PASS','QUALITY_FIREWALL':'PASS'},
           'publication_engineering':'PASS'}
    (out/'learner_semantic_product.json').write_text(json.dumps(product,indent=2,sort_keys=True)+'\n')
    (out/'source_learning_design.json').write_text(json.dumps(design_plan,indent=2,sort_keys=True)+'\n')
    (out/'publication_structure.json').write_text(json.dumps(structure,indent=2,sort_keys=True)+'\n')
    (out/'physical_page_map.json').write_text(json.dumps(page_map,indent=2,sort_keys=True)+'\n')
    (out/'publication_audit.json').write_text(json.dumps(audit,indent=2,sort_keys=True)+'\n')
    desc={'artifact_sha256':art_sha,'semantic_product_sha256':sha_obj(product),'publication_structure_sha256':sha_obj(structure),
          'physical_page_map_sha256':sha_obj(page_map),'publication_audit_sha256':sha_obj(audit),'source_learning_design_sha256':sha_obj(design_plan)}
    manifest={'schema_version':'1.0.0','manifest_id':'PHY-PUB-MANIFEST-SYN-002',**desc,'package_digest':sha_obj(desc),'quality_states':quality()}
    (out/'publication_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    (out/'publication_result.json').write_text(json.dumps({'status':'READY','candidate_artifact':'candidate.pdf','artifact_sha256':art_sha,'quality_states':quality()},indent=2,sort_keys=True)+'\n')
    return manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--product',required=True); ap.add_argument('--target',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--design-plan',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    print(json.dumps(realize(load(a.product),load(a.target),load(a.policy),load(a.design_plan),a.out),sort_keys=True))
if __name__=='__main__': main()
