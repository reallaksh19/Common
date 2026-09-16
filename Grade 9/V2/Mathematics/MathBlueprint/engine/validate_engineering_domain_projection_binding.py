#!/usr/bin/env python3
"""Validate exact custody between Engineering projection receipts and Domain registry.

Global gate membership and local gate role are intentionally distinct. A gate may
be direct authority for one teaching subtopic while appearing only through
prerequisite closure for another. Release validation therefore reconstructs each
subtopic's exact AssessmentScope capability set, resolves its exact Engineering
scope, recomputes prerequisite closure from the current Engineering graph, and
then validates every projected asset in that local context.
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from compile_mathematics_engineering_workbench import digest as engineering_digest
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


def _engineering_gate_index(engineering_registry: dict) -> dict[str, dict]:
    return {row["subtopic_id"]: row for row in engineering_registry.get("subtopic_gates", [])}


def _engineering_closure(gates: dict[str, dict], direct_gate_ids: set[str]) -> set[str]:
    out: set[str] = set()
    visiting: set[str] = set()

    def walk(gate_id: str) -> None:
        if gate_id in out:
            return
        if gate_id in visiting:
            fail("DOMAIN_PROJECTION_ENGINEERING_CYCLE", gate_id)
        gate = gates.get(gate_id)
        if gate is None:
            fail("DOMAIN_PROJECTION_ENGINEERING_GATE_UNKNOWN", gate_id)
        visiting.add(gate_id)
        for prereq in gate.get("prerequisite_ids", []):
            if prereq not in gates:
                fail("DOMAIN_PROJECTION_ENGINEERING_PREREQUISITE_UNKNOWN", f"{gate_id}:{prereq}")
            walk(prereq)
        visiting.remove(gate_id)
        out.add(gate_id)

    for gate_id in direct_gate_ids:
        walk(gate_id)
    return out


def validate_projection_binding(registry: dict, receipt: dict, engineering_registry: dict) -> dict:
    validate_registry(registry)
    schema = json.loads(PROJECTION_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(receipt, schema)

    if receipt["projection_digest"] != _receipt_digest(receipt):
        fail("DOMAIN_PROJECTION_RECEIPT_DIGEST_INVALID")
    if receipt["domain_registry_ref"] != registry["registry_id"]:
        fail("DOMAIN_PROJECTION_REGISTRY_REF_DRIFT")
    if receipt["engineering_registry_id"] != engineering_registry.get("registry_id"):
        fail("DOMAIN_PROJECTION_ENGINEERING_REGISTRY_REF_DRIFT")
    if receipt["engineering_registry_digest"] != engineering_digest(engineering_registry):
        fail("DOMAIN_PROJECTION_ENGINEERING_REGISTRY_DIGEST_DRIFT")

    projections = receipt["asset_projections"]
    if receipt["projected_asset_count"] != len(projections):
        fail("DOMAIN_PROJECTION_PROJECTED_COUNT_DRIFT")
    if receipt["base_asset_count"] + receipt["projected_asset_count"] != len(registry["assets"]):
        fail("DOMAIN_PROJECTION_TOTAL_ASSET_COUNT_DRIFT")

    direct = set(receipt["direct_gate_ids"])
    transitive = set(receipt["transitive_gate_ids"])
    if not direct <= transitive:
        fail("DOMAIN_PROJECTION_DIRECT_NOT_IN_TRANSITIVE_CLOSURE")
    gates = _engineering_gate_index(engineering_registry)
    if _engineering_closure(gates, direct) != transitive:
        fail("DOMAIN_PROJECTION_GLOBAL_TRANSITIVE_CLOSURE_DRIFT")

    assets = {row["asset_id"]: row for row in registry["assets"]}
    projected_ids = [row["asset_id"] for row in projections]
    if len(projected_ids) != len(set(projected_ids)):
        fail("DOMAIN_PROJECTION_RECEIPT_DUPLICATE_ASSET")
    registry_engineering_ids = {aid for aid in assets if aid.startswith("REG-MATH-ENG-")}
    if registry_engineering_ids != set(projected_ids):
        missing = sorted(set(projected_ids) - registry_engineering_ids)
        orphan = sorted(registry_engineering_ids - set(projected_ids))
        fail("DOMAIN_PROJECTION_ENGINEERING_ASSET_RECEIPT_DRIFT", f"missing={missing};orphan={orphan}")

    gates_with_assets: set[str] = set()
    direct_rows: set[str] = set()
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
        role = row["engineering_gate_role"]
        gates_with_assets.add(gate_id)
        if gate_id not in transitive:
            fail("DOMAIN_PROJECTION_ASSET_GATE_OUTSIDE_CLOSURE", f"{aid}:{gate_id}")
        if role == "DIRECT":
            if gate_id not in direct:
                fail("DOMAIN_PROJECTION_DIRECT_ROLE_OUTSIDE_GLOBAL_DIRECT_SET", f"{aid}:{gate_id}")
            direct_rows.add(gate_id)
        elif role == "PREREQUISITE_CLOSURE":
            prerequisite_rows += 1
        else:  # schema normally catches this, retained as a stable semantic failure.
            fail("DOMAIN_PROJECTION_GATE_ROLE_INVALID", f"{aid}:{role}")

    if gates_with_assets != transitive:
        fail(
            "DOMAIN_PROJECTION_TRANSITIVE_GATE_ASSET_GAP",
            f"missing={sorted(transitive-gates_with_assets)};extra={sorted(gates_with_assets-transitive)}",
        )
    if direct_rows != direct:
        fail("DOMAIN_PROJECTION_DIRECT_GATE_ASSET_GAP", f"missing={sorted(direct-direct_rows)}")
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


def _subtopic_capability_sets(registry: dict) -> dict[str, frozenset[str]]:
    out: dict[str, set[str]] = {}
    for asset in registry["assets"]:
        if asset["asset_type"] != "CAPABILITY":
            continue
        out.setdefault(asset["subtopic_id"], set()).update(asset.get("core1_refs", []))
    return {sid: frozenset(refs) for sid, refs in out.items() if refs}


def validate_release_projection_binding(
    registry: dict,
    receipt: dict,
    summary: dict,
    full_engineering_audit: dict,
    engineering_registry: dict,
) -> dict:
    result = validate_projection_binding(registry, receipt, engineering_registry)

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

    bucket_rows = full_engineering_audit.get("bucket_gate_map") or []
    scope_by_caps: dict[frozenset[str], dict] = {}
    for bucket in bucket_rows:
        caps = frozenset(bucket.get("capability_refs") or [])
        if not caps:
            fail("DOMAIN_PROJECTION_FULL_AUDIT_BUCKET_CAPABILITIES_EMPTY", str(bucket.get("bucket_id")))
        if caps in scope_by_caps:
            fail("DOMAIN_PROJECTION_FULL_AUDIT_BUCKET_CAPABILITY_SET_AMBIGUOUS", ",".join(sorted(caps)))
        scope_by_caps[caps] = bucket

    subtopic_caps = _subtopic_capability_sets(registry)
    gates = _engineering_gate_index(engineering_registry)
    projected_by_subtopic: dict[str, list[dict]] = {}
    for row in receipt["asset_projections"]:
        projected_by_subtopic.setdefault(row["subtopic_id"], []).append(row)

    recomputed_direct: set[str] = set()
    recomputed_transitive: set[str] = set()
    locally_prerequisite_rows = 0
    for sid, rows in projected_by_subtopic.items():
        caps = subtopic_caps.get(sid)
        if not caps:
            fail("DOMAIN_PROJECTION_SUBTOPIC_CAPABILITY_BINDING_MISSING", sid)
        bucket = scope_by_caps.get(caps)
        if bucket is None:
            fail("DOMAIN_PROJECTION_SUBTOPIC_BUCKET_MATCH_MISSING", f"{sid}:{sorted(caps)}")
        local_direct = set(bucket.get("engineering_gate_ids") or [])
        if not local_direct:
            fail("DOMAIN_PROJECTION_SUBTOPIC_DIRECT_GATE_SET_EMPTY", sid)
        local_closure = _engineering_closure(gates, local_direct)
        actual_gates = {row["engineering_gate_id"] for row in rows}
        if actual_gates != local_closure:
            fail(
                "DOMAIN_PROJECTION_SUBTOPIC_CLOSURE_DRIFT",
                f"{sid}:missing={sorted(local_closure-actual_gates)};extra={sorted(actual_gates-local_closure)}",
            )
        for row in rows:
            gate_id = row["engineering_gate_id"]
            expected_role = "DIRECT" if gate_id in local_direct else "PREREQUISITE_CLOSURE"
            if row["engineering_gate_role"] != expected_role:
                fail("DOMAIN_PROJECTION_GATE_ROLE_DRIFT", f"{row['asset_id']}:{expected_role}")
            if expected_role == "PREREQUISITE_CLOSURE":
                locally_prerequisite_rows += 1
        recomputed_direct.update(local_direct)
        recomputed_transitive.update(local_closure)

    if recomputed_direct != set(receipt["direct_gate_ids"]):
        fail("DOMAIN_PROJECTION_RECOMPUTED_DIRECT_GATE_DRIFT")
    if recomputed_transitive != set(receipt["transitive_gate_ids"]):
        fail("DOMAIN_PROJECTION_RECOMPUTED_TRANSITIVE_GATE_DRIFT")

    if summary.get("release_gate", {}).get("status") != "PASS":
        fail("DOMAIN_PROJECTION_RELEASE_GATE_NOT_PASS")
    result["release_binding"] = "PASS"
    result["locally_prerequisite_projection_count"] = locally_prerequisite_rows
    return result
