# V3.1 agent task publication lifecycle

## Purpose

Define the normal durable interaction between an engineering agent, its owned child issue, V3.1 recording, the programme Handover ledger and the coordinator.

This is a reconstruction protocol, not an execution gate.

## End-to-end lifecycle

```text
PROGRAMME PARENT
governing human/programme contract
        │
        ▼
CHILD IMPLEMENTATION ISSUE
bounded engineering responsibility
        │
        ▼
THREE-PASS PACKET
independent reasoning + current reality + direction
        │
        ▼
AGENT LIVE REFRESH
confirm current source truth/material
        │
        ▼
IMPLEMENTATION_PLAN rev 1
agent-authored, posted durably on the child issue
        │
        ├────► V3.1 observes/binds current plan to task snapshot
        │
        └────► existing/new EP identifies the bounded responsibility
                  │
                  ▼
              EXECUTION
                  │
          ┌───────┼────────┐
          ▼       ▼        ▼
     PLAN_UPDATE TASK_EVIDENCE PR/TEST/ARTIFACT
          │       │        │
          └───────┼────────┘
                  ▼
            TASK_RESULT
                  │
                  ▼
       [Relay Handover] ledger
        indexes plan/material/result
                  │
                  ▼
             COORDINATOR
        EXPECTED → OBSERVED → CONSEQUENCE
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
     consumer  later check  Owner only if needed
```

## 1. Child issue is the task home

For new multi-agent programmes:

- the **programme parent** carries the governing programme contract;
- the **child implementation issue** carries the bounded engineering responsibility;
- the agent publishes its implementation plan and task evidence on that child issue;
- the dedicated **[Relay Handover]** child indexes the current programme-wide operational picture.

In V3.1 terms, a new EP may therefore carry:

```yaml
programme_parent:
  repository: owner/repo
  number: 210
  ...

parent_issue:
  repository: owner/repo
  number: 232
  ...
```

For compatibility, older EPs may have only `parent_issue`; V3.1 then treats that issue as both work issue and programme parent for reconstruction.

## 2. Three-pass is reasoning, not the implementation plan

A three-pass packet gives the agent:

- programme contribution view;
- independent situated problem view;
- verified current reality;
- reconciled direction;
- revalidated move-forward reasoning.

It does **not** choose the final implementation details for the engineering agent.

After Prompt 3 refreshes live reality, the incoming agent writes its own implementation plan.

## 3. First durable agent publication — IMPLEMENTATION_PLAN

Normal expectation:

> After live revalidation and before substantial material modification, publish `IMPLEMENTATION_PLAN — rev 1` on the owned child implementation issue.

This is a strong reconstruction convention, not permission.

If useful implementation/investigation already happened before the plan was posted, the work remains valid. Publish the current plan as soon as practical and continue.

Do not wait for Relay/coordinator approval after publishing the plan.

Recommended shape:

```text
IMPLEMENTATION_PLAN — rev 1

BASIS
- exact current main/head
- relevant parent programme basis
- three-pass packet ref, when used

MY UNDERSTANDING
What I believe the real engineering problem is.

OWNED OUTCOME
What I intend to make true.

SOURCE TRUTH
What I inspected and which source is authoritative.

APPROACH
The implementation strategy I currently intend to use.

EXPECTED CHANGED SURFACES
Files/components/interfaces likely to change.

DEPENDENCIES
Required production outputs from other workstreams.

INDEPENDENT WORK
What can proceed even if those outputs are not yet available.

FALSIFIER
What would prove this plan unnecessary, wrong or differently scoped.

VALIDATION
Focused tests/oracles/runtime/browser evidence.

PRESERVE
Existing behavior/contracts that must remain true.

UNCERTAINTIES
What is not yet known.

EXPECTED NEXT OBSERVABLE
The next concrete evidence a coordinator should expect.

CONSUMER / HANDOFF
Who needs the result and what they need from it.
```

## 4. EP role

An EP is V3.1's bounded task/execution identity.

It is **not** the agent's implementation plan and does not replace the child issue.

One meaningful engineering responsibility should normally map to one EP, not one EP per command/file/test.

Do not create nano-EPs for:

- inspect file;
- edit helper;
- run test;
- post issue comment;
- create PR.

A new EP is appropriate when the owned engineering responsibility materially changes or a distinct follow-up/revision becomes a new task.

### Plan timing relative to EP

The preferred new-task sequence is:

```text
child responsibility
→ agent plan
→ V3.1 records/binds EP + plan basis
→ execution
```

But an EP may already exist before an incoming agent publishes its plan, for example when a three-pass/handover packet was prepared from existing V3.1 context.

In that case:

```text
existing EP
→ incoming agent publishes plan
→ TASK_SNAPSHOT/Handover observes current plan ref/revision
```

Do **not** create a replacement EP merely because the implementation plan was first published or revised.

## 5. Plan revisions — PLAN_UPDATE

A material implementation-learning change stays on the same task/EP when responsibility remains the same.

Publish:

```text
PLAN_UPDATE — rev N

CHANGED BECAUSE
New evidence.

PREVIOUS ASSUMPTION
What was wrong/incomplete.

NEW APPROACH
What changes.

UNCHANGED
Outcome, ownership boundary, invariants and consumer contract that remain stable.

EXPECTED NEXT OBSERVABLE
What the coordinator should now expect.
```

Use a new EP/child only if the engineering responsibility itself has materially changed.

## 6. Meaningful intermediate evidence — TASK_EVIDENCE

Do not post every action.

Post a durable evidence update when it changes reconstruction or another workstream's next action.

```text
TASK_EVIDENCE

OBSERVED AT
...

EXACT HEAD / BASIS
...

CLAIM
...

EVIDENCE
...

RESULT
PASS | FAIL | NOT_RUN | OBSERVED

CONSEQUENCE
...

DEPENDENCY DISCOVERED
NONE | <missing production truth>

PLAN CONSEQUENCE
NONE | PLAN_UPDATE required
```

Useful triggers include:

- falsifier result;
- newly discovered production dependency;
- consumer-ready producer output;
- important verified negative result;
- runtime/browser evidence that materially changes the plan;
- local/helper result that now matters outside the local workstream.

Routine chatter is not a publication requirement.

## 7. Delivery / handoff — TASK_RESULT

At the meaningful task delivery boundary publish:

```text
TASK_RESULT

OUTCOME
ACHIEVED | PARTIAL | FALSIFIED

EXACT MATERIAL
branch
PR
base
head

CHANGED SURFACES
path/component → purpose

VALIDATION
command/oracle → result

PROVED
...

NOT PROVED
...

KNOWN LIMITATIONS
...

NEGATIVE ASSURANCE
What intentionally did not change.

CONSUMER CONSEQUENCE
Which downstream work can now consume what.

REMAINING DEPENDENCY
...

NEXT
...
```

The PR/commit/test/artifact is the material truth. The comment is the durable semantic handoff/index.

## 8. V3.1 read models

V3.1 may observe the child issue and expose in `TASK_SNAPSHOT`:

```text
programme_parent
parent_issue / work issue
planning.state
planning.provider_ref
planning.revision
planning.digest
planning.observed_at
planning.expected_next_observable
task_publications[]
```

Plan state is:

```text
PRESENT
MISSING
STALE
UNKNOWN
```

A missing/stale plan is reconstruction debt only.

## 9. [Relay Handover] programme ledger

The programme Handover ledger should index each EP/workstream with:

- child work issue;
- plan state/ref/revision;
- expected next observable;
- branch/PR/exact-head material where available;
- latest meaningful task publications;
- dependency/output consequences;
- current task result/handoff.

It should not duplicate full implementation-plan prose.

## 10. Coordinator use

The coordinator watches **expectations**, not agent activity.

```text
EXPECTED
What concrete evidence did the plan say should appear next?

OBSERVED
What durable material/evidence actually exists?

CONSEQUENCE
What changes for this task, another workstream, the plan, the Owner, or the next observation?
```

Examples:

- plan published → expect focused falsifier/PR;
- producer result landed → route to consumer immediately;
- plan changed → retire obsolete timer and watch new expected observable;
- session disappeared → reconstruct from child issue + plan + EP + PR/head/evidence;
- no meaningful change → do nothing.

## 11. Non-blocking invariant

None of the following is engineering permission:

- plan presence;
- plan revision;
- EP state;
- Handover freshness;
- task-publication count;
- timer state;
- coordinator observation;
- V3.1 lease/checkpoint/control state.

Actual production constraints come from source truth, the engineering problem, evidence/tests/runtime, human decisions and real provider permissions.

## 12. V3.1 only

Use Engineering Relay V3.1 only for current recorder/reconstruction/reporting semantics.

Do not use V3 or V2.5 as live coordination, recovery, gating, handover or Owner-command protocols.
