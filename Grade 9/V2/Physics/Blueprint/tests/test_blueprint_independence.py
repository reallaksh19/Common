#!/usr/bin/env python3
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from governor import load_json  # noqa: E402
from independent_validation import audit_session, build_session, digest  # noqa: E402


def make_session():
    claims = {
        "claims": [
            {"claim_id": "C1", "text": "Independent semantic claim from ground truth."},
            {"claim_id": "C2", "text": "Independent boundary claim."},
        ]
    }
    return build_session(
        session_id="VAL-GOLDEN-001",
        topic_id="PHY-GOLDEN",
        validator_role="CORE2",
        validator_instance_id="INSTANCE-CORE2-FRESH",
        upstream_role="CORE1",
        upstream_instance_ids=["INSTANCE-CORE1-ORIGINAL"],
        ground_truth_refs=["GT-1", "GT-2"],
        independent_claims=claims,
        upstream_packet_refs=["K-GOLDEN-001"],
    ), claims


def test_pass1_is_ground_truth_only_and_locked():
    session, _ = make_session()
    assert session["pass1"]["mode"] == "GROUND_TRUTH_ONLY"
    assert session["pass1"]["visible_upstream_packet_refs"] == []
    assert session["pass1"]["locked"] is True
    audit_session(session)


def test_pass1_digest_is_frozen_before_upstream_reveal():
    session, claims = make_session()
    assert session["pass1"]["independent_claims_digest"] == digest(claims)
    assert session["pass2"]["frozen_pass1_digest"] == session["pass1"]["independent_claims_digest"]
    assert session["pass2"]["visible_upstream_packet_refs"] == ["K-GOLDEN-001"]


def test_self_validation_is_rejected():
    try:
        build_session(
            session_id="VAL-BAD",
            topic_id="PHY-GOLDEN",
            validator_role="CORE2",
            validator_instance_id="INSTANCE-SAME",
            upstream_role="CORE1",
            upstream_instance_ids=["INSTANCE-SAME"],
            ground_truth_refs=["GT-1"],
            independent_claims={"claims": []},
            upstream_packet_refs=["K-1"],
        )
    except AssertionError as exc:
        assert str(exc) == "SELF_VALIDATION_FORBIDDEN"
    else:
        raise AssertionError("SELF_VALIDATION_WAS_ACCEPTED")


def test_upstream_cannot_be_injected_into_pass1():
    session, _ = make_session()
    tampered = deepcopy(session)
    tampered["pass1"]["visible_upstream_packet_refs"] = ["K-GOLDEN-001"]
    try:
        audit_session(tampered)
    except AssertionError as exc:
        assert str(exc) == "UPSTREAM_VISIBLE_DURING_GROUND_TRUTH_PASS"
    else:
        raise AssertionError("PASS1_ACCEPTED_UPSTREAM_PACKET")


def test_frozen_claim_digest_cannot_change_after_reveal():
    session, _ = make_session()
    tampered = deepcopy(session)
    tampered["pass2"]["frozen_pass1_digest"] = "0" * 64
    try:
        audit_session(tampered)
    except AssertionError as exc:
        assert str(exc) == "PASS1_CHANGED_AFTER_UPSTREAM_REVEAL"
    else:
        raise AssertionError("CHANGED_PASS1_DIGEST_ACCEPTED")


def test_session_matches_schema():
    session, _ = make_session()
    schema = load_json(ROOT / "contracts" / "independent-validation-session.schema.json")
    Draft202012Validator(schema).validate(session)


def main():
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"Blueprint independence tests: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
