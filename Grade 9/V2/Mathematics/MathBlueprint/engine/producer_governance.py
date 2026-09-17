#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from typing import Iterable

from emit_stage_governance import (
    artifact,
    bind_refs,
    build_receipt,
    coverage_claim,
    digest,
    registry_alias_map,
)

DEMAND_LEVELS = [
    "M0_DIRECT", "M1_CONTROLLED_VARIATION", "M2_REPRESENTATION_TRANSFER",
    "M3_INVERSE_TARGET", "M4_HIDDEN_STRUCTURE", "M5_METHOD_DISCRIMINATION",
    "M6_FAMILY_DISCRIMINATION", "M7_MULTI_STEP_SYNTHESIS", "M8_MIXED_COMPETITIVE",
]


def _support_mode(profile: str) -> str:
    return {
        "FOUNDATION_GUIDED": "FOUNDATION_HIGH_SUPPORT",
        "STANDARD_GUIDED": "GUIDED",
        "REDUCED_SUPPORT": "STANDARD",
        "ADVANCED_APPLIED": "CHALLENGE_MINIMAL",
    }[profile]


def _calibration_basis(cal: dict) -> dict:
    if cal["learner_knowledge_percent"] is not None:
        return {
            "type": "KNOWLEDGE_PERCENT",
            "learner_knowledge_percent": cal["learner_knowledge_percent"],
            "knowledge_source_ref": cal["knowledge_percent_source_ref"],
            "calibration_policy_ref": cal["knowledge_calibration_policy_ref"],
            "capability_knowledge": list(cal["capability_knowledge"]),
        }
    waiver = cal["owner_waiver"]
    return {"type": "OWNER_OVERRIDE", "owner_ref": waiver["owner_ref"], "reason": waiver["reason"]}


def _canonical_capability_refs(caps: Iterable[str], aliases: dict[str, set[str]], registry: dict | None) -> list[str]:
    """Bind upstream capability IDs only to canonical CAPABILITY assets.

    A single upstream capability may legitimately decompose into several registry assets
    (for example CONCEPT + CAPABILITY). Learner-fit contracts must never inherit the
    non-capability aliases merely because they share the same upstream source ref.
    """
    caps = [str(x) for x in caps if str(x).strip()]
    if not registry:
        return list(dict.fromkeys(caps))
    assets = {row["asset_id"]: row for row in registry.get("assets", [])}
    out = []
    for cap in caps:
        hits = sorted(aid for aid in aliases.get(cap, set()) if assets.get(aid, {}).get("asset_type") == "CAPABILITY")
        if len(hits) != 1:
            raise ValueError(f"PRODUCER_GOVERNANCE_CAPABILITY_BINDING_INVALID:{cap}:{','.join(hits)}")
        out.append(hits[0])
    return list(dict.fromkeys(out))


def _difficulty_row(spec_row: dict) -> dict:
    badge = spec_row["difficulty_badge"]
    authority = {
        "OWNER": "OWNER",
        "SOURCE_METADATA": "SOURCE_METADATA",
        "CORE1_SEMANTIC_COMPLEXITY": "DERIVED",
    }[spec_row["difficulty_badge_basis"]]
    evidence = list(spec_row["difficulty_validation_refs"])
    if spec_row.get("pedagogy_research_brief_ref"):
        evidence.append(spec_row["pedagogy_research_brief_ref"])
    evidence.extend(spec_row.get("pedagogy_web_research_refs", []))
    return {
        "subtopic_ref": spec_row["subtopic_id"],
        "declared_badge": badge,
        "badge_authority": authority,
        "derived_dimensions": dict(spec_row["difficulty_dimensions"]),
        "operational_badge": badge,
        "page_ceiling": {"EASY": 10, "MEDIUM": 20, "HARD": 30}[badge],
        "research_level": {"EASY": "NONE", "MEDIUM": "TARGETED", "HARD": "DEEP"}[badge],
        "owner_override_ref": next((x for x in spec_row["difficulty_validation_refs"] if x.startswith("OWNER:")), None),
        "evidence_refs": sorted(set(evidence)),
    }


