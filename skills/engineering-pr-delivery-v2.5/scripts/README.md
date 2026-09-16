# V2.5 validator and lifecycle commands

From the downstream repository root run the validators from this directory. Primary entrypoints:

```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python stress_test_relay.py <repo-root> [<repo-root> ...]
python render_status.py <repo-root>
python render_handover.py <repo-root>
```

Before material writes, resolve and inspect the live Git context:

```bash
python resolve_execution_route.py <repo-root>
python inspect_git_context.py <repo-root>
```

`resolve_execution_route.py` selects the serial EP or exactly one approved parallel lane from the checked-out branch/worktree. `inspect_git_context.py` verifies expected branch/material ancestry and compares the current base branch with the EP's observed base. If the base moved it returns `NEEDS_DRIFT_RECEIPT` plus changed paths; it never auto-classifies drift as safe. The drift receipt may preserve `WRITE` only for a fully `DISJOINT` result or a qualified-boundary result whose independent confirmation is satisfied; otherwise execution remains `READ_ONLY` until reconciliation.

Roadmap, projection, drift and parallel diagnostics:

```bash
python validate_roadmap_continuity.py <repo-root>
python validate_projection_convergence.py <repo-root>
python validate_drift_receipt.py <repo-root>
python validate_parallel_plan.py <repo-root>
python validate_parallel_join.py <repo-root>
python validate_parallel_replan.py <repo-root>
```

If an active serial EP was generated from an older roadmap revision, a `ROADMAP_CONTINUITY` receipt is mandatory. `validate_roadmap_continuity.py` walks every intervening revision record from the EP revision to the current roadmap revision. `CONTINUE_UNCHANGED` requires the active WP to be explicitly listed as unaffected in every covered revision, all contract-impact checks false and the WP still on the computed frontier. `RECONCILE_REQUIRED` keeps repository custody recoverable but requires `active_ep.state: RECONCILING` and `material_authority: READ_ONLY`. `INVALIDATED` cannot remain attached to an active EP.

Required external projection publication is idempotent: persist a stable `operation_id` and target before publication, record `PUBLISHED_UNCONFIRMED` when a receipt is observed but not yet verified, and move to `IN_SYNC` only after the receipt is reconciled against current roadmap/execution state. After an interruption, reconcile the same operation before attempting another publication.

Parallel lane checkpoints use successor mode `JOIN`. `validate_parallel_join.py` verifies the multi-parent baton: every approved lane checkpoint is present, every lane WP is complete, the integration WP is the sole computed frontier, and the integration EP binds the join receipt through `identity.previous_join`.

If one lane becomes invalid before convergence, the active parallel topology is frozen for material writes. `validate_parallel_replan.py` verifies the `PARALLEL_REPLAN` transaction: every old lane receives a `COMPLETE | CARRIED | INVALIDATED` disposition, completed lane checkpoints remain durable, the roadmap frontier is recomputed, and the successor route is deterministically `NONE`, `SERIAL`, or a newly Owner-approved `PARALLEL` plan.

For `CARRIED` and `INVALIDATED` lanes, `unresolved_acceptance` and `evidence` are the complete source inventory and `transfers[]` is an exact partition of that inventory across successor frontier work packages. The validator rejects dropped items, duplicates, status/basis mutation, duplicate transfer targets, and targets outside the recomputed frontier. If several predecessor transfers converge on one successor work package, that EP/lane must inherit their exact aggregate. If one predecessor lane splits across several successor WPs, each new EP/lane inherits only its exact addressed subset. Replacement EPs/plans bind the receipt through `previous_replan`.

Replacement parallel plans also persist `previous_replan_path`. `validate_parallel_replan.py` walks the complete historical `PLAN -> REPLAN -> PLAN -> ...` lineage backward and requires every cited receipt to exist, every receipt ID/path pair to agree, and each historical replan's successor route to point forward to the exact plan that cites it. Missing historical receipts, rewired forward links, and cycles are invalid.

After replan, route resolution reads only the current `REPO_STATE.execution_policy.parallel_plan`; stale predecessor-plan branches/worktrees resolve no executable lane unless the new approved plan explicitly reuses that route and the new EP independently passes live Git/material-basis checks.

Safe initialization and migration helpers:

```bash
# Dry-run by default; add --apply only after reviewing planned files.
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root>
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root> --apply

# Read-only V2 evidence inventory and non-authoritative reconciliation worksheet.
python inventory_v2_relay.py <repo-root> --output <inventory.yaml>
python prepare_v2_migration.py <inventory.yaml> --output <reconciliation.yaml>
```

Aggregate relay conformance verifies repository lifecycle/routing, roadmap topology/frontier, active-EP roadmap continuity, self-contained serial EPs or every Owner-approved parallel lane EP, acceptance mapping, EP staleness, calculated progress, execution/material authority, projection/readiness consistency, drift receipts, serial/fork/join/replan baton linkage, Owner-decision semantics, phase-transition Q1-Q5, issue graph/closure/supersession, and roadmap transactions.

Checkpoint validation binds executable PASS/FAIL/NOT_RUN evidence to the checkpoint's exact `execution_basis.material_ref`; evidence from another material head cannot silently qualify the current checkpoint.

Focused validators remain independently callable for diagnosis. `stress_test_relay.py` is read-only and repository-agnostic; real repositories are validation targets only.

PyYAML is required. Generated Markdown and GitHub Issues are projections, not authority sources.
