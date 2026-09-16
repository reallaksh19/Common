# Phase transitions and Q1-Q5

A phase transition occurs when the recomputed executable frontier moves into another phase. It requires a fresh incoming-phase question set derived from the new EP. Same-phase progression does not require a new Q1-Q5 pack unless the technical/authority boundary materially changes.

Each question has a fixed focus and explicit durable anchors from the incoming EP:

```yaml
phase_transition:
  required: true
  from_phase: PHASE-001
  to_phase: PHASE-002
  questions:
    - id: Q1
      focus: PRODUCTION_PATH
      anchors: [PHASE-002, WP-020]
      question: "<trace the incoming production path>"
    - id: Q2
      focus: ENGINEERING_PROBLEM
      anchors: [WP-020, INPUT-01]
      question: "<explain the incoming implementation problem>"
    - id: Q3
      focus: BOUNDARIES_INVARIANTS
      anchors: [WP-020, AC-01]
      question: "<state change boundaries and invariants>"
    - id: Q4
      focus: VERIFICATION
      anchors: [AC-01, TEST-01]
      question: "<explain independent verification>"
    - id: Q5
      focus: FIRST_SAFE_SLICE
      anchors: [STEP-01, AC-01]
      question: "<identify the first bounded contribution>"
```

Valid anchors are incoming phase/work-package IDs plus IDs declared by the incoming EP's inputs, acceptance criteria, validation plan and implementation steps. Q4 must anchor to verification/acceptance. Q5 must anchor to an implementation step or acceptance criterion.

Reject historical-domain anchors, unknown IDs, wrong focus, a `to_phase` different from the incoming EP, or packs that primarily test the previous phase. The question pack tests readiness for the next implementation; it is not a reusable domain trivia exam.