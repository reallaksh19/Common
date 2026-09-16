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

## 4. Foundation Packet: Linear Systems & Consistency Criteria (`MATH-LIN-EQUATIONS`)

### 4.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-LIN-EQUATIONS`
- **Engineering Gate Binding**: `MATH-LIN-EQUATIONS` (Digest-bound closure receipt)
- **Learner Title**: Pair of Linear Equations in Two Variables, Consistency Ratios & Matrix Determinants
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Non-Degenerate Variable Constraint**: For each equation $a_i x + b_i y + c_i = 0$, the coefficient vector $(a_i, b_i) \neq (0, 0)$ must hold. A relation with $a_i = b_i = 0$ is either a contradiction ($c_i \neq 0 \implies 0 = 1$) or a trivial identity ($c_i = 0$).
  2. **Non-Zero Divisor Invariant in Ratio Form**: Direct comparison $\frac{a_1}{a_2} = \frac{b_1}{b_2} = \frac{c_1}{c_2}$ is valid only if $a_2, b_2, c_2 \neq 0$. In general, cross-multiplication determinant forms ($a_1 b_2 - a_2 b_1 = 0$, etc.) must be evaluated to prevent division by zero.
  3. **Solvability Invariant (Rouché-Capelli Theorem)**: A system $\mathbf{A}\mathbf{x} = \mathbf{b}$ is consistent if and only if $\operatorname{rank}(\mathbf{A}) = \operatorname{rank}([\mathbf{A}|\mathbf{b}])$.

### 4.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-LIN-01` (`CONCEPT`): Linear equation in two variables as an infinite set of ordered pairs $(x, y) \in \mathbb{R}^2$ geometrically forming a Euclidean straight line.
- `ATOM-LIN-02` (`RELATION`): Consistency classification trichotomy:
  - *Unique solution* (consistent & independent, intersecting lines) $\iff \frac{a_1}{a_2} \neq \frac{b_1}{b_2} \iff a_1 b_2 - a_2 b_1 \neq 0$.
  - *Infinitely many solutions* (consistent & dependent, coincident lines) $\iff \frac{a_1}{a_2} = \frac{b_1}{b_2} = \frac{c_1}{c_2}$.
  - *No solution* (inconsistent, distinct parallel lines) $\iff \frac{a_1}{a_2} = \frac{b_1}{b_2} \neq \frac{c_1}{c_2}$.
- `ATOM-LIN-03` (`PROCEDURE`): Algebraic resolution algorithms:
  - Substitution method: isolating one variable and evaluating univariate equation.
  - Elimination by equating coefficients: multiplying by suitable scale factors to cancel one variable.
  - Determinant / Cross-multiplication method: $x = \frac{b_1 c_2 - b_2 c_1}{a_1 b_2 - a_2 b_1}, y = \frac{c_1 a_2 - c_2 a_1}{a_1 b_2 - a_2 b_1}$ where $a_1 b_2 - a_2 b_1 \neq 0$.
- `ATOM-LIN-04` (`STRATEGY`): Rational substitution for reducible nonlinear systems: mapping $u = \frac{1}{x+y}, v = \frac{1}{x-y}$ subject to domain constraints $x \neq \pm y$.
- `ATOM-LIN-05` (`INVARIANT`): Homogeneous linear systems $a_1 x + b_1 y = 0, a_2 x + b_2 y = 0$ always possess the trivial solution $(0, 0)$; non-trivial solutions exist if and only if determinant $D = a_1 b_2 - a_2 b_1 = 0$.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Lines never cross"* | $\frac{a_1}{a_2} = \frac{b_1}{b_2} \neq \frac{c_1}{c_2} \iff \mathbf{n}_1 \parallel \mathbf{n}_2, c_1/c_2 \neq \lambda$ | Inconsistent system; empty intersection set $\emptyset$. |
| *"Same line written twice"* | $\operatorname{rank}(\mathbf{A}) = \operatorname{rank}([\mathbf{A}\mid\mathbf{b}]) = 1 < 2$ | Infinitely many solutions; 1-dimensional solution manifold. |
| *"Cross multiplication rule"* | $\frac{x}{b_1 c_2 - b_2 c_1} = \frac{-y}{a_1 c_2 - a_2 c_1} = \frac{1}{a_1 b_2 - a_2 b_1}$ | Determinant expansion of $2 \times 3$ augmented matrix. |

#### C. Misconception Contrasts
1. **Misconception: Blind Ratio Division with Zero Coefficients**:
   - *Flawed Action*: Evaluating consistency of $3x + 0y = 6$ and $6x + 0y = 12$ by computing $\frac{a_1}{a_2} = \frac{3}{6} = \frac{1}{2}$, and concluding system is undefined because $\frac{b_1}{b_2} = \frac{0}{0}$.
   - *Correct Diagnostic Cue*: Coefficient ratios are a shorthand for the cross-product determinant. Because $a_1 b_2 - a_2 b_1 = 3(0) - 6(0) = 0$ and $b_1 c_2 - b_2 c_1 = 0(-12) - 0(-6) = 0$, both lines represent the identical vertical line $x = 2$, yielding infinitely many solutions.
2. **Misconception: Inconsistent vs Coincident Confusion**:
   - *Flawed Action*: Concluding a system has no solution whenever $\frac{a_1}{a_2} = \frac{b_1}{b_2}$, ignoring the constant ratio $\frac{c_1}{c_2}$.
   - *Correct Diagnostic Cue*: Parallel slope only establishes identical orientation; the lines coincide (infinitely many solutions) if $\frac{c_1}{c_2}$ equals the slope ratio, and are parallel (no solution) only if $\frac{c_1}{c_2}$ differs.
3. **Misconception: Unchecked Rational Substitution Domains**:
   - *Flawed Action*: In solving $\frac{10}{x+y} + \frac{2}{x-y} = 4$, finding $x=3, y=3$ and accepting it without verification.
   - *Correct Diagnostic Cue*: If $x = y = 3$, $x - y = 0$, causing division by zero in the original ground truth equation. All candidates must be checked against domain preconditions.

### 4.3 Layer 3: Reconstructable TTU Library

#### TTU-LIN-01: Incomplete Algebraic Elimination Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Solve the linear system by elimination:
  (1)  3x + 4y = 10
  (2)  2x - 3y = 1

Step 1: Choose variable to eliminate: [ y ]
Step 2: Find LCM of coefficients of y: LCM(4, 3) = [ ___ ]
Step 3: Multiply equation (1) by [ ___ ]:  9x + 12y = [ ___ ]   ... (3)
Step 4: Multiply equation (2) by [ ___ ]:  8x - 12y = [ ___ ]   ... (4)
Step 5: Add equations (3) and (4):
        (9x + 8x) + (12y - 12y) = [ ___ ] + [ ___ ]
        [ ___ ]x = [ ___ ]
        x = [ ___ ]
Step 6: Substitute x into equation (1):
        3([ ___ ]) + 4y = 10  ==>  [ ___ ] + 4y = 10  ==>  4y = [ ___ ]  ==>  y = [ ___ ]
Solution Pair: (x, y) = ([ ___ ], [ ___ ])

[COMPLETION KEY - VERIFICATION ONLY]
Step 2: LCM = 12
Step 3: Multiply (1) by 3: 9x + 12y = 30
Step 4: Multiply (2) by 4: 8x - 12y = 4
Step 5: 17x = 34 ==> x = 2
Step 6: 3(2) + 4y = 10 ==> 6 + 4y = 10 ==> 4y = 4 ==> y = 1
Solution Pair: (x, y) = (2, 1)
```

#### TTU-LIN-02: Parameter Consistency Invariant Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-5, 5], y ∈ [-5, 5], clip_to_viewport = true
System:
  (1)  (k - 1)x + 3y = 2
  (2)  6x + (k + 2)y = k

Target Condition: Find parameter k such that the system has infinitely many solutions.

[INCOMPLETE GEOMETRIC TTU]
Consistency Conditions for Coincident Lines:
  a1 / a2 = b1 / b2 = c1 / c2
  (k - 1) / 6 = 3 / (k + 2) = 2 / k

Step 1: Solve determinant equation D = (k - 1)(k + 2) - 18 = 0
        k² + k - 2 - 18 = 0  ==>  k² + k - 20 = 0
        Factors: (k - [ ___ ])(k + [ ___ ]) = 0  ==>  k ∈ { [ ___ ], [ ___ ] }

Step 2: Test candidate k = 4 against constant ratio:
        a1/a2 = (4-1)/6 = 3/6 = 1/2
        b1/b2 = 3/(4+2) = 3/6 = 1/2
        c1/c2 = 2/4 = 1/2
        Is k = 4 valid? [ YES / NO ]

Step 3: Test candidate k = -5 against constant ratio:
        a1/a2 = (-5-1)/6 = -6/6 = -1
        b1/b2 = 3/(-5+2) = 3/(-3) = -1
        c1/c2 = 2/(-5) = -2/5
        Does -1 = -2/5? [ YES / NO ] ==> k = -5 yields: [ NO SOLUTION / INFINITE SOLUTIONS ]

[COMPLETION DERIVATION KEY]
Step 1: (k - 4)(k + 5) = 0 ==> k ∈ { 4, -5 }
Step 2: All three ratios equal 1/2. k = 4 produces coincident lines (YES).
Step 3: -1 ≠ -2/5. k = -5 produces parallel lines with NO solution.
Conclusion: Unique parameter for infinitely many solutions is k = 4.
```

### 4.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-LIN-01 (Foundation / CBSE):
  Two-variable elimination and substitution, graphical intersection points, upstream/downstream and fraction modeling.
FAMILY-LIN-02 (Olympiad / IOQM):
  Linear Diophantine equations ax + by = c with integer solutions via Euclidean algorithm, Bézout's identity,
  and non-negative integer lattice point counting.
FAMILY-LIN-03 (JEE Main):
  3-variable systems via Cramer's Rule (Δ, Δx, Δy, Δz), parameter intervals for unique vs non-trivial solutions,
  and homogeneous systems.
FAMILY-LIN-04 (JEE Advanced):
  Matrix rank deficiency, geometric planes intersecting in a line vs parallel planes, and parametric
  vector line representations in R³.
