# Repository Ground Truth

Establish mutable repository state before planning or coding.

## Required snapshot

Record, where applicable:

```text
Repository
Default/base branch
Current remote base SHA
Current branch
Current HEAD
Merge base
Working-tree state
PR number and status
PR head/base
Linked issue/task
Actual changed-file list
Known failing checks
Relevant prior work
Work-report path and recorded HEAD
```

## Authority hierarchy

### Task intent and authorization

1. Current explicit user/owner instruction.
2. Current approved issue/task scope.
3. Repository-local governing instructions.

### Mutable repository state

1. Live Git/GitHub state.
2. Current local checkout state.
3. Living work report.
4. Conversation/history.

### Production behavior

1. Executed runtime behavior where applicable.
2. Production source actually consumed by runtime.
3. Tests and fixtures.
4. Documentation/planning material.

### Engineering authority

1. Explicit governing standard/approved source.
2. Authoritative project data.
3. Independently validated engineering formulation.
4. Production implementation.
5. Test fixture.
6. Documentation.

Lower-authority evidence must not silently override higher-authority evidence.

## Reconciliation rules

If local and remote state disagree, record the discrepancy before coding.

If the work report records a different HEAD from the actual branch, mark the report `STALE` until synchronized.

Mutable state remembered from conversation is never sufficient evidence that a PR is still open, a branch still exists, or a check still fails.

## Baseline contamination

Classify pre-existing modified files, failures, warnings, and numerical discrepancies as:

- `PREEXISTING`
- `INTRODUCED_BY_CURRENT_WORK`
- `UNKNOWN_ORIGIN`

Do not attribute a baseline failure to current work without evidence. Do not call a product `PASS` merely because a failure is pre-existing.
