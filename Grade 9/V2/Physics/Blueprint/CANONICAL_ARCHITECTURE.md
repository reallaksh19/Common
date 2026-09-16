# Physics V2 — Canonical Six-Core Architecture

This document is the canonical target architecture for Physics V2. It sits above the existing executable Physics Blueprint increments and the dual-track product model. Existing validators/contracts remain implementation assets, but future schema/engine work must converge on this architecture rather than treating earlier one-axis adaptation assumptions as canonical.

The governing invariants remain:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.

PLANNED PEDAGOGY
!= COMPILED STATIC PRODUCT
!= RENDERED ARTIFACT
!= LEARNER ATTEMPT
!= LEARNER PERFORMANCE EVIDENCE
```

## Consolidated Specification Architecture

The Physics V2 canonical architecture is organized into a single governing root specification and four strictly bounded subordinate normative modules:

- **Root Architectural Specification**:
  - [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md): System topology, authority hierarchy, Core0–Core2 lifecycle, join, SDU/LAU, and publication boundary.
- **Subordinate Normative Modules**:
  1. [`ENGINEERING_AUTHORITY.md`](ENGINEERING_AUTHORITY.md): Upstream Engineering Gates, Transitive Closure, Non-Authoritative Discovery Boundary, and Exact Custody Binding across 43 Gates.
  2. [`PEDAGOGY_AND_CALIBRATION.md`](PEDAGOGY_AND_CALIBRATION.md): Dual-Track Model (SDU vs LAU), Declarative Self-Teaching (A) vs Reconstructive Self-Tutoring (B), Difficulty Badges, and Reconstructable Physical TTUs.
  3. [`PRODUCT_GOVERNANCE_GATE.md`](PRODUCT_GOVERNANCE_GATE.md): Coverage Ledger, Cross-Core Similarity Auditing, Anti-Gaming Invariants, and Publication Freeze Criteria.
  4. [`SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md`](SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md): Subtopic Intelligence Library (SIL) 4-Layer Intake Architecture, Verification Gates, and Concrete Subtopic Foundation Packets.
- **Derived Observability & Tooling**:
  - [`tools/index.html`](tools/index.html): Unified Observability Workbench Portal
  - [`tools/run_builder/index.html`](tools/run_builder/index.html): PhysicsBlueprint Run Builder
  - [`tools/architecture_explorer/index.html`](tools/architecture_explorer/index.html): Blueprint Architecture Explorer
  - [`benchmarks/discovery/index.html`](benchmarks/discovery/index.html): Discovery Benchmark Quality Explorer
  - [`CORE_ARCHITECTURE_DRIFT_AUDIT.md`](CORE_ARCHITECTURE_DRIFT_AUDIT.md): 17-Section Normative Consistency Audit & Academician Matrix

---

## 1. Canonical System Topology

```text
OWNER CONTROL PLANE
purpose • policy • difficulty override • routing override • inclusion/exclusion
learner-% waiver • support override • release/hold
        |
        v
ORIGINAL GROUND TRUTH
questions • syllabus • authoritative sources • figures • answers • owner scope
        |
        v
CORE0 — EVIDENCE + ROUTE
        |
        +-----------------------------+
        |                             |
        v                             v
CORE1 FIRST                      CORE2 FIRST
semantic reconstruction          assessment reconstruction
        |                             |
        v                             v
K-* packets                      D-* packets
instance ends                    instance ends
        |                             |
        v                             v
fresh CORE2                      fresh CORE1
independent GT pass              independent GT pass
        |                             |
        +-------------+---------------+
                      v
              C1 ⋈ C2 JOIN / AUDIT
                      |
                      v
            CANONICAL DOMAIN REGISTRY
concepts • models • equations • derivations • learning atoms
representations • misconceptions • problem families • frozen questions
canonical solutions • capabilities • validity • provenance
                      |
                      v
                    CDAU
       cross-core differentiation + lineage + owner governance
                      |
          +-----------+-----------+
          |                       |
          v                       v
         SDU                     LAU
Study Differentiation       Learner Adaptation
Core1A / Core1B             Core2A / Core2B
intrinsic difficulty        knowledge % OR owner override
NO learner-% depth          • task demand • family • purpose
          |                       |
          v                       v
      CONCEPT TTUs             PROBLEM TTUs
       +-----+                  +-----+
       |     |                  |     |
       v     v                  v     v
    Core1A Core1B            Core2A Core2B
    complete reconstructive  complete reconstructive
       |     |                  |     |
       +--+--+                  +--+--+
          |                       |
          v                       v
      SELF-HELP CLOSURE       SELF-HELP CLOSURE
          +-----------+-----------+
                      v
              PRODUCT GOVERNANCE
        coverage • similarity • anti-gaming
        badge meaning • release integrity
                      |
                      v
           PUBLICATION / COMPOSITION
            page count from structure
          NOT decorative spacing/padding
                      |
                      v
                   RELEASE
```

---

## 2. Core Authority Hierarchy

1. **Ground Truth / Source Evidence**: Immutable foundation. Questions, answers, and authoritative sources are never modified.
2. **Engineering Gate Authority**: Canonical Registry of 43 Gates (`physics-technical-engineering-gates.v1.json`). Preconditions, invariants, and representations must be satisfied.
3. **Non-Authoritative Candidate Discovery**: Broad semantic search over formulas, aliases, Hindi transliterations, and abbreviations. Never confers engineering authorization.
4. **Exact Gate Selection**: Confirmed exact identifier binding before downstream synthesis.
5. **CDAU / SDU & LAU**: Intrinsic difficulty isolation for Core1; calibrated practice adaptation for Core2.
6. **Publication & Rendering**: Composition-only rendering; no semantic mutation.
