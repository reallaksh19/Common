#!/usr/bin/env python3
"""Deterministic Core (1) ResearchPackage builder entry point.

The implementation lives in ``build_research_package_impl.py``.  This wrapper
forces ReportLab invariant mode before the implementation imports ReportLab so
identical research input produces byte-identical Research Core PDFs, stable
artifact hashes, and therefore a stable ResearchBundleManifest package digest.
"""
from __future__ import annotations

import os

# ReportLab reads RL_invariant at configuration startup.  Set both the process
# environment and the live config so this stays deterministic when invoked as a
# script or imported after another module has already imported ReportLab.
os.environ["RL_invariant"] = "1"
from reportlab import rl_config  # noqa: E402

rl_config.invariant = 1

from build_research_package_impl import *  # noqa: E402,F401,F403


if __name__ == "__main__":
    raise SystemExit(main())