def _match_difficulty(bucket_plan: dict, generation_spec: dict | None) -> list[dict]:
    if not generation_spec:
        return []
    by_id = {row["bucket_id"]: row for row in generation_spec["core1_buckets"]}
    by_title = {row["subtopic_title"].strip().lower(): row for row in generation_spec["core1_buckets"]}
    out = []
    for bucket in bucket_plan["buckets"]:
        row = by_id.get(bucket["bucket_id"]) or by_title.get(bucket["title"].strip().lower())
        if row:
            out.append(_difficulty_row(row))
    return out


def core1a_receipt(bucket_plan: dict, book: dict, *, registry: dict | None, generation_spec: dict | None) -> dict:
    aliases, _ = registry_alias_map(registry)
    claims: list[dict] = []
    arts: list[dict] = []
    for bucket in book["buckets"]:
        bid = bucket["bucket_id"]
        caps = bucket["member_capability_refs"]
        for cap in caps:
            claims.append(coverage_claim(cap, "CAPABILITY", "REALIZED", [bid], aliases))
        for atom in bucket.get("learning_atoms", []):
            claims.append(coverage_claim(
                atom["atom_id"], "LEARNING_ATOM", "REALIZED", [bid, atom["capability_ref"]], aliases,
                extra_binding_refs=[atom["source_ref"], atom["capability_ref"]],
            ))
        for unit in bucket["capability_units"]:
            cap = unit["capability_ref"]
            ref = unit["lesson_id"]
            claims.append(coverage_claim(cap, "CAPABILITY", "REALIZED", [ref], aliases))
            family = unit.get("family_ref")
            if family:
                claims.append(coverage_claim(family, "PROBLEM_FAMILY", "REFERENCED", [ref], aliases))
            canonical = bind_refs([cap, family] if family else [cap], aliases)
            arts.append(artifact(
                ref, "TTU",
                [unit.get("opening"), unit.get("concept_explanation"), unit.get("what_to_notice"), unit.get("why_it_works"), unit.get("common_mistake"), unit.get("repair"), unit.get("worked_examples"), unit.get("practice"), unit.get("verification")],
                ["EXPLAIN", "INTERPRET", "WORKED_EXAMPLE", "VERIFY"],
                capability_refs=[cap], canonical_asset_refs=canonical,
                structural_signature=["CORE1A", unit.get("treatment", ""), family or "NO_FAMILY"],
                lineage_keys=[cap, family or cap],
            ))
            for i, ex in enumerate(unit.get("worked_examples", []), 1):
                arts.append(artifact(
                    f"{ref}:EX:{i}", "EXAMPLE", ex,
                    ["MODEL", "EXPLAIN", "VERIFY"], capability_refs=[cap], canonical_asset_refs=canonical,
                    structural_signature=["WORKED_EXAMPLE", family or cap, f"STEPS:{len(ex.get('steps', []))}"],
                    lineage_keys=[family or cap],
                ))
        arts.append(artifact(
            f"{bid}:BUCKET", "NARRATIVE", [bucket["title"], bucket["bucket_invariant"], bucket.get("verification")],
            ["READ", "INTERPRET", "CONNECT"], capability_refs=caps,
            canonical_asset_refs=bind_refs(caps, aliases), structural_signature=["BUCKET", str(len(caps))],
            lineage_keys=caps,
        ))

    difficulty = _match_difficulty(bucket_plan, generation_spec)
    complete = bool(registry and generation_spec and len(difficulty) == len(bucket_plan["buckets"]))
    return build_receipt(
        stage="CORE1A", producer_ref=book["core1a_book_id"],
        source_refs=[bucket_plan["bucket_plan_id"], bucket_plan["source_core1_study_plan_ref"], bucket_plan["source_study_model_ref"]],
        registry=registry,
        purpose_evidence={
            "purpose_contract": "BUILD_UNDERSTANDING",
            "learner_actions": ["READ", "INSPECT", "INTERPRET", "COMPARE", "VERIFY"],
            "canonical_reveal_after_attempt": False,
            "evidence_refs": [book["core1a_book_id"], bucket_plan["bucket_plan_id"]],
        },
        difficulty_evidence=difficulty, coverage_claims=claims, artifacts=arts,
        governance_complete=complete,
    )


