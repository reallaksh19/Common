#!/usr/bin/env python3
"""Canonical Core1A entrypoint: capability-aware Core1 -> learner textbook PDF."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_math_core1a_textbook as base
import core1a_capability_authoring as capability

capability.install()

if __name__ == "__main__":
    base.main()
