#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
sys.path.insert(0, str(ROOT / "engine"))
from compile_engineering_closure import load  # noqa: E402
from compile_engineering_readiness import compile_readiness  # noqa: E402
from validate_ccu_v2 import validate as validate_ccu  # noqa: E402


class EngineeringCCUError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise EngineeringCCUError(code, message)


def validate_engineered_ccu(
    request: dict,
    manifest: dict,
    ccu: dict,
    *,
    authority_receipts: list[dict] | None = None,
    authority_refs: list[str] | None = None,
) -> dict:
    if manifest.get("scope_kind") != "BUCKET":
        fail("E_CCU_ENGINEERING_SCOPE_KIND", "CCU engineering manifest must use scope_kind=BUCKET")
    if manifest.get("scope_ref") != ccu.get("bucket_id"):
        fail("E_CCU_ENGINEERING_SCOPE_MISMATCH", f"manifest scope_ref {manifest.get('scope_ref')} does not match CCU bucket {ccu.get('bucket_id')}")
    if "CCU" not in manifest.get("downstream_consumers", []):
        fail("E_CCU_ENGINEERING_NOT_AUTHORIZED_CONSUMER", "manifest does not authorize CCU as a downstream technical consumer")

    engineering, domain, envelope = compile_readiness(
        request,
        manifest,
        authority_receipts=authority_receipts or [],
        authority_refs=authority_refs or [],
    )
    permission = envelope["consumer_permissions"]["CCU"]
    if permission["status"] != "ALLOWED":
        fail("E_CCU_ENGINEERING_BLOCKED", f"aggregate engineering readiness blocks CCU: {permission['reason_codes']}")

    similarity = validate_ccu(ccu)
    return {
        "status": "PASS",
        "bucket_id": ccu["bucket_id"],
        "engineering_closure_receipt_id": engineering["receipt_id"],
        "engineering_closure_digest": engineering["closure_digest"],
        "domain_closure_receipt_id": domain["receipt_id"],
        "domain_closure_digest": domain["closure_digest"],
        "engineering_readiness_envelope_id": envelope["envelope_id"],
        "engineering_readiness_envelope_digest": envelope["envelope_digest"],
        "engineering_gate_count": engineering["counts"]["transitive_gate_count"],
        "source_item_status": engineering["source_item_status"],
        "similarity": similarity,
    }


def _authority_inputs(raw_refs: list[str]) -> tuple[list[dict], list[str]]:
    receipts, refs = [], []
    for raw in raw_refs:
        path = Path(raw).resolve()
        try:
            ref = path.relative_to(REPO).as_posix()
        except ValueError:
            fail("E_CCU_AUTHORITY_OUTSIDE_REPOSITORY", raw)
        refs.append(ref)
        receipts.append(json.loads(path.read_text(encoding="utf-8")))
    return receipts, refs


def main():
    parser = argparse.ArgumentParser(description="Validate CCU only after aggregate engineering readiness is ALLOWED")
    parser.add_argument("request")
    parser.add_argument("manifest")
    parser.add_argument("ccu")
    parser.add_argument("--authority", action="append", default=[])
    args = parser.parse_args()
    receipts, refs = _authority_inputs(args.authority)
    result = validate_engineered_ccu(
        load(args.request), load(args.manifest), load(args.ccu),
        authority_receipts=receipts, authority_refs=refs,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
