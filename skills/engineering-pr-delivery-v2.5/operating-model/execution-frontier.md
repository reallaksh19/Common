# Executable frontier

A work package is frontier-eligible when: state is `PLANNED` or `ACTIVE`; definition maturity is `DETAILED`; all `depends_on` nodes are `COMPLETE`; it is not superseded/cancelled; and no unresolved true stop makes it ineligible.

Under `SERIAL`, exactly one material work package is executable while non-terminal planned work remains. An active EP must point to that frontier/current-active work package and the current roadmap revision.

When work completes, recompute the frontier. Do not hand-pick the next task.