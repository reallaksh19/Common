#!/usr/bin/env python3
"""Falsifiers for helper pedagogy and Core 1 instructional depth (item 5).

Exercised against the real pipeline plans, not a fixture: every Core 2 hint
ladder the cold-start producer actually emits must pass the actionability gate,
and every full-learning Core 1 lesson must carry the whole instructional spine.
"""
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
REPO = CHEM.parents[2]
sys.path[:0] = [str(D / 'engine'), str(CHEM / 'ColdStart' / 'engine')]
from validate_chemistry_instructional_depth import (
    load_helper_profile, validate_helper_profile, load_depth_profile, classify_hint,
    assert_actionable, validate_core2_helpers, validate_core1_helpers, validate_core1_depth,
    validate_lesson_depth, first_move_for, non_actionable_match)
from chemistry_cold_start_runner import run_cold_start


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


helper = load_helper_profile()
depth = load_depth_profile()
assert validate_helper_profile(helper)

# ---- the rule PR #346 discovered, now machine-checkable --------------------
BAD = ['Use the definition.', 'Use formula writing rules.', 'Apply the mole method.',
       'Recall the law of conservation of mass.', 'Use the mole formula.',
       'Think about the difference.', 'Verify your answer.',
       'A first move should expose the governing evidence, representation or rule.']
GOOD = ['Write n = m/M. Substitute the sample mass and molar mass with units. Cancel g; the remaining unit should be mol.',
        'Write Ca²⁺ and PO₄³⁻. How many calcium ions give +6? How many phosphate ions give −6?',
        'First split the entries into mixtures and pure substances, then ask of each pure substance whether it holds one kind of atom.',
        'Count H and O atoms separately on both sides of the equation.',
        'Circle the superscript and label it before evaluating the options.']
for text in BAD:
    assert not classify_hint(text, helper), text
    expect('NON_ACTIONABLE_HINT', lambda t=text: assert_actionable(t, 'H3_START', helper))
for text in GOOD:
    assert classify_hint(text, helper), text
    assert assert_actionable(text, 'H3_START', helper)

# H2 is allowed to be a statement — its job is to supply the rule — but naming a
# rule without stating it is still caught.
assert assert_actionable('A coefficient multiplies every atom in the formula that follows it.',
                         'H2_RULE_MODEL_REPRESENTATION', helper) == ['RULE_STATEMENT']
expect('NON_ACTIONABLE_HINT', lambda: assert_actionable('Use the coefficient rule.',
                                                        'H2_RULE_MODEL_REPRESENTATION', helper))
expect('NON_ACTIONABLE_HINT', lambda: assert_actionable('Balancing rule.',
                                                        'H2_RULE_MODEL_REPRESENTATION', helper))

# H0 is not a content hint; it must instruct the attempt before support.
assert assert_actionable('Attempt the original question independently before opening any hint or solution.',
                         'H0_ATTEMPT_FIRST', helper) == ['ATTEMPT_FIRST']
expect('NON_ACTIONABLE_HINT', lambda: assert_actionable('Support is revealed progressively.',
                                                        'H0_ATTEMPT_FIRST', helper))

expect('HELPER_MISSING_FOR_PCK_FAMILY', lambda: first_move_for('NO_SUCH_PCK_FAMILY', helper))
assert non_actionable_match('Apply the supplied rule only after checking the recorded condition or exception.', helper) is None

bad = copy.deepcopy(helper)
bad['helper_intent_classes']['COUNT_FEATURE']['example_bad'] = 'Count the atoms on both sides.'
expect('NON_ACTIONABLE_HINT', lambda: validate_helper_profile(bad))
bad = copy.deepcopy(helper); del bad['helper_intent_classes']['CANCEL_UNIT']
expect('HELPER_INTENT_CLASS_UNDECLARED', lambda: validate_helper_profile(bad))
bad = copy.deepcopy(helper)
bad['first_move_by_pck_family']['CONSERVATION_ATOM_CHARGE_SPECIES']['helper_text'] = 'Use the conservation rule.'
expect('NON_ACTIONABLE_HINT', lambda: validate_helper_profile(bad))

# ---- real pipeline plans --------------------------------------------------
F = CHEM / 'AssessmentIntake' / 'fixtures'
report, internal = run_cold_start(load(F / 'mixed-chemistry-source.fixture.json'),
                                  load(F / 'mixed-chemistry-question-set.fixture.json'),
                                  load(F / 'mixed-chemistry-external-corpus.fixture.json'),
                                  load(F / 'mixed-chemistry-topic-scope.fixture.json'),
                                  repo_root=REPO, run_id='CHEM-HELPER-DEPTH-RUN')
core1, core2 = internal['core1'], internal['core2']

ladders = validate_core2_helpers(core2, helper)
assert len(ladders) == len(core2['pages'])
for question_ref, stages in ladders.items():
    assert stages['H0_ATTEMPT_FIRST'] == ['ATTEMPT_FIRST'], question_ref
    assert stages['H1_NOTICE'], question_ref
    assert stages['H3_START'], question_ref
    assert stages['H2_RULE_MODEL_REPRESENTATION'] == ['RULE_STATEMENT'], question_ref

helpers = validate_core1_helpers(core1, helper)
full = [l for l in core1['lessons'] if l['lesson_mode'] == 'FULL_LEARNING']
assert len(helpers) == len(full), (len(helpers), len(full))

counts = validate_core1_depth(core1, depth, helper)
assert counts['full_learning'] == len(full) and counts['full_learning'] > 0