def core1b_receipt(source: dict, plan: dict, *, registry: dict | None) -> dict:
    aliases, _ = registry_alias_map(registry)
    claims: list[dict] = []
    arts: list[dict] = []
    for cap in plan["capability_refs"]:
        claims.append(coverage_claim(cap, "CAPABILITY", "RECONSTRUCTED", [plan["plan_id"]], aliases))
    for block in plan["blocks"]:
        caps = block.get("capability_refs", [])
        for cap in caps:
            claims.append(coverage_claim(cap, "CAPABILITY", "RECONSTRUCTED", [block["block_id"]], aliases))
        arts.append(artifact(
            block["block_id"], "TTU", [block.get("title"), block.get("learner_text"), block.get("math_lines"), block.get("rows")],
            ["ATTEMPT", block["kind"], "RECONSTRUCT", "VERIFY" if block["kind"] == "ANSWER_CHECK" else "SELF_GUIDED_HELP"],
            capability_refs=caps, canonical_asset_refs=bind_refs(caps, aliases),
            structural_signature=[block["kind"], f"CAPS:{len(caps)}"], lineage_keys=caps,
        ))
    difficulty = [dict(source["difficulty_governance"])] if source.get("difficulty_governance") else []
    complete = bool(registry and difficulty)
    return build_receipt(
        stage="CORE1B", producer_ref=plan["plan_id"], source_refs=[plan["source_core1a_authority_ref"]], registry=registry,
        purpose_evidence={
            "purpose_contract": "RECONSTRUCT_CONCEPT",
            "learner_actions": ["PREDICT", "GENERATE", "COMPARE", "DIAGNOSE", "DERIVE", "VERIFY"],
            "canonical_reveal_after_attempt": True,
            "evidence_refs": [plan["plan_id"], plan["source_core1a_authority_ref"]],
        },
        difficulty_evidence=difficulty, coverage_claims=claims, artifacts=arts,
        governance_complete=complete,
    )


def _source_custody(q: dict) -> dict:
    prov = q["provenance"]
    qid = q["question_id"]
    source = prov.get("verified_official_source_ref") or (prov.get("citations") or [{}])[0].get("locator") or qid
    return {
        "question_id": qid,
        "origin": "SOURCE_CORE2",
        "source_question_no": q.get("source_question_no") or qid,
        "source_ref": str(source),
        "source_relation": "EXACT_SOURCE",
        "parent_question_refs": [],
        "exact_stem_hash": hashlib.sha256(q["prompt"].encode("utf-8")).hexdigest(),
        "answer_contract_ref": q.get("answer_contract_ref") or ("ANS-" + qid + "-" + digest(q["answer_contract"])[:12]),
        "answer_status": "VERIFIED",
        "learner_source_label": (prov.get("citations") or [{"label": "Core (2) source"}])[0].get("label", "Core (2) source"),
        "official_past_question_claim": bool(prov.get("official_past_question_claim")),
        "verified_official_source_ref": prov.get("verified_official_source_ref"),
    }


