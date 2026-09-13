#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

HERE=Path(__file__).resolve(); MATH=HERE.parents[3]
COMMON=MATH/'ProductionKits'/'common'/'engine'; UP=MATH/'Core1Authoring'/'engine'
sys.path[:0]=[str(COMMON),str(UP)]
from production_primitives import validate_source_bundle, validate_bound_object
from author_math_core1 import author, load, load_candidate_bundle

REQUIRED_ROLES={'LEARNER_STUDY_MODEL','PCK_CANDIDATE_REGISTRY','PCK_PROMOTION_REGISTRY','CORE1_AUTHORING_PROFILE','CORE1_SCOPE_POLICY'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-bundle',required=True); ap.add_argument('--study-model',required=True)
    ap.add_argument('--pck-candidates',required=True); ap.add_argument('--pck-promotions',required=True)
    ap.add_argument('--profile',required=True); ap.add_argument('--scope-policy',required=True)
    ap.add_argument('--out-dir',required=True); ap.add_argument('--test-mode',action='store_true')
    a=ap.parse_args()
    bundle=load(a.source_bundle); validate_source_bundle(bundle,REQUIRED_ROLES)
    study=load(a.study_model); candidates,assets=load_candidate_bundle(a.pck_candidates)
    promotions=load(a.pck_promotions); profile=load(a.profile); scope=load(a.scope_policy)
    validate_bound_object(bundle,'LEARNER_STUDY_MODEL',study,ref_fields=('study_model_id',),digest_fields=('study_model_digest',))
    validate_bound_object(bundle,'PCK_CANDIDATE_REGISTRY',candidates,ref_fields=('registry_id',),digest_fields=('registry_digest',))
    validate_bound_object(bundle,'PCK_PROMOTION_REGISTRY',promotions,ref_fields=('registry_id',),digest_fields=('registry_digest',))
    validate_bound_object(bundle,'CORE1_AUTHORING_PROFILE',profile,ref_fields=('profile_id','policy_id'),digest_fields=('profile_digest','policy_digest','digest'))
    validate_bound_object(bundle,'CORE1_SCOPE_POLICY',scope,ref_fields=('policy_id','profile_id'),digest_fields=('policy_digest','profile_digest','digest'))
    plan=author(study,candidates,assets,promotions,profile,scope,test_mode=a.test_mode)
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
    (out/'core1_study_plan.json').write_text(json.dumps(plan,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
    audit={'kit_id':'MATH-PRODUCTION-KIT-CORE1-v1','status':'PASS','source_bundle_ref':bundle['bundle_id'],'study_model_ref':plan['study_model_ref'],'core1_plan_ref':plan['core1_study_plan_id'],'release_class':plan['release_class'],'capability_count':len(plan['lessons']),'scope_status':plan['scope_completeness']['status']}
    (out/'core1_kit_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8'); print(json.dumps(audit,indent=2))
if __name__=='__main__': main()
