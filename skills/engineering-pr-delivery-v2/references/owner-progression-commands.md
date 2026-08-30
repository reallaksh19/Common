# Owner Progression Commands — exactly three supported forms

## 1. Control surface

For ordinary bounded progression, the protocol recognizes exactly these three Owner commands:

```text
proceed next
proceed next, no Qs
proceed next, hand over ready
```

Do not invent aliases such as `continue without questions`, `handover mode`, `refresh questions now`, or a fourth progression mode. Other Owner instructions may define task/scope/merge/roadmap authority, but these three phrases alone control normal progression/question/handover behavior.

Internal state may be richer; the Owner control surface stays simple.

## 2. Shared preconditions

All three commands still require:

```text
current Owner instruction/task scope
current Common protocol
valid work-item custody
applicable Owner Roadmap(s) / source / benchmark authority
current PR/main/drift reconciliation
validation truth preserved as PASS/FAIL/NOT_RUN/NOT_APPLICABLE
no unauthorized merge/roadmap/source/oracle mutation
```

The commands change question/handover behavior only. They do not waive engineering/source/roadmap/merge authority.

Internal fields:

```text
OWNER_PROGRESSION_COMMAND:
  PROCEED_NEXT |
  PROCEED_NEXT_NO_QS |
  PROCEED_NEXT_HANDOVER_READY

QUALIFICATION_SCOPE_ID:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT | STALE | NOT_APPLICABLE
QUESTION_PACK_ACTION: REUSED | REFRESHED | SUPPRESSED_BY_OWNER | NOT_APPLICABLE
QUESTION_DISPLAY: SHOW | HIDE
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
```

`CHAIN_HANDOVER_READY` means engineering/task/inputs/benchmarks/roadmaps/PR/exact-next-action custody is recoverable from durable state.

`TAKEOVER_QUALIFICATION_READY` means a replacement can immediately enter question-set admission/qualification with a valid current Q-set.

They are intentionally separate.

## 3. `proceed next`

Meaning:

```text
continue one bounded engineering progression
reuse current qualification pack while its scope remains valid
refresh only when the qualification scope materially changes or the current set is stale
hide unchanged questions
show full questions only when refreshed
```

State rules:

```text
OWNER_PROGRESSION_COMMAND: PROCEED_NEXT

same scope + Q set CURRENT
→ QUESTION_PACK_ACTION: REUSED
→ QUESTION_DISPLAY: HIDE
→ TAKEOVER_QUALIFICATION_READY: TRUE

scope changed OR Q set STALE
→ QUESTION_PACK_ACTION: REFRESHED
→ QUESTION_DISPLAY: SHOW
→ QUESTION_SET_STATUS: CURRENT
→ TAKEOVER_QUALIFICATION_READY: TRUE
```

A normal status/PR/read-only re-ground does not itself force a question refresh.

## 4. `proceed next, no Qs`

Meaning:

```text
continue one bounded engineering progression
DO NOT create or refresh questions
DO NOT display questions
preserve existing Q-set artifact unchanged
```

State rules:

```text
OWNER_PROGRESSION_COMMAND: PROCEED_NEXT_NO_QS
QUESTION_PACK_ACTION: SUPPRESSED_BY_OWNER
QUESTION_DISPLAY: HIDE
```

If the existing set still covers the current qualification scope:

```text
QUESTION_SET_STATUS: CURRENT
TAKEOVER_QUALIFICATION_READY: TRUE
```

If the bounded progression crosses beyond existing qualification coverage:

```text
QUESTION_SET_STATUS: STALE
TAKEOVER_QUALIFICATION_READY: FALSE
```

The current custodian may complete that one Owner-authorized bounded progression if all non-question authority gates remain clear. The next agent may not take write custody from a stale/deferred set; takeover first requires independently authored/adopted current questions.

This command does not authorize indefinite AUTO progression across multiple uncovered qualification scopes. It applies to the requested bounded progression only.

A stale question set must never be silently described as current merely because the Owner suppressed Q generation.

## 5. `proceed next, hand over ready`

Meaning:

```text
continue one bounded engineering progression
then freeze a complete takeover-ready checkpoint
ensure Q-set is current
show full Q1-Q5
synchronize all durable issue/repository handover state
stop at the checkpoint
```

Required final state:

```text
OWNER_PROGRESSION_COMMAND: PROCEED_NEXT_HANDOVER_READY
QUESTION_SET_STATUS: CURRENT
QUESTION_PACK_ACTION: REUSED | REFRESHED
QUESTION_DISPLAY: SHOW
CHAIN_HANDOVER_READY: TRUE
TAKEOVER_QUALIFICATION_READY: TRUE
```

For GitHub-Issue work additionally require:

```text
ISSUE_HANDOVER_SYNC_STATUS: IN_SYNC
```

Before stopping, reconcile:

```text
original task / acceptance ledger
input ledger
benchmark/oracle ledger
Owner/other roadmap ledger and drift
PR status / mergeability / reviews / unresolved threads / required checks
engineering/custody/qualification/write/AUTO state
validation truth
exact next action
current full Q1-Q5
repository endpoint/material receipt
Issue endpoint checkpoint + Active Handover comment when applicable
```

If any required takeover-ready component cannot be validated/synchronized, report the exact blocker and keep the applicable readiness flag FALSE. Do not claim handover-ready merely because the Owner requested it.

## 6. Qualification scope

Questions are bound to a qualification scope, not to every endpoint or commit:

```text
QUALIFICATION_SCOPE_ID: QSCOPE-<work-item>-<engineering-boundary>
```

One current pack may be reused across many endpoints/material batches while all of these remain materially within coverage:

```text
work item / Issue Basis
Owner-roadmap intent
engineering authority boundary
source/oracle authority
technical competency boundary
```

A material change to one of those boundaries makes the old set stale unless an independent coverage rule explicitly retains it.

## 7. Reporting behavior

### `proceed next`

User-visible response:

```text
# Active handover snapshot
...
Qualification:
Scope: <QSCOPE>
Question set: <ID>
Status: CURRENT
This turn: REUSED | REFRESHED
Takeover qualification ready: TRUE

[If REFRESHED only]
## Active qualification questions
Q1 ... Q5 ...

## Changed this turn
...
```

### `proceed next, no Qs`

User-visible response:

```text
# Active handover snapshot
...
Qualification:
Question refresh: SUPPRESSED_BY_OWNER
Existing set: <ID | NONE>
Coverage: CURRENT | STALE | NOT_APPLICABLE
Takeover qualification ready: TRUE | FALSE

## Changed this turn
...
```

Never generate or display Q1-Q5 in this mode.

### `proceed next, hand over ready`

User-visible response:

```text
# Active handover snapshot
...
Chain handover ready: TRUE | FALSE
Takeover qualification ready: TRUE | FALSE

## Active qualification questions
Q1 ...
Q2 ...
Q3 ...
Q4 ...
Q5 ...

## Changed this turn
...
```

Full questions are mandatory here when takeover qualification is ready.

## 8. Decision table

| Command | Work | Q refresh | Q display | Required final takeover-ready state |
|---|---|---|---|---|
| `proceed next` | one bounded progression | only if scope/set requires | only if refreshed | no forced freeze |
| `proceed next, no Qs` | one bounded progression | forbidden | forbidden | may be FALSE if Q coverage became stale |
| `proceed next, hand over ready` | one bounded progression then stop | ensure current | full Q1-Q5 | must be TRUE or exact blocker reported |

No fourth progression-command state is valid.