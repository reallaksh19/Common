#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from production_primitives import route_task
ap=argparse.ArgumentParser(); ap.add_argument('--intent',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
intent=json.loads(Path(a.intent).read_text(encoding='utf-8')); result=route_task(intent); Path(a.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
if result['status']=='NEEDS_USER_INPUT': print(result['question']); raise SystemExit(2)
print(json.dumps(result,indent=2))
