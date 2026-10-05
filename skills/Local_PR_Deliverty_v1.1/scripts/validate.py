"""Read-only consistency checker for supplied issue/PR records; no Git operations."""
import argparse
import hashlib
import json
from functools import lru_cache
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from pipeline import RecordError, validate_evidence, validate_pipeline, status_details

ROOT = Path(__file__).resolve().parents[1]
ORDER = ['CODER', 'REVIEWER', 'COORDINATOR']
DEFAULT_BUDGETS = {'CODER': 15, 'REVIEWER': 15, 'COORDINATOR': 45, 'PARENT_CHECK': 45}
ADVANCING_STATUSES = {'STAGE_COMPLETE', 'STAGE_COMPLETE_WITH_WAIVER'}
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


def canonical_digest(record, omit_fields=('digest',)):
    """Canonical SHA-256 for fully visible in-bundle records."""
    omit = set(omit_fields)
    payload = {key: value for key, value in record.items() if key not in omit}
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def canonical_value_digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def derive_evidence_result(items):
    """Fail-closed aggregation for evidence that claims one method/gate result."""
    require(items, 'Cannot derive a result from empty evidence')
    results = {item['result'] for item in items}
    if 'FAIL' in results:
        return 'FAIL'
    if 'INCONCLUSIVE' in results:
        return 'INCONCLUSIVE'
    if 'NOT_APPLICABLE' in results:
        return 'NOT_APPLICABLE' if results == {'NOT_APPLICABLE'} else 'INCONCLUSIVE'
    if 'PASS' in results:
        return 'PASS'
    if 'NOT_RUN' in results:
        return 'NOT_RUN'
    raise RecordError('Unknown evidence-result combination')


def derive_criterion_result(method_results):
    require(method_results, 'Criterion has no verification-method results')
    values = set(method_results.values())
    if 'FAIL' in values:
        return 'FAIL'
    if 'INCONCLUSIVE' in values:
        return 'INCONCLUSIVE'
    if 'NOT_APPLICABLE' in values:
        return 'NOT_APPLICABLE'
    if 'NOT_RUN' in values:
        return 'NOT_RUN'
    require(values == {'PASS'}, 'Unknown criterion-result combination')
    return 'PASS'


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
            if key in ['environments', 'project_protocols']:
                require(record['digest'] == canonical_digest(record), key + ' record digest does not match canonical content')
            elif key == 'review_leases':
                require(record['lease_id'] == 'sha256:' + canonical_digest(record, ('lease_id',)), 'Review lease ID is not content-addressed to canonical lease content')
        ids = [record[id_field] for record in records]
        require(len(ids) == len(set(ids)), 'Duplicate ' + id_field)
        indexes[key] = {record[id_field]: record for record in records}
    return indexes


def latest_observed_state(task, support):
    states = [state for state in support['observed_states'].values() if state['task_id'] == task['task_id']]
    if not states:
        return None
    return max(states, key=lambda state: instant(state['observed_at']))


def waiver_valid_at(waiver, at):
    return instant(waiver['issued_at']) <= at and (waiver['expires_at'] is None or at <= instant(waiver['expires_at']))


def matching_waivers(task, lease_ref, candidate_sha, target_kind, target_id, support, at, refs=None):
    allowed_refs = set(refs) if refs is not None else None
    matches = []
    for waiver in support['waivers'].values():
        if allowed_refs is not None and waiver['waiver_id'] not in allowed_refs:
            continue
        if (
            waiver['task_id'] == task['task_id']
            and waiver['lease_id'] == lease_ref
            and waiver['candidate_sha'] == candidate_sha
            and waiver['target_kind'] == target_kind
            and waiver['target_id'] == target_id
            and waiver_valid_at(waiver, at)
        ):
            matches.append(waiver)
    require(len(matches) <= 1, 'Multiple active waivers target the same candidate/gate')
    return matches


def has_waiver(task, record, target_kind, target_id, support, at):
    return bool(matching_waivers(
        task, record['review_lease_ref'], record['validated_sha'],
        target_kind, target_id, support, at, record['waiver_refs']
    ))


def active_check_waiver(task, record, check, support, at):
    return bool(matching_waivers(
        task, record['review_lease_ref'], record['validated_sha'],
        'REQUIRED_CHECK', check, support, at
    ))


def merge_authority_ready(parent, observations, pr, at):
    authority = observations.get('merge_authority_observations', {}).get(str(pr))
    if authority is None:
        return False
    required = {
        'principal', 'authority_ref', 'source_kind', 'source_digest',
        'authentication_status', 'observed_at'
    }
    require(set(authority) == required, 'Merge authority observation has unknown/missing fields')
    require(authority['source_kind'] in ['GITHUB_PROVIDER', 'DIRECT_OWNER_SESSION', 'OTHER_AUTHENTICATED_PROVIDER'], 'Merge authority source is unverified')
    require(authority['authentication_status'] in ['AUTHENTICATED', 'OBSERVED_TRUSTED_PROVIDER'], 'Merge authority authentication is unverified')
    require(isinstance(authority['source_digest'], str) and len(authority['source_digest']) == 64 and all(ch in '0123456789abcdef' for ch in authority['source_digest']), 'Merge authority source digest is invalid')
    require(isinstance(authority['authority_ref'], str) and authority['authority_ref'], 'Merge authority lacks source reference')
    require(instant(authority['observed_at']) <= at, 'Merge authority was observed after the decision point')
    policy = parent['merge_authority']
    if policy['mode'] == 'OWNER_ONLY':
        require(authority['principal'] in parent['owner_principals'], 'Merge authority principal is not an authorized Owner')
    else:
        require(authority['principal'] == policy['delegate_principal'], 'Merge authority principal is not the delegated principal')
        require(authority['authority_ref'] == policy['reference'], 'Merge authority reference differs from Owner delegation')
    return True


def validate_context_snapshot(snapshot, task):
    observed_at = instant(snapshot['observed_at'])
    refs = set()
    kinds = set()
    for event in snapshot['context_events']:
        key = (event['source_kind'], event['provider_id'])
        require(key not in refs, 'Duplicate provider context event identity in snapshot')
        refs.add(key)
        kinds.add(event['source_kind'])
        created, updated = instant(event['created_at']), instant(event['updated_at'])
        require(created <= updated <= observed_at, 'Context event timestamps exceed snapshot observation time')
    require('PARENT_ISSUE_BODY' in kinds and 'TASK_ISSUE_BODY' in kinds, 'Context snapshot lacks parent/task issue identity')
    if snapshot['parent_comment_frontier']:
        require(any(event['source_kind'] == 'PARENT_COMMENT' and event['provider_ref'] == snapshot['parent_comment_frontier'] for event in snapshot['context_events']), 'Context snapshot lacks provider event for parent comment frontier')
    if task['pr'] is not None:
        require('PR_DESCRIPTION' in kinds, 'Child context snapshot lacks PR description provider identity')


