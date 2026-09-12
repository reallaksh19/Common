#!/usr/bin/env python3
"""Falsifiers for the generic source-ingestion / denominator-freezing stage.

The proof corpus is deliberately real, not synthetic:

* the live pipeline denominators are re-derived from the committed C-C scope
  registries and reconciled against the coverage closure the pipeline actually
  produces;
* the PR #346 topic baselines are re-derived from two independently authored
  #346 artifacts (HANDOFF_MANIFEST.json and tools/validate_handoff.py), which
  must agree with each other.
"""
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
REPO = CHEM.parents[2]
sys.path[:0] = [str(D / 'engine'), str(CHEM / 'ColdStart' / 'engine')]
from freeze_chemistry_source_denominator import (
    validate_profile, validate_instance, counters_from_items, instance_by_id,
    assert_authoring_allowed, reconcile_with_closure, digest)
from chemistry_cold_start_runner import run_cold_start


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


profile = load(D / 'registry' / 'chemistry-source-ingestion-profile.json')
Draft202012Validator(load(D / 'contracts' / 'chemistry-source-ingestion-profile.schema.json')).validate(profile)
assert validate_profile(profile, REPO)
assert profile['profile_digest'] == digest(profile, 'profile_digest')

# ---- the four PR #346 baselines re-derive from real #346 evidence ----------
BASELINES = {
    'CHEM-INGEST-NCERT-WORKBENCH-REDOX-REACTIONS': 11,
    'CHEM-INGEST-NCERT-WORKBENCH-BEHAVIOUR-OF-GASES': 27,
    'CHEM-INGEST-NCERT-WORKBENCH-CHEMICAL-BONDING': 38,
    'CHEM-INGEST-NCERT-WORKBENCH-SOME-BASIC-CONCEPTS': 68,
}
for instance_id, retained in BASELINES.items():
    derived = validate_instance(instance_by_id(profile, instance_id), profile, REPO)
    assert derived['ELIGIBLE_IN_SCOPE'] == retained, (instance_id, derived)
    assert derived['PLACED_UNIQUE'] == retained, (instance_id, derived)
    assert derived['MISSING'] == 0 and derived['DUPLICATE_PRIMARY'] == 0

# #346 never recorded the scanned denominator for those topics, so authoring a
# new chapter from that baseline must be refused rather than guessed at.
for instance_id in BASELINES:
    expect('AUTHORING_BEFORE_DENOMINATOR_FREEZE',
           lambda i=instance_id: assert_authoring_allowed(profile, i, REPO))

# The two independent #346 artifacts must agree; a doctored manifest is caught.
bad = copy.deepcopy(profile)
instance_by_id(bad, 'CHEM-INGEST-NCERT-WORKBENCH-REDOX-REACTIONS')['frozen_counters']['ELIGIBLE_IN_SCOPE'] = 12
instance_by_id(bad, 'CHEM-INGEST-NCERT-WORKBENCH-REDOX-REACTIONS')['frozen_counters']['PLACED_UNIQUE'] = 12
bad['profile_digest'] = ''
expect('FROZEN_COUNTERS_NOT_DERIVED_FROM_EVIDENCE', lambda: validate_profile(bad, REPO))

bad = copy.deepcopy(profile)
instance_by_id(bad, 'CHEM-INGEST-NCERT-WORKBENCH-BEHAVIOUR-OF-GASES')['evidence']['sha256'] = '0' * 64
bad['profile_digest'] = ''
expect('INGESTION_EVIDENCE_DIGEST_MISMATCH', lambda: validate_profile(bad, REPO))

bad = copy.deepcopy(profile)
instance_by_id(bad, 'CHEM-INGEST-NCERT-WORKBENCH-REDOX-REACTIONS')['corroborating_evidence']['sha256'] = '1' * 64
bad['profile_digest'] = ''
expect('INGESTION_EVIDENCE_DIGEST_MISMATCH', lambda: validate_profile(bad, REPO))

# ---- pipeline denominators: frozen, item-level, and authoring-eligible -----
for instance_id in ['CHEM-INGEST-PIPELINE-EXTERNAL-CORPUS',
                    'CHEM-INGEST-PIPELINE-SOURCE-OBLIGATIONS',
                    'CHEM-INGEST-PIPELINE-ASSESSMENT-QUESTIONS']:
    assert assert_authoring_allowed(profile, instance_id, REPO)

bad = copy.deepcopy(profile)
instance_by_id(bad, 'CHEM-INGEST-PIPELINE-EXTERNAL-CORPUS')['freeze_state'] = 'UNFROZEN'
bad['profile_digest'] = ''
expect('SOURCE_DENOMINATOR_NOT_FROZEN', lambda: validate_profile(bad, REPO))
expect('AUTHORING_BEFORE_DENOMINATOR_FREEZE',
       lambda: assert_authoring_allowed(bad, 'CHEM-INGEST-PIPELINE-EXTERNAL-CORPUS', REPO))

