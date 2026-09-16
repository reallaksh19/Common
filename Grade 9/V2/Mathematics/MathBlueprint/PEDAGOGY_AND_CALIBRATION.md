# Mathematics V2 — Pedagogy, Calibration & Dual-Track Product Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Mathematics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Consolidates**: `DUAL_TRACK_PRODUCT_MODEL.md`, `SELF_TEACHING.md`, `GENERATION_CALIBRATION.md`, and `TECHNICAL_COMPOSITION.md`.
> **Subject**: `MATHEMATICS` only.

---

## 1. Dual-Track Architecture: SDU vs. LAU

The Mathematics V2 architecture enforces a strict separation between **intrinsic concept difficulty** and **learner-adaptive problem solving**:

```text
                           CANONICAL DOMAIN MODEL
            concepts • equations • derivations • models • representations
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

### Non-Conflation Invariant
- **Core1A / Core1B (SDU)**: Governed strictly by the **Subtopic Difficulty Badge** (`EASY | MEDIUM | HARD`). Learner diagnostic percentage ($0–100\%$) MUST NOT alter Core1 depth, page ceilings, or mathematical obligations.
- **Core2A / Core2B (LAU)**: Governed by the **Learner Knowledge Percentage** (or explicit Owner Waiver) combined with question task demand, problem family, and learning purpose.

---

## 2. Declarative Self-Teaching (A) vs. Reconstructive Self-Tutoring (B)

```text
A-Stages (Core1A, Core2A): Explanation-First / Declarative Self-Teaching
  → Complete conceptual exposition, worked examples, explicit symbol bridges, verified answer checks.
  → Canonical completed state of mathematical objects.

B-Stages (Core1B, Core2B): Elicitation-First / Open-Ended Self-Tutoring
  → Open question → Try / Predict / Sketch → Reveal hint → Reconstruct → Verify.
  → Active learner reconstruction state via incomplete Reconstructable TTUs.
```

### The Invariant of B-Layer Production
A B-layer product must require **active learner mathematical production**. It is strictly NOT an A-layer page with answers obscured or text removed. Open-ended B-pages require explicit technical workspace plus verified derivation keys.

---

## 3. Generation Calibration & Research Obligations

### Core1A/Core1B Difficulty Badges

| Badge | Page Ceiling | Pedagogy Web Research | Internal Decomposition | Representation Budget |
|---|---:|---|---|---|
| **EASY** | 10 pages | Optional (default absent; full custody if used) | Subtopic only | Step-by-step diagrams |
| **MEDIUM** | 20 pages | Mandatory targeted brief & web references | Sub-subtopics allowed | High density, dedicated diagrams |
| **HARD** | 30 pages | Mandatory deep brief & web references | Sub-subtopics allowed | Deep representations, contrast tables |

*Note: Page counts are strict ceilings, not targets. Source count is never a proxy for quality.*

### Core2A/Core2B Learner Calibration
Generation requires either:
1. **Known Knowledge %**: Valid percentage ($0–100\%$) bound to an explicit source reference and named calibration policy.
2. **Unknown Knowledge %**: Explicit Owner Waiver with a recorded pedagogical justification and owner-selected profile/demand ceilings.

*Providing both percentage and waiver, or providing neither, blocks generation closed.*

---

## 4. Reconstructable Technical Task Units (TTUs)

A **Reconstructable TTU** is a bounded technical object comprising:
1. A learner-facing incomplete state with explicit missing parts.
2. A specific reconstruction target.
3. A verified completion key matching exactly the missing parts.

### Supported TTU Kinds
- `INCOMPLETE_DIAGRAM`: Incomplete geometric figures, coordinate grids, auxiliary line prompts.
- `COMPONENT_MODEL`: Functional component diagrams, algebraic area models.
- `EQUATION_SKELETON`: Incomplete algebraic identities, factoring frames, Vieta coefficient bridges.
- `TABLE_SKELETON`: Sign analysis grids, discriminant trichotomy tables, truth value sets.
- `PROOF_REASONING_CHAIN`: Step-reason deductive scaffolds, Euclid lemma justifications.

### Cognitive Fading Sequence
```text
MODELLED (Complete worked example)
    ↓
GUIDED (Step hints and partial skeleton)
    ↓
FADED (Minimal scaffold with boundary constraints)
    ↓
INDEPENDENT (Pure problem statement with verification workspace)
```

### Viewport & Geometry Integrity
- Every diagram, graph, and TTU must define a bounded viewport and set `clip_to_viewport = true`.
- Mathematical curves and loci must never draw across margins or overflow into text areas.

---

## 5. Academician Pedagogical Alignment Matrix (Grades 9–11)

| Examination | Target Domains | Learner Pitfalls | Architectural Enforcement |
|---|---|---|---|
| **CBSE/ICSE Board (9-10)** | Linear systems, Euclid division, quadratics, basic circle theorems | Sign errors, premature division by variable, confusing line with line segment | Core1A SDU locks algebraic step-by-step proof; enforces $|x| = \sqrt{x^2}$. |
| **IOQM / Olympiad (9-11)** | Synthetic geometry, cyclic quads, Thales/BPT, Vieta polynomials | Blind formula memorization; inability to construct auxiliary lines | Reconstructable TTUs provide incomplete geometric diagrams requiring auxiliary constructions. |
| **JEE Main (11)** | Discriminant trichotomy, common roots, conic properties, limits | Operating outside validity domains; forgetting leading coefficient $a \ne 0$ | Engineering Gates enforce non-negotiable preconditions upstream of task generation. |
| **JEE Advanced (11)** | Location of roots, complex loci, composite derivatives, Bayes' theorem | Inability to synthesize cross-domain methods (e.g. geometry with algebra) | Core2B LAU transfer demand enforces structural variation without altering frozen source questions. |

---

## 6. Executable Contracts, Engines & Test Suites

| Component | Executable File | Purpose |
|---|---|---|
| **Self-Teaching Contract** | `contracts/math-self-teaching-contract.schema.json` | Stage pedagogical contract schema |
| **Generation Spec Schema** | `contracts/math-self-teaching-generation-spec.schema.json` | SDU/LAU generation specification |
| **Page Blueprint Schema** | `contracts/math-learner-page-blueprint.schema.json` | Validated page composition contract |
| **B-Layer Integration** | `contracts/math-b-layer-integration.schema.json` | B-layer compiler integration contract |
| **Self-Teaching Validator** | `engine/validate_self_teaching_contract.py` | Stage contract validator |
| **Generation Spec Validator** | `engine/validate_self_teaching_generation_spec.py` | Difficulty & calibration validator |
| **Page Blueprint Validator** | `engine/validate_learner_page_blueprint.py` | TTU & layout composition validator |
| **Test Suites** | `tests/test_self_teaching_*.py`, `tests/test_technical_composition.py` | Automated unit test batteries |
