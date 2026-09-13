#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from production_primitives import load_scaffold_profiles, build_scaffold_plan
ap=argparse.ArgumentParser(); ap.add_argument('--purpose',required=True); ap.add_argument('--bucket-ref',required=True); ap.add_argument('--profiles',required=True); ap.add_argument('--out',required=True); a=ap.parse_args(); plan=build_scaffold_plan(a.purpose,load_scaffold_profiles(a.profiles),a.bucket_ref); Path(a.out).write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8'); print(plan['scaffold_plan_id'])
