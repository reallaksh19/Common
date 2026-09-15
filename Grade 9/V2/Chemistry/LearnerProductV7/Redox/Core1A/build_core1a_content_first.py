#!/usr/bin/env python3
"""Content-first pagination wrapper for the Blueprint-driven Core1A renderer.

This module changes layout only. It does not contain or alter Chemistry payload.
A reconstruction block starts on a fresh page only when the remaining frame
cannot hold a meaningful reconstruction/check sequence. Practice remains where
normal flow places it; no filler content or target page count is introduced.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib.units import mm
from reportlab.platypus import CondPageBreak

import build_core1a as core

_original_render_ttu = core.render_ttu


def _content_first_render_ttu(ttu, st):
    flowables = _original_render_ttu(ttu, st)
    # Generic layout rule: reserve contiguous space for reconstruction, hints,
    # canonical completion and verification. Existing content is moved, never padded.
    return [CondPageBreak(125 * mm)] + flowables


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(core.HERE / "out/core1a_redox_blueprint_proof.pdf"))
    parser.add_argument("--manifest", default=str(core.HERE / "out/core1a_redox_blueprint_proof.manifest.json"))
    args = parser.parse_args()
    core.render_ttu = _content_first_render_ttu
    core.build(Path(args.out), Path(args.manifest))
    print(args.out)


if __name__ == "__main__":
    main()