# A hint that leaks the spelled-out answer is not a hint.
bad_core2 = copy.deepcopy(core2)
page = bad_core2['pages'][0]
answer = page['solution_route']['chemical_language_response']
assert len(answer) > 3, answer
page['hint_ladder']['h3_start'] = 'Write down ' + answer + ' and move on.'
expect('HINT_DUPLICATES_FULL_SOLUTION', lambda: validate_core2_helpers(bad_core2, helper))

# A hint that copies a solution reasoning step verbatim is also a leak.
bad_core2 = copy.deepcopy(core2)
page = bad_core2['pages'][2]
page['hint_ladder']['h3_start'] = page['solution_route']['reasoning_steps'][0]
expect('HINT_DUPLICATES_FULL_SOLUTION', lambda: validate_core2_helpers(bad_core2, helper))

bad_core2 = copy.deepcopy(core2)
bad_core2['pages'][1]['hint_ladder']['h1_notice'] = 'Use the definition.'
expect('NON_ACTIONABLE_HINT', lambda: validate_core2_helpers(bad_core2, helper))

bad_core1 = copy.deepcopy(core1)
for lesson in bad_core1['lessons']:
    if lesson['lesson_mode'] == 'FULL_LEARNING':
        lesson['concept_helper'] = 'Use the definition.'
expect('NON_ACTIONABLE_HINT', lambda: validate_core1_helpers(bad_core1, helper))

# Long enough to satisfy the depth floor, so the failure has to come from the
# actionability gate rather than from the role simply being absent.
bad_core1 = copy.deepcopy(core1)
for lesson in bad_core1['lessons']:
    if lesson['lesson_mode'] == 'FULL_LEARNING':
        lesson['concept_helper'] = 'Remember the mole conversion method and everything else follows.'
expect('DEPTH_ROLE_NOT_ACTIONABLE', lambda: validate_core1_depth(bad_core1, depth, helper))

# ---- depth falsifiers ----------------------------------------------------
def mutate(field, value):
    plan = copy.deepcopy(core1)
    for lesson in plan['lessons']:
        if lesson['lesson_mode'] == 'FULL_LEARNING':
            lesson[field] = value
    return plan


expect('CORE1_SUMMARY_LEVEL_NOT_STUDY_MATERIAL', lambda: validate_core1_depth(mutate('reconstruction_steps', []), depth, helper))
expect('CORE1_SUMMARY_LEVEL_NOT_STUDY_MATERIAL', lambda: validate_core1_depth(mutate('worked_example', None), depth, helper))
expect('CORE1_SUMMARY_LEVEL_NOT_STUDY_MATERIAL', lambda: validate_core1_depth(mutate('misconception_repair', None), depth, helper))
expect('INSTRUCTIONAL_SPINE_INCOMPLETE', lambda: validate_core1_depth(mutate('transfer_bridge', ''), depth, helper))
expect('INSTRUCTIONAL_SPINE_INCOMPLETE', lambda: validate_core1_depth(mutate('faded_attempt', None), depth, helper))
expect('INSTRUCTIONAL_SPINE_INCOMPLETE', lambda: validate_core1_depth(mutate('ordinary_language_explanation', 'Short.'), depth, helper))

lesson = copy.deepcopy(full[0])
lesson['worked_example'] = dict(lesson['worked_example'], reasoning_steps=['one'])
expect('WORKED_EXAMPLE_WITHOUT_VISIBLE_STEPS', lambda: validate_lesson_depth(lesson, depth, helper))

lesson = copy.deepcopy(full[0])
lesson['misconception_repair'] = dict(lesson['misconception_repair'], minimal_contrast='')
expect('MISCONCEPTION_REPAIR_WITHOUT_CONTRAST', lambda: validate_lesson_depth(lesson, depth, helper))

lesson = copy.deepcopy(full[0])
shared = lesson['guided_attempt']['prompt']
lesson['faded_attempt'] = dict(lesson['faded_attempt'], prompt=shared)
lesson['independent_attempt'] = dict(lesson['independent_attempt'], prompt=shared)
expect('SUPPORT_FADING_NOT_DIFFERENTIATED', lambda: validate_lesson_depth(lesson, depth, helper))

# The repaired Core 1 helper really is one of the governed learner-directed
# first moves, and the author-voice text that used to be printed is gone.
governed = {record['helper_text'] for record in helper['first_move_by_pck_family'].values()}
for lesson in full:
    assert lesson['concept_helper'] in governed, lesson['capability_ref']
    assert 'A first move should expose' not in lesson['concept_helper'], lesson['capability_ref']
    assert 'Elicit the wrong model.' not in (lesson['misconception_repair'] or {}).get('repair_steps', []), lesson['capability_ref']

print('CHEMISTRY HELPER PEDAGOGY intent classes = %d PASS' % len(helper['helper_intent_classes']))
print('CHEMISTRY HELPER PEDAGOGY per-family actionable first moves = %d PASS' % len(helper['first_move_by_pck_family']))
print('CHEMISTRY HELPER PEDAGOGY Core2 hint ladders actionable = %d/%d PASS' % (len(ladders), len(core2['pages'])))
print('CHEMISTRY HELPER PEDAGOGY required falsifiers = 4 PASS')
print('CHEMISTRY CORE1 DEPTH full-learning spine complete = %d lessons PASS' % counts['full_learning'])
print('CHEMISTRY CORE1 DEPTH required falsifiers = 6 PASS')
