---
name: engineering-pr-delivery
description: Execute, investigate, review, recover, validate, or hand over GitHub pull-request work under a strict engineering delivery protocol. Use for repository issues/PRs, implementation work, agent takeovers, lost or incapable agents, stale or contaminated PRs, multi-agent work in one repository, engineering/FEA/numerical changes, validation, handover, salvage, supersession, and closure. Establish live repository truth first, keep every PR continuously handover-ready, require repository-specific takeover qualification before engineering-critical production changes, and never merge unless explicitly authorized.
---

# Engineering PR Delivery

## Governing objective

Preserve a recoverable chain of engineering work, not conversation memory.

At every durable checkpoint, another qualified agent must be able to recover the mission, current truth, evidence, risks, authority boundaries, partial work, and exact next action from the repository and PR artifacts alone.

Treat agent failure, loss of context, takeover, and PR supersession as normal controlled states.

## 1. Classify before acting

Classify independently:

```text
WORK_INTENT
  IMPLEMENT | INVESTIGATE | REVIEW | AUDIT | HANDOVER

REPOSITORY_STATE
  NO_PR | NEW_PR_REQUIRED | EXISTING_PR

MUTATION_AUTHORITY
  READ_ONLY | WRITE_ALLOWED

CRITICALITY
  STANDARD | ENGINEERING_CRITICAL | SAFETY_CRITICAL
```

Do not infer write authority from the existence of a branch or PR.

For takeover of an existing engineering-critical PR, start `READ_ONLY` until re-grounding and Appendix A qualification are complete.

## 2. Read repository-local instructions first

Inspect applicable repository instructions before changing code.

If the repository uses the protocol structure, read:

- `agents/MASTER_INDEX.md`;
- own `agents/PR<NUMBER>_workreport.md` or unique WIP report;
- own status/claim records;
- repo-local agent policy.

Then fetch live Git/GitHub state. Markdown does not override live mutable repository state.

Read `references/repository-ground-truth.md`.

## 3. Continuous handover invariant

Assume the active agent may disappear or become incapable immediately after any meaningful action.

No essential engineering state may exist only in chat history or private reasoning.

Before and after each meaningful implementation/investigation unit, keep the work report current and create a durable checkpoint soon enough that another agent can continue.

Use unique `WIP-<id>` records before PR allocation; never use one shared `PR_PENDING_workreport.md` in a multi-agent repository.

Read `references/continuous-handover.md` and use `references/workreport-template.md`.

## 4. Establish repository ground truth

Recover at least:

```text
repository
default/base branch
live main/base SHA
working branch
PR number/state/draft state
PR head SHA
merge base
changed files
commits
checks/workflows
open review threads/requested changes
linked source task
relevant predecessor/follow-on PRs
active status/claims
base drift
```

Classify discrepancies between prior reports and live state. Do not silently overwrite history.

Create a grounding epoch for takeover or material reconciliation.

## 5. Check repository-wide coordination

Before implementation and before each new stage:

1. inspect the master index;
2. fetch live open PRs;
3. inspect active status/claim records;
4. compare intended exact files and path prefixes;
5. compare engineering/software authority domains;
6. compare dependencies/workstreams;
7. classify `SAFE`, `COORDINATION_REQUIRED`, `BLOCKED_BY_ACTIVE_CLAIM`, or `UNKNOWN`.

A lack of exact-file overlap does not prove authority independence.

Read `references/multi-agent-coordination.md`.

## 6. Recover or initialize the work report

The current-state section is recovery authority; history is not.

Maintain:

- recovery header;
- Handover in 60 Seconds;
- live ground truth;
- mission/scope/acceptance;
- current implementation/partial state;
- active `ISS-*`, `IMP-*`, `RISK-*`, `DEC-*`, `QST-*`, `DEBT-*`;
- current technical diagnosis and falsifier;
- authority/invariants;
- validation ledger;
- changed-file ledger;
- review/CI state;
- overlap/dependency state;
- exact continuation state;
- takeover/grounding chain;
- Appendix A.

Do not use an impossible self-referential `REPORT_HEAD == containing commit SHA` rule. Use `REPORT_BASIS_HEAD` as described in `references/continuous-handover.md`.

## 7. Use the execution state machine

```text
BOOTSTRAP
  -> COORDINATION CHECK
  -> BASELINE
  -> PLAN
  -> IMPLEMENT / INVESTIGATE
  -> VALIDATE
  -> RECONCILE
  -> HANDOVER
  -> CLOSURE
```

For takeover:

```text
READ-ONLY
  -> LIVE RE-GROUND
  -> REPORT/LIVE RECONCILIATION
  -> DIFF/EVIDENCE INSPECTION
  -> APPENDIX A
  -> CONTINUE | QUARANTINE | SALVAGE | SUPERSEDE
```