def validate_project_protocol(task, support):
    matches = [
        protocol for protocol in support['project_protocols'].values()
        if protocol['source_ref'] == task['project_protocol_ref'] and protocol['digest'] == task['project_protocol_digest']
    ]
    require(len(matches) == 1, 'TASK project protocol reference/digest does not resolve uniquely')
    protocol = matches[0]
    require(protocol['repository'] == task['repository'], 'Project protocol repository differs from TASK repository')

    protected = protocol['protected_surface']
    manifest = protected['manifest']
    require(protected['manifest_digest'] == canonical_value_digest(manifest), 'Protected-surface manifest digest does not match canonical manifest content')
    manifest_by_id = {item['id']: item for item in manifest}
    require(len(manifest_by_id) == len(manifest), 'Duplicate protected-surface manifest ID')

    gates = {gate['id']: gate for gate in protocol['external_gates']}
    require(len(gates) == len(protocol['external_gates']), 'Duplicate project external gate ID')

    methods = {method['id']: method for method in protocol['verification_methods']}
    require(len(methods) == len(protocol['verification_methods']), 'Duplicate project verification-method ID')
    for method in methods.values():
        require(not (method['harness_id'] and method['external_gate_id']), 'Verification method cannot bind both harness and external gate')
        if method['harness_id']:
            require(any(h['id'] == method['harness_id'] for h in protocol['harnesses']), 'Verification method references unknown harness')
        if method['external_gate_id']:
            require(method['external_gate_id'] in gates, 'Verification method references unknown external gate')
            require(set(method['required_evidence_classes']) <= set(gates[method['external_gate_id']]['allowed_evidence_classes']), 'External-gate verification method permits evidence class outside gate policy')

    criteria = {}
    for acceptance_set in protocol['acceptance_sets']:
        for criterion in acceptance_set['criteria']:
            require(criterion['id'] not in criteria, 'Duplicate project-protocol criterion ID')
            require(set(criterion['verification_method_ids']) <= set(methods), 'Project criterion references unknown verification method')
            criteria[criterion['id']] = criterion

    harness_criteria = set()
    harnesses = {}
    for harness in protocol['harnesses']:
        require(harness['id'] not in harnesses, 'Duplicate project harness ID')
        harnesses[harness['id']] = harness
        require(harness['protected'] is True, 'Project Super Review harness must be protected')
        require(set(harness['verification_method_ids']) <= set(methods), 'Project harness references unknown verification method')
        require(all(methods[mid]['harness_id'] == harness['id'] for mid in harness['verification_method_ids']), 'Harness verification-method list contains method bound elsewhere')
        require(set(harness['manifest_refs']) <= set(manifest_by_id), 'Project harness references unknown protected-surface manifest entry')
        require(any(manifest_by_id[mid]['kind'] == 'HARNESS_ENTRYPOINT' for mid in harness['manifest_refs']), 'Project harness lacks a protected HARNESS_ENTRYPOINT manifest entry')
        for criterion_id in harness['criteria']:
            require(criterion_id in criteria, 'Project harness references unknown criterion')
            criterion_methods = set(criteria[criterion_id]['verification_method_ids'])
            require(criterion_methods & set(harness['verification_method_ids']), 'Project harness does not execute any verification method declared by its criterion')
            harness_criteria.add(criterion_id)

    regression_ids = set()
    for regression in protocol['regressions']:
        require(regression['id'] not in regression_ids, 'Duplicate project regression ID')
        regression_ids.add(regression['id'])
        require(regression['criterion_id'] in criteria, 'Project regression references unknown criterion')
        harness = harnesses.get(regression['harness_id'])
        require(harness and regression['criterion_id'] in harness['criteria'], 'Project regression is not bound to a harness covering its criterion')

    for declared in task['acceptance']:
        criterion = criteria.get(declared['id'])
        require(criterion, 'TASK acceptance criterion missing from pinned project protocol')
        require(criterion['required'] == declared['required'], 'TASK acceptance requiredness differs from pinned project protocol')
        require(criterion['super_review_required'] == declared['super_review_required'], 'TASK Super Review requirement differs from pinned project protocol')
        require(set(criterion['verification_method_ids']) == set(declared['verification_method_ids']), 'TASK verification methods differ from pinned project protocol')
        if declared['super_review_required']:
            require(declared['id'] in harness_criteria, 'Super Review criterion is not covered by a protected project harness')

    require(protected['harness_digest'] and protected['baseline_digest'] and isinstance(protected['fixture_digests'], list), 'Pinned project protected surface is incomplete')
    return protocol

