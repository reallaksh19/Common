---
name: engineering-pr-delivery-v2
description: Execute, recover, qualify, and relay engineering repository work across multiple agents using chain-local mutable state under agents/chains/<CHAIN_ID>/ACTIVE.md plus immutable chain-scoped endpoints. Use for engineering implementation, investigation, audit, PR progression, abrupt agent loss, expert takeover, concurrent WRC/LAFEA/LoadCalc workstreams, AUTO MODE, and long-running tasks spanning multiple PRs. Enforce maintainable modular implementation, explicit engineering authority boundaries, validation integrity, source custody, stale-write protection, and crash-safe takeover. Every durable endpoint records trusted repository state, inputs/benchmarks/common and governing documents, exact next action, protected authority, validation limits, and exactly five repository-specific questions for the next agent. Graceful handoff is optional and candidate self-qualification never grants engineering-critical write authority.
---

# Engineering PR Delivery v2 — Relay Engineering

## Governing objective

Run engineering work as a crash-safe, concurrency-safe relay.

The repository owns the baton. The outgoing agent, chat session, and private reasoning are never required for recovery.

For new chains use:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md                    mutable chain-local current state
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md  immutable detailed endpoint
agents/qualifications/<CHAIN_ID>/...                 qualification artifacts
```

Compatibility / derived navigation:

```text
agents/agentchain.md
```

The split is intentional. Independent WRC, LAFEA, LoadCalc, and other agents should not edit one shared relay pointer merely because they work in the same repository.

## 1. Core invariants

```text
R1  Repository state, not conversation memory, is the baton.
R2  Agent disappearance is a normal recoverable condition.
R3  Each canonical chain owns one mutable agents/chains/<CHAIN_ID>/ACTIVE.md.
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
R16 ACTIVE.md must point to the actual latest accepted endpoint for its chain.
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
R26 ENDPOINT_ID is unique within CHAIN_ID; the durable key is
    (CHAIN_ID, ENDPOINT_ID), not ENDPOINT_ID alone.
R27 Canonical chain custody advances by CUSTODY_EPOCH + 1 using exact prior
    ACTIVE.md repository version/blob; stale writes fail closed and re-ground.
R28 agents/agentchain.md is derived/legacy navigation for canonical chains,
    not the authoritative mutable pointer and not required on every endpoint.
```

Read `references/relay-model.md`, `references/agentchain-schema.md`, `references/chain-concurrency.md`, and `references/code-quality.md`.

## 2. Durable work identity

```text
REPOSITORY
  -> CHAIN_ID
  -> LEG_ID
  -> ENDPOINT_ID
  -> PR / branch / commits
```

`CHAIN_ID` identifies the engineering mission and survives PR transitions. A new PR for the same unresolved mission normally starts a new leg, not a new chain.

Endpoint identity is chain-scoped:

```text
ADV-WRC-1389/EP-0001
ADV-LAFEA-1422/EP-0001
ADV-LOADCALC-1505/EP-0001
```

All three are valid simultaneously.

## 3. Chain-local current state

Canonical current-state file:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
```

Required fields:

```text
CHAIN_STATE_VERSION
CHAIN_ID
MISSION
ACTIVE_ENDPOINT
ACTIVE_ENDPOINT_FILE
PR
BRANCH
HEAD
STATE
AUTHORITY_DOMAIN
ACTIVE_CUSTODIAN
CUSTODY_EPOCH
COORDINATION_STATE
DEPENDENCIES
```

Every chain writes only its own `ACTIVE.md`.

Before advancing it:

1. read the exact current repository blob/version and `CUSTODY_EPOCH`;
2. create the next immutable endpoint with `epoch + 1`;
3. update `ACTIVE.md` against the exact prior version;
4. if the write conflicts or the epoch changed, classify `STALE_WRITE`, return READ_ONLY, re-ground, and reconcile.

Do not force a stale pointer.

Repository-wide traffic is discovered by scanning:

```text
agents/chains/*/ACTIVE.md
```

A shared dashboard may be rendered for convenience, but normal endpoint progression does not require a dashboard commit.

## 4. Detailed endpoints

Default path:

```text
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

Create a new file at every durable endpoint. Never edit a durable endpoint merely to make history cleaner. Correct it with a later endpoint and explicit supersession/reconciliation fields.

Every canonical endpoint also records:

```text
CUSTODY_EPOCH: <positive integer>
```

The first endpoint uses `1`; every accepted direct successor increments by exactly one.

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
same-chain custody reconciliation
ready for next engineering leg
chain completion
```

Do not create endpoints for trivial commentary-only edits.

