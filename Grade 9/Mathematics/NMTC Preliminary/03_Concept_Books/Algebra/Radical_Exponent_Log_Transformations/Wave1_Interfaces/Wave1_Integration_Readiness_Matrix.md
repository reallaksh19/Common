# Issue #45 — Wave 1 Integration Readiness Matrix

`STATUS: WAVE1_INTERNAL_STREAMS_COMPLETE`

`NEXT_ALLOWED_WAVE: WAVE2_INTEGRATED_ASSIMILATION_BOOK`

This file audits the six Wave-1 interfaces against Issue #45 before any integrated teaching prose is authored.

## 1. Interface inventory

| Stream | Interface | Main missing bridge | Status |
|---|---|---|---|
| W1-A | Common radical basis & surd structure | choose radical basis / reconstruct hidden power / principal-root sign | PASS |
| W1-B | Exponent normalization | normalize representation before taking logs; preserve positivity | PASS |
| W1-C | Reversible vs non-reversible transformations | distinguish `<=>` from `=>`; preserve zero/domain cases | PASS |
| W1-D | Reciprocal invariants | preserve symmetry; do not solve hidden variable unnecessarily | PASS |
| W1-E | Logarithms as exponents | derive log structure from exponent meaning; exact inverse before decimals | PASS |
| W1-F | Log-to-algebra + domain/source QC | choose repeated object; map back through domain; preserve source conflicts | PASS |

## 2. Required 15-field contract audit

Every stream was checked for the Wave-0 interface fields:

1. `CONCEPTS` — PASS 6/6
2. `PREREQUISITES` — PASS 6/6
3. `RECOGNITION_CUES` — PASS 6/6
4. `FIRST_MOVES` — PASS 6/6
5. `INVARIANTS` — PASS 6/6
6. `REPRESENTATION_SWITCHES` — PASS 6/6
7. `REVERSIBILITY_OR_DOMAIN_CONDITIONS` — PASS 6/6
8. `DECISION_BOUNDARIES` — PASS 6/6
9. `MISCONCEPTION_TRAPS` — PASS 6/6
10. `CONTRAST_PAIRS` — PASS 6/6
11. `TRANSFER_MECHANISMS` — PASS 6/6
12. `SOURCE_IDS_AND_DISPOSITIONS` — PASS 6/6
13. `CANDIDATE_MASTERY_ITEMS` — PASS 6/6
14. `DIAGNOSTIC_TAGS` — PASS 6/6
15. `H3_TO_H0_FADE_PLAN` — PASS 6/6

No stream is formula/exercise-only.

## 3. Cross-stream dependency and handoff graph

```text
W1-A RADICAL REPRESENTATION -------------------+
   |                                           |
   +--> fractional exponents -----------------+--> W1-B EXPONENT NORMALIZATION
   |                                           |        |
   |                                           |        v
   +--> principal-root sign -------------------+--> W1-C REVERSIBILITY / DOMAIN
                                                        |
W1-D RECIPROCAL INVARIANTS <---- structural algebra ---+
   |                                                    |
   +--> avoid explicit solve                             |
                                                        v
W1-E LOGS AS EXPONENTS <----------- exponent meaning ---+
   |                                                    |
   +--> inverse / injective structure                    |
   v                                                    |
W1-F LOG -> ALGEBRA / DOMAIN / SOURCE QC <--------------+
```

Wave 2 must **interleave** W1-C rather than teach it only after the other streams. Reversibility/domain is a checking spine that appears at each representation switch.

## 4. Proposed Wave-2 teaching integration order

This is an integration recommendation, not student prose:

1. **RECONNECT — one object, many languages**: radical/power/log examples showing representation equivalence.
2. **A — radical common language**: common basis -> hidden powers -> principal root.
3. **B — exponent common language**: exponent meaning -> normalization -> repeated power.
4. **C checkpoint 1 — what transformations preserve solutions?**: square/cube, domain ledger, zero-factor boundary.
5. **D — invariant instead of explicit solving**: reciprocal symmetry and recurrence.
6. **E — logarithm is exponent language reversed**: definition -> derive laws -> inverse exactness.
7. **F — choose repeated log object and convert back to algebra**: substitution -> domain -> source QC.
8. **C checkpoint 2 — mixed arrow lab**: learner labels `<=>` or `=>` across radical/exponent/log transformations.
9. **ADOPT mixed unlabelled selection**: no stream labels.
10. **TRANSFER**: surface changes, method competition, source/domain traps.

