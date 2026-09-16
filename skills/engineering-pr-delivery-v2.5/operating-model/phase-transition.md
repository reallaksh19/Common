# Phase transitions, material qualification boundaries, and Q1-Q5

The current kernel creates a fresh incoming-phase question set when the recomputed executable frontier enters a new phase. The completion architecture retains that rule and adds a second mandatory trigger:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

Same-phase progression may reuse a still-current qualification only when the engineering/authority boundary is materially unchanged.

A materially new qualification boundary includes substantial change in one or more of:

- production path or state ownership;
- engineering/numerical method;
- authoritative input source or editability model;
- protected/safety-critical invariant;
- verification/oracle class or independence basis;
- engineering authority needed to execute safely.

Routine refactoring or cosmetic/UI-only movement that does not change the relevant engineering boundary should not mechanically retrigger qualification.

## Question-set grounding

Each question retains a fixed focus and explicit durable anchors from the incoming EP:

```yaml
qualification_trigger:
  phase_changed: true
  material_boundary_changed: false
  basis:
    - PHASE-002
    - WP-020

question_set:
  - id: Q1
    focus: PRODUCTION_PATH
    anchors: [PHASE-002, WP-020]
  - id: Q2
    focus: ENGINEERING_PROBLEM
    anchors: [WP-020, INPUT-01]
  - id: Q3
    focus: BOUNDARIES_INVARIANTS
    anchors: [WP-020, AC-01]
  - id: Q4
    focus: VERIFICATION
    anchors: [AC-01, TEST-01]
  - id: Q5
    focus: FIRST_SAFE_SLICE
    anchors: [STEP-01, AC-01]
```

Valid anchors are incoming phase/work-package IDs plus IDs declared by the incoming EP's typed inputs, benchmarks/oracles, acceptance criteria, validation plan and implementation steps.

## Completion target: evaluated qualification

Question metadata is not qualification. Under WP-03 the transaction becomes:

```text
outgoing relay prepares QUESTION_SET
        |
        v
incoming candidate answers with zero chat custody
        |
        v
independent evaluation
        |
        v
QUAL-xxxx Qualification Receipt
        |
        v
Takeover Certification reconciliation
```

The candidate must not author the criteria, answer them, and unilaterally mark itself PASS without an independent evaluation basis.

## Q1-Q5 semantic target

### Q1 — Production path

Require the actual current production/source trace: relevant source/module/function path, state owner, consumer and output/publication boundary as applicable.

### Q2 — Engineering reconstruction

Where the domain permits concrete reasoning, require real supplied values/payload, units, equation/logic, intermediate result and predicted outcome. A generic prompt such as "explain the engineering problem" is not sufficient qualification by itself.

### Q3 — Boundary and falsifier

Require an authority/input/failure mutation, the invariant that must remain true, and an explicit observation that would falsify the candidate's understanding.

### Q4 — Independent verification

Require an independent oracle/reconstruction. Quantitative work should carry actual payload, expected result, tolerance and independence basis where applicable.

### Q5 — First safe slice

Require exact target files/domains, first implementation action, acceptance/test IDs, predicted before/after or verification result, and stop/reconciliation condition.

## Rejection rules

Reject:

- historical-domain anchors;
- unknown IDs;
- wrong focus;
- packs testing mainly the previous phase;
- a phase target different from the incoming EP;
- missing material-boundary trigger when the incoming contract crosses a documented qualification boundary;
- answers that repeat question wording without demonstrating the required trace/calculation/falsifier/oracle/first slice;
- qualification receipts without a durable independent evaluation basis.

The current kernel validator still checks question-set structure/grounding rather than the full evaluated receipt. WP-03 implements this target after semantic EP and takeover certification are proven.