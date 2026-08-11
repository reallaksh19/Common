# Agent Engineering Work-Report + Delivery Protocol

You are authorized to work on this repository. **Keep all work for this assignment on one PR unless the Owner explicitly changes scope.**

Implementation and engineering handover documentation are part of the same task.

## 1. Living Work Report

Before changing production code, create:

```text
agents/PR_PENDING_workreport.md
```

After GitHub assigns the PR number, rename it:

```text
agents/PR<NUMBER>_workreport.md
```

Maintain this same file throughout the PR. It is the single source of truth for current state, engineering findings, decisions, validation, known issues, deferred work, and handover.

Do not create the report only at the end.

Before production implementation begins, record Stage 1 findings and the implementation roadmap.

---

## 2. Required Report Structure

### PR Mission Control

Maintain current values for:

```text
Mission
Source task / issue
PR number
Branch
Base commit
Current HEAD
PR status
Current stage
Last completed stage
Engineering status
Validation status
Current blocker
Exact next action
```

Maintain **Handover in 60 Seconds** with:

```text
What is now true
What is being worked on
What remains unfinished
What must not be assumed
Highest-risk remaining item
Exact next action
```

A new agent should understand the PR in under one minute.

### Mission and Engineering Intent

Record:

- mission;
- user/engineering consequence;
- scope;
- governing engineering principles;
- explicit non-goals;
- important constraints.

Explain the engineering reason for the work, not only the software change.

### Mission Status

Maintain:

| Work Item | Priority | Status | Stage | Evidence |
|---|---|---|---|---|

Use only:

```text
NOT_STARTED
INVESTIGATING
ACCEPTED
IN_PROGRESS
IMPLEMENTED
VALIDATED
DONE
BLOCKED
DEFERRED
REJECTED
```

### Engineering Item Register

Every credible finding gets a durable ID:

```text
ISS-###   confirmed defect
IMP-###   improvement opportunity
RISK-###  engineering/release risk
DEC-###   deliberate decision
QST-###   unresolved question
DEBT-###  accepted technical debt
```

Maintain:

| ID | Type | Severity/Priority | Status | Summary | Current PR? |
|---|---|---|---|---|---|

Never silently discard a finding because it is outside scope. Explicitly fix, accept, defer, reject with rationale, block, or transfer it to the roadmap.

For significant items record affected components, behavior, engineering consequence, root cause, resolution, alternatives, edge cases, required validation, and closure evidence.

---

## 3. Stage Roadmap and Stage Protocol

Before implementation define logical stages:

```text
Stage 1 — Report initialization + technical findings
Stage 2 — PR allocation + report synchronization
Stage 3 — Changed-file / repository-state verification
Stage 4+ — Implementation stages
```

Prefer small reviewable stages.

Before every stage, update the report with:

```text
Current truth
Objective
Expected scope/files
Engineering rationale
Planned implementation
Expected behavior
Edge cases
Planned validation
Known risks
```

Only then implement.

After every stage record:

```text
Implementation performed
Changed files and reasons
Deviations from plan
Actual behavior / edge cases
Validation performed
New findings
Remaining risks
Stage decision
Handover delta
```

Validation results must be:

```text
PASS
FAIL
NOT_RUN
NOT_APPLICABLE
```

Never write only “tests pass.” Name the exact test/check and tested HEAD where practical.

Stage decision must be:

```text
COMPLETE
PARTIAL
BLOCKED
ABORTED
```

Then refresh all current-state sections before beginning another stage.

---

## 4. Next-Agent Handover

Always maintain a permanent **Next-Agent Handover** containing:

```text
Current stopping point
PR / branch / HEAD
Last completed stage
Current active stage
Start here
Do not redo
Do not assume
Files currently involved
Known failing checks
Validation still required
Open QST-* items
Important deferred IMP-* items
Highest-risk remaining item
Exact next recommended action
Required reading
```

Be concrete.

Bad:

```text
Continue implementation.
```

Good:

```text
Start in src/.../file.js, function X.
ISS-004 remains unresolved because Y.
Reproduce Z, then implement A without changing B.
```

---

## 5. Changed-File Ledger

Maintain:

| File | First Stage | Latest Stage | Purpose | Engineering-sensitive? | Validation |
|---|---|---|---|---|---|

Before PR completion, compare this ledger with GitHub’s actual changed-file list.

Every discrepancy must be investigated and documented.

**Any unexplained changed file blocks closure.**

Do not commit unrelated files, `.bak`, `.old`, copied sources, or unrelated formatting churn.

---

## 6. Engineering Decisions and Invariants

Record significant choices as `DEC-*`.

Record critical invariants such as:

```text
Preview state must never become solver authority.
Unrelated rendering must not discard uncommitted engineering input.
Model-changing mutations must invalidate incompatible execution state.
```

For each invariant record:

```text
What must remain true
Where it is enforced
How it was validated
Whether this PR changes it
```

Future agents should not need to reconstruct important engineering intent from source code.

---

## 7. Validation and Evidence Ledger

Maintain separate current-state ledgers.

### Software Validation

