# RLL-1 reviewed implementation blueprint

## Purpose

This document is the implementation blueprint for the Engineering Relay V3.1 RLL-1 transport.

It preserves the governing concept: V3.1 owns engineering authority and durable evidence semantics; RLL-1 only transports already-authorized work between GitHub/Git and a local scheduled executor.

RLL-1 exists to remove human copy/paste from the normal child-issue -> local-agent -> evidence loop without weakening the Owner approval, independent review, merge or release boundaries.

## Reviewed changes from the original concept

The initial concept is retained with these implementation refinements:

1. **No GitHub MCP dependency.** Use native `git` plus authenticated GitHub CLI `gh` / `gh api`.
2. **Deterministic transport control.** Same-machine mutex, issue selection, execution-envelope validation, directive filtering, lease/state mutation and workspace preparation run in ordinary Python before any LLM invocation.
3. **One engineering-agent invocation per wake.** Prefer an Antigravity sidecar `schedule` command that runs the deterministic launcher; the launcher then invokes one `agy -p` session. This avoids timer-agent -> nested-agent choreography.
4. **Two execution modes.** `BRANCH_RESUME` handles material implementation; `EXACT_HEAD_EVIDENCE` handles read-only certification/offload issues.
5. **Dedicated exact-head worktrees.** Evidence timers never detach or repurpose the user's normal checkout.
6. **Branch positioning before agent invocation.** A clean behind branch may fast-forward; local-ahead material is preserved; dirty wrong-branch or divergent state fails closed to transport escalation.
7. **Authorized execution envelopes.** Issue-body envelopes are trusted only from authorized issue authors; comment envelopes/directives only from configured authorized logins.
8. **Long-thread correctness.** GitHub comment retrieval is paginated; the directive cursor prevents replay.
9. **Durable PAUSE/REPLAN.** These states survive timer wakes until a later authorized `RESUME` / `CONTINUE`.
10. **Smoke-first rollout.** The repository adapter installs with `RLL_SMOKE=1` by default and requires an explicit second action before engineering-agent execution.
11. **No implicit PASS.** Transport `REVIEW_READY` is orthogonal to engineering `PASS | FAIL | NOT_RUN | NOT_APPLICABLE`.
12. **No dangerous unattended bypass.** The profile prohibits `agy --dangerously-skip-permissions`; use scoped project permissions.

## Architecture

```text
Owner / Coordinator
      |
      | V3.1 plan/authority
      v
GitHub bounded child
      |
      | RLL_EXECUTION_V1 + rll-ready
      v
Antigravity sidecar schedule
      |
      v
deterministic rll_worker.py
  - local mutex
  - gh discovery/state/directives
  - Git material/workspace preparation
      |
      v
one agy -p engineering session
      |
      v
branch/tests/exact-head evidence
      |
      v
GitHub TASK_EVIDENCE
      |
      v
independent coordinator review
      |
      | direct Owner merge command only
      v
merge / TASK_RESULT
```

## Stage 0 — protocol integration

Deliver in Common V3.1:

- normative RLL-1 transport specification;
- live `SKILL.md` reference;
- Two-Pass boundary clarification;
- transport run-result schema;
- deterministic launcher;
- unit tests.

Exit:

- RLL semantics do not create engineering authority;
- V3.1 publication vocabulary remains unchanged;
- current Common V3.1 validation is green.

## Stage 1 — consumer adapter

Each repository adds only a thin adapter:

- Antigravity rule pointing back to Common RLL-1;
- platform wrapper around the Common launcher;
- sidecar installer/configuration;
- project setup/smoke documentation;
- optional adapter source guard.

The adapter must not fork generic RLL semantics.

## Stage 2 — provider/control-plane setup

Create transport labels:

```text
rll-ready
rll-active
rll-review-ready
rll-escalation
```

Do not add pass/fail/completed labels.

Provider mutations are bounded to:

- these RLL labels;
- the singular mutable `RLL_WORKER_STATE_V1` comment;
- engineering evidence comments already required by the governing child.

Do not automate merge, release, branch deletion, programme closure or acceptance mutation.

## Stage 3 — non-destructive smoke

Install the sidecar with `RLL_SMOKE=1`.

The smoke must:

1. acquire/release the local mutex;
2. discover exactly one eligible issue;
3. read/validate the authorized execution envelope;
4. fetch and validate Git material basis;
5. prepare the correct branch/exact-head workspace;
6. create/update the singular worker-state comment;
7. transition labels through the transport claim;
8. **not invoke Antigravity**;
9. make no tracked source change.

Exit only after the coordinator verifies the observed state.

## Stage 4 — reentrancy and control tests

Before engineering execution prove:

### Mutex overlap

Two simultaneous launcher invocations using the same RLL data directory must result in exactly one owner; the second exits without agent invocation.

### Stale local lock

A lock whose PID is no longer live may be reclaimed.

