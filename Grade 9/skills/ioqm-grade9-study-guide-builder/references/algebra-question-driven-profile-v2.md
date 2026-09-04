# Algebra Question-Driven Study Guide Profile v2

## Role

This is the **Algebra-specific profile** for the generalized question-driven study-guide skill.

It captures the lessons from rebuilding the Grade 9 IOQM Algebra guide against a 50-question supplied corpus after the first polished PDF failed a benchmark/self-sufficiency audit.

Use this profile together with:

- `../SKILL.md`
- `question-driven-self-sufficient-study-guide-skill-v2.md`

The generalized skill owns production mechanics. This profile owns Algebra-specific teaching families, recognition cues, legality checks, likely orphan methods, visual use, and Appendix A hint references.

---

## 1. Algebra learner objective

The Algebra guide should teach a half-prepared learner to move from:

**surface wording -> structural compression -> legal transformation -> small-variable model -> execution -> branch/domain check.**

The strongest Algebra solutions often do **not** require more computation. They require choosing the representation that closes.

Examples:

- `x+y, xy` instead of solving for `x,y`;
- `s,q,r` instead of expanding three-variable symmetric expressions;
- `p=xyz` instead of solving three nonlinear equations;
- a recurrence state instead of listing many terms;
- Vieta / power sums instead of explicit roots;
- midpoint shift instead of high-degree rational expansion;
- a strategic polynomial evaluation instead of discriminant brute force.

The guide must teach those representation choices explicitly.

---

## 2. Stable Algebra skill families

Use stable IDs so Appendix A hints can point back to previously taught material.

### Foundations, identities, and factorization

- `ALG-ID-01` — standard identities as structural tools, not memory-only formulas
- `ALG-FAC-01` — manufactured factorization / add-subtract to create a product
- `ALG-FAC-02` — cyclic orientation differences and Vandermonde-type factors
- `ALG-FAC-03` — difference of powers and factor-theorem preparation

### Equations and legal manipulation

- `ALG-EQ-01` — equivalence versus implication
- `ALG-EQ-02` — denominator clearing and excluded values
- `ALG-EQ-03` — squaring / radicals / extraneous roots
- `ALG-EQ-04` — rational equations with symmetric poles and midpoint shifts

### Linear systems and averages

- `ALG-LIN-01` — system setup from verbal conditions
- `ALG-LIN-02` — averages as total/count equations
- `ALG-LIN-03` — deletion/restoration of terms and changing counts

### Symmetric two-variable methods

- `ALG-SYM2-01` — set `s=x+y`, `p=xy`
- `ALG-SYM2-02` — rebuild targets: `x^2+y^2=s^2-2p`, `(x-y)^2=s^2-4p`
- `ALG-SYM2-03` — reciprocal-ratio substitutions and complementary identities
- `ALG-SYM2-04` — branch comparison / admissibility

### Symmetric and cyclic three-variable methods

- `ALG-SYM3-01` — `s=x+y+z`, `q=xy+yz+zx`, `r=xyz`
- `ALG-SYM3-02` — cubic power identity `x^3+y^3+z^3=s^3-3sq+3r`
- `ALG-SYM3-03` — reciprocal sum `1/x+1/y+1/z=q/r`
- `ALG-CYC-01` — common-value cyclic systems
- `ALG-CYC-02` — repeated common product `p=xyz`
- `ALG-CYC-03` — complementary cyclic fractions via total sum
- `ALG-CYC-04` — cyclic orientation comparison and forced equality

### Quadratics and root geometry

- `ALG-QUAD-01` — discriminant and real-root classification
- `ALG-QUAD-02` — double root / tangent interpretation
- `ALG-QUAD-03` — simultaneous discriminant inequalities and integer bounds
- `ALG-QUAD-04` — root-sign / coefficient-sign logic

### Polynomial structure

- `ALG-POLY-01` — factor theorem and `P(x)-P(a)`
- `ALG-POLY-02` — remainder theorem / strategic evaluation
- `ALG-POLY-03` — Vieta for monic polynomials
- `ALG-POLY-04` — repeated roots via `f(r)=f'(r)=0`
- `ALG-POLY-05` — composition and quadratic preimage symmetry
- `ALG-POLY-06` — linked-coefficient elimination through root variables

### Power sums and root-reciprocal tools

