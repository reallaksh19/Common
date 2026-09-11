#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "physical-page-map.schema.json"


def main() -> int:
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        print("CORE2_PHYSICAL_PAGE_MAP_SCHEMA = FAIL")
        print(f"- {exc}")
        return 1
    print("CORE2_PHYSICAL_PAGE_MAP_SCHEMA = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
