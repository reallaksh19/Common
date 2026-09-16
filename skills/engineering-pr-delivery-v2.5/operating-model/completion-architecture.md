# V2.5 completion architecture

## Status

This document is the normative architecture for completing Engineering Relay V2.5 after the control-plane kernel in PR #396.

Current implementation status:

```text
WP-00 Kernel baseline / object matrix               DELIVERED — CP-R001
WP-01 Semantic Execution Package                    DELIVERED — CP-R002
WP-02 Baton readiness + Takeover Certification      DELIVERED — CP-R003
WP-03 Strong phase/boundary qualification           CURRENT FRONTIER
```

A target object/predicate is not considered delivered until its schema/template/validator/tests and checkpointed evidence exist. Conversation is acceleration, never custody.

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
BATON_READY                                  [WP-02 delivered]
    |
    v
INCOMING REPLACEMENT — ZERO CHAT CONTEXT
    |
    +--> DISC-* Discovery Receipt            [WP-02 delivered]
    +--> QUAL-* when required                [WP-03 current]
    |
    v
TC-* TAKEOVER CERTIFICATION                  [WP-02 delivered]
    |
    v
TAKEOVER_CERTIFIED(route, candidate)         [WP-02 delivered]
    |
    v
MATERIAL_WRITE_READY(route,candidate,live)   [WP-02 runtime gate]
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
DSTEP-*                   forward discovery requirements
DISC-*                    candidate discovery evidence
TC-*                      route/candidate admission evidence
QUAL-*                    engineering qualification evidence (WP-03)
Live Git observation      runtime fact
CP                        backward execution truth
PROGRESS / ISSUE_GRAPH    reconciled repository state
Generated Markdown        projection only
GitHub                    external coordination projection
Chat                      non-authoritative convenience
```

No downstream repository is a Common implementation target. Real repositories may reveal protocol failure modes only through read-only stress/validation; fixes first become repository-neutral Common invariants and synthetic regressions.

## Semantic Execution Package — delivered WP-01

The EP is semantically validated for serial active work and every Owner-approved parallel lane. It includes typed slice-specific inputs, benchmarks/oracles, executable `DSTEP-*` discovery, bounded scope, structured anti-drift, exact implementation mappings, source-bound report payloads, and durable successor outputs. `REPO_PROFILE.yaml` and the pinned relay protocol basis are admitted into conformance.

Input applicability:

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

Only unresolved requirements relevant to the current slice remove current execution eligibility; future/informational items do not recreate an everything-is-blocked workflow.

## Readiness and candidate admission — delivered WP-02

Read `takeover-certification.md` for the complete contract and `ci-evidence-correction.md` for the corrected workflow evidence rule.

### BATON_READY

Repository-wide and candidate-independent:

```text
BATON_READY =
    roadmap/frontier valid
AND current EP/plan semantically complete
AND predecessor custody valid
AND repository profile/protocol admitted
AND discovery contract complete
AND current-required input/oracle contracts complete
AND scope/anti-drift/report/successor contracts complete
AND conversation context not required
```

A repository may be `BATON_READY` while `takeover_admissions: []`. This is essential: the outgoing agent can leave a complete baton before the future replacement exists.

### TAKEOVER_CERTIFIED(route, candidate)

Route/candidate-specific, never a single repository-wide boolean:

```text
TAKEOVER_CERTIFIED(route,candidate) =
    BATON_READY
AND current DISC receipt for route/candidate PASS
AND current TC receipt for route/candidate PASS
AND current required QUAL receipt PASS when applicable
AND DISC/TC basis matches current roadmap / route / EP contract /
    REPO_PROFILE / predecessor baton / material basis
