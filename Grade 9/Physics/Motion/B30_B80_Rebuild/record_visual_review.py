#!/usr/bin/env python3
"""Record a human visual-review attestation against exact learner PDF hashes."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

import fitz

from review_evidence import ARTIFACT_MODELS, PACKAGE_ROOT, VISUAL_EVIDENCE_PATH, sha256


class PdfRecord(TypedDict):
    """Hash and page count for one visually reviewed PDF."""

    stem: str
    path: str
    sha256: str
    pages: int


def _pdf_record(stem: str) -> PdfRecord:
    """Capture the exact file identity and page count for one learner artifact."""
    path = PACKAGE_ROOT / f'{stem}.pdf'
    with fitz.open(path) as document:
        pages = len(document)
    return {
        'stem': stem,
        'path': path.name,
        'sha256': sha256(path),
        'pages': pages,
    }


def main() -> int:
    """Validate explicit review inputs and write the hash-bound attestation."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--reviewer', required=True)
    parser.add_argument('--result', required=True, choices=('PASS', 'FAIL'))
    parser.add_argument('--dpi', required=True, type=int)
    parser.add_argument('--pages-reviewed', required=True, type=int)
    parser.add_argument('--notes', required=True)
    arguments = parser.parse_args()
    records = [_pdf_record(stem) for stem in ARTIFACT_MODELS]
    expected_pages = sum(record['pages'] for record in records)
    if arguments.result == 'PASS' and arguments.dpi < 200:
        raise ValueError('a PASS visual review requires rendering at 200 DPI or higher')
    if arguments.result == 'PASS' and arguments.pages_reviewed != expected_pages:
        raise ValueError(f'a PASS visual review must cover all {expected_pages} pages')
    payload = {
        'schema_version': 1,
        'reviewed_at_utc': datetime.now(timezone.utc).isoformat(),
        'reviewer': arguments.reviewer,
        'result': arguments.result,
        'dpi': arguments.dpi,
        'pages_reviewed': arguments.pages_reviewed,
        'expected_pages': expected_pages,
        'notes': arguments.notes,
        'pdfs': records,
    }
    VISUAL_EVIDENCE_PATH.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f"{arguments.result}: recorded {arguments.pages_reviewed}/{expected_pages} pages at {arguments.dpi} DPI")
    print(f"Wrote {VISUAL_EVIDENCE_PATH.name} with exact PDF hashes.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
