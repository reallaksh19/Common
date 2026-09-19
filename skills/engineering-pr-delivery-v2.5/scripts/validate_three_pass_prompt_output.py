#!/usr/bin/env python3
"""Compatibility wrapper for the standalone three-pass prompt validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_CANONICAL = (
    Path(__file__).resolve().parents[2]
    / "three-pass-prompt-generator"
    / "validate.py"
)

_SPEC = importlib.util.spec_from_file_location(
    "standalone_three_pass_validator",
    _CANONICAL,
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"Cannot load canonical validator: {_CANONICAL}")

_MOD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MOD)

validate_text = _MOD.validate_text
main = _MOD.main
EXPECTED_PROTOCOL_REVISION = _MOD.EXPECTED_PROTOCOL_REVISION

if __name__ == "__main__":
    main()
