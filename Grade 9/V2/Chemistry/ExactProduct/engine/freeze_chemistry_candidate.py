#!/usr/bin/env python3
"""Persist the frozen Chemistry C-L candidate durably, not only in CI.

Closes the ``FROZEN_CANDIDATE_ONLY_IN_EXPIRING_CI_ARTIFACT`` falsifier. The
realized candidate used to exist solely as a GitHub Actions artifact, so after
retention expired nothing anyone had reviewed could be fetched again.

This writes a durable, hash-bound record into the repository:

    candidates/<candidate_id>/
        core-study-guide.pdf                 (optional; --with-pdfs)
        examside-solution-transfer-book.pdf  (optional; --with-pdfs)
        exact-product-candidate.json
        physical-page-map-core1.json
        physical-page-map-core2.json
        ai-pre-review.json
        FROZEN_MANIFEST.json

``FROZEN_MANIFEST.json`` carries the SHA256 and byte length of every file plus
a non-self-referential package digest, so a later fetch — from the repo, from a
Release asset, or from a CI artifact — can be proved to be the same bytes that
were reviewed. ``--verify`` re-checks an existing frozen directory.
"""

import argparse, hashlib, json, shutil
from pathlib import Path

MANIFEST_NAME = 'FROZEN_MANIFEST.json'
ROLES = {
    'core-study-guide.pdf': 'CORE_STUDY_GUIDE_PDF',
    'examside-solution-transfer-book.pdf': 'EXAMSIDE_SOLUTION_TRANSFER_BOOK_PDF',
    'exact-product-candidate.json': 'EXACT_PRODUCT_CANDIDATE',
    'physical-page-map-core1.json': 'PHYSICAL_PAGE_MAP_CORE1',
    'physical-page-map-core2.json': 'PHYSICAL_PAGE_MAP_CORE2',
    'render-audit-core1.json': 'RENDER_AUDIT_CORE1',
    'render-audit-core2.json': 'RENDER_AUDIT_CORE2',
    'ai-pre-review.json': 'AI_PRE_REVIEW',
    'cold-start-report.json': 'COLD_START_REPORT',
}
PDF_FILES = ('core-study-guide.pdf', 'examside-solution-transfer-book.pdf')


def sha_bytes(data): return hashlib.sha256(data).hexdigest()
def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def package_digest(entries):
    return sha_bytes(canonical(sorted(entries, key=lambda x: x['path'])).encode())


def freeze(source_dir, repo_root, with_pdfs=True):
    source = Path(source_dir)
    candidate = load(source / 'exact-product-candidate.json')
    target = Path(repo_root) / 'Grade 9/V2/Chemistry/ExactProduct/candidates' / candidate['candidate_id']
    target.mkdir(parents=True, exist_ok=True)
    entries = []
    for name, role in sorted(ROLES.items()):
        src = source / name
        if not src.exists():
            continue
        if name in PDF_FILES and not with_pdfs:
            continue
        data = src.read_bytes()
        shutil.copyfile(src, target / name)
        entries.append({'path': name, 'role': role, 'sha256': sha_bytes(data), 'bytes': len(data)})
    if not entries:
        raise ValueError('nothing to freeze')
    review = load(source / 'ai-pre-review.json') if (source / 'ai-pre-review.json').exists() else None
    manifest = {
        'manifest_id': 'CHEM-C-L-FROZEN-' + candidate['candidate_id'],
        'schema_version': '1.0.0',
        'subject': 'CHEMISTRY',
        'candidate_ref': candidate['candidate_id'],
        'candidate_package_digest': candidate['package_digest'],
        'cold_start_report_digest': candidate['cold_start_report_digest'],
        'artifact_sha256': {a['product_id']: a['sha256'] for a in candidate['artifacts']},
        'ai_pre_review_state': (review or {}).get('state', 'NOT_RUN'),
        'ai_pre_review_findings': (review or {}).get('findings', []),
        'quality_states': {
            'PUBLICATION_ENGINEERING': 'SEE_RELEASE_DECISION',
            'SUBJECT_CORRECTNESS': 'PENDING',
            'PEDAGOGICAL_DESIGN': 'PENDING',
            'ASSESSMENT_DESIGN': 'PENDING',
            'VISUAL_USABILITY': 'PENDING',
            'MATURE_DESIGN_QUALITY': 'PENDING',
        },
        'note': 'Durable copy of the exact reviewed bytes. Engineering custody only; '
                'no human review of any kind is recorded or implied by this manifest.',
        'pdfs_included': bool(with_pdfs),
        'files': entries,
        'package_digest': '',
    }
    manifest['package_digest'] = package_digest(entries)
    (target / MANIFEST_NAME).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + '\n',
                                        encoding='utf-8')
    return target, manifest


def verify(frozen_dir):
    frozen = Path(frozen_dir)
    manifest = load(frozen / MANIFEST_NAME)
    if manifest['package_digest'] != package_digest(manifest['files']):
        raise ValueError('FROZEN_PACKAGE_DIGEST_MISMATCH')
    for entry in manifest['files']:
        path = frozen / entry['path']
        if not path.exists():
            raise ValueError('FROZEN_FILE_MISSING: ' + entry['path'])
        data = path.read_bytes()
        if sha_bytes(data) != entry['sha256'] or len(data) != entry['bytes']:
            raise ValueError('FROZEN_FILE_DRIFT: ' + entry['path'])
    candidate = load(frozen / 'exact-product-candidate.json')
    if candidate['package_digest'] != manifest['candidate_package_digest']:
        raise ValueError('FROZEN_CANDIDATE_DIGEST_DRIFT')
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source')
    ap.add_argument('--repo-root', default=str(Path(__file__).resolve().parents[5]))
    ap.add_argument('--no-pdfs', action='store_true')
    ap.add_argument('--verify')
    a = ap.parse_args()
    if a.verify:
        manifest = verify(a.verify)
        print(json.dumps({'verified': a.verify, 'package_digest': manifest['package_digest'],
                          'ai_pre_review': manifest['ai_pre_review_state']}, sort_keys=True))
        return
    if not a.source:
        ap.error('--source is required unless --verify is given')
    target, manifest = freeze(a.source, a.repo_root, not a.no_pdfs)
    print(json.dumps({'frozen_at': str(target), 'package_digest': manifest['package_digest'],
                      'ai_pre_review': manifest['ai_pre_review_state'],
                      'files': len(manifest['files'])}, sort_keys=True))


if __name__ == '__main__':
    main()
