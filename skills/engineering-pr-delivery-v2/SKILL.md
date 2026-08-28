---
name: engineering-pr-delivery-v2
description: Crash-safe, qualification-first engineering PR delivery with centralized cross-repository policy. Downstream AGENTS.md files are project-only overlays; every material leg re-grounds the live Common protocol, uses canonical v3 chain paths, pre-authors expert Q1-Q5 before coding, and exposes the active handover snapshot to the user. A replacement first passes question-set admission, then takeover qualification while READ_ONLY; only after independent PASS and post-basis drift reconciliation may it acquire write authority.
---

# Engineering PR Delivery v2 — qualification-first relay

## 1. Governing objective

The repository must remain **handover-ready after any agent crash**. A replacement agent must not need the outgoing chat or outgoing agent.

Reusable cross-repository policy lives in this Common skill. Repository-root `AGENTS.md` files are project overlays only; they must not fork or copy the relay/qualification state machine.

For a replacement agent, the first engineering competence gate is takeover qualification. Before the exam, only a narrow READ_ONLY **question-set admission** check is allowed to prove that the exam itself is valid.

```text
agent loss / custody change
-> minimal READ_ONLY locator bootstrap
-> QUESTION-SET ADMISSION
-> TAKEOVER QUALIFICATION FIRST
-> independent PASS_QUALIFIED_READ_ONLY
-> post-basis reconciliation while READ_ONLY
-> drift/authority classification
-> WRITE_ALLOWED only if current-state authority is safe
-> execute EXACT_NEXT_ACTION
```

Question-set admission is not task execution and not crash-window recovery. It only validates the exam.

## 2. Protocol precedence and required references

This file is canonical. `references/protocol-foundation-v2.2.md` preserves the full preceding v2 protocol and remains binding where this qualification-first revision does not supersede it.

Read at minimum:

```text
references/repository-agent-policy.md
references/project-agents-template.md
references/qualification.md
references/question-set-admission.md
references/post-basis-drift.md
references/handover-snapshot.md
references/authority-state-model.md
references/crash-recovery.md
references/owner-roadmaps.md
references/chain-concurrency.md
references/code-quality.md
```

The following remain protected unless explicitly strengthened here:

- chain-local `agents/chains/<CHAIN_ID>/**` custody and stale-write protection;
- owner-governed roadmap rules;
- source/benchmark/oracle separation;
- validation integrity and explicit `NOT_RUN`;
- code-quality/modularity gates;
- multi-agent overlap detection;
- AUTO MODE scope limits;
- owner-only merge unless explicitly authorized;
- no silent fallback engineering data.

Where older wording conflicts with this revision, this revision wins. In particular, a question set may be unusable because it is `STALE`, `AUTHORITY_CONTAMINATED`, or `INSUFFICIENT_TECHNICAL_DEPTH`, not only because it is missing or malformed.

## 3. Core invariants

```text
R1  Repository state, not conversation memory, is the baton.
R2  Reusable relay/qualification policy lives in Common; downstream AGENTS.md is project-only.
R3  Every new material leg re-grounds and records the live Common protocol basis.
R4  STALE_PROTOCOL or UNKNOWN protocol status blocks material coding and AUTO progression.
R5  New material legs use canonical v3 chain paths; legacy relay paths are read-only history.
R6  Every non-terminal accepted endpoint is handover-ready before material work starts.
R7  Q1-Q5 are takeover qualification only; they are never the task list.
R8  EXACT_NEXT_ACTION is the work baton for a qualified custodian.
R9  Q1-Q5 are pre-authored before the bounded material batch they protect.
R10 A replacement agent passes question-set admission before taking Q1-Q5.
R11 Admission checks the exam only; it does not recover or mutate engineering work.
R12 A replacement agent qualifies before substantive crash-window recovery/reconciliation.
R13 Qualification PASS is necessary but not sufficient for WRITE_ALLOWED.
R14 After PASS, crash-window/live/roadmap/source drift is reconciled READ_ONLY.
R15 Post-basis drift is explicitly classified before write authority can be granted.
R16 Material boundary/authority drift or contamination forces requalification.
R17 Candidate self-verification, self-admission, or self-confirmation of material coverage cannot grant authority.
R18 Questions are implementation/engineering examinations, not generic descriptions.
R19 Where technically applicable, at least two questions require numerical/hand reconstruction.
R20 Every set requires live repository anchors, an independent oracle, a falsifier, and a safe patch boundary.
R21 Owner roadmap mutation remains separately owner-authorized.
R22 NOT_RUN, blockers, assumptions, and authority boundaries survive the relay.
R23 Endpoint IDs remain chain-local; custody epochs protect same-chain writes.
R24 Merge authority remains independent of qualification, validation, roadmap authority, and write authority.
R25 At every substantive handover/status boundary the user sees the active snapshot including Q1-Q5; saying only that they exist is invalid.
```

