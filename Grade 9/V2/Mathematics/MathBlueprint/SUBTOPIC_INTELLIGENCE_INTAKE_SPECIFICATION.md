# Mathematics V2 — Subtopic Intelligence Intake Specification & Foundation Packet Blueprint

> **ACADEMICIAN PEDAGOGICAL SPECIFICATION**: Architecture for the Subtopic Intelligence Library (SIL).
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Subordinate Modules**: [`ENGINEERING_AUTHORITY.md`](ENGINEERING_AUTHORITY.md), [`PEDAGOGY_AND_CALIBRATION.md`](PEDAGOGY_AND_CALIBRATION.md), [`PRODUCT_GOVERNANCE_GATE.md`](PRODUCT_GOVERNANCE_GATE.md).
> **Target Audience**: Expert academicians, curriculum architects, and automated pedagogical compiler engines.
> **Subject**: `MATHEMATICS` (Grades 9–11: CBSE/ICSE, IOQM/RMO, JEE Main, JEE Advanced).

---

## 1. Pedagogical Scope & Objectives

The transition from Grade 9 foundations to senior competitive examinations (IIT-JEE Advanced, IOQM/RMO) represents a sharp cognitive discontinuity. Students fail not because they lack formulas, but because:
1. **Formula Blindness**: They memorize results (e.g. $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$) without internalizing structural preconditions ($a \neq 0$, domain constraints on radicals).
2. **Missing Auxiliary Reconstruction**: In synthetic geometry and multi-step algebra, they cannot introduce the necessary auxiliary lines, substitutions, or coordinate axes.
3. **Parametric Fragility**: When parameters vary (e.g. location of roots $af(k) > 0$), they rely on algebraic rote rather than geometric parabola morphology.

The **Subtopic Intelligence Library (SIL)** bridges this gap by transforming raw mathematical syllabus topics into **executable, schema-validated knowledge packets** that feed directly into the SDU (Core1A/Core1B) and LAU (Core2A/Core2B) compilers without changing upstream Engineering authority.

---

## 2. Four-Layer Subtopic Intelligence Packet Architecture

Every subtopic admitted to the library is structured as a typed 4-layer intelligence packet:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: MATHEMATICAL CORE & NON-NEGOTIABLE PRECONDITIONS              │
│ • Axiomatic definitions • Domain validity conditions (e.g. a ≠ 0)       │
│ • Mandatory invariant equations • Algebraic identity boundaries         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ feeds
┌───────────────────────────────────▼────────────────────────────────────┐
│ LAYER 2: COGNITIVE TRANSFORMATIONS & LEARNING ATOM DAG                 │
│ • Atomic concepts (CONCEPT, RELATION, INVARIANT, PROCEDURE, STRATEGY)   │
│ • Symbol bridges (formal math notation ↔ intuitive geometric meaning)   │
│ • Misconception repair contrasts (flawed logic ↔ correct diagnostic cue)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ concretizes
┌───────────────────────────────────▼────────────────────────────────────┐
│ LAYER 3: RECONSTRUCTABLE TTU LIBRARY (TECHNICAL TASK UNITS)            │
│ • Incomplete diagrams with missing auxiliary constructions             │
│ • Equation skeletons with factoring frames & coefficient blanks        │
│ • Bounded viewports (clip_to_viewport = true)                          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ exercises
┌───────────────────────────────────▼────────────────────────────────────┐
│ LAYER 4: PROBLEM FAMILIES & TRANSFER DISCRIMINATION                    │
│ • Canonical worked exemplars (Core1A) • Faded self-tutors (Core1B)    │
│ • Expert solution anatomy (Core2A)   • Open transfer challenges (Core2B)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Concrete Exemplar Packet: Quadratic Equations (`MATH-QUAD-EQUATIONS`)

Below is the canonical reference implementation of a Subtopic Intelligence Packet for **Quadratic Equations & Theory of Equations** across Grades 9–11.

### 3.1 Layer 1: Mathematical Core & Non-Negotiable Invariants

