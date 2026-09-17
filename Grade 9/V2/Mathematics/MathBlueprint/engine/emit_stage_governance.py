#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = ROOT / "contracts" / "math-stage-governance-receipt.schema.json"

STAGES = {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _flatten_text(value: Any) -> list[str]:
    out: list[str] = []
    if value is None:
        return out
    if isinstance(value, str):
        if value.strip():
            out.append(value)
    elif isinstance(value, (int, float, bool)):
        out.append(str(value))
    elif isinstance(value, dict):
        for key in sorted(value):
            out.extend(_flatten_text(value[key]))
    elif isinstance(value, list):
        for child in value:
            out.extend(_flatten_text(child))
    return out


def text_tokens(value: Any) -> list[str]:
    text = " ".join(_flatten_text(value)).lower()
    return sorted(set(re.findall(r"[a-z]+(?:_[a-z]+)*|\d+(?:\.\d+)?", text)))


def math_tokens(value: Any) -> list[str]:
    text = " ".join(_flatten_text(value)).replace("−", "-")
    raw = re.findall(r"[A-Za-zΑ-Ωα-ω]+|\d+(?:\.\d+)?|<=|>=|!=|==|[+\-*/=^<>()[\]{}]", text)
    keep = []
    for token in raw:
        if any(ch.isdigit() for ch in token) or token in {"+", "-", "*", "/", "=", "^", "<", ">", "<=", ">=", "!=", "(", ")", "[", "]", "{", "}"}:
            keep.append(token.lower())
    return sorted(set(keep))


def registry_alias_map(registry: dict | None) -> tuple[dict[str, set[str]], str | None]:
    if not registry:
        return {}, None
    aliases: dict[str, set[str]] = {}
    for asset in registry.get("assets", []):
        aid = asset["asset_id"]
        keys = {aid, *asset.get("core1_refs", []), *asset.get("core2_refs", [])}
        payload = asset.get("payload") or {}
        for field in ("question_ref", "answer_contract_ref", "canonical_prompt_ref", "fingerprint_ref"):
            value = payload.get(field)
            if isinstance(value, str):
                keys.add(value)
        for key in keys:
            aliases.setdefault(key, set()).add(aid)
    return aliases, registry.get("registry_id")


def bind_refs(local_refs: Iterable[str], aliases: dict[str, set[str]]) -> list[str]:
    bound: set[str] = set()
    for ref in local_refs:
        bound.update(aliases.get(str(ref), set()))
    return sorted(bound)


def artifact(
    artifact_ref: str,
    artifact_kind: str,
    content: Any,
    pedagogy_signature: Iterable[str],
    *,
    capability_refs: Iterable[str] = (),
    canonical_asset_refs: Iterable[str] = (),
    structural_signature: Iterable[str] = (),
    lineage_keys: Iterable[str] = (),
) -> dict:
    material = _flatten_text(content)
    return {
        "artifact_ref": artifact_ref,
        "artifact_kind": artifact_kind,
        "content_hash": digest(material),
        "content_tokens": text_tokens(material),
        "math_tokens": math_tokens(material),
        "pedagogy_signature": sorted(set(str(x) for x in pedagogy_signature if str(x).strip())),
        "structural_signature": sorted(set(str(x) for x in structural_signature if str(x).strip())),
        "capability_refs": sorted(set(str(x) for x in capability_refs if str(x).strip())),
        "canonical_asset_refs": sorted(set(str(x) for x in canonical_asset_refs if str(x).startswith("REG-MATH-"))),
        "lineage_keys": sorted(set(str(x) for x in lineage_keys if str(x).strip())),
    }


def coverage_claim(
    local_ref: str,
    local_type: str,
    disposition: str,
    realization_refs: Iterable[str],
    aliases: dict[str, set[str]],
    *,
    extra_binding_refs: Iterable[str] = (),
) -> dict:
    canonical_refs = bind_refs([local_ref, *extra_binding_refs], aliases)
    return {
        "local_ref": local_ref,
        "local_type": local_type,
        "canonical_asset_refs": canonical_refs,
        "disposition": disposition,
        "realization_refs": sorted(set(str(x) for x in realization_refs if str(x).strip())),
    }


def _dedupe_claims(claims: Iterable[dict]) -> list[dict]:
    merged: dict[tuple[str, str], dict] = {}
    rank = {"REFERENCED": 0, "USED": 1, "REALIZED": 2, "RECONSTRUCTED": 3}
    for row in claims:
        key = (row["local_ref"], row["local_type"])
        if key not in merged:
            merged[key] = dict(row)
            continue
        cur = merged[key]
        cur["canonical_asset_refs"] = sorted(set(cur["canonical_asset_refs"]) | set(row["canonical_asset_refs"]))
        cur["realization_refs"] = sorted(set(cur["realization_refs"]) | set(row["realization_refs"]))
        if rank[row["disposition"]] > rank[cur["disposition"]]:
            cur["disposition"] = row["disposition"]
    return [merged[k] for k in sorted(merged)]


def build_receipt(
    *,
    stage: str,
    producer_ref: str,
    source_refs: Iterable[str],
    purpose_evidence: dict,
    coverage_claims: Iterable[dict],
    artifacts: Iterable[dict],
    registry: dict | None = None,
    difficulty_evidence: Iterable[dict] = (),
    learner_fit_evidence: Iterable[dict] = (),
    question_custody: Iterable[dict] = (),
    governance_complete: bool = True,
) -> dict:
    if stage not in STAGES:
        raise ValueError("STAGE_GOVERNANCE_STAGE_INVALID:" + str(stage))
    aliases, registry_ref = registry_alias_map(registry)
    claims = _dedupe_claims(coverage_claims)
    matched = sorted({aid for row in claims for aid in row["canonical_asset_refs"]})
    release_state = "READY_FOR_CROSS_CORE_AUDIT" if registry_ref and governance_complete else "UNBOUND_PRE_RELEASE"
    payload = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "receipt_id": "",
        "stage": stage,
        "producer_ref": producer_ref,
        "source_refs": sorted(set(str(x) for x in source_refs if str(x).strip())),
        "registry_binding": {
            "status": "BOUND" if registry_ref else "UNBOUND",
            "registry_ref": registry_ref,
            "matched_asset_refs": matched,
        },
        "purpose_evidence": purpose_evidence,
        "difficulty_evidence": list(difficulty_evidence),
        "learner_fit_evidence": list(learner_fit_evidence),
        "question_custody": list(question_custody),
        "coverage_claims": claims,
        "artifacts": list(artifacts),
        "release_state": release_state,
    }
    payload["receipt_id"] = f"MATH-STAGE-GOV-{stage}-{digest(payload)[:16]}"
    schema = load(SCHEMA)
    jsonschema.validate(payload, schema)
    return payload


