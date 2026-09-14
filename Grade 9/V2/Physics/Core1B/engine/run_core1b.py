from __future__ import annotations

import argparse
import json
from pathlib import Path

from core1b_common import (
    build_independent_evidence,
    build_release_receipt,
    validate_atom_registry,
    validate_unit,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--learner-profile", default="PHY-LS-P20")
    parser.add_argument("--problem-family", default="PF-PROJECTILE-VERTICAL-EVENT")
    parser.add_argument("--teaching-receipt", default="T-PHY-M2D-EVENT-001")
    args = parser.parse_args()

    unit = load_json(Path(args.unit))
    registry = load_json(Path(args.registry))
    validate_atom_registry(registry)
    validate_unit(unit, registry)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    evidence = build_independent_evidence(unit, args.learner_profile, args.problem_family)
    evidence_path = out / "learner-evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    receipt = build_release_receipt(
        unit,
        evidence_ref=str(evidence_path),
        teaching_receipt_ref=args.teaching_receipt,
        problem_family_ref=args.problem_family,
    )
    (out / "release-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("PASS Core1B golden")


if __name__ == "__main__":
    main()
