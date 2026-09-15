#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_engineering_readiness import build_envelope, compile_readiness  # noqa: E402
from compile_engineering_closure import load  # noqa: E402


def test_relative_motion_internal_ready_but_external_math_held():
    request = load("fixtures/engineering-workbench/relative-motion-request.v1.json")
    manifest = load("fixtures/engineering-workbench/relative-motion-manifest.v3.json")
    engineering, domain, envelope = compile_readiness(request, manifest)

    assert engineering["closure_status"] == "READY"
    assert domain["closure_status"] == "HELD"
    assert envelope["dimensions"]["physics_technical"] == "READY"
    assert envelope["dimensions"]["external_prerequisites"] == "HELD"
    assert envelope["overall_state"] == "BLOCKED"
    assert envelope["consumer_permissions"]["CCU"]["status"] == "BLOCKED"
    assert envelope["consumer_permissions"]["CORE1A"]["status"] == "BLOCKED"
    assert envelope["consumer_permissions"]["PUBLICATION"]["status"] == "NOT_AUTHORIZED"
    refs = {row["ref"] for row in envelope["blockers"] if row["dimension"] == "EXTERNAL_PREREQUISITES"}
    assert refs == {"MATH-GEO-2D", "MATH-TRIG-RIGHT"}


def test_research_depth_compiles_evidence_without_requiring_external_promotion():
    request = load("fixtures/engineering-workbench/grav-field-request.v1.json")
    manifest = load("fixtures/engineering-workbench/grav-field-manifest.v3.json")
    engineering, domain, envelope = compile_readiness(request, manifest)

    assert engineering["closure_status"] == "READY"
    assert envelope["dimensions"]["research_provenance"] == "READY"
    assert envelope["engineering_receipt"]["closure_status"] == "READY"
    assert envelope["domain_receipt"]["closure_status"] == domain["closure_status"]
    if domain["closure_status"] == "HELD":
        assert envelope["overall_state"] == "BLOCKED"
        assert envelope["consumer_permissions"]["CORE1A"]["status"] == "BLOCKED"


def test_ready_domain_receipt_allows_technical_consumers_but_not_publication():
    request = load("fixtures/engineering-workbench/relative-motion-request.v1.json")
    manifest = load("fixtures/engineering-workbench/relative-motion-manifest.v3.json")
    engineering, _, held = compile_readiness(request, manifest)
    ready_domain = {
        "schema_version": "1.0.0",
        "receipt_id": "DOMAIN-CLOSURE-PHY-TEST-READY",
        "engineering_receipt_ref": engineering["receipt_id"],
        "prerequisites": [],
        "demands": [],
        "closure_status": "READY",
        "closure_digest": "sha256:" + "1" * 64,
    }
    envelope = build_envelope(request, engineering, ready_domain)
    assert held["overall_state"] == "BLOCKED"
    assert envelope["overall_state"] == "READY_FOR_TECHNICAL_CONSUMPTION"
    for consumer in ["CCU", "CORE1A", "CORE1B", "CORE2A", "CORE2B"]:
        assert envelope["consumer_permissions"][consumer]["status"] == "ALLOWED"
    assert envelope["consumer_permissions"]["PUBLICATION"]["status"] == "NOT_AUTHORIZED"
    assert envelope["publication_authorization"] == "NOT_IMPLIED"


def test_envelope_is_deterministic_for_same_inputs():
    request = load("fixtures/engineering-workbench/relative-motion-request.v1.json")
    manifest = load("fixtures/engineering-workbench/relative-motion-manifest.v3.json")
    *_, one = compile_readiness(request, manifest)
    *_, two = compile_readiness(request, manifest)
    assert one == two
    assert one["envelope_digest"] == two["envelope_digest"]


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"Engineering readiness envelope: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
