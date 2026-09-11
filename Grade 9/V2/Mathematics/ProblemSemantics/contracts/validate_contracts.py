#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parent; R=D.parent/"registry"
def load(p): return json.loads(Path(p).read_text())
def validate(schema,obj,label):
    errors=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.path))
    if errors: raise SystemExit(label+": "+"; ".join(f"{list(e.path)} {e.message}" for e in errors[:10]))
fs=load(D/"math-problem-family.schema.json"); vs=load(D/"math-verification-route.schema.json"); ips=load(D/"math-item-semantic-profile.schema.json")
idx=load(R/"math-problem-family-registry.json")
fr={k:v for k,v in idx.items() if k not in {"family_shards","assembled_registry_digest","family_count","index_digest"}}
fr["families"]=[]
for spec in idx["family_shards"]: fr["families"]+=load(R/spec["path"])["families"]
fr["registry_digest"]=idx["assembled_registry_digest"]
vr=load(R/"math-verification-route-registry.json"); ir=load(R/"mixed-grade9-item-semantics.json")
for x in fr["families"]: validate(fs,x,x["family_id"])
for x in vr["routes"]: validate(vs,x,x["verification_route_id"])
for x in ir["profiles"]: validate(ips,x,x["item_ref"])
print(f"MATH M-D static contracts PASS: {len(fr['families'])} families, {len(vr['routes'])} verification routes, {len(ir['profiles'])} item profiles")
