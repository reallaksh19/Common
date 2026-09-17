#!/usr/bin/env python3
from pathlib import Path
import json, sys
D=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(D/'production_kit'))
from build_learning_representation import build
from validate_learning_representation import validate
from task_router import route

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
files=sorted((D/'fixtures'/'golden').glob('*.json')); assert len(files)==3
for p in files:
    f=load(p); rep=build(f); report=validate(rep,f); assert report['status']=='PASS'
assert route('FULL_LEARNING',20,'D3')['scaffold_profile_id']=='CORE1-FULL-P20'
assert route('READY_VERIFY_ONLY',50,'D2')['scaffold_profile_id']=='CORE1-READY'
assert route('PROBE_FIRST',20,'D3')['scaffold_profile_id']=='CORE1-PROBE-P20'
print('Physics Core1 production kit: PASS (3 golden fixtures)')
