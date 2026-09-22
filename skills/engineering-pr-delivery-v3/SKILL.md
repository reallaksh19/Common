# Engineering Relay V3

Engineering Relay V3 is being implemented under Common issue #418.

## Status

**V3-1 through V3-8 core implementation is present. DEFAULT CUTOVER IS GATED BY #421 INTELLIGENCE-CONTINUITY EVIDENCE.**

Repositories with no explicit protocol selection remain on V2.5 compatibility behavior. Do not silently reinterpret an existing V2.5 repository as V3.

A repository becomes V3-default only after its own `relay/PROTOCOL_SELECTION.yaml` is transactionally activated with passing cutover readiness, direct Owner cutover basis, and resolved `CTRL-V25-INTELLIGENCE-CONTINUITY` evidence proving the #421 roadmap/event/checkpoint/progress semantics are not being retired.

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
python skills/engineering-pr-delivery-v3/scripts/relay_can.py CHECKPOINT <repo-root> --base-ref origin/main
python skills/engineering-pr-delivery-v3/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py PR_READY <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MERGE <repo-root>
```

`MATERIAL_WRITE` is isolated from generated snapshot freshness and delivery/projection-only controls. It requires current authoritative execution state, an ACTIVE lease, in-scope/unprotected path, compatible material basis, mechanically derived acceptable drift, and no OPEN control that blocks `MATERIAL_WRITE`.

`CHECKPOINT` also re-evaluates live material basis/drift and is accepted only when the checkpoint material result and acceptance IDs match the current EP exactly. Handover/local-execution and PR coordination remain usable after execution custody is released when accepted checkpoint/delivery context exists; they are not artificially coupled to an ACTIVE lease.

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

python skills/engineering-pr-delivery-v3/scripts/relay_tx.py . admit-task --tx-id TX-... --event-id EVT-... --actor ... --admission task-admission.yaml --base-ref origin/main
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

## Plan for Handover / three-pass integration

V3 does not redefine the standalone three-pass protocol. It freezes relay truth into:

```text
relay/GENERATED/HANDOVER_CONTEXT.yaml
relay/GENERATED/THREE_PASS_REQUEST.yaml
relay/GENERATED/THREE_PASS_REQUEST.md
```

Generation requires an action-authorized HANDOVER and a normalized provider-readback target.

```bash
python skills/engineering-pr-delivery-v3/scripts/plan_handover.py . \
  --tx-id TX-HANDOVER-001 \
  --event-id EVT-HANDOVER-001 \
  --actor agent-A \
  --target-observation provider-target.yaml \
  --base-ref origin/main \
  --complex
