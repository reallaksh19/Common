# Parallel replan after lane invalidation

An Owner-approved parallel plan is one material execution contract. If any lane becomes stale, invalid, unauthorized, superseded, or otherwise unable to continue under the approved topology, the old plan does not limp forward lane-by-lane.

## Immediate consequence

Material writes under the predecessor plan stop while the replan is reconciled. Read-only inspection may continue. Completed lane work is not discarded and invalidated lane work is not silently erased.

Create a durable `PARALLEL_REPLAN` receipt with:

- predecessor plan ID/path;
- exact trigger, reason and durable basis;
- one disposition for every predecessor lane;
- current roadmap revision and recomputed frontier;
- deterministic successor route.

Lane dispositions are:

```text
COMPLETE    — lane finished; retain its exact checkpoint/evidence.
CARRIED     — lane remains unresolved but its old route/topology is replaced.
INVALIDATED — lane cannot safely continue under the predecessor plan.
```

## Exact transfer partition

`CARRIED` and `INVALIDATED` lanes retain their complete structured `unresolved_acceptance` and `evidence` inventories, including exact state/status and durable basis.

They then declare one or more `transfers`:

```yaml
unresolved_acceptance: [<complete unresolved inventory>]
evidence: [<complete evidence inventory>]
transfers:
  - work_package: WP-R1
    unresolved_acceptance: [<subset>]
    evidence: [<subset>]
  - work_package: WP-R2
    unresolved_acceptance: [<remaining subset>]
    evidence: [<remaining subset>]
```

The transfer sets are a partition, not a summary. Across all transfer targets for that predecessor lane:

- every unresolved acceptance item must appear exactly once;
- every evidence item must appear exactly once;
- evidence status, basis and NOT_RUN reason must remain unchanged;
- duplicate transfer targets are invalid;
- every target must be in the recomputed executable frontier.

This allows a failed lane to split into multiple replacement work packages without losing or duplicating custody. It also allows several predecessor lanes to converge into one successor work package; that successor EP inherits the exact aggregate of all transfers addressed to it.

## Recompute before choosing the route

The roadmap is reconciled first. `frontier_after` must equal the frontier computed from the resulting roadmap.

Then route only from frontier cardinality:

```text
0 nodes  -> NONE      -> IDLE or TERMINAL
1 node   -> SERIAL    -> one replacement EP
2+ nodes -> PARALLEL  -> a new Owner-approved parallel plan
```

The old parallel plan never regains authority merely because one sibling lane remains usable.

## Successor baton

`REPO_STATE.predecessor_replan` identifies the active replan transaction and is mutually exclusive with `last_checkpoint` and `predecessor_join` while that transaction is the current predecessor baton.

A serial replacement EP uses:

```text
identity.previous_replan: <REPLAN-ID>
replan_inheritance:
  from_replan: <REPLAN-ID>
  unresolved_acceptance: <exact aggregate addressed to this WP>
  evidence: <exact aggregate addressed to this WP>
```

A successor parallel plan stores both:

```text
previous_replan: <REPLAN-ID>
previous_replan_path: <durable receipt path>
```

Every successor lane EP also references that replan. Each lane inherits the exact aggregate addressed to its work package. A new frontier lane that received no predecessor transfer still references the replan and has empty inherited acceptance/evidence.

The active `REPO_STATE.execution_policy.parallel_plan` is the only parallel topology eligible for route resolution. Old predecessor-plan branches/worktrees do not resolve an executable lane unless the new approved plan explicitly reuses that route and the new EP passes its live Git/material-basis checks.

## Multi-generation history

A replacement parallel plan may itself later be replanned. Historical custody therefore forms an alternating chain:

```text
PLAN-P1
  -> REPLAN-P2
  -> PLAN-P2
  -> REPLAN-P3
  -> PLAN-P3
  -> ...
```

The chain is not optional audit prose. The validator walks backward from the active `predecessor_replan` and requires:

- every cited historical replan receipt to exist;
- every `previous_replan` ID to match the receipt at `previous_replan_path`;
- every historical replan successor route to point forward to the exact plan that cites it;
- predecessor plan IDs/paths to remain consistent;
- no repeated replan IDs or predecessor-plan paths in the lineage.

Missing receipts, forward-link mismatch and cycles invalidate the current replan chain. This prevents an agent from retaining only the latest plan while silently deleting or rewiring the decisions and evidence that produced it.

After a successor EP/lane produces its next normal checkpoint, ordinary checkpoint custody resumes. Replan receipts and plans remain immutable historical lineage and are not rewritten to simplify the chain.
