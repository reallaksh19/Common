# Engineering Relay V3.1

Engineering Relay V3.1 is a self-contained protocol line. Its implementation lives entirely under this directory and does not import, symlink, or resolve runtime/schema files through the V3 skill tree.

## Status

V3.1 is the current implementation/guideline over a stable native Relay core. It MUST NOT silently replace V2.5 authority, but an already-cut-over `V3 / ACTIVE` repository does **not** require another protocol migration merely to use current V3.1 tooling.

Supported native execution bases are:

```text
V3_1 / ACTIVE  -> native current selector
V3   / ACTIVE  -> compatible native core; current V3.1 tooling may operate without rewriting the selector
V2_5 / PREPARED or legacy-default -> legacy/staged semantics; live native mutations remain blocked until the existing cutover completes
```

Compatibility is read-time and prospective. Existing V3 roadmap/EP/checkpoint/control/event truth is not rewritten. V3.1-only state, such as custody epochs, is established naturally on the next relevant native transition. The repository's implementation-version label and exact Common commit are **not product acceptance criteria** by themselves.

The V3.1 delta focuses on relay continuity at actor boundaries: recipient-ready local execution, typed result return, graceful custody release, human-readable quantitative/value summaries, roadmap reconciliation, parent-issue lineage, and stale-runner fencing.

## V3.1 architecture

V3.1 separates:
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

V3.1 recognizes stable high-level Owner workflow intents through `scripts/owner_commands.py`. Phrase matching is tolerant to minor wording variations, but semantics are not weakened:

- **What next?** — read-only programme reconciliation. Reconstruct live parent/child issue reality and report the real next frontier; do not admit or execute it.
- **Proceed next** — reconcile first, then continue/admit the next task already justified by the programme/ROADMAP.
- **Proceed next complex task** — force a whole-task/programme re-anchor before selecting execution; do not promote a convenient patch, file, or stale EP into task identity.
- **Plan for handover** — full governed handover preparation: programme/roadmap reconciliation, handover context/docs, provider Handover issue synchronization/readback, publication, and standalone three-pass request preparation. Handover is not accepted until a successor actually accepts custody.
- **Stats?** — read-only detailed point-wise checklist against the governing parent issue, relevant sub-issues, current EP acceptance, pending/KI/offloads, material/evidence state and programme debt categories.
- **Prepare for local agent** — recipient-ready local execution packet with clone/checkout basis, exact HEAD, full bounded technical instructions, acceptance/evidence contract, prohibitions, and a governed provider sub-issue that the helper must update with its result/evidence. Relay custody remains with the originating owner.

The parser is side-effect free. Recognition never creates roadmap, lease, checkpoint, delivery, provider, or Owner authority; callers must execute the referenced governed operations.

V3.1 preserves the copied baseline semantics for:
- Owner override semantics;
- local execution export;
- zero-context reconstruction;
- Q1-Q5 for complex takeover;
- Plan for Handover;
- the standalone Prompt 0.5 / 1 / 2 / 2.5 / 3 flow;
- explicit merge/release authority.

## V3.1 delta boundaries

V3.1 adds value at transitions without redefining accepted engineering truth:

- local execution REQUESTs are recipient-ready and carry exact basis, bounded steps, stop/prohibition rules, and a typed return contract;
- local helper return does not transfer custody or automatically create a checkpoint;
- graceful unfinished lease release requires fresh handover context plus explicit roadmap and parent-issue reconciliation;
- quantitative status is rendered from existing TASK_SNAPSHOT/CURRENT_SNAPSHOT facts, while value-added claims come from IMPROVEMENT_VIEW;
- roadmap reconciliation mutates the existing ROADMAP transactionally; there is no second roadmap authority;
- parent-issue transfer/split/supersession/linkage remains provider-derived lineage, not execution authority.

See `operating-model/v31-delta.md`.

## Safety kernel vs coordination quality

Relay is supporting infrastructure, not the programme roadmap. Normal engineering should be blocked only by conditions that can corrupt or mis-authorize work:

- invalid durable authority / interrupted transaction;
- no valid current work identity or execution custody where required;
- stale custody epoch;
- write outside governed scope or into protected scope;
- relevant/unknown material drift at write/checkpoint boundaries;
- invalid checkpoint/material evidence;
- explicit Owner authority missing for merge/release or intent-bearing change.

