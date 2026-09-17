#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402

DISCOVERY_REF = ROOT / "policy" / "physics-engineering-discovery-catalog.pr383.v1.json"
SCHEMA_REF = ROOT / "contracts" / "physics-architecture-observation.schema.json"
WORK_ENERGY_IDS = {
    "PHY-WORK-ENERGY-POWER",
    "PHY-ENERGY-CONSERVATION-LAW",
    "PHY-WEP-VARIABLE-FORCE",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_observation() -> dict[str, Any]:
    registry = build_registry()
    discovery = load(DISCOVERY_REF)
    rows = list(discovery["discovered_subtopics"])
    dispositions = [row["disposition"] for row in rows]

    work_energy = []
    for row in rows:
        if row["discovery_gate_id"] not in WORK_ENERGY_IDS:
            continue
        curriculum = row["curriculum"]
        work_energy.append({
            "discovery_gate_id": row["discovery_gate_id"],
            "disposition": row["disposition"],
            "v3_gate_ids": list(row["v3_gate_ids"]),
            "curriculum_grade": int(curriculum["grade"]),
            "curriculum_chapter": str(curriculum["chapter"]),
        })
    work_energy.sort(key=lambda row: row["discovery_gate_id"])

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_class": "DERIVED_PHYSICS_ARCHITECTURE_OBSERVATION",
        "authority": "DERIVED_OBSERVABILITY_ONLY",
        "engineering_authorization": "NOT_EVALUATED",
        "publication_authorization": "NOT_IMPLIED",
        "canonical_v3": {
            "registry_id": registry["registry_id"],
            "registry_digest": digest(registry),
            "gate_count": len(registry["gates"]),
            "gate_ids": sorted(gate["subtopic_id"] for gate in registry["gates"]),
        },
        "discovery_coverage": {
            "catalog_id": discovery["catalog_id"],
            "catalog_digest": digest(discovery),
            "discovered_subtopic_count": len(rows),
            "exact_v3_count": dispositions.count("EXACT_V3_ID"),
            "mapped_v3_count": dispositions.count("MAPPED_V3"),
            "migration_required_count": dispositions.count("MIGRATION_REQUIRED"),
        },
        "work_energy_reconciliation": work_energy,
        "invariants": {
            "discovery_cannot_authorize": True,
            "observation_cannot_authorize": True,
            "parallel_engineering_authority_prohibited": True,
            "v3_is_canonical_physics_technical_authority": True,
        },
        "observation_digest": "",
    }
    manifest["observation_digest"] = digest({k: v for k, v in manifest.items() if k != "observation_digest"})
    Draft202012Validator(load(SCHEMA_REF)).validate(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a non-authoritative observation of current Physics V3 Engineering and discovery coverage")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = build_observation()
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
