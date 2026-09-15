#!/usr/bin/env python3
"""Mathematics PCK promotion mechanism (M-G).

Generic, subject-wide promotion pipeline. A PCK candidate moves through

    PCK_CANDIDATE
      -> EVIDENCE_PROVENANCE_REVIEW
      -> PEDAGOGICAL_REVIEW
      -> SUBJECT_REVIEW
      -> SCOPE_REVIEW
      -> PROMOTED_INSTRUCTIONAL_KNOWLEDGE

Every stage is expressed over `capability_ref` / `problem_family_ref`; topic
instances are data carried by the bound asset, never separate schema.

Honesty discipline
------------------
Two authorities can act here and they are never interchangeable:

* `AI_ASSISTED_REFERENCE_REVIEW` / `REPOSITORY_SCOPE_AUTHORITY` are machine
  authorities. They can establish digest custody, structural pedagogical
  completeness, cross-registry referential correctness and subject-scope
  admissibility. A promotion carried by them is `PROVISIONAL_PROMOTED`:
  `authoring_legal = true`, `producer_legal = false`, `release_legal = false`,
  and `expert_review_state` stays `PENDING`.
* `SUBJECT_EXPERT_PASS` / `PEDAGOGY_EXPERT_PASS` require an authorized human
  review intake result bound to the exact asset digest. Only those produce
  `PROMOTED` with `producer_legal = release_legal = true`.

This module cannot manufacture the second kind. Passing a synthetic or
test-only intake result is rejected by name.
"""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
MATH = HERE.parent
REPO_PREFIX = "Grade 9/V2/Mathematics/"

PROMOTION_STAGES = [
    "EVIDENCE_PROVENANCE_REVIEW",
    "PEDAGOGICAL_REVIEW",
    "SUBJECT_REVIEW",
    "SCOPE_REVIEW",
]
TERMINAL_LIFECYCLE_STATE = "PROMOTED_INSTRUCTIONAL_KNOWLEDGE"

MACHINE_AUTHORITIES = {"AI_ASSISTED_REFERENCE_REVIEW", "REPOSITORY_SCOPE_AUTHORITY"}
EXPERT_AUTHORITIES = {"SUBJECT_EXPERT_PASS", "PEDAGOGY_EXPERT_PASS"}

SUBJECT_SCOPE = "MATHEMATICS_GRADE9_ASSESSMENT_SCOPE"
PROMOTED_VERSION = "1.0.0"

# Falsifier vocabulary. Each name is asserted by the M-G promotion test suite.
FALSIFIERS = (
    "PCK_PROMOTION_STAGE_SKIPPED",
    "PCK_PROMOTION_STAGE_ORDER_VIOLATION",
    "FABRICATED_EXPERT_REVIEW_AUTHORITY",
    "PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL",
    "PCK_PROMOTION_EVIDENCE_UNBOUND",
    "PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE",
    "PCK_PROMOTION_FAMILY_UNRESOLVED",
    "PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE",
    "PCK_PROVENANCE_UNDECLARED",
    "PCK_PROMOTION_DIGEST_MISMATCH",
    "PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH",
    "PCK_PROMOTION_UNKNOWN_ASSET",
    "TOPIC_SPECIFIC_PROMOTION_RECORD",
    "TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE",
)

# Minimum structural obligations a Mathematics PCK asset must satisfy to be
# pedagogically usable at all. Stated generically over the asset contract.
PEDAGOGICAL_STRUCTURE = {
    "reconstruction_route": 3,
    "repair_route": 2,
    "verification_method": 1,
    "fading_dimensions": 2,
    "applicability_conditions": 1,
    "known_limitations": 1,
    "representation_path": 2,
}
CONTRAST_FIELDS = ("shared_structure", "focal_distinction", "prediction_prompt", "decisive_feature")
DISCRIMINATOR_FIELDS = ("candidate_wrong_model", "probe", "decisive_response")

ALLOWED_EVIDENCE_CLASSES = {"REPOSITORY_AUTHORITY_PLUS_AI_ASSISTED_DRAFT", "HUMAN_REVIEWED_SUBJECT_PCK"}
ALLOWED_AUTHORING_ORIGINS = {"AI_ASSISTED_DRAFT", "HUMAN_AUTHORED", "HUMAN_REVISED"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value, omit=None):
    value = copy.deepcopy(value)
    if omit and isinstance(value, dict):
        value.pop(omit, None)
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def fail(code, detail=""):
    raise ValueError(f"{code}:{detail}" if detail else code)


