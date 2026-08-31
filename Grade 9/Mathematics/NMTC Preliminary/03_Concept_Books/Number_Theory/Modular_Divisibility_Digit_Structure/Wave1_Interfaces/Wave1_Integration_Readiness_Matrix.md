# Issue #47 — Wave 1 Integration Readiness Matrix

`STATUS: WAVE1_SEVEN_STREAM_INTERFACES_PASS`

This matrix is the handoff gate from Wave 1 interfaces to Wave 2 teaching integration. It does **not** authorize student prose before all interface/source-custody checks below pass.

## 1. Interface inventory

| Stream | File | Gate |
|---|---|---|
| W1-A | `W1-A_Congruence_Meaning_Operations_Interface.md` | PASS |
| W1-B | `W1-B_Power_Cycles_Multiplicative_Order_Interface.md` | PASS |
| W1-C | `W1-C_Same_Remainder_Structure_Interface.md` | PASS |
| W1-D | `W1-D_Simultaneous_Congruences_Interface.md` | PASS_WITH_SOURCE_CUSTODY_CORRECTION |
| W1-E | `W1-E_Place_Value_Digit_Divisibility_Interface.md` | PASS |
| W1-F | `W1-F_Factor_Pair_Divisor_Structure_Interface.md` | PASS |
| W1-G | `W1-G_Prefix_Residue_State_Reasoning_Interface.md` | PASS |

## 2. Frozen 16-field contract

Every stream contains all required fields:

1. `CONCEPTS`
2. `PREREQUISITES`
3. `LIKELY_HALF_KNOWLEDGE`
4. `RECOGNITION_CUES`
5. `FIRST_MOVES`
6. `INVARIANTS`
7. `REPRESENTATION_SWITCHES`
8. `LEGALITY / ADMISSIBILITY CONDITIONS`
9. `DECISION_BOUNDARIES`
10. `MISCONCEPTION_TRAPS`
11. `CONTRAST_PAIRS`
12. `TRANSFER_MECHANISMS`
13. `SOURCE_IDS_AND_DISPOSITIONS`
14. `CANDIDATE_MASTERY_ITEMS`
15. `DIAGNOSTIC_TAGS`
16. `H3_TO_H0_FADE_PLAN`

| Stream | 16/16 fields |
|---|---|
| A | PASS |
| B | PASS |
| C | PASS |
| D | PASS |
| E | PASS |
| F | PASS |
| G | PASS |

`INTERFACE_SCHEMA: 16/16 IN 7/7 — PASS`

## 3. Cross-stream spines

| Spine | A | B | C | D | E | F | G | Gate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| representation choice | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| legality/admissibility | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| decision boundary | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| explicit misconception | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| first-move independence | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| non-identical transfer plan | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| source custody | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |
| H3→H0 fade plan | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | PASS |

## 4. Major decision boundaries frozen before prose

Wave 2 must preserve these as close contrasts, not collapse them into formula notes:

1. congruence vs equality;
2. safe modular reduction vs illegal cancellation;
3. reduce base modulo `m` vs reduce exponent modulo the **cycle length**;
4. cycle-position remainder zero vs first cycle entry;
5. same-number/many-divisors -> LCM vs same-divisor/many-numbers -> GCD of differences;
6. compatible vs incompatible non-coprime congruences;
7. simultaneous remainders on one original number vs successive quotient/remainder chain;
8. place-value algebra vs verbal digit guessing;
9. ordered vs unordered digit choices;
10. digit identity vs residue-class identity (`0` vs `9` modulo 9);
11. divisor reduction vs integer trial;
12. factor pair vs **admissible** factor pair (parity/sign/bounds);
13. coprime perfect-power product vs arbitrary product;
14. direct block enumeration vs prefix-residue state;
15. residue-class frequency vs pair count;
16. core cycle/state reasoning vs multiplicative-order/canonical-representation ceiling work.

`DECISION_BOUNDARY_COVERAGE: PASS_STRONG`

## 5. Candidate mastery inventory

Each stream contributes 5 candidate prompts:

- A: 5
- B: 5
- C: 5
- D: 5
- E: 5
- F: 5
- G: 5

Total: **35** candidate prompts.

All 35 were independently checked after authoring for arithmetic, residue classes, admissibility or source-QC conclusion.

Representative independent rechecks:

