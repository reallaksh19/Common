# Checkpoint (CP)

A CP is the durable backward-looking result of an EP, never the next work instruction. It records EP/roadmap basis, exact execution/material basis, completed steps, files changed, acceptance results, validation truth, quality findings, limitations, discoveries, roadmap reconciliation, issue effects, Owner decisions required, remaining work and successor/frontier result.

Partial checkpoints are valid when truthful. At custody transfer the CP is immutable history; current execution moves through the reconciled roadmap and successor route.

## Exact evidence basis

`execution_basis.material_ref` identifies the exact material revision the checkpoint evaluates. Every executable `PASS`, `FAIL`, or `NOT_RUN` validation result carries `basis_ref` equal to that material reference. Evidence from another material head may remain historical evidence, but cannot qualify this checkpoint. `NOT_RUN` also records an explicit reason.

## Successor modes

```text
SERIAL   one successor work package / EP
PARALLEL one Owner-approved fork with exact lane {WP, EP} receipts
JOIN     one completed parallel lane waiting for all sibling lane checkpoints
NONE     no material successor
```

## Serial baton linkage

For a continuing serial relay:

```text
REPO_STATE.last_checkpoint
        |
        v
checkpoint.successor.mode = SERIAL
checkpoint.successor.frontier_work_package / ep_id
        |
        v
REPO_STATE.current_position / active_ep
        |
        v
active EP identity.previous_checkpoint
```

## Parallel fork and join

For an Owner-approved fork:

```text
REPO_STATE.last_checkpoint
        |
        v
checkpoint.successor.mode = PARALLEL
checkpoint.successor.parallel_plan + exact lane {WP, EP} receipts
        |
        v
REPO_STATE PARALLEL router / approved plan
        |
        v
every lane EP identity.previous_checkpoint
```

A completed lane does not claim that integration is ready by itself. Its checkpoint uses `successor.mode: JOIN`, names the parallel plan and its lane ID, and waits for the other approved lanes.

When every lane is complete, a `PARALLEL_JOIN` receipt becomes the multi-parent baton:

```text
lane CP-A --JOIN--+
                  |
lane CP-B --JOIN--+--> PARALLEL_JOIN receipt
                  |        |
...---------------+        v
                    sole recomputed integration frontier
                             |
                             v
                       integration EP
                       previous_join = JOIN-ID
                       previous_checkpoint = NONE
```

The join receipt must cover every approved lane exactly once, validate every lane checkpoint, prove every lane roadmap node is complete, and prove the integration work package is the sole computed frontier. During the integration EP, `REPO_STATE.predecessor_join` points to this join and singular `last_checkpoint` is `NONE`. After integration produces its own checkpoint, normal serial checkpoint custody resumes.

The first EP uses `previous_checkpoint: NONE` with `last_checkpoint: {id: NONE, path: null}` and no predecessor join.

For a terminal/idle relay, the final checkpoint uses `successor.mode: NONE`, the computed frontier is empty, and `active_ep.state: NONE`. A checkpoint or join that routes to one successor while `REPO_STATE` routes to another is invalid even when the individual files are structurally well-formed.
