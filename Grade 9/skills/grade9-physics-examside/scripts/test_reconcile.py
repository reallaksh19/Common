#!/usr/bin/env python3
"""Negative tests for source-ledger, publication-model, and artifact drift."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable

from reconcile import reconcile

JsonObject = dict[str, Any]
Mutation = Callable[[JsonObject], None]
ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_ROOT = ROOT.parent / 'grade9-physics-publication'
LEDGER: JsonObject = json.loads((ROOT / 'references/source-ledger.example.json').read_text(encoding='utf-8'))
MODEL: JsonObject = json.loads((PUBLICATION_ROOT / 'examples/motion_question_bank_v2.json').read_text(encoding='utf-8'))


def _first_question(model: JsonObject) -> JsonObject:
    """Return the first core question in the fixture."""
    return model['questions']['core_calibrated'][0]


def drop_from_model(model: JsonObject) -> None:
    """Remove one expected publication question."""
    model['questions']['core_calibrated'] = [question for question in model['questions']['core_calibrated'] if question['id'] != 'B80-A1']


def drop_from_ledger(ledger: JsonObject) -> None:
    """Remove one ledger identity while leaving the publication unchanged."""
    ledger['expected_ids'].remove('B80-A1')
    ledger['records'] = [record for record in ledger['records'] if record['id'] != 'B80-A1']


def wrong_concept(model: JsonObject) -> None:
    """Drift the published concept link."""
    _first_question(model)['primary_concept_id'] = 'PHY-MOT-VTAREA-01'


def wrong_hint(model: JsonObject) -> None:
    """Drift one tiered hint."""
    _first_question(model)['hints'][0]['text'] = 'A drifted hint not in the frozen ledger.'


def wrong_answer(model: JsonObject) -> None:
    """Drift the publication solution."""
    _first_question(model)['solution']['answer'] = 'A drifted answer.'


def wrong_dependency(model: JsonObject) -> None:
    """Drift the figure dependency class."""
    model['questions']['core_calibrated'][5]['figure']['dependency_class'] = 'DIAGRAM'


def wrong_source_status(ledger: JsonObject) -> None:
    """Prove that workflow state does not substitute for publication source status."""
    ledger['records'][0]['source_status'] = 'SOURCE_VERIFIED'


def wrong_provenance(ledger: JsonObject) -> None:
    """Prove that source status does not determine provenance."""
    ledger['records'][0]['provenance_class'] = 'VERIFIED_EXTERNAL'


def wrong_raw_stem(ledger: JsonObject) -> None:
    """Drift the immutable raw question text."""
    ledger['records'][0]['raw_stem'] += ' Drifted.'


def _external_pair() -> tuple[JsonObject, JsonObject]:
    """Build an exact synthetic external pair for plumbing tests, never source claims."""
    ledger = copy.deepcopy(LEDGER)
    model = copy.deepcopy(MODEL)
    record = ledger['records'][0]
    question = _first_question(model)
    citation = {
        'title': 'TEST FIXTURE — not an exam source',
        'url': 'https://example.org/physics-test-fixture',
        'locator': 'synthetic test only',
        'verification': 'VERIFIED',
        'source_document': 'synthetic-fixture.pdf',
        'source_sha256': '0' * 64,
        'source_page': 1,
        'raw_stem': question['question'],
        'raw_answer': question['answer'],
        'values_units': ['synthetic'],
        'options': [],
        'figure_locator': None,
        'figure_semantics': [],
        'target_ids': [question['id']],
        'adaptation_note': 'Synthetic reconciliation fixture; no external source-truth claim.',
    }
    question.update(
        source_status='ADAPTED',
        provenance_class='OFFICIAL_PYQ',
        transcription_status='VERIFIED_TRANSCRIPTION',
        difficulty_source='SOURCE_ANALYSIS',
        source_citation=citation,
    )
    record.update(
        state='SOURCE_RECONCILED',
        source_status='ADAPTED',
        provenance_class='OFFICIAL_PYQ',
        transcription_status='VERIFIED_TRANSCRIPTION',
        difficulty_source='SOURCE_ANALYSIS',
        source_document=citation['source_document'],
        source_sha256=citation['source_sha256'],
        source_page=citation['source_page'],
        source_url=citation['url'],
        source_locator=citation['locator'],
        raw_stem=citation['raw_stem'],
        raw_answer=citation['raw_answer'],
        values_units=citation['values_units'],
        options=citation['options'],
        figure_locator=citation['figure_locator'],
        figure_semantics=citation['figure_semantics'],
        target_ids=citation['target_ids'],
        adaptation_note=citation['adaptation_note'],
    )
    return ledger, model


def _assert_drift(name: str, mutation: Mutation, target: str) -> None:
    """Assert one model or ledger mutation blocks reconciliation."""
    ledger = copy.deepcopy(LEDGER)
    model = copy.deepcopy(MODEL)
    mutation(ledger if target == 'ledger' else model)
    result = reconcile(ledger, model, None, None)
    assert result['counters']['LEDGER_STATUS'] == 'FAIL', f'{name}: drift not detected'
    print('DETECTED', name)


for case_name, mutate, mutation_target in [
    ('drop_from_model', drop_from_model, 'model'),
    ('drop_from_ledger', drop_from_ledger, 'ledger'),
    ('wrong_concept', wrong_concept, 'model'),
    ('wrong_hint', wrong_hint, 'model'),
    ('wrong_answer', wrong_answer, 'model'),
    ('wrong_dependency', wrong_dependency, 'model'),
    ('wrong_source_status', wrong_source_status, 'ledger'),
    ('wrong_provenance', wrong_provenance, 'ledger'),
    ('wrong_raw_stem', wrong_raw_stem, 'ledger'),
]:
    _assert_drift(case_name, mutate, mutation_target)

original_result = reconcile(LEDGER, MODEL, None, None)
assert original_result['counters']['LEDGER_STATUS'] == 'PASS', 'unmodified original ledger/model must reconcile cleanly'

external_ledger, external_model = _external_pair()
external_result = reconcile(external_ledger, external_model, None, None)
assert external_result['counters']['LEDGER_STATUS'] == 'PASS', 'exact external source fingerprint must reconcile'
external_model['questions']['core_calibrated'][0]['source_citation']['source_sha256'] = '1' * 64
assert reconcile(external_ledger, external_model, None, None)['counters']['LEDGER_STATUS'] == 'FAIL', 'external source fingerprint drift not detected'
print('DETECTED wrong_citation_fingerprint')

matching_audit = {'model_sha256': 'a' * 64, 'pdf_sha256': 'b' * 64}
assert reconcile(LEDGER, MODEL, 'a' * 64, matching_audit)['counters']['LEDGER_STATUS'] == 'PASS', 'matching artifact identity must pass'
wrong_audit = copy.deepcopy(matching_audit)
wrong_audit['model_sha256'] = 'c' * 64
assert reconcile(LEDGER, MODEL, 'a' * 64, wrong_audit)['counters']['LEDGER_STATUS'] == 'FAIL', 'artifact identity drift not detected'
print('DETECTED wrong_artifact_model_hash')
print('11 drift cases detected; original and exact synthetic-external chains reconcile cleanly.')
