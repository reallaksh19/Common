#!/usr/bin/env python3
"""Compile Mathematics self-teaching generation calibration from governed authority.

SDU owns Core1 intrinsic difficulty.  It derives the ten Blueprint difficulty
axes from the current Mathematics Engineering-gate difficulty profiles for the
exact gates bound to each teaching bucket.  It never consumes learner-state
percentages.

LAU owns Core2 learner fit.  It accepts exactly one of:
  * typed learner-knowledge evidence whose observation refs are already present
    in the current StudyModel; or
  * a typed owner waiver.

UNKNOWN learner state is never converted to a synthetic percentage.
"""
from __future__ import annotations

import copy
from typing import Any

from blueprint_common import digest, fail, validate_schema
from validate_pedagogy_research_manifest import (
    validate_generation_research_bindings,
    validate_manifest,
)
from validate_self_teaching_generation_spec import derived_difficulty, validate_generation_spec

PAGE_CAPS = {"EASY": 10, "MEDIUM": 20, "HARD": 30}
ENGINEERING_PROFILE_KEYS = {
    "prerequisite_depth",
    "element_interactivity",
    "inferential_jump_severity",
    "representation_translation",
    "model_discrimination",
    "sign_or_frame_sensitivity",
    "multi_step_dependency",
    "abstraction",
    "misconception_density",
    "synthesis",
}


def _gate_map(engineering_registry: dict) -> dict[str, dict]:
    rows = engineering_registry.get("subtopic_gates") or []
    out: dict[str, dict] = {}
    for gate in rows:
        gid = gate.get("subtopic_id")
        if not gid or gid in out:
            fail("MATH_SDU_ENGINEERING_GATE_ID_INVALID", str(gid))
        out[gid] = gate
    if not out:
        fail("MATH_SDU_ENGINEERING_REGISTRY_EMPTY")
    return out


