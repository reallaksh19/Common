# IOQM Grade 9 — Taxonomy Reconciliation v1

Status: `TAXONOMY_PRIMARY_OWNERSHIP_RECONCILED__ANSWER_RECOMPUTATION_NOT_RUN`

## 1. Why this pass exists

The architecture phase used a deliberately rough mechanism survey. This file records the item-level second pass over all 90 validated 2023–2025 questions and freezes **primary ownership for counting**, while retaining secondary/bridge tags for pedagogy.

A question may be cross-domain. Primary ownership is not a claim that the other mathematics disappears; it is a denominator-control rule that prevents double inflation.

## 2. Reconciled three-paper primary-domain signal

| Domain | Count / 90 |
|---|---:|
| Number Theory | 24 |
| Algebra | 18 |
| Geometry | 25 |
| Combinatorics | 23 |

The earlier rough survey should therefore be treated as superseded by this item-level ledger.

These counts are **not official IOQM weightage** and must not be translated into chapter percentages.

## 3. Topic-level signal

- `IOQM-G9-GEO-01` — Triangle Metric / Feasibility / Cevians: **8/90** primary items.
- `IOQM-G9-NT-03` — Prime Factorisation / Divisors / Perfect Powers: **8/90** primary items.
- `IOQM-G9-NT-04` — Diophantine Equations / Integer Restrictions: **7/90** primary items.
- `IOQM-G9-COMB-01` — Basic Counting / Restrictions / Inclusion–Exclusion: **7/90** primary items.
- `IOQM-G9-COMB-02` — Graphs / Colouring / Incidence: **6/90** primary items.
- `IOQM-G9-GEO-05` — Coordinate / Vector / Mensuration: **5/90** primary items.
- `IOQM-G9-GEO-02` — Angles / Lines / Quadrilaterals / Polygons: **5/90** primary items.
- `IOQM-G9-GEO-04` — Circles / Cyclicity / Tangency: **5/90** primary items.
- `IOQM-G9-COMB-03` — Recurrence / Tilings / State Evolution: **5/90** primary items.
- `IOQM-G9-ALG-01` — Identities / Transformations / Equation Structure: **4/90** primary items.
- `IOQM-G9-NT-05` — Digits / Place Value / Bases: **4/90** primary items.
- `IOQM-G9-ALG-03` — Polynomials / Roots / Vieta / Remainders: **4/90** primary items.
- `IOQM-G9-NT-02` — Modular Arithmetic / Residues / Power Cycles: **3/90** primary items.
- `IOQM-G9-COMB-04` — Games / Invariants: **3/90** primary items.
- `IOQM-G9-NT-01` — Divisibility / GCD / LCM: **2/90** primary items.
- `IOQM-G9-ALG-02` — Inequalities / Bounds / Equality: **2/90** primary items.
- `IOQM-G9-ALG-05` — Functional Equations: **2/90** primary items.
- `IOQM-G9-ALG-04` — Sequences / Progressions / Recurrences: **2/90** primary items.
- `IOQM-G9-ALG-06` — Exponents / Radicals / Logs: **2/90** primary items.
- `IOQM-G9-GEO-03` — Similarity / Ratio / Area / Centroid: **2/90** primary items.
- `IOQM-G9-ALG-07` — Floor / Ceiling / Discrete Functions: **2/90** primary items.
- `IOQM-G9-COMB-05` — Pigeonhole / Extremal Reasoning: **2/90** primary items.

## 4. Canonical overlap-owner decisions

The following rules apply when a production topic consumes cross-domain questions.

