# Issue #45 — Wave 1 Integration Readiness Matrix

`STATUS: WAVE1_INTERNAL_STREAMS_COMPLETE`

`CURRENT_PROGRAM_STATE: WAVE3_FIRST_STEP_REFERENCE_COMPLETE`

`NEXT_ALLOWED_WAVE: WAVE4_MIXED_MASTERY_AND_TRANSFER`

This file audits the six Wave-1 interfaces against Issue #45 before any integrated teaching prose is authored. Wave 1 remains frozen as the integration contract; later waves do not rewrite its source dispositions or interface decisions.

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

Wave 2 interleaves W1-C rather than teaching it only after the other streams. Reversibility/domain is a checking spine that appears at each representation switch.

## 4. Integration status

- Wave 2 integrated Assimilation Book: PASS.
- Wave 3 First-Step Reference: PASS.
- Wave 4 mixed mastery/transfer: NOT_RUN.
- Wave 5 PDF/render QA: NOT_RUN.

Wave 3 is a compression layer derived from Wave 2; it does not alter this Wave-1 contract.

## 5. Decision-boundary preservation matrix

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

These are a design pool, not the final Wave-4 bank.

## 8. Independent mathematics audit of Wave-1 candidate items

`WAVE1_CANDIDATE_MATH_AUDIT: 28/28 PASS`

The detailed 28-item audit was completed before Wave 2 integration. No later wave changes those results.

## 9. Hint-fading consistency

All six interfaces enforce:

1. first exposure to each practice item is **H0 attempt**;
2. if rescue is necessary, H3/H2/H1 may be exposed;
3. across adjacent practice, the maximum available support fades `H3 -> H2 -> H1 -> H0`;
4. H3 gives the first algebraic relation only, not a completed solution.

`ATTEMPT_BEFORE_HINT: PASS`

`H3_TO_H0_INTERFACE_PLAN: PASS`

## 10. Frozen Wave-1 gate table

| Gate | Status |
|---|---|
| six streams created inside Issue #45 | PASS |
| compact interface contract complete | PASS |
| source IDs/dispositions preserved | PASS |
| bonus evidence not inflated | PASS |
| candidate mastery pool | PASS — 28 |
| independent candidate-answer recheck | PASS — 28/28 |
| attempt-before-hint | PASS |
| H3->H0 fading design | PASS |
| Wave 2 integrated student prose | PASS |
| Wave 3 First-Step Reference | PASS |
| Wave 4 final mastery bank | NOT_RUN |
| Wave 5 PDF/render QA | NOT_RUN |
| classroom timing/readability | NOT_RUN |
| longitudinal retention/transfer | NOT_RUN |

`WAVE1_INTERNAL_STREAMS_COMPLETE`
