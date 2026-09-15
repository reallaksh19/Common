#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from blueprint_common import digest, fail, load, validate_schema
from validate_self_teaching_generation_spec import validate_generation_spec

MEDIUM_REQUIRED = {"REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR"}
HARD_REQUIRED = {"REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR", "INFERENTIAL_DECOMPOSITION", "TRANSFER_DESIGN"}

# A source tagged as MULTIPLE_REPRESENTATION_MAPPING may directly ground a
# representation-design claim.  All other promoted claim categories require an
# exact source-support category.  This is subject-wide policy, not topic logic.
CATEGORY_EVIDENCE_EQUIVALENTS = {
    "REPRESENTATION_DESIGN": {"REPRESENTATION_DESIGN", "MULTIPLE_REPRESENTATION_MAPPING"},
}


def _accepted_source_categories(category: str) -> set[str]:
    return CATEGORY_EVIDENCE_EQUIVALENTS.get(category, {category})


def _source_is_relevant(source: dict, category: str) -> bool:
    return bool(set(source["supports"]) & _accepted_source_categories(category))


def validate_manifest(manifest: dict) -> None:
    validate_schema(manifest, "math-pedagogy-research-manifest.schema.json")
    if manifest.get("curriculum_authority") is not False:
        fail("MATH_PEDAGOGY_RESEARCH_CANNOT_BE_CURRICULUM_AUTHORITY")
    if manifest.get("manifest_digest") != digest(manifest, "manifest_digest"):
        fail("MATH_PEDAGOGY_RESEARCH_MANIFEST_DIGEST_MISMATCH")

    refs = [x["research_ref"] for x in manifest["sources"]]
    if len(refs) != len(set(refs)):
        fail("MATH_PEDAGOGY_RESEARCH_SOURCE_REF_DUPLICATE")
    sources = {x["research_ref"]: x for x in manifest["sources"]}

    decision_refs = [x["decision_ref"] for x in manifest["decisions"]]
    if len(decision_refs) != len(set(decision_refs)):
        fail("MATH_PEDAGOGY_RESEARCH_DECISION_REF_DUPLICATE")
    decisions = {x["decision_ref"]: x for x in manifest["decisions"]}

    for decision in manifest["decisions"]:
        missing = set(decision["research_refs"]) - set(sources)
        if missing:
            fail("MATH_PEDAGOGY_RESEARCH_DECISION_SOURCE_UNKNOWN", ",".join(sorted(missing)))

    if manifest["release_class"] == "PRODUCTION":
        bad = [x["research_ref"] for x in manifest["sources"] if x["evidence_class"] != "VERIFIED_WEB_CAPTURE"]
        if bad:
            fail("MATH_PEDAGOGY_RESEARCH_PRODUCTION_REQUIRES_VERIFIED_CAPTURE", ",".join(bad))

    claim_refs = [x["claim_ref"] for x in manifest["claims"]]
    if len(claim_refs) != len(set(claim_refs)):
        fail("MATH_PEDAGOGY_RESEARCH_CLAIM_REF_DUPLICATE")

    claims_by_decision_category: dict[tuple[str, str], list[dict]] = {}
    for claim in manifest["claims"]:
        decision_ref = claim["decision_ref"]
        if decision_ref not in decisions:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_DECISION_UNKNOWN", f"{claim['claim_ref']}:{decision_ref}")
        decision = decisions[decision_ref]
        category = claim["support_category"]
        if category not in set(decision["coverage"]):
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_CATEGORY_OUTSIDE_DECISION", f"{claim['claim_ref']}:{category}")

        link_refs = [link["research_ref"] for link in claim["evidence_links"]]
        if len(link_refs) != len(set(link_refs)):
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_SOURCE_DUPLICATE", claim["claim_ref"])
        unknown = set(link_refs) - set(sources)
        if unknown:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_SOURCE_UNKNOWN", f"{claim['claim_ref']}:{','.join(sorted(unknown))}")
        outside = set(link_refs) - set(decision["research_refs"])
        if outside:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_SOURCE_OUTSIDE_DECISION", f"{claim['claim_ref']}:{','.join(sorted(outside))}")

        irrelevant = sorted(ref for ref in link_refs if not _source_is_relevant(sources[ref], category))
        if irrelevant:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_SOURCE_CATEGORY_MISMATCH", f"{claim['claim_ref']}:{','.join(irrelevant)}")

        relevant = {
            ref for ref in decision["research_refs"]
            if _source_is_relevant(sources[ref], category)
        }
        if not relevant:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_CATEGORY_EVIDENCE_MISSING", f"{claim['claim_ref']}:{category}")
        unclassified = relevant - set(link_refs)
        if unclassified:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_RELEVANT_SOURCE_UNCLASSIFIED", f"{claim['claim_ref']}:{','.join(sorted(unclassified))}")

        supporting = [link for link in claim["evidence_links"] if link["stance"] == "SUPPORTS"]
        contradicting = [link for link in claim["evidence_links"] if link["stance"] == "CONTRADICTS"]
        if not supporting:
            fail("MATH_PEDAGOGY_RESEARCH_CLAIM_SUPPORT_REQUIRED", claim["claim_ref"])
        if contradicting and not claim["contradiction_resolution"]:
            fail("MATH_PEDAGOGY_RESEARCH_CONTRADICTION_UNRESOLVED", claim["claim_ref"])
        if not contradicting and claim["contradiction_resolution"] is not None:
            fail("MATH_PEDAGOGY_RESEARCH_CONTRADICTION_RESOLUTION_SPURIOUS", claim["claim_ref"])
        if manifest["release_class"] == "PRODUCTION" and claim["confidence"] == "LOW":
            fail("MATH_PEDAGOGY_RESEARCH_PRODUCTION_LOW_CONFIDENCE_FORBIDDEN", claim["claim_ref"])

        claims_by_decision_category.setdefault((decision_ref, category), []).append(claim)

    for decision in manifest["decisions"]:
        for category in decision["coverage"]:
            if (decision["decision_ref"], category) not in claims_by_decision_category:
                fail(
                    "MATH_PEDAGOGY_RESEARCH_DECISION_CLAIM_COVERAGE_INCOMPLETE",
                    f"{decision['decision_ref']}:{category}",
                )


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
    claims_by_decision: dict[str, list[dict]] = {}
    for claim in manifest["claims"]:
        claims_by_decision.setdefault(claim["decision_ref"], []).append(claim)

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

        # Every source actually used to promote a claim for this decision must
        # survive into the generation binding.  Discovery-only sources may stay
        # outside the promoted bucket binding.
        promoted_refs = {
            link["research_ref"]
            for claim in claims_by_decision.get(brief_ref, [])
            for link in claim["evidence_links"]
        }
        if not promoted_refs.issubset(refs):
            fail(
                "MATH_PEDAGOGY_RESEARCH_PROMOTED_CLAIM_SOURCE_NOT_RETAINED",
                f"{bucket['bucket_id']}:{','.join(sorted(promoted_refs - refs))}",
            )

        required = HARD_REQUIRED if bucket["difficulty_badge"] == "HARD" else MEDIUM_REQUIRED
        coverage = set(decision["coverage"])
        missing_coverage = required - coverage
        if missing_coverage:
            fail("MATH_PEDAGOGY_RESEARCH_DECISION_COVERAGE_INCOMPLETE", f"{bucket['bucket_id']}:{','.join(sorted(missing_coverage))}")
        supported = set()
        for ref in refs:
            supported.update(sources[ref]["supports"])
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
    print(json.dumps({
        "status":"PASS",
        "manifest_id":manifest["manifest_id"],
        "source_count":len(manifest["sources"]),
        "decision_count":len(manifest["decisions"]),
        "claim_count":len(manifest["claims"]),
    }, indent=2))


if __name__ == "__main__":
    main()
