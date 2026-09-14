#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_engineering_closure import compile_closure, load  # noqa: E402
from validate_ccu_v2 import validate as validate_ccu  # noqa: E402


class EngineeringCCUError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise EngineeringCCUError(code, message)


def validate_engineered_ccu(request: dict, manifest: dict, ccu: dict) -> dict:
    if manifest.get("scope_kind") != "BUCKET":
        fail("E_CCU_ENGINEERING_SCOPE_KIND", "CCU engineering manifest must use scope_kind=BUCKET")
    if manifest.get("scope_ref") != ccu.get("bucket_id"):
        fail("E_CCU_ENGINEERING_SCOPE_MISMATCH", f"manifest scope_ref {manifest.get('scope_ref')} does not match CCU bucket {ccu.get('bucket_id')}")
    if "CCU" not in manifest.get("downstream_consumers", []):
        fail("E_CCU_ENGINEERING_NOT_AUTHORIZED_CONSUMER", "manifest does not authorize CCU as a downstream technical consumer")

    receipt = compile_closure(request, manifest)
    if receipt["closure_status"] != "READY":
        blocker_codes = [item["code"] for item in receipt["blockers"]]
        fail("E_CCU_ENGINEERING_BLOCKED", f"technical engineering closure is BLOCKED: {blocker_codes}")

    similarity = validate_ccu(ccu)
    return {
        "status": "PASS",
        "bucket_id": ccu["bucket_id"],
        "engineering_closure_receipt_id": receipt["receipt_id"],
        "engineering_closure_digest": receipt["closure_digest"],
        "engineering_gate_count": receipt["counts"]["transitive_gate_count"],
        "source_item_status": receipt["source_item_status"],
        "similarity": similarity,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate CCU only after exact Physics engineering closure is READY")
    parser.add_argument("request")
    parser.add_argument("manifest")
    parser.add_argument("ccu")
    args = parser.parse_args()
    result = validate_engineered_ccu(load(args.request), load(args.manifest), load(args.ccu))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