- `2x≡2 (mod6)` -> `x≡1,4 (mod6)`;
- `5x≡10 (mod12)` -> `x≡2 (mod12)`;
- `7^222` last digit -> 9;
- `3^100 mod7` -> 4;
- largest `<5000` with remainder 7 modulo 12,18,30 -> 4867;
- equal-remainder divisor for 84,129,174 -> 45;
- `x≡1 (mod4), x≡2 (mod6)` -> incompatible;
- `x≡1 (mod4), x≡3 (mod6)` -> `x≡9 (mod12)`;
- `x≡2 (mod3),3 (mod5),2 (mod7)` -> `x≡23 (mod105)`;
- two-digit numbers with digit sum divisible by 9 -> 10;
- `k²-n²=96` positive `k>n` -> 4 admissible pairs;
- prefix residues for `2,5,4,7` modulo 3 -> 2 divisible consecutive blocks;
- residue list `0,2,0,3,2,0` -> 4 equal-residue index pairs.

`CANDIDATE_MASTERY_AUDIT: 35/35 PASS`

## 6. Source custody — corrected current authority

### Clean scored core mechanism IDs — 16

- `NMTC-BH-P-2018-Q10`
- `NMTC-BH-P-2018-Q18`
- `NMTC-BH-P-2018-Q19`
- `NMTC-BH-P-2018-Q28`
- `NMTC-BH-P-2018-Q29`
- `NMTC-BH-P-2019-Q01`
- `NMTC-BH-P-2019-Q16`
- `NMTC-BH-P-2019-Q17`
- `NMTC-BH-P-2019-Q27`
- `NMTC-BH-P-2023-Q18`
- `NMTC-BH-P-2024-Q21`
- `NMTC-BH-P-2025-Q01`
- `NMTC-BH-P-2025-Q13`
- `NMTC-BH-P-2025-Q14`
- `NMTC-BH-P-2025-Q21`
- `NMTC-BH-P-2025-Q26`

### Clean scored ceiling / transfer bridges — 4

- `NMTC-BH-P-2019-Q06` — prefix residues;
- `NMTC-BH-P-2019-Q14` — attainability/congruence transfer;
- `NMTC-BH-P-2019-Q26` — multiplicative order ceiling;
- `NMTC-BH-P-2019-Q28` — canonical/balanced-ternary representation ceiling.

Total clean scored mechanism IDs: **20**.

### Blocked evidence

- `NMTC-BH-P-2023-Q12` -> `SOURCE_SENSITIVE_EVIDENCE — BLOCKED_EXACT_ANCHOR`;
- `NMTC-BH-P-2024-Q20` -> `SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`.

Q20 correction is recorded in `Wave1_Source_Custody_Correction_2024_Q20.md` and the corrected topic Source Coverage Map.

### Bonus

`BONUS_EVIDENCE_COUNT: 0`

### Author-created foundation required

Especially:
- illegal modular cancellation;
- compatible/incompatible non-coprime simultaneous congruences;
- full solution-class interpretation;
- cycle-zero indexing;
- leading-zero and ordered-digit boundaries;
- digit-state transitions;
- core-vs-ceiling method choice.

`SOURCE_CUSTODY: PASS_AFTER_Q20_DEMOTION`

## 7. Wave-2 integration requirements

Wave 2 must not simply concatenate seven mini-chapters. The integrated book must use one recurring compression question:

> **What information can the target see, and what smaller representation preserves exactly that information?**

Required teaching choreography:

`RECONNECT -> DISCOVER -> MAKE SENSE -> H0 TRY -> DIAGNOSE -> separate HINT BANK -> FADE -> ADOPT -> TRANSFER`

Hard requirements carried forward:

- student attempt surfaces physically separated from hints/answers;
- at least 7 close contrast pairs, with the flagship LCM-vs-GCD pair explicit;
- modular cancellation receives a concrete falsifier;
- power-cycle zero-index receives its own diagnosis;
- simultaneous congruence compatibility is taught with both compatible and impossible systems;
- Q20 is source-QC only, never a clean CRT example;
- digit counting includes order, leading-zero and residue-class traps;
- prefix/order/balanced-ternary ceiling material comes only after core residue competence;
- no historical source text is silently repaired or overclaimed.

## 8. Gate table

| Gate | Status |
|---|---|
| seven interfaces exist | PASS |
| 16/16 fields in 7/7 | PASS |
| half-knowledge explicit | PASS |
| representation spine explicit | PASS |
| legality/admissibility explicit | PASS |
| close contrasts explicit | PASS_STRONG |
| candidate mastery count | 35 |
| candidate audit | 35/35 PASS |
| H3→H0 plan in every stream | PASS |
| clean/source-sensitive/conflict custody | PASS_AFTER_Q20_DEMOTION |
| Q20 false CRT inheritance prevented | PASS |
| teaching prose authored | NOT_RUN — deliberately deferred to Wave 2 |
| classroom calibration | NOT_RUN |

`WAVE1_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE2_INTEGRATED_ASSIMILATION_BOOK`
