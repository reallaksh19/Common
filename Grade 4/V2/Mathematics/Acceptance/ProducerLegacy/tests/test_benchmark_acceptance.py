"""
Tests for Primary Mathematics V2 Independent Benchmark Acceptance Suite.
"""
import copy
import json
from pathlib import Path
import pytest

from Primary.V2.Mathematics.BenchmarkAcceptance.validator.evaluate_candidate import BenchmarkEvaluator


@pytest.fixture
def evaluator():
    return BenchmarkEvaluator()


@pytest.fixture
def baseline_positive():
    p = Path(__file__).resolve().parent.parent / "fixtures" / "positive" / "semantic_cases.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def negative_mutations():
    p = Path(__file__).resolve().parent.parent / "fixtures" / "negative" / "semantic_mutations.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)["mutations"]


def test_positive_baseline_passes_all_machine_gates(evaluator, baseline_positive):
    report = evaluator.evaluate(baseline_positive)
    assert report["overall_machine_pass"] is True
    assert len(report["triggered_falsifiers"]) == 0
    assert report["passed_cases"] == len(baseline_positive["cases"])
    assert report["failed_cases"] == 0

    # Ensure all human gates remain PENDING
    for gate_name, status in report["human_review_status"].items():
        assert status == "PENDING_HUMAN_REVIEW"


def test_negative_mutations_trigger_expected_falsifiers(evaluator, baseline_positive, negative_mutations):
    for mutation in negative_mutations:
        mut_id = mutation["mutation_id"]
        expected_f = mutation["expected_falsifier"]
        patch = mutation["patch"]

        mutated_data = copy.deepcopy(baseline_positive)
        target_case = mutated_data["cases"][0]

        # Apply patch to target_case
        for k, v in patch.items():
            if isinstance(v, dict) and k in target_case and isinstance(target_case[k], dict):
                target_case[k].update(v)
            else:
                target_case[k] = v

        report = evaluator.evaluate(mutated_data)
        assert expected_f in report["triggered_falsifiers"], (
            f"Mutation {mut_id} did not trigger expected falsifier {expected_f}. "
            f"Triggered: {report['triggered_falsifiers']}"
        )
        assert report["overall_machine_pass"] is False
