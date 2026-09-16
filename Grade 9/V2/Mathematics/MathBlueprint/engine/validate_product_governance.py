#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
COVERAGE_SCHEMA = ROOT / "contracts" / "math-core-coverage-ledger.schema.json"
SIMILARITY_SCHEMA = ROOT / "contracts" / "math-cross-core-similarity-audit.schema.json"
GOVERNANCE_SCHEMA = ROOT / "contracts" / "math-product-governance-audit.schema.json"
SIMILARITY_POLICY = ROOT / "policies" / "math-cross-core-similarity-policy.json"

STAGES = ("CORE1A", "CORE1B", "CORE2A", "CORE2B")
DEMAND_LEVELS = (
    "M0_DIRECT", "M1_CONTROLLED_VARIATION", "M2_REPRESENTATION_TRANSFER",
    "M3_INVERSE_TARGET", "M4_HIDDEN_STRUCTURE", "M5_METHOD_DISCRIMINATION",
    "M6_FAMILY_DISCRIMINATION", "M7_MULTI_STEP_SYNTHESIS", "M8_MIXED_COMPETITIVE",
)
SEMANTIC_TYPES = {
    "CONCEPT", "MODEL", "EQUATION", "DERIVATION", "CAPABILITY",
    "LEARNING_ATOM", "REPRESENTATION", "MISCONCEPTION",
}
ACTIVE_DISPOSITIONS = {"REALIZED", "RECONSTRUCTED", "REFERENCED", "USED"}


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _asset_map(registry: dict) -> dict[str, dict]:
    return {row["asset_id"]: row for row in registry["assets"]}


def _demand_index(level: str) -> int:
    if level not in DEMAND_LEVELS:
        fail("PRODUCT_GOVERNANCE_DEMAND_LEVEL_UNKNOWN", level)
    return DEMAND_LEVELS.index(level)


def validate_coverage(ledger: dict, registry: dict) -> dict:
    jsonschema.validate(ledger, load(COVERAGE_SCHEMA))
    if ledger["registry_ref"] != registry["registry_id"]:
        fail("COVERAGE_REGISTRY_REF_MISMATCH")

    assets = _asset_map(registry)
    seen: dict[str, str] = {}
    for subtopic in ledger["subtopics"]:
        sid = subtopic["subtopic_id"]
        for row in subtopic["asset_coverage"]:
            ref = row["asset_ref"]
            if ref in seen:
                fail("COVERAGE_ASSET_DUPLICATE", ref)
            if ref not in assets:
                fail("COVERAGE_ASSET_UNKNOWN", ref)
            source = assets[ref]
            if source["subtopic_id"] != sid:
                fail("COVERAGE_SUBTOPIC_MISMATCH", f"{ref}:{sid}!={source['subtopic_id']}")
            if row["asset_type"] != source["asset_type"]:
                fail("COVERAGE_ASSET_TYPE_MISMATCH", ref)
            seen[ref] = sid

            for stage in STAGES:
                state = row[stage]
                obligation = state["obligation"]
                disposition = state["disposition"]
                refs = state["realization_refs"]
                override = state["owner_override_ref"]
                reason = state["omission_reason"]

                if obligation == "PROHIBITED" and disposition != "PROHIBITED":
                    fail("COVERAGE_PROHIBITED_REALIZED", f"{ref}:{stage}")
                if obligation == "NOT_APPLICABLE" and disposition != "NOT_APPLICABLE":
                    fail("COVERAGE_NOT_APPLICABLE_DRIFT", f"{ref}:{stage}")
                if disposition in ACTIVE_DISPOSITIONS and not refs:
                    fail("COVERAGE_REALIZATION_REF_MISSING", f"{ref}:{stage}")
                if disposition == "INTENTIONALLY_OMITTED" and (not override or not reason):
                    fail("COVERAGE_OMISSION_UNGOVERNED", f"{ref}:{stage}")
                if obligation == "REQUIRED" and disposition in {"NOT_APPLICABLE", "PROHIBITED"}:
                    fail("COVERAGE_REQUIRED_ASSET_SKIPPED", f"{ref}:{stage}")
                if obligation == "REQUIRED" and disposition == "INTENTIONALLY_OMITTED" and not override:
                    fail("COVERAGE_REQUIRED_OMISSION_WITHOUT_OWNER", f"{ref}:{stage}")

            if row["asset_type"] in SEMANTIC_TYPES:
                for stage in ("CORE1A", "CORE1B"):
                    if row[stage]["obligation"] in {"PROHIBITED", "NOT_APPLICABLE"}:
                        fail("COVERAGE_SEMANTIC_TRACK_GAP", f"{ref}:{stage}")
            if row["asset_type"] == "SOURCE_QUESTION":
                for stage in ("CORE2A", "CORE2B"):
                    if row[stage]["obligation"] == "PROHIBITED":
                        fail("COVERAGE_SOURCE_QUESTION_ILLEGALLY_PROHIBITED", f"{ref}:{stage}")

    missing = sorted(set(assets) - set(seen))
    extra = sorted(set(seen) - set(assets))
    if missing:
        fail("COVERAGE_REGISTRY_ASSET_UNDISPOSED", ",".join(missing))
    if extra:
        fail("COVERAGE_LEDGER_ASSET_NOT_IN_REGISTRY", ",".join(extra))
    return {"asset_count": len(seen), "status": "PASS"}