def _bucket_gate_map(projection_coverage: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for row in projection_coverage.get("bucket_gate_map") or []:
        bid = row.get("bucket_id")
        if not bid or bid in out:
            fail("MATH_SDU_BUCKET_GATE_MAP_INVALID", str(bid))
        gates = list(row.get("engineering_gate_ids") or [])
        if not gates:
            fail("MATH_SDU_BUCKET_WITHOUT_ENGINEERING_GATE", bid)
        out[bid] = gates
    return out


def _profile(gate: dict) -> dict:
    profile = copy.deepcopy(gate.get("difficulty_profile") or {})
    missing = sorted(ENGINEERING_PROFILE_KEYS - set(profile))
    if missing:
        fail("MATH_SDU_ENGINEERING_DIFFICULTY_PROFILE_INCOMPLETE", f"{gate.get('subtopic_id')}:{','.join(missing)}")
    for key in ENGINEERING_PROFILE_KEYS:
        value = profile[key]
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 3:
            fail("MATH_SDU_ENGINEERING_DIFFICULTY_VALUE_INVALID", f"{gate.get('subtopic_id')}:{key}:{value}")
    return profile


def profile_to_sdu_dimensions(profile: dict) -> dict:
    """Map the Engineering 10D profile into the SDU 10D authoring profile.

    The mapping is structural and subject-wide.  No topic names or examples are
    inspected.  Engineering values remain on their native 0..3 scale; the
    Blueprint schema permits 0..4 so an owner can still explicitly raise a
    dimension to 4 through the existing owner-governed path when justified.
    """
    return {
        "prerequisite_depth": profile["prerequisite_depth"],
        "element_interactivity": profile["element_interactivity"],
        "inferential_jump_severity": profile["inferential_jump_severity"],
        "representation_translation": profile["representation_translation"],
        "abstraction": profile["abstraction"],
        "method_discrimination": profile["model_discrimination"],
        "notation_density": max(profile["representation_translation"], profile["abstraction"]),
        "derivation_burden": max(profile["multi_step_dependency"], profile["synthesis"]),
        "misconception_density": profile["misconception_density"],
        "special_case_sensitivity": profile["sign_or_frame_sensitivity"],
    }


def _max_dimensions(rows: list[dict]) -> dict:
    if not rows:
        fail("MATH_SDU_DIFFICULTY_SOURCE_EMPTY")
    keys = rows[0].keys()
    return {key: max(row[key] for row in rows) for key in keys}


def compile_sdu_rows(
    bucket_plan: dict,
    bucket_sid: dict[str, str],
    engineering_registry: dict,
    projection_coverage: dict,
) -> list[dict]:
    gates = _gate_map(engineering_registry)
    by_bucket = _bucket_gate_map(projection_coverage)
    rows: list[dict] = []
    for bucket in bucket_plan.get("buckets") or []:
        bid = bucket["bucket_id"]
        if bid not in bucket_sid:
            fail("MATH_SDU_BUCKET_SUBTOPIC_ID_MISSING", bid)
        if bid not in by_bucket:
            fail("MATH_SDU_BUCKET_ENGINEERING_BINDING_MISSING", bid)
        gate_ids = by_bucket[bid]
        profiles = []
        validation_refs = []
        for gid in gate_ids:
            if gid not in gates:
                fail("MATH_SDU_ENGINEERING_GATE_UNKNOWN", f"{bid}:{gid}")
            profile = _profile(gates[gid])
            profiles.append(profile_to_sdu_dimensions(profile))
            validation_refs.append(f"ENG-DIFF:{gid}:{digest(profile)[:16]}")
        dimensions = _max_dimensions(profiles)
        _, badge = derived_difficulty(dimensions)
        rows.append({
            "bucket_id": bid,
            "subtopic_id": bucket_sid[bid],
            "subtopic_title": bucket["title"],
            "difficulty_badge": badge,
            "difficulty_badge_basis": "CORE1_SEMANTIC_COMPLEXITY",
            "difficulty_dimensions": dimensions,
            "difficulty_validation_refs": validation_refs,
            "target_page_budget": PAGE_CAPS[badge],
            "subsubtopic_plan": [],
            "pedagogy_research_brief_ref": None,
            "pedagogy_web_research_refs": [],
            "source_integrity_verification_refs": [],
        })
    if not rows:
        fail("MATH_SDU_BUCKET_SET_EMPTY")
    return rows


def _validate_owner_waiver(waiver: dict, release_class: str) -> None:
    validate_schema(waiver, "math-core2-owner-waiver.schema.json")
    if waiver.get("waiver_digest") != digest(waiver, "waiver_digest"):
        fail("MATH_LAU_OWNER_WAIVER_DIGEST_MISMATCH")
    if release_class == "PRODUCTION" and waiver["release_class"] != "OWNER_DECLARED":
        fail("MATH_LAU_TEST_WAIVER_FOR_PRODUCTION")


def _validate_knowledge_evidence(evidence: dict, study_model: dict, release_class: str) -> None:
    validate_schema(evidence, "math-core2-learner-knowledge-evidence.schema.json")
    if evidence.get("evidence_digest") != digest(evidence, "evidence_digest"):
        fail("MATH_LAU_KNOWLEDGE_EVIDENCE_DIGEST_MISMATCH")
    if release_class == "PRODUCTION" and evidence["release_class"] != "PRODUCTION":
        fail("MATH_LAU_TEST_EVIDENCE_FOR_PRODUCTION")

    study = {row["capability_ref"]: row for row in study_model.get("capability_plans") or []}
    evidence_rows = {row["capability_ref"]: row for row in evidence["capability_knowledge"]}
    if len(evidence_rows) != len(evidence["capability_knowledge"]):
        fail("MATH_LAU_CAPABILITY_EVIDENCE_DUPLICATE")
    if set(evidence_rows) != set(study):
        missing = sorted(set(study) - set(evidence_rows))
        extra = sorted(set(evidence_rows) - set(study))
        fail("MATH_LAU_CAPABILITY_EVIDENCE_SCOPE_MISMATCH", f"missing={missing};extra={extra}")
    for cap, row in evidence_rows.items():
        observed = set(study[cap].get("learner_state_observation_refs") or [])
        claimed = set(row.get("observation_refs") or [])
        if not claimed or not claimed.issubset(observed):
            fail("MATH_LAU_CAPABILITY_EVIDENCE_NOT_IN_STUDY_MODEL", cap)


def compile_lau_calibration(
    study_model: dict,
    *,
    purpose: str,
    release_class: str,
    learner_knowledge_evidence: dict | None = None,
    owner_waiver: dict | None = None,
) -> dict:
    if (learner_knowledge_evidence is None) == (owner_waiver is None):
        fail("MATH_LAU_EXACTLY_ONE_EVIDENCE_OR_WAIVER_REQUIRED")

    if learner_knowledge_evidence is not None:
        _validate_knowledge_evidence(learner_knowledge_evidence, study_model, release_class)
        ev = learner_knowledge_evidence
        return {
            "purpose": purpose,
            "learner_knowledge_percent": ev["learner_knowledge_percent"],
            "knowledge_percent_source_ref": f"{ev['evidence_id']}@sha256:{ev['evidence_digest']}",
            "knowledge_calibration_policy_ref": ev["calibration_policy_ref"],
            "capability_knowledge": [
                {"capability_ref": row["capability_ref"], "percent": row["percent"]}
                for row in ev["capability_knowledge"]
            ],
            "owner_waiver": None,
            "resolved_core2a_support_profile": ev["resolved_core2a_support_profile"],
            "resolved_core2a_max_demand_level": ev["resolved_core2a_max_demand_level"],
            "resolved_core2b_max_demand_level": ev["resolved_core2b_max_demand_level"],
        }

    assert owner_waiver is not None
    _validate_owner_waiver(owner_waiver, release_class)
    waiver_ref = f"{owner_waiver['waiver_id']}@sha256:{owner_waiver['waiver_digest']}"
    return {
        "purpose": purpose,
        "learner_knowledge_percent": None,
        "knowledge_percent_source_ref": None,
        "knowledge_calibration_policy_ref": None,
        "capability_knowledge": [],
        "owner_waiver": {
            "owner_ref": waiver_ref,
            "reason": owner_waiver["reason"],
            "selected_core2a_support_profile": owner_waiver["selected_core2a_support_profile"],
            "selected_core2a_max_demand_level": owner_waiver["selected_core2a_max_demand_level"],
            "selected_core2b_max_demand_level": owner_waiver["selected_core2b_max_demand_level"],
        },
        "resolved_core2a_support_profile": owner_waiver["selected_core2a_support_profile"],
        "resolved_core2a_max_demand_level": owner_waiver["selected_core2a_max_demand_level"],
        "resolved_core2b_max_demand_level": owner_waiver["selected_core2b_max_demand_level"],
    }


def build_test_research_manifest(rows: list[dict]) -> dict | None:
    non_easy = [row for row in rows if row["difficulty_badge"] != "EASY"]
    if not non_easy:
        return None
    research_ref = "PED-WEB-BOUND-TEST-FIXTURE-v1"
    source = {
        "research_ref": research_ref,
        "source_url": "https://example.org/math-pedagogy-test-fixture",
        "source_title": "Explicit test-only pedagogy research fixture for governance-path validation",
        "publisher": "TEST FIXTURE",
        "accessed_on": "2026-09-15",
        "evidence_class": "TEST_FIXTURE",
        "capture_ref": "TEST_FIXTURE:math-pedagogy-governance",
        "capture_digest": digest({"fixture": "math-pedagogy-governance-v1"}),
        "supports": [
            "REPRESENTATION_DESIGN",
            "MISCONCEPTION_REPAIR",
            "INFERENTIAL_DECOMPOSITION",
            "TRANSFER_DESIGN",
            "WORKED_EXAMPLE_DESIGN",
            "FADING",
        ],
    }
    decisions = []
    claims = []
    for row in non_easy:
        depth = "DEEP" if row["difficulty_badge"] == "HARD" else "STANDARD"
        coverage = ["REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR"]
        if depth == "DEEP":
            coverage.extend(["INFERENTIAL_DECOMPOSITION", "TRANSFER_DESIGN"])
        decision_ref = "PED-BRIEF-TEST-" + digest({"subtopic": row["subtopic_id"], "depth": depth})[:16].upper()
        decisions.append({
            "decision_ref": decision_ref,
            "subtopic_ref": row["subtopic_id"],
            "research_depth": depth,
            "coverage": coverage,
            "research_refs": [research_ref],
            "decision_summary": "Test-only evidence exercises the required research custody path without asserting curriculum authority.",
        })
        for category in coverage:
            claims.append({
                "claim_ref": "PED-CLAIM-TEST-" + digest({"decision_ref": decision_ref, "category": category})[:16].upper(),
                "decision_ref": decision_ref,
                "support_category": category,
                "claim_text": f"Retained test evidence supports the {category.replace('_', ' ').lower()} pedagogy decision for this subtopic.",
                "confidence": "MODERATE",
                "confidence_basis": "Synthetic TEST_ONLY evidence validates claim-to-source custody and does not establish production evidence quality.",
                "evidence_links": [{
                    "research_ref": research_ref,
                    "stance": "SUPPORTS",
                    "rationale": "Fixture is retained to exercise this exact support category.",
                }],
                "contradiction_resolution": None,
            })
    manifest = {
        "schema_version": "1.1.0",
        "subject": "MATHEMATICS",
        "manifest_id": "MATH-PED-RESEARCH-BOUND-TEST-" + digest([row["subtopic_id"] for row in non_easy])[:12].upper(),
        "release_class": "TEST_ONLY",
        "curriculum_authority": False,
        "sources": [source],
        "decisions": decisions,
        "claims": claims,
        "manifest_digest": "",
    }
    manifest["manifest_digest"] = digest(manifest, "manifest_digest")
    validate_manifest(manifest)
    return manifest


def _bind_research(rows: list[dict], manifest: dict | None, release_class: str) -> None:
    non_easy = [row for row in rows if row["difficulty_badge"] != "EASY"]
    if not non_easy:
        return
    if manifest is None:
        fail("MATH_SDU_RESEARCH_BINDING_REQUIRED")
    validate_manifest(manifest)
    if release_class == "PRODUCTION" and manifest["release_class"] != "PRODUCTION":
        fail("MATH_SDU_TEST_RESEARCH_FOR_PRODUCTION")
    decisions = {}
    for decision in manifest["decisions"]:
        decisions[(decision["subtopic_ref"], decision["research_depth"])] = decision
    for row in non_easy:
        depth = "DEEP" if row["difficulty_badge"] == "HARD" else "STANDARD"
        key = (row["subtopic_id"], depth)
        if key not in decisions:
            fail("MATH_SDU_RESEARCH_DECISION_MISSING", f"{row['bucket_id']}:{depth}")
        decision = decisions[key]
        row["pedagogy_research_brief_ref"] = decision["decision_ref"]
        row["pedagogy_web_research_refs"] = list(decision["research_refs"])


def compile_generation_spec(
    *,
    bucket_plan: dict,
    study_model: dict,
    bucket_sid: dict[str, str],
    engineering_registry: dict,
    projection_coverage: dict,
    purpose: str,
    release_class: str,
    learner_knowledge_evidence: dict | None = None,
    owner_waiver: dict | None = None,
    pedagogy_research_manifest: dict | None = None,
    allow_test_research_fixture: bool = False,
) -> tuple[dict, dict | None, dict]:
    if release_class not in {"PRODUCTION", "TEST_ONLY"}:
        fail("MATH_SDU_LAU_RELEASE_CLASS_INVALID", release_class)
    rows = compile_sdu_rows(bucket_plan, bucket_sid, engineering_registry, projection_coverage)
    manifest = pedagogy_research_manifest
    if manifest is None and allow_test_research_fixture:
        if release_class != "TEST_ONLY":
            fail("MATH_SDU_TEST_RESEARCH_FIXTURE_FOR_PRODUCTION")
        manifest = build_test_research_manifest(rows)
    _bind_research(rows, manifest, release_class)
    calibration = compile_lau_calibration(
        study_model,
        purpose=purpose,
        release_class=release_class,
        learner_knowledge_evidence=learner_knowledge_evidence,
        owner_waiver=owner_waiver,
    )
    spec = {
        "schema_version": "1.3.0",
        "subject": "MATHEMATICS",
        "core1_buckets": rows,
        "core2_calibration": calibration,
    }
    validate_generation_spec(spec)
    validate_generation_research_bindings(spec, manifest)
    counts = {"EASY": 0, "MEDIUM": 0, "HARD": 0}
    for row in rows:
        counts[row["difficulty_badge"]] += 1
    audit = {
        "status": "PASS",
        "release_class": release_class,
        "sdu_bucket_count": len(rows),
        "sdu_difficulty_badge_counts": counts,
        "lau_mode": "KNOWLEDGE_PERCENT" if calibration["learner_knowledge_percent"] is not None else "OWNER_WAIVER",
        "lau_fabricated_percent": False,
        "pedagogy_research_manifest_ref": manifest["manifest_id"] if manifest else None,
        "pedagogy_research_manifest_digest": manifest["manifest_digest"] if manifest else None,
        "pedagogy_research_decision_count": len(manifest["decisions"]) if manifest else 0,
        "pedagogy_research_claim_count": len(manifest["claims"]) if manifest else 0,
    }
    return spec, manifest, audit