def applicable_external_gates(task, protocol):
    return {
        gate['id']: gate
        for gate in protocol['external_gates']
        if gate['applies_to'] in ['ALL', task['kind']]
    }


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
    protocol = validate_project_protocol(task, support)
    role = record['role_integrity']
    require(role['claimed_role'] == record['stage'] and role['principal'] == record['executor'], 'Role-integrity claim does not match stage executor')
    effective_role = 'COORDINATOR' if record['stage'] == 'PARENT_CHECK' else record['stage']
    require(record['executor'] in task['role_principals'][effective_role], 'Stage executor is not an authorized principal for this role')
    require(record['common_protocol_ref'] == task['protocol_ref'] and record['common_protocol_digest'] == task['protocol_digest'], 'Stage Common protocol basis is stale')
    require(record['project_protocol_ref'] == task['project_protocol_ref'], 'Stage project protocol reference is stale')

    start = support['context_snapshots'].get(record['context_start_ref'])
    require(start and start['task_id'] == task['task_id'] and start['phase'] == 'START', 'Missing/mismatched START context snapshot')
    validate_context_snapshot(start, task)
    require(start['parent_comment_frontier'] == record['parent_context']['through_comment_ref'], 'START context snapshot does not match reconciled parent frontier')
    require(instant(start['observed_at']) <= instant(record['started_at']), 'START context snapshot must precede stage action')

    environment = support['environments'].get(record['environment_ref'])
    require(environment, 'Missing environment record')

    evidence = {item['evidence_id']: item for item in record['evidence_manifest']}
    require(set(record['evidence_refs']) == set(evidence), 'evidence_refs must exactly name the stage evidence manifest')
    methods = {item['id']: item for item in protocol['verification_methods']}
    harnesses = {item['id']: item for item in protocol['harnesses']}
    for evidence_id, embedded in evidence.items():
        provenance = support['evidence_records'].get(evidence_id)
        require(provenance, 'Stage evidence reference lacks provenance record')
        require(provenance['collected_by_role'] == record['stage'] and provenance['collected_by_principal'] == record['executor'], 'Evidence collector/attester does not match stage executor')
        require(provenance['evidence_class'] == embedded['class'] and provenance['candidate_sha'] == embedded['source_sha'], 'Evidence provenance class/candidate mismatch')
        require(provenance['verification_method_id'] == embedded['verification_method_id'] and provenance['harness_id'] == embedded['harness_id'] and provenance['external_gate_id'] == embedded['external_gate_id'], 'Evidence method/harness/gate binding mismatch')
        method = methods.get(provenance['verification_method_id'])
        require(method, 'Evidence references unknown project verification method')
        require(provenance['evidence_class'] in method['required_evidence_classes'], 'Evidence class is not permitted by its verification method')
        require(provenance['harness_id'] == method['harness_id'] and provenance['external_gate_id'] == method['external_gate_id'], 'Evidence execution binding differs from project verification method')
        if provenance['harness_id']:
            require(provenance['harness_id'] in harnesses, 'Evidence names unknown project harness')
        require(provenance['common_protocol_digest'] == task['protocol_digest'] and provenance['project_protocol_digest'] == task['project_protocol_digest'], 'Evidence provenance uses stale Common/project protocol')
        require(provenance['harness_digest'] == embedded['harness_digest'] and provenance['baseline_digest'] == embedded['baseline_digest'], 'Evidence provenance harness/baseline mismatch')
        require(provenance['environment_digest'] == embedded['environment_digest'], 'Evidence provenance environment mismatch')
        require(provenance['result'] == embedded['result'] and provenance['procedure'] == embedded['procedure'] and provenance['artifact_digest'] == embedded['artifact_digest'], 'Evidence provenance result/procedure/artifact mismatch')
        collected_at = instant(provenance['collected_at'])
        record_end = instant(record['work_periods'][-1]['end']) if record['work_periods'][-1]['end'] else now
        require(instant(record['started_at']) <= collected_at <= record_end, 'Evidence collection time falls outside stage work period')
        if provenance['procedure_kind'] == 'COMMAND' and provenance['result'] != 'NOT_RUN':
            require(provenance['command_argv'] and provenance['exit_code'] is not None, 'Executed command evidence needs argv and exit code')
        elif provenance['procedure_kind'] != 'COMMAND':
            require(not provenance['command_argv'] and provenance['exit_code'] is None, 'Manual/provider evidence cannot claim command execution fields')

        cls = provenance['evidence_class']
        if cls == 'AUTHOR':
            require(provenance['origin_kind'] == 'STAGE_EXECUTOR' and provenance['oracle_independence'] == 'NOT_INDEPENDENT', 'AUTHOR evidence must identify a stage-executor origin and non-independent oracle')
            require(provenance['principal_relationship_to_candidate'] in ['AUTHOR_OF_CANDIDATE', 'LAST_PRODUCT_WRITER', 'PRIOR_PRODUCT_WRITER'], 'AUTHOR evidence has invalid candidate relationship')
        elif cls == 'REVIEWER_INDEPENDENT':
            require(record['stage'] == 'REVIEWER' and provenance['origin_kind'] == 'STAGE_EXECUTOR' and provenance['origin_principal'] == record['executor'], 'Reviewer-independent evidence must originate from the Reviewer stage')
            require(provenance['oracle_independence'] == 'PINNED_ORACLE_INDEPENDENT', 'Reviewer-independent evidence requires a pinned independent oracle/harness')
            require(provenance['principal_relationship_to_candidate'] in ['NON_WRITER_REVIEWER', 'LAST_PRODUCT_WRITER'], 'Reviewer-independent evidence has invalid candidate relationship')
        elif cls == 'SUPER_REVIEW_INDEPENDENT':
            require(record['stage'] in ['COORDINATOR', 'PARENT_CHECK'] and provenance['origin_kind'] == 'STAGE_EXECUTOR' and provenance['origin_principal'] == record['executor'], 'Super-review independent evidence must originate from Super Reviewer')
            require(provenance['oracle_independence'] == 'PINNED_ORACLE_INDEPENDENT', 'Super-review independent evidence requires pinned-oracle independence')
            require(provenance['principal_relationship_to_candidate'] in ['NON_WRITER_REVIEWER', 'LAST_PRODUCT_WRITER'], 'Super-review evidence has invalid candidate relationship')
        elif cls == 'CI_PROVIDER':
            require(provenance['origin_kind'] == 'CI_PROVIDER' and provenance['provider_ref'], 'CI provider evidence must identify its provider origin')
            require(provenance['oracle_independence'] == 'PROVIDER_INDEPENDENT' and provenance['principal_relationship_to_candidate'] == 'EXTERNAL_PROVIDER', 'CI provider evidence must be external/provider independent')
        elif cls == 'EXTERNAL_ORACLE':
            require(provenance['origin_kind'] in ['EXTERNAL_ORACLE', 'OTHER_AUTHENTICATED_PROVIDER', 'HUMAN_OBSERVER'] and provenance['provider_ref'], 'External-oracle evidence must identify an external origin')
            require(provenance['oracle_independence'] in ['PROVIDER_INDEPENDENT', 'HUMAN_INDEPENDENT'], 'External-oracle evidence must declare external independence')
            require(provenance['principal_relationship_to_candidate'] in ['EXTERNAL_PROVIDER', 'EXTERNAL_HUMAN'], 'External-oracle evidence has invalid candidate relationship')

    gate_rows = record['external_gate_results']
    require(len({row['gate_id'] for row in gate_rows}) == len(gate_rows), 'Duplicate external gate result')
    applicable_gates = applicable_external_gates(task, protocol)
    require(set(row['gate_id'] for row in gate_rows) <= set(applicable_gates), 'Stage reports unknown/non-applicable external gate')
    for row in gate_rows:
        require(set(row['evidence_ids']) <= set(evidence), 'External gate result references missing stage evidence')
        gate = applicable_gates[row['gate_id']]
        if row['evidence_ids']:
            classes = {evidence[eid]['class'] for eid in row['evidence_ids']}
            require(classes <= set(gate['allowed_evidence_classes']), 'External gate evidence class is not allowed by project protocol')
            require(all(support['evidence_records'][eid]['external_gate_id'] == row['gate_id'] for eid in row['evidence_ids']), 'External gate cites evidence bound to another gate')
            require(row['result'] == derive_evidence_result([support['evidence_records'][eid] for eid in row['evidence_ids']]), 'External gate result contradicts cited evidence results')
        else:
            require(row['result'] == 'NOT_RUN', 'External gate without evidence must be NOT_RUN')
    if record['stage'] not in ['COORDINATOR', 'PARENT_CHECK']:
        require(not gate_rows, 'Only Super Reviewer/PARENT_CHECK may certify project external gates')

    surface = record['acceptance_surface']
    if surface is not None:
        require(surface['digest'] == canonical_digest(surface), 'Acceptance-surface digest does not match canonical content')
        protected = protocol['protected_surface']
        require(surface['project_protocol_digest'] == protocol['digest'], 'Acceptance surface project-protocol digest differs from pinned project protocol')
        require(surface['harness_digest'] == protected['harness_digest'], 'Acceptance surface harness differs from pinned project protocol')
        require(surface['baseline_digest'] == protected['baseline_digest'], 'Acceptance surface baseline differs from pinned project protocol')
        require(set(surface['oracle_digests']) == set(protected['oracle_digests']), 'Acceptance surface oracle set differs from pinned project protocol')
        require(set(surface['fixture_digests']) == set(protected['fixture_digests']), 'Acceptance surface fixture set differs from pinned project protocol')
        require(surface['manifest_digest'] == protected['manifest_digest'], 'Acceptance surface transitive manifest differs from pinned project protocol')

    if record['status'] not in ADVANCING_STATUSES:
        return

    completed = instant(record['work_periods'][-1]['end'])

    if record['status'] == 'STAGE_COMPLETE':
        require(not record['waiver_refs'], 'STAGE_COMPLETE cannot depend on Owner waivers')
    else:
        require(record['stage'] in ['COORDINATOR', 'PARENT_CHECK'] and record['waiver_refs'], 'STAGE_COMPLETE_WITH_WAIVER is reserved for final engineering stages with explicit waivers')

    used_stage_waivers = set()
    if record['stage'] in ['COORDINATOR', 'PARENT_CHECK']:
        require(set(row['gate_id'] for row in gate_rows) == set(applicable_gates), 'Final engineering outcome must account for every applicable project external gate')
        rows_by_gate = {row['gate_id']: row for row in gate_rows}
        for gate_id, gate in applicable_gates.items():
            if not gate['required']:
                continue
            result = rows_by_gate[gate_id]['result']
            if result == 'PASS':
                continue
            require(result == 'NOT_RUN', 'Required project external gate FAIL/INCONCLUSIVE cannot be waived')
            require(gate['waivable'] is True and record['status'] == 'STAGE_COMPLETE_WITH_WAIVER', 'Required project external gate NOT_RUN needs an explicit waivable policy and stage-complete-with-waiver outcome')
            matches = matching_waivers(task, record['review_lease_ref'], record['validated_sha'], 'EXTERNAL_GATE', gate_id, support, completed, record['waiver_refs'])
            require(len(matches) == 1, 'Required external gate NOT_RUN lacks exact active Owner waiver')
            used_stage_waivers.add(matches[0]['waiver_id'])

    pre = support['context_snapshots'].get(record['context_pre_verdict_ref'])
    require(pre and pre['task_id'] == task['task_id'] and pre['phase'] == 'PRE_VERDICT', 'Advancing outcome needs a PRE_VERDICT context snapshot')
    validate_context_snapshot(pre, task)
    require(instant(start['observed_at']) <= instant(pre['observed_at']) <= completed, 'PRE_VERDICT context snapshot timing invalid')

    attestation = record['source_attestation']
    require(attestation and attestation['candidate_sha'] == record['validated_sha'] and attestation['base_sha'] == record['base_sha'] and attestation['base_ref'] == task['target_ref'], 'Advancing source attestation does not match validated candidate/base target')
    require(attestation['unrecorded_changes'] is False, 'Advancing source attestation reports unrecorded changes')
    require(all(record['freshness'].values()), 'Advancing outcome requires every declared freshness dimension current')
    require(not any(item['blocking'] and item['status'] in ['OPEN', 'CARRIED'] for item in record['carried_findings']), 'Advancing outcome has unresolved blocking carried finding')

    for row in record['acceptance_results']:
        if not row['required']:
            continue
        if row['result'] == 'PASS':
            continue
        require(row['result'] == 'NOT_RUN', 'Required criterion FAIL/INCONCLUSIVE/NOT_APPLICABLE cannot advance')
        require(record['status'] == 'STAGE_COMPLETE_WITH_WAIVER', 'Required criterion NOT_RUN needs stage-complete-with-waiver outcome')
        matches = matching_waivers(task, record['review_lease_ref'], record['validated_sha'], 'CRITERION', row['criterion_id'], support, completed, record['waiver_refs'])
        require(len(matches) == 1, 'Required criterion NOT_RUN lacks exact active Owner waiver')
        used_stage_waivers.add(matches[0]['waiver_id'])

    if record['status'] == 'APPROVED_WITH_WAIVER':
        require(set(record['waiver_refs']) == used_stage_waivers, 'Stage waiver_refs must exactly match required NOT_RUN criterion/external-gate waivers')

    referenced = set()
    for row in record['acceptance_results']:
        if row['required']:
            referenced.update(row['evidence_ids'])
    require(all(evidence[eid]['source_sha'] == record['validated_sha'] for eid in referenced), 'Required acceptance evidence is not bound to final validated candidate')
    require(all(evidence[eid]['environment_digest'] == environment['digest'] for eid in referenced), 'Required acceptance evidence environment differs from stage environment')

    if record['stage'] in ['REVIEWER', 'COORDINATOR', 'PARENT_CHECK']:
        lease = support['review_leases'].get(record['review_lease_ref'])
        require(lease and lease['task_id'] == task['task_id'] and lease['stage_record_id'] == record['record_id'], 'Missing/mismatched review lease')
        require(lease['repository'] == task['repository'] and lease['pr'] == task['pr'], 'Review lease repository/PR identity differs from TASK')
        require(lease['certifier_role'] == record['stage'] and lease['certifier_principal'] == record['executor'], 'Review lease certifier identity differs from stage')
        require(lease['candidate_sha'] == record['validated_sha'] and lease['base_sha'] == record['base_sha'] and lease['target_ref'] == task['target_ref'], 'Review lease is stale for candidate/base target')
        require(lease['common_protocol_ref'] == task['protocol_ref'] and lease['common_protocol_digest'] == task['protocol_digest'] and lease['project_protocol_ref'] == task['project_protocol_ref'] and lease['project_protocol_digest'] == task['project_protocol_digest'], 'Review lease protocol basis is stale')
        require(lease['spec_digest'] == task['spec_digest'] and lease['parent_spec_digest'] == parent['spec_digest'], 'Review lease specification basis is stale')
        require(lease['context_pre_verdict_ref'] == pre['snapshot_id'], 'Review lease does not name PRE_VERDICT context')
        require(lease['parent_context_digest'] == pre['parent_frontier_digest'] and lease['child_context_digest'] == pre['child_issue_digest'] and lease['pr_description_digest'] == pre['pr_description_digest'] and lease['owner_control_digest'] == pre['owner_control_digest'], 'Review lease context/PR/Owner-control basis is stale')
        require(lease['environment_ref'] == environment['environment_id'] and lease['environment_digest'] == environment['digest'], 'Review lease environment is stale')
        require(lease['candidate_tree_digest'] == attestation['candidate_tree_digest'], 'Review lease candidate tree differs from source attestation')
        require(lease['integration_tree_digest'] == attestation['integration_tree_digest'] and lease['merge_base_sha'] == attestation['merge_base_sha'], 'Review lease integration tree/merge base differs from source attestation')
        require(lease['required_check_policy_digest'] == task['required_check_policy']['digest'], 'Review lease required-check policy is stale')
        surface = record['acceptance_surface']
        require(surface is not None, 'Independent review lease requires pinned acceptance surface')
        require(lease['acceptance_surface_digest'] == surface['digest'], 'Review lease acceptance surface is stale')
        require(lease['acceptance_surface_manifest_digest'] == surface['manifest_digest'], 'Review lease transitive acceptance-surface manifest is stale')
        require(lease['harness_digest'] == surface['harness_digest'] and lease['baseline_digest'] == surface['baseline_digest'], 'Review lease harness/baseline differs from stage acceptance surface')
        require(set(lease['oracle_digests']) == set(surface['oracle_digests']) and set(lease['fixture_digests']) == set(surface['fixture_digests']), 'Review lease oracle/fixture set differs from stage acceptance surface')
        require(instant(lease['sealed_at']) <= completed, 'Review lease cannot be sealed after stage completion')
        for evidence_id in record['evidence_refs']:
            provenance = support['evidence_records'][evidence_id]
            if provenance['evidence_class'] in ['REVIEWER_INDEPENDENT', 'SUPER_REVIEW_INDEPENDENT', 'EXTERNAL_ORACLE']:
                require(provenance['review_lease_ref'] == lease['lease_id'], 'Independent evidence is not bound to current review lease')
                require(provenance['acceptance_surface_digest'] == surface['digest'], 'Independent evidence acceptance-surface digest mismatch')
                require(provenance['acceptance_surface_manifest_digest'] == surface['manifest_digest'], 'Independent evidence transitive acceptance-surface manifest mismatch')
                require(set(provenance['fixture_digests']) == set(surface['fixture_digests']), 'Independent evidence fixture set differs from protected acceptance surface')

    if record['stage'] in ['COORDINATOR', 'PARENT_CHECK']:
        surface = record['acceptance_surface']
        require(surface is not None, 'Super Review completion needs pinned acceptance surface')
        for row in record['acceptance_results']:
            if not acceptance_by_id(task)[row['criterion_id']]['super_review_required']:
                continue
            for evidence_id in row['evidence_ids']:
                item = evidence[evidence_id]
                if item['class'] in ['SUPER_REVIEW_INDEPENDENT', 'EXTERNAL_ORACLE']:
                    require(item['harness_digest'] == surface['harness_digest'], 'Independent Super Review evidence uses wrong harness digest')
                    require(item['baseline_digest'] == surface['baseline_digest'], 'Independent Super Review evidence uses wrong baseline digest')


