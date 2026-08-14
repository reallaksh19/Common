# Universal Engineering Agent Policy

This file applies to **all contributors and agents** working in this repository: ChatGPT, Codex, Claude, Cursor, Copilot, Gemini, local agents, scripts acting as agents, and humans.

The repository—not a chat session—is the durable source of work state.

The canonical reusable delivery protocol is maintained in:

- `skills/engineering-pr-delivery/SKILL.md`
- `skills/engineering-pr-delivery/references/`
- `skills/engineering-pr-delivery/scripts/`

Repository-local rules may be stricter. Explicit current owner instructions override generic defaults, but no agent may silently weaken engineering evidence, validation integrity, or handover requirements.

## 1. Continuous handover invariant

Assume the active agent may disappear, lose context, become incapable, or be replaced after any meaningful action.

At every durable checkpoint, another qualified agent must be able to recover the work from repository + PR artifacts without chat history.

No essential mission state, engineering reasoning, current hypothesis, validation limitation, authority decision, risk, or exact next action may exist only in private reasoning or conversation history.

## 2. Establish live ground truth before mutation

Before changing production or engineering-sensitive files, determine from live Git/GitHub where available:

- repository and default/base branch;
- current base/main SHA;
- WIP/branch/PR identity;
- current PR head and merge base;
- actual changed files and commits;
- checks/workflows and review state;
- source issue/task;
- predecessor/follow-on PRs;
- other active work that may overlap.

Live mutable repository state overrides stale work reports and prior conversations.

## 3. Durable work identity

The durable work identity is the **WIP/PR**, not the agent session.

Before a PR exists, use a unique identity:

```text
WIP-<short-id>
agents/WIP-<short-id>_workreport.md
```

Do not use one shared `PR_PENDING_workreport.md` in a multi-agent repository.

After PR allocation, use:

```text
agents/PR<NUMBER>_workreport.md
```

If status/claim registries exist, keep the matching `agents/status/` and `agents/claims/` records current.

## 4. Work report must remain recovery-first

For implementation or engineering investigation, keep the work report synchronized around every meaningful state transition.

The current-state portion must identify at least:

- `HANDOVER_READINESS`;
- `PR_RECOVERY_STATE`;
- `TAKEOVER_AUTHORITY`;
- report basis/current live grounding;
- mission, scope, acceptance and non-goals;
- current implementation/partial work;
- active `ISS-*`, `IMP-*`, `RISK-*`, `DEC-*`, `QST-*`, `DEBT-*`;
- current technical diagnosis and falsifier;
- authority boundaries and invariants;
- validation PASS/FAIL/NOT_RUN state;
- changed-file ledger;
- open reviews/checks;
- highest remaining risk;
- exact file/function/location where work resumes;
- one executable `EXACT_NEXT_ACTION`.

Historical stage logs do not override current recovery state.

## 5. Incoming-agent takeover starts read-only

When taking over an existing engineering-critical PR, begin with:

```text
TAKEOVER_AUTHORITY = READ_ONLY
```

The incoming agent must independently:

1. re-ground against live repository state;
2. reconcile the prior report against the actual PR diff/head/main;
3. inspect important code/tests/evidence;
4. identify stale, contradicted, inherited and newly observed facts;
5. complete repository-specific takeover qualification;
6. decide whether the PR is safe to continue.

Do not grant write authority because an agent claims expertise.

## 6. Appendix A is an implementation qualification gate

For engineering-critical takeover, maintain **Appendix A — Implementation Takeover Qualification** against the **current unresolved work**.

Normally use five challenges:

```text
A1 Production Trace
A2 Current Failure Isolation
A3 Authority / Invariant
A4 Independent Validation
A5 Next-Commit / Minimal Patch
```

A question is invalid if it can be answered correctly without opening the current repository/PR/evidence.

Prefer tasks that require the agent to trace, reproduce, calculate, isolate, predict, falsify, compare, prove, reconcile, or define an exact patch boundary.

Do not use generic textbook prompts such as `What is FEA?`, `Explain validation`, or `Describe dependency injection` as qualification evidence.

For engineering-critical takeover, default qualification is:

```text
total >= 92/100
minimum per challenge >= 17/20
```

Fabricated repository evidence, unsafe engineering claims, validation gaming, or incorrect authority assumptions may cause immediate failure regardless of score.

## 7. Multi-agent coordination

Before implementation and before each new stage, inspect other active PRs/WIPs.

Check overlap in:

- exact files;
- directory/path prefixes;
- engineering/software authority domains;
- shared validation/release infrastructure;
- dependencies and stacked PR lineage;
- base/main drift.

Classify coordination as:

```text
SAFE
COORDINATION_REQUIRED
BLOCKED_BY_ACTIVE_CLAIM
UNKNOWN
```

No exact-file overlap does **not** prove semantic/authority independence.

## 8. Engineering validation integrity

Separate software regression evidence from independent engineering verification.

Every material validation should record:

```text
STATUS      = PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION = execution/inspection/inference basis
ORACLE      = implementation-coupled or independent authority class
```

Never:

- weaken a tolerance just because a test fails;
- replace an independent expected value with production output;
- change implementation and oracle together and call it independent verification;
- delete/skip a difficult benchmark merely to obtain green status;
- hard-code fixture answers into production;
- silence a fail-closed condition to make a test pass;
- represent source inspection as runtime proof;
- claim `NOT_RUN` as `PASS`.

## 9. Damaged or incapable-agent PRs

Do not preserve a PR because of sunk effort.

If current intent cannot be reconstructed safely, authority is unclear, commits cannot be classified, expected values changed with implementation, or rebase/conflict resolution requires guessing engineering intent, quarantine and assess salvage.

Valid recovery outcomes are:

```text
CONTINUE
SALVAGE_PARTIAL
SUPERSEDE
ABANDON
```

Preserve useful benchmarks, independent evidence, known-good commits, decisions, invariants and provenance even when the implementation PR is superseded.

Agent replacement alone is not a reason to create a new PR.

## 10. Scope, commit and merge discipline

- One coherent assignment per PR unless the owner explicitly changes scope.
- Keep implementation changes surgical and reviewable.
- Explain every changed file before closure.
- Do not silently broaden scope.
- Do not modify workflow files unless explicitly authorized.
- Keep the PR handover-ready while waiting for review/merge.
- **Never merge without explicit owner authorization.**

## 11. Repository role

`Common` is the cross-repository governance and controlled-reference repository. Changes to reusable Skills, methodology, controlled evidence, or cross-repo policy can affect many downstream repositories and therefore require explicit provenance, narrow scope, and durable compatibility reasoning.

## 12. AUTO MODE — autonomous phase execution

The exact owner keyword `AUTO MODE` grants **phase-progression authority**, not unlimited authority.

When the current owner instruction contains `AUTO MODE`, persist:

```text
EXECUTION_MODE = AUTO
AUTO_STATE = RUNNING
SCOPE_AUTHORITY = LOCKED_TO_APPROVED_MISSION
PHASE_PROGRESSION = AUTO
MERGE_AUTHORITY = OWNER_ONLY
```

`AUTO MODE` does **not** imply `AUTO MERGE`. Merge authority remains owner-only unless the owner separately and explicitly authorizes automatic merge.

### AUTO execution loop

While the approved mission remains incomplete and no hard-stop condition exists, the agent shall:

1. re-check current durable repository/PR state and active overlaps;
2. select the next approved phase from the recorded plan;
3. record the phase objective, expected files, rationale, predicted behavior, validation, and invariants;
4. implement only that phase;
5. validate and classify evidence accurately;
6. update the work report, findings, changed-file ledger, status/claims, and Appendix A if the next unresolved work changed;
7. create a durable checkpoint;
8. evaluate the hard-stop conditions below;
9. if none applies, continue automatically to the next approved phase.

Completion of a normal phase is **not** a reason to ask for owner confirmation.

While `EXECUTION_MODE=AUTO`, the following are invalid routine stops unless a defined hard-stop condition exists:

- `Phase complete; awaiting confirmation.`
- `Would you like me to continue?`
- `Let me know if you want the next stage.`
- `Should I run the remaining planned tests?`
- `I can continue if desired.`

### AUTO hard-stop conditions

AUTO progression must stop and record the exact reason when any of the following occurs:

- the next action materially expands or changes approved scope;
- the approved plan is materially invalidated and a new owner-level product/engineering choice is required;
- an engineering authority, governing formulation, controlled source, runtime/writer/canvas, or other protected authority must change beyond what was already authorized;
- safety-critical uncertainty cannot be bounded by existing approved evidence;
- takeover qualification fails, expires, or write authority is revoked;
- an independent oracle materially contradicts the implementation and bounded diagnosis cannot resolve it within approved scope;
- an unresolved `BLOCKED_BY_ACTIVE_CLAIM` or equivalent multi-agent authority collision exists;
- a destructive, credential, security, permission, or irreversible operation requires new authorization;
- continuing requires guessing engineering intent or silently weakening a validation/acceptance gate;
- `SUPERSEDE` or `ABANDON` would discard material work and owner disposition is required;
- merge is the next action but merge authority has not been separately granted.

On a hard stop set `AUTO_STATE` to `BLOCKED`, `OWNER_DECISION_REQUIRED`, or `TAKEOVER_REQUIRED` as appropriate, keep `HANDOVER_READINESS` current, and record the evidence, exact blocker, safe options, and one executable next action.

### Bounded self-recovery

AUTO MODE may automatically investigate, repair, rerun validation, and continue when the problem remains inside approved scope and authority boundaries.

It must not thrash indefinitely. If repeated attempts do not narrow the uncertainty, or the agent can no longer state a concrete current hypothesis, falsifier, next isolating experiment, and protected invariants, stop production mutation and set:

```text
PR_RECOVERY_STATE = TAKEOVER_REQUIRED
TAKEOVER_AUTHORITY = READ_ONLY
AUTO_STATE = TAKEOVER_REQUIRED
```

Refresh the work report and Appendix A so another qualified agent can recover immediately.
