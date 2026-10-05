"""Read-only consistency checker for supplied issue/PR records; no Git operations."""
import argparse
import json
from functools import lru_cache
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from pipeline import RecordError, validate_evidence, validate_pipeline, status_details

ROOT = Path(__file__).resolve().parents[1]
ORDER = ['CODER', 'REVIEWER', 'COORDINATOR']
DEFAULT_BUDGETS = {'CODER': 15, 'REVIEWER': 15, 'COORDINATOR': 45, 'PARENT_CHECK': 45}
SCHEMAS = {'TASK': 'task', 'STAGE_RECORD': 'stage-record', 'DELIVERY_RESULT': 'delivery-result'}
SUPPORT_SCHEMAS = {
    'review_leases': ('review-lease', 'lease_id'),
    'environments': ('environment-record', 'environment_id'),
    'context_snapshots': ('context-snapshot', 'snapshot_id'),
    'waivers': ('waiver', 'waiver_id'),
    'observed_states': ('observed-state', 'state_id'),
    'evidence_records': ('evidence-record', 'evidence_id'),
    'project_protocols': ('project-protocol', 'protocol_id'),
}


def require(condition, message):
    if not condition:
        raise RecordError(message)


def instant(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timestamp needs a timezone')
    return parsed.astimezone(timezone.utc)


@lru_cache(maxsize=None)
def schema_validator(schema_name):
    schema = json.loads((ROOT / 'schemas' / (schema_name + '.schema.json')).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_against_schema(record, schema_name):
    require(isinstance(record, dict), 'Each record must be an object')
    errors = sorted(schema_validator(schema_name).iter_errors(record), key=lambda e: str(e.path))
    require(not errors, '; '.join(e.message for e in errors))


def schema_check(record):
    family = record.get('record')
    require(family in SCHEMAS, 'Unknown record family')
    validate_against_schema(record, SCHEMAS[family])


def support_index(bundle):
    support = bundle['support']
    require(isinstance(support, dict) and set(support) == set(SUPPORT_SCHEMAS), 'Support needs review_leases, environments, context_snapshots, waivers, observed_states, evidence_records and project_protocols only')
    indexes = {}
    for key, (schema_name, id_field) in SUPPORT_SCHEMAS.items():
        records = support[key]
        require(isinstance(records, list), key + ' must be an array')
        for record in records:
            validate_against_schema(record, schema_name)
        ids = [record[id_field] for record in records]
        require(len(ids) == len(set(ids)), 'Duplicate ' + id_field)
        indexes[key] = {record[id_field]: record for record in records}
    return indexes


def latest_observed_state(task, support):
    states = [state for state in support['observed_states'].values() if state['task_id'] == task['task_id']]
    if not states:
        return None
    return max(states, key=lambda state: instant(state['observed_at']))


def validate_project_protocol(task, support):
    matches = [
        protocol for protocol in support['project_protocols'].values()
        if protocol['source_ref'] == task['project_protocol_ref'] and protocol['digest'] == task['project_protocol_digest']
    ]
    require(len(matches) == 1, 'TASK project protocol reference/digest does not resolve uniquely')
    protocol = matches[0]
    require(protocol['repository'] == task['repository'], 'Project protocol repository differs from TASK repository')
    criteria = {}
    for acceptance_set in protocol['acceptance_sets']:
        for criterion in acceptance_set['criteria']:
            require(criterion['id'] not in criteria, 'Duplicate project-protocol criterion ID')
            criteria[criterion['id']] = criterion
    harness_criteria = set()
    for harness in protocol['harnesses']:
        require(harness['protected'] is True, 'Project Super Review harness must be protected')
        for criterion_id in harness['criteria']:
            require(criterion_id in criteria, 'Project harness references unknown criterion')
            harness_criteria.add(criterion_id)
    for declared in task['acceptance']:
        criterion = criteria.get(declared['id'])
        require(criterion, 'TASK acceptance criterion missing from pinned project protocol')
        require(criterion['required'] == declared['required'], 'TASK acceptance requiredness differs from pinned project protocol')
        require(criterion['super_review_required'] == declared['super_review_required'], 'TASK Super Review requirement differs from pinned project protocol')
        require(set(criterion['verification_method_ids']) == set(declared['verification_method_ids']), 'TASK verification methods differ from pinned project protocol')
        if declared['super_review_required']:
            require(declared['id'] in harness_criteria, 'Super Review criterion is not covered by a protected project harness')
    return protocol


def acceptance_ids(task, required_only=False):
    return {r['id'] for r in task['acceptance'] if not required_only or r['required']}


def acceptance_by_id(task):
    return {r['id']: r for r in task['acceptance']}


def applies(command, task, stage):
    stage = 'COORDINATOR' if stage in ['PARENT_CHECK', 'PLAN', 'DELIVERY'] else stage
    return (command['child_issue'] is None or command['child_issue'] == task['issue']) and command['target'] in ['ALL', stage]


def controls_at(commands, at):
    """Scoped Resume never clears a broader hold; Status/Timer never resume."""
    controls = []
    for command in commands:
        if instant(command['issued_at']) > at:
            break
        if command['command'] in ['HOLD', 'PAUSE', 'STOP']:
            controls = [c for c in controls if (c['target'], c['child_issue']) != (command['target'], command['child_issue'])]
            controls.append(command)
        elif command['command'] == 'RESUME':
            if command['target'] == 'ALL' and command['child_issue'] is None:
                controls = []
            else:
                controls = [c for c in controls if not ((command['target'] == 'ALL' or c['target'] == command['target']) and (command['child_issue'] is None or c['child_issue'] == command['child_issue']))]
    return controls


def blocking_control(commands, task, stage, at):
    return next((c for c in reversed(controls_at(commands, at)) if applies(c, task, stage)), None)


def resumes_after(commands, task, record, at=None):
    end = instant(record['work_periods'][-1]['end']) if record['writer_stopped'] else instant(record['started_at'])
    return [c for c in commands if c['command'] == 'RESUME' and applies(c, task, record['stage']) and instant(c['issued_at']) > end and (at is None or instant(c['issued_at']) <= at)]


def cloud_resume_pending(commands, observations, now):
    for index, command in enumerate(commands):
        if command['command'] == 'RESUME' and instant(command['issued_at']) <= now:
            before = controls_at(commands[:index], instant(command['issued_at']))
            if any(c['command'] == 'PAUSE' and (command['target'] == 'ALL' or c['target'] == command['target']) and (command['child_issue'] is None or c['child_issue'] == command['child_issue']) for c in before):
                if observations.get('external_writer_stopped') is not True:
                    return True
    return False


def paused_seconds(commands, task, stage, start, end):
    boundaries = [start] + sorted({instant(c['issued_at']) for c in commands if start < instant(c['issued_at']) < end}) + [end]
    return sum((right - left).total_seconds() for left, right in zip(boundaries, boundaries[1:]) if blocking_control(commands, task, stage, left))


def active_seconds(record, commands, task, now):
    elapsed = 0
    for period in record['work_periods']:
        start = instant(period['start'])
        end = instant(period['end']) if period['end'] else now
        end = min(end, now)
        if end > start:
            elapsed += (end - start).total_seconds() - paused_seconds(commands, task, record['stage'], start, end)
    return elapsed


def stage_status(record, timers, commands, task, now):
    if record['status'] == 'STALLED' and not record['writer_stopped']:
        return 'BLOCKED' if now >= instant(record['stalled_at']) + timedelta(minutes=5) else 'STALLED'
    if record['status'] == 'WAITING_CI':
        start = instant(record['ci_wait_started_at'])
        elapsed = (now - start).total_seconds() - paused_seconds(commands, task, record['stage'], start, now)
        if elapsed >= timers['ci_wait_minutes'] * 60:
            return 'BLOCKED'
    if record['status'] in ['RUNNING', 'WAITING_CI'] and active_seconds(record, commands, task, now) >= timers['stage_minutes'][record['stage']] * 60:
        return 'STALLED'
    return record['status']


def validate_periods(record, parent, task, now):
    periods = record['work_periods']
    require(instant(periods[0]['start']) == instant(record['started_at']), 'First active period must match stage start')
    prior_end = None
    for index, period in enumerate(periods):
        start, end = instant(period['start']), instant(period['end']) if period['end'] else None
        require(start <= now and (end is None or start <= end <= now), 'Invalid/future active period')
        require(prior_end is None or start >= prior_end, 'Overlapping work periods')
        require(end is not None or index == len(periods) - 1, 'Only the last work period may be open')
        require(not blocking_control(parent['owner_commands'], task, record['stage'], start), 'A stage/work period started under an Owner hold/pause/stop')
        prior_end = end
    require(not record['writer_stopped'] or all(p['end'] is not None for p in periods), 'Stopped writer needs closed active periods')
    require(len(periods) == 1, 'Resume uses a fresh reconciled attempt, not another period on the old attempt')


def validate_stage_trust(record, task, parent, support, now):
    role = record['role_integrity']
    require(role['claimed_role'] == record['stage'] and role['principal'] == record['executor'], 'Role-integrity claim does not match stage executor')
    effective_role = 'COORDINATOR' if record['stage'] == 'PARENT_CHECK' else record['stage']
    require(record['executor'] in task['role_principals'][effective_role], 'Stage executor is not an authorized principal for this role')
    require(record['common_protocol_ref'] == task['protocol_ref'] and record['common_protocol_digest'] == task['protocol_digest'], 'Stage Common protocol basis is stale')
    require(record['project_protocol_ref'] == task['project_protocol_ref'], 'Stage project protocol reference is stale')

    start = support['context_snapshots'].get(record['context_start_ref'])
    require(start and start['task_id'] == task['task_id'] and start['phase'] == 'START', 'Missing/mismatched START context snapshot')
    require(start['parent_comment_frontier'] == record['parent_context']['through_comment_ref'], 'START context snapshot does not match reconciled parent frontier')
    require(instant(start['observed_at']) <= instant(record['started_at']), 'START context snapshot must precede stage action')

    environment = support['environments'].get(record['environment_ref'])
    require(environment, 'Missing environment record')

    evidence = {item['evidence_id']: item for item in record['evidence_manifest']}
    require(set(record['evidence_refs']) == set(evidence), 'evidence_refs must exactly name the stage evidence manifest')
    for evidence_id, embedded in evidence.items():
        provenance = support['evidence_records'].get(evidence_id)
        require(provenance, 'Stage evidence reference lacks provenance record')
        require(provenance['producer_role'] == record['stage'] and provenance['producer_principal'] == record['executor'], 'Evidence provenance producer does not match stage')
        require(provenance['evidence_class'] == embedded['class'] and provenance['candidate_sha'] == embedded['source_sha'], 'Evidence provenance class/candidate mismatch')
        require(provenance['project_protocol_digest'] == task['project_protocol_digest'], 'Evidence provenance uses stale project protocol')
        require(provenance['harness_digest'] == embedded['harness_digest'] and provenance['baseline_digest'] == embedded['baseline_digest'], 'Evidence provenance harness/baseline mismatch')
        require(provenance['environment_digest'] == embedded['environment_digest'], 'Evidence provenance environment mismatch')
        require(provenance['result'] == embedded['result'] and provenance['procedure'] == embedded['procedure'] and provenance['artifact_digest'] == embedded['artifact_digest'], 'Evidence provenance result/procedure/artifact mismatch')
        if provenance['evidence_class'] == 'REVIEWER_INDEPENDENT':
            require(provenance['producer_role'] == 'REVIEWER', 'Reviewer-independent evidence must be produced by Reviewer')
        if provenance['evidence_class'] == 'SUPER_REVIEW_INDEPENDENT':
            require(provenance['producer_role'] in ['COORDINATOR', 'PARENT_CHECK'], 'Super-review independent evidence must be produced by Super Reviewer')

    if record['status'] != 'PASS':
        return

    completed = instant(record['work_periods'][-1]['end'])
    pre = support['context_snapshots'].get(record['context_pre_verdict_ref'])
    require(pre and pre['task_id'] == task['task_id'] and pre['phase'] == 'PRE_VERDICT', 'PASS needs a PRE_VERDICT context snapshot')
    require(instant(start['observed_at']) <= instant(pre['observed_at']) <= completed, 'PRE_VERDICT context snapshot timing invalid')

    attestation = record['source_attestation']
    require(attestation and attestation['candidate_sha'] == record['validated_sha'] and attestation['base_sha'] == record['base_sha'], 'PASS source attestation does not match validated candidate/base')
    require(attestation['unrecorded_changes'] is False, 'PASS source attestation reports unrecorded changes')
    require(all(record['freshness'].values()), 'PASS requires every declared freshness dimension current')
    require(not any(item['blocking'] and item['status'] == 'OPEN' for item in record['carried_findings']), 'PASS has unresolved blocking carried finding')

    referenced = set()
    for row in record['acceptance_results']:
        if row['required']:
            referenced.update(row['evidence_ids'])
    require(all(evidence[eid]['source_sha'] == record['validated_sha'] for eid in referenced), 'Required acceptance evidence is not bound to final validated candidate')
    require(all(evidence[eid]['environment_digest'] == environment['digest'] for eid in referenced), 'Required acceptance evidence environment differs from stage environment')

    if record['stage'] in ['REVIEWER', 'COORDINATOR', 'PARENT_CHECK']:
        lease = support['review_leases'].get(record['review_lease_ref'])
        require(lease and lease['task_id'] == task['task_id'] and lease['stage_record_id'] == record['record_id'], 'Missing/mismatched review lease')
        require(lease['candidate_sha'] == record['validated_sha'] and lease['base_sha'] == record['base_sha'], 'Review lease is stale for candidate/base')
        require(lease['common_protocol_ref'] == task['protocol_ref'] and lease['common_protocol_digest'] == task['protocol_digest'] and lease['project_protocol_digest'] == task['project_protocol_digest'], 'Review lease protocol basis is stale')
        require(lease['spec_digest'] == task['spec_digest'] and lease['parent_spec_digest'] == parent['spec_digest'], 'Review lease specification basis is stale')
        require(lease['context_pre_verdict_ref'] == pre['snapshot_id'], 'Review lease does not name PRE_VERDICT context')
        require(lease['parent_context_digest'] == pre['parent_frontier_digest'] and lease['child_context_digest'] == pre['child_issue_digest'] and lease['pr_description_digest'] == pre['pr_description_digest'] and lease['owner_control_digest'] == pre['owner_control_digest'], 'Review lease context/PR/Owner-control basis is stale')
        require(lease['environment_ref'] == environment['environment_id'] and lease['environment_digest'] == environment['digest'], 'Review lease environment is stale')
        require(lease['integration_tree_digest'] == attestation['integration_tree_digest'] and lease['merge_base_sha'] == attestation['merge_base_sha'], 'Review lease integration tree/merge base differs from source attestation')
        require(lease['required_check_policy_digest'] == task['required_check_policy']['digest'], 'Review lease required-check policy is stale')
        surface_digest = record['acceptance_surface']['digest'] if record['acceptance_surface'] else task['project_protocol_digest']
        require(lease['acceptance_surface_digest'] == surface_digest, 'Review lease acceptance surface is stale')
        require(instant(lease['sealed_at']) <= completed, 'Review lease cannot be sealed after stage completion')

    if record['stage'] in ['COORDINATOR', 'PARENT_CHECK']:
        surface = record['acceptance_surface']
        for row in record['acceptance_results']:
            if not acceptance_by_id(task)[row['criterion_id']]['super_review_required']:
                continue
            for evidence_id in row['evidence_ids']:
                item = evidence[evidence_id]
                if item['class'] in ['SUPER_REVIEW_INDEPENDENT', 'EXTERNAL_ORACLE']:
                    require(item['harness_digest'] == surface['harness_digest'], 'Independent Super Review evidence uses wrong harness digest')
                    require(item['baseline_digest'] == surface['baseline_digest'], 'Independent Super Review evidence uses wrong baseline digest')


def validate_observed_merge_basis(task, latest, support):
    state = latest_observed_state(task, support)
    require(state, 'Missing structured observed repository/check state')
    require(state['pr'] == task['pr'] and state['pr_head_sha'] == latest['validated_sha'] and state['base_sha'] == latest['base_sha'], 'Observed repository state is stale for PR head/base')
    require(state['common_protocol_digest'] == task['protocol_digest'] and state['project_protocol_digest'] == task['project_protocol_digest'], 'Observed repository state has stale protocol basis')
    require(state['repository_policy_digest'] == task['required_check_policy']['digest'], 'Observed repository policy differs from trusted required-check policy')
    require(state['integration_tree_digest'] == latest['source_attestation']['integration_tree_digest'] and state['merge_base_sha'] == latest['source_attestation']['merge_base_sha'], 'Observed integration tree/merge base differs from reviewed identity')
    require(state['workspace_digest'] == latest['source_attestation']['workspace_digest'], 'Observed workspace digest differs from reviewed candidate')
    lease = support['review_leases'].get(latest['review_lease_ref'])
    require(lease, 'Final review lease missing at pre-merge refresh')
    require(state['environment_digest'] == lease['environment_digest'], 'Observed environment differs from final review lease')
    context = support['context_snapshots'].get(state['pre_merge_context_ref'])
    require(context and context['task_id'] == task['task_id'] and context['phase'] == 'PRE_MERGE', 'Missing/mismatched PRE_MERGE context snapshot')
    require(context['parent_frontier_digest'] == lease['parent_context_digest'] and context['child_issue_digest'] == lease['child_context_digest'] and context['pr_description_digest'] == lease['pr_description_digest'] and context['owner_control_digest'] == lease['owner_control_digest'], 'PRE_MERGE context changed after final review; lease expired')
    require(state['parent_context_digest'] == context['parent_frontier_digest'] and state['child_context_digest'] == context['child_issue_digest'] and state['pr_description_digest'] == context['pr_description_digest'] and state['owner_control_digest'] == context['owner_control_digest'], 'Observed state/context snapshot mismatch')
    contracts = {item['check']: item for item in task['required_check_contracts']}
    observed = {item['check']: item for item in state['required_checks']}
    require(set(contracts) == set(task['required_checks']), 'Required-check contracts must exactly cover required_checks')
    require(set(contracts) <= set(observed), 'Structured observed state is missing required check')
    for name, contract in contracts.items():
        item = observed[name]
        require(item['provider'] == contract['provider'] and item['workflow_digest'] == contract['workflow_digest'], 'Required check provider/workflow identity mismatch')
        require(item['workflow_path'] == contract['workflow_path'] and item['app_identity'] == contract['expected_app'], 'Required check workflow/app identity mismatch')
        require(item['head_sha'] == latest['validated_sha'], 'Required check ran on wrong candidate SHA')
        require(item['mandatory_steps_executed'] is True, 'Required check skipped a mandatory validation step')
        require(item['result'] == 'PASS', 'Required structured check is not PASS')
        require(item['run_id'] and item['job_id'], 'Required check lacks provider run/job identity')
    return state


def task_history(task, records, parent, support, now):
    history = [r for r in records if r['task_id'] == task['task_id']]
    passes, latest, attempts = {}, None, {}
    for record in history:
        stage = record['stage']
        require((stage == 'PARENT_CHECK') == (task['kind'] == 'PARENT'), 'Parent/child stage mismatch')
        require(record['workspace'] == parent['workspace'], 'Every role must use the declared shared folder')
        validate_periods(record, parent, task, now)
        validate_evidence(record, parent, task, bundle_observations=None, now=now)
        validate_stage_trust(record, task, parent, support, now)
        require(record['attempt'] == attempts.get(stage, 0) + 1, 'Attempt numbers must be consecutive within a role')
        attempts[stage] = record['attempt']
        require(record['previous_record'] == (latest['record_id'] if latest else None), 'Broken issue-comment record chain')
        if latest:
            require(latest['writer_stopped'], 'Previous writer has not acknowledged stop')
            require(instant(record['started_at']) >= instant(latest['work_periods'][-1]['end']), 'Shared-folder writers overlapped')
            require(instant(record['started_at']) >= instant(latest['publications']['end']['published_at']), 'Next role must wait for published parent END evidence')
            require(record['handover']['reconciliation'], 'Replacement needs issue/PR/workspace reconciliation')
            if latest['output_sha'] and record['input_sha'] != latest['output_sha'] and task['kind'] == 'CHILD':
                require(record['status'] == 'REWORK', 'External/unexplained HEAD movement requires REWORK reconciliation')
        require(set(record['acceptance_checked']) <= acceptance_ids(task), 'Unknown acceptance ID')
        require(record['spec_digest'] == task['spec_digest'] and record['parent_spec_digest'] == parent['spec_digest'], 'Specification changed; adopt and reconcile the current basis')
        require(len({f['id'] for f in record['findings']}) == len(record['findings']), 'Duplicate finding ID')
        require(not record['repeat_stages'], 'v1.1 forbids reverse stage routing; the current stage owns its production fixes')
        production = record['production_output']
        require(set(production['coverage_completed']) <= acceptance_ids(task), 'Production output names unknown acceptance coverage')
        if record['status'] == 'BLOCKED':
            require(production['blocking_class'] != 'NONE' and production['internal_fixable_defects_remaining'] == 0 and not production['unresolved_internal_defects'], 'BLOCKED is reserved for genuine external/authority boundaries, not internal fixable defects')
        if record['status'] == 'PASS':
            require(production['internal_fixable_defects_remaining'] == 0 and not production['unresolved_internal_defects'], 'PASS cannot push internal fixable defects downstream')
            require(production['coverage_complete_for_stage'] and not production['early_termination'], 'PASS requires work-to-exhaustion for the stage')
            require(production['blocking_class'] == 'NONE', 'PASS cannot retain a blocking class')
        acceptance_rows = record['acceptance_results']
        require(len({r['criterion_id'] for r in acceptance_rows}) == len(acceptance_rows), 'Duplicate acceptance result')
        require({r['criterion_id'] for r in acceptance_rows} <= acceptance_ids(task), 'Acceptance result names unknown criterion')
        evidence = {e['evidence_id']: e for e in record['evidence_manifest']}
        require(len(evidence) == len(record['evidence_manifest']), 'Duplicate evidence ID')
        for row in acceptance_rows:
            require(set(row['evidence_ids']) <= set(evidence), 'Acceptance result references missing evidence')
            declared = acceptance_by_id(task)[row['criterion_id']]
            require(row['required'] == declared['required'], 'Acceptance requiredness differs from TASK')
            require(set(row['verification_method_ids']) == set(declared['verification_method_ids']), 'Acceptance verification methods differ from TASK')
        if stage in ['COORDINATOR', 'PARENT_CHECK']:
            surface = record['acceptance_surface']
            require(surface and surface['project_protocol_digest'] == task['project_protocol_digest'], 'Super Review acceptance surface does not match pinned project protocol')
            require(surface['mutation_detected'] is False, 'Protected acceptance surface changed during certification')
            for row in acceptance_rows:
                declared = acceptance_by_id(task)[row['criterion_id']]
                if declared['super_review_required']:
                    classes = {evidence[eid]['class'] for eid in row['evidence_ids']}
                    require(classes & {'SUPER_REVIEW_INDEPENDENT', 'EXTERNAL_ORACLE'}, 'Super-review criterion lacks independent project-harness/oracle evidence')
        if task['kind'] == 'CHILD':
            expected = next((s for s in ORDER if s not in passes), 'COORDINATOR')
            require(stage == expected or (latest and stage == latest['stage'] and latest['status'] != 'PASS'), 'Role skipped an unfinished prerequisite')
            for later in ORDER[ORDER.index(stage) + 1:]:
                passes.pop(later, None)
        if stage in ['COORDINATOR', 'PARENT_CHECK']:
            require(record['executor'] == parent['parent_owner'], 'Coordinator must be the parent owner')
        else:
            require(record['executor'] != parent['parent_owner'], 'Coder/Reviewer must be independent of Coordinator')
        if latest and record['output_sha'] != latest['output_sha']:
            passes.pop('COORDINATOR', None)
        require(not record['repeat_stages'], 'Reverse stage invalidation is forbidden in v1.1')
        if record['status'] == 'PASS':
            require(record['output_sha'] == record['validated_sha'], 'PASS needs the actual validated output SHA')
            require(acceptance_ids(task, True) <= set(record['acceptance_checked']), 'Missing required acceptance coverage')
            rows = {r['criterion_id']: r for r in record['acceptance_results']}
            require(acceptance_ids(task, True) <= set(rows), 'Missing required structured acceptance result')
            require(all(rows[c]['result'] == 'PASS' for c in acceptance_ids(task, True)), 'Required structured acceptance result is not PASS')
            checks = [c for c in record['validation'] if c['required']]
            require(checks and all(c['result'] == 'PASS' for c in checks), 'Required validation needs actual PASS')
            require(not any(f['status'] == 'OPEN' for f in record['findings']), 'Open blocking finding')
            completed = instant(record['work_periods'][-1]['end'])
            require(not blocking_control(parent['owner_commands'], task, stage, completed), 'Owner control prevents stage advancement')
            passes[stage] = record
        else:
            passes.pop(stage, None)
        latest = record
    executors = [passes[s]['executor'] for s in ORDER if s in passes]
    require(len(executors) == len(set(executors)), 'Coder, Reviewer and Coordinator require distinct identities')
    return latest, passes


def validate_bundle(bundle, now=None):
    now = instant(now) if isinstance(now, str) else now or datetime.now(timezone.utc)
    require(isinstance(bundle, dict) and set(bundle) == {'tasks', 'stages', 'results', 'observed', 'support'}, 'Bundle needs tasks, stages, results, observed and support only')
    require(all(isinstance(bundle[k], list) for k in ['tasks', 'stages', 'results']) and isinstance(bundle['observed'], dict), 'Invalid record collections')
    support = support_index(bundle)
    for record in bundle['tasks'] + bundle['stages'] + bundle['results']:
        schema_check(record)
    tasks = {t['task_id']: t for t in bundle['tasks']}
    require(len(tasks) == len(bundle['tasks']), 'Duplicate task ID')
    require(len({t['issue'] for t in tasks.values()}) == len(tasks), 'Duplicate task issue')
    parents = [t for t in tasks.values() if t['kind'] == 'PARENT']
    require(len(parents) == 1, 'Exactly one parent TASK required')
    parent = parents[0]
    declarations = {c['issue']: c for c in parent['children']}
    require(len(declarations) == len(parent['children']) and parent['issue'] not in declarations, 'Invalid child declarations')
    commands = parent['owner_commands']
    require(all(command['owner_principal'] in parent['owner_principals'] for command in commands), 'Owner command principal is not authorized by TASK')
    require(all(command['source_kind'] != 'UNVERIFIED' and command['authentication_status'] != 'UNVERIFIED' for command in commands), 'Owner command source/authentication is unverified')
    require(len({c['id'] for c in commands}) == len(commands), 'Duplicate Owner command ID')
    require(all(instant(c['issued_at']) <= now for c in commands), 'Future Owner command')
    require(commands == sorted(commands, key=lambda c: instant(c['issued_at'])), 'Owner commands must be chronological')
    require(all(c['child_issue'] is None or c['child_issue'] in declarations for c in commands), 'Command names undeclared child')
    timers = dict(parent['timers'], stage_minutes=dict(parent['timers']['stage_minutes']))
    if timers['stage_minutes'] != DEFAULT_BUDGETS or timers['ci_wait_minutes'] != 30:
        require(timers['override_reason'], 'Timer override needs an Owner reason')
    for command in commands:
        if command['command'] == 'TIMER':
            if command['target'] == 'ALL':
                timers['stage_minutes'] = {s: command['minutes'] for s in DEFAULT_BUDGETS}
                timers['ci_wait_minutes'] = command['minutes']
            else:
                timers['stage_minutes'][command['target']] = command['minutes']
                if command['target'] == 'COORDINATOR':
                    timers['stage_minutes']['PARENT_CHECK'] = command['minutes']
    if parent['merge_authority']['mode'] == 'DELEGATED':
        require(parent['merge_authority']['reference'], 'Delegated authority needs an actual Owner instruction')
    for task in tasks.values():
        require(len(acceptance_ids(task)) == len(task['acceptance']), 'Duplicate acceptance ID')
        validate_project_protocol(task, support)
        require(set(task['waivable_criteria']) <= acceptance_ids(task), 'waivable_criteria names unknown acceptance ID')
        role_sets = [set(task['role_principals'][name]) for name in ['CODER', 'REVIEWER', 'COORDINATOR']]
        require(not (role_sets[0] & role_sets[1] or role_sets[0] & role_sets[2] or role_sets[1] & role_sets[2]), 'Authorized role principal sets must be disjoint')
        contracts = {item['check']: item for item in task['required_check_contracts']}
        require(len(contracts) == len(task['required_check_contracts']) and set(contracts) == set(task['required_checks']), 'required_check_contracts must exactly cover required_checks')
        require(all(item['provider'] == task['required_check_policy']['provider'] and item['policy_source'] == task['required_check_policy']['source_ref'] for item in task['required_check_contracts']), 'Required-check contract is outside trusted policy source/provider')
        require(task['repository'] == parent['repository'] and task['parent_owner'] == parent['parent_owner'] and task['protocol_ref'] == parent['protocol_ref'] and task['protocol_digest'] == parent['protocol_digest'] and task['project_protocol_ref'] == parent['project_protocol_ref'] and task['project_protocol_digest'] == parent['project_protocol_digest'] and task['role_principals'] == parent['role_principals'], 'Inconsistent parent/Common/project protocol or role basis')
        require(set(task['stacked_dependencies']) <= set(tasks) - {task['task_id']}, 'Invalid stacked dependency task ID')
        if task['kind'] == 'CHILD':
            require(task['issue'] in declarations and task['parent_issue'] == parent['issue'], 'Undeclared child')
        else:
            require(not task['stacked_dependencies'], 'Parent TASK cannot declare stacked dependencies')
    for child in declarations.values():
        require(set(child['covers']) <= acceptance_ids(parent), 'Child covers unknown parent requirement')
        require(set(child['depends_on']) <= set(declarations) and child['issue'] not in child['depends_on'], 'Invalid dependency')
    def visit(number, stack):
        require(number not in stack, 'Dependency cycle')
        for dependency in declarations[number]['depends_on']:
            visit(dependency, stack | {number})
    for number in declarations:
        visit(number, set())
    ids = [r['record_id'] for r in bundle['stages'] + bundle['results']]
    require(len(ids) == len(set(ids)), 'Duplicate record ID')
    require(all(r['task_id'] in tasks for r in bundle['stages'] + bundle['results']), 'Unknown task ID')
    for waiver in support['waivers'].values():
        task = tasks.get(waiver['task_id'])
        require(task and waiver['criterion_id'] in task['waivable_criteria'], 'Waiver targets unknown/non-waivable criterion')
        require(waiver['owner_principal'] in parent['owner_principals'], 'Waiver principal is not an authorized Owner')
        lease = support['review_leases'].get(waiver['lease_id'])
        require(lease and lease['task_id'] == waiver['task_id'] and lease['candidate_sha'] == waiver['candidate_sha'], 'Waiver is not bound to its candidate lease')
        require(instant(waiver['issued_at']) <= now and (waiver['expires_at'] is None or instant(waiver['expires_at']) >= now), 'Waiver is future or expired')
        require(waiver['result_override'] is False and waiver['non_transitive'] is True, 'Waiver cannot convert evidence to PASS or transfer automatically')
    history = {key: task_history(task, bundle['stages'], parent, support, now) for key, task in tasks.items()}
    active = [r for r, _ in history.values() if r and not r['writer_stopped']]
    observations = bundle['observed']
    dependency_heads = observations.get('dependency_heads', {})
    require(isinstance(dependency_heads, dict), 'dependency_heads observation must be an object')
    for key, task in tasks.items():
        latest, _passes = history[key]
        if not latest or latest['status'] != 'PASS' or not latest['review_lease_ref']:
            continue
        lease = support['review_leases'][latest['review_lease_ref']]
        current = {}
        for dependency in task['stacked_dependencies']:
            require(dependency in dependency_heads, 'Missing current stacked dependency head observation')
            current[dependency] = dependency_heads[dependency]
        recorded = {item['task_id']: item['sha'] for item in lease['dependency_heads']}
        require(recorded == current, 'Stacked dependency head moved; current review lease expired')
    validate_pipeline(parent, tasks, bundle['stages'], observations, now)
    for record in bundle['stages']:
        validate_evidence(record, parent, tasks[record['task_id']], observations, now)
    result_map, by_task = {}, {}
    stage_map = {r['record_id']: r for r in bundle['stages']}
    for result in bundle['results']:
        task = tasks[result['task_id']]
        final = stage_map.get(result['final_record'])
        latest, passes = history[task['task_id']]
        stage = 'COORDINATOR' if task['kind'] == 'CHILD' else 'PARENT_CHECK'
        require(result['kind'] == task['kind'] and final and final == latest and stage in passes and final['stage'] == stage, 'Delivery lacks its current passing final record')
        require(not resumes_after(commands, task, final, instant(result['recorded_at'])), 'Delivery needs fresh final review after Owner Resume')
        accepted, remaining = set(result['accepted_ids']), set(result['remaining_ids'])
        require(not accepted & remaining and accepted | remaining == acceptance_ids(task), 'Result must partition declared acceptance')
        require(result['head_sha'] == final['validated_sha'] and accepted <= set(final['acceptance_checked']), 'Result claims unvalidated material')
        require(not result['responsibility_complete'] or accepted == acceptance_ids(task), 'Incomplete acceptance cannot be complete')
        require(result['parent_comment_ref'].split('#')[0].rstrip('/').endswith('/issues/' + str(parent['issue'])) and '#' in result['parent_comment_ref'], 'Delivery evidence must be published on parent issue')
        recorded = instant(result['recorded_at'])
        require(instant(final['work_periods'][-1]['end']) <= recorded <= now, 'Result timing invalid')
        require(instant(final['publications']['end']['published_at']) <= recorded, 'Delivery must follow published final role END evidence')
        require(not blocking_control(commands, task, 'COORDINATOR', recorded), 'Owner command blocks delivery publication/advancement')
        if task['kind'] == 'CHILD':
            require(all(s in passes for s in ORDER) and task['pr'] == result['pr'], 'Child delivery lacks full role chain')
            require(result['review_lease_ref'] == final['review_lease_ref'], 'Delivery does not reference final review lease')
            pre_merge = support['context_snapshots'].get(result['pre_merge_context_ref'])
            observed_state = support['observed_states'].get(result['observed_state_ref'])
            require(pre_merge and pre_merge['task_id'] == task['task_id'] and pre_merge['phase'] == 'PRE_MERGE', 'Delivery lacks valid PRE_MERGE context')
            require(observed_state and observed_state['task_id'] == task['task_id'] and observed_state['pre_merge_context_ref'] == pre_merge['snapshot_id'], 'Delivery lacks matching observed state')
            require(observed_state['pr_head_sha'] == result['head_sha'], 'Delivery observed-state head differs from delivered head')
            for waiver_ref in result['waiver_refs']:
                waiver = support['waivers'].get(waiver_ref)
                require(waiver and waiver['task_id'] == task['task_id'] and waiver['lease_id'] == result['review_lease_ref'], 'Delivery references invalid waiver')
            merge = observations.get('merged', {}).get(str(result['pr']))
            require(merge and merge.get('head_sha') == result['head_sha'] and merge.get('merge_commit_sha') == result['merge_commit_sha'], 'Provider merge observation missing/mismatched')
            merged_at = instant(merge['merged_at'])
            require(instant(final['work_periods'][-1]['end']) <= merged_at <= recorded, 'Merge/result timing invalid')
            require(not blocking_control(commands, task, 'COORDINATOR', merged_at), 'Merge occurred under Owner control')
            canonical = result['canonical_observation']
            observed_canonical = observations.get('canonical_main_observations', {}).get(str(result['pr']))
            require(observed_canonical and observed_canonical == canonical, 'Canonical post-merge observation missing/mismatched')
            canonical_at = instant(canonical['observed_at'])
            require(merged_at <= canonical_at <= recorded, 'Canonical post-merge observation timing invalid')
            require(canonical['integrates_reviewed_candidate'] is True, 'Canonical main does not attest reviewed candidate integration')
        else:
            require(observations.get('main_sha') == result['head_sha'] == final['base_sha'], 'Parent must validate integrated current main')
        require(task['task_id'] not in by_task, 'Use latest delivery result per task; preserve history on issues')
        result_map[result['record_id']], by_task[task['task_id']] = result, result
    completed = {tasks[key]['issue'] for key, r in by_task.items() if r['kind'] == 'CHILD' and r['responsibility_complete']}
    for result in result_map.values():
        if result['kind'] == 'PARENT' and result['responsibility_complete']:
            refs = result['child_results']
            require(all(ref in result_map and result_map[ref]['kind'] == 'CHILD' and result_map[ref]['responsibility_complete'] for ref in refs), 'Parent links incomplete child result')
            require({tasks[result_map[ref]['task_id']]['issue'] for ref in refs} == set(declarations), 'Parent must include every declared child')
    for record in bundle['stages']:
        task = tasks[record['task_id']]
        dependencies = set(declarations[task['issue']]['depends_on']) if task['kind'] == 'CHILD' else set(declarations)
        require(dependencies <= completed, 'Dependencies/children not complete before stage')
        for key, result in by_task.items():
            if tasks[key]['issue'] in dependencies:
                require(instant(record['started_at']) >= instant(result['recorded_at']), 'Stage predates dependency delivery')
    states = {}
    for key, task in tasks.items():
        latest, passes = history[key]
        result = by_task.get(key)
        if result:
            stage = 'COMPLETE' if result['responsibility_complete'] else 'DELIVERY'
            status = 'COMPLETE' if result['responsibility_complete'] else 'MERGED' if task['kind'] == 'CHILD' else 'REWORK'
        elif latest:
            stage, status = latest['stage'], stage_status(latest, timers, commands, task, now)
            if task['kind'] == 'CHILD' and all(s in passes for s in ORDER):
                pr = str(task['pr'])
                head = observations.get('pr_heads', {}).get(pr)
                current_basis = observations.get('spec_digests', {})
                workspace = observations.get('workspace', {})
                current = head == latest['validated_sha'] and observations.get('main_sha') == latest['base_sha'] and current_basis.get(key) == task['spec_digest'] and current_basis.get(parent['task_id']) == parent['spec_digest']
                material = observations.get('review_snapshots', {}).get(latest['record_id'], {}) if latest['workspace_mode'] == 'READ_ONLY' else workspace
                stable_source = latest['workspace_mode'] != 'READ_ONLY' or material.get('reference') == latest['review_source']['reference']
                if not current or not stable_source or workspace.get('path') != parent['workspace'] or material.get('head_sha') != head or material.get('unrecorded_changes') is not False:
                    stage, status = 'COORDINATOR', 'REWORK'
                else:
                    checks = observations.get('checks', {}).get(pr)
                    checks_by_name = {c.get('check'): c for c in checks or []}
                    required = set(task['required_checks'])
                    satisfied = checks is not None and required <= set(checks_by_name) and all(checks_by_name[name].get('head_sha') == head and checks_by_name[name].get('result') == 'PASS' for name in required)
                    if not satisfied:
                        failed = any(checks_by_name.get(name, {}).get('result') == 'FAIL' for name in required)
                        wait_start = observations.get('ci_wait_started_at', {}).get(pr)
                        elapsed = (now - instant(wait_start)).total_seconds() - paused_seconds(commands, task, 'COORDINATOR', instant(wait_start), now) if wait_start else 0
                        status = 'BLOCKED' if failed or elapsed >= timers['ci_wait_minutes'] * 60 else 'WAITING_CI'
                    else:
                        validate_observed_merge_basis(task, latest, support)
                        if not observations.get('merge_authority_refs', {}).get(pr):
                            status = 'WAITING_OWNER'
                        else:
                            stage, status = 'DELIVERY', 'MERGE_READY'
            elif status == 'PASS':
                stage, status = next((s for s in ORDER if s not in passes), 'PARENT_CHECK') if task['kind'] == 'CHILD' else 'PARENT_CHECK', 'READY'
        else:
            stage = 'PLAN' if task['kind'] == 'PARENT' else 'CODER'
            status = 'READY' if task['kind'] == 'PARENT' or set(declarations[task['issue']]['depends_on']) <= completed else 'BLOCKED'
        if not result and latest and resumes_after(commands, task, latest):
            stage, status = latest['stage'], 'REWORK' if latest['status'] == 'PASS' else 'READY'
        if not result and cloud_resume_pending(commands, observations, now):
            status = 'BLOCKED'
        if not result:
            command = blocking_control(commands, task, 'COORDINATOR' if stage in ['DELIVERY', 'PARENT_CHECK', 'PLAN'] else stage, now)
            if command:
                stopped = not latest or latest['writer_stopped']
                markers = {'HOLD': ('HELD', 'HOLD_REQUESTED'), 'PAUSE': ('PAUSED', 'PAUSE_REQUESTED'), 'STOP': ('STOPPED', 'STOP_REQUESTED')}
                status = markers[command['command']][0 if stopped else 1]
        states[str(task['issue'])] = {'stage': stage, 'status': status}
    parent_state = states[str(parent['issue'])]
    if parent_state['stage'] == 'PLAN' and active and parent_state['status'] == 'READY':
        parent_state.update(stage=active[0]['stage'], status='RUNNING')
    if parent['task_id'] not in by_task and completed == set(declarations) and not history[parent['task_id']][0]:
        states[str(parent['issue'])]['stage'] = 'PARENT_CHECK'
    status_details(states, tasks, history, observations, now, parent, by_task)
    return {'record_consistency': 'PASS', 'basis': 'SUPPLIED_ISSUE_PR_AND_WORKSPACE_OBSERVATIONS_ONLY', 'owner_controls': [c['id'] for c in controls_at(commands, now)], 'stage_budget_minutes': timers['stage_minutes'], 'issues': states}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--now', help='Timezone-qualified timestamp for replay')
    args = parser.parse_args()
    try:
        print(json.dumps(validate_bundle(json.loads(args.bundle.read_text(encoding='utf-8-sig')), args.now), indent=2))
    except (RecordError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'record_consistency': 'FAIL', 'reason': str(error)}))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
