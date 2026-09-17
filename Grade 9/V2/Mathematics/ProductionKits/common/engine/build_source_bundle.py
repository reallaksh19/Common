#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from production_primitives import digest

def first(obj,fields): return next((obj.get(k) for k in fields if obj.get(k) is not None),None)
ap=argparse.ArgumentParser(); ap.add_argument('--spec',required=True); ap.add_argument('--out',required=True); a=ap.parse_args(); spec=json.loads(Path(a.spec).read_text(encoding='utf-8'))
rows=[]
for item in spec['items']:
    obj=json.loads(Path(item['path']).read_text(encoding='utf-8')); ref=first(obj,item['ref_fields'])
    if item['digest_kind']=='CANONICAL_JSON_SHA256': d=digest(obj)
    else: d=first(obj,item['digest_fields'])
    if item['required'] and (not ref or not d): raise ValueError('SOURCE_BUNDLE_REQUIRED_BINDING_MISSING:'+item['role'])
    rows.append({'role':item['role'],'ref':ref,'digest':d,'digest_kind':item['digest_kind'],'required':item['required'],'release_state':item['release_state'],'path':item['path']})
payload={'subject':'MATHEMATICS','authority_items':rows}; payload['bundle_id']='MATH-SRC-'+digest(payload)[:16]; Path(a.out).write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8'); print(payload['bundle_id'])
