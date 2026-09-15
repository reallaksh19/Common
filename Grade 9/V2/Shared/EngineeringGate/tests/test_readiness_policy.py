#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from evaluate_readiness import EngineeringGateError, build_envelope, digest, require_consumer  # noqa: E402


def fixtures():
    request = {"request_id": "ENG-REQ-GENERIC-1", "engineering_depth": "STANDARD"}
    manifest = {
        "manifest_id": "ENG-MAN-GENERIC-1",
        "request_id": request["request_id"],
        "downstream_consumers": ["ALPHA", "BETA", "PUBLICATION"],
    }
    engineering = {
        "receipt_id": "ENG-CLOSURE-GENERIC-1",
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": digest(manifest),
        "closure_digest": "sha256:" + "1" * 64,
        "closure_status": "READY",
        "source_item_status": "SOURCE_READY",
        "blockers": [],
    }
    domain = {
        "receipt_id": "DOMAIN-CLOSURE-GENERIC-1",
        "engineering_receipt_ref": engineering["receipt_id"],
        "prerequisites": [],
        "closure_status": "READY",
        "closure_digest": "sha256:" + "2" * 64,
    }
    return request, manifest, engineering, domain


def test_permissions_are_manifest_driven_not_blueprint_hardcoded():
    request, manifest, engineering, domain = fixtures()
    envelope = build_envelope(request, manifest, engineering, domain)
    assert envelope["authority_layer"] == "ENGINEERING_GATE"
    assert set(envelope["consumer_permissions"]) == set(manifest["downstream_consumers"])
    assert envelope["consumer_permissions"]["ALPHA"]["status"] == "ALLOWED"
    assert envelope["consumer_permissions"]["BETA"]["status"] == "ALLOWED"
    assert envelope["consumer_permissions"]["PUBLICATION"]["status"] == "NOT_AUTHORIZED"
    assert "CCU" not in envelope["consumer_permissions"]
    assert "CORE1A" not in envelope["consumer_permissions"]


def test_same_id_manifest_mutation_cannot_expand_consumers():
    request, manifest, engineering, domain = fixtures()
    mutated = copy.deepcopy(manifest)
    mutated["downstream_consumers"].append("GAMMA")
    try:
        build_envelope(request, mutated, engineering, domain)
    except EngineeringGateError as exc:
        assert exc.code == "E_ENG_GATE_MANIFEST_DRIFT"
    else:
        raise AssertionError("same-ID manifest mutation must fail closed")


def test_external_hold_blocks_all_declared_technical_consumers():
    request, manifest, engineering, domain = fixtures()
    domain = copy.deepcopy(domain)
    domain["closure_status"] = "HELD"
    domain["prerequisites"] = [{"prerequisite_id": "EXT-PREREQ-1", "status": "HELD_NO_DOMAIN_RECEIPT"}]
    envelope = build_envelope(request, manifest, engineering, domain)
    assert envelope["overall_state"] == "BLOCKED"
    assert envelope["consumer_permissions"]["ALPHA"]["status"] == "BLOCKED"
    assert envelope["consumer_permissions"]["BETA"]["status"] == "BLOCKED"
    assert envelope["consumer_permissions"]["PUBLICATION"]["status"] == "NOT_AUTHORIZED"


def test_undeclared_consumer_cannot_be_requested_from_memory():
    request, manifest, engineering, domain = fixtures()
    envelope = build_envelope(request, manifest, engineering, domain)
    try:
        require_consumer(envelope, "REMEMBERED_CONSUMER")
    except EngineeringGateError as exc:
        assert exc.code == "E_ENG_GATE_CONSUMER_UNDECLARED"
    else:
        raise AssertionError("undeclared consumer must not be inferred")


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"Global Engineering Gate readiness policy: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
