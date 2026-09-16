# V2.5 completion architecture

## Status

This document is the normative **target architecture** for completing Engineering Relay V2.5 after the control-plane kernel in PR #396. It deliberately distinguishes target semantics from the currently implemented kernel. A target object or predicate described here is not considered implemented until its schema/template/validator/tests are added by the serial catch-up roadmap.

The goal is not to add more state-machine surface. The goal is to make the repository baton semantically sufficient, independently take-overable, operationally useful, and understandable to the Owner.

## Governing relay

```text
OWNER INTENT
    |
    v
OVERALL ROADMAP
    |
    v
EXECUTABLE FRONTIER
    |
    v
SEMANTICALLY COMPLETE EP
    |
    v
BATON_READY
    |
    v
INCOMING REPLACEMENT — ZERO CHAT CONTEXT
    |
    v
DISCOVERY RECEIPT
    |
    +--> QUALIFICATION RECEIPT when required
    |
    v
TAKEOVER CERTIFICATION
    |
    v
TAKEOVER_CERTIFIED
    |
    v
MATERIAL_WRITE_READY
    |
    v
IMPLEMENTATION
    |
    v
QUALITY REVIEW
    |
    v
TEST / BENCHMARK EVIDENCE
    |
    v
CHECKPOINT
    |
    v
ROADMAP / PROGRESS / ISSUE RECONCILIATION
    |
    v
NEXT EP
    |
    v
BATON_READY
```

Conversation is acceleration, never custody.

## Five readiness predicates

V2.5 completion separates baton quality, candidate admission, external projection, custody transfer, and live write permission.

### BATON_READY

`BATON_READY` is a property of repository custody left by the outgoing agent. It must be decidable before the identity of a future replacement is known.

Target predicate:

```text
BATON_READY =
    authoritative roadmap/frontier valid
AND current EP/plan semantically complete
AND predecessor baton valid
AND discovery contract complete
AND current-slice input contracts complete
AND current-slice benchmark/oracle contracts complete
AND scope/protected/prohibited/anti-drift contracts complete
AND exact report + successor contract complete
AND conversation context not required
```

An outgoing agent can therefore truthfully state: "I have left a complete baton that a qualified replacement can pick up."

### TAKEOVER_CERTIFIED

`TAKEOVER_CERTIFIED` is candidate-specific. It proves that the current incoming agent independently recovered and understood the baton on the current basis.

Target predicate:

```text
TAKEOVER_CERTIFIED =
    BATON_READY
AND current candidate has current Takeover Certification PASS
AND required Discovery Receipt PASS
AND required Qualification Receipt PASS
AND certification matches current roadmap / EP-or-plan / Git-material basis
```

The candidate must not author its own criteria, answer them, and unilaterally declare itself qualified without an independent evaluation basis.

### PROJECTION_READY

```text
PROJECTION_READY =
    every required external coordination projection represents current repository truth
```

Projection readiness is independent from engineering custody truth.

### HANDOVER_READY

```text
HANDOVER_READY =
    BATON_READY
AND PROJECTION_READY
```

This answers whether the outgoing custody transfer is complete. It does not say a particular future agent is certified to write.

### MATERIAL_WRITE_READY

```text
MATERIAL_WRITE_READY =
    TAKEOVER_CERTIFIED
AND live execution route valid
AND current Git/material basis valid
AND current continuity/drift state permits WRITE
AND material_authority == WRITE
AND no active hard stop
```

This is the final permission predicate for engineering writes by the current candidate.

## Transition from the current kernel readiness fields

The current kernel still exposes `relay_readiness.repository_ready`, `projection_ready`, and `handover_ready`. During the catch-up roadmap:

- `repository_ready` is not to be strengthened by adding candidate-specific certification to it;
- the semantic baton predicate becomes `BATON_READY`;
- `projection_ready` maps to `PROJECTION_READY`;
- `handover_ready` maps to `HANDOVER_READY`;
- candidate-specific `TAKEOVER_CERTIFIED` and `MATERIAL_WRITE_READY` are added separately;
- lifecycle state alone must never be sufficient evidence for `BATON_READY`.

The live schema/validators remain kernel behavior until the corresponding work package implements this transition. Documentation must not claim implementation before that occurs.

