#!/usr/bin/env python3
"""Validate v2 Engineering->Domain canonical assets and scope memberships.

The validator is independent of canonicalization.  It proves one canonical registry
asset per exact Engineering source identity while re-deriving each local membership's
DIRECT/prerequisite role from the current Engineering graph and exact capability
crosswalk.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import jsonschema

from compile_mathematics_engineering_workbench import digest as engineering_digest
from project_engineering_to_domain_registry import _closure, _gate_index, digest
from validate_canonical_domain_registry import validate_registry

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SCHEMA = ROOT / "contracts" / "math-engineering-domain-projection-v2.schema.json"


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _without_digest(row: dict, field: str) -> dict:
    return {k: v for k, v in row.items() if k != field}


def _source_key(row: dict) -> tuple[str, str, str]:
    return (
        row["engineering_gate_id"],
        row["engineering_source_kind"],
        row["engineering_source_ref"],
    )


def validate_projection_binding_v2(
    registry: dict,
    receipt: dict,
    *,
    engineering_registry: dict | None = None,
    projection_coverage: dict | None = None,
) -> dict:
    validate_registry(registry)
    jsonschema.validate(receipt, json.loads(SCHEMA.read_text(encoding="utf-8")))
    if receipt["projection_digest"] != digest(_without_digest(receipt, "projection_digest")):
        fail("DOMAIN_PROJECTION_V2_RECEIPT_DIGEST_INVALID")
    if receipt["domain_registry_ref"] != registry["registry_id"]:
        fail("DOMAIN_PROJECTION_V2_REGISTRY_REF_DRIFT")

    canonical_rows = receipt["canonical_assets"]
    memberships = receipt["scope_memberships"]
    if receipt["projected_asset_count"] != len(canonical_rows):
        fail("DOMAIN_PROJECTION_V2_CANONICAL_COUNT_DRIFT")
    if receipt["scope_membership_count"] != len(memberships):
        fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_COUNT_DRIFT")
    if receipt["expanded_projected_asset_count"] != len(memberships):
        fail("DOMAIN_PROJECTION_V2_EXPANDED_MEMBERSHIP_COUNT_DRIFT")
    if receipt["base_asset_count"] + receipt["projected_asset_count"] != len(registry["assets"]):
        fail("DOMAIN_PROJECTION_V2_TOTAL_ASSET_COUNT_DRIFT")

    assets = {row["asset_id"]: row for row in registry["assets"]}
    canonical_by_id = {row["asset_id"]: row for row in canonical_rows}
    if len(canonical_by_id) != len(canonical_rows):
        fail("DOMAIN_PROJECTION_V2_CANONICAL_ASSET_ID_DUPLICATE")
    source_keys = [_source_key(row) for row in canonical_rows]
    if len(source_keys) != len(set(source_keys)):
        fail("DOMAIN_PROJECTION_V2_SOURCE_IDENTITY_DUPLICATE")

    registry_projected = {aid for aid in assets if aid.startswith("REG-MATH-ENG-")}
    if registry_projected != set(canonical_by_id):
        fail(
            "DOMAIN_PROJECTION_V2_REGISTRY_CANONICAL_SET_DRIFT",
            f"missing={sorted(set(canonical_by_id)-registry_projected)};orphan={sorted(registry_projected-set(canonical_by_id))}",
        )

    membership_ids = [row["membership_id"] for row in memberships]
    if len(membership_ids) != len(set(membership_ids)):
        fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_ID_DUPLICATE")
    by_asset: dict[str, list[dict]] = defaultdict(list)
    join_refs = set(registry["join_refs"])
    for member in memberships:
        if member["membership_digest"] != digest(_without_digest(member, "membership_digest")):
            fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_DIGEST_INVALID", member["membership_id"])
        if member["asset_ref"] not in canonical_by_id:
            fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_ASSET_UNKNOWN", member["membership_id"])
        if member["join_ref"] not in join_refs:
            fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_JOIN_UNKNOWN", member["membership_id"])
        canonical_row = canonical_by_id[member["asset_ref"]]
        if canonical_row["engineering_gate_id"] != member["engineering_gate_id"]:
            fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_GATE_DRIFT", member["membership_id"])
        by_asset[member["asset_ref"]].append(member)

    prerequisite_memberships = 0
    for asset_id, row in canonical_by_id.items():
        asset = assets.get(asset_id)
        if asset is None:
            fail("DOMAIN_PROJECTION_V2_REGISTRY_ASSET_MISSING", asset_id)
        if digest(asset) != row["asset_digest"]:
            fail("DOMAIN_PROJECTION_V2_ASSET_DIGEST_MISMATCH", asset_id)
        members = sorted(
            by_asset.get(asset_id, []),
            key=lambda x: (x["subtopic_id"], x["join_ref"], x["membership_id"]),
        )
        if not members:
            fail("DOMAIN_PROJECTION_V2_ASSET_MEMBERSHIP_MISSING", asset_id)
        if set(row["membership_refs"]) != {x["membership_id"] for x in members}:
            fail("DOMAIN_PROJECTION_V2_ASSET_MEMBERSHIP_REF_DRIFT", asset_id)
        primary = members[0]
        if row["primary_subtopic_id"] != primary["subtopic_id"] or row["primary_join_ref"] != primary["join_ref"]:
            fail("DOMAIN_PROJECTION_V2_PRIMARY_MEMBERSHIP_DRIFT", asset_id)
        if asset["subtopic_id"] != primary["subtopic_id"] or asset["join_ref"] != primary["join_ref"]:
            fail("DOMAIN_PROJECTION_V2_COMPATIBILITY_ANCHOR_DRIFT", asset_id)
        cap_union = sorted({ref for x in members for ref in x["capability_refs"]})
        core2_union = sorted({ref for x in members for ref in x["core2_refs"]})
        if row["capability_refs"] != cap_union or asset["core1_refs"] != cap_union:
            fail("DOMAIN_PROJECTION_V2_CAPABILITY_UNION_DRIFT", asset_id)
        if row["core2_refs"] != core2_union or asset["core2_refs"] != core2_union:
            fail("DOMAIN_PROJECTION_V2_CORE2_UNION_DRIFT", asset_id)
        if core2_union and asset["authority_class"] != "DUAL_VALIDATED":
            fail("DOMAIN_PROJECTION_V2_DUAL_AUTHORITY_MISSING", asset_id)
        prerequisite_memberships += sum(1 for x in members if x["engineering_gate_role"] == "PREREQUISITE_CLOSURE")

    if set(by_asset) != set(canonical_by_id):
        fail("DOMAIN_PROJECTION_V2_ORPHAN_MEMBERSHIP_SET")
    if set(receipt["direct_gate_ids"]) - set(receipt["transitive_gate_ids"]):
        fail("DOMAIN_PROJECTION_V2_DIRECT_OUTSIDE_TRANSITIVE")

    if engineering_registry is not None or projection_coverage is not None:
        if engineering_registry is None or projection_coverage is None:
            fail("DOMAIN_PROJECTION_V2_ROLE_REVALIDATION_INPUT_INCOMPLETE")
        if engineering_digest(engineering_registry) != receipt["engineering_registry_digest"]:
            fail("DOMAIN_PROJECTION_V2_ENGINEERING_REGISTRY_DIGEST_DRIFT")
        if projection_coverage.get("crosswalk_id") != receipt["crosswalk_ref"]:
            fail("DOMAIN_PROJECTION_V2_CROSSWALK_REF_DRIFT")
        gates = _gate_index(engineering_registry)
        cap_gate_map = projection_coverage.get("capability_gate_map") or {}
        closure_cache: dict[str, list[str]] = {}
        all_direct: set[str] = set()
        all_transitive: set[str] = set()
        for member in memberships:
            direct: set[str] = set()
            for cap in member["capability_refs"]:
                refs = cap_gate_map.get(cap)
                if not refs:
                    fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_CAPABILITY_UNMAPPED", f"{member['membership_id']}:{cap}")
                direct.update(refs)
            transitive: set[str] = set()
            for gate_id in direct:
                transitive.update(_closure(gates, gate_id, closure_cache))
            member_gate = member["engineering_gate_id"]
            if member_gate not in transitive:
                fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_GATE_OUTSIDE_LOCAL_CLOSURE", member["membership_id"])
            expected_role = "DIRECT" if member_gate in direct else "PREREQUISITE_CLOSURE"
            if member["engineering_gate_role"] != expected_role:
                fail("DOMAIN_PROJECTION_V2_LOCAL_ROLE_DRIFT", f"{member['membership_id']}:{expected_role}")
            all_direct.update(direct)
            all_transitive.update(transitive)
        if all_direct != set(receipt["direct_gate_ids"]):
            fail("DOMAIN_PROJECTION_V2_DIRECT_GATE_SET_DRIFT")
        if all_transitive != set(receipt["transitive_gate_ids"]):
            fail("DOMAIN_PROJECTION_V2_TRANSITIVE_GATE_SET_DRIFT")

    return {
        "status": "PASS",
        "registry_asset_count": len(registry["assets"]),
        "base_asset_count": receipt["base_asset_count"],
        "canonical_projected_asset_count": len(canonical_rows),
        "scope_membership_count": len(memberships),
        "deduplicated_scope_copy_count": len(memberships) - len(canonical_rows),
        "direct_gate_count": len(receipt["direct_gate_ids"]),
        "transitive_gate_count": len(receipt["transitive_gate_ids"]),
        "prerequisite_membership_count": prerequisite_memberships,
    }


def validate_release_projection_binding_v2(
    registry: dict,
    receipt: dict,
    summary: dict,
    full_engineering_audit: dict,
    *,
    engineering_registry: dict,
    projection_coverage: dict,
) -> dict:
    result = validate_projection_binding_v2(
        registry,
        receipt,
        engineering_registry=engineering_registry,
        projection_coverage=projection_coverage,
    )
    scalar_pairs = {
        "projection_id": (receipt["projection_id"], summary.get("engineering_domain_projection_ref")),
        "projection_digest": (receipt["projection_digest"], summary.get("engineering_domain_projection_digest")),
        "projected_asset_count": (receipt["projected_asset_count"], summary.get("engineering_domain_projected_asset_count")),
        "scope_membership_count": (receipt["scope_membership_count"], summary.get("engineering_domain_scope_membership_count")),
        "base_asset_count": (receipt["base_asset_count"], summary.get("engineering_domain_base_asset_count")),
        "transitive_gate_count": (len(receipt["transitive_gate_ids"]), summary.get("engineering_domain_transitive_gate_count")),
        "registry_ref": (receipt["domain_registry_ref"], summary.get("registry_ref")),
        "crosswalk_ref": (receipt["crosswalk_ref"], summary.get("engineering_crosswalk_ref")),
    }
    for label, (expected, actual) in scalar_pairs.items():
        if expected != actual:
            fail("DOMAIN_PROJECTION_V2_SUMMARY_BINDING_DRIFT", f"{label}:{expected}!={actual}")
    coverage_count = summary.get("release_gate", {}).get("coverage", {}).get("asset_count")
    if coverage_count != len(registry["assets"]) or summary.get("registry_asset_count") != len(registry["assets"]):
        fail("DOMAIN_PROJECTION_V2_RELEASE_COVERAGE_COUNT_DRIFT")
    summary_coverage = summary.get("engineering_projection_coverage") or {}
    direct = set(receipt["direct_gate_ids"])
    if set(summary_coverage.get("required_engineering_gate_ids") or []) != direct:
        fail("DOMAIN_PROJECTION_V2_SUMMARY_DIRECT_GATE_DRIFT")
    if set(full_engineering_audit.get("required_engineering_gate_ids") or []) != direct:
        fail("DOMAIN_PROJECTION_V2_FULL_AUDIT_DIRECT_GATE_DRIFT")
    eng_digest = receipt["engineering_registry_digest"]
    if summary_coverage.get("engineering_registry_digest") != eng_digest:
        fail("DOMAIN_PROJECTION_V2_SUMMARY_ENGINEERING_DIGEST_DRIFT")
    if full_engineering_audit.get("engineering_registry_digest") != eng_digest:
        fail("DOMAIN_PROJECTION_V2_FULL_AUDIT_ENGINEERING_DIGEST_DRIFT")
    if full_engineering_audit.get("crosswalk_id") != receipt["crosswalk_ref"]:
        fail("DOMAIN_PROJECTION_V2_FULL_AUDIT_CROSSWALK_DRIFT")
    if summary.get("release_gate", {}).get("status") != "PASS":
        fail("DOMAIN_PROJECTION_V2_RELEASE_GATE_NOT_PASS")
    result["release_binding"] = "PASS"
    return result
