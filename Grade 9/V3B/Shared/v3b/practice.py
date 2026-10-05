"""Owner-controlled selection and explicit K/D/T/purpose eligibility ledger."""

from __future__ import annotations

from copy import deepcopy
from difflib import SequenceMatcher

from .answers import validate_answer, validate_help
from .contracts import digest, require, strings, text, unique
from .owner import NOVELTY
from .question_sources import source_questions
from .receipts import supports


def _core2(packets: dict) -> dict:
    return next(packets[x]["payload"] for x in ("FIRST_CORE", "SECOND_CORE_BLIND")
                if packets[x]["payload"]["role"] == "CORE2")


def validate_candidates(payload: dict, packets: dict, context: dict) -> dict:
    items = payload.get("items", [])
    unique(items, "question_id", "GENERATED_QUESTION_ID_DUPLICATE")
    source_ids = set(source_questions(context["manifest"], context["source_root"]))
    for item in items:
        require(item.get("origin") == "GENERATED_ORIGINAL", "CANDIDATE_ORIGIN_INVALID")
        require(item["question_id"] not in source_ids, "GENERATED_SOURCE_ID_COLLISION")
        _validate_item(item, context)
    return payload


def _validate_item(item: dict, context: dict) -> None:
    text(item.get("stem"), "QUESTION_STEM_REQUIRED")
    strings(item.get("capability_ids"), "QUESTION_CAPABILITIES_REQUIRED")
    strings(item.get("solution_capability_ids"), "SOLUTION_CAPABILITIES_REQUIRED")
    strings(item.get("subtopic_ids"), "QUESTION_SUBTOPICS_REQUIRED")
    require(set(item["subtopic_ids"]) <= set(context["subtopic_ids"]), "QUESTION_OUTSIDE_BUNDLE")
    require(item.get("novelty") in NOVELTY, "QUESTION_NOVELTY_INVALID")
    require(item.get("support_mode") in {"GUIDED", "OPTIONAL_HINTS", "INDEPENDENT"}, "QUESTION_SUPPORT_INVALID")
    require(item.get("new_semantic_claims") == [], "QUESTION_ADDS_NEW_SEMANTICS")
    provenance = item.get("provenance", {})
    text(provenance.get("display_text"), "SHEET1_SOURCE_REQUIRED")
    if item["origin"] == "GENERATED_ORIGINAL":
        require(provenance.get("official_past_question_claim") is False, "GENERATED_FALSE_OFFICIAL_CLAIM")
        strings(provenance.get("construction_refs"), "CONSTRUCTION_REFERENCES_REQUIRED")
        text(provenance.get("governed_content_anchor"), "GENERATED_CONTENT_ANCHOR_REQUIRED")
    validate_answer(item, context["request"]["subject"])
    validate_help(item)


def compile_eligibility(payload: dict, packets: dict, context: dict) -> dict:
    core2 = _core2(packets)
    sources = deepcopy(core2.get("questions", []))
    for source in sources:
        require(source.get("origin") == "SOURCE_CORE2", "SOURCE_LANE_ORIGIN_INVALID")
        _validate_item(source, context)
    families = unique(core2.get("transfer_families", []), "family_id", "TRANSFER_FAMILY_DUPLICATE")
    all_items = sources + payload["items"]
    unique(all_items, "question_id", "PRACTICE_QUESTION_ID_COLLISION")
    decisions = [_eligibility(item, families, packets, context) for item in all_items]
    eligible = {x["question_id"] for x in decisions if x["status"] == "ELIGIBLE"}
    selected_sources = _select_sources(sources, eligible, context["request"]["practice"])
    selected = selected_sources + [x for x in payload["items"] if x["question_id"] in eligible]
    _validate_mix(selected, context)
    chosen = {x["question_id"] for x in selected}
    for decision in decisions:
        decision["selected"] = decision["question_id"] in chosen
    return {"items": selected, "decisions": decisions,
            "source_custody": [{"question_id": x["question_id"],
                "disposition": "SELECTED" if x["question_id"] in chosen else
                "NOT_SELECTED_BY_OWNER_POLICY" if x["question_id"] in eligible else "HELD_UNTIL_ELIGIBLE"}
                for x in sources], "teaching_digest": packets["TEACHING_RECEIPTS"]["digest"],
            "request_digest": context["request_digest"]}


