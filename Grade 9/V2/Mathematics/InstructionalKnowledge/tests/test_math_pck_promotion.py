#!/usr/bin/env python3
"""Falsifier suite for the Mathematics PCK promotion mechanism (M-G / #319).

Every falsifier named in `promote_math_pck.FALSIFIERS` is asserted by name.
"""
import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
PCK = HERE.parents[1]
MATH = HERE.parents[2]
sys.path.insert(0, str(PCK / "engine"))
sys.path.insert(0, str(MATH / "Core1Authoring" / "engine"))

import promote_math_pck as pm
from author_math_core1 import load_candidate_bundle


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        return
    raise AssertionError(f"expected {code}")


CANDIDATE_REGISTRY, CANDIDATE_ASSETS = load_candidate_bundle(PCK / "registry" / "math-pck-candidates.json")
PRODUCTION = load(PCK / "registry" / "math-pck-promotion-registry.json")
REGISTRY_SCHEMA = load(PCK / "contracts" / "math-pck-promotion-registry.schema.json")
RECORD_SCHEMA = load(PCK / "contracts" / "math-pck-promotion-review-record.schema.json")
CAPS, FAMILIES, REPRESENTATIONS = pm.subject_authorities()

# --- the mechanism runs, deterministically, over every candidate -------------
built, refusals = pm.build_registry(CANDIDATE_REGISTRY, CANDIDATE_ASSETS)
built_again, _ = pm.build_registry(CANDIDATE_REGISTRY, CANDIDATE_ASSETS)
assert built == built_again, "promotion pipeline must be deterministic"
assert not refusals, refusals
assert len(built["promotions"]) == len(CANDIDATE_ASSETS)
Draft202012Validator(REGISTRY_SCHEMA).validate(built)

# --- the committed production registry is exactly what the mechanism emits ---
assert PRODUCTION == built, "committed promotion registry must be reproducible from the pipeline"
assert PRODUCTION["registry_class"] == "PRODUCTION"
assert PRODUCTION["promotions"], "PCK_REGISTRY_EMPTY_BUT_RELEASE_CLAIMED"

# --- no fabricated expert review --------------------------------------------
for rec in PRODUCTION["promotions"]:
    assert rec["promotion_status"] == "PROVISIONAL_PROMOTED", rec["asset_id"]
    assert rec["promotion_class"] == "AI_ASSISTED_PROVISIONAL"
    assert rec["review_authority"] == "AI_ASSISTED_REFERENCE_REVIEW"
    assert rec["review_source"] == "AI_ASSISTED_REFERENCE_REVIEW"
    assert rec["review_registry_class"] == "AI_ASSISTED"
    assert rec["evidence_class"] == "REPOSITORY_AUTHORITY_PLUS_AI_ASSISTED_DRAFT"
    assert rec["authoring_legal"] is True
    assert rec["producer_legal"] is False
    assert rec["release_legal"] is False
    assert rec["expert_review_state"] == {"SUBJECT_EXPERT_PASS": "PENDING", "PEDAGOGY_EXPERT_PASS": "PENDING"}
    assert rec["lifecycle_state"] == pm.TERMINAL_LIFECYCLE_STATE
    assert rec["subject_scope"] == pm.SUBJECT_SCOPE
    # every promoted entry binds the full generic obligation set
    for field in ("capability_refs", "applicability_conditions", "known_limitations", "provenance", "promoted_version"):
        assert rec[field], (rec["asset_id"], field)
    assert [s["stage"] for s in rec["review_pipeline"]] == pm.PROMOTION_STAGES
    assert all(s["status"] == "PASS" for s in rec["review_pipeline"])
    assert all(s["review_authority"] in pm.MACHINE_AUTHORITIES for s in rec["review_pipeline"])

# --- the pipeline is subject-wide, not topic-keyed ---------------------------
promoted_caps = {c for rec in PRODUCTION["promotions"] for c in rec["capability_refs"]}
assert promoted_caps.issubset(set(CAPS)), "promotions must resolve against the subject scope authority"
assert len({rec["subject_scope"] for rec in PRODUCTION["promotions"]}) == 1