## 4. Chain state version 3

New chains and the next material leg/custodian transition use `CHAIN_STATE_VERSION: 3`.

Authority planes:

```text
ENGINEERING_STATE: READY | IN_PROGRESS | BLOCKED | COMPLETE
CUSTODY_STATE: HELD | VACANT | TAKEOVER_REQUIRED | QUALIFIED_PENDING_RECONCILIATION | RECONCILING
QUALIFICATION_STATE: NOT_REQUIRED | PENDING | PASS | FAIL | DEFERRED | REQUALIFICATION_REQUIRED
WRITE_AUTHORITY: READ_ONLY | WRITE_ALLOWED | BLOCKED
AUTO_STATE: RUNNING | PAUSED | BLOCKED | NOT_APPLICABLE
MERGE_AUTHORITY: OWNER_ONLY | AUTHORIZED
```

Also retain chain identity, PR/head, custody epoch, coordination, dependencies, roadmap binding/review state, `HANDOVER_READY`, and the protocol-adoption fields:

```text
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <live Common commit SHA actually read>
COMMON_PROTOCOL_STATUS: CURRENT | STALE_PROTOCOL | UNKNOWN
```

A replacement that passed the exam but has not reconciled current state is:

```text
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
QUALIFICATION_STATE: PASS
WRITE_AUTHORITY: READ_ONLY
```

If post-basis reconciliation finds changed engineering/authority boundaries:

```text
QUALIFICATION_STATE: REQUALIFICATION_REQUIRED
WRITE_AUTHORITY: READ_ONLY
```

Read `references/authority-state-model.md`.

## 5. Repository overlay and protocol-adoption gate

Repository-root `AGENTS.md` is a project overlay only. Follow `references/repository-agent-policy.md` and `references/project-agents-template.md`.

Before every new material leg, including AUTO progression into another bounded implementation/source/benchmark/publication leg:

```text
1. read the project overlay
2. re-ground live Common engineering-pr-delivery-v2
3. record COMMON_PROTOCOL_BASIS
4. classify COMMON_PROTOCOL_STATUS
5. confirm CHAIN_STATE_VERSION: 3
6. confirm canonical agents/chains/** custody
7. confirm no new legacy relay write is planned
8. only then prepare the pre-work endpoint and Q1-Q5
```

Fail closed:

```text
STALE_PROTOCOL | UNKNOWN
-> READ_ONLY
-> NO MATERIAL CODING
-> NO AUTO PROGRESSION
```

A historical endpoint's old Common pin is evidence of what governed that historical leg. It is not permission to keep using that pin for a new leg.

Legacy paths such as `agents/agentchain.md` and `agents/agentchain/<CHAIN_ID>/**` are read/cite/recovery provenance only for new v3 work. Do not create new material endpoints there.

## 6. Handover-ready endpoint and visible handover

Every non-terminal endpoint contains two distinct outputs:

```text
A. WORK BATON
   what a qualified custodian does next

B. TAKEOVER QUALIFICATION PACK
   whether a replacement is competent to take custody
```

It also contains a `### Handover snapshot` of fewer than 300 words with:

1. repo, task, chain, endpoint;
2. PR/branch/head/main/status and merge authority;
3. roadmap, inputs, benchmarks, governing docs/source pointers;
4. engineering/custody/qualification/write state, blocker, exact next action;
5. concise Q1-Q5 prompts.

Detailed evidence and exam rubrics remain outside the 300-word snapshot.

At every substantive stop, PR creation/update boundary, blocker, owner-decision boundary, merge boundary, or explicit handover, the agent's user-facing response must reproduce the active snapshot or an equivalent concise rendering **including Q1-Q5**. It is not sufficient to say `EP-xxxx contains Q1-Q5`.

