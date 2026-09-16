# Repository bootstrap

Every participating repository exposes one deterministic relay entrypoint: `agents/relay/REPO_STATE.yaml`.

Bootstrap sequence:
```text
1. Read REPO_STATE.yaml.
2. Read relay_state and execution_policy.
3. Read referenced OVERALL_ROADMAP.yaml/revision.
4. Validate current_position and compute the executable frontier.
5. Route by lifecycle:
   ACTIVE       -> read the one active serial EP.
   PARALLEL     -> read the Owner-approved parallel plan, then select a lane only from unambiguous branch/worktree routing.
   INITIALIZING -> execute no material work; follow the explicit initialization next action.
   IDLE         -> execute no material work; follow the explicit status next action.
   TERMINAL     -> no material work remains.
6. Verify EP/lane roadmap source, staleness, scope and checkpoint baton.
7. Follow the selected EP.repository_discovery when an EP exists.
8. Execute only authorized material scope.
```

Never bootstrap by searching for the newest handover, issue comment, chain directory, commit message or chat statement. `REPO_STATE.yaml` is a router, not history.

## Safe initialization

Use `scripts/bootstrap_relay.py <manifest> <repo-root>` in dry-run mode first. `--apply` writes a generic `INITIALIZING` scaffold only when no target relay files already exist. Bootstrap never fabricates an executable EP or guessed project progress. The Owner/architect must reconcile intent and promote a `DETAILED` roadmap work package before `relay_state` becomes `ACTIVE`.

If REPO_STATE points to missing/stale/conflicting serial work, a parallel plan does not exactly match the computed frontier, or lane routing is ambiguous, material execution does not begin.