def seal_record(record):
    record["record_id"] = "MATH-PCKREV-{}-{}".format(record["stage"], digest(record, "record_digest")[:16])
    record["record_digest"] = digest(record, "record_digest")
    return record


def make_record(asset, stage, authority, checks, findings, authority_refs, intake_ref=None):
    record = {
        "record_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "asset_id": asset["asset_id"],
        "asset_digest": asset["asset_digest"],
        "stage": stage,
        "review_authority": authority,
        "status": "FAIL" if findings else "PASS",
        "checks_passed": sorted(set(checks)),
        "findings": sorted(set(findings)),
        "authority_refs": sorted(set(authority_refs)),
        "human_review_intake_ref": intake_ref,
        "record_digest": "",
    }
    return seal_record(record)


# ---------------------------------------------------------------------------
# Stage 1: evidence and provenance
# ---------------------------------------------------------------------------
def review_evidence_provenance(asset):
    findings = []
    checks = []
    if asset.get("asset_digest") != digest(asset, "asset_digest"):
        findings.append("PCK_PROMOTION_DIGEST_MISMATCH: asset digest does not seal the asset body")
    else:
        checks.append("ASSET_DIGEST_SEALS_BODY")

    provenance = asset.get("provenance") or {}
    if provenance.get("evidence_class") not in ALLOWED_EVIDENCE_CLASSES:
        findings.append("PCK_PROVENANCE_UNDECLARED: evidence_class is not a declared evidence class")
    else:
        checks.append("EVIDENCE_CLASS_DECLARED")
    if provenance.get("authoring_origin") not in ALLOWED_AUTHORING_ORIGINS:
        findings.append("PCK_PROVENANCE_UNDECLARED: authoring_origin is not a declared origin")
    else:
        checks.append("AUTHORING_ORIGIN_DECLARED")
    if not provenance.get("source_refs"):
        findings.append("PCK_PROVENANCE_UNDECLARED: no upstream source refs recorded")
    else:
        checks.append("SOURCE_REFS_RECORDED")

    review = asset.get("review") or {}
    if set(review.get("required_dimensions") or []) != {"SUBJECT", "PEDAGOGY"}:
        findings.append("PCK_PROVENANCE_UNDECLARED: required review dimensions are not SUBJECT+PEDAGOGY")
    else:
        checks.append("REQUIRED_REVIEW_DIMENSIONS_DECLARED")
    if review.get("status") == "HUMAN_REVIEWED" and not review.get("human_review_evidence_refs"):
        findings.append("PCK_PROMOTION_EVIDENCE_UNBOUND: asset claims human review without evidence refs")
    else:
        checks.append("REVIEW_STATE_CONSISTENT_WITH_EVIDENCE")

    return make_record(
        asset,
        "EVIDENCE_PROVENANCE_REVIEW",
        "AI_ASSISTED_REFERENCE_REVIEW",
        checks or ["NO_CHECK_PASSED"],
        findings,
        [REPO_PREFIX + "InstructionalKnowledge/contracts/math-pck-asset.schema.json"],
    )