- `ALG-ROOTSUM-01` — Newton-style power-sum recurrence
- `ALG-ROOTSUM-02` — changed constant term / preserved symmetric coefficients
- `ALG-ROOTSUM-03` — logarithmic derivative `P'(t)/P(t)` for reciprocal root sums
- `ALG-ROOTSUM-04` — repeated-root multiplicity counting in Vieta sums

### Inequalities and extrema

- `ALG-INEQ-01` — AM-GM with positivity and equality conditions
- `ALG-INEQ-02` — smoothing under fixed sum
- `ALG-INEQ-03` — boundary versus interior extrema
- `ALG-INEQ-04` — ordered-mass / order-statistic bounds
- `ALG-INEQ-05` — equality construction to prove attainability

### Progressions and finite differences

- `ALG-AP-01` — arithmetic progression parameterization
- `ALG-GP-01` — geometric progression parameterization and convergence
- `ALG-MIXSEQ-01` — overlapping AP/GP structures
- `ALG-MIXSEQ-02` — product of AP terms -> quadratic sequence -> constant second difference
- `ALG-MIXSEQ-03` — AP x GP parameterization
- `ALG-GP-02` — rational ratio integrality / denominator divisibility
- `ALG-HP-01` — H.P. bridge where required, explicitly scope-limited if not used

### Recurrences and symbolic pattern proof

- `ALG-REC-01` — derive shift identities from a recurrence
- `ALG-REC-02` — prove periodicity rather than guess it
- `ALG-REC-03` — symbolic term pattern -> induction / structural proof
- `ALG-REC-04` — alternating AP/GP recurrence patterns

### Indices, exponentials, radicals, logarithms

- `ALG-EXP-01` — normalize exponents with a common base-variable substitution
- `ALG-EXP-02` — translate root products in transformed variable back to sums of original exponents
- `ALG-RAD-01` — radical legality and simplification
- `ALG-ALGNUM-01` — linear independence of algebraic irrational bases over the rationals
- `ALG-LOG-01` — log legality / base restrictions when logs are actually needed

### Functional and composition identities

- `ALG-FE-01` — strategic substitutions in functional equations
- `ALG-FE-02` — polynomial functional identity and nested-value naming
- `ALG-FE-03` — coefficient comparison only after identity is established

### Complex-number bridge

- `ALG-CPLX-01` — complex roots are legal unless reality is stated
- `ALG-CPLX-02` — Vieta and symmetric identities over complex numbers
- `ALG-CPLX-03` — do not discard algebraic branches because a quadratic discriminant is negative

### Integer / Diophantine / discrete bridges

- `ALG-INT-01` — integer-factor compatibility and square filters
- `ALG-INT-02` — gap variables for ordered integer triples
- `ALG-INT-03` — monic integer-root consequences
- `ALG-INT-04` — divisibility filters from AP/GP parameterization
- `ALG-DISC-01` — bounded digit sums via stars-and-bars + inclusion-exclusion

---

## 3. Recommended chapter order

A strong dependency order for the 50%-prepared Algebra learner is:

1. Algebraic language and structural identities
2. Manufactured factorization and legal equation manipulation
3. Rational equations and denominator/domain discipline
4. Linear systems, totals, averages, deletion/restoration
5. Symmetric two-variable substitution
6. Symmetric and cyclic three-variable systems
7. Quadratics, discriminants, root signs
8. Polynomial factor/remainder ideas and Vieta
9. Repeated roots, power sums, logarithmic derivative, multiplicity
10. Inequalities, smoothing, equality cases, order-statistic bounds
11. AP, GP, mixed progressions, rational ratios
12. Finite differences and product sequences
13. Recurrences, shift identities, periodicity, symbolic pattern proof
14. Indices, exponentials, radicals, algebraic irrationals
15. Functional / polynomial identities
16. Complex-number bridge
17. Integer / Diophantine / discrete bridges
18. Mixed method-selection lab
19. Advanced Worked Bridges
20. Appendix A + hints
21. Appendix B
22. Appendix C / quick reference

Regroup if the actual supplied corpus requires a different prerequisite order.

---

## 4. Algebra-specific orphan-method traps

The following are common false-positive coverage claims.

### “Vieta is taught”

Not enough if the learner cannot:

- convert a target into `s,p` or `s,q,r`;
- handle higher power sums;
- count repeated-root multiplicities;
- combine Vieta with integer-root restrictions;
- understand when complex roots are allowed.

### “AP/GP is taught”

Not enough if the learner cannot:

- parameterize overlapping AP and GP triples;
- prove rational GP denominator divisibility;
- derive second differences from products of AP terms;
- handle an alternating AP/GP recurrence;
- compare an infinite GP with its squared-term series.