| Overlap | Canonical primary owner rule | Bridge role |
|---|---|---|
| integer geometry | Geometry owns when geometric feasibility/metric relation is the decisive structure | NT-04 receives integer/factor filtering as a bridge |
| digit counting | COMB-01 owns when the main task is counting admissible digit strings; NT-05 owns when place value/divisibility/carry structure is decisive | cross-tag the other |
| polynomial + recurrence | ALG-03 owns when quotient/coefficient algebra is the decisive object; COMB-03 owns when state evolution/count recurrence is the decisive representation | cross-tag |
| inequalities in geometry | geometry owns if the bound is used to establish a geometric feasibility/metric fact; ALG-02 owns if the central learning target is bound/equality/attainment | cross-tag |
| Vieta in geometry | geometry owns if triangle/circle reconstruction is prerequisite and Vieta only packages symmetric data | ALG-03 is bridge |
| modular digit problems | NT-05 owns if decimal/place-value structure is primary; NT-02 owns if residue cycle/congruence is primary | cross-tag |
| state search vs games | COMB-03 owns deterministic shortest-path/state-evolution questions; COMB-04 owns adversarial optimal-play/invariant games | cross-tag where useful |
| extremal geometry/combinatorics | COMB-05 owns when an extremal counting/selection principle is decisive; geometry owns when metric/incidence geometry is the decisive feasibility structure | cross-tag |

## 5. Medium-confidence review set

`MEDIUM` does not mean the source is uncertain. It means **primary pedagogical ownership is genuinely cross-domain or the shortest solution route can vary**.

- `IOQM-G9-NT-01`: IOQM-2025-Q27
- `IOQM-G9-NT-03`: IOQM-2024-Q28
- `IOQM-G9-NT-04`: IOQM-2023-Q04, IOQM-2023-Q11, IOQM-2023-Q29
- `IOQM-G9-NT-05`: IOQM-2025-Q12, IOQM-2023-Q19
- `IOQM-G9-ALG-01`: IOQM-2025-Q21, IOQM-2024-Q05, IOQM-2024-Q11
- `IOQM-G9-ALG-03`: IOQM-2024-Q24
- `IOQM-G9-ALG-04`: IOQM-2023-Q10
- `IOQM-G9-ALG-06`: IOQM-2025-Q28
- `IOQM-G9-GEO-01`: IOQM-2024-Q10, IOQM-2024-Q22, IOQM-2024-Q27, IOQM-2024-Q30, IOQM-2023-Q13
- `IOQM-G9-GEO-02`: IOQM-2025-Q13, IOQM-2023-Q24, IOQM-2023-Q25
- `IOQM-G9-GEO-04`: IOQM-2025-Q19, IOQM-2025-Q23, IOQM-2025-Q30, IOQM-2024-Q17, IOQM-2023-Q15
- `IOQM-G9-GEO-05`: IOQM-2025-Q17, IOQM-2023-Q23
- `IOQM-G9-COMB-01`: IOQM-2023-Q07, IOQM-2023-Q17
- `IOQM-G9-COMB-02`: IOQM-2025-Q29, IOQM-2023-Q16, IOQM-2023-Q22
- `IOQM-G9-COMB-03`: IOQM-2024-Q14, IOQM-2024-Q20, IOQM-2023-Q21
- `IOQM-G9-COMB-04`: IOQM-2025-Q22, IOQM-2025-Q25, IOQM-2023-Q28
- `IOQM-G9-COMB-05`: IOQM-2023-Q18, IOQM-2023-Q27

Total medium-confidence ownership records: **41**.
High-confidence ownership records: **49**.

No quantitative micro-mechanism recurrence should be frozen until the medium-confidence set has been independently reviewed against worked solutions or a second expert route.

## 6. What is now frozen

- 90 unique stable IDs;
- official/validated paper and key custody;
- one primary domain per item;
- one primary main-topic ID per item;
- secondary-domain bridge tags;
- first-pass visible clue, invariant and first-move metadata;
- source-integrity events known from the official/final keys;
- no double counting in main-topic recurrence.

## 7. What remains NOT_RUN

- independent recomputation of all 90 official answers;
- solution-route verification for all medium-confidence ownership items;
- calibrated difficulty scores;
- classroom timing/readability;
- longitudinal transfer/retention;
- any probability of qualification.

## 8. Promotion rule

A main-topic production issue may use this ledger for **source coverage and candidate anchor selection**, but any historical answer promoted into a worked teaching solution must first set `answer_verified_independently=true` for that item.
