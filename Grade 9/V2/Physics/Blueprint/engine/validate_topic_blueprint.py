#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'));from governor import route
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest_without_field(v,field):x=dict(v);x.pop(field,None);return hashlib.sha256(canonical(x).encode('utf-8')).hexdigest()
def validate_topic(bp):
    Draft202012Validator(json.loads((ROOT/'contracts'/'topic-blueprint.schema.json').read_text())).validate(bp)
    Draft202012Validator(json.loads((ROOT/'contracts'/'evidence-state.schema.json').read_text())).validate(bp['evidence'])
    if bp['evidence']['topic_id']!=bp['topic_id']:raise AssertionError('TOPIC_EVIDENCE_ID_DRIFT')
    decision=route(bp['evidence'])
    if decision['final_route']!=bp['expected_route']:raise AssertionError('TOPIC_EXPECTED_ROUTE_DRIFT:'+decision['final_route'])
    if not bp['route_must_be_derived']:raise AssertionError('TOPIC_ROUTE_HARDCODE_FORBIDDEN')
    if bp['topic_blueprint_digest']!=digest_without_field(bp,'topic_blueprint_digest'):raise AssertionError('TOPIC_BLUEPRINT_DIGEST_DRIFT')
    return {'topic_blueprint_id':bp['topic_blueprint_id'],'derived_route':decision['final_route'],'matched_rule_id':decision['matched_rule_id'],'status':'PASS'}
def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('topic',type=Path);a=ap.parse_args();bp=json.loads(a.topic.read_text(encoding='utf-8'));print(json.dumps(validate_topic(bp),indent=2))
if __name__=='__main__':main()