def _generated_custody(q: dict) -> dict:
    qid = q["question_id"]
    prov = q["provenance"]
    parents = q.get("parent_question_refs") or q.get("novelty_check", {}).get("compared_to_refs", [])
    return {
        "question_id": qid,
        "origin": "GENERATED_ORIGINAL",
        "source_question_no": None,
        "source_ref": "GENERATED:" + qid,
        "source_relation": q.get("source_relation", "FRESH_ORIGINAL"),
        "parent_question_refs": list(parents),
        "exact_stem_hash": None,
        "answer_contract_ref": q.get("answer_contract_ref") or ("ANS-" + qid + "-" + digest(q["answer_contract"])[:12]),
        "answer_status": "VERIFIED",
        "learner_source_label": q.get("learner_source_label") or "Generated original practice",
        "official_past_question_claim": bool(prov.get("official_past_question_claim")),
        "verified_official_source_ref": prov.get("verified_official_source_ref"),
    }


def core2a_receipt(blueprint: dict, generation_spec: dict, *, registry: dict | None, all_source_pages: list[dict]) -> dict:
    aliases, _ = registry_alias_map(registry)
    cal = generation_spec["core2_calibration"]
    basis = _calibration_basis(cal)
    support = _support_mode(cal["resolved_core2a_support_profile"])
    claims: list[dict] = []
    fits: list[dict] = []
    custody: list[dict] = []
    arts: list[dict] = []
    source_pages = {row["question_ref"]: row for row in all_source_pages}
    seen_source = set()
    for q in blueprint["question_specs"]:
        qid = q["question_id"]
        is_source = q["question_class"] == "SOURCE_CORE2"
        caps = list(q.get("required_capability_refs", []))
        demand = q["demand_level"]
        canonical = bind_refs([qid, *caps], aliases)
        claims.append(coverage_claim(qid, "SOURCE_QUESTION" if is_source else "EXAMPLE", "USED", [qid], aliases))
        for cap in caps:
            claims.append(coverage_claim(cap, "CAPABILITY", "USED", [qid], aliases))
        arts.append(artifact(
            qid, "QUESTION", [q.get("prompt"), q.get("learner_support")],
            ["STUDY_SOLUTION", "ANALYZE_FIRST_MOVE", "VERIFY"], capability_refs=caps,
            canonical_asset_refs=canonical, structural_signature=[q.get("slot") or "SOURCE", demand],
            lineage_keys=q.get("parent_question_refs") or [qid],
        ))
        if caps:
            fit_caps = _canonical_capability_refs(caps, aliases, registry)
            fits.append({
                "item_ref": qid, "calibration_basis": basis, "required_capability_refs": fit_caps,
                "support_mode": support, "maximum_allowed_demand": cal["resolved_core2a_max_demand_level"],
                "actual_demand": demand, "taught_scope_verified": True,
            })
        if is_source:
            seen_source.add(q.get("source_question_no") or qid)
            custody.append(_source_custody(q))
        else:
            custody.append(_generated_custody(q))

    for qid, page in source_pages.items():
        if qid in seen_source:
            continue
        claims.append(coverage_claim(qid, "SOURCE_QUESTION", "REFERENCED", ["CUSTODY:" + qid], aliases))
        answer_ref = page.get("answer_contract_ref") or "ANS-CUSTODY-" + qid
        custody.append({
            "question_id": qid, "origin": "SOURCE_CORE2", "source_question_no": qid,
            "source_ref": str(page.get("source_ref") or qid), "source_relation": "EXACT_SOURCE",
            "parent_question_refs": [],
            "exact_stem_hash": hashlib.sha256(str(page.get("source_stem", "")).encode("utf-8")).hexdigest(),
            "answer_contract_ref": answer_ref, "answer_status": "VERIFIED",
            "learner_source_label": "Core (2) " + qid, "official_past_question_claim": False,
            "verified_official_source_ref": page.get("source_ref"),
        })

    complete = bool(registry) and (basis["type"] == "OWNER_OVERRIDE" or bool(basis["capability_knowledge"]))
    return build_receipt(
        stage="CORE2A", producer_ref=blueprint["blueprint_id"], source_refs=[blueprint["source_bundle_ref"]], registry=registry,
        purpose_evidence={
            "purpose_contract": "SOLUTION_APPRENTICESHIP",
            "learner_actions": ["STUDY_SOLUTION", "ANALYZE_FIRST_MOVE", "INTERPRET", "VERIFY"],
            "canonical_reveal_after_attempt": False,
            "evidence_refs": [blueprint["blueprint_id"], blueprint["source_bundle_ref"]],
        },
        learner_fit_evidence=fits, question_custody=custody, coverage_claims=claims, artifacts=arts,
        governance_complete=complete,
    )


