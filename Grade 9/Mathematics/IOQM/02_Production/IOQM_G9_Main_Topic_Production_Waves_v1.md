# IOQM Grade 9 — Main-Topic Production Waves v1

Status: `FROZEN_FOR_ISSUE_CREATION`

Purpose: schedule main-topic production without repeating the Quadratics failure mode. Dependency controls **interfaces**, not unnecessary global serialization.

## Governing rule

`ONE MAIN TOPIC = ONE PEDAGOGICAL OWNER = ONE INTEGRATED STUDENT BOOK`

Parallel work is allowed at two levels:

1. multiple **main topics** may run in parallel when prerequisite interfaces are frozen;
2. multiple **microstreams** may run in parallel inside one topic, but they emit structured research/verification interfaces, not standalone canonical student chapters.

A downstream topic does **not** wait for an upstream final PDF when a stable prerequisite interface is sufficient.

## Common Wave 0 — program foundation

Before any topic lead writes integrated prose, inherit:

- `F0 G9_CORE`: integer/rational arithmetic, ratio, exponent basics, linear equations, expansion/factorisation, coordinate basics, elementary Euclidean geometry;
- `F1 IOQM_BRIDGE`: implication/equivalence, counterexample, domain restrictions, parity/divisibility language, finite-case completeness, exact reasoning, check discipline;
- 90-question corpus and verification authority;
- canonical overlap-owner matrix;
- partial-knowledge learner model;
- `RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`.

## Production Wave 1 — canonical primitives

These topics may run **in parallel immediately** after common Wave 0.

| Topic | Why Wave 1 | Interface exported downstream |
|---|---|---|
| `IOQM-G9-NT-01` Divisibility/GCD/LCM | canonical NT structural base | divisibility, gcd/lcm, Euclidean and same-remainder interface |
| `IOQM-G9-ALG-01` Identities/Transformations | canonical algebra manipulation base | factor/substitute/equivalence/reversibility interface |
| `IOQM-G9-ALG-04` Sequences/Progressions/Recurrences | can start from G9 algebra | sequence notation, term/sum, recurrence interface |
| `IOQM-G9-ALG-07` Floor/Ceiling/Discrete Functions | can start from order/integer core | floor/ceiling interval and discrete-filter interface |
| `IOQM-G9-GEO-02` Angles/Lines/Quadrilaterals/Polygons | canonical angle/polygon base | angle chase/cyclic-precondition interface |
| `IOQM-G9-GEO-03` Similarity/Ratio/Area/Centroid | canonical ratio/area base | similarity/ratio/centroid interface |
| `IOQM-G9-GEO-05` Coordinate/Vector/Mensuration | alternate-representation base | coordinate/vector representation interface |
| `IOQM-G9-COMB-01` Basic Counting/Restrictions/IE | canonical counting base | object-definition, addition/multiplication, complement/IE interface |
| `IOQM-G9-COMB-05` Pigeonhole/Extremal | needs proof/model habits, not advanced P&C | pigeonhole/extremal-choice interface |

### Wave-1 completion gate

A Wave-1 topic exports a **stable prerequisite interface** before downstream prose starts. It does not need final classroom calibration or publication approval.

## Production Wave 2 — first downstream layer

May start once the named upstream interfaces are frozen.

| Topic | Required interface(s) | Notes |
|---|---|---|
| `IOQM-G9-NT-02` Modular Arithmetic/Residues/Cycles | NT-01 | do not reteach gcd/divisibility canonically |
| `IOQM-G9-NT-03` Prime Factorisation/Divisors/Perfect Powers | NT-01 | valuation/divisor structure owner |
| `IOQM-G9-ALG-02` Inequalities/Bounds/Equality | ALG-01 | canonical AM-GM/equality/attainment owner |
| `IOQM-G9-ALG-03` Polynomials/Roots/Vieta/Remainders | ALG-01 | canonical Vieta/discriminant/polynomial-reduction owner |
| `IOQM-G9-ALG-05` Functional Equations | ALG-01 bridge | use strategic substitution; avoid abstract theory inflation |
| `IOQM-G9-ALG-06` Exponents/Radicals/Logs | ALG-01 | canonical reversible-transform/domain owner for this family |
| `IOQM-G9-GEO-01` Triangle Feasibility/Metric/Cevians | GEO-03; G9 angle core | may use GEO-05 as alternate representation, not prerequisite teaching |
| `IOQM-G9-GEO-04` Circles/Cyclicity/Tangency | GEO-02 | canonical circle/tangent owner |
| `IOQM-G9-COMB-02` Graphs/Colouring/Incidence | COMB-01 | graph model and incidence owner |
| `IOQM-G9-COMB-03` Recurrence/Tilings/State | COMB-01; ALG-04 bridge | counting-state recurrence, not canonical algebra-sequence teaching |

## Production Wave 3 — composite/cross-domain layer

May start after prerequisite interfaces below are stable.

| Topic | Required interface(s) | Notes |
|---|---|---|
| `IOQM-G9-NT-04` Diophantine/Integer Restrictions | NT-03 + ALG-01; ALG-03 bridge when quadratic feasibility is used | canonical integer-reconstruction/filter owner |
| `IOQM-G9-NT-05` Digits/Place Value/Bases | NT-02 for advanced residue/cycle applications | basic place value may reconnect from G9 core |
| `IOQM-G9-COMB-04` Games/Invariants | NT-01/NT-02 bridge + F1 proof habits | canonical adversarial game/invariant owner |

## Parallelism rule

Within each production wave, topics are parallel unless an issue discovers a new hard dependency. New dependencies must be recorded as an interface edge; do not silently serialize the whole program.

## Canonical teaching vs retrieval

Downstream material may use a prerequisite in three ways:

- **RETRIEVE** — one-line recall/check;
- **BRIDGE** — minimal just-in-time explanation;
- **ROUTE BACK** — if diagnostic shows the prerequisite is missing, send the learner to the canonical owner.

It may not create a second independent canonical derivation merely to make its own booklet self-contained.

## Production sequence inside every main-topic issue

```text
Wave 0  Grounding + concept/dependency/source map
Wave 1  Parallel microstream research/verification interfaces
Wave 2  One lead-authored integrated Assimilation Book
Wave 3  One topic-wide First-Step Reference
Wave 4  Recognition + first-line + mixed H0 mastery + transfer
Wave 5  Independent mathematics/source/pedagogy audit
Wave 6  One production/render authority + page-by-page QA
```

## Evidence gates not implied by these waves

The wave schedule does not manufacture:

- classroom timing/readability;
- longitudinal retention;
- psychometric item difficulty/discrimination;
- qualification probability;
- official IOQM topic weightage.

Those remain separate evidence states.

## Current program state

`PRODUCTION_WAVES_FROZEN__ISSUE_CREATION_READY`