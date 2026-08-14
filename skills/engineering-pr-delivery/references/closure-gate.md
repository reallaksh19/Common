# Closure Gate

Do not claim completion until all applicable closure conditions are evaluated.

## Production capability

- Intended production behavior exists.
- Real production path consumes it.
- Intended operator can use/see/calculate/export/download/inspect/measure the result as required.
- No placeholder path is being represented as production completion.

## Scope and repository integrity

- Repository ground truth is current.
- Work-report HEAD equals actual current HEAD.
- Changed-file ledger matches actual changed files.
- No unexplained changed files exist.
- No unrelated formatting/dependency/generated churn exists.
- No unauthorized workflow change exists.

## Findings

- All `P0/P1` items have explicit disposition.
- Release-blocking `S0/S1` risks are resolved, accepted by the appropriate owner, or clearly block release.
- Deferred work is recorded with rationale and forward sequence.
- Open questions that affect correctness are not hidden.

## Validation

- Required software checks were executed or explicitly recorded `NOT_RUN` with consequence.
- Engineering-critical behavior has independent evidence where required.
- Observation method and oracle class are accurately represented.
- Significant unvalidated properties are listed explicitly.
- Behavior required to remain unchanged has negative-assurance evidence where material.

## Capability maturity

Do not use a single `DONE` label to hide incomplete layers. Evaluate:

```text
IMPLEMENTATION
INTEGRATION
SOFTWARE_VALIDATION
ENGINEERING_VALIDATION
RELEASE_STATE
```

## Handover

- Handover in 60 Seconds is current.
- Exact next action is concrete.
- A competent agent can continue from repository + PR + report without conversation history.

If any mandatory condition fails, closure is `BLOCKED` or `PARTIAL`, not complete.
