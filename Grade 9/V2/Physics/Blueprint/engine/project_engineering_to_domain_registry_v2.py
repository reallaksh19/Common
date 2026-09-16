#!/usr/bin/env python3
"""Canonicalize Engineering-derived Domain assets and separate local scope membership.

v1 projection intentionally materializes one Engineering source object per teaching
subtopic.  This v2 layer preserves that proven materializer, then folds those local
copies by exact Engineering source identity:

    (engineering_gate_id, engineering_source_kind, engineering_source_ref)

The Canonical Domain Registry receives one asset per source identity.  Run-local
subtopic/join/capability/question bindings and DIRECT-vs-PREREQUISITE roles live in
an exact, digest-bound scope-membership ledger in the v2 projection receipt.
"""
from __future__ import annotations

import copy
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import jsonschema

from project_engineering_to_domain_registry import (
    digest,
    project_engineering_to_domain_registry as project_expanded,
)
from validate_canonical_domain_registry import validate_registry

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SCHEMA = ROOT / "contracts" / "physics-engineering-domain-projection-v2.schema.json"


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _source_key(row: dict) -> tuple[str, str, str]:
    return (
        row["engineering_gate_id"],
        row["engineering_source_kind"],
        row["engineering_source_ref"],
    )


def _canonical_asset_id(row: dict, asset_type: str) -> str:
    token = digest([asset_type, *_source_key(row)])[:20].upper()
    return f"REG-PHY-ENG-{asset_type}-{token}"


def _rewrite_refs(value: Any, old_to_new: dict[str, str]) -> Any:
    if isinstance(value, str):
        return old_to_new.get(value, value)
    if isinstance(value, list):
        return [_rewrite_refs(x, old_to_new) for x in value]
    if isinstance(value, dict):
        return {k: _rewrite_refs(v, old_to_new) for k, v in value.items()}
    return value


def _membership(
    row: dict,
    old_asset: dict,
    canonical_asset_id: str,
) -> dict:
    payload = {
        "membership_id": "",
        "asset_ref": canonical_asset_id,
        "subtopic_id": row["subtopic_id"],
        "join_ref": old_asset["join_ref"],
        "engineering_gate_id": row["engineering_gate_id"],
        "engineering_gate_role": row["engineering_gate_role"],
        "capability_refs": sorted(set(row["capability_refs"])),
        "core2_refs": sorted(set(row["core2_refs"])),
    }
    payload["membership_id"] = "PHY-ENG-SCOPE-MEMBER-" + digest(payload)[:20].upper()
    payload["membership_digest"] = digest(payload)
    return payload


def _asset_semantic_material(asset: dict) -> dict:
    """Material that must be identical for one Engineering source object.

    Local bindings and the derived authority class are excluded.  PROBLEM_FAMILY
    required-capability bindings are local projection metadata and are merged below.
    """
    out = copy.deepcopy(asset)
    for key in (
        "asset_id", "subtopic_id", "join_ref", "core1_refs", "core2_refs",
        "authority_class", "provenance_note",
    ):
        out.pop(key, None)
    if out.get("asset_type") == "PROBLEM_FAMILY":
        out.get("payload", {}).pop("required_capability_refs", None)
    return out