Never jump from stale handover material directly to production modification.

## 8. Require implementation takeover qualification

Appendix A is an implementation authorization gate, not a knowledge quiz.

Normally create five repository-specific 20-mark challenges:

```text
A1 Production Trace
A2 Current Failure Isolation
A3 Authority / Invariant
A4 Independent Validation
A5 Next-Commit / Minimal Patch
```

Reject generic questions answerable without opening the current repository.

Require concrete repository anchors, evidence, a prediction, a falsifier, and next-commit implications.

Do not provide model answers that reveal the diagnosis.

For engineering-critical takeover, default threshold:

```text
total >= 92/100
every question >= 17/20
```

Unsafe/fabricated/anti-validation claims can fail immediately regardless of score.

Read `references/takeover-qualification.md`.

## 9. Detect engineering-critical work

Set `ENGINEERING_CRITICAL` when the change can affect, among other things:

- FEA/stress/loads/reactions;
- formulas/correlations;
- geometry/topology/meshing;
- units, coordinate systems, signs, end conventions;
- material/property authority;
- code/standard assessment;
- engineering master data;
- numerical recovery/transformation/publication;
- engineering exports used for design decisions.

Then read `references/engineering-validation.md` in addition to common validation.

## 10. Protect authority boundaries

Trace semantic impact:

```text
authority
-> canonical data
-> transformation
-> solver/calculation
-> recovery
-> publication
-> report/UI/export
```

Identify the first wrong boundary before changing upstream mechanics.

Record negative assurance: what intentionally changed and what must remain invariant.

Read `references/authority-boundaries.md`.

## 11. Implement action-first

Prefer:

```text
core production behavior
-> real production integration
-> visible/downloadable/measurable result
-> focused regression
-> independent engineering evidence where required
```

Do not substitute schemas, validators, certification prose, placeholder adapters, or unused abstractions for usable production behavior.

Keep scope surgical. Read `references/coding-policy.md`.

## 12. Validate with explicit evidence dimensions

For every material check record:

```text
STATUS
  PASS | FAIL | NOT_RUN | NOT_APPLICABLE

OBSERVATION
  LOCAL_EXECUTION | REMOTE_EXECUTION | SOURCE_INSPECTION
  ARTIFACT_INSPECTION | USER_SUPPLIED | INFERRED | NOT_OBSERVED

ORACLE
  NONE | IMPLEMENTATION_COUPLED | INDEPENDENT_REPRODUCTION
  ANALYTICAL | AUTHORITATIVE_REFERENCE | CROSS_SOLVER | EXPERIMENTAL
```

Also record tested HEAD, command/evidence, expected/actual, tolerance where applicable, limitations, and failure origin:

```text
PREEXISTING | INTRODUCED_BY_PR | RESOLVED_BY_PR | UNKNOWN_ORIGIN
```

Read `references/validation-common.md`.

## 13. Enforce integrity rules

Never:

- weaken a tolerance merely because a test fails;
- replace independent expected values with production output;
- delete a difficult benchmark to obtain green status;
- claim pre-step/CI/tool failure as product PASS;
- replace an independent oracle with the implementation;
- hard-code fixture IDs into production;
- silence fail-closed behavior to obtain green tests;
- claim an unexecuted check as PASS;
- treat docs/schema/validator-only work as production completion;
- change several numerical mechanisms at once when isolation is possible.

Read `references/anti-gaming-rules.md`.

## 14. Recover damaged PRs without sunk-cost bias

If the report cannot explain the diff, authority is unclear, expected values and production changed together, commits cannot be classified, main drift is material, or takeover requires guessing intent, quarantine first.

Perform a salvage assessment.

Valid outcomes:

```text
CONTINUE
SALVAGE_PARTIAL
SUPERSEDE
ABANDON
```

Preserve known-good commits, benchmarks, independent evidence, accepted decisions/invariants, and provenance. Rebuild untrusted implementation from current main when safer.

Agent replacement alone is not a reason for a new PR.

Read `references/recovery-salvage.md`.

## 15. Reconcile before handover or closure

Reconcile actual GitHub changed files against the ledger.

Explain every changed path. Unexplained files block closure.

Refresh review/check status and multi-agent overlap state.

A PR remains handover-ready even while waiting for review/merge.

Appendix A may become `NOT_REQUIRED` only when no further technical implementation authority is needed.

Read `references/closure-gate.md`.

## 16. Git/PR rules

Use one PR per coherent assignment unless scope is explicitly changed.

Keep commits logical and recoverable.

Do not merge unless the owner explicitly authorizes merge.

Do not create or modify workflow files unless authorized.

Read `references/git-pr-policy.md`.
