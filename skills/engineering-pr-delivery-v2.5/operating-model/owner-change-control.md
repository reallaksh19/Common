# Owner change control

Owner decisions use Owner Decision Records (ODRs). An ODR captures the exact decision/source, decision kind, effects, impact class, affected roadmap nodes/EPs/issues, required reconciliation and application state.

Decision kinds are:

```text
INTENT_MUTATION        changes project/roadmap intent
DEFERRAL               leaves a named requirement pending for later work
AUTHORIZATION          grants a bounded authority explicitly described by the decision
DECLINE                rejects a proposal/change
NO_CHANGE_CONFIRMATION confirms that existing intent remains authoritative
```

A `DEFERRAL` is not technical satisfaction. It must retain `requirement_disposition: PENDING_NOT_SATISFIED`, name the pending items, and must not itself grant material-write authority. The relay may remain recoverable and may permit read-only reconciliation while those items are pending.

Typical impact classes include `LOCAL`, `EP`, `PHASE`, `ARCHITECTURE`, `PROGRAM`, `UX_CONCEPT`, `SCOPE`, and `ENGINEERING_AUTHORITY`.

An ODR is not complete merely because it exists. Reconcile roadmap revision, stale EPs, issue graph, progress basis, frontier, material authority and REPO_STATE as applicable. An `OWNER_INTENT_MUTATION` roadmap revision must reference an applied `INTENT_MUTATION` ODR; a deferral cannot be used as a substitute for a roadmap-intent mutation receipt. Agents may capture Owner intent accurately; they may not enlarge it.
