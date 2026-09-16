# Physics V2 — Pedagogy, Calibration & Dual-Track Product Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Physics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Consolidates**: Dual-Track Product Model, Self-Teaching vs Self-Tutoring, Generation Calibration, and Technical Composition for Physics.
> **Subject**: `PHYSICS` only.

---

## 1. Dual-Track Architecture: SDU vs. LAU

The Physics V2 architecture enforces a strict separation between **intrinsic concept difficulty** and **learner-adaptive practice**:

```text
                           CANONICAL DOMAIN MODEL
            physical models • equations • derivations • coordinate frames
            misconceptions • learning atoms • problem families
            frozen Core2 questions • canonical solutions
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
          STUDY-MATERIAL TRACK               QUESTION TRACK
            Core1A / Core1B                  Core2A / Core2B
                 │                                 │
                 ▼                                 ▼
      STUDY DIFFERENTIATION UNIT          LEARNER ADAPTATION UNIT
               SDU                                  LAU
                 │                                 │
     intrinsic EASY/MEDIUM/HARD          knowledge % OR owner override
     NO learner % may alter depth        + task demand + purpose
                 │                                 │
                 ▼                                 ▼
           CONCEPT TTU FAMILY                 PROBLEM TTU FAMILY
            ┌────┴────┐                        ┌────┴────┐
            ▼         ▼                        ▼         ▼
          Core1A    Core1B                   Core2A    Core2B
         COMPLETE  RECONSTRUCTIVE           COMPLETE  RECONSTRUCTIVE
```

### Non-Conflation Invariants
- **Core1A / Core1B (SDU)**: Governed strictly by the **Subtopic Difficulty Badge** (`EASY | MEDIUM | HARD`). Learner diagnostic percentage ($0–100\%$) MUST NOT alter Core1 theoretical depth, page ceilings, or physical model rigor.
- **Core2A / Core2B (LAU)**: Governed by the **Learner Knowledge Percentage** (or explicit Owner Waiver) combined with question task demand, problem family, and learning purpose.

---

## 2. Declarative Self-Teaching (A) vs. Reconstructive Self-Tutoring (B)

```text
A-Stages (Core1A, Core2A): Explanation-First / Declarative Self-Teaching
  → Complete physical exposition, resolved free-body diagrams, step-by-step calculus derivations,
    dimensional homogeneity checks, verified numerical answer keys.
  → Canonical completed state of physical models.

B-Stages (Core1B, Core2B): Elicitation-First / Open-Ended Self-Tutoring
  → Open question → Try / Predict / Sketch → Reveal hint → Reconstruct → Verify.
  → Active learner reconstruction state via incomplete Reconstructable TTUs.
```

### The Invariant of B-Layer Production
A B-layer product must require **active learner physical production** (drawing missing vectors, identifying reference frames, completing energy balance terms, calculating limiting conditions). It is strictly NOT an A-layer page with answers obscured or text removed. Open-ended B-pages require explicit technical workspaces plus verified derivation keys.

---

## 3. Generation Calibration & Research Obligations

### Core1A/Core1B Difficulty Badges

| Badge | Page Ceiling | Pedagogy Web Research | Internal Decomposition | Representation Budget |
|---|---:|---|---|---|
| **EASY** | 10 pages | Optional (default absent; full custody if used) | Subtopic only | Step-by-step FBDs, scalar diagrams |
| **MEDIUM** | 20 pages | Mandatory targeted brief & web references | Sub-subtopics allowed | High density, resolved 2D vectors, energy bars |
| **HARD** | 30 pages | Mandatory deep brief & web references | Sub-subtopics allowed | Deep representations, cross-frame transforms |

*Note: Page counts are strict ceilings, not targets. Source count is never a proxy for quality.*

### Core2A/Core2B Learner Calibration
Generation requires either:
1. **Known Knowledge %**: Valid percentage ($0–100\%$) bound to an explicit source reference and named calibration policy.
2. **Unknown Knowledge %**: Explicit Owner Waiver with a recorded pedagogical justification and owner-selected profile/demand ceilings.

*Providing both percentage and waiver, or providing neither, blocks generation closed.*

---

## 4. Reconstructable Technical Task Units (TTUs) for Physics

