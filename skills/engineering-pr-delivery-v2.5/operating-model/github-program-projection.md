# GitHub Program Projection

GitHub is an external coordination projection. `OVERALL_ROADMAP.yaml`, `ISSUE_GRAPH.yaml`, checkpoints, progress, and relay state remain repository authority.

WP-05 adds an operational transaction around the existing issue graph and projection-convergence model. It does **not** make GitHub issue content authoritative engineering state.

## Objects

```text
REPO_STATE.projection
  operation_id: GHGEN-xxxx
  adapter: GITHUB_ISSUES
  plan: agents/relay/projection/generations/GHGEN-xxxx.yaml

GHGEN-xxxx
  └── GHOP-xxxx CREATE | LINK | UPDATE | PUBLISH_HANDOVER |
                  SUPERSEDE | REVISE | CLOSE | REOPEN

GITHUB_OBSERVATION
  external call/readback evidence used to reconcile one GHOP
```

A `GHGEN-*` file is one immutable desired GitHub generation. A generation may contain several ordered operations. Repository state points only to the newest generation with publication authority.

## Verified external presence

`ISSUE_GRAPH.github_state` records the last **verified** external state:

```text
ABSENT   no GitHub issue has been verified for this repository issue node
OPEN     external issue was verified open
CLOSED   external issue was verified closed
UNKNOWN  a prior locator exists, but current external state must be re-observed
```

`github.issue_number` / `github.issue_id` are verified locators. A CREATE attempt does not change `ABSENT` to `OPEN`; only verified readback and reconciliation may do that.

Desired mutations live in `GHGEN-*`, not in `github_state`.

## Operation states

```text
PREPARED
ATTEMPTED_UNCONFIRMED
PUBLISHED_UNCONFIRMED
VERIFIED
SUPERSEDED
FAILED
```

`ATTEMPTED_UNCONFIRMED` is essential. It means the repository durably recorded that an external write was about to occur, but no reliable publication receipt/result is available. The external call may or may not have succeeded.

Never retry such an operation blindly.

## Crash-safe publication order

For every external mutation use this order:

```text
1. validate current GHGEN / GHOP
2. github_projection_next.py selects exactly one operation
3. begin_github_operation.py --apply
      PREPARED -> ATTEMPTED_UNCONFIRMED
      attempt basis is durable BEFORE the external call
4. perform exactly that external GitHub mutation
5. read the external object back
6. write a GITHUB_OBSERVATION
7. reconcile_github_projection.py --apply
8. validate repository conformance
9. only then publish the next GHOP
```

The repository should never execute a second operation while an earlier operation is unconfirmed.

### Crash before step 3

The operation remains `PREPARED`; it has not been granted an external-attempt record.

### Crash after step 3 but before the external call

The operation is `ATTEMPTED_UNCONFIRMED`. Read back GitHub first. If the desired mutation is absent, retry the **same GHOP/idempotency marker** rather than creating a new operation.

### Crash after the external call but before a connector receipt is recorded

The state is still `ATTEMPTED_UNCONFIRMED`. Read back by verified locator and/or the stable marker:

```text
<!-- relay-operation:GHOP-xxxx -->
```

If the mutation is observed, reconciliation can record a `READBACK_RECOVERY:*` repository receipt without pretending a connector response was received. This prevents duplicate CREATEs after timeouts.

### Receipt obtained, readback not yet verified

Use `PUBLISHED_UNCONFIRMED`. Receipt existence does not mean the desired external state has converged.

## Idempotency

Every operation has a stable `idempotency_key` and, for body-changing operations, a stable `relay-operation:GHOP-*` marker.

Idempotency means:

- a replacement agent continues the same GHOP after interruption;
- a timeout is reconciled before retry;
- duplicate issue creation is prevented by readback/search using the stable identity marker;
- an operation that becomes `SUPERSEDED` has no retry authority.

Do not generate a fresh operation ID merely because the previous external call outcome is unknown.

## Operation semantics

### CREATE

