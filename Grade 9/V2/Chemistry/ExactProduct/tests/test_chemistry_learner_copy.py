#!/usr/bin/env python3
"""Falsifiers for kid-appropriate learner-facing nomenclature.

Two things are proved here.

1. The mapping registry is a **separation**, not a rename: every internal role
   identifier keeps its exact spelling as a key, and every learner-facing value
   is plain English that no longer looks like the identifier.
2. The guard actually catches the leak class PR #322's identifier-shape guard
   cannot see — a clinical section title such as "Misconception Repair" or
   "Representation path", which contains no identifier shape at all.
"""
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
sys.path.insert(0, str(D / 'engine'))
import learner_copy_guard as COPY
import learner_surface_guard as GUARD
from learner_copy_guard import (load_registry, validate_registry, title_for,
                                assert_heading_safe, assert_surface_safe, scan_pages, digest)


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


registry = load_registry()
assert validate_registry(registry)
assert registry['registry_digest'] == digest(registry, 'registry_digest')
assert registry['resolution_policy'] == 'FAIL_CLOSED_NEVER_PRINT_INTERNAL_ROLE'

# ---- internal identifiers are untouched -----------------------------------
# These are the spellings schemas, enum values and falsifier names use. If a
# future change "cleans them up", this assertion is the thing that breaks.
for role in ['MISCONCEPTION_REPAIR', 'GUIDED_ATTEMPT', 'FADED_ATTEMPT', 'INDEPENDENT_ATTEMPT',
             'CHEMICAL_VERIFICATION', 'ACTIVATION', 'REPRESENTATION', 'WHY_RECONSTRUCTION',
             'H0_ATTEMPT_FIRST', 'H1_NOTICE', 'H2_RULE_MODEL_REPRESENTATION', 'H3_START',
             'REASONING_ROUTE', 'TRANSFER', 'DIAGNOSTIC_PROBE', 'EVIDENCE_INTERPRETATION',
             'IMMEDIATE_ANSWER_CHECK', 'EXPECTED_RESPONSE_RUBRIC']:
    assert role in registry['titles'], role

# ---- the learner-facing side is warm, plain, and not the identifier --------
assert title_for('MISCONCEPTION_REPAIR', registry) == 'Common mistake to avoid'
assert title_for('CHEMICAL_VERIFICATION', registry) == 'Check your answer'
assert title_for('GUIDED_ATTEMPT', registry) == 'Try it with help'
assert title_for('FADED_ATTEMPT', registry) == 'Try it with less help'
assert title_for('INDEPENDENT_ATTEMPT', registry) == 'Now try it on your own'
for role, entry in registry['titles'].items():
    title = entry['learner_facing_title']
    assert '_' not in title and not title.isupper(), (role, title)
    assert not GUARD.find_internal_identifiers(title), (role, title)

# An unmapped role fails closed. It must NEVER degrade to a prettified
# identifier, because a prettified identifier is the leak being guarded.
expect('LEARNER_TITLE_MISSING_FOR_ROLE', lambda: title_for('SOME_FUTURE_ROLE', registry))
expect('LEARNER_TITLE_MISSING_FOR_ROLE', lambda: title_for(None, registry))

# ---- the guard catches jargon the #322 identifier-shape guard cannot ------
for clinical in ['Misconception Repair', 'Misconception clinic', 'Representation path',
                 'Reasoning route', 'Faded practice', 'Guided attempt', 'Independent attempt',
                 'Reconstruct the reasoning', 'Verification', 'Orient / activate',
                 'Diagnostic probe', 'Treatment depth', 'Hint ladder', 'Expected-response rubric']:
    assert not GUARD.find_internal_identifiers(clinical), clinical  # #322's guard sees nothing
    assert COPY.find_heading_jargon(clinical, registry), clinical   # this guard does
    expect('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE',
           lambda t=clinical: assert_heading_safe(t, registry, 'subheading'))

for warm in [title_for(r, registry) for r in registry['titles']]:
    assert assert_heading_safe(warm, registry)

