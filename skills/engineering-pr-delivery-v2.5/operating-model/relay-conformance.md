# Relay conformance

Question: if the current conversation disappears immediately, can a competent replacement agent recover the correct roadmap position, resolve the correct execution route from the live checkout, and continue safely without borrowing hidden chat context or stale evidence?

A conforming relay has:

- valid `REPO_STATE` lifecycle/routing and current roadmap revision;
- an unambiguous computed frontier;
- one valid serial EP or an Owner-approved parallel router whose lanes exactly cover that frontier;
- explicit EP inputs, scope, acceptance, tests, report contract and successor duties;
- an explicit Git execution basis (expected branch, material ref, observed base and recheck policy);
- no unresolved overlapping/unknown base drift; a preserved EP after base movement requires a durable `DISJOINT` drift receipt;
- checkpoint validation evidence bound to the exact material reference it observed;
- consistent deterministic progress and roadmap transactions;
- independent execution, quality, evidence and stop state;
- a consistent checkpoint → successor baton;
- required external projection state reconciled separately from repository recoverability;
- `relay_readiness.handover_ready` only when repository recovery and required projection convergence are both ready;
- no unauthorized parallel material work;
- durable discoveries/limitations and successor obligations.

`validate_relay_conformance.py` validates the repository-resident contract. It intentionally does not pretend static files can prove the operator's current Git checkout; before material writes, use `resolve_execution_route.py` and `inspect_git_context.py` to bind the live branch/worktree/HEAD/base state to the selected EP.

`cold_start_check.py` is stricter about context sufficiency: structural validity is insufficient if any material instruction still depends on hidden conversational context.

A green generic relay suite proves the reusable protocol checks execute successfully. It does not prove a particular downstream product, engineering calculation, release, or human UX acceptance.
