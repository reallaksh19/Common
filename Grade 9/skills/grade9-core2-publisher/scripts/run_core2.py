#!/usr/bin/env python3
"""Core (2) Publisher entrypoint.

The implementation lives in run_core2_structured_impl.py. The pre-structure
implementation is retained as run_core2_legacy.py for compatibility testing.
"""
from run_core2_structured_impl import main

if __name__ == "__main__":
    raise SystemExit(main())
