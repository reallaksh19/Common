#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from blueprint_common import digest, fail, load, validate_schema
from validate_self_teaching_generation_spec import validate_generation_spec

MEDIUM_REQUIRED = {"REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR"}
HARD_REQUIRED = {"REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR", "INFERENTIAL_DECOMPOSITION", "TRANSFER_DESIGN"}


def validate_manifest(manifest: dict) -> None:
    validate_schema(manifest, "math-pedagogy-research-manifest.schema.json")
    if manifest.get("curriculum_authority") is not False:
        fail("MATH_PEDAGOGY_RESEARCH_CANNOT_BE_CURRICULUM_AUTHORITY")
    if manifest.get("manifest_digest") != digest(manifest, "manifest_digest"):
        fail("MATH_PEDAGOGY_RESEARCH_MANIFEST_DIGEST_MISMATCH")
    refs = [x["research_ref"] for x in manifest["sources"]]
    if len(refs) != len(set(refs)):
        fail("MATH_PEDAGOGY_RESEARCH_SOURCE_REF_DUPLICATE")
    decisions = [x["decision_ref"] for x in manifest["decisions"]]
    if len(decisions) != len(set(decisions)):
        fail("MATH_PEDAGOGY_RESEARCH_DECISION_REF_DUPLICATE")
    source_refs = set(refs)
    for decision in manifest["decisions"]:
        missing = set(decision["research_refs"]) - source_refs
        if missing:
            fail("MATH_PEDAGOGY_RESEARCH_DECISION_SOURCE_UNKNOWN", ",".join(sorted(missing)))
    if manifest["release_class"] == "PRODUCTION":
        bad = [x["research_ref"] for x in manifest["sources"] if x["evidence_class"] != "VERIFIED_WEB_CAPTURE"]
        if bad:
            fail("MATH_PEDAGOGY_RESEARCH_PRODUCTION_REQUIRES_VERIFIED_CAPTURE", ",".join(bad))


def validate_generation_research_bindings(generation_spec: dict, manifest: dict | None) -> None:
    validate_generation_spec(generation_spec)
    non_easy = [x for x in generation_spec["core1_buckets"] if x["difficulty_badge"] != "EASY"]
    if not non_easy:
        if manifest is not None:
            validate_manifest(manifest)
        return
    if manifest is None:
        fail("MATH_PEDAGOGY_RESEARCH_MANIFEST_REQUIRED_FOR_MEDIUM_HARD")
    validate_manifest(manifest)
    sources = {x["research_ref"]: x for x in manifest["sources"]}
    decisions = {x["decision_ref"]: x for x in manifest["decisions"]}

    for bucket in non_easy:
        brief_ref = bucket["pedagogy_research_brief_ref"]
        if brief_ref not in decisions:
            fail("MATH_PEDAGOGY_RESEARCH_BRIEF_UNKNOWN", f"{bucket['bucket_id']}:{brief_ref}")
        decision = decisions[brief_ref]
        if decision["subtopic_ref"] != bucket["subtopic_id"]:
            fail("MATH_PEDAGOGY_RESEARCH_SUBTOPIC_DRIFT", bucket["bucket_id"])
        expected_depth = "DEEP" if bucket["difficulty_badge"] == "HARD" else "STANDARD"
        if decision["research_depth"] != expected_depth:
            fail("MATH_PEDAGOGY_RESEARCH_DEPTH_DRIFT", bucket["bucket_id"])
        refs = set(bucket["pedagogy_web_research_refs"])
        if not refs or not refs.issubset(sources):
            fail("MATH_PEDAGOGY_RESEARCH_SOURCE_BINDING_INCOMPLETE", bucket["bucket_id"])
        if not refs.issubset(set(decision["research_refs"])):
            fail("MATH_PEDAGOGY_RESEARCH_BRIEF_SOURCE_DRIFT", bucket["bucket_id"])
        required = HARD_REQUIRED if bucket["difficulty_badge"] == "HARD" else MEDIUM_REQUIRED
        coverage = set(decision["coverage"])
        missing_coverage = required - coverage
        if missing_coverage:
            fail("MATH_PEDAGOGY_RESEARCH_DECISION_COVERAGE_INCOMPLETE", f"{bucket['bucket_id']}:{','.join(sorted(missing_coverage))}")
        supported = set()
        for ref in refs:
            supported.update(sources[ref]["supports"])
        # At least representation design must be grounded directly in the retained sources.
        if "REPRESENTATION_DESIGN" not in supported and "MULTIPLE_REPRESENTATION_MAPPING" not in supported:
            fail("MATH_PEDAGOGY_RESEARCH_REPRESENTATION_EVIDENCE_MISSING", bucket["bucket_id"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--generation-spec")
    args = ap.parse_args()
    manifest = load(args.manifest)
    if args.generation_spec:
        validate_generation_research_bindings(load(args.generation_spec), manifest)
    else:
        validate_manifest(manifest)
    print(json.dumps({"status":"PASS","manifest_id":manifest["manifest_id"],"source_count":len(manifest["sources"]),"decision_count":len(manifest["decisions"])}, indent=2))


if __name__ == "__main__":
    main()