# --- stage records are schema-valid and digest-sealed ------------------------
sample = CANDIDATE_ASSETS[0]
records = pm.run_pipeline(sample, CAPS, FAMILIES, REPRESENTATIONS)
assert [r["stage"] for r in records] == pm.PROMOTION_STAGES
for record in records:
    Draft202012Validator(RECORD_SCHEMA).validate(record)
    assert record["record_digest"] == pm.digest(record, "record_digest")
    assert record["human_review_intake_ref"] is None

# --- falsifiers --------------------------------------------------------------
# PCK_PROMOTION_STAGE_SKIPPED
expect("PCK_PROMOTION_STAGE_SKIPPED", lambda: pm.assert_pipeline_integrity(records[:3]))
# PCK_PROMOTION_STAGE_ORDER_VIOLATION
expect("PCK_PROMOTION_STAGE_ORDER_VIOLATION", lambda: pm.assert_pipeline_integrity(list(reversed(records))))
# PCK_PROMOTION_DIGEST_MISMATCH on a tampered stage record
tampered = copy.deepcopy(records)
tampered[0]["checks_passed"] = tampered[0]["checks_passed"] + ["FABRICATED_CHECK"]
expect("PCK_PROMOTION_DIGEST_MISMATCH", lambda: pm.assert_pipeline_integrity(tampered))
# FABRICATED_EXPERT_REVIEW_AUTHORITY: an expert-authority record with no intake evidence
forged = copy.deepcopy(records)
extra = copy.deepcopy(records[2])
extra["review_authority"] = "SUBJECT_EXPERT_PASS"
extra["human_review_intake_ref"] = None
extra["record_digest"] = pm.digest(extra, "record_digest")
forged.append(extra)
expect("FABRICATED_EXPERT_REVIEW_AUTHORITY", lambda: pm.assert_pipeline_integrity(forged))
# FABRICATED_EXPERT_REVIEW_AUTHORITY: a provisional promotion relabelled as human-reviewed
lying = copy.deepcopy(PRODUCTION["promotions"][0])
lying["promotion_status"] = "PROMOTED"
lying["review_source"] = "HUMAN_REVIEW_INTAKE_RESULT"
lying["promotion_digest"] = pm.digest(lying, "promotion_digest")
expect("FABRICATED_EXPERT_REVIEW_AUTHORITY", lambda: pm.assert_promotion_honesty(lying))
# PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL
greedy = copy.deepcopy(PRODUCTION["promotions"][0])
greedy["producer_legal"] = True
greedy["promotion_digest"] = pm.digest(greedy, "promotion_digest")
expect("PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL", lambda: pm.assert_promotion_honesty(greedy))
# TOPIC_SPECIFIC_PROMOTION_RECORD
topic_keyed = copy.deepcopy(PRODUCTION["promotions"][0])
topic_keyed["subject_scope"] = "MATHEMATICS_PERMUTATIONS_ONLY"
topic_keyed["promotion_digest"] = pm.digest(topic_keyed, "promotion_digest")
expect("TOPIC_SPECIFIC_PROMOTION_RECORD", lambda: pm.assert_promotion_honesty(topic_keyed))
# PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE
out_of_scope = copy.deepcopy(sample)
out_of_scope["capability_refs"] = ["MATH-NOT-IN-ASSESSMENT-SCOPE"]
out_of_scope["asset_digest"] = pm.digest(out_of_scope, "asset_digest")
record = pm.review_scope(out_of_scope, CAPS)
assert record["status"] == "FAIL"
assert any(f.startswith("PCK_PROMOTION_CAPABILITY_OUT_OF_SUBJECT_SCOPE") for f in record["findings"])
# PCK_PROMOTION_FAMILY_UNRESOLVED
bad_family = copy.deepcopy(sample)
bad_family["transfer_family"] = "MATH-PF-DOES-NOT-EXIST"
bad_family["asset_digest"] = pm.digest(bad_family, "asset_digest")
record = pm.review_subject(bad_family, CAPS, FAMILIES, REPRESENTATIONS)
assert record["status"] == "FAIL"
assert any(f.startswith("PCK_PROMOTION_FAMILY_UNRESOLVED") for f in record["findings"])
# PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE
gutted = copy.deepcopy(sample)
gutted["reconstruction_route"] = gutted["reconstruction_route"][:1]
gutted["asset_digest"] = pm.digest(gutted, "asset_digest")
record = pm.review_pedagogical(gutted)
assert record["status"] == "FAIL"
assert any(f.startswith("PCK_PEDAGOGICAL_STRUCTURE_INCOMPLETE") for f in record["findings"])
# PCK_PROVENANCE_UNDECLARED
no_prov = copy.deepcopy(sample)
no_prov["provenance"] = {"evidence_class": "HEARSAY", "source_refs": [], "authoring_origin": "UNKNOWN"}
no_prov["asset_digest"] = pm.digest(no_prov, "asset_digest")
record = pm.review_evidence_provenance(no_prov)
assert record["status"] == "FAIL"
assert any(f.startswith("PCK_PROVENANCE_UNDECLARED") for f in record["findings"])
# PCK_PROMOTION_DIGEST_MISMATCH on an unsealed asset
unsealed = copy.deepcopy(sample)
unsealed["anchor"] = unsealed["anchor"] + " tampered"
record = pm.review_evidence_provenance(unsealed)
assert record["status"] == "FAIL"
assert any(f.startswith("PCK_PROMOTION_DIGEST_MISMATCH") for f in record["findings"])
# a failing stage refuses promotion instead of downgrading it silently
promotion, blockers = pm.build_promotion(sample, pm.run_pipeline(gutted, CAPS, FAMILIES, REPRESENTATIONS))
assert promotion is None and blockers
# PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH
broken_registry = copy.deepcopy(CANDIDATE_REGISTRY)
broken_registry["registry_digest"] = "0" * 64
expect(
    "PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH",
    lambda: pm.build_registry(broken_registry, CANDIDATE_ASSETS),
)
# PCK_PROMOTION_UNKNOWN_ASSET
expect(
    "PCK_PROMOTION_UNKNOWN_ASSET",
    lambda: pm.build_registry(CANDIDATE_REGISTRY, CANDIDATE_ASSETS, {"MATH-PCK-NOT-A-REAL-ASSET-v1": {}}),
)
# TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE
test_intake = {
    "intake_id": "HRI-TEST",
    "mode": "TEST_ONLY",
    "fixture_class": "TEST_ONLY_SYNTHETIC",
    "release_evidence_eligible": False,
    "intake_status": "READY",
    "candidate_sha256": sample["asset_digest"],
    "quality_review_summary": {"SUBJECT": "PASS", "PEDAGOGY": "PASS"},
}
expect("TEST_ONLY_REVIEW_USED_AS_EXPERT_EVIDENCE", lambda: pm.expert_records(sample, test_intake))
# PCK_PROMOTION_EVIDENCE_UNBOUND: a real intake bound to the wrong artifact
unbound_intake = dict(test_intake, mode="REAL_RELEASE", fixture_class="REAL", release_evidence_eligible=True, candidate_sha256="f" * 64)
expect("PCK_PROMOTION_EVIDENCE_UNBOUND", lambda: pm.expert_records(sample, unbound_intake))

