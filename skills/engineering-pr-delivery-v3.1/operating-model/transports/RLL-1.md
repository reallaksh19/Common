# RLL-1 — Relay Lease Loop v1

## Status

RLL-1 is an Engineering Relay V3.1 **execution transport profile**.

It does not create engineering authority. V3.1 remains the authority/reconstruction layer; RLL-1 only discovers, transports, resumes and records execution of already-authorized work.

The governing rule is:

> V3.1 governs engineering authority. RLL-1 transports already-authorized execution. Git material truth outranks RLL operational state.

RLL-1 is initially single-worker / single-machine. Distributed arbitration is explicitly out of scope.

The reviewed rollout/implementation blueprint is `RLL-1-blueprint.md`. The normative transport contract in this file takes precedence if the rollout document ever drifts.

## Transport implementation

The reference transport does **not** require a GitHub MCP server.

It uses:

- native `git` for material repository truth;
- GitHub CLI `gh` and `gh api` for issue/PR/provider reads plus bounded label/comment mutations;
- a deterministic Python launcher for local mutex, issue selection, lease/state updates and directive filtering;
- Google Antigravity `agy -p` for non-interactive engineering-agent execution;
- Antigravity `/schedule` as the initial recurring trigger.

A persistent Antigravity sidecar is a later lifecycle upgrade, not an RLL-1 prerequisite.

## Authority hierarchy

When observations disagree, resolve them in this order:

1. direct Owner authority;
2. governing programme contract;
3. active bounded child contract / approved implementation plan;
4. repository material truth;
5. executable evidence;
6. durable V3.1 records;
7. RLL operational state;
8. timer/scheduler prompt.

A stale worker-state `material_head` never overrides `git rev-parse HEAD`.

## Eligibility

RLL MUST NOT select arbitrary open issues.

An issue is eligible only when all of the following are true:

- it is open;
- it carries `rll-ready` or `rll-active`;
- its engineering responsibility is already bounded by the issue/programme;
- an approved/durable implementation plan exists when the governing workflow requires one;
- an `RLL_EXECUTION_V1` envelope exists in the issue body or in an authorized coordinator comment;
- explicit non-goals and evidence expectations are recoverable from durable state.

Minimum execution envelope:

```yaml
RLL_EXECUTION_V1

transport: RLL-1
worker: antigravity-local
mode: BRANCH_RESUME
repository: owner/repo
branch: owned-branch
base_sha: <approved-base-sha>
allow_material_write: true
```

For exact-head evidence tasks:

```yaml
RLL_EXECUTION_V1

transport: RLL-1
worker: antigravity-local
mode: EXACT_HEAD_EVIDENCE
repository: owner/repo
head_sha: <exact-sha>
base_sha: <comparison-base-sha>
allow_material_write: false
```

Supported modes:

- `BRANCH_RESUME`: resume the declared branch; prior legitimate worker commits must not be reset to the original base.
- `EXACT_HEAD_EVIDENCE`: execute against the declared immutable head in a clean dedicated worktree/detached checkout; tracked material writes are prohibited.

An `RLL_EXECUTION_V1` envelope in the issue body is trusted only when the issue author is one of the configured authorized GitHub identities. An execution envelope in a later comment is trusted only when that comment author is authorized. This prevents an arbitrary issue/comment author from turning transport metadata into executable work merely by reproducing the marker.

## Labels

Transport labels are deliberately small:

- `rll-ready`
- `rll-active`
- `rll-review-ready`
- `rll-escalation`

Do not introduce `rll-pass`, `rll-fail`, `rll-completed` or `rll-blocked`. Those names collapse transport state into engineering evidence.

Engineering completion remains represented by exact material/evidence, `TASK_RESULT`, merge truth and issue lifecycle.

## State machine

```text
READY
  ↓
ACTIVE
  ├─→ RETRY_WAIT ─→ ACTIVE
  ├─→ ESCALATION_REQUIRED
  └─→ REVIEW_READY

administrative terminal: CANCELLED
```

Definitions:

- `READY`: eligible; no active local execution.
- `ACTIVE`: local worker owns the current single-machine execution lease.
- `RETRY_WAIT`: transient external/environmental condition; not an engineering FAIL.
- `ESCALATION_REQUIRED`: actual contract contradiction or safe-scope conflict requiring coordinator/Owner action.
- `REVIEW_READY`: material edits stopped, required evidence cycle completed, exact material/evidence published, lease released. This does not mean accepted or merged.
- `CANCELLED`: an authorized directive retired transport execution.

The default disposition for routine engineering uncertainty is `CONTINUE`, not HOLD/FAILED/INCOMPLETE.

## Deterministic local mutex

A scheduled LLM invocation MUST NOT be trusted to serialize itself.

The reference launcher acquires an atomic same-machine mutex **before** issue discovery or agent invocation.

Default location:

```text
<RLL_DATA_DIR>/<repo-key>/worker.lock/
```

The lock records worker ID, PID and acquisition time.

