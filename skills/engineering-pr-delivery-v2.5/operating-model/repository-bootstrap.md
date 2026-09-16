# Repository bootstrap

Every participating repository exposes one deterministic relay entrypoint: `agents/relay/REPO_STATE.yaml`.

Bootstrap sequence:
```text
1. Read REPO_STATE.yaml.
2. Read relay_state and execution_policy.
3. Read referenced OVERALL_ROADMAP.yaml/revision.
4. Validate current_position and compute the executable frontier.
5. Route by lifecycle:
   ACTIVE       -> resolve the one active serial EP against the checked-out branch.
   PARALLEL     -> read the Owner-approved parallel plan and resolve exactly one lane from branch/worktree.
   INITIALIZING -> execute no material work; follow the explicit initialization next action.
   IDLE         -> execute no material work; follow the explicit status next action.
   TERMINAL     -> no material work remains.
6. For ACTIVE/PARALLEL run live Git observation:
   - expected branch must match;
   - EP material_ref remains ancestor of current HEAD;
   - live base branch is compared with EP base_observed_ref;
   - any base movement requires a durable drift receipt before writes.
7. Verify EP/lane roadmap source, staleness, scope and checkpoint baton.
8. Follow the selected EP.repository_discovery when an EP exists.
9. Execute only authorized material scope.
10. At custody transfer, reconcile any required external projection before claiming handover_ready.
```

Use `scripts/resolve_execution_route.py` and `scripts/inspect_git_context.py` for steps 5–6. Parallel ambiguity or branch mismatch means no material execution. Base drift is not automatically safe because it is small or relay-only; inspect it and record an explicit `DISJOINT` receipt or reconcile the EP.

Never bootstrap by searching for the newest handover, issue comment, chain directory, commit message or chat statement. `REPO_STATE.yaml` is a router, not history.

## Safe initialization

Use `scripts/bootstrap_relay.py <manifest> <repo-root>` in dry-run mode first. `--apply` writes a generic `INITIALIZING` scaffold only when no target relay files already exist. Bootstrap never fabricates an executable EP or guessed project progress. The Owner/architect must reconcile intent and promote a `DETAILED` roadmap work package before `relay_state` becomes `ACTIVE`.

If REPO_STATE points to missing/stale/conflicting serial work, a parallel plan does not exactly match the computed frontier, lane routing is ambiguous, live Git basis is unreconciled, or required projection synchronization is stale/pending at custody transfer, do not claim a fully ready handover.
