#!/usr/bin/env python3
"""Helper-pedagogy and Core 1 instructional-depth gates.

Two related things a compliant renderer cannot fix downstream.

**Helper pedagogy.** PR #346 found this empirically: a hint that names a method
("use the definition", "apply the mole method") leaves the learner exactly where
they were. A usable hint produces an observable action — something written,
drawn, counted, cancelled, compared, labelled or tested. ``classify_hint``
resolves a hint against the declared intent classes in
``chemistry-helper-pedagogy-profile.json``; ``NON_ACTIONABLE_HINT`` fires when a
hint that must be actionable resolves to none of them, or matches one of the
profile's non-actionable patterns.

H2 is deliberately exempt from the imperative requirement: its job is to supply
the rule, so a statement is correct there. What H2 may *not* do is name a rule
without stating it, which the same falsifier catches.

**Core 1 depth.** ``chemistry-core1-depth-profile.json`` lists the spine roles a
full-learning capability owes: canonical model, plain-language explanation,
technical reconstruction, worked example, misconception repair, guided, faded,
independent, verification, transfer. A lesson that states the rule and stops is
a summary, and ``CORE1_SUMMARY_LEVEL_NOT_STUDY_MATERIAL`` says so.
"""
import argparse, copy, hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]
HELPER_PATH = CHEM / 'CoreAuthoring' / 'registry' / 'chemistry-helper-pedagogy-profile.json'
DEPTH_PATH = CHEM / 'CoreAuthoring' / 'registry' / 'chemistry-core1-depth-profile.json'

HINT_STAGE_FIELDS = {
    'H0_ATTEMPT_FIRST': 'h0_attempt_first',
    'H1_NOTICE': 'h1_notice',
    'H2_RULE_MODEL_REPRESENTATION': 'h2_rule_model_representation',
    'H3_START': 'h3_start',
}


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


def words(text): return [w for w in re.split(r'[^\w’\'-]+', str(text or '')) if w]


# ---------------------------------------------------------------------------
# helper pedagogy
# ---------------------------------------------------------------------------

def load_helper_profile(path=HELPER_PATH):
    profile = load(path)
    stored = profile.get('profile_digest', '')
    if stored and stored != digest(profile, 'profile_digest'):
        fail('HELPER_PEDAGOGY_PROFILE_DIGEST_DRIFT', profile.get('profile_id', 'profile'))
    return profile


def validate_helper_profile(profile):
    if profile.get('subject') != 'CHEMISTRY': fail('HELPER_INTENT_CLASS_UNDECLARED', 'subject')
    required = {'WRITE_RELATION', 'WRITE_SPECIES_OR_FORMULA', 'COUNT_FEATURE', 'CANCEL_UNIT',
                'COMPARE_QUANTITY', 'TEST_DEFINITION', 'VERIFY_RESULT'}
    classes = set(profile['helper_intent_classes'])
    if not required <= classes: fail('HELPER_INTENT_CLASS_UNDECLARED', ', '.join(sorted(required - classes)))
    for name, record in profile['helper_intent_classes'].items():
        if not record.get('learner_action_verbs'): fail('HELPER_INTENT_CLASS_UNDECLARED', name + ':verbs')
        if not record.get('produces'): fail('HELPER_INTENT_CLASS_UNDECLARED', name + ':produces')
        if not record.get('example_good') or not record.get('example_bad'):
            fail('HELPER_INTENT_CLASS_UNDECLARED', name + ':examples')
        # The declared bad example must be caught, and the good one must pass.
        if classify_hint(record['example_bad'], profile):
            fail('NON_ACTIONABLE_HINT', name + ':declared bad example classifies as actionable')
        if name not in classify_hint(record['example_good'], profile):
            fail('HELPER_INTENT_CLASS_UNDECLARED', name + ':declared good example does not classify as its own class')
    for stage, record in profile['stage_requirements'].items():
        unknown = set(record.get('allowed_intent_classes', [])) - classes
        if unknown: fail('HELPER_INTENT_CLASS_UNDECLARED', stage + ':' + ', '.join(sorted(unknown)))
    for family, record in profile['first_move_by_pck_family'].items():
        if record['intent_class'] not in classes: fail('HELPER_INTENT_CLASS_UNDECLARED', family)
        if record['intent_class'] not in classify_hint(record['helper_text'], profile):
            fail('NON_ACTIONABLE_HINT', family + ':declared first move is not actionable as its own class')
    return True


def non_actionable_match(text, profile):
    for pattern in profile['non_actionable_patterns']:
        if re.search(pattern, str(text or ''), re.IGNORECASE):
            return pattern
    return None


def classify_hint(text, profile):
    """Return the intent classes a hint satisfies, or an empty list."""
    lowered = ' ' + ' '.join(words(text)).lower() + ' '
    if non_actionable_match(text, profile): return []
    found = []
    for name, record in profile['helper_intent_classes'].items():
        for verb in record['learner_action_verbs']:
            if ' ' + verb.lower() + ' ' in lowered or lowered.strip().startswith(verb.lower() + ' '):
                found.append(name); break
    return sorted(found)


