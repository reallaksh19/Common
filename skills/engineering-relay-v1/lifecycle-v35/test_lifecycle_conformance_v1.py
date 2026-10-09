"""R14 WP1/U4 exact Python/Node claim-digest conformance, never authority.

Python's *actual* U1/U2/U3 validators determine structural accept/reject.
Node checks nested identity/historical consistency and canonical byte/digest
agreement; it does NOT reimplement Python schema validation or DELP progress.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import unittest

from identity_contract_v1 import validate_identity, IdentityContractError
from owner_session_contract_v1 import validate_owner_session, OwnerSessionError
from evidence_review_contract_v1 import validate_evidence_review, EvidenceReviewError, DELP_FILE
from test_evidence_review_contract_v1 import sample as fixture

HERE = Path(__file__).resolve().parent
NODE_SCRIPT = HERE / 'lifecycle-conformance-v1.mjs'
ROOT = HERE.parents[2]
NODE = shutil.which('node')


def packet(source):
    """Build source-validated fixture. Has no provider-trust or review admission."""
    identity = source['owner_session']['identity']
    owner_session = source['owner_session']
    ids = validate_identity(identity)
    history = validate_owner_session(owner_session)
    evidence = validate_evidence_review(source)
    return {
        'schema': 'relay-lifecycle-cross-language-v1',
        'identity': copy.deepcopy(identity),
        'owner_session': copy.deepcopy(owner_session),
        'evidence_review': copy.deepcopy(source),
        'expected': {
            'identity_sha256': ids['identity_sha256'],
            'history_sha256': history['history_sha256'],
            'evidence_claim_sha256': evidence['evidence_claim_sha256'],
        },
    }


def run_node(payload):
    if NODE is None:
        raise unittest.SkipTest('Node runtime absent; cross-language validation NOT_RUN')
    raw=json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':'))
    return subprocess.run([NODE,str(NODE_SCRIPT)],input=raw,encoding='utf-8',
                          capture_output=True,timeout=10,check=False)


@unittest.skipUnless(NODE is not None, 'Node not installed: cross-language tests NOT_RUN')
class PythonNodeConformanceTests(unittest.TestCase):
    def test_positive_all_three_bound_fingerprints(self):
        p=packet(fixture())
        result=run_node(p)
        self.assertEqual(0,result.returncode,result.stderr)
        output=json.loads(result.stdout)
        self.assertEqual('MATCHED_CALLER_SUPPLIED_DIGESTS_ONLY',output['digest_agreement'])
        for name,digest in p['expected'].items():
            self.assertEqual(digest,output[name])
        self.assertEqual('NOT_GRANTED',output['reviewer_authorization'])
        self.assertEqual('NOT_PROVEN',output['exclusive_writer_lease'])
        self.assertIsNone(output['programme_progress'])
        self.assertEqual('NOT_CALCULATED',output['canonical_programme_projection'])

    def test_stable_source_derived_synthetic_goldens(self):
        p=packet(fixture())
        self.assertEqual('sha256:7337f8d41f821cda3c7a18b648d1c2bbc3f33863aaa1caa14357f2f0c2c8b256',
                         p['expected']['evidence_claim_sha256'])
        self.assertEqual('sha256:9f2fdd9bb4dd151bc4ab9a8161026f0d87ea7c412563b9d97860239dff600517',
                         p['expected']['history_sha256'])
        self.assertEqual('sha256:f8de3b1492ced91cf97f1a52880d3fbe777ad02846899804d824d49b2978150a',
                         p['expected']['identity_sha256'])

    def test_json_object_key_reordering_is_portable(self):
        p=packet(fixture())
        for key in ('identity','owner_session','evidence_review','expected'):
            p[key]=dict(reversed(list(p[key].items())))
        self.assertEqual(0,run_node(p).returncode)

    def test_non_ascii_actor_unicode_matches_python(self):
        src=fixture()
        src['producer']['actor_label']='Agent A — café 🐈'
        for e in src['owner_session']['session_events']:
            e['actor_label']='Agent A — café 🐈'
        out=run_node(packet(src))
        self.assertEqual(0,out.returncode,out.stderr)

    def test_owner_history_mutation_invalidates_old_goldens(self):
        p=packet(fixture())
        modified=copy.deepcopy(p)
        for point in (modified['owner_session']['owner_events'],
                      modified['evidence_review']['owner_session']['owner_events']):
            point[1]['content_sha256']='sha256:'+'e'*64
        out=run_node(modified)
        self.assertEqual(2,out.returncode)
        self.assertIn('CONFORMANCE_DIGEST_MISMATCH',out.stderr)
        updated=packet(modified['evidence_review'])
        self.assertEqual(0,run_node(updated).returncode)

    def test_head_move_invalidates_old_goldens_even_when_all_claims_move(self):
        p=packet(fixture())
        changed=copy.deepcopy(p)
        for iden in (changed['identity'],changed['owner_session']['identity'],
                     changed['evidence_review']['owner_session']['identity']):
            iden['candidate_source']['head_sha']='f'*40
        facts=changed['evidence_review']['checkpoint_facts']
        facts['material']['candidate_sha']='f'*40
        facts['units'][0]['candidate_sha']='f'*40
        changed['evidence_review']['test_observations'][0]['tested_head_sha']='f'*40
        self.assertEqual(2,run_node(changed).returncode)
        self.assertEqual(0,run_node(packet(changed['evidence_review'])).returncode)

    def test_nested_identity_spoof_rejected_even_if_digest_supplied(self):
        p=packet(fixture())
        p['owner_session']['identity']['programme']['root_issue']=999
        out=run_node(p)
        self.assertEqual(2,out.returncode)
        self.assertIn('NESTED_SOURCE_DRIFT',out.stderr)

    def test_nested_history_spoof_rejected(self):
        p=packet(fixture())
        p['evidence_review']['owner_session']['owner_events'][1]['content_sha256']='sha256:'+'e'*64
        out=run_node(p)
        self.assertEqual(2,out.returncode)
        self.assertIn('NESTED_SOURCE_DRIFT',out.stderr)

    def test_mismatched_digest_rejected(self):
        p=packet(fixture())
        p['expected']['identity_sha256']='sha256:'+'f'*64
        out=run_node(p)
        self.assertEqual(2,out.returncode)
        self.assertIn('CONFORMANCE_DIGEST_MISMATCH:identity_sha256',out.stderr)

    def test_no_extra_writers_or_progress_keys(self):
        p=packet(fixture())
        p['writer_authorization']='GRANTED'
        out=run_node(p)
        self.assertEqual(2,out.returncode)
        self.assertIn('BAD_PACKET_SHAPE',out.stderr)

    def test_conformance_cannot_qualify_forged_reviewer(self):
        src=fixture()
        src['reviewer_claim'].update(state='CLAIMED_ACCEPTED',actor_label='different label',
            session_id='DIFFERENT_SESSION',candidate_sha='c'*40,
            source_url='https://github.com/reallaksh19/Common/pull/891#pullrequestreview-123',
            source_digest='sha256:'+'d'*64)
        p=packet(src)
        out=run_node(p)
        self.assertEqual(0,out.returncode,out.stderr)
        value=json.loads(out.stdout)
        self.assertEqual('NOT_GRANTED',value['reviewer_authorization'])
        self.assertEqual('NOT_CALCULATED',value['canonical_programme_projection'])

    def test_complete_failed_claim_cannot_gain_accepted_evidence(self):
        src=fixture()
        src['checkpoint_facts']['units'][0]['result']='FAILED'
        out=run_node(packet(src))
        self.assertEqual(0,out.returncode,out.stderr)
        self.assertIsNone(json.loads(out.stdout)['programme_progress'])

    def test_python_validator_rejects_fake_progress_before_node(self):
        src=fixture()
        src['progress_percent']=100
        with self.assertRaises(EvidenceReviewError):
            packet(src)

    def test_python_validator_rejects_changed_candidate_without_updated_facts(self):
        src=fixture()
        src['owner_session']['identity']['candidate_source']['head_sha']='e'*40
        with self.assertRaises(EvidenceReviewError):
            packet(src)

    def test_python_validator_rejects_owner_source_spoof(self):
        src=fixture()
        src['owner_session']['owner_events'][0]['source_url']='https://github.com.fake/x/y/issues/4#issuecomment-9'
        with self.assertRaises((OwnerSessionError,EvidenceReviewError)):
            packet(src)

    def test_json_nonportable_number_rejected_by_node(self):
        p=packet(fixture())
        p['identity']['programme']['root_issue']=2**53
        p['owner_session']['identity']['programme']['root_issue']=2**53
        p['evidence_review']['owner_session']['identity']['programme']['root_issue']=2**53
        out=run_node(p)
        self.assertEqual(2,out.returncode)
        self.assertIn('NON_PORTABLE_NUMBER',out.stderr)

    def test_node_never_claims_it_ran_python_validation(self):
        p=packet(fixture())
        out=run_node(p)
        self.assertEqual(0,out.returncode)
        self.assertEqual('NOT_CHECKED_BY_NODE',json.loads(out.stdout)['python_contract_status'])


class NativeDelpActualCheckoutTests(unittest.TestCase):
    @unittest.skipUnless(DELP_FILE.is_file(), 'complete Common DELP source absent: native test NOT_RUN')
    def test_native_delp_validate_facts_good_and_forbidden_progress(self):
        source=fixture()
        spec=importlib.util.spec_from_file_location('v32_native_delp_u4',DELP_FILE)
        native=importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(native)
        self.assertEqual([],native.validate_facts(source['checkpoint_facts']))
        result=validate_evidence_review(source)
        self.assertEqual('NATIVE_DELP_STRUCTURE_VALID_ONLY',result['delp_facts_structure'])
        bad=copy.deepcopy(source['checkpoint_facts'])
        bad['progress']=100
        self.assertTrue(native.validate_facts(bad))
        source['checkpoint_facts']=bad
        with self.assertRaises(EvidenceReviewError):
            validate_evidence_review(source)


if __name__=='__main__': unittest.main(verbosity=2)
