"""Parent-visible handovers and permitted PR105/106 pipeline scenarios."""
import copy
import unittest

from test_protocol import checker, premerge_bundle, running_bundle, example_bundle, enrich_v11, HEADS, BASE, command

NOW = '2026-10-04T00:08:00Z'


def active(record):
    record.update(status='RUNNING', output_sha=None, validated_sha=None, acceptance_checked=[], validation=[], writer_stopped=False)
    record['work_periods'][0]['end'] = None
    record['publications']['end'] = None


def pipeline_bundle():
    """Synthetic Coordinator reviews 105 while Reviewer works on 106."""
    bundle = premerge_bundle()
    parent, first = bundle['tasks']
    first['pr'] = 105
    second = copy.deepcopy(first)
    second.update(task_id='T87', issue=87, pr=106, scope='Independent second child')
    bundle['tasks'].append(second)
    parent['children'].append(dict(issue=87, scope=second['scope'], covers=['P1'], depends_on=[]))
    coordinator = bundle['stages'][2]
    active(coordinator)
    coordinator.update(workspace_mode='READ_ONLY', review_source=dict(head_sha=HEADS[1], reference='Synthetic fixed full-source snapshot PR105'))
    parent['start_permissions'].append(dict(parent['start_permissions'][0], id='PERMIT87', child_issue=87, issued_at='2026-10-04T00:02:30Z', parent_comment_ref='https://example.invalid/issues/85#permission87', mode='COORDINATOR_READ_ONLY', during_record='S3', reviewed_head_sha=HEADS[1]))
    for index, template in enumerate(bundle['stages'][:2]):
        record = copy.deepcopy(template)
        start, end = f'2026-10-04T00:0{index + 3}:00Z', f'2026-10-04T00:0{index + 3}:30Z'
        record.update(record_id=f'N{index + 1}', task_id='T87', previous_record='N1' if index else None, started_at=start, work_periods=[dict(start=start, end=end)])
        record['parent_context'].update(read_at=start, through_comment_ref=f'https://example.invalid/issues/85#before-N{index + 1}')
        record['publications'] = dict(start=dict(comment_ref=f'https://example.invalid/issues/85#start-N{index + 1}', published_at=start, summary='Synthetic new child START'), end=dict(comment_ref=f'https://example.invalid/issues/85#end-N{index + 1}', published_at=end, summary='Synthetic new child END'))
        record['handover']['pr_description_ref'] = 'https://example.invalid/pull/106'
        record['handover']['child_comment_ref'] = 'https://example.invalid/issues/87#handover'
        if index:
            active(record)
        bundle['stages'].append(record)
    observed = bundle['observed']
    observed['pr_heads'] = {'105': HEADS[1], '106': HEADS[0]}
    observed['pr_states'] = {'105': 'OPEN', '106': 'DRAFT'}
    observed['checks'] = {'105': [dict(check='Required hosted check', head_sha=HEADS[1], result='PASS')]}
    observed['merge_authority_refs'] = {'105': 'Synthetic actual owner instruction'}
    observed['issue_states']['87'] = 'OPEN'
    observed['spec_digests']['T87'] = first['spec_digest']
    observed['workspace']['head_sha'] = HEADS[0]
    observed['parent_comment_frontiers'] = {r['record_id']: dict(comment_ref=r['parent_context']['through_comment_ref'], observed_at=r['started_at']) for r in bundle['stages']}
    return enrich_v11(bundle)


