#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ENGINE = Path(__file__).resolve().parent
LI_ROOT = ENGINE.parent
CONTRACTS = LI_ROOT / "contracts" / "v1"

schema = json.loads((CONTRACTS / "state-reduction-policy.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(schema)
policy = json.loads((ENGINE / "fixtures" / "state_reduction_policy.v1.json").read_text(encoding="utf-8"))
Draft202012Validator(schema).validate(policy)

registry = json.loads((ENGINE / "fixtures" / "capability_registry.v1.json").read_text(encoding="utf-8"))
ids = [row["capability_id"] for row in registry["capabilities"]]
assert len(ids) == len(set(ids)), "duplicate capability ids in registry fixture"
for row in registry["capabilities"]:
    assert row["scope"] in {"SHARED", "SUBJECT"}
    if row["scope"] == "SUBJECT":
        assert row.get("subject") in {"MATHEMATICS", "PHYSICS", "CHEMISTRY"}

print("LEARNER_INTELLIGENCE_PHASE5_ENGINE_CONTRACTS = PASS")
