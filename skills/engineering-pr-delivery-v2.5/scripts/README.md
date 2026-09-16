# V2.5 validator and lifecycle commands

From the downstream repository root run the validators from this directory. Primary entrypoints:

```bash
python validate_relay_conformance.py <repo-root>
python cold_start_check.py <repo-root>
python stress_test_relay.py <repo-root> [<repo-root> ...]
python render_status.py <repo-root>
python render_handover.py <repo-root>
```

## Semantic baton validation

WP-01 adds two independently callable admission checks:

```bash
python validate_repo_profile.py <repo-root>
python validate_ep_semantics.py <repo-root>
```

`validate_repo_profile.py` makes `agents/relay/REPO_PROFILE.yaml` part of aggregate conformance. `validate_repo_state.py` now also requires `relay_protocol.version: "2.5"` and an explicit non-placeholder pinned `basis_ref`.

`validate_ep_semantics.py` rejects hollow forward contracts. It validates `DSTEP-*` discovery instructions, typed current-slice inputs, typed benchmarks/oracles, semantic write/read/protected/prohibited/Owner-reserved scope, structured anti-drift, implementation-step reference mappings, source-bound report payloads, and durable successor outputs. Aggregate conformance runs it for serial active EPs; `validate_parallel_plan.py` runs the same semantic validator for every approved lane EP.

`validate_report_contract.py` now requires source/reconciliation payloads for every mandatory report heading instead of validating headings alone.

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

`validate_issue_projection_tree.py` treats `PARENT_OF` as a coordination projection tree, never an alternative roadmap. Aggregate parents carry a `graph_revision`-bound `child_rollup` that snapshots direct child work/GitHub state; a closed aggregate parent cannot hide an open direct child.

`validate_supersession.py` supports multi-generation A -> B -> C issue replacement. An intermediate successor must carry inherited unresolved acceptance/evidence unchanged into its outgoing receipt or explicitly resolve the inherited item with durable basis. Silent drop, mutation, branching successors, multiple direct predecessors and cycles are invalid.

Required external projection publication is idempotent per desired generation. `PENDING` has no receipt, `PUBLISHED_UNCONFIRMED` preserves a receipt for reconciliation, and `IN_SYNC` requires durable verification basis. If repository truth advances first, obsolete operations move into `superseded_operations`; only the newest operation retains publication authority.

Parallel lane checkpoints use successor mode `JOIN`. `validate_parallel_join.py` verifies the multi-parent baton: every approved lane checkpoint is present, every lane WP is complete, the integration WP is the sole computed frontier, and the integration EP binds the join receipt through `identity.previous_join`.

If one lane becomes invalid before convergence, the active parallel topology is frozen for material writes. `validate_parallel_replan.py` verifies the `PARALLEL_REPLAN` transaction, lane dispositions, exact unresolved acceptance/evidence transfer partitions, recomputed frontier and deterministic successor route. Replacement EPs/plans bind the receipt through `previous_replan`.

Replacement parallel plans also persist `previous_replan_path`. Replan validation walks the complete historical `PLAN -> REPLAN -> PLAN -> ...` lineage and rejects missing receipts, rewired forward links, and cycles.

After replan, route resolution reads only the current `REPO_STATE.execution_policy.parallel_plan`; stale predecessor-plan branches/worktrees resolve no executable lane unless the new approved plan explicitly reuses that route and the new EP independently passes live Git/material-basis checks.

`validate_roadmap_continuity.py` handles long-lived serial EPs across roadmap revisions. `CONTINUE_UNCHANGED` requires explicit unaffected classification plus no contract impact; `RECONCILE_REQUIRED` forces `active_ep.state: RECONCILING` and `READ_ONLY`; `INVALIDATED` forbids the old EP from remaining active.

Safe initialization and migration helpers:

```bash
# Dry-run by default; add --apply only after reviewing planned files.
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root>
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root> --apply

# Read-only V2 evidence inventory and non-authoritative reconciliation worksheet.
python inventory_v2_relay.py <repo-root> --output <inventory.yaml>
python prepare_v2_migration.py <inventory.yaml> --output <reconciliation.yaml>
```

Aggregate relay conformance verifies repository/profile/protocol admission, lifecycle/routing, roadmap topology/frontier, self-contained and semantic serial EPs or every Owner-approved parallel lane EP, acceptance mapping, EP staleness/continuity, calculated progress, execution/material authority, projection generation/readiness consistency, drift receipts, serial/fork/join/replan baton linkage, Owner-decision semantics, phase-transition Q1-Q5, issue graph/tree/closure/supersession lineage, and roadmap transactions.

Checkpoint validation binds executable PASS/FAIL/NOT_RUN evidence to the checkpoint's exact `execution_basis.material_ref`; evidence from another material head cannot silently qualify the current checkpoint.

Focused validators remain independently callable for diagnosis. `stress_test_relay.py` is read-only and repository-agnostic; real repositories are validation targets only.

PyYAML is required. Procedural semantic/cross-object validators are the enforcement layer today. Declarative schemas and templates are contract aids; generated Markdown and GitHub Issues are projections, not authority sources.
