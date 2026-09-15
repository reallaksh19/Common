#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]; sys.path.insert(0,str(ROOT/'engine'))
from build_physics_engineering_gate_registry_v3 import build_registry

def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(v:Any)->str:return 'sha256:'+hashlib.sha256(canonical(v)).hexdigest()
def schema(n):return json.loads((ROOT/'contracts'/n).read_text(encoding='utf-8'))
def compile_domain_prerequisite_closure(engineering_receipt,authority_receipts=None):
    authority_receipts=authority_receipts or []; validator=Draft202012Validator(schema('domain-prerequisite-authority.schema.json')); authorities={}
    for row in authority_receipts:
        validator.validate(row); pid=row['prerequisite_id']
        if pid in authorities: raise AssertionError('DOMAIN_PREREQUISITE_DUPLICATE_AUTHORITY:'+pid)
        authorities[pid]=row
    gate_map={g['subtopic_id']:g for g in build_registry()['gates']}; external=set()
    for gid in engineering_receipt['transitive_gate_ids']:
        gate=gate_map.get(gid)
        if gate: external.update(p for p in gate['prerequisites'] if not p.startswith('PHY-'))
    rows=[]
    for pid in sorted(external):
        auth=authorities.get(pid); rows.append({'prerequisite_id':pid,'status':'READY_FROM_AUTHORITATIVE_DOMAIN' if auth else 'HELD_NO_DOMAIN_RECEIPT','authority_ref':auth['authority_ref'] if auth else None})
    status='HELD' if any(r['status']!='READY_FROM_AUTHORITATIVE_DOMAIN' for r in rows) else 'READY'
    receipt={'schema_version':'1.0.0','receipt_id':'DOMAIN-CLOSURE-PHY-'+engineering_receipt['request_id'].replace('ENG-REQ-','',1),'engineering_receipt_ref':engineering_receipt['receipt_id'],'prerequisites':rows,'closure_status':status,'closure_digest':''}
    receipt['closure_digest']=digest({k:v for k,v in receipt.items() if k!='closure_digest'}); Draft202012Validator(schema('domain-prerequisite-closure.schema.json')).validate(receipt); return receipt

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('engineering_receipt',type=Path); ap.add_argument('--authority',action='append',default=[]); ap.add_argument('--out',type=Path); a=ap.parse_args(); eng=json.loads(a.engineering_receipt.read_text()); auth=[json.loads(Path(p).read_text()) for p in a.authority]; r=compile_domain_prerequisite_closure(eng,auth); t=json.dumps(r,indent=2)+'\n'; a.out.write_text(t) if a.out else print(t,end='')
if __name__=='__main__':main()
