# Algebra Question-Driven Study Guide Profile v2

## Role

This is the Algebra-specific profile for the generalized question-driven study-guide skill.

Use it with:

- `../SKILL.md`
- `question-driven-self-sufficient-study-guide-skill-v2.md`

The generalized contract owns production mechanics. This profile owns Algebra-specific method families, recognition cues, legality checks, visual use, likely orphan methods, Appendix A hint behavior, book navigation, and the optional simple three-day Algebra Navigator.

It incorporates the lessons from the 50-question Algebra rebuild where a polished first PDF failed a benchmark/self-sufficiency audit.

The durable core remains a reference book. Short-horizon behavior belongs in a **simple 4-page Part 0**, which routes into the core without replacing it.

> **Navigator = where to go. Core = how to do it.**

---

## 1. Algebra learner objective

Teach a partially prepared Grade 9 learner to move from:

**surface wording -> structural compression -> legal transformation -> small-variable model -> execution -> branch/domain check.**

The strongest Algebra solutions often require a better representation rather than more computation.

Typical compression moves include:

- `s=x+y`, `p=xy` instead of solving for `x,y`;
- `s=x+y+z`, `q=xy+yz+zx`, `r=xyz` instead of raw expansion;
- `p=xyz` when the same product repeats through a nonlinear system;
- midpoint shift in symmetric rational equations;
- Vieta/power sums instead of explicit roots;
- recurrence state/shift instead of listing many terms;
- strategic evaluation such as `P(-1)` instead of brute-force discriminants.

The guide must teach why and when those representation choices close the problem.

---

## 2. Stable Algebra skill families

Use stable IDs for durable cross-reference and audit. Student-facing navigation should use readable names first and IDs second.

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

## 3. Kid-facing aliases

Student-facing navigation should pair a readable name with a stable ID in secondary type.

| Stable ID | Readable name |
|---|---|
| `ALG-SYM2-01` | **Sum–Product Trick** |
| `ALG-SYM3-01` | **Three-Variable Symmetry** |
| `ALG-CYC-02` | **Common Product Trick** |
| `ALG-CYC-01` | **Common-Value Method** |
| `ALG-QUAD-01` | **Quadratic Root Test** |
| `ALG-POLY-04` | **Repeated / Touching Root Method** |
| `ALG-POLY-01` | **Polynomial Difference Trick** |
| `ALG-POLY-03` | **Vieta / Root-Sum Method** |
| `ALG-ROOTSUM-03` | **Reciprocal Root Tool** |
| `ALG-MIXSEQ-01` | **Mixed Progressions** |
| `ALG-REC-01` | **Recurrence Shortcut** |
| `ALG-INEQ-02` | **Fixed-Sum Extremum / Smoothing** |
| `ALG-EQ-04` | **Midpoint Shift for Symmetric Poles** |
| `ALG-GP-02` | **Integer GP Denominator Test** |

Stable IDs are for durable reference. Readable names are for retrieval under pressure.

---

## 4. Recommended book architecture

Use the following overall architecture when producing the complete Algebra book:

```text
Cover
Contents and Study Route
Part 0 — Simple 3-Day Algebra Navigator (4 pages, when requested)
One-page Algebra Operating Rule

CORE REFERENCE BOOK
  chapters in prerequisite order
  interleaved Visual Bridges

Advanced Worked Bridges

Appendix A — Guided Q1–Q50
Appendix A Answer Key
Appendix B — Mixed Transfer
Appendix C — Decision-First Visual Quick Reference
Sources and Provenance
```

The cover/index/Visual Bridge/quick-reference philosophy may use a strong completed guide as a quality benchmark, but do not copy its wording or diagrams.

---

## 5. Cover and Contents/Study Route profile

### Cover

Recommended hierarchy:

```text
IOQM GRADE 9
ALGEBRA
Complete Study Guide

3-Day Navigator + durable reference + guided Q1–Q50 + mixed transfer + visual quick reference

SYMMETRY · POLYNOMIALS · ROOTS · SEQUENCES

Built for a learner who:
- knows roughly 30–50% but misses the hidden method;
- needs to recognize structure, choose a legal first move, execute, then check;
- has only a few days and cannot read a textbook front-to-back.

LEARN -> VISUALIZE -> PRACTISE -> RETRIEVE
```

