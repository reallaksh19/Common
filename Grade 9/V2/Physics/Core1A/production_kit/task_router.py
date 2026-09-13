#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

GATES = [
    "G0_INDEX_SYNC",
    "G1_SOURCE_AND_CORE2_AUDIT",
    "G2_DIFFICULTY_AND_READINESS",
    "G3_LEARNING_ATOM_DECOMPOSITION",
    "G4_CORE2_HINT_PRETEACH_AUDIT",
    "G5_PROBLEM_FAMILY_ASSIMILATION",
    "G6_PAGE_PLAN",
    "G7_RENDER_AND_VISUAL_AUDIT",
    "G8_READINESS_AND_TRANSFER_AUDIT",
    "G9_MACHINE_QA_AND_HANDOFF",
]

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def classify_source_mode(source_basis: list[str]) -> str:
    basis = set(source_basis)
    if basis == {"SRC-GPRACTICE"}:
        return "PRACTICE_DRIVEN"
    if basis and basis.issubset({"SRC-GFORM", "SRC-GPRACTICE"}) and "SRC-GPRACTICE" in basis:
        return "SOURCE_VISIBLE_EXTENSION"
    return "THEORY_BACKED"

def load_class(count: int, rules: dict[str, Any]) -> tuple[str, int]:
    for name in ("LOW", "MEDIUM", "HIGH", "VERY_HIGH"):
        rule = rules[name]
        hi = rule["max_questions"]
        if count >= rule["min_questions"] and (hi is None or count <= hi):
            return name, rule["minimum_transfer_families"]
    raise ValueError(f"No question-load rule for count={count}")

def resolve_scaffold(registry: dict[str, Any], prior: int, difficulty: str) -> dict[str, Any]:
    matches = [p for p in registry["profiles"]
               if p["prior_knowledge_pct"] == prior and p["difficulty"] == difficulty]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one scaffold for prior={prior}, difficulty={difficulty}; found {len(matches)}")
    return matches[0]

def derive_next_bucket(sba_registry: dict[str, Any], build_state: dict[str, Any]) -> str | None:
    completed = set(build_state["completed_active_buckets"])
    active = [b["bucket_id"] for b in sba_registry["buckets"] if b["production_status"] == "ACTIVE"]
    remaining = [bid for bid in active if bid not in completed]
    expected = remaining[0] if remaining else None
    if build_state["next_active_bucket"] != expected:
        raise ValueError(
            f"BUILD STATE DRIFT: recorded={build_state['next_active_bucket']!r}, derived={expected!r}"
        )
    return expected

def route(bucket_id: str | None = None, prior_knowledge_pct: int = 20, root: Path = ROOT) -> dict[str, Any]:
    sba_registry = load_json(root / "registry" / "physics-core1a-motion-in-a-plane-sba-v1.json")
    build_state = load_json(root / "registry" / "physics-core1a-motion-in-a-plane-build-state-v1.json")
    scaffolds = load_json(root / "registry" / "physics-core1a-scaffold-profiles-v1.json")

    if bucket_id is None:
        bucket_id = derive_next_bucket(sba_registry, build_state)
        if bucket_id is None:
            raise ValueError("No remaining ACTIVE SBA bucket.")

    by_id = {b["bucket_id"]: b for b in sba_registry["buckets"]}
    if bucket_id not in by_id:
        raise KeyError(f"Unknown SBA bucket {bucket_id}")
    bucket = by_id[bucket_id]

    if bucket["production_status"] != "ACTIVE":
        raise ValueError(f"{bucket_id} is {bucket['production_status']}; no dedicated production task should be created.")

    questions = list(bucket["core2_primary_questions"])
    if not questions:
        raise ValueError(f"{bucket_id} has no primary Core (2) questions.")

    qclass, min_families = load_class(len(questions), scaffolds["question_load_rules"])
    scaffold = resolve_scaffold(scaffolds, prior_knowledge_pct, bucket["intrinsic_difficulty"])

    return {
        "schema_version": "1.0.0",
        "task_id": f"TASK-{bucket_id}-P{prior_knowledge_pct}",
        "bucket_id": bucket_id,
        "prior_knowledge_pct": prior_knowledge_pct,
        "difficulty": bucket["intrinsic_difficulty"],
        "pathway": scaffold["pathway"],
        "primary_questions": questions,
        "question_load": {
            "count": len(questions),
            "class": qclass,
            "minimum_transfer_families": min_families,
        },
        "prerequisite_buckets": list(bucket["prerequisite_buckets"]),
        "source_mode_hint": classify_source_mode(bucket["source_basis"]),
        "scaffold_profile_id": scaffold["profile_id"],
        "required_inputs": [
            "SOURCE_CONTRACT",
            "ANSWER_CONTRACT",
            "SBA_PROFILE",
            "TRANSFER_ROUTINES",
            "SCAFFOLD_PROFILE",
        ],
        "required_outputs": [
            "LEARNING_REPRESENTATION",
            "VALIDATION_REPORT",
            "BUILD_MANIFEST",
            "PDF",
            "MONTAGE",
        ],
        "gates": GATES,
    }

def main() -> None:
    ap = argparse.ArgumentParser(description="Route a Core1A SBA production task.")
    ap.add_argument("--bucket", help="Explicit bucket id. Omit to route the deterministic next active bucket.")
    ap.add_argument("--prior", type=int, choices=[20, 50], default=20)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    task = route(args.bucket, args.prior)
    text = json.dumps(task, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()
