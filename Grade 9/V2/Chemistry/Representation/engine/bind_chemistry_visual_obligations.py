#!/usr/bin/env python3
"""Per-content-reference visual-obligation binding and realization ledger.

PR #322 proved a *global* property: at least N teaching-primitive kinds are
drawn as real vector graphics somewhere in the product. That is necessary and
not sufficient. A learner meets one page at a time, so a classification question
or a mole question that stays text-only is still a failure even when fifteen
other kinds were realized elsewhere.

This module owns the local version of the obligation:

    build_ledger          upstream must BIND an allowed visual family to every
                          lesson and every question whose capability requires a
                          visual (C-H; renderer never selects)
    reconcile_realization the rendered evidence must show that binding actually
                          drawn (C-L); a bound-but-not-drawn obligation is
                          UNREALIZED and is never quietly replaced by prose

Falsifiers: ``VISUAL_OBLIGATION_MISSING``, ``WRONG_VISUAL_FAMILY``,
``TEXT_ONLY_WHEN_VISUAL_REQUIRED``,
``GLOBAL_REALIZATION_CLAIMED_FOR_LOCAL_OBLIGATION``,
``VISUAL_OBLIGATION_COUNTER_NOT_DERIVED_FROM_RECORDS``.
"""
import argparse, copy, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


def taxonomy_index(taxonomy):
    return {c['capability_id']: c for c in taxonomy['capabilities']}


def _obligation(scope, content_ref, capability_ref, allowed, bound):
    allowed_set = set(allowed)
    bound_allowed = [x for x in bound if x in allowed_set]
    if not bound:
        state = 'MISSING'
    elif not bound_allowed:
        state = 'WRONG_FAMILY'
    else:
        state = 'BOUND'
    return {'obligation_id': f'VO-{scope}-{content_ref}',
            'scope': scope, 'content_ref': content_ref, 'capability_ref': capability_ref,
            'allowed_families': sorted(allowed_set),
            'bound_families': sorted(set(bound)),
            'binding_status': state,
            'realization_status': 'PENDING',
            'realized_families': []}


def build_ledger(core1_plan, core2_plan, representation_bundle, taxonomy, profile,
                 ledger_id='CHEM-C-H-VISUAL-OBLIGATIONS-v1'):
    caps = taxonomy_index(taxonomy)
    selected = {}
    for rep in representation_bundle['representations']:
        selected.setdefault(rep['capability_ref'], set()).add(rep['primitive_id'])
    obligations = []
    for index, lesson in enumerate(core1_plan['lessons'], 1):
        cap = lesson['capability_ref']
        record = caps.get(cap)
        if record is None: fail('VISUAL_OBLIGATION_MISSING', cap + ':not in capability taxonomy')
        if not record.get('visual_required'): continue
        obligations.append(_obligation('CORE1_LESSON', 'LESSON-%02d' % index, cap,
                                       record['allowed_visual_families'],
                                       sorted(selected.get(cap, set()))))
    for index, page in enumerate(core2_plan['pages'], 1):
        cap = page['primary_capability_ref']
        record = caps.get(cap)
        if record is None: fail('VISUAL_OBLIGATION_MISSING', cap + ':not in capability taxonomy')
        if not record.get('visual_required'): continue
        bound = {s.get('primitive_id') for s in (page.get('visual_specs') or [])
                 if s.get('primitive_id') and s.get('visual_kind') == 'TEACHING_PRIMITIVE'}
        if page.get('source_figure_required'): bound.add('PARTICLE_MODEL_VIEW')
        if not bound: bound = selected.get(cap, set())
        obligations.append(_obligation('CORE2_QUESTION', 'TRANSFER-%02d' % index, cap,
                                       record['allowed_visual_families'], sorted(bound)))
    out = {'ledger_id': ledger_id, 'schema_version': '1.0.0', 'subject': 'CHEMISTRY',
           'profile_ref': profile['profile_id'], 'taxonomy_ref': taxonomy['taxonomy_id'],
           'representation_bundle_ref': representation_bundle['bundle_id'],
           'obligations': obligations, 'summary': summarize(obligations), 'ledger_digest': ''}
    out['ledger_digest'] = digest(out, 'ledger_digest')
    validate_ledger(out, profile)
    return out


def summarize(obligations):
    questions = [o for o in obligations if o['scope'] == 'CORE2_QUESTION']
    return {'visual_obligations_required': len(obligations),
            'visual_obligations_bound': sum(o['binding_status'] == 'BOUND' for o in obligations),
            'visual_obligations_realized': sum(o['realization_status'] == 'REALIZED' for o in obligations),
            'questions_requiring_visual': len(questions),
            'questions_with_required_visual': sum(
                q['binding_status'] == 'BOUND' and q['realization_status'] == 'REALIZED' for q in questions)}


