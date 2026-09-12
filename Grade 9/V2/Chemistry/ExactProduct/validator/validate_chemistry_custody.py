#!/usr/bin/env python3
"""Independent custody validator for the Chemistry C-L exact artifact.

Recomputes custody from the *bytes on disk* rather than trusting the
producer's own summary. Adapted from the PR #161 / PR #196 PublicationRealization
custody contract, narrowed to the two Chemistry products:

    exact PDF bytes
    -> SHA256
    -> PhysicalPageMap (actual placement evidence)
    -> page-intent reconciliation, bounds, orphan continuations
    -> candidate package digest

A pass here is engineering custody only. It says nothing about subject,
pedagogy, assessment or visual-usability quality, and the validator refuses a
candidate that tries to imply otherwise.
"""

import argparse, copy, hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'engine'))
import learner_surface_guard as GUARD

PAGE_W = 595.2755905511812
PAGE_H = 841.8897637795277


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def digest(obj, field=None):
    x = copy.deepcopy(obj)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def fail(code, detail=''):
    raise ValueError(f'{code}: {detail}' if detail else code)


def validate_page_map(page_map, pdf_path, page_count):
    if page_map.get('artifact_sha256') != sha_file(pdf_path):
        fail('EXACT_ARTIFACT_HASH_MISMATCH', page_map.get('page_map_id', '?'))
    if not page_map.get('actual_placement_evidence'):
        fail('PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE', page_map.get('page_map_id', '?'))
    if page_map.get('page_count') != page_count:
        fail('PHYSICAL_PAGE_COUNT_DRIFT', page_map.get('page_map_id', '?'))
    placements = page_map.get('content_placements') or []
    if not placements:
        fail('PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE', 'no placement fragments')
    intents = {x['page_intent_id']: x for x in page_map.get('page_intents', [])}
    for entry in placements:
        if not (0 <= entry['x0'] < entry['x1'] <= PAGE_W + 1 and 0 <= entry['y0'] < entry['y1'] <= PAGE_H + 1):
            fail('PLACEMENT_OUT_OF_PHYSICAL_BOUNDS', entry['content_ref'])
        if not (1 <= entry['page'] <= page_count):
            fail('PLACEMENT_OUT_OF_PHYSICAL_BOUNDS', entry['content_ref'])
        intent = intents.get(entry['page_intent_id'])
        if intent is None:
            fail('PAGE_INTENT_RECONCILIATION_FAILURE', entry['page_intent_id'])
        if entry['fragment_kind'] == 'CONTINUATION' and (
                not intent['split'] or entry['page'] not in intent['continuation_pages']):
            fail('ORPHAN_CONTINUATION_FRAGMENT', entry['content_ref'])
    for intent in page_map.get('page_intents', []):
        actual = sorted({e['page'] for e in placements if e['page_intent_id'] == intent['page_intent_id']})
        if actual != sorted(intent['physical_pages']):
            fail('PAGE_INTENT_RECONCILIATION_FAILURE', intent['page_intent_id'])
    for entry in page_map.get('realized_primitives', []):
        if not (1 <= entry['page'] <= page_count):
            fail('PLACEMENT_OUT_OF_PHYSICAL_BOUNDS', entry['primitive'])
        if entry.get('validated_by') != 'MasterTemplates.VisualSemanticValidator':
            fail('PRIMITIVE_DRAWN_WITHOUT_SEMANTIC_VALIDATION', entry['primitive'])
    return True


def validate_learner_surface(pdf_path):
    import pymupdf
    doc = pymupdf.open(pdf_path)
    leaks = GUARD.scan_pages([p.get_text('text') for p in doc])
    if leaks:
        fail('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK', json.dumps(leaks, sort_keys=True))
    return True


def validate(out_dir, policy=None):
    out = Path(out_dir)
    candidate = load(out / 'exact-product-candidate.json')
    if candidate['package_digest'] != digest(candidate, 'package_digest'):
        fail('EXACT_ARTIFACT_HASH_MISMATCH', 'package digest')
    arts = {x['product_id']: x for x in candidate['artifacts']}
    pairs = (('CORE_STUDY_GUIDE', 'physical-page-map-core1.json'),
             ('EXAMSIDE_SOLUTION_TRANSFER_BOOK', 'physical-page-map-core2.json'))
    for product_id, map_name in pairs:
        artifact = arts[product_id]
        pdf_path = out / artifact['path']
        if not pdf_path.exists() or not pdf_path.read_bytes().startswith(b'%PDF'):
            fail('MISSING_EXACT_PDF', product_id)
        if sha_file(pdf_path) != artifact['sha256']:
            fail('EXACT_ARTIFACT_HASH_MISMATCH', product_id)
        page_map = load(out / map_name)
        if digest(page_map) != artifact['physical_page_map_digest']:
            fail('EXACT_ARTIFACT_HASH_MISMATCH', map_name)
        validate_page_map(page_map, pdf_path, artifact['page_count'])
        validate_learner_surface(pdf_path)
    evidence = candidate['machine_evidence']
    if evidence.get('learner_internal_identifier_leaks'):
        fail('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK', 'candidate evidence')
    if not evidence.get('actual_placement_evidence'):
        fail('PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE', 'candidate evidence')
    if evidence.get('placement_bounds_violations'):
        fail('PLACEMENT_OUT_OF_PHYSICAL_BOUNDS', 'candidate evidence')
    if evidence.get('orphan_continuations'):
        fail('ORPHAN_CONTINUATION_FRAGMENT', 'candidate evidence')
    floor = (policy or {}).get('minimum_realized_primitive_kinds', 8)
    if len(evidence.get('teaching_primitive_kinds_realized') or []) < floor:
        fail('TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED', 'below policy floor')
    review_path = out / 'ai-pre-review.json'
    if review_path.exists():
        review = load(review_path)
        if review.get('production_claim'):
            fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS', 'AI pre-review claims production')
        if review.get('reviewer_role') != 'AI_PRE_REVIEW':
            fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS', 'AI pre-review role drift')
        if review.get('package_digest') != candidate['package_digest']:
            fail('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT', 'AI pre-review digest')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--policy')
    a = ap.parse_args()
    validate(a.out, load(a.policy) if a.policy else None)
    print('CHEMISTRY C-L independent custody validation: PASS (engineering only; '
          'subject, pedagogy, assessment and visual usability remain PENDING)')


if __name__ == '__main__':
    main()
