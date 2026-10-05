"""Explicit product direction; knowledge percentages never select modes."""

from __future__ import annotations

from copy import deepcopy

from .contracts import require, strings, text


MODES = {"STARTER", "PRACTICE", "REVISION", "COMPETITION"}
PURPOSES = {"FIRST_STUDY", "PRACTICE", "REVISION", "COMPETITIVE_EXAM", "TARGETED_REPAIR"}
SUPPORTS = {"GUIDED", "OPTIONAL_HINTS", "INDEPENDENT"}
NOVELTY = ("DIRECT", "NEAR_TRANSFER", "STRUCTURAL_VARIATION", "MIXED_SYNTHESIS")


def validate_request(request: dict) -> dict:
    out = deepcopy(request)
    text(out.get("request_id"), "REQUEST_ID_REQUIRED")
    require(out.get("subject") in {"Physics", "Mathematics", "Chemistry"},
            "SUBJECT_REQUIRED")
    text(out.get("topic"), "TOPIC_REQUIRED")
    require(out.get("run_kind") in {"PRODUCTION", "PROCESS_FIXTURE"}, "RUN_KIND_REQUIRED")
    require(out.get("practice_mode") in MODES, "CORE2A_USER_PURPOSE_REQUIRED")
    require(out.get("learning_purpose") in PURPOSES, "LEARNING_PURPOSE_REQUIRED")
    text(out.get("owner_basis"), "OWNER_BASIS_REQUIRED")
    strings(out.get("products"), "PRODUCTS_REQUIRED")
    require(set(out["products"]) <= {"CORE1", "CORE2", "CORE1A", "CORE2A"},
            "PRODUCT_UNSUPPORTED")
    _validate_practice(out)
    _validate_readiness(out.get("learner", {}))
    return out


def _validate_practice(request: dict) -> None:
    practice = request.get("practice", {})
    strings(practice.get("allowed_support"), "SUPPORT_POLICY_REQUIRED")
    require(set(practice["allowed_support"]) <= SUPPORTS, "SUPPORT_POLICY_INVALID")
    require(practice.get("max_novelty") in NOVELTY, "NOVELTY_POLICY_REQUIRED")
    require(practice.get("source_selection") in {"ALL_ELIGIBLE", "FIRST_PER_SUBTOPIC",
            "REPRESENTATIVE_PER_SUBTOPIC", "EXPLICIT", "GENERATED_ONLY"}, "SOURCE_SELECTION_REQUIRED")
    require(type(practice.get("max_pages_per_question")) is int and
            practice["max_pages_per_question"] in {1, 2}, "PAGE_BUDGET_INVALID")
    require(practice.get("source_on_attempt_page") is True, "SHEET1_SOURCE_REQUIRED")
    require(practice.get("hint_visibility") in {"VISIBLE_TECHNICAL", "OPTIONAL_AFTER_ATTEMPT", "NONE"},
            "HINT_VISIBILITY_REQUIRED")
    counts = practice.get("required_generated_slots")
    require(isinstance(counts, dict), "GENERATED_MIX_REQUIRED")
    for slot, count in counts.items():
        require(slot in NOVELTY and type(count) is int and count >= 0, "GENERATED_MIX_INVALID", slot)
    if practice["source_selection"] == "EXPLICIT":
        strings(practice.get("source_question_ids"), "EXPLICIT_SOURCE_SELECTION_REQUIRED")
    if request["practice_mode"] == "STARTER":
        require(practice["max_novelty"] in {"DIRECT", "NEAR_TRANSFER"}, "STARTER_NOVELTY_CONFLICT")
    if request["practice_mode"] == "COMPETITION":
        require(practice.get("benchmark_policy") in {"REQUIRED", "OWNER_WAIVED"},
                "COMPETITION_BENCHMARK_POLICY_REQUIRED")
        if practice["benchmark_policy"] == "OWNER_WAIVED":
            text(practice.get("benchmark_waiver_reason"), "BENCHMARK_WAIVER_REASON_REQUIRED")


def _validate_readiness(learner: dict) -> None:
    prior = learner.get("reported_knowledge_percent")
    require(prior is None or (type(prior) in {int, float} and 0 <= prior <= 100),
            "KNOWLEDGE_PRIOR_INVALID")
    for row in learner.get("capabilities", []):
        text(row.get("capability_id"), "LEARNER_CAPABILITY_ID_REQUIRED")
        require(row.get("state") in {"UNKNOWN", "DEVELOPING", "READY"}, "LEARNER_STATE_INVALID")
        if row["state"] != "UNKNOWN":
            require(row.get("evidence_kind") in {"OWNER_REPORT", "LEARNER_RESPONSE",
                    "DIAGNOSTIC", "TEACHER_OBSERVATION"}, "LEARNER_EVIDENCE_REQUIRED")
            strings(row.get("evidence_refs"), "LEARNER_EVIDENCE_REQUIRED")


def capability_state(request: dict, capability_id: str) -> str:
    rows = request.get("learner", {}).get("capabilities", [])
    matches = [x for x in rows if x["capability_id"] == capability_id]
    require(len(matches) <= 1, "DUPLICATE_LEARNER_CAPABILITY", capability_id)
    return matches[0]["state"] if matches else "UNKNOWN"
