# Engineering Relay V3.5 — checkpoint + liveness contract seed

## Status

`engineering-pr-delivery-v3.5` does not yet exist as a complete invocable protocol in `Common`.

This file is a **candidate design contract** for the future V3.5 line. It MUST NOT be treated as an active protocol selector, a complete replacement for V3.2, or authority to fabricate missing V3.5 schemas/scripts/tests.

When V3.5 is created, this contract is intended to be incorporated mechanically into its normative `SKILL.md`, continuity schema, provider projection, tests and replay corpus.

## Governing problem

A recurring failure mode is:

```text
useful inspection / reconstruction
→ useful code or test work
→ material/semantic frontier advances
→ stream/tool/session failure
→ latest durable GitHub state is materially behind the work that actually occurred
→ Owner says "continue"
→ successor/current executor must reconstruct too much transient state
```

The target is not periodic heartbeat ceremony. The target is **bounded recovery distance plus visible Owner observability**.

V3.5 therefore separates four axes:

```text
P = semantic production progress
E = successor-safe evidenced progress
A = meaningful activity/checkpoint epoch
L = derived liveness/motion state
```

No axis may be inferred from another.

## V3.5 checkpoint-before-continue invariant

> After a checkpoint threshold is crossed, the executor MUST durably reconcile current truth, update the configured GitHub projection, verify provider readback, and surface checkpoint evidence to the Owner before starting the next substantial work unit.

This is a write-ahead continuity barrier.

It is not:

- progress by elapsed time;
- a periodic heartbeat;
- a new approval gate;
- evidence that a unit is complete merely because activity occurred;
- permission for provider state to overwrite Git/PR/test/runtime truth.

## Required checkpoint triggers

### 1. Semantic/evidence frontier movement

Checkpoint before continuing when any of the following occurs:

- a declared implementation unit completes;
- P or E changes;
- a root cause/blocker is established and changes the next action;
- an architecture decision is established;
- a material finding is discovered or resolved;
- important negative knowledge is established that a successor would otherwise have to rediscover;
- a candidate/material frontier change materially increases reconstruction distance;
- a meaningful validation/benchmark/browser/external-oracle batch completes.

These checkpoints use the existing publication family:

```text
TASK_EVIDENCE — CHECKPOINT
```

No fifth task-publication family is introduced.

### 2. Substantial activity without semantic completion

Default activity thresholds:

```text
READ / RECONSTRUCTION
- >= 3000 NEW substantive source/document lines; OR
- >= 8 NEW meaningful files; OR
- one complete subsystem/interface boundary reconstructed.

CODE / EDIT
- >= 250 newly authored reviewable lines; OR
- >= 400 materially modified reviewable lines.

HARD CHECKPOINT CEILING
- >= 500 newly authored reviewable lines; OR
- >= 700 materially modified reviewable lines.
```

Project profiles may choose stricter thresholds.

Repeated rereads, unchanged failing-test reruns, generic tool calls, token generation, comments and elapsed time do not renew meaningful activity by themselves.

Activity-only checkpoints:

- increment `A<n>`;
- refresh current provider projection;
- leave P/E unchanged unless progress semantics independently changed;
- need not create a durable GitHub comment if no successor-relevant semantic/evidence truth advanced;
- must still be surfaced to the Owner in chat when Owner-visible checkpoint mode is active.

### 3. Pre-risk checkpoint

Before a higher interruption/latency-risk operation, checkpoint any meaningful uncheckpointed state.

Examples:

```text
long test suite
benchmark corpus run
browser automation
large build/static analysis
external oracle/service invocation
large repository traversal
large patch generation
branch switch/rebase/history rewrite
provider mutation
other interruption-prone tool operation
```

## Owner-visible checkpoint mode

V3.5 should support an explicit responsibility setting:

```text
CHECKPOINT_VISIBILITY_MODE = BEST_EFFORT | OWNER_REQUIRED
```

For `OWNER_REQUIRED`, the barrier order is:

```text
1. OBSERVE exact live material/provider state
2. RECONCILE current unit, findings, negative knowledge and frontiers
3. RECALCULATE P/E honestly and advance A only for valid activity
4. SYNC GitHub current-state + issue-title projection
5. READ BACK provider state
6. SURFACE TASK_EVIDENCE checkpoint in chat
7. CONTINUE to the next substantial work unit
```

If provider synchronization/readback fails:

```text
WAITING_PROVIDER_VISIBILITY
```

must be surfaced. The executor MUST NOT silently cross an Owner-required checkpoint barrier. An explicit Owner waiver may relax the visibility barrier for that responsibility; such a waiver affects observability only and cannot manufacture progress or acceptance.

## GitHub issue title projection

Recommended compact projection:

```text
🟢 {P42% · E31% · A07 · U03 · ACTIVE} <issue title>
```

Where:

```text
P42 = objectively complete declared units
E31 = completed units with durable successor-safe evidence
A07 = seventh valid activity/checkpoint epoch
U03 = active declared unit
ACTIVE = liveness/motion projection
```

