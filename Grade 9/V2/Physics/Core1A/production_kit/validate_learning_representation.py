#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from task_router import ROOT, load_json, route, resolve_scaffold

def schema_validate(instance: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)

def validate_fixture_and_lr(fixture: dict[str, Any], lr: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    bucket_id = fixture["bucket_id"]
    prior = fixture["prior_knowledge_pct"]
    source = fixture["source_contract"]
    answer = fixture["answer_contract"]
    task = route(bucket_id=bucket_id, prior_knowledge_pct=prior, root=root)
    scaffolds = load_json(root / "registry" / "physics-core1a-scaffold-profiles-v1.json")
    scaffold = resolve_scaffold(scaffolds, prior, task["difficulty"])

    schema_validate(task, root / "contracts" / "physics-core1a-task-contract.schema.json")
    schema_validate(source, root / "contracts" / "physics-core1a-source-contract.schema.json")
    schema_validate(answer, root / "contracts" / "physics-core1a-answer-contract.schema.json")
    schema_validate(scaffolds, root / "contracts" / "physics-core1a-scaffold-profiles.schema.json")
    schema_validate(lr, root / "contracts" / "physics-core1a-learning-representation.schema.json")

    errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    check(lr["bucket_id"] == bucket_id, "LR bucket does not match fixture.")
    check(lr["primary_questions"] == task["primary_questions"], "LR primary questions drift from canonical task.")
    check(source["source_mode"] == task["source_mode_hint"], "Source contract does not confirm router source mode.")

    atom_ids = {a["atom_id"] for a in lr["learning_atoms"]}
    family_ids = {f["family_id"] for f in lr["transfer_families"]}

    for item in source["source_items"]:
        if item["integrity_class"] != "CLEAN":
            check(item["use_policy"] != "USE", f"{item['source_id']}: non-clean source cannot be silently USE.")
        for atom in item["teaching_atoms"]:
            check(atom in atom_ids, f"{item['source_id']}: teaching atom {atom} missing from LR.")

    for eq in source["equations"]:
        check(eq["teaching_atom"] in atom_ids, f"{eq['equation_id']}: teaching atom missing from LR.")
        if eq["authority"] == "DERIVED_BRIDGE":
            check(bool(eq["derivation_basis"]), f"{eq['equation_id']}: derived bridge requires derivation_basis.")

    if source["source_mode"] in {"PRACTICE_DRIVEN", "SOURCE_VISIBLE_EXTENSION"}:
        check(bool(source["source_gaps"]), "Practice/extension source mode must record at least one source gap.")
    if source["source_mode"] == "SOURCE_VISIBLE_EXTENSION":
        check(bool(source["forbidden_inventions"]), "Source-visible extension must record forbidden inventions.")

    min_visual = scaffold["minimum_visual_stages_per_atom"]
    for atom in lr["learning_atoms"]:
        check(len(atom["visual_stages"]) >= min_visual,
              f"{atom['atom_id']}: needs >= {min_visual} visual stages for {scaffold['profile_id']}.")
        if scaffold["misconception_policy"] == "REQUIRED":
            check(bool(atom["misconception_targets"]), f"{atom['atom_id']}: misconception target required by scaffold.")

    answer_questions = {q["question_id"]: q for q in answer["questions"]}
    check(set(answer_questions) == set(task["primary_questions"]), "Answer contract must cover canonical primary questions exactly once.")
    check(len(answer_questions) == len(answer["questions"]), "Duplicate question id in answer contract.")

    family_question_union: list[str] = []
    family_by_id = {f["family_id"]: f for f in lr["transfer_families"]}
    for family in lr["transfer_families"]:
        family_question_union.extend(family["core2_questions"])
        check(len(family["hint_ladder"]) == 3, f"{family['family_id']}: needs H1/H2/H3.")
        check([h["rung"] for h in family["hint_ladder"]] == ["H1", "H2", "H3"], f"{family['family_id']}: hint order must be H1,H2,H3.")
        check(len(family["readiness_checks"]) >= 4, f"{family['family_id']}: readiness requires four dimensions.")
        for atom in family["support_atoms"]:
            check(atom in atom_ids, f"{family['family_id']}: support atom {atom} missing.")

    check(set(family_question_union) == set(task["primary_questions"]), "Transfer families must cover primary questions exactly.")
    check(len(family_question_union) == len(set(family_question_union)), "A primary question appears in more than one transfer family.")
    check(len(lr["transfer_families"]) >= task["question_load"]["minimum_transfer_families"], "Transfer-family count is below the question-load minimum.")

    for qid, q in answer_questions.items():
        check(q["family_id"] in family_ids, f"{qid}: family missing from LR.")
        family = family_by_id.get(q["family_id"])
        if family:
            check(qid in family["core2_questions"], f"{qid}: answer family does not claim the question.")
        check([h["rung"] for h in q["hint_ladder"]] == ["H1", "H2", "H3"], f"{qid}: answer hint order must be H1,H2,H3.")
        check([h["role"] for h in q["hint_ladder"]] == ["KEY_PHYSICS", "REPRESENTATION", "FIRST_MOVE"],
              f"{qid}: answer hints must follow key physics -> representation -> first move.")
        for h in q["hint_ladder"]:
            check(h["learning_atom"] in atom_ids, f"{qid} {h['rung']}: learning atom {h['learning_atom']} missing.")
        auth = q["answer_authority"]
        if auth["mode"] == "INLINE_VERIFIED":
            check(bool(auth["canonical_answer"]) and auth["authority_ref"] is None,
                  f"{qid}: INLINE_VERIFIED requires canonical_answer and no authority_ref.")
        else:
            check(auth["canonical_answer"] is None and bool(auth["authority_ref"]),
                  f"{qid}: EXTERNAL_VERIFIED requires authority_ref and no invented inline answer.")
        if q["release_status"] == "HELD":
            check(bool(q["release_prerequisite_buckets"]), f"{qid}: HELD question requires release prerequisites.")

    mods = lr["publication_modules"]
    for required in scaffold["required_modules"]:
        check(required in mods, f"Required module missing: {required}")
    if "INDEPENDENT_PRACTICE" in mods and "HINTS" in mods:
        check(mods.index("INDEPENDENT_PRACTICE") < mods.index("HINTS"), "Independent practice must appear before hints.")
    if "READINESS" in mods and "CORE2_TRANSFER_SUMMARY" in mods:
        check(mods.index("READINESS") < mods.index("CORE2_TRANSFER_SUMMARY"), "Readiness must appear before Core2 transfer.")

    expected = fixture.get("expected", {})
    if expected:
        check(len(lr["learning_atoms"]) >= expected.get("minimum_learning_atoms", 0), "Golden fixture has fewer learning atoms than expected.")
        check(len(lr["transfer_families"]) == expected.get("transfer_family_count", len(lr["transfer_families"])), "Golden fixture transfer-family count drift.")
        check(set(lr["primary_questions"]) == set(expected.get("primary_questions", lr["primary_questions"])), "Golden fixture primary-question set drift.")

    report = {
        "schema_version": "1.0.0",
        "bucket_id": bucket_id,
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "checks": {
            "canonical_question_coverage": not any("primary questions" in e.lower() for e in errors),
            "source_integrity": not any("source" in e.lower() and ("silently" in e.lower() or "gap" in e.lower()) for e in errors),
            "hint_preteach": not any("hint" in e.lower() or "learning atom" in e.lower() for e in errors),
            "scaffold_depth": not any("visual stages" in e.lower() or "misconception" in e.lower() for e in errors),
            "attempt_before_hints": "Independent practice must appear before hints." not in errors,
            "readiness_before_transfer": "Readiness must appear before Core2 transfer." not in errors,
        },
    }
    if errors:
        raise ValueError(json.dumps(report, indent=2))
    return report

def main() -> None:
    ap = argparse.ArgumentParser(description="Validate a Core1A learning representation against production contracts.")
    ap.add_argument("--fixture", type=Path, required=True)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    fixture = load_json(args.fixture)
    lr = load_json(args.input)
    report = validate_fixture_and_lr(fixture, lr)
    text = json.dumps(report, indent=2)
    if args.report:
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
