#!/usr/bin/env python3
"""Canonical Core1A/Core2A learner-product entrypoint.

This entrypoint makes the ordered contract executable before all downstream
stage adapters exist. It validates the run manifest and policy bindings, prints
the exact execution sequence, and fails closed for generation until every stage
runner is wired. Future implementations must extend STAGE_RUNNERS rather than
creating alternate undocumented entrypoints.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
LP = HERE.parents[1]
SCHEMA = LP / "contracts" / "math-learner-product-run.schema.json"

EXPECTED_POLICIES = {
    "core1a_execution_policy": "MATH-CORE1A-EXECUTION-v1",
    "core2a_execution_policy": "MATH-CORE2A-EXECUTION-v1",
    "learner_language_policy": "MATH-LEARNER-LANGUAGE-v1",
    "question_citation_policy": "MATH-QUESTION-CITATION-v1",
    "competitive_challenge_policy": "MATH-COMPETITIVE-CHALLENGE-v1",
}

# Stage runners must be installed here in the canonical order. Empty is
# intentional today: the contract exists before an executable Core2A compiler.
STAGE_RUNNERS: dict[str, object] = {}


def fail(code: str, detail: str = "") -> None:
    raise SystemExit(f"{code}:{detail}" if detail else code)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(path: Path) -> dict:
    manifest = load(path)
    schema = load(SCHEMA)
    jsonschema.validate(manifest, schema)
    for key, expected in EXPECTED_POLICIES.items():
        actual = manifest["policy_refs"].get(key)
        if actual != expected:
            fail("LEARNER_PRODUCT_POLICY_BINDING_DRIFT", f"{key}:{actual}!={expected}")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-manifest", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args()

    manifest = validate_manifest(Path(args.run_manifest))
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    sequence = manifest["execution_sequence"]
    (out / "validated_execution_sequence.json").write_text(
        json.dumps({"run_id": manifest["run_id"], "execution_sequence": sequence}, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.validate_only:
        print(json.dumps({"status": "PASS", "run_id": manifest["run_id"], "stages": sequence}, indent=2))
        return

    missing = [stage for stage in sequence if stage not in STAGE_RUNNERS]
    if missing:
        fail("LEARNER_PRODUCT_STAGE_RUNNERS_NOT_IMPLEMENTED", ",".join(missing))

    # Future implementation: execute each runner strictly in sequence and write
    # the governed artifact manifest. Alternative stage orders are forbidden.


if __name__ == "__main__":
    main()