```

---

## 5. Foundation Packet: Triangles, Similarity & Thales' Theorem (`MATH-GEO-TRIANGLES`)

### 5.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-GEO-TRIANGLES`
- **Engineering Gate Binding**: `MATH-GEO-TRIANGLES` (Digest-bound closure receipt)
- **Learner Title**: Similar Triangles, Basic Proportionality Theorem (Thales) & Cevian Geometry
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Strict Triangle Inequality Invariant**: For three non-collinear vertices $A, B, C$, $AB + BC > AC$, $BC + CA > AB$, and $CA + AB > BC$ strictly. Equality implies collinear degenerate line segment with zero enclosed area ($\operatorname{Area}(\triangle ABC) = 0$).
  2. **Angle Sum Invariant in Euclidean Metric**: $\angle A + \angle B + \angle C = 180^\circ$ ($\pi$ radians).
  3. **Parallel Transversal Ratio Preservation (Thales' Axiom)**: If line $l \parallel BC$ intersects $AB$ at $D$ and $AC$ at $E$, then $\frac{AD}{DB} = \frac{AE}{EC}$.

### 5.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-TRI-01` (`CONCEPT`): Dilation and similarity: Two triangles $\triangle ABC$ and $\triangle DEF$ are similar ($\triangle ABC \sim \triangle DEF$) if and only if corresponding angles are equal ($\angle A = \angle D, \angle B = \angle E, \angle C = \angle F$) and corresponding sides are in a constant proportion $k = \frac{AB}{DE} = \frac{BC}{EF} = \frac{CA}{FD}$.
- `ATOM-TRI-02` (`INVARIANT`): Basic Proportionality Theorem (Thales' Theorem) and its converse: A line drawn parallel to one side of a triangle divides the other two sides in the same ratio; conversely, proportional division implies parallelism.
- `ATOM-TRI-03` (`RELATION`): Internal Angle Bisector Theorem: An interior angle bisector of a triangle divides the opposite side internally in the ratio of the adjacent sides containing the angle: $\frac{BD}{DC} = \frac{AB}{AC}$.
- `ATOM-TRI-04` (`PROCEDURE`): Quadratic area scaling: If $\triangle ABC \sim \triangle DEF$ with scale factor $k$, then $\frac{\operatorname{Area}(\triangle ABC)}{\operatorname{Area}(\triangle DEF)} = k^2 = \left(\frac{AB}{DE}\right)^2$.
- `ATOM-TRI-05` (`STRATEGY`): Auxiliary construction patterns:
  - Dropping perpendicular altitudes from common vertices to evaluate area ratios of triangles sharing a common base line.
  - Constructing parallel auxiliary lines through cevian intersections to transfer segment ratios across multiple triangles (Menelaus and Ceva foundations).

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Same shape, different size"* | Dilation under central homothety $\mathcal{H}_{O, k}$ | Conformal mapping preserving angle measure and scaling lengths by $k$. |
| *"BPT / Thales theorem"* | $DE \parallel BC \implies \frac{AD}{DB} = \frac{AE}{EC}$ and $\frac{AD}{AB} = \frac{AE}{AC} = \frac{DE}{BC}$ | Ratio preservation along transversals. |
| *"Area ratio theorem"* | $\frac{\operatorname{Area}_1}{\operatorname{Area}_2} = \left(\frac{s_1}{s_2}\right)^2 = \left(\frac{h_1}{h_2}\right)^2$ | 2D area scales with square of linear dimensions. |

#### C. Misconception Contrasts
1. **Misconception: Area Ratio Equals Side Ratio**:
   - *Flawed Action*: Stating that if the sides of a triangle are doubled ($k = 2$), its area is also doubled.
   - *Correct Diagnostic Cue*: Area is a two-dimensional measure: $\operatorname{Area} = \frac{1}{2} \cdot \text{base} \cdot \text{height}$. Because both base and altitude scale by factor $k$, area scales by $k^2 = 2^2 = 4$.
2. **Misconception: Blind Side Ratios Without Vertex Order Correspondence**:
   - *Flawed Action*: Given $\triangle ABC \sim \triangle DEF$, writing $\frac{AB}{EF} = \frac{BC}{DE}$.
   - *Correct Diagnostic Cue*: Similarity notation is strictly order-preserving. $\triangle ABC \sim \triangle DEF$ establishes canonical correspondence $A \leftrightarrow D, B \leftrightarrow E, C \leftrightarrow F$. Thus $\frac{AB}{DE} = \frac{BC}{EF} = \frac{CA}{FD}$.
3. **Misconception: Misapplying BPT to Arbitrary Non-Parallel Transversals**:
   - *Flawed Action*: Assuming $\frac{AD}{DB} = \frac{AE}{EC}$ holds for any arbitrary transversal segment $DE$.
   - *Correct Diagnostic Cue*: BPT strictly requires verified parallelism $DE \parallel BC$. Without verified parallelism or equiangular orientation, side ratios cannot be equated.

### 5.3 Layer 3: Reconstructable TTU Library

#### TTU-TRI-01: Incomplete Thales BPT Proof Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Theorem: If a line is drawn parallel to one side of a triangle intersecting the other two sides,
         it divides the two sides in the same ratio.
Given: In ΔABC, DE || BC, intersecting AB at D and AC at E.
To Prove: AD / DB = AE / EC

Construction:
  1. Join BE and [ ___ ].
  2. Draw altitude DM ⊥ AC and altitude EN ⊥ [ ___ ].

Proof Steps:
Step 1: Area(ΔADE) = 1/2 · base · height = 1/2 · AD · [ ___ ]
Step 2: Area(ΔBDE) = 1/2 · base · height = 1/2 · DB · [ ___ ]
Step 3: Ratio (1): Area(ΔADE) / Area(ΔBDE) = (1/2 · AD · EN) / (1/2 · DB · EN) = [ ___ ] / [ ___ ]

Step 4: Similarly, taking base AE and EC with altitude DM:
        Area(ΔADE) = 1/2 · AE · [ ___ ]
        Area(ΔCDE) = 1/2 · EC · [ ___ ]
Step 5: Ratio (2): Area(ΔADE) / Area(ΔCDE) = [ ___ ] / [ ___ ]

Step 6: Geometric Invariant:
        ΔBDE and ΔCDE are on the same base [ ___ ] and between the same parallel lines [ ___ ] and [ ___ ].
        Therefore: Area(ΔBDE) = Area([ ___ ])

Step 7: Equating Ratio (1) and Ratio (2):
        AD / DB = [ ___ ] / [ ___ ]   (Hence Proved)

[COMPLETION KEY - VERIFICATION ONLY]
Construction: 1. Join CD; 2. EN ⊥ AB
Step 1: EN
Step 2: EN
Step 3: AD / DB
Step 4: DM; DM
Step 5: AE / EC
Step 6: Same base DE; parallel lines DE and BC; Area(ΔCDE)
Step 7: AD / DB = AE / EC
```

#### TTU-TRI-02: Trapezoid Parallel Segment Ratio Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-1, 7], y ∈ [-1, 6], clip_to_viewport = true
Figure: Trapezoid ABCD with AB || CD. Diagonals AC and BD intersect at point O.
Target Condition: Prove that AO / OC = BO / OD, and if AB = 12, CD = 8, find AO : OC.

[INCOMPLETE GEOMETRIC TTU]
Step 1: Identify similar triangles:
        In ΔAOB and ΔCOD:
        ∠AOB = ∠COD  (Reason: [ _____________________ ])
        ∠OAB = ∠OCD  (Reason: [ _____________________ ])
        Therefore, ΔAOB ~ ΔCOD by [ AA / SAS / SSS ] similarity criterion.

Step 2: Formulate corresponding side ratios:
        AO / CO = BO / [ ___ ] = AB / [ ___ ]

Step 3: Calculate numerical ratio:
        AO / CO = 12 / [ ___ ] = [ ___ ] / [ ___ ]
        Ratio AO : OC = [ ___ ] : [ ___ ]

[COMPLETION DERIVATION KEY]
Step 1: Vertically opposite angles; Alternate interior angles (since AB || CD); AA criterion.
Step 2: DO; CD
Step 3: 12 / 8 = 3 / 2. Ratio AO : OC = 3 : 2.
```

### 5.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-TRI-01 (Foundation / CBSE):
  Formal BPT proof, ladder against vertical wall, shadow similarity, and trapezoid diagonal proofs.
FAMILY-TRI-02 (Olympiad / IOQM):
  Ceva's Theorem, Menelaus' Theorem on transversals, Stewart's theorem, angle bisector cevian ratios,
  and spiral similarity under central homothety.
FAMILY-TRI-03 (JEE Main):
  Sine rule, cosine rule, projection formula, half-angle formulas, inradius r = Δ/s, and circumradius R = abc/(4Δ).
FAMILY-TRI-04 (JEE Advanced):
  Coordinate and vector geometry synthesis with triangle centers, pedal triangles, distance between
  incentre and circumcentre (Euler's formula: d² = R² - 2Rr), and extremum area bounds.
```

---

## 6. Foundation Packet: Number Theory & Euclid's Division Lemma (`MATH-NUM-EUCLID-DIVISION`)

### 6.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-NUM-EUCLID-DIVISION`
- **Engineering Gate Binding**: `MATH-NUM-EUCLID-DIVISION` (Digest-bound closure receipt)
- **Learner Title**: Euclid's Division Lemma, Euclidean Algorithm & Fundamental Theorem of Arithmetic
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Strict Divisor Non-Zero Invariant**: In $a = bq + r$, the divisor $b \neq 0$ must be strictly non-zero. Division by zero is undefined in all rings.
  2. **Strict Remainder Invariant**: The remainder $r$ must satisfy $0 \le r < |b|$ by definition. Negative remainders or remainders $\ge |b|$ violate the uniqueness theorem.
  3. **Well-Ordering Principle of $\mathbb{Z}^+$**: Every non-empty set of positive integers contains a least element. This guarantees the finite termination of the Euclidean algorithm.
  4. **Prime Uniqueness (Fundamental Theorem of Arithmetic)**: Every integer $n > 1$ can be expressed as a product of prime powers $n = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}$ uniquely, up to the order of factors.

### 6.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NUM-01` (`CONCEPT`): Euclid's Division Lemma: Given positive integers $a$ and $b$, there exist unique integers $q$ and $r$ such that $a = bq + r$ where $0 \le r < b$.
- `ATOM-NUM-02` (`PROCEDURE`): Euclidean Algorithm for Greatest Common Divisor: $\gcd(a, b) = \gcd(b, a \pmod b)$ repeatedly until the remainder is 0; the last non-zero remainder is $\gcd(a, b)$.
- `ATOM-NUM-03` (`RELATION`): Bézout's Identity: For any integers $a$ and $b$, there exist integers $x, y \in \mathbb{Z}$ such that $ax + by = \gcd(a, b)$. In particular, $\gcd(a, b) = 1 \iff \exists x, y: ax + by = 1$.
- `ATOM-NUM-04` (`INVARIANT`): Two-Number Product Theorem: For any two positive integers $a$ and $b$, $\gcd(a, b) \times \operatorname{lcm}(a, b) = a \cdot b$. (Strictly restricted to pairs; does not generalize to triplets without inclusion-exclusion).
- `ATOM-NUM-05` (`STRATEGY`): Proof by Contradiction for Irrationality: Assuming $\sqrt{p} = \frac{a}{b}$ where $\gcd(a, b) = 1$, deriving that $p \mid a^2 \implies p \mid a$, which implies $p \mid b$, contradicting coprimality.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Leaves a remainder"* | $a = bq + r \iff a \equiv r \pmod b$ with $0 \le r < b$ | Congruence modulo $b$ on the integers $\mathbb{Z}$. |
| *"Coprime / relatively prime"* | $\gcd(a, b) = 1 \iff \exists x, y \in \mathbb{Z}: ax + by = 1$ | No shared prime factors; ideal generated is $\mathbb{Z}$. |
| *"Terminating decimal"* | $\frac{p}{q} \in \mathbb{Q}$ where $q = 2^m 5^n$ ($m, n \in \mathbb{N}_0$) | Denominator factors only into base-10 divisors 2 and 5. |

#### C. Misconception Contrasts
1. **Misconception: Negative Remainder in Division**:
   - *Flawed Action*: Calculating $-23 \div 7$ as quotient $-3$ with remainder $-2$.
   - *Correct Diagnostic Cue*: Euclid's lemma requires $0 \le r < b$. Write $-23 = 7(-4) + 5$. The quotient is $-4$ and the remainder is $+5$.
2. **Misconception: Product Rule Applied to Three Numbers**:
   - *Flawed Action*: Stating $\operatorname{lcm}(a, b, c) = \frac{abc}{\gcd(a, b, c)}$.
   - *Correct Diagnostic Cue*: The product identity holds strictly for **two** numbers. For three numbers: $\operatorname{lcm}(a, b, c) = \frac{abc \cdot \gcd(a, b, c)}{\gcd(a, b) \gcd(b, c) \gcd(c, a)}$.
3. **Misconception: Assuming Coprimality Without Declaration**:
   - *Flawed Action*: Proving $\sqrt{2}$ is irrational by setting $\sqrt{2} = a/b$ without explicitly asserting $\gcd(a, b) = 1$.
   - *Correct Diagnostic Cue*: The contradiction depends entirely on the initial assumption that all common factors were cancelled. If $a/b$ were not coprime, finding a factor of 2 would not contradict the premise.

### 6.3 Layer 3: Reconstructable TTU Library

#### TTU-NUM-01: Incomplete Euclidean Algorithm & Reverse Bézout Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Find HCF(135, 225) using Euclid's Division Algorithm, and express it as 135x + 225y.

Step 1: Apply Euclid's lemma to 225 and 135:
        225 = 135 · [ ___ ] + [ ___ ]   ... (1)
Step 2: Since remainder ≠ 0, apply lemma to 135 and remainder:
        135 = [ ___ ] · [ ___ ] + [ ___ ]   ... (2)
Step 3: Since remainder ≠ 0, apply lemma to [ ___ ] and [ ___ ]:
        90 = [ ___ ] · [ ___ ] + 0      ... (3)
Step 4: The last non-zero remainder is: HCF(135, 225) = [ ___ ]

Step 5: Express HCF as linear combination (Bézout's identity):
        From equation (2):  45 = 135 - 90 · [ ___ ]
        From equation (1):  90 = 225 - 135 · [ ___ ]
        Substitute (1) into (2):
        45 = 135 - (225 - 135 · [ ___ ]) · 1
        45 = 135 · [ ___ ] - 225 · [ ___ ]
        x = [ ___ ],  y = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 225 = 135 · 1 + 90
Step 2: 135 = 90 · 1 + 45
Step 3: 90 = 45 · 2 + 0
Step 4: HCF = 45
Step 5: 45 = 135 - 90·1; 90 = 225 - 135·1; 45 = 135·2 - 225·1 ==> x = 2, y = -1
```

#### TTU-NUM-02: Square Root Irrationality Dedekind-Contradiction Scaffold (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Prove that √3 is irrational.

Proof Structure: Proof by Contradiction.
Step 1: Assume the contrary, that √3 is rational.
        Then √3 = a / b, where a, b ∈ ℤ+, b ≠ 0, and gcd(a, b) = [ ___ ].
Step 2: Squaring both sides:
        3 = a² / b²  ==>  3b² = [ ___ ]   ... (1)
Step 3: Since 3 divides 3b², 3 divides [ ___ ].
        By prime divisibility theorem (if p|a² then p|a for prime p):
        3 divides [ ___ ].
Step 4: Since 3 divides a, we can write a = 3c for some integer c.
        Substitute a = 3c into equation (1):
        3b² = (3c)² = [ ___ ]c²
        Dividing both sides by 3:  b² = [ ___ ]c²
Step 5: This means 3 divides b², which implies 3 divides [ ___ ].
Step 6: Deductive Contradiction:
        From Step 3, 3 divides a. From Step 5, 3 divides b.
        Therefore, a and b have at least [ ___ ] as a common factor.
        This contradicts our initial assumption that gcd(a, b) = [ ___ ].
Conclusion: Our assumption was false. Therefore, √3 is [ RATIONAL / IRRATIONAL ].

[COMPLETION DERIVATION KEY]
Step 1: gcd(a, b) = 1 (coprime)
Step 2: a²
Step 3: a²; a
Step 4: 9c²; 3c²
Step 5: b
Step 6: 3; 1
Conclusion: IRRATIONAL (Hence Proved).
```

### 6.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-NUM-01 (Foundation / CBSE):
  HCF and LCM via prime factorisation, terminating decimal form q = 2^m 5^n, irrationality proofs for √2, √5.
FAMILY-NUM-02 (Olympiad / IOQM):
  Linear Diophantine equations ax + by = c, Chinese Remainder Theorem, Fermat's Little Theorem (a^{p-1} ≡ 1 mod p),
  Legendre's formula for highest power of prime p dividing n!, and Wilson's theorem.
FAMILY-NUM-03 (JEE Main):
  Divisibility in binomial expansions (1+x)^n, finding last two digits via mod 100, floor function properties.
FAMILY-NUM-04 (JEE Advanced):
  Cyclotomic polynomial factorization, primitive roots, p-adic valuations in combinatorics,
  and integer solutions to non-linear Diophantine equations (e.g. y² = x³ + k).
```

---

## 7. Foundation Packet: Trigonometric Ratios & Pythagorean Identities (`MATH-TRIG-RATIOS`)

### 7.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-TRIG-RATIOS`
- **Engineering Gate Binding**: `MATH-TRIG-RATIOS` (Digest-bound closure receipt)
- **Learner Title**: Trigonometric Ratios, Pythagorean Identities & Complementary Angle Transformations
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Tangent & Secant Domain Invariant**: $\tan\theta = \frac{\sin\theta}{\cos\theta}$ and $\sec\theta = \frac{1}{\cos\theta}$ require $\cos\theta \neq 0 \iff \theta \neq (2k+1)\frac{\pi}{2}$ for all $k \in \mathbb{Z}$.
  2. **Cotangent & Cosecant Domain Invariant**: $\cot\theta = \frac{\cos\theta}{\sin\theta}$ and $\csc\theta = \frac{1}{\sin\theta}$ require $\sin\theta \neq 0 \iff \theta \neq k\pi$ for all $k \in \mathbb{Z}$.
  3. **Pythagorean Bounded Metric Invariant**: For all real angles $\theta \in \mathbb{R}$, $\sin^2\theta + \cos^2\theta \equiv 1$. Consequently, $|\sin\theta| \le 1$ and $|\cos\theta| \le 1$.

### 7.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-TRIG-01` (`CONCEPT`): Trigonometric ratios as dimensionless scaling invariants of right-angled triangles under central dilation: $\sin\theta = \frac{\text{opp}}{\text{hyp}}, \cos\theta = \frac{\text{adj}}{\text{hyp}}, \tan\theta = \frac{\text{opp}}{\text{adj}}$.
- `ATOM-TRIG-02` (`INVARIANT`): Fundamental Pythagorean identity trichotomy:
  - $\sin^2\theta + \cos^2\theta = 1$
  - $\sec^2\theta - \tan^2\theta = 1 \iff (\sec\theta - \tan\theta)(\sec\theta + \tan\theta) = 1$
  - $\csc^2\theta - \cot^2\theta = 1 \iff (\csc\theta - \cot\theta)(\csc\theta + \cot\theta) = 1$
- `ATOM-TRIG-03` (`RELATION`): Complementary angle co-function identities: $\sin(90^\circ - \theta) = \cos\theta, \cos(90^\circ - \theta) = \sin\theta, \tan(90^\circ - \theta) = \cot\theta$.
- `ATOM-TRIG-04` (`PROCEDURE`): Reciprocal difference-of-squares reduction: Given $\sec\theta + \tan\theta = p$, immediately deduce $\sec\theta - \tan\theta = 1/p$, isolating $\sec\theta = \frac{p+1/p}{2}$ and $\tan\theta = \frac{p-1/p}{2}$.
- `ATOM-TRIG-05` (`STRATEGY`): Structural algebraic substitutions: converting rational trigonometric expressions into fundamental $(\sin\theta, \cos\theta)$ or utilizing $s = \sin\theta + \cos\theta, p = \sin\theta\cos\theta = \frac{s^2-1}{2}$.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"SOH-CAH-TOA"* | Unit circle projection $(x, y) = (\cos\theta, \sin\theta)$ | Dimensionless projection of directed ray on unit circle. |
| *"Sec plus tan gives reciprocal"* | $(\sec\theta - \tan\theta) = \frac{1}{\sec\theta + \tan\theta}$ | Difference-of-squares consequence of $\sec^2\theta - \tan^2\theta = 1$. |
| *"Angle of elevation / depression"* | Alternate interior angles $\theta_1 = \theta_2$ across horizontal sight lines | Establishing right triangles with horizontal baseline. |

#### C. Misconception Contrasts
1. **Misconception: Distributing Trigonometric Operators Over Addition**:
   - *Flawed Action*: Writing $\sin(A + B) = \sin A + \sin B$, or $\sqrt{\sin^2 A + \cos^2 B} = \sin A + \cos B$.
   - *Correct Diagnostic Cue*: Trigonometric functions are non-linear transcendental mappings: $\sin(A + B) = \sin A \cos B + \cos A \sin B \neq \sin A + \sin B$.
2. **Misconception: Unconditional Validity of Tangent Identities**:
   - *Flawed Action*: Asserting $\sec^2\theta - \tan^2\theta = 1$ holds for all real $\theta$.
   - *Correct Diagnostic Cue*: $\sec\theta$ and $\tan\theta$ are undefined at $\theta = \frac{\pi}{2} + k\pi$. The identity holds strictly on the domain of definition $\theta \neq (2k+1)\frac{\pi}{2}$.
3. **Misconception: Unbounded Solutions for Sin and Cos**:
   - *Flawed Action*: Accepting algebraic solutions $\sin\theta = 2$ or $\cos\theta = -1.5$ from quadratic factorizations.
   - *Correct Diagnostic Cue*: For all real $\theta$, projections on the unit circle are bounded: $|\sin\theta| \le 1$ and $|\cos\theta| \le 1$. Values outside $[-1, 1]$ must be discarded.

### 7.3 Layer 3: Reconstructable TTU Library

#### TTU-TRIG-01: Incomplete Reciprocal Conjugate Reduction Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Given sec θ + tan θ = 5, find the exact values of sin θ, cos θ, and tan θ.

Step 1: Write fundamental Pythagorean identity connecting sec θ and tan θ:
        sec² θ - tan² θ = [ ___ ]
Step 2: Factor as difference of squares:
        (sec θ + tan θ)(sec θ - tan θ) = [ ___ ]
Step 3: Substitute known value sec θ + tan θ = 5:
        5 · (sec θ - tan θ) = 1  ==>  sec θ - tan θ = [ ___ ]   ... (1)
        We also have:                 sec θ + tan θ = 5       ... (2)

Step 4: Add equations (1) and (2):
        2 sec θ = 5 + [ ___ ] = [ ___ ] / 5
        sec θ = [ ___ ] / [ ___ ]
        Therefore: cos θ = 1 / sec θ = [ ___ ] / [ ___ ]

Step 5: Subtract equation (1) from equation (2):
        2 tan θ = 5 - [ ___ ] = [ ___ ] / 5
        tan θ = [ ___ ] / [ ___ ]

Step 6: Compute sin θ:
        sin θ = tan θ · cos θ = ([ ___ ] / [ ___ ]) · ([ ___ ] / [ ___ ]) = [ ___ ] / [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 1
Step 2: 1
Step 3: 1/5
Step 4: 1/5; 26/5; 26/10 = 13/5; cos θ = 5/13
Step 5: 1/5; 24/5; 24/10 = 12/5
Step 6: (12/5) · (5/13) = 12/13
```

#### TTU-TRIG-02: Geometric Unit-Circle Angle Representation & Identity Verification Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-1.5, 1.5], y ∈ [-1.5, 1.5], clip_to_viewport = true
Figure: Unit circle x² + y² = 1 with acute ray at angle θ in Quadrant I.
Target Condition: Derive 1 + tan² θ = sec² θ using right triangle geometry on the unit circle.

[INCOMPLETE GEOMETRIC TTU]
Step 1: Ray intersects unit circle at point P with coordinates:
        P = ([ ___ ], [ ___ ])
Step 2: Right triangle OAP has base OA = cos θ, altitude AP = sin θ, hypotenuse OP = [ ___ ].
Step 3: Divide Pythagorean equation (OA)² + (AP)² = (OP)² by (OA)² = cos² θ:
        (cos² θ / cos² θ) + (sin² θ / [ ___ ]) = ([ ___ ] / cos² θ)
        [ ___ ] + tan² θ = sec² θ

Step 4: Domain validity condition:
        Division by cos² θ requires cos θ ≠ [ ___ ]  ==>  θ ≠ [ ___ ]°

[COMPLETION DERIVATION KEY]
Step 1: (cos θ, sin θ)
Step 2: 1
Step 3: cos² θ; 1; 1
Step 4: 0; 90° (or π/2)
```

### 7.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-TRIG-01 (Foundation / CBSE):
  Right-triangle ratio evaluations, standard angle evaluation tables, heights and distances (angles of elevation and depression).
FAMILY-TRIG-02 (Olympiad / IOQM):
  Non-trivial trigonometric equations, product telescoping cos(π/7)cos(2π/7)cos(4π/7) = -1/8, and Chebyshev polynomial representations.
FAMILY-TRIG-03 (JEE Main):
  Compound and multiple angle expansions (sin 2θ, cos 2θ, tan 3θ), conditional identities in ΔABC (A+B+C=π), and maximum/minimum values of a cos θ + b sin θ + c.
FAMILY-TRIG-04 (JEE Advanced):
  Inverse trigonometric relations with principal branch constraints, trigonometric series summation via C+iS method, and complex roots on the unit circle.
```

---

## 8. Foundation Packet: Polynomial Rings, Factor Theorem & Newton Sums (`MATH-ALG-POLYNOMIALS`)

### 8.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-ALG-POLYNOMIALS`
- **Engineering Gate Binding**: `MATH-ALG-POLYNOMIALS` (Digest-bound closure receipt)
- **Learner Title**: Polynomial Rings, Remainder & Factor Theorems, and Newton Sum Recurrences
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Non-Negative Integer Exponent Invariant**: A polynomial $P(x) = \sum_{k=0}^n a_k x^k$ requires all exponents $k \in \mathbb{N}_0 = \{0, 1, 2, \dots\}$. Expressions with fractional or negative exponents (e.g. $\sqrt{x}, 1/x$) are non-polynomials.
  2. **Division Algorithm Degree Invariant**: For polynomials $P(x)$ and non-zero $D(x)$, there exist unique polynomials $Q(x)$ and $R(x)$ such that $P(x) = D(x)Q(x) + R(x)$ where either $R(x) \equiv 0$ or $\deg(R) < \deg(D)$.
  3. **Factor Theorem Exact Equivalence**: A polynomial $P(x)$ has $(x - c)$ as a linear factor if and only if $P(c) = 0$.

### 8.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-POLY-01` (`CONCEPT`): Polynomial as an element of ring $K[x]$, characterized by finite degree $\deg(P) = n \ge 0$ with leading coefficient $a_n \neq 0$.
- `ATOM-POLY-02` (`INVARIANT`): Remainder Theorem: When $P(x)$ is divided by linear divisor $(x - c)$, the remainder is the scalar evaluation $R = P(c)$. If divided by $(ax - b)$, remainder is $P(b/a)$.
- `ATOM-POLY-03` (`RELATION`): Factor Theorem: $(x - c) \mid P(x) \iff P(c) = 0$. For integer polynomials, any rational root $p/q$ in lowest terms satisfies $p \mid a_0$ and $q \mid a_n$ (Rational Root Theorem).
- `ATOM-POLY-04` (`PROCEDURE`): Synthetic division algorithm: Horner's method for rapid evaluation and quotient polynomial computation.
- `ATOM-POLY-05` (`STRATEGY`): Newton's Sum Recurrence: For polynomial $P(x) = a_n x^n + \dots + a_0$ with roots $\alpha_1, \dots, \alpha_n$, the power sums $S_k = \sum_{i=1}^n \alpha_i^k$ satisfy $a_n S_k + a_{n-1} S_{k-1} + \dots = 0$.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Zero of a polynomial"* | $P(\alpha) = 0 \iff (x - \alpha) \mid P(x)$ | Value of $x$ making the polynomial vanish; root of $P(x) = 0$. |
| *"Remainder on division"* | $P(x) \equiv R(x) \pmod{D(x)}$ where $\deg(R) < \deg(D)$ | Polynomial congruence modulo $D(x)$. |
| *"Symmetric root power sum"* | $S_k = \alpha^k + \beta^k + \gamma^k$ satisfying Newton recurrence | Invariant reduction from power sums to elementary symmetric polynomials. |

#### C. Misconception Contrasts
1. **Misconception: Remainder Degree Equal to or Greater Than Divisor**:
   - *Flawed Action*: Dividing by quadratic divisor $(x^2 - 1)$ and assuming remainder is a constant $c$.
   - *Correct Diagnostic Cue*: When dividing by divisor of degree $m$, the remainder is a general polynomial of degree at most $m-1$. For quadratic divisor, remainder must be authored as $R(x) = Ax + B$.
2. **Misconception: Treating Non-Polynomial Expressions as Polynomials**:
   - *Flawed Action*: Stating $f(x) = x^2 + 2\sqrt{x} + 1$ is a quadratic polynomial.
   - *Correct Diagnostic Cue*: Terms with non-integer exponents ($\sqrt{x} = x^{1/2}$) violate the axiomatic definition of a polynomial ring $K[x]$.
3. **Misconception: Sign Inversion in Divisor Evaluation**:
   - *Flawed Action*: In finding remainder when $P(x)$ is divided by $(x + 2)$, calculating $P(2)$.
   - *Correct Diagnostic Cue*: Division by $(x - c)$ evaluates at $x = c$. For $(x + 2) = (x - (-2))$, the remainder is $P(-2)$.

### 8.3 Layer 3: Reconstructable TTU Library

#### TTU-POLY-01: Incomplete Quadratic Remainder Reconstruction Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: A polynomial P(x) leaves remainder 3 when divided by (x - 1), and remainder 7 when divided by (x - 3).
      Find the remainder when P(x) is divided by (x - 1)(x - 3).

Step 1: Identify degree of divisor: Divisor D(x) = (x - 1)(x - 3) has degree [ ___ ].
Step 2: Express general remainder form: Since deg(D) = 2, remainder R(x) has form:
        R(x) = [ ___ ]x + [ ___ ]
Step 3: Write division algorithm equation:
        P(x) = (x - 1)(x - 3) · Q(x) + (Ax + B)

Step 4: Use Remainder Theorem conditions:
        P(1) = 3  ==>  (0) · Q(1) + (A(1) + B) = 3  ==>   A + B = [ ___ ]   ... (1)
        P(3) = 7  ==>  (0) · Q(3) + (A(3) + B) = 7  ==>  3A + B = [ ___ ]   ... (2)

Step 5: Solve linear system for A and B:
        Subtract (1) from (2):
        (3A - A) + (B - B) = 7 - [ ___ ]
        2A = [ ___ ]  ==>  A = [ ___ ]
        Substitute A into (1):
        [ ___ ] + B = 3  ==>  B = [ ___ ]

Conclusion: The remainder is R(x) = [ ___ ]x + [ ___ ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 2
Step 2: Ax + B
Step 4: A + B = 3; 3A + B = 7
Step 5: 3; 4; A = 2; 2 + B = 3 ==> B = 1
Conclusion: R(x) = 2x + 1
```

#### TTU-POLY-02: Newton Sum Power-Recurrence Model (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Let α and β be roots of x² - 5x + 3 = 0.
      Let S_n = αⁿ + βⁿ. Find S_1, S_2, S_3, and derive S_n - 5·S_{n-1} + 3·S_{n-2} = 0.

Step 1: Vieta's formulas:
        α + β = [ ___ ],   α · β = [ ___ ]
Step 2: Base values:
        S_0 = α⁰ + β⁰ = 1 + 1 = [ ___ ]
        S_1 = α + β = [ ___ ]
Step 3: Newton sum recurrence for x² - 5x + 3 = 0:
        Multiply α² - 5α + 3 = 0 by αⁿ⁻²:  αⁿ - 5αⁿ⁻¹ + 3αⁿ⁻² = 0
        Multiply β² - 5β + 3 = 0 by βⁿ⁻²:  βⁿ - 5βⁿ⁻¹ + 3βⁿ⁻² = 0
        Adding the two: S_n - 5·S_{n-1} + 3·S_{n-2} = [ ___ ]

Step 4: Compute S_2:
        S_2 - 5·S_1 + 3·S_0 = 0  ==>  S_2 = 5·([ ___ ]) - 3·([ ___ ]) = [ ___ ] - [ ___ ] = [ ___ ]
Step 5: Compute S_3:
        S_3 - 5·S_2 + 3·S_1 = 0  ==>  S_3 = 5·([ ___ ]) - 3·([ ___ ]) = [ ___ ] - [ ___ ] = [ ___ ]

[COMPLETION DERIVATION KEY]
Step 1: α + β = 5, αβ = 3
Step 2: S_0 = 2, S_1 = 5
Step 3: 0 (Newton's recurrence: S_n = 5 S_{n-1} - 3 S_{n-2})
Step 4: S_2 = 5(5) - 3(2) = 25 - 6 = 19
Step 5: S_3 = 5(19) - 3(5) = 95 - 15 = 80
```

### 8.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-POLY-01 (Foundation / CBSE):
  Zeros of linear and quadratic polynomials, factor theorem proofs, verification of relationship between zeros and coefficients.
FAMILY-POLY-02 (Olympiad / IOQM):
  Integer-valued polynomials, Lagrange interpolation, Vieta's jumping on polynomial Diophantine equations, and Eisenstein's criterion for irreducibility.
FAMILY-POLY-03 (JEE Main):
  Remainder with composite divisors (x-1)(x-2), common zeros between two polynomials, equations reducible to polynomials via reciprocal substitution x + 1/x = t.
FAMILY-POLY-04 (JEE Advanced):
  Roots of unity polynomials sum_{k=0}^{n-1} x^k = 0, maximum number of real roots via Descartes' Rule of Signs, and Taylor expansion of polynomials about x = a.
```

---

## 9. Foundation Packet: Circle Theorems, Cyclic Quadrilaterals & Tangents (`MATH-GEO-CIRCLES`)

### 9.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-GEO-CIRCLES`
- **Engineering Gate Binding**: `MATH-GEO-CIRCLES` (Digest-bound closure receipt)
- **Learner Title**: Circle Theorems, Inscribed Angles, Cyclic Quadrilaterals & Tangent-Secant Invariants
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Strict Radius Invariant**: A circle $\mathcal{C}(O, r)$ requires radius $r > 0$. Points with $r = 0$ represent degenerate point-circles; $r < 0$ is undefined in Euclidean metric.
  2. **Non-Collinearity of Cyclic Vertices**: A cyclic quadrilateral $ABCD$ requires no three vertices to be collinear; vertices must lie in sequential cyclic order along the circumference.
  3. **Tangent Orthogonality Invariant**: At the point of contact $T$, the tangent line $l$ is strictly perpendicular to the radius $OT$: $l \perp OT$.
  4. **Power of a Point Invariant**: For any point $P$ and circle $\mathcal{C}(O, r)$, the power of $P$ is $\operatorname{Pow}(P) = d^2 - r^2 = PA \cdot PB$ for any secant line through $P$ intersecting the circle at $A$ and $B$. If $P$ is outside the circle and $PT$ is tangent, $PT^2 = PA \cdot PB$.

### 9.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-CIRC-01` (`CONCEPT`): Circle as locus of points equidistant from a fixed center. Chord, arc, subtended angle, and tangent defined under Euclidean metric.
- `ATOM-CIRC-02` (`INVARIANT`): Central-to-Inscribed Angle Theorem: The angle subtended by an arc at the center is double the angle subtended by it at any point on the remaining part of the circle: $\angle AOB = 2 \angle APB$.
- `ATOM-CIRC-03` (`RELATION`): Cyclic Quadrilateral Theorem: A quadrilateral is concyclic if and only if opposite angles are supplementary ($\angle A + \angle C = 180^\circ$ and $\angle B + \angle D = 180^\circ$), or exterior angle equals opposite interior angle. Ptolemy's Theorem: $AC \cdot BD = AB \cdot CD + BC \cdot AD$.
- `ATOM-CIRC-04` (`PROCEDURE`): Alternate Segment Theorem: The angle between a tangent and a chord through the point of contact is equal to the angle subtended by the chord in the alternate segment.
- `ATOM-CIRC-05` (`STRATEGY`): Auxiliary radial and chord constructions:
  - Joining the center $O$ to the point of contact of tangents to form congruent right-angled triangles ($\triangle OPT_1 \cong \triangle OPT_2$ by RHS).
  - Constructing common tangents or radical axes for intersecting or touching circles.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Angle at center double"* | $\angle AOB = 2 \angle APB$ for $P$ on opposite arc | Central dilation of angle measure relative to circumferential locus. |
| *"Opposite angles 180"* | $ABCD$ concyclic $\iff \angle A + \angle C = \pi$ | Subtended arcs partition entire circumference ($2\pi$). |
| *"Tangent is perpendicular"* | $l \perp OT \implies OP^2 = r^2 + PT^2$ | Pythagorean relationship from point of contact orthogonality. |

#### C. Misconception Contrasts
1. **Misconception: Inscribed Angle Doubling on Opposite Arc**:
   - *Flawed Action*: Concluding $\angle AOB = 2\angle APB$ when $P$ lies on the *minor* arc subtended by chord $AB$.
   - *Correct Diagnostic Cue*: The inscribed angle theorem strictly relates the subtended central angle to points on the *remaining* (opposite) arc. If $P$ is on the minor arc, $\angle APB = 180^\circ - \frac{1}{2}\angle AOB = \frac{1}{2}\operatorname{reflex}\angle AOB$.
2. **Misconception: Assuming Any Quadrilateral is Cyclic**:
   - *Flawed Action*: Applying cyclic opposite angle relations ($\angle B + \angle D = 180^\circ$) to general parallelograms or rhombuses.
   - *Correct Diagnostic Cue*: A quadrilateral is cyclic only if $\angle A + \angle C = 180^\circ$. A parallelogram is cyclic if and only if it is a rectangle.
3. **Misconception: Confusing Secant Segment Lengths**:
   - *Flawed Action*: In the secant product $PA \cdot PB$, calculating $PA \cdot AB$.
   - *Correct Diagnostic Cue*: The Power of a Point identity strictly multiplies the distances from the external point $P$ to the two intersection points: $PA$ and $PB$, NOT the chord length $AB$.

### 9.3 Layer 3: Reconstructable TTU Library

#### TTU-CIRC-01: Incomplete Alternate Segment Theorem Proof Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Theorem: The angle between a tangent and a chord through the point of contact
         is equal to the angle subtended by the chord in the alternate segment.
Given: Tangent XY touches circle at P. Chord PQ subtends ∠PRQ in the alternate segment.
To Prove: ∠QPY = ∠PRQ

Construction:
  1. Draw diameter PM through center O.
  2. Join MQ.

Proof Steps:
Step 1: Since PM is a diameter, angle in semicircle is:
        ∠PQM = [ ___ ]°
Step 2: In right-angled ΔPQM:
        ∠QPM + ∠PMQ = 180° - 90° = [ ___ ]°   ... (1)
Step 3: Since PM ⊥ tangent XY at point of contact P:
        ∠MPY = [ ___ ]°
Step 4: Express ∠MPY as sum of adjacent angles:
        ∠QPM + ∠QPY = [ ___ ]°               ... (2)
Step 5: Equating (1) and (2):
        ∠QPM + ∠PMQ = ∠QPM + ∠QPY  ==>  ∠QPY = ∠[ ___ ]
Step 6: Circle Invariant:
        ∠PMQ and ∠PRQ are subtended by the same chord [ ___ ] in the same segment.
        Therefore: ∠PMQ = ∠[ ___ ]
Conclusion: ∠QPY = ∠PRQ  (Hence Proved)

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 90°
Step 2: 90°
Step 3: 90°
Step 4: 90°
Step 5: PMQ
Step 6: Same chord PQ; PRQ
Conclusion: ∠QPY = ∠PRQ
```

#### TTU-CIRC-02: Power of a Point & Tangent Length Geometric Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-4, 6], y ∈ [-4, 4], clip_to_viewport = true
Figure: Circle centered at origin with radius r = 3. Point P = (5, 0).
Target Condition: Find length of tangent PT, and given secant PAB passing through center, verify PT² = PA · PB.

[INCOMPLETE GEOMETRIC TTU]
Step 1: Distance from P to center O: OP = [ ___ ].
Step 2: In right ΔOPT (since OT ⊥ PT):
        PT² = OP² - OT² = [ ___ ]² - [ ___ ]² = [ ___ ] - [ ___ ] = [ ___ ]
        Length of tangent PT = √[ ___ ] = [ ___ ].

Step 3: Secant PAB passes through center O:
        Intersection points along line OP:
        Near intersection A has distance: PA = OP - r = 5 - [ ___ ] = [ ___ ]
        Far intersection B has distance:  PB = OP + r = 5 + [ ___ ] = [ ___ ]

Step 4: Verify Power of a Point identity:
        PA · PB = [ ___ ] · [ ___ ] = [ ___ ]
        Does PT² = PA · PB? [ YES / NO ]

[COMPLETION DERIVATION KEY]
Step 1: 5
Step 2: 5² - 3² = 25 - 9 = 16; PT = √16 = 4
Step 3: 5 - 3 = 2; 5 + 3 = 8
Step 4: 2 · 8 = 16. PT² (16) = PA · PB (16) ==> YES.
```

### 9.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-CIRC-01 (Foundation / CBSE):
  Tangent perpendicularity proofs, lengths of tangents from external point, cyclic quadrilateral angle deductions, and angle in semicircle.
FAMILY-CIRC-02 (Olympiad / IOQM):
  Ptolemy's Theorem, Simson line, Miquel's theorem, radical axis of coaxal circles, and spiral homothety.
FAMILY-CIRC-03 (JEE Main):
  Tangents and normals in Cartesian form xx₁ + yy₁ = r², condition of tangency c² = a²(1+m²), chord of contact T = 0, length of chord 2√(r²-d²).
FAMILY-CIRC-04 (JEE Advanced):
  Family of circles S + λL = 0 and S + λS' = 0, common chord, director circle, and orthogonal intersection condition 2g₁g₂ + 2f₁f₂ = c₁ + c₂.
```

---

## 10. Foundation Packet: Arithmetic Progressions & Series Summations (`MATH-SEQ-AP`)

### 10.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-SEQ-AP`
- **Engineering Gate Binding**: `MATH-SEQ-AP` (Digest-bound closure receipt)
- **Learner Title**: Arithmetic Progressions, Linear Recurrences & Finite Series Summations
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Strict Discrete Index Invariant**: The term index $n$ must belong to the positive integers: $n \in \mathbb{Z}^+ = \{1, 2, 3, \dots\}$. Fractional or negative term indices (e.g. $a_{3.5}$ or $a_{-2}$) are undefined in standard progression theory.
  2. **Common Difference Invariant**: A sequence $(a_n)$ is an AP if and only if $a_{n+1} - a_n = d$ is a constant independent of $n$ for all $n \ge 1$.
  3. **Non-Degenerate AP Condition**: If $d = 0$, the progression is a constant sequence ($a, a, a, \dots$). If $d \neq 0$, the sequence is strictly monotonic.

### 10.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-AP-01` (`CONCEPT`): Arithmetic Progression as a linear discrete function $f(n) = a + (n-1)d = dn + (a-d)$ over domain $\mathbb{Z}^+$. The common difference $d$ corresponds to the discrete slope.
- `ATOM-AP-02` (`INVARIANT`): General Term Formula: $a_n = a + (n-1)d$. Term from the end: $a_n' = l - (n-1)d$ where $l$ is the last term.
- `ATOM-AP-03` (`PROCEDURE`): Gauss Summation Identity: $S_n = \frac{n}{2}[2a + (n-1)d] = \frac{n}{2}(a + l)$. Symmetric pairing: $a_k + a_{n-k+1} = a_1 + a_n$ for all $1 \le k \le n$.
- `ATOM-AP-04` (`RELATION`): Term-Sum Inversion: $a_n = S_n - S_{n-1}$ for $n \ge 2$, with $a_1 = S_1$. If $S_n = An^2 + Bn$, the sequence is an AP with common difference $d = 2A$ and first term $a = A + B$.
- `ATOM-AP-05` (`STRATEGY`): Symmetric Variable Selection for Word Problems:
  - 3 terms in AP: $(a - d), a, (a + d)$ with sum $= 3a$.
  - 4 terms in AP: $(a - 3d), (a - d), (a + d), (a + 3d)$ with common difference $2d$ and sum $= 4a$.
  - 5 terms in AP: $(a - 2d), (a - d), a, (a + d), (a + 2d)$ with sum $= 5a$.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Equal steps"* | $a_{n+1} - a_n = d \iff$ linear recurrence $a_{n+1} = a_n + d$ | Discrete constant difference across consecutive elements. |
| *"Average times number of terms"* | $S_n = n \cdot \left(\frac{a + l}{2}\right) = n \cdot a_{\text{mid}}$ | Symmetry of terms about arithmetic center. |
| *"Arithmetic Mean"* | $A = \frac{a + b}{2} \iff a, A, b$ are in AP | Middle term of 3-term progression. |

#### C. Misconception Contrasts
1. **Misconception: Off-by-One in Term Index**:
   - *Flawed Action*: Writing $a_n = a + nd$.
   - *Correct Diagnostic Cue*: For the first term ($n = 1$), the difference $d$ has not been added yet ($a_1 = a + (1-1)d = a$). Adding $nd$ shifts every term forward by one position ($a + nd = a_{n+1}$).
2. **Misconception: Quadratic Term vs Quadratic Sum Confusion**:
   - *Flawed Action*: Concluding $a_n = 3n^2 + 2n$ is an AP because it contains $n$.
   - *Correct Diagnostic Cue*: An AP has a *linear* general term $a_n = dn + c$. A *quadratic* polynomial in $n$ describes the *sum* $S_n = An^2 + Bn$, NOT the individual term $a_n$.
3. **Misconception: Double Counting in Difference for Even Term Selections**:
   - *Flawed Action*: Choosing 4 terms as $(a - 3d), (a - d), (a + d), (a + 3d)$ and setting common difference equal to $d$.
   - *Correct Diagnostic Cue*: The step size between $(a - d)$ and $(a + d)$ is $(a + d) - (a - d) = 2d$. Therefore, the common difference is $2d$, NOT $d$.

### 10.3 Layer 3: Reconstructable TTU Library

#### TTU-AP-01: Incomplete Gaussian Pair-Summation Derivation Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Derive the sum formula Sn = n/2 · [2a + (n-1)d] using Gauss's reverse summation method.

Step 1: Write sum in ascending order:
        Sn = a + (a + d) + (a + 2d) + ... + [l - d] + l       ... (1)
Step 2: Write sum in reversed descending order:
        Sn = l + (l - d) + [ _____ ] + ... + (a + d) + a       ... (2)
Step 3: Add equations (1) and (2) term-by-term:
        Sn + Sn = (a + l) + [(a + d) + (l - d)] + ... + (l + a)
        2Sn = (a + l) + (a + [ ___ ]) + ... + (a + l)

Step 4: Count number of identical paired terms:
        There are [ ___ ] terms, each equal to (a + l).
        2Sn = [ ___ ] · (a + l)  ==>  Sn = ([ ___ ] / 2) · (a + l)

Step 5: Substitute the last term formula l = a + ([ ___ ] - 1)d:
        Sn = (n / 2) · [a + (a + (n - 1)d)]
        Sn = (n / 2) · [ [ ___ ]a + (n - 1)d ]   (Hence Derived)

[COMPLETION KEY - VERIFICATION ONLY]
Step 2: (l - 2d)
Step 3: l
Step 4: n terms; n · (a + l); (n / 2)
Step 5: n; 2a
```

#### TTU-AP-02: Quadratic Sum-to-Term Decompilation Model (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Given the sum of first n terms of a sequence is Sn = 3n² + 5n.
      Prove that it is an AP, and find the first term a and common difference d.

Step 1: Find the first term a:
        a = a₁ = S₁ = 3(1)² + 5(1) = 3 + 5 = [ ___ ]

Step 2: Find the sum of first two terms S₂:
        S₂ = 3(2)² + 5(2) = 3(4) + 10 = [ ___ ] + 10 = [ ___ ]

Step 3: Find the second term a₂:
        a₂ = S₂ - S₁ = [ ___ ] - [ ___ ] = [ ___ ]

Step 4: Calculate the candidate common difference d:
        d = a₂ - a₁ = [ ___ ] - [ ___ ] = [ ___ ]

Step 5: General proof using Sn - S_{n-1}:
        an = Sn - S_{n-1}
           = (3n² + 5n) - [ 3(n - 1)² + 5(n - 1) ]
           = (3n² + 5n) - [ 3(n² - 2n + 1) + 5n - 5 ]
           = (3n² + 5n) - [ 3n² - 6n + 3 + 5n - 5 ]
           = (3n² + 5n) - [ 3n² - n - 2 ]
           = [ ___ ]n + [ ___ ]

Step 6: Since an is a linear polynomial in n, the sequence is an AP:
        Common difference = coefficient of n = [ ___ ]
        First term = a₁ = 6(1) + 2 = [ ___ ]

[COMPLETION DERIVATION KEY]
Step 1: 8
Step 2: 12; 22
Step 3: 22 - 8 = 14
Step 4: 14 - 8 = 6
Step 5: 6n + 2
Step 6: 6; 8
```

### 10.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-AP-01 (Foundation / CBSE):
  Finding n-th term, sum of n terms, checking if a number belongs to an AP (n ∈ ℤ+), savings/installment word problems.
FAMILY-AP-02 (Olympiad / IOQM):
  APs with integer constraints, Green-Tao theorem context (primes in AP), partitioning sets into APs, and nonlinear Diophantine systems with AP terms.
FAMILY-AP-03 (JEE Main):
  Ratio of sums of two APs S_n / S_n' = (7n+1)/(4n+27) mapping to ratio of m-th terms by substitution n = 2m - 1, arithmetic-geometric progressions sum n rⁿ.
FAMILY-AP-04 (JEE Advanced):
  Telescoping series involving reciprocals of AP products sum 1/(a_k a_{k+1}), AP properties in logarithms (log a, log b, log c in AP <=> a, b, c in GP), and multidimensional grid lattices.
```

---

## 11. Foundation Packet: Cartesian Coordinate Geometry & Planar Invariants (`MATH-GEO-COORDINATES`)

### 11.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-GEO-COORDINATES`
- **Engineering Gate Binding**: `MATH-GEO-COORDINATES` (Digest-bound closure receipt)
- **Learner Title**: Cartesian Coordinate Geometry, Section Formulas & Planar Area Invariants
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Cartesian Metric Invariant**: The Euclidean distance between $P_1(x_1, y_1)$ and $P_2(x_2, y_2)$ is $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} \ge 0$. Distance is zero if and only if $P_1 \equiv P_2$.
  2. **Section Formula Denominator Constraint**: The section ratio $m : n$ must satisfy $m + n \neq 0$ for internal division ($m, n > 0$) and external division ($m/n \neq -1$).
  3. **Non-Degenerate Area Invariant**: Three points $A, B, C$ form a triangle if and only if the shoelace determinant is non-zero: $\Delta = \frac{1}{2} |x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)| > 0$. If $\Delta = 0$, the points are strictly collinear.

### 11.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-COORD-01` (`CONCEPT`): Cartesian coordinates as an isometric bijection between Euclidean plane $\mathbb{E}^2$ and $\mathbb{R}^2$. Abscissa $x$ as signed orthogonal distance from $y$-axis; ordinate $y$ as signed orthogonal distance from $x$-axis.
- `ATOM-COORD-02` (`INVARIANT`): Distance Formula as Pythagorean projection: $d^2 = (\Delta x)^2 + (\Delta y)^2$.
- `ATOM-COORD-03` (`PROCEDURE`): Section Formula: Coordinates of point $P$ dividing segment $AB$ in ratio $m : n$:
  - Internal division: $P\left(\frac{m x_2 + n x_1}{m + n}, \frac{m y_2 + n y_1}{m + n}\right)$.
  - Centroid of triangle $\triangle ABC$: $G\left(\frac{x_1 + x_2 + x_3}{3}, \frac{y_1 + y_2 + y_3}{3}\right)$, dividing each median in ratio $2 : 1$.
- `ATOM-COORD-04` (`RELATION`): Shoelace Area Formula: $\operatorname{Area}(\triangle ABC) = \frac{1}{2} |x_1 y_2 + x_2 y_3 + x_3 y_1 - (x_2 y_1 + x_3 y_2 + x_1 y_3)| = \frac{1}{2} \left| \det \begin{pmatrix} x_1 & y_1 & 1 \\ x_2 & y_2 & 1 \\ x_3 & y_3 & 1 \end{pmatrix} \right|$.
- `ATOM-COORD-05` (`STRATEGY`): Collinearity & Ratio Discovery: Using ratio $k : 1$ to determine unknown division ratios and verifying $k > 0$ (internal) vs $k < 0$ (external).

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Ratio m to n"* | Convex combination $\mathbf{p} = \frac{n}{m+n}\mathbf{a} + \frac{m}{m+n}\mathbf{b}$ | Affine barycentric coordinates along 1D line segment. |
| *"Centroid"* | Center of mass $\mathbf{g} = \frac{\mathbf{a} + \mathbf{b} + \mathbf{c}}{3}$ | Intersection of medians; median balance point. |
| *"Shoelace formula"* | $\frac{1}{2} \sum (x_i y_{i+1} - x_{i+1} y_i)$ | Closed contour integral of differential 1-form $x dy$ in $\mathbb{R}^2$. |

#### C. Misconception Contrasts
1. **Misconception: Inverting Point Order in Section Formula**:
   - *Flawed Action*: In dividing segment from $A$ to $B$ in ratio $m : n$, writing $\frac{m x_1 + n x_2}{m + n}$.
   - *Correct Diagnostic Cue*: The ratio multiplier cross-multiplies to the *opposite* point: ratio $m$ attached to $A$ multiplies $B$'s coordinates ($x_2$), and ratio $n$ attached to $B$ multiplies $A$'s coordinates ($x_1$): $x = \frac{m x_2 + n x_1}{m + n}$.
2. **Misconception: Omitting Absolute Value in Area Calculation**:
   - *Flawed Action*: Calculating the determinant as $-15$ and reporting area as $-7.5$.
   - *Correct Diagnostic Cue*: Geometric area is strictly non-negative. The determinant computes signed area depending on clockwise vs counterclockwise orientation. The physical area requires the absolute value: $\text{Area} = \frac{1}{2}|-15| = 7.5$.
3. **Misconception: External Division Denominator Sign Error**:
   - *Flawed Action*: Writing external division coordinates as $\frac{m x_2 + n x_1}{m - n}$.
   - *Correct Diagnostic Cue*: For external division in ratio $m:n$, treat ratio as $m : (-n)$. The formula is $x = \frac{m x_2 - n x_1}{m - n}$. Both numerator and denominator must carry the minus sign.

### 11.3 Layer 3: Reconstructable TTU Library

#### TTU-COORD-01: Incomplete Section Formula Ratio Discovery Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: In what ratio does the point P(2, -5) divide the line segment joining
      A(-3, 5) and B(4, -9)?

Step 1: Assume point P divides segment AB in the ratio k : 1.
        Coordinates of A: (x₁, y₁) = (-3, 5)
        Coordinates of B: (x₂, y₂) = (4, -9)

Step 2: Apply section formula for x-coordinate:
        x_P = (k · x₂ + 1 · x₁) / (k + 1)
        2   = (k · [ ___ ] + 1 · [ ___ ]) / (k + 1)
        2   = ([ ___ ]k - [ ___ ]) / (k + 1)

Step 3: Cross multiply and solve for k:
        2(k + 1) = 4k - 3
        2k + 2   = 4k - 3
        2k       = [ ___ ]  ==>  k = [ ___ ] / [ ___ ]

Step 4: Verify with y-coordinate:
        y_P = (k · y₂ + 1 · y₁) / (k + 1)
            = ((5/2) · (-9) + 5) / ((5/2) + 1)
            = (-45/2 + 10/2) / (7/2)
            = (-35/2) / (7/2) = -35 / 7 = [ ___ ]
        Does this match y_P = -5? [ YES / NO ]

Conclusion: The segment is divided in the ratio [ ___ ] : [ ___ ] internally.

[COMPLETION KEY - VERIFICATION ONLY]
Step 2: 4; -3; 4; 3
Step 3: 5; 5 / 2
Step 4: -5; YES
Conclusion: 5 : 2
```

#### TTU-COORD-02: Shoelace Determinant Planar Area Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-2, 6], y ∈ [-2, 8], clip_to_viewport = true
Points: A(1, 2), B(4, 6), C(3, 8).
Target Condition: Compute Area(ΔABC) and verify non-collinearity.

[INCOMPLETE GEOMETRIC TTU]
Step 1: Write Shoelace Formula layout:
        Δ = 1/2 | x₁(y₂ - y₃) + x₂(y₃ - y₁) + x₃(y₁ - y₂) |

Step 2: Substitute coordinates:
        Δ = 1/2 | 1·(6 - 8) + 4·(8 - 2) + 3·(2 - 6) |
        Δ = 1/2 | 1·([ ___ ]) + 4·([ ___ ]) + 3·([ ___ ]) |
        Δ = 1/2 | [ ___ ] + [ ___ ] + [ ___ ] |
        Δ = 1/2 | [ ___ ] |

Step 3: Compute final area:
        Area(ΔABC) = 1/2 · [ ___ ] = [ ___ ] sq units.

Step 4: Collinearity check:
        Since Area ≠ 0, are the points A, B, C collinear? [ YES / NO ]

[COMPLETION DERIVATION KEY]
Step 2: -2; 6; -4; -2; 24; -12; 10
Step 3: 10; 5
Step 4: NO (non-collinear).
```

### 11.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-COORD-01 (Foundation / CBSE):
  Distance between points, finding coordinates of equidistant points on axes, section formula internal division, finding ratios, collinearity proofs.
FAMILY-COORD-02 (Olympiad / IOQM):
  Pick's Theorem (A = I + B/2 - 1) for lattice polygons, area coordinates (barycentric coordinates), and collinearity via Menelaus in coordinates.
FAMILY-COORD-03 (JEE Main):
  Locus problems, shift of origin (X = x-h, Y = y-k), condition for lines to form equilateral triangle, distance between parallel lines.
FAMILY-COORD-04 (JEE Advanced):
  Concurrence of lines via 3x3 determinant, rotation of axes through angle θ, reflection of point across arbitrary line ax+by+c=0, and harmonic conjugates.
```

---

## 12. Foundation Packet: Conic Sections & Parabolic Geometry (`MATH-CONIC-PARABOLA`)

### 12.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-CONIC-PARABOLA`
- **Engineering Gate Binding**: `MATH-CONIC-PARABOLA` (Digest-bound closure receipt)
- **Learner Title**: Conic Sections, Parabola Focus-Directrix Invariant & Tangency Geometry
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Strict Eccentricity Invariant**: A conic section is a parabola if and only if eccentricity $e = \frac{SP}{PM} \equiv 1$ strictly, where $S$ is the focus and $PM$ is the perpendicular distance from point $P$ to the directrix line $L$.
  2. **Non-Incident Focus Precondition**: The focus $S$ must not lie on the directrix line $L$. If $S \in L$, the locus degenerates into a single straight line through $S$ perpendicular to $L$.
  3. **Focal Parameter Invariant**: The focal length $a > 0$ strictly. The distance between focus and directrix is $2a$. Latus rectum length is $4a$.

### 12.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-PARAB-01` (`CONCEPT`): Parabola as the geometric locus of a point moving such that its distance from a fixed point (focus $S$) equals its perpendicular distance from a fixed straight line (directrix $L$).
- `ATOM-PARAB-02` (`INVARIANT`): Standard Four-Form Canonical Coordinates:
  - $y^2 = 4ax$: Opens right, focus $(a, 0)$, directrix $x = -a$, vertex $(0, 0)$.
  - $y^2 = -4ax$: Opens left, focus $(-a, 0)$, directrix $x = a$.
  - $x^2 = 4ay$: Opens up, focus $(0, a)$, directrix $y = -a$.
  - $x^2 = -4ay$: Opens down, focus $(0, -a)$, directrix $y = a$.
- `ATOM-PARAB-03` (`RELATION`): Parametric representation: Point $P(t) = (at^2, 2at)$. Tangent line at $t$: $ty = x + at^2$. Focal chord endpoint parameter invariant: If $t_1, t_2$ are endpoints of a focal chord, then $t_1 t_2 = -1$.
- `ATOM-PARAB-04` (`PROCEDURE`): Tangency Condition: A line $y = mx + c$ touches the parabola $y^2 = 4ax$ if and only if $c = \frac{a}{m}$ (for $m \neq 0$). The point of contact is $\left(\frac{a}{m^2}, \frac{2a}{m}\right)$.
- `ATOM-PARAB-05` (`STRATEGY`): Optical Reflection Invariant: Any ray parallel to the principal axis of symmetry reflects off the parabolic mirror directly through the focus $S$.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"SP equals PM"* | $SP = PM \iff \sqrt{(x-a)^2 + y^2} = |x+a|$ | Equidistance locus yielding canonical Cartesian equation $y^2 = 4ax$. |
| *"Focal chord product"* | $t_1 t_2 = -1$ | Harmonic segment property of chords passing through $(a, 0)$. |
| *"Perpendicular tangents intersect on directrix"* | $m_1 m_2 = -1 \implies x = -a$ | Director circle of parabola is its directrix $x = -a$. |

#### C. Misconception Contrasts
1. **Misconception: Inverting Axis Orientation in Standard Forms**:
   - *Flawed Action*: Writing focus of $x^2 = 8y$ as $(2, 0)$.
   - *Correct Diagnostic Cue*: In $x^2 = 4ay$, the axis of symmetry is vertical ($y$-axis). The focus lies on the $y$-axis at $(0, a) = (0, 2)$, NOT on the $x$-axis.
2. **Misconception: Applying $c = a/m$ to Vertical Parabolas**:
   - *Flawed Action*: Stating line $y = mx + c$ touches $x^2 = 4ay$ when $c = a/m$.
   - *Correct Diagnostic Cue*: The condition $c = a/m$ holds strictly for horizontal parabola $y^2 = 4ax$. For vertical parabola $x^2 = 4ay$, the tangency condition is $c = -am^2$.
3. **Misconception: Latus Rectum as Arbitrary Focal Segment**:
   - *Flawed Action*: Measuring the length of an inclined focal chord as $4a$.
   - *Correct Diagnostic Cue*: The latus rectum is specifically the focal chord *perpendicular* to the axis of symmetry. Any inclined focal chord has length $a(t + 1/t)^2 \ge 4a$.

### 12.3 Layer 3: Reconstructable TTU Library

#### TTU-PARAB-01: Incomplete Focus-Directrix Standard Form Derivation Frame (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Derive the standard equation of parabola y² = 4ax using focus S(a, 0) and directrix x = -a.

Step 1: Let P(x, y) be any point on the parabola.
        Distance to focus S(a, 0):
        SP = √[ (x - [ ___ ])² + (y - [ ___ ])² ]

Step 2: Distance to directrix line x + a = 0:
        PM = | x + [ ___ ] | / √[ 1² + 0² ] = | x + [ ___ ] |

Step 3: Equating SP = PM by definition of parabola (eccentricity e = 1):
        √[ (x - a)² + y² ] = | x + a |

Step 4: Squaring both sides:
        (x - a)² + y² = (x + a)²
        [ x² - [ ___ ]ax + a² ] + y² = [ x² + [ ___ ]ax + a² ]

Step 5: Cancel common terms x² and a² from both sides:
        -2ax + y² = 2ax
        y² = 2ax + [ ___ ]ax
        y² = [ ___ ]ax   (Hence Derived)

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: a; 0
Step 2: a; a
Step 4: 2; 2
Step 5: 2; 4
```

#### TTU-PARAB-02: Focal Chord Harmonic Mean Geometric Model (Core2A $\to$ Core2B)
```text
[BOUNDED VIEWPORT SPECIFICATION]
Viewport: x ∈ [-3, 8], y ∈ [-6, 6], clip_to_viewport = true
Parabola: y² = 4x  (a = 1). Focal chord PQ passes through focus S(1, 0).
Target Condition: If endpoint P has parameter t = 2, find coordinates of Q and length of PQ.

[INCOMPLETE GEOMETRIC TTU]
Step 1: Endpoint P coordinates: P(t) = (at², 2at) = (1·2², 2·1·2) = ([ ___ ], [ ___ ]).
Step 2: Focal chord parameter property:
        t₁ · t₂ = [ ___ ]  ==>  2 · t₂ = -1  ==>  t₂ = [ ___ ] / [ ___ ]

Step 3: Endpoint Q coordinates:
        x_Q = a · t₂² = 1 · (-1/2)² = [ ___ ] / [ ___ ]
        y_Q = 2a · t₂ = 2(1)(-1/2) = [ ___ ]
        Q = ([ ___ ], [ ___ ])

Step 4: Length of focal chord formula:
        Length PQ = a(t + 1/t)² = 1 · (2 - [ ___ ])² = ( [ ___ ] / 2 )² = [ ___ ] / [ ___ ]

[COMPLETION DERIVATION KEY]
Step 1: (4, 4)
Step 2: -1; -1 / 2
Step 3: 1 / 4; -1; (1/4, -1)
Step 4: 1/2; 5; 25 / 4 (6.25)
```

### 12.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-PARAB-01 (Foundation / CBSE):
  Vertex, focus, axis, directrix equation, and latus rectum length extraction for standard parabolas.
FAMILY-PARAB-02 (Olympiad / IOQM):
  Archimedean quadrature of parabola segment (area = 4/3 of inscribed triangle), Poncelet's porism, and focal inequalities.
FAMILY-PARAB-03 (JEE Main):
  Tangent and normal equations (y = mx - 2am - am³), point of intersection of perpendicular tangents on directrix, common tangents to parabola and circle.
FAMILY-PARAB-04 (JEE Advanced):
  Co-normal points (sum of slopes = 0), circle through feet of three co-normals passing through vertex, and locus of centroids of normal triangles.
```

---

## 13. Foundation Packet: Calculus Foundations, Limits & Indeterminate Forms (`MATH-CALC-LIMITS`)

### 13.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-CALC-LIMITS`
- **Engineering Gate Binding**: `MATH-CALC-LIMITS` (Digest-bound closure receipt)
- **Learner Title**: Calculus Foundations, Limits of Functions & Indeterminate Form Resolution
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Deleted Punctured Neighborhood Precondition**: The limit $\lim_{x \to a} f(x)$ evaluates behavior in a punctured neighborhood $0 < |x - a| < \delta$. The value $f(a)$ at the exact point is entirely irrelevant to the existence or value of the limit.
  2. **Left-Right Hand Limit Equality Invariant**: $\lim_{x \to a} f(x) = L \iff \lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = L$ where $L \in \mathbb{R}$ is finite.
  3. **Radian Measure Precondition in Trigonometric Limits**: The fundamental trigonometric limit $\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$ is valid if and only if $\theta$ is measured in **radians**. If $\theta$ is in degrees, the limit is $\frac{\pi}{180}$.

### 13.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-LIM-01` (`CONCEPT`): Limit as local convergence: For every $\varepsilon > 0$ there exists $\delta > 0$ such that $0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon$.
- `ATOM-LIM-02` (`INVARIANT`): Fundamental Algebraic Standard Limit: $\lim_{x \to a} \frac{x^n - a^n}{x - a} = n a^{n-1}$ for all $n \in \mathbb{Q}$ ($a > 0$).
- `ATOM-LIM-03` (`RELATION`): Sandwich / Squeeze Theorem: If $g(x) \le f(x) \le h(x)$ in a punctured neighborhood of $a$, and $\lim_{x \to a} g(x) = \lim_{x \to a} h(x) = L$, then $\lim_{x \to a} f(x) = L$.
- `ATOM-LIM-04` (`PROCEDURE`): Resolution of Indeterminate Form $1^\infty$: $\lim_{x \to a} [f(x)]^{g(x)} = e^{\lim_{x \to a} [f(x) - 1] \cdot g(x)}$ where $\lim f(x) = 1$ and $\lim g(x) = \infty$.
- `ATOM-LIM-05` (`STRATEGY`): Taylor / Maclaurin series expansion dominance: replacing $\sin x = x - \frac{x^3}{6} + \mathcal{O}(x^5)$, $e^x = 1 + x + \frac{x^2}{2} + \mathcal{O}(x^3)$, $\ln(1+x) = x - \frac{x^2}{2} + \mathcal{O}(x^3)$ to rapidly cancel vanishing lower-order differentials.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Approaches but never reaches"* | $0 < |x - a| < \delta$ | Evaluation in punctured open interval excluding center point. |
| *"Zero over zero"* | Indeterminate form $\frac{0}{0}$ | Competing vanishing infinitesimals requiring algebraic or series resolution. |
| *"One to power infinity"* | $1^\infty \implies e^{\lim (f-1)g}$ | Competing rates of exponential growth vs algebraic decay yielding Euler's constant. |

#### C. Misconception Contrasts
1. **Misconception: Evaluating $f(a)$ Instead of Limit**:
   - *Flawed Action*: Stating $\lim_{x \to 0} \frac{\sin x}{x}$ is undefined because $\frac{\sin 0}{0} = \frac{0}{0}$.
   - *Correct Diagnostic Cue*: A limit evaluates the approach in a punctured neighborhood $x \neq 0$. Cancellation of vanishing factors is mathematically rigorous because $x \neq 0$.
2. **Misconception: Treating $1^\infty$ as Trivial 1**:
   - *Flawed Action*: Concluding $\lim_{x \to 0} (1 + x)^{1/x} = 1$ because "1 to any power is 1".
   - *Correct Diagnostic Cue*: The base $(1+x)$ is not identical to constant 1; it is a dynamic quantity approaching 1 at a rate competing with the exponent approaching $\infty$. This tension resolves to Euler's number $e$.
3. **Misconception: Degree Angle in Trigonometric Limits**:
   - *Flawed Action*: Computing $\lim_{x \to 0} \frac{\sin x^\circ}{x} = 1$.
   - *Correct Diagnostic Cue*: The derivative and limit proofs rely on arc length on the unit circle equaling radian angle $\theta$. In degrees, $x^\circ = \frac{\pi x}{180}$ radians, so the limit is $\frac{\pi}{180}$.

### 13.3 Layer 3: Reconstructable TTU Library

#### TTU-LIM-01: Incomplete Rationalization & Algebraic Factorization Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Evaluate lim_{x -> 0} [ √(1 + x) - √(1 - x) ] / x.

Step 1: Check form at x = 0:
        Numerator: √(1 + 0) - √(1 - 0) = 1 - 1 = [ ___ ]
        Denominator: [ ___ ]
        Form is: [ 0/0 / ∞/∞ / 1^∞ ]

Step 2: Multiply numerator and denominator by conjugate:
        Conjugate of [ √(1+x) - √(1-x) ] is [ √(1+x) + √(1-x) ]
        Expression = [ (√(1+x) - √(1-x))(√(1+x) + √(1-x)) ] / [ x · (√(1+x) + √(1-x)) ]

Step 3: Simplify numerator using (a - b)(a + b) = a² - b²:
        Numerator = (1 + x) - (1 - x) = 1 + x - 1 + x = [ ___ ]x

Step 4: Cancel common non-zero factor x (since x -> 0 implies x ≠ 0):
        Expression = [ ___ ] / [ √(1+x) + √(1-x) ]

Step 5: Evaluate limit by direct substitution:
        Limit = [ ___ ] / [ √(1+0) + √(1-0) ] = [ ___ ] / (1 + 1) = [ ___ ] / 2 = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 0; 0; 0/0
Step 3: 2
Step 4: 2
Step 5: 2; 2; 2; 1
```

#### TTU-LIM-02: Indeterminate Form $1^\infty$ Exponential Decompilation Model (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Evaluate L = lim_{x -> 0} (cos x)^{1/x²}.

Step 1: Check form at x = 0:
        Base: cos(0) = [ ___ ]
        Exponent: 1/0² = [ ___ ]
        Indeterminate form: [ 0/0 / 1^∞ / ∞^0 ]

Step 2: Apply 1^∞ theorem: lim [f(x)]^g(x) = e^{ lim [f(x) - 1] · g(x) }:
        L = e^K, where K = lim_{x -> 0} [ cos x - [ ___ ] ] · (1 / x²)

Step 3: Express K using half-angle trigonometric identity:
        1 - cos x = 2 sin²(x/2)  ==>  cos x - 1 = -[ ___ ] sin²(x/2)
        K = lim_{x -> 0} [ -2 sin²(x/2) ] / x²

Step 4: Regroup into standard limit form [ sin(u) / u ]:
        K = -2 · lim_{x -> 0} [ sin(x/2) / (x/2) ]² · ( (x/2)² / x² )
        K = -2 · [ [ ___ ] ]² · ( [ ___ ] / 4 ) = -2 · 1 · (1/4) = -[ ___ ] / [ ___ ]

Step 5: Compute final limit L = e^K:
        L = e^[ _____ ] = 1 / √e

[COMPLETION DERIVATION KEY]
Step 1: 1; ∞; 1^∞
Step 2: 1
Step 3: 2
Step 4: 1; 1; 1; 2 (-1/2)
Step 5: -1/2
```

### 13.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-LIM-01 (Foundation / CBSE):
  Basic algebraic limits via factorization and rationalization, standard limits (x^n-a^n)/(x-a) and sin(x)/x, left/right hand limit tests for continuity.
FAMILY-LIM-02 (Olympiad / IOQM):
  Cesàro-Stolz theorem for sequence limits, bounding sums via Riemann integration lim sum 1/n f(r/n), and functional equation limits.
FAMILY-LIM-03 (JEE Main):
  Trigonometric limits with compound angles, exponential and logarithmic limits lim (e^x-1)/x = 1, evaluation of 1^∞ forms, L'Hôpital's Rule iterations.
FAMILY-LIM-04 (JEE Advanced):
  Limits involving greatest integer functions floor(x), fractional part {x}, series expansions with non-canceling higher-order differentials, and asymptotic order analysis.
```

---

## 14. Foundation Packet: Combinatorics, Permutations & Counting Invariants (`MATH-PERM-COMB`)

### 14.1 Layer 1: Mathematical Core & Non-Negotiable Preconditions

- **Canonical Subtopic ID**: `MATH-PERM-COMB`
- **Engineering Gate Binding**: `MATH-PERM-COMB` (Digest-bound closure receipt)
- **Learner Title**: Combinatorics, Fundamental Counting Principles, Permutations & Combinations
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 10 (Board/Olympiad) &bull; Grade 11 (JEE Main/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Strict Discrete Domain Invariant**: $n, r \in \mathbb{N}_0$ with $0 \le r \le n$. Factorial $n! = \prod_{k=1}^n k$ with the axiomatic definition $0! \equiv 1$ (the unique number of ways to order an empty set $\emptyset$).
  2. **Disjoint Case Mutual Exclusivity (Addition Principle)**: If events $A_1, \dots, A_k$ are pairwise mutually exclusive ($A_i \cap A_j = \emptyset$ for $i \neq j$), the total number of ways to perform any one event is $\sum |A_i|$.
  3. **Order Sensitivity Trichotomy**:
     - *Permutations* ($nPr$): Order of selection is distinct and significant ($\{A, B\} \neq \{B, A\}$).
     - *Combinations* ($nCr$): Order of selection is irrelevant; subsets are unordered ($\{A, B\} \equiv \{B, A\}$).

### 14.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-COMB-01` (`CONCEPT`): Fundamental Principle of Counting (FPC):
  - Multiplication rule: If operation 1 has $m$ outcomes and operation 2 has $n$ independent outcomes, the composite sequential operation has $m \times n$ outcomes.
  - Addition rule: If operation can be done via mutually exclusive pathways, total outcomes is $m + n$.
- `ATOM-COMB-02` (`INVARIANT`): Pascal's Combination Recurrence: $\binom{n}{r} + \binom{n}{r-1} = \binom{n+1}{r}$ for all $1 \le r \le n$. Symmetric property: $\binom{n}{r} = \binom{n}{n-r}$.
- `ATOM-COMB-03` (`PROCEDURE`): Stars and Bars Multiset Partition Theorem: The number of non-negative integer solutions to $x_1 + x_2 + \dots + x_k = n$ ($x_i \ge 0$) is $\binom{n + k - 1}{k - 1}$. For strictly positive integer solutions ($x_i \ge 1$), it is $\binom{n - 1}{k - 1}$.
- `ATOM-COMB-04` (`RELATION`): Circular Permutation Reduction: The number of distinct circular arrangements of $n$ distinct objects is $(n-1)!$. If clockwise and counter-clockwise arrangements are indistinguishable (e.g. necklaces/garlands), it is $\frac{(n-1)!}{2}$.
- `ATOM-COMB-05` (`STRATEGY`): Grouping / String and Gap Methods:
  - *String method* (objects must be together): Bundle required items into a single mega-element and multiply by internal permutations.
  - *Gap method* (no two objects may be together): Arrange remaining items first, then place constrained items into the available inter-item gaps.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Arrange in a line"* | $n!$ or $nPr = \frac{n!}{(n-r)!}$ | Ordered bijective injection from $\{1,\dots,r\} \to S$. |
| *"Select a committee"* | $\binom{n}{r} = \frac{n!}{r!(n-r)!}$ | Unordered subset selection of cardinality $r$. |
| *"Distribute identical items to distinct boxes"* | $\binom{n+k-1}{k-1}$ | Weak composition / multiset partition via Stars and Bars. |

#### C. Misconception Contrasts
1. **Misconception: Confusing Addition and Multiplication Rules**:
   - *Flawed Action*: If a task requires choosing a shirt (3 colors) AND a tie (4 colors), calculating $3 + 4 = 7$.
   - *Correct Diagnostic Cue*: When actions occur *in conjunction* (successively/jointly), the outcomes multiply: $3 \times 4 = 12$. Addition applies only to *alternative, mutually exclusive* choices (either a shirt OR a tie).
2. **Misconception: Overcounting via Independent Sequential Selections**:
   - *Flawed Action*: Selecting 4 people from 10 including at least 1 woman (from 4 women) by picking 1 woman ($\binom{4}{1}$) and then any 3 from the remaining 9 ($\binom{9}{3}$).
   - *Correct Diagnostic Cue*: Sequential picking labels the chosen elements as "the first woman" and "subsequent people", creating artificial ordering among women and drastically overcounting. Use complementary counting: Total $-$ No Women $= \binom{10}{4} - \binom{6}{4}$.
3. **Misconception: Dividing by 2 for General Circular Arrangements**:
   - *Flawed Action*: Dividing by 2 when seating people around a round table.
   - *Correct Diagnostic Cue*: People have distinct left and right orientations; rotating a table does not flip left and right. Only unoriented physical loops that can be flipped over in 3D (like beads on a necklace) divide by 2: $\frac{(n-1)!}{2}$.

### 14.3 Layer 3: Reconstructable TTU Library

#### TTU-COMB-01: Incomplete Complementary Counting & Gap Method Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: In how many ways can 5 boys and 4 girls be seated in a row such that no two girls are together?

Step 1: Identify method: Constrained items (girls) cannot be adjacent ==> Use [ Gap Method / String Method ].
Step 2: Arrange the unconstrained items (5 boys) first:
        Number of ways to seat 5 boys in a row: 5! = [ ___ ]

Step 3: Count available gaps created by 5 boys:
        _ B1 _ B2 _ B3 _ B4 _ B5 _
        Number of available gaps = 5 + 1 = [ ___ ] gaps.

Step 4: Select and arrange 4 girls in the available gaps:
        Number of ways to choose 4 gaps out of 6 and arrange 4 girls:
        P(6, 4) = 6! / (6 - 4)! = 6! / [ ___ ]! = (6 · 5 · 4 · 3 · 2 · 1) / 2 = [ ___ ]

Step 5: Apply Fundamental Multiplication Principle:
        Total arrangements = (ways to arrange boys) · (ways to place girls in gaps)
                           = [ ___ ] · [ ___ ] = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Gap Method
Step 2: 120
Step 3: 6
Step 4: 2; 360
Step 5: 120; 360; 43200
```

#### TTU-COMB-02: Stars and Bars Multiset Partitioning Model (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Task: Find the number of non-negative integer solutions to x₁ + x₂ + x₃ + x₄ = 12.
      Also find the number of strictly positive integer solutions.

Case A: Non-negative integer solutions (x_i ≥ 0):
Step 1: Identify items n and categories k:
        n (stars) = [ ___ ],   k (variables) = [ ___ ]
Step 2: Apply Stars and Bars Theorem 1:
        Total solutions = C(n + k - 1, k - 1)
                        = C(12 + 4 - 1, 4 - 1)
                        = C([ ___ ], [ ___ ])
Step 3: Calculate numerical value:
        C(15, 3) = (15 · 14 · 13) / (3 · 2 · 1) = (5 · 7 · 13) = [ ___ ]

Case B: Strictly positive integer solutions (x_i ≥ 1):
Step 4: Apply Stars and Bars Theorem 2:
        Total solutions = C(n - 1, k - 1)
                        = C(12 - 1, 4 - 1)
                        = C([ ___ ], [ ___ ])
Step 5: Calculate numerical value:
        C(11, 3) = (11 · 10 · 9) / (3 · 2 · 1) = (11 · 5 · 3) = [ ___ ]

[COMPLETION DERIVATION KEY]
Case A:
Step 1: 12; 4
Step 2: 15; 3
Step 3: 455
Case B:
Step 4: 11; 3
Step 5: 165
```

### 14.4 Layer 4: Problem Families & Transfer Scaffolds

```text
FAMILY-COMB-01 (Foundation / CBSE):
  Basic factorial arithmetic, evaluation of nPr and nCr, word arrangements with repeats (e.g. MATHEMATICS), formation of numbers from digits.
FAMILY-COMB-02 (Olympiad / IOQM):
  Principle of Inclusion-Exclusion (PIE), derangements D_n, double counting proofs, Catalan numbers C_n = 1/(n+1) C(2n, n), Pigeonhole Principle.
FAMILY-COMB-03 (JEE Main):
  Multiset distribution of identical objects (stars and bars), grouping into heaps (dividing by p!), rank of word in dictionary, sum of digits formed.
FAMILY-COMB-04 (JEE Advanced):
  Generating functions for integer partitions, Burnside's Lemma for rotational symmetries, grid walk lattice paths avoiding boundary y = x.
```

---

## 15. Intake Validation Checklist for Future Subtopics

To admit any new mathematics subtopic into the library, it must pass this 6-point intake gate:

1. **Exact Precondition Proof**: Mathematical domain boundaries (denominators $\neq 0$, radicands $\ge 0$, leading coefficients $\neq 0$) must be formally declared in Layer 1.
2. **Atomic Decomposition**: The topic must be factored into at least 4 typed Learning Atoms in Layer 2.
3. **Misconception Pairings**: At least 2 verified student misconceptions with diagnostic contrasts must be articulated.
4. **Reconstructable TTU Pair**: At least one complete Concept TTU and one reconstructive Problem TTU with explicit completion keys must be authored in Layer 3.
5. **Exam Family Mapping**: Clear mapping to at least 2 distinct competitive examination families (e.g. CBSE + JEE Main, or IOQM + JEE Advanced) must be provided in Layer 4.
6. **Zero Topic Hardcoding**: All metadata, terms, and rules must live in JSON data files; zero topic-specific branch logic may be added to Python engine code.




