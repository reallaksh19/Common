#!/usr/bin/env python3
"""Fail-closed validator for mixed-difficulty Mathematics publication bundles."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from blueprint_common import digest, fail, load, validate_schema
from compile_engineering_visibility_manifest import validate_visibility_manifest
from validate_content_complete_page_blueprint import validate_content_complete_blueprint
from validate_pedagogy_research_manifest import validate_generation_research_bindings
from validate_self_teaching_generation_spec import validate_generation_spec


def _component_digest(component: dict) -> str:
    return digest(component, "component_digest")


def _component_identity(prefix: str, component: dict) -> str:
    material = {k: copy.deepcopy(v) for k, v in component.items() if k not in {"component_id", "component_digest"}}
    return prefix + digest(material)[:16]


def _render_ids(pages: list[dict]) -> list[str]:
    ids = []
    for page in pages:
        ids.append(page["page_id"])
        ids.extend(x["block_id"] for x in page.get("technical_blocks", []))
        ids.extend(x["block_id"] for x in page.get("prose_blocks", []))
        ids.extend(x["representation_id"] for x in page.get("representations", []))
        ids.extend(x["ttu_id"] for x in page.get("reconstructable_ttus", []))
        ids.extend(x["workspace_id"] for x in page.get("workspace_blocks", []))
    return ids


def validate_bundle(
    bundle: dict,
    release_gate: dict | None = None,
    generation_spec: dict | None = None,
    catalog: dict | None = None,
    research_manifest: dict | None = None,
    engineering_visibility_manifest: dict | None = None,
) -> dict:
    validate_schema(bundle, "math-learner-publication-bundle.schema.json")
    if bundle.get("bundle_digest") != digest(bundle, "bundle_digest"):
        fail("MATH_PUBLICATION_BUNDLE_DIGEST_MISMATCH")
    expected_bundle_id = "MATH-PUB-BUNDLE-" + digest({k: v for k, v in bundle.items() if k not in {"bundle_id", "bundle_digest"}})[:16]
    if bundle.get("bundle_id") != expected_bundle_id:
        fail("MATH_PUBLICATION_BUNDLE_ID_MISMATCH")

    embedded_visibility = bundle["engineering_visibility"]
    visibility_audit = validate_visibility_manifest(embedded_visibility)
    if bundle["engineering_visibility_manifest_digest"] != embedded_visibility["manifest_digest"]:
        fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_DIGEST_DRIFT")
    if embedded_visibility["publication_authorization"] != "NOT_IMPLIED":
        fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_AUTHORITY_FORBIDDEN")
    if engineering_visibility_manifest is not None:
        validate_visibility_manifest(engineering_visibility_manifest)
        if digest(engineering_visibility_manifest) != digest(embedded_visibility):
            fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_SOURCE_DRIFT")

    if release_gate is not None:
        if release_gate.get("status") != "PASS":
            fail("MATH_PUBLICATION_BUNDLE_RELEASE_GATE_NOT_PASS")
        release_digest = digest(release_gate)
        if bundle["source_release_gate_digest"] != release_digest:
            fail("MATH_PUBLICATION_BUNDLE_RELEASE_GATE_DIGEST_DRIFT")
        if embedded_visibility["source_release_gate_digest"] != release_digest:
            fail("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_RELEASE_DRIFT")
    if generation_spec is not None:
        validate_generation_spec(generation_spec)
        validate_generation_research_bindings(generation_spec, research_manifest)
        if bundle["generation_spec_digest"] != digest(generation_spec):
            fail("MATH_PUBLICATION_BUNDLE_GENERATION_SPEC_DIGEST_DRIFT")
        expected_research_digest = digest(research_manifest) if research_manifest is not None else None
        if bundle["pedagogy_research_manifest_digest"] != expected_research_digest:
            fail("MATH_PUBLICATION_BUNDLE_RESEARCH_MANIFEST_DIGEST_DRIFT")
    elif research_manifest is not None:
        fail("MATH_PUBLICATION_BUNDLE_RESEARCH_WITHOUT_GENERATION_SPEC")
    if catalog is not None:
        material = copy.deepcopy(catalog); expected = material.pop("catalog_digest", None)
        if not expected or digest(material) != expected:
            fail("MATH_PUBLICATION_BUNDLE_CATALOG_INVALID")
        if bundle["governed_example_catalog_digest"] != expected:
            fail("MATH_PUBLICATION_BUNDLE_CATALOG_DIGEST_DRIFT")

    components = sorted(bundle["concept_components"], key=lambda x: x["sequence"])
    if [x["sequence"] for x in components] != list(range(1, len(components) + 1)):
        fail("MATH_PUBLICATION_BUNDLE_SEQUENCE_INVALID")
    bucket_refs = [x["bucket_ref"] for x in components]
    if len(bucket_refs) != len(set(bucket_refs)):
        fail("MATH_PUBLICATION_BUNDLE_BUCKET_DUPLICATE")

    problem = bundle["problem_component"]
    if problem["component_digest"] != _component_digest(problem):
        fail("MATH_PUBLICATION_PROBLEM_COMPONENT_DIGEST_MISMATCH")
    if problem["component_id"] != _component_identity("MATH-PROBLEM-BP-", problem):
        fail("MATH_PUBLICATION_PROBLEM_COMPONENT_ID_MISMATCH")
    problem_stages = {p["stage"] for p in problem["pages"]}
    if problem_stages != {"CORE2A", "CORE2B"}:
        fail("MATH_PUBLICATION_PROBLEM_COMPONENT_STAGE_DRIFT", ",".join(sorted(problem_stages)))

    transient_audits = []
    for component in components:
        if component["component_digest"] != _component_digest(component):
            fail("MATH_PUBLICATION_CONCEPT_COMPONENT_DIGEST_MISMATCH", component["component_id"])
        if component["component_id"] != _component_identity("MATH-CONCEPT-BP-", component):
            fail("MATH_PUBLICATION_CONCEPT_COMPONENT_ID_MISMATCH", component["component_id"])
        stages = {p["stage"] for p in component["pages"]}
        if stages != {"CORE1A", "CORE1B"}:
            fail("MATH_PUBLICATION_CONCEPT_COMPONENT_STAGE_DRIFT", component["component_id"])
        transient = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "blueprint_id": "MATH-PAGE-BP-BUNDLE-" + digest([component["component_id"], problem["component_id"]])[:16],
            "difficulty_badge": component["difficulty_badge"],
            "pages": [*copy.deepcopy(component["pages"]), *copy.deepcopy(problem["pages"])],
            "depth_obligations": copy.deepcopy(component["depth_obligations"]),
        }
        transient_audits.append(validate_content_complete_blueprint(transient))

    all_pages = [p for c in components for p in c["pages"]] + list(problem["pages"])
    page_ids = [p["page_id"] for p in all_pages]
    if len(page_ids) != len(set(page_ids)):
        fail("MATH_PUBLICATION_BUNDLE_PAGE_ID_DUPLICATE")
    object_ids = _render_ids(all_pages)
    if len(object_ids) != len(set(object_ids)):
        fail("MATH_PUBLICATION_BUNDLE_OBJECT_ID_DUPLICATE")

    badge_counts = {b: sum(1 for x in components if x["difficulty_badge"] == b) for b in ("EASY", "MEDIUM", "HARD")}
    return {
        "status": "PASS",
        "bundle_id": bundle["bundle_id"],
        "concept_component_count": len(components),
        "problem_page_count": len(problem["pages"]),
        "difficulty_badge_counts": badge_counts,
        "page_count": len(all_pages),
        "render_object_count": len(object_ids) - len(page_ids),
        "render_object_ids": sorted(set(object_ids) - set(page_ids)),
        "component_validation_count": len(transient_audits),
        "research_manifest_bound": research_manifest is not None,
        "engineering_visibility_bound": engineering_visibility_manifest is not None,
        "engineering_visibility_manifest_id": visibility_audit["manifest_id"],
        "engineering_visibility_manifest_digest": visibility_audit["manifest_digest"],
        "engineering_visibility_authorization_count": visibility_audit["authorization_count"],
        "engineering_visibility_gate_count": visibility_audit["gate_count"],
        "engineering_visibility_gate_ids": [row["gate_id"] for row in embedded_visibility["gates"]],
        "semantic_model": "CONCEPT_BADGE_PLUS_PROBLEM_LEARNER_FIT_PLUS_ENGINEERING_VISIBILITY",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--release-gate", required=True)
    ap.add_argument("--generation-spec", required=True)
    ap.add_argument("--core1a-example-catalog", required=True)
    ap.add_argument("--pedagogy-research-manifest")
    ap.add_argument("--engineering-visibility-manifest", required=True)
    ap.add_argument("--audit-out")
    args = ap.parse_args()
    research = load(args.pedagogy_research_manifest) if args.pedagogy_research_manifest else None
    bundle = load(args.input)
    audit = validate_bundle(
        bundle,
        load(args.release_gate),
        load(args.generation_spec),
        load(args.core1a_example_catalog),
        research,
        load(args.engineering_visibility_manifest),
    )
    audit["bundle_sha256"] = digest(bundle)
    if args.audit_out:
        Path(args.audit_out).write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
