"""Grounded specialist claims and complete two-sided review obligations."""

from __future__ import annotations

from .contracts import digest, require, strings, text, unique, validate_dag


KINDS = {
    "CORE1": {"DEFINITION", "MODEL", "LAW", "DERIVATION", "VALIDITY", "REPRESENTATION", "PREREQUISITE"},
    "CORE2": {"DEMAND", "RECOGNITION", "SOLUTION_ROUTE", "MISCONCEPTION", "TRANSFER", "EVIDENCE_GAP"},
}
DISPOSITIONS = {"CONFIRMED", "REFINED", "UNSUPPORTED", "CONTRADICTED", "OUT_OF_SCOPE", "UNKNOWN"}


def validate_specialist(payload: dict, role: str, context: dict) -> dict:
    require(payload.get("role") == role, "SPECIALIST_ROLE_MISMATCH")
    require(payload.get("visible_upstream_digests") == [], "BLIND_PASS_UPSTREAM_VISIBLE")
    claims = unique(payload.get("claims", []), "claim_id", "CLAIM_ID_DUPLICATE")
    if role == "CORE1":
        require(bool(claims), "SEMANTIC_CLAIMS_REQUIRED")
    evidence = {x["source_id"]: x for x in context["manifest"]["items"]}
    caps = set(context["capability_ids"])
    for claim in claims.values():
        _validate_claim(claim, role, evidence, caps)
    validate_dag(list(claims.values()), "claim_id", "dependency_claim_ids")
    if role == "CORE2":
        _validate_demand(payload, context)
    return payload


def _validate_claim(claim: dict, role: str, evidence: dict, caps: set[str]) -> None:
    require(claim.get("kind") in KINDS[role], "CLAIM_KIND_WRONG_ROLE", claim["claim_id"])
    require(claim.get("capability_id") in caps, "CLAIM_CAPABILITY_OUTSIDE_ASSIGNMENT")
    text(claim.get("statement"), "CLAIM_STATEMENT_REQUIRED")
    text(claim.get("rationale"), "CLAIM_REASONING_REQUIRED")
    refs = strings(claim.get("source_refs"), "CLAIM_SOURCE_REQUIRED")
    require(set(refs) <= set(evidence), "CLAIM_UNKNOWN_SOURCE")
    require(all(evidence[x]["availability"] in {"PRESENT", "PARTIAL"} for x in refs),
            "CLAIM_SOURCE_UNAVAILABLE")
    strings(claim.get("conditions"), "CLAIM_CONDITIONS_REQUIRED")
    if claim["kind"] == "DERIVATION":
        steps = claim.get("steps", [])
        require(bool(steps), "DERIVATION_STEPS_REQUIRED")
        for step in steps:
            for field in ("from", "to", "justification", "meaning"):
                text(step.get(field), "DERIVATION_BRIDGE_REQUIRED")


def _validate_demand(payload: dict, context: dict) -> None:
    state = payload.get("assessment_evidence")
    require(state in {"OBSERVED", "THIN_EVIDENCE", "ZERO_EVIDENCE"}, "ASSESSMENT_EVIDENCE_REQUIRED")
    questions = payload.get("questions", [])
    unique(questions, "question_id", "QUESTION_ID_DUPLICATE")
    require(bool(questions) == (state != "ZERO_EVIDENCE"), "ASSESSMENT_ABSENCE_DRIFT")
    for question in questions:
        strings(question.get("capability_ids"), "QUESTION_CAPABILITIES_REQUIRED")
        require(set(question["capability_ids"]) <= set(context["available_capability_ids"]),
                "QUESTION_CAPABILITY_OUTSIDE_ASSIGNMENT")
        for field in ("stem", "source_locator", "first_nonobvious_move", "wrong_chain"):
            text(question.get(field), "QUESTION_INTELLIGENCE_REQUIRED")
        strings(question.get("solution_steps"), "SOURCE_SOLUTION_REQUIRED")
        require(isinstance(question.get("source_record"), dict), "SOURCE_RECORD_BINDING_REQUIRED")
    for family in payload.get("transfer_families", []):
        text(family.get("family_id"), "TRANSFER_FAMILY_ID_REQUIRED")
        strings(family.get("capability_ids"), "TRANSFER_CAPABILITIES_REQUIRED")
        strings(family.get("safe_axes"), "TRANSFER_AXES_REQUIRED")
        require(isinstance(family.get("conditional_axes"), list), "CONDITIONAL_AXES_REQUIRED")
        strings(family.get("forbidden_axes"), "FORBIDDEN_AXES_REQUIRED")
        require(family.get("basis") in {"OBSERVED_FAMILY", "SEMANTIC_DESIGN"}, "TRANSFER_BASIS_REQUIRED")
        if state == "ZERO_EVIDENCE":
            require(family["basis"] == "SEMANTIC_DESIGN", "INVENTED_ASSESSMENT_PATTERN")


