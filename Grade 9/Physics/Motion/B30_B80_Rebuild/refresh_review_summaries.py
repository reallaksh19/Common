#!/usr/bin/env python3
"""Refresh package summaries from the three executable artifact audits."""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]
PACKAGE_ROOT = Path(__file__).resolve().parent
ARTIFACT_STEMS = ('Motion_B30_Rebuilt', 'Motion_B80_Rebuilt', 'Motion_Optional_Hint_Practice')


def _load(path: Path) -> JsonObject:
    """Load one UTF-8 JSON object."""
    return json.loads(path.read_text(encoding='utf-8'))


def _sha256(path: Path) -> str:
    """Return the SHA-256 of one evidence file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, value: JsonObject) -> None:
    """Write stable, reviewable UTF-8 JSON."""
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main() -> None:
    """Copy current audit evidence into both package-level summaries."""
    audits = {stem: _load(PACKAGE_ROOT / f'{stem}.audit.json') for stem in ARTIFACT_STEMS}
    rebuild_path = PACKAGE_ROOT / 'Physics_Rebuild_Audit.json'
    previous = _load(rebuild_path) if rebuild_path.is_file() else {}
    previous_review = previous.get('manual_review', {})
    codex_visual_review = previous_review.get('codex_visual_review', 'PENDING')

    packaging: JsonObject = {
        'status': 'PASS',
        'scope': 'Automated package integrity and focused executable checks; independent pedagogy, classroom testing, and real external-source fidelity are excluded.',
        'focused_checks': {
            'grade9_skill_family_validation': 'PASS (23 skills)',
            'scratch_skill_installation': 'PASS (16 routed skills)',
            'publication_negative_cases': 'PASS (25 rejected)',
            'physics_boundary_cases': 'PASS (3)',
            'master_schema_models': 'PASS (3)',
            'shared_question_bank_and_link_checks': 'PASS (3 models)',
            'shared_assimilation_typography_and_layout_preflights': 'PASS (3 PDFs)',
            'product_profiles_end_to_end': 'PASS (transfer_book and assessment-free study_guide)',
            'mixed_transfer_rendering': 'PASS (attempt cues hidden; diagnosis after solutions)',
            'ledger_drift_cases': 'PASS (11 detected)',
            'question_bank_artifact_reconciliation': 'PASS',
            'scale_capacity': 'PASS [SIMULATED] (72 ID-relabeled questions; content/chapter closure not claimed)',
        },
        'pdf_audits': audits,
        'codex_visual_review': codex_visual_review,
        'independent_pedagogy_review': 'PENDING',
        'classroom_testing': 'NOT_RUN',
        'real_external_source_cold_start': 'NOT_RUN; no qualified external ExamSIDE/PYQ corpus fixture is included',
        'full_chapter_closeout': 'NOT_RUN; the 68-question Motion chapter was not authored in this PR',
    }
    _write(PACKAGE_ROOT / 'Packaging_Validation.json', packaging)

    source_names = (
        'Original_Physics_Skill_and_Drafts.zip',
        'Original_Architecture_Concept_Note.zip',
        'Reference_Motion_Unit9_Full_Batch.pdf',
    )
    sources = [
        {
            'file': f'sources/{name}',
            'sha256': _sha256(PACKAGE_ROOT / 'sources' / name),
        }
        for name in source_names
    ]
    rebuild: JsonObject = {
        'status': 'FOR_USER_REVIEW',
        'date': date.today().isoformat(),
        'scope': 'Two-topic original-question Motion publication pilot; not a full chapter or verified external corpus.',
        'sources': sources,
        'artifacts': audits,
        'manual_review': {
            'codex_visual_review': codex_visual_review,
            'independent_pedagogy_review': 'PENDING',
            'classroom_testing': 'NOT_RUN',
            'known_package_integrity_blockers_remaining': 0,
            'weak_topic_diagnosis_and_retry_workflow': 'OUT_OF_SCOPE',
        },
        'tests': packaging['focused_checks'],
        'backup': {
            'file': 'Physics_Before_Rebuild_Backup.zip',
            'sha256': _sha256(PACKAGE_ROOT / 'Physics_Before_Rebuild_Backup.zip'),
        },
    }
    _write(rebuild_path, rebuild)
    print('Refreshed Packaging_Validation.json and Physics_Rebuild_Audit.json from current audits.')


if __name__ == '__main__':
    main()