```

The context is structurally partitioned:
- `blind_context` — programme/local responsibility and stable constraints for Prompt 0.5 / Prompt 1;
- `reality_context` — active execution/material/control/delivery truth reserved for Prompt 2 onward;
- `accumulated_learning` — accepted checkpoint history/learning, not action authority.

The request points to the canonical standalone launcher/schema/validator and requires a fresh current-`main` schema fetch at actual prompt-generation time. It never caches or reproduces the five-prompt schema. Complex mode preserves visible Q1–Q5 in Prompt 1 exactly as required by the live standalone schema.

A failed/unverified handover plan can deny HANDOVER but does not itself deny MATERIAL_WRITE.

See `operating-model/three-pass-integration.md`. The richer handover-content redesign tracked separately in Common issue #420 remains separately owned.

## V2.5 migration and protocol cutover

V3 migration is non-destructive. The original `agents/relay/**` tree is inventoried and hashed before V3 authority is created.

```bash
python skills/engineering-pr-delivery-v3/scripts/v25_migration.py <repo-root> report

python skills/engineering-pr-delivery-v3/scripts/v25_migration.py <repo-root> bootstrap \
  --tx-id TX-MIGRATE-001 \
  --event-id EVT-MIGRATE-001 \
  --actor migration-agent \
  --owner-outcome "<explicit Owner outcome>" \
  --current-goal "<explicit current goal>"
```

Bootstrap creates only present-day V3 `INITIALIZING` authority, a generated migration report, one migration-reconciliation control, and a prepared protocol selector. It does **not** translate legacy DISC/QSET/QUAL/TC/checkpoint/projection objects into fictitious V3 events or native acceptance.

Protocol selection is resolved mechanically:

```bash
python skills/engineering-pr-delivery-v3/scripts/protocol_default.py <repo-root>
```

Semantics:
- no selector → V2.5 compatibility remains the default;
- `V2_5 / PREPARED` → V3 is staged, but V2.5 remains live;
- `V3 / ACTIVE` → V3 is the live/default relay; V2.5 becomes read-only history;
- invalid selection/history digest → fail closed; do not guess a protocol.

Before cutover:

```bash
python skills/engineering-pr-delivery-v3/scripts/protocol_cutover.py <repo-root> assess
```

Readiness requires:
- full V3 conformance;
- unchanged legacy-tree digest;
- source V2.5 REPO_STATE validation PASS;
- migration reconciliation control RESOLVED;
- native lifecycle in `ACTIVE | IDLE | TERMINAL`;
- prepared V2.5-selected protocol state;
- #421 continuity evidence showing roadmap admission, ROADMAP_EVENTS, checkpoint/progress reconciliation, discovery, Owner-delta and handover intelligence remain governed across cutover.

Activation additionally requires direct Owner basis:

```bash
python skills/engineering-pr-delivery-v3/scripts/protocol_cutover.py <repo-root> activate \
  --tx-id TX-CUTOVER-001 \
  --event-id EVT-CUTOVER-001 \
  --actor owner \
  --owner-utterance-digest sha256:<digest-of-current-direct-owner-cutover-utterance> \
  --owner-session-timestamp <RFC3339-time>
```

After V3 activation, the preserved V2.5 tree is bound by its cutover digest. Any change under `agents/relay/**` makes protocol-selection validation fail until explicitly reconciled.

```bash
python skills/engineering-pr-delivery-v3/scripts/protocol_cutover.py <repo-root> validate
```

See `operating-model/v25-migration-and-cutover.md`.

## Architectural invariant


**Execution safety is synchronous. Handover quality is deterministically derivable. Delivery synchronization may be eventually consistent until the requested delivery action requires it.**

See:
- `operating-model/authority-model.md`
- `operating-model/action-authorization.md`
- `operating-model/material-basis-and-drift.md`
- `operating-model/current-snapshot.md`
- `operating-model/lease-admission-and-v25-compat.md`
- schemas and scripts under this skill.

## Task intelligence and #421 continuity

V3 keeps engineering truth authoritative exactly once. These are **generated read models**, never execution or acceptance authority:

- `relay-v3-task-snapshot` — task-local purpose, lineage, scope, inputs/benchmarks, evidence, controls, negative knowledge and next action.
- `relay-v3-improvement-view` — evidence-bound capability/evidence/understanding/downstream change between task basis and accepted checkpoint.
- `relay-v3-intelligence-continuity` — cutover proof that V2.5 roadmap admission, ROADMAP_EVENTS, checkpoint/progress, discovery, Owner-delta and handover intelligence remain represented without changing the preserved legacy tree.

Generate or inspect them with:

```bash
python skills/engineering-pr-delivery-v3/scripts/intelligence_projection.py <repo-root> task --base-ref origin/main --output relay/GENERATED/tasks/<EP>.snapshot.yaml
python skills/engineering-pr-delivery-v3/scripts/intelligence_projection.py <repo-root> improvement --output relay/GENERATED/improvements/<CP>.improvement.yaml
python skills/engineering-pr-delivery-v3/scripts/intelligence_projection.py <repo-root> continuity --base-ref origin/main \
  --task-output relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-output relay/GENERATED/improvements/<CP>.improvement.yaml \
  --output relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml
```

While the selector is `V2_5 / PREPARED`, these projections derive from live V2.5 authority. After `V3 / ACTIVE`, they derive from native V3 authority. Merely creating the files never changes protocol selection, custody, acceptance, roadmap authority or progress.

The continuity control may be resolved only after the generated continuity assessment is schema-valid and `ready: true`. `protocol_cutover.py assess` independently verifies that report and requires its legacy-tree digest to equal the migration inventory digest. A resolved control with prose alone is insufficient.

`plan_handover.py` atomically materializes the current TASK_SNAPSHOT and IMPROVEMENT_VIEW with HANDOVER_CONTEXT and binds their digests into accumulated learning. Prompt/handover consumers may use them for reconstruction and negative knowledge, but they grant no new action authority.


## Parent-issue-relative task snapshots

`TASK_SNAPSHOT` is an issue-relative execution read model rather than merely an EP dump. A provider-normalized parent issue observation can be supplied to the task/handover projector to expose:

- parent issue identity, current state, original baseline digest, and relevant issue/comment updates;
- a parent-issue acceptance checklist with COMPLETE / PARTIAL / PENDING / BLOCKED / DEFERRED / NOT_APPLICABLE / UNKNOWN states;
- a separate current-task checklist derived from EP acceptance and checkpoint evidence;
- planned local/third-party offloads declared by the EP;
- Owner-facing `PEND-*` and `KI-*` tracking IDs mapped to internal action-scoped `CTRL-*` controls;
- evidence-bound value-add entries compared with the frozen original issue baseline.

The parent-issue observation is provider-derived context and never grants write, checkpoint, merge, or release authority.

A migrated repository in `V2_5 / PREPARED` may use staged V3 for migration, continuity projection and handover preparation, but live V3 execution/delivery actions fail with `PROTOCOL_NOT_ACTIVE`. After `V3 / ACTIVE`, V2.5 is read-only history and current task snapshots derive from native V3 truth.


### Canonical task admission

New work from an `IDLE` V3 repository must enter through `relay_tx.py admit-task`. The transaction atomically applies the governed roadmap disposition, creates the EP, grants the first lease, moves STATE to ACTIVE, appends OWNER_TASK_ADMITTED / EP_CREATED / LEASE_GRANTED events, and regenerates CURRENT_SNAPSHOT.

The generic transaction layer enforces semantic target constraints for critical commands. In particular, `ACTIVATE_LEASE` cannot create or rewrite roadmap/EP authority, and `RESOLVE_CONTROL` cannot rewrite protocol selection or migration reports. This prevents an atomically journaled transaction from masquerading as a different authority transition.