The issue title is disposable projection, never authority.

## Liveness states

Recommended provider states:

```text
🟢 ACTIVE
  meaningful recent activity + recent frontier movement

🟡 QUIET
  meaningful activity exists, but frontier movement has stalled

🔴 STALE
  external watcher/provider observer detects expired activity state

🔵 WAITING
  explicit named wait on CI/tool/external dependency

✅ COMPLETE
  responsibility ended normally
```

A dead executor cannot mark itself STALE. Reliable dead-agent detection therefore requires an **external watcher** or provider-side observer.

One missed observation must not prove death. V3.5 should support a configurable missed-observation/failure threshold before STALE.

## Activity lease

V3.5 should add a lightweight derived liveness record, separate from task publications:

```yaml
activity_lease:
  authority: DERIVED_LIVENESS_ONLY
  responsibility: <id>
  executor_epoch: <id>
  activity_epoch: 7
  work_state: WORKING
  renewed_at: <timestamp>
  last_activity_kind: SOURCE_READ_BATCH
  last_frontier_advance_at: <timestamp>
  p: 42
  e: 31
  expected_quiet_until: null
```

The activity lease is mutable operational state. It is not engineering acceptance and does not substitute for `TASK_EVIDENCE`.

## Motion / spinning detection

V3.5 should distinguish a live but slow/spinning executor from a dead executor.

Example signal:

```text
multiple valid activity epochs
+
no material/semantic/evidence frontier movement
+
no declared legitimate wait
→ QUIET / POSSIBLE_SPINNING
```

Possible spinning indicators include:

- repeated unchanged test reruns;
- repeated reread of the same source set;
- repeated search paths with no new negative knowledge;
- repeated edit/revert cycles with no candidate/frontier advance.

Spinning detection is advisory/derived. It does not itself decide engineering correctness.

## Checkpoint evidence shape

Recommended Owner-visible checkpoint:

```text
TASK_EVIDENCE — CHECKPOINT
{P18% · E14% · A07 · 🟢 ACTIVE}
CURRENT_UNIT: <unit>
COMPLETED/LEARNED: <bounded summary>
MATERIAL_FRONTIER: <sha / working-delta ref>
SEMANTIC_EVIDENCE_FRONTIER: <ref>
NEGATIVE_KNOWLEDGE: <only materially useful items>
GITHUB_PROJECTION: updated + read back
NEXT: <next substantial work unit>
```

The chat checkpoint is an Owner visibility mirror. It does not replace durable provider publication where durable successor evidence is required.

## Recovery after interruption

Recovery sequence:

```text
1. verify responsibility + exact protocol/Owner basis
2. read latest valid checkpoint/provider projection
3. observe live branch/PR/base/HEAD/checks
4. calculate delta from checkpoint to live material
5. reconcile active unit/findings/negative knowledge
6. publish TASK_EVIDENCE — RECOVERY
7. update/read back GitHub projection
8. surface recovery evidence in chat
9. continue
```

The design objective is:

```text
maximum normal recovery distance
≈ current uncheckpointed micro-unit
```

rather than an entire lost executor session.

## Progress integrity

The following may renew liveness/activity but MUST NOT independently increase P or E:

```text
3000 lines read
files inspected
250/500 lines written
400/700 lines modified
commits
pushes
comments
provider updates
test count
tool calls
elapsed time
activity epochs
```

P/E remain denominator-based semantic/evidence measures.

## Required future implementation surfaces

When V3.5 is created, do not stop at prose. Implement at least:

```text
SKILL.md
continuity/current-state schema
activity-lease schema
checkpoint provider projection
issue-title projection
external watcher contract
recovery logic
focused tests
adversarial tests
mutation tests
real-history replay
```

Required adversarial cases include:

```text
activity without progress does not increase P/E
same lines reread repeatedly does not keep ACTIVE indefinitely
same failing test repeatedly does not manufacture motion
semantic checkpoint requires durable evidence
Owner-required mode cannot silently continue after failed provider readback
abrupt failure after useful work leaves bounded recovery delta
watcher can turn stale executor red without executor cooperation
one missed watcher observation does not declare death
WAITING_TOOL does not become STALE while declared wait is valid
```

## Replay case — Owner interruption example

Retain as a permanent replay scenario:

```text
- inspect benchmark overlay tests and reconstruct persistence blockers
- review focused tests/dependencies/PR/filename overlap
- write audit test
- verify exact source syntax error
- update issue and create branch
- abrupt stream/tool error
- Owner says "continue"
```

Expected future V3.5 behavior:

```text
semantic/activity checkpoints occur before large frontier accumulation
pre-risk checkpoint occurs before provider/branch mutation if useful state is uncheckpointed
GitHub title/current projection is updated and read back
Owner sees checkpoint evidence in chat before the next substantial unit
post-failure recovery starts from latest checkpoint and only reconciles the bounded residual delta
```

This replay must pass before the checkpoint/liveness contract is treated as proven V3.5 behavior.