#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CLAIM_STATES = [
    "CONFIRMED",
    "REFINED",
    "MISSING",
    "UNSUPPORTED",
    "CONTRADICTED",
    "OUT_OF_SCOPE",
    "UNKNOWN",
]


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_session(
    *,
    session_id: str,
    topic_id: str,
    validator_role: str,
    validator_instance_id: str,
    upstream_role: str,
    upstream_instance_ids: list[str],
    ground_truth_refs: list[str],
    independent_claims: Any,
    upstream_packet_refs: list[str],
) -> dict[str, Any]:
    if validator_instance_id in set(upstream_instance_ids):
        raise AssertionError("SELF_VALIDATION_FORBIDDEN")
    if not ground_truth_refs:
        raise AssertionError("GROUND_TRUTH_REQUIRED")
    if not upstream_packet_refs:
        raise AssertionError("UPSTREAM_PACKET_REQUIRED_FOR_PASS2")

    frozen = digest(independent_claims)
    return {
        "schema_version": "1.0.0",
        "session_id": session_id,
        "topic_id": topic_id,
        "validator_role": validator_role,
        "validator_instance_id": validator_instance_id,
        "upstream_role": upstream_role,
        "upstream_instance_ids": list(upstream_instance_ids),
        "ground_truth_refs": list(ground_truth_refs),
        "pass1": {
            "mode": "GROUND_TRUTH_ONLY",
            "visible_ground_truth_refs": list(ground_truth_refs),
            "visible_upstream_packet_refs": [],
            "independent_claims_digest": frozen,
            "locked": True,
        },
        "pass2": {
            "mode": "COMPARE_UPSTREAM",
            "visible_upstream_packet_refs": list(upstream_packet_refs),
            "frozen_pass1_digest": frozen,
        },
        "pass3": {
            "mode": "EMIT_VALIDATION",
            "allowed_claim_states": CLAIM_STATES,
        },
    }


def audit_session(session: dict[str, Any]) -> None:
    if session["validator_instance_id"] in set(session["upstream_instance_ids"]):
        raise AssertionError("SELF_VALIDATION_FORBIDDEN")
    if session["pass1"]["visible_upstream_packet_refs"]:
        raise AssertionError("UPSTREAM_VISIBLE_DURING_GROUND_TRUTH_PASS")
    if set(session["pass1"]["visible_ground_truth_refs"]) != set(session["ground_truth_refs"]):
        raise AssertionError("GROUND_TRUTH_VISIBILITY_DRIFT")
    if not session["pass1"]["locked"]:
        raise AssertionError("PASS1_NOT_LOCKED")
    if session["pass2"]["frozen_pass1_digest"] != session["pass1"]["independent_claims_digest"]:
        raise AssertionError("PASS1_CHANGED_AFTER_UPSTREAM_REVEAL")
    if set(session["pass3"]["allowed_claim_states"]) != set(CLAIM_STATES):
        raise AssertionError("VALIDATION_STATE_VOCABULARY_DRIFT")


def main() -> None:
    import argparse
    from jsonschema import Draft202012Validator

    ap = argparse.ArgumentParser(description="Build and audit an independent validation session manifest.")
    ap.add_argument("spec", type=Path, help="JSON spec containing build_session keyword arguments plus independent_claims")
    args = ap.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    session = build_session(**spec)
    audit_session(session)
    schema = json.loads((ROOT / "contracts" / "independent-validation-session.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(session)
    print(json.dumps(session, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
