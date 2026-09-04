# Algebra Question-Driven Study Guide Profile v2

## Role

This is the Algebra-specific profile for the generalized question-driven study-guide skill.

Use it with:

- `../SKILL.md`
- `question-driven-self-sufficient-study-guide-skill-v2.md`

The generalized contract owns production mechanics. This profile owns Algebra-specific method families, recognition cues, legality checks, visual use, likely orphan methods, and Appendix A hint behavior.

It incorporates the lessons from the 50-question Algebra rebuild where a polished first PDF failed a benchmark/self-sufficiency audit.

---

## 1. Algebra learner objective

Teach a half-prepared learner to move from:

**surface wording -> structural compression -> legal transformation -> small-variable model -> execution -> branch/domain check.**

The strongest Algebra solutions often require a better representation rather than more computation.

Typical compression moves include:

- `s=x+y`, `p=xy` instead of solving for `x,y`;
- `s=x+y+z`, `q=xy+yz+zx`, `r=xyz` instead of raw expansion;
- `p=xyz` when the same product repeats through a nonlinear system;
- midpoint shift in symmetric rational equations;
- Vieta/power sums instead of explicit roots;
- recurrence state instead of listing many terms;
- strategic evaluation such as `P(-1)` instead of brute-force discriminants.

The guide must teach why and when those representation choices close the problem.

---

## 2. Stable Algebra skill families

Use stable IDs so hints can retrieve previously taught methods.

### Foundations and factorization

- `ALG-ID-01 · Structural identities`
- `ALG-FAC-01 · Manufactured factorization`
- `ALG-FAC-02 · Cyclic orientation / Vandermonde factorization`
- `ALG-FAC-03 · Difference-of-powers and factor-theorem preparation`

### Legal equation manipulation

- `ALG-EQ-01 · Equivalence versus implication`
- `ALG-EQ-02 · Denominator clearing and excluded values`
- `ALG-EQ-03 · Squaring, radicals, extraneous roots`
- `ALG-EQ-04 · Symmetric poles and midpoint shifts`

### Linear systems, totals, averages

- `ALG-LIN-01 · Translating verbal conditions into equations`
- `ALG-LIN-02 · Average = total / count`
- `ALG-LIN-03 · Deletion/restoration with changing counts`

### Symmetric two-variable methods

- `ALG-SYM2-01 · Sum-product substitution`
- `ALG-SYM2-02 · Rebuild targets from s,p`
- `ALG-SYM2-03 · Reciprocal-ratio identities`
- `ALG-SYM2-04 · Branch comparison and admissibility`

### Symmetric/cyclic three-variable methods

- `ALG-SYM3-01 · s,q,r substitution`
- `ALG-SYM3-02 · Cubic power identity`
- `ALG-SYM3-03 · Reciprocal sum q/r`
- `ALG-CYC-01 · Common-value cyclic systems`
- `ALG-CYC-02 · Repeated product p=xyz`
- `ALG-CYC-03 · Complementary cyclic fractions`
- `ALG-CYC-04 · Cyclic orientation comparison`

### Quadratics and root geometry

- `ALG-QUAD-01 · Discriminant and root classification`
- `ALG-QUAD-02 · Double root / tangency`
- `ALG-QUAD-03 · Simultaneous discriminant inequalities`
- `ALG-QUAD-04 · Root-sign logic`

### Polynomial structure

- `ALG-POLY-01 · Factor theorem and P(x)-P(a)`
- `ALG-POLY-02 · Remainder theorem / strategic evaluation`
- `ALG-POLY-03 · Vieta`
- `ALG-POLY-04 · Repeated roots via f=f'=0`
- `ALG-POLY-05 · Composition and quadratic preimage symmetry`
- `ALG-POLY-06 · Linked coefficients through root variables`

### Power sums / reciprocal roots

- `ALG-ROOTSUM-01 · Newton-style power sums`
- `ALG-ROOTSUM-02 · Changed constant term / preserved symmetric coefficients`
- `ALG-ROOTSUM-03 · Logarithmic derivative P'/P`
- `ALG-ROOTSUM-04 · Multiplicity-aware Vieta counting`

### Inequalities and extrema

