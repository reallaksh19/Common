# Engineering Relay V3.1

## Recorder-first semantics — normative

V3.1 is a durable **recording, continuity and reconstruction machine**. It does not decide whether engineering work may proceed.

This section is normative and supersedes older V3.1 wording that describes policy conditions as execution blockers.

Relay records, but does not gate:

- current EP/lease/executor and custody epoch;
- intended scope/protected paths;
- material drift and dependency drift;
- controls and unresolved warnings;
- programme/frontier observations;
- checkpoint PASS/FAIL and quality state;
- handover/recovery evidence;
- provider/delivery observations;
- Owner-authority observations.

For every recognized engineering action, `relay_can.py` returns `allowed: true`. Legacy reason codes remain as advisory diagnostics.

A successor may replace an existing executor immediately. Lease age, inactivity horizon, terminal-session evidence, stale epochs and changed unaccepted material are reconstruction evidence, not takeover prerequisites.

A checkpoint may be recorded with failing or partial evidence. Recording it does not magically make its claims true; projections may still distinguish evidence-backed completion from incomplete evidence.

The only remaining hard failures are **recorder-integrity failures**: malformed/schema-invalid records at a concrete write boundary, unsafe identifiers, immutable-ID overwrite, corrupt append-only history, or an atomic transaction that cannot be committed/recovered.

External systems may still reject actions for their own permissions or policies. Relay does not fabricate those permissions.


Engineering Relay V3.1 is a self-contained protocol line. Its implementation lives entirely under this directory and does not import, symlink, or resolve runtime/schema files through the V3 skill tree.

### Current protocol rule — V3.1 only

For current engineering coordination, recording, reconstruction, reporting, handover, local execution packaging, and Owner-command interpretation, **use V3.1 only**.

Do **not** use:

- `engineering-pr-delivery-v3`;
- `engineering-pr-delivery-v2.5`;
- V3/V2.5 gates, blockers, leases, custody rules, controls, recovery rules, checkpoint rules, status logic, or Owner-command semantics.

Older protocol trees are historical/compatibility material only. Their presence in the repository, tests, migration code, or legacy selectors does not make them current authority.

If V3.1 contains compatibility readers for legacy-shaped durable artifacts, those readers exist only so current V3.1 can reconstruct history. They are **not** a direction to execute the older protocol or to import its blocking semantics.

**Normative override:** any later section in this document that mentions V3, V2.5, `V3`, `V2_5`, legacy admission, protocol cutover, migration, compatibility, or historical authority is **archival/migration documentation only**. Current agents/coordinators must not use those passages as live execution, coordination, reporting, recovery, gating, or Owner-command instructions.

## GitHub programme source hierarchy — recorder/reconstruction input

For multi-agent programmes, V3.1 should interpret durable GitHub information using this source hierarchy:

```text
1. Parent programme issue
   = governing human/programme contract

2. Explicit Owner-authorized comments/amendments
   = durable semantic changes, transfers, decisions and evidence chronology

3. Dedicated [Relay Handover] child issue
   = current operational ledger / reconstruction index

4. Child implementation issues
   = bounded engineering responsibilities + revisable implementation plans

5. PRs / commits / tests / artifacts
   = actual material and exact-head evidence

6. V3.1
   = recorder / reconstruction / reporting mechanism
```

The provider-facing `[Relay Handover]` issue is an operational index, not execution authority. Its statements should point to durable material evidence where a production claim matters.

Missing/stale Handover content may reduce reconstruction quality but must never invalidate existing production work, revoke responsibility, block coding/PRs, or create authority.

When reconstructing a programme, preserve:

- current parent basis revision and effective amendment refs;
- all nonterminal PRs;
- implementation-plan refs/revisions when available;
- required production-output dependencies and independent work;
- producer→consumer handoffs;
- pending items / known issues;
- negative knowledge / do-not-reopen evidence;
- genuine Owner decisions;
- exact evidence for programme exit criteria.

V3.1 must not manufacture missing programme semantics from its own leases, checkpoints, controls, generated snapshots or historical protocol state.

