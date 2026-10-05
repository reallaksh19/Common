# AGENT_STATUS_V1 template

One mutable provider comment per execution custody epoch.

```text
AGENT_STATUS_V1
AUTHORITY: DERIVED_EXECUTION_CONTINUITY
```

This is **not** a fifth engineering task publication. It is a mutable continuity/readback surface only.

Material Git/PR/test/runtime truth and the four typed engineering publications outrank stale status.

## Required shape

```text
AGENT_STATUS_V1

AGENT
executor: <agent/runtime>
custody_epoch: <integer>
continuation: NEW | HANDOFF | RECOVERY
status: ACTIVE | HANDOFF_READY | COMPLETE | SUPERSEDED | BLOCKED

PROTOCOL BASIS
V3.1
Common@<sha>
TPG-2P-<revision>

RESPONSIBILITY
issue: #<owned issue>
ep: <EP | NONE>
work_package: <WP | NONE>

PLAN
implementation_plan: <ref | NONE>
plan_revision: <n | NONE>
latest_plan_update: <ref | NONE>
latest_task_evidence: <ref | NONE>
latest_task_result: <ref | NONE>

MATERIAL
branch: <branch | NONE>
primary_pr: <PR | NONE>
base: <sha/ref | NONE>
head: <sha | NONE>

CURRENT
<one concise current execution statement>

## Completed
<recent meaningful completed STEP/FT items + evidence refs>

## Further task
<ordered unresolved FT-* items>

## Pending / blocked
<structured PEND-* items>

## Reasoning refs
<CX-* / reconciliation refs only; no transcript body>

## Local Agent / OFFLOAD
<index existing OFFLOAD/provider issue state only>

## RLL
<index RLL transport state only>

## Delivery
<PR lifecycle / relationship / related stack>

## Negative knowledge
<do-not-reopen facts>

## Handover
predecessor_status_ref: <ref | NONE>
successor_first_action:
1. ...
```

## Further-task identity

Use `FT-<issue>-<serial>` only for continuity/readback.

FT-* does not replace:
- STEP-*;
- AC-*;
- EXIT-*;
- EP/WP;
- OFFLOAD-*.

Allowed states:

```text
PENDING
ACTIVE
BLOCKED
DONE
SUPERSEDED
NOT_APPLICABLE
```

A successor must revalidate every unresolved FT-* item against live provider/material truth before continuing.

## Custody epochs

- first executor: `continuation: NEW`;
- graceful successor: new comment, `continuation: HANDOFF`, predecessor ref set;
- abrupt-loss successor: new comment, `continuation: RECOVERY`, predecessor ref set.

A successor never edits the vanished predecessor's AGENT_STATUS_V1.

## Update at semantic boundaries

Update the same current-epoch comment when:
- session starts/resumes;
- implementation plan/plan update changes current route;
- primary PR is created;
- meaningful FT item completes;
- exact material head becomes a new evidence/review candidate;
- blocker/dependency changes;
- Local Agent/OFFLOAD returns or is dispatched;
- RLL transport state meaningfully changes;
- formal handover begins;
- TASK_RESULT publishes;
- responsibility becomes COMPLETE/SUPERSEDED.

Do not update for routine file reads, commands, timer wakes, lease renewals, repeated retries, or conversational acknowledgements.
