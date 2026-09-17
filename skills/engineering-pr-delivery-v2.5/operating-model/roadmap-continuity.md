# Active EP continuity across roadmap revisions

A long-running EP may outlive one or more roadmap revisions. A roadmap revision mismatch is never ignored and does not automatically invalidate unrelated active work.

## Continuity transaction

If `EP.roadmap_source.roadmap_revision` differs from the current roadmap revision, `REPO_STATE.active_ep.continuity_receipt` is mandatory.

The `ROADMAP_CONTINUITY` receipt binds:

- the active EP and work package;
- the EP's original roadmap revision;
- the current roadmap revision;
- every intervening roadmap revision record, in order;
- explicit impact checks for definition, dependencies, acceptance, scope authority and protected invariants;
- one disposition and durable basis.

The revision chain must be contiguous from the EP revision to the current roadmap revision. Missing or repeated revision records invalidate continuity.

## Dispositions

```text
CONTINUE_UNCHANGED
RECONCILE_REQUIRED
INVALIDATED
```

### CONTINUE_UNCHANGED

The current EP may remain the material contract only when every covered roadmap revision explicitly lists the active work package as `unaffected`, never `changed` or `removed`, all impact checks are false, and the work package remains on the computed frontier.

This is positive evidence of non-impact, not an inference from silence.

### RECONCILE_REQUIRED

The same work package remains on the executable frontier, but at least one contract dimension may have changed. Repository custody remains recoverable, but material engineering writes are withheld:

```text
active_ep.state: RECONCILING
status_planes.execution.material_authority: READ_ONLY
```

Read-only discovery, comparison, validation and EP regeneration may continue. Material execution resumes only after a current-revision EP replaces/reconciles the old contract.

### INVALIDATED

The old EP cannot remain the active execution contract. Supersede/replace it, reconcile the roadmap/frontier and route from the resulting current state. An `INVALIDATED` receipt attached to an active EP is non-conformant.

## Roadmap revision responsibility

Every material roadmap revision that occurs while an EP is active must classify that active work package explicitly in its `changes` set. An active WP omitted from `changed`, `removed` and `unaffected` cannot support `CONTINUE_UNCHANGED`.

The continuity receipt is not a new planning authority. It only proves whether an existing execution contract survived the authoritative roadmap changes.