## 5. Decision-boundary preservation matrix

Wave 2 must preserve at least these boundaries explicitly:

| Boundary | Owning stream(s) |
|---|---|
| product radical vs false sum distribution | A |
| principal root vs roots of a square equation | A + C |
| common basis vs hidden-square reconstruction | A |
| rationalize vs structure first | A |
| negative exponent vs negative base | B |
| multiplication exponent law vs false addition law | B |
| common-base normalization vs unnecessary logs | B + E |
| squaring vs cubing | C |
| divide by nonzero constant vs zero-capable variable factor | C |
| transformed candidate vs original solution | C + F |
| symmetric reciprocal target vs asymmetric target | D |
| invariant reduction vs explicit solving | D |
| log product law vs nonexistent sum law | E |
| exact inverse simplification vs decimal approximation | E |
| `t=log_b x` vs `u=sqrt(log_b x)` | F |
| valid same-base log equality vs undefined argument | E + F |
| learner error vs source conflict | F + source-QC spine |

This exceeds Issue #45's minimum six contrast pairs, but Wave 2 should select a coherent subset rather than display a catalogue mechanically.

## 6. Source-custody integration

### CLEAN_SCORED_ANCHOR — 16 unique IDs

- `NMTC-BH-P-2018-Q01`
- `NMTC-BH-P-2018-Q21`
- `NMTC-BH-P-2018-Q26`
- `NMTC-BH-P-2023-Q07`
- `NMTC-BH-P-2023-Q21`
- `NMTC-BH-P-2023-Q26`
- `NMTC-BH-P-2024-Q04`
- `NMTC-BH-P-2024-Q09`
- `NMTC-BH-P-2024-Q12`
- `NMTC-BH-P-2024-Q26`
- `NMTC-BH-P-2024-Q28`
- `NMTC-BH-P-2025-Q03`
- `NMTC-BH-P-2025-Q04`
- `NMTC-BH-P-2025-Q09`
- `NMTC-BH-P-2025-Q12`
- `NMTC-BH-P-2025-Q27`

### SOURCE_SENSITIVE_EVIDENCE

- `NMTC-BH-P-2023-Q04` — bridge only; notation/options sensitive.
- `NMTC-BH-P-2023-Q20` — bridge only; exact notation delicate.

### SOURCE_CONFLICT_EVIDENCE

- `NMTC-BH-P-2025-Q18` — source/convention QC only; no silent repair.

### BONUS_EVIDENCE

None identified for this topic in the current source coverage map. No bonus recurrence is inferred.

### AUTHOR_CREATED material

Foundations/transfer items remain explicitly author-created and receive no fake year/question attribution.

## 7. Candidate mastery inventory

Wave-1 interfaces propose **28 candidate items** for later selection/rewrite:

- W1-A: 4
- W1-B: 5
- W1-C: 5
- W1-D: 4
- W1-E: 5
- W1-F: 5

These are a design pool, not the final Wave-4 bank. Wave 4 must still meet Issue #45's independent unlabelled totals and avoid over-reusing identical surfaces.

## 8. Independent mathematics audit of Wave-1 candidate items

