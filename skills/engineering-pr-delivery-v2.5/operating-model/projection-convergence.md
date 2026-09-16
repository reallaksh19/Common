# Projection convergence and relay readiness

Repository roadmap/state remains authoritative. GitHub Issues or other human coordination surfaces are projections, but custody transfer is not fully handover-ready until every required projection is synchronized.

## Projection publication identity

Every required projection is prepared before publication with a stable `operation_id`, durable `target`, current `roadmap_revision`, and current `execution_ref`. The same operation ID must be reused after interruption for the **same desired generation**. Never create a second publication merely because the agent cannot remember whether the first call returned.

Projection states are:

```text
NOT_REQUIRED           no external publication is required
PENDING                newest desired publication is durable; no receipt observed yet
PUBLISHED_UNCONFIRMED  newest desired operation has a receipt, but convergence is not verified
IN_SYNC                newest desired operation is verified against current repository state
STALE                  external surface reflects an older generation than current repository state
```

`PENDING` has no receipt. `PUBLISHED_UNCONFIRMED` has a receipt but is not projection-ready. A replacement agent reconciles the same `operation_id` against the same target before retrying publication. `IN_SYNC` requires a verified receipt and durable verification basis.

## Repository advances while projection is stale

The top-level `projection` fields always describe the **newest desired generation**, including while `state: STALE`:

```text
operation_id
roadmap_revision
execution_ref
```

They must match the current authoritative repository state.

`projection.observed` records the older generation currently known to exist on the external surface: its operation ID, target, roadmap revision, execution reference, external receipt and durable observation basis. A STALE projection is invalid if `observed` is actually the same repository generation as the newest desired state.

If repository state advances again before convergence, do not publish every intermediate generation. Move each obsolete desired operation into `superseded_operations` with:

- exact old operation ID/target/roadmap revision/execution reference;
- disposition `SUPERSEDED_BEFORE_PUBLICATION` or `SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED`;
- any observed receipt when publication occurred before supersession;
- durable basis explaining the supersession;
- `superseded_by` link to the next desired operation.

The supersession chain must be unique, acyclic and terminate at the current top-level operation. Superseded operation IDs have **no retry authority**. After a crash or long projection lag, reconcile/publish only the current operation.

Example:

```text
external observed: OP-1 / RM-1
repository desired: OP-2 / RM-2   (never published)
repository advances: OP-3 / RM-3

history:
  OP-2 --SUPERSEDED_BEFORE_PUBLICATION--> OP-3

publish/reconcile: OP-3 only
```

If an obsolete operation had already been published but not confirmed, retain its receipt as `SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED`; do not retry that operation. The receipt remains evidence of what may have occurred externally while the newest desired operation remains the only publication authority.

When the newest operation is published, transition to `PUBLISHED_UNCONFIRMED`. After verifying that receipt against the newest roadmap/execution basis, transition to `IN_SYNC`. At that point any retained `observed` entry must describe the same newest generation, not an older one.

## Readiness

`REPO_STATE.relay_readiness` separates:
- `repository_ready`: a replacement agent can recover authoritative repository state without chat;
- `projection_ready`: every required external coordination projection is `IN_SYNC` (or projection is not required);
- `handover_ready`: both predicates are true.

Projection lag does not rewrite engineering truth and does not automatically create an engineering hard stop. Repository engineering state may continue to advance when otherwise authorized. Projection lag prevents declaring complete custody transfer until the newest desired projection is reconciled. Release qualification is separate from relay handover readiness.