- `ALG-INEQ-01 · AM-GM with equality conditions`
- `ALG-INEQ-02 · Smoothing under fixed sum`
- `ALG-INEQ-03 · Boundary versus interior extrema`
- `ALG-INEQ-04 · Order-statistic mass bounds`
- `ALG-INEQ-05 · Equality construction / attainability`

### Progressions and finite differences

- `ALG-AP-01 · Arithmetic progression parameterization`
- `ALG-GP-01 · Geometric progression and convergence`
- `ALG-GP-02 · Rational GP ratio integrality/divisibility`
- `ALG-MIXSEQ-01 · Overlapping AP/GP`
- `ALG-MIXSEQ-02 · AP product -> quadratic sequence -> second difference`
- `ALG-MIXSEQ-03 · AP × GP parameterization`
- `ALG-HP-01 · H.P. bridge when genuinely required`

### Recurrences

- `ALG-REC-01 · Derive shift identities`
- `ALG-REC-02 · Prove periodicity`
- `ALG-REC-03 · Symbolic pattern -> induction`
- `ALG-REC-04 · Alternating AP/GP recurrence pattern`

### Exponents, radicals, algebraic numbers

- `ALG-EXP-01 · Common exponent substitution`
- `ALG-EXP-02 · Translate transformed-root products back to exponent sums`
- `ALG-RAD-01 · Radical legality`
- `ALG-ALGNUM-01 · Linear independence of algebraic irrational bases`
- `ALG-LOG-01 · Logarithm legality when needed`

### Functional/polynomial identities

- `ALG-FE-01 · Strategic substitutions`
- `ALG-FE-02 · Nested-value naming and self-consistency`
- `ALG-FE-03 · Coefficient comparison after identity is established`

### Complex-number bridge

- `ALG-CPLX-01 · Complex roots remain legal unless reality is required`
- `ALG-CPLX-02 · Vieta over complex numbers`
- `ALG-CPLX-03 · Do not discard branches for negative real discriminant`

### Integer / discrete bridges

- `ALG-INT-01 · Factor compatibility and square filters`
- `ALG-INT-02 · Gap variables for ordered integer triples`
- `ALG-INT-03 · Monic integer-root consequences`
- `ALG-INT-04 · Divisibility from AP/GP parameterization`
- `ALG-DISC-01 · Bounded digit sums with stars-and-bars + inclusion-exclusion`

---

## 3. Recommended chapter order

A strong default order for a 50%-prepared learner is:

1. Structural identities and factorization
2. Legal manipulation, denominators, radicals
3. Linear systems, totals, averages
4. Symmetric two-variable systems
5. Symmetric/cyclic three-variable systems
6. Quadratics and root classification
7. Factor/remainder theorem and Vieta
8. Repeated roots, power sums, P'/P, multiplicity
9. Inequalities, smoothing, equality cases
10. AP, GP, mixed progressions
11. Finite differences
12. Recurrences and pattern proof
13. Exponents, radicals, algebraic irrationals
14. Functional/polynomial identities
15. Complex-number bridge
16. Integer/Diophantine/discrete bridges
17. Mixed method-selection lab
18. Advanced Worked Bridges
19. Appendix A with adaptive hints
20. Appendix B
21. Appendix C / quick reference

Regroup if the actual supplied corpus demands a different dependency order.

---

## 4. Algebra-specific orphan-method traps

### “Vieta is taught” is not enough

The learner must also be able to:

- rebuild a target from `s,p` or `s,q,r`;
- handle higher power sums;
- count multiplicities;
- combine roots with integer restrictions;
- keep complex branches when allowed.

### “AP/GP is taught” is not enough

The learner must also be able to:

- parameterize overlapping AP/GP structures;
- justify rational GP denominator divisibility;
- identify constant second difference from products of AP terms;
- compare an infinite GP with the squared-term series;
- prove an alternating AP/GP recurrence pattern.

### “Repeated roots are taught” is not enough

Explain:

- why repeated roots satisfy `f(r)=f'(r)=0`;
- how tangency relates to a unique distinct real root;
- why a global-shape check may still be necessary.

### “Symmetric sums are taught” is not enough

The learner must know when to choose `s,p`, `s,q,r`, or `p=xyz`, and how to compare branches and admissibility.

