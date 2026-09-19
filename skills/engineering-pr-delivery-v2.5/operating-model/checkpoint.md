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


## Checkpoint contract v2

New checkpoints use:

```yaml
schema_version: relay-v2.5
contract_version: 2
```

`contract_version` is checkpoint-local. It does not change the global V2.5 schema version.

Historical checkpoints without `contract_version` remain readable under the legacy contract. The validator emits a migration warning but does not invalidate old custody chains solely because the field is absent. New checkpoints must not omit it.

A v2 checkpoint makes the human-publication fields structural:

```text
implementation_result
  summary
  completed_steps[]
  files_changed[]

known_limitations[]
remaining_work[]

roadmap_reconciliation
  result
  status_updates[]
  proposals[]
  owner_decisions_required[]
```

Rules:

- `implementation_result.summary` is explicit plain-language engineering outcome, even when no files changed.
- `completed_steps[]` records only work completed on this checkpoint basis; no activity inflation.
- `files_changed[]` is the repository-relative file set changed by the checkpoint result. Empty is valid and explicitly means no files changed.
- `known_limitations[]` records unresolved limitations that remain true after the checkpoint.
- `remaining_work[]` records retained work, not the authoritative forward execution sequence; EP `next_work` remains the forward-work authority.
- roadmap reconciliation always carries all three detail arrays, even when empty.
- `NO_ROADMAP_CHANGE` with empty detail arrays is the normal case when work changed but programme structure did not.
- `ROADMAP_PROPOSAL` records proposed structural effects; it does not apply them.
- `OWNER_DECISION_REQUIRED` records the decision need and basis; it does not manufacture an Owner decision.

The v2 contract deliberately does not invent a second acceptance vocabulary. `acceptance_results` remains a checkpoint result list while acceptance-derived programme accounting remains authoritative in `PROGRESS.yaml`.

