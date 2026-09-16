#!/usr/bin/env python3
"""Compile visibility manifest across Chemistry Engineering Gates."""

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


def compile_visibility(registry: dict | None = None) -> dict:
    registry = registry or load_json("policies/chemistry-technical-engineering-gates.v1.json")
    subtopics = []
    for gate in registry.get("subtopic_gates", []):
        gid = gate["subtopic_id"]
        cbse_ref = gate.get("cbse_ref", {})
        subtopics.append({
            "subtopic_id": gid,
            "learner_title": gate["learner_title"],
            "visibility_tier": "PUBLIC",
            "direct_prerequisites": gate.get("prerequisite_ids", []),
            "transitive_prerequisites": gate.get("prerequisite_ids", []),
            "cbse_grade": cbse_ref.get("grade", 9),
            "jee_tier": gate.get("jee_tier", "BOTH"),
        })

    manifest = {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "visibility_manifest_id": f"CHEM-ENG-VIS-{digest(subtopics).replace('sha256:', '')[:12].upper()}",
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "visible_subtopic_count": len(subtopics),
        "visible_subtopics": subtopics,
    }
    schema = load_json("contracts/chemistry-engineering-visibility-manifest.schema.json")
    Draft202012Validator(schema).validate(manifest)
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile Chemistry Engineering Visibility Manifest")
    ap.add_argument("--out")
    args = ap.parse_args()
    res = compile_visibility()
    if args.out:
        Path(args.out).write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
        print(f"Compiled visibility manifest ({res['visible_subtopic_count']} subtopics) to {args.out}")
    else:
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
