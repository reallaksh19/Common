#!/usr/bin/env python3
"""
Validates all JSON schemas in the contracts directory using Draft202012Validator.
"""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent

def validate_all_contracts():
    schema_files = sorted(ROOT.glob("*.schema.json"))
    if not schema_files:
        print("ERROR: No schema files found in contracts directory.", file=sys.stderr)
        sys.exit(1)

    for p in schema_files:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(obj)
            print(f"Contract valid: {p.name}")
        except Exception as e:
            print(f"ERROR in schema {p.name}: {e}", file=sys.stderr)
            sys.exit(1)

    print("V2 physics agent-tasks contracts = ALL PASS")

if __name__ == "__main__":
    validate_all_contracts()
