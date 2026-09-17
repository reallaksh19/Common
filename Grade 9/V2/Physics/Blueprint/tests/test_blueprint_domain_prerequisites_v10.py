#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
SHARED = REPO / "Grade 9" / "V2" / "Shared" / "CrossDomain"
sys.path.insert(0, str(ROOT / "engine"))

from compile_domain_prerequisite_closure import compile_domain_prerequisite_closure  # noqa: E402
from compile_engineering_closure import compile_closure  # noqa: E402


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def load_shared(rel: str):
    return json.loads((SHARED / rel).read_text(encoding="utf-8"))


def engineering_receipt():
    return compile_closure(
        load("fixtures/engineering-workbench/relative-motion-request.v1.json"),
        load("fixtures/engineering-workbench/relative-motion-manifest.v3.json"),
    )


def assert_fails(code: str, fn) -> None:
    try:
        fn()
    except AssertionError as exc:
        assert str(exc).startswith(code), str(exc)
    else:
        raise AssertionError("EXPECTED_FAILURE:" + code)


def test_missing_external_authority_emits_provider_demands():
    receipt = compile_domain_prerequisite_closure(engineering_receipt(), [], [])
    assert receipt["closure_status"] == "HELD"
    rows = {row["prerequisite_id"]: row for row in receipt["prerequisites"]}
    assert set(rows) == {"MATH-GEO-2D", "MATH-TRIG-RIGHT"}
    assert all(row["status"] == "HELD_NO_DOMAIN_RECEIPT" for row in rows.values())
    assert all(row["authority_ref"] is None for row in rows.values())
    assert all(row["demand_id"] for row in rows.values())

    demands = {row["prerequisite_id"]: row for row in receipt["demands"]}
    assert set(demands) == set(rows)
    assert all(row["requester_subject"] == "PHYSICS" for row in demands.values())
    assert all(row["provider_subject"] == "MATHEMATICS" for row in demands.values())
    assert all(row["status"] == "OPEN_HELD" for row in demands.values())
    assert all(row["provider_entrypoint_ref"] == "Grade 9/V2/Mathematics/V2_GENERATION_ENTRYPOINT.md" for row in demands.values())
    assert all(row["authority_contract_ref"] == "Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-authority.schema.json" for row in demands.values())
    assert "PHY-VEC-BASICS" in demands["MATH-GEO-2D"]["required_by_gate_ids"]
    assert "PHY-VEC-COMPONENTS" in demands["MATH-TRIG-RIGHT"]["required_by_gate_ids"]
    validator = Draft202012Validator(load_shared("contracts/domain-prerequisite-demand.schema.json"))
    for demand in demands.values():
        validator.validate(demand)


def test_raw_authority_dictionary_cannot_close_without_repository_source_ref():
    fake = {
        "schema_version": "1.0.0",
        "receipt_id": "DOMAIN-AUTH-TEST-MATH-GEO-2D",
        "provider_subject": "MATHEMATICS",
        "prerequisite_id": "MATH-GEO-2D",
        "status": "READY_FROM_AUTHORITATIVE_DOMAIN",
        "evidence_refs": ["Grade 9/V2/Mathematics/V2_GENERATION_ENTRYPOINT.md"],
        "receipt_digest": "sha256:" + "0" * 64,
    }
    assert_fails(
        "DOMAIN_PREREQUISITE_AUTHORITY_SOURCE_REF_REQUIRED",
        lambda: compile_domain_prerequisite_closure(engineering_receipt(), [fake], []),
    )


def test_physics_owned_file_cannot_impersonate_math_authority():
    fake = {
        "schema_version": "1.0.0",
        "receipt_id": "DOMAIN-AUTH-TEST-MATH-GEO-2D",
        "provider_subject": "MATHEMATICS",
        "prerequisite_id": "MATH-GEO-2D",
        "status": "READY_FROM_AUTHORITATIVE_DOMAIN",
        "evidence_refs": ["Grade 9/V2/Mathematics/V2_GENERATION_ENTRYPOINT.md"],
        "receipt_digest": "sha256:" + "0" * 64,
    }
    assert_fails(
        "DOMAIN_PREREQUISITE_AUTHORITY_NOT_PROVIDER_OWNED:MATH-GEO-2D",
        lambda: compile_domain_prerequisite_closure(
            engineering_receipt(),
            [fake],
            ["Grade 9/V2/Physics/Blueprint/fixtures/stress-tests/relative-motion-grade9-cbse.request.v1.json"],
        ),
    )


def test_shared_authority_contract_is_provider_owned_not_physics_owned():
    schema = load_shared("contracts/domain-prerequisite-authority.schema.json")
    assert schema["title"] == "Cross-Domain Prerequisite Authority Receipt"
    assert schema["properties"]["provider_subject"] == {"type": "string", "minLength": 1}
    assert not (ROOT / "contracts" / "domain-prerequisite-authority.schema.json").exists()


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"Blueprint V10 domain-prerequisite tests: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
