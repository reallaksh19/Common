#!/usr/bin/env python3
"""Project current machine and visual evidence into package review summaries."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from review_evidence import (
    ARTIFACT_MODELS,
    EVIDENCE_PATH,
    PACKAGE_ROOT,
    VISUAL_EVIDENCE_PATH,
    focused_checks,
    load_json,
    machine_evidence_failures,
    sha256,
    visual_evidence_failures,
    visual_projection,
)

JsonObject = dict[str, Any]


def _write(path: Path, value: JsonObject) -> None:
    """Write stable, reviewable UTF-8 JSON to ``path``."""
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main() -> None:
    """Require current machine evidence, then refresh both derived summaries."""
    evidence = load_json(EVIDENCE_PATH)
    machine_failures = machine_evidence_failures(evidence)
    if machine_failures:
        raise RuntimeError('cannot refresh summaries: ' + '; '.join(machine_failures))
    audits = {
        stem: load_json(PACKAGE_ROOT / f'{stem}.audit.json')
        for stem in ARTIFACT_MODELS
    }
    visual = load_json(VISUAL_EVIDENCE_PATH) if VISUAL_EVIDENCE_PATH.is_file() else {}
    visual_failures = visual_evidence_failures(visual, audits)
    visual_summary = visual_projection(visual, visual_failures)
    package_status = 'PASS' if not visual_failures else 'PENDING_VISUAL_REVIEW'
    checks = focused_checks(evidence)
    evidence_identity = {
        'file': EVIDENCE_PATH.name,
        'sha256': sha256(EVIDENCE_PATH),
        'generated_at_utc': evidence['generated_at_utc'],
        'status': evidence['status'],
    }

    packaging: JsonObject = {
        'status': package_status,
        'scope': 'Machine-produced package checks plus a separately attested hash-bound visual review; independent pedagogy, classroom testing, and real external-source fidelity are excluded.',
        'machine_evidence': evidence_identity,
        'focused_checks': checks,
        'pdf_audits': audits,
        'codex_visual_review': visual_summary,
        'independent_pedagogy_review': 'PENDING',
        'classroom_testing': 'NOT_RUN',
        'real_external_source_cold_start': 'NOT_RUN; no qualified external ExamSIDE/PYQ corpus fixture is included',
        'full_chapter_closeout': 'NOT_RUN; the 68-question Motion chapter was not authored in this PR',
        'source_owned_difficulty_mapping': 'NOT_RUN; preserve source codes separately when a qualified source corpus supplies them',
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
            'sha256': sha256(PACKAGE_ROOT / 'sources' / name),
        }
        for name in source_names
    ]
    rebuild: JsonObject = {
        'status': 'FOR_USER_REVIEW',
        'date': date.today().isoformat(),
        'scope': 'Two-topic original-question Motion publication pilot; not a full chapter or verified external corpus.',
        'sources': sources,
        'artifacts': audits,
        'machine_evidence': evidence_identity,
        'manual_review': {
            'codex_visual_review': visual_summary,
            'independent_pedagogy_review': 'PENDING',
            'classroom_testing': 'NOT_RUN',
            'known_package_integrity_blockers_remaining': len(visual_failures),
            'weak_topic_diagnosis_and_retry_workflow': 'OUT_OF_SCOPE',
            'source_owned_difficulty_mapping': 'NOT_RUN',
        },
        'tests': checks,
        'backup': {
            'file': 'Physics_Before_Rebuild_Backup.zip',
            'sha256': sha256(PACKAGE_ROOT / 'Physics_Before_Rebuild_Backup.zip'),
        },
    }
    _write(PACKAGE_ROOT / 'Physics_Rebuild_Audit.json', rebuild)
    print(f'Refreshed package summaries from {len(evidence["checks"])} command results; status={package_status}.')


if __name__ == '__main__':
    main()