def assert_actionable(text, stage, profile, where=''):
    requirement = profile['stage_requirements'].get(stage)
    if requirement is None: fail('HELPER_INTENT_CLASS_UNDECLARED', stage)
    pattern = non_actionable_match(text, profile)
    if pattern: fail('NON_ACTIONABLE_HINT', f'{where or stage}: matches non-actionable pattern {pattern!r}')
    if requirement.get('must_instruct_attempt_before_support'):
        lowered = ' '.join(words(text)).lower()
        if not re.search(r'\b(attempt|try)\b', lowered):
            fail('NON_ACTIONABLE_HINT', f'{where or stage}: does not instruct an attempt')
        if not re.search(r'\b(before|first)\b', lowered):
            fail('NON_ACTIONABLE_HINT', f'{where or stage}: does not put the attempt before support')
        return ['ATTEMPT_FIRST']
    if requirement.get('must_state_rule_content'):
        if len(words(text)) < requirement.get('minimum_words', 8):
            fail('NON_ACTIONABLE_HINT', f'{where or stage}: names a rule without stating it')
        return ['RULE_STATEMENT']
    if not requirement.get('must_be_actionable'): return []
    classes = classify_hint(text, profile)
    allowed = set(requirement['allowed_intent_classes'])
    if not classes: fail('NON_ACTIONABLE_HINT', f'{where or stage}: "{text}" produces no learner action')
    if not set(classes) & allowed:
        fail('NON_ACTIONABLE_HINT', f'{where or stage}: {classes} not allowed at this stage')
    return classes


def validate_hint_ladder(page, profile):
    ladder = page['hint_ladder']
    out = {}
    for stage, field in HINT_STAGE_FIELDS.items():
        out[stage] = assert_actionable(ladder[field], stage, profile, f"{page['question_ref']}:{stage}")
    solution = page.get('solution_route') or {}
    steps = [str(x).strip() for x in solution.get('reasoning_steps') or []]
    # A single-letter MCQ label cannot be leak-checked by substring (every hint
    # contains the letter "b" somewhere), so the answer-leak check uses the
    # spelled-out answer forms. A short option label is instead protected by the
    # answer-custody contract, which keeps the immediate check on its own surface.
    answers = [str(solution.get('final_answer') or '').strip(),
               str(solution.get('chemical_language_response') or '').strip()]
    answers = [a for a in answers if len(a) > 3]
    leak_stages = set(profile.get('answer_leak_checked_stages') or HINT_STAGE_FIELDS)
    for stage, field in HINT_STAGE_FIELDS.items():
        hint = str(ladder[field] or '').strip()
        if stage in leak_stages:
            for answer in answers:
                if answer.lower() in hint.lower():
                    fail('HINT_DUPLICATES_FULL_SOLUTION', f"{page['question_ref']}:{stage}")
        if hint and hint in steps:
            fail('HINT_DUPLICATES_FULL_SOLUTION', f"{page['question_ref']}:{stage}:reproduces a solution step")
    return out


def validate_core2_helpers(core2_plan, profile):
    validate_helper_profile(profile)
    return {page['question_ref']: validate_hint_ladder(page, profile) for page in core2_plan['pages']}


def validate_core1_helpers(core1_plan, profile):
    validate_helper_profile(profile)
    out = {}
    for lesson in core1_plan['lessons']:
        helper = lesson.get('concept_helper')
        if not helper:
            continue  # verify-only and probe lessons carry no stuck-helper
        out[lesson['capability_ref']] = assert_actionable(
            helper, 'CORE1_CONCEPT_HELPER', profile, lesson['capability_ref'] + ':concept_helper')
    return out


def first_move_for(pck_family, profile):
    record = profile['first_move_by_pck_family'].get(pck_family)
    if not record: fail('HELPER_MISSING_FOR_PCK_FAMILY', str(pck_family))
    return record['helper_text']


# ---------------------------------------------------------------------------
# Core 1 instructional depth
# ---------------------------------------------------------------------------

def load_depth_profile(path=DEPTH_PATH):
    profile = load(path)
    stored = profile.get('profile_digest', '')
    if stored and stored != digest(profile, 'profile_digest'):
        fail('CORE1_DEPTH_PROFILE_DIGEST_DRIFT', profile.get('profile_id', 'profile'))
    return profile