class PipelineTests(unittest.TestCase):
    def rejected(self, bundle, message=None):
        with self.assertRaises(checker.RecordError) as caught:
            checker.validate_bundle(bundle, NOW)
        if message:
            self.assertIn(message, str(caught.exception))

    def state(self, bundle, issue=86, now=NOW):
        return checker.validate_bundle(bundle, now)['issues'][str(issue)]

    def test_role_defaults_15_15_45(self):
        self.assertEqual(checker.DEFAULT_BUDGETS, dict(CODER=15, REVIEWER=15, COORDINATOR=45, PARENT_CHECK=45))

    def test_reviewer_timeout_15_and_coordinator_45(self):
        for count, limit, before, at in [(2, 15, '00:15:59', '00:16:00'), (3, 45, '00:46:59', '00:47:00')]:
            bundle = premerge_bundle()
            bundle['stages'] = bundle['stages'][:count]
            active(bundle['stages'][-1])
            self.assertEqual(self.state(bundle, now=f'2026-10-04T{before}Z')['status'], 'RUNNING')
            self.assertEqual(self.state(bundle, now=f'2026-10-04T{at}Z')['status'], 'STALLED')

    def test_target_timer_does_not_change_other_roles(self):
        bundle = running_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('TIMER', target='REVIEWER', issued='2026-10-04T00:01:00Z', minutes=20)]
        budgets = checker.validate_bundle(bundle, NOW)['stage_budget_minutes']
        self.assertEqual(budgets, dict(CODER=15, REVIEWER=20, COORDINATOR=45, PARENT_CHECK=45))

    def test_done_coder_automatically_makes_reviewer_ready(self):
        bundle = premerge_bundle()
        bundle['stages'] = bundle['stages'][:1]
        state = self.state(bundle)
        self.assertEqual((state['coder'], state['reviewer'], state['stage']), ('DONE', 'READY', 'REVIEWER'))
        self.assertEqual(state['last_parent_evidence'], bundle['stages'][0]['publications']['end']['comment_ref'])

    def test_missing_start_or_end_rejected(self):
        for endpoint in ['start', 'end']:
            bundle = premerge_bundle()
            bundle['stages'][0]['publications'][endpoint] = None
            self.rejected(bundle)

    def test_child_only_evidence_rejected(self):
        bundle = running_bundle()
        bundle['stages'][0]['publications']['start']['comment_ref'] = 'https://example.invalid/issues/86#start'
        self.rejected(bundle, 'parent issue')

    def test_end_not_published_before_next_role_rejected(self):
        bundle = premerge_bundle()
        bundle['stages'][0]['publications']['end']['published_at'] = '2026-10-04T00:01:30Z'
        self.rejected(bundle, 'wait for published parent END')

    def test_parent_frontier_mismatch_rejected(self):
        bundle = running_bundle()
        bundle['observed']['parent_comment_frontiers']['S1']['comment_ref'] = 'https://example.invalid/issues/85#new-owner-comment'
        self.rejected(bundle, 'missed the observed parent comment')

    def test_coder_must_reread_after_grant(self):
        bundle = pipeline_bundle()
        bundle['stages'][3]['parent_context']['read_at'] = '2026-10-04T00:02:00Z'
        self.rejected(bundle, 'reread parent comments after permission')

    def test_no_grant_means_waiting_permission(self):
        bundle = premerge_bundle()
        bundle['stages'] = []
        bundle['tasks'][0]['start_permissions'] = []
        self.assertEqual(self.state(bundle)['coder'], 'WAITING_PERMISSION')

    def test_active_coder_needs_grant(self):
        bundle = running_bundle()
        bundle['tasks'][0]['start_permissions'] = []
        self.rejected(bundle, 'needs the existing Coordinator child permission')

    def test_every_child_requires_own_pr(self):
        bundle = pipeline_bundle()
        bundle['tasks'][2]['pr'] = 105
        self.rejected(bundle, 'different PR')
        bundle = premerge_bundle()
        bundle['tasks'][1]['pr'] = None
        self.rejected(bundle, 'own PR')

    def test_permitted_coordinator_and_reviewer_overlap(self):
        bundle = pipeline_bundle()
        result = checker.validate_bundle(bundle, NOW)['issues']
        self.assertEqual(result['86']['coordinator'], 'RUNNING')
        self.assertEqual(result['87']['coder'], 'DONE')
        self.assertEqual(result['87']['reviewer'], 'RUNNING')

    def test_permitted_coordinator_and_coder_overlap(self):
        bundle = pipeline_bundle()
        bundle['stages'].pop()
        active(bundle['stages'][-1])
        self.assertEqual(self.state(bundle, 87)['coder'], 'RUNNING')

    def test_reviewer_eligible_under_same_overlap_permission(self):
        bundle = pipeline_bundle()
        bundle['stages'].pop()
        state = self.state(bundle, 87)
        self.assertEqual((state['coder'], state['reviewer']), ('DONE', 'READY'))

    def test_second_coordinator_queues(self):
        bundle = pipeline_bundle()
        reviewer = bundle['stages'][-1]
        reviewer.update(status='PASS', output_sha=HEADS[1], validated_sha=HEADS[1], acceptance_checked=['A1'], validation=copy.deepcopy(bundle['stages'][1]['validation']), writer_stopped=True)
        reviewer['work_periods'][0]['end'] = '2026-10-04T00:04:30Z'
        reviewer['publications']['end'] = dict(comment_ref='https://example.invalid/issues/85#end-N2', published_at='2026-10-04T00:04:30Z', summary='Synthetic Reviewer PASS')
        enrich_v11(bundle)
        self.assertEqual(self.state(bundle, 87)['coordinator'], 'QUEUED')

    def test_write_coordinator_cannot_overlap(self):
        bundle = pipeline_bundle()
        bundle['stages'][2].update(workspace_mode='WRITE', review_source=None)
        self.rejected(bundle, 'pinned read-only')

    def test_serial_grant_cannot_authorize_overlap(self):
        bundle = pipeline_bundle()
        bundle['tasks'][0]['start_permissions'][-1].update(mode='SERIAL', during_record=None, reviewed_head_sha=None)
        self.rejected(bundle, 'lacks recorded Coordinator permission')

    def test_wrong_review_head_permission_rejected(self):
        bundle = pipeline_bundle()
        bundle['tasks'][0]['start_permissions'][-1]['reviewed_head_sha'] = HEADS[4]
        self.rejected(bundle, 'wrong Coordinator input')

    def test_two_writers_rejected_with_valid_individual_permissions(self):
        bundle = pipeline_bundle()
        bundle['stages'] = [bundle['stages'][0], bundle['stages'][3]]
        active(bundle['stages'][0])
        active(bundle['stages'][1])
        bundle['tasks'][0]['start_permissions'][-1].update(mode='SERIAL', during_record=None, reviewed_head_sha=None)
        self.rejected(bundle, 'Only one read-only Coordinator')

    def test_revocation_does_not_resurrect_older_permission(self):
        bundle = premerge_bundle()
        bundle['stages'] = []
        parent = bundle['tasks'][0]
        parent['start_permissions'].append(dict(parent['start_permissions'][0], id='NEW86', issued_at='2026-10-04T00:01:00Z', revoked_at='2026-10-04T00:02:00Z'))
        self.assertEqual(self.state(bundle)['status'], 'WAITING_PERMISSION')

    def test_owner_hold_overrides_permission(self):
        bundle = pipeline_bundle()
        bundle['stages'] = bundle['stages'][:3]
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', target='CODER', child=87, issued='2026-10-04T00:03:00Z')]
        self.assertEqual(self.state(bundle, 87)['status'], 'HELD')

    def test_closed_and_merged_are_observed_separately(self):
        bundle = example_bundle()
        bundle['observed']['issue_states']['86'] = 'OPEN'
        state = self.state(bundle)
        self.assertEqual((state['status'], state['issue_state'], state['pr_state']), ('COMPLETE', 'OPEN', 'MERGED'))
        self.assertIn('close', state['next_action'])
        bundle['observed'].pop('issue_states')
        self.assertEqual(self.state(bundle)['issue_state'], 'UNKNOWN')

    def test_parent_coordinator_status_matches_parent_work(self):
        state = self.state(pipeline_bundle(), 85)
        self.assertEqual(state['coordinator'], 'RUNNING')
        self.assertEqual(state['coder'], 'NOT_APPLICABLE')
        self.assertEqual(self.state(example_bundle(), 85)['coordinator'], 'DONE')

    def test_delivery_is_latest_parent_evidence(self):
        bundle = example_bundle()
        self.assertEqual(self.state(bundle)['last_parent_evidence'], bundle['results'][0]['parent_comment_ref'])

    def test_pinned_review_can_finish_while_other_workspace_advances(self):
        bundle = pipeline_bundle()
        coordinator = bundle['stages'][2]
        coordinator.update(status='PASS', writer_stopped=True, output_sha=HEADS[1], validated_sha=HEADS[1], acceptance_checked=['A1'], validation=copy.deepcopy(bundle['stages'][1]['validation']))
        coordinator['work_periods'][0]['end'] = '2026-10-04T00:07:00Z'
        coordinator['publications']['end'] = dict(comment_ref='https://example.invalid/issues/85#end-S3', published_at='2026-10-04T00:07:00Z', summary='Synthetic pinned final review PASS')
        bundle['observed']['review_snapshots'] = {'S3': dict(reference=coordinator['review_source']['reference'], head_sha=HEADS[1], unrecorded_changes=False)}
        enrich_v11(bundle)
        self.assertEqual(self.state(bundle)['status'], 'MERGE_READY')
        bundle['observed']['review_snapshots']['S3']['head_sha'] = HEADS[0]
        self.assertEqual(self.state(bundle)['status'], 'REWORK')


if __name__ == '__main__':
    unittest.main()
