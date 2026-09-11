#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def load(path):
    return json.loads(Path(path).read_text())

def main():
    result_schema = load(HERE / "comparative-validation-result.schema.json")
    human_schema = load(HERE / "human-quality-review.schema.json")
    Draft202012Validator.check_schema(result_schema)
    Draft202012Validator.check_schema(human_schema)
    Draft202012Validator(result_schema).validate(load(ROOT / "fixtures/blocked_result.synthetic.json"))
    Draft202012Validator(human_schema).validate(load(ROOT / "fixtures/no_authorized_human_evidence.synthetic.json"))
    print("PHY-V2-07 comparative-validation contracts/fixtures = PASS")

if __name__ == "__main__":
    main()
