#!/usr/bin/env python3
"""Multi-bucket-safe entrypoint for the Engineering-bound four-producer golden.

The Engineering-bound runner owns authority projection, current Engineering
admission, producer execution and strict release. This entrypoint supplies two
canonical storage rules discovered by the real cold-start corpus:

1. a source question may participate in multiple teaching buckets while the Domain
   Registry stores it under one deterministic primary subtopic; and
2. one Engineering source object must exist only once in the Canonical Domain
   Registry even when it participates in many teaching scopes.

Engineering-derived mathematical truth is therefore canonicalized by exact source
identity.  Local subtopic/join/capability/question bindings and DIRECT-vs-prerequisite
roles are retained in a digest-bound scope-membership ledger and are independently
revalidated against the current Engineering graph before release.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import run_engineering_bound_producer_release_golden as base
from project_engineering_to_domain_registry_v2 import project_engineering_to_domain_registry_v2
from validate_engineering_domain_projection_binding_v2 import validate_release_projection_binding_v2

_LAST_ENGINEERING_DOMAIN_PROJECTION = None
_LAST_ENGINEERING_REGISTRY = None
_LAST_ENGINEERING_PROJECTION_COVERAGE = None
_ORIGINAL_BUILD_REGISTRY = base.legacy.build_registry


def multi_bucket_safe_subtopics(bucket_plan: dict):
    bucket_sid = {}
    cap_sid = {}
    q_sid = {}
    for bucket in bucket_plan["buckets"]:
        sid = "BOUND-SUB-" + base.production_digest(sorted(bucket["member_capability_refs"]))[:12].upper()
        bucket_sid[bucket["bucket_id"]] = sid
        for cap in bucket["member_capability_refs"]:
            if cap in cap_sid and cap_sid[cap] != sid:
                base.fail("BOUND_GOLDEN_CAPABILITY_MULTI_SUBTOPIC", cap)
            cap_sid[cap] = sid
        for qid in bucket.get("core2_question_refs") or []:
            q_sid.setdefault(qid, sid)
    return bucket_sid, cap_sid, q_sid


def rich_engineering_registry_builder(core1, core2, bucket_plan, bucket_sid, cap_sid, q_sid, answer_refs):
    """Upgrade the integration registry to canonical rich Engineering authority."""
    global _LAST_ENGINEERING_DOMAIN_PROJECTION
    global _LAST_ENGINEERING_REGISTRY
    global _LAST_ENGINEERING_PROJECTION_COVERAGE
    base_registry = _ORIGINAL_BUILD_REGISTRY(
        core1, core2, bucket_plan, bucket_sid, cap_sid, q_sid, answer_refs
    )
    engineering_registry = base.load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
    crosswalk = base.load_crosswalk(base.DEFAULT_CROSSWALK)
    projection_coverage = base.resolve_bucket_gate_map(
        crosswalk,
        bucket_plan,
        engineering_registry=engineering_registry,
        fail_on_gap=True,
    )
    rich_registry, receipt = project_engineering_to_domain_registry_v2(
        base_registry,
        engineering_registry=engineering_registry,
        projection_coverage=projection_coverage,
        bucket_plan=bucket_plan,
        bucket_sid=bucket_sid,
        core2_pages=core2["pages"],
    )
    _LAST_ENGINEERING_DOMAIN_PROJECTION = receipt
    _LAST_ENGINEERING_REGISTRY = engineering_registry
    _LAST_ENGINEERING_PROJECTION_COVERAGE = projection_coverage
    return rich_registry


def main() -> None:
    base.bucket_subtopics = multi_bucket_safe_subtopics
    base.legacy.build_registry = rich_engineering_registry_builder
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--core2-plan", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    summary = base.run_bound(Path(args.core1_plan), Path(args.study_model), Path(args.core2_plan), out_dir)

    if _LAST_ENGINEERING_DOMAIN_PROJECTION is None:
        base.fail("BOUND_GOLDEN_ENGINEERING_DOMAIN_PROJECTION_MISSING")
    if _LAST_ENGINEERING_REGISTRY is None or _LAST_ENGINEERING_PROJECTION_COVERAGE is None:
        base.fail("BOUND_GOLDEN_ENGINEERING_DOMAIN_REVALIDATION_CONTEXT_MISSING")

    projection_path = out_dir / "inputs" / "engineering_domain_projection_receipt.json"
    base.write(projection_path, _LAST_ENGINEERING_DOMAIN_PROJECTION)
    summary["engineering_domain_projection_ref"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["projection_id"]
    summary["engineering_domain_projection_digest"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["projection_digest"]
    summary["engineering_domain_base_asset_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["base_asset_count"]
    summary["engineering_domain_projected_asset_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["projected_asset_count"]
    summary["engineering_domain_scope_membership_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["scope_membership_count"]
    summary["engineering_domain_expanded_projection_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["expanded_projected_asset_count"]
    summary["engineering_domain_deduplicated_scope_copy_count"] = (
        _LAST_ENGINEERING_DOMAIN_PROJECTION["scope_membership_count"]
        - _LAST_ENGINEERING_DOMAIN_PROJECTION["projected_asset_count"]
    )
    summary["engineering_domain_transitive_gate_count"] = len(_LAST_ENGINEERING_DOMAIN_PROJECTION["transitive_gate_ids"])
    if summary["registry_ref"] != _LAST_ENGINEERING_DOMAIN_PROJECTION["domain_registry_ref"]:
        base.fail("BOUND_GOLDEN_ENGINEERING_DOMAIN_REGISTRY_REF_DRIFT")

    legacy_key = "engineering_authorized_direct_gate_ids"
    if legacy_key in summary:
        summary["engineering_authorized_direct_gate_count"] = summary.pop(legacy_key)

    registry = json.loads((out_dir / "inputs" / "domain_registry.json").read_text(encoding="utf-8"))
    full_audit = json.loads((out_dir / "full_mixed_engineering_coverage_audit.json").read_text(encoding="utf-8"))
    projection_validation = validate_release_projection_binding_v2(
        registry,
        _LAST_ENGINEERING_DOMAIN_PROJECTION,
        summary,
        full_audit,
        engineering_registry=_LAST_ENGINEERING_REGISTRY,
        projection_coverage=_LAST_ENGINEERING_PROJECTION_COVERAGE,
    )
    summary["engineering_domain_projection_validation"] = projection_validation
    check = "ENGINEERING_DOMAIN_CANONICAL_ASSET_MEMBERSHIP_CUSTODY"
    if check not in summary["release_checks"]:
        summary["release_checks"].append(check)

    base.write(out_dir / "bound_producer_release_summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
