# Projection convergence and relay readiness

Repository roadmap/state remains authoritative. GitHub Issues or other human coordination surfaces are projections, but custody transfer is not fully handover-ready until every required projection is synchronized.

## Projection publication identity

Every required projection is prepared before publication with a stable `operation_id`, durable `target`, current `roadmap_revision`, and current `execution_ref`. The same operation ID must be reused after interruption. Never create a second publication merely because the agent cannot remember whether the first call returned.

Projection states are:

```text
NOT_REQUIRED           no external publication is required
PENDING                desired publication is durable; no receipt observed yet
PUBLISHED_UNCONFIRMED  an external receipt was observed, but convergence has not yet been verified
IN_SYNC                receipt is verified against the current roadmap/execution reference
STALE                  an earlier projection exists but no longer represents current repository state
```

`PENDING` has no receipt. `PUBLISHED_UNCONFIRMED` has a receipt but is not projection-ready. A replacement agent reconciles the same `operation_id` against the same target before retrying publication. `IN_SYNC` requires a verified receipt and durable verification basis. This makes a crash immediately before, during, or after publication recoverable without intentionally creating duplicate projection events.

## Readiness

`REPO_STATE.relay_readiness` separates:
- `repository_ready`: a replacement agent can recover authoritative repository state without chat;
- `projection_ready`: every required external coordination projection is `IN_SYNC` (or projection is not required);
- `handover_ready`: both predicates are true.

Projection lag does not rewrite engineering truth and does not automatically create an engineering hard stop. It prevents declaring complete custody transfer until reconciled. Release qualification is separate from relay handover readiness.
