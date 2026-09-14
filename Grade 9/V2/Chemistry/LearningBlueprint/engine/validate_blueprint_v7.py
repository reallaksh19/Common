#!/usr/bin/env python3
"""Deterministic Product Assurance Layer for Chemistry LearningBlueprint v7."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class BlueprintV7Error(ValueError):
    pass


CORES = ("CORE1", "CORE1A", "CORE1B", "CORE2", "CORE2A", "CORE2B")
MANDATORY = {"MUST_REALIZE", "MUST_REFERENCE", "MUST_RECONSTRUCT", "MUST_APPLY", "MUST_SELECT_OR_RECONSTRUCT"}
SUPPORT_ORDER = ["CHALLENGE_MINIMAL", "STANDARD", "GUIDED", "FOUNDATION_HIGH_SUPPORT"]


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _require(payload: dict[str, Any], names: set[str], code: str) -> None:
    missing = sorted(names - set(payload))
    if missing:
        raise BlueprintV7Error(f"{code}:{','.join(missing)}")


def _band(value: float, bands: list[dict[str, Any]], code: str) -> str:
    for band in bands:
        if band["min"] <= value <= band["max"]:
            return band["id"]
    raise BlueprintV7Error(code)


def validate_ccbom(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "ccbom_id", "subtopic_id", "registry_ref", "assets", "coverage_summary"}, "CHEM_V7_CCBOM_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "7.0.0":
        raise BlueprintV7Error("CHEM_V7_CCBOM_SCHEMA_INVALID")
    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        raise BlueprintV7Error("CHEM_V7_CCBOM_ASSETS_MISSING")
    legal = set(policy["coverage"]["legal_dispositions"])
    ids: set[str] = set()
    mandatory_total = 0
    mandatory_closed = 0
    unresolved: list[str] = []
    for asset in assets:
        _require(asset, {"asset_id", "asset_class", "authority_ref", "core_dispositions"}, "CHEM_V7_CCBOM_ASSET_REQUIRED_FIELD_MISSING")
        aid = str(asset["asset_id"])
        if not aid or aid in ids:
            raise BlueprintV7Error("CHEM_V7_CCBOM_ASSET_ID_INVALID")
        ids.add(aid)
        dispositions = asset["core_dispositions"]
        if set(dispositions) != set(CORES):
            raise BlueprintV7Error(f"CHEM_V7_CCBOM_CORE_DISPOSITION_INCOMPLETE:{aid}")
        for core in CORES:
            entry = dispositions[core]
            if not isinstance(entry, dict) or not str(entry.get("disposition", "")).strip():
                raise BlueprintV7Error(f"CHEM_V7_CCBOM_BLANK_DISPOSITION:{aid}:{core}")
            state = entry["disposition"]
            if state not in legal:
                raise BlueprintV7Error(f"CHEM_V7_CCBOM_DISPOSITION_INVALID:{aid}:{core}")
            if state in MANDATORY:
                mandatory_total += 1
                if not str(entry.get("realization_ref", "")).strip():
                    unresolved.append(f"{aid}:{core}")
                else:
                    mandatory_closed += 1
    summary = payload["coverage_summary"]
    if summary.get("mandatory_total") != mandatory_total or summary.get("mandatory_closed") != mandatory_closed:
        raise BlueprintV7Error("CHEM_V7_CCBOM_SUMMARY_DRIFT")
    if sorted(summary.get("unresolved_asset_ids", [])) != sorted(unresolved):
        raise BlueprintV7Error("CHEM_V7_CCBOM_UNRESOLVED_LIST_DRIFT")
    if unresolved or mandatory_closed != mandatory_total:
        raise BlueprintV7Error("CHEM_V7_COVERAGE_NOT_CLOSED")
    return {"status": "PASS", "asset_count": len(ids), "mandatory_total": mandatory_total, "coverage_ratio": 1.0}


def _weighted(components: dict[str, Any], weights: dict[str, float], code: str) -> float:
    if set(components) != set(weights):
        raise BlueprintV7Error(f"{code}_COMPONENT_SET_INVALID")
    score = 0.0
    for key, weight in weights.items():
        value = components[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
            raise BlueprintV7Error(f"{code}_COMPONENT_INVALID:{key}")
        score += float(value) * float(weight)
    return round(score, 6)


def validate_similarity(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "non_frozen_prose", "generated_example_comparisons", "ab_comparisons"}, "CHEM_V7_SIMILARITY_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "7.0.0":
        raise BlueprintV7Error("CHEM_V7_SIMILARITY_SCHEMA_INVALID")
    sim = policy["similarity"]
    prose = payload["non_frozen_prose"]
    if prose.get("exclusions_applied") is not True:
        raise BlueprintV7Error("CHEM_V7_SIMILARITY_EXCLUSIONS_NOT_APPLIED")
    if float(prose.get("verbatim_5gram_overlap", 1)) > float(sim["non_frozen_prose"]["max_verbatim_5gram_overlap"]):
        raise BlueprintV7Error("CHEM_V7_PROSE_5GRAM_OVERLAP_EXCESSIVE")
    if int(prose.get("max_identical_contiguous_words", 999999)) > int(sim["non_frozen_prose"]["max_identical_contiguous_words"]):
        raise BlueprintV7Error("CHEM_V7_PROSE_CONTIGUOUS_DUPLICATION")

    example_scores = []
    ep = sim["generated_example"]
    exceptions = set(ep["declared_exceptions"])
    for item in payload["generated_example_comparisons"]:
        score = _weighted(item.get("components", {}), ep["weights"], "CHEM_V7_EXAMPLE_SIMILARITY")
        relation = item.get("relation_type")
        reason = str(item.get("pedagogical_reason", "")).strip()
        exempt = relation in exceptions
        if score >= float(ep["fail_from"]) and not exempt:
            raise BlueprintV7Error("CHEM_V7_EXAMPLE_NEAR_DUPLICATE")
        if float(ep["review_from"]) <= score < float(ep["fail_from"]) and not reason:
            raise BlueprintV7Error("CHEM_V7_EXAMPLE_REVIEW_REASON_MISSING")
        example_scores.append(score)

    ped_scores = []
    pp = sim["pedagogical_ab"]
    for item in payload["ab_comparisons"]:
        comps = item.get("components", {})
        score = _weighted(comps, pp["weights"], "CHEM_V7_PEDAGOGICAL_SIMILARITY")
        relation = item.get("relation_type")
        exempt = relation in exceptions
        if all(float(comps.get(k, 0)) == 1.0 for k in pp["hard_fail_all_same"]) and not exempt:
            raise BlueprintV7Error("CHEM_V7_PEDAGOGICAL_DUPLICATION_HARD_FAIL")
        if score > float(pp["fail_above"]) and not exempt:
            raise BlueprintV7Error("CHEM_V7_PEDAGOGICAL_SIMILARITY_EXCESSIVE")
        if float(pp["review_from"]) <= score <= float(pp["fail_above"]) and not str(item.get("review_reason", "")).strip():
            raise BlueprintV7Error("CHEM_V7_PEDAGOGICAL_REVIEW_REASON_MISSING")
        ped_scores.append(score)
    return {"status": "PASS", "example_scores": example_scores, "pedagogical_scores": ped_scores}


def validate_difficulty(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "kind", "product_mode"}, "CHEM_V7_DIFFICULTY_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "7.0.0":
        raise BlueprintV7Error("CHEM_V7_DIFFICULTY_SCHEMA_INVALID")
    mode = payload["product_mode"]
    if mode in {"CORE1A", "CORE1B"}:
        if payload["kind"] != "INTRINSIC_DIFFICULTY":
            raise BlueprintV7Error("CHEM_V7_CORE1_DIFFICULTY_LABEL_INVALID")
        dims = policy["difficulty"]["core1_intrinsic_dimensions"]
        values = payload.get("dimensions", {})
        if set(values) != set(dims):
            raise BlueprintV7Error("CHEM_V7_DIFFICULTY_DIMENSIONS_INCOMPLETE")
        for key, value in values.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 3:
                raise BlueprintV7Error(f"CHEM_V7_DIFFICULTY_DIMENSION_INVALID:{key}")
        score = int(sum(values.values()))
        derived = _band(score, policy["difficulty"]["bands"], "CHEM_V7_DIFFICULTY_SCORE_OUT_OF_RANGE")
        if payload.get("derived_badge") != derived:
            raise BlueprintV7Error("CHEM_V7_DIFFICULTY_DERIVED_BADGE_DRIFT")
        final = payload.get("final_badge")
        order = ["EASY", "MEDIUM", "HARD"]
        if final not in order:
            raise BlueprintV7Error("CHEM_V7_DIFFICULTY_FINAL_BADGE_INVALID")
        distance = abs(order.index(final) - order.index(derived))
        if distance >= 1 and not str(payload.get("disagreement_reason", "")).strip():
            raise BlueprintV7Error("CHEM_V7_DIFFICULTY_DISAGREEMENT_REASON_MISSING")
        if distance >= 2 and payload.get("explicit_owner_confirmation") is not True:
            raise BlueprintV7Error("CHEM_V7_DIFFICULTY_OWNER_CONFIRMATION_REQUIRED")
        return {"status": "PASS", "kind": "INTRINSIC_DIFFICULTY", "score": score, "derived_badge": derived, "final_badge": final}
    if mode in {"CORE2A", "CORE2B"}:
        if payload["kind"] != "TASK_DEMAND":
            raise BlueprintV7Error("CHEM_V7_CORE2_TASK_DEMAND_LABEL_INVALID")
        score = payload.get("demand_score")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 36:
            raise BlueprintV7Error("CHEM_V7_TASK_DEMAND_SCORE_INVALID")
        expected = _band(float(score), policy["learner_fit"]["demand_bands"], "CHEM_V7_TASK_DEMAND_BAND_UNRESOLVED")
        if payload.get("demand_band") != expected:
            raise BlueprintV7Error("CHEM_V7_TASK_DEMAND_BAND_DRIFT")
        return {"status": "PASS", "kind": "TASK_DEMAND", "score": score, "band": expected}
    return {"status": "PASS", "kind": "BASE_AUTHORITY"}


def validate_purpose(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "product_mode", "observed_actions", "dominant_mode", "major_ttu_count", "learner_generated_major_ttu_count"}, "CHEM_V7_PURPOSE_REQUIRED_FIELD_MISSING")
    mode = payload["product_mode"]
    if mode not in policy["purpose_contracts"]:
        return {"status": "PASS", "base_core": True}
    contract = policy["purpose_contracts"][mode]
    observed = set(payload["observed_actions"])
    missing = sorted(set(contract["mandatory_actions"]) - observed)
    if missing:
        raise BlueprintV7Error(f"CHEM_V7_PURPOSE_MANDATORY_ACTION_MISSING:{','.join(missing)}")
    if payload.get("dominant_mode") == contract["forbidden_dominant_mode"]:
        raise BlueprintV7Error("CHEM_V7_PURPOSE_FORBIDDEN_MODE")
    if mode in {"CORE1B", "CORE2B"}:
        total = int(payload["major_ttu_count"])
        generated = int(payload["learner_generated_major_ttu_count"])
        if total < 1 or generated / total < float(contract["learner_generated_major_ttu_ratio_min"]):
            raise BlueprintV7Error("CHEM_V7_B_LAYER_LEARNER_GENERATION_RATIO_LOW")
    return {"status": "PASS", "product_mode": mode, "purpose_contract_closed": True}


def _support_for(knowledge_pct: float, demand_score: float, policy: dict[str, Any]) -> str:
    kp = policy["learner_fit"]
    kb = _band(knowledge_pct, kp["knowledge_bands"], "CHEM_V7_KNOWLEDGE_BAND_UNRESOLVED")
    db = _band(demand_score, kp["demand_bands"], "CHEM_V7_DEMAND_BAND_UNRESOLVED")
    return kp["support_matrix"][kb][db]


def _raise_support(current: str, minimum: str) -> str:
    return SUPPORT_ORDER[max(SUPPORT_ORDER.index(current), SUPPORT_ORDER.index(minimum))]


def validate_learner_fit(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "product_mode", "question_id", "purpose", "conditioning", "task_demand_score", "compiler_support", "fit_focus", "purpose_used"}, "CHEM_V7_FIT_REQUIRED_FIELD_MISSING")
    if payload["product_mode"] not in {"CORE2A", "CORE2B"}:
        raise BlueprintV7Error("CHEM_V7_FIT_NON_CORE2_PRODUCT")
    if payload.get("purpose_used") is not True:
        raise BlueprintV7Error("CHEM_V7_FIT_PURPOSE_NOT_USED")
    demand = float(payload["task_demand_score"])
    conditioning = payload["conditioning"]
    mode = conditioning.get("mode")
    if mode == "KNOWLEDGE_EVIDENCE":
        pct = conditioning.get("knowledge_percent")
        if not isinstance(pct, (int, float)) or isinstance(pct, bool) or not 0 <= pct <= 100:
            raise BlueprintV7Error("CHEM_V7_FIT_KNOWLEDGE_PERCENT_INVALID")
        support = _support_for(float(pct), demand, policy)
        subdims = conditioning.get("subdimensions", {})
        focus = payload.get("fit_focus", [])
        if not focus:
            raise BlueprintV7Error("CHEM_V7_FIT_FOCUS_MISSING")
        vals = []
        for key in focus:
            value = subdims.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 100:
                raise BlueprintV7Error(f"CHEM_V7_FIT_SUBDIMENSION_INVALID:{key}")
            vals.append(float(value))
        minimum = min(vals)
        if minimum < 35:
            support = _raise_support(support, "GUIDED")
        elif minimum < 50:
            support = _raise_support(support, "STANDARD")
    elif mode == "OWNER_OVERRIDE":
        if "knowledge_percent" in conditioning and conditioning.get("knowledge_percent") is not None:
            raise BlueprintV7Error("CHEM_V7_FIT_OWNER_OVERRIDE_FABRICATED_PERCENT")
        support = conditioning.get("support_band")
        if support not in SUPPORT_ORDER or not str(conditioning.get("reason", "")).strip():
            raise BlueprintV7Error("CHEM_V7_FIT_OWNER_OVERRIDE_INVALID")
    else:
        raise BlueprintV7Error("CHEM_V7_FIT_CONDITIONING_UNRESOLVED")
    if payload.get("compiler_support") != support:
        raise BlueprintV7Error(f"CHEM_V7_FIT_COMPILER_VALIDATOR_MISMATCH:{payload.get('compiler_support')}!={support}")
    return {"status": "PASS", "validator_support": support, "conditioning_mode": mode}


def validate_question_custody(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "question_id", "source_class", "learner_visible_source", "answer_status", "answer_ref", "canonical_solution_ref", "verification_ref"}, "CHEM_V7_QUESTION_CUSTODY_REQUIRED_FIELD_MISSING")
    if payload["schema_version"] != "7.0.0" or payload.get("answer_status") != policy["question_custody"]["answer_status_required"]:
        raise BlueprintV7Error("CHEM_V7_QUESTION_ANSWER_CLOSURE_MISSING")
    if not all(str(payload.get(k, "")).strip() for k in ("question_id", "learner_visible_source", "answer_ref", "canonical_solution_ref", "verification_ref")):
        raise BlueprintV7Error("CHEM_V7_QUESTION_CUSTODY_EMPTY_FIELD")
    if payload["source_class"] == "SOURCE_FROZEN":
        for key in policy["question_custody"]["source_frozen_requires"]:
            if not str(payload.get(key, "")).strip():
                raise BlueprintV7Error(f"CHEM_V7_SOURCE_QUESTION_FIELD_MISSING:{key}")
        if payload.get("stem_identity_status") != "EXACT":
            raise BlueprintV7Error("CHEM_V7_SOURCE_STEM_DRIFT")
        qno = str(payload["source_question_number"])
        if qno not in str(payload["learner_visible_source"]):
            raise BlueprintV7Error("CHEM_V7_SOURCE_QUESTION_NUMBER_NOT_VISIBLE")
    elif payload["source_class"] == "GENERATED_ORIGINAL":
        if not payload.get("generated_grounding_refs"):
            raise BlueprintV7Error("CHEM_V7_GENERATED_QUESTION_GROUNDING_MISSING")
        if "generated" not in str(payload["learner_visible_source"]).lower():
            raise BlueprintV7Error("CHEM_V7_GENERATED_SOURCE_NOT_DISCLOSED")
    else:
        raise BlueprintV7Error("CHEM_V7_SOURCE_CLASS_INVALID")
    return {"status": "PASS", "question_id": payload["question_id"], "source_visible": True, "answer_closed": True}


def validate_badges(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    _require(payload, {"schema_version", "product_mode", "learner_visible_badges", "student_knowledge_percent_visible"}, "CHEM_V7_BADGE_REQUIRED_FIELD_MISSING")
    allowed = set(policy["badges"]["learner_visible"])
    badges = payload["learner_visible_badges"]
    if not isinstance(badges, list) or len(badges) > int(policy["badges"]["learner_visible_recommended_max_per_page"]):
        raise BlueprintV7Error("CHEM_V7_BADGE_COUNT_EXCESSIVE")
    if any(b not in allowed for b in badges):
        raise BlueprintV7Error("CHEM_V7_BADGE_UNKNOWN")
    if payload.get("student_knowledge_percent_visible") is not False:
        raise BlueprintV7Error("CHEM_V7_KNOWLEDGE_PERCENT_BADGE_FORBIDDEN")
    mode = payload["product_mode"]
    if mode in {"CORE1", "CORE1A", "CORE1B"} and "TASK_DEMAND" in badges:
        raise BlueprintV7Error("CHEM_V7_CORE1_TASK_DEMAND_BADGE_FORBIDDEN")
    if mode in {"CORE2", "CORE2A", "CORE2B"} and "INTRINSIC_DIFFICULTY" in badges:
        raise BlueprintV7Error("CHEM_V7_CORE2_INTRINSIC_DIFFICULTY_BADGE_FORBIDDEN")
    if mode not in {"CORE2A", "CORE2B"} and "SUPPORT" in badges:
        raise BlueprintV7Error("CHEM_V7_SUPPORT_BADGE_SCOPE_INVALID")
    return {"status": "PASS", "badge_count": len(badges)}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--policy", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--ccbom")
    g.add_argument("--similarity")
    g.add_argument("--difficulty")
    g.add_argument("--purpose")
    g.add_argument("--learner-fit")
    g.add_argument("--question-custody")
    g.add_argument("--badges")
    args = p.parse_args()
    policy = load(args.policy)
    try:
        if args.ccbom:
            result = validate_ccbom(load(args.ccbom), policy)
        elif args.similarity:
            result = validate_similarity(load(args.similarity), policy)
        elif args.difficulty:
            result = validate_difficulty(load(args.difficulty), policy)
        elif args.purpose:
            result = validate_purpose(load(args.purpose), policy)
        elif args.learner_fit:
            result = validate_learner_fit(load(args.learner_fit), policy)
        elif args.question_custody:
            result = validate_question_custody(load(args.question_custody), policy)
        else:
            result = validate_badges(load(args.badges), policy)
    except BlueprintV7Error as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
