import copy
import importlib.util
import json
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SPEC = importlib.util.spec_from_file_location('local_pr_validator', ROOT / 'scripts' / 'validate.py')
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
BASE, MERGE = 'b' * 40, 'c' * 40
HEADS = [str(i) * 40 for i in range(1, 6)]
DIGEST = 'd' * 64
FOLDER = r'C:\Example\SharedEditor'


PROJECT_DIGEST = 'e' * 64
COMMON_DIGEST = '0' * 64
HARNESS_DIGEST = 'f' * 64
BASELINE_DIGEST = '1' * 64
ORACLE_DIGEST = '2' * 64
POLICY_DIGEST = '3' * 64
WORKFLOW_DIGEST = '4' * 64
ENV_DIGEST = '5' * 64
TREE_DIGEST = '6' * 64
SURFACE_DIGEST = '7' * 64
WORKSPACE_DIGEST = '8' * 64
PARENT_CONTEXT_DIGEST = 'a' * 64
CHILD_CONTEXT_DIGEST = 'b' * 64
PR_DESCRIPTION_DIGEST = 'c' * 64
OWNER_CONTROL_DIGEST = '9' * 64
POLICY_SOURCE = 'https://example.invalid/policy/required-checks'
WORKFLOW_PATH = '.github/workflows/required.yml'
EXPECTED_APP = 'github-actions'
ARTIFACT_DIGEST = 'e' * 64