| Validation | Status | Last HEAD | Evidence |
|---|---|---|---|

### Engineering Validation

| Property | Status | Evidence |
|---|---|---|

### Explicitly Not Validated

List significant properties that remain unproven.

Never turn:

```text
not checked
```

into:

```text
assumed correct
```

Unsupported claims are worse than explicitly recorded limitations.

---

## 8. Known / Deferred Work and Forward Sequence

Maintain a current view of:

```text
Open defects
Deferred improvements
Open risks
Open engineering questions
Accepted technical debt
```

Also maintain **Recommended Forward Sequence**.

For each important follow-up explain:

```text
Why it matters
Why it belongs at that point in the sequence
Prerequisites
Related ISS / IMP / RISK / QST IDs
```

The report should make creation of the next PR straightforward.

---

## 9. Current State vs History

Continuously rewrite these to latest truth:

```text
PR Mission Control
Handover in 60 Seconds
Mission Status
Engineering Item statuses
Stage Roadmap
Changed-File Ledger
Decision / invariant status
Validation Ledger
Known / Deferred Work
Recommended Forward Sequence
Next-Agent Handover
```

Keep these append-only where useful:

```text
Stage Execution Log
Process Notes / Lessons Learned
Resolved-item closure evidence
```

Do not force a future agent to read the full history to discover current state.

---

## 10. Process Notes / Lessons Learned

Record only reusable technical lessons, for example:

```text
A synchronous mutation triggered rendering before local state updated.
A planning document was stale relative to production source.
A test oracle depended on the implementation and was not independent.
Independent chart autoscaling made equivalent results appear different.
```

Avoid routine diary entries.

---

## 11. Commit and PR Rules

- Keep assignment work on one PR unless explicitly redirected.
- Prefer commits aligned with logical stages.
- Update the work report before each meaningful commit.
- Commit implementation and corresponding report state together where practical.
- Do not leave commits whose report describes the previous state.
- **Do not merge unless explicitly instructed.**
- Do not add or modify `.github/workflows/*` unless explicitly authorized.
- Use existing checks, targeted tests, local/repository validation, and engineering evidence.

---

## 12. Unexpected Findings and Stop Conditions

If implementation reveals something materially different from the original task:

1. Record it immediately.
2. Assign an `ISS`, `IMP`, `RISK`, `QST`, `DEC`, or `DEBT` ID.
3. Assess the engineering consequence.
4. Classify it as current-PR, deferred, rejected, blocked, or Owner-decision-required.
5. Update Mission Control and handover.

Do not silently broaden scope.

If the finding invalidates the intended approach, mark the stage `BLOCKED` or `PARTIAL` rather than forcing the planned solution.

---

## 13. Coding Rules

### Structure

- New JS modules should normally stay below 300 physical lines.
- Functions should normally stay below 40 logical lines.
- Split large existing files only when directly required.
- Use branch history instead of committed backup files.

### Design

- Prefer named exports.
- Prefer pure functions.
- Limit mutation to explicitly owned UI/runtime/store/transaction boundaries.
- No hidden globals or implicit singleton authority.
- Avoid mutation-heavy shared-object designs.

### Mocks, Defaults, Shims, and Abstractions

- No hidden/default mocks in production.
- No silent fallback engineering data.
- No temporary or authority-changing shims.
- Compatibility adapters must be explicit, bounded, tested, and production-consumed.
- Every new adapter, resolver, service, session, store, or abstraction must have a real production consumer in the same PR.
- New unused production modules: **0**.
- No speculative infrastructure.
- If unavoidable hard-coded/default behavior exists, expose it clearly to the user where relevant.

### Scope Control

- No broad unrelated refactor.
- No unrelated dependency upgrade.
- No generated-data churn unless required.
- No placeholder production behavior.
- No abandoned feature flags.
- No unrelated cleanup or formatting churn.

### Authority Protection

Do not change an authority boundary unless required by the approved task and explicitly documented.

Examples:

```text
Engineering authority
XML writer authority
Runtime publication authority
Renderer / canvas authority
CAD / SVG authority
Topology authority
Registry authority
Support classification authority
Persistence authority
Product-export authority
```

Any intentional authority change requires a `DEC-*` entry and focused validation.

---

## 14. Action-First Delivery Gate

The expected implementation order is:

```text
Core production behavior
→ real production integration
→ visible / downloadable / measurable result
→ focused regression validation
→ minimum required evidence
```

Do not substitute:

```text
Schemas
→ validators
→ certification framework
→ placeholder adapters
→ no usable capability
```

The majority of effort must go to the actual production capability.

A new abstraction is justified only when the current PR consumes it.

A capability is not complete merely because interfaces, schemas, validators, or tests exist.

Use this acceptance question throughout the work:

```text
Can an operator now use, see, download, export, or measure the intended capability through the real production path?
```

If the answer is **No**, the production capability is not yet complete.

---

# Core Operating Rule

At any point another competent agent must be able to continue using only:

```text
the repository
the PR number
agents/PR<NUMBER>_workreport.md
```

without needing prior conversation history.

If that is not currently possible, the work report is not sufficiently up to date.
