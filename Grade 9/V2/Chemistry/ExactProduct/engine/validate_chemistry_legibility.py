#!/usr/bin/env python3
"""Legibility targets for the rendered learner product.

PR #322's minimum-font rule is an absolute engineering floor: it stops a page
being unreadable. It does not make a page comfortable to study from, and it is
trivially satisfiable by a renderer that shrinks leading and packs lines until
the page is a wall. This module carries the pedagogical target instead, from
``chemistry-legibility-target-profile.json``:

    INSTRUCTIONAL_BODY   >= 10 pt      LEARNER_BODY_TOO_SMALL
    QUESTION_STEM        >= 12 pt      LEARNER_BODY_TOO_SMALL
    page density         leading ratio, coverage and a derived line cap
                                       PAGE_DENSITY_EXCEEDS_POLICY

Two targets are deliberately ``MEASURED_NOT_YET_ENFORCED`` and say why in the
profile: key equations have no distinct render role yet, and diagram labels are
drawn by the vendored shared primitives package, which currently emits spans
down to 5.4 pt. Those are measured and reported rather than claimed.
"""
import argparse, copy, hashlib, json, math
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]
PROFILE_PATH = CHEM / 'ExactProduct' / 'registry' / 'chemistry-legibility-target-profile.json'

ENFORCED = 'ENFORCED'
MEASURED = 'MEASURED_NOT_YET_ENFORCED'


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


def load_profile(path=PROFILE_PATH):
    profile = load(path)
    stored = profile.get('profile_digest', '')
    if stored and stored != digest(profile, 'profile_digest'):
        fail('LEGIBILITY_TARGET_PROFILE_DIGEST_DRIFT', profile.get('profile_id', 'profile'))
    return profile


def validate_profile(profile):
    if profile.get('subject') != 'CHEMISTRY': fail('LEGIBILITY_ROLE_NOT_MEASURED', 'subject')
    targets = profile['learner_targets']
    for role in profile['required_measured_roles']:
        if role not in targets: fail('LEGIBILITY_ROLE_NOT_MEASURED', role)
    for role, target in targets.items():
        if target['enforcement_state'] not in (ENFORCED, MEASURED):
            fail('LEGIBILITY_ROLE_NOT_MEASURED', role + ':enforcement_state')
        if target['enforcement_state'] == MEASURED and not target.get('blocked_by'):
            fail('LEGIBILITY_ROLE_NOT_MEASURED', role + ':unenforced target must say why')
        if target['minimum_pt'] > target['preferred_pt']:
            fail('LEGIBILITY_ROLE_NOT_MEASURED', role + ':minimum above preferred')
    body = targets['INSTRUCTIONAL_BODY']
    if body['minimum_pt'] <= profile['absolute_minimum_font_pt']:
        fail('LEARNER_BODY_TOO_SMALL', 'the learner body target must exceed the absolute floor')
    if profile['document_minimum_measurement']['enforcement_state'] not in (ENFORCED, MEASURED):
        fail('LEGIBILITY_ROLE_NOT_MEASURED', 'document_minimum_measurement')
    return True


def max_lines_per_page(profile, printable_height_pt):
    body = profile['learner_targets']['INSTRUCTIONAL_BODY']['minimum_pt']
    ratio = profile['page_density']['min_leading_ratio']
    return int(math.floor(float(printable_height_pt) / (float(body) * float(ratio))))


def validate_font_usage(font_usage, profile):
    """Check the sizes the Chemistry renderer actually used, per role."""
    targets = profile['learner_targets']
    floor = float(profile['absolute_minimum_font_pt'])
    for role in profile['required_measured_roles']:
        if role not in font_usage: fail('LEGIBILITY_ROLE_NOT_MEASURED', role)
    for role, size in sorted(font_usage.items()):
        target = targets.get(role)
        if target is None: fail('LEGIBILITY_ROLE_NOT_MEASURED', role + ':no declared target')
        if float(size) < floor: fail('MIN_FONT_SIZE_FAILURE', f'{role}={size}pt < {floor}pt')
        if target['enforcement_state'] != ENFORCED: continue
        if float(size) < float(target['minimum_pt']):
            fail(target['falsifier'], f"{role}={size}pt < {target['minimum_pt']}pt")
    return True


