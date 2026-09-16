# Checkpoint (CP)

A CP is the durable backward-looking result of an EP, never the next work instruction. It records EP/roadmap basis, exact execution/material basis, completed steps, files changed, acceptance results, validation truth, quality findings, limitations, discoveries, roadmap reconciliation, issue effects, Owner decisions required, remaining work and successor/frontier result.

Partial checkpoints are valid when truthful. At custody transfer the CP is immutable history; current execution moves through the reconciled roadmap and successor route.

## Exact evidence basis

`execution_basis.material_ref` identifies the exact material revision the checkpoint evaluates. Every executable `PASS`, `FAIL`, or `NOT_RUN` validation result carries `basis_ref` equal to that material reference. Evidence from another material head may remain historical evidence, but cannot qualify this checkpoint. `NOT_RUN` also records an explicit reason.

## Baton linkage

For a continuing serial relay, four references must agree:

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

The first EP uses `previous_checkpoint: NONE` with `last_checkpoint: {id: NONE, path: null}`.

For a terminal/idle relay, the final checkpoint uses `successor.mode: NONE`, the computed frontier is empty, and `active_ep.state: NONE`. A checkpoint that routes to one successor while `REPO_STATE` routes to another is invalid even when both files are individually well-formed.