### “Functional equations are taught” is not enough

A chapter containing only “try 0 and 1” is insufficient. Polynomial functional identities need nested-value naming and self-consistency.

### “Integer filters are obvious” is not enough

Teach how positivity, integrality, divisibility, ordering, bounded coefficients, and square constraints turn continuous algebra into finite casework.

---

## 5. Algebra visual-pedagogy profile

Algebra should not be made artificially pictorial. Add visuals only when they reveal structure better than symbols.

### Strong-use cases

#### Root geometry

Use small graphs for:

- two distinct real roots;
- a double/tangent root;
- no real roots;
- a quartic touching the axis at a unique distinct real zero.

These reinforce `ALG-QUAD-01`, `ALG-QUAD-02`, and `ALG-POLY-04`.

#### Domain / sign structure

Use number lines for:

- rational inequalities;
- excluded denominator values;
- radical domains;
- sign changes between roots.

#### Function composition

Use a small mapping diagram for `ALG-POLY-05` to show that roots of `P(Q(x))` are preimages under `Q` of roots of `P`.

#### Sequence evolution

Use compact tables or arrow diagrams for:

- finite differences;
- shift identities;
- periodicity;
- alternating AP/GP recurrences.

#### Smoothing / optimization

Use a one-variable or feasible-interval schematic when it makes the boundary/interior choice easier to see.

### Avoid low-value visuals

Do not add decorative grids, stock math imagery, or generic parabola sketches that do not teach the method.

### Figure integrity

Every Algebra figure should:

- use the same variables as nearby text;
- be mathematically correct;
- have labels readable at final PDF size;
- state `not to scale` where relevant;
- survive 200-dpi visual inspection.

---

## 6. Appendix A local hint architecture

For Algebra, the default student-facing layout is compact question-local hints, not a separate Hint Bank.

Preferred form:

```text
Qn. [problem statement]     [small useful figure/graph if applicable]

H1 👀 Notice   [recognition clue]
H2 ↩ Recall   [stable skill ID + readable skill name]
H3 ✏ Start    [first executable mathematical move]
```

Keep the problem-set feel. Normally aim for 2–3 questions per page where legibility permits.

### Hint depth

Use:

- `NONE` or `H1` for routine/easy transfer;
- `H1-H2` for medium problems;
- `H1-H3` for hard problems with a genuine execution bottleneck.

### Hint length

- H1: one sentence;
- H2: one sentence;
- H3: at most two short sentences/equations.

If a hint needs a paragraph, it belongs in the teaching section or an Advanced Worked Bridge.

### H1 — Notice

Recognition only.

Example:

> **H1 👀 Notice** Both `x+y` and `xy` appear; this is a symmetric two-variable structure.

### H2 — Recall previous learning

H2 should normally contain a stable ID and readable skill name.

Example:

> **H2 ↩ Recall `ALG-SYM2-01 · Sum-product substitution`** Use the same compression idea as in the earlier worked example.

This is especially important on tough problems because it trains retrieval rather than dependence on explicit hints.

### H3 — Start

Give the first executable mathematical move but not the final result.

Example:

> **H3 ✏ Start** Set `s=x+y`, `p=xy`; rewrite both conditions in `s,p`.

### Static-PDF learner instruction

At the beginning of Appendix A include:

> Try the problem first. Read H1 only if you cannot identify the structure. Read H2 only if you cannot retrieve the earlier skill. Use H3 only if you still cannot write the first mathematical move.

Because a PDF cannot truly hide later hints, make H1 visually strongest, H2 quieter, H3 quietest.

### Fallback Hint Bank

Use a separate Hint Bank only when local hints overcrowd a page, interfere with a large figure, or reveal too much by proximity.

---

## 7. Suggested hint depth for the 50-question Algebra corpus

This is a support profile, not source-order authority.

### Usually H1 only

- Q8
- Q12
- Q18
- Q20
- Q24
- Q29
- Q34
- Q37
- Q49

### Usually H1-H2

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

### Usually H1-H3

