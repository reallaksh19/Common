# Engineering Relay V3.2 — worth-gated continuity/recovery candidate

## Status

V3.2 is an additive candidate implementation line created from the frozen Engineering Relay V3.1 tree after the evidence-based audit in Common #483.

Until V3.2 is separately accepted/cut over, V3.1 remains the current production protocol. This directory is the implementation/replay surface for the worth-gated V3.2 continuity slice owned by Common #484.

V3.1 is not modified by V3.2 work.

## Normative recorder-first rule

Relay is a durable **recording, continuity and reconstruction mechanism**. It does not decide whether ordinary engineering work may proceed.

Preserve these boundaries:

- Owner/programme intent is human authority.
- Git / PR / tests / runtime / artifacts are material truth.
- exact-head evidence proves only the exact basis it names.
- recorder-integrity failures remain real hard failures.
- provider/reporting/status failure may reduce observability; it must never reduce production agency.
- generated/current/progress/Further-Task views are derived and disposable.
- execution, evidence, verification, delivery, provider lifecycle, and Owner authority remain separate axes.
- a replacement executor/session does not create a new responsibility.

The engineering task-publication set remains exactly:

```text
IMPLEMENTATION_PLAN
PLAN_UPDATE
TASK_EVIDENCE
TASK_RESULT
```

No heartbeat/activity publication is added.

## Responsibility-first topology

Choose coordination topology from engineering responsibility, dependency, and writer topology — never executor count.

```text
R = independently governed responsibilities
D = cross-responsibility dependency edges
C = concurrent material writers

R = 1
→ SINGLE_RESPONSIBILITY

R >= 2
→ PROGRAMME

C >= 2
→ CONCURRENT_WRITER overlay requiring its own proven conflict/fencing semantics
```

Three to five sequential replacement agents on one issue remain one responsibility.

Programme Handover, RLL, and OFFLOAD traversal are conditional on real references/dependencies. Their mere existence in this copied baseline does not make them mandatory on the simple path.

## Exact protocol provenance

A new V3.2 continuity-managed responsibility SHOULD record an exact successor-verifiable protocol source:

```text
PROTOCOL_REF: owner/repo@<exact-commit>:skills/engineering-pr-delivery-v3.2
```

If the candidate protocol is not present on the responsibility's own base/default branch, `PROTOCOL_REF` must point to the repository/commit where the governing candidate actually exists. A PR number may be added for navigation, but it does not replace the exact commit.

This field is continuity provenance, not authority. Older snapshots without it remain readable as `UNKNOWN`; never fabricate a value.

## Implementation plan → automatic GitHub start update

When an agent begins material implementation of an already-published implementation plan, it MUST emit the V3.2 `implementation-start` semantic event.

```text
IMPLEMENTATION_PLAN present
        ↓
implementation begins
        ↓
implementation-start event
        ↓
refresh responsibility current state
        ↓
best-effort GitHub Further Task + title projection
        ↓
continue engineering
```

Starting implementation earns zero progress.

Use:

```bash
python skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py implementation-start \
  --snapshot relay/GENERATED/tasks/<issue>.continuity.json \
  --output relay/GENERATED/tasks/<issue>.continuity.json
```

If the snapshot contains GitHub provider identity and authenticated `gh` is available, the command automatically updates the managed Further Task comment and title suffix.

Provider synchronization failure is recorded as:

```text
FAILED_OBSERVABILITY_ONLY
```

and does not block material engineering.

No timer, heartbeat, commit count, test count, tool call, or elapsed-time event may substitute for this semantic event.

## Responsibility-scoped current state

Use one mutable current surface per continuity-managed responsibility:

```text
FURTHER_TASK_SNAPSHOT
AUTHORITY: DERIVED_CONTINUITY_ONLY
```

It answers:

- exact protocol provenance (`PROTOCOL_REF`);
- current state;
- current plan;
- declared progress denominator;
- P = objectively completed declared units;
- E = completed units with durable successor-safe evidence;
- active/pending units;
- material frontier;
- semantic/evidence frontier;
- passive reconciliation need;
- active recovery mode/evidence obligation;
- current / next;
- genuine Owner decision if any;
- stream-loss/handover escalation state.

The managed provider surface is a cache/read model, not a fifth publication and not authority.

Reference:
- `operating-model/responsibility-continuity-v32.md`
- `templates/further-task-v32.md`
- `schemas/responsibility-continuity.schema.yaml`
- `scripts/continuity_projection.py`

## Progress semantics

Progress is denominator-based.

```text
P = objectively completed declared units / denominator
E = evidenced completed declared units / denominator
```

A unit cannot be evidenced unless it is complete.

Do not award progress from commits, files, tests, comments/publications, tool calls, tokens, elapsed time, executor/session count, or generic `proceed`.

Percentages may decrease after a legitimate declared-denominator expansion.

The issue title may mirror:

```text
{P77% · E69% · UNIT-09 · RECOVERING}
```

but the title is disposable projection only.

## Material vs semantic/evidence frontier

V3.2 separates:

```text
MATERIAL_FRONTIER
SEMANTIC_EVIDENCE_FRONTIER
```

Material head should be observed from Git/owned PR. Semantic/evidence head comes from the latest durable task evidence that explains/proves the relevant responsibility frontier.

A material-ahead distance is reconstruction distance, not progress.

The derived frontier exposes:

```text
RECONCILIATION_NEEDED: true | false
```

This is a passive discrepancy signal. During uninterrupted work, material may legitimately run ahead of the latest evidence checkpoint; therefore `RECONCILIATION_NEEDED=true` does not by itself force a recovery publication on the current executor.

Refresh Git frontier mechanically with:

```bash
python skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py observe-frontier \
  --snapshot relay/GENERATED/tasks/<issue>.continuity.json \
  --repo-root . \
  --output relay/GENERATED/tasks/<issue>.continuity.json
```

## Active recovery state

Recovery obligation is separate from passive frontier lag:

```text
RECOVERY_MODE: NONE | INTERRUPTED_EXECUTOR | FRONTIER_RECONCILIATION
RECOVERY_EVIDENCE_REQUIRED: true | false
```

A replacement executor that observes recovery-relevant unexplained frontier lag starts recovery explicitly:

```bash
python skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py recovery-start \
  --snapshot relay/GENERATED/tasks/<issue>.continuity.json \
  --mode FRONTIER_RECONCILIATION \
  --output relay/GENERATED/tasks/<issue>.continuity.json
```

That event changes state to `RECOVERING` and sets `RECOVERY_EVIDENCE_REQUIRED=true`. A same-lifecycle unexpected loss uses `stream-loss` and sets `RECOVERY_MODE=INTERRUPTED_EXECUTOR`.

Only durable `TASK_EVIDENCE — RECOVERY` provider readback clears the active evidence obligation and aligns the recovered semantic/evidence frontier.

## Abrupt interruption — fast recovery

Unexpected stream/session loss uses this first-line sequence:

```text
1. BASIS
   verify responsibility, PROTOCOL_REF, and Owner amendments.

2. LIVE MATERIAL
   observe PR / branch / base / HEAD / relevant checks.

3. DELTA
   compare semantic/evidence frontier to material frontier.

4. RECONCILE
   validate active/pending work, assumptions, negative knowledge.

5. TASK_EVIDENCE — RECOVERY
   durably anchor reconstructed truth.

6. CONTRIBUTE + CONTINUE
   resume useful engineering.
```

Full/deep reconstruction remains available when task identity, authority, programme dependencies, RLL/OFFLOAD state, negative knowledge, or material/provider state cannot be reconciled.

The recovery publication is required before the next material change after a detected recovery. This is semantic continuity discipline, not `relay_can` permission gating.

