# Repository bootstrap

Every participating repository exposes one deterministic relay entrypoint: `agents/relay/REPO_STATE.yaml`.

Bootstrap sequence:
```text
1. Read REPO_STATE.yaml.
2. Read referenced OVERALL_ROADMAP.yaml/revision.
3. Validate current_position.
4. Compute/confirm executable frontier.
5. Read active EP.
6. Verify EP roadmap source/staleness.
7. Follow EP.repository_discovery.
8. Execute only authorized material scope.
```
Never bootstrap by searching for the newest handover, issue comment, chain directory, commit message or chat statement. REPO_STATE is a router, not history. If it points to a missing, stale, non-frontier or conflicting EP, material execution does not begin.