The following are coordination-quality concerns and MUST NOT become ordinary `MATERIAL_WRITE` blockers merely because they are stale or absent:

- GitHub Relay/Handover projection freshness;
- parent summary freshness;
- provider readback not required by the requested action;
- implementation-version or Common commit drift;
- handover readiness when no handover is being attempted;
- successor qualification when no successor is being admitted;
- generated status/read-model freshness.

Repair or regenerate those at their natural boundary. Do not promote a tooling/enabler issue above the current programme roadmap frontier.

## Foundation validation

For a V3.1 repository layout:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/validate_foundation.py <repo-root>
```

Full validation checks durable authority, canonical roadmap consistency, generated snapshot agreement, append-only event history, and whether an interrupted relay transaction requires recovery.

Execution-plane callers use the same authority validator and therefore fail closed while a transaction is incomplete. Generated snapshot freshness itself remains outside the MATERIAL_WRITE predicate.

## Action authorization

V3.1 uses action-specific authorization instead of one global readiness boolean:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py CHECKPOINT <repo-root> --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py PR_READY <repo-root>
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MERGE <repo-root>
```

`MATERIAL_WRITE` is isolated from generated snapshot freshness and delivery/projection-only controls. It requires current authoritative execution state, an ACTIVE lease, in-scope/unprotected path, compatible material basis, mechanically derived acceptable drift, and no OPEN control that blocks `MATERIAL_WRITE`.

`CHECKPOINT` also re-evaluates live material basis/drift and is accepted only when the checkpoint material result and acceptance IDs match the current EP exactly. Handover/local-execution and PR coordination remain usable after execution custody is released when accepted checkpoint/delivery context exists; they are not artificially coupled to an ACTIVE lease.

`MERGE` and `RELEASE` remain separate delivery transitions and require their own delivery conditions and explicit Owner authority. An `OWNER_OVERRIDE` execution lease never implies merge/release permission.

## Material vs coordination basis

V3.1 derives `material_basis.head` separately from `coordination_basis.head`.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/material_basis.py <repo-root> --base-ref origin/main
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

Programme progress is derived from authoritative ROADMAP work-package states and weights. Accepted evidence coverage is derived separately from accepted checkpoints. A migrated or historical ROADMAP-complete work package is not reopened merely because its native checkpoint was not replayed into the current protocol tree. Coordination, PR opening, projection refreshes and handover publication earn neither programme completion nor accepted evidence coverage.

## Native admission and V2.5 compatibility

Normal V3 admission is one lease transaction rather than a DISC/QSET/QUAL/TC chain.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/lease_admission.py . \
  --lease-id LEASE-001 \
  --executor-id agent-A \
  --method DETERMINISTIC
