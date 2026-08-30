---
name: engineering-pr-delivery-v2
description: Crash-safe, qualification-first engineering PR delivery with centralized cross-repository policy. Every bounded repository-work response starts with the Active handover snapshot and full expert Q1-Q5. New material legs use canonical v3 custody, exact work-item ownership, UUID-backed agent instances, Owner-question no-downgrade baselines, concrete engineering payloads, Git-provable prework and append-only material receipts. A replacement qualifies while READ_ONLY before reconciliation or write authority.
---

# Engineering PR Delivery v2 — qualification-first, crash-ready, every-turn handover

## 1. Governing objective

The repository must remain handover-ready after any agent crash. A replacement must not need the outgoing chat.

Reusable policy lives in this Common skill. Downstream `AGENTS.md` files are project overlays only.

Takeover sequence:

```text
agent loss / custodian change
→ minimal READ_ONLY locator bootstrap
→ question-set admission
→ TAKEOVER QUALIFICATION FIRST
→ independent PASS_QUALIFIED_READ_ONLY
→ post-basis reconciliation while READ_ONLY
→ drift/authority classification
→ requalify if boundary/authority changed
→ WRITE_ALLOWED only when current-state authority is safe
→ execute EXACT_NEXT_ACTION
```

Question-set admission validates the exam only. Qualification PASS proves competence only; it does not grant write, roadmap or merge authority.

## 2. Required references and precedence

Read at minimum:

```text
references/repository-agent-policy.md
references/reality-check-p0.md
references/project-agents-template.md
references/handover-snapshot.md
references/qualification.md
references/qualification-profiles.md
references/owner-qualification-baseline.md
references/question-set-admission.md
references/post-basis-drift.md
references/authority-state-model.md
references/crash-recovery.md
references/owner-roadmaps.md
references/chain-concurrency.md
references/material-leg-history.md
references/prework-history.md
references/code-quality.md
```

`references/protocol-foundation-v2.2.md` preserves the prior protocol and remains binding where not superseded.

For new material legs, `reality-check-p0.md` supersedes conflicting older wording about handover frequency, question compression, work-item identity and readiness evidence.

## 3. Core invariants

```text
R1  Repository state, not conversation memory, is the baton.
R2  Generic policy lives in Common; downstream AGENTS.md is project-only.
R3  Every new material leg re-grounds live Common and records its basis.
R4  STALE_PROTOCOL or UNKNOWN blocks material coding and AUTO.
R5  New material work uses agents/chains/**; legacy relay is read-only history.
R6  Pre-work endpoint + expert Q1-Q5 exist before the material batch.
R7  Q1-Q5 are qualification, never the implementation task list.
R8  EXACT_NEXT_ACTION is the work baton for a qualified custodian.
R9  Owner-authored qualification/challenges are a no-downgrade floor.
R10 Numerical engineering packs carry concrete payload, not topic labels.
R11 Exact WORK_ITEM_KEY collision is checked before semantic overlap.
R12 A model family/name is not a unique AGENT_INSTANCE_ID.
R13 A replacement qualifies before substantive crash-window recovery.
R14 Qualification PASS is necessary but not sufficient for WRITE_ALLOWED.
R15 Post-basis drift is classified before write authority can be granted.
R16 Material/authority drift or contamination forces requalification.
R17 Candidate cannot self-verify, self-admit or self-confirm coverage.
R18 Owner roadmap mutation remains separately Owner-authorized.
R19 NOT_RUN, blockers, assumptions and authority boundaries survive relay.
R20 Merge authority is independent and Owner-controlled unless explicitly granted.
R21 Every completed material batch gets an append-only history receipt.
R22 HANDOVER_READY is evidence-derived, never a self-declared synonym for content existing.
R23 Every bounded repository-work response starts with Active handover snapshot.
R24 Full Q1-Q5 are outside the State Card word limit and visible every time.
R25 After the snapshot/questions, ordinary reporting is delta-only unless Owner asks for detail.
```

## 4. Chain state and authority planes

Canonical chain version remains:

```text
CHAIN_STATE_VERSION: 3
```

Authority planes:

```text
ENGINEERING_STATE: READY | IN_PROGRESS | BLOCKED | COMPLETE
CUSTODY_STATE: HELD | VACANT | TAKEOVER_REQUIRED | QUALIFIED_PENDING_RECONCILIATION | RECONCILING
QUALIFICATION_STATE: NOT_REQUIRED | PENDING | PASS | FAIL | DEFERRED | REQUALIFICATION_REQUIRED
WRITE_AUTHORITY: READ_ONLY | WRITE_ALLOWED | BLOCKED
AUTO_STATE: RUNNING | PAUSED | BLOCKED | NOT_APPLICABLE
MERGE_AUTHORITY: OWNER_ONLY | AUTHORIZED
```

New material/successor state also records:

