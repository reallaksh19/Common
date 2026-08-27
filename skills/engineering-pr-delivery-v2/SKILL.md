---
name: engineering-pr-delivery-v2
description: Execute, recover, qualify, and relay engineering repository work across multiple agents using a repo-wide append-only agents/agentchain.md. Use for engineering implementation, investigation, audit, PR progression, abrupt agent loss, expert takeover, multi-agent workstreams, AUTO MODE, and long-running tasks spanning multiple PRs. Every durable endpoint records the trusted repository state, required inputs/benchmarks/common and governing documents, exact next action, protected authority, validation limits, and exactly five repository-specific questions for the next agent. The repository baton exists continuously; graceful handoff is optional and candidate self-qualification never grants engineering-critical write authority.
---

# Engineering PR Delivery v2 — Relay Engineering

## Governing objective

Run engineering work as a crash-safe relay.

The authoritative baton is the latest valid endpoint in the repository, not the outgoing agent, chat history, or a large per-PR work report.

At every durable endpoint, another qualified engineer must be able to discover the mission, trusted state, governing inputs and benchmarks, unresolved work, protected authority, exact next safe action, and five qualification questions from repository artifacts plus live Git/GitHub state.

Graceful handoff is useful but never required.

## 1. Core invariants

Always preserve these rules:

```text
R1  Repository state, not conversation memory, is the baton.
R2  Agent disappearance is a normal recoverable condition.
R3  Repo-wide agents/agentchain.md is the primary relay index.
R4  Completed endpoints are append-only; correct them by supersession.
R5  Every non-terminal endpoint contains exactly five next-agent questions.
R6  Questions test the NEXT unresolved engineering work.
R7  Every endpoint lists inputs, benchmarks, common/governing docs,
    authoritative sources, production paths, and validation paths.
R8  Incoming engineering-critical takeover begins READ_ONLY.
R9  Candidate answers do not grant authority; self-verification is invalid.
R10 Qualification is bound to a material repository state.
R11 NOT_RUN, unresolved assumptions, blockers, and risks survive the relay.
R12 A task/chain may span many agents, commits, branches, and PRs.
R13 PR merge does not imply engineering-chain completion.
R14 Every non-terminal endpoint has one exact next safe action.
R15 Detailed evidence stays in its owning artifact; agentchain.md is navigation.
```

Read `references/relay-model.md`.

## 2. Work identity

Use this hierarchy:

```text
REPOSITORY
  -> CHAIN_ID
  -> LEG_ID
  -> ENDPOINT_ID
  -> PR / branch / commits
```

`CHAIN_ID` identifies the durable engineering mission and survives PR transitions.

Examples:

```text
EMP1-ISSUE-1389
LAFEA3-ISSUE-1422
HP-ISSUE-1290
```

A new PR for the same unresolved mission normally starts a new leg, not a new chain.

## 3. Locate or create the repo-wide relay index

Primary file:

```text
agents/agentchain.md
```

If missing and the task requires durable engineering relay state, initialize it from `references/agentchain-template.md`.

The file has two responsibilities:

1. a compact `ACTIVE CHAINS` table at the top;
2. append-only endpoint records below it.

Do not create mandatory per-PR work reports, status files, or claim files merely because this skill is active. Existing repository-local artifacts may still be read and preserved during migration or compatibility work.

Read `references/agentchain-schema.md`.

## 4. Establish live repository truth before mutation

Before engineering-sensitive mutation, determine from live Git/GitHub where available:

```text
repository/default branch
live main/base SHA
branch
PR identity and state
PR head
merge base
changed files and commits
checks/workflows
review state
source issue/task
predecessor/follow-on PRs
active chains and path/authority overlaps
material base drift
```

Live mutable repository state overrides stale chat and stale endpoint observations.

Classify endpoint/live reconciliation as:

```text
MATCH
METADATA_DRIFT
MATERIAL_DRIFT
CONTRADICTION
```

Material drift requires recovery/requalification before engineering-critical mutation.

## 5. Read only the latest endpoint first

For an existing chain:

1. find the chain in `ACTIVE CHAINS`;
2. locate its latest endpoint;
3. read the endpoint's indexed dependencies;
4. fetch only the required inputs, benchmarks, common/governing docs, authoritative sources, production paths, and validation paths;
5. re-ground live repository state;
6. expand investigation only when the endpoint/live evidence requires it.

