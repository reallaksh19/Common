"""R14 WP1/U3: reference-graded checkpoint evidence and reviewer CLAIMS.

This is a boundary adapter to native V3.2 DELP validate_facts, not a new
programme projection, evidence acceptance oracle, reviewer admission or writer.
All URL, SHA and actor checks are structural only; provider GET is not performed.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator

from owner_session_contract_v1 import OwnerSessionError, validate_owner_session

SCHEMA = 'relay-lifecycle-evidence-review-v1'
SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'schemas/lifecycle-v35/lifecycle-evidence-review-v1.schema.json'
ROOT = Path(__file__).resolve().parents[3]
DELP_FILE = ROOT / 'skills/engineering-pr-delivery-v3.2/scripts/delp_projection_v32.py'


class EvidenceReviewError(ValueError):
    """Invalid or inconsistent evidence reference envelope."""


def _valid_url(value: str, repo: str, kind: str, number: int | None = None) -> bool:
    """Syntactic GitHub locator check, never a provider authenticity guarantee."""
    try:
        u = urlsplit(value)
        if u.scheme != 'https' or u.netloc != 'github.com' or u.username or u.password:
            return False
        if u.query or unquote(u.path) != u.path or unquote(u.fragment) != u.fragment:
            return False
        p = u.path
        pre = '/' + repo + '/'
        if not p.startswith(pre):
            return False
        trail = p[len(pre):]
        if kind == 'run':
            return u.fragment == '' and bool(re.fullmatch(r'actions/runs/[1-9][0-9]*', trail))
        if kind == 'review':
            return trail == f'pull/{number}' and bool(re.fullmatch(r'(pullrequestreview|issuecomment)-[1-9][0-9]*', u.fragment))
        return False
    except ValueError:
        return False


def _actual_delp_facts_validation(facts: Mapping[str, Any]) -> str:
    """Use the real DELP validator only when full checkout is actually present.

    Never silently substitute a cloned acceptance calculator if it is absent.
    An available native validator can reject bad facts but cannot accept their
    sources or say that current evidence was approved.
    """
    if not DELP_FILE.is_file():
        return 'NATIVE_DELP_VALIDATOR_NOT_RUN'
    spec = importlib.util.spec_from_file_location('r14_u3_actual_delp', DELP_FILE)
    if spec is None or spec.loader is None:
        raise EvidenceReviewError('DELP_IMPORT_UNAVAILABLE')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    faults = module.validate_facts(dict(facts))
    if faults:
        raise EvidenceReviewError('NATIVE_DELP_FACTS_INVALID:' + ';'.join(faults)[:800])
    return 'NATIVE_DELP_STRUCTURE_VALID_ONLY'


def validate_evidence_review(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise EvidenceReviewError('ENVELOPE_OBJECT_REQUIRED')
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    faults = sorted(Draft202012Validator(schema).iter_errors(payload),
                    key=lambda x: (tuple(map(str, x.path)), x.message))
    if faults:
        x = faults[0]
        raise EvidenceReviewError('SCHEMA_INVALID:' + '.'.join(map(str, x.path)) + ':' + x.message)
    try:
        history = validate_owner_session(payload['owner_session'])
    except OwnerSessionError as e:
        raise EvidenceReviewError('U2_HISTORY_INVALID:' + str(e)) from e
    ident = payload['owner_session']['identity']
    repo = ident['programme']['repository']
    ref = ident['candidate_source']
    if ref['state'] != 'REFERENCED' or ident['graph_source']['state'] != 'REFERENCED':
        raise EvidenceReviewError('PLAN_OR_CANDIDATE_UNOBSERVED')
    head = ref['head_sha']
    pr = ref['pr_number']
    facts = payload['checkpoint_facts']
    r = payload['responsibility']
    if r['issue_number'] == ident['programme']['root_issue']:
        raise EvidenceReviewError('LEAF_CANNOT_BE_PARENT')
    if facts['responsibility']['issue'] != f'{repo}#{r["issue_number"]}':
        raise EvidenceReviewError('FACTS_RESPONSIBILITY_NOT_BOUND')
    if facts['material']['pr'] != f'{repo}#{pr}':
        raise EvidenceReviewError('FACTS_PR_NOT_BOUND')
    if facts['material']['candidate_sha'] != head or facts['material']['base_sha'] != ref['base_sha']:
        raise EvidenceReviewError('MATERIAL_CANDIDATE_MISMATCH')
    producer = payload['producer']
    source_events = payload['owner_session']['session_events']
    producer_started = any(e['session_id'] == producer['session_id']
                           and e['actor_label'] == producer['actor_label']
                           and e['kind'] == 'START_CLAIMED' for e in source_events)
    if not producer_started:
        raise EvidenceReviewError('PRODUCER_SESSION_NOT_BOUND')
    if any(e['session_id'] == producer['session_id'] and e['kind'] == 'STOP_CLAIMED'
           for e in source_events):
        raise EvidenceReviewError('PRODUCER_SESSION_CLAIMED_STOPPED')
    units = facts['units']
    if len({u['id'] for u in units}) != len(units):
        raise EvidenceReviewError('DUPLICATE_FACTS_UNIT')
    for unit in units:
        if unit['candidate_sha'] != head:
            raise EvidenceReviewError('UNIT_HEAD_MISMATCH:' + unit['id'])
        if unit['contract_digest'] != r['contract_digest']:
            raise EvidenceReviewError('UNIT_CONTRACT_MISMATCH:' + unit['id'])
        if unit['state'] == 'COMPLETE' and unit['result'] == 'VERIFIED' and not unit['evidence_refs']:
            raise EvidenceReviewError('VERIFIED_WITHOUT_EVIDENCE:' + unit['id'])

    observed = payload['test_observations']
    if len({t['id'] for t in observed}) != len(observed):
        raise EvidenceReviewError('DUPLICATE_TEST_ID')
    for t in observed:
        if t['result'] == 'NOT_RUN' and t['tested_head_sha'] is not None:
            raise EvidenceReviewError('NOT_RUN_HAS_TEST_HEAD:' + t['id'])
        if t['result'] in {'PASS', 'FAIL'} and t['tested_head_sha'] != head:
            raise EvidenceReviewError('EXECUTED_TEST_HEAD_MISMATCH:' + t['id'])
        if t['result'] == 'UNKNOWN' and t['tested_head_sha'] is not None:
            raise EvidenceReviewError('UNKNOWN_TEST_HEAD_ASSERTED:' + t['id'])
        if t['run_url'] is not None and not _valid_url(t['run_url'], repo, 'run'):
            raise EvidenceReviewError('RUN_URL_UNTRUSTED:' + t['id'])
    review = payload['reviewer_claim']
    if review['state'] == 'NOT_SUBMITTED':
        if any(review[x] is not None for x in ('actor_label', 'session_id', 'candidate_sha', 'source_url', 'source_digest')):
            raise EvidenceReviewError('ABSENT_REVIEW_HAS_ASSERTIONS')
    else:
        if not all(review[x] is not None for x in ('actor_label', 'session_id', 'candidate_sha', 'source_url', 'source_digest')):
            raise EvidenceReviewError('REVIEW_CLAIM_INCOMPLETE')
        if review['actor_label'] == producer['actor_label'] or review['session_id'] == producer['session_id']:
            raise EvidenceReviewError('SELF_REVIEW_CLAIM')
        if review['candidate_sha'] != head:
            raise EvidenceReviewError('STALE_REVIEW_CLAIM')
        if not _valid_url(review['source_url'], repo, 'review', pr):
            raise EvidenceReviewError('REVIEW_URL_UNTRUSTED')

    delp_status = _actual_delp_facts_validation(facts)
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                           separators=(',', ':'), allow_nan=False)
    return {
        'schema': SCHEMA,
        'identity_sha256': history['identity_sha256'],
        'owner_session_history_sha256': history['history_sha256'],
        'evidence_claim_sha256': 'sha256:' + hashlib.sha256(canonical.encode()).hexdigest(),
        'reference_identity': 'CALLER_REFERENCED_UNATTESTED',
        'delp_facts_structure': delp_status,
        'candidate_comparison': 'MATCHES_CALLER_REFERENCE_NOT_PROVIDER_OBSERVED',
        'verification_evidence': 'UNADJUDICATED_CLAIMS',
        'reviewer_independence': ('NO_REVIEW_SUBMITTED' if review['state'] == 'NOT_SUBMITTED'
                                  else 'DIFFERENT_LABELS_NOT_INDEPENDENCE_PROOF'),
        'reviewer_admission': 'NOT_QUALIFIED',
        'owner_authenticity': 'NOT_AUTHENTICATED',
        'lease': 'NOT_PROVEN',
        'publisher': 'OFF',
        'canonical_delp_projection': 'NOT_CALCULATED',
        'programme_progress': None,
    }
