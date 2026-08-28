---
name: engineering-pr-delivery-v2
description: Crash-safe, qualification-first engineering PR delivery. Every non-terminal endpoint is handover-ready before an agent can disappear: it carries a concise <300-word recovery snapshot, exact work baton, owner-roadmap/input/governing-document custody, and five pre-authored expert takeover questions. A replacement agent qualifies first against the last accepted endpoint while READ_ONLY; only after independent PASS may it reconcile crash-window/live drift and then acquire write authority. Use for engineering implementation, FEA/WRC/piping calculations, CAESAR/fixed-format writers, audits, PR progression, abrupt agent loss, concurrent workstreams, and AUTO MODE.
---

# Engineering PR Delivery v2 — qualification-first relay

## 1. Governing objective

The repository must remain **handover-ready after any agent crash**. A replacement agent must not need the outgoing chat or outgoing agent.

The first substantive gate for a replacement agent is **takeover qualification**, not recovery work and not implementation.

Only a minimal READ_ONLY bootstrap is allowed before qualification:

```text
locate repo / chain / ACTIVE.md / latest endpoint
locate PR and pinned qualification basis
confirm the pinned basis and question set are readable
```

The candidate may inspect pinned repository code, tests, benchmark data, roadmap, source material, and perform calculations needed to answer Q1-Q5. That is examination activity, not task execution.

A replacement agent may not before qualification PASS:

- advance `ACTIVE.md` or custody epoch;
- create a recovery endpoint as accepted custody;
- modify production/tests/oracles/roadmaps;
- salvage/reconcile crash-window commits as authoritative decisions;
- resume AUTO MODE;
- grant itself write authority.

## 2. Protocol precedence and preserved rules

This file is canonical. Detailed current references named here are binding. `references/protocol-foundation-v2.2.md` preserves the full immediately preceding v2 protocol and remains binding where this qualification-first revision does not supersede it.

The following existing controls remain unchanged unless explicitly strengthened here:

- chain-local `agents/chains/<CHAIN_ID>/**` custody and stale-write protection;
- owner-governed roadmap rules;
- source/benchmark/oracle separation;
- validation integrity and explicit `NOT_RUN`;
- code-quality/modularity gates;
- multi-agent overlap detection;
- AUTO MODE scope limits;
- owner-only merge unless explicitly authorized;
- no silent fallback engineering data.

Read at minimum:

```text
references/qualification.md
references/handover-snapshot.md
references/authority-state-model.md
references/crash-recovery.md
references/owner-roadmaps.md
references/chain-concurrency.md
references/code-quality.md
```

## 3. Core invariants

```text
R1  Repository state, not conversation memory, is the baton.
R2  Every non-terminal accepted endpoint is handover-ready.
R3  Q1-Q5 are takeover qualification only; they are never the task list.
R4  EXACT_NEXT_ACTION is the work baton for a qualified custodian.
R5  A replacement agent qualifies before substantive recovery/reconciliation.
R6  Qualification PASS is necessary but not sufficient for WRITE_ALLOWED.
R7  After PASS, crash-window/live/roadmap drift is reconciled READ_ONLY.
R8  WRITE_ALLOWED requires both qualification and cleared current-state authority.
R9  Q1-Q5 are pre-authored at every non-terminal endpoint for the next unresolved work.
R10 Questions are implementation/engineering examinations, not generic descriptions.
R11 Where technically applicable, at least two questions require numerical/hand reconstruction.
R12 Every set requires live repository anchors, an independent oracle, a falsifier, and a safe patch boundary.
R13 Candidate self-verification cannot grant authority.
R14 A crash after the endpoint does not erase qualification readiness: qualify against the pinned accepted basis, then reconcile the crash window after PASS.
R15 Owner roadmap mutation remains separately owner-authorized.
R16 NOT_RUN, blockers, assumptions, and authority boundaries survive the relay.
R17 Endpoint IDs remain chain-local; custody epochs protect same-chain writes.
R18 Merge authority remains independent of qualification, validation, and roadmap authority.
```

