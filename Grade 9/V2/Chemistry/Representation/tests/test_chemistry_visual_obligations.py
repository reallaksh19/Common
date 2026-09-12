#!/usr/bin/env python3
"""Falsifiers for capability-taxonomy breadth (item 3) and per-page visual
obligations (item 4).

The point of the obligation ledger is that a global count is not compliance. A
product may realize every primitive kind somewhere and still leave one
classification or mole question text-only, so obligations are counted per
lesson and per question.
"""
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
REPO = CHEM.parents[2]
sys.path[:0] = [str(D / 'engine'), str(CHEM / 'ColdStart' / 'engine')]
from bind_chemistry_visual_obligations import (
    build_ledger, validate_ledger, reconcile_realization, candidate_counters,
    validate_candidate_counters, validate_taxonomy, summarize, digest)
from chemistry_cold_start_runner import run_cold_start


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


def redigest(o, field): o[field] = ''; o[field] = digest(o, field)


taxonomy = load(CHEM / 'AssessmentScope' / 'registry' / 'chemistry-capability-taxonomy.json')
authority = load(CHEM / 'AssessmentScope' / 'authority' / 'chemistry-canonical-authority.json')
primitives = load(D / 'registry' / 'chemistry-teaching-primitive-registry.json')
page_intent = load(D / 'registry' / 'chemistry-page-intent-profile.json')
instructional = load(CHEM / 'CoreAuthoring' / 'registry' / 'chemistry-instructional-authoring-profile.json')
profile = load(D / 'registry' / 'chemistry-visual-obligation-profile.json')

# ---- item 3: the taxonomy is subject-wide, chapter-generic and closed ------
assert validate_taxonomy(taxonomy, authority, primitives, page_intent, instructional)
caps = {c['capability_id']: c for c in taxonomy['capabilities']}
assert len(caps) == 24, len(caps)

NEW = ['CAP-CLASSIFY-MATTER-COMPOSITION', 'CAP-TEST-FIXED-COMPOSITION', 'CAP-CONVERT-UNIT-SCALE',
       'CAP-BUILD-IONIC-FORMULA', 'CAP-COUNT-ENTITY-ATOMICITY', 'CAP-COMPUTE-RELATIVE-FORMULA-MASS',
       'CAP-MASS-TO-MOLES', 'CAP-MOLES-TO-ENTITIES', 'CAP-COMPUTE-CONCENTRATION',
       'CAP-USE-STOICHIOMETRIC-RATIO']
for cap in NEW:
    assert cap in caps, cap
    assert caps[cap]['allowed_visual_families'], cap
    assert caps[cap]['required_source_evidence'], cap
# Chapter-generic: no capability may be named after one of #346's four topics.
for cap in caps:
    for token in ['REDOX', 'GASES', 'BONDING', 'BASIC-CONCEPTS']:
        assert token not in cap.upper(), cap

bad = copy.deepcopy(taxonomy)
bad['capabilities'].append(dict(caps['CAP-MASS-TO-MOLES'], capability_id='CAP-REDOX-MASS-TO-MOLES'))
bad['taxonomy_digest'] = ''
expect('TOPIC_NAMED_CAPABILITY', lambda: validate_taxonomy(bad, authority, primitives, page_intent, instructional))

for field, code in [('learner_can_statement', 'CAPABILITY_WITHOUT_LEARNER_CAN_STATEMENT'),
                    ('required_source_evidence', 'CAPABILITY_WITHOUT_SOURCE_EVIDENCE'),
                    ('primary_pck_family', 'CAPABILITY_WITHOUT_PCK_FAMILY'),
                    ('verification_checks', 'CAPABILITY_WITHOUT_VERIFICATION_CHECK'),
                    ('allowed_visual_families', 'CAPABILITY_WITHOUT_ALLOWED_VISUAL_FAMILY')]:
    bad = copy.deepcopy(taxonomy)
    for record in bad['capabilities']:
        if record['capability_id'] == 'CAP-COMPUTE-CONCENTRATION':
            record[field] = '' if isinstance(record[field], str) else []
    bad['taxonomy_digest'] = ''
    expect(code, lambda b=bad: validate_taxonomy(b, authority, primitives, page_intent, instructional))