```

Serial route keys are `SERIAL:<EP-id>`. Parallel lane route keys are `PARALLEL_LANE:<PLAN-id>:<LANE-id>:<EP-id>` so different approved lanes may have different certified candidates.

`REPO_STATE.takeover_admissions[]` is only a locator/projection to durable DISC/TC receipts. Validators re-open those files and re-compute the current basis.

### DISC/TC staleness binding

Candidate evidence is bound to:

- roadmap ID/revision;
- relay protocol basis;
- route / plan / lane / EP identity;
- material ref;
- canonical semantic EP digest;
- canonical `REPO_PROFILE` digest;
- predecessor checkpoint/join/replan identity and digest;
- required DSTEP IDs and expected output names;
- qualification requirement.

Editing an EP contract in place therefore invalidates old certification even if its EP ID is unchanged.

### PROJECTION_READY

```text
PROJECTION_READY = required external coordination projections represent current repository truth
```

### HANDOVER_READY

```text
HANDOVER_READY = BATON_READY AND PROJECTION_READY
```

This is outgoing custody completeness, not candidate write authority.

### MATERIAL_WRITE_READY(route,candidate,live_git)

Live-derived and deliberately **not persisted**:

```text
MATERIAL_WRITE_READY =
    TAKEOVER_CERTIFIED(route,candidate)
AND live route resolves exactly that route
AND live Git/material basis is acceptable
AND current drift/continuity permits WRITE
AND material_authority == WRITE
AND execution.can_continue == true
AND no active hard stop
```

`material_authority: WRITE` is therefore necessary but not sufficient. A candidate without current certification, on the wrong branch/worktree, or on stale/unqualified base drift cannot write.

The runtime gate is `scripts/material_write_ready.py`.

## Independent takeover

The outgoing preparer creates the semantic EP and discovery/qualification criteria. The incoming candidate performs repository discovery. Takeover Certification records candidate, preparer and evaluator identities and requires `self_certification.allowed: false`.

A candidate may not be its own preparer. An `INDEPENDENT_AGENT` evaluator may not be the candidate. Deterministic evaluation is valid only because the validator itself re-runs the objective semantic/basis checks; a YAML claim naming a validator is not authority.

If the incoming EP requires phase/material qualification, WP-02 prevents a TC from PASSing until WP-03 provides a valid `QUAL-*` transaction. Takeover admission cannot bypass qualification.

## Qualification — WP-03 current frontier

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

Target Q1–Q5 semantics:

```text
Q1 actual production path / source trace
Q2 concrete engineering reconstruction where applicable
Q3 boundary/authority mutation plus falsifier
Q4 independent verification / benchmark reasoning
Q5 exact first safe slice plus predicted verification result
```

Qualification is candidate/route/basis evidence. It does not itself grant write authority; `TC-*` must consume current `QUAL-*` evidence and the live write gate remains final.

## Quality — WP-06 target

Quality remains separate from hard-stop/evidence state. Later quality routing selects applicable procedures with reasons and creates `QRV-*` Quality Review evidence. A quality finding is not automatically a stop.

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
DSTEP-xxxx  EP discovery instruction          delivered WP-01
DISC-xxxx   Discovery Receipt                 delivered WP-02
TC-xxxx     Takeover Certification            delivered WP-02
QUAL-xxxx   Qualification Receipt             current WP-03
QRV-xxxx    Quality Review                    WP-06
CP-xxxx     Checkpoint                        delivered kernel
ODR-xxxx    Owner Decision Record             delivered kernel
```

Existing plan/join/replan/drift namespaces remain unchanged.

## Defining end-to-end acceptance

WP-02 proves the first zero-context candidate can pick up a rich baton without chat and can only obtain live write readiness with current route/certification/Git authority. WP-09 remains the full recursive release test:

```text
AGENT A -> CHAT DELETED -> AGENT B -> CHAT DELETED -> AGENT C
```

Agent C must reconstruct Owner intent, roadmap position, predecessor facts/limitations, current task, input authority/editability, benchmarks/oracles, scope, quality obligations, tests, acceptance, staleness and exact next work from repository state alone and obtain current independent certification.

If prior conversation is materially required, V2.5 completion fails.

## Validation evidence discipline

A whole-suite V2.5 claim requires both explicit CI steps to pass on the claimed exact head:

```text
root unit discovery
synthetic tests/stress discovery
```

Historical runs that compiled stress modules without executing the dedicated stress discovery are interpreted according to `ci-evidence-correction.md`.

## Implementation sequence

```text
baseline                         COMPLETE — CP-R001
-> semantic EP                   COMPLETE — CP-R002
-> baton readiness / TC          COMPLETE — CP-R003
-> strong qualification          CURRENT — WP-03
-> full progress/handover
-> GitHub operations + quality procedures
-> human communication + Owner change intake
-> end-to-end certification
-> self-consistency audit
-> PR readiness
```

First make the baton trustworthy. Then independently prove a replacement can pick it up.
