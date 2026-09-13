#!/usr/bin/env python3
"""Production NCERT entrypoint for the Chemistry Core1A/Core2A pipeline.

The normal LearnerProduct runner is intentionally usable with synthetic and
process-golden authority. This wrapper adds the extra condition needed for a
real NCERT topic run: the live C-J coverage closure must be bound to one of the
independently corroborated PR #346 topic denominators *before* Core1A/Core2A
synthesis starts.

No learner HTML is reverse-engineered into semantic authority here. The caller
must still provide real C-F/C-G/C-H/C-I/C-J artifacts. This wrapper only proves
that those artifacts close against the production retained denominator.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))

import ncert_production_baselines as production  # noqa: E402
import run_chemistry_learner_product as runner  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _require_binding(run):
    if not production.validate_optional_run_binding_shape(run):
        raise ValueError("CHEM_LP_PRODUCTION_BASELINE_REQUIRED")


def _write_binding(out_dir: Path, baseline: dict, bundle: dict) -> None:
    payload = {
        "status": "PASS",
        "production_baseline": baseline,
        "legacy_workbench_source_bundle": bundle,
        "source_bundle_note": (
            "The PR #346 HTML/CSV bundle is archival benchmark evidence. "
            "Production semantic authority must come from the supplied C-F/C-G/C-H/C-I/C-J artifacts."
        ),
    }
    (out_dir / "production_baseline_binding.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _annotate_stage_evidence(out_dir: Path, baseline: dict) -> None:
    path = out_dir / "learner_product_stage_evidence.json"
    if not path.exists():
        return
    doc = load(path)
    stages = doc.get("stages", [])
    if len(stages) < 2 or stages[1].get("stage") != "FREEZE_SOURCE_DENOMINATOR":
        raise ValueError("CHEM_LP_PRODUCTION_STAGE_EVIDENCE_DRIFT")
    stage = stages[1]
    refs = list(stage.get("evidence_refs") or [])
    if baseline["baseline_ref"] not in refs:
        refs.append(baseline["baseline_ref"])
    stage["evidence_refs"] = refs
    counters = dict(stage.get("counters") or {})
    counters["PRODUCTION_RETAINED_DENOMINATOR"] = baseline["retained_questions"]
    counters["PRODUCTION_FREEZE_STATE"] = baseline["freeze_state"]
    stage["counters"] = counters
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def execute_production(run, study_model, core1, representations, core2, closure, out_dir: Path, semantic_only: bool = False):
    runner.validate_foundation(run)
    _require_binding(run)
    baseline = production.assert_run_binding(run, closure)
    if baseline is None:  # defensive; _require_binding already forbids this
        raise ValueError("CHEM_LP_PRODUCTION_BASELINE_REQUIRED")

    if semantic_only:
        package, files = runner.execute_semantic_pipeline(
            run, study_model, core1, representations, core2, closure, out_dir
        )
    else:
        package, files = runner.execute_full_pipeline(
            run, study_model, core1, representations, core2, closure, out_dir
        )

    bundle = production.inspect_legacy_source_bundle()
    _write_binding(out_dir, baseline, bundle)
    _annotate_stage_evidence(out_dir, baseline)
    return package, files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-manifest", type=Path, required=True)
    ap.add_argument("--study-model", type=Path, required=True)
    ap.add_argument("--core1-plan", type=Path, required=True)
    ap.add_argument("--representation-bundle", type=Path, required=True)
    ap.add_argument("--core2-plan", type=Path, required=True)
    ap.add_argument("--coverage-closure", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--semantic-only", action="store_true")
    args = ap.parse_args()

    package, _ = execute_production(
        load(args.run_manifest),
        load(args.study_model),
        load(args.core1_plan),
        load(args.representation_bundle),
        load(args.core2_plan),
        load(args.coverage_closure),
        args.out_dir,
        semantic_only=args.semantic_only,
    )
    print(json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
