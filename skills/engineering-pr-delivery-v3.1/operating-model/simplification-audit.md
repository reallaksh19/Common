# V3.1 simplification audit — EP.438.5

This audit records the bounded deletion decision for Common#438. The optimization rule is not "delete anything derivable"; it is "remove machinery that broadens authority without protecting a distinct invariant, and retain machinery that owns a real boundary."

## Deleted: native `PARALLEL` execution lifecycle

**Decision:** remove.

Native V3.1 has one current execution route, one current lease, one custody epoch and one accepted-checkpoint pointer. It does not implement:

- multiple simultaneously authoritative leases for one execution state;
- per-writer custody epochs or independent fencing;
- conflict/merge semantics for concurrent material writers;
- parallel checkpoint acceptance/merge semantics.

Allowing `STATE.execution.lifecycle = PARALLEL` therefore advertised an authority state that Relay could not safely realize.

The deletion is intentionally limited to the **native execution lifecycle**:

- `state.schema.yaml` no longer accepts `PARALLEL`;
- `relay_can.py` treats only `ACTIVE` as live execution authority;
- `relay_tx.py` enforces custody epochs only for `ACTIVE` execution;
- `lease_liveness.py` renews only an `ACTIVE` current lease.

Historical/migration prose or legacy inventory classification may still use the ordinary word "parallel". That does not create native multi-writer execution authority.

## Retained: three-pass handover request representation

**Decision:** retain.

`THREE_PASS_REQUEST` is a derived invocation package for the standalone generator. It does not grant engineering authority and it deliberately requires the generator to fetch its current schema from `main`. Removing it would collapse an integration boundary, not merely delete duplicate state.

Safety boundary: generated request remains non-authoritative; action authority is revalidated at execution time.

## Retained: V2.5 migration / protocol-selection machinery

**Decision:** retain.

LEGACY/NATIVE normalization prevents V3.1 tooling version from being confused with authority identity, but it does not eliminate the need to migrate an actual V2.5 repository. The migration report, cutover controls and protocol selector preserve:

- legacy-source validation;
- explicit cutover readiness;
- fail-closed handling of dual authority trees;
- non-fabrication of historical V3 acceptance/events.

This machinery is compatibility/cutover authority, not ordinary V3.1 execution ceremony.

## Retained: generated projections and status views

**Decision:** retain as disposable read models.

Snapshot, task, improvement, handover, provider and local-execution projections serve distinct consumers. They remain safe because:

- durable authority is ROADMAP / EP / STATE / LEASE / CONTROLS / CHECKPOINT / EVENTS;
- generated artifacts can be deleted and reconstructed;
- synchronous authorization does not depend on generated freshness.

The preservation suite proves deletion of `relay/GENERATED/**` does not change safety decisions.

## Retained: adjacent validation at distinct boundaries

**Decision:** retain where the failure domain differs.

Schema validation, action authorization, transaction preconditions and checkpoint acceptance may inspect related facts, but they answer different questions:

- schema validation: is durable data structurally admissible?
- `relay.can`: is this action allowed now?
- transaction preconditions: is the mutation still based on the expected durable state?
- checkpoint acceptance: does accepted truth bind exact material/evidence?

A check is not duplicate merely because it reads the same fact. Removal requires proof that the downstream boundary cannot observe a different race/failure state.

## Previously simplified ceremony

The dogfooding programme already removed or automated caller-owned bookkeeping where durable lineage makes it derivable, including issue-rooted EP/LEASE/CP/TX/EVT/CHANGE/LOCAL allocation and several governed transition IDs.

## Stop condition

No further deletion is justified in EP.438.5 unless the preservation suite proves that the candidate has no unique compatibility, provider, invocation, transaction, evidence or user-facing boundary.

The final programme audit should therefore treat the remaining machinery as **retained with an explicit invariant**, not as unfinished deletion work.