| ID | Expected result / conclusion | Independent verification route | Status |
|---|---|---|---|
| A-M1 | `4` | radical reduction | PASS |
| A-M2 | `sqrt(10)-3` | re-square + sign | PASS |
| A-M3 | `|2x-5|`; equals `2x-5` iff `x>=5/2` | principal-root definition | PASS |
| A-M4 | `sqrt7` | combine conjugate fractions independently | PASS |
| B-M1 | `9` | common-base power | PASS |
| B-M2 | `x=3` | normalize to base 2 | PASS |
| B-M3 | `x=1, log_3 4` | solve in `t=3^x>0` | PASS |
| B-M4 | `x=0, log_(3/2)4` | ratio variable and back-map | PASS |
| B-M5 | false exponent addition over sums | numerical falsifier `2+4 != 8` | PASS |
| C-M1 | `x=3` | squared candidates + original check | PASS |
| C-M2 | `x=2,-2` | factor without dividing | PASS |
| C-M3 | arrows `=>, <=>, =>` | injectivity/counterexample check | PASS |
| C-M4 | squaring equivalent after `x>=1` | both sides nonnegative | PASS |
| C-M5 | count original distinct solutions; preserve conflict if key disagrees | source/equivalence logic | PASS |
| D-M1 | `110` | cubic reciprocal identity | PASS |
| D-M2 | `123` | recurrence recomputation from `S0=2,S1=3` | PASS |
| D-M3 | `1,(3±sqrt5)/2` | factor quartic as `(x-1)^2(x^2-3x+1)` | PASS |
| D-M4 | `±8sqrt3`; not unique | derive `x-1/x=±sqrt12` | PASS |
| E-M1 | `5^3=125` | log definition | PASS |
| E-M2 | `x=11` | exponent conversion + domain | PASS |
| E-M3 | `25` | exact inverse rewrite | PASS |
| E-M4 | false sum law | numerical counterexample | PASS |
| E-M5 | `x=2` | common-base normalization | PASS |
| F-M1 | `x=4,8` | quadratic in `log_2 x` | PASS |
| F-M2 | `x=16,512` | quadratic in `sqrt(log_2 x)` + range | PASS |
| F-M3 | `x+y=12` | `x=y^2`, positivity filter | PASS |
| F-M4 | `x=5` | algebraic roots `5,-1`, domain `x>3` | PASS |
| F-M5 | reject invalid key branch; preserve source conflict as warranted | original-domain/source-custody rule | PASS |

`WAVE1_CANDIDATE_MATH_AUDIT: 28/28 PASS`

## 9. Hint-fading consistency

All six interfaces enforce:

1. first exposure to each practice item is **H0 attempt**;
2. if rescue is necessary, H3/H2/H1 may be exposed;
3. across adjacent practice, the maximum available support fades `H3 -> H2 -> H1 -> H0`;
4. H3 gives the first algebraic relation only, not a completed solution.

`ATTEMPT_BEFORE_HINT: PASS`

`H3_TO_H0_INTERFACE_PLAN: PASS`

## 10. Wave-1 gate table

| Gate | Status | Note |
|---|---|---|
| six streams created inside Issue #45 | PASS | no subtopic issues created |
| compact interface contract complete | PASS | 15/15 fields in all six streams |
| prerequisites explicit | PASS | 6/6 |
| recognition cues + first moves | PASS | 6/6 |
| decision boundaries | PASS | 6/6 |
| misconception traps + contrast pairs | PASS | 6/6 |
| reversibility/domain custody | PASS | 6/6, cross-stream spine |
| source IDs/dispositions preserved | PASS | clean/sensitive/conflict separated |
| bonus evidence not inflated | PASS | none identified/invented |
| candidate mastery pool | PASS | 28 candidates |
| independent candidate-answer recheck | PASS | 28/28 |
| attempt-before-hint | PASS | built into each fade plan |
| H3->H0 fading design | PASS | 6/6 |
| Wave-2 integrated student prose | NOT_RUN | next wave |
| First-Step Reference rebuild | NOT_RUN | Wave 3 only, after teaching |
| final mastery bank | NOT_RUN | Wave 4 |
| PDF/render QA | NOT_RUN | Wave 5 |
| classroom timing/readability | NOT_RUN | requires observation |
| longitudinal retention/transfer | NOT_RUN | requires evidence |

## 11. Completion state

`WAVE1_INTERNAL_STREAMS_COMPLETE`

The interfaces are integration-ready. They are **not** themselves a student book and must not be concatenated mechanically. Wave 2 must turn them into a coherent learning journey with discovery, explanation, attempts, diagnosis, fading and unlabelled adoption.