## Three consecutive stream losses

Within one executor lifecycle:

```text
loss 1 → recovery evidence
loss 2 → recovery evidence
loss 3 → recovery evidence + Plan for handover once
loss 4+ → recovery evidence only; no repeat auto trigger
```

A successor lifecycle resets the count/trigger.

This is continuity preparation, not an engineering failure or Owner-approval gate.

## Scoped task results

`TASK_RESULT` must make completion scope explicit:

```text
RESULT_SCOPE: STEP | PRODUCT | RESPONSIBILITY
COVERAGE: <declared coverage>
RESPONSIBILITY_COMPLETE: YES | NO | UNKNOWN
```

`RESPONSIBILITY_COMPLETE: YES` requires `RESULT_SCOPE: RESPONSIBILITY`.

Historical V3.1 results without this field are `UNKNOWN`, never guessed complete.

Provider issue closure and PR merge remain separate from responsibility completion.

## Owner decisions

Owner escalation is based on a genuine decision, not executor replacement or ordinary implementation learning.

Ask Owner when the proposed action changes intended outcome/acceptance, independently governed scope, a protected invariant intentionally, a destructive/irreversible choice, reserved merge/release/publication authority, or another explicitly reserved Owner decision.

Do not ask merely because an executor/session changed, implementation detail changed within accepted responsibility, tests/CI need investigation, a predecessor assumption was wrong, status/projection is stale, or provider title/comment sync failed.

## Compatibility posture

This V3.2 directory was forked from the exact V3.1 tree to preserve compatibility while the narrow slice is replayed.

- V3.1 historical records remain immutable.
- copied V3.1 scripts/schemas not touched by this slice remain compatibility baseline, not evidence that their ceremony is mandatory.
- V3.1 AGENT_STATUS remains readable as executor history.
- new responsibility current state is `FURTHER_TASK_SNAPSHOT`.
- old snapshots missing `PROTOCOL_REF` or recovery `mode` remain readable as UNKNOWN/NONE rather than fabricated provenance/recovery.
- old TASK_RESULT without explicit responsibility-complete maps to `UNKNOWN`.
- programme Handover / RLL / OFFLOAD contracts remain readable and are traversed only when relevant.
- missing V3.2 fields map to UNKNOWN rather than fabricated PASS/completion/authority.

## V3.2 exact-head CI

V3.2 candidate changes must have a dedicated hosted check that validates the candidate itself. The V3.1 workflow may legitimately report V3.2-only changes as `NOT_APPLICABLE`; that is not V3.2 acceptance evidence.

The dedicated workflow is `.github/workflows/engineering-pr-delivery-v3.2.yml`. It must remain scoped to V3.2 candidate paths, compile the V3.2 Python surface, and run the focused continuity/replay regressions that exercise this worth-gated slice.

Retired V2.5/V3 workflows must not be restored merely to create more green checks.

## Worth gate

No audit recommendation becomes permanent V3.2 behavior merely because it sounds cleaner.

Retain a change only when replay shows that it addresses an observed failure or recurring measurable operation, materially reduces affected-path protocol work or removes a demonstrated ambiguity/interruption, adds no more recurring ceremony than it removes, keeps clean-path overhead bounded, introduces zero timer/heartbeat work, preserves recorder/material/human-authority invariants, introduces no new Owner gate, and survives real/replayable cases.

The principal replay cases are recorded in Common #483: #375/#379, #376, #377, plus the controlled #486/#487 cold-takeover drill.

## Inherited baseline

All other files under this V3.2 tree were copied from the audited V3.1 tree at fork time. They remain available for compatibility and regression comparison.

Where inherited V3.1 prose conflicts with this V3.2 document **for the continuity/recovery slice above**, this document is normative for V3.2.

Where this document is silent, preserve the V3.1 recorder/material/acceptance invariant until a separately evidence-backed V3.2 change is implemented and validated.
