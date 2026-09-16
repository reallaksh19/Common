# V2.5 completion architecture

## Status

This document is the normative architecture for completing Engineering Relay V2.5 after the control-plane kernel in PR #396.

Current implementation status:

```text
WP-00 Kernel baseline / object matrix          DELIVERED — CP-R001
WP-01 Semantic Execution Package               DELIVERED — CP-R002
WP-02 Baton readiness + Takeover Certification CURRENT FRONTIER
```

A target object/predicate is not considered implemented until its schema/template/validator/tests and checkpointed evidence exist. The goal is not to add state-machine surface for its own sake; it is to make repository custody semantically sufficient, independently take-overable, operationally useful, and understandable to the Owner.

Conversation is acceleration, never custody.

## Governing relay

```text
OWNER INTENT / OWNER DECISION
    |
    v
OVERALL ROADMAP
    |
    v
EXECUTABLE FRONTIER
    |
    v
SEMANTIC EP / APPROVED PARALLEL PLAN        [WP-01 delivered]
    |
    +--> DSTEP-* discovery contract          [WP-01 delivered]
    |
    v
BATON_READY                                  [WP-02]
    |
    v
INCOMING REPLACEMENT — ZERO CHAT CONTEXT
    |
    +--> DISC-* Discovery Receipt            [WP-02]
    +--> QUAL-* when required                [WP-03]
    |
    v
TC-* TAKEOVER CERTIFICATION                  [WP-02]
    |
    v
TAKEOVER_CERTIFIED                           [WP-02]
    |
    v
MATERIAL_WRITE_READY                         [WP-02]
    |
    v
IMPLEMENTATION
    |
    v
QUALITY REVIEW + TEST/BENCHMARK EVIDENCE     [WP-06 deepens quality]
    |
    v
CHECKPOINT
    |
    v
ROADMAP / PROGRESS / ISSUE RECONCILIATION
    |
    v
NEXT EP
```

## Authority separation

```text
Owner intent / ODR       authoritative intent
Overall Roadmap          authoritative plan/topology
EP / Parallel Plan       authorized forward slice
DSTEP                     forward discovery requirement
DISC / QUAL / TC          candidate evidence/admission (pending)
Live Git observation      runtime fact
CP                        backward execution truth
PROGRESS / ISSUE_GRAPH    reconciled repository state
Generated Markdown        projection only
GitHub                    external coordination projection
Chat                      non-authoritative convenience
```

No downstream repository is a Common implementation target. Real repositories may reveal protocol failure modes only through read-only stress/validation; fixes first become repository-neutral Common invariants and synthetic regressions.

## Semantic Execution Package — delivered WP-01

The EP is now semantically validated for serial active work and every Owner-approved parallel lane.

### Inputs

Inputs carry stable identity, description, authority, source, value or resolution method, type/units, editability, applicability, resolution, consumers, validation and stale conditions.

Applicability:

```text
CURRENT_STEP_REQUIRED
CURRENT_EP_REQUIRED
FUTURE_STEP
INFORMATIONAL
```

Resolution:

```text
READY
OWNER_EDITABLE_READY
DEFERRED_NOT_CURRENTLY_REQUIRED
MISSING_BLOCKING
INVALID
STALE
```

An EP claiming `EXECUTABLE | ACTIVE` cannot carry a current-required input in missing/invalid/stale/deferred state.

### Benchmarks / oracles

Declared benchmarks/oracles carry source, oracle class, payload, expected result, tolerance, independence, applicability/resolution, verification mappings and stale conditions.

Generic oracle classes include:

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

Forward discovery instructions use `DSTEP-*` and carry action, target(s), question, expected outputs, receipt requirement and failure/reconciliation behavior.

```text
DSTEP-* = forward EP discovery instruction
DISC-*  = future candidate Discovery Receipt
```

### Scope / anti-drift / steps

Semantic EP scope distinguishes allowed writes, allowed reads, protected domains/invariants, prohibited changes and Owner-reserved changes.

Anti-drift rules are structured and stable. Implementation steps carry exact targets, reads, writes, input IDs, acceptance IDs, tests, expected state and stop conditions. Vague instructions do not pass.

### Report and successor contract

Every mandatory report heading is paired with source objects and required reconciliation fields. The generated report remains a projection.

The successor contract requires durable outputs including checkpoint, next frontier, and successor-EP-or-terminal disposition.

### Repository admission around the EP

`REPO_PROFILE.yaml` is now required by aggregate conformance. `REPO_STATE.relay_protocol.version/basis_ref` is enforced, including rejection of placeholder/unbound basis refs.

## Five readiness predicates — WP-02 target

V2.5 completion separates baton quality, candidate admission, external projection, custody transfer and live write permission.