## Independent takeover certification

The outgoing agent prepares the baton; the incoming candidate proves takeover.

```text
OUTGOING AGENT
    |
    +-- prepares semantic EP
    +-- prepares discovery contract
    +-- prepares qualification criteria when required
    +-- passes baton semantic validation
    |
    v
BATON_READY
    |
    v
INCOMING AGENT
    |
    +-- discovers repository independently
    +-- resolves current-slice inputs / benchmarks
    +-- answers qualification when required
    |
    v
INDEPENDENT EVALUATION
    |
    v
TAKEOVER CERTIFICATION PASS
```

Target Takeover Certification identity must include:

```yaml
candidate:
  agent_instance_id: "..."
prepared_by:
  agent_instance_id: "..."
evaluated_by:
  type: DETERMINISTIC_VALIDATOR | INDEPENDENT_AGENT | OWNER
  identity: "..."
self_certification:
  allowed: false
```

Deterministic validators may certify objective facts. Engineering comprehension that cannot be mechanically proved requires a durable independent evaluation basis.

## One work package per EP

The existing invariant remains authoritative:

```text
one executable frontier WP -> one EP
```

Catch-up work must therefore dogfood the same model. Multiple roadmap work packages may be defined in advance, but serial execution makes exactly one material WP executable at a time.

The initial revamp sequence is:

```text
WP-00 Kernel baseline
  -> EP-R001 -> CP-R001
WP-01 Semantic EP
  -> EP-R002 -> CP-R002
WP-02 Baton readiness / Takeover Certification
  -> EP-R003
```

WP-01 depends on WP-00. WP-02 depends on WP-01. They are not one combined EP and must not be executed in parallel.

## Semantic Execution Package target

The current EP categories are retained, but completion requires semantic contracts rather than key presence.

### Inputs

Inputs are typed and slice-aware. Target fields include stable ID/name, authority, source, value or resolvable source, type/units, editability, consumers, validation, stale conditions, applicability, and resolution state.

Target applicability:

```text
CURRENT_STEP_REQUIRED
CURRENT_EP_REQUIRED
FUTURE_STEP
INFORMATIONAL
```

Target resolution:

```text
READY
OWNER_EDITABLE_READY
DEFERRED_NOT_CURRENTLY_REQUIRED
MISSING_BLOCKING
INVALID
STALE
```

Only a condition relevant to the currently authorized slice removes current WRITE permission. `DEFERRED_NOT_CURRENTLY_REQUIRED` is not a blocker.

### Benchmarks / oracles

Benchmarks require purpose, source, payload, expected result, tolerance where applicable, oracle class, independence, applicability, resolution status, and mappings to tests/acceptance.

Typical generic oracle classes:

```text
ANALYTICAL
REFERENCE_DATA
INDEPENDENT_IMPLEMENTATION
FROZEN_GOLDEN
EXTERNAL_STANDARD
MANUAL_RECONSTRUCTION
OBSERVATIONAL
```

### Repository discovery

Discovery becomes executable and receipt-producing. A discovery **instruction** uses a `DSTEP-xxxx` ID and identifies an action, target, question, expected outputs, whether a receipt is required, and stop/reconciliation conditions.

Typical actions:

```text
LOCATE
TRACE
VERIFY
COMPARE
INSPECT
RESOLVE
```

The successor produces a separate `DISC-xxxx` Discovery Receipt. `DSTEP-*` therefore means a forward discovery instruction while `DISC-*` means the candidate's backward evidence. `DR-*` is not used for discovery because Drift Receipts already occupy the drift namespace conceptually.

### Scope and anti-drift

Scope distinguishes allowed writes, allowed reads, protected domains/invariants, prohibited changes, and Owner-reserved changes. Anti-drift conditions are stable structured rules; an empty stale-condition set requires an explicit no-known-condition rationale rather than an empty list that looks complete.

### Implementation steps

Each implementation step identifies objective, targets, reads, writes, inputs, acceptance, tests, expected intermediate state, and stop conditions. Vague instructions such as "implement required changes" are not semantically sufficient.

### Exact report / successor contract

The EP defines the exact structured return payload, not only section names. Acceptance reconciliation, changed files, evidence, quality, discoveries, limitations, roadmap impact, and ordered next work have typed payload requirements.

