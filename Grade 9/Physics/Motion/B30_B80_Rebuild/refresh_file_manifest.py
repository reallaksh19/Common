#!/usr/bin/env python3
"""Regenerate the review package's complete content-addressed file manifest."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_ROOT.parents[3]
MANIFEST_PATH = PACKAGE_ROOT / 'FILE_MANIFEST.json'
SCOPES = (
    'Grade 9/SKILLSET.md',
    'Grade 9/install_skills.py',
    'Grade 9/validate_skills.py',
    'Grade 9/Physics/Motion',
    'Grade 9/shared',
    'Grade 9/skills',
)
EXCLUDED = {
    'Grade 9/Physics/Motion/B30_B80_Rebuild/FILE_MANIFEST.json',
    'Grade 9/Physics/Motion/B30_B80_Rebuild/DELIVERY_RECORD.md',
}
GENERATED_EVIDENCE_PATHS = EXCLUDED | {
    'Grade 9/Physics/Motion/B30_B80_Rebuild/Packaging_Validation.json',
    'Grade 9/Physics/Motion/B30_B80_Rebuild/Physics_Rebuild_Audit.json',
    'Grade 9/Physics/Motion/B30_B80_Rebuild/review_evidence.json',
    'Grade 9/Physics/Motion/B30_B80_Rebuild/visual_review_evidence.json',
}


def tracked_paths() -> list[str]:
    """Return every tracked or pending file in the declared review-package scope."""
    command = ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '--', *SCOPES]
    result = subprocess.run(command, cwd=REPOSITORY_ROOT, check=True, capture_output=True, text=True, encoding='utf-8')
    paths = {
        line.strip().replace('\\', '/')
        for line in result.stdout.splitlines()
        if line.strip() and '__pycache__' not in line and not line.endswith('.pyc')
    }
    return sorted(paths - EXCLUDED)


def evidence_basis_paths() -> list[str]:
    """Return the non-generated files whose exact bytes underpin test evidence."""
    return sorted(set(tracked_paths()) - GENERATED_EVIDENCE_PATHS)


def file_record(relative_path: str) -> dict[str, str | int]:
    """Describe one repository file by stable path, byte count, and SHA-256."""
    data = (REPOSITORY_ROOT / relative_path).read_bytes()
    return {'path': relative_path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main() -> None:
    """Write the manifest from current repository bytes."""
    payload = {
        'basis': 'Content-addressed files in the declared review-package scope; recompute with refresh_file_manifest.py.',
        'excluded': sorted(EXCLUDED),
        'files': [file_record(path) for path in tracked_paths()],
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f"Wrote {MANIFEST_PATH.relative_to(REPOSITORY_ROOT)} with {len(payload['files'])} files.")


if __name__ == '__main__':
    main()
