#!/usr/bin/env python3
"""Build the Chemistry learner-product rendered process golden.

This uses the repository synthetic mixed-Chemistry cold-start fixture to exercise
Core1A/Core2A end to end through C-LP-25. It is a process/render regression
fixture only: it is not an NCERT product, official-question corpus, or human
release candidate.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
GOLDEN = HERE.parent
LP = GOLDEN.parents[1]
CHEM = LP.parent
REPO = CHEM.parents[2]
sys.path.insert(0, str(LP / "engine"))
sys.path.insert(0, str(CHEM / "ColdStart" / "engine"))

import run_chemistry_learner_product as runner  # noqa: E402
from chemistry_cold_start_runner import run_cold_start  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def make_run(internals):
    registry = load(LP / "registry" / "chemistry-competitive-archetype-registry.json")
    manifest = {
        "run_id": "CHEM-LPR-fedcba9876543210",
        "contract_version": "1.0.0",
        "subject": "CHEMISTRY",
        "inputs": {
            "learner_study_model_ref": internals["study_model"]["study_model_id"],
            "learner_study_model_digest": internals["study_model"]["study_model_digest"],
            "core1_plan_ref": internals["core1"]["plan_id"],
            "core1_plan_digest": internals["core1"]["plan_digest"],
            "representation_bundle_ref": internals["representations"]["bundle_id"],
            "representation_bundle_digest": internals["representations"]["bundle_digest"],
            "core2_plan_ref": internals["core2"]["plan_id"],
            "core2_plan_digest": internals["core2"]["plan_digest"],
            "coverage_closure_ref": internals["closure"]["closure_id"],
            "coverage_closure_digest": internals["closure"]["closure_digest"],
            "competitive_registry_ref": registry["registry_id"],
            "competitive_registry_digest": runner.object_digest(registry),
        },
        "policy_refs": {
            "core1a_execution_policy": "CHEM-CORE1A-EXECUTION-v1",
            "core2a_execution_policy": "CHEM-CORE2A-EXECUTION-v1",
            "learner_language_policy": "CHEM-LEARNER-LANGUAGE-v1",
            "question_citation_policy": "CHEM-QUESTION-CITATION-v1",
            "competitive_challenge_policy": "CHEM-COMPETITIVE-CHALLENGE-v1",
            "answer_path_policy": "CHEM-ANSWER-PATH-v1"
        },
        "execution_sequence": list(runner.EXECUTION_SEQUENCE),
        "requested_products": {"core1a": True, "core2a_source": True, "core2a_challenges": True},
        "outputs": {
            "core1a_bucket_plan_ref": None,
            "core1a_manuscript_ref": None,
            "core2a_source_plan_ref": None,
            "core2a_challenge_plan_ref": None,
            "answer_closure_audit_ref": None,
            "artifact_manifest_ref": None,
            "handoff_manifest_ref": None
        },
        "run_digest": "0" * 64
    }
    manifest["run_digest"] = runner.canonical_digest(manifest)
    return manifest


def build(out_dir: Path):
    fixtures = CHEM / "AssessmentIntake" / "fixtures"
    _, internals = run_cold_start(
        load(fixtures / "mixed-chemistry-source.fixture.json"),
        load(fixtures / "mixed-chemistry-question-set.fixture.json"),
        load(fixtures / "mixed-chemistry-external-corpus.fixture.json"),
        load(fixtures / "mixed-chemistry-topic-scope.fixture.json"),
        repo_root=REPO,
        run_id="CHEM-LP-RENDER-PROCESS-GOLDEN",
    )
    manifest = make_run(internals)
    package, files = runner.execute_full_pipeline(
        manifest,
        internals["study_model"], internals["core1"], internals["representations"],
        internals["core2"], internals["closure"], out_dir,
    )
    declaration = {
        "fixture_scope": "PROCESS_GOLDEN_USING_SYNTHETIC_COLD_START_AUTHORITY",
        "production_claim": False,
        "official_source_claim": False,
        "human_release_claim": False,
        "complete_through": package["complete_through"],
        "machine_status": package["machine_status"],
        "release_authorized": package["release_authorized"],
        "human_gates": package["human_gates"],
        "core1a_pdf": files["render_manifest.json"]["core1a"]["pdf"],
        "core2a_pdf": files["render_manifest.json"]["core2a"]["pdf"],
    }
    (out_dir / "GOLDEN_DECLARATION.json").write_text(json.dumps(declaration, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return package


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    package = build(args.out_dir)
    print(json.dumps(package, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
