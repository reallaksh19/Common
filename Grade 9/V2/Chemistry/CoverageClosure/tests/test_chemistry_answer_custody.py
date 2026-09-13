#!/usr/bin/env python3
"""Falsifiers for answer custody across Core 1 and Core 2 (item 6).

Proved twice over: against the plans the pipeline actually produces, and against
the four real PR #346 topic baselines, which already satisfy the invariant by
hand at 68 / 27 / 38 / 11.
"""
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
REPO = CHEM.parents[2]
sys.path[:0] = [str(D / 'engine'), str(CHEM / 'ColdStart' / 'engine')]
from validate_chemistry_answer_custody import (
    load_profile, validate_answer_custody, core1_counters, core2_counters, reconcile,
    reconcile_authored_baselines, digest)
from chemistry_cold_start_runner import run_cold_start


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


profile = load_profile()
assert profile['profile_digest'] == digest(profile, 'profile_digest')
assert profile['closed_invariant'] == 'questions_total == immediate_answer_checks_total == full_solutions_total'
assert profile['hint_is_not_an_answer_path'] is True

# ---- the four real #346 baselines reconcile -------------------------------
baselines = reconcile_authored_baselines(profile, REPO)
assert {k: v['questions_total'] for k, v in baselines.items()} == {
    'some-basic-concepts': 68, 'behaviour-of-gases': 27, 'chemical-bonding': 38, 'redox-reactions': 11}
for topic, counters in baselines.items():
    assert counters['questions_total'] == counters['immediate_answer_checks_total'] == counters['full_solutions_total'], topic

bad = copy.deepcopy(profile); bad['baseline_reconciliation']['expected']['redox-reactions'] = 12
expect('ANSWER_COUNT_RECONCILIATION_FAILURE', lambda: reconcile_authored_baselines(bad, REPO))
bad = copy.deepcopy(profile); bad['baseline_reconciliation']['evidence_sha256'] = '0' * 64
expect('ANSWER_COUNT_RECONCILIATION_FAILURE', lambda: reconcile_authored_baselines(bad, REPO))
bad = copy.deepcopy(profile); del bad['baseline_reconciliation']['expected']['chemical-bonding']
expect('ANSWER_COUNT_RECONCILIATION_FAILURE', lambda: reconcile_authored_baselines(bad, REPO))

# ---- the live pipeline ----------------------------------------------------
F = CHEM / 'AssessmentIntake' / 'fixtures'
report, internal = run_cold_start(load(F / 'mixed-chemistry-source.fixture.json'),
                                  load(F / 'mixed-chemistry-question-set.fixture.json'),
                                  load(F / 'mixed-chemistry-external-corpus.fixture.json'),
                                  load(F / 'mixed-chemistry-topic-scope.fixture.json'),
                                  repo_root=REPO, run_id='CHEM-ANSWER-CUSTODY-RUN')
core1, core2 = internal['core1'], internal['core2']

summary = validate_answer_custody(core1, core2, profile)
one, two = summary['core1'], summary['core2']
assert one['questions_total'] == one['immediate_answer_checks_total'] == one['full_solutions_total'] == 36, one
assert two['questions_total'] == two['immediate_answer_checks_total'] == two['full_solutions_total'] == 5, two
assert one['open_response_total'] == one['expected_response_rubrics_total'] == 36, one
assert two['open_response_total'] == 0, two
assert summary['questions_total'] == 41

appendix_schema = Draft202012Validator(
    load(CHEM / 'CoreAuthoring' / 'contracts' / 'chemistry-core-appendix-contract.schema.json'))
appendix_schema.validate(core1['appendices'])
page_schema = Draft202012Validator(
    load(CHEM / 'Core2Transfer' / 'contracts' / 'chemistry-transfer-question-page.schema.json'))
for page in core2['pages']:
    page_schema.validate(page)

# Every Core 2 immediate check names an option that really is on the page.
for page in core2['pages']:
    path = page['answer_path']
    assert path['kind'] in profile['answer_path_kinds'], path
    if page['source_options']:
        assert path['kind'] == 'CLOSED_OPTION'
        assert page['solution_route']['final_answer'] in path['immediate_answer_check']
    assert path['full_solution_ref'] == page['question_ref'] + '-SOLUTION'

# The quick answers live on their own surface, not on the practice page.
strip = core1['appendices']['answer_check_strip']
assert strip['separate_surface_from_practice'] is True
assert len(strip['entries']) == 36