- Q2 — cyclic reciprocal product collapse
- Q3 — exponent substitution + transformed-root product
- Q10 — common-value cyclic multiplication
- Q14 — symmetric cubic factor + opposite pair
- Q15 — factor theorem + unique integer-root case split
- Q23 — two distinct GPs sharing second term
- Q26 — changed constant term + power sums
- Q27 — cyclic orientation / Vandermonde factorization
- Q28 — symmetric poles + midpoint shift + `t^2`
- Q31 — algebraic irrational linear independence
- Q32 — nested polynomial functional identity
- Q33 — nonlinear system collapsed to `p=xyz`
- Q36 — Vieta with repeated multiplicities
- Q38 — rational GP integrality under score bounds
- Q40 — smoothing and global boundary check
- Q41 — linked coefficients -> integer-root enumeration
- Q42 — tangent root plus global quartic shape
- Q43 — engineered subtraction yielding a common factor
- Q44 — quadratic preimage pairing in composition
- Q46 — strategic `P(-1)` and necessity/sufficiency
- Q47 — AP × GP parameterization
- Q48 — bounded stars-and-bars / inclusion-exclusion
- Q50 — symbolic alternating AP/GP pattern and proof

Adjust only if actual learner/teacher evidence becomes available.

---

## 8. Example H1-H3 ladders

### Cyclic reciprocal system

> **H1 👀 Notice** The three cyclic expressions simplify together under `xyz=1`.

> **H2 ↩ Recall `ALG-CYC-01 · Common-value cyclic systems`** Try combining the expressions before solving for individual variables.

> **H3 ✏ Start** Name the requested cyclic quantity `t` and multiply the three given sums; simplify using `xyz=1`.

### Exponential roots

> **H1 👀 Notice** All exponents are built from one common multiple.

> **H2 ↩ Recall `ALG-EXP-01 · Common exponent substitution`** Convert the exponential equation into a polynomial in one positive variable.

> **H3 ✏ Start** Set `u=2^(kx)` for the useful common `k`; later use the product of the `u`-roots to recover the sum of the original `x`-roots via `ALG-EXP-02`.

### Quadratic composition

> **H1 👀 Notice** The four roots of `P(Q(x))` must map under `Q` to only two roots of `P`.

> **H2 ↩ Recall `ALG-POLY-05 · Quadratic preimage symmetry`** Equal outputs of a quadratic occur at inputs symmetric about its axis.

> **H3 ✏ Start** Pair the four given inputs into two pairs having the same sum; that determines the linear coefficient of `Q`.

### Strategic polynomial evaluation

> **H1 👀 Notice** The coefficient pattern is designed to simplify at a small integer.

> **H2 ↩ Recall `ALG-POLY-02 · Strategic evaluation`** First determine the signs of the integer roots.

> **H3 ✏ Start** Interpret `P(-1)` both from the root factorization and from the coefficients; compare the two signs.

### Bounded digit sum

> **H1 👀 Notice** Treat every number below `10000` as a four-digit string with leading zeros.

> **H2 ↩ Recall `ALG-DISC-01 · Bounded digit sums`** The possible positive multiples of `11` are limited by the maximum four-digit digit sum.

> **H3 ✏ Start** Count digit quadruples for each allowed sum using stars-and-bars plus inclusion-exclusion; for a sum near `36`, use the complement `d -> 9-d`.

---

## 9. High-value Advanced Worked Bridge obligations

When required by the supplied corpus, provide non-identical bridges for methods such as:

- cyclic reciprocal product collapse;
- changing-average linear systems;
- polygon AP with parity/integrality/convexity;
- simultaneous discriminant inequalities;
- common-value cyclic multiplication;
- factor-theorem uniqueness counting;
- order-statistic mass bounds with equality construction;
- squared-term GP comparison;
- two distinct GPs sharing a second term;
- changed polynomial constant term and power sums;
- cyclic Vandermonde factorization;
- midpoint shifts in rational equations;
- algebraic-number linear independence;
- nested polynomial functional identities;
- repeated-root multiplicity counting;
- rational GP denominator divisibility;
- smoothing and boundary optimization;
- linked-coefficient integer-root enumeration;
- quartic tangency with global-shape verification;
- quadratic preimage pairing;
- strategic polynomial evaluation;
- AP × GP parameterization;
- bounded stars-and-bars;
- alternating AP/GP symbolic pattern proof.

