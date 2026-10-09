"""WP2/U01: diagnostic R12 candidate → actual DELP consumer, claims quarantined.

Synthetic stub cases verify bridge control flow but are NOT native DELP tests.
The native test explicitly skips when a complete Common source checkout is absent.
"""
from __future__ import annotations

import copy
import importlib.util
import unittest
from unittest.mock import patch

from test_evidence_review_contract_v1 import sample
import diagnostic_delp_bridge_v1 as B

SHA = 'c' * 40

def bundle():
    evidence = sample()
    return {
        'schema': 'relay-diagnostic-delp-bridge-v1',
        'graph': {
            'schema': 'relay-v3.2-delp-execution-graph',
            'programme': {'id': 'R14-WP1-RESEARCH', 'repository': 'reallaksh19/Common', 'root': 'Common#787'},
            'nodes': [
                {'ref': 'Common#787', 'kind': 'ROOT'},
                {'ref': 'Common#878', 'kind': 'LEAF', 'parent': 'Common#787',
                 'primary_pr': 'Common#891', 'weight': 1, 'units': [{'id': 'U03', 'weight': 100}]},
            ],
        },
        'evidence_review': evidence,
        'candidate_state': {
            'schema': 'relay-candidate-verification-v1',
            'repository': 'reallaksh19/Common', 'parent_issue': 787,
            'candidate_state_sha256': 'a' * 64,
            'source_acquisition_attested': True,  # JSON boolean is NOT a capability
            'pr_candidates': [{'number': 891, 'head_sha': SHA, 'expected_head_sha': SHA,
                               'head_state': 'CURRENT', 'selected_ci_state': 'PASS',
                               'selected_ci_qualified': True}],
        },
    }

class FakeDelp:
    """Only for control-flow tests, not native acceptance."""
    def __init__(self, claim_progress=0, reject=True):
        self.progress = claim_progress
        self.reject = reject
        self.invoked = False
        self.ledger = None
    def validate_graph(self, g):
        return {'programme': g['programme'], 'root': 'Common#787',
                'nodes': {'Common#787': {'kind': 'ROOT', 'number': 787},
                          'Common#878': {'kind': 'LEAF', 'number': 878, 'primary_pr': 'Common#891'}}}
    @staticmethod
    def ref_number(v):
        return int(str(v).split('#')[-1])
    def project(self, graph, ledger, observations):
        self.invoked = True
        self.ledger = ledger
        assert ledger[0].get('untrusted_author') and observations['Common#878']['candidate_sha'] == SHA
        return {
            'plan_digest': 'sha256:' + 'a'*64, 'input_digest': 'sha256:' + 'b'*64,
            'rejected_facts': ([{'reasons': ['author is not a trusted fact author']}]
                               if self.reject else []),
            'nodes': {'Common#787': {'progress': {'D': self.progress, 'E': self.progress}, 'state': 'ACTIVE'},
                      'Common#878': {'progress': {'P': self.progress, 'E': self.progress}, 'state': 'ACTIVE'}},
        }

class DiagnosticBridgeTests(unittest.TestCase):
    def error(self, b, message):
        with self.assertRaises(B.DiagnosticBridgeError) as ctx:
            B.preview_diagnostic(b)
        self.assertIn(message, str(ctx.exception))

    def test_bound_native_shape_is_quarantined_even_when_r12_claims_native_green(self):
        b = bundle()
        stub = FakeDelp()
        with patch.object(B, '_load_native_delp', return_value=stub):
            o = B.preview_diagnostic(b)
        self.assertTrue(stub.invoked)
        self.assertEqual('NOT_ATTESTED_AFTER_SERIALIZATION', o['provider_authenticity'])
        self.assertEqual('EXISTING_V3_2_PROJECT', o['actual_delp_source'])
        self.assertFalse(o['publishable_snapshot'])
        self.assertEqual({'P': 0, 'E': 0, 'state': 'ACTIVE'}, o['diagnostic_leaf'])
        self.assertEqual(1, o['quarantined_ledger_claims'])
        self.assertEqual('OFF', o['live_status_writer'])

    def test_no_source_checkout_blocks_real_delp(self):
        b = bundle()
        with patch.object(B, 'NATIVE_DELP', B.NATIVE_DELP.parent/'missing-file.py'):
            self.error(b, 'NATIVE_DELP_NOT_AVAILABLE')

    def test_forged_progress_granted_by_native_fails_closed(self):
        with patch.object(B, '_load_native_delp', return_value=FakeDelp(claim_progress=100)):
            self.error(bundle(), 'QUARANTINED_FACT_ADVANCED_PROGRESS')

    def test_missing_rejection_cannot_silently_proceed(self):
        with patch.object(B, '_load_native_delp', return_value=FakeDelp(reject=False)):
            self.error(bundle(), 'QUARANTINE_NOT_ENFORCED')

    def test_stale_r12_head_refused_before_delp(self):
        b = bundle(); b['candidate_state']['pr_candidates'][0]['head_state'] = 'STALE'
        self.error(b, 'R12_CANDIDATE_NOT_CURRENT')

    def test_wrong_r12_head_refused_before_delp(self):
        b = bundle(); b['candidate_state']['pr_candidates'][0]['head_sha'] = 'd'*40
        self.error(b, 'R12_CANDIDATE_SHA_CHANGED')

    def test_foreign_r12_parent_refused(self):
        b = bundle(); b['candidate_state']['parent_issue'] = 878
        self.error(b, 'R12_PARENT_OR_REPOSITORY_MISMATCH')

    def test_duplicated_r12_pr_refused(self):
        b = bundle(); b['candidate_state']['pr_candidates'].append(copy.deepcopy(b['candidate_state']['pr_candidates'][0]))
        self.error(b, 'R12_EXACT_PR_NOT_UNIQUE')

    def test_changed_u3_producer_claim_refused(self):
        b = bundle(); b['evidence_review']['producer']['session_id'] = 'OTHER'
        self.error(b, 'U3_CLAIM_INVALID')

    def test_forged_u3_review_grant_refused(self):
        b = bundle(); b['evidence_review']['reviewer_claim']['independently_accepted'] = True
        self.error(b, 'U3_CLAIM_INVALID')

    def test_plan_programme_mismatch_refused(self):
        b = bundle(); b['graph']['programme']['id'] = 'WRONG'
        with patch.object(B, '_load_native_delp', return_value=FakeDelp()):
            self.error(b, 'PLAN_PROGRAMME_ID_MISMATCH')

    def test_wrong_validated_plan_root_refused(self):
        b = bundle()
        class FakeWrongRoot(FakeDelp):
            def validate_graph(self, g):
                indexed = super().validate_graph(g)
                indexed['root'] = 'Common#999'
                return indexed
        with patch.object(B, '_load_native_delp', return_value=FakeWrongRoot()):
            self.error(b, 'PLAN_ROOT_MISMATCH')

    @unittest.skipUnless(B.NATIVE_DELP.is_file(), 'complete Common checkout absent: actual DELP.project NOT_RUN')
    def test_full_checkout_uses_actual_delp_validate_and_project(self):
        got = B.preview_diagnostic(bundle())
        self.assertEqual('EXISTING_V3_2_PROJECT', got['actual_delp_source'])
        self.assertEqual({'P': 0, 'E': 0, 'state': 'UNMATERIALIZED'}, got['diagnostic_leaf'])
        self.assertEqual(1, got['quarantined_ledger_claims'])
        self.assertFalse(got['publishable_snapshot'])

if __name__ == '__main__': unittest.main(verbosity=2)
