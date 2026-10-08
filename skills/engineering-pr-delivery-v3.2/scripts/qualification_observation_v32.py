#!/usr/bin/env python3
"""Source-bound qualification observation for V3.2 R-PROOF / Common #724.

DERIVED_OBSERVATION_ONLY: not acceptance, DELP progress, review, merge or custody
authority. Tests below precommit the outside-in acceptance contract before
product logic is added.
"""
from __future__ import annotations

INPUT_SCHEMA = "relay-v3.2-qualification-contract-v1"
RESULT_SCHEMA = "relay-v3.2-qualification-observation-v1"
AUTHORITY = "DERIVED_OBSERVATION_ONLY"


def assess(contract: dict, provider: object) -> dict:
    """Evaluate immutable required obligations using independent read-only provider facts."""
    return {
        "schema": RESULT_SCHEMA,
        "authority": AUTHORITY,
        "repository": contract.get("repository"),
        "responsibility": contract.get("responsibility"),
        "expected_candidate_sha": contract.get("candidate_sha"),
        "observed_candidate_sha": None,
        "overall": "UNKNOWN",
        "requirements": [
            {"id": req["id"], "status": "UNKNOWN", "reason": "NOT_IMPLEMENTED", "evidence_refs": []}
            for req in contract.get("requirements", [])
        ],
    }
