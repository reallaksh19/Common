#!/usr/bin/env python3
from pathlib import Path
import json, sys
D=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(D/'production_kit'))
from build_transfer_representation import build
from validate_transfer_representation import validate
from task_router import route
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
files=sorted((D/'fixtures'/'golden').glob('*.json')); assert len(files)==3
for p in files:
    f=load(p); rep=build(f); report=validate(rep,f); assert report['status']=='PASS'
assert route('QX','MCQ','LOW')['scaffold_profile_id']=='CORE2-GUIDE-LOW'
assert route('QX','NUMERIC','MEDIUM')['scaffold_profile_id']=='CORE2-GUIDE-MEDIUM'
assert route('QX','FIGURE','HIGH')['scaffold_profile_id']=='CORE2-GUIDE-HIGH'
print('Physics Core2 production kit: PASS (3 golden fixtures)')
