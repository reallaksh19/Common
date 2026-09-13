#!/usr/bin/env python3
"""Answer custody across Core 1 and Core 2.

The invariant PR #346 wrote in capitals and satisfied by hand:

    NO QUESTION WITHOUT A CHECKABLE ANSWER PATH.

A hint is not an answer path. A worked solution three appendices later is not,
on its own, an immediate check. So every learner-facing question resolves to
both: a compact immediate check on its own surface, and a full worked solution
or an expected-response rubric.

    questions_total == immediate_answer_checks_total == full_solutions_total
    open_response_total == expected_response_rubrics_total

The counters are reconciled two ways: against the plans the pipeline actually
produces, and against the recorded per-topic counts of the four real #346 topic
baselines (68 / 27 / 38 / 11), so the check is proved against authored content
and not only against a fixture.
"""
import argparse, copy, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]
REPO = HERE.parents[5]
PROFILE_PATH = CHEM / 'CoverageClosure' / 'registry' / 'chemistry-answer-custody-profile.json'


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


def load_profile(path=PROFILE_PATH):
    profile = load(path)
    stored = profile.get('profile_digest', '')
    if stored and stored != digest(profile, 'profile_digest'):
        fail('ANSWER_CUSTODY_PROFILE_DIGEST_DRIFT', profile.get('profile_id', 'profile'))
    return profile


def _check_answer_path(question_id, path, profile, known_solution_refs=None):
    if not path: fail('QUESTION_WITHOUT_ANSWER_PATH', question_id)
    kind = path.get('kind')
    if kind not in profile['answer_path_kinds']: fail('QUESTION_WITHOUT_ANSWER_PATH', f'{question_id}:{kind}')
    if not str(path.get('immediate_answer_check') or '').strip():
        fail('QUESTION_WITHOUT_IMMEDIATE_CHECK', question_id)
    if not str(path.get('full_solution_ref') or '').strip():
        fail('QUESTION_WITHOUT_FULL_SOLUTION', question_id)
    if known_solution_refs is not None and path['full_solution_ref'] not in known_solution_refs:
        fail('QUESTION_WITHOUT_FULL_SOLUTION', f"{question_id}:{path['full_solution_ref']} does not resolve")
    if kind == 'OPEN_RESPONSE':
        rubric = path.get('expected_response_rubric') or []
        if len(rubric) < profile['rubric_minimum_points']:
            fail('OPEN_RESPONSE_WITHOUT_RUBRIC', question_id)
    return kind


def core1_counters(core1_plan, profile):
    appendices = core1_plan['appendices']
    items = appendices['appendix_a']['items']
    solutions = {s['solution_id'] for s in appendices['appendix_b']['solutions']}
    strip = appendices.get('answer_check_strip')
    if not strip: fail('QUESTION_WITHOUT_IMMEDIATE_CHECK', 'no answer-check surface in Core 1')
    if strip.get('separate_surface_from_practice') is not True:
        fail('IMMEDIATE_CHECK_ON_SAME_SURFACE_AS_QUESTION', 'Core 1 answer-check strip')
    by_item = {e['item_ref']: e for e in strip['entries']}
    kinds = []
    for item in items:
        kinds.append(_check_answer_path(item['item_id'], item.get('answer_path'), profile, solutions))
        entry = by_item.get(item['item_id'])
        if not entry: fail('QUESTION_WITHOUT_IMMEDIATE_CHECK', item['item_id'] + ':not on the answer-check surface')
        if entry['immediate_answer_check'] != item['answer_path']['immediate_answer_check']:
            fail('ANSWER_COUNT_RECONCILIATION_FAILURE', item['item_id'] + ':strip disagrees with item')
    if len(by_item) != len(strip['entries']):
        fail('ANSWER_COUNT_RECONCILIATION_FAILURE', 'duplicate answer-check entry')
    return {'surface': 'CORE1_PRACTICE',
            'questions_total': len(items),
            'immediate_answer_checks_total': len(by_item),
            'full_solutions_total': len(appendices['appendix_b']['solutions']),
            'open_response_total': sum(1 for k in kinds if k == 'OPEN_RESPONSE'),
            'expected_response_rubrics_total': sum(
                1 for x in items if (x['answer_path'].get('expected_response_rubric') or []))}


