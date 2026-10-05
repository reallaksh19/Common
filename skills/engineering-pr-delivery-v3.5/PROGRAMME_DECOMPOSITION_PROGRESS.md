# Engineering Relay V3.5 — programme decomposition and progress contract

## Status

`engineering-pr-delivery-v3.5` is not yet a complete invocable protocol in `Common`.

This file is a candidate future contract for the V3.5 line. It MUST NOT be treated as an active selector by itself. When V3.5 is implemented, these semantics should be incorporated into its normative planning, continuity, schema, projection, tests and replay surfaces.

## Governing invariant

> **Coordinator planning defines the denominator; executors contribute evidence against it. Percentage is mechanically projected from the plan and evidence. Splits conserve weight, progressive decomposition consumes reserve, true scope expansion changes the denominator explicitly, and liveness remains independent from percentage.**

## Planning is the source of progress truth

V3.5 should require a Coordinator-produced Programme Decomposition Manifest before production release.

The manifest should define:

```text
Programme
  -> Phases
      -> Responsibility Blocks / PRDs
          -> semantic implementation units
          -> acceptance profile
          -> size budget
          -> write surface
          -> nested Coder identity
```

The same planning model supplies the progress denominator later projected into GitHub titles.

## Three progress levels

Keep distinct:

```text
PRD / COMMENT BLOCK
  P = semantic implementation progress
  E = evidenced semantic implementation progress
  D = Local delivery progress including review/super-review/handoff

PHASE
  D = weighted roll-up of PRD delivery + phase integration/qualification
  E = weighted evidenced delivery

PROGRAMME/PARENT
  D = weighted roll-up of Phase delivery
  E = weighted evidenced delivery
```

`P100` for a nested Coder never means the Local PRD, Phase or Programme is complete.

## Programme Decomposition Manifest

Recommended schema:

```yaml
programme:
  id: <stable id>
  parent_issue: <provider ref>
  owner_basis_ref: <ref>
  coordinator_principal: <principal>

  local_protocol_ref: <exact Local ref>
  engineering_protocol_ref: <exact V3.5 ref>
  acceptance_epoch: <id>
  project_protocol_ref: <ref>
  project_protocol_digest: <digest>

  progress_model:
    total_weight: 10000

  phases:
    - id: PHASE-A
      issue: <ref>
      weight: <integer>
```

For a fixed denominator:

```text
sum(phase weights) = total programme weight
```

## Phase Manifest

Each Phase issue should carry a machine-readable manifest:

```yaml
phase:
  id: PHASE-C
  programme: <id>
  issue: <ref>
  coordinator: <principal>
  outcome: <phase outcome>

  entrance_conditions: [...]
  exit_conditions: [...]
  dependencies: [...]

  weight: 2200

  delivery_pools:
    responsibility_delivery: 1900
    phase_integration: 200
    phase_qualification: 100

  responsibilities: [C01, C02, C03]
  undecomposed_reserve_weight: <integer>
```

Invariant:

```text
instantiated PRD weights
+ undecomposed reserve
+ phase integration/qualification weights
= phase weight
```

A Phase cannot reach 100% while unresolved reserve or required phase gates remain.

## Responsibility Block schema

Recommended:

```yaml
responsibility:
  id: PRD-OCR-C03
  phase: PHASE-C

  representation:
    kind: COMMENT_BLOCK | SINGLE_ISSUE | CONTINUATION
    issue: <ref>
    block: C.3
    spec_comment_ref: <ref>

  outcome: <single coherent outcome>
  dependencies: [...]
  write_surface: [...]

  size_budget:
    target_minutes: 15
    hard_minutes: 20
    target_reviewable_loc: 700
    hard_reviewable_loc: 1500

  progress_weight: <integer>

  acceptance_profile:
    ref: <ref>
    digest: <digest>

  nested_engineering_responsibility:
    id: ENG-PRD-OCR-C03-CODER
```

## Semantic implementation units

Each PRD must declare semantic units with weights summing to 100, for example:

```yaml
implementation_units:
  - id: U1
    outcome: constraint candidate model
    weight: 25
  - id: U2
    outcome: candidate ranking implementation
    weight: 35
  - id: U3
    outcome: grammar-aware rejection
    weight: 20
  - id: U4
    outcome: focused deterministic tests
    weight: 20
```

Then:

```text
P = completed semantic-unit weight / total semantic-unit weight
E = completed semantic-unit weight with current valid durable evidence / total semantic-unit weight
```

Executors update unit/evidence state; deterministic tooling computes P/E.

## Local delivery denominator

V3.5 nested Coder completion is only part of Local delivery.

Recommended fallback when a project-specific Acceptance Profile does not supply more precise weights:

```text
Coder semantic completion   60
Reviewer acceptance         20
Super Review                15
Final handoff/binding        5
                           ---
                           100
```

Where possible, Reviewer/Super Review contribution should be derived from explicit required acceptance methods rather than generic stage percentages.

## Split conservation

A split must conserve programme/phase weight:

```text
C03 weight 300
 -> C03A 100
 -> C03B 120
 -> C03C 80
```

Required:

```text
sum(successor weights) = source weight
```

Replacement executor, replacement PR, retry, acceptance replay or same-stage fresh attempt do not change weight.

## Progressive decomposition reserve

A Coordinator should not be forced to fully micro-design all future blocks before learning begins.

Use `UNDECOMPOSED_RESERVE`.

Example:

```text
Phase C = 2200
C01 = 300
C02 = 250
C03 = 300
phase gates = 300
reserve = 1050
```

Later waves consume reserve while preserving the denominator.

Reserve contributes zero progress until legitimately allocated or dispositioned.

## Scope expansion

A true new requirement is not a split.

Use a governed scope-expansion event such as:

```text
PLAN_UPDATE — SCOPE_EXPANSION
```

Record old denominator, new scope, added weight, new denominator and authority basis where required.

A resulting decrease in displayed progress is valid. V3.5 must not renormalize merely to preserve a previous percentage.

## Responsibility size versus checkpoint size

These must remain independent:

```text
CHECKPOINT threshold
  limits transient recovery distance inside a PRD

SPLIT threshold
  limits cumulative PRD scope
```

Recommended activity checkpoint triggers:

```text
>=3000 new substantive lines reconstructed
>=250 newly authored reviewable LOC
>=400 materially modified reviewable LOC
semantic/evidence frontier movement
pre-risk operation
```

Recommended hard checkpoint ceilings:

```text
>=500 newly authored reviewable LOC
>=700 materially modified reviewable LOC
```

These cause checkpointing, not a new PRD.

Cumulative responsibility limits such as `>20 active Coder minutes` or `>1500 reviewable semantic LOC` trigger `SPLIT_REQUIRED` / `SPLIT_REMAINDER` unless an explicit governed exception applies.

Replacement executors do not reset cumulative PRD budgets.

## Reviewer bounded repair

Recommended starting repair envelope:

```text
TARGET <=5 active minutes / <=150 reviewable LOC
HARD   <=10 active minutes / <=300 reviewable LOC
```

Larger discovered repairs become explicit scope changes or successor repair responsibilities rather than hidden second implementation stages.

## Mechanical/generated work

Classify changed material as appropriate:

```text
SEMANTIC_DELTA
MECHANICAL_DELTA
GENERATED_DELTA
```

A large deterministic protocol tree copy or generated artifact should normally be isolated as a mechanical responsibility with equality/reproducibility proof.

Semantic changes should remain separately bounded/reviewable.

Mechanical/generated LOC do not independently create progress.

## Parallelism and write surfaces

Every PRD should declare `write_surface`.

Before parallel release, compare active surfaces.

Overlap requires:

```text
SERIALIZE
DECLARE DEPENDENCY
or PROVE SAFE ISOLATED INTEGRATION
```

Parallel execution is justified by responsibility/workspace independence, not executor count.

## Deterministic roll-up

Phase:

```text
phase_D = sum(component_weight * component_D) / phase_weight
phase_E = sum(component_weight * component_E) / phase_weight
```

