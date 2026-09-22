# Projection convergence and relay readiness

Repository roadmap/state remains authoritative. GitHub Issues or other human coordination surfaces are projections, but custody transfer is not fully handover-ready until every required projection is synchronized.

Projection readiness is independent from both repository baton completeness and candidate-specific takeover certification.

## Projection publication identity

Every required projection is prepared before publication with a stable `operation_id`, durable `target`, current `roadmap_revision`, and current `execution_ref`. The same operation ID must be reused after interruption for the **same desired generation**. Never create a second publication merely because the agent cannot remember whether the first call returned.

For the operational GitHub adapter, the top-level `operation_id` is a `GHGEN-*` generation and `projection.plan` points to the immutable generation journal under `agents/relay/projection/generations/`. Individual external mutations within the generation use `GHOP-*` IDs and have their own crash-safe state. See `github-program-projection.md`.

Projection states are:

```text
NOT_REQUIRED           no external publication is required
PENDING                newest desired publication is durable; no confirmed top-level receipt
PUBLISHED_UNCONFIRMED  newest desired generation has external receipt evidence but convergence is not verified
IN_SYNC                newest desired generation is verified against current repository state
STALE                  external surface reflects an older generation than current repository state
```

`PENDING` has no top-level receipt. For the GitHub adapter, it may include a `GHOP-* ATTEMPTED_UNCONFIRMED` operation; that uncertain attempt is retained inside the generation journal and must be reconciled before retrying or publishing later operations.

`PUBLISHED_UNCONFIRMED` has a receipt but is not projection-ready. A replacement agent reconciles the same generation/operation identity before republishing. `IN_SYNC` requires verified basis.

## GitHub adapter layering

The generic projection plane and GitHub operation journal have distinct jobs:

```text
REPO_STATE.projection
  newest desired external generation + readiness

GHGEN-*
  ordered external mutation journal

GHOP-*
  one idempotent external operation

GITHUB_OBSERVATION
  external readback evidence

ISSUE_GRAPH
  last verified GitHub issue/relationship projection
```

A GitHub write call does not itself advance `ISSUE_GRAPH`. Only verified readback reconciles external state into the graph.

The write sequence must persist `GHOP: ATTEMPTED_UNCONFIRMED` **before** making the external mutation. This means a crash can always be distinguished from a never-started operation. If the write may have succeeded but no connector receipt exists, stable markers/locators are read back first. Verification may then preserve a `READBACK_RECOVERY:*` receipt without pretending the missing connector response was received.

## Repository advances while projection is stale

The top-level `projection` fields always describe the **newest desired generation**, including while `state: STALE`:

```text
operation_id
roadmap_revision
execution_ref
```

They must match the current authoritative repository state.

`projection.observed` records the older generation currently known to exist on the external surface: its operation ID, target, roadmap revision, execution reference, external receipt and durable observation basis. A STALE projection is invalid if `observed` is actually the same repository generation as the newest desired state under the generic roadmap/execution identity.

If repository state advances again before convergence, do not publish every intermediate generation. Move each obsolete desired generation into history with one of:

```text
SUPERSEDED_BEFORE_PUBLICATION
SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED
SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED
SUPERSEDED_AFTER_VERIFIED_PUBLICATION
```

The middle state records the important case where an external mutation may have occurred but no connector receipt exists. It must not fabricate a receipt.

For the GitHub adapter, `activate_github_generation.py` additionally marks the old `GHGEN-*` immutable `SUPERSEDED`; every old retryable `GHOP-*` loses publication authority. `validate_github_generation_history.py` rejects missing predecessor generations, cycles, or historical retryable operations.

The projection supersession chain must be unique, acyclic and terminate at the current top-level generation. Superseded generation/operation IDs have **no retry authority**. After a crash or long projection lag, reconcile/publish only the current authorized generation.

Example:

```text
external observed: GHGEN-1 / RM-1
repository desired: GHGEN-2 / RM-2   (never published)
repository advances: GHGEN-3 / RM-3

history:
  GHGEN-2 --SUPERSEDED_BEFORE_PUBLICATION--> GHGEN-3

publish/reconcile: GHGEN-3 only
```

If an obsolete generation had already been published but not confirmed, retain its receipt as `SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED`; do not retry it. If only an attempt is known, retain `SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED` without a receipt. If the predecessor was already verified and therefore occupied `projection.observed`, convergence of its successor moves that predecessor into history as `SUPERSEDED_AFTER_VERIFIED_PUBLICATION` with its verified receipt and makes the newly verified generation the current `projection.observed`.

When the newest generation fully verifies, transition to `IN_SYNC`. For `GITHUB_ISSUES`, all generation operations must be `VERIFIED|SUPERSEDED`, `projection.observed` must identify the current verified generation, and `ISSUE_GRAPH` must reflect every declared reconciliation effect.

## Readiness

`REPO_STATE.relay_readiness` separates repository-wide custody predicates:

```text
baton_ready       semantic repository baton is complete for a zero-context replacement
projection_ready  every required external coordination projection is IN_SYNC, or not required
handover_ready    baton_ready AND projection_ready
```

`baton_ready` is not candidate admission. A baton-ready repository may have no future replacement yet and therefore an empty `takeover_admissions[]` list.

Candidate admission is route-scoped and lives in durable `DISC-*` / `TC-*` evidence referenced by `REPO_STATE.takeover_admissions[]`:

```text
TAKEOVER_CERTIFIED(route,candidate)
```

Live engineering write permission is later derived from the certified candidate, live route/Git state, drift/continuity, execution authority and stop state:

```text
MATERIAL_WRITE_READY(route,candidate,live_git)
```

It is never inferred from projection readiness and is not persisted as a timeless repository boolean.

Projection lag or an unavailable external relationship capability does not rewrite engineering truth, baton completeness, or existing candidate evidence and does not automatically create an engineering hard stop. Repository engineering state may continue to advance when otherwise authorized. Projection lag prevents declaring complete custody handover until the newest required projection is reconciled.
