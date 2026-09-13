#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_CONDITION = re.compile(r"^(<=|>=|==|<|>)([0-4])$")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def metric_snapshot(evidence: dict[str, Any]) -> dict[str, int]:
    metrics = evidence["metrics"]
    return {name: int(metrics[name]["value"]) for name in ("SA", "SS", "QE", "QR", "UA", "CI")}


def _matches(value: int, expression: str) -> bool:
    m = _CONDITION.fullmatch(expression)
    if not m:
        raise ValueError(f"Unsupported routing condition: {expression!r}")
    op, raw = m.groups()
    target = int(raw)
    return {
        "<": value < target,
        "<=": value <= target,
        "==": value == target,
        ">=": value >= target,
        ">": value > target,
    }[op]


def rule_matches(rule: dict[str, Any], metrics: dict[str, int]) -> bool:
    return all(_matches(metrics[name], expression) for name, expression in rule["when"].items())


def choose_rule(evidence: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    metrics = metric_snapshot(evidence)
    ordered = sorted(policy["rules"], key=lambda x: int(x["priority"]), reverse=True)
    matches = [rule for rule in ordered if rule_matches(rule, metrics)]
    if not matches:
        raise ValueError("Routing policy has no matching rule and no default rule.")
    return matches[0]


def route(
    evidence: dict[str, Any],
    policy: dict[str, Any] | None = None,
    owner_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_json(ROOT / "policy" / "first-role-routing.v1.json")
    rule = choose_rule(evidence, policy)
    system_route = rule["route"]
    final_route = system_route

    # Overrides alter execution, never the system finding. HARD is universal operational
    # control. SOFT is honored when automatic routing is already safe; it cannot silently
    # turn an evidence BLOCK into a positive evidence claim.
    if owner_override is not None:
        requested = owner_override["requested_route"]
        if owner_override["mode"] == "HARD":
            final_route = requested
        elif owner_override["mode"] == "SOFT" and system_route != "BLOCK":
            final_route = requested

    return {
        "schema_version": "1.0.0",
        "route_id": f"R-{evidence['topic_id']}-{rule['rule_id']}",
        "topic_id": evidence["topic_id"],
        "matched_rule_id": rule["rule_id"],
        "system_finding": {
            "recommended_route": system_route,
            "reason": rule["reason"],
        },
        "owner_override": owner_override,
        "final_route": final_route,
        "evidence_metric_snapshot": metric_snapshot(evidence),
    }


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Route a Physics topic from normalized evidence.")
    ap.add_argument("evidence", type=Path)
    ap.add_argument("--policy", type=Path, default=ROOT / "policy" / "first-role-routing.v1.json")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    result = route(load_json(args.evidence), load_json(args.policy))
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
