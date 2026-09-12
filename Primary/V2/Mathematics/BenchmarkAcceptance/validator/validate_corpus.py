#!/usr/bin/env python3
"""Validate the independent Primary Math V2 benchmark corpus itself."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from evaluate_candidate import evaluate

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "benchmark_cases.json"
FALSIFIERS = ROOT / "registry" / "falsifier_catalog.json"
POSITIVE = ROOT / "fixtures" / "positive" / "semantic_cases.json"
NEGATIVE = ROOT / "fixtures" / "negative" / "semantic_mutations.json"

EXPECTED_PRIMARY_STACK = [163, 171, 172, 185, 182, 164]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"Primary Math V2 benchmark corpus invalid: {message}")


def set_path(obj, path, value):
    cursor = obj
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def mutate_candidate(base, mutation):
    candidate = copy.deepcopy(base)
    cases = {c["case_id"]: c for c in candidate["cases"]}
    target = cases.get(mutation["case_id"])
    if target is None:
        fail(f"mutation {mutation['mutation_id']} targets unknown case {mutation['case_id']}")
    set_path(target, mutation["path"], mutation["value"])
    candidate["candidate_id"] = f"NEG-{mutation['mutation_id']}"
    return candidate


def main() -> None:
    registry = load(REGISTRY)
    falsifiers = load(FALSIFIERS)
    positive = load(POSITIVE)
    negatives = load(NEGATIVE)

    if registry.get("normative_primary_prs") != EXPECTED_PRIMARY_STACK:
        fail(f"normative Primary stack drifted: {registry.get('normative_primary_prs')}")

    case_ids = [c["case_id"] for c in registry["cases"]]
    if len(case_ids) != len(set(case_ids)):
        fail("duplicate benchmark case_id")

    falsifier_ids = [f["id"] for f in falsifiers["falsifiers"]]
    if len(falsifier_ids) != len(set(falsifier_ids)):
        fail("duplicate falsifier id")

    if positive.get("evidence_class") != "TEST_FIXTURE":
        fail("positive oracle fixture must be TEST_FIXTURE")

    positive_ids = [c["case_id"] for c in positive["cases"]]
    if set(positive_ids) != set(case_ids):
        fail(f"positive fixture coverage mismatch; missing={sorted(set(case_ids)-set(positive_ids))}, extra={sorted(set(positive_ids)-set(case_ids))}")

    report = evaluate(positive)
    if report["semantic_status"] != "PASS":
        fail(f"positive semantic fixture does not pass: {report['failures']}")
    if report["artifact_status"] != "BLOCKED":
        fail("test-only semantic fixture must not accidentally become a rendered-artifact PASS")

    mutation_ids = [m["mutation_id"] for m in negatives["mutations"]]
    if len(mutation_ids) != len(set(mutation_ids)):
        fail("duplicate negative mutation id")

    for mutation in negatives["mutations"]:
        expected = mutation["expected_falsifier"]
        if expected not in falsifier_ids:
            fail(f"mutation {mutation['mutation_id']} expects unregistered falsifier {expected}")
        mutated = mutate_candidate(positive, mutation)
        result = evaluate(mutated)
        actual = [f["falsifier"] for f in result["failures"]]
        if expected not in actual:
            fail(f"mutation {mutation['mutation_id']} did not trigger {expected}; got {actual}")

    print(
        "Primary Math V2 BenchmarkAcceptance corpus PASS: "
        f"{len(case_ids)} cases, {len(falsifier_ids)} catalogued falsifiers, "
        f"{len(mutation_ids)} executable negative mutations."
    )


if __name__ == "__main__":
    main()
