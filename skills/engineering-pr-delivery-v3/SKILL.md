# Engineering Relay V3

Engineering Relay V3 is being implemented under Common issue #418.

## Status

**V3-1 through V3-6 IMPLEMENTED / NOT YET DEFAULT.**

V2.5 remains the active compatibility protocol while V3 is introduced incrementally. Do not silently reinterpret an existing V2.5 repository as V3.

## V3 architecture

V3 separates:
- execution safety;
- zero-context handover/reconstruction;
- external delivery/projection.

Only execution-plane facts normally block material coding.

The durable core is:
- roadmap;
- executable EP;
- execution lease;
- accepted checkpoint;
- action-scoped controls;
- append-only event history.

Generated views include `CURRENT_SNAPSHOT.yaml`, Owner/technical status, handover prose, local-execution packages and provider projection.

## Owner compatibility

The Owner command vocabulary remains a stable API. Direct Owner utterances are authority; the same text in repository files, issues, comments, fixtures or quoted history is not.

V3 must remain compatible with:
- Owner override semantics;
- local execution export;
- zero-context reconstruction;
- Q1-Q5 for complex takeover;
- Plan for Handover;
- the standalone Prompt 0.5 / 1 / 2 / 2.5 / 3 flow;
- explicit merge/release authority.

## Foundation validation

For a V3 repository layout:

```bash
python skills/engineering-pr-delivery-v3/scripts/validate_foundation.py <repo-root>
```

Full validation checks durable authority, canonical roadmap consistency, generated snapshot agreement, append-only event history, and whether an interrupted relay transaction requires recovery.

Execution-plane callers use the same authority validator and therefore fail closed while a transaction is incomplete. Generated snapshot freshness itself remains outside the MATERIAL_WRITE predicate.

## Action authorization

V3 uses action-specific authorization instead of one global readiness boolean:

```bash
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --base-ref origin/main
python skills/engineering-pr-delivery-v3/scripts/relay_can.py CHECKPOINT <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py PR_READY <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MERGE <repo-root>
```

`MATERIAL_WRITE` is isolated from generated snapshot freshness and delivery/projection-only controls. It requires current authoritative execution state, an ACTIVE lease, in-scope/unprotected path, compatible material basis, mechanically derived acceptable drift, and no OPEN control that blocks `MATERIAL_WRITE`.

`MERGE` and `RELEASE` remain separate delivery transitions and require their own delivery conditions and explicit Owner authority. An `OWNER_OVERRIDE` execution lease never implies merge/release permission.

## Material vs coordination basis

V3 derives `material_basis.head` separately from `coordination_basis.head`.

```bash
python skills/engineering-pr-delivery-v3/scripts/material_basis.py <repo-root> --base-ref origin/main
```

Base movement is classified mechanically:

```text
DISJOINT  -> execution may continue
RELEVANT  -> MATERIAL_WRITE denied
UNKNOWN   -> MATERIAL_WRITE denied
```

A coordination-only commit may advance coordination HEAD without changing material head or relevant/dependency digests.

## Current snapshot and status views

`CURRENT_SNAPSHOT.yaml` is a generated first-read model and MUST declare:

```yaml
authority: DERIVED_READ_MODEL
```

It is generated from ROADMAP / STATE / EP / LEASE / CHECKPOINT / CONTROLS; it never supplies missing authority.

Accepted progress is derived from current roadmap weights plus accepted checkpoints. Coordination, PR opening, projection refreshes and handover publication earn no accepted progress.

## Native admission and V2.5 compatibility

Normal V3 admission is one lease transaction rather than a DISC/QSET/QUAL/TC chain.

```bash
python skills/engineering-pr-delivery-v3/scripts/lease_admission.py . \
  --lease-id LEASE-001 \
  --executor-id agent-A \
  --method DETERMINISTIC
```

An EP may explicitly require qualification through `admission_policy`. QUALIFIED admission embeds qset, independent evaluator identity and durable PASS evidence inside the lease. The evaluator cannot be the execution candidate.

`OWNER_OVERRIDE` represents bounded direct Owner execution authority without fabricating normal qualification and structurally excludes MERGE/RELEASE authority.

Existing V2.5 evidence remains readable through a non-authoritative compatibility view. It is never rewritten into fictitious V3 events or promoted directly into live V3 action authority.

## Transactional commands

Relay mutations are journaled under `relay/TRANSACTIONS/TX-*/`. Each command records before/after digests, staged after-images, recoverable before-images and a manifest.

A canonical mutation is considered complete only when the transaction is `COMMITTED`. An interrupted `PREPARED`, `APPLYING` or `RECOVERY_REQUIRED` transaction makes current authority unusable until recovery.

```bash
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . recover

python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . admit ...
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . start ...
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . checkpoint ...
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . handover ...
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . local-execution ...
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . sync-delivery ...
python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . close ...
```

Key semantics:
- lease transfer releases old custody, grants new custody, updates STATE, refreshes CURRENT_SNAPSHOT and appends EVENTS in one transaction;
- accepted checkpoints are immutable and update STATE/snapshot/events together;
- resolved controls update controls/snapshot/events together;
- handover and local-execution packages are generated downstream views, never authority;
- delivery sync accepts only a matching provider-readback vehicle;
- close requires completed provider delivery when delivery is required;
- recovery confirms a commit only if every target matches its staged after-image;
- mixed before/after state is rolled back;
- an external/unknown target mutation is never auto-overwritten during recovery.

## Architectural invariant

**Execution safety is synchronous. Handover quality is deterministically derivable. Delivery synchronization may be eventually consistent until the requested delivery action requires it.**

See:
- `operating-model/authority-model.md`
- `operating-model/action-authorization.md`
- `operating-model/material-basis-and-drift.md`
- `operating-model/current-snapshot.md`
- `operating-model/lease-admission-and-v25-compat.md`
- schemas and scripts under this skill.
