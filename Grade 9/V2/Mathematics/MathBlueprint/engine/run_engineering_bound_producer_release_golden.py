#!/usr/bin/env python3
"""Run the actual four Mathematics producer CLIs under current Engineering authority.

The full mixed Grade 9 cold-start output is audited first against the exact
AssessmentScope -> Engineering crosswalk. Any uncovered capability remains visible
and blocks a claim that the full corpus is Engineering-complete.

The release proof itself uses only the exact source-question/capability projection
declared by the golden contract. The projection is deterministic and preserves the
source Core1/StudyModel/Core2 content for those exact IDs; it never chooses scope by
lesson title, fuzzy matching, or remembered topic aliases.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import run_bound_producer_release_golden as legacy
from compile_mathematics_engineering_workbench import (
    compile_binding,
    compile_closure,
    load as load_engineering,
    resolve_manifest,
)
from validate_assessment_engineering_crosswalk import (
    DEFAULT_CROSSWALK,
    load as load_crosswalk,
    resolve_bucket_gate_map,
)
from validate_self_teaching_generation_spec import validate_generation_spec

# Re-exported because the multi-bucket-safe entrypoint patches these names.
production_digest = legacy.production_digest
fail = legacy.fail
bucket_subtopics = legacy.bucket_subtopics


def write(path: Path, obj: Any) -> None:
    legacy.write(path, obj)


def _digest_without(value: dict, field: str) -> str:
    return legacy.c1base.digest(value, field)


def _project_authority_inputs(core1: dict, study: dict, core2: dict, expected: dict) -> tuple[dict, dict, dict, dict]:
    spec = expected["engineering_bound_projection"]
    selected_caps = list(spec["capability_refs"])
    selected_qs = list(spec["source_question_refs"])
    cap_set = set(selected_caps)
    q_set = set(selected_qs)

    core1_caps = {row["capability_ref"] for row in core1["lessons"]}
    study_caps = {row["capability_ref"] for row in study["capability_plans"]}
    core2_qs = {row["question_ref"] for row in core2["pages"]}
    if not cap_set or not q_set:
        fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_EMPTY")
    if not cap_set <= core1_caps or not cap_set <= study_caps:
        fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_CAPABILITY_UNKNOWN", ",".join(sorted(cap_set - (core1_caps & study_caps))))
    if not q_set <= core2_qs:
        fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_QUESTION_UNKNOWN", ",".join(sorted(q_set - core2_qs)))

    projected_study = copy.deepcopy(study)
    projected_study["capability_plans"] = [
        copy.deepcopy(row) for row in study["capability_plans"] if row["capability_ref"] in cap_set
    ]
    projected_study_caps = {row["capability_ref"] for row in projected_study["capability_plans"]}
    for row in projected_study["capability_plans"]:
        outside = sorted(set(row.get("prerequisite_refs", [])) - projected_study_caps)
        if outside:
            fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_PREREQUISITE_OPEN", f"{row['capability_ref']}:{','.join(outside)}")
        row["assessment_question_refs"] = [q for q in row.get("assessment_question_refs", []) if q in q_set]
    seed = {"source_study_model_ref": study["study_model_id"], "capability_refs": selected_caps, "source_question_refs": selected_qs}
    projected_study["study_model_id"] = "MATH-LSM-" + legacy.c1base.digest(seed)[:16]
    projected_study["input_digest"] = legacy.c1base.digest({"projection": seed, "source_input_digest": study["input_digest"]})
    projected_study["study_model_digest"] = _digest_without(projected_study, "study_model_digest")

    projected_core1 = copy.deepcopy(core1)
    projected_core1["lessons"] = [copy.deepcopy(row) for row in core1["lessons"] if row["capability_ref"] in cap_set]
    for lesson in projected_core1["lessons"]:
        lesson["assessment_question_refs"] = [q for q in lesson.get("assessment_question_refs", []) if q in q_set]
    projected_core1["study_model_ref"] = projected_study["study_model_id"]
    projected_core1["study_model_digest"] = projected_study["study_model_digest"]
    projected_core1["scope_completeness"] = {
        "required_capability_refs": sorted(cap_set),
        "covered_capability_refs": sorted(cap_set),
        "omitted_capability_refs": [],
        "status": "PASS",
    }
    projected_core1["input_digest"] = legacy.c1base.digest({"projection": seed, "source_input_digest": core1["input_digest"]})
    projected_core1["core1_study_plan_id"] = "MATH-C1SP-" + legacy.c1base.digest({"projection": seed, "kind": "CORE1"})[:16]
    projected_core1["plan_digest"] = _digest_without(projected_core1, "plan_digest")

    lesson_ids = {row["lesson_id"] for row in projected_core1["lessons"]}
    projected_core2 = copy.deepcopy(core2)
    projected_core2["pages"] = [copy.deepcopy(row) for row in core2["pages"] if row["question_ref"] in q_set]
    for page in projected_core2["pages"]:
        missing_caps = sorted(set(page.get("capability_refs", [])) - cap_set)
        if missing_caps:
            fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_QUESTION_REQUIRES_OUTSIDE_CAPABILITY", f"{page['question_ref']}:{','.join(missing_caps)}")
        linked = []
        for ref in page.get("core1_lesson_refs", []):
            stable = ref.get("stable_id") if isinstance(ref, dict) else None
            materialized = ref.get("materialized_lesson_id") if isinstance(ref, dict) else None
            if stable in lesson_ids or materialized in lesson_ids:
                linked.append(ref)
        page["core1_lesson_refs"] = linked
        if not linked:
            fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_CORE1_LINKAGE_LOST", page["question_ref"])
    projected_core2["summary"] = dict(projected_core2.get("summary") or {})
    projected_core2["summary"]["question_count"] = len(projected_core2["pages"])
    projected_core2["plan_id"] = "MATH-C2TP-" + legacy.c1base.digest({"projection": seed, "kind": "CORE2"})[:16]
    projected_core2["plan_digest"] = _digest_without(projected_core2, "plan_digest")

    projection_receipt = {
        "projection_type": "EXACT_ID_ENGINEERING_COVERED_GOLDEN",
        "source_core1_ref": core1["core1_study_plan_id"],
        "source_study_model_ref": study["study_model_id"],
        "source_core2_ref": core2["plan_id"],
        "projected_core1_ref": projected_core1["core1_study_plan_id"],
        "projected_study_model_ref": projected_study["study_model_id"],
        "projected_core2_ref": projected_core2["plan_id"],
        "capability_refs": selected_caps,
        "source_question_refs": selected_qs,
        "rationale": spec["rationale"],
    }
    projection_receipt["projection_digest"] = legacy.c1base.digest(projection_receipt)
    return projected_core1, projected_study, projected_core2, projection_receipt


def _build_engineering_admission(
    bucket_plan: dict,
    bucket_sid: dict[str, str],
    registry: dict,
    crosswalk: dict,
    inputs: Path,
) -> tuple[Path, dict, dict]:
    engineering_registry = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
    resolved = resolve_bucket_gate_map(
        crosswalk,
        bucket_plan,
        engineering_registry=engineering_registry,
        fail_on_gap=True,
    )
    gate_ids = list(resolved["required_engineering_gate_ids"])
    if not gate_ids:
        fail("BOUND_GOLDEN_ENGINEERING_GATE_SET_EMPTY")

    eng_root = inputs / "engineering"
    eng_root.mkdir(parents=True, exist_ok=True)
    authorizations = []
    gate_to_auth = {}
    for offset in range(0, len(gate_ids), 3):
        chunk = gate_ids[offset:offset + 3]
        idx = offset // 3 + 1
        auth_id = f"MATH-ENG-AUTH-BOUND-{idx:02d}"
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "request_id": f"MATH-ENG-REQ-BOUND-{idx:02d}",
            "scope_kind": "ENGINEERING_GATE",
            "scope_refs": chunk,
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "owner_decision_ref": None,
        }
        manifest = resolve_manifest(request, engineering_registry)
        closure = compile_closure(request, manifest, engineering_registry)
        binding = compile_binding(request, manifest, closure, "CANONICAL_DOMAIN_REGISTRY")
        bundle_dir = eng_root / f"auth-{idx:02d}"
        request_path = bundle_dir / "request.json"; write(request_path, request)
        manifest_path = bundle_dir / "manifest.json"; write(manifest_path, manifest)
        binding_path = bundle_dir / "binding.json"; write(binding_path, binding)
        authorizations.append({
            "authorization_id": auth_id,
            "engineering_request_ref": str(request_path.resolve()),
            "engineering_manifest_ref": str(manifest_path.resolve()),
            "engineering_binding_ref": str(binding_path.resolve()),
        })
        for gate in chunk:
            gate_to_auth[gate] = auth_id

    bucket_rows = {row["bucket_id"]: row for row in resolved["bucket_gate_map"]}
    subtopic_gate_map = []
    for bucket in bucket_plan["buckets"]:
        bid = bucket["bucket_id"]
        gates = bucket_rows[bid]["engineering_gate_ids"]
        if not gates:
            fail("BOUND_GOLDEN_ENGINEERING_BUCKET_WITHOUT_GATE", bid)
        subtopic_gate_map.append({
            "subtopic_id": bucket_sid[bid],
            "gate_bindings": [
                {"engineering_gate_id": gate, "authorization_ref": gate_to_auth[gate]}
                for gate in gates
            ],
        })

    admission = {
        "schema_version": "2.0.0",
        "subject": "MATHEMATICS",
        "admission_id": "MATH-ENG-DOMAIN-ADMISSION-BOUND-" + legacy.production_digest(registry["registry_id"])[:12].upper(),
        "domain_registry_ref": str((inputs / "domain_registry.json").resolve()),
        "authorizations": authorizations,
        "subtopic_gate_map": subtopic_gate_map,
    }
    admission_path = inputs / "engineering_domain_admission.json"
    write(admission_path, admission)
    write(inputs / "engineering_projection_coverage.json", resolved)
    return admission_path, admission, resolved


def run_bound(core1_path: Path, study_model_path: Path, core2_path: Path, out: Path) -> dict:
    expected = legacy.load(legacy.EXPECTED)
    full_core1 = legacy.load(core1_path)
    full_study = legacy.load(study_model_path)
    full_core2 = legacy.load(core2_path)
    out.mkdir(parents=True, exist_ok=True)
    inputs = out / "inputs"; inputs.mkdir(exist_ok=True)

    crosswalk = load_crosswalk(DEFAULT_CROSSWALK)
    if crosswalk["crosswalk_id"] != expected["engineering_crosswalk_ref"]:
        fail("BOUND_GOLDEN_ENGINEERING_CROSSWALK_REF_DRIFT")

    pck = legacy.c1base.load_pck_assets(legacy.c1base.DEFAULT_PCK_INDEX)
    families = legacy.c1base.load_problem_families(legacy.c1base.DEFAULT_FAMILY_INDEX)
    full_bucket_plan = legacy.synthesize_bucket_plan(full_core1, full_study, pck, families)
    full_coverage = resolve_bucket_gate_map(crosswalk, full_bucket_plan, fail_on_gap=False)
    actual_full_gaps = sorted(row["capability_ref"] for row in full_coverage["required_engineering_gaps"])
    expected_full_gaps = sorted(expected["full_mixed_expected_engineering_gap_capability_refs"])
    if actual_full_gaps != expected_full_gaps:
        fail("BOUND_GOLDEN_FULL_MIXED_ENGINEERING_GAP_DRIFT", f"actual={actual_full_gaps};expected={expected_full_gaps}")
    full_coverage["claim"] = "FULL_MIXED_CORPUS_NOT_ENGINEERING_RELEASE_READY" if actual_full_gaps else "FULL_MIXED_CORPUS_ENGINEERING_COVERED"
    write(out / "full_mixed_engineering_coverage_audit.json", full_coverage)

    core1, study, core2, projection_receipt = _project_authority_inputs(full_core1, full_study, full_core2, expected)
    projected_core1_path = inputs / "projected_core1_study_plan.json"; write(projected_core1_path, core1)
    projected_study_path = inputs / "projected_learner_study_model.json"; write(projected_study_path, study)
    projected_core2_path = inputs / "projected_core2_plan.json"; write(projected_core2_path, core2)
    write(inputs / "engineering_bound_projection_receipt.json", projection_receipt)

    preflight_bucket_plan = legacy.synthesize_bucket_plan(core1, study, pck, families)
    projection_coverage = resolve_bucket_gate_map(crosswalk, preflight_bucket_plan, fail_on_gap=True)
    if projection_coverage["required_status"] != "COVERED":
        fail("BOUND_GOLDEN_ENGINEERING_PROJECTION_NOT_COVERED")

    current_bucket_subtopics = bucket_subtopics
    bucket_sid, cap_sid, q_sid = current_bucket_subtopics(preflight_bucket_plan)
    answers, answer_refs = legacy.build_answer_contracts(core2)
    generation_spec = legacy.build_generation_spec(preflight_bucket_plan, core1, bucket_sid)
    validate_generation_spec(generation_spec)
    registry = legacy.build_registry(core1, core2, preflight_bucket_plan, bucket_sid, cap_sid, q_sid, answer_refs)

    registry_path = inputs / "domain_registry.json"; write(registry_path, registry)
    gen_path = inputs / "generation_spec.json"; write(gen_path, generation_spec)
    answers_path = inputs / "core2_answer_contracts.json"; write(answers_path, answers)
    intent_path = inputs / "core2a_intent.json"; write(intent_path, {
        "requested_stage": "CORE2A", "purpose": expected["purpose"],
        "scope": {"scope_type": "TOPIC", "scope_ref": "engineering-covered-bound-projection"},
    })
    admission_path, admission, engineering_projection = _build_engineering_admission(
        preflight_bucket_plan, bucket_sid, registry, crosswalk, inputs
    )

    c1a_out = out / "core1a"
    legacy.run_cli(legacy.MATH / "Core1A" / "engine" / "realize_math_core1a.py", [
        "--core1-plan", str(projected_core1_path), "--study-model", str(projected_study_path),
        "--generation-spec", str(gen_path), "--domain-registry", str(registry_path),
        "--engineering-admission", str(admission_path), "--out-dir", str(c1a_out),
    ])
    emitted_bucket_plan = legacy.load(c1a_out / "core1a_bucket_plan.json")
    if emitted_bucket_plan["bucket_plan_id"] != preflight_bucket_plan["bucket_plan_id"] or emitted_bucket_plan["plan_digest"] != preflight_bucket_plan["plan_digest"]:
        fail("BOUND_GOLDEN_CORE1A_PREFLIGHT_DRIFT")
    c1a_book = legacy.load(c1a_out / "core1a_textbook_manuscript.json")
    c1a_receipt = legacy.load(c1a_out / "core1a_governance_receipt.json")
    if c1a_receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT" or c1a_receipt.get("engineering_custody", {}).get("status") != "BOUND":
        fail("BOUND_GOLDEN_CORE1A_NOT_READY")

    spec_by_bucket = {row["bucket_id"]: row for row in generation_spec["core1_buckets"]}
    book_by_bucket = {row["bucket_id"]: row for row in c1a_book["buckets"]}
    c1b_receipts = []
    c1b_root = out / "core1b"
    for i, bucket in enumerate(emitted_bucket_plan["buckets"], 1):
        source = legacy.core1b_input(bucket, book_by_bucket[bucket["bucket_id"]], spec_by_bucket[bucket["bucket_id"]], c1a_book["core1a_book_id"], i)
        source_path = c1b_root / f"bucket-{i:02d}-input.json"; write(source_path, source)
        plan_path = c1b_root / f"bucket-{i:02d}-plan.json"
        receipt_path = c1b_root / f"bucket-{i:02d}-governance.json"
        legacy.run_cli(legacy.MATH / "Core1B" / "engine" / "compile_core1b.py", [
            "--input", str(source_path), "--out", str(plan_path), "--domain-registry", str(registry_path),
            "--engineering-admission", str(admission_path), "--governance-out", str(receipt_path),
        ])
        receipt = legacy.load(receipt_path)
        if receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT" or receipt.get("engineering_custody", {}).get("status") != "BOUND":
            fail("BOUND_GOLDEN_CORE1B_NOT_READY", receipt["receipt_id"])
        c1b_receipts.append(receipt_path)

    source_bundle_spec = {
        "subject": "MATHEMATICS",
        "items": [
            {
                "role": "CORE1A_BUCKET_PLAN", "path": str(c1a_out / "core1a_bucket_plan.json"),
                "required": True, "release_state": "PRODUCTION", "digest_kind": "EMBEDDED_AUTHORITY_DIGEST",
                "ref_fields": ["bucket_plan_id"], "digest_fields": ["plan_digest"],
            },
            {
                "role": "CORE2_PLAN", "path": str(projected_core2_path),
                "required": True, "release_state": "PRODUCTION", "digest_kind": "EMBEDDED_AUTHORITY_DIGEST",
                "ref_fields": ["plan_id"], "digest_fields": ["plan_digest"],
            },
        ],
    }
    bundle_spec_path = inputs / "source_bundle_spec.json"; write(bundle_spec_path, source_bundle_spec)
    bundle_path = inputs / "source_bundle.json"
    legacy.run_cli(legacy.MATH / "ProductionKits" / "common" / "engine" / "build_source_bundle.py", ["--spec", str(bundle_spec_path), "--out", str(bundle_path)])

    c2a_out = out / "core2a"
    legacy.run_cli(legacy.MATH / "ProductionKits" / "Core2A" / "engine" / "run_core2a_kit.py", [
        "--intent", str(intent_path), "--generation-spec", str(gen_path), "--source-bundle", str(bundle_path),
        "--core1a-bucket-plan", str(c1a_out / "core1a_bucket_plan.json"), "--core2-plan", str(projected_core2_path),
        "--core2-answer-contracts", str(answers_path), "--domain-registry", str(registry_path),
        "--engineering-admission", str(admission_path), "--out-dir", str(c2a_out),
    ])
    c2a_blueprint = legacy.load(c2a_out / "core2a_product_blueprint.json")
    c2a_receipt = legacy.load(c2a_out / "core2a_governance_receipt.json")
    if c2a_receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT" or c2a_receipt.get("engineering_custody", {}).get("status") != "BOUND":
        fail("BOUND_GOLDEN_CORE2A_NOT_READY")

    c2b_source = legacy.core2b_input(c2a_blueprint, generation_spec)
    c2b_root = out / "core2b"; c2b_root.mkdir(exist_ok=True)
    c2b_input_path = c2b_root / "input.json"; write(c2b_input_path, c2b_source)
    c2b_plan_path = c2b_root / "plan.json"; c2b_receipt_path = c2b_root / "governance.json"
    legacy.run_cli(legacy.MATH / "Core2B" / "engine" / "compile_core2b.py", [
        "--input", str(c2b_input_path), "--out", str(c2b_plan_path), "--domain-registry", str(registry_path),
        "--engineering-admission", str(admission_path), "--governance-out", str(c2b_receipt_path),
    ])
    c2b_receipt = legacy.load(c2b_receipt_path)
    if c2b_receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT" or c2b_receipt.get("engineering_custody", {}).get("status") != "BOUND":
        fail("BOUND_GOLDEN_CORE2B_NOT_READY")

    release_out = out / "release"
    receipt_args = ["--receipt", str(c1a_out / "core1a_governance_receipt.json")]
    for path in c1b_receipts:
        receipt_args += ["--receipt", str(path)]
    receipt_args += ["--receipt", str(c2a_out / "core2a_governance_receipt.json"), "--receipt", str(c2b_receipt_path)]
    legacy.run_cli(legacy.MATH_BLUEPRINT / "engine" / "release_product_governance.py", [
        "--registry", str(registry_path), "--engineering-admission", str(admission_path),
        *receipt_args, "--out-dir", str(release_out),
    ])

    gate = legacy.load(release_out / "product_release_gate.json")
    coverage = legacy.load(release_out / "core_coverage_ledger.json")
    similarity = legacy.load(release_out / "cross_core_similarity_audit.json")
    governance = legacy.load(release_out / "product_governance_audit.json")
    if gate.get("status") != "PASS":
        fail("BOUND_GOLDEN_RELEASE_GATE_FAILED")
    if gate.get("engineering_domain_authorization", {}).get("status") != "BOUND":
        fail("BOUND_GOLDEN_ENGINEERING_RELEASE_AUTHORIZATION_MISSING")
    if gate.get("frozen_source_custody", {}).get("status") != "PASS" or gate.get("canonical_answer_custody", {}).get("status") != "PASS":
        fail("BOUND_GOLDEN_SOURCE_OR_ANSWER_CUSTODY_FAILED")
    if coverage.get("coverage_scope") != "FULL_REGISTRY":
        fail("BOUND_GOLDEN_COVERAGE_NOT_FULL")
    if set(similarity["coverage_declaration"]["stage_pairs"]) != set(expected["required_stage_pairs"]):
        fail("BOUND_GOLDEN_STAGE_PAIR_COVERAGE_DRIFT")
    if {row["stage"] for row in governance["purpose_audits"]} != set(expected["required_stages"]):
        fail("BOUND_GOLDEN_PURPOSE_STAGE_COVERAGE_DRIFT")

    summary = {
        "golden_id": expected["golden_id"],
        "status": "PASS",
        "full_mixed_engineering_status": full_coverage["claim"],
        "full_mixed_engineering_gap_capability_refs": actual_full_gaps,
        "engineering_bound_projection": expected["engineering_bound_projection"],
        "projection_receipt_ref": projection_receipt["projection_digest"],
        "engineering_crosswalk_ref": crosswalk["crosswalk_id"],
        "engineering_admission_ref": admission["admission_id"],
        "engineering_authorized_direct_gate_ids": gate["engineering_domain_authorization"]["authorized_direct_gate_count"],
        "registry_ref": registry["registry_id"],
        "registry_asset_count": len(registry["assets"]),
        "core1a_receipt_ref": c1a_receipt["receipt_id"],
        "core1b_receipt_refs": [legacy.load(path)["receipt_id"] for path in c1b_receipts],
        "core2a_receipt_ref": c2a_receipt["receipt_id"],
        "core2b_receipt_ref": c2b_receipt["receipt_id"],
        "source_question_count": len(core2["pages"]),
        "bucket_count": len(emitted_bucket_plan["buckets"]),
        "cross_core_comparison_count": similarity["coverage_declaration"]["candidate_pair_count"],
        "release_checks": expected["required_release_checks"],
        "engineering_projection_coverage": engineering_projection,
        "release_gate": gate,
    }
    write(out / "bound_producer_release_summary.json", summary)
    return summary