## Agent implementation-plan and task-publication lifecycle — normative

For a bounded child implementation issue, the engineering agent owns the implementation plan.

Normal sequence:

```text
repository/application
→ PASS 1 independent system baseline
→ PASS 2 improvement/task reconciliation
→ Owner approval
→ IMPLEMENTATION_PLAN rev 1 on owned issue
→ EP/Task Snapshot/Handover binding
→ engineering execution
→ PLAN_UPDATE only when material learning changes the approach
→ TASK_EVIDENCE only for meaningful intermediate evidence
→ PR/test/artifact material truth
→ TASK_RESULT / handoff
→ [Relay Handover] indexes the current programme consequence
```

For two-pass work, the agent first shows the Owner its Improvement Proposal(s) and draft implementation plan in chat and stops for explicit approval. After approval and a fresh live revalidation, publish `IMPLEMENTATION_PLAN — rev 1` on the owned child issue before substantial material modification when practical. The durable comment should begin with that typed heading; Pass-1/Pass-2 reasoning or execution narrative is input/evidence, not a substitute for the durable plan.

The plan basis should record the owned child responsibility/provider ref and its observed body/contract digest when available, plus the live V3.1 protocol basis:

```text
PROTOCOL BASIS
V3.1
Common@<resolved current-main SHA>
<Two-Pass revision>
```

If the child responsibility later changes, V3.1 may project the prior plan as `STALE`; that is revalidation debt, not an execution block. If the live Common SHA changes, refresh/re-read the current protocol at the next semantic boundary and regenerate the issue-local Task Snapshot on the new basis; do not manufacture a plan revision unless the engineering approach itself changed.

That publication is a **reconstruction convention, not permission**:

- do not wait for Relay/coordinator approval after posting the plan;
- useful work performed before the plan was published remains valid;
- a missing/stale plan reduces reconstruction confidence only;
- plan revision does not require a new EP while the owned responsibility is unchanged.

The implementation plan should normally state:

- exact basis/head;
- understanding of the engineering problem;
- owned outcome and ownership boundary;
- source truth;
- approach;
- expected changed surfaces;
- dependencies and independent work;
- falsifier;
- validation;
- preserve/invariants;
- uncertainties;
- expected next observable;
- consumer/handoff contract.

### EP relationship

The EP is V3.1's bounded task identity, not a duplicate implementation plan.

One meaningful engineering responsibility should normally map to one EP. Do not create nano-EPs for individual file reads, edits, tests, comments or PR operations.

For the new programme topology:

- `programme_parent` identifies the governing programme issue when distinct;
- `parent_issue` identifies the owned child implementation issue;
- the current child-issue provider observation supplies the latest implementation-plan revision and meaningful task publications;
- `TASK_SNAPSHOT` and the Handover ledger expose that plan/expectation context.

An EP may exist before the incoming agent publishes its plan, for example when a handover/two-pass packet was prepared from existing V3.1 context. In that case bind the existing task to the newly observed plan; do not create a replacement EP merely because the plan appeared or changed.

### Meaningful provider publications

Use four durable publication types:

```text
IMPLEMENTATION_PLAN
PLAN_UPDATE
TASK_EVIDENCE
TASK_RESULT
```

Begin the durable comment with the typed publication heading so reconstruction does not have to infer semantic state changes from prose. A correction/narrowing that changes the intended material approach is a `PLAN_UPDATE`; final exact-main/integration acceptance is a `TASK_RESULT` when that is the owned responsibility.

Do not post every command, file read, test retry, timer wake or chat message.

The coordinator watches the plan's **expected next observable** and reasons:

```text
EXPECTED
→ OBSERVED
→ CONSEQUENCE
```

When one issue deliberately owns a stacked or multi-PR delivery, keep `delivery` as the primary/current PR and expose all owned/related PRs through `delivery_stack[]`. Do not flatten a stack into one PR or create one engineering responsibility per PR merely for reporting.