def enrich_v11(bundle):
    tasks = {task['task_id']: task for task in bundle['tasks']}
    for task in bundle['tasks']:
        task['version'] = '1.1'
        task['protocol_ref'] = task['protocol_ref'].replace('Local_PR_Deliverty_v1.0', 'Local_PR_Deliverty_v1.1')
        task['project_protocol_ref'] = 'exampleowner/editor@' + '9' * 40 + ':review/project-protocol.json'
        task['project_protocol_digest'] = PROJECT_DIGEST
        task['protocol_digest'] = COMMON_DIGEST
        task['owner_principals'] = ['owner']
        task['role_principals'] = dict(CODER=['coder', 'new-coder', 'other-coder'], REVIEWER=['reviewer'], COORDINATOR=['coordinator'])
        task.setdefault('stacked_dependencies', [])
        task['required_check_policy'] = dict(source_ref=POLICY_SOURCE, digest=POLICY_DIGEST, provider='GITHUB_ACTIONS')
        task['required_check_contracts'] = [
            dict(check=name, provider='GITHUB_ACTIONS', workflow_digest=WORKFLOW_DIGEST, policy_source=POLICY_SOURCE, workflow_path=WORKFLOW_PATH, expected_app=EXPECTED_APP)
            for name in task['required_checks']
        ]
        task.setdefault('waivable_criteria', [])
        task.setdefault('waivable_required_checks', [])
        for criterion in task['acceptance']:
            criterion['verification_method_ids'] = ['VM-' + criterion['id']]
            criterion.setdefault('super_review_required', True)

    support = dict(review_leases=[], environments=[], context_snapshots=[], waivers=[], observed_states=[], evidence_records=[], project_protocols=[])
    bundle['support'] = support
    criteria = {}
    for task in bundle['tasks']:
        for criterion in task['acceptance']:
            if criterion['id'] not in criteria:
                criteria[criterion['id']] = dict(
                    id=criterion['id'],
                    required=criterion['required'],
                    reviewer_check_required=True,
                    super_review_required=criterion['super_review_required'],
                    verification_method_ids=list(criterion['verification_method_ids']),
                )
    support['project_protocols'].append(dict(
        protocol_id='SYNTHETIC-PROJECT-v1',
        version='1.0',
        repository=bundle['tasks'][0]['repository'],
        source_ref=bundle['tasks'][0]['project_protocol_ref'],
        digest=PROJECT_DIGEST,
        acceptance_sets=[dict(id='ALL', criteria=list(criteria.values()))],
        harnesses=[dict(
            id='SR-ALL',
            criteria=[criterion_id for criterion_id, criterion in criteria.items() if criterion['super_review_required']],
            protected=True,
        )],
        protected_surface=dict(
            harness_digest=HARNESS_DIGEST,
            baseline_digest=BASELINE_DIGEST,
            oracle_digests=[ORACLE_DIGEST],
        ),
        external_gates=[],
    ))

    for record in bundle['stages']:
        record['version'] = '1.1'
        record['repeat_stages'] = []
        record['waiver_refs'] = []
        record['role_integrity'] = dict(claimed_role=record['stage'], principal=record['executor'])
        record['common_protocol_ref'] = tasks[record['task_id']]['protocol_ref']
        record['common_protocol_digest'] = tasks[record['task_id']]['protocol_digest']
        record['project_protocol_ref'] = tasks[record['task_id']]['project_protocol_ref']
        record['environment_ref'] = 'ENV-' + record['record_id']
        support['environments'].append(dict(
            environment_id=record['environment_ref'],
            os='synthetic-os',
            architecture='synthetic-arch',
            toolchain=[dict(name='python', version='3.12')],
            lockfile_digest=None,
            container_digest=None,
            external_versions=[],
            network_policy='OFFLINE',
            secret_values_recorded=False,
            digest=ENV_DIGEST,
        ))

        checked = list(record['acceptance_checked'])
        evidence_id = 'EV-' + record['record_id']
        evidence_class = 'SUPER_REVIEW_INDEPENDENT' if record['stage'] in ['COORDINATOR', 'PARENT_CHECK'] else 'REVIEWER_INDEPENDENT' if record['stage'] == 'REVIEWER' else 'AUTHOR'
        final_source = record['validated_sha'] or record['output_sha'] or record['input_sha']
        record['evidence_manifest'] = [dict(
            evidence_id=evidence_id,
            **{'class': evidence_class},
            result='PASS' if record['status'] == 'PASS' else 'NOT_RUN',
            source_sha=final_source,
            procedure='Synthetic protocol evidence fixture.',
            artifact_digest=None,
            harness_digest=HARNESS_DIGEST if evidence_class == 'SUPER_REVIEW_INDEPENDENT' else None,
            baseline_digest=BASELINE_DIGEST if evidence_class == 'SUPER_REVIEW_INDEPENDENT' else None,
            environment_digest=ENV_DIGEST,
        )]
        record['evidence_refs'] = [evidence_id]
        support['evidence_records'].append(dict(
            evidence_id=evidence_id,
            producer_role=record['stage'],
            producer_principal=record['executor'],
            evidence_class=evidence_class,
            candidate_sha=final_source,
            project_protocol_digest=PROJECT_DIGEST,
            harness_digest=HARNESS_DIGEST if evidence_class == 'SUPER_REVIEW_INDEPENDENT' else None,
            baseline_digest=BASELINE_DIGEST if evidence_class == 'SUPER_REVIEW_INDEPENDENT' else None,
            environment_digest=ENV_DIGEST,
            result='PASS' if record['status'] == 'PASS' else 'NOT_RUN',
            procedure='Synthetic protocol evidence fixture.',
            artifact_digest=None,
        ))
        declared = {criterion['id']: criterion for criterion in tasks[record['task_id']]['acceptance']}
        record['acceptance_results'] = [
            dict(
                criterion_id=cid,
                required=declared[cid]['required'],
                result='PASS' if record['status'] == 'PASS' else 'NOT_RUN',
                verification_method_ids=list(declared[cid]['verification_method_ids']),
                evidence_ids=[evidence_id],
            )
            for cid in checked
        ]
        record['acceptance_surface'] = (
            dict(
                project_protocol_digest=PROJECT_DIGEST,
                harness_digest=HARNESS_DIGEST,
                baseline_digest=BASELINE_DIGEST,
                oracle_digests=[ORACLE_DIGEST],
                mutation_detected=False,
                digest=SURFACE_DIGEST,
            )
            if record['stage'] in ['REVIEWER', 'COORDINATOR', 'PARENT_CHECK']
            else None
        )
        record['production_output'] = dict(
            deliverables=['Synthetic ' + record['stage'] + ' production output'],
            coverage_completed=checked,
            fixes_applied=[],
            regressions_added=[],
            education_points=['Synthetic forward handoff explains evidence and downstream invariant.'],
            unresolved_internal_defects=[],
            internal_fixable_defects_remaining=0,
            blocking_class='NONE',
            coverage_complete_for_stage=record['status'] == 'PASS',
            early_termination=False,
            early_termination_reason=None,
        )
        record['carried_findings'] = []
        record['external_gate_results'] = []
        record['freshness'] = dict(
            common_protocol_current=True,
            project_protocol_current=True,
            spec_current=True,
            parent_context_current=True,
            child_context_current=True,
            pr_description_current=True,
            acceptance_surface_current=True,
            environment_current=True,
            dependencies_current=True,
        )

        start_ref = 'CTX-START-' + record['record_id']
        record['context_start_ref'] = start_ref
        support['context_snapshots'].append(dict(
            snapshot_id=start_ref,
            task_id=record['task_id'],
            phase='START',
            observed_at=record['started_at'],
            parent_issue_digest=PARENT_CONTEXT_DIGEST,
            parent_comment_frontier=record['parent_context']['through_comment_ref'],
            parent_frontier_digest=PARENT_CONTEXT_DIGEST,
            child_issue_digest=CHILD_CONTEXT_DIGEST,
            child_comment_frontier=record['handover']['child_comment_ref'],
            pr_description_digest=PR_DESCRIPTION_DIGEST,
            pr_comment_frontier=record['handover']['pr_description_ref'],
            owner_control_digest=OWNER_CONTROL_DIGEST,
            reconciled=True,
            reconciliation_note='Synthetic START context fully reconciled.',
        ))

        is_pass = record['status'] == 'PASS'
        if is_pass:
            pre_ref = 'CTX-PRE-' + record['record_id']
            record['context_pre_verdict_ref'] = pre_ref
            support['context_snapshots'].append(dict(
                snapshot_id=pre_ref,
                task_id=record['task_id'],
                phase='PRE_VERDICT',
                observed_at=record['work_periods'][-1]['end'],
                parent_issue_digest=PARENT_CONTEXT_DIGEST,
                parent_comment_frontier=record['parent_context']['through_comment_ref'],
                parent_frontier_digest=PARENT_CONTEXT_DIGEST,
                child_issue_digest=CHILD_CONTEXT_DIGEST,
                child_comment_frontier=record['handover']['child_comment_ref'],
                pr_description_digest=PR_DESCRIPTION_DIGEST,
                pr_comment_frontier=record['handover']['pr_description_ref'],
                owner_control_digest=OWNER_CONTROL_DIGEST,
                reconciled=True,
                reconciliation_note='Synthetic PRE_VERDICT context fully reconciled.',
            ))
            record['source_attestation'] = dict(
                candidate_sha=record['validated_sha'],
                base_sha=record['base_sha'],
                merge_base_sha=record['base_sha'],
                integration_tree_digest=TREE_DIGEST,
                workspace_digest=WORKSPACE_DIGEST,
                unrecorded_changes=False,
            )
        else:
            record['context_pre_verdict_ref'] = None
            record['source_attestation'] = None

        if is_pass and record['stage'] in ['REVIEWER', 'COORDINATOR', 'PARENT_CHECK']:
            lease_ref = 'LEASE-' + record['record_id']
            record['review_lease_ref'] = lease_ref
            support['review_leases'].append(dict(
                lease_id=lease_ref,
                task_id=record['task_id'],
                stage_record_id=record['record_id'],
                candidate_sha=record['validated_sha'],
                base_sha=record['base_sha'],
                merge_base_sha=record['base_sha'],
                integration_tree_digest=TREE_DIGEST,
                common_protocol_ref=tasks[record['task_id']]['protocol_ref'],
                common_protocol_digest=COMMON_DIGEST,
                project_protocol_digest=PROJECT_DIGEST,
                spec_digest=record['spec_digest'],
                parent_spec_digest=record['parent_spec_digest'],
                parent_context_digest=PARENT_CONTEXT_DIGEST,
                child_context_digest=CHILD_CONTEXT_DIGEST,
                pr_description_digest=PR_DESCRIPTION_DIGEST,
                required_check_policy_digest=POLICY_DIGEST,
                acceptance_surface_digest=SURFACE_DIGEST,
                environment_digest=ENV_DIGEST,
                dependency_heads=[],
                owner_control_digest=OWNER_CONTROL_DIGEST,
                sealed_at=record['work_periods'][-1]['end'],
                environment_ref=record['environment_ref'],
                context_pre_verdict_ref=record['context_pre_verdict_ref'],
            ))
        else:
            record['review_lease_ref'] = None

    bundle['observed'].setdefault('dependency_heads', {})
    bundle['observed'].setdefault('canonical_main_observations', {})
    child_tasks = [task for task in bundle['tasks'] if task['kind'] == 'CHILD' and task.get('pr') is not None]
    for task in child_tasks:
        final = next((record for record in reversed(bundle['stages']) if record['task_id'] == task['task_id'] and record['stage'] == 'COORDINATOR' and record['status'] == 'PASS'), None)
        if not final:
            continue
        pre_merge_ref = 'CTX-PREMERGE-' + task['task_id']
        support['context_snapshots'].append(dict(
            snapshot_id=pre_merge_ref,
            task_id=task['task_id'],
            phase='PRE_MERGE',
            observed_at='2026-10-04T00:03:00Z',
            parent_issue_digest=PARENT_CONTEXT_DIGEST,
            parent_comment_frontier=final['parent_context']['through_comment_ref'],
            parent_frontier_digest=PARENT_CONTEXT_DIGEST,
            child_issue_digest=CHILD_CONTEXT_DIGEST,
            child_comment_frontier=final['handover']['child_comment_ref'],
            pr_description_digest=PR_DESCRIPTION_DIGEST,
            pr_comment_frontier=final['handover']['pr_description_ref'],
            owner_control_digest=OWNER_CONTROL_DIGEST,
            reconciled=True,
            reconciliation_note='Synthetic PRE_MERGE context fully reconciled.',
        ))
        state_ref = 'OBS-' + task['task_id']
        support['observed_states'].append(dict(
            state_id=state_ref,
            task_id=task['task_id'],
            pr=task['pr'],
            project_protocol_digest=PROJECT_DIGEST,
            pre_merge_context_ref=pre_merge_ref,
            observed_at='2026-10-04T00:03:00Z',
            pr_head_sha=final['validated_sha'],
            base_sha=final['base_sha'],
            merge_base_sha=final['base_sha'],
            integration_tree_digest=TREE_DIGEST,
            repository_policy_digest=POLICY_DIGEST,
            common_protocol_digest=COMMON_DIGEST,
            environment_digest=ENV_DIGEST,
            workspace_digest=WORKSPACE_DIGEST,
            parent_context_digest=PARENT_CONTEXT_DIGEST,
            child_context_digest=CHILD_CONTEXT_DIGEST,
            pr_description_digest=PR_DESCRIPTION_DIGEST,
            owner_control_digest=OWNER_CONTROL_DIGEST,
            required_checks=[
                dict(
                    check=contract['check'],
                    provider=contract['provider'],
                    workflow_digest=contract['workflow_digest'],
                    workflow_path=contract['workflow_path'],
                    app_identity=contract['expected_app'],
                    run_id='RUN-' + task['task_id'],
                    job_id='JOB-' + task['task_id'],
                    artifact_digests=[ARTIFACT_DIGEST],
                    head_sha=final['validated_sha'],
                    result='PASS',
                    mandatory_steps_executed=True,
                )
                for contract in task['required_check_contracts']
            ],
        ))

    for result in bundle['results']:
        result['version'] = '1.1'
        result.setdefault('waiver_refs', [])
        task = tasks[result['task_id']]
        if result['kind'] == 'CHILD':
            final = next(record for record in bundle['stages'] if record['record_id'] == result['final_record'])
            result['review_lease_ref'] = final['review_lease_ref']
            result['pre_merge_context_ref'] = 'CTX-PREMERGE-' + task['task_id']
            result['observed_state_ref'] = 'OBS-' + task['task_id']
            result['canonical_observation'] = dict(
                main_sha=result['merge_commit_sha'],
                observed_at='2026-10-04T00:04:30Z',
                integrates_reviewed_candidate=True,
                provider_ref='Synthetic canonical main observation',
            )
            bundle['observed']['canonical_main_observations'][str(result['pr'])] = copy.deepcopy(result['canonical_observation'])
        else:
            result['review_lease_ref'] = None
            result['pre_merge_context_ref'] = None
            result['observed_state_ref'] = None
            result['canonical_observation'] = None
    return bundle

