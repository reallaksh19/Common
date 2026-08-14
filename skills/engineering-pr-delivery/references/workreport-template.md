# Living Work Report Template

Keep the current-state section concise enough that a new agent can orient quickly. Historical material follows a hard boundary.

```markdown
# PR<NUMBER> Engineering Work Report

# CURRENT STATE — READ THIS FIRST

## Handover in 60 Seconds

**What is now true:**

**What is being worked on:**

**What remains unfinished:**

**What must not be assumed:**

**Highest-risk remaining item:**

**Exact next action:**

## Repository Ground Truth

| Field | Current value |
|---|---|
| Repository | |
| Work intent | |
| Repository state | |
| Mutation authority | |
| Criticality | |
| Source task / issue | |
| PR number / status | |
| Branch | |
| Base branch / SHA | |
| Merge base | |
| Current HEAD | |
| Work-report recorded HEAD | |
| Ground-truth status | CURRENT / STALE |
| Working tree | |
| Current blocker | |

## Mission and Engineering Intent

### Mission

### User / engineering consequence

### Scope

### Governing engineering principles

### Explicit non-goals

### Important constraints

## Capability Status

| Work item | Priority | Implementation | Integration | Software validation | Engineering validation | Release state | Evidence |
|---|---|---|---|---|---|---|---|

## Active Engineering Items

| ID | Type | Severity | Priority | Disposition | Summary | Current PR? |
|---|---|---|---|---|---|---|

## Active Blocking Items

## Current Stage

**State:** BOOTSTRAP / BASELINE / PLAN / IMPLEMENT / VALIDATE / RECONCILE / HANDOVER / CLOSURE

**Objective:**

**Expected files:**

**Planned validation:**

**Known risks:**

## Validation Summary

| Validation | Status | Observation | Oracle | Last HEAD | Evidence |
|---|---|---|---|---|---|

### Explicitly Not Validated

## Changed-File Ledger

| File | First stage | Latest stage | Purpose | Engineering-sensitive? | Validation |
|---|---|---|---|---|---|

## Decisions and Invariants

| ID / invariant | What must remain true | Where enforced | Validation | Changed by PR? |
|---|---|---|---|---|

## Negative Assurance

**Behavior intended to change:**

**Behavior required to remain unchanged:**

**Evidence invariants remain true:**

## Deferred / Forward Work

## Exact Next Action

## Next-Agent Handover

- Current stopping point:
- PR / branch / HEAD:
- Last completed stage:
- Current active stage:
- Start here:
- Do not redo:
- Do not assume:
- Files currently involved:
- Known failing checks:
- Validation still required:
- Open QST-* items:
- Important deferred IMP-* items:
- Highest-risk remaining item:
- Exact next recommended action:
- Required reading:

# HISTORICAL RECORD — DO NOT USE AS CURRENT STATE

## Stage Execution Log

## Resolved Findings / Closure Evidence

## Process Notes / Lessons Learned
```

## Synchronization invariant

Before a stage is considered synchronized:

```text
work-report Current HEAD == actual current HEAD
```

If not, mark the report stale and reconcile it.