# ---------------------------------------------------------------------------
# Stage 2: pedagogical structure
# ---------------------------------------------------------------------------
def review_pedagogical(asset):
    findings = []
    checks = []
    for field, minimum in sorted(PEDAGOGICAL_STRUCTURE.items()):
        value = asset.get(field) or []
        if len(value) < minimum:
            findings.append(f"PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE: {field} has fewer than {minimum} entries")
        else:
            checks.append(f"STRUCTURE_{field.upper()}")

    contrast = asset.get("minimal_contrast") or {}
    if any(not str(contrast.get(k, "")).strip() for k in CONTRAST_FIELDS):
        findings.append("PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE: minimal contrast is not fully specified")
    else:
        checks.append("MINIMAL_CONTRAST_COMPLETE")

    discriminator = asset.get("misconception_discriminator") or {}
    if any(not str(discriminator.get(k, "")).strip() for k in DISCRIMINATOR_FIELDS):
        findings.append("PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE: misconception discriminator is not fully specified")
    else:
        checks.append("MISCONCEPTION_DISCRIMINATOR_COMPLETE")

    # A discriminator that merely restates the anchor cannot discriminate.
    anchor = str(asset.get("anchor", "")).strip().lower()
    probe = str(discriminator.get("probe", "")).strip().lower()
    if anchor and probe and anchor == probe:
        findings.append("PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE: discriminator probe restates the anchor")
    else:
        checks.append("PROBE_DISTINCT_FROM_ANCHOR")

    if not str(asset.get("ordinary_language_bridge", "")).strip():
        findings.append("PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE: no ordinary-language bridge")
    else:
        checks.append("ORDINARY_LANGUAGE_BRIDGE_PRESENT")

    return make_record(
        asset,
        "PEDAGOGICAL_REVIEW",
        "AI_ASSISTED_REFERENCE_REVIEW",
        checks or ["NO_CHECK_PASSED"],
        findings,
        [
            REPO_PREFIX + "InstructionalKnowledge/contracts/math-pck-asset.schema.json",
            REPO_PREFIX + "StudySynthesis/policies/math-treatment-policy.json",
        ],
    )


# ---------------------------------------------------------------------------
# Stage 3: subject referential correctness
# ---------------------------------------------------------------------------
def review_subject(asset, capability_ids, family_ids, representation_identities):
    findings = []
    checks = []
    unknown_caps = sorted(set(asset["capability_refs"]) - set(capability_ids))
    if unknown_caps:
        findings.append("PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE: " + ",".join(unknown_caps))
    else:
        checks.append("CAPABILITY_REFS_RESOLVE")

    unknown_families = sorted(
        {asset["worked_example_family"], asset["transfer_family"]} - set(family_ids)
    )
    if unknown_families:
        findings.append("PCK_PROMOTION_FAMILY_UNRESOLVED: " + ",".join(unknown_families))
    else:
        checks.append("PROBLEM_FAMILY_REFS_RESOLVE")

    if not asset["verification_method"]:
        findings.append("PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE: no verification method declared")
    else:
        checks.append("VERIFICATION_METHOD_DECLARED")

    # The representation path must engage at least one declared subject
    # representation identity; a path made only of ad-hoc labels is not
    # bound to the subject authority.
    path = {str(x).upper() for x in asset["representation_path"]}
    if not path.intersection(set(representation_identities)):
        findings.append(
            "PCK_PROMOTION_EVIDENCE_UNBOUND: representation path engages no declared subject representation identity"
        )
    else:
        checks.append("REPRESENTATION_PATH_BOUND_TO_SUBJECT_AUTHORITY")

    return make_record(
        asset,
        "SUBJECT_REVIEW",
        "AI_ASSISTED_REFERENCE_REVIEW",
        checks or ["NO_CHECK_PASSED"],
        findings,
        [
            REPO_PREFIX + "AssessmentScope/authority/math-assessment-scope-authority.json",
            REPO_PREFIX + "ProblemSemantics/registry/math-problem-family-registry.json",
        ],
    )


# ---------------------------------------------------------------------------
# Stage 4: subject-scope admissibility
# ---------------------------------------------------------------------------
def review_scope(asset, capability_ids):
    findings = []
    checks = []
    if asset.get("subject") != "MATHEMATICS":
        findings.append("PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE: asset is not a Mathematics asset")
    else:
        checks.append("SUBJECT_MATCHES_REGISTRY")

    if not all(ref.startswith("MATH-") for ref in asset["capability_refs"]):
        findings.append("PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE: non-Mathematics capability ref")
    else:
        checks.append("CAPABILITY_NAMESPACE_CONSISTENT")

    if not set(asset["capability_refs"]).issubset(set(capability_ids)):
        findings.append("PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE: capability outside declared assessment scope")
    else:
        checks.append("CAPABILITIES_WITHIN_DECLARED_SCOPE")

    if asset.get("lifecycle_status") not in {"CANDIDATE", "PROMOTED"}:
        findings.append("PCK_PROMOTION_EVIDENCE_UNBOUND: asset lifecycle state is not promotable")
    else:
        checks.append("LIFECYCLE_STATE_PROMOTABLE")

    return make_record(
        asset,
        "SCOPE_REVIEW",
        "REPOSITORY_SCOPE_AUTHORITY",
        checks or ["NO_CHECK_PASSED"],
        findings,
        [REPO_PREFIX + "AssessmentScope/authority/math-assessment-scope-authority.json"],
    )


