#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from jsonschema import Draft202012Validator
from core1b_runtime import build_release_receipt

def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--unit",required=True);ap.add_argument("--registry",required=True);ap.add_argument("--authority",required=True);ap.add_argument("--events",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    root=Path(__file__).resolve().parents[1];unit=load(a.unit);registry=load(a.registry);authority=load(a.authority);events=load(a.events)
    receipt=build_release_receipt(unit,registry,authority,events)
    schema=load(root/"contracts"/"physics-core1b-release-receipt.schema.json");Draft202012Validator(schema).validate(receipt)
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8");print(json.dumps({"status":"PASS","receipt_id":receipt["receipt_id"],"state":receipt["state"]},indent=2))
if __name__=="__main__":main()
