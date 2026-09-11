#!/usr/bin/env python3
"""Falsify PASS when machine output, dependency bytes, or visual hashes drift."""
from __future__ import annotations

import copy
import hashlib

import fitz

from refresh_file_manifest import evidence_basis_paths
from review_evidence import (
    ARTIFACT_MODELS,
    PACKAGE_ROOT,
    artifact_paths,
    load_json,
    machine_evidence_failures,
    repository_hashes,
    sha256,
    visual_evidence_failures,
)


def main() -> int:
    """Exercise the anti-drift checks with controlled in-memory mutations."""
    stdout = 'synthetic command passed\n'
    stderr = ''
    machine = {
        'status': 'PASS',
        'basis_hashes': repository_hashes(evidence_basis_paths()),
        'artifact_hashes': repository_hashes(artifact_paths()),
        'checks': [
            {
                'id': 'synthetic-check',
                'status': 'PASS',
                'exit_code': 0,
                'stdout': stdout,
                'stderr': stderr,
                'stdout_sha256': hashlib.sha256(stdout.encode('utf-8')).hexdigest(),
                'stderr_sha256': hashlib.sha256(stderr.encode('utf-8')).hexdigest(),
            }
        ],
    }
    assert not machine_evidence_failures(machine), 'valid synthetic machine evidence was rejected'
    output_drift = copy.deepcopy(machine)
    output_drift['checks'][0]['stdout'] = 'tampered output\n'
    assert any('stdout hash mismatch' in failure for failure in machine_evidence_failures(output_drift))
    basis_drift = copy.deepcopy(machine)
    first_path = next(iter(basis_drift['basis_hashes']))
    basis_drift['basis_hashes'][first_path] = '0' * 64
    assert any('dependency bytes' in failure for failure in machine_evidence_failures(basis_drift))

    audits = {stem: load_json(PACKAGE_ROOT / f'{stem}.audit.json') for stem in ARTIFACT_MODELS}
    pdfs = []
    for stem in ARTIFACT_MODELS:
        pdf_path = PACKAGE_ROOT / f'{stem}.pdf'
        with fitz.open(pdf_path) as document:
            pages = len(document)
        pdfs.append({'stem': stem, 'path': pdf_path.name, 'sha256': sha256(pdf_path), 'pages': pages})
    visual = {
        'result': 'PASS',
        'dpi': 200,
        'pages_reviewed': sum(record['pages'] for record in pdfs),
        'pdfs': pdfs,
    }
    assert not visual_evidence_failures(visual, audits), 'valid synthetic visual evidence was rejected'
    visual_drift = copy.deepcopy(visual)
    visual_drift['pdfs'][0]['sha256'] = '0' * 64
    assert any('visual review PDF hash is stale' in failure for failure in visual_evidence_failures(visual_drift, audits))
    print('Evidence anti-drift: command output, dependency hash, and visual PDF hash mutations detected.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