- **Canonical Subtopic ID**: `MATH-QUAD-EQUATIONS`
- **Engineering Gate Binding**: `MATH-QUAD-EQUATIONS` (Digest-bound closure receipt)
- **Learner Title**: Quadratic Equations, Discriminant Analysis & Theory of Equations
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Leading Coefficient Invariant**: For $ax^2 + bx + c = 0$, $a \neq 0$ must be explicitly asserted before computing roots, discriminant, or axis of symmetry. If $a = 0$, the equation degrades to a linear relation $bx + c = 0$.
  2. **Radical Non-Negativity Invariant**: The principal square root $\sqrt{\Delta}$ is non-negative by definition. In real analysis, $\Delta \ge 0$ is required for real roots; $\sqrt{x^2} = |x|$, not merely $x$.
  3. **Fundamental Theorem of Algebra**: A quadratic polynomial with real or complex coefficients has exactly two roots (counting multiplicity) in $\mathbb{C}$.

### 3.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-QUAD-01` (`CONCEPT`): Quadratic polynomial as a parabolic mapping $f(x) = ax^2 + bx + c$ with vertex at $\left(-\frac{b}{2a}, -\frac{D}{4a}\right)$.
- `ATOM-QUAD-02` (`RELATION`): Vieta's formulas: $\alpha + \beta = -\frac{b}{a}$, $\alpha\beta = \frac{c}{a}$.
- `ATOM-QUAD-03` (`INVARIANT`): Discriminant trichotomy: $D = b^2 - 4ac$. $D > 0 \iff$ two distinct real roots; $D = 0 \iff$ coincident real roots; $D < 0 \iff$ complex conjugate pair roots.
- `ATOM-QUAD-04` (`PROCEDURE`): Symmetric algebraic reduction: expressing $\alpha^2 + \beta^2 = (\alpha+\beta)^2 - 2\alpha\beta$ and $\alpha^3 + \beta^3 = (\alpha+\beta)^3 - 3\alpha\beta(\alpha+\beta)$.
- `ATOM-QUAD-05` (`STRATEGY`): Location of roots via composite interval testing:
  - Both roots greater than $k$: $D \ge 0$, $-\frac{b}{2a} > k$, and $a \cdot f(k) > 0$.
  - Roots on opposite sides of $k$: $a \cdot f(k) < 0$ (automatically guarantees $D > 0$).

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Middle term split"* | $ax^2 + px + qx + c = 0$ where $p+q=b, pq=ac$ | Factoring via grouping based on distributive law. |
| *"Both roots positive"* | $\alpha > 0, \beta > 0 \iff D \ge 0, S > 0, P > 0$ | Combining discriminant, sum, and product constraints. |
| *"Sign of quadratic"* | $\operatorname{sgn}(ax^2+bx+c) = \operatorname{sgn}(a)$ for $x \notin [\alpha, \beta]$ | Parabolic curvature and interval positivity/negativity. |

#### C. Misconception Contrasts
1. **Misconception: Premature Cancellation of Variable**:
   - *Flawed Action*: Solving $x^2 = 5x$ by dividing both sides by $x \implies x = 5$.
   - *Correct Diagnostic Cue*: Dividing by $x$ assumes $x \neq 0$, silently destroying root $x = 0$. Factor as $x(x - 5) = 0 \implies x \in \{0, 5\}$.
2. **Misconception: Omitting Parameter Non-Zero Check**:
   - *Flawed Action*: Stating $(m-2)x^2 + 4x + 1 = 0$ has two roots when $D \ge 0$.
   - *Correct Diagnostic Cue*: If $m = 2$, the equation is $4x + 1 = 0$, having only one root $x = -1/4$. The condition $m \neq 2$ is an essential independent constraint.
3. **Misconception: Root Location without Axis Position**:
   - *Flawed Action*: For both roots $> k$, only checking $D \ge 0$ and $af(k) > 0$.
   - *Correct Diagnostic Cue*: $af(k) > 0$ holds when both roots are greater than $k$ OR when both roots are less than $k$. The axis condition $-\frac{b}{2a} > k$ is mandatory to orient the parabola.

---

### 3.3 Layer 3: Reconstructable TTU Library

