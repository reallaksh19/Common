#!/usr/bin/env python3
"""Shared validation for machine checks and human visual-review evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from refresh_file_manifest import PACKAGE_ROOT, REPOSITORY_ROOT, evidence_basis_paths

JsonObject = dict[str, Any]
ARTIFACT_MODELS = {
    'Motion_B30_Rebuilt': 'motion_B30_v2.json',
    'Motion_B80_Rebuilt': 'motion_B80_v2.json',
    'Motion_Optional_Hint_Practice': 'motion_question_bank_v2.json',
}
PUBLICATION_ROOT = REPOSITORY_ROOT / 'Grade 9/skills/grade9-physics-publication'
EVIDENCE_PATH = PACKAGE_ROOT / 'review_evidence.json'
VISUAL_EVIDENCE_PATH = PACKAGE_ROOT / 'visual_review_evidence.json'


def load_json(path: Path) -> JsonObject:
    """Load one UTF-8 JSON object from ``path``."""
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 of the exact bytes at ``path``."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_hashes(relative_paths: list[str]) -> dict[str, str]:
    """Map repository-relative paths to hashes, raising when any input is absent."""
    return {relative_path: sha256(REPOSITORY_ROOT / relative_path) for relative_path in relative_paths}


def artifact_paths() -> list[str]:
    """Return model, PDF, layout, and audit paths for all three learner artifacts."""
    paths: list[str] = []
    for stem, model_name in ARTIFACT_MODELS.items():
        paths.extend(
            (
                f'Grade 9/skills/grade9-physics-publication/examples/{model_name}',
                f'Grade 9/Physics/Motion/B30_B80_Rebuild/{stem}.pdf',
                f'Grade 9/Physics/Motion/B30_B80_Rebuild/{stem}.layout.json',
                f'Grade 9/Physics/Motion/B30_B80_Rebuild/{stem}.audit.json',
            )
        )
    return paths


def machine_evidence_failures(evidence: JsonObject) -> list[str]:
    """Check command results and bind them to the current dependency/artifact bytes."""
    failures: list[str] = []
    checks = evidence.get('checks')
    if not isinstance(checks, list) or not checks:
        return ['review_evidence.json has no executable checks']
    if evidence.get('status') != 'PASS':
        failures.append('review_evidence.json status is not PASS')
    for check in checks:
        check_id = str(check.get('id', '<missing>'))
        if check.get('status') != 'PASS' or check.get('exit_code') != 0:
            failures.append(f'{check_id}: recorded command did not pass')
        stdout = str(check.get('stdout', ''))
        stderr = str(check.get('stderr', ''))
        if hashlib.sha256(stdout.encode('utf-8')).hexdigest() != check.get('stdout_sha256'):
            failures.append(f'{check_id}: stdout hash mismatch')
        if hashlib.sha256(stderr.encode('utf-8')).hexdigest() != check.get('stderr_sha256'):
            failures.append(f'{check_id}: stderr hash mismatch')
    current_basis = repository_hashes(evidence_basis_paths())
    if evidence.get('basis_hashes') != current_basis:
        failures.append('review evidence is stale for the current dependency bytes')
    current_artifacts = repository_hashes(artifact_paths())
    if evidence.get('artifact_hashes') != current_artifacts:
        failures.append('review evidence is stale for the current model/PDF/layout/audit bytes')
    return failures


def visual_evidence_failures(visual: JsonObject, audits: dict[str, JsonObject]) -> list[str]:
    """Require a 200-DPI all-page review bound to current audited PDF hashes."""
    failures: list[str] = []
    if visual.get('result') != 'PASS':
        failures.append('visual review result is not PASS')
    if not isinstance(visual.get('dpi'), int) or visual['dpi'] < 200:
        failures.append('visual review DPI is below 200')
    expected_pages = sum(int(audit.get('pages', 0)) for audit in audits.values())
    if visual.get('pages_reviewed') != expected_pages:
        failures.append('visual review does not attest to every audited page')
    pdf_records = visual.get('pdfs')
    if not isinstance(pdf_records, list):
        return failures + ['visual review has no PDF records']
    records = {str(record.get('stem')): record for record in pdf_records}
    if set(records) != set(ARTIFACT_MODELS):
        failures.append('visual review PDF set does not match the learner artifacts')
    for stem in ARTIFACT_MODELS:
        record = records.get(stem)
        audit = audits.get(stem)
        if record is None or audit is None:
            continue
        pdf_path = PACKAGE_ROOT / f'{stem}.pdf'
        if record.get('sha256') != sha256(pdf_path):
            failures.append(f'{stem}: visual review PDF hash is stale')
        if record.get('sha256') != audit.get('pdf_sha256'):
            failures.append(f'{stem}: visual review hash differs from artifact audit')
        if record.get('pages') != audit.get('pages'):
            failures.append(f'{stem}: visual review page count differs from artifact audit')
    return failures


def visual_projection(visual: JsonObject, failures: list[str]) -> JsonObject:
    """Return the summary representation of valid or stale visual evidence."""
    if failures:
        return {
            'status': 'PENDING',
            'reason': '; '.join(failures),
            'evidence_file': VISUAL_EVIDENCE_PATH.name,
        }
    return {
        'status': visual['result'],
        'reviewer': visual['reviewer'],
        'reviewed_at_utc': visual['reviewed_at_utc'],
        'dpi': visual['dpi'],
        'pages_reviewed': visual['pages_reviewed'],
        'pdf_hashes': {record['stem']: record['sha256'] for record in visual['pdfs']},
        'notes': visual['notes'],
        'evidence_file': VISUAL_EVIDENCE_PATH.name,
        'evidence_sha256': sha256(VISUAL_EVIDENCE_PATH),
    }


def focused_checks(evidence: JsonObject) -> dict[str, JsonObject]:
    """Project command results into stable groups without inventing PASS values."""
    grouped: dict[str, list[JsonObject]] = {}
    for check in evidence.get('checks', []):
        group = str(check.get('group', 'ungrouped'))
        grouped.setdefault(group, []).append(check)
    return {
        group: {
            'status': 'PASS' if checks and all(check.get('status') == 'PASS' for check in checks) else 'FAIL',
            'evidence_ids': [str(check.get('id')) for check in checks],
            'exit_codes': [check.get('exit_code') for check in checks],
        }
        for group, checks in grouped.items()
    }