bad = copy.deepcopy(profile)
instance_by_id(bad, 'CHEM-INGEST-PIPELINE-SOURCE-OBLIGATIONS')['frozen_counters']['TOTAL_SCANNED'] = 13
bad['profile_digest'] = ''
expect('FROZEN_COUNTERS_NOT_DERIVED_FROM_EVIDENCE', lambda: validate_profile(bad, REPO))

bad = copy.deepcopy(profile); bad['profile_digest'] = '0' * 64
expect('INGESTION_EVIDENCE_DIGEST_MISMATCH', lambda: validate_profile(bad, REPO))

# ---- counter derivation falsifiers on item rows ---------------------------
assert counters_from_items([
    {'item_id': 'A', 'status': 'ELIGIBLE_IN_SCOPE'},
    {'item_id': 'B', 'status': 'OUT_OF_SCOPE', 'reason': 'different chapter'},
    {'item_id': 'C', 'status': 'SOURCE_UNRESOLVED', 'reason': 'extraction confidence too low'},
]) == {'TOTAL_SCANNED': 3, 'ELIGIBLE_IN_SCOPE': 1, 'PLACED_UNIQUE': 1, 'EXCLUDED_WITH_REASON': 1,
       'UNRESOLVED_WITH_REASON': 1, 'MISSING': 0, 'DUPLICATE_PRIMARY': 0}

expect('EXCLUSION_WITHOUT_REASON', lambda: counters_from_items(
    [{'item_id': 'A', 'status': 'OUT_OF_SCOPE', 'reason': ''}]))
expect('DUPLICATE_PRIMARY_PLACEMENT', lambda: counters_from_items(
    [{'item_id': 'A', 'status': 'ELIGIBLE_IN_SCOPE'}, {'item_id': 'A', 'status': 'ELIGIBLE_IN_SCOPE'}]))
expect('SOURCE_ITEM_LEDGER_UNAVAILABLE', lambda: counters_from_items([{'status': 'ELIGIBLE_IN_SCOPE'}]))

missing_row = counters_from_items([{'item_id': 'A', 'status': 'ELIGIBLE_IN_SCOPE', 'placements': 0}])
assert missing_row['MISSING'] == 1 and missing_row['PLACED_UNIQUE'] == 0
dup_row = counters_from_items([{'item_id': 'A', 'status': 'ELIGIBLE_IN_SCOPE', 'placements': 2}])
assert dup_row['DUPLICATE_PRIMARY'] == 1

bad_closure_instance = {
    'instance_id': 'TMP', 'denominator_class': 'EXTERNAL_QUESTION_CORPUS', 'scope_label': 'tmp',
    'freeze_state': 'FROZEN_ITEM_LEDGER',
    'evidence': dict(instance_by_id(profile, 'CHEM-INGEST-PIPELINE-EXTERNAL-CORPUS')['evidence']),
    'frozen_counters': {'TOTAL_SCANNED': 6, 'ELIGIBLE_IN_SCOPE': 5, 'PLACED_UNIQUE': 4,
                        'EXCLUDED_WITH_REASON': 0, 'UNRESOLVED_WITH_REASON': 1,
                        'MISSING': 1, 'DUPLICATE_PRIMARY': 0},
    'unresolved_counters': [], 'runtime_reconciliation': 'COVERAGE_CLOSURE_EXTERNAL_MATRIX'}
expect('FROZEN_COUNTERS_NOT_DERIVED_FROM_EVIDENCE',
       lambda: validate_instance(bad_closure_instance, profile, REPO))

# ---- the frozen denominator still reconciles after the pipeline runs -------
F = CHEM / 'AssessmentIntake' / 'fixtures'
report, internal = run_cold_start(load(F / 'mixed-chemistry-source.fixture.json'),
                                  load(F / 'mixed-chemistry-question-set.fixture.json'),
                                  load(F / 'mixed-chemistry-external-corpus.fixture.json'),
                                  load(F / 'mixed-chemistry-topic-scope.fixture.json'),
                                  repo_root=REPO, run_id='CHEM-INGEST-RECONCILE-RUN')
closure = internal['closure']
assert reconcile_with_closure(profile, closure, 'CHEM-INGEST-PIPELINE-EXTERNAL-CORPUS', REPO)

drifted = copy.deepcopy(closure)
drifted['external_matrix']['summary']['placed_unique_total'] = 4
drifted['external_matrix']['summary']['missing_total'] = 1
expect('POST_AUTHORING_DENOMINATOR_DRIFT',
       lambda: reconcile_with_closure(profile, drifted, 'CHEM-INGEST-PIPELINE-EXTERNAL-CORPUS', REPO))

print('CHEMISTRY SOURCE-INGESTION required falsifiers = 8 PASS')
print('CHEMISTRY SOURCE-INGESTION PR #346 baselines re-derived = 11/27/38/68 PASS')
print('CHEMISTRY SOURCE-INGESTION pipeline denominators frozen item-level = 3/3 PASS')
print('CHEMISTRY SOURCE-INGESTION post-authoring reconciliation against coverage closure = PASS')
print('CHEMISTRY SOURCE-INGESTION authoring refused on FROZEN_ELIGIBLE_ONLY baselines = PASS')