If the recorded PID is healthy, a second invocation exits with no agent call.

If the process is no longer alive, the stale lock may be reclaimed.

This is the primary same-machine exclusion mechanism.

## GitHub lease

The GitHub lease is observability/recovery state, not a distributed atomic lock.

That is sufficient for RLL-1 because only one local worker is supported.

Lease fields live in the single mutable worker-state comment:

```yaml
RLL_WORKER_STATE_V1

protocol_basis:
  relay: V3.1
  common: <sha>
  two_pass: <revision>
  transport: RLL-1

worker: antigravity-local
issue: 342

state: ACTIVE
phase: IMPLEMENT

mode: BRANCH_RESUME
branch: phase13/example
base_sha: 9e7d3476...
material_head: abc123...

lease_epoch: 6
lease_until: 2026-09-26T04:30:00Z

last_directive_sequence: 4

current: focused semantic journey tests
next: compatibility certification
```

There MUST be at most one `RLL_WORKER_STATE_V1` comment per child issue.

It is mutated in place through the GitHub Issues comment API. Do not append heartbeat comments every timer tick.

RLL state is operational metadata only. It is never acceptance evidence.

## Directive protocol

Ordinary issue comments are not executable instructions.

Only comments that:

1. begin with `RELAY_DIRECTIVE_V1`;
2. are authored by a configured authorized GitHub login;
3. contain the current issue number; and
4. have a sequence greater than the worker cursor

may affect transport control.

Envelope:

```yaml
RELAY_DIRECTIVE_V1

sequence: 12
issue: 342
action: CONTINUE
instruction: >
  Continue the reviewed correction described below.
```

Allowed actions:

- `CONTINUE`
- `PAUSE`
- `RESUME`
- `REPLAN`
- `CANCEL`

Unknown prose remains non-executable context.

Duplicate directive sequence numbers are a protocol contradiction and must not be guessed through.

The worker stores `last_directive_sequence` and processes only newer authorized envelopes in ascending sequence order.

## Engineering publications remain V3.1 publications

Do not use RLL state updates as pseudo-handoffs.

Durable engineering publication types remain:

- `IMPLEMENTATION_PLAN`
- `PLAN_UPDATE`
- `TASK_EVIDENCE`
- `TASK_RESULT`

Timer wake-ups, lease renewals, ordinary edit/test progress and transient retries do not require durable V3.1 comments.

## Semantic-boundary mapping

| RLL event | V3.1 consequence |
| --- | --- |
| timer wake | none |
| mutex check | none |
| lease renewal | none |
| normal implementation/test progress | none |
| transient retry | none |
| initial claim/takeover | live V3.1 refresh |
| implementation begins after claim | live V3.1 refresh |
| governing approach materially changes | live refresh + `PLAN_UPDATE` |
| evidence cycle begins | live V3.1 refresh |
| exact-head evidence publication | `TASK_EVIDENCE` |
| transition to `REVIEW_READY` | semantic-boundary refresh |
| reviewer takeover | semantic-boundary refresh |
| merge | semantic-boundary refresh + direct Owner authority |
| post-merge | `TASK_RESULT` |

## Repository resumption

For `BRANCH_RESUME`, do not check out the original base on every wake.

Record:

```yaml
branch: <owned branch>
base_sha: <approved production base>
```

First claim verifies branch ancestry from `base_sha`.

Before invoking the engineering agent, the deterministic launcher positions the workspace on the governed branch. If the current checkout is clean and merely behind `origin/<branch>`, it may fast-forward. Local-ahead material is preserved. A dirty wrong-branch checkout or divergent branch is an escalation, never an automatic reset/rebase.

Later invocations resume the branch's actual material head.

Every invocation should observe:

```text
git fetch origin
git status --porcelain
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git merge-base <branch> <base_sha>
```

Material Git state wins over a stale RLL comment.

For `EXACT_HEAD_EVIDENCE`, the deterministic launcher creates or reuses a dedicated detached worktree under the RLL data directory at the declared `head_sha`. It must not detach or repurpose the user's normal checkout. The evidence worktree must return clean and remain on the exact declared head.

## Reference launcher

The reference implementation is:

```text
skills/engineering-pr-delivery-v3.1/scripts/rll_worker.py
```

Responsibilities:

1. acquire same-machine mutex;
2. verify `git`, `gh` and `agy` availability;
3. verify authenticated `gh`;
4. discover exactly one active issue or deterministically select the oldest ready issue;
5. load issue + comments using `gh`;
6. validate `RLL_EXECUTION_V1`;
7. find/create the singular worker-state comment;
8. filter/apply authorized directives;
9. claim/renew the GitHub lease;
10. invoke Antigravity headlessly;
11. parse a structured `RLL_RUN_RESULT_V1`;
12. refresh material Git truth;
13. update transport state/labels;
14. release the mutex.

The launcher does not merge, release, delete branches, close programme issues, or mutate acceptance criteria.

## Antigravity invocation

Reference headless execution uses:

