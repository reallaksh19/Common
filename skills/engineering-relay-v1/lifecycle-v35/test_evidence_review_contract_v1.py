"""R14 WP1/U3 native reference-contract unit tests (synthetic inputs)."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_owner_session_contract_v1 import sample as source_sample

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('evidence_review_contract_v1', HERE/'evidence_review_contract_v1.py')
assert spec and spec.loader
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
A, B, C, D = 'a'*40, 'b'*40, 'c'*40, 'sha256:'+'d'*64
REPO = 'reallaksh19/Common'


def sample():
    return {
        'schema':'relay-lifecycle-evidence-review-v1','mode':'RESEARCH_ONLY',
        'owner_session':source_sample(),
        'responsibility':{'id':'R14-WP1-U3','issue_number':878,'spec_generation':1,'contract_digest':D},
        'producer':{'session_id':'AGENT_A_SESSION','actor_label':'Agent A (unverified)'},
        'checkpoint_facts':{
            'schema':'relay-v3.2-delp-checkpoint-facts',
            'responsibility':{'issue':REPO+'#878'},
            'material':{'pr':REPO+'#891','candidate_sha':C,'base_sha':A},
            'units':[{'id':'U03','state':'COMPLETE','result':'VERIFIED',
                      'candidate_sha':C,'contract_digest':D,
                      'evidence_refs':[REPO+'#878#issuecomment-6083423582']}]},
        'test_observations':[{'id':'T1','result':'PASS','tested_head_sha':C,'fixture_sha256':D,
                              'golden_sha256':D,'run_url':None}],
        'reviewer_claim':{'state':'NOT_SUBMITTED','actor_label':None,'session_id':None,
                          'candidate_sha':None,'source_url':None,'source_digest':None},
    }


class EvidenceReviewContractV1Tests(unittest.TestCase):
    def setUp(self):
        self.x = sample()

    def reject(self, phrase):
        with self.assertRaises(M.EvidenceReviewError) as err:
            M.validate_evidence_review(self.x)
        self.assertIn(phrase, str(err.exception))

    def test_positive_untrusted_fact_and_test_claims(self):
        r = M.validate_evidence_review(self.x)
        self.assertEqual('NATIVE_DELP_VALIDATOR_NOT_RUN', r['delp_facts_structure'])
        self.assertEqual('NOT_CALCULATED', r['canonical_delp_projection'])
        self.assertEqual('UNADJUDICATED_CLAIMS', r['verification_evidence'])
        self.assertIsNone(r['programme_progress'])
        self.assertEqual('OFF', r['publisher'])
        self.assertTrue(r['evidence_claim_sha256'].startswith('sha256:'))
        self.assertEqual('sha256:7337f8d41f821cda3c7a18b648d1c2bbc3f33863aaa1caa14357f2f0c2c8b256', r['evidence_claim_sha256'])

    def test_structural_review_claim_never_qualifies_independence(self):
        self.x['reviewer_claim'].update(state='CLAIMED_ACCEPTED',actor_label='separate label',
            session_id='REVIEWER_SESSION',candidate_sha=C,
            source_url=f'https://github.com/{REPO}/pull/891#pullrequestreview-12',source_digest=D)
        r = M.validate_evidence_review(self.x)
        self.assertEqual('DIFFERENT_LABELS_NOT_INDEPENDENCE_PROOF',r['reviewer_independence'])
        self.assertEqual('NOT_QUALIFIED',r['reviewer_admission'])

    def test_rejected_review_is_still_a_claim(self):
        self.x['reviewer_claim'].update(state='CLAIMED_REJECTED',actor_label='reviewer',
            session_id='OTHER',candidate_sha=C,
            source_url=f'https://github.com/{REPO}/pull/891#issuecomment-12',source_digest=D)
        self.assertEqual('NOT_QUALIFIED',M.validate_evidence_review(self.x)['reviewer_admission'])

    def test_candidate_move_changes_digest_only_when_bound_refs_move(self):
        initial=M.validate_evidence_review(self.x)['evidence_claim_sha256']
        moved=copy.deepcopy(self.x)
        new='f'*40
        moved['owner_session']['identity']['candidate_source']['head_sha']=new
        moved['checkpoint_facts']['material']['candidate_sha']=new
        moved['checkpoint_facts']['units'][0]['candidate_sha']=new
        moved['test_observations'][0]['tested_head_sha']=new
        self.assertNotEqual(initial,M.validate_evidence_review(moved)['evidence_claim_sha256'])

    def test_history_amendment_changes_evidence_digest(self):
        old=M.validate_evidence_review(self.x)['evidence_claim_sha256']
        self.x['owner_session']['owner_events'].append({
          'id':'O003','kind':'DECISION_CLAIM','source_grade':'UNKNOWN',
          'source_url':None,'content_sha256':None,'predecessor_id':'O002'})
        self.assertNotEqual(old,M.validate_evidence_review(self.x)['evidence_claim_sha256'])

    def test_parent_issue_cannot_be_leaf(self):
        self.x['responsibility']['issue_number']=787
        self.x['checkpoint_facts']['responsibility']['issue']=REPO+'#787'
        self.reject('LEAF_CANNOT_BE_PARENT')

    def test_wrong_leaf_binding_rejected(self):
        self.x['checkpoint_facts']['responsibility']['issue']=REPO+'#999'
        self.reject('FACTS_RESPONSIBILITY_NOT_BOUND')

    def test_wrong_pr_binding_rejected(self):
        self.x['checkpoint_facts']['material']['pr']=REPO+'#999'
        self.reject('FACTS_PR_NOT_BOUND')

    def test_moved_candidate_unupdated_facts_rejected(self):
        self.x['owner_session']['identity']['candidate_source']['head_sha']='f'*40
        self.reject('MATERIAL_CANDIDATE_MISMATCH')

    def test_moved_base_rejected(self):
        self.x['checkpoint_facts']['material']['base_sha']='f'*40
        self.reject('MATERIAL_CANDIDATE_MISMATCH')

    def test_unobserved_plan_ref_rejected(self):
        self.x['owner_session']['identity']['graph_source'].update(state='UNKNOWN',
         revision_sha=None,path=None,content_sha256=None)
        self.reject('PLAN_OR_CANDIDATE_UNOBSERVED')

    def test_unobserved_candidate_ref_rejected(self):
        self.x['owner_session']['identity']['candidate_source'].update(state='UNKNOWN',
         pr_number=None,head_sha=None,base_sha=None)
        self.reject('PLAN_OR_CANDIDATE_UNOBSERVED')

    def test_wrong_producer_session_rejected(self):
        self.x['producer']['session_id']='FAKE'
        self.reject('PRODUCER_SESSION_NOT_BOUND')

    def test_claimed_stopped_producer_rejected(self):
        self.x['owner_session']['session_events'].append({
         'id':'S003','session_id':'AGENT_A_SESSION','actor_label':'Agent A (unverified)',
         'kind':'STOP_CLAIMED','owner_event_id':'O002','source_commit':B,'predecessor_id':'S002'})
        self.reject('PRODUCER_SESSION_CLAIMED_STOPPED')

    def test_unit_head_wrong_rejected(self):
        self.x['checkpoint_facts']['units'][0]['candidate_sha']='e'*40
        self.reject('UNIT_HEAD_MISMATCH')

    def test_unit_contract_wrong_rejected(self):
        self.x['checkpoint_facts']['units'][0]['contract_digest']='sha256:'+'e'*64
        self.reject('UNIT_CONTRACT_MISMATCH')

    def test_verified_without_evidence_rejected(self):
        self.x['checkpoint_facts']['units'][0]['evidence_refs']=[]
        self.reject('VERIFIED_WITHOUT_EVIDENCE')

    def test_duplicate_unit_rejected(self):
        self.x['checkpoint_facts']['units']*=2
        self.reject('DUPLICATE_FACTS_UNIT')

    def test_failed_complete_is_not_silently_promoted(self):
        self.x['checkpoint_facts']['units'][0]['result']='FAILED'
        r=M.validate_evidence_review(self.x)
        self.assertEqual('UNADJUDICATED_CLAIMS',r['verification_evidence'])
        self.assertIsNone(r['programme_progress'])

    def test_tests_moved_head_rejected(self):
        self.x['test_observations'][0]['tested_head_sha']='e'*40
        self.reject('EXECUTED_TEST_HEAD_MISMATCH')

    def test_not_run_test_cannot_have_head(self):
        self.x['test_observations'][0]['result']='NOT_RUN'
        self.reject('NOT_RUN_HAS_TEST_HEAD')

    def test_not_run_without_head_is_preserved_as_unadjudicated(self):
        self.x['test_observations'][0].update(result='NOT_RUN',tested_head_sha=None)
        self.assertEqual('UNADJUDICATED_CLAIMS',M.validate_evidence_review(self.x)['verification_evidence'])

    def test_unknown_test_with_claimed_head_rejected(self):
        self.x['test_observations'][0]['result']='UNKNOWN'
        self.reject('UNKNOWN_TEST_HEAD_ASSERTED')

    def test_run_url_off_repo_rejected(self):
        self.x['test_observations'][0]['run_url']='https://github.com/evil/repo/actions/runs/1'
        self.reject('RUN_URL_UNTRUSTED')

    def test_lookalike_run_domain_rejected(self):
        self.x['test_observations'][0]['run_url']='https://github.com.evil.test/'+REPO+'/actions/runs/1'
        self.reject('RUN_URL_UNTRUSTED')

    def test_duplicate_test_identifier_rejected(self):
        self.x['test_observations']*=2
        self.reject('DUPLICATE_TEST_ID')

    def test_fake_evidence_percent_rejected(self):
        self.x['evidence_percent']=100
        self.reject('SCHEMA_INVALID')

    def test_fake_reviewer_grant_rejected(self):
        self.x['reviewer_claim']['independently_accepted']=True
        self.reject('SCHEMA_INVALID')

    def test_self_review_actor_rejected(self):
        self.x['reviewer_claim'].update(state='CLAIMED_ACCEPTED',actor_label='Agent A (unverified)',
            session_id='R2',candidate_sha=C,
            source_url=f'https://github.com/{REPO}/pull/891#pullrequestreview-12',source_digest=D)
        self.reject('SELF_REVIEW_CLAIM')

    def test_self_review_session_rejected(self):
        self.x['reviewer_claim'].update(state='CLAIMED_ACCEPTED',actor_label='Other',
            session_id='AGENT_A_SESSION',candidate_sha=C,
            source_url=f'https://github.com/{REPO}/pull/891#pullrequestreview-12',source_digest=D)
        self.reject('SELF_REVIEW_CLAIM')

    def test_stale_review_rejected(self):
        self.x['reviewer_claim'].update(state='CLAIMED_ACCEPTED',actor_label='Other',
            session_id='Other',candidate_sha='e'*40,
            source_url=f'https://github.com/{REPO}/pull/891#pullrequestreview-12',source_digest=D)
        self.reject('STALE_REVIEW_CLAIM')

    def test_review_wrong_pr_rejected(self):
        self.x['reviewer_claim'].update(state='CLAIMED_ACCEPTED',actor_label='Other',
            session_id='Other',candidate_sha=C,
            source_url=f'https://github.com/{REPO}/pull/892#pullrequestreview-12',source_digest=D)
        self.reject('REVIEW_URL_UNTRUSTED')

    def test_review_missing_material_rejected(self):
        self.x['reviewer_claim']['state']='CLAIMED_ACCEPTED'
        self.reject('REVIEW_CLAIM_INCOMPLETE')

    def test_absent_reviewer_own_claim_rejected(self):
        self.x['reviewer_claim']['actor_label']='unverified'
        self.reject('ABSENT_REVIEW_HAS_ASSERTIONS')

    def test_upstream_u2_mirror_spoof_rejected(self):
        self.x['owner_session']['owner_events'][0]['source_url']='https://github.com.fake/'+REPO+'/issues/787#issuecomment-1'
        self.reject('U2_HISTORY_INVALID')

    def test_real_delp_validator_when_available_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_file=Path(tmp)/'delp_stub.py'
            module_file.write_text('def validate_facts(facts):\n    return ["synthetic validation error"]\n')
            with patch.object(M,'DELP_FILE',module_file):
                self.reject('NATIVE_DELP_FACTS_INVALID:synthetic validation error')

    def test_real_delp_validator_when_available_success_still_unaccepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_file=Path(tmp)/'delp_stub.py'
            module_file.write_text('def validate_facts(facts):\n    return []\n')
            with patch.object(M,'DELP_FILE',module_file):
                r=M.validate_evidence_review(self.x)
                self.assertEqual('NATIVE_DELP_STRUCTURE_VALID_ONLY',r['delp_facts_structure'])
                self.assertEqual('NOT_QUALIFIED',r['reviewer_admission'])

if __name__=='__main__': unittest.main(verbosity=2)
