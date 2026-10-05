# Parent evidence and visible status

Every role publishes two separate comments on the parent issue for every attempt. Link those comments in the child handover and PR description. The role also reports the transition and evidence link to the Owner in its current chat. Do not send unsolicited messages to unrelated chats.

## At START, before taking action

```text
TASK_EVIDENCE — START
Parent: #85 | Child: #XX | PR: #105 (or pending allocation)
Role: CODER / REVIEWER / COORDINATOR | Executor: actual identity
Attempt: 1 | Status: RUNNING | Start: actual UTC timestamp
Budget: Coder 15m / Reviewer 15m / Coordinator 45m

Parent context read through: actual latest comment URL
Earlier instructions/findings carried forward: concrete list
Not applicable to this child: list with reasons, or none
Permission: Coordinator's actual parent grant comment URL
Source/input: actual branch/HEAD and specification basis
Shared folder / access: actual path; WRITE or fixed-source READ_ONLY
Action and intended acceptance: specific scope and criteria
Planned verification: actual checks/observations
Next expected handover: role and conditions
```

START records what is understood and planned; it earns no engineering completion. A Coder must read all old parent comments before each new child/PR, including completed work, unresolved findings, Owner commands and lessons. Record its reconciliation through the observed comment frontier. Read new comments that arrive before actual work begins. A replacement repeats this step.

## At END, after work stops

```text
TASK_EVIDENCE — END
Parent: #85 | Child: #XX | PR: #105
Role: actual role | Executor: actual identity | Attempt: 1
Status: PASS / REWORK / BLOCKED / STALLED / HELD / PAUSED / STOPPED
End: actual UTC timestamp | Actual active time: observed duration

START evidence: earlier parent comment URL
Performed: actual implementation/review/corrections
Files/functions affected: concrete inventory; no diff-based handover
Output and validated HEAD: actual SHAs, or explicit unknown/unvalidated
Verification: named checks, PASS/FAIL/NOT_RUN, evidence and limitations
Findings: resolved/open, including items affecting other children
Unfinished / preserved workspace: actual state
Writer stopped: acknowledged yes; if not yet stopped publish STOP_REQUESTED
Next action: eligible role, repeat required or blocker
Provider state: observed child OPEN/CLOSED; PR DRAFT/OPEN/CLOSED/MERGED
```

An interruption/hold/time budget end also needs an END checkpoint with honest partial results. Minimum acknowledgement bookkeeping is allowed during Hold/Pause. Publication failure is BLOCKED handover until readback confirms the real parent comment. Never post guessed execution evidence or an END that claims completion while its process remains active.

Coder END/PASS makes Reviewer eligible automatically under the existing child permission, stopped-writer acknowledgement and effective Owner controls. Reviewer END/PASS queues Coordinator review if the Coordinator is still busy. Coordinator's review END/PASS may precede merge; publish a parent DELIVERY_RESULT after actual merge and closure observations, so the Owner can distinguish review completion, merged material and closed issues. If review/delivery is one uninterrupted action, its END may summarize both with the observed facts.

## Permission for the next child

```text
COORDINATOR START_PERMISSION
Parent: #85 | Next child: #YY | New PR: pending allocation / #106
Permission: GRANTED | Issued: actual UTC timestamp
While reviewing: #105 at actual fixed HEAD
Basis: dependency-ready, applicable parent findings reconciled
Mode: COORDINATOR_READ_ONLY
Workspace: same authoring folder; previous PR output preserved
Coordinator source: actual immutable full-source snapshot/reference
Coder/Reviewer: one writer at a time; Reviewer eligible after Coder PASS
Restrictions: no competing branch changes or shared mutable test outputs
Owner commands: checked; none blocking, or actual scoped restrictions
Grant by: parent Coordinator identity
Revocation/hold: explicit parent comment if shared writes become necessary
```

Use a SERIAL grant for normal non-overlapping assignment. Permission should normally be granted to an independent next child; if withheld, publish the real dependency/material/Owner-control blocker. Permission is not waiver of acceptance, hard dependencies, Owner commands or actual merge authority.

## One current parent dashboard

```text
Child   PR    Coder    Reviewer  Coordinator  Issue   PR state  Next action
#XX     #105  DONE     DONE      RUNNING      OPEN    DRAFT     Final review
#YY     #106  DONE     RUNNING   NOT_STARTED  OPEN    DRAFT     Reviewer output
#ZZ     #107  DONE     DONE      DONE         CLOSED  MERGED    Delivery recorded
```

These rows are examples. Each actual row also includes the permission URL, latest START/END link, relevant Owner control, role budget, source HEAD and blocker. Update on meaningful transitions, not on heartbeat polls. DONE means that role passed; CLOSED is observed GitHub state, never inferred from a pass or merge. Separate NOT_STARTED, READY, RUNNING, QUEUED, WAITING_PERMISSION, HELD, PAUSED and BLOCKED so absence of a start is visible.

The Coordinator owns the dashboard. Roles own their START and END comments. Publishing START and END, reconciling all old parent comments and refreshing the dashboard are part of action completion.

## V1.1 END production content

Reviewer and Coordinator/Super Reviewer END evidence must distinguish product changes from protected acceptance-surface changes.

Include deliverables, coverage completed, defects fixed in this stage, regressions added, structured acceptance/evidence references, downstream education, external/authority blockers, and exact output SHA.

Do not publish `Coder fix`, `Reviewer investigate`, or equivalent reverse delegation for an internal fixable defect. If a stage cannot continue because of a genuine Owner/external/provider/protected-policy boundary, name that boundary precisely.

When Super Reviewer fixes product behavior, rerun the unchanged pinned project harness. If project protocol/harness/oracle/baseline changes, record a new acceptance basis instead of treating prior evidence as current.
