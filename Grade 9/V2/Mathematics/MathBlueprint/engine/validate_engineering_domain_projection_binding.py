#!/usr/bin/env python3
"""Validate exact custody between Engineering projection receipts and Domain registry.

This validator is deliberately independent of the projector's construction path.
A projection is acceptable only when its receipt, every projected registry asset,
and (when supplied) the final release summary all agree exactly.
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from project_engineering_to_domain_registry import digest
from validate_canonical_domain_registry import validate_registry

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
PROJECTION_SCHEMA = ROOT / "contracts" / "math-engineering-domain-projection.schema.json"

SOURCE_KIND_ASSET_TYPE = {
    "TECHNICAL_CORE": "CONCEPT",
    "MODEL_CONDITIONS": "MODEL",
    "MANDATORY_EQUATION": "EQUATION",
    "REPRESENTATION": "REPRESENTATION",
    "REASONING_STEP": "LEARNING_ATOM",
    "REQUIRED_TRANSFORMATION": "LEARNING_ATOM",
    "MISCONCEPTION": "MISCONCEPTION",
    "MANDATORY_VERIFICATION": "VERIFICATION_RULE",
    "PROBLEM_FAMILY": "PROBLEM_FAMILY",
}


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _receipt_digest(receipt: dict) -> str:
    return digest({k: v for k, v in receipt.items() if k != "projection_digest"})


def validate_projection_binding(registry: dict, receipt: dict) -> dict:
    validate_registry(registry)
    schema = json.loads(PROJECTION_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(receipt, schema)

    if receipt["projection_digest"] != _receipt_digest(receipt):
        fail("DOMAIN_PROJECTION_RECEIPT_DIGEST_INVALID")
    if receipt["domain_registry_ref"] != registry["registry_id"]:
        fail("DOMAIN_PROJECTION_REGISTRY_REF_DRIFT")

    projections = receipt["asset_projections"]
    if receipt["projected_asset_count"] != len(projections):
        fail("DOMAIN_PROJECTION_PROJECTED_COUNT_DRIFT")
    if receipt["base_asset_count"] + receipt["projected_asset_count"] != len(registry["assets"]):
        fail("DOMAIN_PROJECTION_TOTAL_ASSET_COUNT_DRIFT")

    direct = set(receipt["direct_gate_ids"])
    transitive = set(receipt["transitive_gate_ids"])
    if not direct <= transitive:
        fail("DOMAIN_PROJECTION_DIRECT_NOT_IN_TRANSITIVE_CLOSURE")

    assets = {row["asset_id"]: row for row in registry["assets"]}
    projected_ids = [row["asset_id"] for row in projections]
    if len(projected_ids) != len(set(projected_ids)):
        fail("DOMAIN_PROJECTION_RECEIPT_DUPLICATE_ASSET")
    registry_engineering_ids = {
        aid for aid in assets if aid.startswith("REG-MATH-ENG-")
    }
    if registry_engineering_ids != set(projected_ids):
        missing = sorted(set(projected_ids) - registry_engineering_ids)
        orphan = sorted(registry_engineering_ids - set(projected_ids))
        fail("DOMAIN_PROJECTION_ENGINEERING_ASSET_RECEIPT_DRIFT", f"missing={missing};orphan={orphan}")

    gates_with_assets: set[str] = set()
    prerequisite_rows = 0
    type_counts: dict[str, int] = {}
    for row in projections:
        aid = row["asset_id"]
        asset = assets.get(aid)
        if asset is None:
            fail("DOMAIN_PROJECTION_REGISTRY_ASSET_MISSING", aid)
        if digest(asset) != row["asset_digest"]:
            fail("DOMAIN_PROJECTION_ASSET_DIGEST_MISMATCH", aid)
        if asset["subtopic_id"] != row["subtopic_id"]:
            fail("DOMAIN_PROJECTION_ASSET_SUBTOPIC_DRIFT", aid)
        if sorted(asset.get("core1_refs", [])) != sorted(row["capability_refs"]):
            fail("DOMAIN_PROJECTION_ASSET_CAPABILITY_DRIFT", aid)
        if sorted(asset.get("core2_refs", [])) != sorted(row["core2_refs"]):
            fail("DOMAIN_PROJECTION_ASSET_CORE2_DRIFT", aid)

        source_kind = row["engineering_source_kind"]
        expected_type = SOURCE_KIND_ASSET_TYPE[source_kind]
        if asset["asset_type"] != expected_type:
            fail("DOMAIN_PROJECTION_SOURCE_KIND_TYPE_DRIFT", f"{aid}:{source_kind}!={asset['asset_type']}")
        type_counts[expected_type] = type_counts.get(expected_type, 0) + 1

        gate_id = row["engineering_gate_id"]
        gates_with_assets.add(gate_id)
        if gate_id not in transitive:
            fail("DOMAIN_PROJECTION_ASSET_GATE_OUTSIDE_CLOSURE", f"{aid}:{gate_id}")
        expected_role = "DIRECT" if gate_id in direct else "PREREQUISITE_CLOSURE"
        if row["engineering_gate_role"] != expected_role:
            fail("DOMAIN_PROJECTION_GATE_ROLE_DRIFT", f"{aid}:{expected_role}")
        if expected_role == "PREREQUISITE_CLOSURE":
            prerequisite_rows += 1

    if gates_with_assets != transitive:
        fail(
            "DOMAIN_PROJECTION_TRANSITIVE_GATE_ASSET_GAP",
            f"missing={sorted(transitive-gates_with_assets)};extra={sorted(gates_with_assets-transitive)}",
        )
    if transitive - direct and prerequisite_rows == 0:
        fail("DOMAIN_PROJECTION_PREREQUISITE_ASSETS_MISSING")

    return {
        "status": "PASS",
        "registry_asset_count": len(registry["assets"]),
        "projected_asset_count": len(projections),
        "direct_gate_count": len(direct),
        "transitive_gate_count": len(transitive),
        "prerequisite_projection_count": prerequisite_rows,
        "projected_asset_type_counts": dict(sorted(type_counts.items())),
    }


def validate_release_projection_binding(
    registry: dict,
    receipt: dict,
    summary: dict,
    full_engineering_audit: dict,
) -> dict:
    result = validate_projection_binding(registry, receipt)

    scalar_pairs = {
        "projection_id": (receipt["projection_id"], summary.get("engineering_domain_projection_ref")),
        "projection_digest": (receipt["projection_digest"], summary.get("engineering_domain_projection_digest")),
        "projected_asset_count": (receipt["projected_asset_count"], summary.get("engineering_domain_projected_asset_count")),
        "transitive_gate_count": (len(receipt["transitive_gate_ids"]), summary.get("engineering_domain_transitive_gate_count")),
        "registry_ref": (receipt["domain_registry_ref"], summary.get("registry_ref")),
        "crosswalk_ref": (receipt["crosswalk_ref"], summary.get("engineering_crosswalk_ref")),
    }
    for label, (expected, actual) in scalar_pairs.items():
        if expected != actual:
            fail("DOMAIN_PROJECTION_SUMMARY_BINDING_DRIFT", f"{label}:{expected}!={actual}")

    coverage_count = summary.get("release_gate", {}).get("coverage", {}).get("asset_count")
    if coverage_count != len(registry["assets"]) or summary.get("registry_asset_count") != len(registry["assets"]):
        fail("DOMAIN_PROJECTION_RELEASE_COVERAGE_COUNT_DRIFT")

    summary_coverage = summary.get("engineering_projection_coverage") or {}
    direct = set(receipt["direct_gate_ids"])
    if set(summary_coverage.get("required_engineering_gate_ids") or []) != direct:
        fail("DOMAIN_PROJECTION_SUMMARY_DIRECT_GATE_DRIFT")
    if set(full_engineering_audit.get("required_engineering_gate_ids") or []) != direct:
        fail("DOMAIN_PROJECTION_FULL_AUDIT_DIRECT_GATE_DRIFT")

    eng_digest = receipt["engineering_registry_digest"]
    if summary_coverage.get("engineering_registry_digest") != eng_digest:
        fail("DOMAIN_PROJECTION_SUMMARY_ENGINEERING_DIGEST_DRIFT")
    if full_engineering_audit.get("engineering_registry_digest") != eng_digest:
        fail("DOMAIN_PROJECTION_FULL_AUDIT_ENGINEERING_DIGEST_DRIFT")
    if full_engineering_audit.get("crosswalk_id") != receipt["crosswalk_ref"]:
        fail("DOMAIN_PROJECTION_FULL_AUDIT_CROSSWALK_DRIFT")

    if summary.get("release_gate", {}).get("status") != "PASS":
        fail("DOMAIN_PROJECTION_RELEASE_GATE_NOT_PASS")
    result["release_binding"] = "PASS"
    return result
