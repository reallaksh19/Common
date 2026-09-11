#!/usr/bin/env python3
"""Fail-closed Core (2) publisher preflight for the frozen v1 hand-off.

This is intentionally downstream of PR #160's schema/handoff validation. It does
not perform subject research and does not replace validate_handoff.py. It checks
that an already contract-valid package is actually ready to enter learner
publication planning.

Required inputs:
  --bundle    ResearchBundle JSON
  --manifest  ResearchBundleManifest JSON
  --learner   LearnerProfile JSON
  --target    PublicationTarget JSON

Exit codes:
  0  Core (2) publisher preflight PASS
  1  publication-blocking mismatch/readiness failure
  2  input file/JSON error
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MATERIAL_CLASSES = {
    "MATERIAL_CLAIM",
    "MATERIAL_CONDITION",
    "MATERIAL_EXAMPLE",
    "MATERIAL_REPRESENTATION",
    "MATERIAL_QUESTION",
    "MATERIAL_SOLUTION_METHOD",
    "MATERIAL_EXAM_FACT",
}


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--learner", type=Path, required=True)
    p.add_argument("--target", type=Path, required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        bundle = load(args.bundle)
        manifest = load(args.manifest)
        learner = load(args.learner)
        target = load(args.target)
    except Exception as exc:
        print("CORE2_PREFLIGHT = BLOCKED_INPUT")
        print(f"- {exc}")
        return 2

    failures: list[str] = []

    # A schema-valid research-in-progress package is not publishable.
    if bundle.get("status") != "READY_FOR_PUBLISH":
        failures.append(
            f"ResearchBundle.status must be READY_FOR_PUBLISH; got {bundle.get('status')!r}"
        )

    bundle_id = bundle.get("research_bundle_id")
    evidence_version = bundle.get("evidence_version")

    if manifest.get("research_bundle_id") != bundle_id:
        failures.append("ResearchBundleManifest.research_bundle_id does not match ResearchBundle")
    if manifest.get("evidence_version") != evidence_version:
        failures.append("ResearchBundleManifest.evidence_version does not match ResearchBundle")
    if target.get("research_bundle_id") != bundle_id:
        failures.append("PublicationTarget.research_bundle_id does not match ResearchBundle")
    if target.get("research_package_digest") != manifest.get("package_digest"):
        failures.append(
            "PublicationTarget.research_package_digest does not match ResearchBundleManifest.package_digest"
        )
    if target.get("learner_profile_id") != learner.get("learner_profile_id"):
        failures.append("PublicationTarget.learner_profile_id does not match LearnerProfile")

    blocking_gaps = [
        item
        for item in bundle.get("unresolved_items", [])
        if item.get("blocking") is True
    ]
    if blocking_gaps:
        failures.append(f"ResearchBundle contains {len(blocking_gaps)} blocking unresolved item(s)")

    # Publisher-specific readiness rule: material learner claims must be settled.
    unverified_material = []
    for claim in bundle.get("research_claims", []):
        if claim.get("traceability_class") in MATERIAL_CLASSES and claim.get("verification_status") != "VERIFIED":
            unverified_material.append(
                f"{claim.get('claim_id', '<missing-id>')}:{claim.get('verification_status')}"
            )
    if unverified_material:
        failures.append(
            "material Research Claims are not VERIFIED: " + ", ".join(unverified_material)
        )

    # READY_FOR_PUBLISH must also have complete material human-view reconciliation.
    rec = manifest.get("material_view_reconciliation") or {}
    if rec.get("bundle_to_md_coverage") != 1:
        failures.append("ResearchBundleManifest.bundle_to_md_coverage must equal 1")
    if rec.get("bundle_to_pdf_coverage") != 1:
        failures.append("ResearchBundleManifest.bundle_to_pdf_coverage must equal 1")
    if rec.get("unmapped_md_material_claims") != 0:
        failures.append("ResearchBundleManifest.unmapped_md_material_claims must equal 0")
    if rec.get("unmapped_pdf_material_claims") != 0:
        failures.append("ResearchBundleManifest.unmapped_pdf_material_claims must equal 0")

    requested = target.get("requested_products") or {}
    if not (requested.get("study_guide") or requested.get("transfer_book")):
        failures.append("PublicationTarget must request at least one learner product")

    purpose = target.get("purpose") or {}
    if purpose.get("type") in {
        "COMPETITIVE_FOUNDATION",
        "COMPETITIVE_EXAM",
        "MOCK_EXAM_PREPARATION",
    } and not purpose.get("exam_profile_id"):
        failures.append("competitive PublicationTarget requires purpose.exam_profile_id")

    if failures:
        print("CORE2_PREFLIGHT = FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CORE2_PREFLIGHT = PASS")
    print("RESEARCH_BUNDLE_READY_FOR_PUBLISH = PASS")
    print("RESEARCH_PACKAGE_DIGEST_BINDING = PASS")
    print("LEARNER_TARGET_BINDING = PASS")
    print("BLOCKING_RESEARCH_GAPS = 0")
    print("MATERIAL_RESEARCH_CLAIMS_VERIFIED = PASS")
    print("MATERIAL_VIEW_RECONCILIATION = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
