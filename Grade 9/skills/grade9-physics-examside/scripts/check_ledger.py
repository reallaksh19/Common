#!/usr/bin/env python3
"""Check a frozen source ledger; source truth still requires page-by-page review."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]
_HASH = re.compile(r'^[0-9a-f]{64}$')
_EXTERNAL_PROVENANCE = {
    'USER_UPLOADED_ANCHOR',
    'OFFICIAL_PYQ',
    'SECONDARY_VERIFIED_PYQ',
    'PUBLISHED_REFERENCE',
    'RECONSTRUCTED_FROM_SCAN',
}
_DEPENDENCIES = {'NONE', 'GRAPH', 'DIAGRAM', 'TABLE', 'TIMELINE', 'NUMBER_LINE', 'OPTION_FIGURES', 'STATEMENT_SET', 'MIXED'}
_DIFFICULTY_SOURCES = {'AUTHOR_HEURISTIC', 'SOURCE_ANALYSIS', 'EXPERT_CALIBRATED', 'EMPIRICAL'}


def _check_source_fields(record: JsonObject) -> None:
    """Validate source custody without conflating independent state axes."""
    required = {
        'source_status', 'provenance_class', 'transcription_status', 'difficulty_source',
        'source_document', 'source_sha256', 'source_page', 'source_url', 'source_locator',
        'raw_stem', 'values_units', 'options', 'figure_locator', 'figure_semantics',
        'raw_answer', 'adaptation_note', 'target_ids',
    }
    assert required <= record.keys(), f"{record['id']}: missing source fields {sorted(required - record.keys())}"
    assert record['difficulty_source'] in _DIFFICULTY_SOURCES, f"{record['id']}: invalid difficulty source"
    assert isinstance(record['values_units'], list) and isinstance(record['options'], list), f"{record['id']}: source values/options must be lists"
    assert isinstance(record['figure_semantics'], list), f"{record['id']}: figure semantics must be a list"
    assert record['target_ids'] and record['id'] in record['target_ids'], f"{record['id']}: target_ids must include record ID"
    assert record['raw_stem'] and record['raw_answer'], f"{record['id']}: raw source identity is incomplete"

    if record['state'] == 'ORIGINAL':
        assert record['source_status'] == 'ORIGINAL', f"{record['id']}: original workflow state requires ORIGINAL source status"
        assert record['provenance_class'] == 'ORIGINAL_CALIBRATED', f"{record['id']}: original provenance mismatch"
        assert record['transcription_status'] is None, f"{record['id']}: original item cannot claim transcription"
        assert record['source_sha256'] is None and record['source_page'] is None, f"{record['id']}: original item cannot claim an external page fingerprint"
        assert record['source_url'] == '' and record['adaptation_note'] is None, f"{record['id']}: original item has external/adaptation metadata"
        return

    assert record['state'] == 'SOURCE_RECONCILED', f"{record['id']}: unsupported workflow state"
    assert record['source_status'] in {'SOURCE_VERIFIED', 'ADAPTED'}, f"{record['id']}: reconciled item has invalid source status"
    assert record['provenance_class'] in _EXTERNAL_PROVENANCE, f"{record['id']}: external provenance is not qualified"
    assert record['transcription_status'] in {'VERIFIED_TRANSCRIPTION', 'RECONSTRUCTED'}, f"{record['id']}: transcription remains unresolved"
    assert isinstance(record['source_sha256'], str) and _HASH.fullmatch(record['source_sha256']), f"{record['id']}: invalid source SHA-256"
    assert isinstance(record['source_page'], int) and record['source_page'] >= 1, f"{record['id']}: invalid source page"
    assert record['source_url'].startswith('https://'), f"{record['id']}: exact source URL missing"
    if record['source_status'] == 'ADAPTED':
        assert record['adaptation_note'], f"{record['id']}: adaptation note missing"


def check(ledger: JsonObject) -> JsonObject:
    """Return an internal-consistency result for one immutable corpus ledger."""
    expected: list[str] = ledger['expected_ids']
    records: list[JsonObject] = ledger['records']
    record_ids = [record['id'] for record in records]
    assert len(expected) == len(set(expected)) and len(record_ids) == len(set(record_ids)), 'duplicate identities'
    assert set(expected) == set(record_ids), 'unexplained corpus loss/addition'
    for record in records:
        assert record['primary_concept'], f"{record['id']}: missing primary concept"
        assert record['dependency'] in _DEPENDENCIES, f"{record['id']}: invalid dependency"
        assert len(set(record['hints'].values())) == 3 and set(record['hints']) == {'h1', 'h2', 'h3'}, f"{record['id']}: hint progression fields"
        assert all(record['solution'].get(key) for key in ['why', 'method', 'answer', 'keep']), f"{record['id']}: solution incomplete"
        assert record['solution']['method'] != record['solution']['answer'], f"{record['id']}: method equals answer"
        assert record['links_closed'] and not record['editorial_issue'], f"{record['id']}: unclosed dependency or issue"
        if record['dependency'] != 'NONE':
            assert record['question_representation'] and record['solution_representation'], f"{record['id']}: missing representation"
        _check_source_fields(record)
        if ledger['claim'] == 'SOURCE_RECONCILED':
            assert record['state'] == 'SOURCE_RECONCILED' and record['exam_metadata_verified'], f"{record['id']}: source not verified"
        else:
            assert ledger['claim'] == 'PILOT_ORIGINAL' and record['state'] == 'ORIGINAL' and not record['exam_metadata_verified'], f"{record['id']}: invalid pilot attribution"
    return {
        'records_checked': len(record_ids),
        'claim': ledger['claim'],
        'source_truth_and_hint_leakage': 'MANUAL_REVIEW_REQUIRED',
    }


def main(arguments: list[str]) -> int:
    """Validate one ledger path supplied on the command line."""
    if len(arguments) != 2:
        raise ValueError('usage: check_ledger.py <ledger.json>')
    ledger = json.loads(Path(arguments[1]).read_text(encoding='utf-8'))
    print(json.dumps(check(ledger), indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
