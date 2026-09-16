#!/usr/bin/env python3
"""Project Chemistry Engineering Gates to Canonical Domain Registry contracts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(val).encode("utf-8")).hexdigest()


def load_json(rel_or_path: str | Path) -> dict:
    p = Path(rel_or_path) if Path(rel_or_path).is_absolute() else ROOT / rel_or_path
    return json.loads(p.read_text(encoding="utf-8"))


def project_registry(registry: dict | None = None) -> dict:
    registry = registry or load_json("policies/chemistry-technical-engineering-gates.v1.json")
    projected = []
    for gate in registry.get("subtopic_gates", []):
        gid = gate["subtopic_id"]
        tags = ["CHEMISTRY", f"GRADE_{gate.get('cbse_ref', {}).get('grade', 9)}", gate.get("jee_tier", "BOTH")]
        projected.append({
            "gate_id": gid,
            "canonical_id": f"CANONICAL-{gid}",
            "domain_tags": tags,
            "prerequisite_closure": gate.get("prerequisite_ids", []),
        })

    receipt = {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "projection_id": f"CHEM-ENG-PROJ-{digest(projected).replace('sha256:', '')[:12].upper()}",
        "source_registry_id": registry["registry_id"],
        "source_registry_digest": digest(registry),
        "target_domain": "CANONICAL_DOMAIN_REGISTRY",
        "projected_gates": projected,
    }
    schema = load_json("contracts/chemistry-engineering-domain-projection.schema.json")
    Draft202012Validator(schema).validate(receipt)
    return receipt


def main() -> None:
    ap = argparse.ArgumentParser(description="Project Engineering Gates to Domain Registry")
    ap.add_argument("--out")
    args = ap.parse_args()
    res = project_registry()
    if args.out:
        Path(args.out).write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
        print(f"Projected {len(res['projected_gates'])} gates to {args.out}")
    else:
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