# ---------------------------------------------------------------------------
# Expert review evidence
# ---------------------------------------------------------------------------
def expert_records(asset, intake_result):
    """Normalize an authorized human review intake result into expert stage records.

    Refuses anything that is not a REAL, release-eligible intake bound to this
    exact asset digest. This is the only path to `producer_legal = true`.
    """
    if intake_result is None:
        return []
    if intake_result.get("mode") != "REAL_RELEASE" or intake_result.get("fixture_class") != "REAL":
        fail("TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE", asset["asset_id"])
    if not intake_result.get("release_evidence_eligible"):
        fail("TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE", asset["asset_id"])
    if intake_result.get("candidate_sha256") != asset["asset_digest"]:
        fail("PCK_PROMOTION_EVIDENCE_UNBOUND", asset["asset_id"])
    if intake_result.get("intake_status") != "READY":
        fail("PCK_PROMOTION_EVIDENCE_UNBOUND", asset["asset_id"])
    summary = intake_result.get("quality_review_summary") or {}
    records = []
    for dimension, authority, stage in (
        ("SUBJECT", "SUBJECT_EXPERT_PASS", "SUBJECT_REVIEW"),
        ("PEDAGOGY", "PEDAGOGY_EXPERT_PASS", "PEDAGOGICAL_REVIEW"),
    ):
        state = summary.get(dimension)
        if state != "PASS":
            fail("PCK_PROMOTION_EVIDENCE_UNBOUND", f"{asset['asset_id']}:{dimension}")
        records.append(
            make_record(
                asset,
                stage,
                authority,
                [f"AUTHORIZED_{dimension}_EXPERT_PASS"],
                [],
                [REPO_PREFIX.replace("Mathematics/", "") + "Shared/HumanReview/contracts/human-review-intake-result.schema.json"],
                intake_ref=intake_result.get("intake_id"),
            )
        )
    return records


# ---------------------------------------------------------------------------
# Promotion
# ---------------------------------------------------------------------------
def run_pipeline(asset, capability_ids, family_ids, representation_identities, intake_result=None):
    """Run every stage in order and return the stage records.

    Stages always run in `PROMOTION_STAGES` order; a caller cannot reorder or
    skip them, which is what `PCK_PROMOTION_STAGE_ORDER_VIOLATION` and
    `PCK_PROMOTION_STAGE_SKIPPED` guard downstream.
    """
    machine = {
        "EVIDENCE_PROVENANCE_REVIEW": review_evidence_provenance(asset),
        "PEDAGOGICAL_REVIEW": review_pedagogical(asset),
        "SUBJECT_REVIEW": review_subject(asset, capability_ids, family_ids, representation_identities),
        "SCOPE_REVIEW": review_scope(asset, capability_ids),
    }
    records = [machine[stage] for stage in PROMOTION_STAGES]
    records.extend(expert_records(asset, intake_result))
    return records


def assert_pipeline_integrity(records):
    seen = [r["stage"] for r in records if r["review_authority"] in MACHINE_AUTHORITIES]
    missing = [stage for stage in PROMOTION_STAGES if stage not in seen]
    if missing:
        fail("PCK_PROMOTION_STAGE_SKIPPED", ",".join(missing))
    if seen != PROMOTION_STAGES:
        fail("PCK_PROMOTION_STAGE_ORDER_VIOLATION", ",".join(seen))
    for record in records:
        if record["record_digest"] != digest(record, "record_digest"):
            fail("PCK_PROMOTION_DIGEST_MISMATCH", record["record_id"])
        if record["review_authority"] in EXPERT_AUTHORITIES and not record.get("human_review_intake_ref"):
            fail("FABRICATED_EXPERT_REVIEW_AUTHORITY", record["record_id"])
        if record["review_authority"] in MACHINE_AUTHORITIES and record.get("human_review_intake_ref"):
            fail("FABRICATED_EXPERT_REVIEW_AUTHORITY", record["record_id"])
    return True