## Qualification trigger and qualification receipt

Fresh qualification is mandatory when either condition is true:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

A materially new boundary includes a significant change in production path, engineering authority, numerical method, safety/protected invariant, input authority, or verification/oracle class. Same phase + same engineering boundary may reuse a still-current qualification.

The outgoing relay prepares the question set. The incoming candidate answers it. Evaluation produces a durable `QUAL-xxxx` Qualification Receipt before material writes when qualification is required.

Q1-Q5 target semantics remain:

```text
Q1 actual production path / source trace
Q2 concrete engineering reconstruction where the domain permits
Q3 boundary/authority mutation plus explicit falsifier
Q4 independent verification / benchmark reasoning
Q5 exact first safe slice plus predicted verification result
```

Correct IDs with meaningless answers do not constitute qualification.

## Quality applicability router

Quality remains distinct from stop/evidence. An EP explicitly selects applicable quality blueprints and records why others do not apply.

Target shape:

```yaml
quality:
  applicable:
    - blueprint: software-design
      reason: "state ownership changes"
    - blueprint: testing
      reason: "material behavior changes"
  not_applicable:
    - blueprint: engineering-numerics
      reason: "no numerical authority changes"
```

This prevents quality from becoming a universal bureaucracy. Applicable procedures produce a durable `QRV-xxxx` Quality Review. A quality finding is not automatically a hard stop.

## Reports are projections, never authority

Structured reports and generated Markdown are derived/reconciled views. They do not become another writable truth source.

Authority flow:

```text
ROADMAP
EP
DISC / QUAL / TC
QUALITY REVIEW
CP
PROGRESS
ISSUE GRAPH
      |
      v
STRUCTURED REPORT
      |
      +--> OWNER_STATUS.md
      +--> TECHNICAL_STATUS.md
      +--> HANDOVER.md
```

A report records its generation basis and must reconcile to source objects. If it disagrees with its sources, the report is stale or invalid; it does not override them.

## Target object namespaces

```text
DSTEP-xxxx  EP discovery instruction
DISC-xxxx   Discovery Receipt
TC-xxxx     Takeover Certification
QUAL-xxxx   Qualification Receipt
QRV-xxxx    Quality Review
CP-xxxx     Checkpoint
ODR-xxxx    Owner Decision Record
```

Existing plan/join/replan/drift namespaces remain unchanged.

## Human and machine representations

Machine precision remains necessary, but Owner communication is a projection of machine truth into plain engineering language.

Machine representation may use states such as `READ_ONLY`, `STALE`, `PARTIAL`, or `RECONCILE_REQUIRED`. The default Owner view explains what can be done, what cannot be changed yet, why, what evidence exists, what remains missing, what changed, what happens next, and what Owner decision is actually required.

The human representation may never conceal machine truth, but it should not make control-plane vocabulary the primary language of normal Owner interaction.

## Defining end-to-end acceptance test

The release-level acceptance criterion is an A -> B -> C relay with chat custody deliberately removed between candidates.

```text
AGENT A
  creates CP-A + EP-B
  exits

CHAT DELETED

AGENT B
  receives repository only
  finds REPO_STATE / roadmap / EP-B
  performs discovery
  performs qualification when required
  receives TC-B PASS
  executes
  creates CP-B + EP-C
  exits

CHAT DELETED

AGENT C
  receives repository only
  reconstructs Owner intent, roadmap position, history,
  current task, inputs, benchmarks, scope, quality obligations,
  tests, acceptance, staleness rules and exact next work
  receives TC-C PASS
```

If Agent C requires prior chat to answer any material custody question, V2.5 completion fails.

## Implementation sequencing rule

Do not build GitHub orchestration, Owner-facing polish, or expanded blueprint machinery on top of a semantically weak baton. The required order is:

```text
baseline
-> semantic EP
-> baton readiness / takeover certification
-> zero-context takeover proof
-> strong qualification
-> full progress/handover
-> GitHub operations + quality procedures
-> human communication + Owner change intake
-> end-to-end certification
-> self-consistency audit
-> PR readiness
```

First make the baton trustworthy. Then independently prove that a replacement can pick it up.