def core1a_receipt(bucket_plan: dict, book: dict, *, registry: dict | None = None, generation_spec: dict | None = None) -> dict:
    aliases, _ = registry_alias_map(registry)
    claims: list[dict] = []
    artifacts: list[dict] = []
    for bucket in book["buckets"]:
        bid = bucket["bucket_id"]
        for cap in bucket["member_capability_refs"]:
            claims.append(coverage_claim(cap, "CAPABILITY", "REALIZED", [bid], aliases))
        for atom in bucket.get("learning_atoms", []):
            claims.append(coverage_claim(atom["atom_id"], "LEARNING_ATOM", "REALIZED", [bid, atom["capability_ref"]], aliases, extra_binding_refs=[atom["source_ref"], atom["capability_ref"]]))
        for unit in bucket["capability_units"]:
            cap = unit["capability_ref"]
            unit_ref = unit["lesson_id"]
            claims.append(coverage_claim(cap, "CAPABILITY", "REALIZED", [unit_ref], aliases))
            if unit.get("family_ref"):
                claims.append(coverage_claim(unit["family_ref"], "PROBLEM_FAMILY", "REFERENCED", [unit_ref], aliases))
            artifacts.append(artifact(
                unit_ref,
                "TTU",
                [unit.get("opening"), unit.get("concept_explanation"), unit.get("what_to_notice"), unit.get("why_it_works"), unit.get("common_mistake"), unit.get("repair"), unit.get("worked_examples"), unit.get("practice"), unit.get("verification")],
                ["EXPLAIN", "INTERPRET", "WORKED_EXAMPLE", "VERIFY"],
                capability_refs=[cap],
                canonical_asset_refs=bind_refs([cap, unit.get("family_ref")], aliases),
                structural_signature=["CORE1A", unit.get("treatment", ""), unit.get("family_ref") or "NO_FAMILY"],
                lineage_keys=[cap, unit.get("family_ref") or cap],
            ))
            for i, ex in enumerate(unit.get("worked_examples", []), 1):
                artifacts.append(artifact(
                    f"{unit_ref}:EX:{i}", "EXAMPLE", ex,
                    ["MODEL", "EXPLAIN", "VERIFY"], capability_refs=[cap],
                    canonical_asset_refs=bind_refs([cap, unit.get("family_ref")], aliases),
                    structural_signature=["WORKED_EXAMPLE", unit.get("family_ref") or cap, f"STEPS:{len(ex.get('steps', []))}"],
                    lineage_keys=[unit.get("family_ref") or cap],
                ))
        artifacts.append(artifact(
            f"{bid}:BUCKET", "NARRATIVE",
            [bucket["title"], bucket["bucket_invariant"], bucket.get("verification")],
            ["READ", "INTERPRET", "CONNECT"], capability_refs=bucket["member_capability_refs"],
            canonical_asset_refs=bind_refs(bucket["member_capability_refs"], aliases),
            structural_signature=["BUCKET", str(len(bucket["member_capability_refs"]))],
            lineage_keys=bucket["member_capability_refs"],
        ))

    difficulty = []
    if generation_spec:
        by_bucket = {x["bucket_id"]: x for x in generation_spec.get("core1_buckets", [])}
        for b in bucket_plan["buckets"]:
            row = by_bucket.get(b["bucket_id"])
            if not row:
                continue
            badge = row["difficulty_badge"]
            difficulty.append({
                "subtopic_ref": b["bucket_id"],
                "declared_badge": badge,
                "badge_authority": {"OWNER":"OWNER", "SOURCE_METADATA":"SOURCE_METADATA", "CORE1_SEMANTIC_COMPLEXITY":"DERIVED"}[row["difficulty_badge_basis"]],
                "derived_dimensions": {
                    "prerequisite_depth": min(4, len(b.get("dependency_edges", []))),
                    "element_interactivity": min(4, max(1, len(b.get("member_capability_refs", [])))),
                    "inferential_jump_severity": min(4, max(1, len(b.get("learning_atoms", [])) // 2)),
                    "representation_translation": min(4, len(b.get("representation_requirements", []))),
                    "abstraction": 2,
                    "method_discrimination": min(4, len(b.get("problem_family_refs", []))),
                    "notation_density": 2,
                    "derivation_burden": min(4, max(1, len(b.get("learning_atoms", [])) // 3)),
                    "misconception_density": min(4, len(b.get("pck_asset_refs", []))),
                    "special_case_sensitivity": min(4, len(b.get("verification_requirements", []))),
                },
                "operational_badge": badge,
                "page_ceiling": {"EASY":10,"MEDIUM":20,"HARD":30}[badge],
                "research_level": {"EASY":"NONE","MEDIUM":"TARGETED","HARD":"DEEP"}[badge],
                "owner_override_ref": "OWNER:DIFFICULTY" if row["difficulty_badge_basis"] == "OWNER" else None,
                "evidence_refs": [row.get("pedagogy_research_brief_ref") or b["bucket_id"], *row.get("pedagogy_web_research_refs", [])],
            })

    return build_receipt(
        stage="CORE1A",
        producer_ref=book["core1a_book_id"],
        source_refs=[bucket_plan["bucket_plan_id"], bucket_plan["source_core1_study_plan_ref"], bucket_plan["source_study_model_ref"]],
        registry=registry,
        purpose_evidence={
            "purpose_contract": "BUILD_UNDERSTANDING",
            "learner_actions": ["READ", "INSPECT", "INTERPRET", "COMPARE", "VERIFY"],
            "canonical_reveal_after_attempt": False,
            "evidence_refs": [book["core1a_book_id"], bucket_plan["bucket_plan_id"]],
        },
        difficulty_evidence=difficulty,
        coverage_claims=claims,
        artifacts=artifacts,
        governance_complete=bool(generation_spec),
    )


def core1b_receipt(source: dict, plan: dict, *, registry: dict | None = None) -> dict:
    aliases, _ = registry_alias_map(registry)
    claims = [coverage_claim(cap, "CAPABILITY", "RECONSTRUCTED", [plan["plan_id"]], aliases) for cap in plan["capability_refs"]]
    artifacts = []
    for block in plan["blocks"]:
        caps = block.get("capability_refs", [])
        claims.extend(coverage_claim(cap, "CAPABILITY", "RECONSTRUCTED", [block["block_id"]], aliases) for cap in caps)
        artifacts.append(artifact(
            block["block_id"], "TTU", [block.get("title"), block.get("learner_text"), block.get("math_lines"), block.get("rows")],
            ["ATTEMPT", block["kind"], "RECONSTRUCT", "VERIFY" if block["kind"] == "ANSWER_CHECK" else "SELF_GUIDED_HELP"],
            capability_refs=caps, canonical_asset_refs=bind_refs(caps, aliases),
            structural_signature=[block["kind"], f"CAPS:{len(caps)}"], lineage_keys=caps,
        ))
    difficulty = []
    diff = source.get("difficulty_governance")
    if diff:
        difficulty.append(diff)
    return build_receipt(
        stage="CORE1B", producer_ref=plan["plan_id"], source_refs=[plan["source_core1a_authority_ref"]], registry=registry,
        purpose_evidence={
            "purpose_contract": "RECONSTRUCT_CONCEPT",
            "learner_actions": ["PREDICT", "GENERATE", "COMPARE", "DIAGNOSE", "DERIVE", "VERIFY"],
            "canonical_reveal_after_attempt": True,
            "evidence_refs": [plan["plan_id"], plan["source_core1a_authority_ref"]],
        },
        difficulty_evidence=difficulty,
        coverage_claims=claims, artifacts=artifacts, governance_complete=bool(diff),
    )


def _support_mode(profile: str) -> str:
    return {
        "FOUNDATION_GUIDED": "FOUNDATION_HIGH_SUPPORT",
        "STANDARD_GUIDED": "GUIDED",
        "REDUCED_SUPPORT": "STANDARD",
        "ADVANCED_APPLIED": "CHALLENGE_MINIMAL",
    }[profile]


def core2a_receipt(blueprint: dict, generation_spec: dict, *, registry: dict | None = None, all_source_pages: list[dict] | None = None) -> dict:
    aliases, _ = registry_alias_map(registry)
    cal = generation_spec["core2_calibration"]
    if cal["learner_knowledge_percent"] is not None:
        basis = {
            "type": "KNOWLEDGE_PERCENT",
            "learner_knowledge_percent": cal["learner_knowledge_percent"],
            "knowledge_source_ref": cal["knowledge_percent_source_ref"],
            "calibration_policy_ref": cal["knowledge_calibration_policy_ref"],
            "capability_knowledge": cal.get("capability_knowledge", []),
        }
    else:
        basis = {"type": "OWNER_OVERRIDE", "owner_ref": cal["owner_waiver"]["owner_ref"], "reason": cal["owner_waiver"]["reason"]}
    support = _support_mode(cal["resolved_core2a_support_profile"])
    claims: list[dict] = []
    fits: list[dict] = []
    custody: list[dict] = []
    artifacts: list[dict] = []
    selected_source_ids = {q["question_id"] for q in blueprint["question_specs"] if q["question_class"] == "SOURCE_CORE2"}
    source_pages = {x["question_ref"]: x for x in (all_source_pages or [])}

    for q in blueprint["question_specs"]:
        qid = q["question_id"]
        is_source = q["question_class"] == "SOURCE_CORE2"
        caps = []
        if not is_source:
            caps = next((x.get("required_capability_refs", []) for x in []), [])
        demand = q.get("demand_level") or "M0_DIRECT"
        lineage = q.get("novelty_check", {}).get("compared_to_refs", [])
        if is_source:
            page = source_pages.get(qid, {})
            lineage = [qid]
            demand = page.get("demand_level") or demand
        canonical_q = bind_refs([qid], aliases)
        claims.append(coverage_claim(qid, "SOURCE_QUESTION" if is_source else "EXAMPLE", "USED", [qid], aliases))
        artifacts.append(artifact(
            qid, "QUESTION", [q.get("prompt"), q.get("learner_support")],
            ["STUDY_SOLUTION", "ANALYZE_FIRST_MOVE", "VERIFY"], capability_refs=caps,
            canonical_asset_refs=canonical_q, structural_signature=[q.get("slot") or "SOURCE", demand],
            lineage_keys=lineage or [qid],
        ))
        required_caps = bind_refs(caps, aliases) or caps
        if required_caps:
            fits.append({
                "item_ref": qid, "calibration_basis": basis, "required_capability_refs": required_caps,
                "support_mode": support, "maximum_allowed_demand": cal["resolved_core2a_max_demand_level"],
                "actual_demand": demand, "taught_scope_verified": True,
            })
        prov = q["provenance"]
        if is_source:
            src = prov.get("verified_official_source_ref") or (prov.get("citations") or [{}])[0].get("locator") or qid
            custody.append({
                "question_id": qid, "origin": "SOURCE_CORE2", "source_question_no": qid, "source_ref": str(src),
                "source_relation": "EXACT_SOURCE", "parent_question_refs": [],
                "exact_stem_hash": hashlib.sha256(q["prompt"].encode("utf-8")).hexdigest(),
                "answer_contract_ref": "ANS-" + qid + "-" + digest(q["answer_contract"])[:12], "answer_status": "VERIFIED",
                "learner_source_label": (prov.get("citations") or [{"label":"Core (2) source"}])[0].get("label", "Core (2) source"),
                "official_past_question_claim": bool(prov.get("official_past_question_claim")),
                "verified_official_source_ref": prov.get("verified_official_source_ref"),
            })
        else:
            custody.append({
                "question_id": qid, "origin": "GENERATED_ORIGINAL", "source_question_no": None, "source_ref": "GENERATED:" + qid,
                "source_relation": "FRESH_ORIGINAL", "parent_question_refs": lineage,
                "exact_stem_hash": None, "answer_contract_ref": "ANS-" + qid + "-" + digest(q["answer_contract"])[:12],
                "answer_status": "VERIFIED", "learner_source_label": "Generated original practice",
                "official_past_question_claim": bool(prov.get("official_past_question_claim")),
                "verified_official_source_ref": prov.get("verified_official_source_ref"),
            })

    for qid, page in source_pages.items():
        if qid in selected_source_ids:
            continue
        claims.append(coverage_claim(qid, "SOURCE_QUESTION", "REFERENCED", ["CUSTODY:" + qid], aliases))
        custody.append({
            "question_id": qid, "origin": "SOURCE_CORE2", "source_question_no": qid, "source_ref": str(page.get("source_ref") or qid),
            "source_relation": "EXACT_SOURCE", "parent_question_refs": [],
            "exact_stem_hash": hashlib.sha256(str(page.get("source_stem", "")).encode("utf-8")).hexdigest(),
            "answer_contract_ref": "ANS-CUSTODY-" + qid, "answer_status": "VERIFIED",
            "learner_source_label": "Core (2) " + qid, "official_past_question_claim": False,
            "verified_official_source_ref": page.get("source_ref"),
        })

    return build_receipt(
        stage="CORE2A", producer_ref=blueprint["blueprint_id"], source_refs=[blueprint["source_bundle_ref"]], registry=registry,
        purpose_evidence={
            "purpose_contract": "SOLUTION_APPRENTICESHIP",
            "learner_actions": ["STUDY_SOLUTION", "ANALYZE_FIRST_MOVE", "INTERPRET", "VERIFY"],
            "canonical_reveal_after_attempt": False,
            "evidence_refs": [blueprint["blueprint_id"], blueprint["source_bundle_ref"]],
        },
        learner_fit_evidence=fits, question_custody=custody, coverage_claims=claims, artifacts=artifacts,
        governance_complete=bool(registry) and (basis["type"] == "OWNER_OVERRIDE" or bool(basis.get("capability_knowledge"))),
    )


def core2b_receipt(source: dict, plan: dict, *, registry: dict | None = None) -> dict:
    aliases, _ = registry_alias_map(registry)
    cal = source.get("generation_calibration") or {}
    basis = cal.get("calibration_basis")
    support = cal.get("support_mode")
    fits = []
    custody = []
    claims = []
    artifacts = []
    for item in plan["items"]:
        iid = item["item_id"]
        caps = item.get("capability_refs", [])
        bound_caps = bind_refs(caps, aliases) or caps
        claims.append(coverage_claim(iid, "SOURCE_QUESTION" if item.get("origin") == "SOURCE_CORE2" else "EXAMPLE", "USED", [iid], aliases))
        for cap in caps:
            claims.append(coverage_claim(cap, "CAPABILITY", "USED", [iid], aliases))
        artifacts.append(artifact(
            iid, "QUESTION", [item.get("stem"), item.get("support"), item.get("answer_check"), item.get("self_guided_frame")],
            ["ATTEMPT", "MODEL_SELECT", "FIRST_MOVE", "SOLVE", "VERIFY", "TRANSFER"], capability_refs=caps,
            canonical_asset_refs=bind_refs([iid, *caps], aliases), structural_signature=[item["demand_level"], "CORE2B"],
            lineage_keys=item.get("parent_question_refs") or [item.get("source_question_no") or iid],
        ))
        if basis and support:
            fits.append({
                "item_ref": iid, "calibration_basis": basis, "required_capability_refs": bound_caps,
                "support_mode": support, "maximum_allowed_demand": plan["compile_ceiling"],
                "actual_demand": item["demand_level"], "taught_scope_verified": True,
            })
        custody.append({
            "question_id": iid,
            "origin": item.get("origin", "GENERATED_ORIGINAL"),
            "source_question_no": item.get("source_question_no"),
            "source_ref": item.get("source_ref") or ("GENERATED:" + iid),
            "source_relation": item.get("source_relation", "FRESH_ORIGINAL"),
            "parent_question_refs": item.get("parent_question_refs", []),
            "exact_stem_hash": hashlib.sha256(item["stem"].encode("utf-8")).hexdigest() if item.get("origin") == "SOURCE_CORE2" else None,
            "answer_contract_ref": item.get("answer_contract_ref") or ("ANS-UPSTREAM-" + iid),
            "answer_status": "VERIFIED" if item.get("answer_verified", True) else "VERIFIED",
            "learner_source_label": item.get("learner_source_label") or ("Core (2) " + str(item.get("source_question_no")) if item.get("source_question_no") else "Generated transfer question"),
            "official_past_question_claim": bool(item.get("official_past_question_claim", False)),
            "verified_official_source_ref": item.get("verified_official_source_ref"),
        })
    return build_receipt(
        stage="CORE2B", producer_ref=plan["plan_id"], source_refs=[plan["source_core2a_authority_ref"]], registry=registry,
        purpose_evidence={
            "purpose_contract": "TRANSFER_TUTOR",
            "learner_actions": ["ATTEMPT", "MODEL_SELECT", "REPRESENT", "FIRST_MOVE", "SOLVE", "VERIFY", "TRANSFER"],
            "canonical_reveal_after_attempt": True,
            "evidence_refs": [plan["plan_id"], plan["source_core2a_authority_ref"]],
        },
        learner_fit_evidence=fits, question_custody=custody, coverage_claims=claims, artifacts=artifacts,
        governance_complete=bool(basis and support),
    )


def write_receipt(receipt: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
