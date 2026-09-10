#!/usr/bin/env python3
"""Core (2) Publisher entrypoint.

Two execution modes are intentionally supported:

* ENGINEERING_REPLAY keeps the deterministic cold-start projection used to
  falsify contracts and renderer mechanics.
* MATURE_LEARNER_PRODUCT requires authored LearningDesign, StudyGuide semantic
  content and PublicationStructure, and binds LearningDesign into the exact
  publication package.

Both modes now emit a PhysicalPageMap for Study Guides from ReportLab placement
evidence. The mature path fails closed rather than silently falling back to
generic connective prose.
"""
from __future__ import annotations

import sys
from pathlib import Path

import mature_product as mature
import physical_page_runtime as physical
import run_core2_patch4 as publisher


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

    publisher.impl.render_study_pdf = physical.make_study_renderer(publisher.impl)
    sys.argv = mature.cleaned_publisher_argv(original_argv)
    try:
        rc = publisher.main()
    finally:
        sys.argv = original_argv
        publisher.impl._ORIG_BUILD_STUDY_MODEL = original_study_builder
        publisher.impl.render_study_pdf = original_study_renderer
    if rc != 0:
        return rc

    errors = physical.finalize_page_map(
        original_argv,
        publisher.impl.legacy,
        contracts,
    )
    if errors:
        return mature.print_errors("CORE2_PHYSICAL_PAGE_MAP_PACKAGE", errors)

    if design is not None:
        errors = mature.finalize_learning_design(
            original_argv,
            design,
            contracts,
            publisher.impl.legacy,
        )
        if errors:
            return mature.print_errors("CORE2_LEARNING_DESIGN_PACKAGE", errors)

    if mature_mode:
        print("CORE2_MATURE_PRODUCT = PASS")
    else:
        print("CORE2_EXECUTION_MODE = ENGINEERING_REPLAY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
