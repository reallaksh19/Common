#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
C = D / "contracts"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def check(schema_name, value):
    schema = load(C / schema_name)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e:list(e.path))
    if errors:
        for err in errors:
            print(f"{schema_name}: {list(err.path)}: {err.message}")
        raise SystemExit(1)

ap = argparse.ArgumentParser()
ap.add_argument("bundle")
a = ap.parse_args()
bundle = load(a.bundle)
check("chemistry-scope-reconciliation.schema.json", bundle["scope_reconciliation"])
check("chemistry-assessment-scope-model.schema.json", bundle["assessment_scope_model"])
check("chemistry-assessment-coverage-matrix.schema.json", bundle["assessment_coverage_matrix"])
check("chemistry-prerequisite-closure.schema.json", bundle["prerequisite_closure"])
print("CHEMISTRY C-C generated scope contracts = PASS")
