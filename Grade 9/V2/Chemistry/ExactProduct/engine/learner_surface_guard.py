#!/usr/bin/env python3
"""Machine falsifier for learner-facing internal-identifier leakage.

The Chemistry V2 chain carries internal identifiers in every upstream bundle:

    capability refs      CAP-READ-FORMULA, CAP-TRACK-OXIDATION-STATE
    lesson ids           CORE1-CAP-ATTACH-SPECIES-ROLE
    concept refs         CHEM-CONCEPT-ION-NOTATION
    PCK asset refs       PCK-CHEM-FIRST-MOVE
    representation ids   REP-CAP-PARSE-ION-CHARGE-01-FORMULA_ANATOMY_VIEW
    primitive ids        MACRO_PARTICLE_SYMBOLIC_BRIDGE, CONSERVATION_LEDGER
    route / check steps  READ_GIVEN, CHECK_SPECIES_IDENTITY, VERIFY_RESULT
    obligation tokens    OBLIGATION_LEVEL:SYMBOLIC, OBLIGATION_REP:FORMULA
    treatment states     ACTIVE_STUDY, FULL_LEARNING, EXPLICIT_EXCEPTION
    problem families     PF-AGENT_ROLE_ASSIGNMENT, QF-SPECIES-ROLE
    source refs          CO-CS12, CQ12, EXT05

None of those may reach a learner-visible text run. The two shape rules below
are derived from the identifier spellings actually used by the registries above
(screaming-snake with at least one underscore; all-caps hyphenated with at
least one hyphen), plus a short list of literal short refs that match neither
shape. Chemistry notation is unaffected: element symbols are mixed case
(``Zn``, ``Cu``), subscripts and charges are Unicode (``H₂O``, ``Fe³⁺``), and
state symbols are lower case (``(aq)``), so no legitimate chemical token has
the internal-identifier shape.
"""

import re

SNAKE_IDENTIFIER = re.compile(r'\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b')
HYPHEN_IDENTIFIER = re.compile(r'\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b')
SHORT_REF_IDENTIFIER = re.compile(r'\b(?:CQ|EXT|CO|CS|PF|QF|REP|PCK|CAP)\d{1,4}\b')
OBLIGATION_PREFIX = re.compile(r'\b[A-Z][A-Z0-9_]*:[A-Z][A-Z0-9_]*\b')

PATTERNS = (
    ('SNAKE_CASE_INTERNAL_ID', SNAKE_IDENTIFIER),
    ('HYPHENATED_INTERNAL_ID', HYPHEN_IDENTIFIER),
    ('SHORT_SOURCE_REF', SHORT_REF_IDENTIFIER),
    ('NAMESPACED_OBLIGATION_TOKEN', OBLIGATION_PREFIX),
)

# Learner-facing all-caps wording that is ordinary English, not an internal id.
# Kept deliberately tiny: anything added here must be readable prose a learner
# can act on, never a registry key.
ALLOWED_TOKENS = frozenset({
    'PDF',
    'A4',
})


def find_internal_identifiers(text):
    """Return sorted internal-identifier-shaped tokens found in learner text."""
    found = set()
    for _name, pattern in PATTERNS:
        for match in pattern.findall(str(text or '')):
            token = match if isinstance(match, str) else match[0]
            if token in ALLOWED_TOKENS:
                continue
            found.add(token)
    return sorted(found)


def classify(token):
    for name, pattern in PATTERNS:
        if pattern.fullmatch(token):
            return name
    return 'UNCLASSIFIED_INTERNAL_ID'


def assert_learner_safe(text, where='learner surface'):
    leaks = find_internal_identifiers(text)
    if leaks:
        raise ValueError('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK at %s: %s' % (where, ', '.join(leaks)))
    return True


def scan_pages(page_texts):
    """Scan rendered per-page text runs; returns {token: [page numbers]}."""
    leaks = {}
    for index, text in enumerate(page_texts, 1):
        for token in find_internal_identifiers(text):
            leaks.setdefault(token, []).append(index)
    return {k: leaks[k] for k in sorted(leaks)}