Read `references/repository-agent-policy.md` and `references/handover-snapshot.md`.

## 7. Always-ready crash discipline — write ahead

Before a material engineering batch, the accepted endpoint must already contain the exact intended next action and Q1-Q5 capable of qualifying a replacement for that boundary.

Required order:

```text
PROTOCOL ADOPTION GATE
-> PRE-WORK V3 ENDPOINT
-> Q1-Q5 QUALITY VALIDATION
-> MATERIAL WORK
-> VALIDATION TRUTH
-> SUCCESSOR ENDPOINT BEFORE NEXT MATERIAL BATCH
```

Do not code first and manufacture the qualification pack afterward.

After a coherent material batch, create the next endpoint **before starting another material batch**.

Therefore a crash leaves:

```text
last accepted endpoint
+ pinned qualification basis
+ pre-authored Q1-Q5
+ exact next action / expected safe patch boundary
```

available to the replacement.

If the pre-work endpoint/Q pack is absent or invalid, AUTO MODE pauses before mutation.

## 8. Question-set admission — pre-qualification integrity gate

Before a replacement answers Q1-Q5, classify the exam:

```text
QUESTION_SET_ADMISSION_STATUS:
VALID
STALE
MALFORMED
AUTHORITY_CONTAMINATED
INSUFFICIENT_TECHNICAL_DEPTH
```

Only `VALID` proceeds to qualification.

Admission verifies exactly Q1-Q5, retrievable basis, expert technical depth, concrete repository anchors, and valid roadmap/source/benchmark/oracle/methodology/release-authority assumptions. A technically current exam can still be `AUTHORITY_CONTAMINATED`.

The candidate may supply evidence but cannot be the sole authority that admits its own exam. Legacy v1/v2 endpoints require explicit admission under the current standard before their Q1-Q5 are used.

If admission fails, remain READ_ONLY. An independent question authority/Owner repairs or adopts a valid set; the candidate does not self-author and self-qualify.

Read `references/question-set-admission.md`.

## 9. Qualification-first takeover

For a replacement engineering-critical agent:

```text
TAKEOVER_AUTHORITY: READ_ONLY
```

Allowed before qualification:

```text
locate repo / chain / ACTIVE.md / latest accepted endpoint
locate PR and qualification basis
perform question-set admission
read pinned code/tests/data/roadmaps/sources needed to answer
perform calculations needed for Q1-Q5
```

Not allowed before PASS:

- advance `ACTIVE.md` or custody epoch;
- create an accepted recovery endpoint;
- reconcile later commits as accepted work;
- modify production/tests/oracles/roadmaps;
- resume AUTO MODE;
- grant write authority.

Sequence:

```text
1. minimal locator/bootstrap
2. question-set admission = VALID
3. answer pinned Q1-Q5
4. independent verifier scores
5. FAIL/DEFERRED -> READ_ONLY
6. PASS -> PASS_QUALIFIED_READ_ONLY / QUALIFIED_PENDING_RECONCILIATION
7. reconcile live PR/main, crash-window commits, roadmaps/sources/oracles, overlaps
8. classify POST_BASIS_DRIFT
9. retain qualification, independently confirm coverage, or requalify as required
10. only if all current-state authority clears -> HELD + WRITE_ALLOWED
11. execute EXACT_NEXT_ACTION
```

## 10. Q1-Q5 expert qualification standard

Exactly five questions:

```text
Q1 Production Trace
   actual object/case/value; exact files/functions/IDs/hashes; end-to-end reconstruction

Q2 Current Unresolved Problem / Failure Isolation
   real hand/numerical or equivalent technical reconstruction; predicted intermediates; first wrong boundary

Q3 Authority / Invariant
   source/ownership boundary plus exact falsifier and invalid shortcut

Q4 Independent Validation
   independent hand calculation/published oracle/cross-solver/byte reconstruction with units/signs/tolerance

Q5 Next Contribution / Minimal Patch
   safe implementation boundary exam; exact files/functions, before/after values, tests, rollback and NO-PATCH condition
```

Q5 is not an instruction to patch.

Minimum set quality where the domain permits:

```text
>=2 numerical/hand or equivalent exact technical reconstructions
>=3 questions requiring exact live-repository evidence
>=1 end-to-end production reconstruction
>=1 independent engineering oracle
>=1 explicit falsifier
>=1 exact safe-patch design with NO-PATCH condition
```

