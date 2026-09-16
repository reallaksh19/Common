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

`CARRIED` and `INVALIDATED` lanes retain structured unresolved acceptance and evidence, including exact evidence status/basis, and name the work package receiving that custody. A transfer may not upgrade, drop, or rewrite unresolved evidence.

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
  unresolved_acceptance: ...
  evidence: ...
```

A successor parallel plan uses `previous_replan: <REPLAN-ID>`, and every successor lane EP also references that replan. Transferred acceptance/evidence must match the replan receipt exactly.

After a successor EP/lane produces its next normal checkpoint, ordinary checkpoint custody resumes and the replan becomes immutable history.
