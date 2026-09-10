#!/usr/bin/env python3
"""Core (2) Publisher entrypoint.

The executable PublicationStructure layer lives in run_core2_structured_impl.py.
run_core2_patch2.py adds the legacy-replay compatibility projection while
preserving unique publication item identity per arc role.
"""
from run_core2_patch2 import main

if __name__ == "__main__":
    raise SystemExit(main())