assert assert_surface_safe('Write n = m/M, then cancel grams and check that moles remain.', registry)
expect('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE',
       lambda: assert_surface_safe('This page closes the capability record.', registry))
expect('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE',
       lambda: assert_surface_safe('Derived from the study model for this learner.', registry))

assert scan_pages(['clean page', 'a misconception slipped in'], registry) == {'misconception': [2]}

# ---- registry tamper detection --------------------------------------------
bad = copy.deepcopy(registry); bad['registry_digest'] = '0' * 64
path = CHEM / 'CoreAuthoring' / 'registry' / 'chemistry-learner-copy-titles.json'
tmp = Path('/tmp/chemistry-learner-copy-tamper.json')
tmp.write_text(json.dumps(bad, ensure_ascii=False), encoding='utf-8')
expect('LEARNER_TITLE_REGISTRY_DIGEST_DRIFT', lambda: load_registry(tmp))

bad = copy.deepcopy(registry); bad['titles']['MISCONCEPTION_REPAIR']['learner_facing_title'] = 'Misconception Repair'
expect('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE', lambda: validate_registry(bad))
bad = copy.deepcopy(registry); bad['titles']['GUIDED_ATTEMPT']['learner_facing_title'] = 'GUIDED_ATTEMPT'
expect('LEARNER_TITLE_IS_INTERNAL_ROLE', lambda: validate_registry(bad))
bad = copy.deepcopy(registry); bad['titles']['TRANSFER']['learner_facing_title'] = ''
expect('LEARNER_TITLE_MISSING_FOR_ROLE', lambda: validate_registry(bad))
bad = copy.deepcopy(registry); bad['resolution_policy'] = 'BEST_EFFORT'
expect('LEARNER_TITLE_MISSING_FOR_ROLE', lambda: validate_registry(bad))
tmp.unlink()

# ---- the rendered pages a learner actually opens ---------------------------
# The frozen candidate is the exact reviewed bytes, so the scan runs against it
# rather than against a re-render.
import pymupdf
CANDIDATE = CHEM / 'ExactProduct' / 'candidates' / 'CHEM-C-L-EXACT-CANDIDATE-A'
CLINICAL_HEADINGS = ['Misconception clinic', 'Misconception Repair', 'Representation path',
                     'Reasoning route', 'Faded practice', 'Orient / activate', 'Verification',
                     'Reconstruct the reasoning', 'Concept helper', 'Check your knowledge',
                     'Try with me', 'H0 — Attempt first', 'H1 — Notice', 'H3 — Start']
WARM_HEADINGS = [title_for(r, registry) for r in
                 ['MISCONCEPTION_REPAIR', 'GUIDED_ATTEMPT', 'FADED_ATTEMPT', 'INDEPENDENT_ATTEMPT',
                  'CHEMICAL_VERIFICATION', 'H0_ATTEMPT_FIRST', 'H1_NOTICE', 'H3_START',
                  'IMMEDIATE_ANSWER_CHECK', 'CONCEPT_HELPER']]
pages_text = []
for name in ['core-study-guide.pdf', 'examside-solution-transfer-book.pdf']:
    doc = pymupdf.open(str(CANDIDATE / name))
    pages_text.extend(page.get_text('text') for page in doc)
whole = '\n'.join(pages_text)
assert pages_text, 'no rendered pages to scan'

for clinical in CLINICAL_HEADINGS:
    assert clinical not in whole, clinical
assert scan_pages(pages_text, registry) == {}, scan_pages(pages_text, registry)
for warm in WARM_HEADINGS:
    assert warm in whole, warm

print('CHEMISTRY LEARNER-COPY mapped internal roles = %d PASS' % len(registry['titles']))
print('CHEMISTRY LEARNER-COPY internal identifiers unchanged = PASS')
print('CHEMISTRY LEARNER-COPY clinical-heading falsifier catches what #322 cannot = PASS')
print('CHEMISTRY LEARNER-COPY unmapped role fails closed = PASS')
print('CHEMISTRY LEARNER-COPY rendered pages scanned = %d, clinical headings found = 0 PASS' % len(pages_text))
