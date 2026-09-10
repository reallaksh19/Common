#!/usr/bin/env python3
"""Core (2) Publisher entrypoint.

The executable PublicationStructure layer lives in run_core2_structured_impl.py.
Compatibility projections preserve existing replays while exact morphology and
shared XY graph rendering remain fail-closed and independently auditable.
"""
from run_core2_patch3 import main

if __name__ == "__main__":
    raise SystemExit(main())