def validate_observed_merge_basis(task, latest, support, at, state_ref=None):
    state = support['observed_states'].get(state_ref) if state_ref else latest_observed_state(task, support)
    require(state, 'Missing structured observed repository/check state')
    require(instant(state['observed_at']) <= at, 'Structured observed repository/check state is from the future')
    require(state['pr'] == task['pr'] and state['pr_head_sha'] == latest['validated_sha'] and state['base_sha'] == latest['base_sha'] and state['target_ref'] == task['target_ref'], 'Observed repository state is stale for PR head/base target')
    require(state['common_protocol_digest'] == task['protocol_digest'] and state['project_protocol_digest'] == task['project_protocol_digest'], 'Observed repository state has stale protocol basis')
    require(state['repository_policy_visibility'] == 'CONFIRMED', 'Repository policy visibility is not confirmed')
    require(state['repository_policy_source_ref'] == task['required_check_policy']['source_ref'], 'Observed repository policy source differs from trusted policy source')
    require(state['repository_policy_digest'] == task['required_check_policy']['digest'], 'Observed repository policy differs from trusted required-check policy')
    require(state['integration_tree_digest'] == latest['source_attestation']['integration_tree_digest'] and state['merge_base_sha'] == latest['source_attestation']['merge_base_sha'], 'Observed integration tree/merge base differs from reviewed identity')
    require(state['workspace_digest'] == latest['source_attestation']['workspace_digest'], 'Observed workspace digest differs from reviewed candidate')
    lease = support['review_leases'].get(latest['review_lease_ref'])
    require(lease, 'Final review lease missing at pre-merge refresh')
    require(state['environment_digest'] == lease['environment_digest'], 'Observed environment differs from final review lease')
    context = support['context_snapshots'].get(state['pre_merge_context_ref'])
    require(context and context['task_id'] == task['task_id'] and context['phase'] == 'PRE_MERGE', 'Missing/mismatched PRE_MERGE context snapshot')
    validate_context_snapshot(context, task)
    require(context['parent_frontier_digest'] == lease['parent_context_digest'] and context['child_issue_digest'] == lease['child_context_digest'] and context['pr_description_digest'] == lease['pr_description_digest'] and context['owner_control_digest'] == lease['owner_control_digest'], 'PRE_MERGE context changed after final review; lease expired')
    require(state['parent_context_digest'] == context['parent_frontier_digest'] and state['child_context_digest'] == context['child_issue_digest'] and state['pr_description_digest'] == context['pr_description_digest'] and state['owner_control_digest'] == context['owner_control_digest'], 'Observed state/context snapshot mismatch')
    used_check_waivers = set()
    contracts = {item['check']: item for item in task['required_check_contracts']}
    observed = {item['check']: item for item in state['required_checks']}
    require(set(contracts) == set(task['required_checks']), 'Required-check contracts must exactly cover required_checks')
    require(set(contracts) <= set(observed), 'Structured observed state is missing required check')
    for name, contract in contracts.items():
        item = observed[name]
        require(item['provider'] == contract['provider'] and item['workflow_digest'] == contract['workflow_digest'], 'Required check provider/workflow identity mismatch')
        require(item['workflow_path'] == contract['workflow_path'] and item['app_identity'] == contract['expected_app'], 'Required check workflow/app identity mismatch')
        require(item['trigger_pr_head_sha'] == latest['validated_sha'], 'Required check was triggered for wrong PR head SHA')
        require(item['checkout_mode'] in contract['allowed_checkout_modes'], 'Required check checkout mode is not permitted by trusted policy')
        require(item['base_sha'] == latest['base_sha'] and item['merge_base_sha'] == latest['source_attestation']['merge_base_sha'], 'Required check base/merge-base identity is stale')
        if contract['certifies'] == 'PR_HEAD':
            require(item['checkout_mode'] == 'PR_HEAD', 'PR-head certification must actually checkout PR_HEAD')
            require(item['tested_commit_sha'] == latest['validated_sha'] and item['provider_run_head_sha'] == latest['validated_sha'], 'PR-head check did not execute the reviewed head')
            require(item['tested_tree_digest'] == latest['source_attestation']['candidate_tree_digest'], 'PR-head check tested wrong candidate tree')
        else:
            require(item['checkout_mode'] in ['SYNTHETIC_MERGE', 'MERGE_QUEUE'], 'Integration-candidate check must execute a synthetic merge or merge-queue candidate')
            require(item['provider_run_head_sha'] == item['tested_commit_sha'], 'Integration provider run head must identify the tested integration commit')
            require(item['integration_tree_digest'] == latest['source_attestation']['integration_tree_digest'], 'Required check integration-tree identity differs from reviewed integration candidate')
            require(item['tested_tree_digest'] == latest['source_attestation']['integration_tree_digest'], 'Required check tested tree differs from reviewed integration candidate')
        if item['result'] == 'PASS':
            require(item['mandatory_steps_executed'] is True, 'Required PASS check skipped a mandatory validation step')
            require(item['run_id'] and item['job_id'], 'Required PASS check lacks provider run/job identity')
        else:
            require(item['result'] == 'NOT_RUN', 'Required check FAIL/PENDING/INCONCLUSIVE cannot be waived')
            require(item['mandatory_steps_executed'] is False, 'NOT_RUN required check cannot claim all mandatory steps executed')
            matches = matching_waivers(task, latest['review_lease_ref'], latest['validated_sha'], 'REQUIRED_CHECK', name, support, at)
            require(len(matches) == 1, 'Required NOT_RUN check lacks active Owner waiver bound to final review lease')
            used_check_waivers.add(matches[0]['waiver_id'])
    for waiver_id in latest['waiver_refs']:
        waiver = support['waivers'].get(waiver_id)
        require(waiver and waiver_valid_at(waiver, at), 'Final engineering waiver expired or is unavailable at pre-merge/merge time')
    return state, used_check_waivers


