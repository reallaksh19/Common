#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
for p in sorted((ROOT/'contracts').glob('*.schema.json')):
    Draft202012Validator.check_schema(json.loads(p.read_text()))
sys.path.insert(0,str(ROOT/'engine'))
from build_canonical_package import load_inputs, build_package
build_package(load_inputs())
print('PHY-V2-01 canonical contracts + semantic package = PASS')
