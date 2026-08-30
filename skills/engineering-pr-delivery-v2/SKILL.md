---
name: engineering-pr-delivery-v2
description: Crash-safe, qualification-first engineering PR delivery with centralized cross-repository policy. Issue-based work uses an immutable Issue Basis, cumulative repository issue state, one mutable GitHub Issue Active Handover comment and immutable endpoint comments; non-issue work remains repository-only. Owner progression uses exactly three commands: proceed next, proceed next no Qs, and proceed next hand over ready. Questions are qualification-scope-bound rather than generated every endpoint. Exact work-item custody, Owner-roadmap/source/oracle authority, no-downgrade qualification, validation truth and Owner-only merge remain protected.
---

# Engineering PR Delivery v2 — qualification-first, crash-ready, durable multi-agent delivery

## 1. Governing objective

The repository must remain recoverable after any agent crash or replacement. A replacement must not need the outgoing chat.

Reusable policy lives in this Common skill. Downstream `AGENTS.md` files are project overlays only.

For GitHub-Issue work, the Issue is the human-visible control plane while repository artifacts remain the machine-verifiable custody authority.

Takeover remains qualification-first:

```text
agent loss / custodian change
→ minimal READ_ONLY locator bootstrap
→ locate current repository/Issue baton
→ require takeover qualification readiness
→ question-set admission
→ TAKEOVER QUALIFICATION FIRST
→ independent PASS_QUALIFIED_READ_ONLY
→ post-basis reconciliation while READ_ONLY
→ drift/authority classification
→ requalify if boundary/authority changed
→ WRITE_ALLOWED only when current-state authority is safe
→ execute EXACT_NEXT_ACTION
```

Qualification PASS proves competence only. It does not grant roadmap, source/oracle, write or merge authority.

## 2. Required references and precedence

Read at minimum:

