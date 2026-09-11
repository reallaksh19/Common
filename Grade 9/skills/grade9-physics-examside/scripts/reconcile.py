#!/usr/bin/env python3
"""Reconcile source custody, publication content, and optional artifact identity.

The ledger owns source facts. The publication model owns learner-facing content. The
audit owns the hashes of the rendered artifact and its exact input model. A PASS is
issued only when every available boundary agrees; source review itself remains a
human responsibility.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]
_TIER_KEY: dict[str, str] = {'H1': 'h1', 'H2': 'h2', 'H3': 'h3'}
_HASH = re.compile(r'^[0-9a-f]{64}$')


def _questions(model: JsonObject) -> dict[str, JsonObject]:
    """Return every published question keyed by its immutable ID."""
    buckets: JsonObject = model['questions']
    questions: list[JsonObject] = buckets['anchors'] + buckets['core_calibrated'] + buckets['challenges']
    return {question['id']: question for question in questions}


def _source_state(record: JsonObject, question: JsonObject) -> tuple[bool, list[str]]:
    """Compare independent workflow, source, provenance, transcription, and difficulty axes."""
    expected_state = 'ORIGINAL' if question['source_status'] == 'ORIGINAL' else 'SOURCE_RECONCILED'
    checks = {
        'workflow_state': (record['state'], expected_state),
        'source_status': (record['source_status'], question['source_status']),
        'provenance_class': (record['provenance_class'], question['provenance_class']),
        'transcription_status': (record['transcription_status'], question.get('transcription_status')),
        'difficulty_source': (record['difficulty_source'], question['difficulty_source']),
    }
    failures = [f'{name} ledger={actual!r} published={expected!r}' for name, (actual, expected) in checks.items() if actual != expected]
    return not failures, failures


def _source_identity(record: JsonObject, question: JsonObject) -> tuple[bool, list[str]]:
    """Compare raw source fields to the citation rendered from the publication model."""
    if question['source_status'] == 'ORIGINAL':
        checks = {
            'raw_stem': (record['raw_stem'], question['question']),
            'raw_answer': (record['raw_answer'], question['answer']),
            'source_url': (record['source_url'], ''),
            'source_sha256': (record['source_sha256'], None),
            'source_page': (record['source_page'], None),
            'adaptation_note': (record['adaptation_note'], None),
            'target_ids': (record['target_ids'], [question['id']]),
        }
    else:
        citation: JsonObject | None = question.get('source_citation')
        if citation is None:
            return False, ['published external question has no source_citation']
        checks = {
            'source_document': (record['source_document'], citation['source_document']),
            'source_sha256': (record['source_sha256'], citation['source_sha256']),
            'source_page': (record['source_page'], citation['source_page']),
            'source_url': (record['source_url'], citation['url']),
            'source_locator': (record['source_locator'], citation['locator']),
            'raw_stem': (record['raw_stem'], citation['raw_stem']),
            'raw_answer': (record['raw_answer'], citation['raw_answer']),
            'values_units': (record['values_units'], citation['values_units']),
            'options': (record['options'], citation['options']),
            'figure_locator': (record['figure_locator'], citation['figure_locator']),
            'figure_semantics': (record['figure_semantics'], citation['figure_semantics']),
            'adaptation_note': (record['adaptation_note'], citation.get('adaptation_note')),
            'target_ids': (record['target_ids'], citation['target_ids']),
        }
    failures = [f'{name} ledger={actual!r} published={expected!r}' for name, (actual, expected) in checks.items() if actual != expected]
    return not failures, failures


def _artifact_identity(model_sha256: str | None, audit: JsonObject | None) -> tuple[bool, list[str]]:
    """Verify that an optional audit names the exact model and a concrete PDF hash."""
    if model_sha256 is None and audit is None:
        return True, []
    if model_sha256 is None or audit is None:
        return False, ['model_sha256 and audit must be supplied together']
    failures: list[str] = []
    if audit.get('model_sha256') != model_sha256:
        failures.append(f"audit.model_sha256={audit.get('model_sha256')!r} actual={model_sha256!r}")
    pdf_sha256 = audit.get('pdf_sha256')
    if not isinstance(pdf_sha256, str) or _HASH.fullmatch(pdf_sha256) is None:
        failures.append(f'audit.pdf_sha256 is not a lowercase SHA-256: {pdf_sha256!r}')
    return not failures, failures


def reconcile(
    ledger: JsonObject,
    model: JsonObject,
    model_sha256: str | None,
    audit: JsonObject | None,
) -> JsonObject:
    """Return dual-view evidence and blocking counters for the full custody chain."""
    expected = set(ledger['expected_ids'])
    records = {record['id']: record for record in ledger['records']}
    published = _questions(model)
    missing = sorted(expected - published.keys())
    unledgered = sorted(published.keys() - expected)
    concept_failures: list[str] = []
    hint_failures: list[str] = []
    solution_failures: list[str] = []
    source_state_failures: list[str] = []
    source_identity_failures: list[str] = []
    dependency_failures: list[str] = []
    view1: list[str] = []
    view2: list[JsonObject] = []

    for question_id in sorted(expected & published.keys()):
        record = records[question_id]
        question = published[question_id]
        chain: list[str] = []

        concept_ok = record['primary_concept'] == question['primary_concept_id']
        if not concept_ok:
            concept_failures.append(question_id)
        chain.append('primary_concept ' + ('MATCH ' + question['primary_concept_id'] if concept_ok else f"MISMATCH ledger={record['primary_concept']} published={question['primary_concept_id']}"))

        published_hints = {hint['tier']: hint['text'] for hint in question['hints']}
        hints_ok = len(question['hints']) == 3 and all(record['hints'].get(ledger_key) == published_hints.get(published_key) for published_key, ledger_key in _TIER_KEY.items())
        if not hints_ok:
            hint_failures.append(question_id)
        chain.append('hints ' + ('MATCH H1-H3' if hints_ok else 'MISMATCH ledger h1/h2/h3 vs published hints[*].tier/.text'))

        solution_ok = all(question['solution'].get(key) == record['solution'].get(key) for key in ('why', 'method', 'answer', 'keep'))
        if not solution_ok:
            solution_failures.append(question_id)
        chain.append('solution ' + ('MATCH why/method/answer/keep' if solution_ok else 'MISMATCH'))

        source_state_ok, source_state_details = _source_state(record, question)
        if not source_state_ok:
            source_state_failures.append(question_id)
        chain.append('source_state ' + ('MATCH independent axes' if source_state_ok else 'MISMATCH ' + '; '.join(source_state_details)))

        source_identity_ok, source_identity_details = _source_identity(record, question)
        if not source_identity_ok:
            source_identity_failures.append(question_id)
        chain.append('source_identity ' + ('MATCH raw source fingerprint' if source_identity_ok else 'MISMATCH ' + '; '.join(source_identity_details)))

        ledger_dependency = record.get('dependency', 'NONE')
        published_dependency = (question.get('figure') or {}).get('dependency_class', 'NONE')
        dependency_ok = ledger_dependency == published_dependency
        if not dependency_ok:
            dependency_failures.append(question_id)
        chain.append('dependency ' + ('MATCH ' + published_dependency if dependency_ok else f'MISMATCH ledger.dependency={ledger_dependency} published.figure.dependency_class={published_dependency}'))

        complete = all((concept_ok, hints_ok, solution_ok, source_state_ok, source_identity_ok, dependency_ok))
        chain.append('COMPLETE' if complete else 'DRIFTED')
        view1.append(f"{question_id} {'PLACED' if complete else 'DRIFTED'}")
        view2.append({'id': question_id, 'chain': chain})

    view1.extend(f'{question_id} MISSING (ledgered, never published)' for question_id in missing)
    view1.extend(f'{question_id} UNLEDGERED (published, not in frozen ledger)' for question_id in unledgered)
    artifact_ok, artifact_failures = _artifact_identity(model_sha256, audit)
    blocking = (
        missing
        or unledgered
        or concept_failures
        or hint_failures
        or solution_failures
        or source_state_failures
        or source_identity_failures
        or dependency_failures
        or artifact_failures
    )
    counters = {
        'LEDGER_REQUIRED': len(expected),
        'LEDGER_PLACED': len(expected) - len(missing),
        'LEDGER_MISSING': len(missing),
        'LEDGER_UNLEDGERED': len(unledgered),
        'LEDGER_CONCEPT_LINK_FAILURES': len(concept_failures),
        'LEDGER_HINT_FAILURES': len(hint_failures),
        'LEDGER_SOLUTION_FAILURES': len(solution_failures),
        'LEDGER_SOURCE_STATE_FAILURES': len(source_state_failures),
        'LEDGER_SOURCE_IDENTITY_FAILURES': len(source_identity_failures),
        'LEDGER_DEPENDENCY_FAILURES': len(dependency_failures),
        'ARTIFACT_IDENTITY_FAILURES': len(artifact_failures),
        'LEDGER_STATUS': 'FAIL' if blocking else 'PASS',
    }
    return {
        'view1_subtopic_to_questions': view1,
        'view2_question_to_support_chain': view2,
        'artifact_identity': {'status': 'PASS' if artifact_ok else 'FAIL', 'failures': artifact_failures},
        'counters': counters,
        'missing': missing,
        'unledgered': unledgered,
        'concept_link_failures': concept_failures,
        'hint_failures': hint_failures,
        'solution_failures': solution_failures,
        'source_state_failures': source_state_failures,
        'source_identity_failures': source_identity_failures,
        'dependency_failures': dependency_failures,
    }


def _sha256(path: Path) -> str:
    """Hash one model file without mutating it."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(arguments: list[str]) -> int:
    """Run reconciliation for ledger/model and, when supplied, an audit artifact."""
    if len(arguments) not in (3, 4):
        raise ValueError('usage: reconcile.py <ledger.json> <published_model.json> [artifact.audit.json]')
    ledger_path = Path(arguments[1])
    model_path = Path(arguments[2])
    audit_path = Path(arguments[3]) if len(arguments) == 4 else None
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    model = json.loads(model_path.read_text(encoding='utf-8'))
    audit = json.loads(audit_path.read_text(encoding='utf-8')) if audit_path is not None else None
    output = reconcile(ledger, model, _sha256(model_path) if audit is not None else None, audit)
    print(json.dumps(output, indent=2))
    return 0 if output['counters']['LEDGER_STATUS'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
