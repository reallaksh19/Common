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

`resolve_execution_route.py` selects the serial EP or exactly one approved parallel lane from the checked-out branch/worktree. `inspect_git_context.py` verifies the expected branch/material ancestry and compares the current base branch with the EP's observed base. If the base moved it returns `NEEDS_DRIFT_RECEIPT` plus changed paths; it never auto-classifies drift as safe.

Projection and drift diagnostics:

```bash
python validate_projection_convergence.py <repo-root>
python validate_drift_receipt.py <repo-root>
```

Safe initialization and migration helpers:

```bash
# Dry-run by default; add --apply only after reviewing planned files.
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root>
python bootstrap_relay.py <BOOTSTRAP_MANIFEST.yaml> <repo-root> --apply

# Read-only V2 evidence inventory and non-authoritative reconciliation worksheet.
python inventory_v2_relay.py <repo-root> --output <inventory.yaml>
python prepare_v2_migration.py <inventory.yaml> --output <reconciliation.yaml>
```

Aggregate relay conformance verifies repository lifecycle/routing, roadmap topology/frontier, self-contained serial EPs or every Owner-approved parallel lane EP, acceptance mapping, EP staleness, calculated progress, execution policy, independent status planes, projection/readiness consistency, drift receipts, checkpoint baton linkage, phase-transition Q1-Q5, issue graph/closure/supersession, and roadmap transactions.

`validate_parallel_plan.py` additionally checks Owner approval, ASCII topology, exact frontier-to-lane correspondence, unique branch/worktree routing, lane EP validity, write-domain isolation/exceptions, and integration dependencies.

Checkpoint validation binds executable PASS/FAIL/NOT_RUN evidence to the checkpoint's exact `execution_basis.material_ref`; evidence from another material head cannot silently qualify the current checkpoint.

Focused validators remain independently callable for diagnosis. `stress_test_relay.py` is read-only and repository-agnostic; real repositories are validation targets only.

PyYAML is required. Generated Markdown and GitHub Issues are projections, not authority sources.