### “Repeated roots are taught”

Not enough if the guide states `f=f'=0` but never explains:

- why a repeated root satisfies both;
- how this relates to tangency / exactly one distinct real root;
- why a global-shape check may still be needed.

### “Symmetric sums are taught”

Not enough if the learner cannot:

- decide between `s,p` and `s,q,r`;
- recover reciprocal sums;
- compare branches;
- exploit `p=xyz` in a cyclic system;
- turn a large odd-power target into an opposite-pair cancellation.

### “Functional equations are taught”

Not enough if the chapter contains only `try x=0,1`.

For polynomial functional identities, teach naming nested values and using self-consistency.

### “Indices are taught”

Not enough if the learner cannot see that all exponents share a common multiple and convert an exponential equation into a polynomial.

### “Integer filters are obvious”

They are not.

Teach how positivity, integrality, divisibility, ordering, and bounded coefficients shrink continuous algebra into finite cases.

---

## 5. Algebra visual-pedagogy profile

Algebra should not be made artificially pictorial. Use visuals when they reveal structure more efficiently than symbols.

### Strong-use cases

#### Root geometry

Use graphs for:

- two distinct real roots;
- double/tangent root;
- no real root;
- quartic touching the axis at one distinct real zero.

These visuals are especially useful beside `ALG-QUAD-02` and `ALG-POLY-04`.

#### Sign / domain intervals

Use number-line diagrams for:

- rational inequalities;
- denominator exclusions;
- radical domains;
- sign changes between polynomial roots.

#### Function composition

Use a small mapping schematic for `ALG-POLY-05` when explaining why four roots of `P(Q(x))` are preimages under `Q` of two roots of `P`.

#### Sequence evolution

Use compact term tables / arrow diagrams for:

- finite differences;
- recurrence shift identities;
- alternating AP/GP structure;
- periodicity.

#### Inequality smoothing

Use a feasible-interval or one-variable reduction diagram when it genuinely clarifies why fixing one variable reduces the problem to maximizing/minimizing a product.

### Avoid low-value visuals

Do not add:

- decorative coordinate grids;
- generic parabola pictures when the question is purely symbolic;
- stock math imagery;
- complex diagrams that are harder to read than the algebra.

### Figure integrity

Every Algebra figure must:

- have readable labels;
- use the same variables as the nearby text;
- be mathematically correct;
- state `not to scale` if appropriate;
- be inspected at 200 dpi in the final PDF.

---

## 6. Appendix A hint architecture for Algebra

Appendix A should preserve the supplied 50-question corpus, but hard questions should receive progressive hints referring to earlier Algebra skill IDs / bridges.

The preferred layout is:

1. questions remain clean;
2. after all questions, include an **Appendix A Hint Bank**;
3. answers remain after the hint bank or in the final answer-key section, depending on the chosen student flow;
4. each hint entry uses `H1`, `H2`, `H3` progressively.

### H1 — recognize the family

Example:

> **Q1 H1:** The equations contain both `x+y` and `xy`. Revisit `ALG-SYM2-01`.

### H2 — first useful line

Example:

> **Q1 H2:** Set `s=x+y` and `p=xy`. Translate both equations into `s,p`.

### H3 — execution direction

Example:

> **Q1 H3:** Once `s,p` are known, do not solve for `x,y`; use `ALG-SYM2-02` to rebuild `x^2+y^2`.

No hint prints the final answer.

---

## 7. Suggested hint-depth policy for the 50-question Algebra corpus

This is a **difficulty/support profile**, not a source-order authority claim.

### Usually `H1` only

Questions where the taught method is direct once recognized:

- Q8
- Q12
- Q18
- Q20
- Q24
- Q29
- Q34
- Q37
- Q49

### Usually `H1-H2`

Questions with a non-obvious opening but routine execution after the first line:

- Q1
- Q4
- Q5
- Q6
- Q7
- Q9
- Q11
- Q13
- Q16
- Q17
- Q19
- Q21
- Q22
- Q25
- Q30
- Q35
- Q39
- Q45

### Usually `H1-H3`

Questions with a genuine execution bottleneck or cross-topic bridge:

- Q2 — cyclic reciprocal product collapse
- Q3 — exponent substitution + transformed-root product
- Q10 — common-value cyclic multiplication
- Q14 — symmetric cubic factor + opposite pair
- Q15 — factor theorem + unique integer-root case split
- Q23 — two distinct GPs sharing second term
- Q26 — changed constant term + power sums
- Q27 — cyclic orientation / Vandermonde factorization
- Q28 — pole symmetry + midpoint shift + `t^2`
- Q31 — algebraic irrational linear independence
- Q32 — nested polynomial functional identity
- Q33 — nonlinear system collapsed to `p=xyz`
- Q36 — Vieta with repeated multiplicities
- Q38 — rational GP integrality under score bounds
- Q40 — smoothing and global boundary check
- Q41 — linked coefficients -> root Diophantine enumeration
- Q42 — tangent root plus global quartic shape
- Q43 — engineered subtraction yielding common factor
- Q44 — quadratic preimage pairing in composition
- Q46 — strategic `P(-1)` and necessity/sufficiency
- Q47 — AP x GP parameterization
- Q48 — bounded stars-and-bars / inclusion-exclusion
- Q50 — symbolic alternating AP/GP pattern and proof

Adjust after actual learner/teacher review if evidence becomes available.

---

## 8. Example H1-H3 ladders for difficult Algebra questions

These examples illustrate style only. They deliberately avoid final answers.

### Cyclic reciprocal system

- **H1:** The three expressions become much simpler when multiplied together under the condition `xyz=1`. See `ALG-CYC-01`.
- **H2:** Name the requested cyclic expression `t` and multiply the three given sums before trying to solve individual variables.
- **H3:** Expand only far enough to use `xyz=1`; compare the resulting product with the product of the known numerical expressions.

### Exponential roots

- **H1:** All exponents are built from one common multiple. See `ALG-EXP-01`.
- **H2:** Set `u=2^(kx)` for the largest useful common `k` so that the equation becomes a polynomial in `u`.
- **H3:** The question asks for a sum of `x`-roots; use the **product** of the positive `u`-roots and translate it back with `ALG-EXP-02`.

### Composition of quadratics

- **H1:** Roots of `P(Q(x))` are inputs that `Q` sends to roots of `P`. See `ALG-POLY-05`.
- **H2:** For a quadratic `Q`, equal outputs occur at input pairs symmetric about its axis, so paired inputs have a constant sum.
- **H3:** Pair the four given roots into two pairs with the same sum; that determines the linear coefficient of `Q` before you compare the second composition.

### Strategic polynomial evaluation

- **H1:** The polynomial is designed to simplify at a small integer. See `ALG-POLY-02` and `ALG-QUAD-04`.
- **H2:** First determine the signs of the two integer roots from their sum and product; then interpret `P(-1)` as a product involving those roots.
- **H3:** Compute `P(-1)` from the coefficients and compare its sign with the root-factor interpretation. Equality should force a simple linear relation among the parameters.

### Bounded digit sum

- **H1:** Treat numbers below `10000` as four-digit strings with leading zeros. See `ALG-DISC-01`.
- **H2:** The digit sum can only be the positive multiples of `11` that do not exceed `36`.
- **H3:** Use stars-and-bars for each target sum, subtract digit values `>=10` by inclusion-exclusion, and use the `d -> 9-d` complement for a sum close to `36`.

---

## 9. Algebra-specific Advanced Worked Bridge obligations

Before self-sufficiency can pass, add non-identical bridges for any corpus-required method not already executable in the main chapters.

The 50-question rebuild showed high-value bridge families including:

- cyclic reciprocal product collapse;
- changing-average linear systems;
- polygon AP with integrality/parity/convexity;
- simultaneous discriminant inequalities;
- common-value cyclic multiplication;
- large odd-power cancellation from symmetric cubic factorization;
- factor-theorem uniqueness counting;
- order-statistic mass bounds with equality construction;
- GP versus squared-term GP;
- two distinct GPs with same second term;
- changed polynomial constant term and power sums;
- cyclic Vandermonde factorization;
- symmetric-pole midpoint shift;
- algebraic-number linear independence;
- nested polynomial functional identity;
- repeated-root multiplicity counting;
- rational-GP denominator divisibility;
- smoothing / boundary optimization;
- linked-coefficient integer-root enumeration;
- quartic tangency with global shape;
- quadratic preimage pairing;
- strategic polynomial evaluation;
- AP x GP product parameterization;
- bounded stars-and-bars;
- alternating AP/GP symbolic pattern proof.

Do not assume these are universally required in every Algebra guide. They are obligations only when the corpus/syllabus requires them.

---

## 10. Algebra legality checklist

Every relevant chapter / worked bridge should explicitly check the applicable conditions.