## 6. Incoming takeover

For engineering-critical takeover:

```text
TAKEOVER_AUTHORITY = READ_ONLY
```

Then:

1. locate the chain under `agents/chains/<CHAIN_ID>/ACTIVE.md`;
2. open its referenced active endpoint;
3. read the endpoint-listed inputs, benchmarks, common/governing docs, authoritative sources, production paths, and validation paths;
4. fetch live main/PR/head/diff/reviews/checks;
5. reconcile live state, current `CUSTODY_EPOCH`, and endpoint state;
6. inspect any material commits and orphan/divergent endpoint files after the active endpoint;
7. answer Q1–Q5;
8. obtain an independent verifier verdict;
9. only after a valid verdict acquire engineering-critical write authority.

For a legacy-format chain that has not migrated, recover from its existing `agents/agentchain.md` locator instead. Do not require the outgoing agent.

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

Question-set IDs should be visibly chain-namespaced, for example `QS-ADV-WRC-1389-0012`.

## 9. Crash recovery

If an agent disappears, recover from that chain's `ACTIVE.md`, referenced immutable endpoint, and live repository state.

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

If an endpoint exists but `ACTIVE.md` was not advanced, treat it as an orphan durable artifact. If another agent already advanced `ACTIVE.md`, do not overwrite it; re-ground and reconcile same-chain custody.

Read `references/crash-recovery.md` and `references/chain-concurrency.md`.

## 10. Qualification freshness

Bind question sets to:

```text
QUALIFICATION_BASIS_HEAD
QUESTION_SET_ID
QUESTION_SET_STATUS
```

Material changes to production, tests, benchmarks, oracles, engineering inputs, source authority, behavior-changing configuration, methodology, or publication authority make the old question set stale.

Relay metadata-only changes do not by themselves change the material basis.

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

Different chains own different relay files. Do not create a coordination problem merely because several agents work in one repository.

Before mutation and before a new leg, compare active chains for:

- exact-file/path overlap;
- authority-domain overlap;
- benchmark/oracle overlap;
- controlled-input overlap;
- release/publication overlap;
- dependency/stacking;
- base drift.

Classify:

```text
SAFE
COORDINATION_REQUIRED
BLOCKED_BY_ACTIVE_CHAIN
UNKNOWN
```

Examples:

```text
WRC src/core/emp1/** vs LAFEA src/core/lafea/**
  -> likely SAFE if authority/benchmarks/inputs are also independent

WRC and LAFEA both modify src/core/non-fea-common-checker/**
  -> COORDINATION_REQUIRED

separate files but both change canonical units/source authority
  -> COORDINATION_REQUIRED or BLOCKED
```

Same-chain concurrent advancement is different: one `ACTIVE.md` + one custody epoch sequence. Divergent successors must reconcile before either becomes authoritative.

Read `references/multi-agent-coordination.md` and `references/chain-concurrency.md`.

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

`AUTO MODE` permits automatic progression through an approved plan; it does not waive qualification, source authority, validation integrity, concurrency/custody checks, code-quality gates, destructive-operation limits, or merge authority.

While AUTO is active, continue through ordinary successful phases, create durable endpoints at material transitions, use compare-and-swap discipline when advancing `ACTIVE.md`, and stop on stale write, real authority overlap, or other defined hard stops.

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

Advance that chain's `ACTIVE.md` to the terminal endpoint/epoch. Derived dashboards omit terminal chains automatically. Retain immutable endpoint history.

## 17. Legacy compatibility

Existing repositories may contain:

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
```

Preserve these artifacts as historical/recovery evidence. Do not mass-rewrite immutable history.

Existing legacy-format chains may finish under the legacy structure or migrate deliberately at a new endpoint. New chains and independent new workstreams should use `agents/chains/**`.

## 18. Executable checks

Canonical chain-local store:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_chain_store.py .
python skills/engineering-pr-delivery-v2/scripts/detect_chain_overlap.py .
python skills/engineering-pr-delivery-v2/scripts/render_agentchain_dashboard.py .
python skills/engineering-pr-delivery-v2/scripts/check_relay.py . [<answer.md> <verdict.md>]
```

Legacy shared-index store:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py agents/agentchain.md
python skills/engineering-pr-delivery-v2/scripts/check_relay.py agents/agentchain.md [<answer.md> <verdict.md>]
```

Qualification:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_qualification.py <answer.md> <verdict.md>
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Structural checks do not replace expert engineering verification. Code-size thresholds do not replace architectural review. A syntactically perfect generic or fabricated answer must still fail substantive verification.
