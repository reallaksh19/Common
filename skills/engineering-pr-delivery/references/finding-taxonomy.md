# Engineering Finding Taxonomy

Assign durable IDs to credible findings.

- `ISS-###` — confirmed defect.
- `IMP-###` — improvement opportunity.
- `RISK-###` — engineering/release risk.
- `DEC-###` — deliberate decision.
- `QST-###` — unresolved question.
- `DEBT-###` — accepted technical debt.

## Severity

- `S0` — safety/fundamental engineering correctness.
- `S1` — release blocking.
- `S2` — major functional/engineering impact.
- `S3` — moderate.
- `S4` — minor.

## Priority

- `P0` — immediate action.
- `P1` — current PR/stage.
- `P2` — next planned work.
- `P3` — backlog.

Severity is not priority.

## Disposition

Use:

- `OPEN`
- `CURRENT_PR`
- `FIXED`
- `VALIDATED`
- `ACCEPTED`
- `DEFERRED`
- `REJECTED`
- `BLOCKED`
- `TRANSFERRED`

Never silently drop an item because it is outside scope.

For significant items record affected components, observed behavior, engineering consequence, root cause or current hypothesis, resolution/decision, alternatives considered, edge cases, required validation, and closure evidence.