def validate_ledger(ledger, profile, require_realized=False):
    if ledger['ledger_digest'] != digest(ledger, 'ledger_digest'):
        fail('VISUAL_OBLIGATION_COUNTER_NOT_DERIVED_FROM_RECORDS', 'ledger digest')
    if ledger['summary'] != summarize(ledger['obligations']):
        fail('VISUAL_OBLIGATION_COUNTER_NOT_DERIVED_FROM_RECORDS', 'summary')
    for o in ledger['obligations']:
        if o['scope'] not in profile['obligation_scopes']: fail('VISUAL_OBLIGATION_MISSING', o['obligation_id'] + ':scope')
        if o['binding_status'] == 'MISSING': fail('VISUAL_OBLIGATION_MISSING', o['obligation_id'])
        if o['binding_status'] == 'WRONG_FAMILY':
            fail('WRONG_VISUAL_FAMILY', f"{o['obligation_id']}: bound {o['bound_families']} not in {o['allowed_families']}")
        if not set(o['realized_families']) <= set(o['bound_families']):
            fail('GLOBAL_REALIZATION_CLAIMED_FOR_LOCAL_OBLIGATION',
                 o['obligation_id'] + ':realized family was never bound here')
        if o['realization_status'] == 'REALIZED' and not o['realized_families']:
            fail('UNREALIZED_VISUAL_SUBSTITUTED_BY_TEXT', o['obligation_id'])
        if require_realized and o['realization_status'] != 'REALIZED':
            fail('TEXT_ONLY_WHEN_VISUAL_REQUIRED', o['obligation_id'])
    return True


def reconcile_realization(ledger, evidence, profile, require_realized=True):
    """Mark obligations realized from rendered-page evidence.

    ``evidence`` maps a content reference to the primitive kinds that were
    actually drawn on that content's pages, as recorded by the renderer at the
    moment it emitted the drawing operations.
    """
    out = copy.deepcopy(ledger)
    for o in out['obligations']:
        drawn = set(evidence.get(o['content_ref'], []))
        realized = sorted(drawn & set(o['bound_families']))
        o['realized_families'] = realized
        o['realization_status'] = 'REALIZED' if realized else 'UNREALIZED'
    out['summary'] = summarize(out['obligations'])
    out['ledger_digest'] = ''
    out['ledger_digest'] = digest(out, 'ledger_digest')
    validate_ledger(out, profile, require_realized=require_realized)
    return out


def candidate_counters(ledger):
    s = ledger['summary']
    return {k: s[k] for k in ['visual_obligations_required', 'visual_obligations_realized',
                              'questions_requiring_visual', 'questions_with_required_visual']}


def validate_candidate_counters(counters, ledger):
    expected = candidate_counters(ledger)
    if counters != expected:
        fail('VISUAL_OBLIGATION_COUNTER_NOT_DERIVED_FROM_RECORDS', canonical({'claimed': counters, 'derived': expected}))
    if counters['visual_obligations_realized'] < counters['visual_obligations_required']:
        fail('TEXT_ONLY_WHEN_VISUAL_REQUIRED',
             f"{counters['visual_obligations_realized']}/{counters['visual_obligations_required']} realized")
    if counters['questions_with_required_visual'] < counters['questions_requiring_visual']:
        fail('TEXT_ONLY_WHEN_VISUAL_REQUIRED',
             f"{counters['questions_with_required_visual']}/{counters['questions_requiring_visual']} questions")
    return True