def task_history(task, records, parent, support, now):
    protocol = validate_project_protocol(task, support)
    project_criteria = {
        criterion['id']: criterion
        for acceptance_set in protocol['acceptance_sets']
        for criterion in acceptance_set['criteria']
        if criterion['id'] in acceptance_ids(task)
    }
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
        if record['output_sha'] is not None:
            require(production['candidate_changed'] == (record['output_sha'] != record['input_sha']), 'production_output candidate_changed disagrees with actual stage input/output identity')
        if production['candidate_changed']:
            require(production['changed_components'], 'Changed candidate must declare changed component classes')
        require(set(production['defects_fixed_here']) <= set(production['defects_found']), 'Stage cannot claim a fixed defect it did not record as found/consumed')
        if production['defects_fixed_here']:
            require(production['candidate_changed'], 'Fixing product defects requires a changed candidate')

        acceptance_rows = record['acceptance_results']
        require(len({r['criterion_id'] for r in acceptance_rows}) == len(acceptance_rows), 'Duplicate acceptance result')
        require({r['criterion_id'] for r in acceptance_rows} <= acceptance_ids(task), 'Acceptance result names unknown criterion')
        evidence = {e['evidence_id']: e for e in record['evidence_manifest']}
        require(len(evidence) == len(record['evidence_manifest']), 'Duplicate evidence ID')
        provenance = {eid: support['evidence_records'][eid] for eid in evidence}
        methods = {method['id']: method for method in protocol['verification_methods']}

        finding_ids = {finding['id'] for finding in record['findings']}
        require(set(production['defects_found']) == finding_ids, 'production_output.defects_found must exactly name current-stage findings')
        fixed_ids = set(production['defects_fixed_here'])
        escalation_ids = set(production['external_escalations'])
        for finding in record['findings']:
            require(set(finding['resolution_evidence_ids']) <= set(evidence), 'Finding resolution references missing stage evidence')
            if finding['status'] == 'RESOLVED':
                require(finding['resolution_evidence_ids'], 'Resolved finding needs resolution evidence')
                require(all(evidence[eid]['result'] == 'PASS' for eid in finding['resolution_evidence_ids']), 'Resolved finding requires PASS resolution evidence')
            if finding['classification'] == 'BOUNDED_PRODUCT_FIX':
                require(finding['repair_disposition'] in ['FIXED_HERE', 'OBSERVED_NO_CHANGE'], 'Bounded product finding cannot be delegated externally')
                if finding['repair_disposition'] == 'FIXED_HERE':
                    require(finding['id'] in fixed_ids and finding['status'] == 'RESOLVED', 'Fixed-here finding must be resolved and listed in defects_fixed_here')
                    require(set(finding['affected_components']) & set(production['changed_components']), 'Fixed finding does not intersect declared changed components')
            else:
                require(finding['repair_disposition'] == 'ESCALATED', 'Non-bounded finding must use explicit escalation path')
                require(finding['id'] in escalation_ids, 'Escalated finding missing from production_output.external_escalations')
                require(finding['id'] not in fixed_ids, 'Material/protocol/external finding cannot be self-certified as fixed here')

        carried_ids = {finding['id'] for finding in record['carried_findings']}
        require(len(carried_ids) == len(record['carried_findings']), 'Duplicate carried finding ID')
        require(not (finding_ids & carried_ids), 'Current and carried findings must use distinct IDs')
        for carried in record['carried_findings']:
            require(set(carried['affected_acceptance']) <= acceptance_ids(task), 'Carried finding affects unknown acceptance criterion')
            require(set(carried['resolution_evidence_ids']) <= set(evidence), 'Carried finding resolution references missing stage evidence')
            if carried['status'] == 'RESOLVED':
                require(carried['resolution_evidence_ids'], 'Resolved carried finding needs resolution evidence')
                require(all(evidence[eid]['result'] == 'PASS' for eid in carried['resolution_evidence_ids']), 'Resolved carried finding requires PASS resolution evidence')

        for row in acceptance_rows:
            require(set(row['evidence_ids']) <= set(evidence), 'Acceptance result references missing evidence')
            require(set(row['finding_ids']) <= finding_ids | carried_ids, 'Acceptance result references unknown finding')
            declared = acceptance_by_id(task)[row['criterion_id']]
            require(row['required'] == declared['required'], 'Acceptance requiredness differs from TASK')
            require(set(row['verification_method_ids']) == set(declared['verification_method_ids']), 'Acceptance verification methods differ from TASK')
            cited_methods = {provenance[eid]['verification_method_id'] for eid in row['evidence_ids']}
            require(cited_methods == set(row['verification_method_ids']), 'Acceptance evidence does not exactly cover declared verification methods')
            method_results = {}
            for method_id in row['verification_method_ids']:
                method = methods[method_id]
                items = [provenance[eid] for eid in row['evidence_ids'] if provenance[eid]['verification_method_id'] == method_id]
                require(items, 'Acceptance verification method lacks evidence')
                require(all(item['evidence_class'] in method['required_evidence_classes'] for item in items), 'Acceptance method cites evidence class outside project method policy')
                method_results[method_id] = derive_evidence_result(items)
            derived = derive_criterion_result(method_results)
            require(row['result'] == derived, 'Acceptance result contradicts cited per-method evidence results')
            if row['result'] != 'NOT_APPLICABLE':
                require(row['rationale'] is None or row['rationale'], 'Acceptance rationale must be null or non-empty')

        discovery = record['discovery_freeze']
        if discovery is not None:
            require(discovery['candidate_sha'] == record['input_sha'], 'Discovery freeze must describe the stage input candidate')
            frozen_at = instant(discovery['frozen_at'])
            require(instant(record['started_at']) <= frozen_at <= (instant(record['work_periods'][-1]['end']) if record['work_periods'][-1]['end'] else now), 'Discovery freeze timing is outside stage work period')
            require(set(discovery['method_ids_attempted']) <= set(methods), 'Discovery freeze names unknown verification method')
            require(set(discovery['finding_ids']) <= {finding['id'] for finding in record['findings'] if finding['phase_found'] == 'DISCOVERY'}, 'Discovery freeze names finding not frozen during DISCOVERY')
            require(set(discovery['evidence_ids']) <= set(evidence), 'Discovery freeze references missing evidence')
            for eid in discovery['evidence_ids']:
                item = provenance[eid]
                require(item['candidate_sha'] == record['input_sha'], 'Discovery evidence must be bound to pre-repair input candidate')
                require(item['verification_method_id'] in discovery['method_ids_attempted'], 'Discovery evidence method not declared attempted')
                require(instant(item['collected_at']) <= frozen_at, 'Discovery evidence was collected after findings freeze')
            if production['candidate_changed']:
                require(discovery['first_repair_at'] is not None, 'Changed Reviewer/Super Reviewer candidate needs first repair timestamp')
                require(frozen_at < instant(discovery['first_repair_at']) <= instant(record['work_periods'][-1]['end']), 'Repair began before discovery findings were frozen')
            else:
                require(discovery['first_repair_at'] is None, 'Unchanged candidate cannot claim a first repair timestamp')

        if record['status'] == 'BLOCKED':
            require(production['blocking_class'] != 'NONE' and production['external_escalations'] and production['internal_fixable_defects_remaining'] == 0 and not production['unresolved_internal_defects'], 'BLOCKED is reserved for explicit genuine external/authority boundaries, not internal fixable defects')
        if record['status'] in ADVANCING_STATUSES:
            require(production['internal_fixable_defects_remaining'] == 0 and not production['unresolved_internal_defects'], 'Advancing outcome cannot push internal fixable defects downstream')
            require(production['coverage_complete_for_stage'] and not production['early_termination'], 'Advancing outcome requires work-to-exhaustion for the stage')
            require(production['blocking_class'] == 'NONE', 'Advancing outcome cannot retain a blocking class')
            require(not escalation_ids, 'Advancing outcome cannot retain material/protocol/external escalations in the same acceptance epoch')
            if stage in ['REVIEWER', 'COORDINATOR', 'PARENT_CHECK']:
                require(discovery is not None and discovery['sweep_complete'], 'Reviewer/Super Reviewer completion requires frozen pre-repair discovery sweep')
                role_criteria = {
                    criterion_id for criterion_id, criterion in project_criteria.items()
                    if (stage == 'REVIEWER' and criterion['reviewer_check_required'])
                    or (stage in ['COORDINATOR', 'PARENT_CHECK'] and criterion['super_review_required'])
                }
                role_methods = set().union(*(set(project_criteria[cid]['verification_method_ids']) for cid in role_criteria)) if role_criteria else set()
                require(role_methods <= set(discovery['method_ids_attempted']), 'Discovery sweep did not attempt the full role-required verification-method set before repair')
                require(role_methods <= {provenance[eid]['verification_method_id'] for eid in discovery['evidence_ids']}, 'Discovery sweep lacks pre-repair evidence for a role-required verification method')
        if record['status'] in ADVANCING_STATUSES:
            role_required = set()
            if stage == 'REVIEWER':
                role_required = {criterion_id for criterion_id, criterion in project_criteria.items() if criterion['reviewer_check_required']}
            elif stage in ['COORDINATOR', 'PARENT_CHECK']:
                role_required = {criterion_id for criterion_id, criterion in project_criteria.items() if criterion['super_review_required']}
            row_ids = {row['criterion_id'] for row in acceptance_rows}
            require(role_required <= row_ids, 'Advancing stage omitted project-declared role-specific acceptance coverage')
            require(role_required <= set(record['acceptance_checked']) and role_required <= set(production['coverage_completed']), 'Role-specific acceptance coverage is missing from stage coverage ledgers')
            if stage == 'REVIEWER':
                rows_by_id = {row['criterion_id']: row for row in acceptance_rows}
                for criterion_id in role_required:
                    row = rows_by_id[criterion_id]
                    for method_id in row['verification_method_ids']:
                        method = methods[method_id]
                        items = [provenance[eid] for eid in row['evidence_ids'] if provenance[eid]['verification_method_id'] == method_id]
                        require(any(item['evidence_class'] == 'REVIEWER_INDEPENDENT' for item in items) or 'REVIEWER_INDEPENDENT' not in method['required_evidence_classes'], 'Reviewer-required verification method lacks Reviewer-independent evidence')
        if stage in ['COORDINATOR', 'PARENT_CHECK']:
            surface = record['acceptance_surface']
            require(surface and surface['project_protocol_digest'] == task['project_protocol_digest'], 'Super Review acceptance surface does not match pinned project protocol')
            require(surface['mutation_detected'] is False, 'Protected acceptance surface changed during certification')
            for row in acceptance_rows:
                declared = acceptance_by_id(task)[row['criterion_id']]
                if declared['super_review_required']:
                    for method_id in row['verification_method_ids']:
                        method = methods[method_id]
                        items = [provenance[eid] for eid in row['evidence_ids'] if provenance[eid]['verification_method_id'] == method_id]
                        require(items, 'Super-review verification method lacks evidence')
                        if method['harness_id']:
                            require(any(item['harness_id'] == method['harness_id'] and item['evidence_class'] in ['SUPER_REVIEW_INDEPENDENT', 'EXTERNAL_ORACLE'] for item in items), 'Required project harness method was not executed by independent Super Review/oracle evidence')
        if task['kind'] == 'CHILD':
            expected = next((s for s in ORDER if s not in passes), 'COORDINATOR')
            require(stage == expected or (latest and stage == latest['stage'] and latest['status'] not in ADVANCING_STATUSES), 'Role skipped an unfinished prerequisite')
            for later in ORDER[ORDER.index(stage) + 1:]:
                passes.pop(later, None)
        if stage in ['COORDINATOR', 'PARENT_CHECK']:
            require(record['executor'] == parent['parent_owner'], 'Coordinator must be the parent owner')
        else:
            require(record['executor'] != parent['parent_owner'], 'Coder/Reviewer must be independent of Coordinator')
        if latest and record['output_sha'] != latest['output_sha']:
            passes.pop('COORDINATOR', None)
        require(not record['repeat_stages'], 'Reverse stage invalidation is forbidden in v1.1')
        if record['status'] in ADVANCING_STATUSES:
            require(record['output_sha'] == record['validated_sha'], 'Advancing outcome needs the actual validated output SHA')
            require(acceptance_ids(task, True) <= set(record['acceptance_checked']), 'Missing required acceptance coverage')
            rows = {r['criterion_id']: r for r in record['acceptance_results']}
            require(acceptance_ids(task, True) <= set(rows), 'Missing required structured acceptance result')
            if record['status'] == 'STAGE_COMPLETE':
                require(all(rows[c]['result'] == 'PASS' for c in acceptance_ids(task, True)), 'STAGE_COMPLETE requires every required structured acceptance result to be PASS')
            else:
                require(all(rows[c]['result'] in ['PASS', 'NOT_RUN'] for c in acceptance_ids(task, True)), 'STAGE_COMPLETE_WITH_WAIVER permits only PASS or explicitly waived NOT_RUN acceptance')
            checks = [c for c in record['validation'] if c['required']]
            require(checks and all(c['result'] == 'PASS' for c in checks), 'Required stage validation needs actual PASS')
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
        require(parent['merge_authority']['reference'] and parent['merge_authority']['delegate_principal'], 'Delegated authority needs an actual Owner instruction and principal')
        require(parent['merge_authority']['delegate_principal'] not in parent['role_principals']['CODER'] + parent['role_principals']['REVIEWER'] + parent['role_principals']['COORDINATOR'], 'Merge delegate must not silently reuse a production-role principal')
    else:
        require(parent['merge_authority']['delegate_principal'] is None, 'OWNER_ONLY merge policy cannot declare a delegate')
    for task in tasks.values():
        require(len(acceptance_ids(task)) == len(task['acceptance']), 'Duplicate acceptance ID')
        validate_project_protocol(task, support)
        require(set(task['waivable_criteria']) <= acceptance_ids(task), 'waivable_criteria names unknown acceptance ID')
        require(set(task['waivable_required_checks']) <= set(task['required_checks']), 'waivable_required_checks names unknown required check')
        role_sets = [set(task['role_principals'][name]) for name in ['CODER', 'REVIEWER', 'COORDINATOR']]
        require(not (role_sets[0] & role_sets[1] or role_sets[0] & role_sets[2] or role_sets[1] & role_sets[2]), 'Authorized role principal sets must be disjoint')
        contracts = {item['check']: item for item in task['required_check_contracts']}
        require(len(contracts) == len(task['required_check_contracts']) and set(contracts) == set(task['required_checks']), 'required_check_contracts must exactly cover required_checks')
        require(all(item['provider'] == task['required_check_policy']['provider'] and item['policy_source'] == task['required_check_policy']['source_ref'] for item in task['required_check_contracts']), 'Required-check contract is outside trusted policy source/provider')
        for item in task['required_check_contracts']:
            if item['certifies'] == 'PR_HEAD':
                require(item['allowed_checkout_modes'] == ['PR_HEAD'], 'PR_HEAD check contract may only allow PR_HEAD checkout mode')
            else:
                require(set(item['allowed_checkout_modes']) <= {'SYNTHETIC_MERGE', 'MERGE_QUEUE'} and item['allowed_checkout_modes'], 'Integration-candidate check contract may only allow SYNTHETIC_MERGE/MERGE_QUEUE')
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
        require(task, 'Waiver targets unknown task')
        target_kind, target_id = waiver['target_kind'], waiver['target_id']
        if target_kind == 'CRITERION':
            require(target_id in task['waivable_criteria'], 'Waiver targets unknown/non-waivable criterion')
        elif target_kind == 'REQUIRED_CHECK':
            require(target_id in task['waivable_required_checks'] and target_id in task['required_checks'], 'Waiver targets unknown/non-waivable required check')
        else:
            protocol = validate_project_protocol(task, support)
            gates = applicable_external_gates(task, protocol)
            require(target_id in gates and gates[target_id]['waivable'] is True, 'Waiver targets unknown/non-waivable external gate')
        require(waiver['owner_principal'] in parent['owner_principals'], 'Waiver principal is not an authorized Owner')
        lease = support['review_leases'].get(waiver['lease_id'])
        require(lease and lease['task_id'] == waiver['task_id'] and lease['candidate_sha'] == waiver['candidate_sha'], 'Waiver is not bound to its candidate lease')
        require(instant(waiver['issued_at']) <= now, 'Waiver is issued in the future')
        require(waiver['expires_at'] is None or instant(waiver['issued_at']) <= instant(waiver['expires_at']), 'Waiver expiry precedes issuance')
        require(waiver['result_override'] is False and waiver['non_transitive'] is True, 'Waiver cannot convert evidence to PASS or transfer automatically')
    history = {key: task_history(task, bundle['stages'], parent, support, now) for key, task in tasks.items()}
    active = [r for r, _ in history.values() if r and not r['writer_stopped']]
    observations = bundle['observed']
    dependency_heads = observations.get('dependency_heads', {})
    require(isinstance(dependency_heads, dict), 'dependency_heads observation must be an object')
    for key, task in tasks.items():
        latest, _passes = history[key]
        if not latest or latest['status'] not in ADVANCING_STATUSES or not latest['review_lease_ref']:
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
            require(merge and merge.get('head_sha') == result['head_sha'] and merge.get('merge_commit_sha') == result['merge_commit_sha'] and merge.get('target_ref') == task['target_ref'], 'Provider merge observation missing/mismatched target/head/merge identity')
            merged_at = instant(merge['merged_at'])
            require(instant(final['work_periods'][-1]['end']) <= merged_at <= recorded, 'Merge/result timing invalid')
            require(not blocking_control(commands, task, 'COORDINATOR', merged_at), 'Merge occurred under Owner control')
            require(merge_authority_ready(parent, observations, result['pr'], merged_at), 'Merge occurred without current authenticated merge authority')
            _merge_state, used_check_waivers = validate_observed_merge_basis(task, final, support, merged_at, result['observed_state_ref'])
            expected_waivers = set(final['waiver_refs']) | used_check_waivers
            require(set(result['waiver_refs']) == expected_waivers, 'Delivery waiver_refs must exactly match waivers actually used for engineering/pre-merge advancement')
            canonical = result['canonical_observation']
            observed_canonical = observations.get('canonical_target_observations', {}).get(str(result['pr']))
            require(observed_canonical and observed_canonical == canonical, 'Canonical post-merge target observation missing/mismatched')
            canonical_at = instant(canonical['observed_at'])
            require(merged_at <= canonical_at <= recorded, 'Canonical post-merge observation timing invalid')
            require(canonical['target_ref'] == task['target_ref'], 'Canonical observation names wrong target ref')
            require(canonical['reviewed_head_sha'] == result['head_sha'] and canonical['merge_commit_sha'] == result['merge_commit_sha'], 'Canonical observation is not bound to reviewed head/merge commit')
            if canonical['relation'] == 'EXACT_MERGE_COMMIT':
                require(canonical['target_sha'] == result['merge_commit_sha'] and canonical['ancestry_proof_ref'] is None, 'Exact canonical relation requires target SHA equal merge commit and no ancestry proof')
            else:
                require(canonical['ancestry_proof_ref'], 'Descendant canonical relation requires provider ancestry proof reference')
        else:
            require(observations.get('target_heads', {}).get(task['task_id']) == result['head_sha'] == final['base_sha'], 'Parent must validate its integrated current target ref')
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
        engineering_approved = bool(result)
        merge_ready = False
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
                target_head = observations.get('target_heads', {}).get(key)
                current = head == latest['validated_sha'] and target_head == latest['base_sha'] and current_basis.get(key) == task['spec_digest'] and current_basis.get(parent['task_id']) == parent['spec_digest']
                material = observations.get('review_snapshots', {}).get(latest['record_id'], {}) if latest['workspace_mode'] == 'READ_ONLY' else workspace
                stable_source = latest['workspace_mode'] != 'READ_ONLY' or material.get('reference') == latest['review_source']['reference']
                if not current or not stable_source or workspace.get('path') != parent['workspace'] or material.get('head_sha') != head or material.get('unrecorded_changes') is not False:
                    stage, status = 'COORDINATOR', 'REWORK'
                elif latest['status'] == 'APPROVED_WITH_WAIVER' and any(
                    not support['waivers'].get(waiver_id) or not waiver_valid_at(support['waivers'][waiver_id], now)
                    for waiver_id in latest['waiver_refs']
                ):
                    stage, status = 'DELIVERY', 'WAITING_OWNER'
                    engineering_approved = False
                else:
                    checks = observations.get('checks', {}).get(pr)
                    checks_by_name = {c.get('check'): c for c in checks or []}
                    required = set(task['required_checks'])
                    def legacy_check_satisfied(name):
                        item = checks_by_name.get(name, {})
                        if item.get('head_sha') != head:
                            return False
                        if item.get('result') == 'PASS':
                            return True
                        return item.get('result') == 'NOT_RUN' and active_check_waiver(task, latest, name, support, now)
                    satisfied = checks is not None and required <= set(checks_by_name) and all(legacy_check_satisfied(name) for name in required)
                    if not satisfied:
                        failed = any(checks_by_name.get(name, {}).get('result') in ['FAIL', 'INCONCLUSIVE'] for name in required)
                        owner_waiver_needed = any(
                            checks_by_name.get(name, {}).get('result') == 'NOT_RUN'
                            and name in task['waivable_required_checks']
                            and not active_check_waiver(task, latest, name, support, now)
                            for name in required
                        )
                        wait_start = observations.get('ci_wait_started_at', {}).get(pr)
                        elapsed = (now - instant(wait_start)).total_seconds() - paused_seconds(commands, task, 'COORDINATOR', instant(wait_start), now) if wait_start else 0
                        status = 'BLOCKED' if failed else 'WAITING_OWNER' if owner_waiver_needed else 'BLOCKED' if elapsed >= timers['ci_wait_minutes'] * 60 else 'WAITING_CI'
                    else:
                        policy_state = latest_observed_state(task, support)
                        if not policy_state or policy_state.get('repository_policy_visibility') != 'CONFIRMED':
                            stage, status = 'DELIVERY', 'WAITING_EXTERNAL'
                            engineering_approved = False
                        else:
                            validate_observed_merge_basis(task, latest, support, now)
                            engineering_approved = True
                            if not merge_authority_ready(parent, observations, task['pr'], now):
                                status = 'WAITING_OWNER'
                            else:
                                stage, status = 'DELIVERY', 'MERGE_READY'
                                merge_ready = True
            elif status in ADVANCING_STATUSES:
                stage, status = next((s for s in ORDER if s not in passes), 'PARENT_CHECK') if task['kind'] == 'CHILD' else 'PARENT_CHECK', 'READY'
        else:
            stage = 'PLAN' if task['kind'] == 'PARENT' else 'CODER'
            status = 'READY' if task['kind'] == 'PARENT' or set(declarations[task['issue']]['depends_on']) <= completed else 'BLOCKED'
        if not result and latest and resumes_after(commands, task, latest):
            stage, status = latest['stage'], 'REWORK' if latest['status'] in ADVANCING_STATUSES else 'READY'
        if not result and cloud_resume_pending(commands, observations, now):
            status = 'BLOCKED'
            engineering_approved = False
            merge_ready = False
        if not result:
            command = blocking_control(commands, task, 'COORDINATOR' if stage in ['DELIVERY', 'PARENT_CHECK', 'PLAN'] else stage, now)
            if command:
                stopped = not latest or latest['writer_stopped']
                markers = {'HOLD': ('HELD', 'HOLD_REQUESTED'), 'PAUSE': ('PAUSED', 'PAUSE_REQUESTED'), 'STOP': ('STOPPED', 'STOP_REQUESTED')}
                status = markers[command['command']][0 if stopped else 1]
                engineering_approved = False
                merge_ready = False
        states[str(task['issue'])] = {'stage': stage, 'status': status, 'engineering_approved': engineering_approved, 'merge_ready': merge_ready}
    parent_state = states[str(parent['issue'])]
    if parent_state['stage'] == 'PLAN' and active and parent_state['status'] == 'READY':
        parent_state.update(stage=active[0]['stage'], status='RUNNING')
    if parent['task_id'] not in by_task and completed == set(declarations) and not history[parent['task_id']][0]:
        states[str(parent['issue'])]['stage'] = 'PARENT_CHECK'
    status_details(states, tasks, history, observations, now, parent, by_task)
    return {'record_consistency': 'PASS', 'basis': 'SUPPLIED_ISSUE_PR_WORKSPACE_AND_PINNED_TRUST_RECORDS_ONLY', 'owner_controls': [c['id'] for c in controls_at(commands, now)], 'stage_budget_minutes': timers['stage_minutes'], 'issues': states}


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