A **Reconstructable TTU** is a bounded technical object comprising:
1. A learner-facing incomplete state with explicit missing components.
2. A specific physical reconstruction target.
3. A verified completion key matching exactly the missing parts.

### Supported TTU Kinds in Physics
- `INCOMPLETE_FBD`: Unresolved force vectors, missing normal reactions, tension vectors, friction arrows, or reference axes.
- `ENERGY_ACCOUNTING_BAR`: Work-energy bar graphs with missing potential ($U$), kinetic ($K$), or non-conservative work ($W_{\text{nc}}$) slices.
- `RAY_TRACING_FRAME`: Optical diagrams with missing principal rays, refractive interfaces, or image focus points.
- `MOTION_GRAPH_CANVAS`: Position-time ($s\text{-}t$), velocity-time ($v\text{-}t$), or acceleration-time ($a\text{-}t$) graphs with missing slope or area interpretations.
- `EQUATION_SKELETON`: Algebraic conservation or dynamic balance frames requiring variable substitution and SI unit consistency.
- `CIRCUIT_SCHEMATIC_FRAME`: Electrical circuit with missing branch currents, loop potentials (KVL/KCL), or component labels.

### Cognitive Fading Sequence
```text
MODELLED (Complete physical worked example with verified free-body diagram)
    ↓
GUIDED (Step-by-step vector scaffolding with partial equation skeleton)
    ↓
FADED (Minimal coordinate axes and boundary constraints)
    ↓
INDEPENDENT (Pure physical scenario statement with independent workspace)
```

### Viewport & Diagram Integrity
- Every diagram, graph, ray trace, and vector diagram must define a bounded viewport and set `clip_to_viewport = true`.
- Vectors and rays must never draw across margins or overflow into surrounding textual explanations.

---

## 5. Academician Pedagogical Alignment Matrix (Grades 9–11)

| Examination | Target Domains | Learner Pitfalls | Architectural Enforcement |
|---|---|---|---|
| **CBSE Board (9-10)** | 1D kinematics, Newton's laws, Work-energy scalar, Ray optics, Ohm's law | Confusing mass with weight; treating normal force as always equal to $mg$; forgetting sign convention in mirror formula | Core1A SDU enforces strict coordinate sign conventions and explicit normal force balance derivations. |
| **NSEP Olympiad (9-11)** | Fluid dynamics, Archimedes principle, Surface tension, Variable mass, Dimensional analysis | Neglecting non-inertial pseudo forces; applying Bernoulli across differing streamlines with vorticity | Core1A and Core2B enforce explicit reference frame declarations and streamline irrotationality preconditions. |
| **JEE Main (11)** | Projectile motion, Friction dynamics, Work-energy theorem, Center of mass, Hooke's law | Misapplying mechanical energy conservation when friction does work; confusing static vs kinetic friction | Engineering Gates enforce $W_{\text{nc}} = 0$ invariant before allowing $K_i + U_i = K_f + U_f$. |
| **JEE Advanced (11)** | Rigid body rotation, Angular momentum conservation, Bernoulli with viscosity, SHM superposition | Assuming angular momentum is conserved about an arbitrary non-inertial origin; neglecting rolling friction work | Core2B LAU transfer demand enforces structural variation without altering frozen source questions. |

---

## 6. Executable Contracts, Engines & Test Suites

| Component | Executable File | Purpose |
|---|---|---|
| **Technical Teaching Unit Schema** | `contracts/technical-teaching-unit.schema.json` | Normative TTU schema |
| **CDAU / SDU / LAU Schemas** | `contracts/canonical-domain-admission-unit.schema.json` | SDU and LAU contracts |
| **Composition Plan Schema** | `contracts/m2d-composition-plan.schema.json` | Layout and page composition contract |
| **TTU Validator** | `engine/validate_technical_teaching_unit.py` | Validates complete vs reconstructive TTUs |
| **B-Layer Boundary Validator** | `engine/validate_b_layer_boundary.py` | Strict A vs B layer boundary enforcement |
| **Render Readiness Compiler** | `engine/compile_m2d_render_readiness.py` | Viewport clipping and composition check |
| **Test Suites** | `tests/test_blueprint_cdau_sdu_lau_ttu_v7.py`, `tests/test_blueprint_b_layer_boundary.py` | Automated unit test batteries |