```text
agy -p <prompt>
    --output-format json
    --json-schema <rll-run-result.schema.json>
    --effort high
    --print-timeout <bounded-duration>
```

Do not use `--dangerously-skip-permissions`.

Antigravity must be authenticated interactively once before unattended use.

Use scoped permissions in `~/.gemini/antigravity-cli/settings.json`.

Recommended permission shape is repository-specific and should allow only the commands/files needed by the task. In particular, do not authorize GitHub merge/release/destructive commands.

RLL recommends that provider-control mutations (RLL labels/state) remain in the deterministic launcher. The engineering agent needs provider read access and, when evidence publication is required, bounded issue-comment authority.

## Structured run result

The agent result is transport metadata, not engineering acceptance:

```json
{
  "schema": "RLL_RUN_RESULT_V1",
  "transport_state": "REVIEW_READY",
  "current": "exact-head certification complete",
  "next": "independent coordinator review",
  "evidence_comment_url": "https://github.com/owner/repo/issues/342#issuecomment-...",
  "engineering_summary": "focused tests PASS; hosted CI NOT_RUN_INFRASTRUCTURE",
  "notes": []
}
```

Allowed `transport_state` values returned by the agent:

- `ACTIVE`
- `RETRY_WAIT`
- `ESCALATION_REQUIRED`
- `REVIEW_READY`

The launcher re-observes Git HEAD/tree state and does not trust an agent-supplied SHA as material truth.

## GitHub CLI access model

RLL-1 intentionally avoids a GitHub MCP dependency.

Provider reads use `gh issue list`, `gh issue view`, `gh pr view`, and bounded `gh api` GETs.

Provider-control writes use only:

- add/remove `rll-*` labels on the selected issue;
- create/update the singular `RLL_WORKER_STATE_V1` comment;
- bounded engineering evidence comments when required by the child contract.

The reference launcher contains no merge, release, branch-delete or issue-delete operation.

Repository material writes use normal `git` on the declared branch and are governed by the issue/plan, not by RLL.

## Scheduler

Initial cadence:

```cron
*/10 * * * *
```

The scheduler prompt should stay small:

```text
Run this repository's RLL-1 worker once.
Use the repo-local RLL adapter/launcher.
Resume only durable rll-ready/rll-active work.
Never infer Owner authority, broaden scope, merge, or release.
```

The detailed protocol belongs in this file and the repository adapter, not in the timer string.

## Scheduled Task vs sidecar

Start with Antigravity Scheduled Tasks.

Upgrade to a sidecar only after evidence shows a need for stronger lifecycle control such as:

- serialized queues across repositories;
- precise retry clocks;
- continuous event processing;
- multiple workers;
- richer health telemetry.

Do not build distributed locking on top of GitHub labels/comments in RLL-1.

## Two-Pass relationship

RLL executes after the applicable planning/approval boundary:

```text
research
→ Pass 1 baseline
→ Pass 2 proposal/plan
→ Owner approval when required
→ IMPLEMENTATION_PLAN
→ bounded child/branch
→ RLL_EXECUTION_V1
→ rll-ready
→ unattended execution
```

RLL may research implementation details inside the approved responsibility. It may not use that research to redefine the capability.

A material contradiction requires `REPLAN` / `ESCALATION_REQUIRED`.

## Failure classification

Transport state and engineering result remain orthogonal.

Valid example:

```text
RLL: REVIEW_READY

engineering:
  focused tests: PASS
  typecheck: FAIL — PREEXISTING_UNRELATED
  hosted CI: NOT_RUN — INFRASTRUCTURE
```

Never map `REVIEW_READY → PASS` or `RETRY_WAIT → FAIL`.

## Independent review and merge

At `REVIEW_READY` the worker stops material edits and releases execution ownership.

The coordinator independently reviews exact branch ancestry, diff, scope, tests and evidence.

If correction is needed, publish an authorized `RELAY_DIRECTIVE_V1 / CONTINUE` or `REPLAN`.

Merge remains outside RLL:

```text
Coordinator review
→ Owner says merge
→ coordinator refreshes live V3.1
→ exact reviewed head verified
→ merge
→ TASK_RESULT / reconciliation
```

## Pilot sequence

1. land this transport profile in Common V3.1;
2. add a thin repository adapter;
3. create the four RLL labels;
4. configure scoped Antigravity permissions;
5. create one Scheduled Task;
6. run a non-destructive smoke issue;
7. prove mutex overlap rejection;
8. prove lease-expiry reconstruction;
9. prove stale worker-state head loses to Git;
10. prove PAUSE/RESUME and prose-comment non-execution;
11. run an exact-head evidence pilot;
12. only then enable a source-write pilot.

The first pilot must not merge or release anything.

## Rollback

RLL is removable without rewriting V3.1 material truth:

- disable the Scheduled Task;
- remove RLL labels;
- retain child issue, branch, commits and evidence;
- resume interactive execution.

The design invariant is:

> Automate movement of authority and evidence; do not automate creation of authority.
