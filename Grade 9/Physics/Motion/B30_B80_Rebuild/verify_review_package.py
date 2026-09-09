#!/usr/bin/env python3
"""Fail when a reviewed model, PDF, audit, summary, or manifest drifts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from refresh_file_manifest import EXCLUDED, MANIFEST_PATH, PACKAGE_ROOT, REPOSITORY_ROOT, tracked_paths

JsonObject = dict[str, Any]
PUBLICATION_ROOT = REPOSITORY_ROOT / 'Grade 9/skills/grade9-physics-publication'
ARTIFACTS = {
    'Motion_B30_Rebuilt': 'motion_B30_v2.json',
    'Motion_B80_Rebuilt': 'motion_B80_v2.json',
    'Motion_Optional_Hint_Practice': 'motion_question_bank_v2.json',
}


def _load(path: Path) -> JsonObject:
    """Load one UTF-8 JSON object."""
    return json.loads(path.read_text(encoding='utf-8'))


def _sha256(path: Path) -> str:
    """Return a lowercase SHA-256 for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_audits() -> tuple[dict[str, JsonObject], list[str]]:
    """Check every model/PDF pair against its committed audit."""
    audits: dict[str, JsonObject] = {}
    failures: list[str] = []
    for stem, model_name in ARTIFACTS.items():
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
        audit = _load(audit_path)
        audits[stem] = audit
        if audit.get('model_sha256') != _sha256(model_path):
            failures.append(f'{stem}: audit model_sha256 does not match current model')
        if audit.get('pdf_sha256') != _sha256(pdf_path):
            failures.append(f'{stem}: audit pdf_sha256 does not match current PDF')
        if audit.get('broken_links') or audit.get('text_overlap_findings') or audit.get('outside_page'):
            failures.append(f'{stem}: audit contains blocking render findings')
    return audits, failures


def _summary_failures(audits: dict[str, JsonObject]) -> list[str]:
    """Require both human-facing package summaries to carry the exact audits."""
    packaging = _load(PACKAGE_ROOT / 'Packaging_Validation.json')
    rebuild = _load(PACKAGE_ROOT / 'Physics_Rebuild_Audit.json')
    failures: list[str] = []
    if packaging.get('status') != 'PASS':
        failures.append('Packaging_Validation.json status is not PASS')
    if packaging.get('pdf_audits') != audits:
        failures.append('Packaging_Validation.json pdf_audits drifted from artifact audits')
    if rebuild.get('artifacts') != audits:
        failures.append('Physics_Rebuild_Audit.json artifacts drifted from artifact audits')
    return failures


def _manifest_failures() -> list[str]:
    """Require complete scope coverage and exact bytes for every manifest entry."""
    manifest = _load(MANIFEST_PATH)
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
        if record.get('bytes') != len(data) or record.get('sha256') != hashlib.sha256(data).hexdigest():
            failures.append(f'manifest bytes/hash mismatch: {relative_path}')
    return failures


def main() -> int:
    """Print a truthful package-integrity result and return a blocking exit code."""
    audits, failures = _artifact_audits()
    failures.extend(_summary_failures(audits))
    failures.extend(_manifest_failures())
    result = {
        'status': 'PASS' if not failures else 'FAIL',
        'artifacts_checked': len(audits),
        'manifest_files_checked': len(_load(MANIFEST_PATH)['files']),
        'failures': failures,
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