bad = copy.deepcopy(taxonomy)
for record in bad['capabilities']:
    if record['capability_id'] == 'CAP-USE-STOICHIOMETRIC-RATIO':
        record['allowed_visual_families'] = ['NOT_A_REGISTERED_PRIMITIVE']
bad['taxonomy_digest'] = ''
expect('ALLOWED_VISUAL_FAMILY_NOT_IN_PRIMITIVE_REGISTRY',
       lambda: validate_taxonomy(bad, authority, primitives, page_intent, instructional))

bad = copy.deepcopy(taxonomy)
bad['capabilities'] = [c for c in bad['capabilities'] if c['capability_id'] != 'CAP-READ-FORMULA']
bad['taxonomy_digest'] = ''
expect('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY',
       lambda: validate_taxonomy(bad, authority, primitives, page_intent, instructional))

bad = copy.deepcopy(taxonomy)
for record in bad['capabilities']:
    if record['capability_id'] == 'CAP-READ-FORMULA':
        record['primary_pck_family'] = 'CHEMICAL_VERIFICATION'
bad['taxonomy_digest'] = ''
expect('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY',
       lambda: validate_taxonomy(bad, authority, primitives, page_intent, instructional))

bad_intent = copy.deepcopy(page_intent)
bad_intent['primary_primitives_by_capability']['CAP-MASS-TO-MOLES'] = ['OXIDATION_STATE_LANE']
expect('PAGE_INTENT_PRIMITIVE_NOT_ALLOWED_BY_TAXONOMY',
       lambda: validate_taxonomy(taxonomy, authority, primitives, bad_intent, instructional))

# New families must fail closed rather than pretend to be drawable.
by_primitive = {p['primitive_id']: p for p in primitives['primitives']}
for family in ['MATTER_CLASSIFICATION_TREE', 'FIXED_COMPOSITION_TEST_TABLE', 'DIMENSIONAL_ANALYSIS_LADDER',
               'CHARGE_BALANCE_BUILDER', 'ATOMICITY_COUNT_MODEL', 'MOLAR_MASS_BREAKDOWN',
               'MASS_MOLE_PARTICLE_BRIDGE', 'PART_WHOLE_CONCENTRATION_MODEL', 'STOICHIOMETRIC_ROUTE_MAP']:
    assert by_primitive[family]['renderer_realization'] == 'RENDERER_PENDING_FAIL_CLOSED', family
    assert by_primitive[family]['decorative'] is False, family
    assert by_primitive[family]['renderer_constraints'], family

# ---- item 4: obligations are per lesson and per question ------------------
F = CHEM / 'AssessmentIntake' / 'fixtures'
report, internal = run_cold_start(load(F / 'mixed-chemistry-source.fixture.json'),
                                  load(F / 'mixed-chemistry-question-set.fixture.json'),
                                  load(F / 'mixed-chemistry-external-corpus.fixture.json'),
                                  load(F / 'mixed-chemistry-topic-scope.fixture.json'),
                                  repo_root=REPO, run_id='CHEM-VISUAL-OBLIGATION-RUN')
core1, core2, reps = internal['core1'], internal['core2'], internal['representations']

ledger = build_ledger(core1, core2, reps, taxonomy, profile)
assert validate_ledger(ledger, profile)
assert all(o['binding_status'] == 'BOUND' for o in ledger['obligations'])
assert ledger['summary']['questions_requiring_visual'] == len(core2['pages'])
assert ledger['summary']['visual_obligations_required'] == len(core1['lessons']) + len(core2['pages'])
assert ledger['summary']['visual_obligations_realized'] == 0  # nothing rendered yet

full_evidence = {o['content_ref']: list(o['bound_families']) for o in ledger['obligations']}
realized = reconcile_realization(ledger, full_evidence, profile)
assert all(o['realization_status'] == 'REALIZED' for o in realized['obligations'])
counters = candidate_counters(realized)
assert validate_candidate_counters(counters, realized)
assert counters['questions_with_required_visual'] == counters['questions_requiring_visual']
assert counters['visual_obligations_realized'] == counters['visual_obligations_required']

