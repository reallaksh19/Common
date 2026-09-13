#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

from governor import load_json, route

ROOT = Path(__file__).resolve().parents[1]


def run() -> list[dict]:
    evidence_schema = load_json(ROOT / "contracts" / "evidence-state.schema.json")
    route_schema = load_json(ROOT / "contracts" / "routing-decision.schema.json")
    evidence_validator = Draft202012Validator(evidence_schema)
    route_validator = Draft202012Validator(route_schema)
    policy = load_json(ROOT / "policy" / "first-role-routing.v1.json")

    results = []
    for path in sorted((ROOT / "fixtures" / "golden").glob("*.json")):
        fixture = load_json(path)
        evidence_validator.validate(fixture["evidence"])
        decision = route(fixture["evidence"], policy)
        route_validator.validate(decision)
        actual = decision["final_route"]
        expected = fixture["expected_route"]
        if actual != expected:
            raise AssertionError(f"{fixture['fixture_id']}: expected {expected}, got {actual}")
        results.append({
            "fixture_id": fixture["fixture_id"],
            "expected_route": expected,
            "matched_rule_id": decision["matched_rule_id"],
            "status": "PASS",
        })
    return results


def main() -> None:
    print(json.dumps({"status": "PASS", "fixtures": run()}, indent=2))


if __name__ == "__main__":
    main()