def build_promotion(asset, records):
    assert_pipeline_integrity(records)
    blocking = [r for r in records if r["status"] != "PASS"]
    if blocking:
        return None, sorted({f"{r['stage']}:{f}" for r in blocking for f in (r["findings"] or ["UNSPECIFIED"])})

    expert = {r["review_authority"] for r in records if r["review_authority"] in EXPERT_AUTHORITIES}
    fully_expert_reviewed = expert == EXPERT_AUTHORITIES
    expert_state = {
        "SUBJECT_EXPERT_PASS": "PASS" if "SUBJECT_EXPERT_PASS" in expert else "PENDING",
        "PEDAGOGY_EXPERT_PASS": "PASS" if "PEDAGOGY_EXPERT_PASS" in expert else "PENDING",
    }

    promotion = {
        "asset_id": asset["asset_id"],
        "asset_digest": asset["asset_digest"],
        "promotion_status": "PROMOTED" if fully_expert_reviewed else "PROVISIONAL_PROMOTED",
        "promotion_class": "HUMAN_REVIEWED_PRODUCTION" if fully_expert_reviewed else "AI_ASSISTED_PROVISIONAL",
        "lifecycle_state": TERMINAL_LIFECYCLE_STATE,
        "subject_scope": SUBJECT_SCOPE,
        "capability_refs": sorted(set(asset["capability_refs"])),
        "applicability_conditions": list(asset["applicability_conditions"]),
        "known_limitations": list(asset["known_limitations"]),
        "evidence_class": "HUMAN_REVIEWED_SUBJECT_PCK" if fully_expert_reviewed else asset["provenance"]["evidence_class"],
        "provenance": copy.deepcopy(asset["provenance"]),
        "review_authority": "AUTHORIZED_HUMAN_EXPERT_REVIEW" if fully_expert_reviewed else "AI_ASSISTED_REFERENCE_REVIEW",
        "review_pipeline": [
            {
                "stage": r["stage"],
                "record_id": r["record_id"],
                "review_authority": r["review_authority"],
                "status": r["status"],
                "record_digest": r["record_digest"],
            }
            for r in records
        ],
        "expert_review_state": expert_state,
        "review_dimensions": ["PEDAGOGY", "SUBJECT"],
        "review_evidence_refs": sorted({r["record_id"] for r in records}),
        "review_source": "HUMAN_REVIEW_INTAKE_RESULT" if fully_expert_reviewed else "AI_ASSISTED_REFERENCE_REVIEW",
        "review_registry_class": "REAL" if fully_expert_reviewed else "AI_ASSISTED",
        "authoring_legal": True,
        "producer_legal": bool(fully_expert_reviewed),
        "release_legal": bool(fully_expert_reviewed),
        "promoted_version": PROMOTED_VERSION,
        "promotion_digest": "",
    }
    promotion["promotion_digest"] = digest(promotion, "promotion_digest")
    assert_promotion_honesty(promotion)
    return promotion, []


def assert_promotion_honesty(promotion):
    """Fail closed on any promotion that overstates its own review authority."""
    if promotion["promotion_digest"] != digest(promotion, "promotion_digest"):
        fail("PCK_PROMOTION_DIGEST_MISMATCH", promotion["asset_id"])
    provisional = promotion["promotion_status"] == "PROVISIONAL_PROMOTED"
    expert_pending = any(v != "PASS" for v in promotion["expert_review_state"].values())
    if provisional and (promotion["producer_legal"] or promotion["release_legal"]):
        fail("PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL", promotion["asset_id"])
    if expert_pending and promotion["promotion_status"] == "PROMOTED":
        fail("FABRICATED_EXPERT_REVIEW_AUTHORITY", promotion["asset_id"])
    if expert_pending and promotion["review_source"] == "HUMAN_REVIEW_INTAKE_RESULT":
        fail("FABRICATED_EXPERT_REVIEW_AUTHORITY", promotion["asset_id"])
    if promotion["review_authority"] == "AI_ASSISTED_REFERENCE_REVIEW" and promotion["review_registry_class"] == "REAL":
        fail("FABRICATED_EXPERT_REVIEW_AUTHORITY", promotion["asset_id"])
    if not promotion["capability_refs"]:
        fail("PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE", promotion["asset_id"])
    # A promotion record must be generic over capabilities, never keyed to one
    # topic instance. `subject_scope` is the subject-wide scope token.
    if promotion["subject_scope"] != SUBJECT_SCOPE:
        fail("TOPIC_SPECIFIC_PROMOTION_RECORD", promotion["asset_id"])
    return True