Do not force every incoming agent to rediscover the whole repository.

## 6. Endpoint creation triggers

Create or refresh a durable endpoint at meaningful engineering boundaries, including:

```text
before first engineering-critical production mutation
after one coherent implementation unit
after a material hypothesis change
after significant PASS/FAIL validation
when a blocker materially changes
before changing source/benchmark/authority assumptions
before moving to another PR
before requesting merge
before intentionally stopping
when recovering after another agent disappears
when the engineering chain becomes objectively complete
```

Do not checkpoint every trivial edit. Prefer coherent, recoverable engineering units.

## 7. Mandatory endpoint content

Every endpoint must record at least:

```text
CHAIN_ID / LEG_ID / ENDPOINT_ID / PREVIOUS_ENDPOINT
ENDPOINT_REASON
TASK / ISSUE / PR / BRANCH
CHECKPOINT_HEAD / MAIN_HEAD_OBSERVED / MERGE_BASE
STATE
MISSION
THIS LEG COMPLETED
CURRENTLY IN PROGRESS
REMAINING WORK
EXACT NEXT ACTION
KNOWN / PROVEN
NOT PROVEN
NOT_RUN
ACTIVE HYPOTHESIS
FALSIFIER
PROTECTED INVARIANTS
DO NOT REDO
DO NOT CHANGE
EXPECTED NEXT-LEG FILES / DOMAINS
INPUTS
BENCHMARKS
COMMON / GOVERNING DOCUMENTS
AUTHORITATIVE SOURCES
PRODUCTION PATHS
VALIDATION / TEST PATHS
CHANGED DURING THIS LEG
VALIDATION SUMMARY
OPEN RISKS / QUESTIONS
QUALIFICATION_BASIS_HEAD
QUESTION_SET_ID
Q1..Q5
```

If a section genuinely has no item, write `NONE — <reason>` rather than silently omitting it.

## 8. Source, benchmark, and common-document custody

Every endpoint explicitly indexes what the next engineer needs.

Where practical, pin controlled material with:

```text
repository
path
commit / blob / semantic hash
page / section / table / equation when relevant
authority class
```

The six required inventories are:

```text
INPUTS
BENCHMARKS
COMMON / GOVERNING DOCUMENTS
AUTHORITATIVE SOURCES
PRODUCTION PATHS
VALIDATION / TEST PATHS
```

Read `references/source-indexing.md`.

## 9. Five next-agent questions

Every non-terminal endpoint contains exactly five repository-specific questions:

```text
Q1 Production Trace
Q2 Current Unresolved Problem / Failure Isolation
Q3 Authority / Invariant
Q4 Independent Validation
Q5 Next Contribution / Minimal Patch
```

Questions must be derived from the current remaining work and require live repository evidence.

Reject a question if it:

- can be answered from general theory without the repository;
- primarily audits already-completed work rather than the next leg;
- has no concrete repository anchor;
- has no falsifiable prediction, evidence requirement, or patch implication where applicable;
- could be pasted unchanged into an unrelated task.

Read `references/qualification.md`.

## 10. Incoming-agent qualification

For engineering-critical takeover:

```text
TAKEOVER_AUTHORITY = READ_ONLY
```

The candidate may inspect, calculate, reproduce, and gather evidence, but must not make engineering-critical production mutations before qualification.

The candidate answers Q1-Q5 in a separate qualification-answer artifact.

A verifier records the verdict separately.

Hard rule:

```text
candidate_id == verifier_id
-> qualification cannot grant WRITE_ALLOWED
```

Default pass threshold:

```text
total >= 92/100
minimum each >= 17/20
```

Fabricated evidence, unsafe authority claims, validation gaming, or pretending NOT_RUN is PASS can fail immediately regardless of score.

If independent verification is unavailable, the candidate may continue read-only investigation but must not manufacture an independent PASS.

## 11. Qualification freshness

Bind every question set and verdict to `QUALIFICATION_BASIS_HEAD` plus the latest endpoint.

Material changes after the qualification basis make the question set or verdict stale.

Material changes include production behavior, tests, benchmarks, oracle/expected values, engineering inputs, source authority, behavior-affecting configuration, engineering methodology, or publication authority.