#### TTU-QUAD-01: Incomplete Factoring Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Solve for x: 2x² - 7x + 3 = 0
Step 1: Identify product ac = [ ___ ] and sum b = [ ___ ]
Step 2: Find factors p, q such that p·q = ac and p + q = b:
        p = [ ___ ],  q = [ ___ ]
Step 3: Split middle term: 2x² - [ ___ ]x - [ ___ ]x + 3 = 0
Step 4: Group terms: 2x(x - [ ___ ]) - 1(x - [ ___ ]) = 0
Step 5: Factor out common binomial: (2x - 1)(x - [ ___ ]) = 0
Roots: x = [ ___ ] or x = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: ac = 6, b = -7
Step 2: p = -6, q = -1
Step 3: 2x² - 6x - 1x + 3 = 0
Step 4: 2x(x - 3) - 1(x - 3) = 0
Step 5: (2x - 1)(x - 3) = 0
Roots: x = 1/2, x = 3
```

#### TTU-QUAD-02: Parabolic Location-of-Roots Geometric Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-4, 6], y ∈ [-5, 10], clip_to_viewport = true
Object: Parabola f(x) = x² - 2(k-1)x + (k+5)
Target Condition: Find parameter k such that both roots are strictly greater than 2.

[INCOMPLETE GEOMETRIC TTU]
Condition Checklist:
1. Real roots exist:              D = 4(k-1)² - 4(k+5) ≥ 0   ==> k ∈ [ ___ , ___ ] ∪ [ ___ , ___ ]
2. Axis of symmetry to the right: -b/(2a) = (k-1) > 2        ==> k > [ ___ ]
3. Function value at boundary:    f(2) = 4 - 4(k-1) + (k+5) > 0 ==> k < [ ___ ]

[COMPLETION DERIVATION KEY]
1. 4(k² - 2k + 1 - k - 5) = 4(k² - 3k - 4) ≥ 0 ==> (k - 4)(k + 1) ≥ 0 ==> k ≤ -1 or k ≥ 4
2. k - 1 > 2 ==> k > 3
3. 4 - 4k + 4 + k + 5 = 13 - 3k > 0 ==> 3k < 13 ==> k < 13/3 (4.33)
Intersection: (k ≤ -1 or k ≥ 4) ∩ (k > 3) ∩ (k < 13/3)
Result: k ∈ [4, 13/3)
```

---

### 3.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-QUAD-01 (Foundation / CBSE):
  Standard algebraic factoring, discriminant classification, and quadratic formula application.
FAMILY-QUAD-02 (Olympiad / IOQM):
  Nonlinear symmetric systems, Newton's sums (S_n = α^n + β^n satisfying a·S_n + b·S_{n-1} + c·S_{n-2} = 0),
  and integer root constraints via discriminant perfect square analysis.
FAMILY-QUAD-03 (JEE Main):
  Quadratic inequalities with sign charts, common root condition (determinant eliminant method),
  and equations reducible to quadratics via substitution (e.g. t = x + 1/x).
FAMILY-QUAD-04 (JEE Advanced):
  Parametric root location intervals, modulus and logarithmic quadratics, and simultaneous
  extremum analysis combining calculus with discriminant geometry.
```

---

## 4. Intake Validation Checklist for Future Subtopics

To admit any new mathematics subtopic into the library, it must pass this 6-point intake gate:

1. **Exact Precondition Proof**: Mathematical domain boundaries (denominators $\neq 0$, radicands $\ge 0$, leading coefficients $\neq 0$) must be formally declared in Layer 1.
2. **Atomic Decomposition**: The topic must be factored into at least 4 typed Learning Atoms in Layer 2.
3. **Misconception Pairings**: At least 2 verified student misconceptions with diagnostic contrasts must be articulated.
4. **Reconstructable TTU Pair**: At least one complete Concept TTU and one reconstructive Problem TTU with explicit completion keys must be authored in Layer 3.
5. **Exam Family Mapping**: Clear mapping to at least 2 distinct competitive examination families (e.g. CBSE + JEE Main, or IOQM + JEE Advanced) must be provided in Layer 4.
6. **Zero Topic Hardcoding**: All metadata, terms, and rules must live in JSON data files; zero topic-specific branch logic may be added to Python engine code.
