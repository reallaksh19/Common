# Migration blueprint

A migration must preserve durable truth while refusing to manufacture V2.5 certainty.

## Procedure

1. Run `inventory_v2_relay.py` against the repository. This inventories generic V2 relay artifacts only; it does not interpret them as current authority.
2. Run `prepare_v2_migration.py` to produce a `NEEDS_RECONCILIATION` worksheet.
3. Reconcile explicit Owner intent, roadmap topology, current position, unresolved work, inputs, benchmarks, decisions and evidence.
4. Establish a new V2.5 Progress Basis. Do not copy narrative V2 percentages.
5. Use `bootstrap_relay.py` only when creating a fresh V2.5 relay root. Bootstrap starts `INITIALIZING` with no executable EP.
6. Promote work to `DETAILED`, compute the frontier, and only then create the first genuine V2.5 EP.
7. Run full relay conformance and cold-start validation before declaring the migration executable.

A V2 endpoint may seed a checkpoint, history reference or context capsule, but is never automatically a valid V2.5 EP. V2 qualification/evidence remains historical evidence unless the new EP explicitly binds it under a current acceptance/verification contract.

Migration tooling is repository-neutral: it scans only protocol-defined V2 locations and never introduces downstream repository names, product semantics, issue-specific exceptions or inferred architecture.