Repository issue node must be `github_state: ABSENT` (or `UNKNOWN` while reconciling a prior locator). The operation carries desired title/body/state. After verified readback, reconciliation records `OPEN` plus observed GitHub locator.

### LINK

The relationship must already exist in authoritative `ISSUE_GRAPH.yaml`. The operation projects that relationship externally and verification must observe the provider relationship.

A body hyperlink is not evidence of a provider-native parent/sub-issue relationship. If the available GitHub integration cannot perform or verify the required native relation, do not claim LINK verified. Keep projection incomplete and report the external capability limitation. Projection lag does not rewrite engineering truth or automatically become an engineering hard stop.

### UPDATE

Updates an existing issue projection. Source body/status must be derived from repository objects; GitHub text cannot be used to override them.

### PUBLISH_HANDOVER

Publishes the current source-derived handover/status projection to the existing issue coordination surface. Stable markers make replacement-agent retries idempotent.

### SUPERSEDE

Requires the repository `SUPERSEDES` relation and evidence-preserving supersession receipt first. GitHub then receives the corresponding successor/predecessor projection. External links never create engineering supersession authority.

### REVISE

Projects a repository-authorized issue revision/change. It must be based on current roadmap/issue truth rather than editing GitHub first and importing the result as intent.

### CLOSE

Allowed only after repository engineering state is terminal and the repository closure receipt is complete. Verification must observe GitHub `CLOSED`; only then is `ISSUE_GRAPH.github_state` reconciled to `CLOSED`.

### REOPEN

Allowed only when repository engineering state has already returned to `OPEN|ACTIVE` and the last verified external state is `CLOSED`. Repository truth changes first; GitHub follows.

## Dependencies

A generation may contain dependent operations, for example:

```text
CREATE child
   ↓
LINK child to parent
   ↓
PUBLISH_HANDOVER parent
   ↓
CLOSE superseded predecessor
```

`github_projection_next.py` only returns the first PREPARED operation whose dependencies are `VERIFIED|SUPERSEDED`. Dependency cycles are invalid.

## Reconciliation authority

An external write call never edits `ISSUE_GRAPH` by itself.

Only verified observation may apply declared `issue_graph_effects`, such as:

```text
ABSENT -> OPEN + observed locator
OPEN   -> CLOSED
CLOSED -> OPEN
```

Parent `child_rollup` snapshots are refreshed when child external state is reconciled, but the rollup remains a projection rather than roadmap authority.

## Generation supersession

When repository desired state changes before the current generation converges, prepare a new `GHGEN-*` and activate it transactionally.

The old generation becomes immutable `SUPERSEDED`. Any old retryable GHOP becomes `SUPERSEDED` and loses publication authority.

Top-level projection history preserves whether the old generation was:

```text
SUPERSEDED_BEFORE_PUBLICATION
SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED
SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED
```

A previously confirmed generation may instead become `projection.observed` while the new desired generation is `STALE` relative to the external surface.

`validate_github_generation_history.py` walks this chain and rejects missing history, cycles, or historical operations that remain retryable.

## Readiness

GitHub projection state remains independent from engineering execution authority.

```text
projection not IN_SYNC
  -> PROJECTION_READY false
  -> HANDOVER_READY false when projection is required

but does not automatically imply
  -> engineering hard stop
  -> loss of BATON_READY
  -> loss of candidate qualification
```

Engineering work may continue when otherwise authorized while external projection catches up.

## Operator commands

```bash
python validate_github_projection.py <repo-root>
python validate_github_generation_history.py <repo-root>
python github_projection_next.py <repo-root>
python begin_github_operation.py <repo-root> --basis <durable-basis> --apply
# perform exactly the returned external action
# read it back and write GITHUB_OBSERVATION.yaml
python reconcile_github_projection.py <observation.yaml> <repo-root> --apply
```

To replace an obsolete desired generation:

```bash
python activate_github_generation.py agents/relay/projection/generations/GHGEN-xxxx.yaml <repo-root> --apply
```

All mutating scripts are dry-run unless `--apply` is provided.
