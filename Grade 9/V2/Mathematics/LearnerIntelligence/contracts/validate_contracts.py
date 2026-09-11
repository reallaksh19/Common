#!/usr/bin/env python3
import json
from pathlib import Path
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
schemas={p.name:json.loads(p.read_text()) for p in ROOT.joinpath("contracts").glob("*.schema.json")}
evidence=json.loads(ROOT.joinpath("fixtures/learner_evidence.synthetic.json").read_text())
jsonschema.validate(evidence, schemas["math-learner-evidence.schema.json"])
print("MATH-V2-02 contracts: PASS")
