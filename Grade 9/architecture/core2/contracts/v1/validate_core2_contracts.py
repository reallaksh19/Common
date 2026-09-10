#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent
REP_REG = ROOT.parents[1] / "representation" / "capabilities.v1.json"


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    errors: list[str] = []
    schemas = {}
    for path in sorted(ROOT.glob("*.schema.json")):
        try:
            schema = load(path)
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")

    required = {
        "badge.schema.json",
        "representation-instance.schema.json",
        "publication-plan.schema.json",
        "study-guide.schema.json",
        "transfer-book.schema.json",
        "publication-audit.schema.json",
        "publication-manifest.schema.json",
    }
    missing = sorted(required - schemas.keys())
    if missing:
        errors.append("missing schemas: " + ", ".join(missing))

    base_uri = ROOT.as_uri().rstrip("/") + "/"
    store = {}
    for name, schema in schemas.items():
        sid = schema.get("$id", name)
        store[name] = schema
        store[sid] = schema
        store[base_uri + name] = schema
        store[base_uri + sid] = schema

    if "publication-plan.schema.json" in schemas:
        try:
            RefResolver(base_uri=base_uri, referrer=schemas["publication-plan.schema.json"], store=store)
        except Exception as exc:
            errors.append(f"publication-plan ref resolution: {exc}")

    try:
        registry = load(REP_REG)
        rows = registry.get("capabilities", [])
        ids = [r.get("capability_id") for r in rows]
        types = [(r.get("representation_type"), tuple(r.get("subjects", []))) for r in rows]
        if len(ids) != len(set(ids)):
            errors.append("duplicate representation capability_id")
        if not any(r.get("status") == "IMPLEMENTED" for r in rows):
            errors.append("representation registry has no IMPLEMENTED capability")
        if any(not r.get("representation_type") for r in rows):
            errors.append("representation capability missing representation_type")
        if len(types) != len(set(types)):
            errors.append("duplicate representation_type + subjects capability declaration")
    except Exception as exc:
        errors.append(f"representation registry: {exc}")

    if errors:
        print("CORE2_CONTRACTS_V1 = FAIL")
        for err in errors:
            print("- " + err)
        return 1

    print(f"CORE2_CONTRACTS_V1 = PASS ({len(schemas)} schemas)")
    print("SHARED_REPRESENTATION_REGISTRY = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