Keep production/audit metadata off the cover.

### Contents and Study Route

Use **Contents and Study Route**, not a bare index.

Show one-line purpose + page number for:

- START HERE / Simple 3-Day Navigator;
- Core Reference Book;
- each Algebra Visual Bridge;
- Advanced Worked Bridges;
- Appendix A Guided Q1–Q50;
- Appendix A Answer Key;
- Appendix B Mixed Transfer;
- Appendix C Decision-First Visual Quick Reference;
- Sources and Provenance.

The learner should understand where to go before reading Chapter 1.

---

## 6. One-page Algebra Operating Rule

Before the core, include one calm operating-rule page with four questions:

1. **What structure repeats?**
2. **Can I compress the variables?**
3. **Is my first operation legal/reversible?**
4. **What is my first useful line?**

Optional small footer:

```text
If stuck:
Notice -> Recall -> Start -> worked example -> final legality check
```

Do not expose RMSEC codes or internal routing labels here.

---

## 7. Recommended chapter order

A strong default order for a 30–50% prepared learner is:

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
19. Appendix A
20. Appendix B
21. Appendix C

Regroup if the actual supplied corpus demands a different prerequisite order.

---

## 8. Algebra-specific orphan-method traps

### “Vieta is taught” is not enough

The learner must also be able to rebuild a target from symmetric sums, handle higher power sums, count multiplicities, combine roots with integer restrictions, and keep complex branches when allowed.

### “AP/GP is taught” is not enough

The learner must also be able to parameterize overlapping AP/GP structures, justify rational GP denominator divisibility, identify constant second difference from AP products, compare transformed GPs, and prove alternating AP/GP recurrence patterns.

### “Repeated roots are taught” is not enough

Explain why repeated roots satisfy `f(r)=f'(r)=0`, how tangency relates to root multiplicity, and why a global shape check may still be necessary.

### “Symmetric sums are taught” is not enough

The learner must know when to choose `s,p`, `s,q,r`, or `p=xyz`, and how to compare branches/admissibility.

### “Functional equations are taught” is not enough

A chapter containing only “try 0 and 1” is insufficient. Polynomial functional identities need nested-value naming and self-consistency.

### “Integer filters are obvious” is not enough

Teach how positivity, integrality, divisibility, ordering, bounded coefficients, and square constraints turn continuous algebra into finite casework.

---

## 9. Algebra visual-pedagogy profile

Algebra should not be made artificially pictorial. Add visuals only when they reveal structure better than symbols.

### Visual Bridge 1 — Roots and Tangency

Use small graphs to distinguish:

- two distinct real roots;
- double/tangent root;
- no real roots;
- quartic touching at a unique distinct real zero.

Reinforces `ALG-QUAD-01`, `ALG-QUAD-02`, `ALG-POLY-04`.

### Visual Bridge 2 — Symmetry and Compression

Show compact before/after representations:

- `x,y -> s=x+y, p=xy`;
- `x,y,z -> s,q,r`;
- repeated `xyz -> p`;
- symmetric poles -> midpoint shift.

The visual goal is representation choice, not decoration.

### Visual Bridge 3 — Polynomial Structure

Useful panels:

- `P(m)=P(k) -> P(m)-P(k)`;
- Vieta without explicit roots;
- repeated root `f=f'=0`;
- composition/preimage mapping for `P(Q(x))`.

### Visual Bridge 4 — Sequences and Recurrences

Use compact tables/arrows for:

- AP/GP overlap;
- finite differences;
- shift identities;
- periodicity;
- alternating AP/GP recurrence.

### Visual Bridge 5 — Extremes and Domains, if space permits

Use number lines/branch schematics for:

- denominator exclusions;
- symmetric poles;
- fixed-sum smoothing;
- boundary vs interior extrema.

### High-value question-level visuals for the 50-question corpus

Where useful:

- Q17: positive/negative mass bar;
- Q20: finite-difference table;
- Q24: recurrence shift arrow;
- Q28: symmetric-pole midpoint number line;
- Q36: repeated-root multiplicity grouping;
- Q40: smoothing branch schematic;
- Q42: quartic tangency/global minimum graph;
- Q44: quadratic preimage mapping;
- Q50: alternating AP/GP flow.

Do not add decorative grids or generic stock math imagery.

Every figure must use nearby notation, be mathematically correct, be readable at final size, and survive 200-dpi inspection.

---

## 10. Appendix A local hint architecture

For Algebra, default to compact local hints.

Preferred form:

```text
Qn. [problem statement]     [small useful figure if applicable]

H1 👀 Notice   [recognition clue]
H2 ↩ Recall   [readable skill name + stable ID]
H3 ✏ Start    [first executable mathematical move]
```

Keep the problem-set feel. Aim for 2–3 questions/page where legibility permits.

### Hint depth

- routine/easy: `NONE` or `H1`;
- medium: `H1-H2`;
- hard: `H1-H3`.

### Hint length

- H1: one sentence;
- H2: one sentence;
- H3: at most two short sentences/equations.

If a hint needs a paragraph, move the material into the teaching section or a Worked Bridge.

### H1 — Notice

Recognition only.

> **H1 👀 Notice** Both `x+y` and `xy` appear; this is a symmetric two-variable structure.

### H2 — Recall

Retrieve previous learning.

> **H2 ↩ Recall Sum–Product Trick · `ALG-SYM2-01`** Use the same compression idea as in the earlier worked example.

### H3 — Start

Give the first executable move, not the answer.

> **H3 ✏ Start** Set `s=x+y`, `p=xy`; rewrite both conditions in `s,p`.

### Static-PDF learner instruction

> Try the problem first. Read H1 only if you cannot identify the structure. Read H2 only if you cannot retrieve the earlier skill. Use H3 only if you still cannot write the first mathematical move.

Use H1 strongest, H2 quieter, H3 quietest.

---

## 11. Suggested hint depth for the 50-question Algebra corpus

This is a support profile, not source-order authority.

### Usually H1 only — 9

- Q8
- Q12
- Q18
- Q20
- Q24
- Q29
- Q34
- Q37
- Q49

### Usually H1-H2 — 18

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

### Usually H1-H3 — 23

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

## 12. Example H1-H3 ladders

### Cyclic reciprocal system

> **H1 👀 Notice** The three cyclic expressions simplify together under `xyz=1`.

> **H2 ↩ Recall Common-Value Method · `ALG-CYC-01`** Try combining the expressions before solving individual variables.

> **H3 ✏ Start** Name the requested cyclic quantity `t` and multiply the three given sums; simplify using `xyz=1`.

### Exponential roots

> **H1 👀 Notice** All exponents are built from one common multiple.

> **H2 ↩ Recall Common Exponent Substitution · `ALG-EXP-01`** Convert the exponential equation into a polynomial in one positive variable.

> **H3 ✏ Start** Set `u=2^(kx)` for a useful common `k`; later translate the product of `u`-roots back to the original exponent sum via `ALG-EXP-02`.

### Quadratic composition

> **H1 👀 Notice** The four roots of `P(Q(x))` map under `Q` to only two roots of `P`.

> **H2 ↩ Recall Quadratic Preimage Symmetry · `ALG-POLY-05`** Equal outputs of a quadratic occur at inputs symmetric about its axis.

> **H3 ✏ Start** Pair the four inputs into two pairs having the same sum; that determines the linear coefficient of `Q`.

### Strategic polynomial evaluation

> **H1 👀 Notice** The coefficient pattern is designed to simplify at a small integer.

> **H2 ↩ Recall Strategic Evaluation · `ALG-POLY-02`** First determine the signs of the integer roots.

> **H3 ✏ Start** Interpret `P(-1)` from both the root factorization and the coefficients; compare signs.

### Bounded digit sum

> **H1 👀 Notice** Treat every number below `10000` as a four-digit string with leading zeros.

> **H2 ↩ Recall Bounded Digit Sums · `ALG-DISC-01`** The possible positive multiples of `11` are limited by the maximum four-digit digit sum.

> **H3 ✏ Start** Count digit quadruples for each allowed sum using stars-and-bars plus inclusion-exclusion; near `36`, use `d -> 9-d`.

