#!/usr/bin/env python3
"""Canonical Chemistry Core (1A) / Core (2A) learner-product entrypoint.

Foundation implementation: validates the run contract, exact policy IDs, run
manifest digest and challenge-registry requirement. It intentionally does not
pretend downstream production adapters exist. A normal generation invocation
fails closed until those stages are implemented; --validate-only proves the
foundation contract and writes machine-readable stage evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover - exercised by environment
    raise SystemExit("jsonschema>=4.20 is required for Chemistry LearnerProduct") from exc


HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]

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


def canonical_digest(obj: dict[str, Any]) -> str:
    payload = dict(obj)
    payload.pop("run_digest", None)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_foundation(run: dict[str, Any]) -> dict[str, Any]:
    schema = load_json(LP_ROOT / "contracts/chemistry-learner-product-run.schema.json")
    jsonschema.Draft202012Validator(schema).validate(run)

    if run["execution_sequence"] != EXECUTION_SEQUENCE:
        raise ValueError("CHEM_LP_EXECUTION_SEQUENCE_DRIFT")

    expected_digest = canonical_digest(run)
    if run["run_digest"] != expected_digest:
        raise ValueError(
            f"CHEM_LP_RUN_DIGEST_MISMATCH expected={expected_digest} actual={run['run_digest']}"
        )

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
            "CORE2_HINT_PRETEACH_CLOSURE",
            "CORE2A_REALIZATION",
            "CHALLENGE_CHEMISTRY_VALIDATION",
            "ANSWER_CLOSURE",
            "RENDERED_VISUAL_USABILITY",
            "HUMAN_REVIEW_GATES",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    run = load_json(args.run_manifest)
    evidence = validate_foundation(run)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "validated_run_manifest.json").write_text(
        json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (args.out_dir / "learner_product_stage_evidence.json").write_text(
        json.dumps({"stages": [evidence]}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if args.validate_only:
        print(json.dumps(evidence, indent=2))
        return

    raise SystemExit(
        "CHEM_LP_DOWNSTREAM_STAGE_NOT_IMPLEMENTED: foundation contract validated; "
        "production adapters C-LP-01..C-LP-25 must be implemented before generation."
    )


if __name__ == "__main__":
    main()