## 4. Chain state version 3

New chains and the next material leg/custodian transition should use:

```text
CHAIN_STATE_VERSION: 3
```

Version 3 keeps `STATE` only as a derived compatibility summary. Authority comes from orthogonal fields:

```text
ENGINEERING_STATE: READY | IN_PROGRESS | BLOCKED | COMPLETE
CUSTODY_STATE: HELD | VACANT | TAKEOVER_REQUIRED | QUALIFIED_PENDING_RECONCILIATION | RECONCILING
QUALIFICATION_STATE: NOT_REQUIRED | PENDING | PASS | FAIL | DEFERRED
WRITE_AUTHORITY: READ_ONLY | WRITE_ALLOWED | BLOCKED
AUTO_STATE: RUNNING | PAUSED | BLOCKED | NOT_APPLICABLE
MERGE_AUTHORITY: OWNER_ONLY | AUTHORIZED
```

Also retain the existing chain identity/custody/roadmap fields:

```text
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
ROADMAPS
ROADMAP_REVIEW_STATUS
HANDOVER_READY
```

`WRITE_ALLOWED` is valid only when current custody is `HELD` and qualification/current-state authority allows it.

A replacement that has passed the exam but has not reconciled current state uses:

```text
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
QUALIFICATION_STATE: PASS
WRITE_AUTHORITY: READ_ONLY
```

Read `references/authority-state-model.md`.

## 5. Handover-ready endpoint

Every non-terminal endpoint contains two clearly separated outputs:

```text
A. WORK BATON
   what the qualified custodian does next

B. TAKEOVER QUALIFICATION PACK
   whether a replacement is competent to take custody
```

It also contains a `### Handover snapshot` of fewer than 300 words. The snapshot must concisely include:

1. repo, task, chain, endpoint;
2. PR/branch/head/main/status and merge authority;
3. roadmap, inputs, benchmarks, governing docs/source pointers;
4. engineering/custody/qualification/write state, blocker, exact next action;
5. concise Q1-Q5 prompts.

Detailed evidence stays in the endpoint inventories and qualification pack; the snapshot points to it rather than duplicating it.

Read `references/handover-snapshot.md` and `references/agentchain-template.md`.

## 6. Always-ready crash discipline

Before a material engineering batch, the current accepted endpoint must already describe the exact intended next action and contain Q1-Q5 capable of qualifying a replacement to understand that boundary.

After a coherent material batch, create the next endpoint **before starting another material batch**.

Therefore, if an agent crashes:

```text
last accepted endpoint
+ pinned qualification basis
+ pre-authored Q1-Q5
+ exact next action / expected patch boundary
```

remain available even if later crash-window commits exist.

Crash-window commits do not automatically invalidate the exam. The exam qualifies the candidate against the last accepted basis. After PASS, the qualified candidate reconciles every later commit/diff before acquiring write authority.

If the pinned basis itself is unavailable/corrupt or the question artifact is malformed, qualification cannot proceed and an independent question authority/Owner must repair the qualification artifact; the candidate may not author an easier replacement exam and self-qualify.

## 7. Qualification-first takeover

For a new/replacement engineering-critical agent:

```text
TAKEOVER_AUTHORITY: READ_ONLY
```

Sequence:

```text
1. minimal locator/bootstrap only
2. answer pinned Q1-Q5 from repository + engineering evidence
3. independent verifier scores the answer
4. FAIL/DEFERRED -> remain READ_ONLY
5. PASS -> QUALIFIED_PENDING_RECONCILIATION, still READ_ONLY
6. reconcile live PR/main, crash-window commits, active chains, roadmap/source drift
7. if safe -> CUSTODY_STATE HELD + WRITE_AUTHORITY WRITE_ALLOWED
8. execute EXACT_NEXT_ACTION
```

Qualification proves **technical competence**. Reconciliation proves **current-state safety**. Neither substitutes for the other.