def validate_claim_review(payload: dict, packets: dict, actor: str) -> dict:
    all_claims = {}
    for stage in ("FIRST_CORE", "SECOND_CORE_BLIND"):
        packet = packets[stage]
        for claim in packet["payload"]["claims"]:
            cid = claim["claim_id"]
            require(cid not in all_claims, "CROSS_ROLE_CLAIM_ID_COLLISION", cid)
            all_claims[cid] = (claim, packet["actor"], packet["digest"])
    reviews = unique(payload.get("reviews", []), "claim_id", "REVIEW_CLAIM_DUPLICATE")
    require(set(reviews) == set(all_claims), "CRITICAL_CLAIM_REVIEW_COVERAGE")
    for cid, review in reviews.items():
        claim, producer, fingerprint = all_claims[cid]
        require(actor != producer, "CLAIM_SELF_VALIDATION", cid)
        require(review.get("packet_digest") == fingerprint, "REVIEW_PACKET_BINDING_MISMATCH", cid)
        require(review.get("claim_digest") == digest(claim), "REVIEW_CLAIM_BINDING_MISMATCH", cid)
        require(review.get("disposition") in DISPOSITIONS, "REVIEW_DISPOSITION_INVALID", cid)
        strings(review.get("source_refs"), "REVIEW_SOURCE_REQUIRED")
        text(review.get("independent_reasoning"), "INDEPENDENT_REVIEW_REASONING_REQUIRED")
        if review["disposition"] == "REFINED":
            text(review.get("refined_statement"), "REFINEMENT_REQUIRED")
            require(review.get("requires_new_semantics") is False, "REFINEMENT_REQUIRES_NEW_REVIEW")
    require(payload.get("new_claims") == [], "NEW_REVIEW_CLAIMS_REQUIRE_SEPARATE_CYCLE")
    return payload


def compile_join(packets: dict, context: dict) -> dict:
    review = packets["CLAIM_REVIEW"]["payload"]
    unresolved = [x for x in review["reviews"] if x["disposition"] not in {"CONFIRMED", "REFINED", "OUT_OF_SCOPE"}]
    require(not unresolved, "JOIN_UNRESOLVED_CLAIMS", ",".join(x["claim_id"] for x in unresolved))
    claims = {c["claim_id"]: c for stage in ("FIRST_CORE", "SECOND_CORE_BLIND")
              for c in packets[stage]["payload"]["claims"]}
    admitted = {x["claim_id"] for x in review["reviews"] if x["disposition"] in {"CONFIRMED", "REFINED"}}
    for cid in admitted:
        require(set(claims[cid].get("dependency_claim_ids", [])) <= admitted,
                "JOIN_CLAIM_PREREQUISITE_NOT_ADMITTED", cid)
    obligations = unique(review.get("obligations", []), "obligation_id", "OBLIGATION_ID_DUPLICATE")
    covered = set()
    for obligation in obligations.values():
        refs = strings(obligation.get("claim_ids"), "OBLIGATION_CLAIMS_REQUIRED")
        require(set(refs) <= admitted, "OBLIGATION_UNREVIEWED_CLAIM")
        cap = obligation.get("capability_id")
        require(cap in context["capability_ids"], "OBLIGATION_UNKNOWN_CAPABILITY")
        require(any(claims[x]["capability_id"] == cap and claims[x]["kind"] in KINDS["CORE1"] for x in refs),
                "OBLIGATION_SEMANTIC_GROUNDING_REQUIRED")
        strings(obligation.get("required_components"), "OBLIGATION_COMPONENTS_REQUIRED")
        text(obligation.get("acceptance_criterion"), "OBLIGATION_ACCEPTANCE_REQUIRED")
        covered.add(cap)
    require(covered == set(context["capability_ids"]), "JOIN_CAPABILITY_COVERAGE")
    return {"obligations": list(obligations.values()), "admitted_claim_ids": sorted(admitted),
            "review_digest": packets["CLAIM_REVIEW"]["digest"], "scope": context["subtopic_ids"]}
