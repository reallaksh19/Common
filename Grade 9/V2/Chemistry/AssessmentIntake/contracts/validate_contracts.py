#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
pairs=[
 ("chemistry-source-set.schema.json","mixed-chemistry-source.fixture.json"),
 ("question-set.schema.json","mixed-chemistry-question-set.fixture.json"),
 ("external-corpus-snapshot.schema.json","mixed-chemistry-external-corpus.fixture.json"),
 ("declared-topic-scope.schema.json","mixed-chemistry-topic-scope.fixture.json"),
 ("attempt-set.schema.json","mixed-chemistry-attempt-set.fixture.json"),
]
bad=False
for sname,fname in pairs:
    s=json.loads((BASE/"contracts"/sname).read_text(encoding="utf-8"))
    f=json.loads((BASE/"fixtures"/fname).read_text(encoding="utf-8"))
    errs=list(Draft202012Validator(s).iter_errors(f))
    if errs:
        bad=True
        for e in errs: print(fname,":",e.message)
    else: print("PASS",fname)
sys.exit(1 if bad else 0)