---

## 13. High-value Advanced Worked Bridge obligations

When required by the supplied corpus, provide non-identical, imitation-level bridges for methods such as:

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

A bridge must contain enough intermediate algebra that H2 can point to it and a half-prepared learner can imitate the mechanism on a nearby problem.

---

## 14. Algebra legality checklist

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

## 15. Appendix B Algebra transfer set

Appendix B should contain approximately 20 reliable-source or clearly labeled author-created questions sampling the revised guide.

A useful spread is approximately:

- 2 identities/factorization;
- 2 symmetric systems;
- 2 quadratics/root conditions;
- 3 polynomial/Vieta/power-sum;
- 2 inequalities/extrema;
- 3 AP/GP/sequence/recurrence;
- 2 exponent/radical/algebraic-number;
- 1 functional identity;
- 1 complex-number bridge;
- 2 integer/discrete-filter.

Use lighter scaffolding than Appendix A so Appendix B functions as mixed transfer.

Independently recompute every answer.

---

## 16. Appendix C — Decision-First Algebra Quick Reference

Keep Appendix C compact, usually 2 pages.

### C1 — What do I see? -> What should I write first?

Examples:

| What do I see? | First thought / first line |
|---|---|
| `x+y`, `xy`, `x^2+y^2` | `s=x+y`, `p=xy` |
| symmetric `x,y,z` | `s,q,r` |
| repeated `xyz` | `p=xyz` |
| several expressions equal | name common value `k` |
| quadratic root condition | write discriminant/root-sign condition |
| repeated root | `f(r)=f'(r)=0` |
| `P(m)=P(k)` | factor `P(m)-P(k)` |
| many roots + symmetric target | Vieta / power sums; do not solve roots |
| reciprocal root sum | consider `P'/P` |
| huge recurrence index | search for shift/period |
| fixed-sum max/min | smoothing + equality/attainability |
| symmetric poles | shift to midpoint |

### C2 — Tools after method choice

Include compact formulas and checks:

- structural identities;
- `s,p` and `s,q,r` identities;
- discriminant facts;
- Vieta;
- factor/remainder theorem;
- repeated-root condition;
- AP/GP formulas;
- finite-difference reminder;
- exponent laws;
- radical/log legality;
- AM-GM equality condition;
- `P'(t)/P(t)` if genuinely taught;
- final candidate/domain/branch checklist.

Do not place full worked solutions in Appendix C.

---

## 17. Part 0 — Simple 3-Day Algebra Navigator

### 17.1 Role

Part 0 is an optional front-end for a student who has only a few days before the exam.

It appears after Contents and Study Route and before the core.

The student-facing Navigator is **4 pages maximum**.

The sophisticated diagnostic machinery remains author/teacher-side. The child sees only a simple route.

> **Complexity belongs in the engine, not in the learner interface.**

### 17.2 Page 1 — Start Here

Use one calm message:

> **You do not need to read this book from beginning to end in three days.**

Then:

```text
QUICK CHECK -> FIND WEAK TOPICS -> FIX IMPORTANT GAPS -> PRACTISE -> MIXED TEST
```

Simple three-day table:

| Day | Main job |
|---|---|
| Day 1 | Recognize the main Algebra patterns |
| Day 2 | Practise the important weak areas |
| Day 3 | Mixed questions + quick revision |

No internal metrics, formulas, RMSEC codes, or traffic-light subtypes on this page.

### 17.3 Page 2 — Quick Check: T1–T10

Diagnostic labels must use `T1`–`T10`, never `Q1`–`Q10`, because `Q1`–`Q50` are reserved for the real Algebra corpus.

Print this instruction exactly or equivalently:

> **Quick Check — What would you try first?**  
> Spend about 1–2 minutes on each. Do not fully solve. Mark: `[OK] knew the move` `[?] unsure` `[X] no idea`.

Use these ten recognition prompts:

#### T1

You know `x+y` and `xy`, and need `x^2+y^2`. What would you name first?

`[ ] OK   [ ] ?   [ ] X`

#### T2

The same product `xyz` appears in three nonlinear equations. What single variable would you set?