### Material truth wins

If the worker-state comment names a stale material head, the next run re-observes Git and corrects operational state rather than resetting material.

### Directive filtering

- authorized structured `PAUSE` persists across wakes;
- ordinary prose does nothing;
- unauthorized structured prose does nothing;
- duplicate directive sequences fail closed;
- authorized `RESUME` / `CONTINUE` advances the cursor and permits work.

## Stage 5 — read-only exact-head pilot

Use an already-authorized exact-head evidence child before source-write automation.

Required properties:

- exact immutable candidate SHA;
- explicit base/comparison SHA;
- `allow_material_write: false`;
- executable evidence contract;
- no merge/release authority.

The launcher creates a dedicated detached worktree and Antigravity executes the child contract there.

Exit:

- exact head unchanged;
- clean postflight;
- evidence posted to the child;
- transport state `REVIEW_READY` only when durable evidence URL exists;
- coordinator can review entirely from GitHub without Owner copy/paste.

## Stage 6 — source-write pilot

Only after Stage 5 succeeds:

- select a bounded child with approved implementation plan;
- use `BRANCH_RESUME`;
- verify owned branch descends from approved base;
- enable source-write permissions narrowly;
- let the worker research/implement/test/commit/push within the issue boundary.

Routine uncertainty is implementation responsibility. Actual authority contradictions use `REPLAN` / `ESCALATION_REQUIRED`.

## Stage 7 — independent review loop

At `REVIEW_READY`:

- worker stops material edits;
- transport lease is released;
- exact pushed head and evidence are durable;
- coordinator independently inspects ancestry, diff, source semantics, tests and classification.

If correction is needed, coordinator publishes a new authorized `RELAY_DIRECTIVE_V1 / CONTINUE` or `REPLAN`. The next timer wake resumes the same governed branch.

## Stage 8 — Owner merge boundary

RLL remains uninvolved in merge authority.

Normal flow:

```text
REVIEW_READY
-> independent coordinator review
-> Owner: merge
-> live V3.1 refresh
-> exact reviewed head check
-> merge
-> TASK_RESULT / reconciliation
```

## Scheduler choice

### Preferred initial implementation

Use Antigravity 2.0 sidecar builtin `schedule` to execute the deterministic launcher command on a standard five-field cron.

Why:

- mutex/lease code runs before the agent;
- no nested scheduled-agent invocation;
- sidecar runtime gives persistent data/log directories;
- command lifecycle is observable;
- schedule cadence remains operational rather than protocol-semantic.

Default cadence:

```cron
*/10 * * * *
```

### `/schedule`

`/schedule` remains suitable for one-off/manual smoke experiments or environments where sidecars are unavailable. If used, the scheduled prompt should invoke the repository launcher once and must not duplicate protocol logic inside the prompt.

### Later sidecar coordinator / RLL-2

Do not add multi-machine/distributed claims until the single-worker transport has repeated evidence of safe operation.

## Security model

### GitHub access

Use authenticated `gh`. Separate authentication from authorization:

- `gh auth login` establishes identity;
- RLL code constrains which provider operations it performs;
- repository/Antigravity permissions constrain shell/file capabilities;
- engineering issue/plan constrains material scope.

### Prompt injection resistance

Only configured authorized identities plus structured markers may supply execution/control envelopes. Ordinary comments are never automatically promoted into control instructions.

### Workspace safety

Exact-head evidence runs in dedicated worktrees. Branch automation refuses destructive reset/rebase reconciliation.

### Merge isolation

The reference launcher does not contain merge/release/delete provider operations. The engineering prompt also prohibits them.

## Failure semantics

Examples:

```text
RLL: REVIEW_READY
engineering: focused PASS; hosted CI NOT_RUN_INFRASTRUCTURE

RLL: RETRY_WAIT
engineering: no new result; package registry unavailable

RLL: ESCALATION_REQUIRED
engineering: contract contradiction requires coordinator/Owner decision
```

Do not translate transport state into engineering acceptance.

## Rollback

If the pilot is unreliable:

- disable/remove the sidecar;
- remove RLL labels;
- retain child issue, branch, commits and evidence;
- resume normal interactive V3.1 execution.

No engineering truth depends on RLL being present.

## Acceptance criteria

RLL-1 is ready for normal use only after evidence proves:

- unattended timer fires;
- local overlap is excluded;
- exact-head evidence uses an isolated worktree;
- branch work resumes rather than resets;
- lease/state survives conversation loss;
- comment pagination/cursor behavior is correct;
- PAUSE/RESUME is durable;
- ordinary prose is non-executable;
- exact SHA binds final evidence;
- no merge/release authority leaks into the worker;
- coordinator can review without Owner copy/paste;
- disabling RLL leaves V3.1 engineering state intact.

## Invariant

> Automate movement of authority and evidence; do not automate creation of authority.
