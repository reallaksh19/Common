#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import jsonschema
from production_primitives import validate_answer_contract
HERE=Path(__file__).resolve(); SCHEMA=HERE.parents[1]/'contracts'/'math-answer-contract.schema.json'
ap=argparse.ArgumentParser(); ap.add_argument('--answer-contract',required=True); a=ap.parse_args(); obj=json.loads(Path(a.answer_contract).read_text(encoding='utf-8')); schema=json.loads(SCHEMA.read_text(encoding='utf-8')); jsonschema.validate(obj,schema); validate_answer_contract(obj); print('PASS')
