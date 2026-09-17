#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_ccu import validate as validate_ccu


def load(rel):
    return json.loads((ROOT / rel).read_text())


def must_fail(doc, contains=None):
    try:
        validate_ccu(doc)
    except AssertionError as e:
        if contains is not None:
            assert contains in str(e), (contains, str(e))
        return
    raise AssertionError("expected CCU validation failure")


CCU = load("topics/m2d-sba23-ccu.v1.json")
PLAN = load("topics/m2d-sba23-v8-realization-plan.json")
CCU_POLICY = load("policy/content-custody-coverage-unit.v1.json")
CDAU = load("policy/core-governance-cdau.v2.json")
SDU = load("policy/study-differentiation-unit.v2.json")
LAU = load("policy/learner-adaptation-unit.v2.json")
BADGES = load("policy/question-badge-metadata.v1.json")

# Positive process golden.
results = validate_ccu(CCU)
assert len(results) == len(CCU["similarity_pairs"])
assert CCU["production_release_authorized"] is False
assert CCU["receipts"]["coverage_receipt"] == "PASS"
assert CCU["receipts"]["question_custody_receipt"] == "PASS"
assert CCU["receipts"]["duplication_receipt"] == "PASS"
assert CCU["receipts"]["source_integrity_receipt"] == "HELD"

# CCU must sit before CDAU and may not be bypassed by owner control.
assert CDAU["authority_order"].index("CCU") < CDAU["authority_order"].index("CDAU")
assert CDAU["owner_control"]["may_bypass_ccu_receipts"] is False
assert "G_CUSTODY_COVERAGE" in CDAU["release_gates"]

# Similarity thresholds are deterministic engineering gates; semantic cosine is deliberately not universal.
sim = CCU_POLICY["similarity"]
assert sim["lexical_five_shingle_jaccard"]["high_duplicate_risk_at_or_above"] == 0.90
assert sim["lexical_five_shingle_jaccard"]["review_at_or_above"] == 0.80
assert sim["structural_fingerprint"]["block_at_or_above_when_same_or_equivalent_pedagogical_usage"] == 0.85
assert sim["structural_fingerprint"]["review_at_or_above"] == 0.70
assert sim["semantic_similarity"]["hardcoded_universal_cosine_threshold_allowed"] is False
assert sim["semantic_similarity"]["threshold_mode"] == "CALIBRATED_ON_LABELLED_PHYSICS_PAIRS"

# Required learner-facing badges include the custody essentials.
required_badges = set(BADGES["student_facing_badges"]["required_for_every_released_question"])
assert required_badges == {"CORE", "BUCKET", "CONCEPT", "SOURCE", "ANSWER_STATUS"}
assert BADGES["display_rules"]["source_identity_must_be_visible_to_learner"] is True
assert BADGES["display_rules"]["frozen_source_question_number_must_be_retained"] is True

# SBA23 difficulty must be evidenced, not asserted only by a badge.
d = PLAN["difficulty_receipt"]
scores = d["dimension_scores"]
assert set(scores) == set(SDU["difficulty"]["evidence_profile_dimensions"])
assert all(SDU["difficulty"]["dimension_scale"]["minimum"] <= v <= SDU["difficulty"]["dimension_scale"]["maximum"] for v in scores.values())
assert sum(v == 3 for v in scores.values()) >= 2
assert d["final_badge"] == "HARD"
assert d["psychometric_claim"] is False
assert PLAN["sdu_realization"]["student_knowledge_pct_used"] is False

# Purpose receipts prove 1A/1B are not merely duplicate books.
assert PLAN["purpose_receipts"]["CORE1A"]["status"] == "PASS"
assert PLAN["purpose_receipts"]["CORE1B"]["status"] == "PASS"
assert PLAN["purpose_receipts"]["CORE1B"]["fragile_checkpoint_without_generative_transformation"] is False
assert PLAN["purpose_receipts"]["CORE1B"]["passive_reference_only_checkpoint"] is False

# Learner fit is explicit. With no usable knowledge %, the pilot must say it is owner-routed, not knowledge-validated.
fit = PLAN["lau_realization"]["design_pilot_fit_receipt"]
assert fit["selection_basis"] == "OWNER_OVERRIDE"
assert fit["fit_prediction"] == "OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED"
assert fit["psychometric_claim"] is False
assert PLAN["lau_realization"]["core2a_production_legal_items"] == []
assert PLAN["lau_realization"]["core2b_production_transfer_items"] == []
assert LAU["no_silent_default"] is True
assert LAU["post_use_evidence"]["knowledge_percent_is_mastery_claim_by_itself"] is False

# Falsifier 1: silently skipping one applicable asset disposition must fail.
bad = copy.deepcopy(CCU)
bad["coverage_matrix"] = [r for r in bad["coverage_matrix"] if not (r["asset_id"] == "EQ-ML-GALILEAN-ADD-01" and r["core"] == "CORE1B")]
must_fail(bad, "silent asset omission")

# Falsifier 2: learner-facing question without canonical answer/resolution must fail.
bad = copy.deepcopy(CCU)
q = next(q for q in bad["question_records"] if q["question_id"] == "AC-M23-C1B-001")
q["answer"] = {"answer_type": "HELD", "status": "HELD"}
must_fail(bad, "lacks canonical resolution")

# Falsifier 3: frozen source number may not be renumbered.
bad = copy.deepcopy(CCU)
q = next(q for q in bad["question_records"] if q["question_id"] == "SRC-M23-Q15")
q["display_number"] = "Question 3"
must_fail(bad, "frozen source number changed")

# Falsifier 4: an author-created question may not impersonate source material.
bad = copy.deepcopy(CCU)
q = next(q for q in bad["question_records"] if q["question_id"] == "AC-M23-C1A-001")
q["display_source_label"] = "SOURCE Q15"
must_fail(bad, "source identity hidden")

# Falsifier 5: exact numeric/example reuse across adjacent A/B layers is blocked unless explicit FADING_ANCHOR.
bad = copy.deepcopy(CCU)
left = next(q for q in bad["question_records"] if q["question_id"] == "AC-M23-C1A-001")
right = next(q for q in bad["question_records"] if q["question_id"] == "AC-M23-C1B-001")
right["example_fingerprint"] = copy.deepcopy(left["example_fingerprint"])
pair = next(p for p in bad["similarity_pairs"] if p["left_question_id"] == "AC-M23-C1A-001")
pair["usage_equivalent"] = True
pair["relationship"] = "PEDAGOGICAL_TRANSFORMATION"
must_fail(bad, "exact numeric dataset reused across adjacent layers")

print("Physics CCU V8 custody/coverage/difficulty/fit falsifiers: PASS")
