# Checkpoint (CP)

A CP is the durable backward-looking result of an EP, never the next work instruction. It records EP/roadmap basis, completed steps, files changed, acceptance results, validation truth, quality findings, limitations, discoveries, roadmap reconciliation, issue effects, Owner decisions required, remaining work and successor/frontier result.

Partial checkpoints are valid when truthful. At custody transfer the CP is immutable history; current execution moves through the reconciled roadmap and successor EP.

## Baton linkage

For a continuing relay, four references must agree:

```text
REPO_STATE.last_checkpoint
        |
        v
checkpoint.successor.frontier_work_package
checkpoint.successor.ep_id
        |
        v
REPO_STATE.current_position / active_ep
        |
        v
active EP identity.previous_checkpoint
```

The first EP uses `previous_checkpoint: NONE` with `last_checkpoint: {id: NONE, path: null}`.

For a terminal/idle relay, the final checkpoint has no successor, the computed frontier is empty, and `active_ep.state: NONE`. A checkpoint that routes to one successor while `REPO_STATE` routes to another is invalid even when both files are individually well-formed.