def validate_taxonomy(taxonomy, authority, primitive_registry, page_intent_profile, instructional_profile):
    """Cross-registry closure for the capability taxonomy (item 3)."""
    if taxonomy.get('subject') != 'CHEMISTRY': fail('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY', 'subject')
    stored = taxonomy.get('taxonomy_digest', '')
    if stored and stored != digest(taxonomy, 'taxonomy_digest'):
        fail('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY', 'taxonomy digest')
    caps = taxonomy_index(taxonomy)
    if len(caps) != len(taxonomy['capabilities']):
        fail('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY', 'duplicate capability id')
    families = {p['primitive_id'] for p in primitive_registry['primitives']}
    declared_pck = set(taxonomy['pck_families'])
    profile_pck = set((instructional_profile.get('primary_pck_family_by_capability') or {}).values())
    forbidden = [x.upper() for x in taxonomy['forbidden_capability_name_fragments']]
    for cap_id, record in caps.items():
        for fragment in forbidden:
            if fragment in cap_id.upper(): fail('TOPIC_NAMED_CAPABILITY', f'{cap_id} contains {fragment}')
        if not record.get('learner_can_statement', '').strip():
            fail('CAPABILITY_WITHOUT_LEARNER_CAN_STATEMENT', cap_id)
        if not record.get('learner_can_statement', '').lower().startswith('i can'):
            fail('CAPABILITY_WITHOUT_LEARNER_CAN_STATEMENT', cap_id + ':not a learner-voice statement')
        if not record.get('required_source_evidence'): fail('CAPABILITY_WITHOUT_SOURCE_EVIDENCE', cap_id)
        if not record.get('primary_pck_family'): fail('CAPABILITY_WITHOUT_PCK_FAMILY', cap_id)
        if record['primary_pck_family'] not in declared_pck: fail('PCK_FAMILY_NOT_DECLARED', cap_id)
        if not record.get('verification_checks'): fail('CAPABILITY_WITHOUT_VERIFICATION_CHECK', cap_id)
        if not record.get('allowed_visual_families'): fail('CAPABILITY_WITHOUT_ALLOWED_VISUAL_FAMILY', cap_id)
        for family in record['allowed_visual_families']:
            if family not in families: fail('ALLOWED_VISUAL_FAMILY_NOT_IN_PRIMITIVE_REGISTRY', f'{cap_id}:{family}')
        mapped = (instructional_profile.get('primary_pck_family_by_capability') or {}).get(cap_id)
        if mapped and mapped != record['primary_pck_family']:
            fail('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY', f'{cap_id}:pck family {mapped} != {record["primary_pck_family"]}')
    for cap in authority['capabilities']:
        if cap['capability_id'] not in caps:
            fail('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY', cap['capability_id'] + ':missing from taxonomy')
    for cap_id, primitives in (page_intent_profile.get('primary_primitives_by_capability') or {}).items():
        record = caps.get(cap_id)
        if record is None:
            fail('CAPABILITY_TAXONOMY_DRIFT_FROM_CANONICAL_AUTHORITY', cap_id + ':page intent without taxonomy record')
        if not set(primitives) <= set(record['allowed_visual_families']):
            fail('PAGE_INTENT_PRIMITIVE_NOT_ALLOWED_BY_TAXONOMY',
                 f'{cap_id}:{sorted(set(primitives) - set(record["allowed_visual_families"]))}')
    unused_pck = declared_pck - {r['primary_pck_family'] for r in caps.values()} - profile_pck
    if unused_pck: fail('PCK_FAMILY_NOT_DECLARED', 'declared but unused: ' + ', '.join(sorted(unused_pck)))
    return True


def seal_taxonomy(path):
    taxonomy = load(path)
    taxonomy['taxonomy_digest'] = ''
    taxonomy['taxonomy_digest'] = digest(taxonomy, 'taxonomy_digest')
    Path(path).write_text(json.dumps(taxonomy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return taxonomy['taxonomy_digest']


def seal_profile(path):
    profile = load(path)
    profile['profile_digest'] = ''
    profile['profile_digest'] = digest(profile, 'profile_digest')
    Path(path).write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return profile['profile_digest']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seal-taxonomy', default=str(CHEM / 'AssessmentScope' / 'registry' / 'chemistry-capability-taxonomy.json'))
    ap.add_argument('--seal-profile', default=str(CHEM / 'Representation' / 'registry' / 'chemistry-visual-obligation-profile.json'))
    ap.add_argument('--seal', action='store_true')
    a = ap.parse_args()
    if a.seal:
        print(json.dumps({'taxonomy_digest': seal_taxonomy(a.seal_taxonomy),
                          'profile_digest': seal_profile(a.seal_profile)}, sort_keys=True)); return
    taxonomy = load(a.seal_taxonomy)
    validate_taxonomy(taxonomy,
                      load(CHEM / 'AssessmentScope' / 'authority' / 'chemistry-canonical-authority.json'),
                      load(CHEM / 'Representation' / 'registry' / 'chemistry-teaching-primitive-registry.json'),
                      load(CHEM / 'Representation' / 'registry' / 'chemistry-page-intent-profile.json'),
                      load(CHEM / 'CoreAuthoring' / 'registry' / 'chemistry-instructional-authoring-profile.json'))
    print(json.dumps({'taxonomy_id': taxonomy['taxonomy_id'],
                      'capabilities': len(taxonomy['capabilities']), 'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__': main()
