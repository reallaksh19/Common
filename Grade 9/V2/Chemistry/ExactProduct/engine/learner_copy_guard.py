#!/usr/bin/env python3
"""Machine falsifier for internal role/jargon labels on a learner surface.

PR #322 already guards raw identifier *shapes* — ``CHECK_SPECIES_IDENTITY``,
``CAP-READ-FORMULA``, ``OBLIGATION_REP:FORMULA`` — in
``learner_surface_guard``. That guard cannot see the other half of the problem:
a heading like "Misconception Repair" or "Representation path" contains no
identifier shape at all, reads as ordinary English to a regex, and is still
curriculum-committee vocabulary printed at a 14-year-old.

This module is the second guard. It is a *separation*, not a rename: the
internal role identifiers stay exactly as they are in schemas, enum values and
falsifier names, and every engine keeps matching on them. Only the rendered
string changes, and only by resolving the role through
``CoreAuthoring/registry/chemistry-learner-copy-titles.json``.

Resolution is fail-closed. An unmapped role raises
``LEARNER_TITLE_MISSING_FOR_ROLE`` rather than falling back to a prettified
version of the internal identifier, because a prettified identifier is exactly
the leak this guard exists to catch.
"""
import copy, hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]
REGISTRY_PATH = CHEM / 'CoreAuthoring' / 'registry' / 'chemistry-learner-copy-titles.json'

INTERNAL_ROLE_SHAPE = re.compile(r'^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*$')


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


def load_registry(path=REGISTRY_PATH):
    registry = json.loads(Path(path).read_text(encoding='utf-8'))
    stored = registry.get('registry_digest', '')
    if stored and stored != digest(registry, 'registry_digest'):
        fail('LEARNER_TITLE_REGISTRY_DIGEST_DRIFT', registry.get('registry_id', 'registry'))
    return registry


def validate_registry(registry):
    if registry.get('subject') != 'CHEMISTRY': fail('LEARNER_TITLE_MISSING_FOR_ROLE', 'subject')
    if registry.get('resolution_policy') != 'FAIL_CLOSED_NEVER_PRINT_INTERNAL_ROLE':
        fail('LEARNER_TITLE_MISSING_FOR_ROLE', 'resolution_policy')
    forbidden_headings = [x.lower() for x in registry['forbidden_heading_phrases']]
    for role, entry in registry['titles'].items():
        if not INTERNAL_ROLE_SHAPE.match(role):
            fail('LEARNER_TITLE_MISSING_FOR_ROLE', role + ':not an internal role identifier')
        title = entry.get('learner_facing_title', '')
        if not title: fail('LEARNER_TITLE_MISSING_FOR_ROLE', role)
        # A title is a leak when it is still shaped like the identifier: an
        # underscore, or shouted all-caps. "Final answer" for FINAL_ANSWER is
        # not a leak — it is the plain-English reading of an already-plain role.
        if '_' in title or title.strip().isupper():
            fail('LEARNER_TITLE_IS_INTERNAL_ROLE', f'{role}: "{title}"')
        lowered = title.lower()
        for phrase in forbidden_headings:
            if phrase in lowered:
                fail('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE', f'{role}: title contains "{phrase}"')
    return True


def title_for(role, registry):
    """Resolve an internal role to its learner-facing title, or fail closed."""
    entry = registry['titles'].get(role)
    if not entry: fail('LEARNER_TITLE_MISSING_FOR_ROLE', str(role))
    return entry['learner_facing_title']


def _scan(text, phrases):
    lowered = str(text or '').lower()
    return sorted({p for p in phrases if p.lower() in lowered})


def find_heading_jargon(text, registry):
    return _scan(text, registry['forbidden_heading_phrases'])


def find_surface_jargon(text, registry):
    return _scan(text, registry['forbidden_anywhere_phrases'])


def assert_heading_safe(text, registry, where='heading'):
    hits = find_heading_jargon(text, registry)
    if hits:
        fail('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE', f'{where}: {", ".join(hits)} in "{text}"')
    return True


def assert_surface_safe(text, registry, where='learner surface'):
    hits = find_surface_jargon(text, registry)
    if hits:
        fail('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE', f'{where}: {", ".join(hits)}')
    return True


def scan_pages(page_texts, registry):
    """Scan rendered per-page text; returns {phrase: [page numbers]}."""
    hits = {}
    for index, text in enumerate(page_texts, 1):
        for phrase in find_surface_jargon(text, registry):
            hits.setdefault(phrase, []).append(index)
    return {k: hits[k] for k in sorted(hits)}


def seal(path=REGISTRY_PATH):
    registry = json.loads(Path(path).read_text(encoding='utf-8'))
    registry['registry_digest'] = ''
    registry['registry_digest'] = digest(registry, 'registry_digest')
    Path(path).write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return registry['registry_digest']


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--seal', action='store_true'); a = ap.parse_args()
    if a.seal:
        print(json.dumps({'registry_digest': seal()}, sort_keys=True))
    else:
        reg = load_registry(); validate_registry(reg)
        print(json.dumps({'registry_id': reg['registry_id'], 'roles': len(reg['titles']), 'status': 'PASS'}, sort_keys=True))
