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

Projection, drift, issue and parallel diagnostics:

```bash
python validate_projection_convergence.py <repo-root>
python validate_drift_receipt.py <repo-root>
python validate_issue_graph.py <repo-root>
python validate_issue_projection_tree.py <repo-root>
python validate_issue_closure.py <repo-root>
python validate_supersession.py <repo-root>
python validate_parallel_plan.py <repo-root>
python validate_parallel_join.py <repo-root>
python validate_parallel_replan.py <repo-root>
python validate_roadmap_continuity.py <repo-root>
```

`validate_projection_convergence.py` distinguishes newest desired projection state from the older generation actually observed externally. While `STALE`, top-level operation/roadmap/execution fields must match current repository truth, `observed` identifies the older external generation, and `superseded_operations` retires intermediate desired generations. Superseded operation IDs have no retry authority; their chain must terminate at the current operation. An obsolete published-but-unconfirmed generation retains its receipt as history rather than being replayed.

`validate_issue_projection_tree.py` treats `PARENT_OF` as a coordination projection tree, never an alternative roadmap. The parent graph must be acyclic and every child has at most one direct parent. Aggregate parents carry a `graph_revision`-bound `child_rollup` that exactly snapshots direct child work/GitHub state; parent work state is deterministically projected from those direct children. A closed aggregate parent cannot hide an open direct child, and the rule recursively covers deep trees because aggregate children are validated the same way.

`validate_supersession.py` supports multi-generation A -> B -> C issue replacement. Supersession is linear and acyclic at issue level. An intermediate successor must carry inherited unresolved acceptance/evidence unchanged into its outgoing receipt or explicitly resolve the inherited item with durable basis. Silent drop, status/basis mutation, double carry+resolve, resolution of unknown inherited IDs, branching successors, multiple direct predecessors and cycles are invalid. Work splitting belongs in roadmap/child-issue topology rather than competing supersession edges.

Required external projection publication is idempotent per desired generation. `PENDING` has no receipt, `PUBLISHED_UNCONFIRMED` preserves a receipt for reconciliation, and `IN_SYNC` requires durable verification basis. If repository truth advances first, move obsolete operations into `superseded_operations` and publish/reconcile only the newest operation.

Parallel lane checkpoints use successor mode `JOIN`. `validate_parallel_join.py` verifies the multi-parent baton: every approved lane checkpoint is present, every lane WP is complete, the integration WP is the sole computed frontier, and the integration EP binds the join receipt through `identity.previous_join`.

If one lane becomes invalid before convergence, the active parallel topology is frozen for material writes. `validate_parallel_replan.py` verifies the `PARALLEL_REPLAN` transaction: every old lane receives a `COMPLETE | CARRIED | INVALIDATED` disposition, completed lane checkpoints remain durable, the roadmap frontier is recomputed, and the successor route is deterministically `NONE`, `SERIAL`, or a newly Owner-approved `PARALLEL` plan.

For `CARRIED` and `INVALIDATED` lanes, `unresolved_acceptance` and `evidence` are the complete source inventory and `transfers[]` is an exact partition of that inventory across successor frontier work packages. The validator rejects dropped items, duplicates, status/basis mutation, duplicate transfer targets, and targets outside the recomputed frontier. If several predecessor transfers converge on one successor work package, that EP/lane must inherit their exact aggregate. If one predecessor lane splits across several successor WPs, each new EP/lane inherits only its exact addressed subset. Replacement EPs/plans bind the receipt through `previous_replan`.

Replacement parallel plans also persist `previous_replan_path`. `validate_parallel_replan.py` walks the complete historical `PLAN -> REPLAN -> PLAN -> ...` lineage backward and requires every cited receipt to exist, every receipt ID/path pair to agree, and each historical replan's successor route to point forward to the exact plan that cites it. Missing historical receipts, rewired forward links, and cycles are invalid.

After replan, route resolution reads only the current `REPO_STATE.execution_policy.parallel_plan`; stale predecessor-plan branches/worktrees resolve no executable lane unless the new approved plan explicitly reuses that route and the new EP independently passes live Git/material-basis checks.

`validate_roadmap_continuity.py` handles long-lived serial EPs across roadmap revisions. An old-revision EP requires a `ROADMAP_CONTINUITY` receipt covering every intervening revision. `CONTINUE_UNCHANGED` requires explicit unaffected classification plus no contract impact; `RECONCILE_REQUIRED` forces `active_ep.state: RECONCILING` and `READ_ONLY`; `INVALIDATED` forbids the old EP from remaining active.

Safe initialization and migration helpers:

```bash
# Dry-run by default; add --apply only after reviewing planned files.
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root>
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root> --apply

# Read-only V2 evidence inventory and non-authoritative reconciliation worksheet.
python inventory_v2_relay.py <repo-root> --output <inventory.yaml>
python prepare_v2_migration.py <inventory.yaml> --output <reconciliation.yaml>
```

Aggregate relay conformance verifies repository lifecycle/routing, roadmap topology/frontier, self-contained serial EPs or every Owner-approved parallel lane EP, acceptance mapping, EP staleness/continuity, calculated progress, execution/material authority, projection generation/readiness consistency, drift receipts, serial/fork/join/replan baton linkage, Owner-decision semantics, phase-transition Q1-Q5, issue graph/tree/closure/supersession lineage, and roadmap transactions.

Checkpoint validation binds executable PASS/FAIL/NOT_RUN evidence to the checkpoint's exact `execution_basis.material_ref`; evidence from another material head cannot silently qualify the current checkpoint.

Focused validators remain independently callable for diagnosis. `stress_test_relay.py` is read-only and repository-agnostic; real repositories are validation targets only.

PyYAML is required. Generated Markdown and GitHub Issues are projections, not authority sources.
