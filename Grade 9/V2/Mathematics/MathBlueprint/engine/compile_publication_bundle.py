#!/usr/bin/env python3
"""Compile mixed-difficulty Mathematics publication components.

Intrinsic difficulty belongs to the Core1 concept track, not to Core2. Each
Core1 bucket is therefore materialized as its own badge-governed Concept
Blueprint component. Core2A/Core2B live once in a learner-fit-governed Problem
Blueprint component. The resulting bundle is the semantic input to publication.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import compile_bound_product_page_blueprint as legacy
from blueprint_common import digest, fail, load, validate_schema
from compile_engineering_visibility_manifest import validate_visibility_manifest
from compile_governed_product_page_blueprint import bind_governed_example_authority
from materialize_intrinsic_depth import materialize_uniform_depth, depth_obligations
from validate_pedagogy_research_manifest import validate_generation_research_bindings
from validate_self_teaching_generation_spec import validate_generation_spec


def _seal_component(prefix: str, body: dict) -> dict:
    out = copy.deepcopy(body)
    out["component_id"] = prefix + digest({k: v for k, v in out.items() if k not in {"component_id", "component_digest"}})[:16]
    out["component_digest"] = digest(out, "component_digest")
    return out


def compile_bundle(
    bucket_plan: dict,
    book: dict,
    core1b_dir: Path,
    c2a: dict,
    c2b: dict,
    gen: dict,
    catalog: dict,
    release_gate: dict,
    engineering_visibility: dict,
    research_manifest: dict | None = None,
) -> dict:
    validate_generation_spec(gen)
    validate_generation_research_bindings(gen, research_manifest)
    visibility_audit = validate_visibility_manifest(engineering_visibility)
    if release_gate.get("status") != "PASS":
        fail("MATH_PUBLICATION_BUNDLE_RELEASE_GATE_REQUIRED")
    if engineering_visibility["source_release_gate_digest"] != digest(release_gate):
        fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_RELEASE_DRIFT")
    if engineering_visibility["publication_authorization"] != "NOT_IMPLIED":
        fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_AUTHORITY_FORBIDDEN")
    if visibility_audit["status"] != "PASS":
        fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_INVALID")
    if catalog.get("catalog_role") != "GOVERNED_CORE1A_EXAMPLE_ADMISSION" or not catalog.get("catalog_digest"):
        fail("MATH_PUBLICATION_BUNDLE_EXAMPLE_CATALOG_INVALID")
    material = copy.deepcopy(catalog); material.pop("catalog_digest", None)
    if digest(material) != catalog["catalog_digest"]:
        fail("MATH_PUBLICATION_BUNDLE_EXAMPLE_CATALOG_DIGEST_INVALID")

    spec_by_bucket = {row["bucket_id"]: row for row in gen["core1_buckets"]}
    if len(spec_by_bucket) != len(gen["core1_buckets"]):
        fail("MATH_PUBLICATION_BUNDLE_DUPLICATE_BUCKET_SPEC")

    buckets = list(bucket_plan["buckets"])
    if [b["bucket_id"] for b in buckets] != [b["bucket_id"] for b in book["buckets"]]:
        fail("MATH_PUBLICATION_BUNDLE_BOOK_BUCKET_ORDER_DRIFT")
    missing_specs = [b["bucket_id"] for b in buckets if b["bucket_id"] not in spec_by_bucket]
    if missing_specs:
        fail("MATH_PUBLICATION_BUNDLE_BUCKET_SPEC_MISSING", ",".join(missing_specs))

    c1a_pages, c1a_ttu, unit_by_cap = legacy.compile_core1a_pages(book)
    plans = legacy.load_core1b_plans(core1b_dir, [b["title"] for b in buckets])
    c1b_pages, _ = legacy.compile_core1b_pages(bucket_plan, plans, c1a_ttu)
    c2a_pages, c2a_ttu, _ = legacy.compile_core2a_pages(c2a, unit_by_cap)
    c2b_pages = legacy.compile_core2b_pages(c2b, c2a_ttu)
    bind_governed_example_authority(c1a_pages, book, catalog)

    concept_components = []
    for index, (bucket, a_page, b_page, book_bucket) in enumerate(zip(buckets, c1a_pages, c1b_pages, book["buckets"]), 1):
        spec = spec_by_bucket[bucket["bucket_id"]]
        badge = spec["difficulty_badge"]
        component_pages = materialize_uniform_depth([a_page, b_page], badge, {"buckets": [book_bucket]})
        concept_components.append(_seal_component("MATH-CONCEPT-BP-", {
            "sequence": index,
            "bucket_ref": bucket["bucket_id"],
            "subtopic_ref": spec["subtopic_id"],
            "title": bucket["title"],
            "difficulty_badge": badge,
            "pages": component_pages,
            "depth_obligations": depth_obligations(badge, component_pages),
        }))

    problem_component = _seal_component("MATH-PROBLEM-BP-", {
        "governance": "LEARNER_FIT",
        "pages": [*c2a_pages, *c2b_pages],
    })
    bundle = {
        "schema_version": "1.1.0",
        "subject": "MATHEMATICS",
        "bundle_id": "",
        "source_release_status": "PASS",
        "source_release_gate_digest": digest(release_gate),
        "generation_spec_digest": digest(gen),
        "governed_example_catalog_digest": catalog["catalog_digest"],
        "pedagogy_research_manifest_digest": digest(research_manifest) if research_manifest is not None else None,
        "engineering_visibility_manifest_digest": engineering_visibility["manifest_digest"],
        "engineering_visibility": copy.deepcopy(engineering_visibility),
        "concept_components": concept_components,
        "problem_component": problem_component,
        "publication_stage_order": ["CORE1A", "CORE1B", "CORE2A", "CORE2B"],
        "bundle_digest": "",
    }
    bundle["bundle_id"] = "MATH-PUB-BUNDLE-" + digest({k: v for k, v in bundle.items() if k not in {"bundle_id", "bundle_digest"}})[:16]
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")
    validate_schema(bundle, "math-learner-publication-bundle.schema.json")
    return bundle


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket-plan", required=True)
    ap.add_argument("--core1a-manuscript", required=True)
    ap.add_argument("--core1a-example-catalog", required=True)
    ap.add_argument("--core1b-dir", required=True)
    ap.add_argument("--core2a-blueprint", required=True)
    ap.add_argument("--core2b-plan", required=True)
    ap.add_argument("--generation-spec", required=True)
    ap.add_argument("--pedagogy-research-manifest")
    ap.add_argument("--engineering-visibility-manifest", required=True)
    ap.add_argument("--release-gate", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    research = load(args.pedagogy_research_manifest) if args.pedagogy_research_manifest else None
    bundle = compile_bundle(
        load(args.bucket_plan), load(args.core1a_manuscript), Path(args.core1b_dir),
        load(args.core2a_blueprint), load(args.core2b_plan), load(args.generation_spec),
        load(args.core1a_example_catalog), load(args.release_gate),
        load(args.engineering_visibility_manifest), research,
    )
    Path(args.out).write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "COMPILED",
        "bundle_id": bundle["bundle_id"],
        "concept_components": len(bundle["concept_components"]),
        "difficulty_badges": sorted({x["difficulty_badge"] for x in bundle["concept_components"]}),
        "problem_pages": len(bundle["problem_component"]["pages"]),
        "engineering_visibility_gate_count": bundle["engineering_visibility"]["gate_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
