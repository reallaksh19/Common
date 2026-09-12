"""Python import alias for the canonical `Grade 4/` product tree.

Filesystem ownership remains under `Grade 4/V2/...`. This package only gives
Python a whitespace-safe import root: `Grade4.V2...`.
"""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "Grade 4")]
