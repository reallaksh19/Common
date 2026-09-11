#!/usr/bin/env python3
"""Final hardening patch for executable Core (2) morphology.

Measured-render compatibility is normalized here:
1. PDF text extraction can insert line breaks inside a cognitive-job sentence;
   morphology reconciliation therefore compares normalized whitespace.
2. Learner PDFs must not expose machine-only support states such as FULL,
   GUIDED, FADED, or INDEPENDENT merely to satisfy morphology QA. Arc order is
   reconciled against learner-visible role cues while exact support state stays
   authoritative in PublicationStructure/LearningDesign.
3. The generic XY_GRAPH renderer must respect the publication typography floor;
   all graph text is clamped to at least 7.5 pt during rendering.
4. The Transfer Book Markdown retains the mature human-facing heading
   ``Complete Solutions`` while the PDF/structure contract uses the canonical
   COMPLETE_SOLUTIONS section token.
"""
from __future__ import annotations

import re

import run_core2_patch2 as patch2

impl = patch2.impl
_ORIG_MORPHOLOGY = impl.morphology_evidence
_ORIG_FLOWABLE = impl.StructuredRepresentationFlowable
_ORIG_TRANSFER_MD = impl.build_transfer_markdown


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


def _ordered(text: str, markers: list[str]) -> bool:
    """Return true when learner-visible markers occur in declared order."""
    pos = -1
    upper = text.upper()
    for marker in markers:
        needle = _norm(marker).upper()
        pos = upper.find(needle, pos + 1)
        if pos < 0:
            return False
    return True


def _learner_role_marker(role: str) -> str:
    """Map machine arc roles to the cue a learner should actually see."""
    return {
        "PHYSICAL_SITUATION": "PHYSICAL SITUATION",
        "DEPICTION": "DEPICTION",
        "NOTICE": "NOTICE",
        "SAY_IN_WORDS": "SAY IN WORDS",
        "CONCEPT_INVARIANT": "CONCEPT INVARIANT",
        "MEMORY_ANCHOR": "MEMORY ANCHOR",
        "CONCEPT_HELPER": "CONCEPT HELPER",
        "BUILD_RELATION": "BUILD RELATION",
        "WHY_THIS_WORKS": "WHY THIS WORKS",
        "WORKED_EXAMPLE": "WORKED",
        "APPLICATION": "APPLICATION",
        "VARIANT_CONTRAST": "CONTRAST",
        "MISCONCEPTION_REPAIR": "MISCONCEPTION REPAIR",
        "MODEL_BOUNDARY": "MODEL BOUNDARY",
        "GUIDED_1": "GUIDED 1",
        "GUIDED_2_FADED": "GUIDED 2",
        "INDEPENDENT_TRANSFER": "INDEPENDENT TRANSFER",
        "RETRIEVAL_CHECK": "RETRIEVAL CHECK",
    }.get(role, role.replace("_", " "))


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

        # Reconcile what is actually meant to be visible to the learner. The
        # exact FULL/GUIDED/FADED/INDEPENDENT state remains machine evidence in
        # PublicationStructure; it is not a learner-facing typography token.
        out["arc_step_order_reconciliation"] = True
        out["support_progression_reconciliation"] = True
        for unit in structure["study_guide"]["learning_units"]:
            markers = [_learner_role_marker(step["role"]) for step in unit["arc_steps"]]
            if not _ordered(text, markers):
                out["arc_step_order_reconciliation"] = False

            progression = unit["support_progression"]
            visible_support_cues = {
                "worked_example": "WORKED",
                "guided_1": "GUIDED 1",
                "guided_2_faded": "GUIDED 2",
                "independent_transfer": "INDEPENDENT TRANSFER",
            }
            for key, cue in visible_support_cues.items():
                if progression[key]["state"] == "PRESENT" and _norm(cue).upper() not in text.upper():
                    out["support_progression_reconciliation"] = False

        out["page_intent_reconciliation"] = all(
            _norm(page["cognitive_job"]) in text
            for page in structure["study_guide"]["page_intents"]
        )
    return out


def build_transfer_markdown(model: dict, plan: dict) -> str:
    text = _ORIG_TRANSFER_MD(model, plan)
    return text.replace("# COMPLETE SOLUTIONS", "# Complete Solutions")


def main() -> int:
    impl.StructuredRepresentationFlowable = TypographySafeRepresentationFlowable
    impl.morphology_evidence = morphology_evidence
    impl.build_transfer_markdown = build_transfer_markdown
    return patch2.main()


if __name__ == "__main__":
    raise SystemExit(main())
