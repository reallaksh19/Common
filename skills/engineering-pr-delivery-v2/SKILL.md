---
name: engineering-pr-delivery-v2
description: Execute, recover, qualify, and relay engineering repository work across multiple agents using a compact repo-wide agents/agentchain.md index plus immutable chain-scoped endpoint files. Use for engineering implementation, investigation, audit, PR progression, abrupt agent loss, expert takeover, multi-agent workstreams, AUTO MODE, and long-running tasks spanning multiple PRs. Enforce maintainable modular implementation, explicit engineering authority boundaries, validation integrity, source custody, and crash-safe takeover. Every durable endpoint records trusted repository state, inputs/benchmarks/common and governing documents, exact next action, protected authority, validation limits, and exactly five repository-specific questions for the next agent. Graceful handoff is optional and candidate self-qualification never grants engineering-critical write authority.
---

# Engineering PR Delivery v2 — Relay Engineering

## Governing objective

Run engineering work as a crash-safe relay.

The repository owns the baton. The outgoing agent, chat session, and private reasoning are never required for recovery.

Use:

```text
agents/agentchain.md                         repo-wide traffic/index log
agents/agentchain/<CHAIN_ID>/<ENDPOINT>.md  immutable detailed endpoint
```

The split is intentional. A single ever-growing Markdown baton becomes a multi-agent write hotspot. The repo-wide index stays small; detailed endpoints are created once and never rewritten.

## 1. Core invariants

```text
R1  Repository state, not conversation memory, is the baton.
R2  Agent disappearance is a normal recoverable condition.
R3  agents/agentchain.md is the compact repo-wide index/log.
R4  Detailed endpoint files are immutable after durable creation.
R5  Every non-terminal endpoint contains exactly five next-agent questions.
R6  Questions test the NEXT unresolved engineering work.
R7  Every endpoint lists inputs, benchmarks, common/governing docs,
    authoritative sources, production paths, and validation paths.
R8  Incoming engineering-critical takeover begins READ_ONLY.
R9  Candidate answers do not grant authority; self-verification is invalid.
R10 Qualification is bound to a material repository state.
R11 NOT_RUN, unresolved assumptions, blockers, and risks survive the relay.
R12 A chain may span many agents, commits, branches, and PRs.
R13 PR merge does not imply engineering-chain completion.
R14 Every non-terminal endpoint has one exact next safe action.
R15 Detailed evidence stays in its owning artifact; endpoints index it.
R16 ACTIVE CHAINS must point to the actual latest endpoint for that chain.
R17 PREVIOUS_ENDPOINT is chain-local and cannot skip or cross chains.
R18 New production modules normally stay <= 300 physical lines; exceeding
    the threshold requires review and justification, not metric gaming.
R19 Functions/methods normally stay <= 40 logical lines; split when a
    coherent responsibility, invariant, failure mode, or test seam exists.
R20 Module boundaries follow responsibility, state ownership, and
    engineering authority boundaries, not arbitrary line-count splitting.
R21 New abstractions require a real production consumer in the same PR
    unless an explicitly approved staged prerequisite says otherwise.
R22 New unused production modules are 0 by default.
R23 Hidden globals and implicit singleton engineering authority are prohibited.
R24 Source authority, applicability, numerical mechanics, independent oracle,
    publication/release authority, and presentation remain separable.
R25 Every production-coding leg records a pre/post code-quality review and
    explicitly justifies any size, modularity, or ownership exception.
```

Read `references/relay-model.md`, `references/agentchain-schema.md`, and `references/code-quality.md`.

## 2. Durable work identity

```text
REPOSITORY
  -> CHAIN_ID
  -> LEG_ID
  -> ENDPOINT_ID
  -> PR / branch / commits
```

`CHAIN_ID` identifies the engineering mission and survives PR transitions. A new PR for the same unresolved mission normally starts a new leg, not a new chain.

## 3. Repo-wide index

Primary index:

```text
agents/agentchain.md
```

It contains only:

