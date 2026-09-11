#!/usr/bin/env python3
"""Run the focused review suite and capture immutable command evidence."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from refresh_file_manifest import REPOSITORY_ROOT, evidence_basis_paths
from review_evidence import EVIDENCE_PATH, artifact_paths, repository_hashes


class CheckSpec(TypedDict):
    """One executable check with a stable identifier and reporting group."""

    id: str
    group: str
    arguments: list[str]


class CheckResult(TypedDict):
    """Captured result for one real subprocess execution."""

    id: str
    group: str
    command: list[str]
    cwd: str
    started_at_utc: str
    duration_seconds: float
    exit_code: int
    status: str
    stdout: str
    stderr: str
    stdout_sha256: str
    stderr_sha256: str


def _relative(path: str) -> str:
    """Return one repository-relative path using forward slashes."""
    return path.replace('\\', '/')


def _spec(check_id: str, group: str, *arguments: str) -> CheckSpec:
    """Construct one typed Python command specification."""
    return {'id': check_id, 'group': group, 'arguments': list(arguments)}


def _specifications(scratch_destination: Path) -> list[CheckSpec]:
    """Build the complete focused suite against current models and PDFs."""
    publication = 'Grade 9/skills/grade9-physics-publication'
    examside = 'Grade 9/skills/grade9-physics-examside'
    generic_publication = 'Grade 9/skills/grade9-publication/scripts'
    package = 'Grade 9/Physics/Motion/B30_B80_Rebuild'
    models = (
        'motion_B30_v2.json',
        'motion_B80_v2.json',
        'motion_question_bank_v2.json',
    )
    stems = (
        'Motion_B30_Rebuilt',
        'Motion_B80_Rebuilt',
        'Motion_Optional_Hint_Practice',
    )
    specs = [
        _spec('skill-family', 'skill_family_validation', 'Grade 9/validate_skills.py'),
        _spec(
            'scratch-install',
            'skill_installation',
            'Grade 9/install_skills.py',
            '--dest',
            _relative(str(scratch_destination)),
        ),
        _spec('publication-suite', 'publication_contract', f'{publication}/scripts/test_v2.py'),
        _spec('review-evidence-contract', 'evidence_integrity', f'{package}/test_review_evidence.py'),
        _spec(
            'source-ledger',
            'source_reconciliation',
            f'{examside}/scripts/check_ledger.py',
            f'{examside}/references/source-ledger.example.json',
        ),
        _spec('reconciliation-suite', 'source_reconciliation', f'{examside}/scripts/test_reconcile.py'),
        _spec(
            'artifact-reconciliation',
            'source_reconciliation',
            f'{examside}/scripts/reconcile.py',
            f'{examside}/references/source-ledger.example.json',
            f'{publication}/examples/motion_question_bank_v2.json',
            f'{package}/Motion_Optional_Hint_Practice.audit.json',
        ),
    ]
    for model_name in models:
        slug = Path(model_name).stem
        model_path = f'{publication}/examples/{model_name}'
        specs.extend(
            (
                _spec(f'bank-{slug}', 'shared_model_contracts', 'Grade 9/skills/grade9-question-bank/scripts/validate_bank.py', model_path),
                _spec(f'links-{slug}', 'shared_model_contracts', 'Grade 9/skills/grade9-textbook-publisher/scripts/check_master_links.py', model_path),
            )
        )
    for stem in stems:
        slug = stem.lower().replace('_', '-')
        pdf_path = f'{package}/{stem}.pdf'
        specs.extend(
            (
                _spec(f'assimilation-{slug}', 'pdf_preflights', f'{generic_publication}/check_question_bank_assimilation.py', pdf_path),
                _spec(f'typography-{slug}', 'pdf_preflights', f'{generic_publication}/check_math_typography.py', pdf_path),
                _spec(f'overlap-{slug}', 'pdf_preflights', f'{generic_publication}/check_text_overlaps.py', pdf_path),
            )
        )
    return specs


def _redact(value: str, redactions: dict[str, str]) -> str:
    """Replace machine-local paths with stable audit placeholders."""
    result = value
    for source, replacement in sorted(redactions.items(), key=lambda item: len(item[0]), reverse=True):
        result = result.replace(source, replacement)
    return result


def _run(specification: CheckSpec, environment: dict[str, str], redactions: dict[str, str]) -> CheckResult:
    """Execute one check and capture its exact UTF-8 output, status, and timing."""
    command = [sys.executable, *specification['arguments']]
    started_at = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    result = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        check=False,
    )
    duration = round(time.monotonic() - start, 3)
    stdout = _redact(result.stdout.replace('\r\n', '\n'), redactions)
    stderr = _redact(result.stderr.replace('\r\n', '\n'), redactions)
    return {
        'id': specification['id'],
        'group': specification['group'],
        'command': ['python', *[_redact(argument, redactions) for argument in specification['arguments']]],
        'cwd': '.',
        'started_at_utc': started_at,
        'duration_seconds': duration,
        'exit_code': result.returncode,
        'status': 'PASS' if result.returncode == 0 else 'FAIL',
        'stdout': stdout,
        'stderr': stderr,
        'stdout_sha256': hashlib.sha256(stdout.encode('utf-8')).hexdigest(),
        'stderr_sha256': hashlib.sha256(stderr.encode('utf-8')).hexdigest(),
    }


def main() -> int:
    """Run every focused check, write evidence even on failure, and return truthfully."""
    environment = dict(os.environ)
    environment['PYTHONUTF8'] = '1'
    with tempfile.TemporaryDirectory(prefix='grade9-skill-install-') as scratch:
        scratch_destination = Path(scratch) / 'skills'
        redactions = {
            str(scratch_destination): '<temporary-skill-install>/skills',
            _relative(str(scratch_destination)): '<temporary-skill-install>/skills',
            str(REPOSITORY_ROOT): '<repository>',
            _relative(str(REPOSITORY_ROOT)): '<repository>',
            sys.executable: '<python-executable>',
            _relative(sys.executable): '<python-executable>',
        }
        results = [
            _run(specification, environment, redactions)
            for specification in _specifications(scratch_destination)
        ]
    payload = {
        'schema_version': 1,
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'python_runtime': platform.python_version(),
        'basis': 'Real subprocess exit codes and captured output, bound to exact dependency and artifact bytes.',
        'output_normalization': 'CRLF converted to LF; machine-local Python, repository, and scratch-install paths replaced with stable placeholders before hashing.',
        'basis_hashes': repository_hashes(evidence_basis_paths()),
        'artifact_hashes': repository_hashes(artifact_paths()),
        'status': 'PASS' if all(result['status'] == 'PASS' for result in results) else 'FAIL',
        'checks': results,
    }
    EVIDENCE_PATH.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8', newline='\n')
    for result in results:
        print(f"{result['status']} {result['id']} (exit {result['exit_code']}, {result['duration_seconds']:.3f}s)")
    print(f"{payload['status']}: wrote {EVIDENCE_PATH.relative_to(REPOSITORY_ROOT)}")
    return 0 if payload['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