### Rational expressions

- denominator nonzero;
- no pole introduced by clearing denominators;
- excluded values not counted later.

### Radicals

- radicand/domain where working over reals;
- squaring may introduce candidates;
- final candidate substitution.

### Logarithms

- argument positive;
- base positive and not `1`;
- transformation preserves equivalence.

### Inequalities

- positivity before AM-GM;
- direction of multiplication/division by signed quantities;
- equality condition;
- boundary cases.

### Vieta / roots

- monic vs non-monic coefficients;
- multiplicity counting;
- real versus complex assumptions;
- integer-root consequences only when coefficients/integrality justify them.

### Infinite GP

- `|r|<1`;
- transformed/squared series also convergent.

### Optimization

- prove upper/lower bound;
- construct or identify equality case;
- check boundaries and interior candidates.

### Functional identities

- distinguish identity for all real/complex inputs from equation true at isolated values;
- compare coefficients only after identity status is established.

---

## 11. Appendix B Algebra audit set

Appendix B should contain approximately 20 reliable-source or clearly labeled author-created questions sampling the revised guide.

Recommended spread:

- 2 identities/factorization
- 2 symmetric systems
- 2 quadratics/root conditions
- 3 polynomial/Vieta/power-sum problems
- 2 inequalities/extrema
- 3 AP/GP/sequence/recurrence
- 2 exponent/radical/algebraic-number
- 1 functional identity
- 1 complex-number bridge
- 2 integer/discrete-filter problems

Adjust to actual guide coverage.

Every answer must be independently recomputed.

For the hardest Appendix B questions, H1-H3 hints may be included using the same skill-ID reference system.

---

## 12. Appendix C Algebra memory helper

Keep Appendix C to approximately 1-2 pages.

High-value items include:

- standard identities and manufactured factor patterns;
- `s,p` and `s,q,r` identities;
- discriminant/root facts;
- Vieta;
- factor/remainder theorem;
- repeated-root condition;
- AP/GP formulas;
- finite-difference reminder;
- index laws;
- radical/log legality;
- AM-GM with equality condition;
- core binomial identities if actually taught;
- `P'(t)/P(t)` reciprocal-root identity if taught;
- candidate-check checklist;
- stable skill IDs for deeper review where space permits.

Do not put full worked solutions in Appendix C.

---

## 13. Algebra self-sufficiency acceptance

For a corpus of `n` Algebra questions, require:

```text
ALGEBRA_QUESTION_INVENTORY = PASS_n_OF_n
ALGEBRA_QUESTION_TO_METHOD_MATRIX = PASS_n_OF_n
ALGEBRA_ORPHAN_METHOD_AUDIT = PASS_n_OF_n
ALGEBRA_VISUAL_PEDAGOGY_AUDIT = PASS_n_OF_n
ALGEBRA_APPENDIX_A_CUSTODY = PASS_n_OF_n
ALGEBRA_APPENDIX_A_HINT_AUDIT = PASS_n_OF_n
ALGEBRA_STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
```

For the 50-question corpus that motivated this profile, the valid target is:

```text
ALGEBRA_STATIC_CONTENT_SELF_SUFFICIENCY = PASS_50_OF_50
```

Do not infer:

- classroom solve rate;
- timing;
- retention;
- psychometric calibration;
- IOQM qualification probability.

Those require separate evidence.

---

## 14. Algebra PDF acceptance

Do not generate the final PDF while any question is `PARTIAL` or `FAIL`.

After the content gate closes:

- integrate guide, worked bridges, Appendix A, hint bank, Appendix B, Appendix C, and student-appropriate sources;
- render every page at 200 dpi;
- visually inspect every page;
- inspect graphs/diagrams at final size;
- check mathematical glyphs and line wrapping;
- ensure H1/H2/H3 formatting is visibly progressive;
- ensure answer key is not accidentally adjacent to unsolved questions in a way that defeats practice;
- record exact page count and SHA-256.

---

## 15. Final Algebra principle

A high-quality Algebra guide should not train the learner to ask only:

> “Which formula applies?”

It should train the learner to ask:

1. What structure repeats?
2. Which variables can be compressed?
3. Which operations are reversible?
4. What is the smallest useful representation?
5. Which branch / domain / equality condition survives?
6. Can I prove the extremum or integer restriction is attainable?
7. Which previously learned Algebra skill ID does this resemble?

That is the behavior the guide, worked bridges, visuals, and H1-H3 hint system should reinforce.
