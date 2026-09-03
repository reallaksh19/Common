# IOQM Grade 9 — Knowledge Dependency Map v1

Status: `V1_FROZEN_FOR_PRODUCTION_WAVES`

Purpose: prevent prerequisite inversion and make the learner journey explicit before topic prose exists.

Coverage-hardening overlays are recorded in `IOQM_G9_Coverage_Hardening_Overlay_v1.md`; cross-topic proof modes are defined in `IOQM_G9_Proof_Strategy_Toolkit_v1.md`.

## 1. Dependency semantics

Use these edge labels:

- `REQUIRES` — downstream teaching assumes ownership of upstream concept;
- `BRIDGE_REQUIRES` — only a small just-in-time bridge is needed;
- `APPLICATION_OF` — downstream may use but must not reteach canonically;
- `PARALLEL_READY` — topics can be built independently after common prerequisites;
- `TRANSFER_LINK` — no teaching dependency; useful cross-domain transfer only.

## 2. Program prerequisite spine

### F0 — Arithmetic/algebra fluency

`G9_CORE`

- integer arithmetic;
- fractions/rational expressions;
- ratio/proportion;
- exponent basics;
- linear equations;
- expansion/factorisation;
- coordinate basics;
- elementary Euclidean geometry.

### F1 — Mathematical language and proof habits

`IOQM_BRIDGE`

- implication vs equivalence;
- counterexample;
- parity/divisibility language;
- variable/domain restrictions;
- finite case completeness;
- exact vs approximate reasoning;
- proof/check discipline;
- direct proof, contradiction, contrapositive where useful, construction/obstruction, extremal choice, invariant/monovariant and equality-condition closure through `IOQM_G9_Proof_Strategy_Toolkit_v1.md`.

All four domains `REQUIRE F0` and `BRIDGE_REQUIRE F1`.

## 3. Number Theory dependency graph

```text
F0/F1
  |
  +--> NT-01 Divisibility/GCD/LCM
  |       |    exports Euclid's Lemma
  |       |
  |       +--> NT-02 Modular Arithmetic/Cycles/Euler bridge
  |       |       |
  |       |       +--> NT-05 Digit/Base Structure
  |       |
  |       +--> NT-03 Prime Factorisation/Divisors/Perfect Powers
  |               |    retrieves Euclid's Lemma
  |               |
  |               +--> NT-04 Diophantine/Integer Restrictions
  |
  +--> ALG-01 factorisation/substitution --BRIDGE_REQUIRES--> NT-04
```

Notes:
- NT-01 is the main structural prerequisite for NT-02 and NT-03.
- NT-01 canonically owns Euclid's Lemma: prime `p|ab` implies `p|a` or `p|b`; NT-03 retrieves it when prime divisibility must split across a product.
- NT-02 canonically owns the bounded Euler theorem bridge and optional prime-modulus Fermat companion, with explicit coprimality checks and a cycle-vs-theorem decision boundary.
- NT-04 depends jointly on factorisation/algebra and number-theoretic restrictions.
- NT-05 can begin early with place value, but advanced divisibility/cycle work follows NT-02.

## 4. Algebra dependency graph

```text
F0/F1
  |
  +--> ALG-01 Identities/Transformations/Equation Structure
  |       |
  |       +--> ALG-03 Polynomials/Roots/Vieta/Remainders
  |       |       |
  |       |       +--> transformed-root / polynomial-reduction ceiling work
  |       |
  |       +--> ALG-02 Inequalities/Bounds/Equality
  |       |       |
  |       |       +--> integer/discrete extremal bridges
  |       |
  |       +--> ALG-06 Exponents/Radicals/Logs
  |
  +--> ALG-04 Sequences/Recurrences
  |
  +--> ALG-07 Floor/Ceiling/Discrete Functions
  |
  +--> ALG-05 Functional Equations
          ^
          |
          BRIDGE_REQUIRES ALG-01 substitution/equivalence discipline
```

Important ownership rule:
- Vieta is canonically taught in ALG-03.
- Other topics may retrieve/use Vieta but must not create an independent canonical derivation.
- AM-GM/equality is canonically taught in ALG-02.
- Other topics may apply it but should link back rather than reteach from scratch.
- Generic proof modes are retrieved from the proof toolkit; specialized algebraic legality remains owned by the relevant algebra topic.

## 5. Geometry dependency graph

```text
F0 geometry + F1 proof habits
  |
  +--> GEO-02 Angles/Lines/Quadrilaterals/Polygons
  |       |
  |       +--> GEO-04 Circles/Cyclicity/Tangency
  |
  +--> GEO-03 Similarity/Ratio/Area/Centroid
  |       |
  |       +--> GEO-01 Triangle Metric/Special Cevians
  |
  +--> GEO-05 Coordinate/Vector/Mensuration
          |
          +--TRANSFER_LINK--> GEO-01/GEO-03/GEO-04 as alternate representation
```

