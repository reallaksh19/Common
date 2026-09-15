#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from assemble_product_governance_from_receipts import assemble
from engineering_product_custody import build_custody, custody_summary
from validate_product_governance import load


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def validate_engineering_custody(registry: dict, receipts: list[dict], current_custody: dict | None) -> None:
    if current_custody is None or current_custody.get("status") != "BOUND":
        fail("RELEASE_ENGINEERING_ADMISSION_REQUIRED")
    if current_custody.get("domain_registry_id") != registry.get("registry_id"):
        fail("RELEASE_ENGINEERING_DOMAIN_REGISTRY_ID_MISMATCH")
    for receipt in receipts:
        stamped = receipt.get("engineering_custody")
        if stamped is None:
            fail("RELEASE_ENGINEERING_CUSTODY_MISSING", receipt.get("receipt_id", "UNKNOWN"))
        if stamped.get("status") != "BOUND":
            fail("RELEASE_ENGINEERING_CUSTODY_UNBOUND", receipt.get("receipt_id", "UNKNOWN"))
        if stamped != current_custody:
            fail("RELEASE_ENGINEERING_CUSTODY_STALE_OR_DRIFT", receipt.get("receipt_id", "UNKNOWN"))


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

    source_asset_by_ref = {
        row["payload"]["question_ref"]: row["asset_id"]
        for row in registry["assets"]
        if row["asset_type"] == "SOURCE_QUESTION"
    }
    canonical_solution_by_question = {}
    for row in registry["assets"]:
        if row["asset_type"] != "CANONICAL_SOLUTION":
            continue
        qasset = row["payload"]["question_asset_ref"]
        qref = next((q for q, aid in source_asset_by_ref.items() if aid == qasset), None)
        if qref is None:
            fail("RELEASE_CANONICAL_SOLUTION_QUESTION_BINDING_MISSING", row["asset_id"])
        if qref in canonical_solution_by_question:
            fail("RELEASE_CANONICAL_SOLUTION_DUPLICATE", qref)
        canonical_solution_by_question[qref] = row["payload"]["answer_contract_ref"]

    for qref, frozen in expected.items():
        row = custody[qref]
        if row["source_relation"] != "EXACT_SOURCE":
            fail("RELEASE_FROZEN_SOURCE_RELATION_DRIFT", qref)
        if row["exact_stem_hash"] != frozen:
            fail("RELEASE_FROZEN_SOURCE_DIGEST_MISMATCH", qref)
        expected_answer = canonical_solution_by_question.get(qref)
        if expected_answer is None:
            fail("RELEASE_CANONICAL_SOLUTION_MISSING", qref)
        if row["answer_contract_ref"] != expected_answer:
            fail("RELEASE_CANONICAL_ANSWER_CONTRACT_MISMATCH", qref)


def release(
    registry: dict,
    receipts: list[dict],
    engineering_admission: dict | None = None,
    *,
    engineering_authorizations: dict[str, dict] | None = None,
    technical_registry: dict | None = None,
):
    if engineering_admission is None:
        fail("RELEASE_ENGINEERING_ADMISSION_REQUIRED")
    current_custody = build_custody(
        engineering_admission,
        registry,
        engineering_authorizations=engineering_authorizations,
        technical_registry=technical_registry,
    )
    validate_engineering_custody(registry, receipts, current_custody)
    coverage, similarity, governance, result = assemble(registry, receipts)
    validate_frozen_source_custody(registry, governance)
    result = dict(result)
    result["engineering_domain_authorization"] = {"status": "PASS", **custody_summary(current_custody)}
    result["frozen_source_custody"] = {"status": "PASS"}
    result["canonical_answer_custody"] = {"status": "PASS"}
    return coverage, similarity, governance, result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--engineering-admission", required=True)
    ap.add_argument("--receipt", action="append", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    registry = load(args.registry)
    engineering_admission = load(args.engineering_admission)
    receipts = [load(x) for x in args.receipt]
    coverage, similarity, governance, result = release(registry, receipts, engineering_admission)
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
