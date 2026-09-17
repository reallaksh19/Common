#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from copy import deepcopy
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'));from compile_publication_ir import compile_publication_ir
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def fixture():return load(ROOT/'fixtures'/'publication'/'m2d-core1a-ir.json')
def policy():return load(ROOT/'policy'/'publication-boundary.v1.json')
def fail(s,code):
    try:compile_publication_ir(s,policy())
    except AssertionError as e:assert str(e).startswith(code),str(e)
    else:raise AssertionError('EXPECTED_FAILURE:'+code)
def test_golden_is_lossless_and_renderer_is_composition_only():o=compile_publication_ir(fixture(),policy());assert o['lossless_audit']['status']=='PASS';assert o['authority_boundary']['renderer_authority']=='COMPOSITION_ONLY';assert o['authority_boundary']['renderer_may_introduce_semantic_claims'] is False
def test_required_ref_missing_fails():s=fixture();s['publication_units']=s['publication_units'][1:];fail(s,'PUBLICATION_REQUIRED_REF_MISSING')
def test_required_ref_duplicate_fails():s=fixture();s['publication_units'].append(deepcopy(s['publication_units'][0]));fail(s,'PUBLICATION_REQUIRED_REF_DUPLICATED')
def test_unknown_ref_fails():s=fixture();s['publication_units'].append({"source_role":"CORE1","source_artifact_ref":"K-PHY-M2D-GOLDEN","semantic_ref":"K-INVENTED","content_digest":"d"*64,"surface_kind":"EXPLANATION","representation_refs":[]});fail(s,'PUBLICATION_UNKNOWN_SEMANTIC_REF')
def test_content_mutation_fails():s=fixture();s['publication_units'][0]['content_digest']='0'*64;fail(s,'PUBLICATION_CONTENT_DIGEST_MISMATCH')
def test_representation_substitution_fails():s=fixture();s['publication_units'][0]['representation_refs']=['RD-UNAUTHORIZED'];fail(s,'PUBLICATION_REPRESENTATION_NOT_AUTHORIZED')
def test_unreleased_upstream_fails():s=fixture();s['upstream_artifacts'][0]['release_state']='PROVISIONAL';fail(s,'PUBLICATION_UPSTREAM_NOT_RELEASED')
def test_role_drift_fails():s=fixture();s['publication_units'][0]['source_role']='CORE2';fail(s,'PUBLICATION_SOURCE_ROLE_DRIFT')
def test_optional_ref_may_be_omitted():o=compile_publication_ir(fixture(),policy());assert all(x['semantic_ref']!='A-OPTIONAL-RETRIEVAL' for x in o['units'])
def test_schema_validates():o=compile_publication_ir(fixture(),policy());Draft202012Validator(load(ROOT/'contracts'/'publication-ir.schema.json')).validate(o)
def test_deterministic_ir_digest():assert compile_publication_ir(fixture(),policy())['publication_ir_digest']==compile_publication_ir(deepcopy(fixture()),policy())['publication_ir_digest']
def main():
    ts=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
    for t in ts:t()
    print(f'Blueprint publication-IR tests: PASS ({len(ts)} tests)')
if __name__=='__main__':main()