These are not universal requirements; they become obligations when the corpus requires them.

---

## 10. Algebra legality checklist

### Rational expressions

- denominators nonzero;
- no pole introduced by clearing denominators;
- excluded values not counted later.

### Radicals

- real-domain condition where applicable;
- squaring may introduce candidates;
- final substitution check.

### Logarithms

- positive argument;
- positive base not equal to 1;
- equivalence preserved.

### Inequalities

- positivity before AM-GM;
- sign before multiplying/dividing;
- equality condition;
- boundary cases.

### Vieta / roots

- monic versus non-monic coefficients;
- multiplicity counting;
- real versus complex assumptions;
- integer-root consequences only when justified.

### Infinite GP

- `|r|<1`;
- transformed series still converges.

### Optimization

- prove the bound;
- prove attainability;
- check boundary and interior candidates.

### Functional identities

- distinguish an identity from an equation at isolated inputs;
- compare coefficients only after identity status is established.

---

## 11. Appendix B Algebra audit set

Appendix B should contain approximately 20 reliable-source or clearly labeled author-created questions sampling the revised guide.

A useful spread is approximately:

- 2 identities/factorization
- 2 symmetric systems
- 2 quadratics/root conditions
- 3 polynomial/Vieta/power-sum
- 2 inequalities/extrema
- 3 AP/GP/sequence/recurrence
- 2 exponent/radical/algebraic-number
- 1 functional identity
- 1 complex-number bridge
- 2 integer/discrete-filter

Use the same local adaptive hint system only on the harder questions.

Independently recompute every answer.

---

## 12. Appendix C Algebra memory helper

Keep Appendix C to approximately 1–2 pages.

High-value items include:

- structural identities and manufactured factor patterns;
- `s,p` and `s,q,r` identities;
- discriminant/root facts;
- Vieta;
- factor/remainder theorem;
- repeated-root condition;
- AP/GP formulas;
- finite-difference reminder;
- index laws;
- radical/log legality;
- AM-GM equality condition;
- binomial identities if genuinely taught;
- `P'(t)/P(t)` if genuinely taught;
- candidate-check checklist;
- stable skill IDs for deeper review.

Do not put full worked solutions in Appendix C.

---

## 13. Algebra acceptance gate

For a corpus of `n` questions require:

```text
ALGEBRA_QUESTION_INVENTORY = PASS_n_OF_n
ALGEBRA_QUESTION_TO_METHOD_MATRIX = PASS_n_OF_n
ALGEBRA_ORPHAN_METHOD_AUDIT = PASS_n_OF_n
ALGEBRA_VISUAL_PEDAGOGY_AUDIT = PASS_n_OF_n
ALGEBRA_APPENDIX_A_CUSTODY = PASS_n_OF_n
ALGEBRA_APPENDIX_A_HINT_AUDIT = PASS_n_OF_n
ALGEBRA_STATIC_CONTENT_SELF_SUFFICIENCY = PASS_n_OF_n
```

For the motivating 50-question corpus:

```text
ALGEBRA_STATIC_CONTENT_SELF_SUFFICIENCY = PASS_50_OF_50
```

This does not imply classroom solve rate, timing, retention, psychometrics, or qualification probability.

---

## 14. Algebra PDF acceptance

Do not generate the final PDF while any question is `PARTIAL` or `FAIL`.

After content qualification:

- integrate the study guide, worked bridges, Appendix A, local hints, Appendix B, Appendix C, and student-appropriate source notes;
- render every page at 200 dpi;
- visually inspect every page;
- inspect all graphs and diagrams at final size;
- verify H1/H2/H3 strips are compact, readable, and subordinate to the question;
- ensure the answer key does not visually leak into unsolved questions;
- record exact page count and SHA-256.

---

## 15. Final Algebra principle

A strong Algebra guide should train the learner to ask:

1. What structure repeats?
2. Which variables can be compressed?
3. Which operations are reversible?
4. What is the smallest useful representation?
5. Which branch/domain/equality condition survives?
6. Can I prove the extremum or integer restriction is attainable?
7. Which previously learned Algebra skill ID does this resemble?

The main guide, visuals, worked bridges, and compact H1-H3 strips should all reinforce that behavior.
