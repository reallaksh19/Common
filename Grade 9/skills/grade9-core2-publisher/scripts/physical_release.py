#!/usr/bin/env python3
"""Release finalization for Core (2) PhysicalPageMap evidence.

The Study Guide renderer emits PhysicalPageMap from actual ReportLab placement.
This module promotes that evidence from diagnostics into release-blocking audit
gates and re-binds both the audit and page map into the final manifest digest.
"""
from __future__ import annotations

import sys
from pathlib import Path

GRADE9 = Path(__file__).resolve().parents[3]
CORE2 = GRADE9 / "architecture" / "core2"
sys.path.insert(0, str(CORE2))

from physical_page_custody import custody_errors, morphology_errors  # noqa: E402


def _arg_value(argv: list[str], name: str) -> str | None:
    if name not in argv:
        return None
    index = argv.index(name)
    return argv[index + 1] if index + 1 < len(argv) else None


def _artifact(legacy, role: str, path: Path) -> dict:
    return legacy.artifact(role, path, "application/json")


def finalize(original_argv: list[str], legacy, contracts: Path) -> list[str]:
    """Write release-blocking physical-page gates and refresh package custody.

    Returns the physical custody/morphology errors. The audit and manifest are
    still rewritten on failure so the rejected artifact records *why* release
    failed instead of disappearing without evidence.
    """
    out_value = _arg_value(original_argv, "--out")
    prefix = _arg_value(original_argv, "--prefix")
    if not out_value or not prefix:
        return ["cannot finalize physical-page release evidence without --out and --prefix"]

    out = Path(out_value)
    page_map_path = out / f"{prefix}_Core2_Physical_Page_Map.json"
    study_pdf_path = out / f"{prefix}_Core2_Study_Guide.pdf"
    audit_path = out / f"{prefix}_Core2_Publication_Audit.json"
    manifest_path = out / f"{prefix}_Core2_Publication_Manifest.json"

    missing = [
        path.name
        for path in (page_map_path, study_pdf_path, audit_path, manifest_path)
        if not path.exists()
    ]
    if missing:
        return ["physical-page release finalization missing artifact(s): " + ", ".join(missing)]

    page_map = legacy.load(page_map_path)
    legacy.validate_schema("physical-page-map.schema.json", page_map, contracts)

    custody = custody_errors(page_map)
    expected_pdf_sha = legacy.sha256(study_pdf_path)
    if page_map.get("pdf_sha256") != expected_pdf_sha:
        custody.append("PhysicalPageMap pdf_sha256 does not bind exact Study Guide PDF")
    morphology = morphology_errors(page_map)

    audit = legacy.load(audit_path)
    gates = audit.setdefault("gates", {})
    gates["physical_page_custody"] = not custody
    gates["physical_page_morphology"] = not morphology

    release_errors = custody + morphology
    if release_errors:
        audit["status"] = "FAIL"
        audit["release_state"] = "AUTOMATED_FAIL"
    else:
        automated_pass = all(value is True for value in gates.values())
        if automated_pass:
            audit["status"] = "PASS_WITH_WARNINGS" if audit.get("warnings") else "PASS"
            human_status = audit.get("human_visual_review", {}).get("status")
            if human_status == "PASS":
                audit["release_state"] = "HUMAN_REVIEW_PASS"
            elif human_status == "FAIL":
                audit["release_state"] = "HUMAN_REVIEW_FAIL"
            else:
                audit["release_state"] = "AUTOMATED_PASS_HUMAN_REVIEW_PENDING"
        else:
            # A non-physical automated gate already failed. Do not let successful
            # physical evidence accidentally restore a failed release.
            audit["status"] = "FAIL"
            audit["release_state"] = "AUTOMATED_FAIL"

    legacy.validate_schema("publication-audit.schema.json", audit, contracts)
    legacy.write_json(audit_path, audit)

    manifest = legacy.load(manifest_path)
    artifacts = [
        row
        for row in manifest.get("artifacts", [])
        if row.get("role") not in {"PHYSICAL_PAGE_MAP", "PUBLICATION_AUDIT"}
    ]
    artifacts.append(_artifact(legacy, "PUBLICATION_AUDIT", audit_path))
    artifacts.append(_artifact(legacy, "PHYSICAL_PAGE_MAP", page_map_path))
    manifest["artifacts"] = artifacts
    manifest["package_digest"] = legacy.package_digest(artifacts)
    legacy.validate_schema("publication-manifest.schema.json", manifest, contracts)
    legacy.write_json(manifest_path, manifest)

    if release_errors:
        return release_errors

    print("PHYSICAL_PAGE_CUSTODY_GATE = PASS")
    print("PHYSICAL_PAGE_MORPHOLOGY_GATE = PASS")
    print("PHYSICAL_PAGE_RELEASE_BINDING = PASS")
    return []
