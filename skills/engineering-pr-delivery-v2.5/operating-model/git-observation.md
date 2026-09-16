# Live Git observation and base drift

An EP is generated against a concrete Git basis. Before material writes, the incoming agent must resolve the current execution route and verify the live checkout.

Every executable EP declares `git_basis`:
- expected branch;
- material reference that must remain an ancestor of current HEAD;
- base branch;
- base commit observed when the EP was prepared;
- `RECHECK_BEFORE_WRITE` drift policy;
- optional durable drift receipt.

`resolve_execution_route.py` selects the serial EP or exactly one Owner-approved parallel lane from the checked-out branch/worktree. Ambiguous or mismatched routing means no material execution.

`inspect_git_context.py` compares the live checkout with the EP basis. If the base commit has advanced, it reports changed paths and requires a `DRIFT_RECEIPT`; it does not automatically call the drift safe.

A drift receipt is `DISJOINT`, `OVERLAPPING`, or `UNKNOWN`. Only an explicitly reasoned `DISJOINT` receipt permits the existing EP to remain executable. `OVERLAPPING` or `UNKNOWN` requires roadmap/EP reconciliation. Commit distance alone never proves safety.