def core2b_receipt(source: dict, plan: dict, *, registry: dict | None) -> dict:
    aliases, _ = registry_alias_map(registry)
    cal = source.get("generation_calibration") or {}
    basis = cal.get("calibration_basis")
    support = cal.get("support_mode")
    claims: list[dict] = []
    fits: list[dict] = []
    custody: list[dict] = []
    arts: list[dict] = []
    for item in plan["items"]:
        iid = item["item_id"]
        caps = list(item.get("capability_refs", []))
        origin = item.get("origin", "GENERATED_ORIGINAL")
        claims.append(coverage_claim(iid, "SOURCE_QUESTION" if origin == "SOURCE_CORE2" else "EXAMPLE", "USED", [iid], aliases))
        for cap in caps:
            claims.append(coverage_claim(cap, "CAPABILITY", "USED", [iid], aliases))
        arts.append(artifact(
            iid, "QUESTION", [item.get("stem"), item.get("support"), item.get("answer_check"), item.get("self_guided_frame")],
            ["ATTEMPT", "MODEL_SELECT", "FIRST_MOVE", "SOLVE", "VERIFY", "TRANSFER"], capability_refs=caps,
            canonical_asset_refs=bind_refs([iid, *caps], aliases), structural_signature=[item["demand_level"], "CORE2B"],
            lineage_keys=item.get("parent_question_refs") or [item.get("source_question_no") or iid],
        ))
        if basis and support:
            fits.append({
                "item_ref": iid, "calibration_basis": basis,
                "required_capability_refs": _canonical_capability_refs(caps, aliases, registry),
                "support_mode": support, "maximum_allowed_demand": plan["compile_ceiling"],
                "actual_demand": item["demand_level"], "taught_scope_verified": True,
            })
        custody.append({
            "question_id": iid, "origin": origin,
            "source_question_no": item.get("source_question_no") if origin == "SOURCE_CORE2" else None,
            "source_ref": item.get("source_ref") or ("GENERATED:" + iid),
            "source_relation": item.get("source_relation", "EXACT_SOURCE" if origin == "SOURCE_CORE2" else "FRESH_ORIGINAL"),
            "parent_question_refs": item.get("parent_question_refs", []),
            "exact_stem_hash": hashlib.sha256(item["stem"].encode("utf-8")).hexdigest() if origin == "SOURCE_CORE2" else None,
            "answer_contract_ref": item["answer_contract_ref"], "answer_status": "VERIFIED",
            "learner_source_label": item["learner_source_label"],
            "official_past_question_claim": bool(item.get("official_past_question_claim", False)),
            "verified_official_source_ref": item.get("verified_official_source_ref"),
        })
    complete = bool(registry and basis and support)
    return build_receipt(
        stage="CORE2B", producer_ref=plan["plan_id"], source_refs=[plan["source_core2a_authority_ref"]], registry=registry,
        purpose_evidence={
            "purpose_contract": "TRANSFER_TUTOR",
            "learner_actions": ["ATTEMPT", "MODEL_SELECT", "REPRESENT", "FIRST_MOVE", "SOLVE", "VERIFY", "TRANSFER"],
            "canonical_reveal_after_attempt": True,
            "evidence_refs": [plan["plan_id"], plan["source_core2a_authority_ref"]],
        },
        learner_fit_evidence=fits, question_custody=custody, coverage_claims=claims, artifacts=arts,
        governance_complete=complete,
    )
