#!/usr/bin/env python3
"""Independent Core (2) package validator entrypoint.

The base validator proves structure/content/page-map custody. This entrypoint
promotes physical-page custody and morphology to release-blocking properties:
the exact PhysicalPageMap is re-checked independently and both corresponding
PublicationAudit gates must be true.
"""
from __future__ import annotations

from pathlib import Path

import validate_core2_package_patch2 as base

_BASE_VALIDATE_STRUCTURE_PACKAGE = base.validate_structure_package


def _release_validate_structure_package(argv: list[str]) -> int:
    rc = _BASE_VALIDATE_STRUCTURE_PACKAGE(argv)
    if rc != 0:
        return rc

    directory = Path(base.impl._arg_value(argv, "--dir"))
    prefix = base.impl._arg_value(argv, "--prefix")
    plan = base.impl.load(directory / f"{prefix}_Core2_Publication_Plan.json")
    if not plan.get("requested_products", {}).get("study_guide", False):
        return 0

    audit = base.impl.load(directory / f"{prefix}_Core2_Publication_Audit.json")
    page_map = base.impl.load(directory / f"{prefix}_Core2_Physical_Page_Map.json")
    errors: list[str] = []

    gates = audit.get("gates", {})
    for gate in ("physical_page_custody", "physical_page_morphology"):
        if gates.get(gate) is not True:
            errors.append(f"missing/failed release audit gate: {gate}")

    # Re-run the release checks rather than trusting the producer's booleans.
    errors.extend("PhysicalPageMap release: " + err for err in base.custody_errors(page_map))
    errors.extend("PhysicalPageMap release: " + err for err in base.morphology_errors(page_map))

    if audit.get("status") not in {"PASS", "PASS_WITH_WARNINGS"}:
        errors.append(f"publication audit is not releasable: status={audit.get('status')!r}")
    if audit.get("release_state") not in {
        "AUTOMATED_PASS_HUMAN_REVIEW_PENDING",
        "HUMAN_REVIEW_PASS",
    }:
        errors.append(f"publication audit release_state is not releasable: {audit.get('release_state')!r}")

    if errors:
        print("CORE2_PHYSICAL_RELEASE_PACKAGE = FAIL")
        for error in errors:
            print("- " + error)
        return 1

    print("PHYSICAL_PAGE_CUSTODY_GATE = PASS")
    print("PHYSICAL_PAGE_MORPHOLOGY_GATE = PASS")
    print("CORE2_PHYSICAL_RELEASE_PACKAGE = PASS")
    return 0


def main() -> int:
    # base.main() installs its module-global validator into the structured
    # implementation; replace that module-global with the release wrapper.
    base.validate_structure_package = _release_validate_structure_package
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