def _similarity_class(row: dict, policy: dict) -> str:
    c = row["content_similarity"]
    p = row["pedagogical_similarity"]
    s = row["structural_similarity"]
    kind = row["artifact_kind"]
    rel = row["declared_relation"]
    ct = policy["content_thresholds"]
    pt = policy["pedagogy_thresholds"]
    st = policy["structural_thresholds"]
    exempt = set(policy["exact_repeat_exempt_kinds"])
    exact_rel = set(policy["exact_repeat_allowed_relations"])

    if rel == "FADING_ANCHOR":
        if s is not None and s < st["same_or_near_copy"]:
            fail("SIMILARITY_FADING_ANCHOR_NOT_SAME_PROBLEM", row["comparison_id"])
        return "LEGITIMATE_TRANSFORMATION"
    if rel == "STRUCTURAL_SIBLING":
        if s is None or not (st["structural_sibling_min"] <= s < st["same_or_near_copy"]):
            fail("SIMILARITY_STRUCTURAL_SIBLING_RANGE_INVALID", row["comparison_id"])
        if not row["capability_overlap"]:
            fail("SIMILARITY_TRANSFER_CAPABILITY_DRIFT", row["comparison_id"])
    if rel == "FAR_TRANSFER_SIBLING":
        if s is None or not (st["far_transfer_min"] <= s < st["structural_sibling_min"]):
            fail("SIMILARITY_FAR_TRANSFER_RANGE_INVALID", row["comparison_id"])
        if not row["capability_overlap"]:
            fail("SIMILARITY_TRANSFER_CAPABILITY_DRIFT", row["comparison_id"])
    if s is not None and s < st["far_transfer_min"] and rel in {"STRUCTURAL_SIBLING", "FAR_TRANSFER_SIBLING"}:
        return "FAMILY_DRIFT_REVIEW"

    if kind in exempt and c >= ct["hard_duplicate"]:
        if rel not in exact_rel:
            fail("SIMILARITY_CANONICAL_REPEAT_LINEAGE_MISSING", row["comparison_id"])
        return "LEGITIMATE_TRANSFORMATION"

    if c >= ct["hard_duplicate"] and p >= pt["same_realization"]:
        return "HARD_DUPLICATE"
    if c >= ct["near_duplicate"] and p >= pt["strong_overlap"]:
        return "NEAR_DUPLICATE" if rel == "NONE" else "STRONG_OVERLAP"
    if c >= ct["near_duplicate"] and p < pt["strong_overlap"]:
        return "LEGITIMATE_TRANSFORMATION" if rel != "NONE" else "STRONG_OVERLAP"
    if rel in {"SEMANTIC_REUSE", "CANONICAL_REPEAT", "STRUCTURAL_SIBLING", "FAR_TRANSFER_SIBLING"}:
        return "LEGITIMATE_TRANSFORMATION"
    return "DISTINCT"