# --- the expert path is real: given genuine authorized evidence it promotes ---
real_intake = dict(test_intake, mode="REAL_RELEASE", fixture_class="REAL", release_evidence_eligible=True)
expert = pm.run_pipeline(sample, CAPS, FAMILIES, REPRESENTATIONS, real_intake)
promoted, blockers = pm.build_promotion(sample, expert)
assert not blockers
assert promoted["promotion_status"] == "PROMOTED"
assert promoted["promotion_class"] == "HUMAN_REVIEWED_PRODUCTION"
assert promoted["review_source"] == "HUMAN_REVIEW_INTAKE_RESULT"
assert promoted["review_registry_class"] == "REAL"
assert promoted["producer_legal"] is True and promoted["release_legal"] is True
assert promoted["expert_review_state"] == {"SUBJECT_EXPERT_PASS": "PASS", "PEDAGOGY_EXPERT_PASS": "PASS"}
assert promoted["evidence_class"] == "HUMAN_REVIEWED_SUBJECT_PCK"

# --- no such evidence exists in this repository ------------------------------
assert not any(rec["producer_legal"] for rec in PRODUCTION["promotions"]), "FAKE_HUMAN_REVIEW_STATE"

print("MATH M-G PCK promotion pipeline falsifiers PASS")
print("MATH M-G promotion registry exercised: %d provisional, 0 producer-legal, expert review PENDING" % len(PRODUCTION["promotions"]))
