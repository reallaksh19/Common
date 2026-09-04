# IOQM Grade 9 — Taxonomy Reconciliation v1

Status: `TAXONOMY_PRIMARY_OWNERSHIP_RECONCILED__ANSWER_VERIFICATION_PASS_90_OF_90`

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

The earlier rough survey is superseded by this item-level ledger.

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
| integer geometry | Geometry owns when geometric feasibility/metric relation is decisive | NT-04 receives integer/factor filtering as a bridge |
| digit counting | COMB-01 owns when the main task is counting admissible digit strings; NT-05 owns when place value/divisibility/carry structure is decisive | cross-tag the other |
| polynomial + recurrence | ALG-03 owns quotient/coefficient algebra; COMB-03 owns state-evolution/count recurrence | cross-tag |
| inequalities in geometry | geometry owns if the bound establishes geometric feasibility/metric fact; ALG-02 owns if bound/equality/attainment is the learning target | cross-tag |
| Vieta in geometry | geometry may own the historical problem if geometry reconstructs the quantities and Vieta only packages symmetric data | ALG-03 remains canonical Vieta teacher |
| modular digit problems | NT-05 owns decimal/place-value structure; NT-02 owns residue-cycle/congruence structure | cross-tag |
| state search vs games | COMB-03 owns deterministic state evolution; COMB-04 owns adversarial optimal-play/invariant games | cross-tag where useful |
| extremal geometry/combinatorics | COMB-05 owns when extremal selection is decisive; geometry owns metric/incidence feasibility | cross-tag |

The production-wide detailed ownership matrix is now frozen at `02_Production/IOQM_G9_Canonical_Overlap_Ownership_v1.md`.

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

No fine-grained micro-mechanism recurrence should be frozen solely from these ownership labels. Topic leads may conduct a second-route review and propose an ownership change through explicit change control.

## 6. What is now frozen

- 90 unique stable IDs;
- official/validated paper and key custody;
- independent answer verification 90/90 with zero key mismatches;
- one primary domain per item;
- one primary main-topic ID per item;
- secondary-domain bridge tags;
- first-pass visible clue, invariant and first-move metadata;
- source-integrity events known from official/final keys;
- no double counting in main-topic recurrence;
- 22 main-topic production issues and dependency waves;
- canonical overlap-owner rules for production.

## 7. What remains NOT_RUN / open evidence

- second-route ownership review for medium-confidence items where a topic lead challenges current ownership;
- calibrated difficulty scores;
- classroom timing/readability;
- longitudinal transfer/retention;
- psychometric discrimination;
- any probability of qualification.

Answer recomputation is **no longer NOT_RUN**: all 90 validated answers have been independently recomputed and agree with key authority.

## 8. Promotion rule

A main-topic production issue may use this ledger for source coverage, candidate anchor selection and answer-level historical teaching authority, provided:

1. exact source wording/figures are read from the validated paper;
2. `IOQM-2023-Q04` and `IOQM-2025-Q28` obey the metadata-correction overlay;
3. borrowed mechanisms obey canonical overlap ownership;
4. no topic-frequency claim is presented as official IOQM weightage.

Production issues are registered in `02_Production/IOQM_G9_Main_Topic_Issue_Registry_v1.md`.