def _eligibility(item: dict, families: dict, packets: dict, context: dict) -> dict:
    practice = context["request"]["practice"]
    required = set(item["capability_ids"]) | set(item["solution_capability_ids"])
    for hint in item.get("hints", []):
        required.update(hint["capability_ids"])
    family = families.get(item.get("family_id"), {})
    semantics_ok = required <= set(context["available_capability_ids"]) and not item["new_semantic_claims"]
    envelope_ok = bool(family) and required <= set(family.get("capability_ids", []))
    envelope_ok = envelope_ok and item["novelty"] in family.get("allowed_novelty", [])
    axis = item.get("transfer_axis")
    envelope_ok = envelope_ok and axis in family.get("safe_axes", [])
    receipts = deepcopy(packets["TEACHING_RECEIPTS"]["payload"])
    for external in context["external_teaching_packets"].values():
        receipts["capabilities"].extend(external["payload"]["capabilities"])
    missing = supports(receipts, sorted(required), item["support_mode"])
    purpose_ok = item["support_mode"] in practice["allowed_support"]
    purpose_ok = purpose_ok and NOVELTY.index(item["novelty"]) <= NOVELTY.index(practice["max_novelty"])
    checks = {"semantic_scope": semantics_ok, "transfer_envelope": envelope_ok,
              "teaching_support": not missing, "owner_purpose": purpose_ok}
    if item["origin"] == "GENERATED_ORIGINAL":
        checks["near_copy"] = _near_copy_clear(item, context)
        checks["benchmark_policy"] = _benchmarks_valid(item, context["request"])
    reasons = [name.upper() for name, passed in checks.items() if not passed]
    return {"question_id": item["question_id"], "status": "ELIGIBLE" if not reasons else "HELD",
            "intersection": checks, "reason_codes": reasons, "missing_teaching_support": missing}


def _near_copy_clear(item: dict, context: dict) -> bool:
    normalize = lambda value: " ".join(value.casefold().split())
    candidate = normalize(item["stem"])
    sources = source_questions(context["manifest"], context["source_root"])
    return all(SequenceMatcher(None, candidate, normalize(x["record"]["stem"])).ratio() < 0.9
               for x in sources.values())


def _benchmarks_valid(item: dict, request: dict) -> bool:
    refs = item.get("benchmarks", [])
    if refs and request["practice_mode"] != "COMPETITION":
        return False
    if request["practice_mode"] != "COMPETITION" or request["practice"]["benchmark_policy"] == "OWNER_WAIVED":
        return True
    if len({x.get("source_id") for x in refs}) < 2:
        return False
    return all(x.get("role") == "CONSTRUCTION_REFERENCE" and x.get("curriculum_authority") is False
               and x.get("locator") and x.get("inspected_design_feature") for x in refs)


def _select_sources(sources: list[dict], eligible: set[str], policy: dict) -> list[dict]:
    rows = [x for x in sources if x["question_id"] in eligible]
    selection = policy["source_selection"]
    if selection == "GENERATED_ONLY":
        return []
    if selection == "ALL_ELIGIBLE":
        return rows
    if selection == "EXPLICIT":
        required = policy["source_question_ids"]
        require(set(required) <= eligible, "EXPLICIT_SOURCE_ITEM_NOT_ELIGIBLE")
        by_id = {x["question_id"]: x for x in rows}
        return [by_id[x] for x in required]
    groups = {}
    for row in rows:
        groups.setdefault(row["subtopic_ids"][0], []).append(row)
    if selection == "FIRST_PER_SUBTOPIC":
        return [group[0] for group in groups.values()]
    return [max(group, key=lambda x: (x.get("demand_rank", 0), -group.index(x))) for group in groups.values()]


def _validate_mix(selected: list[dict], context: dict) -> None:
    if "CORE2A" in context["request"]["products"]:
        require(bool(selected), "NO_ELIGIBLE_OWNER_PRACTICE")
    for sid in context["subtopic_ids"]:
        for slot, minimum in context["request"]["practice"]["required_generated_slots"].items():
            count = sum(x["origin"] == "GENERATED_ORIGINAL" and x["novelty"] == slot and sid in x["subtopic_ids"] for x in selected)
            require(count >= minimum, "OWNER_PRACTICE_MIX_UNSATISFIED", f"{sid}:{slot}:{count}/{minimum}")


def validate_practice_review(review: dict, packet: dict, actor: str) -> dict:
    require(review.get("practice_digest") == packet["digest"], "PRACTICE_REVIEW_STALE")
    items = unique(packet["payload"]["items"], "question_id", "QUESTION_ID_DUPLICATE")
    rows = unique(review.get("items", []), "question_id", "QUESTION_REVIEW_DUPLICATE")
    require(set(rows) == set(items), "QUESTION_REVIEW_COVERAGE")
    for qid, row in rows.items():
        require(row.get("question_digest") == digest(items[qid]), "QUESTION_REVIEW_CHANGED")
        require(row.get("decision") in {"ACCEPT", "REWORK"}, "QUESTION_REVIEW_DECISION_REQUIRED")
        for field in ("independent_solution", "prompt_case_alignment", "ambiguity_check", "hint_disclosure_check", "provenance_check", "owner_fit_check"):
            text(row.get(field), "QUESTION_REVIEW_REASON_REQUIRED")
        require(row.get("expected_answer") == items[qid]["answer"].get("canonical_answer"), "INDEPENDENT_ANSWER_DISAGREEMENT")
    return review