```

An EP may explicitly require qualification through `admission_policy`. QUALIFIED admission embeds qset, independent evaluator identity and durable PASS evidence inside the lease. The evaluator cannot be the execution candidate.

`OWNER_OVERRIDE` represents bounded direct Owner execution authority without fabricating normal qualification and structurally excludes MERGE/RELEASE authority.

Existing V2.5 evidence remains readable through a non-authoritative compatibility view. It is never rewritten into fictitious V3.1 events or promoted directly into live V3.1 action authority.

## Transactional commands

Relay mutations are journaled under `relay/TRANSACTIONS/TX-*/`. Each command records before/after digests, staged after-images, recoverable before-images and a manifest.

A canonical mutation is considered complete only when the transaction is `COMMITTED`. An interrupted `PREPARED`, `APPLYING` or `RECOVERY_REQUIRED` transaction makes current authority unusable until recovery.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . recover

python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . admit-task --tx-id TX-... --event-id EVT-... --actor ... --admission task-admission.yaml --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . start ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . checkpoint ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . handover ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . local-execution ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . sync-delivery ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . close ...
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
python skills/engineering-pr-delivery-v3.1/scripts/plan_handover.py . \
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

V3.1 migration is non-destructive. The original `agents/relay/**` tree is inventoried and hashed before V3.1 authority is created.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/v25_migration.py <repo-root> report

python skills/engineering-pr-delivery-v3.1/scripts/v25_migration.py <repo-root> bootstrap \
  --tx-id TX-MIGRATE-001 \
  --event-id EVT-MIGRATE-001 \
  --actor migration-agent \
  --owner-outcome "<explicit Owner outcome>" \
  --current-goal "<explicit current goal>"
```

Bootstrap creates only present-day V3 `INITIALIZING` authority, a generated migration report, one migration-reconciliation control, and a prepared protocol selector. It does **not** translate legacy DISC/QSET/QUAL/TC/checkpoint/projection objects into fictitious V3.1 events or native acceptance.

Protocol selection is resolved mechanically:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/protocol_default.py <repo-root>
```

Semantics:
- authority identity is `LEGACY` vs `NATIVE`; `V2_5` / `V3` / `V3_1` are compatibility/tooling metadata, not programme state;
- no selector + only `agents/relay/REPO_STATE.yaml` → `LEGACY / LEGACY_DEFAULT`;
- no selector + only `relay/STATE.yaml` → `NATIVE / ACTIVE` using current V3.1-compatible tooling without a migration ceremony;
- no selector + both durable authority trees → `INVALID`; fail closed rather than guess;
- `V2_5 / PREPARED` → LEGACY remains live while native authority is staged;
- `V3 / ACTIVE` or `V3_1 / ACTIVE` → NATIVE is live; accepted history is not rewritten merely to consume current tooling;
- invalid selection/history digest → fail closed.

Before cutover:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/protocol_cutover.py <repo-root> assess
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
python skills/engineering-pr-delivery-v3.1/scripts/protocol_cutover.py <repo-root> activate \
  --tx-id TX-CUTOVER-001 \
  --event-id EVT-CUTOVER-001 \
  --actor owner \
  --owner-utterance-digest sha256:<digest-of-current-direct-owner-cutover-utterance> \
  --owner-session-timestamp <RFC3339-time>
```

After V3.1 activation, the preserved V2.5 tree is bound by its cutover digest. Any change under `agents/relay/**` makes protocol-selection validation fail until explicitly reconciled.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/protocol_cutover.py <repo-root> validate
```

See `operating-model/v25-migration-and-cutover.md`.

## Architectural invariant


**Execution safety is synchronous. Handover quality is deterministically derivable. Delivery synchronization may be eventually consistent until the requested delivery action requires it.**

Optimisation is governed by the architecture preservation contract. Generated/read-model machinery may be removed, merged or regenerated only when destructive reconstruction and safety-decision tests continue to prove the durable programme/authority/acceptance/history kernel.

See:
- `operating-model/architecture-preservation-contract.md`
- `operating-model/authority-model.md`
- `operating-model/action-authorization.md`
- `operating-model/material-basis-and-drift.md`
- `operating-model/current-snapshot.md`
- `operating-model/lease-admission-and-v25-compat.md`
- schemas and scripts under this skill.

## Task intelligence and #421 continuity

V3 keeps engineering truth authoritative exactly once. These are **generated read models**, never execution or acceptance authority:

- `relay-v3.1-task-snapshot` — task-local purpose, lineage, scope, inputs/benchmarks, evidence, controls, negative knowledge and next action.
- `relay-v3.1-improvement-view` — evidence-bound capability/evidence/understanding/downstream change between task basis and accepted checkpoint.
- `relay-v3.1-intelligence-continuity` — cutover proof that V2.5 roadmap admission, ROADMAP_EVENTS, checkpoint/progress, discovery, Owner-delta and handover intelligence remain represented without changing the preserved legacy tree.

Generate or inspect them with:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/intelligence_projection.py <repo-root> task --base-ref origin/main --output relay/GENERATED/tasks/<EP>.snapshot.yaml
python skills/engineering-pr-delivery-v3.1/scripts/intelligence_projection.py <repo-root> improvement --output relay/GENERATED/improvements/<CP>.improvement.yaml
python skills/engineering-pr-delivery-v3.1/scripts/intelligence_projection.py <repo-root> continuity --base-ref origin/main \
  --task-output relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-output relay/GENERATED/improvements/<CP>.improvement.yaml \
  --output relay/GENERATED/INTELLIGENCE_CONTINUITY.yaml
```

While the selector is `V2_5 / PREPARED`, these projections derive from live V2.5 authority. After `V3_1 / ACTIVE`, they derive from native V3.1 authority. Merely creating the files never changes protocol selection, custody, acceptance, roadmap authority or progress.

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

A migrated repository in `V2_5 / PREPARED` may use staged V3.1 for migration, continuity projection and handover preparation, but live V3.1 execution/delivery actions fail with `PROTOCOL_NOT_ACTIVE`. After `V3_1 / ACTIVE`, V2.5 is read-only history and current task snapshots derive from native V3 truth.


### Canonical task admission

New work from an `IDLE` V3.1 repository must enter through `relay_tx.py admit-task`. The transaction atomically applies the governed roadmap disposition, creates the EP, grants the first lease, moves STATE to ACTIVE, appends OWNER_TASK_ADMITTED / EP_CREATED / LEASE_GRANTED events, and regenerates CURRENT_SNAPSHOT.

The generic transaction layer enforces semantic target constraints for critical commands. In particular, `ACTIVATE_LEASE` cannot create or rewrite roadmap/EP authority, and `RESOLVE_CONTROL` cannot rewrite protocol selection or migration reports. This prevents an atomically journaled transaction from masquerading as a different authority transition.


### Legacy cutover freeze

Do not rewrite the bootstrap V2.5 migration digest when legacy authority legitimately changes during `V2_5 / PREPARED`. Before cutover, run `protocol_cutover.py freeze` to bind the final live V2.5 tree. Continuity and post-cutover immutability are checked against that explicit freeze digest; the bootstrap digest remains historical migration evidence.


## Parent issue / Handover ledger synchronization

A governed parent issue SHOULD have exactly one dedicated `[Relay Handover]` child/sub-issue. The parent remains the compact goal/acceptance summary; the Handover issue is the generated operational ledger.

Generate the provider projections with:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/handover_ledger_projection.py . \
  --parent-observation parent-issue.yaml \
  --base-ref origin/main \
  --output relay/GENERATED/HANDOVER_LEDGER.yaml \
  --ledger-markdown relay/GENERATED/HANDOVER_LEDGER.md \
  --parent-summary relay/GENERATED/PARENT_RELAY_SUMMARY.md
```

The Handover ledger reuses existing V3.1 truth rather than creating duplicate authority:

- EP/checkpoint/lease state -> EP index and current frontier;
- tracked controls -> pending items and known issues;
- EP `offloads` -> local/helper work;
- CURRENT snapshot -> delivery/PR state;
- EVENTS -> handover/recovery chronology.

If a historical EP has no accepted completion checkpoint and its lease is RELEASED/REVOKED/INVALIDATED, the ledger exposes it as `RECOVERY_REQUIRED`. No final message from the previous agent is required for this projection.

Responsibility is explicit:

- **Owner decides** intent-bearing goal/scope/priority changes.
- **Active agent discovers and produces canonical evidence**.
- **Relay records, projects, synchronizes, and reads provider state back**.
- **Local/helper agents return bounded evidence only**.
- **Prompt 0.5/1/2/2.5 reason/propose; Prompt 3 executes only already-authorized reconciliation**.

Parent issue changes use the existing disposition vocabulary. Status-only truth may be synchronized by Relay. Intent-bearing UPDATE/TRANSFER/SPLIT/SUPERSEDE/CLOSE changes require Owner authority when they alter governing intent. Transfers preserve old/new issue lineage and each target parent has its own Handover ledger.

See `operating-model/parent-handover-ledger.md`.


## Custody fencing, recovery, and accepted handover

New V3.1 custody is fenced by a monotonic `custody_epoch`. Once an active STATE carries an epoch, every state-changing execution action MUST present the current expected epoch. Missing or stale epochs fail closed. A recovery takeover increments the epoch, so a predecessor that later returns cannot mutate the work using stale custody.

Leases carry `granted_at`, `renewed_at`, `recovery_after_seconds`, and a recovery policy. V3.1 does not run a polling daemon. Recovery eligibility is evaluated on demand when a different executor attempts explicit recovery. `TAKEOVER_AFTER_EXPIRY` permits recovery only after the persisted horizon; `MANUAL_ONLY` does not infer abandonment from time.

The active runner may renew custody transactionally:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . renew-lease \
  --tx-id TX-... --event-id EVT-... --actor agent-A \
  --expected-custody-epoch 7 --base-ref origin/main
```

Clean responsibility transfer is two-sided. `HANDOVER_PLANNED/HANDOVER_PUBLISHED` prepare and expose the frozen continuation basis; they do not themselves prove that another runner accepted responsibility. When the successor validates that fresh basis and activates its lease, the same custody transaction emits `HANDOVER_ACCEPTED` and advances the epoch. Until then the derived Relay ledger may show `HANDOFF_PENDING`.

Recovery is semantically distinct. An expiry-eligible explicit takeover emits `RECOVERY_STARTED`, invalidates predecessor custody, preserves the same EP where the work identity is unchanged, advances the epoch, and grants successor custody. After the successor reconstructs unaccepted material/evidence it records `RECOVERY_RECONSTRUCTED` with durable evidence. Do not represent recovery as a successful predecessor handover.

Legacy V3.1 repositories without epoch/liveness fields remain readable. Explicit recovery remains available for such legacy custody, but newly issued leases use fenced custody.

## Governed continuous improvement / Change Delta

Prompt 1 reasoning is not roadmap authority. Continuous improvement uses one governed `CHANGE-*` object:

```text
Prompt 1 / Owner
  -> CHANGE_HYPOTHESIS_RECORDED
Prompt 2
  -> CHANGE_VERIFIED or CHANGE_REJECTED
Prompt 2.5
  -> CHANGE_DELTA_PROPOSED
required authority
  -> CHANGE_AUTHORIZED
Relay / Prompt 3
  -> ROADMAP_RECONCILED + Change Delta APPLIED
```

Use the transactional commands `record-change`, `verify-change`, `propose-change`, and `authorize-change`. A confirmed proposal that requires Owner authority cannot be applied until direct Owner basis is recorded. `reconcile-roadmap --change-delta ...` validates the expected roadmap revision and STATE digest and atomically records the roadmap result in the Change Delta. Rejected hypotheses remain historical learning rather than silently disappearing.

Do not create a new GitHub issue merely because Prompt 1 generated a hypothesis. A new issue is justified only when authorized reconciliation establishes an independently governable obligation (for example SPLIT/TRANSFER).

## Relay issue materialization

The existing Handover ledger is the single derived Relay Envelope; do not create a parallel work/change/handover token.

Provider sync ensures one active Relay case-file sub-issue per governed parent. If the projected Relay issue is absent, sync reads the parent's sub-issues, reuses the one matching the deterministic Relay marker/title, or creates and attaches one when none exists. More than one matching Relay sub-issue is a fail-closed `MULTIPLE_RELAY_ISSUES` condition.

The generated Relay envelope exposes the current frontier/custody epoch, accepted checkpoint/head versus working head, pending/KI/offloads, negative knowledge, accountability, active Change Delta, delivery state, history, exact next action, and stop conditions. GitHub remains a provider projection; repository authority and events remain reconstructable truth.

## V3.1 communication boundary

V3.1 distinguishes three outward communication modes:

- **STATUS** — report what is true.
- **REQUEST** — another actor is expected to perform bounded work.
- **HANDOVER** — continuation responsibility is being released or transferred.

A REQUEST MUST NOT be satisfied with status prose alone. When another actor is expected to act, emit a recipient-ready action contract containing purpose, exact basis, bounded steps, success conditions, stop conditions, prohibited actions, and the required return contract.

LOCAL_EXECUTION_EXPORT materializes both relay/GENERATED/LOCAL_EXECUTION.yaml and relay/GENERATED/LOCAL_EXECUTION.md.

The Markdown artifact is the minimum runnable packet to present to the recipient in the same interaction. A pointer to an earlier issue/PR comment is not a substitute for the runnable packet.

The `relay_tx.py local-execution` command prints the committed Markdown packet immediately after the transaction result so the caller cannot mistake a successful export for completion of the communication step. When exact commands are already known, pass every one with repeated `--command`; do not downgrade known executable steps into generic prose.

A bounded local helper does not inherit task custody. LOCAL_EXECUTION_RETURNED records returned external execution evidence; the originating owner resumes responsibility and decides how that evidence affects checkpoint, controls, roadmap, or delivery.

## Graceful custody release

A normal unfinished RELEASE_LEASE uses reason HANDOFF and MUST be backed by a fresh, committed HANDOVER_CONTEXT / HANDOVER_PLANNED basis matching the current STATE, EP, lease, and material reality.

Administrative recovery may use reason ADMINISTRATIVE; this is explicitly non-graceful and MUST NOT be represented as a successful handover.

Accepted checkpoint semantics are unchanged. V3.1 does not create or weaken a checkpoint merely to permit retirement.
