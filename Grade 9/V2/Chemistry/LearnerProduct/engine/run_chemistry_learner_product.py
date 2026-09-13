#!/usr/bin/env python3
"""Canonical Chemistry Core (1A) / Core (2A) learner-product entrypoint.

The runner has two honest operating boundaries:

* --validate-only validates the immutable run contract and policy bindings.
* --semantic-only executes the governed semantic learner-product chain through
  C-LP-21 (answer closure), writes durable machine-readable outputs, and stops
  before page rendering. C-LP-22..25 remain explicitly pending.

A normal production invocation executes the same semantic chain and then fails
closed at the unimplemented render boundary rather than pretending the product
is publication-ready.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema>=4.20 is required for Chemistry LearnerProduct") from exc

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent

sys.path.insert(0, str(CHEM_ROOT / "Core1A" / "engine"))
sys.path.insert(0, str(CHEM_ROOT / "Core2A" / "engine"))

from build_chemistry_core1a_bucket_plan import build_bucket_plan  # noqa: E402
from build_chemistry_core1a_build_state import compile_build_state  # noqa: E402
from build_chemistry_core1a_manuscript import build_manuscript  # noqa: E402
from build_chemistry_core2a_source import build_source_plan  # noqa: E402
from build_chemistry_core2a_challenges import build_challenge_plan  # noqa: E402

EXECUTION_SEQUENCE = [
    "VALIDATE_UPSTREAM_BINDINGS",
    "FREEZE_SOURCE_DENOMINATOR",
    "CLASSIFY_SOURCE_INTEGRITY",
    "SYNTHESIZE_CORE1A_BUCKETS",
    "BIND_LEARNER_TREATMENT",
    "DECOMPOSE_LEARNING_ATOMS",
    "BUILD_REPRESENTATION_SEQUENCE",
    "BUILD_PROBLEM_FAMILIES",
    "CLOSE_CORE2_HINT_PRETEACH",
    "REALIZE_CORE1A",
    "MAP_CORE2_TO_CORE1A",
    "REALIZE_SOURCE_CORE2A_ITEMS",
    "SELECT_CHALLENGE_TARGETS",
    "GENERATE_CHALLENGE_CANDIDATES",
    "VALIDATE_CHEMISTRY",
    "VALIDATE_TAUGHT_SCOPE",
    "VALIDATE_NEAR_COPY",
    "BIND_PROVENANCE",
    "AUTHOR_STAGED_HELP",
    "AUTHOR_QUICK_CHECK",
    "AUTHOR_FULL_WORKING",
    "VALIDATE_ANSWER_CLOSURE",
    "RENDER_LEARNER_PRODUCTS",
    "VISUAL_PREFLIGHT",
    "FINAL_AUDIT",
    "FREEZE_HANDOFF",
]

POLICY_FILES = {
    "core1a_execution_policy": ("policies/chemistry-core1a-execution-policy.json", "CHEM-CORE1A-EXECUTION-v1"),
    "core2a_execution_policy": ("policies/chemistry-core2a-execution-policy.json", "CHEM-CORE2A-EXECUTION-v1"),
    "learner_language_policy": ("policies/chemistry-learner-language-policy.json", "CHEM-LEARNER-LANGUAGE-v1"),
    "question_citation_policy": ("policies/chemistry-question-citation-policy.json", "CHEM-QUESTION-CITATION-v1"),
    "competitive_challenge_policy": ("policies/chemistry-competitive-challenge-policy.json", "CHEM-COMPETITIVE-CHALLENGE-v1"),
    "answer_path_policy": ("policies/chemistry-answer-path-policy.json", "CHEM-ANSWER-PATH-v1"),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def object_digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def canonical_digest(obj: dict[str, Any]) -> str:
    payload = copy.deepcopy(obj)
    payload.pop("run_digest", None)
    return object_digest(payload)


def validate_foundation(run: dict[str, Any]) -> dict[str, Any]:
    schema = load_json(LP_ROOT / "contracts/chemistry-learner-product-run.schema.json")
    jsonschema.Draft202012Validator(schema).validate(run)
    if run["execution_sequence"] != EXECUTION_SEQUENCE:
        raise ValueError("CHEM_LP_EXECUTION_SEQUENCE_DRIFT")
    expected_digest = canonical_digest(run)
    if run["run_digest"] != expected_digest:
        raise ValueError(f"CHEM_LP_RUN_DIGEST_MISMATCH expected={expected_digest} actual={run['run_digest']}")

    loaded_policies: dict[str, dict[str, Any]] = {}
    for manifest_key, (relative_path, expected_id) in POLICY_FILES.items():
        policy = load_json(LP_ROOT / relative_path)
        if policy.get("policy_id") != expected_id:
            raise ValueError(f"CHEM_LP_POLICY_FILE_ID_MISMATCH:{manifest_key}")
        if run["policy_refs"].get(manifest_key) != expected_id:
            raise ValueError(f"CHEM_LP_POLICY_BINDING_MISMATCH:{manifest_key}")
        loaded_policies[manifest_key] = policy

    if run["requested_products"]["core2a_challenges"]:
        inputs = run["inputs"]
        if not inputs.get("competitive_registry_ref") or not inputs.get("competitive_registry_digest"):
            raise ValueError("CHEM_LP_CHALLENGE_REGISTRY_REQUIRED")

    return {
        "status": "PASS",
        "stage": "VALIDATE_UPSTREAM_BINDINGS",
        "run_id": run["run_id"],
        "run_digest": run["run_digest"],
        "contract_version": run["contract_version"],
        "execution_stage_count": len(EXECUTION_SEQUENCE),
        "policy_ids": {k: v["policy_id"] for k, v in loaded_policies.items()},
        "not_established": [
            "UPSTREAM_FILE_DIGEST_RECOMPUTATION",
            "CORE1A_BUCKET_SYNTHESIS",
            "CORE1A_MANUSCRIPT_REALIZATION",
            "CORE2_HINT_PRETEACH_CLOSURE",
            "CORE2A_REALIZATION",
            "CHALLENGE_CHEMISTRY_VALIDATION",
            "ANSWER_CLOSURE",
            "RENDERED_VISUAL_USABILITY",
            "HUMAN_REVIEW_GATES",
        ],
    }


def _verify_input(run, obj, input_prefix, ref_field, digest_field):
    expected_ref = run["inputs"][input_prefix + "_ref"]
    expected_digest = run["inputs"][input_prefix + "_digest"]
    if obj.get(ref_field) != expected_ref:
        raise ValueError(f"CHEM_LP_UPSTREAM_REF_MISMATCH:{input_prefix}")
    if obj.get(digest_field) != expected_digest:
        raise ValueError(f"CHEM_LP_UPSTREAM_DIGEST_MISMATCH:{input_prefix}")


def _load_authority_bundle():
    return {
        "problem_families": load_json(CHEM_ROOT / "ReasoningSemantics/registry/chemistry-problem-family-registry.json"),
        "core1a_synthesis": load_json(CHEM_ROOT / "Core1A/policies/chemistry-core1a-bucket-synthesis-policy.json"),
        "core2a_source": load_json(CHEM_ROOT / "Core2A/policies/chemistry-core2a-source-realization-policy.json"),
        "core2a_challenge": load_json(CHEM_ROOT / "Core2A/policies/chemistry-core2a-challenge-realization-policy.json"),
        "core2a_execution": load_json(LP_ROOT / "policies/chemistry-core2a-execution-policy.json"),
        "competitive": load_json(LP_ROOT / "policies/chemistry-competitive-challenge-policy.json"),
        "language": load_json(LP_ROOT / "policies/chemistry-learner-language-policy.json"),
        "citation": load_json(LP_ROOT / "policies/chemistry-question-citation-policy.json"),
        "answer": load_json(LP_ROOT / "policies/chemistry-answer-path-policy.json"),
        "archetypes": load_json(LP_ROOT / "registry/chemistry-competitive-archetype-registry.json"),
    }


def _stage(stage, status="PASS", refs=None, counters=None, reason=None):
    return {
        "stage": stage,
        "status": status,
        "evidence_refs": refs or [],
        "counters": counters or {},
        "reason": reason,
    }


def _answer_closure(manuscript, source_plan, challenge_plan, audit_id):
    core1_questions = [i for b in manuscript["buckets"] for i in b["practice_items"]]
    source_items = source_plan["items"] if source_plan else []
    challenge_items = challenge_plan["items"] if challenge_plan else []
    open_items = [i for i in core1_questions if i["answer_path"]["answer_path_kind"] == "OPEN_RUBRIC"]
    objective_items = source_items + challenge_items
    quick = sum(i["answer_path"].get("quick_check") is not None for i in objective_items)
    full = sum(i["answer_path"].get("full_working") is not None for i in objective_items)
    rubrics = sum((i["answer_path"].get("expected_response_rubric") or {}).get("criteria") is not None for i in open_items)
    if quick != len(objective_items) or full != len(objective_items):
        raise ValueError("CHEM_LP_ANSWER_CLOSURE_FAILED:objective")
    if rubrics != len(open_items):
        raise ValueError("CHEM_LP_ANSWER_CLOSURE_FAILED:open")
    out = {
        "audit_id": audit_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "core1a_manuscript_ref": manuscript["manuscript_id"],
        "core1a_manuscript_digest": manuscript["manuscript_digest"],
        "core2a_source_plan_ref": source_plan["plan_id"] if source_plan else None,
        "core2a_source_plan_digest": source_plan["plan_digest"] if source_plan else None,
        "core2a_challenge_plan_ref": challenge_plan["plan_id"] if challenge_plan else None,
        "core2a_challenge_plan_digest": challenge_plan["plan_digest"] if challenge_plan else None,
        "counts": {
            "learner_questions_total": len(core1_questions) + len(objective_items),
            "objective_questions_total": len(objective_items),
            "quick_checks_total": quick,
            "full_workings_total": full,
            "open_questions_total": len(open_items),
            "expected_response_rubrics_total": rubrics,
        },
        "status": "PASS",
        "audit_digest": "",
    }
    payload = copy.deepcopy(out)
    payload.pop("audit_digest")
    out["audit_digest"] = object_digest(payload)
    return out


def execute_semantic_pipeline(run, study_model, core1, representations, core2, closure, out_dir: Path):
    foundation = validate_foundation(run)
    _verify_input(run, study_model, "learner_study_model", "study_model_id", "study_model_digest")
    _verify_input(run, core1, "core1_plan", "plan_id", "plan_digest")
    _verify_input(run, representations, "representation_bundle", "bundle_id", "bundle_digest")
    _verify_input(run, core2, "core2_plan", "plan_id", "plan_digest")
    _verify_input(run, closure, "coverage_closure", "closure_id", "closure_digest")
    if closure.get("summary", {}).get("status") != "PASS" or closure.get("summary", {}).get("blocking_failures") != 0:
        raise ValueError("CHEM_LP_COVERAGE_CLOSURE_NOT_PASS")

    auth = _load_authority_bundle()
    if run["requested_products"]["core2a_challenges"]:
        registry = auth["archetypes"]
        if run["inputs"]["competitive_registry_ref"] != registry["registry_id"]:
            raise ValueError("CHEM_LP_CHALLENGE_REGISTRY_REF_MISMATCH")
        if run["inputs"]["competitive_registry_digest"] != object_digest(registry):
            raise ValueError("CHEM_LP_CHALLENGE_REGISTRY_DIGEST_MISMATCH")

    tag = run["run_id"].split("-")[-1]
    bucket_plan = build_bucket_plan(
        study_model, core1, representations, core2, auth["problem_families"], auth["core1a_synthesis"],
        f"CHEM-C1A-BP-LPR-{tag}",
    )
    build_state = compile_build_state(bucket_plan, f"CHEM-C1A-BUILD-STATE-LPR-{tag}")
    manuscript = build_manuscript(
        bucket_plan, core1, auth["language"], auth["answer"], f"CHEM-C1A-MANUSCRIPT-LPR-{tag}",
    )

    source_plan = None
    if run["requested_products"]["core2a_source"]:
        source_plan = build_source_plan(
            core2, bucket_plan, auth["problem_families"], auth["core2a_execution"], auth["core2a_source"],
            auth["language"], auth["citation"], auth["answer"], f"CHEM-C2A-SOURCE-LPR-{tag}",
        )
    elif run["requested_products"]["core2a_challenges"]:
        raise ValueError("CHEM_LP_CHALLENGES_REQUIRE_SOURCE_LANE")

    challenge_plan = None
    if run["requested_products"]["core2a_challenges"]:
        challenge_plan = build_challenge_plan(
            source_plan, bucket_plan, auth["problem_families"], auth["core2a_execution"], auth["competitive"],
            auth["archetypes"], auth["core2a_challenge"], auth["language"], auth["citation"], auth["answer"],
            f"CHEM-C2A-CHALLENGE-LPR-{tag}",
        )

    closure_audit = _answer_closure(manuscript, source_plan, challenge_plan, f"CHEM-LP-ANSWER-CLOSURE-{tag}")

    external_summary = closure.get("external_matrix", {}).get("summary", {})
    qc_counts = Counter(page.get("source_qc_status", "UNKNOWN") for page in core2["pages"])
    stages = [
        _stage("VALIDATE_UPSTREAM_BINDINGS", refs=[run["run_id"], closure["closure_id"]]),
        _stage("FREEZE_SOURCE_DENOMINATOR", refs=[closure["external_matrix_ref"]], counters={
            "TOTAL_SCANNED": external_summary.get("candidate_total", 0),
            "ELIGIBLE_IN_TOPIC": external_summary.get("eligible_total", 0),
            "PLACED_UNIQUE": external_summary.get("placed_unique_total", 0),
            "MISSING": external_summary.get("missing_total", 0),
            "DUPLICATE_PRIMARY": external_summary.get("duplicate_primary_total", 0),
        }),
        _stage("CLASSIFY_SOURCE_INTEGRITY", refs=[core2["plan_id"]], counters=dict(sorted(qc_counts.items()))),
        _stage("SYNTHESIZE_CORE1A_BUCKETS", refs=[bucket_plan["plan_id"]], counters={"buckets": len(bucket_plan["buckets"])}),
        _stage("BIND_LEARNER_TREATMENT", refs=[study_model["study_model_id"], bucket_plan["plan_id"]]),
        _stage("DECOMPOSE_LEARNING_ATOMS", refs=[bucket_plan["plan_id"]], counters={"atoms": sum(len(b["learning_atoms"]) for b in bucket_plan["buckets"])}),
        _stage("BUILD_REPRESENTATION_SEQUENCE", refs=[representations["bundle_id"], bucket_plan["plan_id"]]),
        _stage("BUILD_PROBLEM_FAMILIES", refs=[auth["problem_families"]["registry_id"], bucket_plan["plan_id"]]),
        _stage("CLOSE_CORE2_HINT_PRETEACH", refs=[bucket_plan["plan_id"]], counters={"reveals": bucket_plan["coverage"]["hint_reveals_bound"]}),
        _stage("REALIZE_CORE1A", refs=[manuscript["manuscript_id"]], counters={"practice_questions": manuscript["summary"]["practice_question_count"]}),
        _stage("MAP_CORE2_TO_CORE1A", refs=[bucket_plan["plan_id"], core2["plan_id"]]),
        _stage("REALIZE_SOURCE_CORE2A_ITEMS", refs=[source_plan["plan_id"]] if source_plan else [], counters={"items": len(source_plan["items"]) if source_plan else 0}),
        _stage("SELECT_CHALLENGE_TARGETS", refs=[challenge_plan["plan_id"]] if challenge_plan else [], counters={"generated": len(challenge_plan["items"]) if challenge_plan else 0}),
        _stage("GENERATE_CHALLENGE_CANDIDATES", refs=[challenge_plan["plan_id"]] if challenge_plan else []),
        _stage("VALIDATE_CHEMISTRY", refs=[challenge_plan["plan_id"]] if challenge_plan else [], counters={"passed": challenge_plan["summary"]["independent_chemistry_checks_passed"] if challenge_plan else 0}),
        _stage("VALIDATE_TAUGHT_SCOPE", refs=[bucket_plan["plan_id"], challenge_plan["plan_id"]] if challenge_plan else [bucket_plan["plan_id"]]),
        _stage("VALIDATE_NEAR_COPY", refs=[challenge_plan["plan_id"]] if challenge_plan else [], counters={"passed": challenge_plan["summary"]["near_copy_checks_passed"] if challenge_plan else 0}),
        _stage("BIND_PROVENANCE", refs=[source_plan["plan_id"]] + ([challenge_plan["plan_id"]] if challenge_plan else []) if source_plan else []),
        _stage("AUTHOR_STAGED_HELP", refs=[source_plan["plan_id"]] + ([challenge_plan["plan_id"]] if challenge_plan else []) if source_plan else []),
        _stage("AUTHOR_QUICK_CHECK", refs=[closure_audit["audit_id"]], counters={"quick_checks": closure_audit["counts"]["quick_checks_total"]}),
        _stage("AUTHOR_FULL_WORKING", refs=[closure_audit["audit_id"]], counters={"full_workings": closure_audit["counts"]["full_workings_total"]}),
        _stage("VALIDATE_ANSWER_CLOSURE", refs=[closure_audit["audit_id"]], counters=copy.deepcopy(closure_audit["counts"])),
    ]
    for stage in EXECUTION_SEQUENCE[22:]:
        stages.append(_stage(stage, status="PENDING_RENDER_BOUNDARY", reason="Semantic-only execution stops before page rendering; this is not a release pass."))

    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "core1a_bucket_plan.json": bucket_plan,
        "core1a_build_state.json": build_state,
        "core1a_manuscript.json": manuscript,
        "core2a_source_plan.json": source_plan,
        "core2a_challenge_plan.json": challenge_plan,
        "answer_closure_audit.json": closure_audit,
        "learner_product_stage_evidence.json": {"run_id": run["run_id"], "stages": stages},
    }
    for name, obj in files.items():
        if obj is not None:
            (out_dir / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    package = {
        "package_id": f"CHEM-LP-SEMANTIC-{tag}",
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "run_ref": run["run_id"],
        "run_digest": run["run_digest"],
        "semantic_complete_through": "VALIDATE_ANSWER_CLOSURE",
        "render_pending": True,
        "outputs": {
            "core1a_bucket_plan_ref": bucket_plan["plan_id"],
            "core1a_bucket_plan_digest": bucket_plan["plan_digest"],
            "core1a_manuscript_ref": manuscript["manuscript_id"],
            "core1a_manuscript_digest": manuscript["manuscript_digest"],
            "core2a_source_plan_ref": source_plan["plan_id"] if source_plan else None,
            "core2a_source_plan_digest": source_plan["plan_digest"] if source_plan else None,
            "core2a_challenge_plan_ref": challenge_plan["plan_id"] if challenge_plan else None,
            "core2a_challenge_plan_digest": challenge_plan["plan_digest"] if challenge_plan else None,
            "answer_closure_audit_ref": closure_audit["audit_id"],
            "answer_closure_audit_digest": closure_audit["audit_digest"],
        },
        "package_digest": "",
    }
    payload = copy.deepcopy(package)
    payload.pop("package_digest")
    package["package_digest"] = object_digest(payload)
    (out_dir / "semantic_package_manifest.json").write_text(json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return package, files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--semantic-only", action="store_true")
    parser.add_argument("--study-model", type=Path)
    parser.add_argument("--core1-plan", type=Path)
    parser.add_argument("--representation-bundle", type=Path)
    parser.add_argument("--core2-plan", type=Path)
    parser.add_argument("--coverage-closure", type=Path)
    args = parser.parse_args()

    run = load_json(args.run_manifest)
    evidence = validate_foundation(run)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "validated_run_manifest.json").write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.validate_only:
        (args.out_dir / "learner_product_stage_evidence.json").write_text(
            json.dumps({"stages": [evidence]}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(evidence, indent=2))
        return

    required_paths = [args.study_model, args.core1_plan, args.representation_bundle, args.core2_plan, args.coverage_closure]
    if any(path is None for path in required_paths):
        raise SystemExit("CHEM_LP_SEMANTIC_INPUT_FILES_REQUIRED")

    package, _ = execute_semantic_pipeline(
        run,
        load_json(args.study_model),
        load_json(args.core1_plan),
        load_json(args.representation_bundle),
        load_json(args.core2_plan),
        load_json(args.coverage_closure),
        args.out_dir,
    )
    if args.semantic_only:
        print(json.dumps(package, indent=2))
        return
    raise SystemExit(
        "CHEM_LP_RENDER_STAGE_NOT_IMPLEMENTED: semantic chain passed through C-LP-21; "
        "C-LP-22..C-LP-25 remain pending and no release claim is authorized."
    )


if __name__ == "__main__":
    main()