Programme:

```text
programme_D = sum(phase_weight * phase_D) / total_programme_weight
programme_E = sum(phase_weight * phase_E) / total_programme_weight
```

Do not derive percentages from issue count, PR count, LOC, elapsed time, commits, tool calls, tokens or model confidence.

## Status is independent of percentage

Use liveness/motion state separately:

```text
🟢 ACTIVE
🟡 QUIET / POSSIBLE_SPINNING
🔵 WAITING
🔴 STALE
✅ COMPLETE
```

Critical-path metadata should influence aggregate Phase/Programme status.

Recommended aggregate logic:

```text
RED    critical-path PRD/Coordinator STALE or critical dependency irrecoverably blocked
YELLOW critical-path QUIET/SPINNING or noncritical PRD STALE
BLUE   no red/yellow but critical path legitimately WAITING
GREEN  otherwise while work is active
COMPLETE only when delivery/acceptance completion semantics are satisfied
```

Do not average colors.

## Title projections

Responsibility:

```text
🟢 {P60% · E45% · A07 · U3} <responsibility title>
```

Phase:

```text
🟡 {D43% · E36% | 🟢2 🟡1 🔵1} <phase title>
```

Programme:

```text
🟡 {D28% · E22% | 🟢4 🟡1 🔴0 🔵1} <programme title>
```

Titles are read models, never authority.

## Decomposition Validation Gate

Future V3.5 should mechanically refuse production release when the Coordinator plan is not structurally complete enough to produce a defensible denominator.

Validate at least:

```text
PROGRAMME
- parent outcome
- phase coverage
- denominator allocation

PHASE
- outcome
- entrance/exit criteria
- dependencies
- Coordinator identity
- phase integration/qualification allocation
- reserve conservation

RESPONSIBILITY
- stable PRD id
- bounded outcome
- size estimate
- write surface
- acceptance profile
- semantic units
- valid dependency graph
- collision classification

ACCEPTANCE
- pinned project protocol
- resolvable Reviewer/Super Reviewer methods
- external gates where required

PROGRESS
- full denominator allocation
- split conservation
- reserve representation
- no LOC/time/activity-derived completion

OBSERVABILITY
- title projection
- checkpoint/liveness projection
- truthful watcher availability
```

Produce a machine result such as:

```text
DECOMPOSITION_QUALITY_REPORT
PLAN_STATE: RELEASEABLE | NOT_RELEASEABLE
```

## Projection engine

V3.5 should implement deterministic code that consumes structured manifests and evidence and emits title/current-state projections.

Conceptual flow:

```text
programme manifest
+ phase manifests
+ responsibility blocks
+ acceptance profiles
+ evidence validity
+ activity leases
+ provider state
      |
      v
projection engine
      |
      +-- PRD P/E/D
      +-- Phase D/E/status
      +-- Programme D/E/status
      +-- title strings
      `-- managed current-state tables
```

The model should never manually calculate or choose percentages in prose.

## Executor lifetime

Recommended:

```text
ONE EXECUTOR EPOCH
NORMALLY ONE PRODUCTION RESPONSIBILITY
```

Each PRD begins from a fresh bounded context, checkpoints during execution, publishes scoped result/handoff, and ends its executor epoch.

The Phase Coordinator is the longer-lived contextual owner across PRDs.

This is intended to prevent a programme split on GitHub from degenerating into one enormous transient agent session.

## Required future tests

Future V3.5 implementation should include tests proving:

- executor cannot manually set projected P/E/D;
- Coder P100 cannot make Local D100;
- split conserves weight;
- reserve consumption preserves denominator;
- genuine scope expansion changes denominator explicitly;
- replacement executor does not reset size budget;
- checkpoint threshold does not mint new PRD;
- hard PRD size overrun requires split/remainder handling;
- phase cannot reach 100 with unresolved reserve/integration/qualification;
- mechanical 35k-line copy does not create semantic progress;
- traffic-light roll-up honors critical path and does not average colors;
- parent/phase title percentage is deterministic from the same input manifests/evidence.
