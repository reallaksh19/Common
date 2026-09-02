---
name: engineering-pr-delivery-v2
description: Execute, recover, qualify, and relay engineering repository work across multiple agents using a compact repo-wide agents/agentchain.md index plus immutable chain-scoped endpoint files. Use for engineering implementation, investigation, audit, PR progression, abrupt agent loss, expert takeover, multi-agent workstreams, AUTO MODE, and long-running tasks spanning multiple PRs. Every durable endpoint records trusted repository state, inputs/benchmarks/common and governing documents, exact next action, protected authority, validation limits, and exactly five repository-specific questions for the next agent. Graceful handoff is optional. Incoming takeover candidates cannot self-qualify for engineering-critical write authority; a continuous active agent may proceed under explicit owner-authorized continuation when the material basis and bounded scope are durably recorded.
---

# Engineering PR Delivery v2 — Relay Engineering

## Governing objective

Run engineering work as a crash-safe relay without turning relay qualification into an artificial blocker for a continuous active leg.

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
R9  A takeover candidate answer never grants its own write authority;
    self-verification is invalid.
R10 Qualification is bound to a material repository state.
R11 NOT_RUN, unresolved assumptions, blockers, and risks survive the relay.
R12 A chain may span many agents, commits, branches, and PRs.
R13 PR merge does not imply engineering-chain completion.
R14 Every non-terminal endpoint has one exact next safe action.
R15 Detailed evidence stays in its owning artifact; endpoints index it.
R16 ACTIVE CHAINS must point to the actual latest endpoint for that chain.
R17 PREVIOUS_ENDPOINT is chain-local and cannot skip or cross chains.
R18 A continuous active agent is not an incoming takeover candidate merely
    because a new endpoint was created or the owner says proceed.
R19 A continuous active agent may perform bounded engineering-critical mutation
    under explicit OWNER_AUTHORIZED_CONTINUATION when the same material basis,
    scope, protected invariants, and rollback boundary are durably recorded.
R20 Owner-authorized continuation never grants merge authority, destructive
    authority, source-authority widening, benchmark/oracle mutation, or a PASS
    result for validation that was not actually run.
```

Read `references/relay-model.md` and `references/agentchain-schema.md`.

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
agents/agentchain/<CHAIN_ID>/<ENDPOINT>.md
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
- open risks/questions;
- exactly Q1–Q5 for the next agent.

For an owner-authorized continuation endpoint also record:

```text
CONTINUATION_MODE: OWNER_AUTHORIZED_CONTINUATION
CONTINUATION_AGENT_ID:
CONTINUATION_BASIS_HEAD:
OWNER_AUTHORIZATION_EVIDENCE:
AUTHORIZED_SCOPE:
PROHIBITED_SCOPE:
ROLLBACK_OR_STOP_CONDITION:
```

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

For engineering-critical **incoming takeover or recovery**:

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
9. only after a valid verdict acquire engineering-critical takeover write authority.

Do not require the outgoing agent.

## 6A. Continuous active-agent continuation

Do **not** reclassify the current active agent as an incoming takeover candidate solely because:

- the owner says `proceed`, `continue`, `next`, or otherwise explicitly authorizes the next bounded implementation step;
- the agent creates a new durable endpoint during the same active leg;
- relay metadata commits move the branch head without changing material engineering state.

A continuous active agent may acquire bounded write authority without a candidate/verifier cycle when all of the following are true:

```text
same active engineering agent / same continuous leg
explicit owner authorization to continue
material engineering basis reconciled and unchanged, or newly re-grounded
coordination state is SAFE or explicitly bounded
exact authorized production/test scope recorded before mutation
protected unchanged domains recorded
validation/falsifier and rollback/stop condition recorded
merge authority remains OWNER_ONLY
```

Record before mutation:

```text
CONTINUATION_MODE: OWNER_AUTHORIZED_CONTINUATION
ENGINEERING_CRITICAL_WRITE_AUTHORITY: BOUNDED
```

This is **not self-verification**. No candidate verdict is created because no takeover candidate exists. Engineering validation after the patch must still distinguish PASS / FAIL / NOT_RUN, and independent engineering evidence remains required where the engineering problem itself demands it.

Hard stops that terminate continuation authority and require re-grounding or takeover qualification include:

```text
agent/session handoff to a different engineering agent
crash recovery where active-agent continuity cannot be established
material source-authority contradiction
unplanned scope expansion beyond the recorded authorized scope
benchmark/oracle/tolerance/workflow mutation not explicitly authorized
coordination state becomes BLOCKED_BY_ACTIVE_CHAIN or UNKNOWN
owner revokes or narrows authorization
```

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

For continuous owner-authorized work, Q1–Q5 remain recovery material for the **next** agent; the current continuous agent does not need to answer its own endpoint questions to keep working.

Read `references/qualification.md`.

## 8. Separation of qualification roles

For takeover qualification, keep separate artifacts:

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

These candidate/verifier artifacts are not required to manufacture authority for a continuous active agent operating under Section 6A.

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

Then create a recovery endpoint. Never pretend an abrupt loss was continuous-agent continuation.

If an endpoint file exists but the index was not updated before the crash, treat it as an orphan durable artifact: reconcile it, then repair the index with explicit recovery provenance rather than deleting it.

Read `references/crash-recovery.md`.

## 10. Qualification freshness

Bind takeover question sets to:

```text
QUALIFICATION_BASIS_HEAD
QUESTION_SET_ID
QUESTION_SET_STATUS
```

Material changes to production, tests, benchmarks, oracles, engineering inputs, source authority, behavior-changing configuration, methodology, or publication authority make the old takeover question set stale.

Metadata-only relay/index synchronization does not by itself change the material basis.

Owner-authorized continuation authority is likewise bound to its recorded `CONTINUATION_BASIS_HEAD` and `AUTHORIZED_SCOPE`; scope expansion requires a new continuation endpoint and explicit owner authorization.

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

## 13. PR discipline

A PR is a delivery container, not the durable work identity.

Keep one coherent assignment per PR unless scope is explicitly changed. Never infer chain completion from merge. Never merge without owner authorization.

Read `references/git-pr-policy.md`.

## 14. AUTO MODE

`AUTO MODE` permits automatic progression through an approved plan; it does not waive source authority, validation integrity, destructive-operation limits, coordination limits, or merge authority.

AUTO MODE does not manufacture owner-authorized continuation. The owner must have explicitly authorized the bounded continuation scope, or an incoming takeover must have passed qualification.

While AUTO is active, continue through ordinary successful phases, create durable endpoints at material transitions, and stop only at defined hard stops.

Read `references/auto-mode.md`.

## 15. Chain completion

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

## 16. Executable checks

Use:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py agents/agentchain.md
python skills/engineering-pr-delivery-v2/scripts/validate_qualification.py <answer.md> <verdict.md>
python skills/engineering-pr-delivery-v2/scripts/check_relay.py agents/agentchain.md [<answer.md> <verdict.md>]
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Qualification scripts apply when takeover qualification artifacts exist. Continuous owner-authorized continuation is validated through endpoint structure, exact scope custody, live diff review, and engineering validation evidence; it must not create fake candidate/verifier artifacts.

Structural checks do not replace expert engineering verification. A syntactically perfect generic or fabricated answer must still fail substantive verification.
