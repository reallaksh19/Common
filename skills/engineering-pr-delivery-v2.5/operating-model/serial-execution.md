# Serial execution and controlled parallelism

Default material execution mode is `SERIAL`. Read-only discovery may be broad, but no agent starts another material stream merely because it appears independent.

## Serial

`relay_state: ACTIVE` + `execution_policy.mode: SERIAL` means exactly one computed frontier work package and one active EP. `INITIALIZING`, `IDLE`, and `TERMINAL` are also serial control states but expose no active EP and require an empty executable frontier.

## Owner-approved parallel

Parallelism requires `relay_state: PARALLEL`, `execution_policy.mode: OWNER_APPROVED_PARALLEL`, an Owner-approved plan ID, and ASCII topology shown before approval. `REPO_STATE.active_ep` becomes a router (`state: ROUTER`, no EP path); lane EPs live only in the approved parallel plan.

The plan must declare:
- every current frontier work package exactly once;
- a unique lane ID, EP ID/path, branch and optional worktree per lane;
- exclusive write domains and shared read domains;
- any shared-write exception with the exact lane pair, domain, reason, and explicit Owner approval;
- integration owner/work package, with roadmap dependencies on every lane;
- collision/integration risks and explicit stop conditions.

Each lane EP must independently satisfy the normal self-contained EP and acceptance-mapping rules and must bind to the same roadmap revision/frontier. A replacement agent selects a material lane only when the checked-out branch/worktree maps unambiguously to that lane. Ambiguity means no material execution.

The integration work package is not executable while lanes are active. Its EP is created only when lane completion causes that integration work package to become the recomputed frontier (`creation_policy: WHEN_FRONTIER`).