`[ ] OK   [ ] ?   [ ] X`

#### T3

A quadratic must not have two distinct real roots. What condition do you write first?

`[ ] OK   [ ] ?   [ ] X`

#### T4

A cubic has exactly two distinct real roots. What must the repeated root satisfy?

`[ ] OK   [ ] ?   [ ] X`

#### T5

`P(m)=P(3)` for an integer-coefficient cubic. What expression should you factor?

`[ ] OK   [ ] ?   [ ] X`

#### T6

The first three terms are in AP and the last three in GP. How would you represent the AP terms?

`[ ] OK   [ ] ?   [ ] X`

#### T7

A recurrence asks for a huge index. What should you search for before calculating many terms?

`[ ] OK   [ ] ?   [ ] X`

#### T8

An equation contains powers with a common exponential base. What substitution makes it polynomial?

`[ ] OK   [ ] ?   [ ] X`

#### T9

`x+y+z` is fixed and the target is a maximum/minimum. What structural idea should you test?

`[ ] OK   [ ] ?   [ ] X`

#### T10

A rational equation has poles in symmetric pairs around one midpoint. What shift should you try?

`[ ] OK   [ ] ?   [ ] X`

**No H1 or method router appears before the learner marks T1–T10.**

The purpose is unaided recognition. H1 may be used after marking for learning.

### 17.4 Page 3 — What should I study?

Map T1–T10 to readable skills and core locations.

| Quick Check | Topic to review | Stable reference |
|---|---|---|
| T1 | **Sum–Product Trick** | `ALG-SYM2-01` |
| T2 | **Common Product Trick** | `ALG-CYC-02` |
| T3 | **Quadratic Root Test** | `ALG-QUAD-01` |
| T4 | **Repeated / Touching Root Method** | `ALG-POLY-04` |
| T5 | **Polynomial Difference Trick** | `ALG-POLY-01` |
| T6 | **Mixed Progressions** | `ALG-MIXSEQ-01` + `ALG-AP-01` |
| T7 | **Recurrence Shortcut** | `ALG-REC-01` |
| T8 | **Common Exponent Substitution** | `ALG-EXP-01` |
| T9 | **Fixed-Sum Extremum / Smoothing** | `ALG-INEQ-02` |
| T10 | **Midpoint Shift for Symmetric Poles** | `ALG-EQ-04` |

Use only three student-facing priorities:

- **DO FIRST** — `[X]` on an important core family;
- **DO NEXT** — `[?]` or slow/uncertain;
- **ONLY IF TIME** — narrow advanced material or already-secure topics.

Readable skill names dominate. Stable IDs remain secondary.

A small post-check method router may appear here, after T1–T10 have been scored.

### 17.5 Page 4 — When you get stuck

Use plain language:

```text
I don't know what method applies
-> Read H1 · Notice

I know the topic but forgot the method
-> Read H2 · Recall

I know the method but cannot begin
-> Read H3 · Start

I started correctly but got stuck halfway
-> Open the linked Worked Bridge / worked example

I reached an answer but it is wrong
-> Check domain, denominator, branch, equality, convergence, integer restriction, and the exact requested target
```

Then:

> **Try a nearby problem with less help. Do not immediately redo only the same numbers and call it mastery.**

Add the simple 3-day reminder:

- **Day 1 — Recognize:** Quick Check, repair weak high-value topics, solve representative guided questions.
- **Day 2 — Practise:** harder core questions, worked bridges for places where execution breaks down, use fewer hints.
- **Day 3 — Mix:** unlabeled mixed questions, hints closed first, quick reference + personal error list only.

Night-before rule:

> Do not begin a major new advanced topic. Review triggers and legality checks, stop at a sensible time, and protect normal sleep.

### 17.6 Internal Algebra routing — not normally printed

The author/teacher layer may still retain:

- unaided vs after-H1 recognition;
- recognition weakness vs execution weakness;
- internal `R/M/S/E/C` repair labels;
- global `MUST/SHOULD/IF_TIME` curriculum value;
- workload caps;
- hint dependency;
- non-identical transfer success;
- suggested readiness thresholds.

These are routing aids, not a validated psychometric system and not appropriate for the simple child-facing Navigator.