Relay metadata-only changes do not by themselves invalidate qualification.

When the unresolved engineering problem changes materially, generate a new question set at the new endpoint.

## 12. Crash recovery

Do not require the outgoing agent to release anything.

If an agent disappears:

1. read the latest valid endpoint;
2. fetch live PR/main state;
3. inspect all material changes after `CHECKPOINT_HEAD`;
4. classify post-endpoint work as `RECOVERABLE`, `PARTIAL_UNKNOWN`, `CONTAMINATED`, or `UNTRUSTED`;
5. create an `AGENT_LOST_RECOVERY` endpoint;
6. preserve known-good work and explicit uncertainty;
7. regenerate Q1-Q5 against the recovered current state when needed;
8. qualify before further engineering-critical mutation.

Unpushed/unpersisted private work is unrecoverable and therefore non-authoritative.

Read `references/crash-recovery.md`.

## 13. Multi-agent coordination

At chain start and before each material leg, compare active chains for:

```text
exact-file overlap
path-prefix overlap
engineering/software authority overlap
benchmark/oracle overlap
dependency/stacked-PR relationships
base drift
```

Classify:

```text
SAFE
COORDINATION_REQUIRED
BLOCKED
UNKNOWN
```

No exact-file overlap does not prove authority independence.

Read `references/multi-agent-coordination.md`.

## 14. Engineering validation integrity

For material checks preserve:

```text
STATUS      PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION execution / inspection / inference basis
ORACLE      implementation-coupled or independent authority class
TESTED_HEAD
EXPECTED
ACTUAL
TOLERANCE where applicable
LIMITATIONS
```

Never weaken tolerances, rewrite expected values from production output, delete difficult benchmarks, hard-code fixture answers, silence fail-closed behavior, or call unexecuted checks PASS.

Read `references/engineering-validation.md` and `references/anti-gaming-rules.md`.

## 15. Contribute one coherent leg

After qualification and coordination checks:

```text
diagnose/isolate
-> implement smallest legitimate production change
-> integrate through the real production path
-> validate
-> record negative assurance / protected invariants
-> create next endpoint with fresh Q1-Q5
```

If evidence disproves the current hypothesis, update the hypothesis and endpoint rather than forcing the planned patch.

## 16. PR and merge discipline

PRs are implementation vehicles, not durable chain identity.

Keep PR scope coherent and changed files explainable.

Do not infer chain completion from PR merge.

Do not modify workflow/security/credential or destructive infrastructure without explicit authorization.

Do not merge unless owner authority permits it.

Read `references/git-pr-policy.md`.

## 17. Chain completion

Distinguish:

```text
AGENT LEG COMPLETE
PR COMPLETE
ENGINEERING CHAIN COMPLETE
```

Only a truly terminal endpoint may use:

```text
STATE: COMPLETE
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
COMPLETION_BASIS: <objective engineering basis>
```

A merged PR with follow-on technical work remains an active chain and therefore requires a next action and Q1-Q5.

## 18. AUTO MODE

When the owner explicitly activates `AUTO MODE`, a qualified agent may progress through the approved mission without routine phase-by-phase confirmation.

AUTO MODE does not bypass:

- qualification on new custody acquisition;
- chain/endpoint maintenance;
- source/benchmark custody;
- engineering authority boundaries;
- independent validation requirements;
- overlap hard stops;
- explicit merge authority.

At every material endpoint, refresh the baton and Q1-Q5 so abrupt loss remains recoverable.

Read `references/auto-mode.md`.

## 19. Migration from legacy work reports

Do not rewrite historic work reports.

For a live legacy task, create a forward-only migration endpoint:

```text
ENDPOINT_REASON: LEGACY_TO_RELAY_MIGRATION
LEGACY_STATE_SOURCE: <paths>
CURRENT_AUTHORITY: this endpoint onward
```

Import only current live mission/state/dependencies needed to continue safely. Preserve legacy reports as historical evidence.

## 20. Governing test

At every endpoint ask:

> If the current agent vanishes now, can the next competent engineer discover the task, authoritative inputs and benchmarks, trusted state, unresolved problem, protected invariants, exact next safe action, and five questions needed to prove competence without asking what the previous agent was doing?

If not, the endpoint is not relay-ready.
