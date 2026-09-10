#!/usr/bin/env python3
"""Core (2) Publisher entrypoint.

The executable PublicationStructure layer lives in run_core2_structured_impl.py.
Compatibility projections preserve existing replays, route every selected
representation through the executable structure, and keep morphology/XY graph
rendering fail-closed and independently auditable.
"""
from run_core2_patch4 import main

if __name__ == "__main__":
    raise SystemExit(main())
