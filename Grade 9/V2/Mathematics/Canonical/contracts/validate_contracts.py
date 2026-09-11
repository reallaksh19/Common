#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
CANON = ROOT / "canonical"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def validate_many(schema_name, data_name):
    schema = load(CONTRACTS / schema_name)
    Draft202012Validator.check_schema(schema)
    v = Draft202012Validator(schema)
    rows = load(CANON / data_name)
    for i, row in enumerate(rows):
        errors = sorted(v.iter_errors(row), key=lambda e: list(e.path))
        if errors:
            raise AssertionError(f"{data_name}[{i}] invalid: " + "; ".join(e.message for e in errors))

def main():
    validate_many("math-capability.schema.json","capabilities.v1.json")
    validate_many("math-error-signature.schema.json","error_signatures.v1.json")
    validate_many("math-diagnostic-probe.schema.json","diagnostic_probes.v1.json")
    validate_many("math-reasoning-contract.schema.json","reasoning_contracts.v1.json")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)/"package.json"
        subprocess.check_call([sys.executable, str(ROOT/"engine"/"build_math_canonical.py"), "--out", str(out)])
        schema=load(CONTRACTS/"math-canonical-package.schema.json")
        Draft202012Validator.check_schema(schema)
        errors=list(Draft202012Validator(schema).iter_errors(load(out)))
        if errors: raise AssertionError("; ".join(e.message for e in errors))
    print("MATH-V2-01 contract validation: PASS")

if __name__ == "__main__":
    main()