def validate_similarity(audit: dict, policy: dict | None = None) -> dict:
    jsonschema.validate(audit, load(SIMILARITY_SCHEMA))
    policy = policy or load(SIMILARITY_POLICY)
    hard = []
    near = []
    strong = []
    for row in audit["comparisons"]:
        computed = _similarity_class(row, policy)
        if computed != row["classification"]:
            fail("SIMILARITY_CLASSIFICATION_MISMATCH", f"{row['comparison_id']}:{computed}!={row['classification']}")
        if computed == "HARD_DUPLICATE":
            hard.append(row["comparison_id"])
        if computed == "NEAR_DUPLICATE":
            near.append(row["comparison_id"])
        if computed == "STRONG_OVERLAP":
            strong.append(row["comparison_id"])
    if hard:
        fail("SIMILARITY_HARD_DUPLICATE", ",".join(hard))
    if near:
        fail("SIMILARITY_NEAR_DUPLICATE_UNDECLARED", ",".join(near))
    if strong:
        fail("SIMILARITY_STRONG_PEDAGOGICAL_OVERLAP", ",".join(strong))
    return {"comparison_count": len(audit["comparisons"]), "status": "PASS"}


def _derived_difficulty(dimensions: dict) -> tuple[float, str]:
    score = round(sum(dimensions.values()) / (4 * len(dimensions)) * 100, 2)
    badge = "EASY" if score <= 32 else "MEDIUM" if score <= 65 else "HARD"
    return score, badge


def _validate_difficulty(rows: list[dict]) -> None:
    consequence = {
        "EASY": (10, "NONE"),
        "MEDIUM": (20, "TARGETED"),
        "HARD": (30, "DEEP"),
    }
    seen = set()
    for row in rows:
        sid = row["subtopic_id"]
        if sid in seen:
            fail("DIFFICULTY_SUBTOPIC_DUPLICATE", sid)
        seen.add(sid)
        score, badge = _derived_difficulty(row["derived_dimensions"])
        if abs(score - row["derived_score"]) > 0.02:
            fail("DIFFICULTY_SCORE_MISMATCH", sid)
        if badge != row["derived_badge"]:
            fail("DIFFICULTY_DERIVED_BADGE_MISMATCH", sid)
        if row["badge_authority"] in {"DERIVED", "VALIDATED_DERIVED"}:
            if row["operational_badge"] != badge or row["status"] != "ALIGNED":
                fail("DIFFICULTY_DERIVED_AUTHORITY_DRIFT", sid)
        elif row["operational_badge"] != row["declared_badge"]:
            fail("DIFFICULTY_DECLARED_AUTHORITY_NOT_HONOURED", sid)
        if row["declared_badge"] != badge:
            expected_status = "OWNER_OVERRIDDEN_MISMATCH" if row["badge_authority"] == "OWNER" else "SOURCE_OVERRIDDEN_MISMATCH"
            if row["status"] != expected_status:
                fail("DIFFICULTY_OVERRIDE_STATUS_MISSING", sid)
        elif row["status"] != "ALIGNED":
            fail("DIFFICULTY_FALSE_MISMATCH_STATUS", sid)
        expected_pages, expected_research = consequence[row["operational_badge"]]
        if row["page_ceiling"] != expected_pages or row["research_level"] != expected_research:
            fail("DIFFICULTY_BADGE_CONSEQUENCE_DRIFT", sid)


