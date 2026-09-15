#!/usr/bin/env python3
"""Content-first pagination wrapper for the Blueprint-driven Core1A renderer.

This module changes layout only. It does not contain or alter Chemistry payload.
A reconstruction block starts on a fresh page only when the remaining frame
cannot hold a meaningful reconstruction/check sequence. Titled learner blocks
and misconception/repair pairs remain visually intact across page boundaries.
No filler content or target page count is introduced.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib.units import mm
from reportlab.platypus import CondPageBreak, KeepTogether

import build_core1a as core

_original_box = core.box
_original_render_object = core.render_object
_original_render_ttu = core.render_ttu


def _content_first_box(*args, **kwargs):
    # A titled box is one learner-facing unit. If it fits on a fresh page,
    # never strand the title row at the foot of the preceding page.
    return KeepTogether([_original_box(*args, **kwargs)])


def _content_first_render_object(obj, st, realized, question_ids, source_labels):
    flowables = _original_render_object(obj, st, realized, question_ids, source_labels)
    if obj.get("object_class") == "MISCONCEPTION_REPAIR":
        # The wrong model and its repair are a single contrast. Keep the pair
        # together rather than splitting "Common wrong move" from "Repair".
        return [KeepTogether(flowables)]
    return flowables


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
    core.box = _content_first_box
    core.render_object = _content_first_render_object
    core.render_ttu = _content_first_render_ttu
    core.build(Path(args.out), Path(args.manifest))
    print(args.out)


if __name__ == "__main__":
    main()