For an existing v1/v2 chain, do not rewrite history. Use its latest accepted Q1-Q5 for qualification first. After PASS and current-state reconciliation, migrate to version 3 at a new endpoint before material mutation.

## 8. Q1-Q5 expert qualification standard

Exactly five questions remain in every non-terminal endpoint, but the semantic standard is strengthened:

```text
Q1 Production Trace
   actual live object/case/value; exact files/functions/IDs/hashes; end-to-end reconstruction

Q2 Current Unresolved Problem / Failure Isolation
   real hand/numerical or technical reconstruction; predicted intermediates; first wrong boundary

Q3 Authority / Invariant
   source/ownership boundary plus exact falsifier and invalid shortcut

Q4 Independent Validation
   independent hand calculation/published oracle/cross-solver/byte-level reconstruction with units/signs/tolerance

Q5 Next Contribution / Minimal Patch
   examination of the SAFE implementation boundary; exact files/functions, before/after values, tests, rollback and NO-PATCH condition
```

Q5 is **not an instruction to patch**. It tests whether the candidate knows when and where a patch would be authorized.

Minimum set quality, where the domain permits:

```text
>=2 numerical/hand or equivalent technical reconstructions
>=3 questions requiring exact live-repository evidence
>=1 end-to-end production trace
>=1 independent engineering oracle
>=1 explicit falsifier
>=1 exact safe-patch design with NO-PATCH condition
```

For non-numerical software domains, byte offsets, pointer/cardinality arithmetic, parser state transitions, topology ownership, deterministic hashes, or equivalent exact technical reconstruction may substitute for arithmetic. The substitute must be explicit and technically demanding.

Generic questions such as `Explain the solver`, `Describe the benchmark`, `Which file would you inspect?`, or `What would you change?` are invalid.

Read `references/qualification.md`.

## 9. Qualification roles and scoring

Artifacts remain separate:

```text
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

Rules:

```text
candidate != verifier
candidate cannot self-award WRITE_ALLOWED
question set is pre-authored by the prior accepted endpoint author/question authority
verdict basis == pinned qualification basis
total >= 92/100
every question >= 17/20
```

A candidate may inspect and calculate extensively while answering. It may not make accepted repository mutations as part of the exam.

Verdicts should distinguish competence from write authority:

```text
PASS_QUALIFIED_READ_ONLY
FAIL_READ_ONLY
DEFERRED_READ_ONLY
INVALID_SELF_VERIFIED
```

`PASS_QUALIFIED_READ_ONLY` moves the candidate to post-qualification reconciliation; it does not itself set `WRITE_ALLOWED`.

## 10. Roadmaps, validation, concurrency, AUTO, merge

All prior v2.2 controls remain binding. In particular:

- applicable owner roadmap(s) are read/pinned before material coding;
- agents may propose roadmap changes but cannot mutate owner roadmaps without explicit owner authorization;
- roadmap/source/benchmark/oracle authority is reconciled after qualification before write enablement;
- validation distinguishes PASS/FAIL/NOT_RUN/NOT_APPLICABLE and independent vs implementation-coupled evidence;
- cross-chain authority overlap is checked before mutation;
- AUTO MODE pauses on agent loss and cannot resume merely because qualification passed;
- merge remains owner-only unless separately authorized.

## 11. Executable controls

For canonical chains:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_chain_store.py .
python skills/engineering-pr-delivery-v2/scripts/validate_roadmap_bindings.py .
python skills/engineering-pr-delivery-v2/scripts/validate_handover_snapshot.py .
python skills/engineering-pr-delivery-v2/scripts/validate_qualification_questions.py .
python skills/engineering-pr-delivery-v2/scripts/check_relay.py . [answer.md verdict.md]
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Legacy v1/v2 stores remain readable and are not mass-rewritten.

Structural validation does not replace expert verification. A syntactically valid but technically shallow questionnaire or answer must still fail substantive review.
