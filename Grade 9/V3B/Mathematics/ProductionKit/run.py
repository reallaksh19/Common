#!/usr/bin/env python3
"""Mathematics-only entry gate onto the shared V3B production runtime."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Shared"))
from v3b.cli import main

if __name__ == "__main__":
    raise SystemExit(main(expected_subject="Mathematics"))