def validate_page_density(density, profile, printable_height_pt, printable_width_pt=None):
    policy = profile['page_density']
    if policy['enforcement_state'] != ENFORCED: return True
    cap = max_lines_per_page(profile, printable_height_pt)
    for page in density:
        if page['text_lines'] > cap:
            fail('PAGE_DENSITY_EXCEEDS_POLICY',
                 f"page {page['page']}: {page['text_lines']} lines > derived cap {cap}")
        if page['text_coverage_ratio'] > policy['max_text_coverage_ratio']:
            fail('PAGE_DENSITY_EXCEEDS_POLICY',
                 f"page {page['page']}: coverage {page['text_coverage_ratio']} > {policy['max_text_coverage_ratio']}")
    return True


def validate_leading(body_pt, leading_pt, profile):
    ratio = float(leading_pt) / float(body_pt)
    if ratio < float(profile['page_density']['min_leading_ratio']):
        fail('PAGE_DENSITY_EXCEEDS_POLICY', f'leading ratio {ratio:.3f} below policy')
    return True


def document_minimum_span_pt(pdf_path):
    """Smallest text span anywhere in the PDF, vendored primitive labels included."""
    import pymupdf
    smallest = None
    doc = pymupdf.open(str(pdf_path))
    for page in doc:
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    if not str(span.get('text') or '').strip(): continue
                    size = round(float(span['size']), 2)
                    smallest = size if smallest is None else min(smallest, size)
    return smallest


def legibility_evidence(metrics, profile, printable_height_pt, printable_width_pt,
                        document_minimum_pt=None, body_pt=None, leading_pt=None):
    """Build the machine evidence block and run every ENFORCED check."""
    font_usage = metrics['font_usage_pt']
    density = metrics['page_density']
    validate_font_usage(font_usage, profile)
    validate_page_density(density, profile, printable_height_pt, printable_width_pt)
    if body_pt and leading_pt: validate_leading(body_pt, leading_pt, profile)
    cap = max_lines_per_page(profile, printable_height_pt)
    unenforced = sorted(role for role, t in profile['learner_targets'].items()
                        if t['enforcement_state'] != ENFORCED)
    return {'legibility_profile_ref': profile['profile_id'],
            'font_usage_pt': dict(font_usage),
            'renderer_controlled_minimum_font_pt': min(font_usage.values()),
            'document_minimum_font_pt': document_minimum_pt,
            'instructional_body_pt': font_usage.get('INSTRUCTIONAL_BODY'),
            'question_stem_pt': font_usage.get('QUESTION_STEM'),
            'max_lines_per_page_cap': cap,
            'observed_max_lines_per_page': max((p['text_lines'] for p in density), default=0),
            'observed_max_text_coverage_ratio': max((p['text_coverage_ratio'] for p in density), default=0.0),
            'page_density_pass': True,
            'learner_body_target_pass': True,
            'unenforced_legibility_targets': unenforced}


def seal(path=PROFILE_PATH):
    profile = load(path)
    profile['profile_digest'] = ''
    profile['profile_digest'] = digest(profile, 'profile_digest')
    Path(path).write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return profile['profile_digest']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seal', action='store_true'); a = ap.parse_args()
    if a.seal:
        print(json.dumps({'profile_digest': seal()}, sort_keys=True)); return
    profile = load_profile(); validate_profile(profile)
    print(json.dumps({'profile_id': profile['profile_id'],
                      'enforced_roles': sorted(r for r, t in profile['learner_targets'].items()
                                               if t['enforcement_state'] == ENFORCED),
                      'measured_not_enforced': sorted(r for r, t in profile['learner_targets'].items()
                                                      if t['enforcement_state'] != ENFORCED),
                      'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__': main()