For pull-request CI, `scripts/validate_task_binding.py` can assert that an explicitly owned issue has a Task Snapshot containing the current PR at the exact head. With `--require-current-protocol-basis`, it also requires that snapshot to name the exact Common checkout and live Two-Pass revision executing the validator. This is a reporting/reconstruction integrity check, not engineering authorization.

See `operating-model/agent-task-publication.md`.


## RLL-1 execution transport — normative

V3.1 may use **RLL-1 (Relay Lease Loop v1)** to transport already-authorized work to a scheduled local engineering agent.

RLL-1 is below V3.1. It does not create product requirements, acceptance criteria, implementation authority, Owner approval, merge authority, release authority, or programme completion. Its operational labels/leases/comments are never engineering acceptance evidence.

Reference:

`operating-model/transports/RLL-1.md`

The reference transport intentionally requires no GitHub MCP server. It uses native `git`, GitHub CLI `gh` / `gh api`, a deterministic single-machine mutex/lease launcher, and Antigravity headless execution.

An RLL child is eligible only after the governing engineering contract/plan is already recoverable and an `RLL_EXECUTION_V1` envelope identifies either:

- `BRANCH_RESUME` for an owned implementation branch; or
- `EXACT_HEAD_EVIDENCE` for read-only exact-head execution/certification.

The transport labels are limited to:

```text
rll-ready
rll-active
rll-review-ready
rll-escalation
```

Do not infer PASS/FAIL/completion from those labels. Engineering result semantics remain the normal V3.1 evidence vocabulary.

Only structured `RELAY_DIRECTIVE_V1` comments from configured authorized identities are executable transport directives. Ordinary GitHub prose remains context only.

A scheduled/timer wake, mutex acquisition, lease renewal, routine edit/test progress, or transient retry does not warrant a V3.1 durable publication. The existing four publication types remain unchanged.

The transport must never merge, release, delete branches, close programme work, or use `agy --dangerously-skip-permissions`. Scoped local permissions are required for unattended execution.


## Owner reporting delta

V3.1 may keep a derived Owner-publication cursor solely to answer **what changed since the last Owner-visible report**.

Use:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/owner_publication.py \
  relay/GENERATED/CURRENT_SNAPSHOT.yaml \
  --task-snapshot relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-view relay/GENERATED/improvements/<CP>.improvement.yaml
```

After the status has actually been shown to the Owner, `--apply` may advance `relay/PUBLICATION/OWNER_STATUS.yaml`.

The cursor and delta classification are **reporting metadata only**. Missing/stale reporting state must never block production, and no authorization/admission/recovery/checkpoint/delivery path may consume the cursor as a gate.

See `operating-model/owner-reporting-delta.md`.

## Status

V3.1 is the **only current Relay implementation/guideline** for live engineering coordination and recording.

### Live protocol handshake

A consumer repository must not treat an old prompt, old checkout, pinned workflow SHA, legacy `AGENTS.md`, or prior task publication as proof that its agent is still on the current V3.1 contract.

At these semantic boundaries, resolve **current `reallaksh19/Common@main`**, establish the exact SHA with `scripts/live_protocol_basis.py`, and re-read the live V3.1 skill plus current Two-Pass schema before continuing:

- new agent/session start;
- resumed task after session loss or handover;
- before publishing `IMPLEMENTATION_PLAN`;
- before a material `PLAN_UPDATE`;
- before `TASK_RESULT`;
- before PR-ready, merge, handover/takeover, or coordinator dispatch based on prior state.

If the resolved Common SHA is unchanged from the agent's recorded basis, continue normally. If it changed, refresh the live contract and revalidate **only the pending action/plan assumption**; do not restart completed engineering work or invalidate material evidence merely because the recorder protocol changed.

The exact resolved SHA and Two-Pass revision should be recorded in the implementation-plan `PROTOCOL BASIS` and issue-local Task Snapshot. A protocol refresh is reconstruction/coordination work, not production permission.

Current agents and coordinators must not choose V3 or V2.5 as an execution/coordination basis, even when legacy-shaped artifacts or selectors remain readable for migration/reconstruction compatibility.

```text
CURRENT LIVE PROTOCOL
V3.1