### 17.7 Global priority and source stability

The internal priority rubric may consider transfer, distinct-mechanism frequency/canonical relevance, dependency, and repair value.

Do not equate difficulty with importance.

Important corpus-specific rules:

- Q29 has unresolved recovered wording; keep it in the durable corpus for custody but set `72_HOUR_CORE = NO` / `ONLY_IF_TIME`;
- Q37/Q49 are duplicates; deduplicate them for priority-frequency calculations and do not require both in the core short-horizon route;
- duplicates may still be used deliberately for spaced retrieval, but only if labeled as such internally.

### 17.8 Workload and spacing defaults

Useful internal defaults:

```text
MAX_ACTIVE_WEAK_CORE_FAMILIES_PER_DAY = 4
MAX_NEW_CORE_SKILLS_DAY3 = 0
GLOBAL_CORE_PRACTICE_ROUTE <= ~24 ITEMS
```

These are workload guardrails, not empirically validated IOQM constants.

Space important skills across the three days.

Example:

```text
Day 1: learn/review Sum–Product + one guided problem
Day 2: different Sum–Product problem with less help
Day 3: mixed unlabeled problem requiring Sum–Product recognition
```

### 17.9 Simple Algebra Navigator acceptance

When the 3-day mode is requested, require:

```text
ALGEBRA_SIMPLE_NAVIGATOR = PASS
ALGEBRA_NAVIGATOR_PAGES <= 4
ALGEBRA_QUICK_CHECK_ITEMS = 10
ALGEBRA_QUICK_CHECK_LABELS = T1_TO_T10
ALGEBRA_QUICK_CHECK_Q_LABEL_COLLISION = 0
ALGEBRA_QUICK_CHECK_UNAIDED_BEFORE_HINT = PASS
ALGEBRA_READABLE_SKILL_ROUTE = PASS
ALGEBRA_DO_FIRST_NEXT_IF_TIME = PASS
ALGEBRA_PLAIN_LANGUAGE_STUCK_REPAIR = PASS
ALGEBRA_INTERNAL_JARGON_EXPOSED = 0
ALGEBRA_NAVIGATOR_THEORY_DUPLICATION = 0
ALGEBRA_Q29_72H_CORE = NO
ALGEBRA_Q37_Q49_DEDUP_FOR_PRIORITY = PASS
ALGEBRA_DAY3_NEW_MAJOR_CORE_SKILLS = 0
```

---

## 18. Algebra acceptance gate

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

For the motivating corpus:

```text
ALGEBRA_STATIC_CONTENT_SELF_SUFFICIENCY = PASS_50_OF_50
```

This does not imply classroom solve rate, timing, retention, psychometrics, or qualification probability.

---

## 19. Algebra PDF acceptance

Do not generate the final PDF while any required question is `PARTIAL` or `FAIL`.

After content qualification:

- integrate cover, Contents and Study Route, simple Navigator if requested, one-page operating rule, core chapters, Visual Bridges, Advanced Worked Bridges, Appendix A, Appendix B, Appendix C, and source notes;
- keep T1–T10 unique to Quick Check and Q1–Q50 unique to the actual corpus;
- render every page at 200 dpi;
- visually inspect every page;
- inspect all graphs/diagrams at final size;
- inspect cover hierarchy, Contents/Study Route, Visual Bridge panels, and decision-first Appendix C;
- verify H1/H2/H3 strips are compact, readable, and subordinate to the question;
- ensure answer keys do not visually leak into unsolved questions;
- record exact page count and SHA-256.

---

## 20. Final Algebra principle

A strong Algebra guide should train the learner to ask:

1. What structure repeats?
2. Which variables can be compressed?
3. Which operations are reversible?
4. What is the smallest useful representation?
5. Which branch/domain/equality condition survives?
6. Can I prove the extremum or integer restriction is attainable?
7. Which previously learned readable skill does this resemble?

The core, Visual Bridges, Worked Bridges, local H1-H3 strips, and simple Navigator should all reinforce that behavior.

For a three-day learner:

> **Quick Check -> fix the important weak topics -> practise -> mixed retrieval. Do not try to read the whole reference book in order.**