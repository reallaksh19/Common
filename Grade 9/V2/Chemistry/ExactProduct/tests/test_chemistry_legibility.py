#!/usr/bin/env python3
"""Falsifiers for the legibility target upgrade (item 7).

The point of this item is that PR #322's 8 pt rule is a floor, not a target, and
that a floor alone is gameable: shrink the leading, pack the lines, and every
font check still passes on a page no learner can study from. So the learner
targets and the page-density rule are checked against the frozen candidate's own
recorded evidence.
"""
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
sys.path.insert(0, str(D / 'engine'))
from validate_chemistry_legibility import (
    load_profile, validate_profile, validate_font_usage, validate_page_density,
    validate_leading, max_lines_per_page, document_minimum_span_pt, digest)


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


profile = load_profile()
assert validate_profile(profile)
assert profile['profile_digest'] == digest(profile, 'profile_digest')

FLOOR = profile['absolute_minimum_font_pt']
assert FLOOR == 8.0
assert profile['learner_targets']['INSTRUCTIONAL_BODY']['minimum_pt'] == 10.0
assert profile['learner_targets']['QUESTION_STEM']['minimum_pt'] == 12.0
# The learner target must be strictly above the engineering floor, or the upgrade
# is cosmetic.
assert profile['learner_targets']['INSTRUCTIONAL_BODY']['minimum_pt'] > FLOOR

# Every unenforced target has to say what blocks it, rather than quietly passing.
for role, target in profile['learner_targets'].items():
    if target['enforcement_state'] != 'ENFORCED':
        assert target.get('blocked_by'), role
assert sorted(r for r, t in profile['learner_targets'].items()
              if t['enforcement_state'] != 'ENFORCED') == ['DIAGRAM_LABEL', 'KEY_EQUATION']

# ---- the frozen candidate's own recorded evidence -------------------------
CANDIDATE = CHEM / 'ExactProduct' / 'candidates' / 'CHEM-C-L-EXACT-CANDIDATE-A'
candidate = load(CANDIDATE / 'exact-product-candidate.json')
evidence = candidate['machine_evidence']
assert evidence['learner_body_pt'] >= 10.0, evidence['learner_body_pt']
assert evidence['question_stem_pt'] >= 12.0, evidence['question_stem_pt']
for key in ['legibility_core1', 'legibility_core2']:
    leg = evidence[key]
    assert leg['page_density_pass'] is True, key
    assert leg['renderer_controlled_minimum_font_pt'] >= FLOOR, (key, leg)
    assert leg['observed_max_lines_per_page'] <= leg['max_lines_per_page_cap'], (key, leg)
    validate_font_usage(leg['font_usage_pt'], profile)

# The document minimum is measured and reported, not claimed to pass.
assert evidence['document_minimum_font_pt'] < FLOOR
assert profile['document_minimum_measurement']['enforcement_state'] == 'MEASURED_NOT_YET_ENFORCED'
measured = document_minimum_span_pt(CANDIDATE / 'core-study-guide.pdf')
assert measured is not None and measured < FLOOR

# ---- falsifiers ----------------------------------------------------------
usage = dict(evidence['legibility_core1']['font_usage_pt'])
bad = dict(usage, INSTRUCTIONAL_BODY=9.0)
expect('LEARNER_BODY_TOO_SMALL', lambda: validate_font_usage(bad, profile))
bad = dict(usage, QUESTION_STEM=10.0)
expect('LEARNER_BODY_TOO_SMALL', lambda: validate_font_usage(bad, profile))
bad = dict(usage, PAGE_FOOTER=7.5)
expect('MIN_FONT_SIZE_FAILURE', lambda: validate_font_usage(bad, profile))
bad = dict(usage, SOME_NEW_ROLE=11.0)
expect('LEGIBILITY_ROLE_NOT_MEASURED', lambda: validate_font_usage(bad, profile))
bad = {k: v for k, v in usage.items() if k != 'QUESTION_STEM'}
expect('LEGIBILITY_ROLE_NOT_MEASURED', lambda: validate_font_usage(bad, profile))

HEIGHT = 842 - 84
cap = max_lines_per_page(profile, HEIGHT)
assert cap == 60, cap
expect('PAGE_DENSITY_EXCEEDS_POLICY', lambda: validate_page_density(
    [{'page': 1, 'text_lines': cap + 1, 'text_coverage_ratio': 0.2}], profile, HEIGHT))
expect('PAGE_DENSITY_EXCEEDS_POLICY', lambda: validate_page_density(
    [{'page': 1, 'text_lines': 10, 'text_coverage_ratio': 0.9}], profile, HEIGHT))
assert validate_page_density([{'page': 1, 'text_lines': cap, 'text_coverage_ratio': 0.5}], profile, HEIGHT)

# Cramming: the font floor is satisfied but the leading is not.
assert validate_leading(10.5, 13.5, profile)
expect('PAGE_DENSITY_EXCEEDS_POLICY', lambda: validate_leading(10.5, 11.0, profile))

bad = copy.deepcopy(profile)
bad['learner_targets']['DIAGRAM_LABEL'].pop('blocked_by')
expect('LEGIBILITY_ROLE_NOT_MEASURED', lambda: validate_profile(bad))
bad = copy.deepcopy(profile)
bad['learner_targets']['INSTRUCTIONAL_BODY']['minimum_pt'] = 8.0
expect('LEARNER_BODY_TOO_SMALL', lambda: validate_profile(bad))
bad = copy.deepcopy(profile); bad['profile_digest'] = '0' * 64
tmp = Path('/tmp/chemistry-legibility-tamper.json'); tmp.write_text(json.dumps(bad), encoding='utf-8')
expect('LEGIBILITY_TARGET_PROFILE_DIGEST_DRIFT', lambda: load_profile(tmp))
tmp.unlink()

print('CHEMISTRY LEGIBILITY required falsifiers = 5 PASS')
print('CHEMISTRY LEGIBILITY learner body = %.1f pt (target 10.0, floor %.1f) PASS'
      % (evidence['learner_body_pt'], FLOOR))
print('CHEMISTRY LEGIBILITY question stem = %.1f pt (target 12.0) PASS' % evidence['question_stem_pt'])
print('CHEMISTRY LEGIBILITY page density within derived cap of %d lines PASS' % cap)
print('CHEMISTRY LEGIBILITY document minimum %.1f pt measured, not claimed as a pass = HONEST'
      % evidence['document_minimum_font_pt'])