NOT LIVE COORDINATION PROTOCOLS
V3
V2.5
```

A legacy selector, object shape, issue comment, test fixture, or historical record may be read by V3.1 when necessary to reconstruct history. That compatibility does not grant legacy protocol authority and must never reintroduce old gates or blockers.

The repository's implementation-version label and exact Common commit are not product acceptance criteria by themselves.

## V3.1 architecture

V3.1 separates:
- execution safety;
- zero-context handover/reconstruction;
- external delivery/projection.

V3.1 execution-plane facts are recorder/reconstruction observations. They do not block material coding; actual production constraints come from the engineering problem, source truth, tests/runtime evidence, human decisions, and real provider permissions.

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
- **Plan for handover** — full governed handover preparation: programme/roadmap reconciliation, handover context/docs, provider Handover issue synchronization/readback, publication, and standalone two-pass request preparation. Handover is not accepted until a successor actually accepts custody.
- **Stats?** — read-only detailed point-wise checklist against the governing parent issue, relevant sub-issues, current EP acceptance, pending/KI/offloads, material/evidence state and programme debt categories.
- **Prepare for local agent** — recipient-ready local execution packet with clone/checkout basis, exact HEAD, full bounded technical instructions, acceptance/evidence contract, prohibitions, and a governed provider sub-issue that the helper must update with its result/evidence. Relay custody remains with the originating owner.

The parser is side-effect free. Recognition never creates roadmap, lease, checkpoint, delivery, provider, or Owner authority; callers must execute the referenced governed operations.

V3.1 preserves the copied baseline semantics for:
- Owner override semantics;
- local execution export;
- zero-context reconstruction;
- Q1-Q5 for complex takeover;
- Plan for Handover;
- the standalone Pass 1 / Pass 2 flow with the Owner approval boundary inside Pass 2;
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

## Recorder integrity vs engineering policy

Relay must keep its ledger structurally trustworthy, but it must not turn coordination policy into an engineering stop condition.

Hard failures are limited to recorder integrity:

- unreadable/malformed durable objects needed for the concrete write;
- unsafe or duplicate immutable identities;
- corrupt append-only event history;
- impossible filesystem/provider write;
- interrupted transaction state that must be atomically recovered.

Everything else is advisory context, including:

- no active lease or stale custody epoch;
- out-of-scope/protected-path declarations;
- material drift;
- open controls;
- missing checkpoint/quality;
- programme selection uncertainty;
- handover freshness;
- delivery/provider state;
- Owner-delivery-authority observation.

Agents should respond to those diagnostics intelligently, but V3.1 itself does not block the work.

## Foundation validation

For a V3.1 repository layout:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/validate_foundation.py <repo-root>
```

Full validation checks durable authority, canonical roadmap consistency, generated snapshot agreement, append-only event history, and whether an interrupted relay transaction requires recovery.

Execution-plane callers use the same authority validator and therefore fail closed while a transaction is incomplete. Generated snapshot freshness itself remains outside the MATERIAL_WRITE predicate.

## Action diagnostics

The compatibility surface remains:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py CHECKPOINT <repo-root> --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MERGE <repo-root>
```

The result is diagnostic, not authorizing. For every recognized action:

```yaml
allowed: true
```

`basis`, legacy `blocking_controls`, and `reason_codes` explain the observed state. They are intended for reconstruction, review and human judgement, not execution denial.

Examples such as `DRIFT_RELEVANT`, `STALE_CUSTODY_EPOCH`, `CONTROL_BLOCKS_ACTION`, `CHECKPOINT_NOT_ACCEPTED`, and `OWNER_DELIVERY_AUTHORITY_REQUIRED` are advisories.

## Material vs coordination basis

V3.1 still derives `material_basis.head` separately from `coordination_basis.head` because that distinction is useful for reconstruction.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/material_basis.py <repo-root> --base-ref origin/main
```

Base movement is classified mechanically:

```text
DISJOINT  -> diagnostic
RELEVANT  -> diagnostic; revalidate what matters
UNKNOWN   -> diagnostic; current comparison is unavailable
```

No drift classification denies MATERIAL_WRITE or CHECKPOINT.

## Task Snapshot reporting contract — Owner-facing

A Task Snapshot must answer immediately:

```text
WHAT IS THIS TASK?
WHAT IS DONE?
HOW MUCH OF THE CHILD/WORK ISSUE IS ACCEPTED?
WHAT PROGRAMME CRITERIA DOES IT SATISFY?
WHAT REMAINS?
WHY IS IT REMAINING?
WHAT IS THE DELIVERY STATE?
WHAT HAPPENS NEXT?
DOES THE OWNER NEED TO DECIDE ANYTHING?
```

Keep these axes independent:

```text
programme progress
work/child issue acceptance
implementation-plan progress
current task/EP acceptance
verification
delivery/PR lifecycle
provider issue lifecycle
```

Never collapse them into a single ambiguous `DONE`.

State semantics preserve:

```text
PASS
PARTIAL
FAIL
NOT_RUN
PENDING
DEFERRED
NOT_APPLICABLE
UNKNOWN
```

and failure/wait origin:

```text
CURRENT_TASK
UPSTREAM_DEPENDENCY
SIBLING_WORKSTREAM
PREEXISTING_UNRELATED
INFRASTRUCTURE
PROVIDER
OWNER_DECISION
UNKNOWN
```

`FAIL` is not automatically a blocker. `NOT_RUN` is never a code failure.

Percentages are permitted only from an explicit acceptance or plan denominator. Prefer stable `EXIT-*`, `AC-*`, and `STEP-*` IDs. If no denominator exists, render `UNKNOWN / UNMAPPED` rather than inventing a percentage.

Owner-facing status should begin with:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/render_task_snapshot.py \
  relay/GENERATED/tasks/<EP>.snapshot.yaml
```

Finished examples are indexed in:

```text
skills/engineering-programme-coordinator/references/OUTPUT_EXAMPLE_INDEX.md
```

## Current snapshot and status views

`CURRENT_SNAPSHOT.yaml` is a generated first-read model and MUST declare:

```yaml
authority: DERIVED_READ_MODEL
```

It is generated from ROADMAP / STATE / EP / LEASE / CHECKPOINT / CONTROLS; it never supplies missing authority.

Programme progress is derived from authoritative ROADMAP work-package states and weights. Accepted evidence coverage is derived separately from accepted checkpoints. A migrated or historical ROADMAP-complete work package is not reopened merely because its native checkpoint was not replayed into the current protocol tree. Coordination, PR opening, projection refreshes and handover publication earn neither programme completion nor accepted evidence coverage.

Do not create a fourth "completion snapshot". Owner/task completion reporting is rendered on demand from the existing derived project/task/improvement views:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/render_owner_status.py \
  relay/GENERATED/CURRENT_SNAPSHOT.yaml \
  --task-snapshot relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-view relay/GENERATED/improvements/<CP>.improvement.yaml
```

That rendering remains `DERIVED_READ_MODEL` presentation. It must keep programme progress, accepted evidence coverage, task-local completion, blockers, evidence-bound improvement and legal next actions distinct.

## Historical native admission / V2.5 compatibility — archival only

Historical native admission used one lease transaction rather than a DISC/QSET/QUAL/TC chain. This is not a current instruction to use V3.

For a provider-backed EP, the transactional surface derives canonical issue-rooted `TX`, `EVT` and `LEASE` identities when they are omitted:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . start \
  --executor-id agent-A \
  --actor agent-A \
  --method DETERMINISTIC \
  --base-ref origin/main
