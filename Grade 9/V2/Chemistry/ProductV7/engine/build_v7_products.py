#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
from model import build_page_models
from assure import validate_authority_and_pal
from render import render_product, preflight_pdf

HERE=Path(__file__).resolve().parent
PRODUCT=HERE.parent
CHEM=PRODUCT.parent
BLUEPRINT=CHEM/'LearningBlueprint'
SPEC=importlib.util.spec_from_file_location('v7',BLUEPRINT/'engine'/'validate_blueprint_v7.py')
v7=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(v7)
POLICY=json.loads((BLUEPRINT/'policies'/'v7-product-assurance-policy.json').read_text())
AUTH=json.loads((PRODUCT/'authority'/'observation-evidence-inference-v7.json').read_text())
CCBOM=json.loads((PRODUCT/'assurance'/'ccbom-observation-evidence-inference.json').read_text())
QUESTIONS={q['question_id']:q for q in AUTH['questions']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',required=True); args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    models=build_page_models(AUTH)
    sim=validate_authority_and_pal(models,AUTH,QUESTIONS,CCBOM,POLICY,v7)
    manifest={'schema_version':'7.0.0','subtopic_id':AUTH['subtopic_id'],'products':{},'similarity':sim,'assurance':{'ccbom':'PASS','difficulty':'PASS','purpose':'PASS','learner_fit':'PASS','question_custody':'PASS','badges':'PASS'}}
    all_realized=set()
    for mode,pages in models.items():
        pdf,realized,audits=render_product(mode,pages,out); all_realized.update(realized)
        count=preflight_pdf(pdf)
        for a in audits:
            threshold=.58 if a['workspace'] else .50
            if a['technical_area_fraction']<threshold: raise RuntimeError(f'TECHNICAL_AREA_TOO_LOW:{mode}:{a}')
            if a['technical_object_count']<4: raise RuntimeError(f'TECHNICAL_OBJECT_DENSITY_LOW:{mode}:{a}')
        manifest['products'][mode]={'pdf':pdf.name,'page_count':count,'page_audits':audits,'realization_ids':sorted(realized)}
    expected=[]
    for asset in CCBOM['assets']:
        for core,disp in asset['core_dispositions'].items():
            if core in models and disp['disposition'] in v7.MANDATORY: expected.append(disp['realization_ref'])
    missing=sorted(set(expected)-all_realized)
    if missing: raise RuntimeError('REALIZATION_REF_MISSING:'+','.join(missing))
    manifest['assurance']['realization_ref_closure']='PASS'; manifest['assurance']['technical_density']='PASS'
    (out/'product_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    (out/'similarity_audit.json').write_text(json.dumps(sim,indent=2),encoding='utf-8')
    print(json.dumps({'status':'PASS','products':{k:v['page_count'] for k,v in manifest['products'].items()},'max_5gram_overlap':sim['non_frozen_prose']['verbatim_5gram_overlap'],'max_identical_run':sim['non_frozen_prose']['max_identical_contiguous_words']},indent=2))

if __name__=='__main__': main()
