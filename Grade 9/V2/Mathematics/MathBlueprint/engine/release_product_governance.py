#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from assemble_product_governance_from_receipts import assemble
from validate_product_governance import load


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def validate_frozen_source_custody(registry: dict, governance: dict) -> None:
    expected = {
        row["payload"]["question_ref"]: row["payload"]["frozen_digest"]
        for row in registry["assets"]
        if row["asset_type"] == "SOURCE_QUESTION"
    }
    custody = {
        row["source_question_no"]: row
        for row in governance["question_custody"]
        if row["origin"] == "SOURCE_CORE2"
    }
    missing = sorted(set(expected) - set(custody))
    if missing:
        fail("RELEASE_FROZEN_SOURCE_CUSTODY_MISSING", ",".join(missing))
    for qref, frozen in expected.items():
        row = custody[qref]
        if row["source_relation"] != "EXACT_SOURCE":
            fail("RELEASE_FROZEN_SOURCE_RELATION_DRIFT", qref)
        if row["exact_stem_hash"] != frozen:
            fail("RELEASE_FROZEN_SOURCE_DIGEST_MISMATCH", qref)


def release(registry: dict, receipts: list[dict]):
    coverage, similarity, governance, result = assemble(registry, receipts)
    validate_frozen_source_custody(registry, governance)
    result = dict(result)
    result["frozen_source_custody"] = {"status": "PASS"}
    return coverage, similarity, governance, result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--receipt", action="append", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    registry = load(args.registry)
    receipts = [load(x) for x in args.receipt]
    coverage, similarity, governance, result = release(registry, receipts)
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    for name, obj in (
        ("core_coverage_ledger.json", coverage),
        ("cross_core_similarity_audit.json", similarity),
        ("product_governance_audit.json", governance),
        ("product_release_gate.json", result),
    ):
        (out / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
