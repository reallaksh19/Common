#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema

HERE = Path(__file__).resolve()
MATH_BLUEPRINT = HERE.parents[1]
DEFAULT_SCHEMA = MATH_BLUEPRINT / "contracts" / "math-canonical-domain-registry.schema.json"
DEFAULT_POLICY = MATH_BLUEPRINT / "policies" / "math-canonical-domain-registry-policy.json"


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _walk_forbidden(value: Any, forbidden: set[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in forbidden:
                fail("DOMAIN_REGISTRY_RUNTIME_FIELD_FORBIDDEN", f"{path}.{key}")
            _walk_forbidden(child, forbidden, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _walk_forbidden(child, forbidden, f"{path}[{i}]")


def _internal_refs(asset: dict) -> set[str]:
    refs = set(asset.get("depends_on") or [])
    payload = asset.get("payload") or {}
    for key, value in payload.items():
        if key.endswith("_ref") and isinstance(value, str) and value.startswith("REG-MATH-"):
            refs.add(value)
        elif key.endswith("_refs") and isinstance(value, list):
            refs.update(x for x in value if isinstance(x, str) and x.startswith("REG-MATH-"))
    return refs


def _check_acyclic(assets: dict[str, dict]) -> None:
    state: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        mark = state.get(node, 0)
        if mark == 2:
            return
        if mark == 1:
            cycle = "->".join(stack + [node])
            fail("DOMAIN_REGISTRY_DEPENDENCY_CYCLE", cycle)
        state[node] = 1
        for dep in assets[node].get("depends_on") or []:
            visit(dep, stack + [node])
        state[node] = 2

    for asset_id in assets:
        visit(asset_id, [])


def validate_registry(
    registry: dict,
    *,
    schema: dict | None = None,
    policy: dict | None = None,
) -> dict:
    schema = schema or load(DEFAULT_SCHEMA)
    policy = policy or load(DEFAULT_POLICY)

    _walk_forbidden(registry, set(policy.get("forbidden_runtime_fields") or []))
    jsonschema.validate(registry, schema)

    rows = registry["assets"]
    ids = [row["asset_id"] for row in rows]
    if len(ids) != len(set(ids)):
        fail("DOMAIN_REGISTRY_DUPLICATE_ASSET_ID")

    assets = {row["asset_id"]: row for row in rows}
    join_refs = set(registry["join_refs"])
    authority_map = policy["authority_by_asset_type"]
    binding_rules = policy["authority_binding_rules"]

    for row in rows:
        asset_id = row["asset_id"]
        asset_type = row["asset_type"]
        authority = row["authority_class"]

        allowed = set(authority_map.get(asset_type) or [])
        if authority not in allowed:
            fail("DOMAIN_REGISTRY_AUTHORITY_MISMATCH", f"{asset_id}:{asset_type}:{authority}")

        rules = binding_rules[authority]
        if rules.get("requires_core1_refs") and not row["core1_refs"]:
            fail("DOMAIN_REGISTRY_CORE1_BINDING_MISSING", asset_id)
        if rules.get("requires_core2_refs") and not row["core2_refs"]:
            fail("DOMAIN_REGISTRY_CORE2_BINDING_MISSING", asset_id)

        if row["join_ref"] not in join_refs:
            fail("DOMAIN_REGISTRY_JOIN_REF_UNKNOWN", f"{asset_id}:{row['join_ref']}")

        if asset_id in set(row.get("depends_on") or []):
            fail("DOMAIN_REGISTRY_SELF_DEPENDENCY", asset_id)

        for ref in _internal_refs(row):
            if ref not in assets:
                fail("DOMAIN_REGISTRY_INTERNAL_REF_UNKNOWN", f"{asset_id}:{ref}")

        if asset_type == "SOURCE_QUESTION" and authority != "SOURCE_FROZEN":
            fail("DOMAIN_REGISTRY_SOURCE_QUESTION_NOT_FROZEN", asset_id)

        if asset_type == "PROBLEM_FAMILY" and not row["core2_refs"]:
            fail("DOMAIN_REGISTRY_PROBLEM_FAMILY_CORE2_BINDING_MISSING", asset_id)

        if asset_type in {
            "CONCEPT", "MODEL", "EQUATION", "DERIVATION", "CAPABILITY",
            "LEARNING_ATOM", "REPRESENTATION", "MISCONCEPTION",
        } and not row["core1_refs"]:
            fail("DOMAIN_REGISTRY_SEMANTIC_CORE1_BINDING_MISSING", asset_id)

    _check_acyclic(assets)

    return {
        "registry_id": registry["registry_id"],
        "asset_count": len(rows),
        "asset_type_counts": {
            kind: sum(1 for row in rows if row["asset_type"] == kind)
            for kind in sorted({row["asset_type"] for row in rows})
        },
        "status": "PASS",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    ap.add_argument("--policy", default=str(DEFAULT_POLICY))
    args = ap.parse_args()

    result = validate_registry(
        load(args.registry),
        schema=load(args.schema),
        policy=load(args.policy),
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
