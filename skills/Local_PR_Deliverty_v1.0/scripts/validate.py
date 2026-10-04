"""Read-only consistency checker for supplied issue/PR records; no Git operations."""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ORDER = ['CODER', 'REVIEWER', 'COORDINATOR']
DEFAULT_BUDGETS = {stage: 30 for stage in ORDER + ['PARENT_CHECK']}
SCHEMAS = {'TASK': 'task', 'STAGE_RECORD': 'stage-record', 'DELIVERY_RESULT': 'delivery-result'}


class RecordError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RecordError(message)


def instant(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timestamp needs a timezone')
    return parsed.astimezone(timezone.utc)


def schema_check(record):
    require(isinstance(record, dict), 'Each record must be an object')
    family = record.get('record')
    require(family in SCHEMAS, 'Unknown record family')
    schema = json.loads((ROOT / 'schemas' / (SCHEMAS[family] + '.schema.json')).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record), key=lambda e: str(e.path))
    require(not errors, '; '.join(e.message for e in errors))


def acceptance_ids(task, required_only=False):
    return {r['id'] for r in task['acceptance'] if not required_only or r['required']}


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


def task_history(task, records, parent, now):
    history = [r for r in records if r['task_id'] == task['task_id']]
    passes, latest, attempts = {}, None, {}
    for record in history:
        stage = record['stage']
        require((stage == 'PARENT_CHECK') == (task['kind'] == 'PARENT'), 'Parent/child stage mismatch')
        require(record['workspace'] == parent['workspace'], 'Every role must use the declared shared folder')
        validate_periods(record, parent, task, now)
        require(record['attempt'] == attempts.get(stage, 0) + 1, 'Attempt numbers must be consecutive within a role')
        attempts[stage] = record['attempt']
        require(record['previous_record'] == (latest['record_id'] if latest else None), 'Broken issue-comment record chain')
        if latest:
            require(latest['writer_stopped'], 'Previous writer has not acknowledged stop')
            require(instant(record['started_at']) >= instant(latest['work_periods'][-1]['end']), 'Shared-folder writers overlapped')
            require(record['handover']['reconciliation'], 'Replacement needs issue/PR/workspace reconciliation')
            if latest['output_sha'] and record['input_sha'] != latest['output_sha'] and task['kind'] == 'CHILD':
                require(record['status'] == 'REWORK', 'External/unexplained HEAD movement requires REWORK reconciliation')
        require(set(record['acceptance_checked']) <= acceptance_ids(task), 'Unknown acceptance ID')
        require(record['spec_digest'] == task['spec_digest'] and record['parent_spec_digest'] == parent['spec_digest'], 'Specification changed; adopt and reconcile the current basis')
        require(len({f['id'] for f in record['findings']}) == len(record['findings']), 'Duplicate finding ID')
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
        for invalidated in record['repeat_stages']:
            require(invalidated in passes, 'repeat_stages must name a previously passing role')
            passes.pop(invalidated)
        if record['status'] == 'PASS':
            require(record['output_sha'] == record['validated_sha'], 'PASS needs the actual validated output SHA')
            require(acceptance_ids(task, True) <= set(record['acceptance_checked']), 'Missing required acceptance coverage')
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
    require(isinstance(bundle, dict) and set(bundle) == {'tasks', 'stages', 'results', 'observed'}, 'Bundle needs tasks, stages, results, observed only')
    require(all(isinstance(bundle[k], list) for k in ['tasks', 'stages', 'results']) and isinstance(bundle['observed'], dict), 'Invalid record collections')
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
    require(len({c['id'] for c in commands}) == len(commands), 'Duplicate Owner command ID')
    require(all(instant(c['issued_at']) <= now for c in commands), 'Future Owner command')
    require(commands == sorted(commands, key=lambda c: instant(c['issued_at'])), 'Owner commands must be chronological')
    require(all(c['child_issue'] is None or c['child_issue'] in declarations for c in commands), 'Command names undeclared child')
    timers = dict(parent['timers'], stage_minutes=dict(parent['timers']['stage_minutes']))
    if timers['stage_minutes'] != DEFAULT_BUDGETS or timers['ci_wait_minutes'] != 30:
        require(timers['override_reason'], 'Timer override needs an Owner reason')
    for command in commands:
        if command['command'] == 'TIMER':
            timers['stage_minutes'] = {s: command['minutes'] for s in DEFAULT_BUDGETS}
            timers['ci_wait_minutes'] = command['minutes']
    if parent['merge_authority']['mode'] == 'DELEGATED':
        require(parent['merge_authority']['reference'], 'Delegated authority needs an actual Owner instruction')
    for task in tasks.values():
        require(len(acceptance_ids(task)) == len(task['acceptance']), 'Duplicate acceptance ID')
        require(task['repository'] == parent['repository'] and task['parent_owner'] == parent['parent_owner'] and task['protocol_ref'] == parent['protocol_ref'], 'Inconsistent parent identity/basis')
        if task['kind'] == 'CHILD':
            require(task['issue'] in declarations and task['parent_issue'] == parent['issue'], 'Undeclared child')
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
    history = {key: task_history(task, bundle['stages'], parent, now) for key, task in tasks.items()}
    active = [r for r, _ in history.values() if r and not r['writer_stopped']]
    require(len(active) <= 1, 'More than one shared-folder writer')
    observations = bundle['observed']
    intervals = sorted((instant(p['start']), instant(p['end']) if p['end'] else now, r['record_id']) for r in bundle['stages'] for p in r['work_periods'])
    require(all(left[1] <= right[0] for left, right in zip(intervals, intervals[1:])), 'Shared-folder stage execution periods overlapped')
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
        recorded = instant(result['recorded_at'])
        require(instant(final['work_periods'][-1]['end']) <= recorded <= now, 'Result timing invalid')
        require(not blocking_control(commands, task, 'COORDINATOR', recorded), 'Owner command blocks delivery publication/advancement')
        if task['kind'] == 'CHILD':
            require(all(s in passes for s in ORDER) and task['pr'] == result['pr'], 'Child delivery lacks full role chain')
            merge = observations.get('merged', {}).get(str(result['pr']))
            require(merge and merge.get('head_sha') == result['head_sha'] and merge.get('merge_commit_sha') == result['merge_commit_sha'], 'Provider merge observation missing/mismatched')
            merged_at = instant(merge['merged_at'])
            require(instant(final['work_periods'][-1]['end']) <= merged_at <= recorded, 'Merge/result timing invalid')
            require(not blocking_control(commands, task, 'COORDINATOR', merged_at), 'Merge occurred under Owner control')
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
                if not current or workspace.get('path') != parent['workspace'] or workspace.get('head_sha') != head or workspace.get('unrecorded_changes') is not False:
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
                    elif not observations.get('merge_authority_refs', {}).get(pr):
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