```text
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <live Common SHA actually read>
COMMON_PROTOCOL_STATUS: CURRENT
WORK_ITEM_KEY: <stable identity>
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

For `PARTITIONED`, require distinct partition identity plus `WORK_ITEM_PARTITION_AUTHORITY: OWNER:<locator>`.

## 5. Protocol-adoption gate before every material batch

```text
1. read project overlay
2. re-ground live Common skill/references
3. record COMMON_PROTOCOL_BASIS / CURRENT
4. confirm canonical v3 chain path
5. reserve exact WORK_ITEM_KEY
6. confirm UUID-backed AGENT_INSTANCE_ID
7. discover Owner qualification baseline
8. create work-ahead endpoint
9. author full profile-v2 Q1-Q5
10. validate handover/baseline/payload/work-item gates
11. only then mutate material engineering/policy/source/benchmark/publication files
```

Fail closed on stale protocol, duplicate exclusive work item, invalid agent instance, invalid handover, missing Owner baseline coverage or insufficient technical depth.

## 6. Exact work-item concurrency

For `WORK_ITEM_MODE: EXCLUSIVE`, at most one non-terminal chain may hold a work-item key such as:

```text
WORK_ITEM_KEY: github:reallaksh19/Advanced_Analysis#1535
```

A second agent does not create another writer chain; it joins/takes over the existing chain under qualification-first rules or stops.

Partitioning requires explicit Owner-authorized non-overlapping partitions. After exact work-item admission, still run path/authority/benchmark/release overlap detection.

Read `chain-concurrency.md`.

## 7. Every-turn Active handover response contract

For **any** response that performed, attempted, audited, blocked, resumed, advanced, completed or re-grounded repository work, the first user-visible section is:

```text
# Active handover snapshot
```

No prose precedes it. This includes `proceed next`, AUTO batches, read-only audits, NOT_RUN/blockers, PR create/update, status/review gates, merge gates and task completion.

New durable endpoints use:

```text
### Active handover snapshot
<State Card; target <220 words>

### Active qualification questions
Q1: <full prompt>
Q2: <full prompt>
Q3: <full prompt>
Q4: <full prompt>
Q5: <full prompt>
```

The State Card includes repo/task/chain/endpoint, PR/branch/head/main/status, merge authority, engineering/custody/qualification/write/AUTO state, protocol, roadmap, inputs/benchmarks/source pointers, blocker, leg diagnosis and exact next action.

The word limit applies only to the State Card. Never delete numerical inputs, derivations, oracle requirements or falsifiers from Q1-Q5 to fit it.

After the questions, ordinary turn reporting is:

```text
## Changed this turn
```

with at most eight concise bullets unless Owner explicitly asks for a detailed report.

It is invalid to say only `EP-xxxx contains Q1-Q5`.

## 8. Evidence-derived handover readiness

New successor endpoints use:

```text
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <durable evidence or NONE>
HANDOVER_READY: TRUE | FALSE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
```

`HANDOVER_READY: TRUE` requires content ready + validation PASS + non-empty evidence. If validation is NOT_RUN/FAIL, preserve the baton but keep HANDOVER_READY FALSE.

Historical endpoints are not rewritten. The next material leg adopts protocol version 2.

## 9. Owner qualification baseline — no downgrade

Before writing a new Q pack, inspect current Owner instructions, issue body/appendix, Owner roadmaps and accepted handovers for Owner-authored qualification questions or explicit challenges.

Record:

```text
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE | <owner locator>
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE | <repo-relative JSON>
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

If Owner questions exist, the active pack may reorganize/strengthen them but may not remove supplied coordinates/loads/dimensions/materials/integration points, requested hand derivations, mechanisms, independent oracles, negative controls, falsifiers or safe-patch reasoning.

The manifest maps each Owner question to active Q1-Q5 and preserves required literals/concepts/obligations. Incomplete coverage is `INSUFFICIENT_TECHNICAL_DEPTH` and blocks the next material batch.

Read `owner-qualification-baseline.md`.

## 10. Q1-Q5 expert standard and concrete payload

Exactly five questions:

```text
Q1 Production Trace
Q2 Current Unresolved Problem / Failure Isolation
Q3 Authority / Invariant
Q4 Independent Validation
Q5 Next Contribution / Minimal Patch
```

Q5 tests competence; it is not an instruction to implement.

New packs declare:

```text
QUALIFICATION_PROFILE_VERSION: 2
```

Each detailed question includes:

```text
Domain challenge:
Exact repository data required:
Concrete payload:
Required derivation:
```

Q2/Q4 retain `Calculation/reconstruction:`.

For FEA/WRC/Load Calc/fixed-format profiles, at least two questions contain real hand-computable values/coordinates/loads/dimensions/record offsets or equivalent exact payload. Q2/Q4 normally contain at least three concrete numeric literals plus an explicit derivation.

Minimum set quality:

```text
>=2 numerical/hand or equivalent exact reconstructions
>=3 questions requiring exact live-repository evidence
>=1 end-to-end production reconstruction
>=1 independent engineering oracle
>=1 explicit falsifier
>=1 exact safe-patch + NO-PATCH boundary
```

Topic labels such as `Reconstruct distorted-T6 Jacobians` are insufficient when the element coordinates/integration points are known.

Read `qualification.md` and `qualification-profiles.md`.

## 11. Write-ahead crash discipline and material history

Required order:

```text
PROTOCOL + WORK-ITEM ADOPTION
→ PRE-WORK ENDPOINT
→ Q1-Q5 / BASELINE / HANDOVER VALIDATION
→ MATERIAL BATCH
→ EXECUTION TRUTH
→ MATERIAL-LEG RECEIPT
→ SUCCESSOR ENDPOINT BEFORE ANOTHER MATERIAL BATCH
```

`validate_prework_history.py` proves the work-ahead endpoint preceded material mutation. `validate_material_leg_history.py` preserves that proof for every completed AUTO/material batch and rejects hidden inter-leg/trailing material.

## 12. Question-set admission and takeover

Admission statuses:

```text
VALID
STALE
MALFORMED
AUTHORITY_CONTAMINATED
INSUFFICIENT_TECHNICAL_DEPTH
```

Only VALID proceeds to qualification. Admission checks the exam, current baseline coverage, authority assumptions and technical depth. Candidate may supply evidence but cannot be sole authority admitting its own questionable set.

After independent PASS:

```text
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
QUALIFICATION_STATE: PASS
WRITE_AUTHORITY: READ_ONLY
```

Then reconcile current PR/main/crash-window/roadmap/source/oracle/overlap state.

## 13. Post-basis drift

```text
POST_BASIS_DRIFT:
NONE
METADATA_ONLY
MATERIAL_WITHIN_QUALIFIED_BOUNDARY
MATERIAL_BOUNDARY_CHANGED
AUTHORITY_CHANGED
CONTAMINATED
```

```text
NONE | METADATA_ONLY
→ qualification retained

MATERIAL_WITHIN_QUALIFIED_BOUNDARY
→ independent coverage confirmation required

MATERIAL_BOUNDARY_CHANGED | AUTHORITY_CHANGED | CONTAMINATED
→ REQUALIFICATION_REQUIRED
→ WRITE_AUTHORITY: READ_ONLY
→ fresh independently authored Q1-Q5 against recovered basis
```

## 14. Roadmaps, validation, AUTO and merge

Applicable Owner roadmaps are read/pinned before material coding. Roadmap mutation requires explicit Owner authorization. Source/benchmark/oracle authority remains independent.

Validation always distinguishes PASS/FAIL/NOT_RUN/NOT_APPLICABLE. Empty workflow jobs, transport failure, mergeability or source inspection cannot become engineering PASS.

AUTO cannot bypass protocol/work-item/prework/qualification/handover gates and cannot authorize roadmap/source/oracle changes or merge.

Merge remains Owner-controlled unless separately authorized.

## 15. Executable controls

Canonical relay:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_chain_store.py .
python skills/engineering-pr-delivery-v2/scripts/validate_roadmap_bindings.py .
python skills/engineering-pr-delivery-v2/scripts/validate_handover_snapshot.py .
python skills/engineering-pr-delivery-v2/scripts/validate_handover_readiness.py .
python skills/engineering-pr-delivery-v2/scripts/validate_qualification_questions.py .
python skills/engineering-pr-delivery-v2/scripts/validate_qualification_profile.py .
python skills/engineering-pr-delivery-v2/scripts/validate_engineering_question_payload.py .
python skills/engineering-pr-delivery-v2/scripts/validate_owner_qualification_baseline.py .
python skills/engineering-pr-delivery-v2/scripts/validate_work_item_exclusivity.py .
python skills/engineering-pr-delivery-v2/scripts/validate_material_leg_history.py .
```

New material leg:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_leg_adoption.py <repo-root> <ACTIVE.md>
python skills/engineering-pr-delivery-v2/scripts/validate_prework_history.py <repo-root> <base-ref> <head-ref> <ACTIVE.md>
python skills/engineering-pr-delivery-v2/scripts/validate_legacy_relay_diff.py <repo-root> <base-ref> <head-ref>
```

Takeover:

```text
python skills/engineering-pr-delivery-v2/scripts/validate_question_set_admission.py <endpoint> <admission> [answer]
python skills/engineering-pr-delivery-v2/scripts/validate_qualification.py <answer> <verdict>
python skills/engineering-pr-delivery-v2/scripts/validate_post_basis_drift.py <reconciliation>
```

Aggregate:

```text
python skills/engineering-pr-delivery-v2/scripts/check_relay.py . [options]
python skills/engineering-pr-delivery-v2/scripts/self_test.py
```

Historical v1/v2/pre-P0 endpoints remain readable immutable evidence. Structural validation never replaces expert engineering verification.
