# Engineering Relay V3

Engineering Relay V3 is being implemented under Common issue #418.

## Status

**V3-1 through V3-4 IMPLEMENTED / NOT YET DEFAULT.**

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

Generated views include `CURRENT_SNAPSHOT.yaml`, Owner/technical status, handover prose and provider projection.

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

Full foundation validation checks durable authority, canonical roadmap consistency, generated snapshot agreement, and append-only event history.

Execution-plane callers that must not depend on derived-view/history freshness use:

```bash
python skills/engineering-pr-delivery-v3/scripts/validate_foundation.py <repo-root> --authority-only
```

Generated snapshot disagreement remains a full-conformance failure; the snapshot never overrides authority.

## Action authorization

V3 uses action-specific authorization instead of one global readiness boolean:

```bash
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --base-ref origin/main
python skills/engineering-pr-delivery-v3/scripts/relay_can.py CHECKPOINT <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py PR_READY <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MERGE <repo-root>
```

`MATERIAL_WRITE` is intentionally isolated from generated snapshot freshness and delivery/projection-only controls. It requires current authoritative execution state, an ACTIVE lease, in-scope/unprotected path, compatible material basis, mechanically derived acceptable drift, and no OPEN control that blocks `MATERIAL_WRITE`.

`MERGE` and `RELEASE` remain separate delivery transitions and require an accepted checkpoint, clear required quality, a declared delivery vehicle, and explicit Owner delivery authority. An `OWNER_OVERRIDE` execution lease never implies merge/release permission.

## Material vs coordination basis

V3 derives:

```text
material_basis.head
coordination_basis.head
```

rather than binding engineering evidence to generic Git HEAD.

```bash
python skills/engineering-pr-delivery-v3/scripts/material_basis.py <repo-root> --base-ref origin/main
```

The material sensitivity set is derived from EP write/read/protected paths, semantic dependencies, and path-shaped acceptance dependencies.

Base movement is classified mechanically:

```text
DISJOINT  -> execution may continue
RELEVANT  -> MATERIAL_WRITE denied
UNKNOWN   -> MATERIAL_WRITE denied
```

A coordination-only commit may advance `coordination_basis.head` without changing `material_basis.head` or relevant/dependency digests.

## Current snapshot and status views

`CURRENT_SNAPSHOT.yaml` is a generated first-read model and MUST declare:

```yaml
authority: DERIVED_READ_MODEL
```

It is generated from ROADMAP / STATE / EP / LEASE / CHECKPOINT / CONTROLS; it never supplies missing authority.

For active execution:

```bash
python skills/engineering-pr-delivery-v3/scripts/generate_snapshot.py <repo-root> --base-ref origin/main --apply
```

Accepted progress is derived from current roadmap weights plus accepted checkpoints. Coordination, PR opening, projection refreshes and handover publication earn no accepted progress.

Owner and technical status are downstream views of the generated snapshot:

```bash
python skills/engineering-pr-delivery-v3/scripts/render_owner_status.py relay/GENERATED/CURRENT_SNAPSHOT.yaml
python skills/engineering-pr-delivery-v3/scripts/render_technical_status.py relay/GENERATED/CURRENT_SNAPSHOT.yaml
```

See:
- `operating-model/authority-model.md`
- `operating-model/action-authorization.md`
- `operating-model/material-basis-and-drift.md`
- `operating-model/current-snapshot.md`
- schemas under `schemas/`.
