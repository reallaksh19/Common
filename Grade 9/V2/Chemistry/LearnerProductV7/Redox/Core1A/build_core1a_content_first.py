#!/usr/bin/env python3
"""Content-first pagination wrapper for the Blueprint-driven Core1A renderer.

This module changes layout only. It does not contain or alter Chemistry payload.
Independent-practice blocks start on a fresh page only when the remaining frame
cannot hold a meaningful practice/reconstruction sequence, preventing a dense
penultimate page from producing a sparse tail page.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib.units import mm
from reportlab.platypus import CondPageBreak

import build_core1a as core

_original_render_object = core.render_object


def _content_first_render_object(obj, st, realized, question_ids, source_labels):
    flowables = _original_render_object(obj, st, realized, question_ids, source_labels)
    if obj.get("object_class") == "INDEPENDENT_PRACTICE":
        # Generic layout rule: avoid beginning an independent-practice/reconstruction
        # sequence in a shallow remainder. This moves existing content; it adds none.
        return [CondPageBreak(95 * mm)] + flowables
    return flowables


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(core.HERE / "out/core1a_redox_blueprint_proof.pdf"))
    parser.add_argument("--manifest", default=str(core.HERE / "out/core1a_redox_blueprint_proof.manifest.json"))
    args = parser.parse_args()
    core.render_object = _content_first_render_object
    core.build(Path(args.out), Path(args.manifest))
    print(args.out)


if __name__ == "__main__":
    main()
