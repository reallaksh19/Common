"""R14 WP2/U01: quarantine R12 material claims before native DELP projection.

READ-ONLY DIAGNOSTIC: never accepts a serialized Node R12 capability as native
GitHub attestation, never publishes DELP output, and never claims Owner review.
Requires the real, existing V3.2 DELP implementation; has no fallback engine.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from typing import Any, Mapping

from evidence_review_contract_v1 import validate_evidence_review, EvidenceReviewError

NATIVE_DELP = Path(__file__).resolve().parents[3] / 'skills/engineering-pr-delivery-v3.2/scripts/delp_projection_v32.py'
H40 = re.compile(r'^[0-9a-f]{40}$')
H64 = re.compile(r'^[0-9a-f]{64}$')

class DiagnosticBridgeError(ValueError):
    """A material, scope, trust, or contract discrepancy blocks a preview."""


def _load_native_delp():
    if not NATIVE_DELP.is_file():
        raise DiagnosticBridgeError('NATIVE_DELP_NOT_AVAILABLE')
    spec = importlib.util.spec_from_file_location('wp2_u01_actual_v32_delp', NATIVE_DELP)
    if spec is None or spec.loader is None:
        raise DiagnosticBridgeError('NATIVE_DELP_LOAD_FAILED')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _candidate(candidate: Mapping[str, Any], *, repo: str, root: int, number: int, head: str):
    if not isinstance(candidate, dict) or candidate.get('schema') != 'relay-candidate-verification-v1':
        raise DiagnosticBridgeError('R12_CANDIDATE_CONTRACT_INVALID')
    if candidate.get('repository') != repo or candidate.get('parent_issue') != root:
        raise DiagnosticBridgeError('R12_PARENT_OR_REPOSITORY_MISMATCH')
    if not H64.fullmatch(str(candidate.get('candidate_state_sha256', ''))):
        raise DiagnosticBridgeError('R12_CANDIDATE_FINGERPRINT_MISSING')
    prs = candidate.get('pr_candidates')
    if not isinstance(prs, list) or len(prs) < 1 or len(prs) > 4:
        raise DiagnosticBridgeError('R12_PR_CANDIDATES_INVALID')
    matching = [p for p in prs if isinstance(p, dict) and p.get('number') == number]
    if len(matching) != 1:
        raise DiagnosticBridgeError('R12_EXACT_PR_NOT_UNIQUE')
    pr = matching[0]
    if pr.get('head_sha') != head or not H40.fullmatch(head):
        raise DiagnosticBridgeError('R12_CANDIDATE_SHA_CHANGED')
    if pr.get('head_state') != 'CURRENT' or pr.get('expected_head_sha') != head:
        raise DiagnosticBridgeError('R12_CANDIDATE_NOT_CURRENT')
    # Even a serialized R12 source_acquisition_attested=true is only a JSON claim.
    # The JS in-process native acquisition capability is not transferable here.
    return pr


def preview_diagnostic(bundle: Mapping[str, Any]) -> dict[str, Any]:
    """Actually invoke canonical DELP with U3 facts quarantined as untrusted.

    This demonstrates the real R12-source→V3.2 projection consumer edge,
    not reviewer adjudication or one-source programme acceptance. Never pass
    this result into any live issue/PR title writer.
    """
    if not isinstance(bundle, dict) or set(bundle) != {'schema', 'graph', 'evidence_review', 'candidate_state'}:
        raise DiagnosticBridgeError('BRIDGE_INPUT_SHAPE_INVALID')
    if bundle['schema'] != 'relay-diagnostic-delp-bridge-v1':
        raise DiagnosticBridgeError('BRIDGE_SCHEMA_INVALID')
    try:
        claim = validate_evidence_review(bundle['evidence_review'])
    except EvidenceReviewError as exc:
        raise DiagnosticBridgeError('U3_CLAIM_INVALID:' + str(exc)) from exc
    source = bundle['evidence_review']
    identity = source['owner_session']['identity']
    repo = identity['programme']['repository']
    root_issue = identity['programme']['root_issue']
    c = identity['candidate_source']
    pr = _candidate(bundle['candidate_state'], repo=repo, root=root_issue,
                    number=c['pr_number'], head=c['head_sha'])
    if claim['reviewer_admission'] != 'NOT_QUALIFIED' or claim['lease'] != 'NOT_PROVEN':
        raise DiagnosticBridgeError('CLAIM_AUTHORITY_PROMOTED')
    # No fallback projector. This must be an actual module from Common.
    delp = _load_native_delp()
    try:
        indexed = delp.validate_graph(bundle['graph'])
        if indexed['programme'].get('id') != identity['programme']['id']:
            raise DiagnosticBridgeError('PLAN_PROGRAMME_ID_MISMATCH')
        if delp.ref_number(indexed['root']) != root_issue:
            raise DiagnosticBridgeError('PLAN_ROOT_MISMATCH')
        leaves = [(ref, row) for ref, row in indexed['nodes'].items()
                  if row['kind'] == 'LEAF' and row['number'] == source['responsibility']['issue_number']]
        if len(leaves) != 1:
            raise DiagnosticBridgeError('LEAF_NOT_IN_PLAN')
        leaf_ref, leaf = leaves[0]
        if leaf.get('primary_pr') is None or delp.ref_number(leaf['primary_pr']) != c['pr_number']:
            raise DiagnosticBridgeError('PLAN_PR_NOT_BOUND')
        # This source is a serialized, caller-supplied U3 evidence envelope.
        # Mark the entire ledger input as untrusted, so even perfect claimed
        # COMPLETE/VERIFIED, CI=PASS and reviewer CLAIMED_ACCEPTED yield E0.
        ledger = [{
            'source': 'R14_U3_UNTRUSTED_SERIALIZATION',
            'order': 0,
            'untrusted_author': 'SERIALIZED_PROVIDER_AND_REVIEW_CLAIM_NOT_AUTHENTICATED',
            'facts': source['checkpoint_facts'],
        }]
        material = {leaf_ref: {'candidate_sha': pr['head_sha'], 'pr_state': 'OPEN'}}
        projection = delp.project(bundle['graph'], ledger, material)
    except DiagnosticBridgeError:
        raise
    except (KeyError, ValueError, TypeError, RuntimeError, AttributeError) as exc:
        raise DiagnosticBridgeError('NATIVE_DELP_PROJECT_FAILED') from exc
    rejected = projection['rejected_facts']
    if len(rejected) != 1 or 'not a trusted fact author' not in str(rejected[0]).lower():
        raise DiagnosticBridgeError('QUARANTINE_NOT_ENFORCED')
    leaf_result = projection['nodes'][leaf_ref]
    root_result = projection['nodes'][indexed['root']]
    if any(leaf_result['progress'][k] != 0 for k in ('P', 'E')):
        raise DiagnosticBridgeError('QUARANTINED_FACT_ADVANCED_PROGRESS')
    if any(root_result['progress'][k] != 0 for k in ('D', 'E')):
        raise DiagnosticBridgeError('QUARANTINED_ROOT_ADVANCED_PROGRESS')
    return {
        'schema': 'relay-diagnostic-delp-bridge-v1-result',
        'source_authority': 'SERIALIZED_R12_SOURCE_UNATTESTED',
        'r12_candidate_state_sha256': bundle['candidate_state']['candidate_state_sha256'],
        'u3_evidence_claim_sha256': claim['evidence_claim_sha256'],
        'actual_delp_source': 'EXISTING_V3_2_PROJECT',
        'delp_plan_digest': projection['plan_digest'],
        'delp_input_digest': projection['input_digest'],
        'leaf_ref': leaf_ref,
        'root_ref': indexed['root'],
        'diagnostic_leaf': {'P': leaf_result['progress']['P'], 'E': leaf_result['progress']['E'], 'state': leaf_result['state']},
        'diagnostic_root': {'D': root_result['progress']['D'], 'E': root_result['progress']['E'], 'state': root_result['state']},
        'quarantined_ledger_claims': len(rejected),
        'provider_authenticity': 'NOT_ATTESTED_AFTER_SERIALIZATION',
        'reviewer_admission': 'NOT_QUALIFIED',
        'owner_authenticity': 'NOT_AUTHENTICATED',
        'writer_lease': 'NOT_PROVEN',
        'publishable_snapshot': False,
        'canonical_programme_acceptance': 'NOT_ADJUDICATED',
        'live_status_writer': 'OFF',
    }


def _cli() -> int:
    """Bounded diagnostic stdin JSON → read-only JSON, never a publishing CLI."""
    import json
    import sys
    try:
        raw = sys.stdin.buffer.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise DiagnosticBridgeError('INPUT_BYTES_LIMIT')
        value = json.loads(raw)
        result = preview_diagnostic(value)
        sys.stdout.write(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
        return 0
    except (DiagnosticBridgeError, ValueError, TypeError, UnicodeError) as exc:
        sys.stderr.write('DIAGNOSTIC_REJECTED:' + str(exc)[:350] + '\n')
        return 2


if __name__ == '__main__':
    raise SystemExit(_cli())