### BATON_READY

Property of repository custody left by the outgoing agent; candidate-independent.

```text
BATON_READY =
    roadmap/frontier valid
AND current EP/plan semantically complete
AND predecessor baton valid
AND discovery contract complete
AND current-required inputs/oracles complete
AND scope/anti-drift/report/successor contracts complete
AND repository/profile/protocol basis admitted
AND conversation not required
```

Lifecycle alone must never prove this predicate.

### TAKEOVER_CERTIFIED

Candidate-specific proof:

```text
TAKEOVER_CERTIFIED =
    BATON_READY
AND current candidate has TC PASS
AND required DISC receipt PASS
AND required QUAL receipt PASS/NA as applicable
AND certification matches current roadmap / route / predecessor / material basis
```

The outgoing preparer cannot unilaterally self-certify the incoming candidate.

### PROJECTION_READY

```text
PROJECTION_READY = required external coordination projections represent current repository truth
```

### HANDOVER_READY

```text
HANDOVER_READY = BATON_READY AND PROJECTION_READY
```

This answers whether outgoing custody is complete, not whether an arbitrary future agent may write.

### MATERIAL_WRITE_READY

```text
MATERIAL_WRITE_READY =
    TAKEOVER_CERTIFIED
AND live execution route valid
AND Git/material basis valid
AND continuity/drift permits WRITE
AND material_authority == WRITE
AND no active hard stop
```

## Candidate discovery / Takeover Certification — WP-02

The incoming candidate executes the EP's `DSTEP-*` instructions and records a durable `DISC-*` receipt bound to exact candidate, roadmap, EP/plan route, predecessor baton and material basis.

Takeover Certification must identify:

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

Certification becomes stale when a relevant roadmap/EP/predecessor/Git/input/oracle/scope/qualification basis changes.

## Qualification — WP-03

Fresh qualification is required when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

A material boundary includes significant change in production path, engineering authority, numerical method, protected/safety invariant, input authority or verification/oracle class.

```text
QUESTION_SET -> candidate answers -> independent evaluation -> QUAL-* -> TC reconciliation
```

Q1–Q5 target semantics:

```text
Q1 actual production path / source trace
Q2 concrete engineering reconstruction where applicable
Q3 boundary/authority mutation plus falsifier
Q4 independent verification / benchmark reasoning
Q5 exact first safe slice plus predicted verification result
```

## Quality — WP-06 target

Quality remains separate from hard-stop/evidence state. Later quality routing will select applicable procedures with reasons and create `QRV-*` Quality Review evidence. A quality finding is not automatically a stop.

## Reports and human representation — WP-04/WP-07 target

Authority flow remains:

```text
ROADMAP / EP / DISC / QUAL / TC / QRV / CP / PROGRESS / ISSUE_GRAPH
    -> structured reconciled report
    -> TECHNICAL_STATUS
    -> OWNER_STATUS
    -> HANDOVER
```

Machine vocabulary may remain precise. The Owner view will explain capabilities, restrictions, evidence, gaps, roadmap effect, next work and actual Owner decisions in plain engineering language without concealing machine truth.

## Object namespaces

```text
DSTEP-xxxx  EP discovery instruction          delivered
DISC-xxxx   Discovery Receipt                 WP-02
TC-xxxx     Takeover Certification            WP-02
QUAL-xxxx   Qualification Receipt             WP-03
QRV-xxxx    Quality Review                    WP-06
CP-xxxx     Checkpoint                        delivered kernel
ODR-xxxx    Owner Decision Record             delivered kernel
```

Existing plan/join/replan/drift namespaces remain unchanged.

## Defining end-to-end acceptance test

Release-level acceptance is A -> B -> C with chat custody deleted between candidates:

```text
AGENT A
  creates CP-A + semantic EP-B
  exits

CHAT DELETED

AGENT B
  repository-only discovery
  DISC/QUAL as required
  TC-B PASS
  executes
  creates CP-B + semantic EP-C
  exits

CHAT DELETED

AGENT C
  reconstructs Owner intent, roadmap position, history,
  current task, inputs, benchmarks/oracles, scope,
  quality obligations, tests, acceptance, staleness and next work
  receives TC-C PASS
```

If Agent C materially requires prior conversation, V2.5 completion fails.

## Implementation sequence

```text
baseline                         COMPLETE
-> semantic EP                   COMPLETE
-> baton readiness / TC          CURRENT
-> zero-context takeover proof
-> strong qualification
-> full progress/handover
-> GitHub operations + quality procedures
-> human communication + Owner change intake
-> end-to-end certification
-> self-consistency audit
-> PR readiness
```

First make the baton trustworthy. Then independently prove a replacement can pick it up.