def canonicalize_expanded_projection(
    expanded_registry: dict,
    expanded_receipt: dict,
) -> tuple[dict, dict]:
    validate_registry(expanded_registry)
    old_rows = list(expanded_receipt["asset_projections"])
    old_assets = {row["asset_id"]: row for row in expanded_registry["assets"]}
    projected_old_ids = {row["asset_id"] for row in old_rows}
    if len(projected_old_ids) != len(old_rows):
        fail("DOMAIN_PROJECTION_V2_EXPANDED_ASSET_DUPLICATE")

    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in old_rows:
        grouped[_source_key(row)].append(row)

    old_to_new: dict[str, str] = {}
    for key, rows in grouped.items():
        sample = old_assets.get(rows[0]["asset_id"])
        if sample is None:
            fail("DOMAIN_PROJECTION_V2_EXPANDED_ASSET_MISSING", rows[0]["asset_id"])
        new_id = _canonical_asset_id(rows[0], sample["asset_type"])
        for row in rows:
            old_to_new[row["asset_id"]] = new_id

    canonical_assets: list[dict] = []
    canonical_rows: list[dict] = []
    memberships: list[dict] = []

    for source_key in sorted(grouped):
        rows = grouped[source_key]
        old_group_assets = []
        group_memberships = []
        for row in rows:
            old_asset = old_assets.get(row["asset_id"])
            if old_asset is None:
                fail("DOMAIN_PROJECTION_V2_EXPANDED_ASSET_MISSING", row["asset_id"])
            rewritten = _rewrite_refs(old_asset, old_to_new)
            old_group_assets.append(rewritten)
            group_memberships.append(_membership(row, old_asset, old_to_new[row["asset_id"]]))

        semantic_materials = {
            json.dumps(_asset_semantic_material(x), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            for x in old_group_assets
        }
        if len(semantic_materials) != 1:
            fail("DOMAIN_PROJECTION_V2_SOURCE_SEMANTIC_DRIFT", ":".join(source_key))

        group_memberships = sorted(
            group_memberships,
            key=lambda x: (x["subtopic_id"], x["join_ref"], x["membership_id"]),
        )
        if len({x["membership_id"] for x in group_memberships}) != len(group_memberships):
            fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_DUPLICATE", ":".join(source_key))
        primary = group_memberships[0]

        canonical = copy.deepcopy(old_group_assets[0])
        canonical["asset_id"] = primary["asset_ref"]
        canonical["subtopic_id"] = primary["subtopic_id"]
        canonical["join_ref"] = primary["join_ref"]
        canonical["core1_refs"] = sorted({
            ref for member in group_memberships for ref in member["capability_refs"]
        })
        canonical["core2_refs"] = sorted({
            ref for member in group_memberships for ref in member["core2_refs"]
        })
        if canonical["core2_refs"]:
            canonical["authority_class"] = "DUAL_VALIDATED"
        else:
            authorities = {x["authority_class"] for x in old_group_assets}
            if len(authorities) != 1:
                fail("DOMAIN_PROJECTION_V2_AUTHORITY_DRIFT", ":".join(source_key))
            canonical["authority_class"] = next(iter(authorities))

        if canonical["asset_type"] == "PROBLEM_FAMILY":
            required_caps = sorted({
                ref
                for asset in old_group_assets
                for ref in asset["payload"].get("required_capability_refs", [])
            })
            canonical["payload"]["required_capability_refs"] = required_caps

        canonical["depends_on"] = sorted(set(canonical.get("depends_on", [])))
        canonical["provenance_note"] = (
            "Canonical Engineering-derived Domain asset; exact source identity="
            f"{source_key[0]}::{source_key[1]}::{source_key[2]}. "
            "Teaching-scope membership and DIRECT/prerequisite role are custodied "
            "separately in the Engineering Domain Projection v2 receipt."
        )
        canonical_assets.append(canonical)
        memberships.extend(group_memberships)
        canonical_rows.append({
            "asset_id": canonical["asset_id"],
            "engineering_gate_id": source_key[0],
            "engineering_source_kind": source_key[1],
            "engineering_source_ref": source_key[2],
            "primary_subtopic_id": primary["subtopic_id"],
            "primary_join_ref": primary["join_ref"],
            "capability_refs": canonical["core1_refs"],
            "core2_refs": canonical["core2_refs"],
            "membership_refs": [x["membership_id"] for x in group_memberships],
            "asset_digest": digest(canonical),
        })

    base_assets = [
        copy.deepcopy(row) for row in expanded_registry["assets"]
        if row["asset_id"] not in projected_old_ids
    ]
    rich_registry = copy.deepcopy(expanded_registry)
    rich_registry["assets"] = base_assets + sorted(canonical_assets, key=lambda x: x["asset_id"])
    validate_registry(rich_registry)

    memberships = sorted(memberships, key=lambda x: x["membership_id"])
    canonical_rows = sorted(canonical_rows, key=lambda x: x["asset_id"])
    receipt = {
        "schema_version": "2.0.0",
        "subject": "PHYSICS",
        "projection_id": "",
        "domain_registry_ref": rich_registry["registry_id"],
        "engineering_registry_id": expanded_receipt["engineering_registry_id"],
        "engineering_registry_digest": expanded_receipt["engineering_registry_digest"],
        "crosswalk_ref": expanded_receipt["crosswalk_ref"],
        "base_asset_count": len(base_assets),
        "projected_asset_count": len(canonical_rows),
        "scope_membership_count": len(memberships),
        "expanded_projection_digest": expanded_receipt["projection_digest"],
        "expanded_projected_asset_count": expanded_receipt["projected_asset_count"],
        "direct_gate_ids": list(expanded_receipt["direct_gate_ids"]),
        "transitive_gate_ids": list(expanded_receipt["transitive_gate_ids"]),
        "canonical_assets": canonical_rows,
        "scope_memberships": memberships,
        "projection_digest": "",
    }
    receipt["projection_id"] = "PHY-ENG-DOMAIN-PROJ-V2-" + digest({
        "registry": receipt["domain_registry_ref"],
        "engineering": receipt["engineering_registry_digest"],
        "crosswalk": receipt["crosswalk_ref"],
        "assets": canonical_rows,
        "memberships": memberships,
    })[:16].upper()
    receipt["projection_digest"] = digest({k: v for k, v in receipt.items() if k != "projection_digest"})
    jsonschema.validate(receipt, json.loads(SCHEMA.read_text(encoding="utf-8")))

    if receipt["scope_membership_count"] != receipt["expanded_projected_asset_count"]:
        fail("DOMAIN_PROJECTION_V2_MEMBERSHIP_EXPANSION_COUNT_DRIFT")
    if receipt["projected_asset_count"] >= receipt["scope_membership_count"]:
        fail("DOMAIN_PROJECTION_V2_CANONICALIZATION_NOT_EFFECTIVE")
    return rich_registry, receipt


def project_engineering_to_domain_registry_v2(
    base_registry: dict,
    *,
    engineering_registry: dict,
    projection_coverage: dict,
    bucket_plan: dict,
    bucket_sid: dict[str, str],
    core2_pages: list[dict],
) -> tuple[dict, dict]:
    expanded_registry, expanded_receipt = project_expanded(
        base_registry,
        engineering_registry=engineering_registry,
        projection_coverage=projection_coverage,
        bucket_plan=bucket_plan,
        bucket_sid=bucket_sid,
        core2_pages=core2_pages,
    )
    return canonicalize_expanded_projection(expanded_registry, expanded_receipt)