Non-numerical domains may substitute byte offsets, pointer/cardinality arithmetic, parser transitions, topology ownership, deterministic hashes, or equivalent exact reconstruction.

Generic questions such as `Explain the solver`, `Describe the benchmark`, `Which file would you inspect?`, `List the claims`, or source-reading comprehension without available implementation reconstruction are invalid.

For FEA/WRC/load-calculation/fixed-format work, prefer real calculation/reconstruction: actual element/node/load case, Jacobian/determinant, stiffness/end-force, equilibrium/free body, `r x F` and moment transfer, local/global axes, pointer/cardinality/byte arithmetic, or another domain-equivalent falsifiable computation.

Read `references/qualification.md` and `references/repository-agent-policy.md`.

## 11. Qualification roles and scoring

Artifacts remain separate under `agents/qualifications/<CHAIN_ID>/`.

Rules:

```text
candidate != verifier
candidate cannot self-award WRITE_ALLOWED
candidate cannot self-admit its own questionable set
question set is pre-authored by prior endpoint author/question authority
verdict basis == pinned qualification basis
total >= 92/100
every question >= 17/20
```

Version-3 verdicts:

```text
PASS_QUALIFIED_READ_ONLY
FAIL_READ_ONLY
DEFERRED_READ_ONLY
INVALID_SELF_VERIFIED
```

PASS proves competence only.

## 12. Post-PASS reconciliation and drift classification

After PASS, reconcile every post-basis commit/path and current authority while still READ_ONLY.

Classify:

```text
POST_BASIS_DRIFT:
NONE
METADATA_ONLY
MATERIAL_WITHIN_QUALIFIED_BOUNDARY
MATERIAL_BOUNDARY_CHANGED
AUTHORITY_CHANGED
CONTAMINATED
```

Consequences:

```text
NONE | METADATA_ONLY
-> QUALIFICATION_COVERAGE: RETAINED

MATERIAL_WITHIN_QUALIFIED_BOUNDARY
-> QUALIFICATION_COVERAGE: INDEPENDENTLY_CONFIRMED required

MATERIAL_BOUNDARY_CHANGED | AUTHORITY_CHANGED | CONTAMINATED
-> QUALIFICATION_COVERAGE: REQUALIFICATION_REQUIRED
-> WRITE_AUTHORITY: READ_ONLY
-> fresh independently authored Q1-Q5 against recovered basis
-> qualify again
```

A candidate cannot self-classify material drift as covered and self-enable writes.

Read `references/post-basis-drift.md`.

## 13. Roadmaps, validation, concurrency, AUTO, merge

All prior controls remain binding. In particular:

- applicable owner roadmap(s) are read/pinned before material coding;
- roadmap mutation needs explicit Owner authorization;
- source/benchmark/oracle authority is independent;
- validation distinguishes PASS/FAIL/NOT_RUN/NOT_APPLICABLE;
- cross-chain overlap is checked before mutation;
- AUTO MODE cannot enter a material leg until protocol adoption, pre-work endpoint and Q-pack validation are complete;
- AUTO MODE pauses on agent loss and cannot resume merely because qualification passed;
- merge remains Owner-controlled unless separately authorized.

## 14. Executable controls

Canonical structural checks:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_chain_store.py .
python skills/engineering-pr-delivery-v2/scripts/validate_roadmap_bindings.py .
python skills/engineering-pr-delivery-v2/scripts/validate_handover_snapshot.py .
python skills/engineering-pr-delivery-v2/scripts/validate_qualification_questions.py .
```

Takeover gates:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_question_set_admission.py <endpoint.md> <admission.md> [candidate-answer.md]
python skills/engineering-pr-delivery-v2/scripts/validate_qualification.py <answer.md> <verdict.md>
python skills/engineering-pr-delivery-v2/scripts/validate_post_basis_drift.py <reconciliation.md>
```

Repository adoption/legacy-write controls are defined in `references/repository-agent-policy.md`; when their executable validators are available in the current skill revision, they are mandatory before a new material leg.

Aggregate:

```text
python skills/engineering-pr-delivery-v2/scripts/check_relay.py . [options]
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Legacy v1/v2 history remains readable and is not mass-rewritten. Structural validation never replaces expert engineering verification.
