#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from production_primitives import build_learning_representation, validate_learning_representation
ap=argparse.ArgumentParser(); ap.add_argument('--spec',required=True); ap.add_argument('--out',required=True); a=ap.parse_args(); s=json.loads(Path(a.spec).read_text(encoding='utf-8')); plan=build_learning_representation(bucket_ref=s['bucket_ref'],purpose=s['purpose'],stage_inputs=s['stage_inputs'],required_atom_refs=s['required_atom_refs']); validate_learning_representation(plan,s['required_atom_refs']); Path(a.out).write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8'); print(plan['representation_id'])
