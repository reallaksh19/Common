#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from validate_calibration_audit import validate_state  # noqa: E402
from validate_ccu_v2 import validate as validate_ccu  # noqa: E402


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def must_fail(fn, value, contains=None):
    try:
        fn(value)
    except AssertionError as exc:
        if contains:
            assert contains in str(exc), (contains, str(exc))
        return
    raise AssertionError("expected validation failure")


STATE = load("calibration/physics-calibration-state.v1.json")
CCU = load("topics/m2d-sba23-ccu.v1.json")
CCU_POLICY = load("policy/content-custody-coverage-unit.v2.json")
CAL_POLICY = load("policy/calibration-audit-layer.v1.json")

# Positive current maturity state.
assert validate_state(STATE) is True
assert STATE["duplication"]["maturity"] == "ENGINEERING"
assert STATE["difficulty"]["maturity"] == "ENGINEERING"
assert STATE["learner_fit"]["maturity"] == "ENGINEERING"

# Engineering thresholds are review signals, never automatic threshold-only blocks.
assert CCU_POLICY["similarity"]["lexical_five_shingle_jaccard"]["engineering_threshold_action"] == "REVIEW_ONLY"
assert CCU_POLICY["similarity"]["structural_fingerprint"]["engineering_threshold_action"] == "REVIEW_ONLY"
assert CAL_POLICY["duplication_calibration"]["engineering_threshold_action"] == "REVIEW_ONLY"
assert CCU_POLICY["similarity"]["semantic_similarity"]["hardcoded_universal_cosine_threshold_allowed"] is False

# Promotion falsifier 1: merely relabelling ENGINEERING as VALIDATED must fail.
bad_state = copy.deepcopy(STATE)
bad_state["duplication"]["maturity"] = "VALIDATED"
must_fail(validate_state, bad_state, "VALIDATED requires evidence refs")

# Promotion falsifier 2: CALIBRATING also requires actual evidence refs.
bad_state = copy.deepcopy(STATE)
bad_state["difficulty"]["maturity"] = "CALIBRATING"
must_fail(validate_state, bad_state, "CALIBRATING requires evidence refs")

# Baseline CCU remains valid under calibration-aware validator.
base_results = validate_ccu(CCU)
assert CCU["receipts"]["duplication_receipt"] == "PASS"

# Heuristic falsifier: make two adjacent examples structurally very similar but not exact.
# This must require REVIEW, not produce an automatic BLOCK.
review_doc = copy.deepcopy(CCU)
left = next(q for q in review_doc["question_records"] if q["question_id"] == "AC-M23-C1A-001")
right = next(q for q in review_doc["question_records"] if q["question_id"] == "AC-M23-C1B-001")
right["example_fingerprint"] = copy.deepcopy(left["example_fingerprint"])
right["example_fingerprint"]["numeric_values"] = ["7", "11", "37", "0.6", "0.8"]
pair = next(p for p in review_doc["similarity_pairs"] if p["left_question_id"] == "AC-M23-C1A-001" and p["right_question_id"] == "AC-M23-C1B-001")
pair["usage_equivalent"] = True
pair["relationship"] = "PEDAGOGICAL_TRANSFORMATION"
pair.pop("review_disposition", None)
review_doc["receipts"]["duplication_receipt"] = "REVIEW"
review_results = validate_ccu(review_doc)
review_result = next(r for r in review_results if r["left"] == "AC-M23-C1A-001" and r["right"] == "AC-M23-C1B-001")
assert review_result["review_required"] is True
assert review_result["review_disposition"] == "PENDING"
assert review_result["risk"] in {"REVIEW", "HIGH_REVIEW"}

# Same heuristic state may not falsely claim a clean PASS while review is unresolved.
bad_review_receipt = copy.deepcopy(review_doc)
bad_review_receipt["receipts"]["duplication_receipt"] = "PASS"
must_fail(validate_ccu, bad_review_receipt, "similarity review unresolved")

# Deterministic falsifier: exact adjacent numerical/example fingerprint reuse remains a hard block.
exact_duplicate = copy.deepcopy(CCU)
left = next(q for q in exact_duplicate["question_records"] if q["question_id"] == "AC-M23-C1A-001")
right = next(q for q in exact_duplicate["question_records"] if q["question_id"] == "AC-M23-C1B-001")
right["example_fingerprint"] = copy.deepcopy(left["example_fingerprint"])
pair = next(p for p in exact_duplicate["similarity_pairs"] if p["left_question_id"] == "AC-M23-C1A-001" and p["right_question_id"] == "AC-M23-C1B-001")
pair["usage_equivalent"] = True
pair["relationship"] = "PEDAGOGICAL_TRANSFORMATION"
must_fail(validate_ccu, exact_duplicate, "exact numeric dataset reused across adjacent layers")

print("Physics V9 calibration / heuristic-review / deterministic-block falsifiers: PASS")