Notes:
- GEO-01 and GEO-04 can be authored in parallel after their prerequisite interfaces are frozen.
- Coordinate/vector methods are alternate representations, not mandatory first methods for every geometry problem.
- exact figure custody belongs to source provenance, not mathematical dependency.
- contradiction, construction/obstruction and proof-hypothesis checks retrieve the shared proof toolkit rather than forming a separate geometry proof chapter.

## 6. Combinatorics dependency graph

```text
F0 arithmetic + F1 proof/model habits
  |
  +--> COMB-01 Basic Counting/Restrictions/IE
  |       |
  |       +--> COMB-02 Graphs/Colouring/Incidence
  |       |
  |       +--> COMB-03 Recurrence/Tilings/State
  |
  +--> COMB-05 Pigeonhole/Extremal
  |
  +--> COMB-04 Games/Invariants
          ^
          |
          BRIDGE_REQUIRES parity/residue ideas from NT-01/NT-02 for many applications
```

COMB-04 and COMB-05 do not require advanced permutation formulas; they require modelling and proof discipline. Their invariant/monovariant, contradiction, extremal and construction/obstruction proof modes retrieve the shared proof toolkit.

## 7. Cross-domain prerequisite edges

### Number Theory -> Combinatorics
- parity/residue invariants `APPLICATION_OF NT-02` in COMB-04;
- divisor/factor-state models `APPLICATION_OF NT-03` in counting problems.

### Algebra -> Number Theory
- factorisation/substitution `APPLICATION_OF ALG-01` in NT-04;
- discriminant/perfect-square feasibility `APPLICATION_OF ALG-03` where an integer quadratic is used.

### Algebra -> Geometry
- inequalities `APPLICATION_OF ALG-02` in geometric bounds;
- polynomial/Vieta data `APPLICATION_OF ALG-03` only when geometry encodes roots;
- coordinates `BRIDGE_REQUIRES G9_CORE algebra` in GEO-05.

### Geometry -> Algebra
No general prerequisite. Geometry may provide transfer surfaces for algebraic invariants.

### Combinatorics -> Algebra
- recurrence notation in COMB-03 may `BRIDGE_REQUIRE ALG-04` or be introduced locally at minimal depth.

## 8. Frozen production waves

Dependency does not mean every topic waits globally. The production schedule is frozen in `02_Production/IOQM_G9_Main_Topic_Production_Waves_v1.md`:

### Wave 1 — parallel canonical primitives
`NT-01`, `ALG-01`, `ALG-04`, `ALG-07`, `GEO-02`, `GEO-03`, `GEO-05`, `COMB-01`, `COMB-05`.

### Wave 2 — after prerequisite interfaces
`NT-02`, `NT-03`, `ALG-02`, `ALG-03`, `ALG-05`, `ALG-06`, `GEO-01`, `GEO-04`, `COMB-02`, `COMB-03`.

### Wave 3 — composite/cross-domain
`NT-04`, `NT-05`, `COMB-04`.

A downstream topic waits for a **stable prerequisite interface**, not necessarily the upstream final PDF.

## 9. Build-order states

### READY_PARALLEL
Topic prerequisites are frozen; production may proceed independently.

### WAIT_FOR_INTERFACE
The topic needs a stable prerequisite interface but not the final upstream PDF.

### WAIT_FOR_CANONICAL_TEACHING
The topic would otherwise teach a concept before its canonical owner. Do not author integrated prose yet.

## 10. Anti-failure rule

Forbidden sequence:

`Topic B assumes Vieta -> Topic A later teaches Vieta`

Allowed sequence:

1. ALG-03 canonical Vieta interface frozen;
2. downstream topic references that interface;
3. downstream prose gives only a short retrieval cue;
4. learner is routed to ALG-03 for reconstruction if diagnostic shows the prerequisite is missing.

The same rule applies to the named coverage bridges: NT-03 retrieves Euclid's Lemma from NT-01; downstream modular applications retrieve Euler/Fermat legality from NT-02.

## 11. Main-topic dependency checklist

Before Wave 0 closes, answer:
- Which concepts are `REQUIRES` prerequisites?
- Which are only `BRIDGE_REQUIRES`?
- Which overlap concepts have another canonical owner?
- Which generic proof modes should be retrieved from `IOQM_G9_Proof_Strategy_Toolkit_v1.md`?
- Could a Grade-9 learner enter this topic with the stated prerequisites?
- Does any planned section use a concept whose canonical teaching appears later?
- Are any two parallel microstreams mutually dependent?
- Can the dependency be reduced by teaching a small bridge rather than importing a whole higher-grade chapter?

Any unresolved prerequisite inversion blocks integrated prose.

## Change-control rule

The dependency graph is frozen for v1 production. A new hard dependency must be recorded explicitly with its effect on production wave, overlap ownership and issue registry. The issue-#132 coverage hardening adds named content within existing ownership and does not alter the production wave graph. Do not silently serialize the program.