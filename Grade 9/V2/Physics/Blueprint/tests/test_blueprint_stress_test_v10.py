#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_engineering_closure import compile_closure  # noqa: E402
from compile_seven_core_stress_test import compile_stress_test  # noqa: E402


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def request():
    return load("fixtures/stress-tests/relative-motion-grade9-cbse.request.v1.json")


def test_request_cannot_assert_final_verdict():
    value = request()
    value["final_verdict"] = "STRESS_TEST_PASS"
    try:
        Draft202012Validator(load("contracts/seven-core-stress-test-request.schema.json")).validate(value)
    except ValidationError:
        pass
    else:
        raise AssertionError("STRESS_REQUEST_ALLOWED_SELF_ASSERTED_VERDICT")


def test_relative_motion_stress_receipt_is_machine_derived():
    receipt = compile_stress_test(request())
    Draft202012Validator(load("contracts/seven-core-stress-test-receipt.schema.json")).validate(receipt)
    assert receipt["final_verdict"] == "STRESS_TEST_PASS"
    assert receipt["routing"]["target_route"] == "CORE1_FIRST"
    assert receipt["join"]["join_status"] == "JOIN_READY_NO_CORE2_DEMAND"
    assert receipt["cores"]["CORE2"]["status"] == "HELD_VERIFIED_NO_TARGET_DEMAND"
    assert receipt["cores"]["CORE2A"]["status"] == "NOT_INSTANTIATED_NO_LEGAL_ITEM"
    assert receipt["cores"]["CORE1A"]["status"] == "BLOCKED_BEFORE_STAGE_RELEASE"
    assert "JOIN_NOT_ASSIMILATION_READY" not in receipt["cores"]["CORE1A"]["blockers"]
    assert "MISSING_GOVERNED_CONTROL_STATE" in receipt["cores"]["CORE1A"]["blockers"]
    assert "EXTERNAL_DOMAIN_PREREQUISITES_HELD" in receipt["cores"]["CORE1A"]["blockers"]
    assert receipt["downstream"]["CCU"] == "NOT_INSTANTIATED"
    assert receipt["downstream"]["CDAU"] == "NOT_INSTANTIATED"
    assert receipt["downstream"]["SDU"] == "NOT_ISSUED"
    assert receipt["downstream"]["LAU"] == "NOT_ISSUED"
    assert receipt["downstream"]["PUBLICATION"] == "NOT_AUTHORIZED"
    assert receipt["architecture_violations"] == []


def test_external_math_is_held_and_emits_provider_demands():
    receipt = compile_stress_test(request())
    rows = {row["prerequisite_id"]: row for row in receipt["domain_prerequisites"]["prerequisites"]}
    assert rows["MATH-GEO-2D"]["status"] == "HELD_NO_DOMAIN_RECEIPT"
    assert rows["MATH-TRIG-RIGHT"]["status"] == "HELD_NO_DOMAIN_RECEIPT"
    assert receipt["domain_prerequisites"]["closure_status"] == "HELD"

    demands = {row["prerequisite_id"]: row for row in receipt["domain_prerequisites"]["demands"]}
    assert set(demands) == {"MATH-GEO-2D", "MATH-TRIG-RIGHT"}
    assert all(row["provider_subject"] == "MATHEMATICS" for row in demands.values())
    assert all(row["status"] == "OPEN_HELD" for row in demands.values())
    assert all(row["demand_digest"].startswith("sha256:") for row in demands.values())


def test_engineering_depth_research_is_additive_and_fail_closed():
    base_request = load("fixtures/engineering-workbench/relative-motion-request.v1.json")
    manifest = load("fixtures/engineering-workbench/relative-motion-manifest.v3.json")
    standard = compile_closure(base_request, manifest)

    research_request = deepcopy(base_request)
    research_request["engineering_depth"] = "RESEARCH"
    research = compile_closure(research_request, manifest)

    assert standard["closure_status"] == "READY"
    assert research["closure_status"] == "BLOCKED"
    assert standard["gate_states"] == research["gate_states"]
    assert standard["direct_gate_ids"] == research["direct_gate_ids"]
    assert standard["transitive_gate_ids"] == research["transitive_gate_ids"]
    blocker_codes = {row["code"] for row in research["blockers"]}
    assert blocker_codes == {"E_ENG_RESEARCH_DOSSIER_REQUIRED", "E_ENG_CLAIM_LEDGER_REQUIRED"}


def test_no_surrogate_pass_labels_exist():
    receipt = compile_stress_test(request())
    statuses = {value["status"] for value in receipt["cores"].values()}
    assert "PASS_BY_NONFABRICATION" not in statuses
    assert "PASS_FAIL_CLOSED_DIFFERENTIATION" not in statuses


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"Blueprint V10 seven-core stress tests: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