def subject_authorities():
    scope_authority = load(MATH / "AssessmentScope" / "authority" / "math-assessment-scope-authority.json")
    capability_ids = [c["capability_id"] for c in scope_authority["capabilities"]]
    representation_identities = list(scope_authority["representation_identities"])
    sys.path.insert(0, str(MATH / "ProblemSemantics" / "engine"))
    from build_math_problem_semantics import load_family_registry

    family_registry = load_family_registry(MATH / "ProblemSemantics" / "registry" / "math-problem-family-registry.json")
    family_ids = [f["family_id"] for f in family_registry["families"]]
    return capability_ids, family_ids, representation_identities


def build_registry(candidate_registry, candidate_assets, intake_results=None, registry_class="PRODUCTION"):
    """Run every candidate through the pipeline and emit a promotion registry."""
    if candidate_registry["registry_digest"] != digest(candidate_registry, "registry_digest"):
        fail("PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH", candidate_registry["registry_id"])
    known = {doc["asset_id"] for doc in candidate_registry["asset_documents"]}
    intake_results = intake_results or {}
    for asset_id in intake_results:
        if asset_id not in known:
            fail("PCK_PROMOTION_UNKNOWN_ASSET", asset_id)

    capability_ids, family_ids, representation_identities = subject_authorities()
    promotions = []
    refusals = []
    for asset in sorted(candidate_assets, key=lambda x: x["asset_id"]):
        if asset["asset_id"] not in known:
            fail("PCK_PROMOTION_UNKNOWN_ASSET", asset["asset_id"])
        records = run_pipeline(
            asset, capability_ids, family_ids, representation_identities, intake_results.get(asset["asset_id"])
        )
        promotion, blockers = build_promotion(asset, records)
        if promotion is None:
            refusals.append({"asset_id": asset["asset_id"], "blockers": blockers})
        else:
            promotions.append(promotion)

    registry = {
        "registry_id": "MATH-PCK-PROMOTION-REGISTRY-v1",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "registry_class": registry_class,
        "promotion_pipeline_ref": REPO_PREFIX + "InstructionalKnowledge/engine/promote_math_pck.py",
        "promotions": sorted(promotions, key=lambda x: x["asset_id"]),
        "registry_digest": "",
    }
    registry["registry_digest"] = digest(registry, "registry_digest")
    return registry, refusals


def main():
    ap = argparse.ArgumentParser(description="Run Mathematics PCK candidates through the promotion pipeline.")
    ap.add_argument("--pck-candidates", default=str(HERE / "registry" / "math-pck-candidates.json"))
    ap.add_argument("--human-review-intake", help="JSON map of asset_id -> authorized human review intake result")
    ap.add_argument("--registry-class", choices=["PRODUCTION", "TEST_ONLY"], default="PRODUCTION")
    ap.add_argument("--out", required=True)
    ap.add_argument("--refusals-out")
    args = ap.parse_args()

    sys.path.insert(0, str(MATH / "Core1Authoring" / "engine"))
    from author_math_core1 import load_candidate_bundle

    candidate_registry, candidate_assets = load_candidate_bundle(args.pck_candidates)
    intake = load(args.human_review_intake) if args.human_review_intake else None
    registry, refusals = build_registry(candidate_registry, candidate_assets, intake, args.registry_class)
    Path(args.out).write_text(json.dumps(registry, separators=(",", ":")), encoding="utf-8")
    if args.refusals_out:
        Path(args.refusals_out).write_text(json.dumps(refusals, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    promoted = len(registry["promotions"])
    provisional = sum(1 for p in registry["promotions"] if p["promotion_status"] == "PROVISIONAL_PROMOTED")
    print(
        f"promotions={promoted} provisional={provisional} producer_legal="
        f"{sum(1 for p in registry['promotions'] if p['producer_legal'])} refused={len(refusals)}"
    )
    return 0 if not refusals else 1


if __name__ == "__main__":
    raise SystemExit(main())