def command(name, target='ALL', child=None, issued='2026-10-04T00:10:00Z', minutes=None, identifier='CMD1'):
    return dict(id=identifier, command=name, target=target, child_issue=child, issued_at=issued, instruction_ref='Synthetic human instruction reference', reason='Synthetic command behavior test', minutes=minutes, owner_principal='owner', source_kind='DIRECT_OWNER_SESSION', source_digest='f' * 64, authentication_status='AUTHENTICATED')


def example_bundle():
    common = dict(record='TASK', version='1.1', repository='exampleowner/editor', parent_owner='coordinator', spec_ref='https://example.invalid/issues/85', spec_digest=DIGEST, required_checks=['Required hosted check'], protocol_ref='exampleowner/Common@' + 'a' * 40 + ':skills/Local_PR_Deliverty_v1.1')
    parent = dict(common, task_id='T85', kind='PARENT', issue=85, parent_issue=None, pr=None, scope='Deliver child and prove integrated parent outcome.', acceptance=[dict(id='P1', requirement='Child capability works in integrated product.', required=True)], children=[dict(issue=86, scope='Native parser foundation.', covers=['P1'], depends_on=[])], workspace=FOLDER, timers=dict(poll_seconds=60, stage_minutes=dict(checker.DEFAULT_BUDGETS), ci_wait_minutes=30, recovery_grace_minutes=5, handover_seconds=0, override_reason=None), owner_commands=[], start_permissions=[dict(id='PERMIT86', child_issue=86, issued_at='2026-10-04T00:00:00Z', coordinator='coordinator', parent_comment_ref='https://example.invalid/issues/85#permission86', reason='Ready independent child', during_record=None, reviewed_head_sha=None, mode='SERIAL', revoked_at=None)], merge_authority=dict(mode='OWNER_ONLY', reference=None))
    child = dict(common, task_id='T86', kind='CHILD', issue=86, parent_issue=85, pr=101, scope='Deliver native parser foundation.', acceptance=[dict(id='A1', requirement='Preserve native source structure.', required=True)], children=[])
    parent['required_checks'] = list(parent['required_checks'])
    child['required_checks'] = list(child['required_checks'])
    handover = dict(pr_description_ref='https://example.invalid/pull/101', child_comment_ref='https://example.invalid/issues/86#comment', parent_comment_ref='https://example.invalid/issues/85#comment', changed_files=['src/parser.py'], workspace_notes='No unrecorded work; synthetic example.', reconciliation='Read parent/child comments and PR description; inspect actual current files, no diff-based reconstruction.')
    stages = []
    for index, (stage, executor) in enumerate(zip(checker.ORDER, ['coder', 'reviewer', 'coordinator'])):
        start, end = f'2026-10-04T00:0{index}:00Z', f'2026-10-04T00:0{index}:30Z'
        stages.append(dict(record='STAGE_RECORD', version='1.1', record_id='S' + str(index + 1), task_id='T86', stage=stage, attempt=1, executor=executor, previous_record=stages[-1]['record_id'] if stages else None, started_at=start, work_periods=[dict(start=start, end=end)], status='PASS', input_sha=BASE if index == 0 else HEADS[index - 1], output_sha=HEADS[index], validated_sha=HEADS[index], base_sha=BASE, spec_digest=DIGEST, parent_spec_digest=DIGEST, workspace=FOLDER, handover=copy.deepcopy(handover), acceptance_checked=['A1'], findings=[], validation=[dict(check='Synthetic behavior observation', required=True, result='PASS', evidence='Synthetic fixture; no real product test claimed.')], changes='Bounded correction; retained earlier claims checked by Coordinator.', repeat_stages=[], writer_stopped=True, next_action='Handover to eligible role.', ci_wait_started_at=None, stalled_at=None))
    stages.append(dict(stages[-1], record_id='S4', task_id='T85', stage='PARENT_CHECK', previous_record=None, input_sha=MERGE, output_sha=MERGE, validated_sha=MERGE, base_sha=MERGE, acceptance_checked=['P1'], started_at='2026-10-04T00:06:00Z', work_periods=[dict(start='2026-10-04T00:06:00Z', end='2026-10-04T00:06:30Z')]))
    child_result = dict(record='DELIVERY_RESULT', version='1.1', record_id='D86', task_id='T86', kind='CHILD', final_record='S3', head_sha=HEADS[2], pr=101, merge_commit_sha=MERGE, accepted_ids=['A1'], remaining_ids=[], responsibility_complete=True, child_results=[], parent_comment_ref='https://example.invalid/issues/85#delivery86', evidence='Synthetic provider merge and acceptance.', recorded_at='2026-10-04T00:05:00Z')
    parent_result = dict(child_result, parent_comment_ref='https://example.invalid/issues/85#delivery85', record_id='D85', task_id='T85', kind='PARENT', final_record='S4', head_sha=MERGE, pr=None, merge_commit_sha=None, accepted_ids=['P1'], child_results=['D86'], recorded_at='2026-10-04T00:07:00Z')
    for record in stages:
        record_id = record['record_id']
        record['publications'] = dict(start=dict(comment_ref=f'https://example.invalid/issues/85#start-{record_id}', published_at=record['started_at'], summary='Synthetic role start, intended scope and validation.'), end=dict(comment_ref=f'https://example.invalid/issues/85#end-{record_id}', published_at=record['work_periods'][0]['end'], summary='Synthetic findings, output evidence and next eligible role.'))
        record['parent_context'] = dict(read_at=record['started_at'], through_comment_ref=f'https://example.invalid/issues/85#before-{record_id}', reconciled_points=['Read and reconcile complete prior parent history and active controls.'])
        record['workspace_mode'] = 'WRITE'
        record['review_source'] = None
    observed = dict(main_sha=MERGE, pr_heads={'101': HEADS[2]}, spec_digests={'T85': DIGEST, 'T86': DIGEST}, workspace=dict(path=FOLDER, head_sha=HEADS[2], unrecorded_changes=False), merged={'101': dict(head_sha=HEADS[2], merge_commit_sha=MERGE, merged_at='2026-10-04T00:04:00Z')}, checks={'101': [dict(check='Required hosted check', head_sha=HEADS[2], result='PASS')]}, merge_authority_refs={'101': 'Synthetic owner authorization reference'}, external_writer_stopped=True)
    observed['parent_comment_frontiers'] = {r['record_id']: dict(comment_ref=r['parent_context']['through_comment_ref'], observed_at=r['started_at']) for r in stages}
    observed['issue_states'] = {'85': 'CLOSED', '86': 'CLOSED'}
    observed['pr_states'] = {'101': 'MERGED'}
    return enrich_v11(dict(tasks=[parent, child], stages=stages, results=[child_result, parent_result], observed=observed))


