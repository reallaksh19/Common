#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D=Path(__file__).resolve().parent
STORE={}
for p in D.glob("*.schema.json"):
    doc=json.loads(p.read_text(encoding="utf-8"))
    STORE[doc["$id"]]=doc
root=json.loads((D/"math-core2-transfer-plan.schema.json").read_text(encoding="utf-8"))
resolver=RefResolver.from_schema(root, store=STORE)
Draft202012Validator(root,resolver=resolver).check_schema()
for p in D.glob("*.schema.json"):
    Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))
print("MATH M-I contracts valid")