def _validate_purpose(rows: list[dict]) -> None:
    by = {row["stage"]: row for row in rows}
    if set(by) != set(STAGES) or len(rows) != 4:
        fail("PURPOSE_STAGE_COVERAGE_INVALID")
    expected = {
        "CORE1A": "BUILD_UNDERSTANDING",
        "CORE1B": "RECONSTRUCT_CONCEPT",
        "CORE2A": "SOLUTION_APPRENTICESHIP",
        "CORE2B": "TRANSFER_TUTOR",
    }
    for stage, contract in expected.items():
        if by[stage]["purpose_contract"] != contract:
            fail("PURPOSE_CONTRACT_MISMATCH", stage)
    if not ({"READ", "INTERPRET"} & set(by["CORE1A"]["learner_actions"])):
        fail("PURPOSE_CORE1A_DECLARATIVE_ACTION_MISSING")
    reconstructive = {"PREDICT", "GENERATE", "SELECT", "DISCRIMINATE", "DIAGNOSE", "DERIVE", "CONNECT", "VERIFY", "TRANSFER"}
    if len(reconstructive & set(by["CORE1B"]["learner_actions"])) < 2 or not by["CORE1B"]["canonical_reveal_after_attempt"]:
        fail("PURPOSE_CORE1B_RECONSTRUCTION_WEAK")
    if not {"STUDY_SOLUTION", "ANALYZE_FIRST_MOVE", "VERIFY"}.issubset(set(by["CORE2A"]["learner_actions"])):
        fail("PURPOSE_CORE2A_SOLUTION_APPRENTICESHIP_WEAK")
    if not {"ATTEMPT", "FIRST_MOVE", "VERIFY"}.issubset(set(by["CORE2B"]["learner_actions"])) or not ({"MODEL_SELECT", "SELECT"} & set(by["CORE2B"]["learner_actions"])) or not by["CORE2B"]["canonical_reveal_after_attempt"]:
        fail("PURPOSE_CORE2B_TRANSFER_TUTOR_WEAK")


def _validate_learner_fit(rows: list[dict], assets: dict[str, dict]) -> None:
    for row in rows:
        if _demand_index(row["actual_demand"]) > _demand_index(row["maximum_allowed_demand"]):
            fail("LEARNER_FIT_DEMAND_CEILING_EXCEEDED", row["item_ref"])
        for ref in row["required_capability_refs"]:
            if ref not in assets or assets[ref]["asset_type"] != "CAPABILITY":
                fail("LEARNER_FIT_CAPABILITY_UNKNOWN", f"{row['item_ref']}:{ref}")
        basis = row["calibration_basis"]
        if basis["type"] == "KNOWLEDGE_PERCENT":
            cap = {x["capability_ref"]: x["percent"] for x in basis["capability_knowledge"]}
            missing = sorted(set(row["required_capability_refs"]) - set(cap))
            if missing:
                fail("LEARNER_FIT_CAPABILITY_KNOWLEDGE_MISSING", f"{row['item_ref']}:{','.join(missing)}")


def _validate_question_custody(rows: list[dict], registry: dict) -> None:
    source_assets = [x for x in registry["assets"] if x["asset_type"] == "SOURCE_QUESTION"]
    required_source_refs = {x["payload"]["question_ref"] for x in source_assets}
    seen_source = set()
    seen_ids = set()
    for row in rows:
        qid = row["question_id"]
        if qid in seen_ids:
            fail("QUESTION_CUSTODY_DUPLICATE_ID", qid)
        seen_ids.add(qid)
        if not row["answer_contract_ref"] or row["answer_status"] != "VERIFIED":
            fail("QUESTION_CUSTODY_ANSWER_MISSING", qid)
        if not row["learner_source_label"].strip():
            fail("QUESTION_CUSTODY_LEARNER_SOURCE_LABEL_MISSING", qid)
        if row["official_past_question_claim"] and not row["verified_official_source_ref"]:
            fail("QUESTION_CUSTODY_UNVERIFIED_OFFICIAL_CLAIM", qid)
        if row["origin"] == "SOURCE_CORE2":
            if not row["source_question_no"] or row["source_relation"] != "EXACT_SOURCE" or not row["exact_stem_hash"]:
                fail("QUESTION_CUSTODY_SOURCE_IDENTITY_BROKEN", qid)
            if row["parent_question_refs"]:
                fail("QUESTION_CUSTODY_SOURCE_HAS_PARENT_VARIANT", qid)
            seen_source.add(row["source_question_no"])
        else:
            if row["source_question_no"] is not None or row["source_relation"] == "EXACT_SOURCE":
                fail("QUESTION_CUSTODY_GENERATED_MASQUERADES_AS_SOURCE", qid)
            if row["source_relation"] in {"FADING_ANCHOR", "STRUCTURAL_SIBLING", "FAR_TRANSFER_SIBLING"} and not row["parent_question_refs"]:
                fail("QUESTION_CUSTODY_GENERATED_LINEAGE_MISSING", qid)
    missing = sorted(required_source_refs - seen_source)
    if missing:
        fail("QUESTION_CUSTODY_SOURCE_QUESTION_MISSING", ",".join(missing))