1. `ACTIVE CHAINS` — mutable current traffic table;
2. `ENDPOINT LOG` — compact append-only endpoint rows.

Every non-terminal chain must have exactly one active row pointing to its actual latest endpoint and endpoint file. Completed/superseded chains leave the active table but remain in the endpoint log.

Do not put full calculations, investigation narratives, or full endpoint bodies into the index.

## 4. Detailed endpoints

Default path:

```text
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

Create a new file at every durable endpoint. Never edit a durable endpoint merely to make history cleaner. Correct it with a later endpoint and explicit supersession fields.

Every non-terminal endpoint must contain:

- mission and current state;
- completed/current/remaining work;
- exactly one exact next action;
- known/proven and not-proven state;
- explicit `NOT_RUN`;
- current hypothesis and falsifier;
- protected invariants, do-not-redo, do-not-change;
- expected next-leg files/domains;
- Inputs;
- Benchmarks;
- Common/governing documents;
- Authoritative sources;
- Production paths;
- Validation/test paths;
- changed-this-leg summary;
- validation summary;
- code-quality gate result and justified exceptions when production code changed;
- open risks/questions;
- exactly Q1–Q5 for the next agent.

Read `references/source-indexing.md`.

## 5. Endpoint triggers

Create an endpoint at meaningful durable transitions, especially:

```text
before first engineering-critical mutation
post coherent implementation unit
after material hypothesis change
after important validation PASS/FAIL
blocker change
before/after PR transition
before intentional stop
before merge request
recovery after agent loss
ready for next engineering leg
chain completion
```

Do not create endpoints for trivial commentary-only changes.

## 6. Incoming takeover

For engineering-critical takeover:

```text
TAKEOVER_AUTHORITY = READ_ONLY
```

Then:

1. read `agents/agentchain.md`;
2. find the chain and latest endpoint file;
3. read the endpoint-listed inputs, benchmarks, common/governing docs, authoritative sources, production paths, and validation paths;
4. fetch live main/PR/head/diff/reviews/checks;
5. reconcile live state with the endpoint;
6. inspect any material commits after the endpoint;
7. answer Q1–Q5;
8. obtain an independent verifier verdict;
9. only after a valid verdict acquire engineering-critical write authority.

Do not require the outgoing agent.

## 7. Five-question gate

Every non-terminal endpoint has exactly:

```text
Q1 Production Trace
Q2 Current Unresolved Problem / Failure Isolation
Q3 Authority / Invariant
Q4 Independent Validation
Q5 Next Contribution / Minimal Patch
```

The questions must be generated from the current unresolved next leg, not generic theory and not retrospective praise of the completed leg.

Read `references/qualification.md`.

## 8. Separation of qualification roles

Keep separate artifacts:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

Rules:

```text
candidate != verifier
candidate cannot self-award WRITE_ALLOWED
verdict basis == question material basis
total >= 92/100
every question >= 17/20
```

A verifier may still fail a numeric pass for a substantive automatic-failure reason such as fabricated evidence or unsafe authority claims.

## 9. Crash recovery

If an agent disappears, recover from the latest indexed endpoint and live repository state.

If later commits exist after the endpoint:

```text
ENDPOINT_HEAD -> live PR HEAD
```

inspect every material commit and classify:

```text
RECOVERABLE
PARTIAL_UNKNOWN
CONTAMINATED
UNTRUSTED
```

Then create a recovery endpoint. Never pretend an abrupt loss was a graceful handoff.

If an endpoint file exists but the index was not updated before the crash, treat it as an orphan durable artifact: reconcile it, then repair the index with explicit recovery provenance rather than deleting it.

Read `references/crash-recovery.md`.

## 10. Qualification freshness

Bind question sets to:

```text
QUALIFICATION_BASIS_HEAD
QUESTION_SET_ID
QUESTION_SET_STATUS
```

Material changes to production, tests, benchmarks, oracles, engineering inputs, source authority, behavior-changing configuration, methodology, or publication authority make the old question set stale.

Metadata-only relay/index synchronization does not by itself change the material basis.

## 11. Engineering validation integrity

For material checks distinguish:

```text
STATUS      PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION execution | source inspection | artifact inspection | inference
ORACLE      implementation-coupled | independent reproduction |
            analytical | authoritative reference | cross-solver | experimental
