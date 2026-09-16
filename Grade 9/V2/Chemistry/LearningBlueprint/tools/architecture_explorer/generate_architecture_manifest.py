#!/usr/bin/env python3
"""
Generate Chemistry LearningBlueprint Architecture Observation Manifest
======================================================================
Scans schemas, policies, engines, and tests.
Supports --check mode for CI drift detection.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(val).encode("utf-8")).hexdigest()


def scan_components() -> dict[str, Any]:
    components: dict[str, dict[str, Any]] = {}
    relations: list[dict[str, Any]] = []

    contracts_dir = ROOT / "contracts"
    policies_dir = ROOT / "policies"
    engine_dir = ROOT / "engine"
    tests_dir = ROOT / "tests"

    if contracts_dir.exists():
        for path in sorted(contracts_dir.glob("*.schema.json")):
            cid = f"schema:{path.name}"
            components[cid] = {
                "component_id": cid,
                "name": path.name,
                "component_type": "SCHEMA",
                "producer_refs": [],
                "validator_refs": [],
                "consumer_refs": [],
                "test_refs": [],
            }

    if policies_dir.exists():
        for path in sorted(policies_dir.glob("*.json")):
            cid = f"policy:{path.name}"
            components[cid] = {
                "component_id": cid,
                "name": path.name,
                "component_type": "POLICY",
                "consumer_refs": [],
                "test_refs": [],
            }

    if engine_dir.exists():
        for path in sorted(engine_dir.glob("*.py")):
            cid = f"engine:{path.name}"
            ctype = "VALIDATOR" if "validate_" in path.name else "COMPILER"
            components[cid] = {
                "component_id": cid,
                "name": path.name,
                "component_type": ctype,
                "test_refs": [],
            }
            content = path.read_text(encoding="utf-8")
            schemas_found = sorted(set(re.findall(r'[\w-]+\.schema\.json', content)))
            for s_name in schemas_found:
                s_id = f"schema:{s_name}"
                if s_id in components:
                    relations.append({"source": cid, "target": s_id, "relation_type": "USES_SCHEMA", "confidence": "EXPLICIT"})

    relations.sort(key=lambda r: (r["source"], r["target"], r["relation_type"]))

    if tests_dir.exists():
        for path in sorted(tests_dir.glob("*.py")):
            cid = f"test:{path.name}"
            components[cid] = {
                "component_id": cid,
                "name": path.name,
                "component_type": "TEST",
            }

    manifest = {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "manifest_class": "DERIVED_ARCHITECTURE_OBSERVATION",
        "authority": "DERIVED_ARCHITECTURE_OBSERVATION",
        "technical_authorization": "NOT_EVALUATED",
        "publication_authorization": "NOT_IMPLIED",
        "component_count": len(components),
        "relation_count": len(relations),
        "components": components,
        "relations": relations,
    }
    manifest["manifest_digest"] = _digest(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Chemistry Architecture Observation Manifest")
    parser.add_argument("--out", default=str(HERE / "architecture_observation_manifest.json"))
    parser.add_argument("--check", action="store_true", help="Check manifest drift")
    args = parser.parse_args()

    manifest = scan_components()
    out_path = Path(args.out)

    if args.check:
        if not out_path.exists():
            raise SystemExit("Manifest not found on disk.")
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        if existing.get("manifest_digest") != manifest.get("manifest_digest"):
            raise SystemExit("Architecture manifest is OUT OF DATE. Run generator without --check.")
        print("Architecture manifest is UP TO DATE.")
        return

    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Observation manifest generated with {manifest['component_count']} components.")


if __name__ == "__main__":
    main()
