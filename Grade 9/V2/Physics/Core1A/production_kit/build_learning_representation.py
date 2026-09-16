#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from task_router import ROOT, load_json, route, resolve_scaffold

def validate_schema(instance: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)

def build_from_fixture(fixture: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    bucket_id = fixture["bucket_id"]
    prior = fixture["prior_knowledge_pct"]
    task = route(bucket_id=bucket_id, prior_knowledge_pct=prior, root=root)

    source = fixture["source_contract"]
    answer = fixture["answer_contract"]
    authoring = fixture["authoring"]

    validate_schema(task, root / "contracts" / "physics-core1a-task-contract.schema.json")
    validate_schema(source, root / "contracts" / "physics-core1a-source-contract.schema.json")
    validate_schema(answer, root / "contracts" / "physics-core1a-answer-contract.schema.json")

    if source["bucket_id"] != bucket_id or answer["bucket_id"] != bucket_id:
        raise ValueError("Fixture bucket_id must match source and answer contracts.")
    if source["source_mode"] != task["source_mode_hint"]:
        raise ValueError(
            f"Source-mode mismatch for {bucket_id}: router={task['source_mode_hint']}, contract={source['source_mode']}"
        )

    scaffolds = load_json(root / "registry" / "physics-core1a-scaffold-profiles-v1.json")
    validate_schema(scaffolds, root / "contracts" / "physics-core1a-scaffold-profiles.schema.json")
    scaffold = resolve_scaffold(scaffolds, prior, task["difficulty"])
    if scaffold["profile_id"] != task["scaffold_profile_id"]:
        raise ValueError("Router/scaffold-profile mismatch.")

    atoms = authoring["learning_atoms"]
    families = authoring["transfer_families"]

    source_item_to_atoms = {item["source_id"]: list(item["teaching_atoms"]) for item in source["source_items"]}
    equation_to_atom = {eq["equation_id"]: eq["teaching_atom"] for eq in source["equations"]}
    question_to_family = {q["question_id"]: q["family_id"] for q in answer["questions"]}
    question_hint_to_atom = {
        q["question_id"]: {h["rung"]: h["learning_atom"] for h in q["hint_ladder"]}
        for q in answer["questions"]
    }

    lr = {
        "schema_version": "1.0.0",
        "lr_id": f"LR-{bucket_id}-P{prior}-v1",
        "bucket_id": bucket_id,
        "task_id": task["task_id"],
        "scaffold_profile_id": scaffold["profile_id"],
        "source_contract_id": source["source_contract_id"],
        "answer_contract_id": answer["answer_contract_id"],
        "learner_profile": {
            "prior_knowledge_pct": prior,
            "difficulty": task["difficulty"],
            "pathway": scaffold["pathway"],
            "question_load_class": task["question_load"]["class"],
        },
        "source_mode": source["source_mode"],
        "primary_questions": task["primary_questions"],
        "learning_atoms": atoms,
        "transfer_families": families,
        "publication_modules": list(scaffold["required_modules"]),
        "traceability": {
            "source_item_to_atoms": source_item_to_atoms,
            "equation_to_atom": equation_to_atom,
            "question_to_family": question_to_family,
            "question_hint_to_atom": question_hint_to_atom,
        },
        "validation_snapshot": {
            "generated_by": "Core1AProductionKit",
            "contract_versions": {
                "task": task["schema_version"],
                "source": source["schema_version"],
                "answer": answer["schema_version"],
                "scaffold": scaffolds["schema_version"],
                "learning_representation": "1.0.0",
            },
        },
    }
    validate_schema(lr, root / "contracts" / "physics-core1a-learning-representation.schema.json")
    return lr

def build_fixture_file(path: Path, out: Path | None = None, root: Path = ROOT) -> dict[str, Any]:
    fixture = load_json(path)
    lr = build_from_fixture(fixture, root=root)
    if out:
        out.write_text(json.dumps(lr, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return lr

def main() -> None:
    ap = argparse.ArgumentParser(description="Build a normalized Core1A learning representation from a production fixture.")
    ap.add_argument("--fixture", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    lr = build_fixture_file(args.fixture, args.out)
    print(f"BUILT {lr['lr_id']} -> {args.out}")

if __name__ == "__main__":
    main()
