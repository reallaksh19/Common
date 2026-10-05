"""Forward-only production stages, parent evidence, permissions and safe Coordinator overlap."""
from datetime import datetime, timezone
from urllib.parse import urlparse


class RecordError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RecordError(message)


def instant(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timestamp needs a timezone')
    return parsed.astimezone(timezone.utc)


def parent_comment(reference, parent):
    parsed = urlparse(reference)
    return parsed.path.rstrip('/').endswith('/issues/' + str(parent['issue'])) and bool(parsed.fragment)


def permission_at(parent, child_issue, at):
    latest = next((p for p in reversed(parent['start_permissions']) if p['child_issue'] == child_issue and instant(p['issued_at']) <= at), None)
    return latest if latest and (latest['revoked_at'] is None or at < instant(latest['revoked_at'])) else None


def validate_evidence(record, parent, task, bundle_observations, now):
    start = record['publications']['start']
    started = instant(record['started_at'])
    context = record['parent_context']
    require(instant(context['read_at']) <= instant(start['published_at']) <= started, 'Read parent context and publish START before action')
    require(parent_comment(start['comment_ref'], parent), 'START evidence must be a comment on the parent issue')
    require(parent_comment(context['through_comment_ref'], parent), 'Parent context must identify the last reconciled parent comment')
    end = record['publications']['end']
    if end is not None:
        require(record['writer_stopped'], 'END cannot claim an action finished while it remains active')
        stopped = instant(record['work_periods'][-1]['end'])
        require(stopped <= instant(end['published_at']) <= now, 'Publish END after the action actually stopped')
        require(parent_comment(end['comment_ref'], parent) and end['comment_ref'] != start['comment_ref'], 'START and END need distinct parent comments')
    else:
        require(not record['writer_stopped'], 'Stopped action must publish parent END evidence')
    if bundle_observations is not None:
        frontier = bundle_observations.get('parent_comment_frontiers', {}).get(record['record_id'])
        require(frontier and frontier['comment_ref'] == context['through_comment_ref'], 'Action missed the observed parent comment frontier')
        require(instant(frontier['observed_at']) <= instant(context['read_at']), 'Parent reconciliation predates its comment read')
    if record['stage'] in ['CODER', 'REVIEWER']:
        grant = permission_at(parent, task['issue'], started)
        require(grant, 'Coder/Reviewer needs the existing Coordinator child permission')
        if record['stage'] == 'CODER':
            require(instant(grant['issued_at']) <= instant(context['read_at']), 'Coder must reread parent comments after permission')
    if record['status'] == 'PASS' and task['kind'] == 'CHILD':
        require(task['pr'] is not None, 'Each child needs its own PR before Coder can pass')


def validate_pipeline(parent, tasks, records, observations, now):
    require(all(value in ['OPEN', 'CLOSED'] for value in observations.get('issue_states', {}).values()), 'Invalid observed issue state')
    require(all(value in ['DRAFT', 'OPEN', 'CLOSED', 'MERGED'] for value in observations.get('pr_states', {}).values()), 'Invalid observed PR state')
    permissions = parent['start_permissions']
    require(len({p['id'] for p in permissions}) == len(permissions), 'Duplicate start permission ID')
    require(permissions == sorted(permissions, key=lambda p: instant(p['issued_at'])), 'Permissions must be chronological')
    declared = {c['issue'] for c in parent['children']}
    record_map = {r['record_id']: r for r in records}
    child_prs = [t['pr'] for t in tasks.values() if t['kind'] == 'CHILD' and t['pr'] is not None]
    require(len(child_prs) == len(set(child_prs)), 'Every child must have a different PR')
    refs = []
    for record in records:
        refs.append(record['publications']['start']['comment_ref'])
        if record['publications']['end']:
            refs.append(record['publications']['end']['comment_ref'])
    require(len(refs) == len(set(refs)), 'Role START/END publications need distinct parent comments')
    for grant in permissions:
        require(grant['coordinator'] == parent['parent_owner'] and grant['child_issue'] in declared, 'Permission must come from parent Coordinator for a declared child')
        require(parent_comment(grant['parent_comment_ref'], parent), 'Permission must be published on parent issue')
        issued = instant(grant['issued_at'])
        require(issued <= now and (grant['revoked_at'] is None or issued <= instant(grant['revoked_at']) <= now), 'Invalid permission timing')
        if grant['mode'] == 'SERIAL':
            require(grant['during_record'] is None and grant['reviewed_head_sha'] is None, 'Serial assignment has no overlapping review record')
        else:
            coordinator = record_map.get(grant['during_record'])
            require(coordinator and coordinator['stage'] == 'COORDINATOR' and coordinator['workspace_mode'] == 'READ_ONLY', 'Overlap permission needs a pinned read-only Coordinator review')
            require(tasks[coordinator['task_id']]['issue'] != grant['child_issue'], 'Overlap permission must target a different child')
            require(grant['reviewed_head_sha'] == coordinator['input_sha'], 'Permission names wrong Coordinator input')
            end = instant(coordinator['work_periods'][-1]['end']) if coordinator['writer_stopped'] else now
            require(instant(coordinator['started_at']) <= issued <= end, 'Permission must be issued during stated Coordinator review')
    for record in records:
        if record['workspace_mode'] == 'READ_ONLY':
            require(record['stage'] == 'COORDINATOR' and record['review_source'], 'Only Coordinator may use overlapping read-only review mode')
            require(record['review_source']['head_sha'] == record['input_sha'], 'Coordinator needs immutable source at reviewed input SHA')
            require(record['output_sha'] is None or record['output_sha'] == record['input_sha'], 'Read-only Coordinator cannot modify reviewed output')
    for index, left in enumerate(records):
        left_start = instant(left['started_at'])
        left_end = instant(left['work_periods'][-1]['end']) if left['writer_stopped'] else now
        for right in records[index + 1:]:
            right_start = instant(right['started_at'])
            right_end = instant(right['work_periods'][-1]['end']) if right['writer_stopped'] else now
            if max(left_start, right_start) >= min(left_end, right_end):
                continue
            readonly = left if left['workspace_mode'] == 'READ_ONLY' else right
            writer = right if readonly is left else left
            require(readonly['workspace_mode'] == 'READ_ONLY' and readonly['stage'] == 'COORDINATOR' and writer['workspace_mode'] == 'WRITE' and writer['stage'] in ['CODER', 'REVIEWER'], 'Only one pinned read-only Coordinator may overlap one Coder/Reviewer product writer; Coordinator fixes require exclusive WRITE use')
            require(readonly['task_id'] != writer['task_id'], 'Concurrent review and writing must concern different children')
            grant = permission_at(parent, tasks[writer['task_id']]['issue'], right_start if writer is right else left_start)
            require(grant and grant['mode'] == 'COORDINATOR_READ_ONLY' and grant['during_record'] == readonly['record_id'], 'Concurrent work lacks recorded Coordinator permission')
    workspace = observations.get('workspace', {})
    if workspace.get('unrecorded_changes') is False:
        require(workspace.get('path') == parent['workspace'], 'Observed workspace must match common folder')


def status_details(states, tasks, history, observations, now, parent, results):
    active_coordinators = [r for r, _ in history.values() if r and r['stage'] == 'COORDINATOR' and not r['writer_stopped']]
    active_writers = [r for r, _ in history.values() if r and r['workspace_mode'] == 'WRITE' and not r['writer_stopped']]
    for key, task in tasks.items():
        state = states[str(task['issue'])]
        latest, passes = history[key]
        roles = {role.lower(): 'DONE' if role in passes else 'NOT_STARTED' for role in ['CODER', 'REVIEWER', 'COORDINATOR']}
        if latest and latest['stage'] in ['CODER', 'REVIEWER', 'COORDINATOR'] and latest['status'] != 'PASS':
            roles[latest['stage'].lower()] = state['status']
        if state['stage'] in ['CODER', 'REVIEWER', 'COORDINATOR'] and state['status'] == 'READY':
            roles[state['stage'].lower()] = 'READY'
        if task['kind'] == 'CHILD' and not latest:
            grant = permission_at(parent, task['issue'], now)
            if state['status'] == 'READY' and not grant:
                state['status'] = 'WAITING_PERMISSION'
                roles['coder'] = 'WAITING_PERMISSION'
        if task['kind'] == 'CHILD' and state['stage'] in ['CODER', 'REVIEWER'] and state['status'] == 'READY':
            grant = permission_at(parent, task['issue'], now)
            if not grant:
                state['status'] = 'WAITING_PERMISSION'
            elif any(r['task_id'] != key for r in active_writers):
                state['status'] = 'QUEUED'
            elif any(r['task_id'] != key for r in active_coordinators) and not any(grant['mode'] == 'COORDINATOR_READ_ONLY' and grant['during_record'] == r['record_id'] for r in active_coordinators):
                state['status'] = 'WAITING_PERMISSION'
            roles[state['stage'].lower()] = state['status']
        if task['kind'] == 'CHILD' and state['stage'] == 'COORDINATOR' and state['status'] == 'READY' and any(r['task_id'] != key for r in active_coordinators):
            state['status'] = 'QUEUED'
            roles['coordinator'] = 'QUEUED'
        state.update(roles)
        state['issue_state'] = observations.get('issue_states', {}).get(str(task['issue']), 'UNKNOWN')
        state['pr_state'] = observations.get('pr_states', {}).get(str(task['pr']), 'UNKNOWN') if task['pr'] else 'NONE'
        evidence = (latest['publications']['end'] or latest['publications']['start']) if latest else None
        state['last_parent_evidence'] = evidence['comment_ref'] if evidence else None
        if key in results:
            state['last_parent_evidence'] = results[key]['parent_comment_ref']
        grant = permission_at(parent, task['issue'], now) if task['kind'] == 'CHILD' else None
        state['start_permission'] = grant['parent_comment_ref'] if grant else None
        state['next_action'] = latest['next_action'] if latest else 'Coordinator publishes permission; Coder rereads entire parent history.'
        if key in results and state['issue_state'] == 'OPEN':
            state['next_action'] = 'Verify acceptance/closure authority, then close and publish observed issue state.' if results[key]['responsibility_complete'] else 'Keep open; resolve remaining acceptance.'
        if task['kind'] == 'PARENT':
            state.update(coder='NOT_APPLICABLE', reviewer='NOT_APPLICABLE', coordinator='DONE' if 'PARENT_CHECK' in passes else state['status'])
            if not latest:
                state['next_action'] = 'Coordinator maintains child permissions, evidence and status; run Parent Check after every child completes.'
