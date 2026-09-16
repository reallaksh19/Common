#!/usr/bin/env python3
"""Multi-bucket-safe entrypoint for the Engineering-bound four-producer golden.

The Engineering-bound runner owns authority projection, current Engineering
admission, producer execution and strict release. This entrypoint supplies three
canonical rules discovered by the real cold-start corpus:

1. a source question may participate in multiple teaching buckets while the Domain
   Registry stores it under one deterministic primary subtopic;
2. one Engineering source object must exist only once in the Canonical Domain
   Registry even when it participates in many teaching scopes; and
3. generation calibration must come from current authority: SDU derives Core1
   intrinsic difficulty from exact Engineering profiles, while LAU consumes actual
   learner evidence or an explicit owner waiver and never fabricates a percentage.

Engineering-derived mathematical truth is canonicalized by exact source identity.
Local subtopic/join/capability/question bindings and DIRECT-vs-prerequisite roles
are retained in a digest-bound scope-membership ledger and independently
revalidated against the current Engineering graph before release.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import run_engineering_bound_producer_release_golden as base
from compile_sdu_lau_generation_spec import compile_generation_spec
from project_engineering_to_domain_registry_v2 import project_engineering_to_domain_registry_v2
from validate_engineering_domain_projection_binding_v2 import validate_release_projection_binding_v2

_LAST_ENGINEERING_DOMAIN_PROJECTION = None
_LAST_ENGINEERING_REGISTRY = None
_LAST_ENGINEERING_PROJECTION_COVERAGE = None
_LAST_STUDY_MODEL = None
_LAST_SDU_LAU_AUDIT = None
_LAST_PEDAGOGY_RESEARCH_MANIFEST = None
_ORIGINAL_BUILD_REGISTRY = base.legacy.build_registry
_ORIGINAL_CORE1B_INPUT = base.legacy.core1b_input
_ORIGINAL_CORE2B_INPUT = base.legacy.core2b_input
_ORIGINAL_RUN_CLI = base.legacy.run_cli

HERE = Path(__file__).resolve()
MATH_BLUEPRINT = HERE.parents[1]
BOUND_WAIVER = MATH_BLUEPRINT / "golden" / "bound_producer_release" / "core2-owner-waiver.test.json"
CORE1B_DIFFICULTY_CONSEQUENCES = {
    "EASY": {"page_ceiling": 10, "research_level": "NONE"},
    "MEDIUM": {"page_ceiling": 20, "research_level": "TARGETED"},
    "HARD": {"page_ceiling": 30, "research_level": "DEEP"},
}


def multi_bucket_safe_subtopics(bucket_plan: dict):
    bucket_sid = {}
    cap_sid = {}
    q_sid = {}
    for bucket in bucket_plan["buckets"]:
        sid = "BOUND-SUB-" + base.production_digest(sorted(bucket["member_capability_refs"]))[:12].upper()
        bucket_sid[bucket["bucket_id"]] = sid
        for cap in bucket["member_capability_refs"]:
            if cap in cap_sid and cap_sid[cap] != sid:
                base.fail("BOUND_GOLDEN_CAPABILITY_MULTI_SUBTOPIC", cap)
            cap_sid[cap] = sid
        for qid in bucket.get("core2_question_refs") or []:
            q_sid.setdefault(qid, sid)
    return bucket_sid, cap_sid, q_sid


def authority_generation_spec(bucket_plan: dict, core1: dict, bucket_sid: dict[str, str]) -> dict:
    """Replace the legacy EASY/1/60% golden fixture with SDU/LAU authority."""
    global _LAST_SDU_LAU_AUDIT
    global _LAST_PEDAGOGY_RESEARCH_MANIFEST
    if _LAST_STUDY_MODEL is None:
        base.fail("BOUND_GOLDEN_STUDY_MODEL_CONTEXT_MISSING")

    engineering_registry = base.load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
    crosswalk = base.load_crosswalk(base.DEFAULT_CROSSWALK)
    projection_coverage = base.resolve_bucket_gate_map(
        crosswalk,
        bucket_plan,
        engineering_registry=engineering_registry,
        fail_on_gap=True,
    )
    waiver = json.loads(BOUND_WAIVER.read_text(encoding="utf-8"))
    expected = base.legacy.load(base.legacy.EXPECTED)
    spec, research_manifest, audit = compile_generation_spec(
        bucket_plan=bucket_plan,
        study_model=_LAST_STUDY_MODEL,
        bucket_sid=bucket_sid,
        engineering_registry=engineering_registry,
        projection_coverage=projection_coverage,
        purpose=expected["purpose"],
        release_class="TEST_ONLY",
        owner_waiver=waiver,
        allow_test_research_fixture=True,
    )

    capability_plans = _LAST_STUDY_MODEL.get("capability_plans") or []
    audit["study_model_ref"] = _LAST_STUDY_MODEL.get("study_model_id")
    audit["study_model_digest"] = _LAST_STUDY_MODEL.get("study_model_digest")
    audit["unknown_capability_count"] = sum(
        1 for row in capability_plans if row.get("learner_state_readiness") == "UNKNOWN"
    )
    audit["learner_observation_ref_count"] = sum(
        len(row.get("learner_state_observation_refs") or []) for row in capability_plans
    )
    audit["owner_waiver_id"] = waiver["waiver_id"]
    audit["owner_waiver_digest"] = waiver["waiver_digest"]
    _LAST_SDU_LAU_AUDIT = audit
    _LAST_PEDAGOGY_RESEARCH_MANIFEST = research_manifest
    return spec


def sdu_aware_core1b_input(bucket: dict, book_bucket: dict, spec_row: dict, core1a_book_id: str, index: int) -> dict:
    """Preserve the same SDU finding and its operational consequences in Core1B."""
    doc = _ORIGINAL_CORE1B_INPUT(bucket, book_bucket, spec_row, core1a_book_id, index)
    badge = spec_row["difficulty_badge"]
    if badge not in CORE1B_DIFFICULTY_CONSEQUENCES:
        base.fail("BOUND_GOLDEN_CORE1B_DIFFICULTY_BADGE_INVALID", badge)
    consequence = CORE1B_DIFFICULTY_CONSEQUENCES[badge]
    difficulty = doc["difficulty_governance"]
    difficulty["page_ceiling"] = consequence["page_ceiling"]
    difficulty["research_level"] = consequence["research_level"]
    if difficulty["operational_badge"] != badge or difficulty["declared_badge"] != badge:
        base.fail("BOUND_GOLDEN_CORE1B_DIFFICULTY_BADGE_DRIFT", bucket["bucket_id"])
    return doc


def lau_aware_core2b_input(blueprint: dict, generation_spec: dict) -> dict:
    """Build Core2B calibration without inventing capability percentages in waiver mode."""
    cal = generation_spec["core2_calibration"]
    if cal["learner_knowledge_percent"] is not None:
        return _ORIGINAL_CORE2B_INPUT(blueprint, generation_spec)

    waiver = cal.get("owner_waiver")
    if not waiver:
        base.fail("BOUND_GOLDEN_CORE2B_LAU_WAIVER_MISSING")
    if cal.get("capability_knowledge"):
        base.fail("BOUND_GOLDEN_CORE2B_WAIVER_HAS_FAKE_CAPABILITY_KNOWLEDGE")

    specs = list(blueprint["question_specs"])
    if not specs:
        base.fail("BOUND_GOLDEN_CORE2A_NO_LEGAL_ITEMS")
    caps = sorted({cap for row in specs for cap in row.get("required_capability_refs", [])})
    items = []
    for i, row in enumerate(specs, 1):
        parent = row["question_id"]
        iid = "B2-" + base.production_digest([parent, i])[:12].upper()
        rcaps = list(row.get("required_capability_refs", []))
        items.append({
            "item_id": iid,
            "core2a_item_ref": parent,
            "demand_level": "M1_CONTROLLED_VARIATION",
            "learner_label": "Fresh controlled transfer",
            "family_label_visible": True,
            "capability_refs": rcaps,
            "stem": "A fresh variation preserves the governed mathematical capability behind source item " + parent + ". Select the model, state the first executable move, and explain how the result should be independently verified.",
            "support": [],
            "answer_check": "A valid response must select a model consistent with the governed capability, justify the first move, and state an independent verification that checks the result against the problem conditions.",
            "origin": "GENERATED_ORIGINAL",
            "source_question_no": None,
            "source_ref": "GENERATED:" + iid,
            "source_relation": "FRESH_ORIGINAL",
            "parent_question_refs": [parent],
            "answer_contract_ref": "ANS-" + iid + "-OPEN",
            "learner_source_label": "Generated transfer from " + parent,
            "official_past_question_claim": False,
            "verified_official_source_ref": None,
        })
    return {
        "core2a_authority_ref": blueprint["blueprint_id"],
        "purpose": blueprint["purpose"],
        "max_demand_level": cal["resolved_core2b_max_demand_level"],
        "approved_capability_refs": caps,
        "core2a_legal_item_ids": [row["question_id"] for row in specs],
        "generation_calibration": {
            "support_mode": "GUIDED",
            "calibration_basis": {
                "type": "OWNER_OVERRIDE",
                "owner_ref": waiver["owner_ref"],
                "reason": waiver["reason"],
            },
        },
        "title": "Bound Core2B transfer golden",
        "items": items,
    }


def research_aware_run_cli(script: Path, args: list[str]) -> str:
    """Carry the exact compiled pedagogy-research manifest into Core1A.

    The legacy bound runner predates the manifest argument. Keep its orchestration
    intact while supplying the missing custody edge at the CLI boundary.
    """
    forwarded = list(args)
    if script.name == "realize_math_core1a.py" and _LAST_PEDAGOGY_RESEARCH_MANIFEST is not None:
        if "--generation-spec" not in forwarded:
            base.fail("BOUND_GOLDEN_RESEARCH_WITHOUT_GENERATION_SPEC")
        spec_path = Path(forwarded[forwarded.index("--generation-spec") + 1])
        research_path = spec_path.parent / "pedagogy_research_manifest.test.json"
        base.write(research_path, _LAST_PEDAGOGY_RESEARCH_MANIFEST)
        if "--pedagogy-research-manifest" not in forwarded:
            forwarded += ["--pedagogy-research-manifest", str(research_path)]
    return _ORIGINAL_RUN_CLI(script, forwarded)


def rich_engineering_registry_builder(core1, core2, bucket_plan, bucket_sid, cap_sid, q_sid, answer_refs):
    """Upgrade the integration registry to canonical rich Engineering authority."""
    global _LAST_ENGINEERING_DOMAIN_PROJECTION
    global _LAST_ENGINEERING_REGISTRY
    global _LAST_ENGINEERING_PROJECTION_COVERAGE
    base_registry = _ORIGINAL_BUILD_REGISTRY(
        core1, core2, bucket_plan, bucket_sid, cap_sid, q_sid, answer_refs
    )
    engineering_registry = base.load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
    crosswalk = base.load_crosswalk(base.DEFAULT_CROSSWALK)
    projection_coverage = base.resolve_bucket_gate_map(
        crosswalk,
        bucket_plan,
        engineering_registry=engineering_registry,
        fail_on_gap=True,
    )
    rich_registry, receipt = project_engineering_to_domain_registry_v2(
        base_registry,
        engineering_registry=engineering_registry,
        projection_coverage=projection_coverage,
        bucket_plan=bucket_plan,
        bucket_sid=bucket_sid,
        core2_pages=core2["pages"],
    )
    _LAST_ENGINEERING_DOMAIN_PROJECTION = receipt
    _LAST_ENGINEERING_REGISTRY = engineering_registry
    _LAST_ENGINEERING_PROJECTION_COVERAGE = projection_coverage
    return rich_registry


def main() -> None:
    global _LAST_STUDY_MODEL
    base.bucket_subtopics = multi_bucket_safe_subtopics
    base.legacy.build_generation_spec = authority_generation_spec
    base.legacy.core1b_input = sdu_aware_core1b_input
    base.legacy.core2b_input = lau_aware_core2b_input
    base.legacy.build_registry = rich_engineering_registry_builder
    base.legacy.run_cli = research_aware_run_cli
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--core2-plan", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    _LAST_STUDY_MODEL = json.loads(Path(args.study_model).read_text(encoding="utf-8"))
    summary = base.run_bound(Path(args.core1_plan), Path(args.study_model), Path(args.core2_plan), out_dir)

    if _LAST_ENGINEERING_DOMAIN_PROJECTION is None:
        base.fail("BOUND_GOLDEN_ENGINEERING_DOMAIN_PROJECTION_MISSING")
    if _LAST_ENGINEERING_REGISTRY is None or _LAST_ENGINEERING_PROJECTION_COVERAGE is None:
        base.fail("BOUND_GOLDEN_ENGINEERING_DOMAIN_REVALIDATION_CONTEXT_MISSING")
    if _LAST_SDU_LAU_AUDIT is None:
        base.fail("BOUND_GOLDEN_SDU_LAU_AUDIT_MISSING")

    projection_path = out_dir / "inputs" / "engineering_domain_projection_receipt.json"
    base.write(projection_path, _LAST_ENGINEERING_DOMAIN_PROJECTION)
    base.write(out_dir / "inputs" / "sdu_lau_generation_audit.json", _LAST_SDU_LAU_AUDIT)
    if _LAST_PEDAGOGY_RESEARCH_MANIFEST is not None:
        base.write(
            out_dir / "inputs" / "pedagogy_research_manifest.test.json",
            _LAST_PEDAGOGY_RESEARCH_MANIFEST,
        )

    generation_spec = json.loads((out_dir / "inputs" / "generation_spec.json").read_text(encoding="utf-8"))
    calibration = generation_spec["core2_calibration"]
    if calibration["learner_knowledge_percent"] is not None:
        base.fail("BOUND_GOLDEN_LAU_FABRICATED_PERCENT_PRESENT")
    if not calibration.get("owner_waiver"):
        base.fail("BOUND_GOLDEN_LAU_OWNER_WAIVER_MISSING")

    summary["engineering_domain_projection_ref"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["projection_id"]
    summary["engineering_domain_projection_digest"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["projection_digest"]
    summary["engineering_domain_base_asset_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["base_asset_count"]
    summary["engineering_domain_projected_asset_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["projected_asset_count"]
    summary["engineering_domain_scope_membership_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["scope_membership_count"]
    summary["engineering_domain_expanded_projection_count"] = _LAST_ENGINEERING_DOMAIN_PROJECTION["expanded_projected_asset_count"]
    summary["engineering_domain_deduplicated_scope_copy_count"] = (
        _LAST_ENGINEERING_DOMAIN_PROJECTION["scope_membership_count"]
        - _LAST_ENGINEERING_DOMAIN_PROJECTION["projected_asset_count"]
    )
    summary["engineering_domain_transitive_gate_count"] = len(_LAST_ENGINEERING_DOMAIN_PROJECTION["transitive_gate_ids"])
    summary["sdu_difficulty_badge_counts"] = _LAST_SDU_LAU_AUDIT["sdu_difficulty_badge_counts"]
    summary["lau_calibration_mode"] = _LAST_SDU_LAU_AUDIT["lau_mode"]
    summary["lau_fabricated_percent"] = _LAST_SDU_LAU_AUDIT["lau_fabricated_percent"]
    summary["lau_owner_waiver_id"] = _LAST_SDU_LAU_AUDIT["owner_waiver_id"]
    summary["lau_owner_waiver_digest"] = _LAST_SDU_LAU_AUDIT["owner_waiver_digest"]
    summary["learner_observation_ref_count"] = _LAST_SDU_LAU_AUDIT["learner_observation_ref_count"]
    summary["pedagogy_research_manifest_ref"] = _LAST_SDU_LAU_AUDIT["pedagogy_research_manifest_ref"]
    summary["pedagogy_research_manifest_digest"] = _LAST_SDU_LAU_AUDIT["pedagogy_research_manifest_digest"]

    if _LAST_PEDAGOGY_RESEARCH_MANIFEST is None:
        base.fail("BOUND_GOLDEN_PEDAGOGY_RESEARCH_MANIFEST_MISSING")
    if summary["pedagogy_research_manifest_ref"] != _LAST_PEDAGOGY_RESEARCH_MANIFEST["manifest_id"]:
        base.fail("BOUND_GOLDEN_PEDAGOGY_RESEARCH_MANIFEST_REF_DRIFT")
    if summary["pedagogy_research_manifest_digest"] != _LAST_PEDAGOGY_RESEARCH_MANIFEST["manifest_digest"]:
        base.fail("BOUND_GOLDEN_PEDAGOGY_RESEARCH_MANIFEST_DIGEST_DRIFT")

    decision_count = _LAST_SDU_LAU_AUDIT["pedagogy_research_decision_count"]
    claim_count = _LAST_SDU_LAU_AUDIT["pedagogy_research_claim_count"]
    if decision_count != len(_LAST_PEDAGOGY_RESEARCH_MANIFEST["decisions"]):
        base.fail("BOUND_GOLDEN_PEDAGOGY_RESEARCH_DECISION_COUNT_DRIFT")
    if claim_count != len(_LAST_PEDAGOGY_RESEARCH_MANIFEST["claims"]):
        base.fail("BOUND_GOLDEN_PEDAGOGY_RESEARCH_CLAIM_COUNT_DRIFT")
    summary["pedagogy_research_manifest_release_class"] = _LAST_PEDAGOGY_RESEARCH_MANIFEST["release_class"]
    summary["pedagogy_research_decision_count"] = decision_count
    summary["pedagogy_research_claim_count"] = claim_count

    if summary["registry_ref"] != _LAST_ENGINEERING_DOMAIN_PROJECTION["domain_registry_ref"]:
        base.fail("BOUND_GOLDEN_ENGINEERING_DOMAIN_REGISTRY_REF_DRIFT")

    legacy_key = "engineering_authorized_direct_gate_ids"
    if legacy_key in summary:
        summary["engineering_authorized_direct_gate_count"] = summary.pop(legacy_key)

    registry = json.loads((out_dir / "inputs" / "domain_registry.json").read_text(encoding="utf-8"))
    full_audit = json.loads((out_dir / "full_mixed_engineering_coverage_audit.json").read_text(encoding="utf-8"))
    projection_validation = validate_release_projection_binding_v2(
        registry,
        _LAST_ENGINEERING_DOMAIN_PROJECTION,
        summary,
        full_audit,
        engineering_registry=_LAST_ENGINEERING_REGISTRY,
        projection_coverage=_LAST_ENGINEERING_PROJECTION_COVERAGE,
    )
    summary["engineering_domain_projection_validation"] = projection_validation
    for check in (
        "ENGINEERING_DOMAIN_CANONICAL_ASSET_MEMBERSHIP_CUSTODY",
        "SDU_LAU_AUTHORITY_CALIBRATION",
    ):
        if check not in summary["release_checks"]:
            summary["release_checks"].append(check)

    base.write(out_dir / "bound_producer_release_summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
