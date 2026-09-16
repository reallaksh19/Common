#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from compile_physics_engineering_discovery import (
    ROOT,
    VOCABULARY_REL,
    validate_discovery_vocabulary_catalog,
)
from compile_physics_engineering_workbench import REGISTRY_REL, load


def main() -> None:
    registry = load(REGISTRY_REL)
    catalog = json.loads((ROOT / VOCABULARY_REL).read_text(encoding="utf-8"))
    result = validate_discovery_vocabulary_catalog(catalog, registry)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