```

`lease_admission.py` remains a low-level object builder and accepts an explicit lease ID when a caller needs to inspect a lease object without activating it.

An EP may still declare qualification intent through `admission_policy`, and QUALIFIED admission may embed qset/evaluator/evidence. In recorder-first V3.1 this is descriptive provenance only; missing qualification does not prevent a deterministic executor from being recorded.

`OWNER_OVERRIDE` remains a descriptive admission form. Relay records its bounded scope and Owner basis when supplied, but Relay does not use missing delivery authority as an execution gate.

Existing V2.5 evidence remains readable through a non-authoritative compatibility view. It is never rewritten into fictitious V3.1 events or promoted directly into live V3.1 action authority.

## Transactional commands

Relay mutations are journaled under `relay/TRANSACTIONS/` using legacy `TX-*` or canonical `TX.<root>.<serial>` identities.

While a transaction is `PREPARED`, `APPLYING`, or `RECOVERY_REQUIRED`, its journal retains staged after-images plus recoverable before-images because those bytes are still required for confirm-commit or rollback.

Once the transaction becomes `COMMITTED` or `ROLLED_BACK`, the recovery payload is disposable: the manifest is compacted to a digest-only receipt and the `staged/` and `backups/` directories are pruned. Before/after digests, target paths, actor, command, timestamps, applied targets, and recovery basis remain durable.

A canonical mutation is considered durably recorded only when the transaction is `COMMITTED`. Interrupted transaction state remains a recorder-integrity concern and should be recovered before trusting that specific mutation.

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . recover

# Provider-backed issue-scoped transitions allocate canonical IDs when omitted.
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . admit-task --actor ... --admission task-admission.yaml --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . start --executor-id ... --actor ... --method DETERMINISTIC --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . checkpoint --actor ... --checkpoint checkpoint.yaml --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . renew-lease --actor ... --expected-custody-epoch ... --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . release-lease --actor ... --reason ADMINISTRATIVE --expected-custody-epoch ...

# Mixed-scope/provider coordination commands still require the identifiers their
# governing scope cannot yet be inferred safely.
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . handover ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . local-execution ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . sync-delivery ...
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . close ...
```

Key semantics:
- canonical IDs record governing scope but never imply currentness, priority or relationship;
- issue-rooted allocation is automatic only when the governing issue is unambiguous; mixed/repository scope must remain explicit until its governing scope is typed;
- lease transfer releases old custody, grants new custody, updates STATE, refreshes CURRENT_SNAPSHOT and appends EVENTS in one transaction;
- checkpoint records are immutable and update STATE/snapshot/events together; PASS/FAIL remains evidence, not a write gate;
- resolved controls update controls/snapshot/events together;
- handover and local-execution packages are generated downstream views, never authority;
- delivery sync accepts only a matching provider-readback vehicle;
- close requires completed provider delivery when delivery is required;
- recovery confirms a commit only if every target matches its staged after-image;
- mixed before/after state is rolled back;
- an external/unknown target mutation is never auto-overwritten during recovery.

## Plan for Handover / two-pass integration

V3.1 binds current handover generation to the standalone two-pass protocol. Historical Three-Pass artifacts remain compatibility/history only.