def core2_counters(core2_plan, profile):
    pages = core2_plan['pages']
    kinds = []
    for page in pages:
        path = page.get('answer_path')
        kinds.append(_check_answer_path(page['question_ref'], path, profile))
        solution = page.get('solution_route') or {}
        if not (solution.get('reasoning_steps') and solution.get('verification_steps')):
            fail('QUESTION_WITHOUT_FULL_SOLUTION', page['question_ref'])
        # The immediate check must not be the hint ladder wearing a different hat.
        ladder = page.get('hint_ladder') or {}
        for field in ['h0_attempt_first', 'h1_notice', 'h2_rule_model_representation', 'h3_start']:
            if str(ladder.get(field) or '').strip() == path['immediate_answer_check'].strip():
                fail('QUESTION_WITHOUT_IMMEDIATE_CHECK', page['question_ref'] + ':hint reused as answer check')
    return {'surface': 'CORE2_TRANSFER',
            'questions_total': len(pages),
            'immediate_answer_checks_total': sum(
                1 for p in pages if str(p['answer_path'].get('immediate_answer_check') or '').strip()),
            'full_solutions_total': sum(
                1 for p in pages if (p.get('solution_route') or {}).get('reasoning_steps')),
            'open_response_total': sum(1 for k in kinds if k == 'OPEN_RESPONSE'),
            'expected_response_rubrics_total': sum(
                1 for p in pages if (p['answer_path'].get('expected_response_rubric') or []))}


def reconcile(counters, profile):
    for key in ['questions_total', 'immediate_answer_checks_total', 'full_solutions_total']:
        if key not in counters: fail('ANSWER_COUNT_RECONCILIATION_FAILURE', counters.get('surface', '?') + ':' + key)
    if not (counters['questions_total'] == counters['immediate_answer_checks_total'] == counters['full_solutions_total']):
        fail('ANSWER_COUNT_RECONCILIATION_FAILURE',
             f"{counters['surface']}: {counters['questions_total']}/"
             f"{counters['immediate_answer_checks_total']}/{counters['full_solutions_total']}")
    if counters['open_response_total'] != counters['expected_response_rubrics_total']:
        fail('OPEN_RESPONSE_WITHOUT_RUBRIC',
             f"{counters['surface']}: {counters['open_response_total']} open vs "
             f"{counters['expected_response_rubrics_total']} rubrics")
    return True


def validate_answer_custody(core1_plan, core2_plan, profile):
    one = core1_counters(core1_plan, profile)
    two = core2_counters(core2_plan, profile)
    reconcile(one, profile); reconcile(two, profile)
    return {'core1': one, 'core2': two,
            'questions_total': one['questions_total'] + two['questions_total'],
            'immediate_answer_checks_total': one['immediate_answer_checks_total'] + two['immediate_answer_checks_total'],
            'full_solutions_total': one['full_solutions_total'] + two['full_solutions_total']}


def reconcile_authored_baselines(profile, repo_root=REPO):
    """Reconcile against PR #346's four real, already-answer-complete topics."""
    baseline = profile['baseline_reconciliation']
    path = Path(repo_root) / baseline['evidence_path']
    if not path.exists(): fail('ANSWER_COUNT_RECONCILIATION_FAILURE', baseline['evidence_path'] + ':missing')
    if sha_file(path) != baseline['evidence_sha256']:
        fail('ANSWER_COUNT_RECONCILIATION_FAILURE', baseline['evidence_path'] + ':digest')
    manifest = load(path)
    out = {}
    for topic in manifest['topics']:
        expected = baseline['expected'].get(topic['id'])
        if expected is None: fail('ANSWER_COUNT_RECONCILIATION_FAILURE', topic['id'] + ':not declared')
        counters = {'surface': 'AUTHORED_BASELINE:' + topic['id'],
                    'questions_total': topic['retained_questions'],
                    'immediate_answer_checks_total': topic['required_immediate_answer_checks'],
                    'full_solutions_total': topic['required_full_solutions'],
                    'open_response_total': 0, 'expected_response_rubrics_total': 0}
        if counters['questions_total'] != expected:
            fail('ANSWER_COUNT_RECONCILIATION_FAILURE',
                 f"{topic['id']}: manifest {counters['questions_total']} != declared {expected}")
        reconcile(counters, profile)
        out[topic['id']] = counters
    missing = set(baseline['expected']) - set(out)
    if missing: fail('ANSWER_COUNT_RECONCILIATION_FAILURE', 'missing baselines: ' + ', '.join(sorted(missing)))
    return out


def seal(path=PROFILE_PATH):
    profile = load(path)
    profile['profile_digest'] = ''
    profile['profile_digest'] = digest(profile, 'profile_digest')
    Path(path).write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return profile['profile_digest']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--profile', default=str(PROFILE_PATH))
    ap.add_argument('--repo-root', default=str(REPO))
    ap.add_argument('--seal', action='store_true')
    a = ap.parse_args()
    if a.seal:
        print(json.dumps({'profile_digest': seal(a.profile)}, sort_keys=True)); return
    profile = load_profile(a.profile)
    baselines = reconcile_authored_baselines(profile, a.repo_root)
    print(json.dumps({'profile_id': profile['profile_id'],
                      'authored_baselines_reconciled': {k: v['questions_total'] for k, v in baselines.items()},
                      'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__': main()
