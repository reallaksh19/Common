#!/usr/bin/env python3
"""Fail when reviewed dependencies, evidence, artifacts, summaries, or manifest drift."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from refresh_file_manifest import EXCLUDED, MANIFEST_PATH, PACKAGE_ROOT, REPOSITORY_ROOT, tracked_paths
from review_evidence import (
    ARTIFACT_MODELS,
    EVIDENCE_PATH,
    PUBLICATION_ROOT,
    VISUAL_EVIDENCE_PATH,
    focused_checks,
    load_json,
    machine_evidence_failures,
    sha256,
    visual_evidence_failures,
    visual_projection,
)

JsonObject = dict[str, Any]


def _artifact_audits() -> tuple[dict[str, JsonObject], list[str]]:
    """Check every model/PDF pair against its committed audit."""
    audits: dict[str, JsonObject] = {}
    failures: list[str] = []
    for stem, model_name in ARTIFACT_MODELS.items():
        model_path = PUBLICATION_ROOT / 'examples' / model_name
        pdf_path = PACKAGE_ROOT / f'{stem}.pdf'
        audit_path = PACKAGE_ROOT / f'{stem}.audit.json'
        layout_path = PACKAGE_ROOT / f'{stem}.layout.json'
        required_paths = (model_path, pdf_path, audit_path, layout_path)
        missing_paths = [path for path in required_paths if not path.is_file()]
        failures.extend(
            f'missing artifact file: {path.relative_to(REPOSITORY_ROOT)}'
            for path in missing_paths
        )
        if missing_paths:
            continue
        audit = load_json(audit_path)
        audits[stem] = audit
        if audit.get('model_sha256') != sha256(model_path):
            failures.append(f'{stem}: audit model_sha256 does not match current model')
        if audit.get('pdf_sha256') != sha256(pdf_path):
            failures.append(f'{stem}: audit pdf_sha256 does not match current PDF')
        if audit.get('broken_links') or audit.get('text_overlap_findings') or audit.get('outside_page'):
            failures.append(f'{stem}: audit contains blocking render findings')
    return audits, failures


def _summary_failures(
    audits: dict[str, JsonObject],
    evidence: JsonObject,
    visual: JsonObject,
    visual_failures: list[str],
) -> list[str]:
    """Require exact evidence projections in both human-facing summaries."""
    packaging = load_json(PACKAGE_ROOT / 'Packaging_Validation.json')
    rebuild = load_json(PACKAGE_ROOT / 'Physics_Rebuild_Audit.json')
    evidence_identity = {
        'file': EVIDENCE_PATH.name,
        'sha256': sha256(EVIDENCE_PATH),
        'generated_at_utc': evidence.get('generated_at_utc'),
        'status': evidence.get('status'),
    }
    checks = focused_checks(evidence)
    visual_summary = visual_projection(visual, visual_failures)
    failures: list[str] = []
    if packaging.get('status') != 'PASS':
        failures.append('Packaging_Validation.json status is not PASS')
    if packaging.get('machine_evidence') != evidence_identity:
        failures.append('Packaging_Validation.json machine evidence identity drifted')
    if packaging.get('focused_checks') != checks:
        failures.append('Packaging_Validation.json focused checks are not an exact evidence projection')
    if packaging.get('pdf_audits') != audits:
        failures.append('Packaging_Validation.json pdf_audits drifted from artifact audits')
    if packaging.get('codex_visual_review') != visual_summary:
        failures.append('Packaging_Validation.json visual review drifted from visual evidence')
    if rebuild.get('machine_evidence') != evidence_identity:
        failures.append('Physics_Rebuild_Audit.json machine evidence identity drifted')
    if rebuild.get('tests') != checks:
        failures.append('Physics_Rebuild_Audit.json tests are not an exact evidence projection')
    if rebuild.get('artifacts') != audits:
        failures.append('Physics_Rebuild_Audit.json artifacts drifted from artifact audits')
    manual = rebuild.get('manual_review', {})
    if manual.get('codex_visual_review') != visual_summary:
        failures.append('Physics_Rebuild_Audit.json visual review drifted from visual evidence')
    if manual.get('known_package_integrity_blockers_remaining') != len(visual_failures):
        failures.append('Physics_Rebuild_Audit.json blocker count is not derived from current evidence')
    return failures


def _manifest_failures() -> list[str]:
    """Require complete declared scope and exact bytes for every manifest entry."""
    manifest = load_json(MANIFEST_PATH)
    records = {record['path']: record for record in manifest['files']}
    expected = set(tracked_paths())
    failures: list[str] = []
    if set(manifest.get('excluded', [])) != EXCLUDED:
        failures.append('FILE_MANIFEST.json exclusions changed')
    if set(records) != expected:
        missing = sorted(expected - records.keys())
        stale = sorted(records.keys() - expected)
        failures.append(f'FILE_MANIFEST.json scope drift: missing={missing}, stale={stale}')
    for relative_path, record in records.items():
        path = REPOSITORY_ROOT / relative_path
        if not path.is_file():
            failures.append(f'manifest path missing: {relative_path}')
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if record.get('bytes') != len(data) or record.get('sha256') != digest:
            failures.append(f'manifest bytes/hash mismatch: {relative_path}')
    return failures


def main() -> int:
    """Print a truthful package-integrity result and return a blocking exit code."""
    audits, failures = _artifact_audits()
    evidence = load_json(EVIDENCE_PATH)
    visual = load_json(VISUAL_EVIDENCE_PATH)
    machine_failures = machine_evidence_failures(evidence)
    current_visual_failures = visual_evidence_failures(visual, audits)
    failures.extend(machine_failures)
    failures.extend(current_visual_failures)
    failures.extend(_summary_failures(audits, evidence, visual, current_visual_failures))
    failures.extend(_manifest_failures())
    result = {
        'status': 'PASS' if not failures else 'FAIL',
        'commands_checked': len(evidence.get('checks', [])),
        'artifacts_checked': len(audits),
        'visual_pages_checked': visual.get('pages_reviewed', 0),
        'manifest_files_checked': len(load_json(MANIFEST_PATH)['files']),
        'failures': failures,
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