def _role_present(lesson, role):
    value = lesson.get(role['lesson_field'])
    kind = role['kind']
    if kind == 'TEXT':
        return bool(str(value or '').strip()) and len(words(value)) >= role.get('minimum_words', 1)
    if kind == 'STEPS':
        return isinstance(value, list) and len(value) >= role.get('minimum_items', 1)
    if kind == 'WORKED':
        if not value: return False
        return (len(value.get('reasoning_steps') or []) >= role.get('minimum_reasoning_steps', 1)
                and len(value.get('verification_steps') or []) >= role.get('minimum_verification_steps', 1))
    if kind == 'REPAIR':
        if not value: return False
        return (len(value.get('repair_steps') or []) >= role.get('minimum_repair_steps', 1)
                and bool(str(value.get('minimal_contrast') or '').strip())
                and bool(str(value.get('retry_prompt') or '').strip()))
    if kind == 'ATTEMPT':
        return bool(value) and bool(str((value or {}).get('prompt') or '').strip())
    fail('INSTRUCTIONAL_SPINE_INCOMPLETE', role['role'] + ':unknown kind')


def validate_lesson_depth(lesson, depth_profile, helper_profile=None):
    mode = lesson['lesson_mode']
    roles = {r['role']: r for r in depth_profile['required_spine_roles']}
    cap = lesson['capability_ref']
    if mode == 'FULL_LEARNING':
        # Present-but-thin is a more specific diagnosis than absent, so it is
        # reported first: a worked example with one step and no worked example at
        # all are different authoring defects.
        worked = lesson.get('worked_example')
        if worked and len(worked.get('reasoning_steps') or []) < roles['WORKED_EXAMPLE']['minimum_reasoning_steps']:
            fail('WORKED_EXAMPLE_WITHOUT_VISIBLE_STEPS', cap)
        repair = lesson.get('misconception_repair')
        if repair and not str(repair.get('minimal_contrast') or '').strip():
            fail('MISCONCEPTION_REPAIR_WITHOUT_CONTRAST', cap)
        missing = [name for name, role in roles.items() if not _role_present(lesson, role)]
        if missing:
            if {'TECHNICAL_RECONSTRUCTION', 'WORKED_EXAMPLE', 'MISCONCEPTION_REPAIR'} & set(missing):
                fail('CORE1_SUMMARY_LEVEL_NOT_STUDY_MATERIAL', f'{cap}: missing {sorted(missing)}')
            fail('INSTRUCTIONAL_SPINE_INCOMPLETE', f'{cap}: missing {sorted(missing)}')
        prompts = {str((lesson.get(f) or {}).get('prompt') or '')
                   for f in ['guided_attempt', 'faded_attempt', 'independent_attempt']}
        if len(prompts) < 3: fail('SUPPORT_FADING_NOT_DIFFERENTIATED', cap)
    elif mode == 'CONCISE_VERIFY_ONLY':
        for name in depth_profile['verify_only_required_roles']:
            if not _role_present(lesson, roles[name]): fail('INSTRUCTIONAL_SPINE_INCOMPLETE', f'{cap}:{name}')
        for name in depth_profile['verify_only_forbidden_roles']:
            if lesson.get(roles[name]['lesson_field']): fail('INSTRUCTIONAL_SPINE_INCOMPLETE', f'{cap}:{name} forbidden')
    else:
        for name in depth_profile['probe_required_roles']:
            if not _role_present(lesson, roles[name]): fail('INSTRUCTIONAL_SPINE_INCOMPLETE', f'{cap}:{name}')
        for name in depth_profile['probe_forbidden_roles']:
            if lesson.get(roles[name]['lesson_field']): fail('INSTRUCTIONAL_SPINE_INCOMPLETE', f'{cap}:{name} forbidden')
    if helper_profile is not None and roles['CONCEPT_HELPER'].get('actionable') and lesson.get('concept_helper'):
        try:
            assert_actionable(lesson['concept_helper'], 'CORE1_CONCEPT_HELPER', helper_profile, cap)
        except ValueError as exc:
            fail('DEPTH_ROLE_NOT_ACTIONABLE', str(exc))
    return True


def validate_core1_depth(core1_plan, depth_profile, helper_profile=None):
    report = {'full_learning': 0, 'concise_verify_only': 0, 'probe': 0}
    for lesson in core1_plan['lessons']:
        validate_lesson_depth(lesson, depth_profile, helper_profile)
        report[lesson['lesson_mode'].lower()] = report.get(lesson['lesson_mode'].lower(), 0) + 1
    return report


def seal(path, field):
    record = load(path)
    record[field] = ''
    record[field] = digest(record, field)
    Path(path).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return record[field]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seal', action='store_true'); a = ap.parse_args()
    if a.seal:
        print(json.dumps({'helper_profile_digest': seal(HELPER_PATH, 'profile_digest'),
                          'depth_profile_digest': seal(DEPTH_PATH, 'profile_digest')}, sort_keys=True)); return
    helper = load_helper_profile(); validate_helper_profile(helper); depth = load_depth_profile()
    print(json.dumps({'helper_profile_id': helper['profile_id'],
                      'intent_classes': len(helper['helper_intent_classes']),
                      'pck_first_moves': len(helper['first_move_by_pck_family']),
                      'depth_profile_id': depth['profile_id'],
                      'spine_roles': len(depth['required_spine_roles']),
                      'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__': main()