# One question left text-only must fail, even though everything else is drawn
# and every primitive kind is realized somewhere in the product.
text_only = dict(full_evidence)
victim = next(o['content_ref'] for o in ledger['obligations'] if o['scope'] == 'CORE2_QUESTION')
text_only[victim] = []
expect('TEXT_ONLY_WHEN_VISUAL_REQUIRED', lambda: reconcile_realization(ledger, text_only, profile))
partial = reconcile_realization(ledger, text_only, profile, require_realized=False)
assert partial['summary']['questions_with_required_visual'] < partial['summary']['questions_requiring_visual']
expect('TEXT_ONLY_WHEN_VISUAL_REQUIRED',
       lambda: validate_candidate_counters(candidate_counters(partial), partial))

# A lesson left text-only fails the same way.
lesson_only = dict(full_evidence)
lesson_only[next(o['content_ref'] for o in ledger['obligations'] if o['scope'] == 'CORE1_LESSON')] = []
expect('TEXT_ONLY_WHEN_VISUAL_REQUIRED', lambda: reconcile_realization(ledger, lesson_only, profile))

# A realized family that was never bound to this content reference is not
# evidence of local compliance.
bad = copy.deepcopy(realized)
bad['obligations'][0]['realized_families'] = ['OXIDATION_STATE_LANE']
redigest(bad, 'ledger_digest'); bad['summary'] = summarize(bad['obligations']); redigest(bad, 'ledger_digest')
expect('GLOBAL_REALIZATION_CLAIMED_FOR_LOCAL_OBLIGATION', lambda: validate_ledger(bad, profile))

bad = copy.deepcopy(ledger); bad['obligations'][0]['bound_families'] = []
bad['obligations'][0]['binding_status'] = 'MISSING'
bad['summary'] = summarize(bad['obligations']); redigest(bad, 'ledger_digest')
expect('VISUAL_OBLIGATION_MISSING', lambda: validate_ledger(bad, profile))

bad = copy.deepcopy(ledger); bad['obligations'][0]['bound_families'] = ['OXIDATION_STATE_LANE']
bad['obligations'][0]['binding_status'] = 'WRONG_FAMILY'
bad['summary'] = summarize(bad['obligations']); redigest(bad, 'ledger_digest')
expect('WRONG_VISUAL_FAMILY', lambda: validate_ledger(bad, profile))

bad = copy.deepcopy(realized); bad['summary']['visual_obligations_realized'] = 99
redigest(bad, 'ledger_digest')
expect('VISUAL_OBLIGATION_COUNTER_NOT_DERIVED_FROM_RECORDS', lambda: validate_ledger(bad, profile))

bad = copy.deepcopy(realized); bad['obligations'][0]['realized_families'] = []
redigest(bad, 'ledger_digest')
expect('UNREALIZED_VISUAL_SUBSTITUTED_BY_TEXT', lambda: validate_ledger(bad, profile))

expect('VISUAL_OBLIGATION_COUNTER_NOT_DERIVED_FROM_RECORDS',
       lambda: validate_candidate_counters({'visual_obligations_required': 0, 'visual_obligations_realized': 0,
                                            'questions_requiring_visual': 0,
                                            'questions_with_required_visual': 0}, realized))

again = build_ledger(core1, core2, reps, taxonomy, profile)
assert json.dumps(ledger, sort_keys=True) == json.dumps(again, sort_keys=True)

print('CHEMISTRY CAPABILITY TAXONOMY capabilities = %d (14 carried forward + 10 new) PASS' % len(caps))
print('CHEMISTRY CAPABILITY TAXONOMY required falsifiers = 7 PASS')
print('CHEMISTRY VISUAL OBLIGATION per-content obligations = %d bound PASS' % ledger['summary']['visual_obligations_required'])
print('CHEMISTRY VISUAL OBLIGATION text-only question rejected despite global realization = PASS')
print('CHEMISTRY VISUAL OBLIGATION new families fail closed as RENDERER_PENDING = 9 PASS')
print('CHEMISTRY VISUAL OBLIGATION deterministic replay = PASS')