# ---- falsifiers ----------------------------------------------------------
bad = copy.deepcopy(core1); del bad['appendices']['appendix_a']['items'][0]['answer_path']
expect('QUESTION_WITHOUT_ANSWER_PATH', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); bad['appendices']['appendix_a']['items'][1]['answer_path']['immediate_answer_check'] = '  '
expect('QUESTION_WITHOUT_IMMEDIATE_CHECK', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); bad['appendices']['appendix_a']['items'][2]['answer_path']['full_solution_ref'] = 'B-SOL-NOT-REAL'
expect('QUESTION_WITHOUT_FULL_SOLUTION', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); bad['appendices']['appendix_a']['items'][3]['answer_path']['expected_response_rubric'] = ['only one point']
expect('OPEN_RESPONSE_WITHOUT_RUBRIC', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); bad['appendices']['answer_check_strip']['entries'] = bad['appendices']['answer_check_strip']['entries'][:-1]
expect('QUESTION_WITHOUT_IMMEDIATE_CHECK', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); bad['appendices']['answer_check_strip']['entries'][0]['immediate_answer_check'] = 'Something else.'
expect('ANSWER_COUNT_RECONCILIATION_FAILURE', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); bad['appendices']['answer_check_strip']['separate_surface_from_practice'] = False
expect('IMMEDIATE_CHECK_ON_SAME_SURFACE_AS_QUESTION', lambda: core1_counters(bad, profile))

bad = copy.deepcopy(core1); del bad['appendices']['answer_check_strip']
expect('QUESTION_WITHOUT_IMMEDIATE_CHECK', lambda: core1_counters(bad, profile))

# Losing a full solution while keeping the question breaks reconciliation.
bad = copy.deepcopy(core1)
victim = bad['appendices']['appendix_b']['solutions'].pop()
bad['appendices']['appendix_a']['items'] = [
    x for x in bad['appendices']['appendix_a']['items'] if x['item_id'] != victim['item_ref']] + \
    [dict(x, answer_path=dict(x['answer_path'], full_solution_ref=bad['appendices']['appendix_b']['solutions'][0]['solution_id']))
     for x in bad['appendices']['appendix_a']['items'] if x['item_id'] == victim['item_ref']]
expect('ANSWER_COUNT_RECONCILIATION_FAILURE', lambda: reconcile(core1_counters(bad, profile), profile))

bad = copy.deepcopy(core2); del bad['pages'][0]['answer_path']
expect('QUESTION_WITHOUT_ANSWER_PATH', lambda: core2_counters(bad, profile))

bad = copy.deepcopy(core2); bad['pages'][1]['solution_route']['verification_steps'] = []
expect('QUESTION_WITHOUT_FULL_SOLUTION', lambda: core2_counters(bad, profile))

# A hint reused as the answer check is not an answer check.
bad = copy.deepcopy(core2)
page = bad['pages'][2]
page['answer_path']['immediate_answer_check'] = page['hint_ladder']['h3_start']
expect('QUESTION_WITHOUT_IMMEDIATE_CHECK', lambda: core2_counters(bad, profile))

# An open-response transfer item with no rubric.
bad = copy.deepcopy(core2)
bad['pages'][3]['answer_path'] = dict(bad['pages'][3]['answer_path'], kind='OPEN_RESPONSE')
expect('OPEN_RESPONSE_WITHOUT_RUBRIC', lambda: core2_counters(bad, profile))

expect('ANSWER_COUNT_RECONCILIATION_FAILURE', lambda: reconcile(
    {'surface': 'TEST', 'questions_total': 5, 'immediate_answer_checks_total': 4,
     'full_solutions_total': 5, 'open_response_total': 0, 'expected_response_rubrics_total': 0}, profile))

bad = copy.deepcopy(profile); bad['profile_digest'] = '0' * 64
tmp = Path('/tmp/chemistry-answer-custody-tamper.json'); tmp.write_text(json.dumps(bad), encoding='utf-8')
expect('ANSWER_CUSTODY_PROFILE_DIGEST_DRIFT', lambda: load_profile(tmp))
tmp.unlink()

print('CHEMISTRY ANSWER CUSTODY required falsifiers = 7 PASS')
print('CHEMISTRY ANSWER CUSTODY Core1 practice = %d/%d/%d questions/checks/solutions PASS'
      % (one['questions_total'], one['immediate_answer_checks_total'], one['full_solutions_total']))
print('CHEMISTRY ANSWER CUSTODY Core2 transfer = %d/%d/%d questions/checks/solutions PASS'
      % (two['questions_total'], two['immediate_answer_checks_total'], two['full_solutions_total']))
print('CHEMISTRY ANSWER CUSTODY PR #346 authored baselines = 68/27/38/11 reconciled PASS')
print('CHEMISTRY ANSWER CUSTODY immediate check on its own surface = PASS')
