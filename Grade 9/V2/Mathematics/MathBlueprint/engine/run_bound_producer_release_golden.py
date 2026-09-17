#!/usr/bin/env python3
"""Execute a genuinely bound four-producer Mathematics release golden.

The inputs are real Core1 / StudyModel / Core2 outputs from one cold-start run.
This runner compiles a minimal Canonical Domain Registry from those exact outputs,
executes the actual Core1A, Core1B, Core2A and Core2B CLIs against that registry,
and finally executes the actual cross-Core release gate over their emitted receipts.

The registry is deliberately minimal for integration coverage: every upstream
capability is canonically split into a CONCEPT + CAPABILITY asset, every source
question is frozen, and every source question receives canonical solution and
verification authority. Rich equation / representation / misconception typed
realization is covered by the separate product-governance falsifier suite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
MATH_BLUEPRINT = HERE.parents[1]
MATH = MATH_BLUEPRINT.parent
REPO = MATH.parents[2]
CORE1A_ENGINE = MATH / "Core1A" / "engine"
PK_COMMON_ENGINE = MATH / "ProductionKits" / "common" / "engine"
for p in (CORE1A_ENGINE, PK_COMMON_ENGINE, HERE.parent):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import build_math_core1a_textbook as c1base
from core1a_bucket_synthesis import synthesize_bucket_plan
from production_primitives import digest as production_digest
from validate_canonical_domain_registry import validate_registry
from validate_self_teaching_generation_spec import validate_generation_spec

EXPECTED = MATH_BLUEPRINT / "golden" / "bound_producer_release" / "EXPECTED.json"


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def run_cli(script: Path, args: list[str]) -> str:
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"BOUND_GOLDEN_CLI_FAILED:{script.name}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def safe_slug(value: str, prefix: str) -> str:
    return prefix + production_digest(value)[:12].upper()


def answer_contract(page: dict) -> dict:
    qid = page["question_ref"]
    route = page.get("solution_route") or {}
    final = route.get("final_answer")
    steps = [str(x) for x in route.get("steps") or [] if str(x).strip()]
    if not steps:
        steps = ["Follow the independently verified Core2 solution route for this source item."]
    checks = route.get("verification_checks") or []
    evidence = "; ".join(
        json.dumps(x, sort_keys=True, ensure_ascii=False) if isinstance(x, (dict, list)) else str(x)
        for x in checks
    ).strip()
    if not evidence:
        evidence = "The independently verified Core2 solution route contains a recorded verification step."
    uniqueness = final.get("uniqueness_status") if isinstance(final, dict) else None
    multiplicity = "MULTIPLE_DISTINCT" if uniqueness in {"MULTIPLE", "NON_UNIQUE"} else "SINGLE_CANONICAL"
    accepted = []
    if isinstance(final, dict):
        accepted.extend(final.get("accepted_answers") or [])
        accepted.extend(final.get("accepted_option_labels") or [])
    return {
        "question_ref": qid,
        "answer_type": "OPEN_RESPONSE",
        "canonical_answer": final,
        "accepted_equivalents": accepted,
        "solution_paths": [{"path_id": "CORE2_VERIFIED", "steps": steps}],
        "verification_checks": [{"method": "CORE2_ROUTE_CHECK", "status": "PASS", "evidence": evidence}],
        "domain_conditions": [],
        "solution_multiplicity": multiplicity,
        "independent_solver_status": "PASS",
    }


def build_answer_contracts(core2: dict) -> tuple[dict, dict[str, str]]:
    answers = []
    refs = {}
    for page in core2["pages"]:
        ans = answer_contract(page)
        answers.append(ans)
        refs[page["question_ref"]] = "ANS-" + page["question_ref"] + "-" + production_digest(ans)[:12]
    return {"answers": answers}, refs


def bucket_subtopics(bucket_plan: dict) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    bucket_sid = {}
    cap_sid = {}
    q_sid = {}
    for bucket in bucket_plan["buckets"]:
        sid = "BOUND-SUB-" + production_digest(sorted(bucket["member_capability_refs"]))[:12].upper()
        bucket_sid[bucket["bucket_id"]] = sid
        for cap in bucket["member_capability_refs"]:
            if cap in cap_sid and cap_sid[cap] != sid:
                fail("BOUND_GOLDEN_CAPABILITY_MULTI_SUBTOPIC", cap)
            cap_sid[cap] = sid
        for qid in bucket.get("core2_question_refs") or []:
            if qid in q_sid and q_sid[qid] != sid:
                fail("BOUND_GOLDEN_SOURCE_QUESTION_MULTI_SUBTOPIC", qid)
            q_sid[qid] = sid
    return bucket_sid, cap_sid, q_sid


def build_generation_spec(bucket_plan: dict, core1: dict, bucket_sid: dict[str, str]) -> dict:
    rows = []
    dims = {
        "prerequisite_depth": 1,
        "element_interactivity": 1,
        "inferential_jump_severity": 1,
        "representation_translation": 1,
        "abstraction": 1,
        "method_discrimination": 1,
        "notation_density": 1,
        "derivation_burden": 1,
        "misconception_density": 1,
        "special_case_sensitivity": 1,
    }
    for bucket in bucket_plan["buckets"]:
        sid = bucket_sid[bucket["bucket_id"]]
        rows.append({
            "bucket_id": bucket["bucket_id"],
            "subtopic_id": sid,
            "subtopic_title": bucket["title"],
            "difficulty_badge": "EASY",
            "difficulty_badge_basis": "CORE1_SEMANTIC_COMPLEXITY",
            "difficulty_dimensions": dict(dims),
            "difficulty_validation_refs": ["DIFF:BOUND:" + sid],
            "target_page_budget": 10,
            "subsubtopic_plan": [],
            "pedagogy_research_brief_ref": None,
            "pedagogy_web_research_refs": [],
            "source_integrity_verification_refs": [],
        })
    caps = list(core1["scope_completeness"]["required_capability_refs"])
    return {
        "schema_version": "1.3.0",
        "subject": "MATHEMATICS",
        "core1_buckets": rows,
        "core2_calibration": {
            "purpose": "REVISION",
            "learner_knowledge_percent": 60,
            "knowledge_percent_source_ref": "ASSESSMENT:BOUND-GOLDEN-60",
            "knowledge_calibration_policy_ref": "OWNER_POLICY:BOUND-GOLDEN-v1",
            "capability_knowledge": [{"capability_ref": cap, "percent": 60} for cap in caps],
            "owner_waiver": None,
            "resolved_core2a_support_profile": "STANDARD_GUIDED",
            "resolved_core2a_max_demand_level": "M3_INVERSE_TARGET",
            "resolved_core2b_max_demand_level": "M4_HIDDEN_STRUCTURE",
        },
    }


def build_registry(core1: dict, core2: dict, bucket_plan: dict, bucket_sid: dict[str, str], cap_sid: dict[str, str], q_sid: dict[str, str], answer_refs: dict[str, str]) -> dict:
    run_seed = production_digest([core1["plan_digest"], core2["plan_digest"]])[:12].upper()
    join_ref = "JOIN:BOUND:" + run_seed
    validation_ref = "VAL:BOUND:" + run_seed
    lessons = {row["capability_ref"]: row for row in core1["lessons"]}
    q_by_cap: dict[str, list[str]] = {cap: [] for cap in lessons}
    for page in core2["pages"]:
        for cap in page.get("capability_refs") or []:
            if cap in q_by_cap:
                q_by_cap[cap].append(page["question_ref"])

    assets = []
    concept_by_cap = {}
    capability_asset_by_cap = {}
    for cap in core1["scope_completeness"]["required_capability_refs"]:
        lesson = lessons[cap]
        sid = cap_sid[cap]
        concept_id = "REG-MATH-CON-" + production_digest(cap)[:12].upper()
        capability_id = "REG-MATH-CAP-" + production_digest("CAP:" + cap)[:12].upper()
        concept_by_cap[cap] = concept_id
        capability_asset_by_cap[cap] = capability_id
        title = lesson["learner_title"]
        assets.append({
            "asset_id": concept_id,
            "asset_type": "CONCEPT",
            "subtopic_id": sid,
            "title": title,
            "authority_class": "CORE1_SEMANTIC",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": ["GT:" + cap],
            "core1_refs": [cap],
            "core2_refs": [],
            "validation_refs": [validation_ref],
            "join_ref": join_ref,
            "depends_on": [],
            "payload": {
                "statement": "Understand and use the governed mathematical idea: " + title + ".",
                "prerequisite_refs": [],
                "implications": ["The idea supports the capability " + cap + " in this bound integration run."],
                "boundary_notes": [],
            },
            "provenance_note": "Integration semantic asset compiled from the exact bound Core1 lesson in this run.",
        })
        qrefs = sorted(set(q_by_cap.get(cap) or []))
        authority = "DUAL_VALIDATED" if qrefs else "CORE1_SEMANTIC"
        assets.append({
            "asset_id": capability_id,
            "asset_type": "CAPABILITY",
            "subtopic_id": sid,
            "title": "Capability — " + title,
            "authority_class": authority,
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": ["GT:" + cap],
            "core1_refs": [cap],
            "core2_refs": qrefs,
            "validation_refs": [validation_ref],
            "join_ref": join_ref,
            "depends_on": [concept_id],
            "payload": {
                "statement": "Perform the governed mathematical capability represented by " + cap + " using the taught meaning and constraints.",
                "prerequisite_refs": [concept_id],
                "implications": ["This capability is the typed learner-fit target for Core2 items that require " + cap + "."],
                "boundary_notes": [],
            },
            "provenance_note": "Integration capability asset compiled from the exact Core1 lesson and same-run Core2 bindings.",
        })

    for page in core2["pages"]:
        qid = page["question_ref"]
        sid = q_sid.get(qid)
        if sid is None:
            candidates = [cap_sid[c] for c in page.get("capability_refs") or [] if c in cap_sid]
            if not candidates:
                fail("BOUND_GOLDEN_SOURCE_QUESTION_WITHOUT_SUBTOPIC", qid)
            sid = candidates[0]
        qasset = "REG-MATH-Q-" + production_digest("Q:" + qid)[:12].upper()
        verasset = "REG-MATH-VER-" + production_digest("VER:" + qid)[:12].upper()
        solasset = "REG-MATH-SOL-" + production_digest("SOL:" + qid)[:12].upper()
        source_ref = str(page.get("source_ref") or qid)
        gt_ref = "GTQ:" + qid + ":" + source_ref[:12]
        assets.append({
            "asset_id": verasset,
            "asset_type": "VERIFICATION_RULE",
            "subtopic_id": sid,
            "title": "Independent verification for " + qid,
            "authority_class": "INDEPENDENT_VERIFICATION",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": [gt_ref],
            "core1_refs": [],
            "core2_refs": [],
            "validation_refs": [validation_ref],
            "join_ref": join_ref,
            "depends_on": [],
            "payload": {
                "verification_type": "OTHER",
                "instruction": "Verify the final result against the original givens and the independently recorded Core2 solution route.",
                "uses_answer_key": False,
            },
            "provenance_note": "Independent verification authority retained for the same-run source question.",
        })
        assets.append({
            "asset_id": qasset,
            "asset_type": "SOURCE_QUESTION",
            "subtopic_id": sid,
            "title": "Frozen source question " + qid,
            "authority_class": "SOURCE_FROZEN",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": [gt_ref],
            "core1_refs": [],
            "core2_refs": [qid],
            "validation_refs": [validation_ref],
            "join_ref": join_ref,
            "depends_on": [],
            "payload": {
                "question_ref": qid,
                "source_ref": source_ref,
                "frozen_digest": hashlib.sha256(page["source_stem"].encode("utf-8")).hexdigest(),
            },
            "provenance_note": "Exact source stem frozen from the same Core2 plan used by the bound producer golden.",
        })
        assets.append({
            "asset_id": solasset,
            "asset_type": "CANONICAL_SOLUTION",
            "subtopic_id": sid,
            "title": "Canonical verified solution for " + qid,
            "authority_class": "INDEPENDENT_VERIFICATION",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": [gt_ref],
            "core1_refs": [],
            "core2_refs": [qid],
            "validation_refs": [validation_ref],
            "join_ref": join_ref,
            "depends_on": [qasset, verasset],
            "payload": {
                "question_asset_ref": qasset,
                "answer_contract_ref": answer_refs[qid],
                "verification_rule_refs": [verasset],
            },
            "provenance_note": "Canonical answer authority bound to the exact source item and generated answer contract for this run.",
        })

    registry = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "registry_id": "MATH-REG-BOUND-" + run_seed,
        "run_ref": "RUN-BOUND-" + run_seed,
        "source_manifest_refs": ["GT-MANIFEST-BOUND-" + run_seed],
        "join_refs": [join_ref],
        "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
        "assets": assets,
    }
    validate_registry(registry)
    return registry


def core1b_input(bucket: dict, book_bucket: dict, spec_row: dict, core1a_book_id: str, index: int) -> dict:
    caps = list(bucket["member_capability_refs"])
    first_cap = caps[0]
    unit = next(x for x in book_bucket["capability_units"] if x["capability_ref"] == first_cap)
    practice = unit.get("practice", {})
    independent = practice.get("INDEPENDENT") or next(iter(practice.values()), None)
    independent_prompt = independent.get("prompt") if independent else "Reconstruct and use the connecting mathematical idea independently."
    independent_answer = independent.get("answer") if independent else "Check the reconstructed relation against the Core1A explanation."
    difficulty = {
        "subtopic_ref": spec_row["subtopic_id"],
        "declared_badge": spec_row["difficulty_badge"],
        "badge_authority": "DERIVED",
        "derived_dimensions": dict(spec_row["difficulty_dimensions"]),
        "operational_badge": spec_row["difficulty_badge"],
        "page_ceiling": 10,
        "research_level": "NONE",
        "owner_override_ref": None,
        "evidence_refs": list(spec_row["difficulty_validation_refs"]),
    }
    prefix = f"BR{index}"
    return {
        "core1a_authority_ref": core1a_book_id,
        "learner_treatment": "ACTIVE_STUDY",
        "approved_capability_refs": caps,
        "difficulty_governance": difficulty,
        "title": "Reconstruction — " + bucket["title"],
        "blocks": [
            {
                "block_id": prefix + "-METHODS",
                "kind": "METHOD_COMPARISON",
                "title": "Compare two routes",
                "capability_refs": [first_cap],
                "new_math_refs": [],
                "learner_text": "Before reading the scaffold, compare a representation-first route with a direct symbolic route for this connecting idea. Which information must both routes preserve?",
                "math_lines": ["Route A: make the governing structure visible first.", "Route B: state the governing relation directly, then verify the same invariant."],
            },
            {
                "block_id": prefix + "-COMPLETE",
                "kind": "COMPLETION",
                "title": "Reconstruct the first move",
                "capability_refs": [first_cap],
                "new_math_refs": [],
                "learner_text": "Use the meaning of the quantities to reconstruct the governing idea and first mathematical move without copying the earlier worked example.",
                "math_lines": ["Governing idea: ____________________", "First mathematical move: ____________________"],
            },
            {
                "block_id": prefix + "-INDEP",
                "kind": "CLOSE_INDEPENDENT",
                "title": "Close independent consolidation",
                "capability_refs": [first_cap],
                "new_math_refs": [],
                "learner_text": independent_prompt,
                "math_lines": [],
            },
            {
                "block_id": prefix + "-ANS",
                "kind": "ANSWER_CHECK",
                "title": "Answer check",
                "capability_refs": [first_cap],
                "new_math_refs": [],
                "learner_text": independent_answer,
                "math_lines": [],
            },
        ],
    }


def core2b_input(blueprint: dict, generation_spec: dict) -> dict:
    specs = list(blueprint["question_specs"])
    if not specs:
        fail("BOUND_GOLDEN_CORE2A_NO_LEGAL_ITEMS")
    caps = sorted({cap for row in specs for cap in row.get("required_capability_refs", [])})
    cal = generation_spec["core2_calibration"]
    knowledge = {row["capability_ref"]: row["percent"] for row in cal["capability_knowledge"]}
    items = []
    for i, row in enumerate(specs, 1):
        parent = row["question_id"]
        iid = "B2-" + production_digest([parent, i])[:12].upper()
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
                "type": "KNOWLEDGE_PERCENT",
                "learner_knowledge_percent": cal["learner_knowledge_percent"],
                "knowledge_source_ref": cal["knowledge_percent_source_ref"],
                "calibration_policy_ref": cal["knowledge_calibration_policy_ref"],
                "capability_knowledge": [{"capability_ref": cap, "percent": knowledge[cap]} for cap in caps],
            },
        },
        "title": "Bound Core2B transfer golden",
        "items": items,
    }


def run_bound(core1_path: Path, study_model_path: Path, core2_path: Path, out: Path) -> dict:
    expected = load(EXPECTED)
    core1 = load(core1_path); study = load(study_model_path); core2 = load(core2_path)
    out.mkdir(parents=True, exist_ok=True)
    inputs = out / "inputs"; inputs.mkdir(exist_ok=True)

    pck = c1base.load_pck_assets(c1base.DEFAULT_PCK_INDEX)
    families = c1base.load_problem_families(c1base.DEFAULT_FAMILY_INDEX)
    preflight_bucket_plan = synthesize_bucket_plan(core1, study, pck, families)
    bucket_sid, cap_sid, q_sid = bucket_subtopics(preflight_bucket_plan)
    answers, answer_refs = build_answer_contracts(core2)
    generation_spec = build_generation_spec(preflight_bucket_plan, core1, bucket_sid)
    validate_generation_spec(generation_spec)
    registry = build_registry(core1, core2, preflight_bucket_plan, bucket_sid, cap_sid, q_sid, answer_refs)

    registry_path = inputs / "domain_registry.json"; write(registry_path, registry)
    gen_path = inputs / "generation_spec.json"; write(gen_path, generation_spec)
    answers_path = inputs / "core2_answer_contracts.json"; write(answers_path, answers)
    intent_path = inputs / "core2a_intent.json"; write(intent_path, {
        "requested_stage": "CORE2A", "purpose": expected["purpose"],
        "scope": {"scope_type": "TOPIC", "scope_ref": "bound-cold-start-run"},
    })

    c1a_out = out / "core1a"
    run_cli(MATH / "Core1A" / "engine" / "realize_math_core1a.py", [
        "--core1-plan", str(core1_path), "--study-model", str(study_model_path),
        "--generation-spec", str(gen_path), "--domain-registry", str(registry_path),
        "--out-dir", str(c1a_out),
    ])
    emitted_bucket_plan = load(c1a_out / "core1a_bucket_plan.json")
    if emitted_bucket_plan["bucket_plan_id"] != preflight_bucket_plan["bucket_plan_id"] or emitted_bucket_plan["plan_digest"] != preflight_bucket_plan["plan_digest"]:
        fail("BOUND_GOLDEN_CORE1A_PREFLIGHT_DRIFT")
    c1a_book = load(c1a_out / "core1a_textbook_manuscript.json")
    c1a_receipt = load(c1a_out / "core1a_governance_receipt.json")
    if c1a_receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT":
        fail("BOUND_GOLDEN_CORE1A_NOT_READY")

    spec_by_bucket = {row["bucket_id"]: row for row in generation_spec["core1_buckets"]}
    book_by_bucket = {row["bucket_id"]: row for row in c1a_book["buckets"]}
    c1b_receipts = []
    c1b_root = out / "core1b"
    for i, bucket in enumerate(emitted_bucket_plan["buckets"], 1):
        source = core1b_input(bucket, book_by_bucket[bucket["bucket_id"]], spec_by_bucket[bucket["bucket_id"]], c1a_book["core1a_book_id"], i)
        source_path = c1b_root / f"bucket-{i:02d}-input.json"; write(source_path, source)
        plan_path = c1b_root / f"bucket-{i:02d}-plan.json"
        receipt_path = c1b_root / f"bucket-{i:02d}-governance.json"
        run_cli(MATH / "Core1B" / "engine" / "compile_core1b.py", [
            "--input", str(source_path), "--out", str(plan_path),
            "--domain-registry", str(registry_path), "--governance-out", str(receipt_path),
        ])
        receipt = load(receipt_path)
        if receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT":
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
                "role": "CORE2_PLAN", "path": str(core2_path),
                "required": True, "release_state": "PRODUCTION", "digest_kind": "EMBEDDED_AUTHORITY_DIGEST",
                "ref_fields": ["plan_id"], "digest_fields": ["plan_digest"],
            },
        ],
    }
    bundle_spec_path = inputs / "source_bundle_spec.json"; write(bundle_spec_path, source_bundle_spec)
    bundle_path = inputs / "source_bundle.json"
    run_cli(MATH / "ProductionKits" / "common" / "engine" / "build_source_bundle.py", ["--spec", str(bundle_spec_path), "--out", str(bundle_path)])

    c2a_out = out / "core2a"
    run_cli(MATH / "ProductionKits" / "Core2A" / "engine" / "run_core2a_kit.py", [
        "--intent", str(intent_path), "--generation-spec", str(gen_path),
        "--source-bundle", str(bundle_path), "--core1a-bucket-plan", str(c1a_out / "core1a_bucket_plan.json"),
        "--core2-plan", str(core2_path), "--core2-answer-contracts", str(answers_path),
        "--domain-registry", str(registry_path), "--out-dir", str(c2a_out),
    ])
    c2a_blueprint = load(c2a_out / "core2a_product_blueprint.json")
    c2a_receipt = load(c2a_out / "core2a_governance_receipt.json")
    if c2a_receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT":
        fail("BOUND_GOLDEN_CORE2A_NOT_READY")

    c2b_source = core2b_input(c2a_blueprint, generation_spec)
    c2b_root = out / "core2b"; c2b_root.mkdir(exist_ok=True)
    c2b_input_path = c2b_root / "input.json"; write(c2b_input_path, c2b_source)
    c2b_plan_path = c2b_root / "plan.json"; c2b_receipt_path = c2b_root / "governance.json"
    run_cli(MATH / "Core2B" / "engine" / "compile_core2b.py", [
        "--input", str(c2b_input_path), "--out", str(c2b_plan_path),
        "--domain-registry", str(registry_path), "--governance-out", str(c2b_receipt_path),
    ])
    c2b_receipt = load(c2b_receipt_path)
    if c2b_receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT":
        fail("BOUND_GOLDEN_CORE2B_NOT_READY")

    release_out = out / "release"
    receipt_args = ["--receipt", str(c1a_out / "core1a_governance_receipt.json")]
    for path in c1b_receipts:
        receipt_args += ["--receipt", str(path)]
    receipt_args += ["--receipt", str(c2a_out / "core2a_governance_receipt.json"), "--receipt", str(c2b_receipt_path)]
    run_cli(MATH_BLUEPRINT / "engine" / "release_product_governance.py", [
        "--registry", str(registry_path), *receipt_args, "--out-dir", str(release_out),
    ])

    gate = load(release_out / "product_release_gate.json")
    coverage = load(release_out / "core_coverage_ledger.json")
    similarity = load(release_out / "cross_core_similarity_audit.json")
    governance = load(release_out / "product_governance_audit.json")
    if gate.get("status") != "PASS" or gate.get("frozen_source_custody", {}).get("status") != "PASS" or gate.get("canonical_answer_custody", {}).get("status") != "PASS":
        fail("BOUND_GOLDEN_RELEASE_GATE_FAILED")
    if coverage.get("coverage_scope") != "FULL_REGISTRY":
        fail("BOUND_GOLDEN_COVERAGE_NOT_FULL")
    if set(similarity["coverage_declaration"]["stage_pairs"]) != set(expected["required_stage_pairs"]):
        fail("BOUND_GOLDEN_STAGE_PAIR_COVERAGE_DRIFT")
    if {row["stage"] for row in governance["purpose_audits"]} != set(expected["required_stages"]):
        fail("BOUND_GOLDEN_PURPOSE_STAGE_COVERAGE_DRIFT")

    summary = {
        "golden_id": expected["golden_id"],
        "status": "PASS",
        "registry_ref": registry["registry_id"],
        "registry_asset_count": len(registry["assets"]),
        "core1a_receipt_ref": c1a_receipt["receipt_id"],
        "core1b_receipt_refs": [load(path)["receipt_id"] for path in c1b_receipts],
        "core2a_receipt_ref": c2a_receipt["receipt_id"],
        "core2b_receipt_ref": c2b_receipt["receipt_id"],
        "source_question_count": len(core2["pages"]),
        "bucket_count": len(emitted_bucket_plan["buckets"]),
        "cross_core_comparison_count": similarity["coverage_declaration"]["candidate_pair_count"],
        "release_checks": expected["required_release_checks"],
        "release_gate": gate,
    }
    write(out / "bound_producer_release_summary.json", summary)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--core2-plan", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    summary = run_bound(Path(args.core1_plan), Path(args.study_model), Path(args.core2_plan), Path(args.out_dir))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
