# Context and freshness

## Three snapshots

Every material acceptance path uses:

1. `START` — context reconciled before stage work.
2. `PRE_VERDICT` — context refreshed before an advancing engineering outcome.
3. `PRE_MERGE` — context refreshed before merge readiness/merge.

## Provider-level context identity

A context snapshot records aggregate digests plus provider-level events. Each event records:

- source kind;
- provider ID/reference;
- author principal;
- created/updated timestamps;
- body digest;
- mutability.

This prevents a mutable comment or description from being represented only as an ambiguous prose frontier.

At minimum the snapshot carries parent-issue and current-task issue identity. Child/PR work also carries PR-description identity. The parent-comment frontier must resolve to an event in the snapshot.

## Lease relationship

The independent review lease is sealed against PRE_VERDICT context, including parent frontier, task context, PR description and Owner-control digest.

PRE_MERGE context must still match the final lease. Material drift expires current engineering approval instead of being reconciled by memory or prose.

## Repository freshness

Merge readiness also checks:

- exact PR head;
- exact task target ref and target head;
- merge base;
- integration tree;
- workspace/source digest;
- Common/project protocol;
- required-check policy;
- environment;
- stacked dependency heads.

## Owner controls

Hold/Pause/Stop are re-read at stage boundaries, pre-verdict, pre-merge and merge timing. Resume is not approval; it requires fresh reconciliation.

## Post-merge canonical target

Delivery records provider-observed target-ref state after merge. The observation binds reviewed head and merge commit. If the target still equals the merge commit, use `EXACT_MERGE_COMMIT`. If the target has advanced, use `DESCENDANT_CONTAINS_MERGE` with an explicit provider ancestry-proof reference.

Common uses “target ref,” not a universal assumption that every child PR merges directly to `main`.

## Merge-decision freshness

PRE_MERGE trust also includes current repository-policy visibility and current merge authority. Unknown policy visibility waits externally; missing authority waits on the Owner. A malformed/unauthenticated authority claim is rejected. Delivery rechecks authority at the actual merge timestamp, so an authorization observed only after merge cannot retroactively justify it.