def _validate_badges(rows: list[dict], assets: dict[str, dict], difficulty_rows: list[dict]) -> None:
    difficulty = {x["subtopic_id"]: x for x in difficulty_rows}
    expected_types = {
        "concept_refs": {"CONCEPT", "MODEL"},
        "equation_refs": {"EQUATION"},
        "representation_refs": {"REPRESENTATION"},
        "misconception_refs": {"MISCONCEPTION"},
        "problem_family_refs": {"PROBLEM_FAMILY"},
    }
    seen = set()
    for row in rows:
        sid = row["subtopic_id"]
        if sid in seen:
            fail("BADGE_SUBTOPIC_DUPLICATE", sid)
        seen.add(sid)
        if sid not in difficulty:
            fail("BADGE_DIFFICULTY_AUDIT_MISSING", sid)
        if row["difficulty"] != difficulty[sid]["operational_badge"]:
            fail("BADGE_DIFFICULTY_MISMATCH", sid)
        if row["research_badge"] != difficulty[sid]["research_level"]:
            fail("BADGE_RESEARCH_MISMATCH", sid)
        for field, allowed in expected_types.items():
            for ref in row[field]:
                if ref not in assets or assets[ref]["asset_type"] not in allowed:
                    fail("BADGE_REF_TYPE_MISMATCH", f"{sid}:{field}:{ref}")
        for field in ("linkage_refs", "prerequisite_refs"):
            for ref in row[field]:
                if ref not in assets:
                    fail("BADGE_REF_UNKNOWN", f"{sid}:{field}:{ref}")


def validate_governance(audit: dict, registry: dict) -> dict:
    jsonschema.validate(audit, load(GOVERNANCE_SCHEMA))
    if audit["registry_ref"] != registry["registry_id"]:
        fail("PRODUCT_GOVERNANCE_REGISTRY_REF_MISMATCH")
    assets = _asset_map(registry)
    _validate_difficulty(audit["difficulty_audits"])
    _validate_purpose(audit["purpose_audits"])
    _validate_learner_fit(audit["learner_fit_audits"], assets)
    _validate_question_custody(audit["question_custody"], registry)
    _validate_badges(audit["badge_sets"], assets, audit["difficulty_audits"])
    return {
        "difficulty_count": len(audit["difficulty_audits"]),
        "learner_fit_count": len(audit["learner_fit_audits"]),
        "question_count": len(audit["question_custody"]),
        "status": "PASS",
    }


def validate_release(registry: dict, coverage: dict, similarity: dict, governance: dict) -> dict:
    return {
        "coverage": validate_coverage(coverage, registry),
        "similarity": validate_similarity(similarity),
        "governance": validate_governance(governance, registry),
        "status": "PASS",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--coverage", required=True)
    ap.add_argument("--similarity", required=True)
    ap.add_argument("--governance", required=True)
    args = ap.parse_args()
    result = validate_release(load(args.registry), load(args.coverage), load(args.similarity), load(args.governance))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
