# Stage Protocol

Use state-dependent bootstrap rather than manufacturing fixed stages that do not fit the repository state.

## State machine

```text
BOOTSTRAP -> BASELINE -> PLAN -> IMPLEMENT -> VALIDATE -> RECONCILE -> HANDOVER -> CLOSURE
```

Review/audit tasks may omit implementation. Continuation work begins with `BOOTSTRAP`, recovers prior state, reconciles the report and repository, then resumes the appropriate state.

## Before an implementation stage

Record:

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
Behavior that must remain unchanged
```

Only then implement.

## After a stage

Record:

```text
Implementation performed
Changed files and reasons
Deviations from plan
Actual behavior / edge cases
Validation performed
New findings
Remaining risks
Negative-assurance evidence
Stage decision
Handover delta
```

Stage decision must be one of:

- `COMPLETE`
- `PARTIAL`
- `BLOCKED`
- `ABORTED`

Refresh all current-state sections before another stage.

## Stop conditions

Mark the stage `PARTIAL` or `BLOCKED` when:

- repository truth materially differs from the assumed baseline;
- a new finding invalidates the intended approach;
- required authority is missing or ambiguous;
- independent validation required for an engineering-critical change cannot be established;
- an unexplained changed file exists;
- a required check fails and the failure cannot be responsibly dispositioned.

Do not force the planned solution through a contradicted baseline.
