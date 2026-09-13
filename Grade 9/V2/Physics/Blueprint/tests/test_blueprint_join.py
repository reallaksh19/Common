#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_join import compile_join  # noqa: E402


def golden():
    return json.loads((ROOT / "fixtures" / "join" / "join-ready.json").read_text(encoding="utf-8"))


def assert_fails(spec, code):
    try:
        compile_join(spec)
    except AssertionError as exc:
        assert str(exc).startswith(code), str(exc)
    else:
        raise AssertionError("EXPECTED_FAILURE:" + code)


def test_ready_join():
    packet = compile_join(golden())
    assert packet["join_status"] == "JOIN_READY"
    assert packet["assimilation_ready"] is True
    assert packet["critical_conflicts"] == []
    assert packet["demand_claim_count"] == 2


def test_schema_validates_golden():
    schema = json.loads((ROOT / "contracts" / "join-packet.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(compile_join(golden()))


def test_required_contradiction_blocks():
    spec = golden()
    spec["reconciliations"][0]["status"] = "CONTRADICTED"
    spec["reconciliations"][0]["unresolved_issues"] = ["Source and semantic claim disagree on the event condition."]
    packet = compile_join(spec)
    assert packet["join_status"] == "JOIN_BLOCKED"
    assert packet["assimilation_ready"] is False
    assert packet["items"][0]["disposition"] == "BLOCK"


def test_nonblocking_unknown_is_hold_not_block():
    spec = golden()
    spec["reconciliations"][1]["status"] = "UNKNOWN"
    spec["reconciliations"][1]["criticality"] = "NON_BLOCKING"
    spec["reconciliations"][1]["unresolved_issues"] = ["Insufficient evidence for this optional extension."]
    packet = compile_join(spec)
    assert packet["join_status"] == "JOIN_READY_WITH_HOLDS"
    assert packet["assimilation_ready"] is True
    assert packet["items"][1]["disposition"] == "HOLD"


def test_every_demand_must_be_reconciled_exactly_once():
    spec = golden()
    spec["reconciliations"] = spec["reconciliations"][:1]
    assert_fails(spec, "JOIN_DEMAND_COVERAGE_GAP")
    spec = golden()
    spec["reconciliations"].append(deepcopy(spec["reconciliations"][0]))
    assert_fails(spec, "JOIN_DUPLICATE_DEMAND_RECONCILIATION")


def test_unknown_knowledge_ref_fails():
    spec = golden()
    spec["reconciliations"][0]["knowledge_claim_refs"].append("K-NOT-DECLARED")
    assert_fails(spec, "JOIN_UNKNOWN_KNOWLEDGE_REF")


def test_confirmed_requires_semantic_grounding():
    spec = golden()
    spec["reconciliations"][0]["knowledge_claim_refs"] = []
    assert_fails(spec, "JOIN_SEMANTIC_GROUNDING_REQUIRED")


def test_ready_requires_assimilation_obligation():
    spec = golden()
    spec["reconciliations"][0]["assimilation_obligations"] = []
    assert_fails(spec, "JOIN_ASSIMILATION_OBLIGATION_REQUIRED")


def test_unresolved_requires_issue_record():
    spec = golden()
    spec["reconciliations"][0]["status"] = "MISSING"
    spec["reconciliations"][0]["unresolved_issues"] = []
    assert_fails(spec, "JOIN_UNRESOLVED_ISSUE_REQUIRED")


def test_validation_session_is_mandatory():
    spec = golden()
    spec["validation_session_refs"] = []
    assert_fails(spec, "JOIN_VALIDATION_SESSION_REQUIRED")


def test_digest_is_deterministic_under_reconciliation_order():
    a = golden()
    b = golden()
    b["reconciliations"] = list(reversed(b["reconciliations"]))
    assert compile_join(a)["join_digest"] == compile_join(b)["join_digest"]


def main():
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"Blueprint join tests: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
