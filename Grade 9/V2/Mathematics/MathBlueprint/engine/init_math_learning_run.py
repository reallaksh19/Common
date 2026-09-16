#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import load, seal_learning_run, validate_ground_truth_manifest

PURPOSES = {"FIRST_STUDY", "CONSOLIDATION", "REVISION", "COMPETITIVE_EXAM"}
MODES = {"STARTER", "PRACTICE", "REVISION", "COMPETITION"}


def build_run(
    manifest: dict,
    *,
    learner_prior_percent: int | None = None,
    learning_purpose: str | None = None,
    product_mode: str | None = None,
    owner_override_refs: list[str] | None = None,
) -> dict:
    validate_ground_truth_manifest(manifest)
    if learner_prior_percent is not None and not 0 <= learner_prior_percent <= 100:
        raise ValueError("LEARNER_PRIOR_PERCENT_OUT_OF_RANGE")
    if learning_purpose is not None and learning_purpose not in PURPOSES:
        raise ValueError("LEARNING_PURPOSE_UNKNOWN:" + learning_purpose)
    if product_mode is not None and product_mode not in MODES:
        raise ValueError("PRODUCT_MODE_UNKNOWN:" + product_mode)

    run = {
        "run_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "control_plane": {
            "learner_prior_percent": learner_prior_percent,
            "learning_purpose": learning_purpose,
            "product_mode": product_mode,
            "owner_override_refs": sorted(set(owner_override_refs or [])),
        },
        "current_state": "GT_READY",
        "state_history": [
            {
                "sequence": 0,
                "state": "GT_READY",
                "reason_code": "GROUND_TRUTH_MANIFEST_VALIDATED"
            }
        ],
        "routing_ref": None,
        "bundles": [],
        "publication_ref": None,
        "audit_ref": None,
        "run_digest": "",
    }
    return seal_learning_run(run)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ground-truth", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--learner-prior-percent", type=int)
    ap.add_argument("--learning-purpose", choices=sorted(PURPOSES))
    ap.add_argument("--product-mode", choices=sorted(MODES))
    ap.add_argument("--owner-override-ref", action="append", default=[])
    args = ap.parse_args()

    run = build_run(
        load(args.ground_truth),
        learner_prior_percent=args.learner_prior_percent,
        learning_purpose=args.learning_purpose,
        product_mode=args.product_mode,
        owner_override_refs=args.owner_override_ref,
    )
    Path(args.out).write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "run_id": run["run_id"],
        "current_state": run["current_state"],
        "run_digest": run["run_digest"],
    }, indent=2))


if __name__ == "__main__":
    main()
