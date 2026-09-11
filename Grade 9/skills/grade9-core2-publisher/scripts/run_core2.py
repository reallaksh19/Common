#!/usr/bin/env python3
"""Core (2) Publisher entrypoint.

Two execution modes are intentionally supported:

* ENGINEERING_REPLAY keeps the deterministic cold-start projection used to
  falsify contracts and renderer mechanics.
* MATURE_LEARNER_PRODUCT requires authored LearningDesign, StudyGuide semantic
  content and PublicationStructure, and binds LearningDesign into the exact
  publication package.

Both modes emit a PhysicalPageMap for Study Guides from ReportLab placement
evidence. The mature path fails closed rather than silently falling back to
generic connective prose.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import learner_layout
import mature_product as mature
import physical_release
import run_core2_patch4 as publisher


def _learner_surface_inspector(original, target: dict):
    """Keep reopened-PDF QA focused on learner-visible contract markers.

    Research/package/learner/publication identifiers are machine-custody data.
    They are validated through the target, semantic models, manifest hashes and
    PhysicalPageMap and therefore must not be required as printed learner text.
    """
    internal_ids = {
        value
        for value in (
            target.get("research_bundle_id"),
            target.get("research_package_digest"),
            target.get("learner_profile_id"),
            target.get("publication_target_id"),
        )
        if value
    }

    def inspect(path, role, required_text, notation_probes, check_answer_separation=False):
        if role == "STUDY_GUIDE_PDF":
            required_text = [text for text in required_text if text not in internal_ids]
        return original(path, role, required_text, notation_probes, check_answer_separation)

    return inspect


def _norm(text: object) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


def _ordered(text: str, markers: list[str]) -> bool:
    haystack = _norm(text).upper()
    cursor = 0
    for marker in markers:
        normalized = _norm(marker).upper()
        pos = haystack.find(normalized, cursor)
        if pos < 0:
            return False
        cursor = pos + len(normalized)
    return True


def _learner_step_marker(step: dict) -> str:
    """Return the cue that should be visible, not the machine-only role token."""
    if step.get("learner_visible_heading"):
        return step["learner_visible_heading"]
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
    }.get(step.get("role"), step.get("role", "").replace("_", " "))


def _learner_surface_morphology(original):
    """Adapt structure morphology checks to learner-visible presentation.

    PublicationStructure retains exact machine roles/support states. The PDF is
    allowed to use concise learner cues such as ``WORKED`` and ``GUIDED 2``
    rather than printing internal tokens such as ``WORKED EXAMPLE`` or
    ``GUIDED 2 FADED``. Only learner-text marker checks are recomputed; all
    other morphology evidence remains delegated unchanged.
    """

    def morphology(structure, study_pdf, transfer_pdf):
        out = original(structure, study_pdf, transfer_pdf)
        if study_pdf and study_pdf.exists():
            doc = publisher.impl.legacy.fitz.open(study_pdf)
            text = _norm("\n".join(page.get_text() for page in doc))
            doc.close()

            arc_ok = True
            support_ok = True
            for unit in structure["study_guide"]["learning_units"]:
                markers = [_learner_step_marker(step) for step in unit["arc_steps"]]
                if not _ordered(text, markers):
                    arc_ok = False

                progression = unit["support_progression"]
                present_to_marker = {
                    "worked_example": "WORKED",
                    "guided_1": "GUIDED 1",
                    "guided_2_faded": "GUIDED 2",
                    "independent_transfer": "INDEPENDENT TRANSFER",
                }
                upper_text = text.upper()
                for key, marker in present_to_marker.items():
                    if progression[key]["state"] == "PRESENT" and marker.upper() not in upper_text:
                        support_ok = False

            out["arc_step_order_reconciliation"] = arc_ok
            out["support_progression_reconciliation"] = support_ok
        return out

    return morphology


def main() -> int:
    original_argv = list(sys.argv)
    target_value = mature.arg_value(original_argv, "--target")
    target = mature.load(Path(target_value)) if target_value else {}
    design_value = mature.arg_value(original_argv, "--learning-design")
    design = mature.load(Path(design_value)) if design_value else None

    errors = mature.preflight_errors(original_argv, target, design)
    if errors:
        return mature.print_errors("CORE2_MATURE_PRODUCT_PREFLIGHT", errors)

    if design is not None:
        errors = mature.validate_learning_design_contract(design)
        if errors:
            return mature.print_errors("CORE2_LEARNING_DESIGN_CONTRACT", errors)

    mature_mode = mature.mature_requested(original_argv, design)
    authored_study = None
    original_study_builder = publisher.impl._ORIG_BUILD_STUDY_MODEL
    original_study_renderer = publisher.impl.render_study_pdf
    original_pdf_inspector = publisher.impl.legacy.inspect_pdf
    original_impl_morphology = publisher.impl.morphology_evidence
    original_patch3_morphology = publisher.patch3.morphology_evidence
    contracts = Path(__file__).resolve().parents[3] / "architecture" / "core2" / "contracts" / "v1"

    if mature_mode:
        study_value = mature.arg_value(original_argv, "--study-model")
        if study_value:
            authored_study = mature.load(Path(study_value))
            publisher.impl._ORIG_BUILD_STUDY_MODEL = mature.make_study_builder(
                authored_study,
                design,
                contracts,
                publisher.impl.legacy,
            )

    publisher.impl.render_study_pdf = learner_layout.make_study_renderer(publisher.impl)
    publisher.impl.legacy.inspect_pdf = _learner_surface_inspector(original_pdf_inspector, target)

    # run_core2_patch3.main() installs its own module-global morphology_evidence
    # into the structured implementation immediately before delegation. Patch
    # that owning module-global function, not only impl.morphology_evidence, or
    # the learner-aware checker is overwritten during startup.
    learner_morphology = _learner_surface_morphology(original_patch3_morphology)
    publisher.patch3.morphology_evidence = learner_morphology
    publisher.impl.morphology_evidence = learner_morphology

    sys.argv = mature.cleaned_publisher_argv(original_argv)
    try:
        rc = publisher.main()
    finally:
        sys.argv = original_argv
        publisher.impl._ORIG_BUILD_STUDY_MODEL = original_study_builder
        publisher.impl.render_study_pdf = original_study_renderer
        publisher.impl.legacy.inspect_pdf = original_pdf_inspector
        publisher.patch3.morphology_evidence = original_patch3_morphology
        publisher.impl.morphology_evidence = original_impl_morphology
    if rc != 0:
        return rc

    # Bind authored LearningDesign first so physical release finalization writes
    # the final audit against the complete artifact set and then recomputes the
    # authoritative manifest/package digest.
    if design is not None:
        errors = mature.finalize_learning_design(
            original_argv,
            design,
            contracts,
            publisher.impl.legacy,
        )
        if errors:
            return mature.print_errors("CORE2_LEARNING_DESIGN_PACKAGE", errors)

    errors = physical_release.finalize(
        original_argv,
        publisher.impl.legacy,
        contracts,
    )
    if errors:
        return mature.print_errors("CORE2_PHYSICAL_PAGE_RELEASE", errors)

    if mature_mode:
        print("CORE2_MATURE_PRODUCT = PASS")
    else:
        print("CORE2_EXECUTION_MODE = ENGINEERING_REPLAY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
