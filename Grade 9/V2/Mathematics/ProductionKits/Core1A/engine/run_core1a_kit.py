#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

HERE=Path(__file__).resolve(); MATH=HERE.parents[3]
COMMON=MATH/'ProductionKits'/'common'/'engine'; UP1A=MATH/'Core1A'/'engine'; UP1=MATH/'Core1Authoring'/'engine'
sys.path[:0]=[str(COMMON),str(UP1A),str(UP1)]
from production_primitives import validate_source_bundle, validate_bound_object, build_learning_representation, validate_learning_representation, build_blueprint_id
import build_math_core1a_textbook as base
from core1a_bucket_synthesis import synthesize_bucket_plan

REQUIRED_ROLES={'LEARNER_STUDY_MODEL','CORE1_PLAN','PCK_CANDIDATE_REGISTRY','PROBLEM_FAMILY_REGISTRY'}
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))

def match_representation_input(bucket, authored):
    wanted=set(bucket['member_capability_refs']); rows=[x for x in authored if set(x.get('member_capability_refs') or [])==wanted]
    if len(rows)!=1: raise ValueError('CORE1A_KIT_REPRESENTATION_INPUT_MISSING:'+bucket['bucket_id'])
    return rows[0]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-bundle',required=True); ap.add_argument('--core1-plan',required=True); ap.add_argument('--study-model',required=True)
    ap.add_argument('--pck-index',required=True); ap.add_argument('--problem-family-index',required=True); ap.add_argument('--representation-inputs',required=True); ap.add_argument('--out-dir',required=True)
    a=ap.parse_args()
    bundle=load(a.source_bundle); validate_source_bundle(bundle,REQUIRED_ROLES); core1=load(a.core1_plan); study=load(a.study_model)
    validate_bound_object(bundle,'LEARNER_STUDY_MODEL',study,ref_fields=('study_model_id',),digest_fields=('study_model_digest',))
    validate_bound_object(bundle,'CORE1_PLAN',core1,ref_fields=('core1_study_plan_id',),digest_fields=('plan_digest',))
    assets=base.load_pck_assets(Path(a.pck_index)); families=base.load_problem_families(Path(a.problem_family_index))
    pck_index=load(a.pck_index); fam_index=load(a.problem_family_index)
    validate_bound_object(bundle,'PCK_CANDIDATE_REGISTRY',pck_index,ref_fields=('registry_id',),digest_fields=('registry_digest','index_digest'))
    validate_bound_object(bundle,'PROBLEM_FAMILY_REGISTRY',fam_index,ref_fields=('registry_id',),digest_fields=('index_digest','assembled_registry_digest','registry_digest'))
    bucket_plan=synthesize_bucket_plan(core1,study,assets,families)
    authored=load(a.representation_inputs).get('buckets') or []; rep_plans=[]; used=[]
    for b in bucket_plan['buckets']:
        row=match_representation_input(b,authored); used.append(tuple(sorted(row['member_capability_refs'])))
        atoms=[x['atom_id'] for x in b['learning_atoms']]
        rep=build_learning_representation(bucket_ref=b['bucket_id'],purpose='CORE1A_TEACHING',stage_inputs=row['stage_inputs'],required_atom_refs=atoms)
        validate_learning_representation(rep,atoms); rep_plans.append(rep)
    if [x for x in authored if tuple(sorted(x['member_capability_refs'])) not in used]: raise ValueError('CORE1A_KIT_UNUSED_REPRESENTATION_INPUT')
    sections=[{'bucket_ref':b['bucket_id'],'title':b['title'],'invariant':b['bucket_invariant']['text'],'member_capability_refs':b['member_capability_refs'],'representation_ref':r['representation_id'],'core2_question_refs':b['core2_question_refs']} for b,r in zip(bucket_plan['buckets'],rep_plans)]
    bp={'stage':'CORE1A','purpose':None,'source_bundle_ref':bundle['bundle_id'],'sections':sections,'question_specs':[],'audit_requirements':['EXACT_CAPABILITY_COVERAGE','LEARNER_TREATMENT_PRESERVED','REPRESENTATION_SEQUENCE_COMPLETE','NO_INTERNAL_JARGON']}; bp['blueprint_id']=build_blueprint_id(bp)
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
    (out/'core1a_bucket_plan.json').write_text(json.dumps(bucket_plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'core1a_representation_plans.json').write_text(json.dumps({'plans':rep_plans},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'core1a_product_blueprint.json').write_text(json.dumps(bp,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    audit={'kit_id':'MATH-PRODUCTION-KIT-CORE1A-v1','status':'PASS','bucket_count':len(bucket_plan['buckets']),'representation_count':len(rep_plans),'coverage_status':bucket_plan['coverage']['status'],'blueprint_ref':bp['blueprint_id']}
    (out/'core1a_kit_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8'); print(json.dumps(audit,indent=2))
if __name__=='__main__': main()
