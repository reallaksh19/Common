#!/usr/bin/env python3
"""Final hardening patch for executable Core (2) morphology.

Two measured-render details are normalized here:
1. PDF text extraction can insert line breaks inside a cognitive-job sentence;
   morphology reconciliation therefore compares normalized whitespace.
2. The generic XY_GRAPH renderer must respect the publication typography floor;
   all graph text is clamped to at least 7.5 pt during rendering.
"""
from __future__ import annotations

import re

import run_core2_patch2 as patch2

impl = patch2.impl
_ORIG_MORPHOLOGY = impl.morphology_evidence
_ORIG_FLOWABLE = impl.StructuredRepresentationFlowable


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


class TypographySafeRepresentationFlowable(_ORIG_FLOWABLE):
    def _draw_xy(self):
        canvas = self.canv
        original = canvas.setFont

        def clamped(name, size, *args, **kwargs):
            return original(name, max(7.5, float(size)), *args, **kwargs)

        canvas.setFont = clamped
        try:
            return super()._draw_xy()
        finally:
            canvas.setFont = original


def morphology_evidence(structure: dict, study_pdf, transfer_pdf):
    out = _ORIG_MORPHOLOGY(structure, study_pdf, transfer_pdf)
    if study_pdf and study_pdf.exists():
        doc = impl.legacy.fitz.open(study_pdf)
        text = _norm("\n".join(page.get_text() for page in doc))
        doc.close()
        out["page_intent_reconciliation"] = all(
            _norm(page["cognitive_job"]) in text
            for page in structure["study_guide"]["page_intents"]
        )
    return out


def main() -> int:
    impl.StructuredRepresentationFlowable = TypographySafeRepresentationFlowable
    impl.morphology_evidence = morphology_evidence
    return patch2.main()


if __name__ == "__main__":
    raise SystemExit(main())