```

Never weaken tolerances, overwrite independent expected values from production output, delete difficult benchmarks, silence fail-closed behavior, or call `NOT_RUN` a PASS.

Read `references/engineering-validation.md` and `references/anti-gaming-rules.md`.

## 12. Multi-agent coordination

Before mutation and before a new leg, compare active chains for:

- exact-file/path overlap;
- authority-domain overlap;
- benchmark/oracle overlap;
- dependency/stacking;
- base drift.

Classify:

```text
SAFE
COORDINATION_REQUIRED
BLOCKED_BY_ACTIVE_CHAIN
UNKNOWN
```

The compact index is traffic control, not proof that semantic overlap is absent.

Read `references/multi-agent-coordination.md`.

## 13. Code quality and maintainability

Apply the code-quality gate to every leg that changes production code.

Default review thresholds:

```text
new production module     normally <= 300 physical lines
function / method          normally <= 40 logical lines
```

These are design-review triggers, not blind hard limits. Do not game them by creating arbitrary `part1`/`part2` files or meaningless wrappers.

Before material coding, identify:

- the existing owner implementation;
- the intended module responsibility;
- engineering/software authority boundaries;
- state and mutation ownership;
- expected size and meaningful extraction boundaries;
- independent test seams;
- the real production consumer for every new abstraction;
- any existing calculation/source/tolerance implementation that would otherwise be duplicated.

After implementation, verify:

```text
new modules <= 300 lines or exception justified
functions <= 40 logical lines or exception justified
no god module / mixed authority owner introduced
no hidden globals or implicit singleton authority
mutation boundaries explicit
no circular ownership
new unused production modules = 0 unless explicitly staged
no duplicate production engineering calculation path
source / calculation / oracle / publication / UI boundaries preserved
negative / fail-closed behavior tested where applicable
no unrelated refactor or formatting churn
```

For engineering software, modularity follows domain and authority boundaries before cosmetic size goals. A cohesive justified 330-line numerical kernel can be safer than three artificial files that obscure ownership; conversely a 220-line module that mixes source authority, solver mechanics, and publication authority should be split even though it is below the size threshold.

Read `references/code-quality.md`.

## 14. PR discipline

A PR is a delivery container, not the durable work identity.

Keep one coherent assignment per PR unless scope is explicitly changed. Never infer chain completion from merge. Never merge without owner authorization.

Read `references/git-pr-policy.md`.

## 15. AUTO MODE

`AUTO MODE` permits automatic progression through an approved plan; it does not waive qualification, source authority, validation integrity, code-quality gates, destructive-operation limits, or merge authority.

While AUTO is active, continue through ordinary successful phases, create durable endpoints at material transitions, and stop only at defined hard stops.

Read `references/auto-mode.md`.

## 16. Chain completion

Distinguish:

```text
AGENT_LEG_COMPLETE
PR_COMPLETE
CHAIN_COMPLETE
```

A terminal endpoint uses:

```text
STATE: COMPLETE
NEXT_AGENT_QUALIFICATION: NOT_REQUIRED
QUESTION_SET_STATUS: NOT_REQUIRED
COMPLETION_BASIS:
```

Remove the chain from `ACTIVE CHAINS` but retain its endpoint-log history.

## 17. Executable checks

Use:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py agents/agentchain.md
python skills/engineering-pr-delivery-v2/scripts/validate_qualification.py <answer.md> <verdict.md>
python skills/engineering-pr-delivery-v2/scripts/check_relay.py agents/agentchain.md [<answer.md> <verdict.md>]
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Structural checks do not replace expert engineering verification. Code-size thresholds do not replace architectural review. A syntactically perfect generic or fabricated answer must still fail substantive verification.
