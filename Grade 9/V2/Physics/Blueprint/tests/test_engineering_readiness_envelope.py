#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_engineering_readiness import build_envelope, compile_readiness  # noqa: E402
from compile_engineering_closure import load  # noqa: E402


def test_subject_adapter_uses_global_manifest_driven_permissions():
    request = load("fixtures/engineering-workbench/relative-motion-request.v1.json")
    manifest = load("fixtures/engineering-workbench/relative-motion-manifest.v3.json")
    engineering, domain, envelope = compile_readiness(request, manifest)

    assert engineering["closure_status"] == "READY"
    assert domain["closure_status"] == "HELD"
    assert envelope["authority_layer"] == "ENGINEERING_GATE"
    assert envelope["dimensions"]["technical"] == "READY"
    assert envelope["dimensions"]["external_prerequisites"] == "HELD"
    assert envelope["overall_state"] == "BLOCKED"
    assert set(envelope["consumer_permissions"]) == set(manifest["downstream_consumers"])
    assert envelope["consumer_permissions"]["CCU"]["status"] == "BLOCKED"
    assert envelope["consumer_permissions"]["PUBLICATION"]["status"] == "NOT_AUTHORIZED"
    assert "CORE1A" not in envelope["consumer_permissions"]


def test_research_depth_compiles_evidence_without_external_promotion():
    request = load("fixtures/engineering-workbench/grav-field-request.v1.json")
    manifest = load("fixtures/engineering-workbench/grav-field-manifest.v3.json")
    engineering, domain, envelope = compile_readiness(request, manifest)

    assert engineering["closure_status"] == "READY"
    assert envelope["dimensions"]["research_provenance"] == "READY"
    assert envelope["engineering_receipt"]["closure_status"] == "READY"
    assert envelope["domain_receipt"]["closure_status"] == domain["closure_status"]
    if domain["closure_status"] == "HELD":
        assert envelope["overall_state"] == "BLOCKED"
        for consumer, row in envelope["consumer_permissions"].items():
            if consumer != "PUBLICATION":
                assert row["status"] == "BLOCKED"


def test_ready_domain_allows_only_manifest_declared_technical_consumers():
    request = load("fixtures/engineering-workbench/relative-motion-request.v1.json")
    manifest = load("fixtures/engineering-workbench/relative-motion-manifest.v3.json")
    engineering, _, held = compile_readiness(request, manifest)
    ready_domain = {
        "schema_version": "1.0.0",
        "receipt_id": "DOMAIN-CLOSURE-TEST-READY",
        "engineering_receipt_ref": engineering["receipt_id"],
        "prerequisites": [],
        "demands": [],
        "closure_status": "READY",
        "closure_digest": "sha256:" + "1" * 64,
    }
    envelope = build_envelope(request, manifest, engineering, ready_domain)
    assert held["overall_state"] == "BLOCKED"
    assert envelope["overall_state"] == "READY_FOR_TECHNICAL_CONSUMPTION"
    assert set(envelope["consumer_permissions"]) == set(manifest["downstream_consumers"])
    for consumer, row in envelope["consumer_permissions"].items():
        expected = "NOT_AUTHORIZED" if consumer == "PUBLICATION" else "ALLOWED"
        assert row["status"] == expected
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
    print(f"Blueprint Engineering Gate adapter: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