def premerge_bundle():
    bundle = example_bundle()
    bundle['stages'] = bundle['stages'][:3]
    bundle['results'] = []
    bundle['observed']['main_sha'] = BASE
    bundle['observed']['merged'] = {}
    bundle['observed']['pr_states']['101'] = 'DRAFT'
    bundle['observed']['issue_states'] = {'85': 'OPEN', '86': 'OPEN'}
    return bundle


def running_bundle():
    bundle = premerge_bundle()
    bundle['stages'] = bundle['stages'][:1]
    bundle['stages'][0].update(status='RUNNING', output_sha=None, validated_sha=None, acceptance_checked=[], validation=[], writer_stopped=False)
    bundle['stages'][0]['work_periods'][0]['end'] = None
    bundle['stages'][0]['publications']['end'] = None
    return bundle


class ProtocolTests(unittest.TestCase):
    def rejected(self, bundle, now='2026-10-04T00:08:00Z'):
        with self.assertRaises(checker.RecordError):
            checker.validate_bundle(bundle, now)

    def state(self, bundle, now='2026-10-04T00:08:00Z'):
        return checker.validate_bundle(bundle, now)['issues']['86']['status']

    def test_cold_reconstruction_complete_without_git(self):
        state = checker.validate_bundle(json.loads(json.dumps(example_bundle())), '2026-10-04T00:08:00Z')
        self.assertEqual(state['issues']['85']['status'], 'COMPLETE')
        self.assertEqual(state['issues']['86']['status'], 'COMPLETE')

    def test_three_named_roles_and_merge_ready(self):
        self.assertEqual(checker.ORDER, ['CODER', 'REVIEWER', 'COORDINATOR'])
        self.assertEqual(self.state(premerge_bundle()), 'MERGE_READY')

    def test_partial_child_does_not_complete_parent(self):
        bundle = example_bundle()
        bundle['tasks'][1]['acceptance'].append(dict(id='A2', requirement='Follow-up remains declared.', required=False, verification_method_ids=['VM-A2'], super_review_required=False))
        enrich_v11(bundle)
        bundle['stages'] = bundle['stages'][:3]
        bundle['results'] = bundle['results'][:1]
        bundle['results'][0].update(remaining_ids=['A2'], responsibility_complete=False)
        self.assertEqual(self.state(bundle), 'MERGED')
        self.assertNotEqual(checker.validate_bundle(bundle)['issues']['85']['status'], 'COMPLETE')

    def test_child_merge_does_not_replace_parent_check(self):
        bundle = example_bundle()
        bundle['stages'] = bundle['stages'][:3]
        bundle['results'] = bundle['results'][:1]
        self.assertEqual({k: checker.validate_bundle(bundle)['issues']['85'][k] for k in ['stage','status']}, {'stage': 'PARENT_CHECK', 'status': 'READY'})

    def test_unvalidated_output_rejected(self):
        bundle = example_bundle()
        bundle['stages'][1]['validated_sha'] = HEADS[4]
        self.rejected(bundle)

    def test_required_not_run_rejected(self):
        bundle = example_bundle()
        bundle['stages'][1]['validation'][0]['result'] = 'NOT_RUN'
        self.rejected(bundle)

    def test_missing_acceptance_coverage_rejected(self):
        bundle = example_bundle()
        bundle['stages'][1]['acceptance_checked'] = []
        self.rejected(bundle)

    def test_open_finding_rejected(self):
        bundle = example_bundle()
        bundle['stages'][1]['findings'] = [dict(id='F1', problem='Unresolved defect', status='OPEN', resolution=None)]
        self.rejected(bundle)

    def test_stale_head_base_or_spec_requires_rework(self):
        for field, key, value in [('pr_heads', '101', HEADS[4]), ('spec_digests', 'T86', 'e' * 64), ('spec_digests', 'T85', 'e' * 64), (None, 'main_sha', MERGE)]:
            bundle = premerge_bundle()
            target = bundle['observed'][field] if field else bundle['observed']
            target[key] = value
            self.assertEqual(self.state(bundle), 'REWORK')

    def test_pending_checks_and_missing_authority_are_distinct(self):
        bundle = premerge_bundle()
        bundle['observed']['checks'] = {}
        pending = checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']
        self.assertEqual((pending['status'], pending['engineering_approved'], pending['merge_ready']), ('WAITING_CI', False, False))

        bundle = premerge_bundle()
        bundle['observed']['merge_authority_refs'] = {}
        owner_wait = checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']
        self.assertEqual((owner_wait['status'], owner_wait['engineering_approved'], owner_wait['merge_ready']), ('WAITING_OWNER', True, False))

        ready = checker.validate_bundle(premerge_bundle(), '2026-10-04T00:08:00Z')['issues']['86']
        self.assertEqual((ready['status'], ready['engineering_approved'], ready['merge_ready']), ('MERGE_READY', True, True))

    def test_fifteen_coder_minutes_stalls_never_passes(self):
        self.assertEqual(self.state(running_bundle(), '2026-10-04T00:14:59Z'), 'RUNNING')
        self.assertEqual(self.state(running_bundle(), '2026-10-04T00:15:00Z'), 'STALLED')

    def test_recovery_grace_follows_actual_stall_detection(self):
        bundle = running_bundle()
        bundle['stages'][0].update(status='STALLED', stalled_at='2026-10-04T00:31:00Z')
        self.assertEqual(self.state(bundle, '2026-10-04T00:37:00Z'), 'BLOCKED')

    def test_ci_wait_thirty_minutes_blocks(self):
        bundle = running_bundle()
        bundle['stages'][0].update(status='WAITING_CI', ci_wait_started_at='2026-10-04T00:00:00Z')
        self.assertEqual(self.state(bundle, '2026-10-04T00:30:00Z'), 'BLOCKED')

    def test_unstopped_writer_cannot_hand_over(self):
        bundle = premerge_bundle()
        bundle['stages'][0].update(status='STALLED', stalled_at='2026-10-04T00:00:00Z', writer_stopped=False)
        self.rejected(bundle)

    def test_concurrent_writers_rejected(self):
        bundle = running_bundle()
        child = copy.deepcopy(bundle['tasks'][1])
        child.update(task_id='T87', issue=87, pr=102)
        bundle['tasks'].append(child)
        bundle['tasks'][0]['children'].append(dict(issue=87, scope=child['scope'], covers=['P1'], depends_on=[]))
        bundle['stages'].append(dict(bundle['stages'][0], record_id='S87', task_id='T87', executor='other-coder'))
        self.rejected(bundle)

    def test_skipped_reviewer_rejected(self):
        bundle = premerge_bundle()
        bundle['stages'].pop(1)
        bundle['stages'][1].update(previous_record='S1', input_sha=HEADS[0])
        self.rejected(bundle)

    def test_distinct_role_identities(self):
        bundle = example_bundle()
        bundle['stages'][1]['executor'] = 'coder'
        self.rejected(bundle)

    def test_coordinator_is_parent_owner(self):
        bundle = example_bundle()
        bundle['stages'][2]['executor'] = 'other-coordinator'
        self.rejected(bundle)

    def test_coordinator_cannot_route_back_to_reviewer(self):
        bundle = premerge_bundle()
        bundle['stages'][-1]['repeat_stages'] = ['REVIEWER']
        self.rejected(bundle)

    def test_unknown_fields_duplicate_ids_and_unobserved_merge_rejected(self):
        bundle = example_bundle()
        bundle['tasks'][0]['guess_completion'] = True
        self.rejected(bundle)
        bundle = example_bundle()
        bundle['stages'][1]['record_id'] = 'S1'
        self.rejected(bundle)
        bundle = example_bundle()
        bundle['observed']['merged'] = {}
        self.rejected(bundle)

    def test_parent_cannot_ignore_declared_child(self):
        bundle = example_bundle()
        bundle['tasks'][0]['children'].append(dict(issue=87, scope='Another deliverable', covers=['P1'], depends_on=[]))
        self.rejected(bundle)

    def test_dependency_cycle_rejected(self):
        bundle = example_bundle()
        bundle['tasks'][0]['children'][0]['depends_on'] = [87]
        bundle['tasks'][0]['children'].append(dict(issue=87, scope='Another deliverable', covers=['P1'], depends_on=[86]))
        self.rejected(bundle)

    def test_dependency_start_must_follow_delivery(self):
        bundle = example_bundle()
        bundle['stages'] = bundle['stages'][:3]
        bundle['results'] = bundle['results'][:1]
        child = copy.deepcopy(bundle['tasks'][1])
        child.update(task_id='T87', issue=87, pr=102)
        bundle['tasks'].append(child)
        bundle['tasks'][0]['children'].append(dict(issue=87, scope=child['scope'], covers=['P1'], depends_on=[86]))
        bundle['stages'].append(dict(bundle['stages'][0], record_id='S87', task_id='T87', executor='new-coder', status='RUNNING', output_sha=None, validated_sha=None, writer_stopped=False))
        self.rejected(bundle)

    def test_omitted_required_check_never_merge_ready(self):
        bundle = premerge_bundle()
        bundle['tasks'][1]['required_checks'].append('Second required check')
        bundle['tasks'][1]['required_check_contracts'].append(dict(check='Second required check', provider='GITHUB_ACTIONS', workflow_digest=WORKFLOW_DIGEST, policy_source=POLICY_SOURCE, workflow_path=WORKFLOW_PATH, expected_app=EXPECTED_APP))
        self.assertEqual(self.state(bundle), 'WAITING_CI')

    def test_final_ci_failure_and_timeout_block(self):
        bundle = premerge_bundle()
        bundle['observed']['checks']['101'][0]['result'] = 'FAIL'
        self.assertEqual(self.state(bundle), 'BLOCKED')
        bundle = premerge_bundle()
        bundle['observed']['checks']['101'][0]['result'] = 'PENDING'
        bundle['observed']['ci_wait_started_at'] = {'101': '2026-10-04T00:00:00Z'}
        self.assertEqual(self.state(bundle, '2026-10-04T00:30:00Z'), 'BLOCKED')

    def test_declared_no_ci_does_not_invent_gate(self):
        bundle = premerge_bundle()
        bundle['tasks'][1]['required_checks'] = []
        bundle['tasks'][1]['required_check_contracts'] = []
        bundle['observed']['checks']['101'] = []
        self.assertEqual(self.state(bundle), 'MERGE_READY')

    def test_timer_override_needs_reason(self):
        bundle = example_bundle()
        bundle['tasks'][0]['timers']['stage_minutes']['CODER'] = 90
        self.rejected(bundle)

    def test_same_folder_and_unrecorded_work_guards(self):
        bundle = example_bundle()
        bundle['stages'][1]['workspace'] = r'C:\OtherFolder'
        self.rejected(bundle)
        bundle = premerge_bundle()
        bundle['observed']['workspace']['unrecorded_changes'] = True
        self.assertEqual(self.state(bundle), 'REWORK')

    def test_handover_needs_pr_and_issue_anchors(self):
        bundle = example_bundle()
        del bundle['stages'][1]['handover']['parent_comment_ref']
        self.rejected(bundle)

    def test_hold_coder_requires_ack_then_freezes_timer(self):
        bundle = running_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', target='CODER')]
        self.assertEqual(self.state(bundle, '2026-10-04T04:00:00Z'), 'HOLD_REQUESTED')
        bundle['stages'][0].update(status='HELD', writer_stopped=True)
        bundle['stages'][0]['work_periods'][0]['end'] = '2026-10-04T00:10:05Z'
        bundle['stages'][0]['publications']['end'] = dict(comment_ref='https://example.invalid/issues/85#hold-end', published_at='2026-10-04T00:10:05Z', summary='Hold acknowledgement.')
        self.assertEqual(self.state(bundle, '2026-10-04T04:00:00Z'), 'HELD')
        self.assertEqual(checker.active_seconds(bundle['stages'][0], bundle['tasks'][0]['owner_commands'], bundle['tasks'][1], checker.instant('2026-10-04T04:00:00Z')), 600)

    def test_hold_or_pause_blocks_otherwise_ready_merge(self):
        for name, marker in [('HOLD', 'HELD'), ('PAUSE', 'PAUSED'), ('STOP', 'STOPPED')]:
            bundle = premerge_bundle()
            bundle['tasks'][0]['owner_commands'] = [command(name, issued='2026-10-04T00:03:00Z')]
            self.assertEqual(self.state(bundle), marker)

    def test_targeted_resume_does_not_clear_all_hold(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:03:00Z'), command('RESUME', target='CODER', issued='2026-10-04T00:04:00Z', identifier='CMD2')]
        self.assertEqual(self.state(bundle), 'HELD')

    def test_status_and_timer_cannot_release_hold(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:03:00Z'), command('STATUS', issued='2026-10-04T00:04:00Z', identifier='CMD2'), command('TIMER', issued='2026-10-04T00:05:00Z', identifier='CMD3', minutes=30)]
        self.assertEqual(self.state(bundle), 'HELD')

    def test_new_stage_cannot_start_under_hold(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:00:45Z')]
        self.rejected(bundle)

    def test_merge_observed_under_hold_rejected(self):
        bundle = example_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:03:00Z')]
        self.rejected(bundle)

    def test_coder_hold_does_not_impersonate_coordinator_hold(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', target='CODER', issued='2026-10-04T00:03:00Z')]
        self.assertEqual(self.state(bundle), 'MERGE_READY')

    def test_resume_requires_fresh_attempt_and_cloud_writer_stop(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('PAUSE', issued='2026-10-04T00:03:00Z'), command('RESUME', issued='2026-10-04T00:04:00Z', identifier='CMD2')]
        self.assertEqual(self.state(bundle), 'REWORK')
        bundle['observed']['external_writer_stopped'] = False
        self.assertEqual(self.state(bundle), 'BLOCKED')

    def test_resume_held_coder_requests_new_reconciled_attempt(self):
        bundle = running_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', target='CODER', issued='2026-10-04T00:01:00Z'), command('RESUME', target='CODER', issued='2026-10-04T00:03:00Z', identifier='CMD2')]
        bundle['stages'][0].update(status='HELD', writer_stopped=True)
        bundle['stages'][0]['work_periods'][0]['end'] = '2026-10-04T00:01:05Z'
        bundle['stages'][0]['publications']['end'] = dict(comment_ref='https://example.invalid/issues/85#hold-end', published_at='2026-10-04T00:01:05Z', summary='Hold acknowledgement.')
        self.assertEqual(self.state(bundle), 'READY')

    def test_downstream_stage_cannot_reopen_prior_stage(self):
        bundle = premerge_bundle()
        bundle['stages'][2]['repeat_stages'] = ['REVIEWER']
        self.rejected(bundle)

    def test_historical_overlapping_writers_rejected(self):
        bundle = example_bundle()
        bundle['stages'][1]['started_at'] = '2026-10-04T00:00:15Z'
        bundle['stages'][1]['work_periods'][0]['start'] = '2026-10-04T00:00:15Z'
        self.rejected(bundle)

    def test_delivered_history_is_preserved_after_later_resume(self):
        bundle = example_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:08:00Z'), command('RESUME', issued='2026-10-04T00:09:00Z', identifier='CMD2')]
        self.assertEqual(self.state(bundle, '2026-10-04T00:10:00Z'), 'COMPLETE')

    def test_coordinator_hold_applies_to_parent_check(self):
        bundle = example_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', target='COORDINATOR', issued='2026-10-04T00:05:30Z')]
        self.rejected(bundle)

    def test_child_hold_does_not_hold_other_child_or_parent(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', child=86, issued='2026-10-04T00:03:00Z')]
        result = checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')
        self.assertEqual(result['issues']['86']['status'], 'HELD')
        self.assertEqual(result['issues']['85']['status'], 'READY')

    def test_future_or_unordered_owner_commands_rejected(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD')]
        self.rejected(bundle)
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:05:00Z'), command('RESUME', issued='2026-10-04T00:04:00Z', identifier='CMD2')]
        self.rejected(bundle)

class ProductionStageV11Tests(unittest.TestCase):
    def rejected(self, bundle):
        with self.assertRaises(checker.RecordError):
            checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')

    def test_reviewer_product_fix_flows_forward(self):
        bundle = premerge_bundle()
        self.assertNotEqual(bundle['stages'][0]['output_sha'], bundle['stages'][1]['output_sha'])
        state = checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']
        self.assertEqual((state['stage'], state['status']), ('DELIVERY', 'MERGE_READY'))

    def test_super_reviewer_product_fix_does_not_reopen_reviewer(self):
        bundle = premerge_bundle()
        self.assertNotEqual(bundle['stages'][1]['output_sha'], bundle['stages'][2]['output_sha'])
        state = checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']
        self.assertEqual(state['status'], 'MERGE_READY')

    def test_super_review_acceptance_surface_mutation_rejected(self):
        bundle = premerge_bundle()
        bundle['stages'][2]['acceptance_surface']['mutation_detected'] = True
        self.rejected(bundle)

    def test_super_review_project_protocol_digest_mismatch_rejected(self):
        bundle = premerge_bundle()
        bundle['stages'][2]['acceptance_surface']['project_protocol_digest'] = '3' * 64
        self.rejected(bundle)

    def test_pass_cannot_push_fixable_defect_downstream(self):
        bundle = premerge_bundle()
        bundle['stages'][1]['production_output']['internal_fixable_defects_remaining'] = 1
        bundle['stages'][1]['production_output']['unresolved_internal_defects'] = ['F-UNFINISHED']
        self.rejected(bundle)

    def test_super_review_required_criterion_needs_independent_evidence(self):
        bundle = premerge_bundle()
        bundle['stages'][2]['evidence_manifest'][0]['class'] = 'AUTHOR'
        self.rejected(bundle)

class TrustGraphV11Tests(unittest.TestCase):
    def rejected(self, bundle):
        with self.assertRaises(checker.RecordError):
            checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')

    def test_stale_review_lease_candidate_rejected(self):
        bundle = premerge_bundle()
        lease_id = bundle['stages'][2]['review_lease_ref']
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == lease_id)
        lease['candidate_sha'] = HEADS[4]
        self.rejected(bundle)

    def test_stale_pre_verdict_context_rejected(self):
        bundle = premerge_bundle()
        lease_id = bundle['stages'][2]['review_lease_ref']
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == lease_id)
        lease['parent_context_digest'] = '0' * 64
        self.rejected(bundle)

    def test_environment_drift_rejected(self):
        bundle = premerge_bundle()
        environment_id = bundle['stages'][2]['environment_ref']
        environment = next(item for item in bundle['support']['environments'] if item['environment_id'] == environment_id)
        environment['digest'] = '0' * 64
        self.rejected(bundle)

    def test_skipped_mandatory_ci_step_rejected(self):
        bundle = premerge_bundle()
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['required_checks'][0]['mandatory_steps_executed'] = False
        self.rejected(bundle)

    def test_wrong_repository_policy_digest_rejected(self):
        bundle = premerge_bundle()
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['repository_policy_digest'] = '0' * 64
        self.rejected(bundle)

    def test_unauthorized_owner_principal_rejected(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:03:00Z')]
        bundle['tasks'][0]['owner_commands'][0]['owner_principal'] = 'not-an-owner'
        self.rejected(bundle)

    def test_waiver_is_bound_and_never_result_override(self):
        bundle = premerge_bundle()
        task = bundle['tasks'][1]
        task['waivable_criteria'] = ['A1']
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == bundle['stages'][2]['review_lease_ref'])
        bundle['support']['waivers'] = [dict(
            waiver_id='W1',
            task_id='T86',
            target_kind='CRITERION',
            target_id='A1',
            lease_id=lease['lease_id'],
            candidate_sha=lease['candidate_sha'],
            owner_principal='owner',
            authority_ref='Synthetic Owner waiver',
            reason='Synthetic risk acceptance',
            risk='Synthetic residual risk',
            compensating_controls=['Synthetic compensating control'],
            issued_at='2026-10-04T00:03:00Z',
            expires_at='2026-10-04T01:00:00Z',
            non_transitive=True,
            result_override=False,
        )]
        checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')
        bundle['support']['waivers'][0]['result_override'] = True
        self.rejected(bundle)


    def test_unauthorized_reviewer_principal_rejected(self):
        bundle = premerge_bundle()
        reviewer = bundle['stages'][1]
        reviewer['executor'] = 'intruder'
        reviewer['role_integrity']['principal'] = 'intruder'
        self.rejected(bundle)

    def test_unverified_owner_command_rejected(self):
        bundle = premerge_bundle()
        cmd = command('HOLD', issued='2026-10-04T00:03:00Z')
        cmd['source_kind'] = 'UNVERIFIED'
        cmd['authentication_status'] = 'UNVERIFIED'
        bundle['tasks'][0]['owner_commands'] = [cmd]
        self.rejected(bundle)

    def test_evidence_provenance_mismatch_rejected(self):
        bundle = premerge_bundle()
        evidence_id = bundle['stages'][2]['evidence_refs'][0]
        provenance = next(item for item in bundle['support']['evidence_records'] if item['evidence_id'] == evidence_id)
        provenance['producer_role'] = 'REVIEWER'
        self.rejected(bundle)

    def test_common_protocol_digest_drift_rejected(self):
        bundle = premerge_bundle()
        bundle['stages'][2]['common_protocol_digest'] = '1' * 64
        self.rejected(bundle)

    def test_merge_base_drift_rejected(self):
        bundle = premerge_bundle()
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['merge_base_sha'] = HEADS[4]
        self.rejected(bundle)

    def test_stacked_dependency_head_movement_expires_latest_lease(self):
        bundle = premerge_bundle()
        upstream = copy.deepcopy(bundle['tasks'][1])
        upstream.update(task_id='T87', issue=87, pr=102, scope='Synthetic stacked upstream')
        upstream['stacked_dependencies'] = []
        bundle['tasks'].append(upstream)
        bundle['tasks'][0]['children'].append(dict(issue=87, scope='Synthetic stacked upstream', covers=['P1'], depends_on=[]))
        bundle['tasks'][1]['stacked_dependencies'] = ['T87']
        bundle['observed']['dependency_heads'] = {'T87': HEADS[0]}
        enrich_v11(bundle)
        bundle['observed']['dependency_heads'] = {'T87': HEADS[0]}
        lease_id = bundle['stages'][2]['review_lease_ref']
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == lease_id)
        lease['dependency_heads'] = [dict(task_id='T87', sha=HEADS[0])]
        checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')
        bundle['observed']['dependency_heads']['T87'] = HEADS[4]
        self.rejected(bundle)

    def test_blocked_cannot_hide_internal_fixable_defect(self):
        bundle = running_bundle()
        record = bundle['stages'][0]
        record['status'] = 'BLOCKED'
        record['production_output']['blocking_class'] = 'EXTERNAL'
        record['production_output']['internal_fixable_defects_remaining'] = 1
        record['production_output']['unresolved_internal_defects'] = ['F-INTERNAL']
        self.rejected(bundle)

    def test_canonical_post_merge_observation_must_match_provider_record(self):
        bundle = example_bundle()
        bundle['results'][0]['canonical_observation']['main_sha'] = HEADS[4]
        self.rejected(bundle)


    def test_task_only_acceptance_criterion_rejected(self):
        bundle = premerge_bundle()
        protocol = bundle['support']['project_protocols'][0]
        protocol['acceptance_sets'][0]['criteria'] = [
            criterion for criterion in protocol['acceptance_sets'][0]['criteria'] if criterion['id'] != 'A1'
        ]
        self.rejected(bundle)

    def test_super_review_criterion_without_project_harness_rejected(self):
        bundle = premerge_bundle()
        protocol = bundle['support']['project_protocols'][0]
        protocol['harnesses'][0]['criteria'] = ['P1']
        self.rejected(bundle)

    def test_ci_app_identity_mismatch_rejected(self):
        bundle = premerge_bundle()
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['required_checks'][0]['app_identity'] = 'unexpected-app'
        self.rejected(bundle)

    def test_ci_workflow_path_mismatch_rejected(self):
        bundle = premerge_bundle()
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['required_checks'][0]['workflow_path'] = '.github/workflows/other.yml'
        self.rejected(bundle)

    def test_pre_merge_context_drift_expires_final_lease(self):
        bundle = premerge_bundle()
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        context = next(item for item in bundle['support']['context_snapshots'] if item['snapshot_id'] == state['pre_merge_context_ref'])
        context['parent_frontier_digest'] = '0' * 64
        self.rejected(bundle)

    def test_authorized_role_sets_must_not_overlap(self):
        bundle = premerge_bundle()
        for task in bundle['tasks']:
            task['role_principals']['REVIEWER'].append('coder')
        self.rejected(bundle)


class WaiverOutcomeV11Tests(unittest.TestCase):
    def rejected(self, bundle):
        with self.assertRaises(checker.RecordError):
            checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')

    def criterion_waiver(self, bundle, waiver_id='W-CRITERION', expires='2026-10-04T01:00:00Z'):
        task = bundle['tasks'][1]
        task['waivable_criteria'] = ['A1']
        final = bundle['stages'][2]
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == final['review_lease_ref'])
        waiver = dict(
            waiver_id=waiver_id,
            task_id='T86',
            target_kind='CRITERION',
            target_id='A1',
            lease_id=lease['lease_id'],
            candidate_sha=lease['candidate_sha'],
            owner_principal='owner',
            authority_ref='Synthetic Owner criterion waiver',
            reason='Required criterion could not be executed in this environment.',
            risk='Residual risk explicitly accepted for this exact candidate.',
            compensating_controls=['Synthetic compensating control'],
            issued_at='2026-10-04T00:02:20Z',
            expires_at=expires,
            non_transitive=True,
            result_override=False,
        )
        bundle['support']['waivers'].append(waiver)
        return waiver

    def check_waiver(self, bundle, waiver_id='W-CHECK', expires='2026-10-04T01:00:00Z'):
        task = bundle['tasks'][1]
        task['waivable_required_checks'] = ['Required hosted check']
        final = bundle['stages'][2]
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == final['review_lease_ref'])
        waiver = dict(
            waiver_id=waiver_id,
            task_id='T86',
            target_kind='REQUIRED_CHECK',
            target_id='Required hosted check',
            lease_id=lease['lease_id'],
            candidate_sha=lease['candidate_sha'],
            owner_principal='owner',
            authority_ref='Synthetic Owner required-check waiver',
            reason='Required hosted check is unavailable for this exact candidate.',
            risk='Residual CI risk explicitly accepted.',
            compensating_controls=['Independent Super Review already passed.'],
            issued_at='2026-10-04T00:02:40Z',
            expires_at=expires,
            non_transitive=True,
            result_override=False,
        )
        bundle['support']['waivers'].append(waiver)
        return waiver

    def test_required_not_run_advances_only_as_approved_with_waiver(self):
        bundle = premerge_bundle()
        waiver = self.criterion_waiver(bundle)
        final = bundle['stages'][2]
        final['status'] = 'APPROVED_WITH_WAIVER'
        final['waiver_refs'] = [waiver['waiver_id']]
        final['acceptance_results'][0]['result'] = 'NOT_RUN'
        final['evidence_manifest'][0]['result'] = 'NOT_RUN'
        evidence_id = final['evidence_refs'][0]
        provenance = next(item for item in bundle['support']['evidence_records'] if item['evidence_id'] == evidence_id)
        provenance['result'] = 'NOT_RUN'
        state = checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']
        self.assertEqual((state['status'], state['engineering_approved']), ('MERGE_READY', True))
        self.assertEqual(final['acceptance_results'][0]['result'], 'NOT_RUN')

    def test_required_not_run_without_waiver_rejected(self):
        bundle = premerge_bundle()
        final = bundle['stages'][2]
        final['status'] = 'APPROVED_WITH_WAIVER'
        final['acceptance_results'][0]['result'] = 'NOT_RUN'
        final['evidence_manifest'][0]['result'] = 'NOT_RUN'
        evidence_id = final['evidence_refs'][0]
        provenance = next(item for item in bundle['support']['evidence_records'] if item['evidence_id'] == evidence_id)
        provenance['result'] = 'NOT_RUN'
        self.rejected(bundle)

    def test_fail_cannot_be_waived(self):
        bundle = premerge_bundle()
        waiver = self.criterion_waiver(bundle)
        final = bundle['stages'][2]
        final['status'] = 'APPROVED_WITH_WAIVER'
        final['waiver_refs'] = [waiver['waiver_id']]
        final['acceptance_results'][0]['result'] = 'FAIL'
        final['evidence_manifest'][0]['result'] = 'FAIL'
        evidence_id = final['evidence_refs'][0]
        provenance = next(item for item in bundle['support']['evidence_records'] if item['evidence_id'] == evidence_id)
        provenance['result'] = 'FAIL'
        self.rejected(bundle)

    def test_required_check_not_run_with_active_waiver_can_be_merge_ready(self):
        bundle = premerge_bundle()
        self.check_waiver(bundle)
        bundle['observed']['checks']['101'][0]['result'] = 'NOT_RUN'
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['required_checks'][0]['result'] = 'NOT_RUN'
        state['required_checks'][0]['mandatory_steps_executed'] = False
        state['required_checks'][0]['run_id'] = None
        state['required_checks'][0]['job_id'] = None
        self.assertEqual(checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']['status'], 'MERGE_READY')

    def test_expired_required_check_waiver_does_not_keep_merge_ready(self):
        bundle = premerge_bundle()
        self.check_waiver(bundle, expires='2026-10-04T00:04:00Z')
        bundle['observed']['checks']['101'][0]['result'] = 'NOT_RUN'
        state = next(item for item in bundle['support']['observed_states'] if item['task_id'] == 'T86')
        state['required_checks'][0]['result'] = 'NOT_RUN'
        state['required_checks'][0]['mandatory_steps_executed'] = False
        state['required_checks'][0]['run_id'] = None
        state['required_checks'][0]['job_id'] = None
        self.assertEqual(checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')['issues']['86']['status'], 'WAITING_OWNER')


class PrincipalAndDependencyV11Tests(unittest.TestCase):
    def rejected(self, bundle):
        with self.assertRaises(checker.RecordError):
            checker.validate_bundle(bundle, '2026-10-04T00:08:00Z')

    def test_role_impersonation_rejected(self):
        bundle = premerge_bundle()
        bundle['stages'][1]['executor'] = 'coder'
        bundle['stages'][1]['role_integrity']['principal'] = 'coder'
        self.rejected(bundle)

    def test_unverified_owner_command_rejected(self):
        bundle = premerge_bundle()
        bundle['tasks'][0]['owner_commands'] = [command('HOLD', issued='2026-10-04T00:03:00Z')]
        bundle['tasks'][0]['owner_commands'][0]['source_kind'] = 'UNVERIFIED'
        bundle['tasks'][0]['owner_commands'][0]['authentication_status'] = 'UNVERIFIED'
        self.rejected(bundle)

    def test_evidence_provenance_mismatch_rejected(self):
        bundle = premerge_bundle()
        evidence_id = bundle['stages'][2]['evidence_refs'][0]
        provenance = next(item for item in bundle['support']['evidence_records'] if item['evidence_id'] == evidence_id)
        provenance['candidate_sha'] = HEADS[4]
        self.rejected(bundle)

    def test_super_review_evidence_cannot_claim_wrong_producer_role(self):
        bundle = premerge_bundle()
        evidence_id = bundle['stages'][2]['evidence_refs'][0]
        provenance = next(item for item in bundle['support']['evidence_records'] if item['evidence_id'] == evidence_id)
        provenance['producer_role'] = 'REVIEWER'
        self.rejected(bundle)

    def test_stacked_dependency_head_drift_rejected(self):
        bundle = premerge_bundle()
        task = bundle['tasks'][1]
        task['stacked_dependencies'] = ['TUPSTREAM']
        upstream = copy.deepcopy(task)
        upstream.update(task_id='TUPSTREAM', issue=87, pr=102, stacked_dependencies=[])
        bundle['tasks'].append(upstream)
        bundle['tasks'][0]['children'].append(dict(issue=87, scope='Synthetic upstream dependency', covers=['P1'], depends_on=[]))
        bundle['observed']['dependency_heads']['TUPSTREAM'] = HEADS[4]
        lease_id = bundle['stages'][2]['review_lease_ref']
        lease = next(item for item in bundle['support']['review_leases'] if item['lease_id'] == lease_id)
        lease['dependency_heads'] = [dict(task_id='TUPSTREAM', sha=HEADS[3])]
        self.rejected(bundle)

    def test_blocked_cannot_hide_internal_fixable_defect(self):
        bundle = running_bundle()
        record = bundle['stages'][0]
        record['status'] = 'BLOCKED'
        record['writer_stopped'] = True
        record['work_periods'][0]['end'] = '2026-10-04T00:00:30Z'
        record['publications']['end'] = dict(
            comment_ref='https://example.invalid/issues/85#blocked-end',
            published_at='2026-10-04T00:00:30Z',
            summary='Synthetic blocked END.',
        )
        record['production_output']['blocking_class'] = 'EXTERNAL'
        record['production_output']['internal_fixable_defects_remaining'] = 1
        record['production_output']['unresolved_internal_defects'] = ['F-INTERNAL']
        self.rejected(bundle)


class SchemaSurfaceV11Tests(unittest.TestCase):
    def test_every_v11_schema_is_valid_draft_2020_12(self):
        from jsonschema import Draft202012Validator
        for schema_path in sorted((ROOT / 'schemas').glob('*.schema.json')):
            with self.subTest(schema=schema_path.name):
                Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding='utf-8')))

    def test_project_protocol_schema_accepts_domain_neutral_contract(self):
        from jsonschema import Draft202012Validator
        schema = json.loads((ROOT / 'schemas' / 'project-protocol.schema.json').read_text(encoding='utf-8'))
        sample = {
            'protocol_id': 'example-project-v1',
            'version': '1.0',
            'repository': 'exampleowner/editor',
            'source_ref': 'exampleowner/editor@' + '9' * 40 + ':review/project-protocol.json',
            'digest': PROJECT_DIGEST,
            'acceptance_sets': [{
                'id': 'A1',
                'criteria': [{
                    'id': 'A1-001',
                    'required': True,
                    'reviewer_check_required': True,
                    'super_review_required': True,
                    'verification_method_ids': ['VM-A1-001'],
                }],
            }],
            'harnesses': [{'id': 'SR-A1', 'criteria': ['A1-001'], 'protected': True}],
            'protected_surface': {
                'harness_digest': HARNESS_DIGEST,
                'baseline_digest': BASELINE_DIGEST,
                'oracle_digests': [ORACLE_DIGEST],
            },
            'external_gates': [],
        }
        errors = list(Draft202012Validator(schema).iter_errors(sample))
        self.assertEqual(errors, [])

if __name__ == '__main__':
    unittest.main()