```text
relay/GENERATED/HANDOVER_CONTEXT.yaml
relay/GENERATED/TWO_PASS_REQUEST.yaml
relay/GENERATED/TWO_PASS_REQUEST.md
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

The context remains structurally partitioned for reconstruction, but the generated prompt applies it differently:
- Pass 1 receives repository/system identity, broad human outcome and stable constraints, then independently inspects live system reality while the actual issue/task/action request stays quarantined.
- Pass 2 receives the Pass-1 baseline plus the actual target, reality context and accumulated learning, performs the high-ROI improvement scan, reconciles the issue, drafts the implementation plan, and stops for Owner approval.
- accumulated learning remains history/evidence, not action authority.

The request points to the canonical standalone launcher/schema/validator and requires a fresh current-`main` schema fetch at actual prompt-generation time. It never caches or reproduces the five-prompt schema. Complex mode preserves visible Q1–Q5 in Prompt 1 exactly as required by the live standalone schema.

A failed/unverified handover plan can deny HANDOVER but does not itself deny MATERIAL_WRITE.

See `operating-model/two-pass-integration.md`.

## Historical V2.5 migration / protocol cutover — archival only

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

`plan_handover.py` derives the current TASK_SNAPSHOT and IMPROVEMENT_VIEW on demand, freezes those exact read models **inside** HANDOVER_CONTEXT, and binds their digests into accumulated learning. It no longer persists separate handover-only task/improvement files that must remain synchronized with the context. The standalone intelligence projection CLI remains available when a human/tool explicitly wants those views as separate diagnostic artifacts. None of these projections grants new action authority.


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
- **Pass 1 understands without task/action bias; Pass 2 proposes/reconciles, pauses for Owner approval, then persists/executes only within approved authority**.

Parent issue changes use the existing disposition vocabulary. Status-only truth may be synchronized by Relay. Intent-bearing UPDATE/TRANSFER/SPLIT/SUPERSEDE/CLOSE changes require Owner authority when they alter governing intent. Transfers preserve old/new issue lineage and each target parent has its own Handover ledger.

See `operating-model/parent-handover-ledger.md`.


## Custody fencing, recovery, and accepted handover

New V3.1 custody is fenced by a monotonic `custody_epoch`. Once an active STATE carries an epoch, every state-changing execution action MUST present the current expected epoch. Missing or stale epochs fail closed. A recovery takeover increments the epoch, so a predecessor that later returns cannot mutate the work using stale custody.

Newly issued leases default to a **300-second inactivity horizon**. Relay does not require a polling daemon or a separate manual heartbeat loop. Meaningful governed activity performed by the current lease executor renews `custody.renewed_at` transactionally with that action. When a material basis is available, renewal also captures a non-authoritative `activity_basis` containing digests of the current sensitive worktree and semantic-dependency worktree.

This liveness basis is deliberately distinct from checkpoint/material authority:

- it may observe uncommitted sensitive work so recovery does not race an active writer;
- it never proves acceptance or changes programme progress;
- it never changes the custody epoch;
- ordinary commands may mutate only `renewed_at` and `activity_basis` on the current executor's ACTIVE lease; they cannot use liveness renewal to rewrite lease authority.

For `TAKEOVER_AFTER_EXPIRY`, explicit recovery after the inactivity horizon is allowed only when the sensitive worktree/dependency digests still match the predecessor's last activity basis. If sensitive material changed after the last recorded activity, timeout alone is insufficient and recovery fails with `UNACCEPTED_MATERIAL_ACTIVITY_PRESENT`.

A provider/session termination observation may establish stronger abandonment evidence before the timeout. `--recovery-observation` accepts a schema-validated observation bound to the exact predecessor lease, executor, custody epoch and observation time, with a terminal state of `TERMINATED`, `CANCELLED`, or `FAILED`. A stale, mismatched, or non-terminal observation cannot invalidate custody.

The explicit `renew-lease` command remains available for diagnostics/compatibility, but normal active runners should not need heartbeat ceremony:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_tx.py . renew-lease \
  --tx-id TX-... --event-id EVT-... --actor agent-A \
  --expected-custody-epoch 7 --base-ref origin/main
```

Clean responsibility transfer is two-sided. `HANDOVER_PLANNED/HANDOVER_PUBLISHED` prepare and expose the frozen continuation basis; they do not themselves prove that another runner accepted responsibility. When the successor validates that fresh basis and activates its lease, the same custody transaction emits `HANDOVER_ACCEPTED` and advances the epoch. Until then the derived Relay ledger may show `HANDOFF_PENDING`.

Recovery remains semantically distinct. An eligible explicit takeover emits `RECOVERY_STARTED`, invalidates predecessor custody, preserves the same EP only when programme reconciliation still says that work is real, advances the epoch, and grants successor custody. After the successor reconstructs unaccepted material/evidence it records `RECOVERY_RECONSTRUCTED` with durable evidence. Do not represent recovery as a successful predecessor handover.

Legacy native repositories without complete epoch/liveness fields remain readable and are not partially upgraded as a side effect of unrelated commands. Explicit legacy recovery remains available; newly issued leases use fenced five-minute liveness.

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
Relay / approved Pass-2 continuation
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