```text
references/repository-agent-policy.md
references/github-issue-control-plane.md
references/owner-progression-commands.md
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

`protocol-foundation-v2.2.md` preserves prior policy where not superseded.

Specific newer references win over older generic wording. In particular:

- `github-issue-control-plane.md` governs Issue-based durable projection/cumulative custody;
- `owner-progression-commands.md` governs question generation/display for the three Owner progression commands;
- `reality-check-p0.md` continues to govern no-downgrade question quality, exact work-item identity and evidence-derived readiness.

## 3. Core invariants

```text
R1  Repository state, not conversation memory, is the baton.
R2  Generic policy lives in Common; downstream AGENTS.md is project-only.
R3  Explicit current Owner instruction is highest current authority.
R4  Applicable Owner Roadmap(s) remain above Issue execution plans and agent proposals.
R5  Every new material boundary re-grounds live Common and records its basis.
R6  STALE_PROTOCOL or UNKNOWN blocks material coding and AUTO.
R7  New material work uses agents/chains/**; legacy relay is read-only history.
R8  Exact WORK_ITEM_KEY collision is checked before semantic overlap.
R9  A model family/name is not a unique AGENT_INSTANCE_ID.
R10 Issue-based work preserves immutable Issue Basis + cumulative current issue state.
R11 Original task, inputs, benchmarks/oracles and roadmaps cannot silently disappear across agents.
R12 Issue comments are synchronized projections/navigation; they do not replace repository/source/roadmap authority.
R13 Normal Owner progression recognizes exactly three commands.
R14 Questions are bound to qualification scope, not generated merely because an endpoint/commit exists.
R15 `proceed next, no Qs` may defer takeover qualification readiness without losing chain custody.
R16 `proceed next, hand over ready` must leave a complete takeover checkpoint or report an exact blocker.
R17 Owner-authored technical questions/challenges are a no-downgrade floor when questions are refreshed.
R18 Numerical engineering packs carry concrete payload, not topic labels.
R19 A replacement qualifies before substantive crash-window recovery.
R20 Qualification PASS is necessary but not sufficient for WRITE_ALLOWED.
R21 Post-basis drift is classified before write authority can be granted.
R22 Material/authority drift or contamination forces requalification.
R23 Candidate cannot self-verify, self-admit or self-confirm coverage.
R24 NOT_RUN, blockers, assumptions and authority boundaries survive relay.
R25 Mergeability and merge authority are separate and always reported separately.
R26 Merge remains Owner-controlled unless explicitly granted.
R27 Every completed material batch gets an append-only history receipt.
R28 Chain handover readiness and takeover qualification readiness are separate planes.
R29 Every bounded repository-work response starts with the Active handover snapshot.
R30 Ordinary reporting after the required envelope is delta-only unless Owner requests detail.
```

## 4. Work-item source

Every active new material state declares:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE | REPOSITORY_TASK | OWNER_DIRECT
```

### GitHub Issue

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE
WORK_ITEM_KEY: github:<owner>/<repo>#<issue>
```

Use the Issue control-plane architecture in section 7.

### No GitHub Issue

For `REPOSITORY_TASK` and `OWNER_DIRECT`, current repository chain/endpoint/material-receipt/qualification custody remains sufficient. Do not create fake issue artifacts.

## 5. Chain state and authority planes

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
MERGE_AUTHORIZED: TRUE | FALSE
MERGEABILITY: MERGEABLE | CONFLICTING | UNKNOWN
```

Core identity:

```text
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <live Common SHA actually read>
COMMON_PROTOCOL_STATUS: CURRENT | STALE_PROTOCOL | UNKNOWN
WORK_ITEM_SOURCE:
WORK_ITEM_KEY:
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

## 6. Protocol-adoption gate

Before material progression:

```text
1. read project overlay
2. re-ground live Common skill/references
3. record COMMON_PROTOCOL_BASIS/status
4. resolve WORK_ITEM_SOURCE and exact WORK_ITEM_KEY
5. check exclusive/partitioned custody
6. confirm UUID-backed AGENT_INSTANCE_ID
7. read applicable Owner Roadmap(s) and source/oracle authority
8. for Issue work, resolve Issue Basis + current cumulative state + sync state
9. reconcile current PR/main/reviews/checks/mergeability
10. apply one of the three Owner progression commands
11. preserve validation truth
12. mutate only inside current authority
```

Question refresh is no longer an unconditional precondition for every same-agent material batch. It follows section 8.

## 7. GitHub-Issue durable architecture

For `WORK_ITEM_SOURCE: GITHUB_ISSUE`, repository custody includes:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/issue-basis/<IB-ID>.md          # immutable Owner task basis
agents/chains/<CHAIN_ID>/issue-state/CURRENT.md          # mutable cumulative materialized state
agents/chains/<CHAIN_ID>/endpoints/<EP-ID>.md            # immutable checkpoint history
agents/chains/<CHAIN_ID>/material-legs/**                 # material receipts
agents/qualifications/<CHAIN_ID>/**                       # qualification evidence
```

### Issue Basis

Capture item-level:

```text
original task / acceptance obligations
inputs
benchmarks / independent oracles
Owner and other applicable roadmaps
Owner qualification baseline
```

If Owner requirements change, create a successor Issue Basis; never rewrite the old basis.

### Issue Current State

`issue-state/CURRENT.md` materializes the current item-level state so Agent 5/10 does not need to replay every historical delta. Stable Issue-Basis row IDs cannot silently disappear.

### GitHub Issue comments

Maintain exactly three roles:

```text
CHAIN_ROOT  immutable once
ACTIVE      exactly one mutable current handover comment per non-terminal chain
ENDPOINT    immutable one per accepted endpoint
```

The Active comment projects repository `CURRENT.md` and current PR/roadmap/qualification state.

Repository↔Issue sync fields:

```text
ISSUE_BASIS_ID
ISSUE_BASIS_FILE
ISSUE_CURRENT_STATE_FILE
ISSUE_CHAIN_ROOT_COMMENT_ID
ISSUE_ACTIVE_HANDOVER_COMMENT_ID
ISSUE_LATEST_ENDPOINT_COMMENT_ID
ISSUE_HANDOVER_SYNC_STATUS: IN_SYNC | STALE | NOT_RUN | FAILED
```

Before another material progression:

```text
accepted endpoint
→ update CURRENT.md
→ publish immutable Issue endpoint comment
→ update mutable Issue Active comment
→ record comment IDs
→ ISSUE_HANDOVER_SYNC_STATUS = IN_SYNC
```

If synchronization fails, preserve repository custody but block the next material progression until reconciled.

Read `github-issue-control-plane.md`.

## 8. Exactly three Owner progression commands

Normal progression recognizes only:

```text
proceed next
proceed next, no Qs
proceed next, hand over ready
```

Internal state:

```text
OWNER_PROGRESSION_COMMAND:
QUALIFICATION_SCOPE_ID:
QUESTION_SET_ID:
QUESTION_SET_STATUS: CURRENT | STALE | NOT_APPLICABLE
QUESTION_PACK_ACTION: REUSED | REFRESHED | SUPPRESSED_BY_OWNER | NOT_APPLICABLE
QUESTION_DISPLAY: SHOW | HIDE
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
```

### `proceed next`

Continue one bounded progression.

```text
same qualification scope + current Q set
→ REUSED
→ HIDE unchanged Qs

scope materially changed or set stale
→ REFRESHED
→ SHOW full Q1-Q5
→ current takeover qualification readiness
```

### `proceed next, no Qs`

Continue one bounded progression and do not create, refresh or display questions.

```text
QUESTION_PACK_ACTION: SUPPRESSED_BY_OWNER
QUESTION_DISPLAY: HIDE
```

If existing coverage remains current, takeover qualification may remain ready. If it becomes stale:

```text
QUESTION_SET_STATUS: STALE
TAKEOVER_QUALIFICATION_READY: FALSE
```

The current custodian may complete that one Owner-authorized progression if all non-question authority gates remain clear. A replacement cannot take write custody until current questions are independently established and qualification passes.

### `proceed next, hand over ready`

Continue one bounded progression, then freeze a complete takeover checkpoint.

Ensure/refresh current Q1-Q5 as needed, show them in full, reconcile cumulative task/input/benchmark/roadmap/PR state, synchronize Issue comments when applicable, record endpoint/material receipts and stop.

Required target:

```text
QUESTION_SET_STATUS: CURRENT
QUESTION_DISPLAY: SHOW
CHAIN_HANDOVER_READY: TRUE
TAKEOVER_QUALIFICATION_READY: TRUE
```

For Issue work also target:

```text
ISSUE_HANDOVER_SYNC_STATUS: IN_SYNC
```

If a required component cannot be proven, report the blocker and keep readiness FALSE rather than faking success.

Read `owner-progression-commands.md`.

## 9. Qualification scope and question reuse

Questions bind to:

```text
QUALIFICATION_SCOPE_ID: QSCOPE-<work-item>-<technical-boundary>
QUESTION_SET_ID:
```

One pack may be reused across many endpoints/material batches while all materially remain within:

```text
same work item / Issue Basis
same Owner-roadmap intent
a covered engineering authority boundary
a covered source/oracle authority boundary
the same technical competency boundary
```

A new endpoint/commit alone is not a reason to regenerate questions.

Durable endpoints may retain the same full Q pack unchanged while the user-facing response hides unchanged questions.

## 10. Owner qualification baseline — no downgrade

Whenever questions are refreshed, inspect current Owner instructions, issue body/appendix, Owner Roadmaps and accepted handovers for Owner-authored qualification questions/challenges.

Record:

```text
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE:
OWNER_QUALIFICATION_BASELINE_MANIFEST:
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

A refreshed pack may reorganize/strengthen but may not remove supplied coordinates/loads/dimensions/materials/integration points, requested derivations, mechanisms, independent oracles, negative controls, falsifiers or safe-patch reasoning.

## 11. Q1-Q5 expert standard

Exactly five questions:

```text
Q1 Production Trace
Q2 Current Unresolved Problem / Failure Isolation
Q3 Authority / Invariant
Q4 Independent Validation
Q5 Next Contribution / Minimal Patch
```

New packs use `QUALIFICATION_PROFILE_VERSION: 2` and include concrete payload/required derivation fields. Engineering numerical profiles require real falsifiable calculations, not technical vocabulary.

Minimum set quality when applicable:

```text
>=2 numerical/hand or equivalent exact reconstructions
>=3 questions requiring exact live-repository evidence
>=1 end-to-end production reconstruction
>=1 independent engineering oracle
>=1 explicit falsifier
>=1 exact safe-patch + NO-PATCH boundary
```

Read `qualification.md`, `qualification-profiles.md`, `owner-qualification-baseline.md`.

## 12. Active handover response contract

Every bounded repository-work response begins:

```text
# Active handover snapshot
```

Always show:

```text
repo/task/chain/endpoint
PR/branch/head/main/status
mergeability/reviews/unresolved threads/required checks
merge authority + merge authorized
engineering/custody/qualification/write/AUTO
protocol/work item/Issue Basis
Owner + other roadmap state/drift/mutation authority
original task/input/benchmark status
qualification scope/set/action/readiness
blocker/leg diagnosis/exact next action
```

The State Card targets `<220 words`.

Full Q display follows section 8:

```text
proceed next
→ show Q1-Q5 only if refreshed

proceed next, no Qs
→ never show Q1-Q5

proceed next, hand over ready
→ show full current Q1-Q5
```

Then use `## Changed this turn` with at most eight concise delta bullets unless Owner asks for detail.

Read `handover-snapshot.md`.

## 13. Readiness planes

Use separately:

```text
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE:
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
HANDOVER_READY: TRUE | FALSE
```

`CHAIN_HANDOVER_READY` = durable task/roadmap/input/benchmark/PR/endpoint custody exists.

`TAKEOVER_QUALIFICATION_READY` = a current valid Q-set is available for immediate admission/qualification.

For new states:

```text
HANDOVER_READY
= complete validated/synchronized chain handover
  AND takeover qualification ready
```

Therefore after `proceed next, no Qs` it is valid to have:

```text
CHAIN_HANDOVER_READY: TRUE
TAKEOVER_QUALIFICATION_READY: FALSE
HANDOVER_READY: FALSE
```

## 14. Write-ahead material history

Material history remains append-only:

```text
protocol/work-item/authority adoption
→ bounded progression
→ validation truth
→ material-leg receipt
→ accepted successor endpoint
→ Issue Current State/comment synchronization when applicable
→ only then another material progression
```

Existing Git-provable prework/material receipts remain valid history. The new question-scope model supersedes only the old requirement to author a fresh Q-pack before every same-scope material batch.

## 15. Question-set admission and takeover

Admission statuses remain:

```text
VALID
STALE
MALFORMED
AUTHORITY_CONTAMINATED
INSUFFICIENT_TECHNICAL_DEPTH
```

A replacement first requires:

```text
TAKEOVER_QUALIFICATION_READY: TRUE
```

If FALSE, it remains READ_ONLY while a current set is independently established.

After independent PASS:

```text
CUSTODY_STATE: QUALIFIED_PENDING_RECONCILIATION
QUALIFICATION_STATE: PASS
WRITE_AUTHORITY: READ_ONLY
```

Then reconcile current PR/main/crash-window/roadmap/source/oracle/overlap state.

## 16. Post-basis drift

```text
POST_BASIS_DRIFT:
NONE
METADATA_ONLY
MATERIAL_WITHIN_QUALIFIED_BOUNDARY
MATERIAL_BOUNDARY_CHANGED
AUTHORITY_CHANGED
CONTAMINATED
```

Material/authority boundary changes force requalification unless independent current policy explicitly retains coverage.

For Issue-based roadmaps also classify:

```text
NO_DRIFT
STATUS_ONLY_DRIFT
OWNER_INTENT_DRIFT
ROADMAP_REMOVED
NEW_APPLICABLE_ROADMAP
UNKNOWN
```

Owner-intent/new/unknown roadmap drift blocks write/AUTO pending re-ground/Owner decision.

## 17. Validation integrity, AUTO and merge

Validation always distinguishes PASS/FAIL/NOT_RUN/NOT_APPLICABLE. Empty workflow jobs, transport failure, mergeability or source inspection cannot become engineering PASS.

AUTO cannot bypass work-item, roadmap/source/oracle, validation, cumulative Issue sync or takeover rules. `proceed next, no Qs` applies only to the requested bounded progression, not indefinite uncovered AUTO.

Always distinguish:

```text
MERGEABILITY
MERGE_AUTHORITY
MERGE_AUTHORIZED
```

Merge remains Owner-controlled unless separately authorized.

## 18. Executable controls

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
python skills/engineering-pr-delivery-v2/scripts/validate_issue_control_plane.py .
python skills/engineering-pr-delivery-v2/scripts/validate_progression_command.py .
python skills/engineering-pr-delivery-v2/scripts/validate_material_leg_history.py .
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

Historical endpoints remain immutable evidence. Structural validation never replaces expert engineering verification.